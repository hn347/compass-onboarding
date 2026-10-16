#!/usr/bin/env python3
"""
verify_citations.py - mechanical anti-hallucination check for the packet.

Scans the generated onboarding artifacts (markdown and the walkthrough HTML) for
every `path:line` (or `path:start-end`) citation and checks, against the real
repository, that:
    - the cited file actually exists, and
    - the cited line (or range) is within that file's length.

If an `astmap.json` is supplied, it additionally reports whether the cited line
falls inside a known symbol's range (informational, never a failure).

The point: a claim is only allowed to ship if its citation is real. Anything
that fails here must be fixed or rewritten as an explicit UNKNOWN. This is the
deterministic guard that stops a confident-but-wrong map from reaching a reader.

Usage:
    python3 verify_citations.py --repo <root> --docs <dir> [--astmap PATH] [--json]

Exit codes: 0 if every citation verifies, 1 if any fail, 2 on usage error.
"""
import argparse, json, os, re, sys

# path-like token with an extension, then :line or :line-line
CITE = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_./\-]*\.[A-Za-z0-9]{1,10}):(\d+)(?:[-:](\d+))?")
SCAN_EXT = {".md", ".html", ".htm", ".txt"}


def find_docs(docs_dir):
    out = []
    for dp, dn, fns in os.walk(docs_dir):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for fn in fns:
            if os.path.splitext(fn)[1].lower() in SCAN_EXT:
                out.append(os.path.join(dp, fn))
    return sorted(out)


def line_count(path):
    with open(path, "rb") as fh:
        return fh.read().count(b"\n") + 1


def load_astmap(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        idx = {}
        for f in data.get("files", []):
            idx[f["path"]] = f.get("symbols", [])
        return idx
    except Exception:
        return None


def symbol_at(symbols, line):
    hit = None
    for s in symbols:
        if s["start_line"] <= line <= s["end_line"]:
            if hit is None or (s["end_line"] - s["start_line"]) < (hit["end_line"] - hit["start_line"]):
                hit = s  # smallest enclosing symbol
    return hit["name"] if hit else None


def main():
    ap = argparse.ArgumentParser(description="Verify file:line citations against the repo.")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--docs", required=True)
    ap.add_argument("--astmap", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    docs = os.path.abspath(args.docs)
    if not os.path.isdir(repo) or not os.path.isdir(docs):
        print("error: --repo and --docs must be directories", file=sys.stderr)
        return 2

    astmap = load_astmap(args.astmap) if args.astmap else None

    seen = {}  # (path,start,end,source) -> dedup
    results = []
    for doc in find_docs(docs):
        try:
            text = open(doc, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        rel_doc = os.path.relpath(doc, docs)
        for m in CITE.finditer(text):
            path, start = m.group(1), int(m.group(2))
            end = int(m.group(3)) if m.group(3) else start
            # skip obvious non-citations (urls, times, version-like)
            ctx = text[max(0, m.start() - 3):m.start()]
            if "://" in ctx or path.lower().startswith(("http", "www.")):
                continue
            key = (path, start, end)
            if key in seen:
                continue
            seen[key] = True

            target = os.path.normpath(os.path.join(repo, path))
            rec = {"citation": f"{path}:{start}" + (f"-{end}" if end != start else ""),
                   "in": rel_doc, "status": "ok", "reason": ""}
            if not (os.path.isfile(target) and os.path.abspath(target).startswith(repo)):
                rec["status"] = "FAIL"; rec["reason"] = "file does not exist"
            else:
                lc = line_count(target)
                if start < 1 or start > lc or end < start or end > lc:
                    rec["status"] = "FAIL"
                    rec["reason"] = f"line out of range (file has {lc} lines)"
                elif astmap is not None and path in astmap:
                    sym = symbol_at(astmap[path], start)
                    if sym:
                        rec["reason"] = f"in symbol '{sym}'"
            results.append(rec)

    total = len(results)
    failed = [r for r in results if r["status"] == "FAIL"]
    ok = total - len(failed)

    if args.json:
        print(json.dumps({"total": total, "ok": ok, "failed": len(failed),
                          "results": results}, indent=2))
    else:
        print(f"Citations checked: {total}  verified: {ok}  failed: {len(failed)}")
        for r in failed:
            print(f"  FAIL  {r['citation']}  ({r['reason']})  [{r['in']}]")
        if not failed and total:
            print("  All citations resolve to real files and valid line ranges.")
        if total == 0:
            print("  No citations found to verify.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
