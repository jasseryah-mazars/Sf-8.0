# Forms

The **Form component** is where three earlier stages meet: it renders through
**Twig**, checks input through **Validation**, and is wired through the
**service container** and the **EventDispatcher**. A Symfony form is not an HTML
`<form>` helper — it is a bidirectional data-mapping engine that turns a PHP
object into HTTP-friendly strings, and turns submitted strings back into a typed
object, dispatching events at every step.

This stage teaches the component from the outside in: create a form, handle a
submission, understand the *three data representations* (model / normalized /
view), then drill into the extension points — types, transformers, events and
type extensions — that the Expert exam loves.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [Templating (Twig)](../twig/index.md) · [Validation](../validation/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★★ |
    | **Dependencies** | Twig (7), Validation (8), DI + Events (3–4) |
    | **Revision priority** | **High** |
    | **Est. time** | 5–6 h |

## Why this stage matters

Forms compose almost everything you have learned. `FormFactory` is a service;
form types are services tagged `form.type`; the submit flow is a chain of
`FormEvents`; validation runs through a form extension; rendering is a Twig
theme. The exam probes the **seams** between these: the order of form events,
which direction a data transformer runs, what `handleRequest` actually inspects,
and how CSRF tokens are generated and checked. Learn the data-flow mental model
and the rest is detail.

## Micro-chapters

Work through them roughly in order:

- [ ] [Creating forms](creation.md) — `createForm`, form type classes,
  `buildForm`, `configureOptions`, `createFormBuilder`, `data_class`.
- [ ] [Handling submissions](handling.md) — `handleRequest`, `isSubmitted`,
  `isValid`, `getData`, the request→model flow, POST-redirect-GET.
- [ ] [Form types & the type hierarchy](types.md) — built-in vs custom,
  `getParent`, option resolution, `ResolvedFormType`.
- [ ] [Rendering with Twig](rendering.md) — `form()`, `form_start`/`form_end`,
  `form_row`/`form_widget`/`form_label`/`form_errors`/`form_help`, `form_rest`.
- [ ] [Form theming](theming.md) — `form_theme`, built-in themes, overriding
  blocks, block-name resolution.
- [ ] [CSRF protection](csrf.md) — how it works, the options, **stateless CSRF**
  (8.x), manual tokens.
- [ ] [File uploads](file-upload.md) — `FileType`, `UploadedFile`,
  `mapped => false`, moving files, `File`/`Image` constraints.
- [ ] [Built-in types catalogue](built-in-types.md) — the core, non-Doctrine
  field types and their key options.
- [ ] [Data transformers](data-transformers.md) — `DataTransformerInterface`,
  model↔norm↔view, model vs view transformers, `TransformationFailedException`.
- [ ] [Form events](events.md) — `FormEvents`, dynamic modification, subscribers.
- [ ] [Type extensions](type-extensions.md) — `AbstractTypeExtension`,
  `#[AsFormTypeExtension]`, `getExtendedTypes`.

## How to study it

1. Read [creation](creation.md) and [handling](handling.md) together — they give
   you the whole round-trip.
2. Internalise the **three data representations** (covered in
   [handling](handling.md) and [transformers](data-transformers.md)); everything
   else hangs off that.
3. Memorise the **two event sequences** in [events](events.md) — a guaranteed
   exam question.
4. Skim [rendering](rendering.md)/[theming](theming.md), then finish with the
   power tools: [transformers](data-transformers.md) and
   [type extensions](type-extensions.md).

---

<small>Related: [Templating](../twig/index.md) ·
[Validation](../validation/index.md) ·
[Web Security Fundamentals](../php-web-security/web-security.md) ·
[Controllers](../controllers/index.md)</small>
</content>
</invoke>

## Official References

- [Symfony documentation — Forms](https://symfony.com/doc/current/forms.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
