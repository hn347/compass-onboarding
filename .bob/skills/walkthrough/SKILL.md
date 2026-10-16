---
name: walkthrough
description: >-
  Generates a self-contained interactive HTML walkthrough with a clickable
  Mermaid diagram to explain a codebase feature, flow, architecture, or database
  schema. Each node opens a detail panel with a plain-English description,
  grounded file:line references, and a syntax-highlighted snippet. Use this
  whenever the user wants to see, visualize, or be walked through how something
  works, asks "walk me through X", "explain this flow", "how does X work", or
  "show me the architecture / the schema", and as the visual output of an
  onboarding run. The goal is a mental model in under two minutes: a map, not a
  code reference.
---

# Walkthrough

Produces one self-contained `walkthrough-{topic}.html` you can open in any
browser. No build step. The look and behavior match a clickable diagram
walkthrough: a Mermaid flowchart or ER diagram whose nodes you click to read a
grounded explanation, with pan and zoom and syntax-highlighted code. Nodes that
represent a subflow can be drilled into: clicking opens a deeper diagram of just
that piece, with a breadcrumb back up, so the top level stays abstract and the
reader opens detail on demand instead of scrolling a long document. Themed to
IBM Carbon (dark). Inspired by the open-source walkthrough skill (alexanderop)
and Amp's shareable walkthroughs; this is an original implementation.

## When to use

"Walk me through X", "explain this flow", "how does X work", "show me the
architecture", "explain the database schema / the tables", or as the visual
artifact at the end of `/onboard`.

## Workflow

1. **Scope.** Decide what to explain (a feature, a flow, the architecture, or a
   schema) and pick the diagram type: a `flowchart` for control or data flow, an
   `erDiagram` for a database schema.
2. **Explore, grounded.** Use the repo-explorer to gather the relevant slices.
   Reuse area summaries that already exist; do not re-read the whole repo. Every
   concept you will show must trace to a real `file:line`.
3. **Synthesize.** Reduce to five to twelve concept nodes and their connections.
   Fewer is better; this is a map, not an inventory. For each node capture: a
   short label, a plain-English description, one or more `file:line` references,
   and a short representative snippet (at most about a dozen lines) with its
   language. For any node that is itself a subflow worth opening, attach a
   `subflow` (its own diagram and nodes) so a reader can drill into it; keep the
   top level abstract.
4. **Generate.** Produce a single self-contained HTML file following
   `references/html-patterns.md`: fill the `DATA` object with the topic, the
   Mermaid diagram string, and the per-node details. Write it to
   `docs/onboarding/walkthrough-{topic}.html`.
5. **Stamp and report.** Add the provenance comment (commit, branch, time,
   depth) at the top of the file and tell the user the path to open.
6. **Verify.** Run `verify_citations.py` over `docs/onboarding/` so every
   `file:line` in the walkthrough resolves to a real file and line. Fix or mark
   UNKNOWN anything that fails before sharing the file.

## Grounding

- Every node description and snippet is tied to a real `file:line`. No citation,
  no node.
- If a concept cannot be grounded, leave it out or mark it UNKNOWN in the node
  description. Never invent a file path or a snippet.
- Keep snippets short (a representative excerpt), not whole files.

## Output contract

- Exactly one self-contained `.html` file under `docs/onboarding/`.
- Opens offline except for two CDN dependencies (the diagram and the
  highlighter); see the reference for the vendoring fallback if the network
  blocks CDNs.
- Five to twelve nodes, each grounded. Modifies no source.
