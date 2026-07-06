# String Interpolation

!!! tip "In a nutshell"
    Build strings three ways: `#{expr}` interpolation (double quotes only), `~`
    concatenation, and the `format` (sprintf) filter. Exam hook: `~` joins as strings
    while `+` adds numbers, and `~` has lower precedence than arithmetic.

!!! example "Real-world analogy"
    Think of assembling a form letter. `#{...}` interpolation is the mail-merge field — but
    the merge only fires on the official letterhead (double-quoted strings); type it on plain
    scratch paper (single quotes) and the field prints as literal ink. The `~` operator is
    stapling sheets end to end: everything, numbers included, becomes just more paper (text).
    The `+` operator is a pocket calculator that genuinely adds figures. And because you must
    finish the sums before you can staple the results together, the calculator always runs
    before the stapler (`~` has the lower precedence).

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Interpolate expressions in double-quoted strings with `#{...}`.
    - [ ] Concatenate with the `~` operator and know how it differs from `+`.
    - [ ] Format strings with the `format` filter (sprintf).

    **Syllabus:** `Templating (Twig) → String interpolation` ·
    **Level:** Advanced ·
    **Est. time:** 15 min ·
    **Prerequisites:** [Twig Syntax](syntax.md)

---

## Theory

Three ways to build a string from parts:

```twig
{# 1. interpolation — double quotes only #}
{{ "Hello #{name}, you have #{count} items" }}

{# 2. concatenation with ~ #}
{{ "Hello " ~ name ~ "!" }}

{# 3. format filter (sprintf) #}
{{ "Hello %s, %d items"|format(name, count) }}
```

- **`#{...}`** evaluates a Twig expression inside a **double-quoted** string.
- **`~`** joins values as strings (numbers are cast to string).
- **`format`** applies `sprintf` placeholders (`%s`, `%d`, `%.2f`, `%1$s`).

!!! question "Predict first"
    What does `{{ 1 + 2 ~ 3 }}` produce — `6`, `"123"`, or `"33"`?

??? note "Reveal"
    `"33"`. `+` binds **tighter** than `~`, so it evaluates as `(1 + 2) ~ 3` →
    `3 ~ 3` → the string `"33"`. `~` concatenates (casting to string); `+` is
    arithmetic — they are not interchangeable.

## Deep Dive — how it works internally

Interpolation is a **lexer** feature: inside a `"..."` string, `#{` opens an
embedded expression that the lexer tokenises and the parser compiles into a
concatenation. It works **only** in double quotes — single-quoted strings are
literal, so `'#{x}'` prints the raw text.

`~` compiles to PHP string concatenation (`.`) after casting each operand to
string, which is why `1 ~ 1` is `"11"` while `1 + 1` is `2`. `~` sits *below*
arithmetic in precedence (see [Syntax](syntax.md)), so `1 + 1 ~ "x"` is `"2x"`.

`format` and its cousin **`replace`** live in `Twig\Extension\CoreExtension`.
`format` calls PHP `vsprintf` under the hood; `replace` does keyed substitution:
`{{ "%name%"|replace({ '%name%': n }) }}`.

```mermaid
flowchart LR
    A["\"a #{x} b\""] --> L[Lexer detects #{ }]
    L --> E[Expression token x]
    E --> C["compile: 'a ' ~ x ~ ' b'"]
    C --> O[echo]
```

!!! note "Source reference"
    `Twig\Lexer` (string interpolation), `Twig\Extension\CoreExtension` (`format`) —
    [twigphp/Twig `3.x`](https://github.com/twigphp/Twig/blob/3.x/src/Lexer.php).

## Configuration & code

=== "Interpolation vs concat"

    ```twig
    {% set name = 'Ada' %}
    {{ "Hi #{name}" }}      {# Hi Ada #}
    {{ 'Hi #{name}' }}      {# Hi #{name}  — single quotes: literal #}
    {{ "sum: #{1 + 2}" }}   {# sum: 3 — full expression allowed #}
    ```

=== "format & replace"

    ```twig
    {{ "%s scored %d%%"|format(player, score) }}
    {{ "Price: $%.2f"|format(amount) }}
    {{ "Hello %who%"|replace({ '%who%': name }) }}
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `#{}` for readable inline values | Long `~` chains that hurt legibility |
| `format` for numeric/padding needs | Manual rounding via concatenation |
| `~` to join a couple of parts | `+` to "join" strings (it's arithmetic) |
| Double quotes for interpolation | Expecting `'…#{x}…'` to interpolate |

## When (not) to use it / alternatives

Reach for `#{}` when embedding one or two values reads best; use `~` for simple
joins; use `format`/`replace` when you need padding, precision, or reusable
placeholders (translation strings use `%name%` placeholders — see
[Translations](translations.md)).

!!! danger "Certification traps"
    - Interpolation `#{}` works **only in double-quoted** strings.
    - `~` is concatenation; `+` is **addition** — `"1" + "2"` is `3`, `"1" ~ "2"`
      is `"12"`.
    - `~` has **lower precedence** than `+`/`*`, so arithmetic happens first.
    - `#{...}` is unrelated to Twig's `{{ }}` — it lives *inside* a string literal.

!!! warning "Common mistakes"
    - Single-quoting an interpolated string and wondering why `#{name}` prints
      literally.
    - Using `+` to concatenate and getting `0` or a type error.

## Exercises

1. **(Basic)** Build `"Order #42 (paid)"` from `id = 42` and `status = 'paid'`
   using interpolation.
2. **(Intermediate)** Same string using only `~`.
3. **(Advanced)** Format a price to two decimals with a currency suffix using
   `format`.

??? success "Solutions"

    **1.** Combine a literal `#` with interpolation:
    `{{ "Order #" ~ "#{id} (#{status})" }}` — or, cleanest, use `format`:
    `{{ "Order #%d (%s)"|format(id, status) }}`.

    **2.** `{{ "Order #" ~ id ~ " (" ~ status ~ ")" }}`.

    **3.** `{{ "%.2f €"|format(amount) }}`.

## Certification questions

??? question "Q1. Where does `#{...}` interpolation work?"
    - [x] A. Only inside double-quoted strings ✅
    - [ ] B. In any string
    - [ ] C. Only inside `{% %}`
    - [ ] D. Only in single-quoted strings

    **Why:** The lexer only interpolates within `"..."`. **Ref:**
    [String interpolation](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation).

??? question "Q2. What is `{{ 1 + 2 ~ 3 }}`?"
    - [x] A. `"33"` ✅
    - [ ] B. `"123"`
    - [ ] C. `6`
    - [ ] D. `"15"`

    **Why:** `+` binds tighter than `~`: `(1 + 2) ~ 3` → `3 ~ 3` → `"33"`. **Ref:**
    [operators](https://twig.symfony.com/doc/3.x/templates.html#other-operators).

??? question "Q3. Which filter applies sprintf-style formatting?"
    - [x] A. `format` ✅
    - [ ] B. `sprintf`
    - [ ] C. `printf`
    - [ ] D. `interpolate`

    **Why:** `|format(...)` wraps `vsprintf`. **Ref:**
    [format filter](https://twig.symfony.com/doc/3.x/filters/format.html).

## Key takeaways

- `#{expr}` interpolates inside **double-quoted** strings only.
- `~` concatenates (string cast); `+` is arithmetic.
- `~` has lower precedence than arithmetic.
- `format` = sprintf; `replace` = keyed substitution.

## Last-minute revision

!!! tip "Cheat sheet"
    - `"hi #{name}"` (double quotes) · `'hi #{name}'` = literal.
    - `a ~ b` join · `a + b` add.
    - `"%s %d"|format(a, b)` · `"%x%"|replace({'%x%': v})`.

## Connections

- **Depends on:** [Twig Syntax](syntax.md) — `~` vs `+` and their precedence come straight from the operator table.
- **Reused in:** [Translations](translations.md) — translation messages use `%name%` placeholders, the same substitution idea as `format`/`replace`.
- **Confused with:** [Filters & Functions](filters-functions.md) — `format` is a filter (`|format`), not string syntax.

## Official References
- [Twig — string interpolation](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)
- [Twig — format filter](https://twig.symfony.com/doc/3.x/filters/format.html)
- [Twig source — Lexer](https://github.com/twigphp/Twig/blob/3.x/src/Lexer.php)

## Confidence check

I'm ready when I can:

- [ ] explain **why** `~` and `+` differ and when to reach for `#{}` vs `format`
- [ ] build a string three ways (interpolation, `~`, `format`) in Symfony 8
- [ ] debug `#{name}` printing literally inside a single-quoted string
- [ ] spot the trick answer on `~`/`+` precedence (e.g. `1 + 2 ~ 3`)
- [ ] explain that `#{}` is a lexer feature living inside a double-quoted literal

---

<small>Related: [Twig Syntax](syntax.md) · [Filters & Functions](filters-functions.md) · [Translations](translations.md)</small>
