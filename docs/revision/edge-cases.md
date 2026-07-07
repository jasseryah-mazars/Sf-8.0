# "What happens if…?" — Edge-Case Drills

Expert exams live in the edge cases: the situations where the framework does
something *other* than what the naive answer predicts. This page is a drill deck —
79 "What happens if…?" questions across all 14 syllabus areas, each hiding a
precise, verifiable behaviour.

!!! tip "How to drill"
    Read the question, answer it **out loud** in one or two sentences — commit to
    an answer before you peek — then click to reveal. If your answer missed the
    key word (the status code, the exception class, the default), open the linked
    chapter and re-read it. Wrong-then-corrected beats vaguely-right every time.

## PHP & Web Security

??? question "What happens if a `TypeError` is thrown inside a `catch (\Exception $e)` block's `try`?"
    It is **not caught** — `TypeError` extends `\Error`, which sits on a separate
    branch of the hierarchy from `\Exception`. Only `catch (\Throwable)` (or
    `\Error`/`TypeError` explicitly) catches it; the uncaught error becomes fatal.
    **Ref:** [Exceptions](../php-web-security/exceptions.md)

??? question "What happens if both `try` and `finally` contain a `return` statement?"
    The `finally` return **wins** — it overrides the value already computed in
    `try`. `finally` always executes, even after a `return` or a thrown exception,
    so a `return` there silently swallows both.
    **Ref:** [Exceptions](../php-web-security/exceptions.md)

??? question "What happens if two traits used by the same class define a method with the same name?"
    A **fatal collision error** — PHP refuses to guess. You must resolve it
    explicitly with `insteadof` (pick one) or `as` (alias the other); `as` can also
    change visibility. Note the class's *own* method would win over both traits.
    **Ref:** [Traits](../php-web-security/traits.md)

??? question "What happens if you call `new DateTime()` inside a namespaced file without importing it?"
    A fatal **"Class App\\…\\DateTime not found"** error. Unqualified *class* names
    never fall back to the global namespace — only functions and constants do. Use
    `use DateTime;` or write `new \DateTime()`.
    **Ref:** [Namespaces](../php-web-security/namespaces.md)

??? question "What happens if a `match` expression receives a value no arm covers?"
    It throws **`\UnhandledMatchError`** — unlike `switch`, which silently does
    nothing without a `default`. Remember `match` also compares **strictly**
    (`===`), so `match(0)` will not enter a `'0'` arm.
    **Ref:** [PHP API & language features](../php-web-security/php-api.md)

??? question "What happens if you HTML-escape a user value and then print it inside a `<script>` block?"
    You can still be XSS'd. HTML escaping neutralises markup context only; inside
    JavaScript (or a URL) different characters are dangerous, so you need the
    **context-appropriate** escaper (e.g. Twig's `|e('js')`).
    **Ref:** [Web security](../php-web-security/web-security.md)

## HTTP

??? question "What happens if you set a cookie after the body has started being output — native PHP vs HttpFoundation?"
    Native `setcookie()` fails with a **"headers already sent"** warning and the
    cookie is never sent. With HttpFoundation, cookies are queued on the
    `Response`'s `ResponseHeaderBag` and only emitted when `Response::send()` runs,
    so the order of your calls doesn't matter — as long as nothing echoes output
    before `send()`.
    **Ref:** [Cookies](../http/cookies.md)

??? question "What happens if you create a cookie with `SameSite=None` but without the `Secure` flag?"
    Browsers **reject/drop the cookie** — `SameSite=None` is only accepted over
    HTTPS with `Secure=true`. This is a favourite trap because the server-side
    code runs without any error; the cookie just never comes back.
    **Ref:** [Cookies](../http/cookies.md)

??? question "What happens if you call `$cookie->withSecure(true)` and don't reassign the result?"
    Nothing — a **silent no-op**. Symfony's `Cookie` object is immutable; every
    `with*()` method returns a **new instance** and leaves the original untouched.
    You must write `$cookie = $cookie->withSecure(true)`.
    **Ref:** [Cookies](../http/cookies.md)

??? question "What happens to the response body when `prepare()` runs for a HEAD request or a 204/304 response?"
    The body is **stripped** — those responses must not carry content. `prepare()`
    (called by the kernel, rarely by you) also fixes `Content-Type`/charset
    inconsistencies against the request.
    **Ref:** [Response](../http/response.md)

??? question "What happens if you call `getContent()` on an HttpClient response that returned a 404?"
    It **throws** (a `ClientException` for 4xx; 3xx/5xx throw their own families) —
    `getContent()`/`toArray()` throw on any 3xx/4xx/5xx by default. Only
    `getStatusCode()` never throws; pass `false`/`throw: false` to read an error
    body.
    **Ref:** [HttpClient](../http/httpclient.md)

??? question "What happens if a POST request carries `_method=PUT` in its body by default?"
    Nothing — the request stays a POST. `http_method_override` defaults to
    **`false`**, so `_method` is ignored until you enable it; even enabled, the
    override only applies to POST requests. `getMethod()` honours the override,
    `getRealMethod()` never does.
    **Ref:** [HTTP methods](../http/methods.md)

## Symfony Architecture

??? question "What happens if a `kernel.request` listener sets a response?"
    Request handling **short-circuits**: the controller is never resolved, and
    `kernel.controller`, `kernel.controller_arguments` and `kernel.view` are all
    skipped. The response still passes through `kernel.response` before being sent.
    **Ref:** [Request handling](../architecture/request-handling.md)

??? question "What happens if a controller returns a non-`Response` value and no `kernel.view` listener converts it?"
    The kernel throws a **`LogicException`** ("The controller must return a
    Response…") — not a silent 200. `kernel.view` only *offers* the chance to
    build a `Response` from the value; someone has to take it.
    **Ref:** [Request handling](../architecture/request-handling.md)

??? question "What happens if an exception is thrown and no `kernel.exception` listener sets a response?"
    The exception is **re-thrown** and surfaces as a 500. In practice the built-in
    `ErrorListener` (priority **−128**, so after your listeners) renders an error
    response; a response set on `kernel.exception` still passes through
    `kernel.response`.
    **Ref:** [Exception handling](../architecture/exception-handling.md)

??? question "What happens if your code extends a Symfony class marked `final` or relies on `@internal` API?"
    It can break on **any release** — `@internal` code has **no BC guarantee**
    even when PHP-`public`, and subclassing around `final` is outside the promise
    entirely. The BC promise covers documented, non-internal, non-experimental API
    only.
    **Ref:** [Backward-compatibility promise](../architecture/bc-promise.md)

??? question "What happens to the generated config files when you `composer remove` a package installed via Flex?"
    Flex **reverses the recipe**: the bundle registration, config files and env
    placeholders it added are removed again. `symfony.lock` (recipes) is updated —
    that file tracks recipes, while `composer.lock` tracks package versions.
    **Ref:** [Flex](../architecture/flex.md)

## Controllers

??? question "What happens if a controller returns a plain string?"
    A string is not a `Response`, so **`kernel.view`** fires; with no listener to
    convert it you get a **`LogicException`**, not a page containing the string.
    Return `new Response($string)` or install a view listener.
    **Ref:** [Response](../controllers/response.md)

??? question "What happens if you call `$this->createNotFoundException()` but forget to `throw` it?"
    Nothing aborts — the method only **returns** a `NotFoundHttpException` object
    and execution continues to the next line. The 404 happens only when you
    `throw` it yourself.
    **Ref:** [Error pages](../controllers/error-pages.md)

??? question "What happens to the firewall and the URL when you `forward()` to another controller?"
    Neither changes. `forward()` runs an **internal sub-request** —
    `isMainRequest()` is `false`, the security firewall does **not**
    re-authenticate, no 3xx is sent, and the browser's URL stays the same. Data
    travels through the sub-request's *attributes*, not the query string.
    **Ref:** [Internal redirects (forwarding)](../controllers/internal-redirects.md)

??? question "What happens if you `addFlash()` and then `render()` in the same action instead of redirecting?"
    The flash is not consumed by that render if the template doesn't read it — it
    **persists and shows up on the following request**, seemingly out of nowhere.
    Flashes are designed for the redirect-then-display pattern; reading them
    (e.g. `app.flashes`) is what consumes them.
    **Ref:** [Flash messages](../controllers/flash-messages.md)

??? question "What happens if you type-hint `Request` in a service's constructor?"
    A container error — `Request` is **request-scoped**, not a service, so it
    cannot be constructor-injected. Inject **`RequestStack`** and call
    `getCurrentRequest()` at use time (controllers are special: their *action
    arguments* can receive the `Request` via a value resolver).
    **Ref:** [The Request](../controllers/request.md)

??? question "What happens if an uploaded file exceeds PHP's `post_max_size`?"
    You can get an **empty `files` bag with no exception** — PHP discards the
    oversized body before Symfony sees it. Always null-check the `UploadedFile`;
    also remember `getClientOriginalName()`/`getClientMimeType()` are
    client-controlled and spoofable.
    **Ref:** [File upload](../controllers/file-upload.md)

## Routing

??? question "What happens if two routes match the same URL?"
    The router tests routes in declaration order and the **first match wins** —
    the second route is silently never reached. With attributes, use `priority`
    to reorder; `debug:router` shows the effective order.
    **Ref:** [Routing configuration](../routing/configuration.md)

??? question "What happens if the path matches a route but the HTTP method doesn't?"
    A **405 Method Not Allowed** with an `Allow` header listing the valid methods —
    not a 404. Bonus nuance: `methods: ['GET']` also matches **HEAD**
    automatically, and a *scheme* mismatch triggers a redirect instead of a 405.
    **Ref:** [Routing methods](../routing/methods.md)

??? question "What happens if a URL matches a route's path but fails its `requirements` regex?"
    The route simply **doesn't match** — you get a **404** (or another route gets
    its chance), never a 400. Requirements are implicitly anchored, so adding
    `^`/`$` yourself is wrong; the default placeholder regex `[^/]+` never crosses
    a slash.
    **Ref:** [Route requirements](../routing/requirements.md)

??? question "What happens if a route's `condition` expression evaluates to false?"
    The route is treated as **not matched → 404**, not 403. Conditions affect
    **matching only** — URL *generation* completely ignores them, so `path()` will
    happily generate a URL the matcher will then refuse.
    **Ref:** [Route conditions](../routing/conditions.md)

??? question "What happens if you POST to `/blog/` when the route is defined as `/blog`?"
    A **405** — the automatic trailing-slash redirect (301) applies to **GET and
    HEAD only**. Only safe-method requests get redirected to the canonical form;
    other methods fail rather than lose their body to a redirect.
    **Ref:** [Routing redirects](../routing/redirects.md)

??? question "What happens if you pass `generateUrl()` a parameter that isn't a route placeholder?"
    It is appended as the **query string** — extra parameters are never silently
    dropped. Also remember the default reference type is **`ABSOLUTE_PATH`** (a
    root-relative path), not a full URL.
    **Ref:** [URL generation](../routing/url-generation.md)

## Templating (Twig)

??? question "What happens if `path()` is called with a route name that doesn't exist?"
    A **`RouteNotFoundException` at render time** — template URL generation is not
    checked at compile time. And in an email body, `path()` produces a *relative*
    URL that breaks in mail clients; use `url()` there.
    **Ref:** [URLs in templates](../twig/urls.md)

??? question "What happens if an `{% include %}` with `ignore missing` hits an error *inside* the included template?"
    The error **still propagates** — `ignore missing` only suppresses the
    `LoaderError` for a template that doesn't exist, not runtime errors within one
    that does. Passing a *list* of templates renders the first existing one.
    **Ref:** [Includes](../twig/includes.md)

??? question "What happens to auto-escaping if the template is named `report.txt.twig`?"
    **Nothing is escaped** — the escaping strategy is chosen by *file extension*,
    and `txt` maps to no escaping. Auto-escaping is applied at **print** (`{{ }}`),
    not when a variable is `set`.
    **Ref:** [Auto-escaping](../twig/auto-escaping.md)

??? question "What happens if a template uses `render_esi()` but no ESI-capable surrogate is in front of the app?"
    The fragment renders **inline via a regular sub-request** — same output,
    silently, with no error. The `<esi:include>` tag is only emitted when a
    surrogate advertises ESI capability, so you lose the per-fragment TTL benefit
    without noticing.
    **Ref:** [Embedding controllers](../twig/controller-rendering.md)

??? question "What happens if a child template that `extends` a parent prints markup outside of any block?"
    A **Twig error** — a template that extends another may only define blocks
    (`{% extends %}` must come first). Also, a template can `extends` exactly
    **one** parent but `use` many.
    **Ref:** [Template inheritance](../twig/inheritance.md)

??? question "What happens if you `{% set app = ... %}` in a template?"
    Your local variable **shadows the `app` global** for the rest of the template —
    `app.user`, `app.request`, etc. become whatever you set. Also remember
    `app.user` is `null` for unauthenticated requests and reading `app.session`
    *starts* the session.
    **Ref:** [Twig globals](../twig/globals.md)

## Forms

??? question "What happens if you call `isValid()` on a form that was never submitted?"
    A **`LogicException`** ("Cannot check if an unsubmitted form is valid") — not
    `false`. Always guard with `$form->isSubmitted() && $form->isValid()` after
    `handleRequest()`.
    **Ref:** [Form handling](../forms/handling.md)

??? question "What happens if `handleRequest()` receives a request whose HTTP method doesn't match the form's `method` option?"
    The request is **silently ignored** — the form simply stays unsubmitted, with
    no error to point you at the mismatch. Bonus: for PATCH, `clearMissing` is
    `false`, so fields absent from the payload keep their current value.
    **Ref:** [Form handling](../forms/handling.md)

??? question "What happens if you call `submit()` on a form that has already been submitted?"
    It throws an **`AlreadySubmittedException`** — a form can be submitted only
    once. The same applies to mutating a submitted form, e.g. `add()`ing a child
    after submission.
    **Ref:** [Symfony Forms — direct submit](https://symfony.com/doc/current/form/direct_submit.html)

??? question "What happens if you render fields manually and forget `form_rest()` (so no `_token` is printed)?"
    The next submission fails CSRF validation — a guaranteed **"invalid token"**
    error, because CSRF protection is on by default and the token is validated on
    **PRE_SUBMIT**. `form_end()` normally saves you by rendering leftover fields,
    unless you passed `render_rest: false`.
    **Ref:** [Forms & CSRF](../forms/csrf.md)

??? question "What happens if a data transformer's `reverseTransform()` throws a `TransformationFailedException`?"
    The form becomes **invalid** with the field's `invalid_message` — it is *not*
    a 500. Direction reminder: `transform()` is model → view (display);
    `reverseTransform()` is view → model (submit).
    **Ref:** [Data transformers](../forms/data-transformers.md)

??? question "What happens if a form listener tries to `add()` a field during `POST_SUBMIT`?"
    It fails — children cannot be added to a form that has already been submitted
    (an `AlreadySubmittedException`). Dynamic fields must be added in **PRE_SET_DATA
    or PRE_SUBMIT**, before binding; validation itself runs as a POST_SUBMIT
    listener.
    **Ref:** [Form events](../forms/events.md)

## Data Validation

??? question "What happens if a property has `#[Assert\Email]` and the value is `null` or an empty string?"
    It **passes** — `Email`, `Url` and most format constraints deliberately accept
    empty/null so they compose with optional fields. Rejecting empties is
    `NotBlank`'s job (and `NotBlank ≠ NotNull`: `''`, `[]`, `'   '` fail `NotBlank`
    but pass `NotNull`).
    **Ref:** [Built-in constraints](../validation/built-in-constraints.md)

??? question "What happens if you validate with a group that no constraint on the object belongs to?"
    **Zero violations** — the object appears valid because nothing ran. Passing a
    custom group does **not** implicitly include `Default`; list both
    (`['Default', 'registration']`) if you want both. Group names are
    case-sensitive.
    **Ref:** [Validation groups](../validation/groups.md)

??? question "What happens to a nested object's constraints if the parent property lacks `#[Assert\Valid]`?"
    They are **skipped entirely** — validation does not cascade by default, even
    if the nested class is covered in constraints. `Valid` is not a group and
    doesn't change groups; it only enables cascading.
    **Ref:** [Validation scopes](../validation/scopes.md)

??? question "What happens when the first group of a `GroupSequence` has a failing constraint?"
    All constraints **in that group** still run, then the sequence **stops** —
    later groups are never validated. And the sequence is triggered by validating
    `Default`; validating the `{ClassName}` group bypasses it with a flat run.
    **Ref:** [Group sequence](../validation/group-sequence.md)

??? question "What happens if a custom validator calls `buildViolation()` but never `addViolation()`?"
    **Nothing is recorded** — `buildViolation()` returns a builder and stays
    inert until `addViolation()` finalises it. Also remember `atPath()` *appends*
    to the current property path; it does not reset the root.
    **Ref:** [Violations builder](../validation/violations-builder.md)

## Dependency Injection

??? question "What happens if you call `$container->get()` with the id of a private service?"
    A **`ServiceNotFoundException`** — services are private by default since
    Symfony 4, and the compiled container doesn't expose them. Use constructor
    injection, a service locator, or the *test* container
    (`self::getContainer()`) in tests.
    **Ref:** [The container](../dependency-injection/container.md)

??? question "What happens if autowiring finds two services implementing the type-hinted interface?"
    A **compile-time ambiguity error** — never a silent pick. Fix it with a
    default alias, a named autowiring alias (whose id is literally
    `Type $paramName`, so the parameter name must match), or `#[Target]`.
    **Ref:** [Autowiring](../dependency-injection/autowiring.md)

??? question "What happens if a service constructor type-hints `string $apiKey` with autowiring on?"
    A **compile error** — autowiring resolves *objects by type* and can never
    guess scalars. Provide the value via `bind`, `#[Autowire]`, or an explicit
    argument. And `%env(MAX)%` stays a **string** until you add the `int:`
    processor.
    **Ref:** [Parameters](../dependency-injection/parameters.md)

??? question "What happens if service A's constructor needs B and B's constructor needs A?"
    The container throws a **`ServiceCircularReferenceException`** — constructor
    cycles cannot be instantiated. Break the cycle by making one side `lazy` (a
    proxy defers instantiation), injecting a service locator, or switching one
    edge to setter injection.
    **Ref:** [Lazy services](https://symfony.com/doc/current/service_container/lazy_services.html)

??? question "What happens if you tag a service with a custom tag and nothing else?"
    **Nothing** — a tag is inert metadata until a consumer (a `tagged_iterator`/
    `tagged_locator` argument or a compiler pass) collects it. Higher tag
    `priority` means earlier in the iterator.
    **Ref:** [Tags](../dependency-injection/tags.md)

??? question "What happens to the original service when another service decorates it?"
    It is **renamed** and becomes available as the special `.inner` reference,
    while the decorator **takes over the original id** — consumers are unaware.
    With multiple decorators, higher `decoration_priority` is applied first,
    i.e. ends up *closest to the original*.
    **Ref:** [Decoration](../dependency-injection/decoration.md)

## Security

??? question "What happens if you call `getUser()` in a controller on a route with no authenticated user?"
    It returns **`null`** — no exception. Same in Twig: `app.user` is `null` for
    anonymous requests, so guard before dereferencing. Forcing authentication is
    `access_control`/`#[IsGranted]`'s job, not `getUser()`'s.
    **Ref:** [Users](../security/users.md)

??? question "What happens if every voter abstains on an `isGranted()` check?"
    Access is **denied** — unless `allow_if_all_abstain: true` is configured.
    Under the default `affirmative` strategy one grant suffices, but zero grants
    with all abstentions falls back to deny; and a `Voter::supports()` returning
    `false` counts as abstain, not deny.
    **Ref:** [Voters](../security/voters.md)

??? question "What happens when an `AccessDeniedException` is thrown for a user who isn't authenticated at all?"
    The firewall's **entry point** kicks in (e.g. redirect to the login form) —
    not a raw 403. The 403 is reserved for users who *are* authenticated but lack
    permission.
    **Ref:** [Authorization](../security/authorization.md)

??? question "What happens if you check `isGranted('ADMIN')` — without the `ROLE_` prefix — against a user who has `ROLE_ADMIN`?"
    **Denied.** `RoleVoter` silently ignores attributes lacking the `ROLE_`
    prefix (it abstains), and with nothing granting, the decision falls through
    to deny. `IS_AUTHENTICATED_*` and `PUBLIC_ACCESS` are handled by the separate
    `AuthenticatedVoter`, not `RoleVoter`.
    **Ref:** [Roles](../security/roles.md)

??? question "What happens to a request whose URL matches no `access_control` rule?"
    Access is **allowed** — no matching rule means no restriction, not an implicit
    deny. Rules are evaluated top-to-bottom and only the **first match** applies,
    so ordering (and a final catch-all, if you want deny-by-default) matters.
    **Ref:** [Access control](../security/access-control.md)

??? question "What happens on the next request if your user class's `isEqualTo()` returns `false` during refresh?"
    The token is **invalidated** — a silent logout. `refreshUser()` runs on
    **every stateful request** (never on `stateless: true` firewalls), and the
    equality check is how Symfony decides whether the session user is still the
    same user.
    **Ref:** [User providers](../security/providers.md)

## HTTP Caching

??? question "What happens if you send a response without setting any `Cache-Control` header?"
    Symfony gives it **`Cache-Control: no-cache, private`** — safe by default, but
    invisible to shared caches. You must opt in with `setPublic()` +
    `setMaxAge()`/`setSharedMaxAge()` to make it cacheable.
    **Ref:** [Cache types](../http-caching/cache-types.md)

??? question "What happens if you call `setPublic()` and later `setPrivate()` on the same response?"
    The **last call wins** and removes the other directive — you can never end up
    with `public, private` together. Related nuance: `setSharedMaxAge()` also
    marks the response `public` for you.
    **Ref:** [Expiration](../http-caching/expiration.md)

??? question "What happens when `isNotModified($request)` finds the client's validators still match?"
    It **mutates the response in place**: status becomes **304**, the body and
    content headers are stripped — and it returns `bool`, so you still must
    `return $response` yourself.
    **Ref:** [Validation](../http-caching/validation.md)

??? question "What happens if a conditional request carries both `If-None-Match` and `If-Modified-Since`?"
    The **ETag takes precedence** — a matching `Last-Modified` alone is ignored if
    the ETag differs. Also, `#[Cache]` ETag expressions are SHA-256 hashed; the
    raw expression value is never the ETag.
    **Ref:** [Validation](../http-caching/validation.md)

??? question "What happens when a request with a session cookie reaches Symfony's `HttpCache`?"
    It **bypasses the shared cache** — `Cookie` and `Authorization` are the
    default `private_headers`, so such requests are treated as private and go to
    the backend. This is why one session cookie can quietly kill your hit rate.
    **Ref:** [Server-side caching (HttpCache)](../http-caching/server-side.md)

??? question "What happens to a fully-cacheable page that embeds one short-lived fragment *without* ESI?"
    The **whole page's TTL is capped** by the shortest-lived embedded fragment —
    `ResponseCacheStrategy` merges them down. ESI is the fix: each fragment keeps
    its own TTL because the surrogate assembles the page itself.
    **Ref:** [ESI](../http-caching/esi.md)

## Console

??? question "What happens to the exit code when a failing command is run with `-q`?"
    Nothing — `-q` only suppresses output; the command still runs and **returns
    its real exit code**, so CI failure detection keeps working. Verbosity lives
    on the *output* object (constants 16/32/64/128/256).
    **Ref:** [Verbosity](../console/verbosity.md)

??? question "What happens if `execute()` returns nothing?"
    An error — in Symfony 8, `execute()` **must return an `int`**
    (`Command::SUCCESS` = 0, `FAILURE` = 1, `INVALID` = 2); returning `null`/void
    violates the return type. Invokable `#[AsCommand]` classes don't extend
    `Command` but still use its constants.
    **Ref:** [Custom commands](../console/custom-commands.md)

??? question "What happens if a command returns an exit code greater than 255?"
    It **wraps modulo 256** — exit codes are clamped to the 0–255 range, so
    returning 256 looks like success (0) to the shell. Also: `console.terminate`
    fires even after an error, and `disableCommand()` yields code **113**.
    **Ref:** [Console events](../console/events.md)

??? question "What happens to `interact()` when a command runs with `--no-interaction`?"
    It is **skipped entirely** — `interact()` only runs for interactive input, and
    missing required arguments then fail validation instead of being asked for.
    Lifecycle order: `configure` → `initialize` → `interact` → validation →
    `execute`.
    **Ref:** [Command lifecycle](../console/configuration.md)

??? question "What happens if you give an `InputOption::VALUE_NONE` option a default value?"
    A **`LogicException`** — a `VALUE_NONE` option is a pure flag (presence =
    `true`) and cannot carry a default or a value. Mode constants: `VALUE_NONE` 1,
    `VALUE_REQUIRED` 2, `VALUE_OPTIONAL` 4, `VALUE_IS_ARRAY` 8, `VALUE_NEGATABLE` 16.
    **Ref:** [Options & arguments](../console/options-arguments.md)

## Automated Tests

??? question "What happens if a test calls `createClient()` twice?"
    The second call **throws** — one client per test (booting a second kernel
    would clash). If you need multiple "browsers", reuse the client or use
    separate test methods.
    **Ref:** [Functional tests](../testing/functional-tests.md)

??? question "What happens after the client receives a 302 — does the next assertion see the target page?"
    No — the test client does **not follow redirects by default**. You assert the
    redirect (`assertResponseRedirects()`), then call `$client->followRedirect()`
    explicitly (or enable `followRedirects()` up front).
    **Ref:** [The test client](../testing/client.md)

??? question "What happens to a service you replaced with `$container->set()` when the test makes a second request?"
    It is **lost** — the kernel reboots between requests and rebuilds the
    container, discarding your replacement. Pair the replacement with
    `$client->disableReboot()` to keep it alive across requests.
    **Ref:** [Framework objects in tests](../testing/framework-objects.md)

??? question "What happens if you call `getProfile()` without having called `enableProfiler()` before the request?"
    It returns **`false`** (not `null`, not an exception) — in the `test`
    environment `profiler.collect` is off by default, so profiles exist only for
    requests that opted in beforehand.
    **Ref:** [Profiler in tests](../testing/profiler.md)

??? question "What happens if you call `text()` on a Crawler whose filter matched zero nodes?"
    It **throws** — `text()`/`attr()` operate on the first node and error on an
    empty set unless you pass a default argument. The Crawler is immutable:
    `filter()` returns a new instance, and CSS filtering needs the css-selector
    component.
    **Ref:** [The Crawler](../testing/crawler.md)

## Miscellaneous

??? question "What happens to the callback passed to `CacheInterface::get()` when the item is already cached?"
    It is **never executed** — the callback runs only on a miss, and its return
    value is what gets cached. Stampede protection comes free via probabilistic
    early expiration (`$beta`; `INF` forces recomputation).
    **Ref:** [Cache](../miscellaneous/cache.md)

??? question "What happens when you translate a message id that has no translation in the current locale?"
    The **message id itself is returned** — no exception, no warning in the
    output. The default domain is `messages` (`validators`/`security` are
    separate), and Symfony 8 uses ICU MessageFormat for plurals.
    **Ref:** [Translations & Intl](../miscellaneous/intl.md)

??? question "What happens if a `Process` started with `run()` takes longer than 60 seconds?"
    It is killed with a **`ProcessTimedOutException`** — the default timeout is
    60 s; pass `null` to disable it. Also: array arguments are auto-escaped, but
    `fromShellCommandline()` is not (injection risk), and `mustRun()` throws on
    failure where `run()` returns the exit code.
    **Ref:** [Process](../miscellaneous/process.md)

??? question "What happens to `.env.local` when the app runs in the `test` environment?"
    It is **ignored** — tests must be reproducible, so machine-local overrides
    don't apply (use `.env.test`/`.env.test.local`). Also: real OS env vars always
    beat `.env*` values, and if `.env.local.php` exists the `.env*` files aren't
    parsed at all.
    **Ref:** [Configuration & environments](../miscellaneous/configuration.md)

??? question "What happens if you call `$lock->acquire()` while another process holds the lock?"
    It returns **`false` immediately** — `acquire()` is non-blocking by default;
    pass `true` to block. Locks also carry a TTL (default 300 s), so long jobs
    must `refresh()`, and `FlockStore`/`SemaphoreStore` protect a single machine
    only.
    **Ref:** [Lock](../miscellaneous/lock.md)

## Official References

- [Symfony documentation home](https://symfony.com/doc/current/)
- [Routing](https://symfony.com/doc/current/routing.html) · [Controllers](https://symfony.com/doc/current/controller.html) · [Forms](https://symfony.com/doc/current/forms.html) · [Validation](https://symfony.com/doc/current/validation.html)
- [Service container](https://symfony.com/doc/current/service_container.html) · [Security](https://symfony.com/doc/current/security.html) · [HTTP cache](https://symfony.com/doc/current/http_cache.html)
- [Console](https://symfony.com/doc/current/console.html) · [Testing](https://symfony.com/doc/current/testing.html) · [Twig](https://twig.symfony.com/doc/3.x/)
- [PHP manual](https://www.php.net/manual/en/) · [Certification syllabus](https://certification.symfony.com/exams/symfony.html)

---

<small>Related: [Top Certification Traps](traps.md) · [Easily Confused](confusions.md) · [Revision Hub](index.md)</small>
