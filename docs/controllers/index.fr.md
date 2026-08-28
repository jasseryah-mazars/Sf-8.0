# Controllers

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Value Resolver](../labs/controllers.md)** — un TD pas à pas, guidé en test-first, avec une solution de référence.

Un **controller** est le callable PHP que Symfony exécute pour transformer une
`Request` en `Response`. C'est la première *couche fonctionnelle* que vous
écrivez au-dessus du kernel et du container : tout ce qui vient du
[request lifecycle](../architecture/index.md) et de la
[dependency injection](../dependency-injection/index.md) converge ici.
Cette étape vous apprend comment les controllers sont résolus, quelles
facilités `AbstractController` vous offre, comment les arguments sont remplis
par les **value resolvers**, et comment parler couramment
[HttpFoundation](../http/index.md) — requests, responses, cookies, sessions et
flash messages.

!!! info "Stage at a glance"
    | Champ | Valeur |
    |---|---|
    | **Prérequis** | [Architecture](../architecture/index.md), [Dependency Injection](../dependency-injection/index.md), [HTTP](../http/index.md) |
    | **Niveau** | Avancé → Expert |
    | **Difficulté** | ★★☆ |
    | **Dépendances** | Étapes 3 et 4 |
    | **Priorité de révision** | **Élevée** |
    | **Temps estimé** | 3–4 h |

## Why this stage matters

Un controller est trompeusement simple — « retourner une `Response` » — mais
l'examen sonde la mécanique qui l'entoure : comment
`ControllerResolverInterface` trouve votre callable, comment
`ArgumentResolverInterface` remplit ses paramètres, pourquoi
`AbstractController` est un *service subscriber* plutôt qu'une classe de base
fourre-tout, et le cycle de vie exact d'un flash message ou d'une sub-request.
Maîtrisez la mécanique ici et le routing, les forms et la security deviennent
évidents.

## Micro-chapters

- [Naming Conventions](naming-conventions.md) — le nommage des controllers, les
  controllers à action unique (invokables), `__invoke`, le mythe du suffixe
  `Action`.
- [AbstractController](abstract-controller.md) — les méthodes utilitaires qu'il
  fournit, comment il obtient ses services via `getSubscribedServices()`, et
  pourquoi ce n'est *pas* un `ControllerBase`.
- [The Request](request.md) — type-hinter `Request`, les parameter bags, et
  comment la `Request` atteint votre action (renvoie vers
  [HTTP → Request](../http/request.md)).
- [The Response](response.md) — `Response`, `JsonResponse`, les responses
  streamées et binaires (renvoie vers [HTTP → Response](../http/response.md)).
- [Cookies](cookies.md) — lire et définir des cookies depuis un controller.
- [The Session](session.md) — `RequestStack::getSession()`, `SessionInterface`,
  l'attribute bag, le stockage, l'invalidation et les sessions lazy.
- [Flash Messages](flash-messages.md) — `addFlash()`, `FlashBagInterface`, le
  rendu dans Twig, et le cycle de vie à usage unique.
- [HTTP Redirects](http-redirects.md) — `redirectToRoute()`, `redirect()`,
  `RedirectResponse`, 301 vs 302, et les autres codes de statut de redirection.
- [Internal Redirects (Forwarding)](internal-redirects.md) — `forward()`, les
  sub-requests, et en quoi elles diffèrent d'une redirection HTTP.
- [404 & Error Pages](error-pages.md) — `createNotFoundException()`, lancer une
  `HttpException`, et personnaliser les templates/controllers d'erreur.
- [File Upload](file-upload.md) — `UploadedFile`, déplacer les fichiers,
  `#[MapUploadedFile]` (renvoie vers
  [Forms → File Upload](../forms/file-upload.md)).
- [Built-in Internal Controllers](built-in-controllers.md) —
  `TemplateController` et `RedirectController` pilotés uniquement par la
  configuration des routes.
- [Argument Value Resolvers](value-resolvers.md) — `ValueResolverInterface`,
  les resolvers intégrés, les resolvers ciblés, écrire le vôtre, et les
  priorités.

## How to study this stage

1. Lisez d'abord [Naming](naming-conventions.md) et
   [AbstractController](abstract-controller.md) — ils cadrent tout le reste.
2. Faites le deep dive [Value Resolvers](value-resolvers.md) en pratiquant ;
   c'est le sujet le plus orienté internals et le plus examiné de cette étape.
3. Traitez [Session](session.md), [Flash](flash-messages.md) et les
   [redirects](http-redirects.md) comme un trio — ils partagent le cycle
   request/response.

---

<small>Étape précédente : [Dependency Injection](../dependency-injection/index.md) · Étape suivante : [Routing](../routing/index.md)</small>

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Un contrôleur est le morceau de code que Symfony appelle une fois qu'il sait quelle route a matché — son seul travail est de transformer une requête en réponse.

**Pourquoi ça existe ?** Il faut bien un endroit où écrire "quand quelqu'un visite `/produits`, voici ce qu'il faut faire". Le contrôleur est cet endroit — volontairement simple, pour que la vraie logique vive ailleurs (dans des services).

**🏠 Analogie de la vraie vie :** Le serveur d'un restaurant. Il prend ta commande (la requête), la transmet à la cuisine (les services), et te rapporte le plat fini (la réponse) — il ne cuisine jamais lui-même.

**Symfony dans la vraie vie :** `Client → client du restaurant`, `Request → commande`, `Controller → serveur`, `Service → cuisine`, `Response → plat servi`.

**⚠️ Erreur fréquente :** mettre la "cuisine" (logique métier, requêtes base de données) directement dans le contrôleur — un serveur qui se met à cuisiner ralentit tout le restaurant.

**🧠 Comment le mémoriser :** "Le contrôleur prend la commande et sert le plat — il ne cuisine jamais."


## Official References

- [Symfony documentation — Controllers](https://symfony.com/doc/8.0/controller.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
