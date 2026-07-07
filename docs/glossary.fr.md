# Glossaire

Consultation rapide des termes utilisés par la certification Symfony 8. Chaque
entrée tient en une ligne ; suivez le lien pour le chapitre complet.

!!! tip "How to use"
    Survolez-le avant l'examen pour ancrer le vocabulaire. Si une définition vous
    semble floue, ouvrez le chapitre lié et faites son lab.

## A

- **AbstractController** — Controller de base avec des raccourcis utilitaires (`render`, `json`,
  `redirectToRoute`, `denyAccessUnlessGranted`…) ; c'est un service subscriber. → [chapter](controllers/abstract-controller.md)
- **Access decision** — Comment l'autorisation aboutit à une décision à partir des voters via une
  stratégie (affirmative/unanimous/consensus/priority). → [voters](security/voters.md)
- **`access_control`** — Règles de firewall évaluées **de haut en bas, la première correspondance gagne**. → [chapter](security/access-control.md)
- **Argument value resolver** — Transforme les données de la request en arguments typés du controller
  (`ValueResolverInterface`). → [chapter](controllers/value-resolvers.md)
- **Attribute** — Métadonnées PHP 8 `#[...]` (p. ex. `#[Route]`, `#[AsCommand]`). Préférées aux annotations.
- **Autoconfiguration** — Applique automatiquement des tags/appels aux services selon leur interface/attribut. → [registration](dependency-injection/registration.md)
- **Autowiring** — Injecte les arguments des services d'après leur type-hint. → [chapter](dependency-injection/autowiring.md)

## B

- **Badge** — Un élément d'un `Passport` résolu lors du `CheckPassportEvent` (`UserBadge`,
  `CsrfTokenBadge`, `RememberMeBadge`…). → [authenticators](security/authenticators.md)
- **BC promise** — Contrat de rétrocompatibilité : les ruptures n'arrivent que dans les versions majeures,
  après dépréciation. → [chapter](architecture/bc-promise.md)
- **Bus (message bus)** — `MessageBusInterface` ; fait passer un message à travers des middlewares jusqu'à son handler. → [messenger](miscellaneous/messenger.md)

## C

- **Cache-Control** — Header HTTP pilotant la fraîcheur (`max-age`, `s-maxage`, `public`,
  `private`, `no-cache`, `no-store`). → [expiration](http-caching/expiration.md)
- **CompiledContainer** — Le container PHP dumpé, construit une seule fois à la compilation. → [container](dependency-injection/container.md)
- **Compiler pass** — `CompilerPassInterface` ; modifie le container au moment de la construction
  (enregistré dans `Kernel::build()` — **pas d'attribut `#[CompilerPass]`**). → [chapter](dependency-injection/compiler-passes.md)
- **Constraint / Validator** — Une règle (`Constraint`) + la classe qui la fait respecter
  (`ConstraintValidator`). → [custom constraints](validation/custom-constraints.md)
- **Content negotiation** — Choisir un format de response à partir des headers `Accept*`. → [chapter](http/content-negotiation.md)
- **CSRF token** — Token anti-falsification ; stateless depuis Symfony 7.2+/8. → [chapter](forms/csrf.md)

## D

- **Data collector** — Alimente le Web Profiler (`DataCollectorInterface`). → [profiler](miscellaneous/profiler.md)
- **Data transformer** — Convertit les données du form entre model↔norm↔view
  (`transform`/`reverseTransform`). → [chapter](forms/data-transformers.md)
- **Decoration** — Envelopper un service ; plus `decoration_priority` est élevé, plus on est à l'extérieur ; `.inner` = le service décoré. → [chapter](dependency-injection/decoration.md)
- **Deprecation** — `trigger_deprecation()` ; un avertissement doux avant une suppression future. → [chapter](architecture/deprecations.md)

## E

- **Envelope** — Enveloppe un message Messenger avec des **stamps** (métadonnées). → [messenger](miscellaneous/messenger.md)
- **ESI (Edge Side Includes)** — Mettre en cache des fragments indépendamment, au niveau d'une gateway. → [chapter](http-caching/esi.md)
- **ETag** — Header de cache par validation (empreinte du contenu) ; l'emporte sur `Last-Modified`. → [validation](http-caching/validation.md)
- **EventDispatcher** — Distribue les events aux listeners/subscribers par priorité. → [chapter](architecture/events.md)
- **`empty_data`** — Valeur du form utilisée quand rien n'est soumis. → [creation](forms/creation.md)

## F

- **Factory** — Un callable qui construit un service (statique/instance/invokable). → [chapter](dependency-injection/factories.md)
- **Firewall** — Le contexte de sécurité d'un ensemble d'URLs ; détermine comment l'identité est prouvée. → [chapter](security/firewalls.md)
- **Flash message** — Message de session à usage unique, lu à la request suivante. → [chapter](controllers/flash-messages.md)
- **Flex** — Plugin Composer qui auto-configure les packages via des recipes. → [chapter](architecture/flex.md)

## G–H

- **Group (validation)** — Un sous-ensemble nommé de constraints ; `Default` vs `{ClassName}`. → [groups](validation/groups.md)
- **GroupSequence** — Validation ordonnée ; s'arrête au premier groupe en échec. → [chapter](validation/group-sequence.md)
- **HttpKernel** — Transforme une `Request` en `Response` ; distribue les 8 kernel events. → [request handling](architecture/request-handling.md)
- **HttpClient** — `HttpClientInterface` ; à tester avec `MockHttpClient`. → [chapter](http/httpclient.md)

## I–K

- **`#[IsGranted]`** — Attribut imposant l'autorisation sur un controller/une action. → [authorization](security/authorization.md)
- **`IS_AUTHENTICATED_*` / `PUBLIC_ACCESS`** — Attributs d'accès évalués à l'exécution (ce ne sont pas des rôles) ;
  `IS_AUTHENTICATED_ANONYMOUSLY` a été remplacé par `PUBLIC_ACCESS`. → [roles](security/roles.md)
- **Kernel events** — `kernel.request` → `controller` → `controller_arguments` →
  `view` → `response` → `finish_request` → `terminate` (+ `exception` hors séquence). → [request handling](architecture/request-handling.md)

## L–M

- **Last-Modified** — Header de cache par validation basé sur un horodatage. → [validation](http-caching/validation.md)
- **Middleware (Messenger)** — Couches enveloppant le traitement ; en poupées russes via `stack->next()`. → [messenger](miscellaneous/messenger.md)
- **MockHttpClient** — HttpClient en mémoire pour les tests. → [chapter](http/httpclient.md)

## N–P

- **`NotBlank` vs `NotNull`** — `NotBlank` rejette `''`/`[]`/le vide ; `NotNull` ne rejette que `null`. → [built-in constraints](validation/built-in-constraints.md)
- **Passport** — La charge utile d'authentification, composée de badges construits par un authenticator. → [authenticators](security/authenticators.md)
- **Password hasher** — Hachage à sens unique (`auto`/bcrypt/sodium) ; prend en charge le rehachage. → [chapter](security/password-hashers.md)
- **Profiler** — Débogage en dev + data collectors ; utilisable aussi dans les tests. → [chapter](miscellaneous/profiler.md)
- **PSR** — Interfaces partagées que Symfony implémente/consomme (PSR-3/4/6/7/11/14/16/20). → [chapter](architecture/psr.md)

## Q–R

- **Reference type** — Mode de génération d'URL : `ABSOLUTE_PATH` (par défaut), `ABSOLUTE_URL`,
  `NETWORK_PATH`, `RELATIVE_PATH`. → [url generation](routing/url-generation.md)
- **Retry strategy / failure transport** — Redistribution Messenger puis mise en dead-letter. → [messenger](miscellaneous/messenger.md)
- **Role hierarchy** — Héritage des `ROLE_*` (p. ex. `ROLE_ADMIN` ⊃ `ROLE_USER`). → [roles](security/roles.md)
- **Runtime** — Amorce le point d'entrée de l'application (`SymfonyRuntime`). → [chapter](miscellaneous/runtime.md)

## S

- **Service locator** — Accès lazy, à la demande, à un ensemble fixe de services. → [chapter](dependency-injection/service-locators.md)
- **Serializer** — normalizers + encoders ; `#[Groups]` contrôle les champs. → [chapter](miscellaneous/serializer.md)
- **Stamp** — Métadonnées sur une `Envelope` Messenger. → [messenger](miscellaneous/messenger.md)
- **Stateless CSRF** — CSRF basé sur cookie/origin, sans session (7.2+/8). → [csrf](forms/csrf.md)

## T–V

- **Tag** — Marque des services pour les collecter (`tagged_iterator`, `#[AutowireLocator]`). → [chapter](dependency-injection/tags.md)
- **Token / TokenStorage** — L'état d'authentification courant. → [authentication](security/authentication.md)
- **Value object** — Conteneur de données typé et immuable (souvent `readonly`). → [OOP](php-web-security/oop.md)
- **Voter** — Vote GRANTED/DENIED/ABSTAIN sur une décision d'accès. → [chapter](security/voters.md)

## W

- **WebTestCase / KernelTestCase** — Classes de base de tests fonctionnels (client HTTP) vs
  d'intégration (container). → [functional tests](testing/functional-tests.md)
- **Web Profiler** — La toolbar de dev + l'interface du profiler. → [chapter](miscellaneous/profiler.md)

---

<small>Related: [Roadmap](roadmap.md) · [Revision Hub](revision/index.md) · [Cheat Sheet](revision/cheat-sheet.md)</small>

## Official References

- [Symfony documentation home](https://symfony.com/doc/current/)
- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
