---
description: Generate an interactive HTML walkthrough of a feature, flow, architecture, or schema
argument-hint: "<topic, e.g. 'how auth works' or 'database schema'>"
allowed-tools: Read, Grep, Glob
---

Produce an interactive HTML walkthrough of: $ARGUMENTS

Switch to the `onboarding` mode and run the `walkthrough` skill.

1. Scope the topic and pick a diagram type: a flowchart for a feature, flow, or
   architecture; an ER diagram for a database schema.
2. Gather the relevant slices via the read-only `repo-explorer`, reusing any area
   summaries that already exist. Do not read the whole repo.
3. Reduce to five to twelve grounded concept nodes, each tied to a real
   file:line, each with a short description and a short snippet.
4. Generate one self-contained docs/onboarding/walkthrough-{topic}.html following
   .bob/skills/walkthrough/references/html-patterns.md, themed to IBM Carbon.
5. Stamp provenance and print the path to open. Modify no source.
