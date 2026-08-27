# Appendices — Out of Syllabus

!!! danger "Hors syllabus officiel Symfony 8.0"
    Every chapter under this section is explicitly **excluded from the official
    Symfony 8 certification syllabus**. They are kept here — physically separated
    from the certification content — as optional, additional/enrichment reading
    for readers who want the full picture of a related Symfony component. None
    of it is tested in generated exams, counted toward official syllabus
    coverage, or scored in the quiz bank's official statistics.

## Why these exist at all

Each topic below sits right next to an in-scope chapter that mentions it in
passing (ESI is the third fragment-rendering strategy alongside `render()` and
`render_hinclude()`; the PHPUnit Bridge is what Symfony's own test suite uses
for deprecation collection; the Lock component is a natural "what about
distributed locking" question after Cache). Moving them here — rather than
deleting them — keeps that curiosity satisfied without ever mixing them into
graded, in-scope material. See `specs/TraceabilityMatrix.md`'s
"Out-of-scope / Additional Learning" section for the row-by-row justification.

## Contents

| Topic | Related in-scope chapter | Why it's excluded |
|---|---|---|
| [Edge Side Includes (ESI)](esi.md) | [HTTP Caching](../../http-caching/index.md), [Templating (Twig) → Controller Rendering](../../twig/controller-rendering.md) | Not named in the official syllabus's HTTP Caching sub-topics |
| [PHPUnit Bridge](phpunit-bridge.md) | [Automated Tests](../../testing/index.md) | Not named in the official syllabus's Automated Tests sub-topics |
| [Lock Component](lock.md) | [Miscellaneous](../../miscellaneous/index.md) | Not named in the official syllabus's Miscellaneous sub-topics |

---

<small>Related: [Learning Dashboard](../../index.md) · [Traceability Matrix](https://github.com/jasseryah-mazars/Sf-8.0/blob/master/specs/TraceabilityMatrix.md)</small>
