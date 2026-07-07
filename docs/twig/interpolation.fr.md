# String Interpolation

!!! tip "In a nutshell"
    Construisez des chaînes de trois façons : l'interpolation `#{expr}` (guillemets
    doubles uniquement), la concaténation `~`, et le filtre `format` (sprintf).
    Point d'examen : `~` joint comme des chaînes tandis que `+` additionne des
    nombres, et `~` a une précédence plus faible que l'arithmétique.

!!! example "Real-world analogy"
    Pensez à l'assemblage d'une lettre type. L'interpolation `#{...}` est le champ
    de publipostage — mais la fusion ne s'active que sur le papier à en-tête
    officiel (les chaînes entre guillemets doubles) ; tapez-le sur du brouillon
    (guillemets simples) et le champ s'imprime en encre littérale. L'opérateur `~`
    agrafe des feuilles bout à bout : tout, nombres compris, devient simplement
    plus de papier (du texte). L'opérateur `+` est une calculatrice de poche qui
    additionne réellement des chiffres. Et comme il faut terminer les calculs
    avant de pouvoir agrafer les résultats, la calculatrice passe toujours avant
    l'agrafeuse (`~` a la précédence la plus faible).

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Interpoler des expressions dans des chaînes à guillemets doubles avec `#{...}`.
    - [ ] Concaténer avec l'opérateur `~` et savoir en quoi il diffère de `+`.
    - [ ] Formater des chaînes avec le filtre `format` (sprintf).

    **Syllabus:** `Templating (Twig) → String interpolation` ·
    **Level:** Advanced ·
    **Est. time:** 15 min ·
    **Prerequisites:** [Twig Syntax](syntax.md)

---

## Theory

Trois façons de construire une chaîne à partir de morceaux :

```twig
{# 1. interpolation — double quotes only #}
{{ "Hello #{name}, you have #{count} items" }}

{# 2. concatenation with ~ #}
{{ "Hello " ~ name ~ "!" }}

{# 3. format filter (sprintf) #}
{{ "Hello %s, %d items"|format(name, count) }}
```

- **`#{...}`** évalue une expression Twig dans une chaîne à **guillemets doubles**.
- **`~`** joint des valeurs comme des chaînes (les nombres sont convertis en chaîne).
- **`format`** applique les placeholders `sprintf` (`%s`, `%d`, `%.2f`, `%1$s`).

!!! question "Predict first"
    Que produit `{{ 1 + 2 ~ 3 }}` — `6`, `"123"` ou `"33"` ?

??? note "Reveal"
    `"33"`. `+` est **prioritaire** sur `~`, donc l'évaluation est `(1 + 2) ~ 3` →
    `3 ~ 3` → la chaîne `"33"`. `~` concatène (conversion en chaîne) ; `+` est
    arithmétique — ils ne sont pas interchangeables.

## Deep Dive — how it works internally

L'interpolation est une fonctionnalité du **lexer** : dans une chaîne `"..."`,
`#{` ouvre une expression embarquée que le lexer tokenise et que le parser
compile en concaténation. Elle ne fonctionne **que** dans les guillemets
doubles — les chaînes à guillemets simples sont littérales, donc `'#{x}'`
affiche le texte brut.

`~` compile en concaténation de chaînes PHP (`.`) après conversion de chaque
opérande en chaîne, d'où `1 ~ 1` donnant `"11"` tandis que `1 + 1` vaut `2`. `~`
se situe *en dessous* de l'arithmétique dans la précédence (voir
[Syntax](syntax.md)), donc `1 + 1 ~ "x"` vaut `"2x"`.

`format` et son cousin **`replace`** vivent dans `Twig\Extension\CoreExtension`.
`format` appelle le `vsprintf` de PHP sous le capot ; `replace` fait une
substitution par clés : `{{ "%name%"|replace({ '%name%': n }) }}`.

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

| ✅ À faire | ❌ À éviter |
|---|---|
| `#{}` pour des valeurs inline lisibles | De longues chaînes de `~` qui nuisent à la lisibilité |
| `format` pour les besoins numériques/de padding | L'arrondi manuel par concaténation |
| `~` pour joindre quelques morceaux | `+` pour « joindre » des chaînes (c'est de l'arithmétique) |
| Des guillemets doubles pour l'interpolation | Attendre que `'…#{x}…'` interpole |

## When (not) to use it / alternatives

Optez pour `#{}` quand l'insertion d'une ou deux valeurs se lit le mieux ;
utilisez `~` pour des jointures simples ; utilisez `format`/`replace` quand vous
avez besoin de padding, de précision ou de placeholders réutilisables (les
chaînes de traduction utilisent des placeholders `%name%` — voir
[Translations](translations.md)).

!!! danger "Certification traps"
    - L'interpolation `#{}` ne fonctionne **que dans les chaînes à guillemets doubles**.
    - `~` est la concaténation ; `+` est l'**addition** — `"1" + "2"` vaut `3`,
      `"1" ~ "2"` vaut `"12"`.
    - `~` a une **précédence plus faible** que `+`/`*`, donc l'arithmétique passe d'abord.
    - `#{...}` n'a rien à voir avec le `{{ }}` de Twig — il vit *à l'intérieur* d'un littéral de chaîne.

!!! warning "Common mistakes"
    - Mettre une chaîne interpolée entre guillemets simples et se demander
      pourquoi `#{name}` s'affiche littéralement.
    - Utiliser `+` pour concaténer et obtenir `0` ou une erreur de type.

## Exercises

1. **(Basic)** Construisez `"Order #42 (paid)"` à partir de `id = 42` et
   `status = 'paid'` avec l'interpolation.
2. **(Intermediate)** La même chaîne en utilisant uniquement `~`.
3. **(Advanced)** Formatez un prix à deux décimales avec un suffixe de devise via
   `format`.

??? success "Solutions"

    **1.** Combinez un `#` littéral avec l'interpolation :
    `{{ "Order #" ~ "#{id} (#{status})" }}` — ou, plus propre, utilisez `format` :
    `{{ "Order #%d (%s)"|format(id, status) }}`.

    **2.** `{{ "Order #" ~ id ~ " (" ~ status ~ ")" }}`.

    **3.** `{{ "%.2f €"|format(amount) }}`.

## Certification questions

??? question "Q1. Where does `#{...}` interpolation work?"
    - [x] A. Only inside double-quoted strings ✅
    - [ ] B. In any string
    - [ ] C. Only inside `{% %}`
    - [ ] D. Only in single-quoted strings

    **Why:** Le lexer n'interpole qu'à l'intérieur de `"..."`. **Ref:**
    [String interpolation](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation).

??? question "Q2. What is `{{ 1 + 2 ~ 3 }}`?"
    - [x] A. `"33"` ✅
    - [ ] B. `"123"`
    - [ ] C. `6`
    - [ ] D. `"15"`

    **Why:** `+` est prioritaire sur `~` : `(1 + 2) ~ 3` → `3 ~ 3` → `"33"`. **Ref:**
    [operators](https://twig.symfony.com/doc/3.x/templates.html#other-operators).

??? question "Q3. Which filter applies sprintf-style formatting?"
    - [x] A. `format` ✅
    - [ ] B. `sprintf`
    - [ ] C. `printf`
    - [ ] D. `interpolate`

    **Why:** `|format(...)` enveloppe `vsprintf`. **Ref:**
    [format filter](https://twig.symfony.com/doc/3.x/filters/format.html).

## Key takeaways

- `#{expr}` n'interpole que dans les chaînes à **guillemets doubles**.
- `~` concatène (conversion en chaîne) ; `+` est arithmétique.
- `~` a une précédence plus faible que l'arithmétique.
- `format` = sprintf ; `replace` = substitution par clés.

## Last-minute revision

!!! tip "Cheat sheet"
    - `"hi #{name}"` (guillemets doubles) · `'hi #{name}'` = littéral.
    - `a ~ b` joint · `a + b` additionne.
    - `"%s %d"|format(a, b)` · `"%x%"|replace({'%x%': v})`.

## Connections

- **Depends on:** [Twig Syntax](syntax.md) — `~` vs `+` et leur précédence viennent directement de la table des opérateurs.
- **Reused in:** [Translations](translations.md) — les messages de traduction utilisent des placeholders `%name%`, la même idée de substitution que `format`/`replace`.
- **Confused with:** [Filters & Functions](filters-functions.md) — `format` est un filtre (`|format`), pas une syntaxe de chaîne.

## Official References
- [Twig — string interpolation](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)
- [Twig — format filter](https://twig.symfony.com/doc/3.x/filters/format.html)
- [Twig source — Lexer](https://github.com/twigphp/Twig/blob/3.x/src/Lexer.php)

## Video references

!!! tip "Watch & learn"
    Ce sont des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « Twig templating » pour consolider ce chapitre. Nous lions des chaînes
    stables plutôt que des vidéos individuelles afin que les références ne
    périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences SymfonyCon & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/index.html) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** `~` et `+` diffèrent et quand choisir `#{}` vs `format`
- [ ] construire une chaîne de trois façons (interpolation, `~`, `format`) en Symfony 8
- [ ] déboguer un `#{name}` affiché littéralement dans une chaîne à guillemets simples
- [ ] repérer la réponse piège sur la précédence de `~`/`+` (p. ex. `1 + 2 ~ 3`)
- [ ] expliquer que `#{}` est une fonctionnalité du lexer vivant dans un littéral à guillemets doubles

---

<small>Related: [Twig Syntax](syntax.md) · [Filters & Functions](filters-functions.md) · [Translations](translations.md)</small>
