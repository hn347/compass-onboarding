---
description: Onboard me to this repo and produce the grounded onboarding packet
argument-hint: "[focus-area] [--depth newcomer|expert]"
allowed-tools: Read, Grep, Glob, Bash(git:*)
---

Onboard a developer to this repository. Target: $ARGUMENTS

Switch to the `onboarding` mode and follow AGENTS.md and the .bob/rules.

1. Parse arguments. The trailing `--depth` selects newcomer (default) or expert.
   Any remaining text is the focus area. No focus means a whole-repo orientation,
   which is a valid first-class path, not an error.
2. Run the `repo-cartographer` skill: reconnaissance first (Glob/Grep, not full
   reads), then explore each area via the read-only `repo-explorer`, persisting a
   grounded summary per area and dropping slice detail between areas. For a focus
   run, index the focus area plus its one-hop dependencies only.
3. Run the `onboarding-packet` skill to write the five artifacts under
   docs/onboarding/, each with a provenance header stamped to the current commit.
4. Ground every claim in file:line. Write UNKNOWN, never a guess. Keep each
   artifact scannable in about two minutes. Modify no source.
5. End by printing the reading path from START-HERE.md.
