# Master Cheat Sheet

Les faits à plus fort rendement, consultables d'un coup d'œil, sur les 15 domaines.
C'est un **squelette pour la veille au soir** — chaque section renvoie au domaine
complet pour le détail. Tout ici est Symfony 8 / PHP 8.4 / Twig 3.x.

!!! tip "How to use it"
    Masquez la colonne de droite et récitez-la. Si une section vous semble mince,
    ouvrez l'index du domaine (lié dans chaque titre) pour les chapitres complets
    et les cheat sheets.

## 1. PHP & Web Security → [area](../php-web-security/index.md)

- **PHP 8.4 :** property hooks, visibilité asymétrique (`public private(set)`),
  `new` sans parenthèses dans les chaînages, lazy objects, attribut `#[\Deprecated]`,
  `array_find` / `array_any` / `array_all` / `array_find_key`.
- **PHP 8.3 :** constantes de classe typées, `#[\Override]`, `json_validate()`,
  lecture dynamique de constantes de classe.
- **Menaces web :** XSS → encodage/échappement de la sortie ; CSRF → tokens par
  formulaire ; SQLi → requêtes paramétrées/préparées ; fixation de session →
  régénérer l'id à la connexion ; transport → HTTPS + HSTS.
- **SPL :** `Iterator`, `IteratorAggregate`, `ArrayAccess`, `Countable`,
  `SplStack`, `SplQueue`, `SplObjectStorage`, `ArrayObject`.

## 2. HTTP → [area](../http/index.md)

| Classe | Signification | Courants |
|---|---|---|
| 1xx | Information | 100, 101 |
| 2xx | Succès | 200, 201, 204 |
| 3xx | Redirection | 301, 302, 304, 307, 308 |
| 4xx | Erreur client | 400, 401, 403, 404, 405, 409, 422, 429 |
| 5xx | Erreur serveur | 500, 502, 503, 504 |

- **Méthodes safe :** GET, HEAD, OPTIONS, TRACE. **Idempotentes :** safe + PUT, DELETE.
  **Ni l'une ni l'autre :** POST, PATCH.
- **Headers de négociation :** `Accept`, `Accept-Language`, `Accept-Encoding`,
  `Accept-Charset`.

## 3. Symfony Architecture → [area](../architecture/index.md)

- **Ordre des events du kernel :** `kernel.request` → `kernel.controller` →
  `kernel.controller_arguments` → *(`kernel.view` seulement si le controller retourne
  autre chose qu'une `Response`)* → `kernel.response` → `kernel.finish_request` →
  `kernel.terminate`. `kernel.exception` se déclenche sur toute exception levée.
- **Classes d'events :** `RequestEvent`, `ControllerEvent`, `ControllerArgumentsEvent`,
  `ViewEvent`, `ResponseEvent`, `FinishRequestEvent`, `TerminateEvent`,
  `ExceptionEvent`.
- **Types de request :** `HttpKernelInterface::MAIN_REQUEST` / `SUB_REQUEST`.
- **Releases :** mineure tous les ~6 mois (mai et novembre) ; majeure tous les ~2 ans ;
  la **dernière mineure d'une majeure est la LTS**. Standard = 8 mois de correctifs de
  bugs + 6 mois de sécurité ; LTS = 3 ans de correctifs + 4 ans de sécurité. Suit
  **semver + la promesse de BC** (`@internal`, `@final`, `@experimental`).

## 4. Dependency Injection → [area](../dependency-injection/index.md)

- **Les services sont private par défaut** ; **autowiring + autoconfiguration activés**
  par défaut dans la configuration standard.
- **Le container est compilé une fois** puis mis en cache ; les compiler passes
  s'exécutent à la compilation.
- **Enregistrement d'une compiler pass :** `ContainerBuilder::addCompilerPass()` dans
  `Kernel::build()` ou le `build()` d'un bundle — **aucun attribut** pour cela.
- **Attributs :** `#[Autowire]`, `#[AutowireLocator]`, `#[AutowireIterator]`,
  `#[AsTaggedItem]`, `#[AsDecorator]`, `#[When(env: 'prod')]`, `#[Exclude]`.
- **Paramètres :** `%kernel.project_dir%`, `%env(...)%` ; à injecter via `#[Autowire('%...%')]`.

## 5. Controllers → [area](../controllers/index.md)

- **Helpers d'`AbstractController` :** `render()`, `redirectToRoute()`, `forward()`
  (sub-request interne), `json()`, `file()`, `addFlash()`, `isGranted()`,
  `createNotFoundException()`, `createAccessDeniedException()`, `generateUrl()`,
  `getUser()`, `createForm()`.
- **Value resolvers :** `#[MapRequestPayload]`, `#[MapQueryString]`,
  `#[MapQueryParameter]`, resolvers backed-enum, UID, `DateTime`.
- Un controller doit retourner une `Response` ; sinon `kernel.view` doit en construire une.

## 6. Routing → [area](../routing/index.md)

- **Options de `#[Route]` :** `path`, `name`, `methods`, `requirements`, `defaults`,
  `host`, `schemes`, `condition`, `priority`, `locale`.
- **Types de référence pour la génération d'URL :** `ABSOLUTE_URL`, `ABSOLUTE_PATH`
  (par défaut), `RELATIVE_PATH`, `NETWORK_PATH`.
- **Paramètres spéciaux :** `_controller`, `_format`, `_locale`, `_fragment`.
- **Debug :** `debug:router`, `router:match <path>`.

## 7. Templating (Twig) → [area](../twig/index.md)

- **Délimiteurs :** `{{ ... }}` affichage, `{% ... %}` logique, `{# ... #}` commentaire.
- **L'auto-escaping est ACTIVÉ** (stratégie html) ; à désactiver valeur par valeur avec `|raw`.
- **Héritage :** `{% extends %}`, `{% block %}`, `{{ parent() }}` ; réutilisation avec
  `{% include %}`, `{% embed %}`, `{% use %}`.
- **URLs/assets :** `path()`, `url()` (absolue), `asset()`, `absolute_url()`.
- **i18n :** `|trans`, `{% trans %}`.

## 8. Data Validation → [area](../validation/index.md)

- Constraints sur **les propriétés, les getters ou la classe** ; des attributs comme
  `#[Assert\NotBlank]`, `#[Assert\Length]`, `#[Assert\Valid]` (cascade).
- **Les groups** + **`GroupSequence`** contrôlent lesquelles/quand ; **`Sequentially`**
  s'arrête au premier échec.
- Paire custom = **`Constraint`** (`getTargets()`) + **`ConstraintValidator`**
  (`validate($value, Constraint $c)`), signaler via
  `$this->context->buildViolation()`.

## 9. Forms → [area](../forms/index.md)

- **Flux :** `createForm()` → `handleRequest($request)` → `isSubmitted() && isValid()`.
- **Ordre des form events :** `PRE_SET_DATA` → `POST_SET_DATA` → `PRE_SUBMIT` →
  `SUBMIT` → `POST_SUBMIT`.
- **Data transformers :** model ↔ norm ↔ view ; `addModelTransformer()`,
  `addViewTransformer()`.
- **CSRF activé par défaut** pour les forms (`csrf_protection`, `csrf_token_id`).
- **Extension de type :** implémenter `getExtendedTypes()`.

## 10. Security → [area](../security/index.md)

- **Clés de `security.yaml` :** `firewalls`, `providers`, `password_hashers`,
  `access_control`, `role_hierarchy`.
- **Flux d'authentification :** l'authenticator `supports()` → `authenticate()` retourne
  un **`Passport`** (avec des **badges**) → le token est créé → handler de succès/échec.
- **Badges du passport :** `UserBadge`, `PasswordCredentials`, `CsrfTokenBadge`,
  `RememberMeBadge`, `PasswordUpgradeBadge`, `PreAuthenticatedUserBadge`.
- **Voters :** `voteOnAttribute()` retourne granted/denied/abstain. **Stratégies :**
  **affirmative (par défaut)**, consensus, unanimous, priority.
- **Attributs :** `IS_AUTHENTICATED_FULLY`, `_REMEMBERED`, `_LAZILY`,
  `PUBLIC_ACCESS`, `IS_IMPERSONATOR`.
- **Hashers :** `auto` (bcrypt / Argon2id).

## 11. HTTP Caching → [area](../http-caching/index.md)

- **Modèle d'expiration :** `Expires`, `Cache-Control: max-age` (navigateur),
  `s-maxage` (cache partagé/proxy).
- **Modèle de validation :** `ETag` ↔ `If-None-Match` ; `Last-Modified` ↔
  `If-Modified-Since` → **`304 Not Modified`**.
- **Directives Cache-Control :** `public`, `private`, `no-cache` (revalider avant
  usage), `no-store` (ne jamais stocker), `must-revalidate`, `max-age`, `s-maxage`.
- **`Vary`** fait varier la clé de cache ; Symfony fournit un reverse proxy
  **`HttpCache`**. *(Pondération réduite dans l'examen Symfony 8.)* L'ESI est
  hors programme — **exclu de la certification Symfony 8**.

## 12. Console → [area](../console/index.md)

- **Command :** `#[AsCommand(name: '...', description: '...')]` ; `execute()` retourne
  `Command::SUCCESS` (0), `FAILURE` (1) ou `INVALID` (2).
- **Arguments :** `REQUIRED`, `OPTIONAL`, `IS_ARRAY`. **Options :** `VALUE_NONE`,
  `VALUE_REQUIRED`, `VALUE_OPTIONAL`, `VALUE_IS_ARRAY`, `VALUE_NEGATABLE`.
- **Verbosité :** `-q` quiet (16) · normal (32) · `-v` verbose (64) · `-vv`
  very-verbose (128) · `-vvv` debug (256).
- **Events :** `console.command`, `console.signal`, `console.error`,
  `console.terminate`.

## 13. Messenger → [area](../messenger/index.md)

- **Pondération accrue** à l'examen Symfony 8. `MessageBusInterface::dispatch()`
  retourne une **`Envelope`** enveloppant le message + des **stamps** (métadonnées).
- Handlers via **`#[AsMessageHandler]`** ; le pipeline de middleware est en
  **poupée russe** (`$stack->next()->handle($envelope, $stack)`).
- **Transports** (Doctrine, AMQP, Redis, `sync`, `in-memory`) configurés via DSN ;
  worker via `messenger:consume`.
- **Stratégie de retry** (backoff exponentiel + **jitter**, 0.1 par défaut) +
  **failure transport** pour les tentatives épuisées.

## 14. Automated Tests → [area](../testing/index.md)

- **Classes de base :** `KernelTestCase` (services), `WebTestCase` (HTTP via `Client`).
- **Client :** `request()`, `submitForm()`, `followRedirect()` ; **Crawler :**
  `filter()`, `selectButton()`, `selectLink()`.
- **Assertions :** `assertResponseIsSuccessful()`,
  `assertResponseStatusCodeSame()`, `assertSelectorTextContains()`.
- **Le container dans les tests :** `static::getContainer()`.
- **Dépréciations :** PHPUnit bridge + `SYMFONY_DEPRECATIONS_HELPER`.

## 15. Miscellaneous → [area](../miscellaneous/index.md)

- **Serializer :** normalizers + encoders ; `serialize()` / `deserialize()` ; formats
  json/xml/csv/yaml.
- **Cache :** PSR-6 `CacheItemPoolInterface`, PSR-16, Symfony Contracts
  `CacheInterface::get($key, $callback)`.
- **Lock :** `LockFactory::createLock()`. **Clock :** `ClockInterface::now()`,
  `MockClock` pour les tests. **Runtime :** point d'entrée de l'application. **Intl /
  Config / DotEnv / ExpressionLanguage** complètent le groupe.

---

<small>Related: [Top Certification Traps](traps.md) · [Memory Aids](memory-aids.md) · [Revision Hub](index.md)</small>

## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
