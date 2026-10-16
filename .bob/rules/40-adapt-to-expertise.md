# Rule: adapt depth and vocabulary to the reader, not the facts

The same repository should read differently for a newcomer and a returning expert. Change how much you explain and which words you assume, never the underlying facts.

Newcomer (`--depth newcomer`, the default):
- Lead with orientation: what the system is, who uses it, the one-sentence purpose.
- Use a concrete analogy for each non-obvious concept, and do not reuse the same analogy twice.
- Trace one end-to-end path (for example, a single request lifecycle) so the pieces connect.
- Provide a "where to look" table mapping common tasks to file locations.
- Always include how to build, run, and test.

Returning expert (`--depth expert`):
- Lead with a terse what-changed digest since the reference commit.
- Keep architecture at altitude; skip basics they already know.
- Surface risk: hot-spots, recently churned areas, fragile seams, and open UNKNOWNs.
- Prefer diffs and pointers over prose.

If the level is not given, default to newcomer and a whole-repo orientation.
