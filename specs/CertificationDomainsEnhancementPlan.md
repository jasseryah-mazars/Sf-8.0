# Certification Domains — Expert Learning-Journey Enhancement Plan

_Lot 1: `PHP & Web Security` (13 topics). Established 2026-08-28 on branch `master`,
starting commit `2ff8000`, clean working tree._

## 1. What this changes

Each topic under `Certification Domains` becomes a four-file learning journey instead of a
single page that mixes lesson, a short exercise list, and a certification-question block:

```
docs/<domain>/<topic>.md              enriched Expert lesson
docs/<domain>/<topic>-exercises.md    guided practice, 7 stages
docs/<domain>/<topic>-exam.md         every certification question, answers hidden
docs/<domain>/<topic>-flashcards.md   active-recall deck, answers hidden
```

Reader path: **Read the lesson → Guided exercises → Topic exam → Flashcards → Next topic.**

**Existing slugs are preserved.** A slug is a foreign key shared by `subchapter:` in
`quiz/<domain>.yml`, the `SYLLABUS` table in `tools/gen_traceability_matrix.py`, the
`mkdocs.yml` nav entry, and the `.fr.md` sidecar. Renaming would break traceability and quiz
coverage for no pedagogical gain, so `interfaces.md` stays `interfaces.md` and gains
`interfaces-exercises.md`, `interfaces-exam.md`, `interfaces-flashcards.md`.

**No `.fr.md` file is created or modified in this lot** (explicit mission constraint).
Consequence, recorded rather than hidden: the French sidecars keep their pre-enrichment
content, and the three new activity files have no French counterpart, so the French site
falls back to English for them — the same behaviour `docs/exams/` already has.

## 2. Scope of lot 1

Only `docs/php-web-security/`. No other domain is touched.

## 3. Source-of-truth reachability (measured, not assumed)

The rendered documentation sites are blocked by this environment's egress proxy — confirmed
for both `curl` and `WebFetch`, which return `EGRESS_BLOCKED`. Their canonical git sources
are reachable, and that is where verification happens:

| Authority | Rendered site | Verified at |
|---|---|---|
| Symfony 8.0 documentation | `symfony.com/doc/8.0/` ❌ | `raw.githubusercontent.com/symfony/symfony-docs/8.0/<p>.rst` ✅ |
| Symfony 8.0 source | `github.com/…` 403 | `raw.githubusercontent.com/symfony/symfony/8.0/…` ✅ |
| PHP manual | `www.php.net` ❌ | `raw.githubusercontent.com/php/doc-en/master/…` ✅ |
| Twig 3.x docs | `twig.symfony.com` ❌ | `raw.githubusercontent.com/twigphp/Twig/3.x/doc/…` ✅ |
| Official syllabus | `certification.symfony.com` ❌ | **no git source — remains unverifiable** |

`symfony-docs@8.0` is genuinely version-pinned: `controller.rst` differs between `8.0` and
`7.4`. It is the exact text that renders at `symfony.com/doc/8.0/`.

The syllabus page has no public git mirror. `specs/OfficialSyllabusBaseline.md` keeps its
existing "tracks, but is not itself, the official syllabus" banner, and no syllabus-wording
claim is upgraded to "verified" in this lot.

## 4. Starting inventory (measured 2026-08-28)

| # | Topic | Lines | Lesson Q to migrate | Lesson exercises | Mermaid | Quiz-bank Q |
|---|---|---|---|---|---|---|
| 1 | `php-api` | 520 | 5 | 3 | 1 | 12 |
| 2 | `oop` | 392 | 4 | 2 | 1 | 11 |
| 3 | `attributes` | 417 | 4 | 2 | 1 | **2** |
| 4 | `interfaces` | 365 | 4 | 2 | 1 | 11 |
| 5 | `closures` | 332 | 4 | 2 | 1 | 11 |
| 6 | `abstract-classes` | 322 | 4 | 2 | 1 | 9 |
| 7 | `exceptions` | 377 | 4 | 2 | 1 | 11 |
| 8 | `traits` | 347 | 4 | 2 | 1 | 11 |
| 9 | `enums` | 408 | 4 | 2 | 1 | **2** |
| 10 | `namespaces` | 312 | 4 | 2 | 1 | 9 |
| 11 | `extensions` | 315 | 4 | 2 | 1 | 9 |
| 12 | `spl` | 442 | 5 | 2 | 1 | 12 |
| 13 | `web-security` | 382 | 5 | 2 | 1 | 13 |
| | **Total** | **4,931** | **55** | **27** | **13** | **123** |

Two distinct question pools, not to be confused:

- **55 in-lesson questions** under `## Certification questions`, hand-written. These migrate
  into `<topic>-exam.md`. Conservation is checked by count: nothing may be lost.
- **123 quiz-bank questions** in `quiz/php-web-security.yml`, which feed the *generated*
  `docs/exams/php-web-security.md` and `docs/revision/flashcards/php-web-security.md`. Those
  generated per-domain pages stay as they are; the new per-topic files sit alongside them.

`attributes` and `enums` carry only 2 quiz-bank questions each — both need substantive new
exam content, not just migration.

## 5. Tooling this architecture requires

Five real couplings were found before any content was touched. Each is a genuine breakage,
not housekeeping:

1. **`gen_revision_sheets.py` fails silently.** It regex-extracts `## Key takeaways` and
   `## Last-minute revision` from `docs/<area>/*.md`, and its `section()` returns `""` when a
   heading does not match — no error. Renaming either heading empties every revision sheet
   without warning. → both headings are kept in the lesson structure.
2. **`check_editorial_structure.py` fails CI on orphan pages.** Its carve-out covers only
   `exams/` and `revision/`, so each new activity file must be in `mkdocs.yml` nav or the
   carve-out must learn the three suffixes. Adding all four files per topic to nav would take
   `Certification Domains` from 184 to 691 entries under `navigation.tabs` — unusable. The
   lesson stays in nav; activities are reached from the lesson and the domain index.
3. **`final_audit.py` counts `Questions` as a universal marker.** Moving
   `## Certification questions` out of lessons would report a false regression. → it must
   resolve that marker against `<topic>-exam.md`.
4. **Mermaid is unverified by the existing pipeline.** `mkdocs build --strict` cannot catch a
   broken diagram: MkDocs only copies the fenced text, and Mermaid renders in the visitor's
   browser, so a syntax error ships green and shows `Syntax error in text` to the reader.
   → new blocking validator (§6).
5. **48 generated files carry hand-written `## 🧠 Pour les nuls` blocks** inserted by commit
   `2ff8000`. No generator emits that heading, so re-running any generator deletes them. They
   must move into the generator templates before any regeneration.

## 6. Mermaid validation

`tools/validate_mermaid.py` + `tools/_mermaid_validate.js` parse **and** render every
```mermaid block with the real engine in headless Chromium — never by regex. Two gates per
diagram: `mermaid.parse()` for grammar, then `mermaid.render()` to prove an `<svg>` is
produced and contains no `Syntax error in text`.

**Version contract.** `tools/package.json` pins `mermaid@11.17.2`, and the validator refuses
to run if the installed version differs. Two facts forced the design:

- `@mermaid-js/mermaid-cli@11.17.2` **does not exist** — mermaid-cli's versions do not track
  mermaid core, and its latest release is `11.16.0`. Pinning the CLI to 11.17.2 is impossible.
  Validating with the library itself is also strictly better: it is the same engine the page
  runs.
- The site currently loads `unpkg.com/mermaid@11/dist/mermaid.min.js` — an **unpinned** major
  range — and `unpkg.com` is blocked by the egress proxy here, so diagrams cannot render in
  this environment at all. Vendoring mermaid 11.17.2 into `docs/assets/` pins the version,
  removes the CDN single point of failure, and makes browser verification possible.

## 7. Per-topic method

1. Read every associated file in full: lesson, its quiz questions, its generated exam and
   flashcard entries, its lab.
2. Inventory concepts; compare against the syllabus baseline.
3. Verify each technical claim at an authority in §3, fetching the file before citing it.
4. Enrich the lesson; place references immediately after the block they support.
5. Create the exercises file (7 stages, hint and solution collapsed).
6. Migrate every in-lesson question to the exam file, then add the missing question types.
7. Create the flashcards file.
8. Repair or add diagrams; run the Mermaid validator on the topic.
9. Cross-check coverage: lesson concept → exercise → exam question → flashcard.
10. Update journey links and the domain index row.
11. Run targeted checks; fix failures.
12. Append a compact log entry; commit the topic.

## 8. Per-topic tracking

Status values: `pending` · `in progress` · `migrated` · `done`.

`migrated` in the Lesson column means the four-file contract holds — the questions and
exercises are in their own files, the journey links resolve — but the lesson itself still
carries its pre-lot depth. It is an honest half-step, not a synonym for done.

| # | Topic | Lesson | Exercises | Exam | Flashcards | Mermaid | Checks | Commit |
|---|---|---|---|---|---|---|---|---|
| 1 | `php-api` | done | done | done | done | done | green | see log |
| 2 | `oop` | done | done | done | done | done | green | see log |
| 3 | `attributes` | done | done | done | done | done | green | see log |
| 4 | `interfaces` | done | done | done | done | done | green | see log |
| 5 | `closures` | done | done | done | done | done | green | see log |
| 6 | `abstract-classes` | done | done | done | done | done | green | see log |
| 7 | `exceptions` | done | done | done | done | done | green | see log |
| 8 | `traits` | done | done | done | done | done | green | see log |
| 9 | `enums` | done | done | done | done | done | green | see log |
| 10 | `namespaces` | done | done | done | done | done | green | see log |
| 11 | `extensions` | done | done | done | done | done | green | see log |
| 12 | `spl` | done | done | done | done | done | green | see log |
| 13 | `web-security` | done | done | done | done | done | green | see log |

Execution detail per topic is recorded in `specs/CertificationDomainsEnhancementLog.md`;
the end-of-lot verification is in `specs/CertificationDomainsFinalAudit.md`.

## 9. Definition of done for lot 1

- 13 topics × 4 files = **52 files** present and non-empty.
- No lesson retains a `## Certification questions` section.
- Question conservation proved by count: 55 migrated, plus any added listed explicitly.
- Every answer, hint and solution inside a collapsed `???` block.
- A reference immediately after every explanation; zero `doc/current`.
- English everywhere except `## 🧠 Pour les nuls`.
- Every diagram parses and renders with mermaid 11.17.2; zero `Syntax error in text`.
- Journey links resolve in both directions; domain index updated.
- Full suite green, including `mkdocs build --strict`.
