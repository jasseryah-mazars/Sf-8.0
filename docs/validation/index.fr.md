# Data Validation

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Custom Constraint](../labs/validation.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Le composant `Symfony\Component\Validator` de Symfony décide si une valeur PHP est
*acceptable* — un nom `NotBlank`, un `Email` bien formé, une case à cocher de
conditions `IsTrue` — et, quand elle ne l'est pas, produit une
`Symfony\Component\Validator\ConstraintViolationList` structurée que vous pouvez
afficher, sérialiser ou reporter sur un form. Les constraints se déclarent de
manière **déclarative** (attributs PHP en priorité) et sont appliquées par un
service `ValidatorInterface` que le framework câble pour vous.

Cette étape enseigne le modèle constraint/validator depuis les fondations : comment
les métadonnées sont chargées, comment fonctionnent les portées et la cascade,
comment les groupes et les group sequences déterminent *quelles* règles s'exécutent
et *dans quel ordre*, et comment construire vos propres constraints et violations.
C'est le prérequis direct de [Forms](../forms/index.md), qui lui délègue toute sa
validation.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [Dependency Injection](../dependency-injection/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stage 4 (DI) ; en binôme avec [Forms](../forms/index.md) |
    | **Revision priority** | **Medium** |
    | **Est. time** | 3–4 h |

## Why this stage matters

La validation est un composant que l'examen teste à la fois au niveau de
l'*usage* (quelle constraint intégrée, quelle option) et au niveau des
*mécanismes* (groupe Default vs `{ClassName}`, group sequences, cascade avec
`Valid`). Ce sont les subtilités — pas le catalogue — qui font gagner ou perdre
des points. Intégrez le modèle mental **métadonnées → contexte → violations** et
tout le reste se met en place naturellement.

## Micro-chapters

Travaillez-les dans l'ordre :

- [ ] [PHP Object Validation](object-validation.md) — attributs sur les
  propriétés, les getters et les classes ; `validate()` vs `validateProperty()` ;
  comment les métadonnées se chargent.
- [ ] [Built-in Constraints](built-in-constraints.md) — le catalogue par
  catégorie, centré sur ce que l'examen demande réellement.
- [ ] [Validation Scopes](scopes.md) — constraints de propriété vs getter vs
  classe ; cascade sur les objets imbriqués et les collections avec
  `#[Assert\Valid]`.
- [ ] [Validation Groups](groups.md) — le groupe `Default`, les groupes nommés,
  et l'interaction `Default` vs `{ClassName}`.
- [ ] [Group Sequence](group-sequence.md) — `#[Assert\GroupSequence]`,
  l'arrêt au premier échec, et `GroupSequenceProvider`.
- [ ] [Custom Callback Validators](callbacks.md) — `#[Assert\Callback]` et
  l'utilisation de l'`ExecutionContext` pour construire des violations à la volée.
- [ ] [Custom Constraints](custom-constraints.md) — `Constraint` +
  `ConstraintValidator`, `getTargets()`, `validatedBy()`, `#[HasNamedArguments]`.
- [ ] [Violations Builder](violations-builder.md) — `buildViolation()`,
  `setParameter`/`atPath`/`setInvalidValue`/`setCode`, la lecture de la liste.

## How to study it

1. Commencez par [Object Validation](object-validation.md) — le flux central de
   `validate()` et le chargement des métadonnées sous-tendent tout le reste.
2. Parcourez le catalogue des [Built-in Constraints](built-in-constraints.md),
   puis apprenez les [Scopes](scopes.md) pour savoir *où* une constraint peut se
   placer.
3. Maîtrisez le trio favori de l'examen : [Groups](groups.md),
   [Group Sequence](group-sequence.md), et le piège Default/`{ClassName}`.
4. Terminez par les points d'extension : [Callbacks](callbacks.md),
   [Custom Constraints](custom-constraints.md) et le
   [Violations Builder](violations-builder.md).

---

<small>Related: [Dependency Injection](../dependency-injection/index.md) ·
[Forms](../forms/index.md) · [Twig](../twig/index.md)</small>

## Official References

- [Symfony documentation — Validation](https://symfony.com/doc/current/validation.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
