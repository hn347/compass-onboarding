#!/usr/bin/env python3
"""
astmap.py - deterministic symbol index for grounding.

Walks a repository and extracts, per file, the symbols it DEFINES (functions,
methods, classes, interfaces, enums) with their exact line ranges, using
tree-sitter. The output is a deterministic JSON map the onboarding agent reads
so that every claim it writes can be anchored to a real symbol at a real line,
instead of a guessed location. This is the "deterministic backbone" half of the
two-phase design (parser extracts facts, the model only does semantics).

By design this indexes DEFINITIONS, not a dependency / call graph. Imports are
captured only when --imports is passed, and even then no cross-file edges are
built. Keeping it to definitions gives the grounding value without the cost and
noise of a full dependency map.

Usage:
    python3 astmap.py <repo_root> [--out PATH] [--imports] [--json]

Behavior:
    - Honors .bobignore at the repo root (gitignore-style) plus a built-in
      skip list (.git, node_modules, build output, vendored deps).
    - Uses whichever tree-sitter language wheels are installed. Missing
      languages are skipped, not fatal. Install only what you need, e.g.:
          pip install tree_sitter tree_sitter_python tree_sitter_javascript \\
                      tree_sitter_typescript tree_sitter_go tree_sitter_java
    - If tree-sitter is unavailable entirely, falls back to Python's stdlib
      `ast` for .py files so the script still produces a (partial) map and
      never hard-fails. The chosen parser is recorded in the output.

Exit codes: 0 on success (even with a partial index). Non-zero only on a
usage error.
"""
import argparse, datetime, fnmatch, json, os, subprocess, sys

# extension -> tree-sitter language name
EXT_LANG = {
    ".py": "python",
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "tsx",
    ".go": "go", ".java": "java", ".rb": "ruby", ".rs": "rust",
    ".c": "c", ".h": "c", ".cc": "cpp", ".cpp": "cpp", ".cxx": "cpp", ".hpp": "cpp",
    ".cs": "c_sharp", ".php": "php", ".sh": "bash", ".bash": "bash",
}

# node types that denote a definition worth indexing
DEF_TYPES = {
    "function_definition", "function_declaration", "method_definition",
    "method_declaration", "class_definition", "class_declaration",
    "interface_declaration", "enum_declaration", "constructor_declaration",
}
IMPORT_TYPES = {
    "import_statement", "import_from_statement", "import_declaration",
    "import_spec", "use_declaration", "preproc_include",
}

BUILTIN_SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "out",
    "target", "coverage", ".venv", "venv", "__pycache__", ".next", ".cache",
}


def load_languages():
    """Return {lang_name: Language} for every tree-sitter wheel installed."""
    langs = {}
    try:
        from tree_sitter import Language
    except Exception:
        return langs, None

    def try_lang(name, module, attr="language"):
        try:
            mod = __import__(module)
            fn = getattr(mod, attr)
            langs[name] = Language(fn())
        except Exception:
            pass

    try_lang("python", "tree_sitter_python")
    try_lang("javascript", "tree_sitter_javascript")
    try_lang("go", "tree_sitter_go")
    try_lang("java", "tree_sitter_java")
    try_lang("ruby", "tree_sitter_ruby")
    try_lang("rust", "tree_sitter_rust")
    try_lang("c", "tree_sitter_c")
    try_lang("cpp", "tree_sitter_cpp")
    try_lang("c_sharp", "tree_sitter_c_sharp")
    try_lang("php", "tree_sitter_php", "language_php")
    try_lang("bash", "tree_sitter_bash")
    # typescript wheel exposes two languages
    try:
        import tree_sitter_typescript as tst
        from tree_sitter import Language
        langs["typescript"] = Language(tst.language_typescript())
        langs["tsx"] = Language(tst.language_tsx())
    except Exception:
        pass
    return langs, Language


def make_parser(language):
    from tree_sitter import Parser
    try:
        return Parser(language)
    except TypeError:
        p = Parser()
        p.set_language(language)
        return p


def read_bobignore(root):
    patterns = []
    path = os.path.join(root, ".bobignore")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line.rstrip("/"))
    return patterns


def ignored(rel, patterns):
    parts = rel.split("/")
    if any(p in BUILTIN_SKIP_DIRS for p in parts):
        return True
    base = parts[-1]
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(base, pat):
            return True
        if pat in parts:
            return True
        if rel.startswith(pat + "/"):
            return True
    return False


def node_name(node, src):
    field = node.child_by_field_name("name")
    if field is not None:
        return src[field.start_byte:field.end_byte].decode("utf-8", "ignore")
    for c in node.children:
        if c.type in ("identifier", "type_identifier", "field_identifier",
                      "property_identifier", "constant", "name"):
            return src[c.start_byte:c.end_byte].decode("utf-8", "ignore")
    return None


def extract_ts(src, language, want_imports):
    parser = make_parser(language)
    tree = parser.parse(src)
    symbols, imports = [], []
    stack = [tree.root_node]
    while stack:
        n = stack.pop()
        if n.type in DEF_TYPES:
            name = node_name(n, src)
            if name:
                symbols.append({
                    "name": name,
                    "kind": n.type.replace("_declaration", "").replace("_definition", ""),
                    "start_line": n.start_point[0] + 1,
                    "end_line": n.end_point[0] + 1,
                })
        elif want_imports and n.type in IMPORT_TYPES:
            text = src[n.start_byte:n.end_byte].decode("utf-8", "ignore").strip()
            imports.append({"text": text[:200], "line": n.start_point[0] + 1})
        stack.extend(n.children)
    symbols.sort(key=lambda s: (s["start_line"], s["name"]))
    return symbols, imports


def extract_py_stdlib(src_text):
    import ast as pyast
    symbols = []
    try:
        tree = pyast.parse(src_text)
    except Exception:
        return symbols
    for node in pyast.walk(tree):
        if isinstance(node, (pyast.FunctionDef, pyast.AsyncFunctionDef, pyast.ClassDef)):
            symbols.append({
                "name": node.name,
                "kind": "class" if isinstance(node, pyast.ClassDef) else "function",
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno) or node.lineno,
            })
    symbols.sort(key=lambda s: (s["start_line"], s["name"]))
    return symbols


def git_commit(root):
    try:
        out = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=5)
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser(description="Deterministic tree-sitter symbol index.")
    ap.add_argument("root")
    ap.add_argument("--out", default=None, help="write JSON here (default: stdout)")
    ap.add_argument("--imports", action="store_true", help="also capture import lines")
    ap.add_argument("--json", action="store_true", help="print full JSON to stdout")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    languages, _ = load_languages()
    parser_kind = "tree-sitter" if languages else "stdlib-ast (python only)"
    patterns = read_bobignore(root)

    files_out, lang_counts, symbol_count, skipped = [], {}, 0, 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in BUILTIN_SKIP_DIRS and not d.startswith(".")]
        for fn in sorted(filenames):
            ext = os.path.splitext(fn)[1].lower()
            lang = EXT_LANG.get(ext)
            if not lang:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if ignored(rel, patterns):
                continue
            try:
                with open(full, "rb") as fh:
                    raw = fh.read()
            except Exception:
                skipped += 1
                continue
            line_count = raw.count(b"\n") + 1
            symbols, imports = [], []
            if lang in languages:
                try:
                    symbols, imports = extract_ts(raw, languages[lang], args.imports)
                except Exception:
                    skipped += 1
            elif lang == "python":
                symbols = extract_py_stdlib(raw.decode("utf-8", "ignore"))
            else:
                skipped += 1
                continue
            rec = {"path": rel, "language": lang, "lines": line_count, "symbols": symbols}
            if args.imports:
                rec["imports"] = imports
            files_out.append(rec)
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
            symbol_count += len(symbols)

    files_out.sort(key=lambda f: f["path"])
    result = {
        "schema": "astmap/1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "root": os.path.basename(root),
        "indexed_commit": git_commit(root),
        "parser": parser_kind,
        "note": "Definitions only. No dependency or call graph. Use as grounding anchors.",
        "summary": {"files": len(files_out), "symbols": symbol_count, "skipped": skipped,
                    "languages": lang_counts},
        "files": files_out,
    }

    payload = json.dumps(result, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print(f"astmap: {result['summary']['files']} files, "
              f"{result['summary']['symbols']} symbols, parser={parser_kind} -> {args.out}",
              file=sys.stderr)
    elif args.json:
        print(payload)
    else:
        s = result["summary"]
        print(f"astmap: {s['files']} files, {s['symbols']} symbols, "
              f"{s['skipped']} skipped, parser={parser_kind}", file=sys.stderr)
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
