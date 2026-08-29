---
tags:
  - Labs
  - Twig
---

# Lab : Extension Twig personnalisée — un filtre `excerpt`

!!! abstract "Practical Lab"
    **Objective:** construire et enregistrer un **filtre** Twig personnalisé dont la logique peut
    être testée unitairement en isolation, et comprendre quand sa sortie doit être échappée ·
    **Difficulty:** Facile ·
    **Theory:** [Filters & Functions](../twig/filters-functions.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Créer ton propre filtre Twig (comme `|lower` ou `|date`, mais inventé par toi) et le tester unitairement avant même de l'utiliser dans un vrai template.

**Pourquoi ça existe ?** Twig fournit beaucoup de filtres intégrés, mais un vrai projet a toujours un besoin d'affichage précis non couvert — savoir en créer un proprement est une compétence Symfony de base.

**🏠 Analogie de la vraie vie :** Ajouter ton propre outil personnalisé à une boîte à outils standard — une fois ajouté, il se comporte exactement comme les outils déjà présents, sans que personne ne remarque la différence.

**Symfony dans la vraie vie :** `{{ article.contenu|excerpt(100) }}` appelle ton filtre personnalisé exactement comme `{{ prix|round(2) }}` appelle un filtre intégré — même syntaxe, même comportement.

**⚠️ Erreur fréquente :** oublier de réfléchir à l'échappement automatique — un filtre qui produit du HTML doit explicitement le déclarer (`is_safe: ['html']`), sinon Twig l'échappe et casse l'affichage.

**🧠 Comment le mémoriser :** "Un filtre personnalisé, c'est un outil de plus dans la boîte — indiscernable des outils déjà fournis par Twig."


## Objective

À l'issue de ce lab, vous saurez **écrire un filtre Twig personnalisé**, l'exposer via une
`Twig\Extension\AbstractExtension` (et la variante avec l'attribut `#[AsTwigFilter]`),
**tester directement le callable sous-jacent** avec des cas limites, le rendre dans un vrai
`Twig\Environment`, et décider correctement s'il a besoin de `is_safe: ['html']`.

L'exemple fil rouge est un filtre `excerpt` : `{{ post.body|excerpt(20) }}` tronque
le texte à *N* caractères sur une frontière de mot et ajoute des points de suspension.

## Prerequisites

- Chapitres : [Filters & Functions](../twig/filters-functions.md),
  [Twig Syntax](../twig/syntax.md), [Auto-Escaping](../twig/auto-escaping.md)
- Compétences supposées acquises : écrire un `TestCase` PHPUnit, la syntaxe PHP 8.4 (first-class
  callable `$this->method(...)`, arguments nommés), les fonctions de chaînes `mb_*` de base.

## TD Instructions

Étapes numérotées, à faire dans l'ordre — ne sautez **pas** directement à la solution de référence.

1. Créez `App\Twig\ContentExtension` étendant `Twig\Extension\AbstractExtension`.
2. Ajoutez une méthode publique `excerpt(string $text, int $limit = 100, string $ellipsis = '…'): string`
   qui retourne `$text` inchangé quand il fait au plus `$limit` caractères, et
   sinon tronque à au plus `$limit` caractères **sans couper un mot en
   deux**, puis ajoute `$ellipsis`.
3. Implémentez `getFilters(): array` retournant un seul `Twig\TwigFilter` nommé `excerpt`
   câblé à la méthode via la syntaxe first-class callable `$this->excerpt(...)`.
4. Décidez délibérément de l'option `is_safe` : le filtre retourne du **texte brut**, il
   doit donc rester auto-échappé. Ne le marquez **pas** comme sûr.
5. **Écrivez d'abord le test qui échoue** (voir le bloc TDD) couvrant les cas limites :
   chaîne courte, frontière exacte, chaîne longue, entrée multi-octets, points de suspension personnalisés.
6. Ajoutez un test qui enregistre l'extension sur un `Twig\Environment` (avec un
   `ArrayLoader`) et vérifie la chaîne rendue de `{{ text|excerpt(10) }}`.
7. Lancez les tests au rouge → passez au vert → refactorisez.
8. **Level up :** ré-exposez la même logique avec `#[AsTwigFilter('excerpt')]` sur une classe
   simple et confirmez que le comportement est identique.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · Twig 3.x · aucune bibliothèque hors du périmètre de la certification ·
    respectez les bonnes pratiques (attributs, strict types, `final`, first-class callables).

## Implementation Guide (partial)

Uniquement des repères de haut niveau — pas le code complet.

- Utilisez `Twig\Extension\AbstractExtension` et `Twig\TwigFilter`.
- Enregistrez avec `new TwigFilter('excerpt', $this->excerpt(...))` — le second argument est
  n'importe quel callable ; la syntaxe first-class callable conserve la sécurité des types.
- Pour « ne pas couper un mot », trouvez le dernier espace à la limite ou avant avec
  `mb_strrpos(mb_substr($text, 0, $limit), ' ')` ; retombez sur une coupe brute quand il n'y
  a pas d'espace. Utilisez la famille `mb_*` pour qu'une entrée multi-octets soit comptée en caractères, pas en octets.
- **Échappement :** le callable retourne du texte brut ; laissez `is_safe` non défini pour que Twig
  l'échappe. Vous n'ajouteriez `is_safe: ['html']` que si le filtre produisait lui-même du
  balisage de confiance (ce n'est pas le cas ici).
- Avec l'autoconfiguration de Symfony, une `AbstractExtension` est auto-taguée
  `twig.extension` ; une classe utilisant `#[AsTwigFilter]` est enregistrée automatiquement. Aucun
  câblage manuel de service n'est nécessaire.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez le test ci-dessous qui échoue ; lancez-le, observez-le échouer (classe manquante).
    2. **Green :** écrivez le minimum de `ContentExtension` pour passer.
    3. **Refactor :** nettoyez la logique de troncature avec le test comme filet de sécurité.

**Comportement (Given/When/Then) :**

- **Given** une chaîne à la limite ou en dessous, **When** `excerpt` s'exécute, **Then** il
  retourne la chaîne inchangée (pas de points de suspension).
- **Given** une chaîne plus longue, **When** `excerpt(limit)` s'exécute, **Then** le résultat est au
  plus `limit` caractères de texte, coupé sur une frontière de mot, plus les points de suspension.
- **Given** l'extension enregistrée sur un `Twig\Environment`, **When** un template utilise
  `{{ text|excerpt(10) }}`, **Then** la sortie rendue correspond au callable.

```php
<?php
declare(strict_types=1);

namespace App\Tests\Twig;

use App\Twig\ContentExtension;
use PHPUnit\Framework\TestCase;
use Twig\Environment;
use Twig\Loader\ArrayLoader;

final class ContentExtensionTest extends TestCase
{
    private ContentExtension $extension;

    protected function setUp(): void
    {
        $this->extension = new ContentExtension();
    }

    // --- unit-test the callable directly (fast, no Twig needed) ---

    public function testShortStringIsReturnedUnchanged(): void
    {
        self::assertSame('Hello', $this->extension->excerpt('Hello', 100));
    }

    public function testExactBoundaryIsNotTruncated(): void
    {
        // 5 chars, limit 5 -> unchanged, no ellipsis
        self::assertSame('Hello', $this->extension->excerpt('Hello', 5));
    }

    public function testLongStringIsTruncatedOnWordBoundary(): void
    {
        $result = $this->extension->excerpt('The quick brown fox jumps', 12);

        // cut at the last space at/under 12, no half words
        self::assertSame('The quick…', $result);
    }

    public function testHardCutWhenNoSpaceBeforeLimit(): void
    {
        self::assertSame('abcde…', $this->extension->excerpt('abcdefghij', 5));
    }

    public function testMultibyteCountsCharactersNotBytes(): void
    {
        // 5 accented chars = 10 bytes; limit 5 counts CHARACTERS -> unchanged
        self::assertSame('ééééé', $this->extension->excerpt('ééééé', 5));
    }

    public function testCustomEllipsis(): void
    {
        self::assertSame(
            'The quick...',
            $this->extension->excerpt('The quick brown fox', 12, '...'),
        );
    }

    // --- render through a real Twig\Environment with the extension registered ---

    public function testFilterRendersInTemplate(): void
    {
        $twig = new Environment(new ArrayLoader([
            'p' => '{{ text|excerpt(10) }}',
        ]));
        $twig->addExtension($this->extension);

        self::assertSame(
            'Lorem…',
            $twig->render('p', ['text' => 'Lorem ipsum dolor']),
        );
    }

    public function testFilterOutputIsAutoEscaped(): void
    {
        // Not is_safe -> HTML in the (short) value must come out escaped.
        $twig = new Environment(new ArrayLoader([
            'p' => '{{ text|excerpt(100) }}',
        ]));
        $twig->addExtension($this->extension);

        self::assertSame(
            '&lt;b&gt;hi&lt;/b&gt;',
            $twig->render('p', ['text' => '<b>hi</b>']),
        );
    }
}
```

!!! tip "Setup hints"
    Lancez-le avec `vendor/bin/phpunit tests/Twig/ContentExtensionTest.php`. Aucun
    container ni kernel n'est nécessaire — `new Environment(new ArrayLoader([...]))` plus
    `addExtension()` suffit pour exercer le filtre de bout en bout. Le test d'auto-échappement
    s'appuie sur la stratégie d'autoescape `html` par défaut de `Environment`.

## Validation Steps

En plus de la suite de tests au vert, vérifiez le câblage dans une vraie application :

- [ ] `php bin/console debug:twig --filter=excerpt` liste votre filtre et sa classe.
- [ ] `php bin/console debug:twig` montre `ContentExtension` sous *Extensions*.
- [ ] Une page utilisant `{{ post.body|excerpt(20) }}` affiche du texte tronqué et échappé.

## Review — Common Mistakes

- **Marquer le filtre `is_safe: ['html']` « par sécurité ».** → Cela désactive l'échappement, donc
  une valeur `<b>hi</b>` serait rendue comme du balisage actif (risque XSS). → Laissez `is_safe` non défini
  pour un filtre en texte brut ; seuls les filtres produisant du balisage de confiance le reçoivent.
- **Utiliser `substr`/`strlen` au lieu de `mb_*`.** → Une entrée multi-octets est mal comptée et
  peut être coupée au milieu d'un caractère, produisant du mojibake. → Utilisez `mb_substr`/`mb_strlen`.
- **Ajouter les points de suspension même quand rien n'a été tronqué.** → Le `assertSame` du
  cas limite échoue. → Retournez tôt quand `mb_strlen($text) <= $limit`.
- **Passer un callable sous forme de chaîne comme `'excerpt'` à `TwigFilter`.** → Twig ne peut pas résoudre
  la méthode. → Utilisez `$this->excerpt(...)` (first-class callable) ou `[$this, 'excerpt']`.
- **Oublier que l'extension est auto-taguée.** → Déclarer manuellement un
  service `twig.extension` crée un doublon. → Avec l'autoconfigure activé, ne faites rien.

## Exam Connection

La certification teste la distinction **filtre vs fonction**, l'**API
d'enregistrement** (`AbstractExtension::getFilters()` retournant `TwigFilter`, ou
l'attribut `#[AsTwigFilter]`), et le **piège de l'échappement** : la sortie d'un filtre est
auto-échappée sauf déclaration `is_safe: ['html']`. Ce lab fait travailler les trois, et la
décision sur `is_safe` (texte brut ⇒ rester échappé) est exactement le piège que tend l'examen.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    === "AbstractExtension (classic)"

        ```php
        <?php
        declare(strict_types=1);

        namespace App\Twig;

        use Twig\Extension\AbstractExtension;
        use Twig\TwigFilter;

        final class ContentExtension extends AbstractExtension
        {
            /**
             * @return list<TwigFilter>
             */
            public function getFilters(): array
            {
                return [
                    // No is_safe: output is plain text and must stay auto-escaped.
                    new TwigFilter('excerpt', $this->excerpt(...)),
                ];
            }

            public function excerpt(string $text, int $limit = 100, string $ellipsis = '…'): string
            {
                if ($limit <= 0 || mb_strlen($text) <= $limit) {
                    return $text;
                }

                $slice = mb_substr($text, 0, $limit);
                $lastSpace = mb_strrpos($slice, ' ');

                // Cut on the last word boundary; hard-cut when there is no space.
                $cut = false !== $lastSpace ? mb_substr($slice, 0, $lastSpace) : $slice;

                return $cut.$ellipsis;
            }
        }
        ```

    === "Attribute (Twig 3.x)"

        ```php
        <?php
        declare(strict_types=1);

        namespace App\Twig;

        use Twig\Attribute\AsTwigFilter;

        final class ContentExtension
        {
            #[AsTwigFilter('excerpt')]
            public function excerpt(string $text, int $limit = 100, string $ellipsis = '…'): string
            {
                if ($limit <= 0 || mb_strlen($text) <= $limit) {
                    return $text;
                }

                $slice = mb_substr($text, 0, $limit);
                $lastSpace = mb_strrpos($slice, ' ');
                $cut = false !== $lastSpace ? mb_substr($slice, 0, $lastSpace) : $slice;

                return $cut.$ellipsis;
            }
        }
        ```

    Les deux enregistrent `excerpt` automatiquement grâce à l'autoconfiguration de Symfony et partagent
    le même corps de méthode, testé unitairement — la suite de tests ci-dessus passe donc avec l'un comme l'autre.

## Alternative Approaches (optional)

- **Option A (simple) :** une closure directement dans `getFilters()` —
  `new TwigFilter('excerpt', fn (string $s, int $n = 100) => ...)`. Convient pour une logique
  triviale, mais plus difficile à tester unitairement en isolation qu'une méthode nommée.
- **Option B (avancée) :** déplacez la logique dans une classe runtime
  `RuntimeExtensionInterface` (ou un `#[AsTwigFilter]` sur un runtime) pour qu'elle
  soit instanciée en lazy seulement quand le filtre est utilisé — le bon choix quand le
  filtre a besoin de services injectés.
- **Option C (exam-style) :** exposez-le plutôt comme une **fonction** —
  `new TwigFunction('excerpt', ...)` utilisée comme `{{ excerpt(text, 20) }}`. Même callable,
  site d'appel différent ; sachez lequel se lit le plus naturellement (une transformation de valeur ⇒ filtre).

---

<small>Theory: [Filters & Functions](../twig/filters-functions.md) · Labs: [all labs](index.md)</small>
