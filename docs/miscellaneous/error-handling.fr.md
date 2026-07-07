# Error Handling

!!! tip "In a nutshell"
    Le composant ErrorHandler transforme les erreurs PHP en exceptions
    interceptables et rend les throwables non attrapés (via une
    `FlattenException` sérialisable), tandis que le flux `kernel.exception` de
    HttpKernel transforme une exception en `Response`. À retenir pour l'examen :
    seule `HttpExceptionInterface` porte un status personnalisé ; tout le reste
    devient une 500.

!!! example "Real-world analogy"
    Imaginez les urgences d'un hôpital. Les incidents bruts qui arrivent sous toutes
    les formes — warnings, notices, fatals PHP — sont d'abord consignés sur un dossier
    patient standard unique (transformés en exceptions interceptables) afin de pouvoir
    tous être traités de la même manière, et une photocopie aplatie de ce dossier
    (`FlattenException`) peut être classée ou transmise sans risque. La plupart des
    arrivées sont enregistrées sous un code d'urgence générique (une 500), sauf si
    elles arrivent déjà avec une étiquette de diagnostic précise (quelque chose qui
    implémente `HttpExceptionInterface`), comme l'étiquette 404 que porte une
    `NotFoundHttpException`.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Expliquer comment le composant ErrorHandler transforme les erreurs PHP en exceptions.
    - [ ] Retracer comment une exception devient une `Response` HTTP via l'error controller.
    - [ ] Distinguer la sortie d'erreur en prod et en dev, et personnaliser les pages d'erreur.

    **Syllabus:** `Miscellaneous → Error Handling` ·
    **Level:** Advanced ·
    **Est. time:** 30 min ·
    **Prerequisites:** [Request Handling](../architecture/request-handling.md)

---

## Theory

Deux couches coopèrent. Le composant bas niveau **ErrorHandler** convertit les
**erreurs** PHP (warnings, notices, fatals) en exceptions interceptables et
formate les throwables non attrapés. La couche haut niveau **HttpKernel**
attrape les exceptions qui s'échappent d'une request et dispatche
`kernel.exception` pour qu'un listener puisse construire une `Response`. Ce
chapitre se concentre sur le composant ; le flux d'events du kernel est couvert
dans [Exception Handling](../architecture/exception-handling.md).

```php
// Low-level component: PHP errors become catchable exceptions
try {
    file_get_contents('/missing-file'); // PHP warning -> \ErrorException
} catch (\ErrorException $e) {
    // handled like any exception
}

// High-level kernel flow: a kernel.exception listener builds the Response
#[AsEventListener(event: 'kernel.exception')]
public function onException(ExceptionEvent $event): void
{
    $event->setResponse(new Response('Something went wrong', 500));
}
```

## Deep Dive — how it works internally

!!! question "Predict first"
    Un service lève une simple `\RuntimeException` qui s'échappe du controller.
    Quel status HTTP le client voit-il — et une `NotFoundHttpException`
    ferait-elle une différence ?

??? note "Reveal"
    `\RuntimeException` devient une **500** : seuls les throwables implémentant
    `HttpExceptionInterface` portent un status personnalisé. `NotFoundHttpException`
    l'implémente *bel et bien*, donc `getStatusCode()` retourne **404**.

### The ErrorHandler component

`Symfony\Component\ErrorHandler\ErrorHandler` est enregistré très tôt (via le
Runtime / `Debug::enable()` en mode debug). Il :

- configure `set_error_handler()` pour lever une `\ErrorException` sur les erreurs PHP,
- configure `set_exception_handler()` pour rendre les throwables non attrapés,
- enregistre une fonction de shutdown pour attraper les erreurs fatales.

```php
use Symfony\Component\ErrorHandler\ErrorHandler;

// set_error_handler() + set_exception_handler() + shutdown function, in one call
ErrorHandler::register();

try {
    trigger_error('boom', E_USER_WARNING); // would be a plain PHP error...
} catch (\ErrorException $e) {
    // ...now it is a catchable \ErrorException
}
```

Le rendu est délégué à des **error renderers** implémentant
`Symfony\Component\ErrorHandler\ErrorRenderer\ErrorRendererInterface` :
`HtmlErrorRenderer` (la page dev enrichie avec stack traces),
`SerializerErrorRenderer` (JSON/XML avec négociation de contenu). Les throwables
sont d'abord normalisés en une
`Symfony\Component\ErrorHandler\Exception\FlattenException`, un snapshot
sérialisable (classe, message, status code, trace) qui peut être rendu ou loggé
sans risque.

```php
use Symfony\Component\ErrorHandler\ErrorRenderer\HtmlErrorRenderer;
use Symfony\Component\ErrorHandler\Exception\FlattenException;

// Any throwable is normalised into a serializable snapshot
$flat = FlattenException::createFromThrowable($throwable);
$flat->getStatusCode(); // e.g. 500
$flat->getClass();      // original exception class

// An ErrorRendererInterface implementation renders it
// (SerializerErrorRenderer would negotiate JSON/XML instead)
$html = (new HtmlErrorRenderer(true))->render($throwable);
echo $html->getAsString(); // rich debug page with stack traces
```

```mermaid
flowchart LR
    E[PHP error] --> H[ErrorHandler]
    H -->|throw| Ex[\ErrorException]
    T[Uncaught throwable] --> FE[FlattenException]
    FE --> R[ErrorRendererInterface]
    R --> O[HTML / JSON / XML]
```

!!! note "Source reference"
    `Symfony\Component\ErrorHandler\ErrorHandler` et `FlattenException` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/ErrorHandler/ErrorHandler.php).

### In the framework: the error controller

Lorsqu'une exception s'échappe d'une request (`$catch = true`), HttpKernel
dispatche `kernel.exception` ; l'`ErrorListener` du framework appelle l'**error
controller** (`error_controller`, par défaut
`Symfony\Component\HttpKernel\Controller\ErrorController`). Celui-ci utilise
l'`ErrorRenderer` pour produire le corps et mappe le throwable vers un status
code : `HttpExceptionInterface::getStatusCode()` s'il s'agit d'une
`Symfony\Component\HttpKernel\Exception\HttpException` (p. ex.
`NotFoundHttpException` → 404), sinon **500**.

```php
use Symfony\Component\HttpKernel\Exception\HttpException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

// Status mapping performed by the error controller:
throw new NotFoundHttpException('No such product'); // getStatusCode() -> 404
throw new HttpException(429, 'Slow down');          // explicit status code
throw new \RuntimeException('DB down');             // no HttpExceptionInterface -> 500
```

### Prod vs dev

| | dev (`APP_DEBUG=1`) | prod |
|---|---|---|
| Page | Page d'exception enrichie + trace | Template d'erreur épuré |
| Détail | Message/trace complets exposés | Générique, aucun détail interne |
| Renderer | `HtmlErrorRenderer` (debug) | template `error.html.twig` / pages par status |

Surchargez les pages de prod avec des templates Twig sous
`templates/bundles/TwigBundle/Exception/`
(`error404.html.twig`, `error500.html.twig`, ou le générique `error.html.twig`).

```twig
{# templates/bundles/TwigBundle/Exception/error404.html.twig #}
<h1>Page not found</h1>

{# templates/bundles/TwigBundle/Exception/error.html.twig — generic fallback
   (error500.html.twig would override it for 500s) #}
<h1>Error {{ status_code }}: {{ status_text }}</h1>
```

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    final class ProductController
    {
        public function show(?Product $product): never
        {
            // 404 status derived from HttpExceptionInterface
            throw new NotFoundHttpException('Product not found');
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/packages/framework.yaml
    framework:
        error_controller: App\Controller\CustomErrorController::show
    ```

=== "Console"

    ```console
    $ php bin/console debug:container error_controller
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Lever des sous-classes de `HttpException` pour le status HTTP | Retourner `new Response('', 404)` partout |
| Personnaliser les templates de prod par status code | Divulguer des stack traces en prod |
| Logger via un listener `kernel.exception` | Avaler les exceptions en silence |

## When (not) to use it / alternatives

Vous instanciez rarement `ErrorHandler` vous-même — le Runtime le câble.
Branchez-vous sur `kernel.exception` pour traduire des exceptions métier en
responses, ou enregistrez un `error_controller` personnalisé pour un contrôle
total du rendu.

!!! danger "Certification traps"
    - Les throwables non-`HttpException` deviennent des **500** ; seule
      `HttpExceptionInterface` porte un status code personnalisé.
    - `FlattenException` est la forme sérialisable utilisée pour le rendu/logging.
    - Le dev expose les traces ; la prod ne doit pas — contrôlé par `APP_DEBUG`.

!!! warning "Common mistakes"
    - S'attendre à ce qu'un template 404 personnalisé s'applique en `dev`
      (c'est la page de debug qui s'affiche à la place).
    - Confondre le composant ErrorHandler avec le flux d'event `kernel.exception`.

## Exercises

1. **(Advanced)** Retournez une 404 depuis un controller pour que le framework
   rende la bonne page d'erreur.
2. **(Advanced)** Expliquez pourquoi une `\RuntimeException` non attrapée
   produit une 500.

??? success "Solutions"

    **1.** Levez `NotFoundHttpException` (voir le code ci-dessus) ;
    `ErrorController` la mappe vers 404 via
    `HttpExceptionInterface::getStatusCode()`.

    **2.** `\RuntimeException` n'implémente pas `HttpExceptionInterface`, donc
    l'error controller applique le status code par défaut : 500.

## Certification questions

??? question "Q1. An uncaught exception that is NOT an HttpException produces which status?"
    - [ ] A. 404
    - [x] B. 500 ✅
    - [ ] C. 400

    **Why:** Seule `HttpExceptionInterface` porte un status ; sinon 500.
    **Ref:** [Errors & exceptions](https://symfony.com/doc/current/controller/error_pages.html).

??? question "Q2. What does the ErrorHandler do with a PHP warning?"
    - [x] A. Converts it into an `\ErrorException` ✅
    - [ ] B. Ignores it
    - [ ] C. Writes it to the response body

    **Why:** `set_error_handler()` lève une `\ErrorException` afin que les erreurs PHP soient interceptables.
    **Ref:** [ErrorHandler](https://symfony.com/doc/current/components/error_handler.html).

??? question "Q3. Which serializable object represents a throwable for rendering?"
    - [x] A. `FlattenException` ✅
    - [ ] B. `HttpException`
    - [ ] C. `ErrorEvent`

    **Why:** `FlattenException` capture un snapshot du throwable pour les renderers/loggers.
    **Ref:** [ErrorHandler](https://symfony.com/doc/current/components/error_handler.html).

## Key takeaways

- L'ErrorHandler convertit les erreurs PHP en exceptions et rend les throwables non attrapés.
- `FlattenException` + `ErrorRendererInterface` produisent une sortie HTML/JSON/XML.
- L'`error_controller` mappe les throwables vers des responses ; exceptions non HTTP → 500.
- La prod masque les détails internes ; le dev montre la trace — piloté par `APP_DEBUG`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `ErrorHandler` = `set_error_handler` + `set_exception_handler` + fonction de shutdown.
    - Renderers : `HtmlErrorRenderer`, `SerializerErrorRenderer`.
    - Status : `HttpExceptionInterface::getStatusCode()` sinon 500.
    - Templates de prod : `templates/bundles/TwigBundle/Exception/error{404,500}.html.twig`.

## Connections

- **Depends on:** [Request Handling](../architecture/request-handling.md) — une exception qui s'échappe d'une request déclenche `kernel.exception`.
- **Reused in:** [Debugging](debugging.md) — `Debug::enable()` câble l'ErrorHandler ; [Exception Handling](../architecture/exception-handling.md) couvre le flux d'events du kernel.
- **Confused with:** l'event `kernel.exception` — le composant convertit/rend les erreurs ; le flux d'event transforme une exception en `Response`.

## Official References
- [Official docs — Error pages](https://symfony.com/doc/current/controller/error_pages.html)
- [Official docs — ErrorHandler component](https://symfony.com/doc/current/components/error_handler.html)
- [Symfony source — ErrorHandler](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/ErrorHandler/ErrorHandler.php)

## Video references

!!! tip "Watch & learn"
    Ce sont des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    "Symfony components" pour consolider ce chapitre. Nous lions des chaînes stables
    plutôt que des vidéos individuelles afin que les références ne périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences et keynotes SymfonyCon.
    - [Official docs for this topic](https://symfony.com/doc/current/controller/error_pages.html) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** les erreurs PHP sont transformées en exceptions interceptables
- [ ] lever une sous-classe de `HttpException` pour contrôler le status dans Symfony 8
- [ ] déboguer un status incorrect (throwable non HTTP retombant sur 500)
- [ ] repérer le piège : seule `HttpExceptionInterface` porte un status personnalisé
- [ ] décrire le rendu `FlattenException` + `ErrorRendererInterface`

---

<small>Related: [Exception Handling](../architecture/exception-handling.md) · [Debugging](debugging.md) · [Profiler](profiler.md)</small>
