# Debugging Variables

!!! tip "In a nutshell"
    `{{ dump(x) }}` prints a rich VarDumper view inline; `{% dump x %}` sends it to the
    toolbar without page markup. Exam hook: dump tooling exists only in debug/dev — a
    stray `dump()` errors in prod.

!!! example "Real-world analogy"
    `dump()` is the mechanic's diagnostic scanner plugged into a car up on the workshop lift.
    It shows a rich, expandable readout of any component's state — far more than a bare
    warning light (`var_dump`). The `{{ dump() }}` function prints that readout on a screen
    bolted to the dashboard where you're standing, while `{% dump %}` pipes the same data to
    the workshop's central console without cluttering the dashboard. Crucially, the
    diagnostic port only exists on shop-floor cars (debug/dev); ship a car to a customer with
    the scanner still jacked in (prod) and it jams the ignition entirely.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Inspect template variables with `dump()` and `{% dump %}`.
    - [ ] Explain the Symfony `DumpExtension` vs Twig's core debug extension.
    - [ ] Choose between `{{ dump() }}` and the profiler for diagnosis.

    **Syllabus:** `Templating (Twig) → Debugging variables` ·
    **Level:** Advanced ·
    **Est. time:** 15 min ·
    **Prerequisites:** [Twig Syntax](syntax.md)

---

## Theory

`dump()` renders a rich, expandable view of any variable — the template-side
equivalent of PHP's `dump()`/`var_dump()`:

```twig
{{ dump(user) }}          {# dump one variable, prints inline #}
{{ dump(user, order) }}   {# dump several #}
{{ dump() }}              {# dump ALL variables in the current context #}
{% dump user %}           {# tag form: sends to output, prints nothing here #}
```

`dump()` (function) **outputs** the dump where it is called; `{% dump %}` (tag)
sends data to the dump destination **without** injecting markup into the page.

```twig
{# function form: prints the dump right here in the page #}
{{ dump(order) }}

{# tag form: nothing rendered here — data goes to the profiler/toolbar #}
{% dump order %}
```

!!! question "Predict first"
    A `{{ dump(order) }}` slips into a committed template and reaches **production**.
    What happens on the first request that renders it?

??? note "Reveal"
    A fatal `Unknown "dump" function` error. `DumpExtension` is registered **only**
    in debug mode, so the function simply does not exist in `prod`. Dump tooling is
    a dev-only convenience — remove dumps before deploy and use logging/the profiler
    (in a non-prod env) for diagnosis.

## Deep Dive — how it works internally

Two layers exist:

- **Twig core** ships `Twig\Extension\DebugExtension`, which provides a plain
  `dump()` backed by `var_dump`. It only works when the environment's `debug`
  option is on.
- **Symfony** replaces/augments it with
  **`Symfony\Bridge\Twig\Extension\DumpExtension`**, wired to the **VarDumper**
  component (`Symfony\Component\VarDumper\Dumper\HtmlDumper` +
  `VarCloner`). This gives the collapsible, syntax-highlighted output and routes
  dumps to the **web debug toolbar / profiler** in dev.

```php
use Symfony\Component\VarDumper\Cloner\VarCloner;
use Symfony\Component\VarDumper\Dumper\HtmlDumper;

// Twig core: DebugExtension = plain var_dump-based dump(), needs debug: true
$twig = new \Twig\Environment($loader, ['debug' => true]);
$twig->addExtension(new \Twig\Extension\DebugExtension());

// Symfony's DumpExtension routes dump() through VarDumper instead:
$cloner = new VarCloner();  // safely clones the variable graph
$dumper = new HtmlDumper(); // renders the collapsible, highlighted view
$dumper->dump($cloner->cloneVar($order));
```

```mermaid
flowchart LR
    T["dump(x)"] --> DE[DumpExtension]
    DE --> VC[VarCloner::cloneVar]
    VC --> HD[HtmlDumper]
    HD --> O[rich HTML output]
    T2["{% dump x %}"] --> DE
    DE --> WDT[collected by profiler]
```

- Both are registered **only in debug mode** (`kernel.debug` / `dev`); in `prod`
  `dump()` is not available, so a leftover `dump()` throws an "unknown function"
  error — remove them before deploy.
- `dump()` with **no arguments** dumps the entire render context (all variables
  passed plus globals).
- Because VarDumper clones the variable first, dumping large object graphs is
  safe (it limits depth) but can be memory-heavy on huge structures.

```twig
{# dev (kernel.debug = true): both forms are available #}
{{ dump(user) }}
{{ dump() }}   {# no args: the whole context, variables + globals #}

{# prod: DumpExtension is not registered — this template fails
   to compile with: Unknown "dump" function #}
```

!!! note "Source reference"
    `Symfony\Bridge\Twig\Extension\DumpExtension`,
    `Symfony\Component\VarDumper\Cloner\VarCloner` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/DumpExtension.php).

## Configuration & code

=== "Twig usage"

    ```twig
    {# inline, expandable #}
    <pre>{{ dump(order) }}</pre>

    {# whole context #}
    {{ dump() }}

    {# tag: no markup injected, shows in toolbar #}
    {% dump items %}
    ```

=== "YAML (debug bundle)"

    ```yaml
    # config/packages/debug.yaml  (dev only, auto-configured)
    when@dev:
        debug:
            dump_destination: "tcp://%env(VAR_DUMPER_SERVER)%"
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `dump()` in dev to inspect data | `dump()` left in committed templates |
| `{% dump %}` to keep markup clean | `dump()` inside a loop over 10k rows |
| Profiler for request-wide insight | `dump()` for perf profiling |
| Remove dumps before prod | Relying on `dump()` in `prod` (unavailable) |

## When (not) to use it / alternatives

Use `dump()`/`{% dump %}` for a **quick look** at a variable while building a
template. For request-wide diagnosis (queries, events, timing, the full
translation/route/security picture) use the **Profiler / web debug toolbar**. For
production issues, use logging — never `dump()`.

!!! danger "Certification traps"
    - `dump()` and `{% dump %}` are available **only in debug/dev**; they error in
      `prod`.
    - `{{ dump() }}` (function) **prints** into the page; `{% dump %}` (tag) does
      **not** inject page markup (it goes to the collector/toolbar).
    - `dump()` with no args dumps the **entire context**.
    - Symfony's rich dump comes from **VarDumper**, not Twig's plain
      `DebugExtension`.

!!! warning "Common mistakes"
    - Deploying with a stray `{{ dump() }}` → `Unknown "dump" function` in prod.
    - Confusing `dump()` output location: the tag form won't appear inline.

## Exercises

1. **(Basic)** Dump the `product` variable inline.
2. **(Intermediate)** Dump every variable available in the current template.
3. **(Advanced)** Explain why `{{ dump() }}` fails in `prod` and what to use
   instead.

??? success "Solutions"

    **1.** `{{ dump(product) }}`.

    **2.** `{{ dump() }}` — no arguments dumps the whole context.

    **3.** The `DumpExtension` is only registered in debug mode, so the function
    is undefined in `prod`; use logging or the profiler (in a non-prod env)
    instead, and remove dumps before deploy.

## Certification questions

??? question "Q1. What does `{{ dump() }}` with no arguments do?"
    - [x] A. Dumps all variables in the current context ✅
    - [ ] B. Dumps nothing
    - [ ] C. Throws
    - [ ] D. Dumps only globals

    **Why:** No-arg `dump()` outputs the entire render context. **Ref:**
    [dump function](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities).

??? question "Q2. Difference between `{{ dump(x) }}` and `{% dump x %}`?"
    - [x] A. The function prints inline; the tag sends to the collector without markup ✅
    - [ ] B. They are identical
    - [ ] C. The tag works in prod
    - [ ] D. The function only works in prod

    **Why:** Tag form avoids injecting HTML into the page. **Ref:**
    [dump utilities](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities).

??? question "Q3. Why does `dump()` error in `prod`?"
    - [x] A. The DumpExtension is only registered in debug mode ✅
    - [ ] B. It is a syntax error
    - [ ] C. VarDumper is never installed
    - [ ] D. It is deprecated

    **Why:** Dump tooling is dev-only. **Ref:**
    [VarDumper](https://symfony.com/doc/current/components/var_dumper.html).

## Key takeaways

- `dump()` prints a rich VarDumper view; `{% dump %}` sends it to the collector.
- No-arg `dump()` dumps the whole context.
- Dev/debug only — remove before prod (it errors there).
- Rich output = `DumpExtension` + VarDumper, not Twig's plain debug extension.

## Last-minute revision

!!! tip "Cheat sheet"
    - `{{ dump(a, b) }}` inline · `{{ dump() }}` = all context.
    - `{% dump x %}` = to toolbar, no page markup.
    - Debug/dev only; unavailable in prod.
    - Backed by VarDumper (`VarCloner` + `HtmlDumper`).

## Connections

- **Depends on:** [Twig Syntax](syntax.md) — `dump()` is a function, `{% dump %}` a tag; the delimiter decides where output goes.
- **Reused in:** [Global Variables](globals.md) — no-arg `dump()` inspects the whole render context, `app` global included.
- **Confused with:** [Profiler](../miscellaneous/profiler.md) — for request-wide diagnosis (queries, events, timing) reach for the profiler, not `dump()`.

## Official References
- [Official — The dump Twig utilities](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)
- [Official — VarDumper](https://symfony.com/doc/current/components/var_dumper.html)
- [Symfony source — DumpExtension](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/DumpExtension.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Twig templating" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** rich `dump()` output beats `var_dump` and where it goes
- [ ] use `dump()`, no-arg `dump()`, and `{% dump %}` correctly in Symfony 8
- [ ] debug a stray `dump()` that 500s in production
- [ ] spot the trick answer claiming the tag form prints inline
- [ ] explain that VarDumper (`VarCloner` + `HtmlDumper`), not Twig's `DebugExtension`, powers it

---

<small>Related: [Global Variables](globals.md) · [Twig Syntax](syntax.md) · [Filters & Functions](filters-functions.md)</small>
