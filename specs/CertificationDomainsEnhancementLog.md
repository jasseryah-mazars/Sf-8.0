# Certification Domains — Enhancement Log

_Execution record for `specs/CertificationDomainsEnhancementPlan.md`. One entry per topic,
appended as the work actually runs. Lot 1: `PHP & Web Security`, branch `master`._

Verification convention used throughout: the rendered documentation sites are
egress-blocked in this environment, so every claim is verified at the canonical git source
(`php/doc-en`, `symfony/symfony@8.0`, `symfony-docs@8.0`, `twigphp/Twig@3.x`) and every
cited URL is confirmed to resolve there by `tools/check_doc_refs_resolve.py` before it is
written. The one authority with no git source — `certification.symfony.com` — stays
unverifiable, and no syllabus-wording claim is upgraded to "verified".

---

## Tooling — prerequisites for the lot

**Commit `dbc355e`** — Mermaid validation and the topic agent.

- `tools/validate_mermaid.py` + `tools/_mermaid_validate.js`: parse **and** render every
  ```mermaid block with the real engine in headless Chromium. `mkdocs build --strict`
  cannot catch a broken diagram — MkDocs only copies the fenced text and Mermaid renders in
  the visitor's browser — so a syntax error previously shipped green.
- Version contract: `tools/package.json` pins `mermaid@11.17.2`; the validator refuses to
  run on a mismatch.
- Two constraints forced the design away from the requested `mermaid-cli` pin:
  `@mermaid-js/mermaid-cli@11.17.2` **does not exist** (mermaid-cli does not track mermaid
  core; its latest is `11.16.0`), and the site's `unpkg.com/mermaid@11` is both an unpinned
  range and blocked here. Validating with the library is also strictly better — it is the
  same engine the page runs.
- Implementation notes: the ESM build is a 30 KB stub that lazy-imports `./chunks/*.mjs` and
  cannot resolve them from a blob URL, so the driver loads the self-contained UMD bundle;
  Playwright is resolved from the global install via `NODE_PATH` because a local install
  expects a Chromium build this image does not ship.
- `.claude/agents/certification-domain-expert.md` — the repo's first agent.

**Repo-wide Mermaid baseline (425 diagrams): 5 broken.**

| File | Line | Cause |
|---|---|---|
| `docs/php-web-security/web-security.md` | 143 | **fixed** — `;` is a statement separator in sequence diagrams |
| `docs/php-web-security/web-security.fr.md` | 146 | same bug — **not fixed**, `.fr.md` is out of scope this mission |
| `docs/miscellaneous/error-handling.md` | 135 | lexical error — outside lot 1 |
| `docs/miscellaneous/error-handling.fr.md` | 142 | same — outside lot 1 |
| `docs/twig/interpolation.md` | 127 | parse error line 2 — outside lot 1 |
| `docs/twig/interpolation.fr.md` | 168 | same — outside lot 1 |

These were shipping "Syntax error in text" to readers before this lot began. The one inside
lot 1's English scope is fixed; the rest are reported with exact locations rather than
silently touched outside scope.

**Commit `03d80ff`** — `tools/check_doc_refs_resolve.py`: resolves every cited
`symfony.com/doc/8.0`, `php.net/manual`, `symfony/symfony/blob/8.0` and `twig.symfony.com`
URL against its canonical git source, so an invented or mistyped URL fails. Cached;
`--offline` replays the cache so CI never depends on egress.

**Mermaid pinned on the site.** `mkdocs-material` hardcodes
`typeof mermaid == "undefined" ? load("https://unpkg.com/mermaid@11/...")`, an unpinned
major range and a single point of failure that `specs/SiteQualityReport.md` had already
flagged. Because it only fetches when `mermaid` is undefined, loading our copy first wins.
`tools/vendor_mermaid.py` copies the pinned build to `docs/assets/mermaid.min.js` and
refuses to run on a version mismatch, which is what makes "the site and the validator use
the same engine" a guarantee rather than a hope. Trade-off accepted deliberately:
`navigation.instant` is disabled in this repo, so the 3.4 MiB file is an eager load
(~1 MB gzipped, browser-cached for the visit) instead of Material's lazy CDN fetch. 66% of
English pages carry a diagram, and the alternative was an unverifiable, unpinned dependency.

`tools/check_mermaid_render.py` + `tools/_mermaid_render_check.js` verify the **built site**
in real Chromium at desktop and mobile viewports: one `<svg>` per `.mermaid` block, no
`.mermaid-error`, no visible "Syntax error in text", no mermaid console error, and **no
external mermaid request** — the last being what proves the vendored copy is in use.

---

## Topic 1 — `interfaces` (Interfaces & Type Declarations)

**Commit `30d4b33`.** Status: **done**.

**Files read:** `interfaces.md`, its 11 quiz-bank questions in `quiz/php-web-security.yml`,
its entries in the generated `docs/exams/php-web-security.md` and
`docs/revision/flashcards/php-web-security.md`, and `docs/php-web-security/index.md`.

**Files written:** `interfaces.md` (rewritten), `interfaces-exercises.md`,
`interfaces-exam.md`, `interfaces-flashcards.md` (new), plus the index row.

**Factual error corrected.** The comparison table stated `Properties | No (constants only)`.
`php/doc-en` `language/oop5/interfaces.xml` states: *"As of PHP 8.4.0, interfaces may also
declare properties. If they do, the declaration must specify if the property is to be
readable, writeable, or both."* Since this repo's baseline **is** PHP 8.4, the table was
wrong for its own target version. Corrected, with the accompanying asymmetry: a `readonly`
property satisfies `{ get; }` but never `{ set; }`.

**Verified depth added** (each fetched before citing):

- Property variance and its 8.4 exception — properties are invariant because reads want
  covariance and writes want contravariance; only abstract/virtual properties requiring a
  single operation may vary (`language/oop5/variance.xml`).
- The manual's two-interfaces-different-signatures case, the hardest legal construct in the
  topic: widest parameter, narrowest return is the only signature satisfying both.
- Version boundaries that function as distractors: interface constants overridable **since
  8.1.0** (forbidden before), intersection **8.1**, `never` **8.1**, DNF **8.2**, union
  **8.0** — union and intersection being one version apart is a routine swap.
- Variance violations are **link-time** fatals, not runtime errors: they take the whole
  application down and cannot be caught.

**Questions:** 4 migrated out of the lesson (none lost) + 11 added = **15**, covering single,
multiple, true/false, code analysis, execution order, debugging, edge case, scenario and
trap. Every distractor explained individually.

**Exercises:** 7, following discover → implement → inspect → change one variable → diagnose
→ edge case → Expert challenge. Hints and solutions collapsed.

**Flashcards:** 21, one idea per card, answers collapsed.

**Diagrams:** the `classDiagram` was replaced by a variance decision `flowchart` that carries
the chapter's actual rule; validated with mermaid 11.17.2.

**Checks:** `check_topic_journey` OK (15 questions, 7 exercises, 21 cards) ·
`validate_mermaid` OK · `lint_php` 386 snippets, 0 failures · `check_placeholders` OK ·
`check_editorial_structure` OK · `check_doc_refs_resolve` 8/8 citations resolve ·
`mkdocs build --strict` exit 0, 0 warnings.

---

## Topics 2–13

Dispatched to `certification-domain-expert`, one topic per invocation, in nav order:
`php-api`, `oop`, `attributes`, `closures`, `abstract-classes`, `exceptions`, `traits`,
`enums`, `namespaces`, `extensions`, `spl`, `web-security`. Entries are appended below as
each completes and passes its checks.

`attributes` and `enums` carry only 2 quiz-bank questions each and need substantive new exam
content rather than migration alone.
