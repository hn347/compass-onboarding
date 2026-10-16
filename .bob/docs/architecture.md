# Compass architecture

How the pack is built and why. This is the design record; the README is the pitch.

## The one idea

Index a large repository without its raw code ever filling the context window.
Everything else follows from that. A coordinator holds a small running map; a
read-only explorer does the heavy reading one slice at a time and hands back only
a summary; each summary is persisted to disk and the slice detail is dropped.

## The pieces and how they connect

```
/onboard ──▶ onboarding mode (coordinator)
                 │  reconnaissance (Glob/Grep)
                 │  repo-cartographer skill
                 ├──▶ repo-explorer (read-only) ── area summary ──┐
                 ├──▶ repo-explorer (read-only) ── area summary ──┤
                 │                                                ▼
                 │                        summaries persisted to docs/onboarding/
                 │  onboarding-packet skill
                 ▼
        START-HERE / ARCHITECTURE / MODULE-MAP / GLOSSARY / RUNBOOK
                 + walkthrough-overview.html (clickable, IBM-themed)
                 (each stamped Indexed-at: <commit>)

/walkthrough ──▶ walkthrough skill ── grounded nodes ──▶ self-contained clickable HTML

/reindex ──▶ change-digest skill ── git diff since Indexed-at ──▶ update changed blocks only
/tour    ──▶ repo-explorer on one module + one-hop dependency note
/glossary──▶ glossary-builder ── grounded, confidence-marked terms
```

- **Coordinator vs worker.** `onboarding` plans, delegates, and writes (markdown
  only, scoped by allowedEditPatterns). `repo-explorer` is read-only with no edit
  group, so
  it physically cannot change the repo. This mirrors the proven explore-and-return
  -a-summary pattern: understanding is a prerequisite to writing docs, so the
  expensive reading happens in an isolated context that returns a summary rather
  than dumping files into the main conversation.
- **Skills carry the workflows.** repo-cartographer (reconnaissance + per-area
  exploration), onboarding-packet (assembly), change-digest (diff-driven refresh),
  glossary-builder (grounded terms), and walkthrough (the self-contained clickable
  HTML, modeled on standard libraries and themed to IBM Carbon). Templates live in
  each skill's `references/`
  so they load only when needed.
- **Rules carry the guarantees.** Grounding, context hygiene, honor .bobignore,
  docs-only output, adapt-to-expertise, Chesterton's Fence.

## Design decisions (and why)

1. **Reconnaissance before reading.** Signals (manifests, fingerprints, entry
   points) are cheap and tell you which few areas deserve a deep pass. Reading
   everything is the failure mode that defeats the whole point.
2. **Summaries, not contents.** The explorer returns file:line references and
   excerpts of at most two lines. This keeps the coordinator's context small even
   on a huge repo.
3. **Grounding with abstention.** Every claim cites a file; every gap is an
   explicit UNKNOWN. Confident-but-wrong onboarding docs are worse than none,
   because newcomers trust them. Abstaining is treated as a success.
3a. **Deterministic facts, then semantics, then verification.** Following the
   two-phase design of the strongest tools, a tree-sitter pass (`astmap.py`)
   extracts the real symbols and exact line ranges as a deterministic backbone;
   the model only does the semantic layer on top; and `verify_citations.py`
   mechanically checks every `file:line` in the packet against the repo, failing
   the run on a missing file or out-of-range line. Both scripts degrade
   gracefully (Glob/Grep fallback; stdlib parser for Python) so the pack works
   without them. Compass indexes definitions, not a dependency or call graph,
   on purpose, to keep the output focused and accurate.
4. **Provenance stamp enables cheap refresh.** Stamping artifacts with the source
   commit turns `/reindex` into a diff against that commit, so refresh touches
   only changed areas, and the map can tell when it is behind the code.
5. **One-hop dependency bound on focus.** A focused run indexes the named area
   plus what it directly touches, never the transitive closure, or it quietly
   re-indexes the whole repo.
6. **Adapt depth, not facts.** Newcomer and expert outputs differ in depth and
   vocabulary, drawn from the same grounded summaries.

## What to confirm against your Bob install

These are modeled on Bob's documented behavior and its lineage; verify the
specifics on your version before relying on them.

- Skills auto-activate in Advanced mode; test skills there, not in Code mode.
- The `.bob/custom_modes.yaml` schema and tool-group names (read, command), and
  whether write scoping uses the `allowedEditPatterns` key (as written here) or an
  inline edit-with-fileRegex group, and how those patterns anchor against paths.
- Whether a custom mode can delegate isolated subtasks, or whether delegation
  must run through Orchestrator. The pack is written to degrade gracefully: if
  delegation is unavailable, the coordinator explores one area at a time and
  persists before continuing, which preserves context hygiene either way.
- Whether commands can pre-authorize `git` via the tool group, which `/reindex`
  needs for its diff. If not, fall back to timestamp-only staleness.

## Known limitations

- AI-distilled maps are an orientation, not ground truth; that is why everything
  is grounded and unknowns are flagged.
- Exploration is coordinated and effectively sequential; the benefit is context
  isolation, not parallel speed.
- The first run on a repo is always a full index; `/reindex` needs a prior stamp.
