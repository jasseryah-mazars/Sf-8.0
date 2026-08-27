# Navigation Experience Audit

_Generated 2026-08-27, branch `master`, commit at generation time: see
`specs/RemediationLog.md`'s "Master as the project's reference branch" and
subsequent entries. Real inspection of the files listed below, not a
generic checklist filled in from memory._

## Method

Read, in full or in relevant part: `docs/index.md`/`.fr.md`, `docs/roadmap.md`,
`docs/exam-guide/index.md`, `docs/revision/index.md`, `docs/exam-simulator.md`,
`mkdocs.yml`'s complete `nav:` tree, `docs/assets/quiz.js`,
`docs/assets/{code.css,a11y.js}`, `docs/_meta/CHAPTER_TEMPLATE.md`, one
representative area index (`docs/dependency-injection/index.md`) and one leaf
chapter (`docs/dependency-injection/autowiring.md`), and `docs/revision/flashcards/index.md`.

## Finding 1 — The homepage is a technical table, not a guided entry point

`docs/index.md` opens reasonably (one intro paragraph, a "What this is"
admonition) but its main content **is** a dense reference table: 16 rows ×
9 columns, mixing English UI vocabulary with French-only column headers in
the `.fr.md` version's own English section title ("## Learning Dashboard"
stays untranslated even on the French page — see Finding 5), status codes
like `9/9 PASS` / `5 TO VERIFY` that assume the reader already knows what
"PASS" means in this project's own tooling vocabulary, and abbreviations
(`TP`, `Cours`) a first-time visitor has no way to decode without reading
the tip box above the table first. There is no single, unmissable primary
action ("start here") — the page's first real CTA-shaped element is buried
inside a numbered "How to use this platform" section two-thirds down the
page. A beginner lands here and has to *parse a spreadsheet* before doing
anything.

**Verdict:** fails the mission's own bar ("pas de page d'accueil réduite à
une liste technique de liens") — this is close to exactly that description.

## Finding 2 — No single guided step-by-step path; three partial ones instead

Three different pages each contain a *fragment* of a step-by-step path,
none of them the obvious first thing a beginner opens:
- `docs/index.md`'s own "How to use this platform" section (5 numbered
  steps + a Mermaid flowchart) — reasonable content, badly placed (below
  the giant table, not above it).
- `docs/roadmap.md`'s "The study loop" (4 steps, repeated per stage) — a
  *meta*-loop for people already inside a stage, not a first-visit guide.
- `docs/exam-guide/how-to-use.md` — a dedicated page, one click removed
  from the Exam Guide index, not linked from the homepage at all except
  via the generic "Exam Guide" nav entry.

None of these says, in one clickable action, "click here to start" — they
all describe a path in prose the reader must then go execute manually by
finding the right links elsewhere on the page.

## Finding 3 — No resume/progress mechanism visible to the reader, despite
one already existing under the hood

`docs/assets/quiz.js` already implements a real, working, privacy-respecting
local mechanism: per-area attempt stats in `localStorage` (`sfq-stats-v1`),
used internally to power a "Drill my weaknesses" button inside the quiz
tool itself. **This is never surfaced anywhere else** — not on the
homepage, not as a "continue where you left off" prompt. The mission's
explicit fallback rule ("si le mécanisme existant permet de conserver la
progression, afficher 'Continuer là où je me suis arrêté'") is directly
actionable here: extend what already exists rather than invent a new
mechanism or a backend.

## Finding 4 — Deep, mostly-flat top-level navigation (`navigation.tabs` +
`navigation.sections` makes this worse, not better)

`mkdocs.yml`'s `nav:` has **~20 top-level entries**: Home, Exam Guide,
Roadmap, Exam Simulator, Glossary, Resources, Tags, then all **15 official
topic areas each as their own top-level entry** (each expanding to its
full chapter list), then Labs, Source Tours, Chapter Exams, Revision Hub,
Appendices. Because `navigation.tabs` is enabled, every one of those ~20
entries renders as its own tab across the top of the page — an
overwhelming first impression, and exactly the "aucun besoin de connaître
l'arborescence interne" bar this mission sets is not met: a new visitor
has to already understand that "the 15 areas are the syllabus" to make
sense of a 20-tab bar mixing meta-tools and content areas at the same
level.

**Concrete, low-risk fix:** nest the 15 areas under one "Domaines de
certification" parent (they already share equal footing conceptually —
this is a pure regrouping, no content moves, no URLs change), and group
the remaining meta-tools into the 6 other buckets the mission specifies.
See Phase 5 implementation below.

## Finding 5 — French/English mixing on the French homepage

`docs/index.fr.md` translates almost everything (table content, tip-box
prose, area descriptions) but leaves several **section headings and
admonition titles in English**: `## Learning Dashboard`, `!!! abstract
"What this is"`. This is a real, fixable instance of the "mélange
français/anglais" the mission asks to check for — not a fabricated
finding: confirmed by direct diff against the English original.

Separately, `mkdocs.yml` has **no `nav_translations` configured** for the
`i18n` plugin at all — the French build's sidebar/tab labels are 100%
identical to the English ones (e.g. a French reader sees the tab labelled
"Home", not "Accueil"). `mkdocs-static-i18n` supports partial
`nav_translations` (untranslated entries fall back to the original label,
which is itself an acceptable, explicit fallback per the mission's own
Phase 6 rule) — not configuring it at all means the fallback is silently
100% of the nav, not a deliberate, bounded gap.

**Scope decision, stated honestly:** translating the labels of all ~500
nav entries (every chapter, every lab, every exam) is not attempted this
pass — that is a large, low-marginal-value undertaking (chapter titles are
mostly proper nouns / already-common technical terms Symfony developers
recognize in English regardless of UI language). What **is** done: add
`nav_translations` for the handful of new top-level structural labels this
mission's Phase 5 introduces, plus the 15 area names (a bounded, reused-
everywhere list), so the *structural* navigation (the part a beginner
actually needs to orient) is in French on the French site. This is a
partial, explicit translation — not a claim of full nav parity.

## Finding 6 — Stale numbers undermining trust in the guided experience

`docs/revision/index.md` states "**1,179** tap-to-reveal cards" and a
"1,179-question bank" twice — the live figures (`tools/validate_quiz.py`,
re-run this session) are **1,292 questions** and (per
`docs/revision/flashcards/index.md`, itself regenerated this session)
**1,292 flashcards**. This is exactly the kind of stale claim that erodes
a beginner's trust the moment they cross-check two pages. Not part of the
Phase 3 checklist verbatim, but surfaced by it and fixed as part of this
pass (see Phase 4/6 below) since a "guided, trustworthy" experience cannot
coexist with a number that's provably wrong on inspection.

## Finding 7 — What already works well (not rebuilt, reused)

- **`navigation.footer` is already enabled** in `mkdocs.yml` — every
  content page already gets an automatic, title-labelled Previous/Next
  link from Material itself, satisfying "chapitre précédent / chapitre
  suivant" sitewide with zero per-chapter edits needed.
- **Every chapter already opens with "In a nutshell" + "Real-world
  analogy" + "Learning objectives"** (checked via `CHAPTER_TEMPLATE.md`
  and a live chapter) — the "ce que vous allez apprendre" requirement is
  already met content-wise; it doesn't need new prose, only a scalable way
  to surface quick actions around it (see Phase 4 below — a sitewide
  injected quick-actions bar rather than 176 manual chapter edits).
  Every area **index** page additionally already has a "Stage at a
  glance" info box (Prerequisites/Level/Difficulty/Dependencies/Revision
  priority) and a "🧪 Practice this area" callout linking to its lab.
- **No broken links, no orphan pages** — confirmed by re-running
  `tools/check_editorial_structure.py` and `tools/check_placeholders.py`
  before starting this audit (0 violations both).
- **Mobile:** `docs/assets/code.css`'s existing `white-space: pre-wrap`
  rule already prevents the most common mobile failure mode (horizontal
  code-block overflow) sitewide; P2-03's real-Chromium audit (375px
  viewport) found 0 horizontal-overflow violations across all 5 sampled
  pages once its own methodology bug was fixed (see
  `specs/SiteQualityReport.md`) — not re-litigated here.
- **Quiz filtering by area already exists** in `docs/assets/quiz.js`, just
  not URL-addressable yet (Finding 8) — the underlying capability a
  per-domain "Se tester" button needs is already built.

## Finding 8 — No direct, one-click "test this specific topic" action

`docs/assets/quiz.js`'s area filter is a set of checkboxes the user must
tick by hand after opening the simulator — there is no way for a link
elsewhere on the site (an area index page, a chapter, the new dashboard)
to deep-link straight into "practice questions for *this* area only."
Fixable without a redesign: read a `?area=<name>` query parameter at
mount time and pre-select just that area (implemented below).

## Decisions carried into implementation

1. New guided dashboard (`docs/index.md` + `.fr.md`) — Phase 4.
2. `mkdocs.yml` nav regrouped per the mission's 8-bucket order — Phase 5.
   Mapping decision: "Commencer" (bucket 2) is the existing "Exam Guide"
   section relabelled — its content (format, scoring, how-to-use,
   strategy) already *is* "what a beginner needs before starting,"
   avoiding a near-duplicate new page.
3. New `docs/assets/progress.js`: extends the existing `sfq-stats-v1`
   mechanism with a lightweight "last page visited" record (same
   `localStorage`, no backend, no new dependency) and injects a universal
   quick-actions strip (back to domain / test this topic, URL-derived, no
   per-chapter edits) — Phase 4.7/4.4.
4. `docs/assets/quiz.js`: `?area=` URL param support for direct-link
   "test this topic" actions — Phase 4.5/4.7.
5. Fix the two stale `1,179` mentions in `docs/revision/index.md`.
6. Partial `nav_translations` (structural labels + 15 area names only,
   stated as partial, not full parity) — Phase 6.
7. **Not attempted, stated honestly:** individually rewriting all 176
   chapters with a hand-authored "Prerequisites / Back to domain / Test
   this topic" block each. The combination of (a) already-existing
   per-chapter Learning-objectives content, (b) already-enabled
   `navigation.footer`, and (c) the new sitewide quick-actions bar (item 3
   above) covers the same user-facing need without a 176-file editing
   pass this session's budget cannot respectably absorb with the quality
   bar the rest of this mission has held to (every prior "regenerate
   wholesale" temptation in this project's history has produced
   unreviewed drift — see `specs/RemediationLog.md`'s repeated
   historical-drift entries).
