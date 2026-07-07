# Loops & Conditions

!!! tip "In a nutshell"
    `{% for %}` itère et expose la variable `loop` (`index`, `first`, `last`,
    `length`) ; `{% for … else %}` gère le cas vide. Point d'examen : Twig n'a pas
    de `break`/`continue` — filtrez plutôt la source avec `for x in items if …`.

!!! example "Real-world analogy"
    `{% for %}` est un guide de musée qui fait passer un groupe devant chaque
    œuvre : la variable `loop` est le porte-bloc du guide indiquant à quel arrêt
    il se trouve (`index`), s'il s'agit du premier ou du dernier (`first`/`last`)
    et combien il en reste. `for … else` est le panneau « galerie fermée » affiché
    quand il n'y a rien à visiter.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Itérer avec `for` et utiliser chaque membre de la variable `loop`.
    - [ ] Brancher avec `if`/`elseif`/`else` et les tests Twig courants.
    - [ ] Utiliser la clause `for … else` pour les collections vides.

    **Syllabus:** `Templating (Twig) → Loops & conditions` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Twig Syntax](syntax.md)

---

## Theory

### `for`

```twig
{% for item in items %}
    {{ loop.index }}. {{ item.name }}
{% endfor %}
```

Itérez des tableaux, des `Traversable`, ou en clé→valeur avec
`{% for key, value in map %}`.

```twig
{# works on arrays and any Traversable (e.g. a Doctrine Collection) #}
{% for key, value in map %}
    {{ key }}: {{ value }}
{% endfor %}
```

La variable **`loop`** dans un `for` :

| Membre | Signification |
|---|---|
| `loop.index` / `loop.index0` | position à partir de 1 / de 0 |
| `loop.revindex` / `loop.revindex0` | distance depuis la fin |
| `loop.first` / `loop.last` | `bool` |
| `loop.length` | total |
| `loop.parent` | contexte de la boucle englobante |

```twig
{% for group in groups %}
    {% for user in group.users %}
        {{ loop.parent.loop.index }}.{{ loop.index }}/{{ loop.length }}
        {# outer index via loop.parent · 1-based index / total count #}
        {{ loop.index0 }} {{ loop.revindex }} {{ loop.revindex0 }}  {# 0-based / from the end #}
        {% if loop.first %}first{% elseif loop.last %}last{% endif %}  {# booleans #}
    {% endfor %}
{% endfor %}
```

### `if`

```twig
{% if score >= 90 %}A
{% elseif score >= 60 %}B
{% else %}F
{% endif %}
```

### `for … else`

```twig
{% for u in users %}{{ u.name }}
{% else %}<p>No users.</p>
{% endfor %}
```

!!! question "Predict first"
    Vous devez sauter les lignes inactives dans un `{% for %}`. Vous cherchez
    `{% continue %}` ? Que propose réellement Twig ?

??? note "Reveal"
    Rien — Twig n'a **ni `break` ni `continue`** (délibérément, pour garder les
    templates déclaratifs). Filtrez plutôt la source :
    `{% for x in items if x.active %}`, découpez-la, ou enveloppez le corps dans
    un `{% if %}`.

## Deep Dive — how it works internally

`{% for %}` compile en un `foreach` PHP, et la variable `loop` est un petit
tableau que Twig maintient à chaque itération. Point crucial : `loop.length`,
`loop.last`, `loop.revindex` ne sont disponibles que si l'itérable est
**dénombrable** (un tableau ou un `Countable`/`Traversable` que Twig peut
compter) — pour un simple `Generator`, Twig peut les mettre en mémoire tampon ou
les omettre. `loop.first`/`loop.index` sont toujours disponibles.

```twig
{% for row in rows %}  {# compiles to a PHP foreach #}
    {{ loop.index }} {{ loop.first ? 'first' }}    {# always available #}
    {{ loop.length }} {{ loop.revindex }} {{ loop.last ? 'last' }}
    {# ^ need a countable iterable (array/Countable) — not a bare Generator #}
{% endfor %}
```

```mermaid
flowchart TD
    F["for x in items"] --> Cnt{Countable?}
    Cnt -- yes --> Full["loop.* incl. length/last"]
    Cnt -- no --> Part["loop.index/first only"]
    Full --> Body[render body]
    Part --> Body
    Body --> Else{"any iterations?"}
    Else -- none --> E["for … else block"]
```

- La clause **`else`** ne s'exécute que si la collection produit **zéro** itération.
- `{% for %}` peut **filtrer** et **découper** en ligne :
  `{% for x in items if x.active %}` et `{% for x in items|slice(0, 10) %}`.
- Vous **ne pouvez pas `break`/`continue`** en Twig — filtrez la source ou
  utilisez un `if` dans le corps. C'est délibéré (garde les templates déclaratifs).

```twig
{# no break/continue: filter and slice the source instead #}
{% for x in items|slice(0, 10) if x.active %}
    {{ x.name }}
{% else %}
    No active items.   {# else: runs only on zero iterations #}
{% endfor %}
```

!!! note "Source reference"
    `for`/`if` token parsers, `Twig\Node\ForNode`, `Twig\Node\ForLoopNode` —
    [twigphp/Twig `3.x`](https://github.com/twigphp/Twig/blob/3.x/src/Node/ForNode.php).

### Tests (used in conditions)

`is defined`, `is null`, `is empty`, `is even`/`odd`, `is iterable`,
`is same as(x)` (identité `===`), `divisible by(n)`, `constant('X')`. Négation
avec `is not`. `empty` est vrai pour `null`, `false`, `0`, `''`, `[]`.

```twig
{% if x is defined and x is not null %}has a real value{% endif %}
{% if items is empty %}empty: null / false / 0 / '' / []{% endif %}
{% if n is even %}even{% elseif n is odd %}odd{% endif %}
{% if items is iterable %}can be looped{% endif %}
{% if a is same as(b) %}identical (===){% endif %}
{% if n is divisible by(3) %}multiple of 3{% endif %}
{% if status == constant('App\\Entity\\Order::PAID') %}paid{% endif %}
```

### Null behavior

Itérer sur `null` est sans danger : `{% for x in items %}` quand `items` est
`null` effectue **zéro** itération et tombe directement dans le bloc
`for … else` — pas d'erreur en mode tolérant. Cela fait de `for … else` la garde
naturelle pour une collection potentiellement null ; vous avez rarement besoin
d'un `{% if items %}` autour.

```twig
{# items is null → zero iterations, straight to else — no wrapping if needed #}
{% for x in items %}
    {{ x }}
{% else %}
    <p>Nothing to show.</p>
{% endfor %}
```

Dans les conditions, gardez les trois tests distincts :

- `x is defined` — la variable existe tout court (non défini ≠ null).
- `x is null` — elle existe et vaut `null`.
- `x is empty` — plus large : vrai pour `null`, `false`, `0`, `''` et `[]`.

Le piège : `{% if items %}` traite `null`, `0` et `[]` pareillement comme falsy ;
utilisez donc `is null` quand vous devez distinguer « pas de valeur » de « liste
vide ». Combinez avec `is defined` quand une variable peut manquer entièrement :
`{% if x is defined and x is not null %}`.

```twig
{% if items %}truthy{% endif %}             {# falsy for null, 0 and [] alike #}
{% if items is null %}no value{% endif %}   {# "no value" only #}
{% if items is empty %}nothing{% endif %}   {# null, false, 0, '', [] #}
{% if x is defined and x is not null %}{{ x }}{% endif %}  {# may be missing entirely #}
```

!!! note "Null in real life"
    Une collection null est un groupe de visite vide : le guide n'a personne à
    promener devant les œuvres, alors il passe directement au panneau « galerie
    fermée » (`for … else`).

## Configuration & code

=== "loop members"

    ```twig
    <ul>
    {% for row in rows %}
        <li class="{{ loop.first ? 'top' }} {{ loop.last ? 'bottom' }}">
            {{ loop.index }}/{{ loop.length }} — {{ row.title }}
        </li>
    {% endfor %}
    </ul>
    ```

=== "nested + loop.parent"

    ```twig
    {% for group in groups %}
        {% for item in group.items %}
            {{ loop.parent.loop.index }}.{{ loop.index }}
        {% endfor %}
    {% endfor %}
    ```

=== "inline filter + else"

    ```twig
    {% for p in products if p.inStock %}
        {{ p.name }}
    {% else %}
        Nothing in stock.
    {% endfor %}
    ```

## Best practices & anti-patterns

| ✅ À faire | ❌ À éviter |
|---|---|
| `for … else` pour l'état vide | Un `{% if items %}` superflu autour |
| Filtrer la source dans le controller | Une logique de filtrage lourde dans la boucle |
| `loop.first`/`last` pour les bords | Des compteurs d'index manuels |
| `is same as` pour l'identité | `==` quand vous voulez dire `===` |

## When (not) to use it / alternatives

Gardez les boucles présentationnelles. Tri, filtrage et pagination relèvent du
controller/repository ; les templates doivent itérer sur des données prêtes.
Pour de grandes collections, paginez plutôt que de boucler sur des milliers de
lignes dans Twig.

!!! danger "Certification traps"
    - Il n'y a **ni `break` ni `continue`** en Twig — utilisez `if` ou filtrez l'itérable.
    - `loop.length`/`loop.last` sont indisponibles pour les itérateurs **non dénombrables**.
    - `loop.index` commence à **1** ; `loop.index0` à 0.
    - Le `else` du `for … else` se déclenche sur une collection **vide**, pas sur le dernier élément.
    - `is empty` est vrai pour `0`, `''`, `false`, `[]`, `null` — plus large que `is null`.

!!! warning "Common mistakes"
    - Imbriquer des boucles et utiliser `loop.index` en attendant l'index externe —
      utilisez `loop.parent.loop.index`.
    - Utiliser `==` pour l'identité d'objets là où `is same as` (`===`) est voulu.

## Exercises

1. **(Basic)** Affichez une liste numérotée, en marquant le dernier élément d'un séparateur.
2. **(Intermediate)** Affichez « No results » quand une liste filtrée est vide, en
   une seule construction.
3. **(Advanced)** Dans des boucles imbriquées, affichez `outerIndex.innerIndex`.

??? success "Solutions"

    **1.** `{% for i in items %}{{ loop.index }}. {{ i }}{% if not loop.last %}—{% endif %}{% endfor %}`.

    **2.** `{% for r in results if r.match %}{{ r }}{% else %}No results{% endfor %}`.

    **3.** `{{ loop.parent.loop.index }}.{{ loop.index }}` dans la boucle interne.

## Certification questions

??? question "Q1. What is `loop.index` on the first iteration?"
    - [ ] A. `0`
    - [x] B. `1` ✅
    - [ ] C. `null`
    - [ ] D. `-1`

    **Why:** `loop.index` commence à 1 ; `loop.index0` à 0. **Ref:**
    [for tag](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable).

??? question "Q2. When does the `else` of a `for` run?"
    - [ ] A. On the last item
    - [x] B. When the collection is empty ✅
    - [ ] C. On error
    - [ ] D. Every iteration

    **Why:** `for … else` s'affiche quand il y a zéro itération. **Ref:**
    [for … else](https://twig.symfony.com/doc/3.x/tags/for.html#the-else-clause).

??? question "Q3. How do you skip an iteration in Twig?"
    - [ ] A. `{% continue %}`
    - [ ] B. `{% break %}`
    - [x] C. Filter the source (`for x in items if …`) ✅
    - [ ] D. `loop.skip()`

    **Why:** Twig n'a pas de `break`/`continue` ; utilisez un `if` en ligne ou un
    filtre. **Ref:**
    [for tag](https://twig.symfony.com/doc/3.x/tags/for.html).

## Key takeaways

- `for` → `foreach` ; `loop` fournit `index`, `first`, `last`, `length`, `parent`.
- `for … else` gère proprement le cas vide.
- Pas de `break`/`continue` — filtrez (`for x in items if …`) à la place.
- `loop.length`/`last` exigent un itérable dénombrable.

## Last-minute revision

!!! tip "Cheat sheet"
    - `loop.index`(1) `index0`(0) `first` `last` `length` `revindex` `parent`.
    - `{% for k, v in map %}` · `{% for x in items if cond %}`.
    - `for … else … endfor` = état vide.
    - Tests : `is defined/null/empty/even/odd/iterable/same as/divisible by`.

## Connections

- **Depends on:** [Twig Syntax](syntax.md) — les tests (`is defined`/`null`/`empty`) et les règles de null utilisés dans les conditions y sont définis.
- **Reused in:** [Filters & Functions](filters-functions.md) — `slice`, `default`, `length` façonnent et protègent l'itérable qu'une boucle parcourt.
- **Confused with:** [Twig Syntax](syntax.md) — `is empty` (vrai pour `0`/`''`/`[]`/`null`) est plus large que `is null`.

## Official References
- [Official — Loops in templates](https://symfony.com/doc/current/templates.html)
- [Twig — for / if tags](https://twig.symfony.com/doc/3.x/tags/for.html)
- [Twig source — ForNode](https://github.com/twigphp/Twig/blob/3.x/src/Node/ForNode.php)

## Video references

!!! tip "Watch & learn"
    Ce sont des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « Twig templating » pour consolider ce chapitre. Nous lions des chaînes
    stables plutôt que des vidéos individuelles afin que les références ne
    périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences SymfonyCon & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/templates.html) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** Twig omet `break`/`continue` et ce qui les remplace
- [ ] utiliser chaque membre de `loop.*` et `for … else` en Symfony 8
- [ ] déboguer un `loop.length`/`loop.last` manquant sur un itérateur non dénombrable
- [ ] repérer la réponse piège qui confond `is null`, `is empty` et `is defined`
- [ ] expliquer comment `for` compile en `foreach` et quand la clause `else` se déclenche

---

<small>Related: [Twig Syntax](syntax.md) · [Filters & Functions](filters-functions.md) · [Includes](includes.md)</small>
