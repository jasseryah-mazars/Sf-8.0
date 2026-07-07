---
tags:
  - Labs
  - Validation
---

# Lab : Constraint + Validator personnalisés — une règle `StrongPassword`

!!! abstract "Practical Lab"
    **Objective:** construire et tester une paire réutilisable `Constraint` + `ConstraintValidator`
    à partir de zéro, en la pilotant avec le harnais de test du Validator lui-même ·
    **Difficulty:** Moyenne ·
    **Theory:** [Custom Constraints](../validation/custom-constraints.md) ·
    [Violations Builder](../validation/violations-builder.md) ·
    **Mode:** TDD

## Objective

À l'issue de ce lab, vous saurez **écrire une règle de validation personnalisée en test-first** : vérifier que
les valeurs valides ne lèvent aucune violation, que les valeurs invalides lèvent exactement une violation
avec le bon template de message, les bons paramètres, la valeur invalide et le code, et que le
validator protège ses entrées avec `UnexpectedTypeException` /
`UnexpectedValueException`. Vous implémentez ensuite la `Constraint` (options,
`getTargets()`, `#[HasNamedArguments]`) et le `ConstraintValidator` qui fait passer
le test au vert.

La règle : une constraint de propriété `#[StrongPassword]`. Une valeur passe quand elle fait au
moins `minLength` caractères (12 par défaut) **et** contient au moins une lettre
**et** au moins un chiffre. `null`/`''` passent par convention (composez avec
`NotBlank`).

## Prerequisites

- Chapitres : [Custom Constraints](../validation/custom-constraints.md),
  [Violations Builder](../validation/violations-builder.md)
- Compétences supposées acquises : les bases de PHPUnit, les attributs, `preg_match`, et le
  contrat de `ConstraintValidator` (`validate(mixed $value, Constraint $constraint)`).

## TD Instructions

Étapes numérotées, façon TD universitaire. Faites chacune vous-même avant d'ouvrir la solution.

1. Créez `tests/Validator/StrongPasswordValidatorTest.php` étendant
   `Symfony\Component\Validator\Test\ConstraintValidatorTestCase`. Implémentez la
   méthode abstraite `createValidator()` pour retourner votre validator (pas encore écrit).
2. **Red.** Écrivez ces méthodes de test, en utilisant uniquement l'API du harnais
   (`$this->validator->validate()`, `$this->assertNoViolation()`,
   `$this->buildViolation(...)->...->assertRaised()`) :
    - `null` et `''` ne lèvent **aucune** violation.
    - un mot de passe fort (`'C0rrectHorseBattery'`) ne lève **aucune** violation.
    - un mot de passe faible (`'abc'`) lève **une** violation avec le template
      de message attendu, les paramètres `{{ value }}` et `{{ limit }}`, la valeur invalide
      et le code `WEAK_PASSWORD_ERROR`.
    - passer la **mauvaise constraint** (`new NotBlank()`) lève
      `UnexpectedTypeException`.
    - passer une valeur **non-string** (`12345`) lève `UnexpectedValueException`.
   Lancez-le ; observez chaque test échouer (les classes n'existent pas encore).
3. **Green — la Constraint.** Créez `src/Validator/StrongPassword.php` :
   `extends Constraint`, `#[\Attribute(...TARGET_PROPERTY | IS_REPEATABLE)]`, une
   option `public int $minLength = 12`, un template `public string $message` avec
   les placeholders `{{ value }}` et `{{ limit }}`, une constante de code `WEAK_PASSWORD_ERROR`,
   un constructeur `#[HasNamedArguments]` transmettant `$groups`/`$payload`,
   et `getTargets()`.
4. **Green — le Validator.** Créez `src/Validator/StrongPasswordValidator.php` :
   `extends ConstraintValidator` ; protégez le type de la constraint, ignorez null/vide,
   protégez le type de la valeur, puis `buildViolation()->setParameter()->…->addViolation()`.
5. Relancez le test — tout au vert. **Refactorisez** (extrayez les trois vérifications dans
   des variables locales lisibles) avec le test comme filet de sécurité.
6. Câblez-la sur une propriété d'entité (`#[Assert\NotBlank] #[StrongPassword]`) et
   confirmez avec `php bin/console debug:validator`.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification · respectez
    les bonnes pratiques (attributs, strict types, `readonly`/propriétés typées quand c'est pertinent).

## Implementation Guide (partial)

Uniquement des repères de haut niveau — pas le code complet.

- **Classe de base de test :** `Symfony\Component\Validator\Test\ConstraintValidatorTestCase`
  câble pour vous un faux `ExecutionContext`. Implémentez `createValidator()` ; il
  injecte le contexte via `initialize()`. Assertions :
  `assertNoViolation()` et `buildViolation($template)->setParameter(...)
  ->setInvalidValue(...)->setCode(...)->assertRaised()`.
- **`formatValue()` compte pour l'assertion :** `ConstraintValidator::formatValue('abc')`
  retourne la chaîne entourée de guillemets → `"abc"`. Le test attend donc
  `setParameter('{{ value }}', '"abc"')`, pas `'abc'`.
- **Chemin de propriété par défaut :** une constraint de propriété lève à `property.path` (la
  valeur par défaut du harnais) — vous n'appelez **pas** `atPath()`. `atPath()` sert à
  rediriger vers un autre champ (voir [Violations Builder](../validation/violations-builder.md)).
- **Gardes :** vérification `instanceof` → `UnexpectedTypeException` ; vérification string →
  `UnexpectedValueException`. Les deux vivent dans
  `Symfony\Component\Validator\Exception`.
- **Forme de la constraint :** les options sont des propriétés publiques ; `getTargets()` retourne
  `self::PROPERTY_CONSTRAINT` (la valeur par défaut — montrée explicitement ici) ;
  `#[HasNamedArguments]` active la construction typée par arguments nommés.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** le test ci-dessous référence des classes qui n'existent pas — il échoue au
       chargement. Parfait ; c'est votre barre rouge.
    2. **Green :** ajoutez la `Constraint` puis le `ConstraintValidator`.
    3. **Refactor :** peaufinez les trois vérifications booléennes ; le test vous garde honnête.

**Comportement (Given/When/Then) :**

- **Given** le `StrongPasswordValidator`, **When** il valide `null`, `''`, ou un
  mot de passe de ≥ `minLength` caractères contenant une lettre et un chiffre, **Then** aucune
  violation n'est levée.
- **Given** un mot de passe faible `'abc'`, **When** validé contre
  `new StrongPassword(minLength: 12)`, **Then** exactement une violation est levée
  avec le template de message, `{{ value }} = "abc"`, `{{ limit }} = 12`, la valeur
  invalide `'abc'`, et le code `WEAK_PASSWORD_ERROR`.
- **Given** une mauvaise constraint ou une valeur non-string, **When** validée, **Then**
  `UnexpectedTypeException` / `UnexpectedValueException` est levée.

```php
<?php
declare(strict_types=1);

namespace App\Tests\Validator;

use App\Validator\StrongPassword;
use App\Validator\StrongPasswordValidator;
use Symfony\Component\Validator\Constraints\NotBlank;
use Symfony\Component\Validator\ConstraintValidatorInterface;
use Symfony\Component\Validator\Exception\UnexpectedTypeException;
use Symfony\Component\Validator\Exception\UnexpectedValueException;
use Symfony\Component\Validator\Test\ConstraintValidatorTestCase;

final class StrongPasswordValidatorTest extends ConstraintValidatorTestCase
{
    protected function createValidator(): ConstraintValidatorInterface
    {
        return new StrongPasswordValidator();
    }

    public function testNullAndEmptyStringRaiseNoViolation(): void
    {
        $this->validator->validate(null, new StrongPassword());
        $this->validator->validate('', new StrongPassword());

        $this->assertNoViolation();
    }

    public function testStrongPasswordRaisesNoViolation(): void
    {
        $this->validator->validate('C0rrectHorseBattery', new StrongPassword());

        $this->assertNoViolation();
    }

    public function testWeakPasswordRaisesViolationWithParametersAndCode(): void
    {
        $constraint = new StrongPassword(minLength: 12);

        $this->validator->validate('abc', $constraint);

        $this->buildViolation('The password "{{ value }}" is too weak: use at least {{ limit }} characters, including letters and digits.')
            ->setParameter('{{ value }}', '"abc"')   // formatValue() quotes strings
            ->setParameter('{{ limit }}', '12')
            ->setInvalidValue('abc')
            ->setCode(StrongPassword::WEAK_PASSWORD_ERROR)
            ->assertRaised();
    }

    public function testWrongConstraintTypeThrows(): void
    {
        $this->expectException(UnexpectedTypeException::class);

        $this->validator->validate('anything', new NotBlank());
    }

    public function testNonStringValueThrows(): void
    {
        $this->expectException(UnexpectedValueException::class);

        $this->validator->validate(12345, new StrongPassword());
    }
}
```

!!! tip "Setup hints"
    Lancez-le : `vendor/bin/phpunit tests/Validator/StrongPasswordValidatorTest.php`.
    Aucun mock nécessaire — `ConstraintValidatorTestCase` construit un faux
    `ExecutionContext` et expose `$this->validator` (votre validator, déjà
    passé par `initialize()`) plus l'assertion fluide
    `buildViolation(...)->assertRaised()`. `assertNoViolation()` est votre vert par défaut.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Validator/StrongPasswordValidatorTest.php` — les
      cinq tests au vert.
- [ ] `php bin/console debug:validator "App\Entity\Account"` liste
      `App\Validator\StrongPassword` sur la propriété `password`.
- [ ] Soumettez une valeur faible via un form/DTO et confirmez que le message interpolé
      affiche la vraie limite de longueur et la valeur fautive.

## Review — Common Mistakes

- **Attendre `'abc'` au lieu de `'"abc"'` pour `{{ value }}`** → le test échoue sur
  un paramètre non concordant. `formatValue()` entoure les chaînes de guillemets ; vérifiez la
  valeur formatée.
- **Appeler `atPath('password')` dans le validator** → le harnais attend
  `property.path` ; une constraint au niveau propriété cible déjà la propriété. Ne
  redirigez que pour rapporter sur un champ *différent*.
- **Oublier `addViolation()`** → le builder n'enregistre rien ; le test du mot de passe
  faible échoue avec « no violation raised ». Tout l'intérêt du builder est qu'il
  ne valide qu'au moment de `addViolation()`.
- **Sauter la garde `instanceof`** → les analyseurs statiques ne peuvent pas affiner le type et
  l'examen teste explicitement l'étape `UnexpectedTypeException` en premier.
- **Rejeter `null`/`''`** → casse la composition avec `NotBlank` ; le test de la valeur
  vide échoue. Laissez une constraint dédiée imposer « obligatoire ».
- **Laisser tomber `$groups`/`$payload`** dans `parent::__construct()` → la constraint
  ignore silencieusement les groupes de validation.

## Exam Connection

La certification teste le *contrat*, pas des regex astucieuses :

- Le **premier acte** du validator est la garde `instanceof` →
  `UnexpectedTypeException` ; une garde sur les valeurs non scalaires → `UnexpectedValueException`.
- Les violations sont **construites et validées** via
  `buildViolation()->setParameter()->addViolation()` ; les placeholders utilisent
  `{{ name }}` rempli par `setParameter`, jamais de concaténation de chaînes.
- `#[HasNamedArguments]` change la façon dont les arguments d'attribut sont mappés au constructeur, et une
  règle au niveau classe nécessiterait `getTargets()` → `CLASS_CONSTRAINT` (ici elle reste
  `PROPERTY_CONSTRAINT`).
- `ConstraintValidatorTestCase` est la façon *documentée* de tester unitairement un validator —
  connaître `createValidator()`, `assertNoViolation()` et la chaîne
  `buildViolation(...)->assertRaised()` fait partie du jeu.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    ```php
    <?php
    declare(strict_types=1);

    // src/Validator/StrongPassword.php
    namespace App\Validator;

    use Symfony\Component\Validator\Attribute\HasNamedArguments;
    use Symfony\Component\Validator\Constraint;

    #[\Attribute(\Attribute::TARGET_PROPERTY | \Attribute::IS_REPEATABLE)]
    final class StrongPassword extends Constraint
    {
        public const string WEAK_PASSWORD_ERROR = 'f5e6a7b8-1c2d-3e4f-5a6b-7c8d9e0f1a2b';

        protected const ERROR_NAMES = [
            self::WEAK_PASSWORD_ERROR => 'WEAK_PASSWORD_ERROR',
        ];

        public string $message = 'The password "{{ value }}" is too weak: use at least {{ limit }} characters, including letters and digits.';

        #[HasNamedArguments]
        public function __construct(
            public int $minLength = 12,
            ?string $message = null,
            ?array $groups = null,
            mixed $payload = null,
        ) {
            parent::__construct([], $groups, $payload);

            $this->message = $message ?? $this->message;
        }

        public function getTargets(): string
        {
            return self::PROPERTY_CONSTRAINT; // default; shown for clarity
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Validator/StrongPasswordValidator.php
    namespace App\Validator;

    use Symfony\Component\Validator\Constraint;
    use Symfony\Component\Validator\ConstraintValidator;
    use Symfony\Component\Validator\Exception\UnexpectedTypeException;
    use Symfony\Component\Validator\Exception\UnexpectedValueException;

    final class StrongPasswordValidator extends ConstraintValidator
    {
        public function validate(mixed $value, Constraint $constraint): void
        {
            if (!$constraint instanceof StrongPassword) {
                throw new UnexpectedTypeException($constraint, StrongPassword::class);
            }

            // Convention: null/empty pass — compose with #[Assert\NotBlank].
            if (null === $value || '' === $value) {
                return;
            }

            if (!\is_string($value)) {
                throw new UnexpectedValueException($value, 'string');
            }

            $longEnough = mb_strlen($value) >= $constraint->minLength;
            $hasLetter = 1 === preg_match('/\p{L}/u', $value);
            $hasDigit = 1 === preg_match('/\p{N}/u', $value);

            if ($longEnough && $hasLetter && $hasDigit) {
                return;
            }

            $this->context->buildViolation($constraint->message)
                ->setParameter('{{ value }}', $this->formatValue($value))
                ->setParameter('{{ limit }}', (string) $constraint->minLength)
                ->setInvalidValue($value)
                ->setCode(StrongPassword::WEAK_PASSWORD_ERROR)
                ->addViolation();
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Entity/Account.php — usage
    namespace App\Entity;

    use App\Validator\StrongPassword;
    use Symfony\Component\Validator\Constraints as Assert;

    final class Account
    {
        #[Assert\NotBlank]
        #[StrongPassword(minLength: 12)]
        public string $password = '';
    }
    ```

## Alternative Approaches (optional)

- **Option A (simple) :** une violation, un message (ce lab) — le plus propre à tester
  et à interpoler.
- **Option B (avancée) :** levez une **violation distincte par règle échouée**
  (trop court / pas de lettre / pas de chiffre), chacune avec sa propre constante de code ; le test
  chaîne alors `->buildNextViolation(...)` dans `ConstraintValidatorTestCase`.
- **Option C (exam-style) :** promouvez-la en règle **au niveau classe** qui
  interdit aussi que le mot de passe soit égal au nom d'utilisateur — `getTargets()` retourne
  `CLASS_CONSTRAINT`, `$value` devient l'objet, et vous appelez `atPath('password')` pour
  rapporter sur le champ.

---

<small>Theory: [Custom Constraints](../validation/custom-constraints.md) ·
[Violations Builder](../validation/violations-builder.md) · Labs: [all labs](index.md)</small>
