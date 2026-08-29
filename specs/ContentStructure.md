# Content Structure

The anatomy of the content: what a micro-chapter contains, how files are named and
linked, which admonitions mean what, and the size targets that keep the platform
mobile-first. This is the normative companion to
[`docs/_meta/CHAPTER_TEMPLATE.md`](../docs/_meta/CHAPTER_TEMPLATE.md) and
[`CONVENTIONS.md`](../docs/_meta/CONVENTIONS.md).

## 1. Two content units

| Unit | File | Purpose |
|---|---|---|
| **Area index** | `docs/<area>/index.md` | Landing page: intro + stage metadata + chapter checklist |
| **Micro-chapter** | `docs/<area>/<sub-topic>.md` | One syllabus sub-topic, taught end-to-end |

Everything else (Home, Roadmap, Exam Guide, Revision Hub) is a **landing/aggregation
page** that links into these units and does not teach new syllabus content.

## 2. Anatomy of a micro-chapter

The template section order is mandatory. Delete a section only when genuinely
inapplicable, with an HTML comment saying why.

| # | Section | Markdown | Purpose |
|---|---|---|---|
| 1 | Title | `# <Chapter Title>` (one H1) | Page title |
| 2 | Learning objectives | `!!! abstract` | Measurable goals + syllabus map, level, time, prereqs |
| 3 | Theory | `## Theory` | Progressive, define-before-use explanation |
| 4 | Deep Dive | `## Deep Dive — how it works internally` | FQCNs, execution flow, extension points, trade-offs, ≥1 diagram + source note |
| 5 | Configuration & code | `## Configuration & code` | Same concept across `=== "PHP Attributes"` / `"YAML"` / `"Console"` tabs |
| 6 | Best practices & anti-patterns | `## Best practices & anti-patterns` | ✅/❌ two-column table |
| 7 | When (not) to use / alternatives | `## When (not) to use it / alternatives` | Decision guidance |
| 8 | Certification traps | `!!! danger` | Subtle exam-tested distinctions |
| 9 | Common mistakes | `!!! warning` | Frequent errors + correct approach |
| 10 | Exercises | `## Exercises` + `??? success "Solutions"` | Applied tasks with hidden solutions |
| 11 | Certification questions | `## Certification questions` (`??? question`) | Inline self-test, collapsible, with Why + ref |
| 12 | Key takeaways | `## Key takeaways` | 3–6 bullets |
| 13 | Last-minute revision | `!!! tip "Cheat sheet"` | Glanceable condensed facts |
| 14 | References | `## References` | `doc/8.0` + `blob/8.0` links |
| 15 | Related | `<small>Related: …</small>` | 2–4 relative cross-links |

## 3. Anatomy of an area index

`docs/<area>/index.md` restates, from [Roadmap.md](Roadmap.md), the stage's:
**prerequisites, expected level, difficulty, dependencies, revision priority**,
a 2–4 sentence intro, and a bullet list linking **every** sub-chapter in study
order. It uses `!!! abstract` for the metadata block and benefits from Material's
`navigation.indexes` (the folder's landing page).

## 4. Naming conventions

- **Folders:** kebab-case topic area matching the Traceability Matrix
  (`php-web-security`, `dependency-injection`, `http-caching`, `miscellaneous`).
- **Files:** kebab-case sub-topic, `.md` (`compiler-passes.md`, `value-resolvers.md`).
  File stems match the Matrix paths exactly.
- **Index:** always `index.md` (never `README.md`) so `navigation.indexes` works.
- **Quiz:** `quiz/<area>.yml`, one per area, same stem as the folder.
- **Headings:** one `# H1` per file; sections `##`; sub-sections `###` (max depth 3,
  matching `toc_depth: 3`).
- **Anchors:** rely on auto-generated slugs; do not hand-author IDs.

## 5. Cross-linking rules

- **Relative links only** — `../security/voters.md`, never absolute site URLs or
  bare paths. They must resolve both in the built site and on GitHub, and are
  enforced by `mkdocs build --strict`.
- Link to a **file**, not a directory (`../http/index.md`, not `../http/`).
- Every chapter ends with a `Related:` line of **2–4** cross-links.
- Every major concept links out to **official docs** (`doc/8.0`); internals get
  a `!!! note "Source reference"` with a `blob/8.0` source link.
- **Cross-reference instead of duplicating.** If a concept is taught elsewhere,
  link it rather than re-explaining (keeps files small and single-sourced).
- Landing pages link **into** chapters; chapters link **sideways** to related
  chapters and **up** to their area index where useful.

## 6. Admonition taxonomy

One meaning per admonition type, used consistently platform-wide:

| Admonition | Type | Meaning |
|---|---|---|
| `!!! abstract` | Objectives | Learning objectives + syllabus metadata block |
| `!!! note` | Source ref / aside | "Source reference" to Symfony source, factual notes |
| `!!! tip` | Cheat sheet | Last-minute revision, condensed recall facts |
| `!!! info` | Aside | Useful context that is not a warning |
| `!!! warning` | Common mistakes | Frequent errors and the correct approach |
| `!!! danger` | Certification traps | Subtle, exam-tested distinctions and gotchas |
| `??? success` | Solutions | Collapsible exercise solutions (hidden by default) |
| `??? question` | Self-test | Collapsible inline certification questions |
| `???+` | Expanded collapsible | Same, but open by default (use sparingly) |

Do not repurpose an admonition type for another meaning.

## 7. Diagram guidance

- Use fenced ```mermaid blocks (rendered via `pymdownx.superfences`).
- At least one diagram whenever a **flow, lifecycle, or hierarchy** exists.
- Prefer `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`.
- **≤ ~12 nodes**, label edges, keep legible on a phone. Split a big diagram rather
  than shrink it into illegibility.
- Diagrams complement prose; never carry load-bearing facts that appear nowhere
  else in text (accessibility + searchability).

## 8. Code block rules

- Standalone PHP starts with `<?php` then `declare(strict_types=1);`.
- Snippets **compile**: real `use` imports, valid types, no `// ...` breaking an
  expression. Attributes first (`#[Route]`, `#[AsCommand]`, `#[AsEventListener]`).
- Show config in **tabs** (PHP Attributes / YAML / Console; XML only when relevant).
- Config files carry their real path in a line-1 comment (`# config/services.yaml`).
- Console fences use ```console with a leading `$`.

## 9. Size targets

| Target | Value |
|---|---|
| Micro-chapter length | 150–450 lines (split if longer) |
| Paragraphs | Short; one idea each |
| Tables | 2–4 columns (must render on a phone) |
| Diagrams | ≤ ~12 nodes |
| Heading depth | ≤ 3 (`toc_depth: 3`) |
| Idea per section | One |

Oversized files are a smell: prefer two focused micro-chapters and cross-link them.

## Related specs

[Specification](Specification.md) · [Requirements](Requirements.md) ·
[Architecture](Architecture.md) · [LearningStrategy](LearningStrategy.md) ·
[DefinitionOfDone](DefinitionOfDone.md) · [ReviewChecklist](ReviewChecklist.md).
