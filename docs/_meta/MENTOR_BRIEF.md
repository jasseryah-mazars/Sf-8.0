# Mentor-Layer Brief (shared)

Add the learning-graph + confidence + active-recall layer to an area's chapters.
Additive only; keep it concise and mobile-friendly. Read `docs/_meta/CONVENTIONS.md`.

## Every chapter (all areas) — add THREE compact blocks

**1. Active-recall prompt** — place it inside/just before the Deep Dive, as:

```
!!! question "Predict first"
    <A one-line "what do you think happens / which is correct?" prompt tied to the
    concept. Then reveal in a collapsible:>

??? note "Reveal"
    <2–4 lines answering it, pointing at the mechanism.>
```

**2. Connections** — near the end (before References), as a `## Connections` section:

```
## Connections

- **Depends on:** [Chapter](../area/file.md) — one clause why.
- **Reused in:** [Chapter](../area/file.md) — where this shows up again.
- **Confused with:** [Chapter](../area/file.md) — the distinction in one clause.
```

Use real relative links to existing chapters. 2–4 bullets total; skip a line if
genuinely N/A.

**3. Confidence check** — the final section before the `Related` footer:

```
## Confidence check

I'm ready when I can:

- [ ] explain **why** this exists and what problem it solves
- [ ] implement it in Symfony 8
- [ ] debug the common failure
- [ ] spot the wrong answer in a trick question
- [ ] explain the internal behaviour
```

Tailor the five bullets to the chapter's concept (don't leave them generic).

## Critical areas ONLY (architecture, dependency-injection, security, messenger)

For the flagship chapters of these areas, ALSO add (where they add real value —
skip if forced):

- `!!! info "Expert note"` — a detail seniors know that beginners miss.
- `??? example "Debugging story"` — a realistic bug → how it was diagnosed → fix →
  how to avoid. (Collapsible to protect length.)
- `??? abstract "Source-code tour"` — 3–6 bullets naming the key Symfony classes
  involved and how they collaborate (FQCNs), for that chapter's concept.

## Hard rules

- Additive only — never remove/shorten existing content. Symfony 8 / PHP 8.4.
- Any complete `<?php` snippet must compile (`php -l`). Keep blocks short (mobile).
- Do NOT add video links/durations (a curated, verified list lives in
  `docs/resources.md`); link there if useful.
- Edit only your area's `docs/<area>/*.md` (skip `index.md`). Don't touch nav/quiz/specs.

## Report
Chapters given Connections + Confidence + Predict; Critical-area chapters given
Expert note / Debugging story / Source-code tour; anything skipped and why.
