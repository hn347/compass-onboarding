# Walkthrough HTML patterns

How to generate the self-contained interactive walkthrough. The canonical
working instance is `examples/walkthrough-compass.html` in this pack: copy its
structure and replace only the `DATA` object. Everything else (the engine, the
theme, pan and zoom, the panel) stays the same.

## What you produce

One file, `docs/onboarding/walkthrough-{topic}.html`, that opens in any browser
with no build step. It shows a clickable Mermaid diagram on the left and a detail
panel on the right. Clicking a node fills the panel with a plain-English
description, the grounded `file:line` references, and a syntax-highlighted
snippet. Scroll zooms, drag pans, and the view auto-fits on load.

## The only thing you fill in: DATA

```js
const DATA = {
  topic: "How authentication works",        // shown in the header and filename
  diagramType: "flowchart",                 // "flowchart" or "erDiagram"
  mermaid: `flowchart TD
    A["Login form"] --> B["Auth service"]
    B --> C["Session store"]
  `,
  nodes: {
    A: {
      label: "Login form",                  // must match the diagram node text
      files: ["src/ui/Login.tsx:20"],       // one or more real file:line refs
      lang: "tsx",                           // highlight.js language id
      description: "Plain-English explanation, grounded in the files above.",
      code: "function Login() {\n  // short, representative excerpt\n}",
      subflow: {                             // OPTIONAL: adds an abstraction layer
        diagramType: "flowchart",            // clicking this node drills in here
        mermaid: `flowchart TD\n  A1[\"Validate\"] --> A2[\"Call API\"]`,
        nodes: { /* same node shape, recursively; can nest further */ }
      }
    }
    // ... 5 to 12 nodes total
  }
};
```

Rules for `DATA`:
- Five to twelve nodes per level. Fewer is better. This is a map, not an inventory.
- Every node has at least one real `file:line`. No citation, no node.
- Snippets are short representative excerpts, not whole files.
- Node keys (A, B, ...) are simple identifiers with no spaces or hyphens, so the
  click-binding regex can recover them from the rendered diagram.
- For a database schema use `diagramType: "erDiagram"` and a Mermaid `erDiagram`
  body; the engine treats nodes the same way.

## Abstraction layers (drill-down)

A node may carry a `subflow` (its own `mermaid` plus `nodes`, same shape,
nestable to any depth). When present:

- The node is outlined in teal and the right-rail list shows a `›`.
- Clicking the node still fills the detail panel, and a "Drill into ..." button
  appears; double-clicking the node drills in directly.
- Drilling pushes a new level and renders the sub-diagram; a breadcrumb at the
  top left ("Overview › repo-explorer") navigates back up.

Use subflows to keep the top level small and abstract (the system in six or
seven boxes) while letting a reader open any one box into its internal steps,
instead of scrolling a long document. Each subflow node is grounded the same
way: real `file:line`, short snippet, honest UNKNOWNs.

## Dependencies (CDN, with a fallback)

Two scripts load from a CDN:
- Mermaid 11 — `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js`
- highlight.js 11 — `.../gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js`
  plus the `github-dark` stylesheet.

IBM Plex fonts load from Google Fonts but degrade gracefully to system fonts.

If the network blocks CDNs (common inside a corporate firewall), vendor the two
scripts next to the HTML and change the `src` URLs to relative paths:

```
docs/onboarding/
  walkthrough-auth.html
  vendor/mermaid.min.js
  vendor/highlight.min.js
  vendor/github-dark.min.css
```

The engine already handles a failed Mermaid load by showing a clear message
rather than a blank page.

## IBM Carbon theme tokens

The dark theme uses Carbon-style values. Keep these in the `:root` block:

```
--bg:#161616; --layer:#262626; --layer2:#393939; --border:#393939;
--text:#f4f4f4; --text2:#c6c6c6; --muted:#8d8d8d;
--blue:#0f62fe; --blue-l:#4589ff; --blue-ll:#78a9ff; --teal:#08bdba;
```

Mermaid is themed to match via `themeVariables` in `mermaid.initialize`
(`primaryColor:#262626`, `primaryBorderColor:#0f62fe`, IBM Plex font). The active
node gets a blue glow via the `.node.wt-active` CSS rule.

## How the engine works (already implemented; do not rewrite)

- **Render.** `mermaid.render` returns an SVG string injected into `#vp`; its
  `max-width` is stripped so transforms work.
- **Click binding.** After render, every `.node` group gets a click handler.
  `nodeIdFromGroup` recovers the node key from the group id (for example
  `flowchart-A-0` to `A`), with a fallback that matches on the visible label.
- **Pan and zoom.** A transform on `#vp`: wheel zooms toward the cursor, pointer
  drag pans, and `fit()` centers and scales to the stage on load and on demand.
- **Panel.** `select(id)` writes the label, description, file chips, and the
  highlighted snippet, and marks the active node and list item.
- **Drill-down.** A node with a `subflow` gets a teal outline and a "Drill into"
  button; `drillInto(id)` pushes a level and re-renders the sub-diagram, and the
  breadcrumb pops back up. Levels are a simple stack, so nesting is unlimited.
- **Node list.** Every node at the current level also appears as a button in the
  right rail so the walkthrough is navigable without the diagram.

## Provenance

Open the file with the same provenance comment used by the rest of the packet
(commit, branch, timestamp, depth) so the walkthrough can be checked for
staleness like any other artifact.

## Attribution

The interaction model (clickable diagram, per-node detail, mental model in under
two minutes) is inspired by the open-source walkthrough skill by alexanderop and
by Amp's shareable walkthroughs. This is an original implementation built on
standard libraries; no code was copied from those projects.
