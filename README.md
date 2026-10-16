# Compass

**Codebase onboarding for IBM Bob: turn an unfamiliar repository into a guided reading path, an architecture map, and an interactive walkthrough.**

Compass helps new contributors find the right starting point and returning contributors understand what changed. A coordinator explores the repository in focused slices, persists concise summaries, and assembles documentation with references back to the source.

Built for **HelloPOK Hackathon 2026** by **team-zbringup**.

## At a glance

- **What it is:** an IBM Bob onboarding pack with modes, commands, rules, reusable skills, two Python utilities, and HTML examples.
- **Core design:** keep context focused, ground explanations in source references, and preserve useful findings as versioned documentation.
- **Stack:** Python, optional tree-sitter parsers, Markdown, YAML, HTML/CSS/JavaScript, Mermaid, and highlight.js.
- **Start exploring:** [architecture](.bob/docs/architecture.md), [indexing and verification scripts](.bob/skills/repo-cartographer/scripts/), and [interactive Compass example](examples/walkthrough-compass.html).

## What it produces

An `/onboard` run is designed to create a packet in `docs/onboarding/`:

| Artifact | Reader benefit |
| --- | --- |
| `START-HERE.md` | A short reading path and first steps |
| `ARCHITECTURE.md` | The main components and how they fit together |
| `MODULE-MAP.md` | Where to look for a particular responsibility |
| `GLOSSARY.md` | Project terminology grounded in its usage |
| `RUNBOOK.md` | Setup, development, and verification guidance |
| `walkthrough-overview.html` | Clickable diagrams, code panels, and drill-down views |

The newcomer path emphasizes orientation and setup. The expert path emphasizes architecture, risks, and changes since a previous index. Artifacts carry source-commit provenance so readers can assess freshness.

## How it works

```text
/onboard -> Reconnaissance -> Focused repository exploration
                                       |
                              Persist area summaries
                                       |
                            Assemble onboarding packet
                                       |
                             Check source citations
                                       |
                          Markdown + HTML walkthrough
```

The coordinator delegates focused exploration to a read-only worker when supported, or explores sequentially when delegation is unavailable. The optional `astmap.py` utility extracts symbol definitions and line ranges. `verify_citations.py` checks recognized citations for file existence and valid line bounds; it does not establish that a written claim is semantically correct.

`/reindex` uses the recorded commit to identify committed changes and refresh relevant documentation. `/tour` and `/walkthrough` provide focused explanations without rebuilding the whole packet.

## Quick start

1. Clone the pack:

   ```bash
   git clone https://github.com/hn347/compass-onboarding.git
   ```

2. Merge `.bob/`, `AGENTS.md`, and the sample `.bobignore` into the repository you want to explore. Preserve existing project instructions and configuration when merging.
3. Open the target repository in IBM Bob. The original setup uses Advanced mode for skills; confirm mode and tool support in your installed version.
4. Run:

   ```text
   /onboard
   ```

5. Review the generated packet in `docs/onboarding/`, following its references back to the source.

### Commands

```text
/onboard                              Whole-repository orientation
/onboard --depth expert               Returning-contributor overview
/onboard --depth newcomer "billing"   Focused onboarding
/walkthrough how billing works        Interactive explanation
/tour billing                         Guided tour of one area
/glossary                             Grounded project terminology
/reindex                              Refresh since the recorded commit
```

### Optional deterministic indexing

Python 3 runs the utilities. Install tree-sitter and only the language packages you need in your preferred Python environment, for example:

```bash
python3 -m pip install tree_sitter tree_sitter_python tree_sitter_javascript \
  tree_sitter_typescript tree_sitter_go tree_sitter_java
```

Without tree-sitter, the indexer can use Python's standard-library parser for Python files. The onboarding workflow can also fall back to file searches. See the [script guide](.bob/skills/repo-cartographer/scripts/README.md) for indexing and verification commands.

## Try the walkthroughs

Download or clone the repository, then open either HTML file in a browser; GitHub's file view displays the source.

- [Compass walkthrough](examples/walkthrough-compass.html): explore the coordinator, worker, packet assembly, and refresh flow. Click diagram nodes to inspect details and drill into subflows.
- [Docling walkthrough](examples/walkthrough-docling.html): a reference example explaining document conversion in the upstream [Docling project](https://github.com/docling-project/docling). Its recorded source revision is `b613414`; the snippets and described code belong to that project.

There is no frontend build step. These single-file examples load Mermaid, highlight.js, and fonts from external services, so they require internet access as shipped. The walkthrough skill describes a local-vendoring fallback for offline use.

## Repository guide

| Location | Purpose |
| --- | --- |
| [`.bob/custom_modes.yaml`](.bob/custom_modes.yaml) | Onboarding coordinator and read-only explorer |
| [`.bob/commands/`](.bob/commands/) | Five user-facing commands |
| [`.bob/skills/repo-cartographer/`](.bob/skills/repo-cartographer/) | Exploration workflow, symbol indexer, and citation checker |
| [`.bob/skills/onboarding-packet/`](.bob/skills/onboarding-packet/) | Packet assembly and Markdown templates |
| [`.bob/skills/walkthrough/`](.bob/skills/walkthrough/) | Interactive HTML generation patterns |
| [`.bob/skills/change-digest/`](.bob/skills/change-digest/) | Changes since a recorded commit |
| [`.bob/skills/glossary-builder/`](.bob/skills/glossary-builder/) | Contextual terminology |
| [`.bob/rules/`](.bob/rules/) | Grounding, context management, output boundaries, and expertise adaptation |
| [`AGENTS.md`](AGENTS.md) | Coordination and provenance contracts |

## Project status and limitations

Compass is a hackathon prototype. Its generated guides need human review, and the complete workflow depends on IBM Bob's supported mode schema, tool permissions, and delegation behavior.

- Citation checks validate locations, not meaning. A document with no recognized citations can pass. The current checker also has a known limitation with paths beginning with a dot, including `.bob/`.
- The indexer skips hidden directories and uses simplified `.bobignore` matching. Static parsing cannot resolve all dynamic behavior; language coverage depends on installed parsers.
- The current refresh command compares committed revisions; uncommitted edits are not a reliable refresh trigger.
- Example citations are illustrative and may be stale. Validate them against the matching source checkout, especially for the external Docling example.
- The first onboarding run explores the repository; later refreshes require a previous provenance stamp. Context isolation is the main benefit, rather than parallel execution speed.

## Development context

The original project was designed with IBM Bob in Plan mode and authored in Advanced mode. Bob helped seed the onboarding contract, refine the skills and rules, and test component wiring. Team attribution is preserved from the original submission.
