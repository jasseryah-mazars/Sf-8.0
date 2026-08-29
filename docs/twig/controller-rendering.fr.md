# Controller Rendering

!!! tip "In a nutshell"
    Quand un fragment a besoin de ses propres données, embarquez un controller
    avec `render(controller(...))` plutôt que de faire des requêtes dans le
    template. Point d'examen : le rendu inline est une vraie sous-request
    HttpKernel.

!!! example "Real-world analogy"
    Embarquer un controller, c'est comme une page de journal qui envoie un jeune
    reporter chercher l'encadré « dernières nouvelles » pendant que l'article
    principal est mis en page. `render(controller(...))` dépêche ce reporter —
    une vraie sous-request — qui revient avec une coupure finie et autonome.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Embarquer la sortie d'un controller avec `render(controller(...))`.
    - [ ] Choisir entre le rendu de fragment inline et hinclude.
    - [ ] Décider quand embarquer un controller vaut mieux qu'un `include`.

    **Syllabus:** `Templating (Twig) → Controller rendering` ·
    **Level:** Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Includes](includes.md), [Controllers](../controllers/index.md)

---

## Pour les nuls

### L'idée en une phrase
Quand un fragment de page a besoin de ses propres données, on lui fait exécuter son propre mini-contrôleur plutôt que de tout charger dans le contrôleur principal.

### Imagine dans la vraie vie
Intégrer un contrôleur, c'est comme une page de journal qui envoie un journaliste junior chercher l'encadré "dernières actualités" pendant que l'article principal est déjà mis en page. `render(controller(...))` envoie ce journaliste — une vraie sous-requête — qui revient avec une coupure de presse finie et autonome.

### Dans Symfony
Un panneau "produits recommandés" affiché sur *chaque* page du site est un candidat idéal : plutôt que de faire calculer les recommandations par chaque contrôleur qui affiche une page, un seul contrôleur dédié s'en charge, appelé depuis le template.

### Exemple simple
```twig
{{ render(controller('App\\Controller\\RecoController::afficher')) }}
```

### Comment le mémoriser 🧠
`render(controller(...))` déclenche une **vraie sous-requête HttpKernel** — ce n'est pas un simple appel de fonction PHP, le fragment traverse tout le cycle de requête comme une page normale.


## Theory

Parfois, un fragment a besoin de **sa propre logique et de ses propres données** —
une barre latérale « dernières nouvelles », un résumé de panier, un menu
construit depuis la base de données. Au lieu de récupérer ces données dans le
controller principal, **embarquez un controller** et laissez-le se rendre
lui-même :

```twig
{{ render(controller('App\\Controller\\NewsController::latest', { max: 3 })) }}
```

`controller('…::method', {args})` construit une **référence** vers un
controller ; `render()` l'exécute en **sous-request** et insère le contenu de la
`Response` retournée.

```twig
{# controller() only builds a reference — nothing executes yet #}
{% set ref = controller(
    'App\\Controller\\CartController::summary',
    { max: 3 }
) %}

{# render() runs it as a sub-request and inlines the Response body #}
{{ render(ref) }}
```

## Deep Dive — how it works internally

`render` et `controller` sont fournis par
**`Symfony\Bridge\Twig\Extension\HttpKernelExtension`**, qui délègue à
**`Symfony\Component\HttpKernel\Fragment\FragmentHandler`**. Le handler choisit
un **`FragmentRendererInterface`** par nom de stratégie :

| Appel Twig | Renderer | Ce qu'il fait |
|---|---|---|
| `render(controller(...))` | `InlineFragmentRenderer` | sous-request immédiate, insérée |
| `render_esi(controller(...))` | `EsiFragmentRenderer` | émet un tag `<esi:include>` |
| `render_hinclude(...)` | `HIncludeFragmentRenderer` | émet un tag JS/hinclude |

```php
use Symfony\Component\HttpKernel\Controller\ControllerReference;
use Symfony\Component\HttpKernel\Fragment\FragmentHandler;
use Symfony\Component\HttpKernel\Fragment\InlineFragmentRenderer;

// FragmentHandler holds one FragmentRendererInterface per strategy name
$handler = new FragmentHandler($requestStack, [new InlineFragmentRenderer($kernel)]);

// what HttpKernelExtension does for {{ render(controller('C::m')) }}:
$ref = new ControllerReference('App\\Controller\\NewsController::latest', ['max' => 3]);
echo $handler->render($ref, 'inline');
```

```mermaid
flowchart LR
    T["render(controller('C::m'))"] --> HK[HttpKernelExtension::renderFragment]
    HK --> FH[FragmentHandler::render]
    FH --> R{strategy}
    R -- inline --> IR[InlineFragmentRenderer]
    IR --> SR[HttpKernel sub-request]
    SR --> Resp[Response content]
    R -- esi --> ER[EsiFragmentRenderer → esi:include]
```

- **Inline** émet une vraie sous-request via `HttpKernel::handle(..., SUB_REQUEST)`,
  donc tout le cycle de vie de la request (listeners, resolver) s'exécute pour le
  fragment. Cela coûte une sous-request mais reste transparent et fonctionne partout.
- **hinclude** retourne un placeholder résolu par le **navigateur** via
  JavaScript — la page se rend immédiatement et le fragment se charge de façon
  asynchrone.
- Les controllers embarqués ne sont normalement exposés qu'aux sous-requests ;
  pour autoriser des URL hinclude directes, activez le listener/la route
  **`fragments`** (`framework.fragments`).
- `render_esi(...)` existe aussi comme troisième stratégie, qui délègue le
  fragment à un reverse proxy. **Excluded from Symfony 8 certification** — voir
  [HTTP Caching → ESI](../appendices/out-of-syllabus/esi.md).

```yaml
# config/packages/framework.yaml
framework:
    # fragments listener/route: allow direct (signed) hinclude URLs;
    # hinclude placeholders are resolved by the browser via JavaScript
    fragments:
        enabled: true
        path: /_fragment
```

!!! note "Source reference"
    `Symfony\Bridge\Twig\Extension\HttpKernelExtension`,
    `Symfony\Component\HttpKernel\Fragment\FragmentHandler` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php).

## Configuration & code

=== "Twig"

    ```twig
    {# inline sub-request #}
    {{ render(controller('App\\Controller\\CartController::summary')) }}

    {# placeholder resolved asynchronously by the browser #}
    {{ render_hinclude(controller('App\\Controller\\NewsController::latest', { max: 5 })) }}
    ```

=== "The embedded controller"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Repository\NewsRepository;
    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;

    final class NewsController extends AbstractController
    {
        public function latest(NewsRepository $repo, int $max = 3): Response
        {
            return $this->render('news/_latest.html.twig', [
                'items' => $repo->findLatest($max),
            ]);
        }
    }
    ```

=== "YAML — enable fragments"

    ```yaml
    # config/packages/framework.yaml
    framework:
        fragments:
            enabled: true
            path: /_fragment
    ```

## Best practices & anti-patterns

| ✅ À faire | ❌ À éviter |
|---|---|
| Embarquer un controller pour ses propres données | Interroger la BDD dans un template |
| `render_hinclude` pour du contenu qui peut charger de façon asynchrone | Bloquer toute la page sur un fragment inline lent |
| Garder les controllers embarqués petits | Embarquer de nombreux fragments inline par page |
| Passer des scalaires via les arguments de `controller()` | Passer de gros objets entre sous-requests |

## When (not) to use it / alternatives

- **`include`** — le fragment n'a besoin que de variables déjà disponibles. Le moins cher.
- **`render(controller())`** — le fragment a besoin de **ses propres** services/données/cache.
- **`render_hinclude`** — le fragment peut charger de façon asynchrone après la page principale.

Chaque embed inline est une sous-request ; en abuser nuit aux performances.
Préférez les includes simples sauf si le fragment a réellement besoin d'une
logique isolée.

!!! danger "Certification traps"
    - `render()` prend le **résultat** de `controller()`, pas directement une
      chaîne de controller pour les stratégies de fragment — `controller()`
      construit la référence.
    - Le rendu inline est une **vraie sous-request** (les listeners s'exécutent à
      nouveau), pas un appel de fonction.
    - Les controllers embarqués ne sont joignables directement que lorsque les
      **fragments** sont activés (et l'URL signée).

!!! warning "Common mistakes"
    - Faire des requêtes BDD dans le controller parent *et* les transmettre alors
      qu'un controller embarqué autonome isolerait les responsabilités.
    - Oublier qu'une sous-request a sa **propre** `Request` — les attributs de la
      request parente ne sont pas automatiquement partagés.

## Exercises

1. **(Basic)** Embarquez `CartController::summary` en inline dans le header.
2. **(Intermediate)** Rendez la liste des nouvelles via hinclude pour qu'elle
   charge de façon asynchrone.
3. **(Advanced)** Expliquez ce qu'il advient des listeners quand le fragment
   inline est rendu.

??? success "Solutions"

    **1.** `{{ render(controller('App\\Controller\\CartController::summary')) }}`.

    **2.** `{{ render_hinclude(controller('App\\Controller\\NewsController::latest')) }}`.

    **3.** Une sous-request complète traverse `HttpKernel`, déclenchant les events
    du kernel (`REQUEST`, `CONTROLLER`, `RESPONSE`) pour le fragment de façon
    indépendante.

## Certification questions

??? question "Q1. `render(controller('C::m'))` executes the controller as…"
    - [x] A. A sub-request through HttpKernel ✅
    - [ ] B. A static method call, no request
    - [ ] C. A redirect
    - [ ] D. A CLI command

    **Why:** Le renderer inline émet une `SUB_REQUEST`. **Ref:**
    [Embedding controllers](https://symfony.com/doc/8.0/templates.html#embedding-controllers).

??? question "Q2. Which handler chooses the fragment renderer?"
    - [x] A. `FragmentHandler` ✅
    - [ ] B. `UrlGenerator`
    - [ ] C. `EscaperExtension`
    - [ ] D. `AppVariable`

    **Why:** `FragmentHandler` sélectionne le `FragmentRendererInterface`. **Ref:**
    [FragmentHandler](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php).

## Key takeaways

- `render(controller(...))` embarque un controller en sous-request (inline).
- `render_hinclude` délègue le chargement au navigateur via un placeholder JS.
- Soutenu par `HttpKernelExtension` → `FragmentHandler` → un `FragmentRenderer`.
- N'utilisez-le que quand le fragment a besoin de sa propre logique/données/cache.

## Last-minute revision

!!! tip "Cheat sheet"
    - `render(controller('C::m', {a:1}))` = sous-request inline.
    - `render_hinclude(...)` = placeholder asynchrone résolu par le navigateur.
    - Activation des URL de fragment directes via `framework.fragments`.
    - `include` pour les fragments peu coûteux ; embed pour la logique isolée.

## Connections

- **Depends on:** [Includes](includes.md) — l'embed est l'alternative plus lourde quand un simple `include` ne peut pas récupérer ses propres données.
- **Related but excluded:** [HTTP Caching → ESI](../appendices/out-of-syllabus/esi.md) — `render_esi` utilise le même `FragmentHandler`, mais l'ESI elle-même est **exclue de la certification Symfony 8**.
- **Confused with:** [Controllers](../controllers/index.md) — le rendu inline est une vraie **sous-request**, pas un simple appel de méthode.

## Official References
- [Official — Embedding controllers](https://symfony.com/doc/8.0/templates.html#embedding-controllers)
- [Symfony source — FragmentHandler](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

## Video references

!!! tip "Watch & learn"
    Ce sont des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « Twig templating » pour consolider ce chapitre. Nous lions des chaînes
    stables plutôt que des vidéos individuelles afin que les références ne
    périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences SymfonyCon & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/templates.html#embedding-controllers) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** embarquer un controller plutôt que de faire des requêtes dans le template
- [ ] embarquer un controller en inline et via hinclude en Symfony 8
- [ ] déboguer un fragment qui relance les listeners du kernel dans sa propre sous-request
- [ ] expliquer le chemin `HttpKernelExtension` → `FragmentHandler` → renderer

---

<small>Related: [Includes](includes.md) · [Controllers](../controllers/index.md)</small>
