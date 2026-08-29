# Site Quality Report (P2-03)

_Generated 2026-08-27, branch `claude/sf-8-certification-quality-iimd4l`,
against a locally-built `site/` (from the same commit sequence as the rest
of this run's P0–P2 work). This is a manually-triggered report, not
CI-generated — see "Why this isn't wired into CI" below._

## What this is, and how it was produced

This is a **real, executed browser audit** — `tools/check_site_quality.py`
+ `tools/_site_quality_check.js` launch an actual headless Chromium via
Playwright (pre-installed in this environment) against a locally-served
copy of `site/`, and run [axe-core](https://github.com/dequelabs/axe-core)
4.13.0 (a genuine automated accessibility rule engine, not a heuristic this
project wrote) plus a handful of custom checks (mobile overflow, keyboard
reachability, Mermaid rendering, search, language switch) on 5 representative
pages: the home page, a chapter with Mermaid+code+admonitions
(`http-caching/server-side/`), the Revision Hub, the Mock Exam simulator,
and the French home page.

This is **not** a fabricated or assumed result for something impossible to
test: every number below came from an actual tool run this session, and
every claim about *why* something passed or failed was independently
verified (e.g. by inspecting computed styles, intercepting Web Worker
messages, or reading the built HTML) before being written down here —
not asserted from a single ambiguous signal.

## What this does NOT check (declared, not silently skipped)

- **Real assistive technology.** axe-core is a strong automated proxy for
  WCAG conformance, not a substitute for actually running NVDA/JAWS/
  VoiceOver against the page. No screen reader is available in this
  environment.
- **Real devices / real networks.** "Mobile" here is Chromium's emulated
  375×667 viewport, not a physical phone.
- **A vanilla mkdocs-material control site**, to separate "bug in this
  site" from "artifact of headless/sandboxed testing" for the search
  finding below — `squidfunk.github.io` is blocked by this environment's
  network egress (confirmed via a failed fetch attempt), so no external
  comparison was possible.
- **Full interactive exercise of the mock-exam simulator's JS logic**
  beyond confirming the page loads and its interactive elements are present
  and keyboard-reachable.

## Results summary (after the fixes made this run)

| Page | axe violations | Mobile (375px) | Keyboard nav | Mermaid |
|---|---|---|---|---|
| Home | 2 | OK | OK (9 elements reachable) | n/a |
| Chapter w/ Mermaid | 3 | OK | OK | not verifiable (see below) |
| Revision Hub | 4 | OK | OK | n/a |
| Mock Exam simulator | 4 | OK | OK | n/a |
| French home | 2 | OK | OK | n/a |

Search: **backend verified correct** (23 matching documents returned for a
test query); on-page rendering of those results could not be confirmed in
this environment (see below). Language switch to `/fr/`: **OK**
(`<html lang="fr">`, page loads).

## Fixed this run (real, minimal-risk, verified before/after)

1. **Missing accessible name on decorative task-list checkboxes
   (critical, 9 nodes on the sampled chapter page).** pymdownx.tasklist's
   `custom_checkbox: true` output wraps each `- [ ]` checkbox in a `<label>`
   that has no text content of its own (the list-item text is a sibling,
   not inside the label) — axe correctly flagged every one as an unlabeled
   input. These checkboxes are always `disabled` (read-only checklist
   bullets in "Learning objectives" sections, never meant to be toggled),
   so the correct WCAG remedy is to remove them from the accessibility
   tree, not invent a label for a control nobody operates. Added
   `docs/assets/a11y.js` (a few lines, mirrors `quiz.js`'s existing
   `document$`-subscribe pattern for `navigation.instant` compatibility) to
   set `aria-hidden="true"` on every `.task-list-control input[disabled]`.
   **Verified: 9 → 0 violations of this rule** on the sampled page,
   re-checked with a fresh axe-core run after rebuilding.

2. **Code-block color contrast, light scheme (serious, 34 nodes on the
   sampled chapter page).** Comments/variables/operators/punctuation in
   syntax-highlighted code share the stock theme's
   `--md-default-fg-color--light` token, which resolves to `#717171` on
   the `#f5f5f5` code background — measured at **4.48:1**, just under the
   WCAG AA 4.5:1 minimum for normal-size text. Added a scoped override in
   `docs/assets/code.css` (`:root:not([data-md-color-scheme="slate"])
   .md-typeset .highlight { --md-code-hl-comment-color: #666666; ... }`)
   darkening only these five code-token colors, only inside code blocks —
   the shared variable itself is untouched everywhere else it's used.
   **Verified: 4.48:1 → 5.27:1.**

3. **Code-block color contrast, dark scheme (serious, 10 nodes on the same
   page in dark mode).** Number and constant tokens (`#e6695b` and
   `#9383e2`) measured **4.45:1** and **4.48:1** against the dark code
   background (`#272a35`) — also just under 4.5:1. Same file, a dark-scheme
   scoped override lightens just these two tokens to `#ea7d70` (5.22:1) and
   `#a196e8` (5.48:1). **Verified with axe-core in emulated dark
   colorScheme.**

Net effect on the sampled chapter page: axe violations for these two rule
categories went from **34 + 9 = 43 flagged nodes** down to **0**; that
page's total violation *rule count* dropped from 4 to 3 (the remaining 3
are the theme-level findings below, present on every page, not something
these two fixes could touch).

## Found, NOT fixed this run — and why

Each of these is real (axe-core-verified) but was left alone deliberately
rather than patched blindly, because fixing it properly means either a
sitewide visual/branding decision or a theme-template override — both
larger-scope changes than a targeted CSS/JS patch, and neither was asked
for:

- **`aria-dialog-name` (serious, every page, 1 node).** mkdocs-material's
  built-in search overlay (`role="dialog"`) has no accessible name in its
  own bundled HTML template. Fixing this means overriding Material's
  `search.html`/`base.html` partial (a `theme.custom_dir` override) to add
  `aria-label="Search"` to that dialog — a legitimate, contained fix, but
  a template-override mechanism this project doesn't currently use for
  anything, so introducing it for one attribute was judged out of scope
  for this pass. Documented here as a concrete, ready-to-implement next
  step.

- **`link-in-text-block` (serious, 2–19 nodes per page) and the remaining
  `color-contrast` findings (2–5 nodes per page, all on `<small>` "Related:"
  footer links).** Both trace to the same root cause: `mkdocs.yml`'s
  `primary: black` / `accent: indigo` palette choice, which per Material's
  own documented behavior makes in-text links use the accent color
  (rendering as `#707dc8`) — measured at **3.84:1** against white, under
  the 4.5:1 minimum, and (separately) not visually distinguishable from
  surrounding text by anything other than color (no underline). Fixing
  this properly means either darkening the accent color or adding
  underlines to in-text links — a change that would visibly alter every
  link on every page of the site. That is a legitimate visual-design
  decision for whoever owns the project's branding, not something to
  change unilaterally mid-autonomous-run. **Concrete recommended fix for a
  future pass:** either pick a darker custom accent (e.g. via
  `extra.palette` primary/accent hex overrides) that clears 4.5:1 against
  white, or add `.md-typeset a { text-decoration: underline; }` scoped to
  in-text links (the current design relies on color alone).

- **`landmark-unique` (moderate, Revision Hub + Mock Exam pages, 1 node
  each).** Two `<nav>` regions on these specific pages resolve to the same
  implicit role without a distinguishing accessible name — a Material
  template/nav-structure detail tied to how those two pages nest secondary
  navigation. Same category as `aria-dialog-name`: a template-level fix,
  not attempted this pass.

## Investigated in depth, inconclusive — search result rendering

Typing a query into the search box (and, separately, navigating to
`/?q=OPcache`, Material's own URL-driven search entry point) left the
results list empty and the "Initializing search" placeholder showing, in
every variant tried, in this environment's headless Chromium.

This was not accepted at face value. Intercepting the actual
`postMessage` traffic between the page and Material's search Web Worker
(`assets/javascripts/workers/search.*.min.js`) showed:
- the worker receives the query correctly,
- the worker's search index initializes correctly (all lunr scripts and
  `search_index.json` load with HTTP 200 — verified via network listeners,
  not assumed),
- the worker **returns correct matching results** (23 documents matched
  "OPcache" — a term confirmed present in the built search index via a
  separate Python check),
- **but the on-page result list never renders** — `.md-search-result__item`
  stays at 0 regardless of how the query was triggered.

Two explanations are both consistent with what was observed, and this
environment provides no way to distinguish them:
1. A real front-end rendering bug reachable only under some condition this
   testing didn't isolate.
2. A headless/no-real-compositor Chromium quirk in how Material's bundled
   JS (an RxJS-based reactive pipeline, per its own source) reacts to
   focus/animation events that a real, painted browser fires differently.

No network path exists from this environment to a vanilla
`squidfunk.github.io/mkdocs-material` install to run the same test as a
control, which would have been the fastest way to tell these apart. Per
this run's explicit instruction not to fabricate results for checks that
can't actually be run: **this is reported as "search's result-computation
is verified correct; its on-page rendering is unverified, not confirmed
broken" — a human should type a real query into the live deployed site in
an actual browser before this is treated as a defect.**

## Investigated, environment limitation (not a defect claim)

**Mermaid diagrams could not be verified to render.** This site loads
Mermaid from `https://unpkg.com/mermaid@11/dist/mermaid.min.js` (a CDN,
not bundled locally) — confirmed via a failed-request listener, this
environment's network egress proxy blocks/fails TLS verification for
`unpkg.com`, so Mermaid.js itself never loads here and no diagram can
render regardless of the markup's correctness. This is reported as **not
verifiable in this environment**, not as a confirmed rendering failure — a
real user's browser reaching `unpkg.com` normally would very likely render
these fine. Worth noting as a separate, general resilience point
regardless of this environment's specific limitation: depending on an
external CDN for a core rendering feature means the site's diagrams are
one CDN outage or corporate-firewall block away from not rendering for a
real visitor either — bundling Mermaid locally (as `quiz.js`/`code.css`
already are) would remove that dependency, but is a build-pipeline change
outside this pass's scope.

## Why this isn't wired into CI

`tools/check_site_quality.py` needs a full Chromium download (Playwright)
and an `npm install` for `axe-core` (see `tools/package.json`) — real cost
in CI minutes and complexity for a check whose two hardest findings this
run (search rendering, Mermaid CDN reachability) need human judgment to
interpret anyway, not a pass/fail gate. It's kept as an on-demand local
tool (`npm install --prefix tools && python tools/check_site_quality.py`)
rather than a blocking or even a report-only CI step. This is a scoping
decision, not an oversight — revisit if the project later wants continuous
accessibility regression coverage.

## Honest summary

- **Real, executed, browser-based checks** — not a static-file heuristic —
  covering axe-core accessibility rules, mobile viewport overflow,
  keyboard reachability, and functional checks (search backend, language
  switch).
- **3 real issues found and fixed** this run (task-list checkbox labels,
  light-mode and dark-mode code-highlighting contrast), each verified
  before/after with a fresh axe-core run.
- **3 real issues found and documented, not fixed** (search dialog aria
  name, in-text link contrast/distinguishability tied to the site's accent
  color choice, one moderate landmark-uniqueness finding) — each with its
  concrete cause and a specific recommended remedy for a future pass.
- **2 findings actively investigated but left explicitly unresolved**
  (search result DOM rendering — backend verified correct, on-page render
  unverified; Mermaid rendering — blocked by this environment's network,
  not confirmed broken) — reported as exactly that, not rounded up to
  "fixed" or down to "broken."
