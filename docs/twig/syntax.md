# Twig Syntax

!!! tip "In a nutshell"
    Twig has three delimiters — `{{ }}` prints, `{% %}` does, `{# #}` comments.
    Templates compile once to cached PHP classes, so rendering is cheap. Exam hook:
    `~` concatenates (not `+`), `//` is floor division, and filters bind tightest.

!!! example "Real-world analogy"
    Reading a Twig template is like performing from a script. `{{ … }}` are the
    lines you say **out loud** (printed to the audience), `{% … %}` are the stage
    directions that shape the scene but are **never spoken**, and `{# … #}` are the
    director's margin notes — for you only, never performed. The compile step is a
    one-time rehearsal; every show after is fast.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Distinguish the three Twig delimiters and what each compiles to.
    - [ ] Read expressions, operators, tests and their precedence correctly.
    - [ ] Control whitespace with `-` modifiers and the `spaceless` apply block.

    **Syllabus:** `Templating (Twig) → Twig syntax` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Controllers](../controllers/index.md)

---

## Theory

Twig has exactly **three delimiters**:

| Delimiter | Purpose | Compiles to |
|---|---|---|
| `{{ … }}` | **print** an expression | `echo …;` (through the escaper) |
| `{% … %}` | a **tag / statement** (control flow, blocks) | PHP control structures |
| `{# … #}` | a **comment** — never rendered | nothing |

```twig
{# a comment, stripped at compile time #}
<h1>{{ title }}</h1>
{% if items %}<p>{{ items|length }} item(s)</p>{% endif %}
```

### Variables & attribute access

`{{ user.name }}` resolves `user.name` in this order: `$user['name']`,
`$user->name`, `$user->name()`, `$user->getName()`, `$user->isName()`,
`$user->hasName()`. Use the **subscript** form `{{ user['name'] }}` to force an
array/`ArrayAccess` lookup, and `{{ attribute(obj, method, args) }}` when the
name is dynamic. A missing attribute yields `null` (or throws under `strict_variables`).

### Expressions & literals

Strings `"hi"`/`'hi'`, numbers `42`/`4.2`, booleans `true`/`false`, `null`,
arrays `[1, 2]`, hashes `{ key: 'v', (expr): 'v2' }`, and ranges `1..5`.

## Deep Dive — how it works internally

Twig is a **compiler**, not an interpreter. `Twig\Environment::render()` runs a
three-stage pipeline: **lex → parse → compile**.

```mermaid
flowchart LR
    S[Template source] --> L[Lexer<br/>Twig\\Lexer]
    L --> T[Token stream]
    T --> P[Parser<br/>Twig\\Parser]
    P --> A[AST: Twig\\Node\\ModuleNode]
    A --> C[Compiler<br/>Twig\\Compiler]
    C --> PHP[PHP class extends Twig\\Template]
    PHP --> Cache[(var/cache/…)]
```

- **Lexer** (`Twig\Lexer`) splits source into tokens using the delimiter regexes.
- **Parser** (`Twig\Parser`) + **token parsers** (`Twig\TokenParser\*`) build an
  abstract syntax tree of `Twig\Node\Node` objects. Each tag (`if`, `for`, `block`)
  has its own token parser.
- **Expression parser** (`Twig\ExpressionParser`) encodes the **operator
  precedence table** — this is *the* thing the exam probes.
- **Compiler** (`Twig\Compiler`) walks the AST and emits a PHP class extending
  `Twig\Template`, whose `doDisplay()` contains `echo` statements. It is written
  once to the cache (`Twig\Cache\FilesystemCache`, default `var/cache/<env>/twig`)
  and reused on every subsequent request — templates cost nothing to "parse" at
  runtime after the first compile.

!!! note "Source reference"
    `Twig\Environment`, `Twig\Lexer`, `Twig\Parser`, `Twig\Compiler` —
    [twigphp/Twig `3.x`](https://github.com/twigphp/Twig/blob/3.x/src/Environment.php).

### Operators & precedence

From **lowest** to **highest** binding:

| Group | Operators |
|---|---|
| ternary | `? :`, `?:`, `??` |
| logic | `or` → `and` → `not` |
| bitwise | `b-or` `b-xor` `b-and` |
| comparison | `==` `!=` `<` `>` `<=` `>=` `<=>` `in` `is` `matches` `starts with` `ends with` |
| string | `~` (concatenation) |
| additive | `+` `-` |
| multiplicative | `*` `/` `//` (floor div) `%` |
| power | `**` (right-assoc) |
| unary | `-` `+` `not` |

`{{ 2 + 3 * 4 }}` → `14`. `{{ "a" ~ 1 + 1 }}` → `a2` (`+` binds tighter than `~`).
Filters (`|`) bind tighter than any operator: `{{ -x|abs }}` is `-(x|abs)`.

### Tests

Tests use `is`: `{{ x is defined }}`, `is null`, `is empty`, `is even`/`odd`,
`is iterable`, `is same as(y)`, `divisible by(3)`, `constant('App\\Foo::BAR')`.
Negate with `is not`: `{% if x is not null %}`.

### Null behavior

Twig is deliberately null-tolerant. **Printing** `null` outputs an empty string,
never an error: `{{ missing }}` renders nothing. (With `strict_variables` on, an
*undefined* variable throws, but a variable that resolves to `null` still prints
empty.) Reading an attribute **on** `null` — `{{ user.name }}` when `user` is
`null` — yields `null` (again, empty on print) unless `strict_variables` is on.

Handle it explicitly with three tools:

- **`??`** — null-coalescing: `{{ count ?? 0 }}` replaces `null`/undefined only.
- **`|default`** — `{{ name|default('Anon') }}` replaces `null`, undefined **and**
  empty (`''`, `[]`).
- **tests** — `{% if x is defined %}`, `{% if x is null %}`, `is not null` to
  branch before you touch a value.

The classic bug: assuming `{{ a.b.c }}` throws when `a.b` is `null`. In lenient
mode it quietly prints empty and the typo only surfaces once `strict_variables`
is on — so keep it on in dev.

!!! note "Null in real life"
    A null variable is a blank line on a form: Twig leaves it empty and moves on
    rather than refusing the whole page.

## Configuration & code

=== "Twig template"

    ```twig
    {% set total = (price * qty)|round(2) %}
    {{ total ?? 0 }} — {{ name|default('Anonymous') }}
    {% if user is defined and user.active %}✓{% endif %}
    ```

=== "PHP (rendering)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;

    final class HomeController extends AbstractController
    {
        #[Route('/', name: 'home')]
        public function index(): Response
        {
            return $this->render('home/index.html.twig', [
                'title' => 'Hello',
                'items' => ['a', 'b'],
            ]);
        }
    }
    ```

### Whitespace control

- `{{- x -}}` / `{%- … -%}` trim whitespace on the marked side.
- `{% apply spaceless %}…{% endapply %}` removes whitespace **between HTML tags**
  (the old `{% spaceless %}` tag was removed in Twig 3).

```twig
<ul>
{%- for i in items -%}
  <li>{{ i }}</li>
{%- endfor -%}
</ul>
```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Keep logic in PHP; templates present | Business logic / DB calls in Twig |
| Use `{# #}` for template comments | `<!-- -->` (leaks to output) |
| Rely on precedence, add `()` for clarity | Guessing operator binding |
| `{% apply spaceless %}` | The removed `{% spaceless %}` tag |

## When (not) to use it / alternatives

Twig is the default for HTML/text. For pure PHP responses use `JsonResponse`.
Enable `strict_variables` in dev to catch typos; keep it lenient (default) in
prod so a missing optional variable renders as empty rather than erroring.

!!! danger "Certification traps"
    - `{{ }}` **prints and escapes**; `{% %}` **does not print**. Confusing them
      is a classic distractor.
    - `~` is string concatenation, **not** `+`. `1 + 1` is `2`; `1 ~ 1` is `"11"`.
    - `//` is **floor division**, `/` is float division: `{{ 7 // 2 }}` → `3`.
    - Filters bind tighter than arithmetic: `{{ 1 + 2|abs }}` is `1 + (2|abs)`.
    - `{% spaceless %}` no longer exists — use `{% apply spaceless %}`.

!!! warning "Common mistakes"
    - Using `<!-- -->` for notes: it renders to the client. Use `{# #}`.
    - Assuming `{{ a.b }}` throws on missing `b` — it returns `null` unless
      `strict_variables` is on.

## Exercises

1. **(Basic)** Predict the output of `{{ 2 ~ 3 + 4 }}` and explain the precedence.
2. **(Intermediate)** Write a snippet that prints `count` if defined, else `0`,
   using both `??` and `default`.
3. **(Advanced)** Access a property whose name is stored in `key` on object `obj`.

??? success "Solutions"

    **1.** `27`. `+` binds tighter than `~`, so it is `2 ~ (3 + 4)` → `2 ~ 7` →
    the string `"27"`.

    **2.** `{{ count ?? 0 }}` (null-coalescing on undefined) and
    `{{ count|default(0) }}` (also treats empty as default). `??` only replaces
    `null`/undefined; `default` also replaces empty values (`''`, `[]`) as well as
    undefined/null.

    **3.** `{{ attribute(obj, key) }}` — dynamic attribute access.

## Certification questions

??? question "Q1. What does `{{ 7 // 2 }}` output?"
    - [ ] A. `3.5`
    - [x] B. `3` ✅
    - [ ] C. `4`
    - [ ] D. Error

    **Why:** `//` is integer (floor) division in Twig. **Ref:**
    [Twig operators](https://twig.symfony.com/doc/3.x/templates.html#math).

??? question "Q2. Which delimiter executes a statement without printing?"
    - [ ] A. `{{ … }}`
    - [x] B. `{% … %}` ✅
    - [ ] C. `{# … #}`
    - [ ] D. `#{ … }`

    **Why:** `{% %}` is for tags/control flow; `{{ }}` prints; `{# #}` comments.
    **Ref:** [Twig syntax](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references).

## Key takeaways

- Three delimiters: `{{ }}` print, `{% %}` do, `{# #}` comment.
- Twig **compiles to a PHP class** cached under `var/cache/`; runtime is cheap.
- `~` concatenates; `//` floors; filters bind tightest.
- Whitespace: `-` modifiers and `{% apply spaceless %}`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `{{ }}` echo · `{% %}` logic · `{# #}` comment.
    - Attribute order: index → property → method → getX → isX → hasX.
    - Precedence high→low: `**` > `* / // %` > `+ -` > `~` > compare > `and`/`or` > `?:`.
    - Trim: `{{- -}}`. `{% apply spaceless %}`.

## Official References
- [Official — Twig for template designers](https://twig.symfony.com/doc/3.x/templates.html)
- [Official — Creating templates (Symfony)](https://symfony.com/doc/current/templates.html)
- [Twig source — Environment/Compiler](https://github.com/twigphp/Twig/blob/3.x/src/Environment.php)

---

<small>Related: [Auto-Escaping](auto-escaping.md) · [Loops & Conditions](loops-conditions.md) · [Filters & Functions](filters-functions.md)</small>
