# Revision Sheet — Controllers

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Controllers](../../controllers/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Une **fiche imprimable, tenant sur une page**, qui résume chaque sous-chapitre de Controllers en quelques puces "à retenir" suivies d'une ligne "Cheat" très dense.

**Pourquoi ça existe ?** Dans les derniers jours avant l'examen, on veut un support papier ou PDF unique par domaine — pas 10 onglets de navigateur ouverts. Cette fiche condense un domaine entier sur une seule page imprimable.

**🏠 Analogie de la vraie vie :** C'est la **fiche de révision recto-verso** qu'un étudiant prépare avant un examen universitaire : tout le cours du semestre réduit à une page, à relire dans le métro le matin de l'épreuve.

**Symfony dans la vraie vie :** Chaque puce "à retenir" → une règle déjà apprise en détail dans le chapitre / La ligne "Cheat:" → la version ultra-compacte, presque un aide-mémoire de syntaxe / Lien "Full detail" → retour au chapitre complet si un point ne "sonne" plus familier.

**⚠️ Erreur fréquente :** Imprimer cette fiche *avant* d'avoir étudié Controllers en détail, en espérant apprendre directement dessus — le format est trop dense pour un premier apprentissage, il ne fonctionne qu'en rappel.

**🧠 Comment le mémoriser :** *« Une page, un domaine, la veille de l'examen »* — cette fiche est le tout dernier support à consulter, pas le premier.

## AbstractController
- `AbstractController` is optional sugar built on a **service subscriber**.
- Services arrive through a **lazy locator**, keyed by `getSubscribedServices()`.
- Helpers are `protected`; optional services carry the `?` prefix.
- Inject your *own* dependencies via the constructor — don't fetch them from
  `$this->container`.

**Cheat:** Implements `ServiceSubscriberInterface`; `setContainer()` injects a locator. Subscribed: router, request_stack, http_kernel, serializer, twig, form.factory, security.*, parameter_bag, web_link serializer. `?ServiceClass` = optional. Merge `parent::getSubscribedServices()`. Helpers return: `render`→Response, `json`→JsonResponse, `redirectToRoute`→ RedirectResponse, `createNotFoundException`→exception (you `throw` it).

## Built-in Internal Controllers
- `TemplateController` renders a template (with optional cache headers) from config.
- `RedirectController::redirectAction` (route) / `urlRedirectAction` (URL) redirect
  from config.
- `permanent: true` → 301/308 (cached); empty target → 410 Gone.
- Use them only for logic-free routes; otherwise write a controller.

**Cheat:** Template: `controller: TemplateController`, `defaults.template`. Redirect route: `RedirectController::redirectAction`, `defaults.route`. Redirect URL: `RedirectController::urlRedirectAction`, `defaults.path`. `permanent`→301/308 · empty target→410 · `keepRequestMethod`/`keepQueryParams`.

## Cookies
- Read from `$request->cookies`; write with `$response->headers->setCookie()`.
- Use the immutable `Cookie` value object and its `with*()` methods.
- Secure defaults: `HttpOnly=true`, `SameSite=lax`; `None` needs `Secure`.
- Deleting requires matching path/domain; cookies are client-visible — no secrets.

**Cheat:** Read: `$request->cookies->get('x')`. Set: `Cookie::create('x','v')->withSecure(true)->withHttpOnly(true)`; `$response->headers->setCookie($c)`. Delete: `$response->headers->clearCookie('x', path, domain)`. `SameSite=None` ⇒ must be `Secure`.

## 404 & Error Pages
- Throw exceptions; the kernel maps `HttpExceptionInterface` to status codes.
- `createNotFoundException()` returns an exception — remember to `throw`.
- `kernel.exception` → error controller → error renderer produces the page.
- Override `errorXXX.html.twig` (prod) or the error controller for full control.

**Cheat:** `throw $this->createNotFoundException()` → 404. `denyAccessUnlessGranted()` → 403 via `AccessDeniedException`. Non-Http exception → 500. Status from `getStatusCode()`. Prod templates: `templates/bundles/TwigBundle/Exception/errorXXX.html.twig`.

## Handling File Uploads
- Uploads arrive as `UploadedFile` in `$request->files`; always null-check.
- Trust `getMimeType()`/`guessExtension()`, never the client-supplied name/MIME.
- `move()` throws `FileException`; store files outside the web root.
- `#[MapUploadedFile]` maps + validates uploads as controller arguments.

**Cheat:** `$request->files->get('field')` → `?UploadedFile`. Validate: `isValid()`, `getMimeType()`, `getSize()`. `move($dir, $safeName)` (throws `FileException`). `#[MapUploadedFile([new File(...)])] UploadedFile $x`.

## Flash Messages
- `addFlash($type, $msg)` queues a one-shot message in the session flash bag.
- Reading consumes; `peek`/`peekAll` reads without consuming.
- Designed for Post/Redirect/Get — add, redirect, show, discard.
- Twig: iterate `app.flashes` (all) or `app.flashes('type')`.

**Cheat:** `$this->addFlash('success','...')` → FlashBag. Twig: `{% for label, messages in app.flashes %}`. `get/all` consume; `peek/peekAll` don't. Needs a session ⇒ not for shared-cached pages.

## HTTP Redirects
- `redirectToRoute()` (route name) and `redirect()` (URL) return a `RedirectResponse`.
- Default is **302**; 307/308 preserve method+body; 301/308 are cached.
- A redirect is a new browser request — use flashes to carry a message.
- Never redirect to unvalidated user input (open redirect).

**Cheat:** `redirectToRoute('name', ['id'=>1], 302)` · `redirect('/url', 302)`. 302 default · 303 force GET (PRG) · 307/308 keep method · 301/308 cached. Internal target ⇒ `redirectToRoute`. External input ⇒ validate.

## Internal Redirects (Forwarding)
- `forward()` = sub-request, same HTTP request, URL unchanged, returns a Response.
- Redirect = new client request with a `3xx` + `Location`.
- Sub-requests run as `SUB_REQUEST`; `isMainRequest()` is false; firewall skips.
- Prefer a shared service to reuse *logic*; forward to reuse a whole *response*.

**Cheat:** `$this->forward('Ctrl::action', ['arg'=>v])` → Response, internal. Kernel: `SUB_REQUEST`, pushed on `RequestStack`. forward ≠ redirect (no 3xx, no URL change).

## Controller Naming Conventions
- A controller is *any callable*; conventions are for humans, not the framework.
- Class suffix `Controller`, method `camelCase`, **no** `Action` suffix.
- Invokable controllers use `__invoke()` and are referenced by class name alone.
- Action methods must be `public`; controllers are services (autowiring).

**Cheat:** `_controller`: `Class::method` | `Class` (invokable) | `service::method`. Invokable = `#[Route]` on class + `public function __invoke()`. No `Action` suffix. Methods `public`. Classes usually `final`.

## The Request in a Controller
- Type-hint `Request` in actions; inject `RequestStack` in services.
- Bags: `query` (GET), `request` (POST body), `attributes` (route/internal),
  `headers`, `cookies`, `files`, `server`.
- `InputBag` typed getters cast safely; prefer mapping attributes for validation.

**Cheat:** `query`→GET, `request`→POST, `attributes`→route params. `getInt/getString/getEnum/getBoolean` on `query` & `request`. Services: `RequestStack::getCurrentRequest()`. Never autowire `Request`.

## Returning Responses
- Actions must return a `Response`; non-Response values need a `kernel.view` listener.
- Pick `JsonResponse`, `StreamedResponse`, or `BinaryFileResponse` by payload shape.
- `StreamedResponse` streams at send time — no header changes mid-stream.
- Use `Response::HTTP_*` constants for status codes.

**Cheat:** `render`→Response, `json`→JsonResponse, `file`→BinaryFileResponse, `stream`→StreamedResponse. Non-Response return ⇒ ViewEvent ⇒ else LogicException. `JsonResponse::fromJsonString($json)` for pre-encoded JSON.

## The Session
- Get the session via `RequestStack::getSession()` or an action type-hint.
- Attribute bag: `set/get/has/remove/clear`; also holds the flash bag.
- Sessions are lazy — cookie/start only on first use.
- `migrate()` = new id keep data (fixation defence); `invalidate()` = wipe + new id.

**Cheat:** Service: `RequestStack::getSession()`. Controller: type-hint `SessionInterface`. Storage: `NativeSessionStorage` + save handler (files/redis/pdo). Lazy: no `Set-Cookie` until touched ⇒ don't touch on cacheable pages. `migrate()` after login; `invalidate()` on logout.

## Argument Value Resolvers
- `ArgumentResolver` walks ordered `ValueResolverInterface`s; the first to yield wins.
- `resolve()` returns an `iterable`; yield nothing to decline.
- Built-in chain: Request/Session (120) → Backed/Uid/DateTime/RequestAttribute
  (100) → Service (-50) → Default (-100) → Variadic (-150).
- Attribute resolvers (`MapRequestPayload`, `MapQueryParameter`,
  `MapUploadedFile`, `CurrentUser`) are **targeted** — activated by the attribute.

**Cheat:** Interface: `ValueResolverInterface::resolve(Request, ArgumentMetadata): iterable`. Tag: `controller.argument_value_resolver` (chain) / `controller.targeted_value_resolver` (attribute-only). Priorities: Request/Session 120 · attrs 100 · Service -50 · Default -100 · Variadic -150. `#[MapRequestPayload]`→body DTO (422/400) · `#[MapQueryString]`→query DTO · `#[MapQueryParameter]`→one param · `#[CurrentUser]`→user.
