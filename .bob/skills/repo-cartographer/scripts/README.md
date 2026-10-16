# Cartographer scripts: deterministic indexing and verification

Two small scripts that give the onboarding agent accurate, grounded context and
mechanically stop hallucination. They follow the two-phase principle used by the
strongest tools (Understand-Anything, Codebase-Memory): a deterministic parser
extracts the facts, the model only does the semantics on top, and a verification
pass refuses anything the facts do not support.

Both are optional and degrade gracefully. If the dependencies are missing, the
skill falls back to Glob and Grep and the pack still works.

## astmap.py — deterministic symbol index

Parses the repo with tree-sitter and emits a JSON map of the symbols each file
DEFINES (functions, methods, classes, interfaces, enums) with exact line ranges.
The agent reads this so every reference it writes is anchored to a real symbol at
a real line, instead of a guessed location.

```
python3 astmap.py <repo_root> --out docs/onboarding/.astmap.json
python3 astmap.py <repo_root> --json            # print full map
python3 astmap.py <repo_root> --imports         # also capture import lines
```

By design this indexes definitions only, not a dependency or call graph. Imports
are captured only with `--imports`, and no cross-file edges are built. That keeps
the grounding value without the cost and noise of a full dependency map.

Dependencies (install only the languages you need):

```
pip install tree_sitter tree_sitter_python tree_sitter_javascript \
            tree_sitter_typescript tree_sitter_go tree_sitter_java
```

If tree-sitter is unavailable, astmap falls back to Python's stdlib parser for
`.py` files so it still produces a partial map. The parser used is recorded in
the output. It honors `.bobignore` and skips vendored and build directories.

## verify_citations.py — anti-hallucination gate

Scans the generated artifacts for every `path:line` citation and checks, against
the real repo, that the file exists and the line (or range) is in bounds. With
`--astmap` it also reports the enclosing symbol. Exit code is non-zero if any
citation fails, so it can gate a run.

```
python3 verify_citations.py --repo <root> --docs docs/onboarding \
        --astmap docs/onboarding/.astmap.json
```

Any failure must be fixed or rewritten as an explicit UNKNOWN before the packet
ships. A claim is only allowed if its citation resolves.

## How the skill uses them

1. Reconnaissance runs `astmap.py` when tree-sitter is present and uses the map
   to anchor references; otherwise it uses Glob and Grep.
2. After the packet (and the walkthrough HTML) are written,
   `verify_citations.py` runs over `docs/onboarding/`. If it fails, the offending
   claims are corrected or marked UNKNOWN, and it runs again until clean.

## Confirm in your environment

These need the skill to be allowed to run a script and need tree-sitter
installed. Both are environment specific; confirm against your Bob install. The
fallbacks mean the pack still functions if either is unavailable.
