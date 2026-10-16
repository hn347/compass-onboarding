---
name: glossary-builder
description: >-
  Builds a grounded glossary of a repository's domain terms and acronyms, with
  each entry tied to where it actually appears and a confidence marker. Use this
  whenever the user is confused by jargon or acronyms, asks what a term means,
  or wants a glossary, and as part of generating the onboarding packet. Never
  invents a definition; ambiguous terms are marked, not guessed.
---

# Glossary Builder

Acronyms are the steepest part of any onboarding, and they are the easiest thing
for a model to hallucinate, because the same letters mean different things in
different organizations. This skill builds a glossary that points at evidence.

## When to use

When a reader hits unfamiliar jargon, asks what a term or acronym means, or wants
a glossary, and as part of the onboarding packet.

## Workflow

1. Harvest candidate terms from where domain language actually lives: README and
   docs, module and package names, code comments, type and class names, config
   keys, and error messages. Honor `.bobignore`.
2. For each term, capture at least one occurrence as `file:line`.
3. Define the term only from evidence in the repository. If the meaning is clear
   from usage, mark confidence high. If you are inferring, mark it low.
4. If a term cannot be defined from the repo, list it under unconfirmed terms
   with `UNKNOWN meaning`, its occurrence, and what would confirm it. Do not
   guess, and do not import a definition from outside the repo without saying so.
5. Flag overloaded terms (the same acronym used two ways) explicitly, with both
   occurrences.

## Output contract

A `GLOSSARY.md` table of Term, Meaning, Seen in (`file:line`), and Confidence,
plus an unconfirmed-terms section. Every row is grounded; nothing is invented.
