---
description: Refresh the onboarding packet for only what changed since the last run
argument-hint: ""
allowed-tools: Read, Grep, Glob, Bash(git:*)
---

Refresh the onboarding packet using a diff, not a full re-scan.

Switch to the `onboarding` mode and run the `change-digest` skill.

1. Read the `Indexed-at` commit from docs/onboarding/MODULE-MAP.md. If it equals
   HEAD, report that the packet is current and stop.
2. Diff with `git diff --name-status <Indexed-at> HEAD`, honoring .bobignore.
3. Re-explore only substantively changed areas (new modules, env vars, entry
   points, data flow, dependencies, public interfaces). Ignore pure refactors,
   formatting, and test-only churn.
4. Update only the changed blocks in MODULE-MAP.md and add a short "What changed"
   section to the top of START-HERE.md.
5. Flag any area whose map predates that area's latest commit as possibly stale.
6. Re-stamp provenance only after the change digest has been reviewed.
