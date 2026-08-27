# Rendering Forms with Twig

!!! tip "In a nutshell"
    Twig form functions turn a form into HTML at any granularity, from `form(form)`
    to per-part `form_label`/`form_widget`. Don't forget: `form_end` renders the
    remaining fields — including the hidden **CSRF token** — unless you pass `render_rest: false`.

!!! example "Real-world analogy"
    Rendering is the **print shop** that lays out your blank paper form from a spec
    (the `FormView`). `form(form)` prints the whole page; the granular functions
    (`form_row`, `form_label`, `form_widget`) let you place each field by hand for a
    custom layout. `form_end`/`form_rest` is the shop making sure it also prints the
    small print at the bottom — the hidden and **CSRF** fields — so nothing you
    forgot to place is left off the page.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Render a whole form with `form()` and control layout with `form_start`/`form_end`.
    - [ ] Render fields granularly with `form_row`, `form_widget`, `form_label`, `form_errors`, `form_help`.
    - [ ] Use `form_rest` to render remaining (including hidden/CSRF) fields.

    **Syllabus:** `Forms → Rendering` ·
    **Level:** Advanced → Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Creating forms](creation.md) · [Templating](../twig/index.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
Twig peut afficher un formulaire entier d'un coup (`form(form)`) ou champ par champ pour un contrôle total (`form_row`, `form_widget`...).

### Imagine dans la vraie vie
Le rendu, c'est l'**imprimerie** qui met en page ton formulaire papier vierge à partir d'un plan (le `FormView`). `form(form)` imprime toute la page ; les fonctions granulaires (`form_row`, `form_label`, `form_widget`) te laissent placer chaque champ à la main pour une mise en page sur mesure.

### Dans Symfony
Oublier d'appeler `{{ form_end(form) }}` (ou `form_rest`) peut faire disparaître silencieusement le champ CSRF caché — le formulaire semble fonctionner en dev, mais échoue en soumission car le token n'a jamais été rendu.

### Exemple simple
```twig
{{ form_start(form) }}
{{ form_row(form.email) }}
{{ form_end(form) }} {# rend aussi les champs restants + le token CSRF caché #}
```

### Comment le mémoriser 🧠
`form_end` rend **tout ce qui reste**, y compris le champ CSRF caché — sauf si tu passes explicitement `render_rest: false`. Ne jamais l'oublier sur un rendu granulaire.

Twig form functions turn a `FormView` (the render-time snapshot from
`createView()`) into HTML. You choose the granularity:

```php
// createView() produces the render-time FormView snapshot
$view = $form->createView();
assert($view instanceof \Symfony\Component\Form\FormView);

// In Twig you pass the form itself; Symfony calls createView() for you
return $this->render('contact/index.html.twig', ['form' => $form]);
```

| Function | Renders |
|---|---|
| `form(form)` | The entire form (start, all rows, end) |
| `form_start(form)` / `form_end(form)` | Opening/closing `<form>` tag |
| `form_row(field)` | Label + widget + errors + help for one field |
| `form_label` / `form_widget` / `form_errors` / `form_help` | One part of a field |
| `form_rest(form)` | All not-yet-rendered fields (incl. hidden + CSRF) |

!!! question "Predict first"
    You render every visible field by hand and finish with
    `form_end(form, {'render_rest': false})`. What silently goes missing?

??? note "Reveal"
    The hidden fields — most importantly the **CSRF `_token`**. `form_end` calls
    `form_rest` by default to emit them; with `render_rest: false` you must render
    `form_rest`/the token yourself or every submit fails CSRF validation.

## Deep Dive — how it works internally

### From `FormInterface` to `FormView`

Rendering operates on `Symfony\Component\Form\FormView`, produced by
`FormInterface::createView()`. The Twig functions are provided by
`Symfony\Bridge\Twig\Extension\FormExtension`, which delegates real rendering to
a `Symfony\Component\Form\FormRendererInterface`
(`Symfony\Bridge\Twig\Form\TwigRendererEngine`).

```php
// FormInterface::createView() builds the FormView tree
$view = $form->createView();

// Twig's FormExtension functions delegate to a FormRendererInterface,
// whose engine (TwigRendererEngine) loads the form theme templates
$html = $renderer->searchAndRenderBlock($view, 'widget');
```

The renderer resolves, for each function + field, a **block** in the active form
theme (e.g. `form_row`, `text_widget`) using the field's *block prefix hierarchy*
— covered in [theming](theming.md).

```twig
{# form_row on a text field resolves blocks by block-prefix hierarchy: #}
{{ form_row(form.name) }}
{# looks for 'text_row' first, falls back to the generic 'form_row';
   the widget inside resolves 'text_widget' → 'form_widget_simple' #}
```

```mermaid
flowchart LR
    A["createView()"] --> B[FormView tree]
    B --> C[FormExtension functions]
    C --> D[FormRenderer]
    D --> E[Theme block] --> F[HTML]
```

!!! note "Source reference"
    `Symfony\Bridge\Twig\Extension\FormExtension` and `FormRenderer` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/FormExtension.php).

### `form_end` and `form_rest`

`form_end(form)` closes the tag **and** by default calls `form_rest` internally,
rendering any fields you did not render manually — crucially the **hidden CSRF
token** and any hidden fields. Pass `{'render_rest': false}` to suppress that:

```twig
{{ form_end(form, {'render_rest': false}) }}
```

If you render fields manually and set `render_rest: false`, you must render
`form_rest(form)` (or the CSRF field) yourself, or CSRF validation fails.

```twig
{{ form_start(form) }}
    {{ form_row(form.email) }}
    {{ form_rest(form) }}  {# emit the hidden CSRF token yourself #}
{{ form_end(form, {'render_rest': false}) }}
```

### The "rendered" flag

Each `FormView` has an `isRendered()` flag. Calling `form_row`/`form_widget`
marks it rendered so `form_rest` skips it. That is how partial + rest rendering
coexist without duplication.

```twig
{{ form_start(form) }}
{{ form_row(form.name) }}     {# this FormView now returns isRendered() = true #}
{{ form_widget(form.email) }} {# marked as rendered too #}
{{ form_rest(form) }}         {# skips rendered views — no duplication #}
{{ form_end(form) }}
```

## Configuration & code

=== "Whole form"

    ```twig
    {# templates/contact/index.html.twig #}
    {{ form(form) }}
    ```

=== "Manual layout"

    ```twig
    {{ form_start(form, {'attr': {'novalidate': 'novalidate'}}) }}
        {{ form_errors(form) }}                {# form-level errors #}

        {{ form_row(form.name) }}

        <div class="grid">
            {{ form_label(form.email) }}
            {{ form_widget(form.email, {'attr': {'placeholder': 'you@example.com'}}) }}
            {{ form_errors(form.email) }}
            {{ form_help(form.email) }}
        </div>

        {{ form_rest(form) }}                  {# hidden + CSRF fields #}
    {{ form_end(form) }}
    ```

=== "Controller"

    ```php
    <?php
    declare(strict_types=1);

    // Pass the FormInterface directly (Symfony calls createView() for you).
    return $this->render('contact/index.html.twig', ['form' => $form]);
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Use `form_row` for the common case | Hand-writing `<input>` tags |
| Keep `form_rest`/`form_end` to emit CSRF | Rendering fields but dropping CSRF |
| Set attrs via the `attr` variable | Hard-coding `name`/`id` attributes |
| Theme globally, not inline hacks | Copy-pasting widget HTML per template |

## When (not) to use it / alternatives

Granular functions are for custom layouts. For a fully bespoke front-end
(hydrated by JS) you may render only `form_start`/`form_widget` for specific
fields — but always emit the CSRF token (via `form_rest` or `csrf_token()`), or
switch off CSRF explicitly.

!!! danger "Certification traps"
    - `form_end` renders remaining fields **by default**; suppress with
      `render_rest: false` — and then render CSRF yourself.
    - `form_row` = label + widget + errors + **help**; `form_widget` is the
      control only.
    - `form_errors(form)` (root) shows **form-level** errors; per-field errors
      need `form_errors(form.field)`.
    - `form_label(field, 'Custom')` overrides the label text inline.

!!! warning "Common mistakes"
    - Rendering fields manually, setting `render_rest: false`, forgetting CSRF →
      "invalid token" on submit.
    - Passing `form.vars` values you didn't define; unknown variables are just
      empty.
    - Calling `form(form.email)` — `form()` is for the whole form, use
      `form_row`/`form_widget` for a field.

## Exercises

1. **(Advanced)** Render a form manually with a custom two-column grid, ensuring
   CSRF still submits correctly.
2. **(Expert)** You rendered every field with `form_row` but a hidden field is
   missing from the HTML. Why, and what fixes it?

??? success "Solutions"

    **1.** Use `form_start`, explicit `form_row`s inside your grid markup, then
    `form_rest(form)` before `form_end(form, {'render_rest': false})` — or simply
    let `form_end` render the rest. `form_rest` emits the hidden CSRF token.

    **2.** You never rendered that field and you disabled the rest (or used
    `render_rest: false` on `form_end`). Add `{{ form_widget(form.theField) }}`
    or restore `form_rest`/default `form_end`.

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. What does `form_row(form.email)` render?"
    - [ ] A. Only the `<input>`
    - [x] B. Label, widget, errors and help for that field ✅
    - [ ] C. The whole form
    - [ ] D. Just the label

    **Why:** `form_row` composes label + widget + errors + help via the
    `field_row`/`*_row` theme block.
    **Ref:** [Form rendering functions](https://symfony.com/doc/8.0/form/form_customization.html).

??? question "Q2. How is the CSRF token normally emitted in the HTML?"
    - [x] A. By `form_rest`, which `form_end` calls by default ✅
    - [ ] B. Only by writing `<input name="_token">` by hand
    - [ ] C. In `form_start`
    - [ ] D. It is never rendered in the form

    **Why:** The CSRF field is a hidden child rendered by `form_rest`; `form_end`
    triggers `form_rest` unless `render_rest: false`.
    **Ref:** [CSRF protection](https://symfony.com/doc/8.0/security/csrf.html).

??? question "Q3. Which shows form-level (non-field) errors?"
    - [x] A. `form_errors(form)` ✅
    - [ ] B. `form_errors(form.name)`
    - [ ] C. `form_widget(form)`
    - [ ] D. `form_help(form)`

    **Why:** Passing the root view to `form_errors` renders errors attached to
    the form itself (e.g. from a class-level constraint).
    **Ref:** [Form errors](https://symfony.com/doc/8.0/forms.html).

## Key takeaways

- `form(form)` renders everything; `form_start`/`form_end` bracket manual layouts.
- `form_row` = label + widget + errors + help; the granular functions split it.
- `form_end`/`form_rest` emit hidden + CSRF fields — never lose them.
- Rendering works on the `FormView` via `FormRenderer` resolving theme blocks.

## Last-minute revision

!!! tip "Cheat sheet"
    - `form_start(form, {attr:{...}})` / `form_end(form, {render_rest:false})`
    - `form_row / form_label / form_widget / form_errors / form_help`
    - `form_rest(form)` → hidden + CSRF.
    - Override label: `form_label(field, 'Text')`.
    - Pass the `FormInterface`; Twig calls `createView()`.

## Connections

- **Depends on:** [Creating forms](creation.md) — rendering operates on the `FormView` from `createView()`; [Twig templating](../twig/index.md) provides the functions.
- **Reused in:** [Theming](theming.md) — each function resolves a theme block via the block-prefix hierarchy.
- **Confused with:** [CSRF protection](csrf.md) — `form_rest`/`form_end` is what actually emits the token into the HTML.

## Official References
- [Official Symfony docs — Form customization](https://symfony.com/doc/8.0/form/form_customization.html)
- [Official Symfony docs — Rendering forms](https://symfony.com/doc/8.0/forms.html)
- [Symfony source — Twig FormExtension](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/FormExtension.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony forms" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/form/form_customization.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** `form_end`/`form_rest` must emit the hidden CSRF field
- [ ] render a form whole or granularly (`form_row`/`form_widget`/`form_label`) in Symfony 8
- [ ] debug a missing hidden field caused by `render_rest: false`
- [ ] spot the wrong answer about what `form_row` includes (label + widget + errors + help)
- [ ] explain how the `isRendered()` flag lets partial + `form_rest` rendering coexist

---

<small>Related: [Theming](theming.md) · [Creating forms](creation.md) ·
[CSRF protection](csrf.md)</small>
