# Filters & Functions

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Use the most exam-relevant built-in filters and functions correctly.
    - [ ] Distinguish a **filter** (`value|f`) from a **function** (`f(value)`).
    - [ ] Create custom filters/functions via a Twig extension and the
          `#[AsTwigFilter]` / `#[AsTwigFunction]` attributes.

    **Syllabus:** `Templating (Twig) → Filters & functions` ·
    **Level:** Advanced → Expert ·
    **Est. time:** 30 min ·
    **Prerequisites:** [Twig Syntax](syntax.md)

---

## Theory

A **filter** transforms a value with the pipe: `{{ price|round(2) }}`. Filters
chain left-to-right: `{{ name|lower|capitalize }}`. A **function** is called by
name and returns a value: `{{ max(a, b) }}`, `{{ path('home') }}`.

Common built-in **filters**:

| Filter | Purpose |
|---|---|
| `date('d/m/Y')` | format a date/`DateTimeInterface` |
| `format(a, b)` | `sprintf`-style interpolation |
| `merge({...})` | merge arrays/hashes |
| `default('x')` | fallback for undefined/null/empty |
| `json_encode` | JSON encode (escapes for HTML) |
| `length` `first` `last` `join(', ')` | collections |
| `escape`/`e` `raw` | escaping (see [Auto-Escaping](auto-escaping.md)) |
| `trans` | translation (see [Translations](translations.md)) |

Common built-in **functions**: `path()`, `url()`, `asset()`, `range()`, `max()`,
`min()`, `random()`, `include()`, `dump()`, `constant()`, `cycle()`.

## Deep Dive — how it works internally

Filters and functions are provided by **Twig extensions** —
`Twig\Extension\CoreExtension` (`date`, `merge`, `default`…) and Symfony bridge
extensions (`RoutingExtension` for `path`/`url`, `AssetExtension` for `asset`,
`TranslationExtension` for `trans`). Each is registered as a
`Twig\TwigFilter` or `Twig\TwigFunction` object.

```mermaid
flowchart LR
    E[Twig\\Environment] --> X1[CoreExtension]
    E --> X2[RoutingExtension]
    E --> X3[Custom AppExtension]
    X1 --> F1["TwigFilter 'date'"]
    X2 --> F2["TwigFunction 'path'"]
    X3 --> F3["TwigFilter 'price'"]
```

Key `TwigFilter`/`TwigFunction` options:

- **`is_safe: ['html']`** — output is trusted HTML, skip auto-escaping.
- **`needs_environment: true`** — first callable arg is the `Twig\Environment`.
- **`needs_context: true`** — receive the render context array.
- **`is_variadic: true`** — collect extra args into an array.
- **`deprecated`** — mark for the deprecation path.

At compile time Twig resolves the name to the callable and inlines the call in
the generated PHP, so filters/functions cost a normal function call at runtime.

!!! note "Source reference"
    `Twig\Extension\CoreExtension`, `Twig\TwigFilter`, `Twig\TwigFunction` —
    [twigphp/Twig `3.x`](https://github.com/twigphp/Twig/blob/3.x/src/Extension/CoreExtension.php).

### Custom filters/functions

Two equivalent registration styles in current Twig 3.x:

=== "AbstractExtension (classic)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Twig;

    use Twig\Extension\AbstractExtension;
    use Twig\TwigFilter;
    use Twig\TwigFunction;

    final class PriceExtension extends AbstractExtension
    {
        public function getFilters(): array
        {
            return [
                new TwigFilter('price', $this->formatPrice(...)),
            ];
        }

        public function getFunctions(): array
        {
            return [
                new TwigFunction('vat', $this->vat(...)),
            ];
        }

        public function formatPrice(float $n, string $currency = '€'): string
        {
            return number_format($n, 2, '.', ' ').' '.$currency;
        }

        public function vat(float $n, float $rate = 0.20): float
        {
            return round($n * (1 + $rate), 2);
        }
    }
    ```

=== "Attributes (Twig 3.x)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Twig;

    use Twig\Attribute\AsTwigFilter;
    use Twig\Attribute\AsTwigFunction;

    final class PriceRuntime
    {
        #[AsTwigFilter('price')]
        public function formatPrice(float $n, string $currency = '€'): string
        {
            return number_format($n, 2, '.', ' ').' '.$currency;
        }

        #[AsTwigFunction('vat')]
        public function vat(float $n, float $rate = 0.20): float
        {
            return round($n * (1 + $rate), 2);
        }
    }
    ```

With Symfony autoconfiguration, an `AbstractExtension` is auto-tagged
`twig.extension`, and classes using `#[AsTwigFilter]`/`#[AsTwigFunction]` are
registered automatically. Use `{{ 9.9|price }}` and `{{ vat(100) }}`.

!!! info "Runtime extensions"
    For heavy dependencies, put the logic in a **runtime** class (lazy-instantiated
    via `RuntimeExtensionInterface` / the attribute style) and reference it with a
    lightweight extension — the service is only built when the filter is actually used.

## Configuration & code

=== "Built-ins in action"

    ```twig
    {{ now|date('Y-m-d H:i') }}
    {{ 'Hello %s'|format(name) }}
    {{ {a: 1}|merge({b: 2})|json_encode }}
    {{ tags|default([])|join(', ') }}
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `is_safe` only for genuinely safe HTML | Marking user data safe |
| Runtime classes for costly deps | Injecting DB into an eager extension |
| Filters for value → value | Filters with side effects |
| `default([])` before `join` | `join` on possibly-undefined |

## When (not) to use it / alternatives

Add a custom filter when a transformation is **presentational and reused**. If it
needs a service or is business logic, compute it in PHP and pass the result.
Prefer functions when the call reads naturally (`path('x')`) and filters when it
transforms an existing value (`value|price`).

!!! danger "Certification traps"
    - `|` is a **filter**, `f()` is a **function** — `date` exists as both a
      filter *and* a function.
    - A custom filter returning HTML is auto-escaped unless declared
      `is_safe: ['html']`.
    - `default` also replaces **empty** values, not just undefined/null.
    - `needs_environment`/`needs_context` shift the callable's argument positions.

!!! warning "Common mistakes"
    - Forgetting to inject services into an *eager* extension slows every request —
      use a runtime.
    - Expecting `json_encode` output to be printable raw — it is HTML-escaped by
      default (use in `<script type="application/json">` or `|raw` carefully).

## Exercises

1. **(Basic)** Format `total` to two decimals and append `€`.
2. **(Intermediate)** Write a custom `excerpt` filter truncating to N chars.
3. **(Advanced)** Register the same `excerpt` using `#[AsTwigFilter]`.

??? success "Solutions"

    **1.** `{{ total|number_format(2, '.', ' ') }} €` (or a custom `price` filter).

    **2.** `new TwigFilter('excerpt', fn(string $s, int $n = 100) => mb_strlen($s) > $n ? mb_substr($s, 0, $n).'…' : $s)`.

    **3.** A method `#[AsTwigFilter('excerpt')] public function excerpt(string $s, int $n = 100): string` with the same body.

## Certification questions

??? question "Q1. Which attribute registers a custom Twig filter?"
    - [x] A. `#[AsTwigFilter]` ✅
    - [ ] B. `#[TwigFilter]`
    - [ ] C. `#[Filter]`
    - [ ] D. `#[AsFilter]`

    **Why:** Current Twig 3.x provides `Twig\Attribute\AsTwigFilter` (and
    `AsTwigFunction`). **Ref:**
    [Custom extensions](https://symfony.com/doc/current/templates.html#creating-a-twig-extension).

??? question "Q2. A custom filter returns `<b>x</b>`. Why does the page show escaped text?"
    - [ ] A. Twig never escapes filter output
    - [x] B. It must be declared `is_safe: ['html']` ✅
    - [ ] C. You must call `|raw` on the input
    - [ ] D. It's a bug

    **Why:** Filter output is auto-escaped unless marked safe. **Ref:**
    [is_safe](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping).

??? question "Q3. What does `{{ items|default([])|length }}` guarantee?"
    - [x] A. No error when `items` is undefined/empty ✅
    - [ ] B. Sorts items
    - [ ] C. Always returns 0
    - [ ] D. Escapes items

    **Why:** `default([])` supplies an empty array so `length` is safe. **Ref:**
    [default filter](https://twig.symfony.com/doc/3.x/filters/default.html).

## Key takeaways

- Filters (`|`) transform; functions (`f()`) return values.
- Built-ins live in `CoreExtension` + Symfony bridge extensions.
- Custom: `AbstractExtension` returning `TwigFilter`/`TwigFunction`, or
  `#[AsTwigFilter]`/`#[AsTwigFunction]`.
- Mark trusted HTML with `is_safe`; use runtimes for heavy deps.

## Last-minute revision

!!! tip "Cheat sheet"
    - `value|filter(args)` · `function(args)`.
    - Options: `is_safe`, `needs_environment`, `needs_context`, `is_variadic`.
    - Register: `getFilters()`/`getFunctions()` or `#[AsTwigFilter/Function]`.
    - `default` covers undefined **and** empty; `json_encode` is escaped.

## Official References
- [Official — Twig extensions](https://symfony.com/doc/current/templates.html#creating-a-twig-extension)
- [Twig — filters & functions reference](https://twig.symfony.com/doc/3.x/#reference)
- [Twig source — CoreExtension](https://github.com/twigphp/Twig/blob/3.x/src/Extension/CoreExtension.php)

---

<small>Related: [URL Generation](urls.md) · [Auto-Escaping](auto-escaping.md) · [Translations](translations.md)</small>
