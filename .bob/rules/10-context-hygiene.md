# Rule: never load the whole repo; slice, summarize, persist, drop

Keep the working context lean. A large repository must be indexed without its raw code ever filling the window.

- Start with reconnaissance, not reading. Use Glob and Grep to gather signals (directory tree, package manifests, framework fingerprints, entry points, test layout). Read a file fully only when a signal is ambiguous.
- Explore one area at a time. Prefer delegating each area to an isolated `repo-explorer` so the heavy reading happens in a separate context that returns only a summary.
- Persist each area summary to disk immediately, then drop that area's detail from the working context before starting the next area.
- The coordinator's context should hold only the running map plus the single area under examination, never the whole codebase.
- Summaries returned from exploration use `file:line` references and excerpts of at most two lines, never raw file dumps.
