---
description: Build or show the grounded domain and acronym glossary
argument-hint: "[term]"
allowed-tools: Read, Grep, Glob
---

Build or show the glossary. Optional term to look up: $ARGUMENTS

Switch to the `onboarding` mode and run the `glossary-builder` skill.

1. If a term is given, define just that term from evidence in the repo, with its
   occurrence as file:line and a confidence marker. If it cannot be defined from
   the repo, say UNKNOWN and what would confirm it.
2. If no term is given, build or refresh docs/onboarding/GLOSSARY.md across the
   repository's domain language.
3. Every entry must be grounded in where the term actually appears. Flag
   overloaded acronyms with both usages. Never invent a definition.
