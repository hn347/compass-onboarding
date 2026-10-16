---
name: repo-cartographer
description: >-
  Maps an unfamiliar repository into a grounded architecture and module map
  without loading the whole codebase. Use this whenever the user wants to
  understand, explore, onboard to, navigate, or get oriented in a codebase, or
  asks how something works, where something lives, or what the overall structure
  is. Use it proactively at the start of any onboarding run, even if the user
  does not say the word "map".
---

# Repo Cartographer

Turns a cold repository into a set of grounded area summaries that the
onboarding-packet skill assembles into the final packet. The whole point is to
build understanding without flooding the context window.

## When to use

Onboarding a new repo, ramping on a specific area, refreshing a stale map, or
answering "how does this work" / "where is X" on a codebase you have not loaded.

## Workflow

Four phases. Do not skip phase 1.

1. **Reconnaissance (cheap, no full reads).** Use Glob and Grep, not Read on
   every file. Gather: the directory tree at two levels, package manifests and
   their declared scripts, framework fingerprints, entry points (main, server,
   index, CLI roots), test directory layout, and config files. Honor
   `.bobignore`. Read a file in full only when a signal is ambiguous.
   When tree-sitter is available, also run `scripts/astmap.py <root> --out
   docs/onboarding/.astmap.json` to get a deterministic symbol index, and anchor
   every reference to the real symbol and line range it reports. Fall back to
   Glob and Grep when tree-sitter is not installed. See `scripts/README.md`.

2. **Architecture mapping.** From the signals, identify the top-level areas
   (modules, services, layers). For each area, decide whether it warrants its
   own exploration pass. Sketch how areas connect (who calls whom, where data
   flows). Keep this in the running map, not as raw code in context.

3. **Per-area exploration.** For each area, prefer delegating an isolated
   `repo-explorer` subtask scoped to that area; otherwise explore it directly,
   one area at a time. The explorer reads only that slice and returns a summary
   using `references/area-summary.template.md`: responsibility, key files with
   `file:line`, entry points, one-hop dependencies, gotchas, and any UNKNOWNs.
   Persist each summary to disk, then drop the slice detail before the next area.

4. **Convention detection.** Note repository-wide conventions grounded in
   examples: naming, error handling, logging, config, how tests are run. Mark
   anything you cannot confirm as UNKNOWN.

## Output contract

- A set of area summaries on disk, each grounded in `file:line` references with
  excerpts of at most two lines.
- A scope note: which areas were explored, and (for a focused run) the one-hop
  dependencies that were touched but not fully indexed.
- Never paste large file contents. Never modify source.

## Anti-patterns

- Reading the whole repo into context. Use reconnaissance and delegation.
- Asserting behavior you did not verify. Cite or write UNKNOWN.
- Following every dependency edge. Stop at one hop for a focused run.
