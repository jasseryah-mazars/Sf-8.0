# SymfonyCasts-Style Enrichment Brief (shared)

You add two focused, additive blocks to specific chapters. Goal: teach like
SymfonyCasts (intuition + analogy + "why before how") **without** bloating the
mobile-first micro-chapters or duplicating existing sections.

## Read first
- The target chapter (it already has: In-a-nutshell TL;DR, Theory, Deep Dive,
  Common Mistakes, Certification traps, code, revision — **do not duplicate these**).
- `docs/_meta/CONVENTIONS.md`.

## Block 1 — Real-world analogy (add to EVERY target chapter)

Place an admonition **right after the `!!! tip "In a nutshell"` block** (or after
the objectives if no TL;DR exists):

```
!!! example "Real-world analogy"
    <2–4 short lines: one vivid, accurate real-life analogy that builds intuition
    before the mechanics. Tie each analogy element to the real Symfony concept.>
```

Guidance: DI ≈ restaurant kitchen/ordering; EventDispatcher ≈ airport control
tower / newsroom; Security firewall ≈ building security desk; HTTP ≈ postal
mail; Voter ≈ panel of judges; DataTransformer ≈ currency exchange booth;
Messenger ≈ post office sorting + courier; container compile ≈ IKEA flat-pack
pre-assembly. Pick the clearest; keep it honest (don't break the mental model).

## Block 2 — Null behavior (ONLY where null/empty/missing data is real)

If the concept can meet `null` / empty / missing data (e.g. `getUser()`,
`$request->query->get()`, `tryFrom()`, form/model data, container/param lookups,
value resolvers, optional deps, cache miss, nullable returns), add a subsection
**inside or right after the Deep Dive**:

```
### Null behavior

<what null means here · why it appears · how Symfony handles it internally
(named method/return type) · what happens if null is passed · how to handle it
safely (nullsafe `?->`, `??`, typed nullable, guards) · the common null bug>

!!! note "Null in real life"
    <one-line real-life analogy: null = missing package at delivery / empty form
    field / unknown visitor at the security desk / missing recipe ingredient>
```

Skip Block 2 entirely for pure-theory/config topics where null is not meaningful
(licensing, release cadence, naming conventions) — say so in your report; do NOT
invent contrived null content.

## Hard rules
- **Additive only** — never remove/shorten/duplicate existing content
  (`specs/AuditPolicy.md`). Do not restructure the chapter.
- Symfony 8 / PHP 8.4. Any complete `<?php` snippet must compile (`php -l`).
- Friendly-but-expert SymfonyCasts tone; short paragraphs; mobile-legible.
- Do not touch `mkdocs.yml`, quiz, specs, or other areas.

## Report
List chapters given an analogy, chapters given a Null-behavior block, and any
where you deliberately skipped Null (with reason).
