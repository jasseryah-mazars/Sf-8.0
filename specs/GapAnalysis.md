# Gap Analysis

**Date:** 2026-07-06 · **Baseline:** `ThomasBerends/symfony-certification-preparation-list`
(master = Symfony 7.0) · **Target:** Symfony 8.0 Expert Certification.

## 1. What the source repository is

A curated **list of links**, not a learning resource:

- `readme.md` — table of contents mirroring the official syllabus.
- `topics/*.md` — 14 files, ~672 lines total. Each is a bulleted list of links to
  `symfony.com/doc/7.0/...`, `php.net`, and SymfonyCasts. No prose, no code, no
  diagrams, no exercises, no answers.
- Jekyll (`_config.yml`) for GitHub Pages; `contributing.md`; MIT `LICENSE`.

## 2. Gap summary

| Dimension | Source (7.0) | Required (8.0 platform) | Gap |
|---|---|---|---|
| Learning prose | None (links only) | Full theory per sub-topic | **100%** |
| Deep dives (internals) | None | Every concept | **100%** |
| Code examples | None | PHP 8.4 / SF8, attributes | **100%** |
| Diagrams (Mermaid) | None | Per flow/lifecycle | **100%** |
| Exercises + solutions | None | Every chapter | **100%** |
| Certification traps | None | Every chapter | **100%** |
| Last-minute revision | None | Every chapter + hub | **100%** |
| Practice questions | None | YAML bank + inline | **100%** |
| Navigation / search | Jekyll TOC | MkDocs Material | Rebuild |
| Smartphone readability | Poor (long files) | Micro-chapters | Rebuild |

**Conclusion:** this is a green-field authoring effort against a known syllabus,
not a prose migration. Only the *topic structure* is reused.

## 3. Version deltas (7.0 → 8.0) that change content

| Area | Change | Action |
|---|---|---|
| PHP baseline | 7.x/8.2 → **PHP 8.4+** | Rewrite "PHP API" around 8.3/8.4 features (typed class constants, `#[\Override]`, `json_validate()`, `new` in initializers, property hooks & asymmetric visibility context, DNF types, `readonly` classes). |
| Symfony version | 7.0 → 8.0 | All doc links → `doc/current`; source links → `blob/8.0`. Remove any 7.x-only guidance. |
| HTTP Caching | Reduced exam weight | Keep full coverage; note reduced weighting in revision priority. |
| Messenger | **Increased** exam weight | Expand Messenger to multiple sub-sections; raise revision priority. |
| Twig | 3.8 → current 3.x | Syntax chapter targets current Twig 3; flag any deprecations. |
| Deprecated APIs | Present in ecosystem | Ban across all content; show modern replacements only. |

## 4. Missing topics vs official syllabus

The source lists all 14 topic groups but provides no depth. Additionally the
platform explicitly **adds** these sub-chapters that the exam tests but the list
under-serves:

- Web Security fundamentals (XSS/CSRF/SQLi/session/HTTPS) under "PHP & Web Security".
- Custom validation constraints (constraint + validator pair).
- Messenger breakdown (buses, transports, middleware, stamps, retries, failure
  transport, worker lifecycle).
- Exam Guide (format, scoring, Advanced vs Expert, exam-day strategy).
- Revision Hub (master cheat sheet, trap index, memory aids, quiz).

## 5. Out of scope (must NOT be added)

Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore,
third-party bundles/bridges, and any component absent from the official syllabus.

## 6. Coverage tracking

100% syllabus coverage is enforced via [TraceabilityMatrix.md](TraceabilityMatrix.md).
The project is "done" only when every syllabus row maps to at least one shipped,
DoD-passing chapter.
