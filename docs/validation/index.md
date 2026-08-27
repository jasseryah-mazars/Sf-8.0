# Data Validation

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Custom Constraint](../labs/validation.md)** — a step-by-step TD with test-first guidance and a reference solution.

Symfony's `Symfony\Component\Validator` component decides whether a PHP value is
*acceptable* — a `NotBlank` name, a well-formed `Email`, an `IsTrue` terms
checkbox — and, when it is not, produces a structured
`Symfony\Component\Validator\ConstraintViolationList` you can render, serialise
or map back onto a form. Constraints are declared **declaratively** (PHP
attributes first) and enforced by a `ValidatorInterface` service that the
framework wires for you.

This stage teaches the constraint/validator model from the ground up: how
metadata is loaded, how scopes and cascading work, how groups and group
sequences steer *which* rules run and *in what order*, and how to build your own
constraints and violations. It is the direct prerequisite for
[Forms](../forms/index.md), which delegates all its validation here.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [Dependency Injection](../dependency-injection/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stage 4 (DI); pairs with [Forms](../forms/index.md) |
    | **Revision priority** | **Medium** |
    | **Est. time** | 3–4 h |

## Why this stage matters

Validation is a component the exam tests both at the *usage* level (which
built-in constraint, which option) and at the *mechanics* level (Default vs
`{ClassName}` group, group sequences, cascading with `Valid`). The subtleties —
not the catalogue — are where marks are won and lost. Get the mental model of
**metadata → context → violations** and everything else falls into place.

## Micro-chapters

Work through them in order:

- [ ] [PHP Object Validation](object-validation.md) — attributes on properties,
  getters and classes; `validate()` vs `validateProperty()`; how metadata loads.
- [ ] [Built-in Constraints](built-in-constraints.md) — the catalogue by
  category, focused on what the exam actually asks.
- [ ] [Validation Scopes](scopes.md) — property vs getter vs class constraints;
  cascading nested objects and collections with `#[Assert\Valid]`.
- [ ] [Validation Groups](groups.md) — the `Default` group, named groups, and
  the `Default` vs `{ClassName}` interplay.
- [ ] [Group Sequence](group-sequence.md) — `#[Assert\GroupSequence]`,
  stop-on-first-failure, and `GroupSequenceProvider`.
- [ ] [Custom Callback Validators](callbacks.md) — `#[Assert\Callback]` and using
  the `ExecutionContext` to build violations inline.
- [ ] [Custom Constraints](custom-constraints.md) — `Constraint` +
  `ConstraintValidator`, `getTargets()`, `validatedBy()`, `#[HasNamedArguments]`.
- [ ] [Violations Builder](violations-builder.md) — `buildViolation()`,
  `setParameter`/`atPath`/`setInvalidValue`/`setCode`, reading the list.

## How to study it

1. Start with [Object Validation](object-validation.md) — the core `validate()`
   flow and metadata loading underpin everything else.
2. Skim the [Built-in Constraints](built-in-constraints.md) catalogue, then learn
   [Scopes](scopes.md) so you know *where* a constraint may sit.
3. Master the trio the exam loves: [Groups](groups.md),
   [Group Sequence](group-sequence.md), and the Default/`{ClassName}` trap.
4. Finish with the extension points: [Callbacks](callbacks.md),
   [Custom Constraints](custom-constraints.md) and the
   [Violations Builder](violations-builder.md).

---

<small>Related: [Dependency Injection](../dependency-injection/index.md) ·
[Forms](../forms/index.md) · [Twig](../twig/index.md)</small>

## Official References

- [Symfony documentation — Validation](https://symfony.com/doc/8.0/validation.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
