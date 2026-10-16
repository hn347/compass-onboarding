# Rule: write only the onboarding packet, never source

Onboarding is a read-and-document activity. It must never change the code it describes.

- Write only markdown and HTML inside `docs/onboarding/`, plus `AGENTS.md` when enhancing it.
- Never edit, refactor, rename, move, or delete source files during onboarding.
- The packet contains five markdown files: `START-HERE.md`, `ARCHITECTURE.md`, `MODULE-MAP.md`, `GLOSSARY.md`, `RUNBOOK.md`, plus the interactive `walkthrough-overview.html`.
- Every artifact opens with a provenance header:

```
<!--
Compass packet
Indexed-at: <commit-sha>
Branch: <branch>
Generated: <ISO timestamp>
Depth: newcomer | expert
-->
```

- Keep each artifact scannable in about two minutes. Push detail into the code, not the guide.
