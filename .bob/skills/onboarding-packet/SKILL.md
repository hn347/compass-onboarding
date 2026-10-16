---
name: onboarding-packet
description: >-
  Assembles the five-file onboarding packet (START-HERE, ARCHITECTURE,
  MODULE-MAP, GLOSSARY, RUNBOOK) from area summaries produced by repo-cartographer.
  Use this whenever the user wants onboarding documentation, a getting-started
  guide, an architecture overview, or a reading path generated for a repository,
  and after repo-cartographer has gathered area summaries.
---

# Onboarding Packet

Takes the grounded area summaries and writes the durable packet under
`docs/onboarding/`, adapted to the requested depth.

## When to use

After reconnaissance and exploration, to produce or refresh the onboarding
artifacts. Also when the user explicitly asks for onboarding docs, an
architecture overview, or a reading path.

## Inputs

- The area summaries on disk (from repo-cartographer).
- The requested depth (`newcomer` default, or `expert`).
- An optional focus area.
- The current commit SHA, branch, and timestamp for the provenance header.

## Workflow

1. Write the provenance header (see below) at the top of every artifact.
2. Generate each artifact from the matching template in `references/`:
   - `START-HERE.md` from `start-here.template.md` — the entry point and reading path.
   - `ARCHITECTURE.md` from `architecture.template.md` — the system at altitude.
   - `MODULE-MAP.md` from `module-map.template.md` — per-area summaries, and the `Indexed-at` stamp.
   - `GLOSSARY.md` from `glossary.template.md` — delegate to glossary-builder.
   - `RUNBOOK.md` from `runbook.template.md` — build, run, test, deploy.
3. Generate the visual entry point: delegate to the `walkthrough` skill to
   produce `walkthrough-overview.html`, a clickable diagram of the system whose
   nodes carry the same grounded file:line references and snippets. This is the
   artifact most newcomers open first; the markdown files are the durable detail
   behind it.
4. Adapt depth: newcomer gets analogies, a request-lifecycle trace, and a
   where-to-look table; expert gets a terse change digest and risk hot-spots.
5. Keep every artifact scannable in about two minutes. Carry UNKNOWNs through;
   do not silently drop them.
6. Verify before finalizing. Run
   `.bob/skills/repo-cartographer/scripts/verify_citations.py --repo . --docs
   docs/onboarding` (with `--astmap` if a map exists). Fix or downgrade to
   UNKNOWN any citation that fails, then re-run until the check is clean.

## Provenance header (top of every artifact)

```
<!--
Compass packet
Indexed-at: <commit-sha>
Branch: <branch>
Generated: <ISO timestamp>
Depth: newcomer | expert
-->
```

## Output contract

- Five markdown files plus one interactive `walkthrough-overview.html` in `docs/onboarding/`.
- Every claim grounded in `file:line`; every gap an explicit UNKNOWN.
- No source files modified.
