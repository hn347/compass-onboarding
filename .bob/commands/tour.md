---
description: Guided walkthrough of one module, with a one-hop dependency note
argument-hint: "<module-or-path>"
allowed-tools: Read, Grep, Glob
---

Give a guided tour of: $ARGUMENTS

Switch to the `onboarding` mode.

1. Locate the module or path. If ambiguous, ask which one rather than guessing.
2. Delegate a read-only `repo-explorer` pass scoped to that module.
3. Walk the reader through it: its responsibility, entry points, the key files in
   the order you would read them (with file:line), and the gotchas.
4. Add a one-hop dependency note: what this module calls and what calls it, with
   references. Do not expand beyond one hop.
5. If a module map block exists and predates the module's latest commit, say it
   may be stale and offer to /reindex.
6. Ground every claim; mark anything unverified as UNKNOWN. Modify no source.
