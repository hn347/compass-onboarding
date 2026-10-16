# Rule: machine-verify every citation before finalizing

Grounding (rule 00) requires a citation on every claim. This rule makes that
mechanical, so nothing confident-but-wrong reaches a reader.

- When tree-sitter is available, run `.bob/skills/repo-cartographer/scripts/astmap.py`
  during reconnaissance and anchor references to the real symbol and line range
  it reports, rather than a guessed location. Fall back to Glob and Grep when it
  is not available.
- Before finalizing the packet, run
  `.bob/skills/repo-cartographer/scripts/verify_citations.py --repo . --docs docs/onboarding`
  (pass `--astmap` if a map was generated). Every `path:line` citation must
  resolve to a real file and an in-range line.
- If a citation fails, do not ship it. Fix the reference, or rewrite the claim as
  an explicit UNKNOWN with what would confirm it, then run the check again until
  it is clean.
- A static parse cannot see dynamic dispatch, reflection, or config-driven
  wiring. Treat a relationship the parser does not show as "not found by static
  analysis," not as "does not exist."
