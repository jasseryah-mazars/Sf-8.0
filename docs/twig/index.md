# Templating (Twig)

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Custom Extension](../labs/twig.md)** — a step-by-step TD with test-first guidance and a reference solution.

Twig is Symfony's default template engine: a compiled, sandboxed, auto-escaping
language that turns `.html.twig` files into optimised PHP classes. This stage
covers the syntax, the security model (auto-escaping), inheritance and reuse, the
`app` global, the Symfony-provided filters/functions (`path`, `asset`, `trans`,
`render`), and the tooling (`dump`) — always through the lens of *what the engine
compiles to and why*.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | [Controllers](../controllers/index.md), [PHP API](../php-web-security/php-api.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stage 5 (Controllers) |
    | **Revision priority** | **Medium** |
    | **Est. time** | 3–4 h |

## Why this stage matters

The exam rarely asks you to *write* a full template; it asks whether you know
what a construct **does**, when auto-escaping fires, the difference between
`path()` and `url()`, what `app.user` returns when nobody is logged in, and how
`render(controller(...))` interacts with the fragment sub-system. Understanding
that Twig **compiles to PHP** (via `Twig\Environment`, cached under
`var/cache/`) demystifies performance, escaping and debugging in one stroke.

## Micro-chapters

- [Twig Syntax](syntax.md) — `{{ }}`, `{% %}`, `{# #}`, variables, expressions,
  operators, tests, precedence, whitespace control.
- [Auto-Escaping](auto-escaping.md) — the HTML strategy, escape contexts, `|raw`,
  `|e('js'|'css'|'url'|'html_attr')`, `autoescape` blocks, security rationale.
- [Template Inheritance](inheritance.md) — `extends`, `block`, `parent()`,
  multi-level inheritance, `use` (horizontal reuse) vs `extends`.
- [Global Variables](globals.md) — the `app` global (`app.user`, `app.request`,
  `app.session`, `app.flashes`, `app.environment`, `app.debug`), custom globals.
- [Filters & Functions](filters-functions.md) — built-ins (`date`, `format`,
  `merge`, `default`, `json_encode`, `path`, `url`…) and custom ones via a
  Twig extension / `#[AsTwigFilter]` / `#[AsTwigFunction]`.
- [Template Includes](includes.md) — `include` tag/function, `embed`, `with`,
  `only`, `ignore missing`.
- [Loops & Conditions](loops-conditions.md) — `for` (the `loop` variable),
  `if`/`elseif`/`else`, the `for … else` clause, tests.
- [URL Generation](urls.md) — `path()` vs `url()`, passing parameters.
- [Controller Rendering](controller-rendering.md) — `render(controller(...))`,
  `render_esi`, fragments, when to embed a controller.
- [Translations & Pluralization](translations.md) — the `trans` filter/tag,
  parameters, ICU MessageFormat pluralization, domains.
- [String Interpolation](interpolation.md) — `"#{...}"`, `~` concatenation,
  `format`/sprintf.
- [Assets Management](assets.md) — the `asset()` function and asset versioning
  (AssetMapper & Encore are out of scope).
- [Debugging Variables](debugging.md) — `dump()` / `{% dump %}`, the debug
  extension, `{{ dump() }}` vs the profiler.

## How to study this stage

1. Start with [Syntax](syntax.md) and [Auto-Escaping](auto-escaping.md) — the two
   most heavily tested topics.
2. Learn the [`app` global](globals.md) cold; its members appear in many stems.
3. Practise [inheritance](inheritance.md) + [includes](includes.md) hands-on.
4. Treat [URL generation](urls.md) and [translations](translations.md) as the
   bridges to the [Routing](../routing/index.md) and Intl stages.

---

<small>Previous stage: [Routing](../routing/index.md) · Next stage: [Forms](../forms/index.md)</small>

## Official References

- [Symfony documentation — Creating and Using Templates (Twig)](https://symfony.com/doc/8.0/templates.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
