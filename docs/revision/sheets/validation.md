# Revision Sheet — Data Validation

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Data Validation](../../validation/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Une **fiche imprimable, tenant sur une page**, qui résume chaque sous-chapitre de Data Validation en quelques puces "à retenir" suivies d'une ligne "Cheat" très dense.

**Pourquoi ça existe ?** Dans les derniers jours avant l'examen, on veut un support papier ou PDF unique par domaine — pas 10 onglets de navigateur ouverts. Cette fiche condense un domaine entier sur une seule page imprimable.

**🏠 Analogie de la vraie vie :** C'est la **fiche de révision recto-verso** qu'un étudiant prépare avant un examen universitaire : tout le cours du semestre réduit à une page, à relire dans le métro le matin de l'épreuve.

**Symfony dans la vraie vie :** Chaque puce "à retenir" → une règle déjà apprise en détail dans le chapitre / La ligne "Cheat:" → la version ultra-compacte, presque un aide-mémoire de syntaxe / Lien "Full detail" → retour au chapitre complet si un point ne "sonne" plus familier.

**⚠️ Erreur fréquente :** Imprimer cette fiche *avant* d'avoir étudié Data Validation en détail, en espérant apprendre directement dessus — le format est trop dense pour un premier apprentissage, il ne fonctionne qu'en rappel.

**🧠 Comment le mémoriser :** *« Une page, un domaine, la veille de l'examen »* — cette fiche est le tout dernier support à consulter, pas le premier.

## Built-in Constraints
- `NotBlank` rejects empty; `NotNull` only rejects `null`.
- `Email`/`Url`/`Regex` pass on empty — stack with `NotBlank` when needed.
- `All` = each element; `Collection` = keyed array; `Valid` = cascade.
- Comparison constraints can target another field via `propertyPath`.
- `When` applies constraints conditionally via an expression.

**Cheat:** Basic: `NotBlank`, `NotNull`, `IsNull`, `IsTrue`/`IsFalse`, `Blank`. String: `Length`, `Regex`, `Email`, `Url`. Number: `Range`, `Positive(OrZero)`, `Negative(OrZero)`, `GreaterThan(OrEqual)`. Compare: `EqualTo` (`==`) vs `IdenticalTo` (`===`), `propertyPath` option. Collection: `Collection`, `Count`, `Unique`, `All`, `Valid`. Conditional: `When(expression, constraints)`.

## Custom Callback Validators
- `#[Assert\Callback]` on a method runs arbitrary class-level validation.
- Instance: `(ExecutionContextInterface, mixed $payload)`; static: object first.
- Add errors via `$context->buildViolation()->addViolation()`.
- Callbacks respect `groups` and participate in sequences.

**Cheat:** Attribute on a method → `(ExecutionContextInterface $context, mixed $payload)`. `callback: [Class, 'method']` → static, object is 1st arg. Class-scoped: read object via `$this` / `$context->getObject()`. `atPath('field')` to attribute the error to a property.

## Custom Constraints
- A custom constraint = `Constraint` (options/message) + `ConstraintValidator`
  (logic).
- `validatedBy()` defaults to name + `Validator`.
- Override `getTargets()` → `CLASS_CONSTRAINT` for class-level rules.
- Guard the constraint type; skip empty/null; use `#[HasNamedArguments]`.
- Validators are services — inject dependencies freely.

**Cheat:** `extends Constraint`; public props = options; `message` = template. `#[HasNamedArguments]` for typed named options; forward `$groups`/`$payload`. `getTargets()`: `PROPERTY_CONSTRAINT` (default) / `CLASS_CONSTRAINT`. `extends ConstraintValidator` → `validate($value, Constraint $c): void`, use `$this->context`. Class validator: `$value` is the object.

## Group Sequence
- `#[Assert\GroupSequence]` runs groups in order, stopping at the first failing
  group.
- It fires when validating `Default`; `{ClassName}` bypasses it.
- Reference `{ClassName}`, never `Default`, inside the sequence.
- `GroupSequenceProvider` computes the order from object state via
  `getGroupSequence()`.

**Cheat:** `#[Assert\GroupSequence(['ClassName', 'Extra'])]` at class scope. Stop-on-first-failing-**group** (not constraint). Provider: `#[Assert\GroupSequenceProvider]` + `implements GroupSequenceProviderInterface`. `getGroupSequence(): array|GroupSequence`.

## Validation Groups
- Default group is `Default`; unnamed constraints belong to it.
- Passing a custom group excludes `Default` unless you list it.
- `{ClassName}` = short-name group; equals `Default` unless a sequence exists.
- On a sequenced class: `Default` = run sequence, `{ClassName}` = flat run.

**Cheat:** `groups` option default: `['Default']`. `validate($o, groups: ['g'])` runs only `g`. Sequenced class: `Default` → sequence; `{ShortClassName}` → no sequence. Case-sensitive; capital-D `Default`.

## PHP Object Validation
- `validate()` returns a `ConstraintViolationListInterface`; check `count()`.
- `validateProperty()` uses current state; `validatePropertyValue()` uses a
  supplied value.
- Metadata comes from `AttributeLoader` → `ClassMetadata`, cached per class.
- Autowire `ValidatorInterface`; never instantiate the validator yourself.

**Cheat:** Service: `Symfony\Component\Validator\Validator\ValidatorInterface`. Returns `ConstraintViolationListInterface` — `count()`, iterable, `__toString()`. Scopes: property · getter (`isX`/`getX`/`hasX` return value) · class. Metadata: `AttributeLoader` → `ClassMetadata`, PSR-6 cached. `debug:validator "App\Entity\X"` lists the mapped constraints.

## Validation Scopes
- Three scopes: property, getter (return value), class (whole object).
- Cross-field rules belong at class scope.
- Nested objects/collections validate only with `#[Assert\Valid]`.
- The cascaded group is the *current* group; `Valid` never changes groups.

**Cheat:** Getter path: `isX`/`getX`/`hasX` → `x`. Class-scope constraints must target the class (`CLASS_CONSTRAINT`). `Valid` = cascade; `traverse` (default true) controls iterating a collection. Object collection → `#[Assert\Valid]`; scalar collection → `All`.

## Violations Builder
- `buildViolation()` → fluent builder; commit with `addViolation()`.
- Setters: `setParameter`, `atPath`, `setInvalidValue`, `setCode`, `setPlural`.
- `getMessage()` (interpolated) vs `getMessageTemplate()` (raw).
- The result is a Countable/iterable `ConstraintViolationListInterface`.

**Cheat:** `$this->context->buildViolation($msg)->setParameter('{{ x }}', $v)->addViolation();` Shortcut: `$this->context->addViolation($msg, $params)`. Read: `getPropertyPath()`, `getMessage()`, `getCode()`, `getInvalidValue()`. List: `count()`, `foreach`, `findByCodes()`, `__toString()`.
