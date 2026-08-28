---
tags:
  - Labs
  - Validation
---

# Lab: Custom Constraint + Validator — a `StrongPassword` rule

!!! abstract "Practical Lab"
    **Objective:** build and test a reusable `Constraint` + `ConstraintValidator`
    pair from scratch, driving it with the Validator's own test harness ·
    **Difficulty:** Medium ·
    **Theory:** [Custom Constraints](../validation/custom-constraints.md) ·
    [Violations Builder](../validation/violations-builder.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Construire ta propre règle de validation réutilisable (ici, "mot de passe suffisamment fort") au lieu d'utiliser uniquement les contraintes déjà fournies par Symfony.

**Pourquoi ça existe ?** Les contraintes intégrées (`NotBlank`, `Email`...) ne couvrent pas des règles métier spécifiques — savoir créer les tiennes est indispensable dès qu'un projet a des besoins particuliers.

**🏠 Analogie de la vraie vie :** Un scanner sur mesure à l'aéroport, conçu spécifiquement pour détecter un objet que les scanners standards ne repèrent pas — deux pièces séparées : la machine qui déclare ce qu'elle cherche (la `Constraint`), et l'opérateur qui l'applique réellement (le `ConstraintValidator`).

**Symfony dans la vraie vie :** `#[StrongPassword]` sur une propriété déclenche automatiquement ton `ConstraintValidator` personnalisé, exactement comme `#[Assert\Email]` déclenche le validateur intégré d'email.

**⚠️ Erreur fréquente :** oublier de gérer le cas `null`/vide dans le validateur — par convention, une valeur vide est valide (c'est `NotBlank` qui doit s'en occuper séparément), pas ta contrainte personnalisée.

**🧠 Comment le mémoriser :** "Deux classes, un seul travail : la Constraint décrit la règle, le Validator l'applique."

## Objective

After this lab you can **write a custom validation rule test-first**: assert that
valid values raise no violation, that invalid ones raise exactly one violation
with the right message template, parameters, invalid value and code, and that the
validator guards its inputs with `UnexpectedTypeException` /
`UnexpectedValueException`. Then you implement the `Constraint` (options,
`getTargets()`, `#[HasNamedArguments]`) and the `ConstraintValidator` that makes
the test green.

The rule: a `#[StrongPassword]` property constraint. A value passes when it is at
least `minLength` characters (default 12) **and** contains at least one letter
**and** at least one digit. `null`/`''` pass by convention (compose with
`NotBlank`).

## Prerequisites

- Chapters: [Custom Constraints](../validation/custom-constraints.md),
  [Violations Builder](../validation/violations-builder.md)
- Assumed skills: PHPUnit basics, attributes, `preg_match`, and the
  `ConstraintValidator` contract (`validate(mixed $value, Constraint $constraint)`).

## TD Instructions

Numbered, university-TD-style steps. Do each yourself before opening the solution.

1. Create `tests/Validator/StrongPasswordValidatorTest.php` extending
   `Symfony\Component\Validator\Test\ConstraintValidatorTestCase`. Implement the
   abstract `createValidator()` to return your (not-yet-written) validator.
2. **Red.** Write these test methods, using only the harness API
   (`$this->validator->validate()`, `$this->assertNoViolation()`,
   `$this->buildViolation(...)->...->assertRaised()`):
    - `null` and `''` raise **no** violation.
    - a strong password (`'C0rrectHorseBattery'`) raises **no** violation.
    - a weak password (`'abc'`) raises **one** violation with the expected
      message template, `{{ value }}` and `{{ limit }}` parameters, invalid value
      and `WEAK_PASSWORD_ERROR` code.
    - passing the **wrong constraint** (`new NotBlank()`) throws
      `UnexpectedTypeException`.
    - passing a **non-string** value (`12345`) throws `UnexpectedValueException`.
   Run it; watch every test fail (the classes don't exist yet).
3. **Green — the Constraint.** Create `src/Validator/StrongPassword.php`:
   `extends Constraint`, `#[\Attribute(...TARGET_PROPERTY | IS_REPEATABLE)]`, a
   `public int $minLength = 12` option, a `public string $message` template with
   `{{ value }}` and `{{ limit }}` placeholders, a `WEAK_PASSWORD_ERROR` code
   constant, a `#[HasNamedArguments]` constructor forwarding `$groups`/`$payload`,
   and `getTargets()`.
4. **Green — the Validator.** Create `src/Validator/StrongPasswordValidator.php`:
   `extends ConstraintValidator`; guard the constraint type, skip null/empty,
   guard the value type, then `buildViolation()->setParameter()->…->addViolation()`.
5. Run the test again — all green. **Refactor** (extract the three checks into
   readable locals) with the test as your safety net.
6. Wire it onto an entity property (`#[Assert\NotBlank] #[StrongPassword]`) and
   confirm with `php bin/console debug:validator`.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, strict types, `readonly`/typed props where apt).

## Implementation Guide (partial)

High-level pointers only — not the full code.

- **Test base class:** `Symfony\Component\Validator\Test\ConstraintValidatorTestCase`
  wires a fake `ExecutionContext` for you. Implement `createValidator()`; it
  injects the context via `initialize()`. Assertions:
  `assertNoViolation()` and `buildViolation($template)->setParameter(...)
  ->setInvalidValue(...)->setCode(...)->assertRaised()`.
- **`formatValue()` matters for the assertion:** `ConstraintValidator::formatValue('abc')`
  returns the string wrapped in quotes → `"abc"`. So the test expects
  `setParameter('{{ value }}', '"abc"')`, not `'abc'`.
- **Default property path:** a property constraint raises at `property.path` (the
  harness default) — you do **not** call `atPath()`. `atPath()` is for
  redirecting to another field (see [Violations Builder](../validation/violations-builder.md)).
- **Guards:** `instanceof` check → `UnexpectedTypeException`; string check →
  `UnexpectedValueException`. Both live in
  `Symfony\Component\Validator\Exception`.
- **Constraint shape:** options are public properties; `getTargets()` returns
  `self::PROPERTY_CONSTRAINT` (the default — shown explicitly here);
  `#[HasNamedArguments]` opts into typed named-argument construction.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** the test below references classes that don't exist — it fails to
       load. Good; that is your red bar.
    2. **Green:** add the `Constraint` then the `ConstraintValidator`.
    3. **Refactor:** tidy the three boolean checks; the test keeps you honest.

**Behaviour (Given/When/Then):**

- **Given** the `StrongPasswordValidator`, **When** it validates `null`, `''`, or a
  password with ≥ `minLength` chars containing a letter and a digit, **Then** no
  violation is raised.
- **Given** a weak password `'abc'`, **When** validated against
  `new StrongPassword(minLength: 12)`, **Then** exactly one violation is raised
  with the message template, `{{ value }} = "abc"`, `{{ limit }} = 12`, invalid
  value `'abc'`, and code `WEAK_PASSWORD_ERROR`.
- **Given** a wrong constraint or a non-string value, **When** validated, **Then**
  `UnexpectedTypeException` / `UnexpectedValueException` is thrown.

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
    Run it: `vendor/bin/phpunit tests/Validator/StrongPasswordValidatorTest.php`.
    No mocks needed — `ConstraintValidatorTestCase` builds a fake
    `ExecutionContext` and exposes `$this->validator` (your validator, already
    `initialize()`-d) plus the fluent `buildViolation(...)->assertRaised()`
    assertion. `assertNoViolation()` is your default green.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Validator/StrongPasswordValidatorTest.php` — all
      five tests green.
- [ ] `php bin/console debug:validator "App\Entity\Account"` lists
      `App\Validator\StrongPassword` on the `password` property.
- [ ] Submit a weak value through a form/DTO and confirm the interpolated message
      shows the real length limit and the offending value.

## Review — Common Mistakes

- **Expecting `'abc'` instead of `'"abc"'` for `{{ value }}`** → the test fails on
  a parameter mismatch. `formatValue()` wraps strings in quotes; assert the
  formatted value.
- **Calling `atPath('password')` in the validator** → the harness expects
  `property.path`; a property-level constraint already targets the property. Only
  redirect when reporting on a *different* field.
- **Forgetting `addViolation()`** → the builder records nothing; the weak-password
  test fails with "no violation raised". The whole point of the builder is that
  it commits only on `addViolation()`.
- **Skipping the `instanceof` guard** → static analysers can't narrow the type and
  the exam explicitly tests the `UnexpectedTypeException` first step.
- **Rejecting `null`/`''`** → breaks composition with `NotBlank`; the empty-value
  test fails. Let a dedicated constraint enforce "required".
- **Dropping `$groups`/`$payload`** from `parent::__construct()` → the constraint
  silently ignores validation groups.

## Exam Connection

The certification tests the *contract*, not clever regexes:

- The validator's **first act** is the `instanceof` guard →
  `UnexpectedTypeException`; a non-scalar value guard → `UnexpectedValueException`.
- Violations are **built and committed** via
  `buildViolation()->setParameter()->addViolation()`; placeholders use
  `{{ name }}` filled by `setParameter`, never string concatenation.
- `#[HasNamedArguments]` changes how attribute args map to the constructor, and a
  class-level rule would need `getTargets()` → `CLASS_CONSTRAINT` (here it stays
  `PROPERTY_CONSTRAINT`).
- `ConstraintValidatorTestCase` is the *documented* way to unit-test a validator —
  knowing `createValidator()`, `assertNoViolation()`, and the
  `buildViolation(...)->assertRaised()` chain is fair game.

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

- **Option A (simple):** one violation, one message (this lab) — cleanest to test
  and interpolate.
- **Option B (advanced):** raise a **distinct violation per failed rule**
  (too short / no letter / no digit), each with its own code constant; the test
  then chains `->buildNextViolation(...)` in `ConstraintValidatorTestCase`.
- **Option C (exam-style):** promote it to a **class-level** rule that also
  forbids the password from equalling the username — `getTargets()` returns
  `CLASS_CONSTRAINT`, `$value` becomes the object, and you `atPath('password')` to
  report on the field.

---

<small>Theory: [Custom Constraints](../validation/custom-constraints.md) ·
[Violations Builder](../validation/violations-builder.md) · Labs: [all labs](index.md)</small>
