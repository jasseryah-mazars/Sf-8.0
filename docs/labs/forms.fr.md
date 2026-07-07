---
tags:
  - Labs
  - Forms
---

# Lab: Data Transformer — A `GeoPointType` field backed by a value object

!!! abstract "Practical Lab"
    **Objective :** construire un champ de form réutilisable dont la *vue* est une
    chaîne `"lat,lng"` mais dont le *modèle* est un value object immuable `GeoPoint`,
    via une `DataTransformerInterface` ·
    **Difficulty:** Advanced ·
    **Theory:** [Data transformers](../forms/data-transformers.md) ·
    [Form types](../forms/types.md) ·
    **Mode:** TDD

## Objective

À l'issue de ce lab, vous saurez transformer un simple champ texte en champ *typé* : le
navigateur envoie une chaîne, votre controller reçoit un objet `GeoPoint` (ou un form
proprement invalidé). Vous serez capable de :

- implémenter `transform()`/`reverseTransform()` dans les **bonnes directions** ;
- faire échouer une mauvaise conversion avec `TransformationFailedException` plutôt qu'une 500 ;
- brancher le transformer dans un type personnalisé bâti sur `TextType` avec `getParent()` ;
- prouver que le champ fonctionne de bout en bout avec `TypeTestCase` — sans navigateur,
  sans kernel, sans base de données.

## Prerequisites

- Chapitres : [Data transformers](../forms/data-transformers.md) ·
  [Form types](../forms/types.md) · [Handling submissions](../forms/handling.md)
- Compétences supposées acquises : bases de PHPUnit, classes readonly de PHP 8.4, le
  modèle model/norm/view d'un form Symfony.

## TD Instructions

Vous allez modéliser un champ de coordonnées. La valeur **model** est un value object
`GeoPoint` `(latitude, longitude)` ; la valeur **view** est la chaîne `"48.8566,2.3522"`.

1. Créez un value object immuable `App\Form\Model\GeoPoint` avec deux propriétés
   `float`, en contraignant la latitude à `-90..90` et la longitude à `-180..180` dans
   son constructeur.
2. **Écrivez d'abord le test du transformer** (`tests/Form/Transformer/…`). Couvrez les
   deux directions : `transform(null) === ''`, `transform(GeoPoint) === '48.8566,2.3522'`,
   `transform('a string')` lève une exception, `reverseTransform('48.8566,2.3522')` est
   égal à l'objet, vide/espaces/`null` donnent `null`, et un data provider d'entrées
   malformées lève à chaque fois `TransformationFailedException`. Lancez-le — regardez-le
   échouer (Red).
3. Implémentez `App\Form\Transformer\GeoPointToStringTransformer` implémentant
   `DataTransformerInterface` pour faire passer le test au vert. Gérez vide/`null` **en premier**.
4. **Écrivez le test du type** avec `TypeTestCase` : créez le form via la `factory` du
   test, `submit('48.8566,2.3522')`, vérifiez `isSynchronized()` et que
   `getData()` est bien le `GeoPoint` attendu ; puis soumettez n'importe quoi et vérifiez
   que le form n'est **pas** synchronisé et que `getData()` vaut `null`.
5. Implémentez `App\Form\Type\GeoPointType` étendant `AbstractType` : enregistrez le
   transformer avec `addViewTransformer()`, définissez un `invalid_message` parlant, et
   retournez `TextType::class` depuis `getParent()`. Faites passer l'étape 4.
6. Refactorez avec les deux tests au vert.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification ·
    respectez les bonnes pratiques (attributs, strict types, `readonly` quand c'est pertinent).

## Implementation Guide (partial)

Uniquement des repères de haut niveau — appuyez-vous dessus, ne copiez pas encore la référence.

- **Value object :** `final readonly class GeoPoint` avec des propriétés `public float`
  promues ; levez `\InvalidArgumentException` depuis le constructeur en cas de coordonnée
  hors plage. C'est le *seul* endroit où vivent les règles de plage.
- **Transformer :** `implements DataTransformerInterface`. La direction est tout l'enjeu :
  `transform()` est **model → view** (retourne une chaîne), `reverseTransform()` est
  **view → model** (retourne un `GeoPoint|null`). Ajoutez le docblock
  `@implements DataTransformerInterface<GeoPoint|null, string>`.
- **Gérez le vide en premier :** `transform(null)` retourne `''` ; `reverseTransform('')`
  ainsi que les chaînes d'espaces / `null` retournent `null`. Un champ optionnel ne doit pas planter.
- **Chemin d'échec :** sur une chaîne de vue non analysable, levez
  `Symfony\Component\Form\Exception\TransformationFailedException`. Quand le constructeur
  de `GeoPoint` rejette une coordonnée, **attrapez** la
  `\InvalidArgumentException` et relancez-la en `TransformationFailedException`
  (passez `previous:`), afin qu'une garde métier devienne un *champ* invalide, pas une 500.
- **Type :** puisque seule la représentation en chaîne change, utilisez
  `addViewTransformer()` (pas model), parent = `TextType::class`, et définissez
  `invalid_message` dans `configureOptions()`.
- **Test du type :** un type mono-champ bâti sur `TextType` *est* le champ — appelez
  `->submit('…')` avec un scalaire (pas un tableau). Enregistrez le type dans la factory
  du test avec une `PreloadedExtension` pour qu'il se résolve par FQCN.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez le test du transformer, lancez-le, regardez-le échouer (classe manquante).
    2. **Green :** écrivez le minimum de transformer + type pour le faire passer.
    3. **Refactor :** faites le ménage avec les tests comme filet de sécurité.

**Comportement (Given/When/Then) :**

- **Given** la chaîne `"48.8566,2.3522"` **When** le form est soumis **Then**
  `getData()` vaut `new GeoPoint(48.8566, 2.3522)` et le form est *synchronisé*.
- **Given** un `GeoPoint` comme données model préchargées **When** la vue est construite
  **Then** la donnée de vue est la chaîne `"48.8566,2.3522"`.
- **Given** la chaîne `"not-a-coordinate"` (ou une valeur hors plage) **When** elle est
  soumise **Then** le transformer lève `TransformationFailedException`, le form n'est
  **pas** synchronisé et `getData()` vaut `null` — aucune exception ne s'échappe.

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
    Lancez : `vendor/bin/phpunit tests/Form`. `TypeTestCase` vous fournit une
    `$this->factory` prête à l'emploi avec la core extension déjà chargée, si bien que
    `TextType` (le parent) se résout gratuitement — mais **votre** type non, d'où la
    `PreloadedExtension` dans `getExtensions()`. Un type mono-champ bâti sur
    `TextType` est le champ lui-même, donc `submit()` prend une chaîne **scalaire**, pas
    un tableau. Un transformer qui lève une exception à la soumission fait basculer
    `isSynchronized()` à `false` et laisse `getData()` à sa valeur par défaut (`null`) —
    c'est exactement ainsi qu'un form « affiche une erreur » au lieu d'exploser.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Form/Transformer/GeoPointToStringTransformerTest.php`
  est au vert (les deux directions + chaque entrée invalide).
- [ ] `vendor/bin/phpunit tests/Form/Type/GeoPointTypeTest.php` est au vert.
- [ ] `php bin/console debug:form GeoPointType` liste le champ et la valeur par défaut de
  son `invalid_message`.
- [ ] Dans un controller, `$form->getData()` retourne un `GeoPoint` en cas de succès ; une
  soumission invalide affiche `invalid_message` sans aucune 500 dans le profiler.

## Review — Common Mistakes

- **Directions inversées** → `transform()` retourne l'objet et
  `reverseTransform()` retourne la chaîne → le champ affiche n'importe quoi et soumet
  de travers. Correction : `transform` = **model → view** (chaîne en sortie),
  `reverseTransform` = **view → model** (objet en sortie).
- **Retourner `null` / lever `\InvalidArgumentException` sur une mauvaise entrée** → le
  form croit la valeur valide, ou une 500 s'échappe. Correction : levez
  `TransformationFailedException` ; attrapez la
  `\InvalidArgumentException` du value object et relancez-la sous cette forme.
- **Pas de gestion du vide** → un champ optionnel plante sur `''`/`null`. Correction :
  gérez le vide **en premier** dans les deux méthodes.
- **`addModelTransformer()` pour du pur formatage** → mauvais emplacement ; ici seule la
  représentation en chaîne change, c'est donc un transformer de **view**.
- **`submit(['value' => …])` dans le test du type** → ce type est un champ unique, pas un
  form composé ; soumettez directement la chaîne scalaire.
- **Oublier `getExtensions()`** → `Could not load type "App\Form\Type\GeoPointType"`.
  Enregistrez-le avec une `PreloadedExtension`.

## Exam Connection

La certification adore le **piège des directions** : `transform()` c'est l'affichage
(model→view), `reverseTransform()` c'est la soumission (view→model). Elle vérifie aussi
qu'une conversion échouée produit un **form invalide affiché via `invalid_message`**, et
non une exception — piloté par `TransformationFailedException`, qui fait basculer
`isSynchronized()` à `false`. Savoir qu'un transformer de *view* fait le pont norm↔view
(formatage) tandis qu'un transformer de *model* fait le pont model↔norm (identité de
l'objet), et que `getParent()` retourne une **chaîne de classe**, couvre le reste des
questions sur ce sujet.

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

- **Option A (simple)** — faites l'économie du value object : transformez une chaîne
  `"lat,lng"` en simple tableau `['lat' => float, 'lng' => float]`. Moins de pièces
  mobiles, mais vous perdez la garde du constructeur et la sûreté de typage.
- **Option B (avancée)** — un transformer de **model** à la place : gardez la vue sous
  forme de deux sous-champs `NumberType` séparés (un type composé sur `FormType`) et
  transformez la donnée norm `array` en model `GeoPoint`. À utiliser quand le widget
  lui-même est composé plutôt qu'un simple champ texte.
- **Option C (style examen)** — un [form event](../forms/events.md) `PRE_SUBMIT` qui
  retouche l'entrée brute avant la liaison. Correct pour de légers ajustements de forme de
  la request, mais *incorrect* pour de la conversion de type : un transformer est le pont
  model↔view canonique et celui que la certification attend ici.

!!! danger "Level up"
    Ajoutez un **second** view transformer qui arrondit les coordonnées à 4 décimales,
    puis prédisez l'ordre à la soumission : les view transformers s'exécutent en **ordre
    inverse d'enregistrement** sur `reverseTransform` (view→norm→model). Si le premier
    transformer exécuté lève `TransformationFailedException`, la chaîne s'arrête, les
    transformers suivants ne s'exécutent jamais, et le champ affiche `invalid_message`.

---

<small>Theory: [Data transformers](../forms/data-transformers.md) ·
[Form types](../forms/types.md) · Labs: [all labs](index.md)</small>
