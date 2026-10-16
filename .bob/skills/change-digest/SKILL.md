---
name: change-digest
description: >-
  Summarizes what changed in a repository since a reference commit and refreshes
  only the affected parts of the onboarding packet. Use this whenever the user
  is a returning developer asking what changed, what is new, or what they missed,
  and whenever /reindex runs. Focuses on substantive change and ignores noise.
---

# Change Digest

The expert path. Instead of re-onboarding from scratch, diff against the last
indexed commit and report only what matters.

## When to use

A returning developer asking "what changed since I was last here", or any
`/reindex` run.

## Inputs

- The `Indexed-at` commit recorded in `MODULE-MAP.md`.
- The current `HEAD`.

## Workflow

1. Read the stamped `Indexed-at` commit from `MODULE-MAP.md`. If it equals
   `HEAD`, report that the packet is current and stop.
2. Get the changed files: `git diff --name-status <Indexed-at> HEAD`, honoring
   `.bobignore`.
3. Classify changes. Flag substantive ones: new modules or services, new or
   removed env vars, changed entry points, altered data flow, dependency
   changes, public interface changes. Ignore noise: pure refactors with no
   behavior change, formatting, test-only edits, comment churn.
4. For each substantively changed area, re-run repo-explorer on just that area
   and update its block in `MODULE-MAP.md`. Touch nothing else.
5. Write a short `What changed` section at the top of `START-HERE.md` for the
   expert reader: the few things worth knowing, each linked to a file.
6. Re-stamp provenance only after the digest has been reviewed. Never re-stamp
   an unreviewed diff.

## Output contract

- A concise change digest (substantive changes only), grounded in file references.
- Updated module-map blocks for changed areas, with refreshed map-age notes.
- Stale flags on any area whose map predates that area's latest commit.
