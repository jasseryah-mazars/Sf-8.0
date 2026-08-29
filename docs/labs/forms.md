---
tags:
  - Labs
  - Forms
---

# Lab: Data Transformer — A `GeoPointType` field backed by a value object

!!! abstract "Practical Lab"
    **Objective:** build a reusable form field whose *view* is a `"lat,lng"` string
    but whose *model* is an immutable `GeoPoint` value object, via a
    `DataTransformerInterface` ·
    **Difficulty:** Advanced ·
    **Theory:** [Data transformers](../forms/data-transformers.md) ·
    [Form types](../forms/types.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Faire qu'un simple champ texte du navigateur (`"48.85,2.35"`) devienne automatiquement un vrai objet PHP typé (`GeoPoint`) côté serveur, et inversement à l'affichage.

**Pourquoi ça existe ?** Sans transformateur, il faudrait convertir manuellement cette chaîne en objet à chaque soumission de formulaire, et reconvertir l'objet en chaîne à chaque affichage — le transformateur automatise ces deux sens.

**🏠 Analogie de la vraie vie :** Un bureau de change à une frontière : `transform()` convertit ta monnaie locale (l'objet PHP) en devise étrangère pour l'affichage (la vue) ; `reverseTransform()` fait l'inverse quand la monnaie étrangère revient.

**Symfony dans la vraie vie :** Le visiteur voit et remplit `"48.85,2.35"` dans un simple champ texte, mais ton contrôleur reçoit directement un objet `GeoPoint` déjà validé et typé, prêt à l'emploi.

**⚠️ Erreur fréquente :** confondre `addModelTransformer` et `addViewTransformer` — l'un transforme entre modèle et normalisé, l'autre entre normalisé et vue ; les inverser casse la conversion.

**🧠 Comment le mémoriser :** "`transform` va vers l'écran (vue) ; `reverseTransform` revient vers l'objet (modèle)."

## Objective

After this lab you can turn a plain text field into a *typed* field: the browser
sends a string, your controller receives a `GeoPoint` object (or a cleanly
invalidated form). You will be able to:

- implement `transform()`/`reverseTransform()` in the **correct directions**;
- fail a bad conversion with `TransformationFailedException` instead of a 500;
- wire the transformer into a custom type built on `TextType` with `getParent()`;
- prove the whole field works end-to-end with `TypeTestCase` — no browser, no
  kernel, no database.

## Prerequisites

- Chapters: [Data transformers](../forms/data-transformers.md) ·
  [Form types](../forms/types.md) · [Handling submissions](../forms/handling.md)
- Assumed skills: PHPUnit basics, PHP 8.4 readonly classes, the model/norm/view
  data model of a Symfony form.

## TD Instructions

You will model a coordinate field. The **model** value is a `GeoPoint` value
object `(latitude, longitude)`; the **view** value is the string `"48.8566,2.3522"`.

1. Create an immutable `App\Form\Model\GeoPoint` value object with two `float`
   properties, guarding latitude to `-90..90` and longitude to `-180..180` in its
   constructor.
2. **Write the transformer test first** (`tests/Form/Transformer/…`). Cover both
   directions: `transform(null) === ''`, `transform(GeoPoint) === '48.8566,2.3522'`,
   `transform('a string')` throws, `reverseTransform('48.8566,2.3522')` equals the
   object, empty/whitespace/`null` give `null`, and a data-provider of malformed
   inputs each throws `TransformationFailedException`. Run it — watch it fail (Red).
3. Implement `App\Form\Transformer\GeoPointToStringTransformer` implementing
   `DataTransformerInterface` to make the test green. Handle empty/`null` **first**.
4. **Write the type test** with `TypeTestCase`: create the form through the test
   `factory`, `submit('48.8566,2.3522')`, assert `isSynchronized()` and that
   `getData()` is the expected `GeoPoint`; then submit garbage and assert the form
   is **not** synchronized and `getData()` is `null`.
5. Implement `App\Form\Type\GeoPointType` extending `AbstractType`: register the
   transformer with `addViewTransformer()`, set a helpful `invalid_message`, and
   return `TextType::class` from `getParent()`. Make step 4 pass.
6. Refactor with both tests green.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, strict types, `readonly` where apt).

## Implementation Guide (partial)

High-level pointers only — reach for these, don't copy the reference yet.

- **Value object:** `final readonly class GeoPoint` with promoted `public float`
  properties; throw `\InvalidArgumentException` from the constructor on an
  out-of-range coordinate. This is the *only* place range rules live.
- **Transformer:** `implements DataTransformerInterface`. Direction is the whole
  point: `transform()` is **model → view** (return a string), `reverseTransform()`
  is **view → model** (return a `GeoPoint|null`). Add the docblock
  `@implements DataTransformerInterface<GeoPoint|null, string>`.
- **Empty handling first:** `transform(null)` returns `''`; `reverseTransform('')`
  and whitespace-only / `null` return `null`. An optional field must not crash.
- **Failure path:** on an unparseable view string throw
  `Symfony\Component\Form\Exception\TransformationFailedException`. When the
  `GeoPoint` constructor rejects a coordinate, **catch** the
  `\InvalidArgumentException` and rethrow it as a `TransformationFailedException`
  (pass `previous:`), so a domain guard becomes an invalid *field*, not a 500.
- **Type:** since only the string representation changes, use
  `addViewTransformer()` (not model), parent = `TextType::class`, and set
  `invalid_message` in `configureOptions()`.
- **Type test:** a single-field type built on `TextType` *is* the field — call
  `->submit('…')` with a scalar (not an array). Register the type in the test
  factory with a `PreloadedExtension` so it resolves by FQCN.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the transformer test, run it, watch it fail (class missing).
    2. **Green:** write the minimum transformer + type to pass.
    3. **Refactor:** tidy up with the tests as your safety net.

**Behaviour (Given/When/Then):**

- **Given** the string `"48.8566,2.3522"` **When** the form is submitted **Then**
  `getData()` is `new GeoPoint(48.8566, 2.3522)` and the form is *synchronized*.
- **Given** a `GeoPoint` as preset model data **When** the view is built **Then**
  the view data is the string `"48.8566,2.3522"`.
- **Given** the string `"not-a-coordinate"` (or an out-of-range value) **When**
  submitted **Then** the transformer throws `TransformationFailedException`, the
  form is **not** synchronized and `getData()` is `null` — no exception escapes.

### 1 — Transformer unit test (both directions + failure)

```php
<?php
declare(strict_types=1);

namespace App\Tests\Form\Transformer;

use App\Form\Model\GeoPoint;
use App\Form\Transformer\GeoPointToStringTransformer;
use PHPUnit\Framework\TestCase;
use Symfony\Component\Form\Exception\TransformationFailedException;

final class GeoPointToStringTransformerTest extends TestCase
{
    private GeoPointToStringTransformer $transformer;

    protected function setUp(): void
    {
        $this->transformer = new GeoPointToStringTransformer();
    }

    // ---- transform(): model -> view ----

    public function testTransformNullGivesEmptyString(): void
    {
        self::assertSame('', $this->transformer->transform(null));
    }

    public function testTransformGeoPointGivesString(): void
    {
        $point = new GeoPoint(48.8566, 2.3522);

        self::assertSame('48.8566,2.3522', $this->transformer->transform($point));
    }

    public function testTransformRejectsNonGeoPoint(): void
    {
        $this->expectException(TransformationFailedException::class);

        $this->transformer->transform('48.8566,2.3522');
    }

    // ---- reverseTransform(): view -> model ----

    public function testReverseTransformParsesString(): void
    {
        self::assertEquals(
            new GeoPoint(48.8566, 2.3522),
            $this->transformer->reverseTransform('48.8566,2.3522'),
        );
    }

    public function testReverseTransformEmptyGivesNull(): void
    {
        self::assertNull($this->transformer->reverseTransform(''));
        self::assertNull($this->transformer->reverseTransform('   '));
        self::assertNull($this->transformer->reverseTransform(null));
    }

    /** @return iterable<string, array{string}> */
    public static function badInputs(): iterable
    {
        yield 'no comma'        => ['48.8566'];
        yield 'too many parts'  => ['1,2,3'];
        yield 'not numeric'     => ['north,east'];
        yield 'latitude range'  => ['91,2.3522'];
        yield 'longitude range' => ['48.8566,200'];
    }

    /** @dataProvider badInputs */
    public function testReverseTransformThrowsOnBadInput(string $input): void
    {
        $this->expectException(TransformationFailedException::class);

        $this->transformer->reverseTransform($input);
    }
}
```

### 2 — Form end-to-end test with `TypeTestCase`

```php
<?php
declare(strict_types=1);

namespace App\Tests\Form\Type;

use App\Form\Model\GeoPoint;
use App\Form\Type\GeoPointType;
use Symfony\Component\Form\PreloadedExtension;
use Symfony\Component\Form\Test\TypeTestCase;

final class GeoPointTypeTest extends TypeTestCase
{
    protected function getExtensions(): array
    {
        // Make the custom type resolvable by FQCN inside the test factory.
        return [new PreloadedExtension([new GeoPointType()], [])];
    }

    public function testSubmitValidStringBecomesGeoPoint(): void
    {
        $form = $this->factory->create(GeoPointType::class);

        $form->submit('48.8566,2.3522');

        self::assertTrue($form->isSynchronized());
        self::assertEquals(new GeoPoint(48.8566, 2.3522), $form->getData());
    }

    public function testPresetModelDataRendersAsString(): void
    {
        $form = $this->factory->create(GeoPointType::class, new GeoPoint(48.8566, 2.3522));

        self::assertSame('48.8566,2.3522', $form->getViewData());
    }

    public function testSubmitInvalidStringMarksFormNotSynchronized(): void
    {
        $form = $this->factory->create(GeoPointType::class);

        $form->submit('not-a-coordinate');

        self::assertFalse($form->isSynchronized());
        self::assertNull($form->getData());
    }
}
```

!!! tip "Setup hints"
    Run: `vendor/bin/phpunit tests/Form`. `TypeTestCase` gives you a ready
    `$this->factory` with the core extension already loaded, so `TextType` (the
    parent) resolves for free — but **your** type does not, hence the
    `PreloadedExtension` in `getExtensions()`. A single-field type built on
    `TextType` is the field itself, so `submit()` takes a **scalar** string, not an
    array. A transformer that throws on submit flips `isSynchronized()` to `false`
    and leaves `getData()` at its default (`null`) — that is exactly how a form
    "shows an error" instead of blowing up.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Form/Transformer/GeoPointToStringTransformerTest.php`
  is green (both directions + every bad input).
- [ ] `vendor/bin/phpunit tests/Form/Type/GeoPointTypeTest.php` is green.
- [ ] `php bin/console debug:form GeoPointType` lists the field and its
  `invalid_message` default.
- [ ] In a controller, `$form->getData()` returns a `GeoPoint` on success; an
  invalid submit renders `invalid_message` with no 500 in the profiler.

## Review — Common Mistakes

- **Swapped directions** → `transform()` returns the object and
  `reverseTransform()` returns the string → the field displays garbage and submits
  wrong. Fix: `transform` = **model → view** (string out), `reverseTransform` =
  **view → model** (object out).
- **Returning `null` / throwing `\InvalidArgumentException` on bad input** → the
  form thinks the value is valid, or a 500 escapes. Fix: throw
  `TransformationFailedException`; catch the value object's own
  `\InvalidArgumentException` and rethrow it as one.
- **No empty handling** → an optional field crashes on `''`/`null`. Fix: handle
  empty **first** in both methods.
- **`addModelTransformer()` for pure formatting** → wrong slot; here only the
  string representation changes, so it is a **view** transformer.
- **`submit(['value' => …])` in the type test** → this type is a single field, not
  a compound form; submit the scalar string directly.
- **Forgetting `getExtensions()`** → `Could not load type "App\Form\Type\GeoPointType"`.
  Register it with a `PreloadedExtension`.

## Exam Connection

The certification loves the **direction trap**: `transform()` is display
(model→view), `reverseTransform()` is submit (view→model). It also tests that a
failed conversion yields an **invalid form surfaced via `invalid_message`**, not
an exception — driven by `TransformationFailedException`, which flips
`isSynchronized()` to `false`. Knowing that a *view* transformer bridges norm↔view
(formatting) while a *model* transformer bridges model↔norm (object identity), and
that `getParent()` returns a **class string**, covers the rest of this topic's
questions.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    ```php
    <?php
    declare(strict_types=1);

    namespace App\Form\Model;

    /** Immutable value object: a WGS84 coordinate. No entity, no id. */
    final readonly class GeoPoint
    {
        public function __construct(
            public float $latitude,
            public float $longitude,
        ) {
            if ($latitude < -90.0 || $latitude > 90.0) {
                throw new \InvalidArgumentException('Latitude must be within -90..90.');
            }
            if ($longitude < -180.0 || $longitude > 180.0) {
                throw new \InvalidArgumentException('Longitude must be within -180..180.');
            }
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Form\Transformer;

    use App\Form\Model\GeoPoint;
    use Symfony\Component\Form\DataTransformerInterface;
    use Symfony\Component\Form\Exception\TransformationFailedException;

    /**
     * Model/norm: GeoPoint|null. View: "lat,lng" string.
     *
     * @implements DataTransformerInterface<GeoPoint|null, string>
     */
    final class GeoPointToStringTransformer implements DataTransformerInterface
    {
        // model -> view (display)
        public function transform(mixed $value): string
        {
            if (null === $value) {
                return '';
            }
            if (!$value instanceof GeoPoint) {
                throw new TransformationFailedException('Expected a GeoPoint or null.');
            }

            return \sprintf('%s,%s', $value->latitude, $value->longitude);
        }

        // view -> model (submit)
        public function reverseTransform(mixed $value): ?GeoPoint
        {
            if (null === $value || '' === trim((string) $value)) {
                return null;
            }
            if (!\is_string($value)) {
                throw new TransformationFailedException('Expected a string.');
            }

            $parts = explode(',', $value);
            if (2 !== \count($parts)) {
                throw new TransformationFailedException('Use the "lat,lng" format.');
            }

            [$lat, $lng] = array_map(trim(...), $parts);
            if (!is_numeric($lat) || !is_numeric($lng)) {
                throw new TransformationFailedException('Both coordinates must be numeric.');
            }

            try {
                return new GeoPoint((float) $lat, (float) $lng);
            } catch (\InvalidArgumentException $e) {
                // Turn a domain guard into a form-level failure, not a 500.
                throw new TransformationFailedException($e->getMessage(), previous: $e);
            }
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Form\Type;

    use App\Form\Transformer\GeoPointToStringTransformer;
    use Symfony\Component\Form\AbstractType;
    use Symfony\Component\Form\Extension\Core\Type\TextType;
    use Symfony\Component\Form\FormBuilderInterface;
    use Symfony\Component\OptionsResolver\OptionsResolver;

    /** A text field whose model value is a GeoPoint value object. */
    final class GeoPointType extends AbstractType
    {
        public function buildForm(FormBuilderInterface $builder, array $options): void
        {
            // View transformer: norm(GeoPoint) <-> view(string).
            $builder->addViewTransformer(new GeoPointToStringTransformer());
        }

        public function configureOptions(OptionsResolver $resolver): void
        {
            $resolver->setDefaults([
                'invalid_message' => 'Enter coordinates as "lat,lng" (e.g. 48.8566,2.3522).',
            ]);
        }

        public function getParent(): string
        {
            return TextType::class;
        }
    }
    ```

## Alternative Approaches (optional)

- **Option A (simple)** — skip the value object: transform a `"lat,lng"` string to
  a plain `['lat' => float, 'lng' => float]` array. Fewer moving parts, but you lose
  the constructor guard and type safety.
- **Option B (advanced)** — a **model** transformer instead: keep the view as two
  separate `NumberType` sub-fields (a compound type on `FormType`) and transform the
  `array` norm data to a `GeoPoint` model. Use this when the widget itself is
  compound rather than a single text input.
- **Option C (exam-style)** — a `PRE_SUBMIT` [form event](../forms/events.md) that
  massages the raw input before binding. Correct for light request-shape fixes, but
  *wrong* for type conversion: a transformer is the canonical model↔view bridge and
  the one the certification expects here.

!!! danger "Level up"
    Add a **second** view transformer that rounds coordinates to 4 decimals, then
    predict the submit order: view transformers run in **reverse registration
    order** on `reverseTransform` (view→norm→model). If the first-run transformer
    throws `TransformationFailedException`, the chain stops, later transformers
    never run, and the field shows `invalid_message`.

---

<small>Theory: [Data transformers](../forms/data-transformers.md) ·
[Form types](../forms/types.md) · Labs: [all labs](index.md)</small>
