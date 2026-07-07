# Namespaces & Autoloading

!!! tip "In a nutshell"
    Les namespaces évitent les collisions de noms ; PSR-4 fait correspondre un
    préfixe à un répertoire pour que Composer charge automatiquement les classes.
    Le piège : les appels de **fonctions/constantes** non qualifiés retombent sur
    le namespace global, mais **pas les noms de classes**.

!!! example "Real-world analogy"
    Un namespace est comme une adresse postale complète : deux personnes nommées
    « John Smith » se distinguent par leur rue et leur ville, tout comme
    `App\Service\Mailer` n'entre jamais en collision avec un autre `Mailer`
    ailleurs. PSR-4 est la règle de classement qui associe un nom de département à
    un tiroir physique, si bien que le commis (l'autoloader) trouve le bon dossier
    sans que vous ne citiez jamais le chemin exact. La bizarrerie du repli : les
    mots du quotidien — comme appeler une ligne d'assistance partagée (`strlen`) —
    se rabattent sur l'annuaire central de la ville s'il n'y a pas d'entrée locale,
    mais un *nom propre* comme `DateTime` ne le fait jamais ; vous devez donner son
    adresse complète.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Expliquer les règles de résolution des noms de PHP (qualifié, non qualifié, pleinement qualifié).
    - [ ] Configurer et raisonner sur l'autoloading **PSR-4** via Composer.
    - [ ] Utiliser correctement `use`, les alias et les imports groupés.

    **Syllabus:** `PHP → Namespaces` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [OOP](oop.md)

---

## Theory

Un **namespace** est une étiquette hiérarchique (`App\Service\Mailer`) qui évite
les collisions de noms. PHP résout les noms selon des règles qui dépendent de la
forme du nom : **non qualifié** (`Mailer`), **qualifié** (`Service\Mailer`) ou
**pleinement qualifié** (`\App\Service\Mailer`). L'**autoloading** transforme un
nom de classe en chemin de fichier, si bien que vous n'écrivez jamais `require`.

| Forme | Exemple | Résolution |
|---|---|---|
| Pleinement qualifié | `\App\Foo` | Absolue, depuis la racine globale |
| Qualifié | `Service\Foo` | Relative au namespace courant (ou à un `use`) |
| Non qualifié | `Foo` | Namespace courant, puis un `use` correspondant |

!!! question "Predict first"
    Dans `namespace App;`, `strlen($s)` fonctionne sans `use`, mais
    `new DateTime()` échoue. Pourquoi cette différence ?

??? note "Reveal"
    Les appels de **fonctions/constantes** non qualifiés retombent sur le
    namespace global ; **pas les noms de classes**. Ainsi `strlen` se résout en
    `\strlen`, mais `DateTime` signifie `App\DateTime`, sauf si vous écrivez
    `\DateTime` ou l'importez.

## Deep Dive — how it works internally

### Name resolution rules

1. `declare(strict_types=1)` et `namespace` doivent être les **premières** instructions.
2. Les noms **pleinement qualifiés** (avec `\` initial) sont utilisés tels quels.
3. Pour les **classes/interfaces/traits**, les noms non qualifiés et qualifiés se
   résolvent d'abord contre les imports `use`, puis contre le namespace courant.
4. Pour les **fonctions et constantes**, un appel non qualifié essaie d'abord le
   namespace courant, puis **retombe sur le namespace global** — ce repli
   n'existe que pour les fonctions/constantes, pas pour les classes. C'est
   pourquoi `\strlen()` dans un namespace fonctionne toujours, et pourquoi un
   `\` initial micro-optimise la recherche.

```php
<?php
declare(strict_types=1);

namespace App\Service;

use App\Contract\MailerInterface;
use App\Contract\Transport as Tx;   // alias
use function App\Support\slugify;   // function import
use const App\Support\VERSION;      // const import

final class Mailer implements MailerInterface
{
    public function send(Tx $t): void
    {
        $count = \count($t->messages);  // leading \ = global function
        echo slugify(VERSION);
    }
}
```

### PSR-4 autoloading

PSR-4 fait correspondre un **préfixe de namespace** à un **répertoire de base**.
L'autoloader retire le préfixe, remplace `\` par `/` et ajoute `.php`.

```json
{
    "autoload": {
        "psr-4": { "App\\": "src/" }
    }
}
```

`App\Service\Mailer` → `src/Service/Mailer.php`. Composer génère
`vendor/autoload.php`, qui enregistre le loader via `spl_autoload_register()`.

```mermaid
flowchart LR
    A["new App\\Service\\Mailer()"] --> B[Class not loaded]
    B --> C[spl_autoload_register callback]
    C --> D[PSR-4 prefix map: App\\ → src/]
    D --> E[require src/Service/Mailer.php]
```

En production, `composer dump-autoload --optimize` (ou `--classmap-authoritative`)
construit une classmap statique, ce qui évite tout stat du système de fichiers
par classe.

!!! note "Source reference"
    Le loader de Composer implémente PSR-4 ; le `MicroKernelTrait` de Symfony et
    l'autoconfiguration s'appuient dessus —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Kernel/MicroKernelTrait.php).

## Configuration & code

=== "Grouped use"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Service\{Mailer, Reporter, Clock};   // grouped import
    use function array_map;
    ```

=== "Console"

    ```console
    $ composer dump-autoload --optimize
    Generating optimized autoload files
    ```

## Best practices & anti-patterns

| ✅ À faire | ❌ À éviter |
|---|---|
| Une classe par fichier, chemin = namespace | Plusieurs classes par fichier |
| `use` en tête, alias en cas de collision | De longs FQCN en ligne partout |
| Préfixe `\` sur les fonctions globales critiques | Redéfinir des noms SPL/globaux |
| Autoload `--optimize` en prod | Livrer l'autoloader de dev |

## When (not) to use it / alternatives

- Placez toujours le code applicatif dans un namespace ; seul un petit script ou
  un polyfill global a sa place dans le namespace global.
- Utilisez un alias quand deux imports partagent un nom court ; n'aliasez pas
  par simple style.

!!! danger "Certification traps"
    - Les appels de fonctions/constantes **retombent sur le global** ; les noms
      de classes, **non**. `new DateTime()` dans un namespace échoue sauf import
      ou préfixe `\`.
    - Les imports `use` **ne chargent pas** de fichier — ce sont seulement des
      alias résolus à la compilation.
    - `namespace` et `declare` doivent précéder toute autre instruction (aucune
      sortie avant).
    - PSR-4 est **sensible à la casse** dans la correspondance classe → chemin
      sous Linux.

!!! warning "Common mistakes"
    - Écrire `\App\...` avec un slash initial dans un `use` (invalide — `use`
      est déjà toujours absolu).
    - Supposer que `use App\Foo;` importe aussi `App\Foo\Bar` (il n'importe que `Foo`).

## Exercises

1. **(Advanced)** Étant donné `namespace App;` et un appel à `strlen()`,
   expliquez pourquoi cela fonctionne sans `use`.
2. **(Advanced)** Faites correspondre `App\Repository\UserRepository` à un chemin
   de fichier selon une règle PSR-4 `"App\\": "src/"`.

??? success "Solutions"

    **1.** `strlen` est une fonction ; les appels de fonctions non qualifiés
    retombent sur le namespace global quand aucun `App\strlen` n'existe. Ajouter
    `\strlen()` évite cette recherche et est légèrement plus rapide.

    **2.** `src/Repository/UserRepository.php` — retirez le préfixe `App\`,
    remplacez `\` par `/`, ajoutez `.php`.

## Certification questions

??? question "Q1. Inside `namespace App;`, an unqualified call `count($x)` resolves to…"
    - [x] A. `App\count` if defined, else global `\count` ✅
    - [ ] B. Always `App\count`
    - [ ] C. A fatal error
    - [ ] D. `\count` only

    **Why:** Les fonctions retombent sur le namespace global. **Ref:** [Namespace resolution](https://www.php.net/manual/en/language.namespaces.rules.php).

??? question "Q2. What does `use App\Service\Mailer;` do?"
    - [ ] A. Loads the file immediately
    - [x] B. Creates a compile-time alias so `Mailer` means the FQCN ✅
    - [ ] C. Instantiates the class
    - [ ] D. Registers an autoloader

    **Why:** `use` est un pur alias ; le chargement intervient plus tard via
    l'autoloader.
    **Ref:** [Using namespaces](https://www.php.net/manual/en/language.namespaces.importing.php).

??? question "Q3. Under PSR-4 `\"App\\\\\": \"src/\"`, where does `App\\Foo\\Bar` live?"
    - [ ] A. `src/App/Foo/Bar.php`
    - [x] B. `src/Foo/Bar.php` ✅
    - [ ] C. `src/foo/bar.php`
    - [ ] D. `App/Foo/Bar.php`

    **Why:** Le préfixe `App\` correspond à `src/`, donc seul le reste devient le chemin.
    **Ref:** [PSR-4](https://www.php-fig.org/psr/psr-4/).

??? question "Q4. Inside `namespace App;`, which correctly references the global `DateTime`?"
    - [ ] A. `new DateTime()`
    - [x] B. `new \DateTime()` ✅
    - [ ] C. `new App\DateTime()`
    - [ ] D. `new DateTime\Global()`

    **Why:** Les noms de classes ne retombent pas sur le global ; un `\` initial
    (ou un `use`) est donc requis. **Ref:** [Namespace resolution](https://www.php.net/manual/en/language.namespaces.rules.php).

## Key takeaways

- Les fonctions/constantes retombent sur le global ; **pas les classes**.
- `use` est un alias résolu à la compilation, pas un chargement de fichier.
- PSR-4 associe préfixe → répertoire de base ; retirer le préfixe, `\`→`/`, ajouter `.php`.
- `composer dump-autoload --optimize` en production.

## Last-minute revision

!!! tip "Cheat sheet"
    - `namespace` + `declare` en premier ; rien avant eux.
    - `\Foo` = pleinement qualifié ; `Foo` = namespace courant (classe) ou global (fonction).
    - Groupé : `use App\{A, B, C};` · fonction : `use function` ; constante : `use const`.
    - PSR-4 : `App\ → src/`, sensible à la casse sous Linux.

## Connections

- **Dépend de :** [OOP](oop.md) — les namespaces organisent les classes/interfaces que vous définissez.
- **Réutilisé dans :** [Extensions](extensions.md) — le même `composer.json` déclare les `ext-*` à côté de PSR-4 ; [Interfaces](interfaces.md) type-hinte les FQCN importés.
- **À ne pas confondre avec :** [Traits](traits.md) — le `use Some\Class;` au niveau du fichier (import) vs le `use TraitName;` dans le corps de la classe (inclusion de trait).

## Official References
- [PHP: Namespaces](https://www.php.net/manual/en/language.namespaces.php)
- [PHP: Name resolution rules](https://www.php.net/manual/en/language.namespaces.rules.php)
- [PSR-4 Autoloader](https://www.php-fig.org/psr/psr-4/)
- [Symfony source — MicroKernelTrait](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Kernel/MicroKernelTrait.php)

## Video references

!!! tip "Watch & learn"
    Voici des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « PHP & web security » pour consolider ce chapitre. Nous référençons des
    chaînes stables plutôt que des vidéos individuelles pour que les liens ne
    périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences et keynotes de SymfonyCon.
    - [Official docs for this topic](https://symfony.com/doc/current/index.html) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** les fonctions retombent sur le global mais pas les classes
- [ ] configurer PSR-4 et `dump-autoload --optimize` pour une application Symfony 8
- [ ] déboguer un « class not found » dû à un `\` ou un `use` manquant dans un namespace
- [ ] repérer le piège : un `use` censé charger un fichier (il ne fait qu'aliaser) ou un `\` initial dans un `use`
- [ ] expliquer comment PSR-4 associe un préfixe à un chemin (retirer le préfixe, `\`→`/`, ajouter `.php`)

---

<small>Related: [OOP](oop.md) · [Interfaces](interfaces.md) · [PHP API](php-api.md)</small>
