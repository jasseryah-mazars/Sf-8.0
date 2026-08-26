# Mock Exam A (Exam Mode)

!!! note "Three independent papers"
    This is **Mock A**. Also try: [Mock B](mock-exam-b.md) · [Mock C](mock-exam-c.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** Which response header ensures a shared cache stores one entry per representation? (choose one)  <small>_(HTTP)_</small>

- A. Vary
- B. Content-Type
- C. Cache-Control: private
- D. Accept

??? success "Answer Q1"
    **A**

    Vary lists the request headers that change the response, so caches key each variant separately.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

**Q2.** Consider: $response->setEtag(sha1($post->getContent())); if ($response->isNotModified($request)) { return $response; } return $this->render('post.html.twig', ['post' => $post], $response); — what is the benefit when If-None-Match matches?  <small>_(HTTP Caching)_</small>

- A. A bodyless 304 is returned and the template is never rendered
- B. The template is rendered, then discarded, and a 304 is sent
- C. A 200 with the full body is always returned
- D. The response is sent twice

??? success "Answer Q2"
    **A**

    isNotModified() sets 304 and strips the body when the ETag matches, and the early return short-circuits before render() runs — so no template work happens at all. If you called render() first you would lose that saving. It never sends twice; you return the response once.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

**Q3.** Which methods does UserInterface declare in Symfony 8?  <small>_(Security)_</small>

- A. getRoles() and getUserIdentifier()
- B. getUsername() and getRoles()
- C. getRoles(), getUserIdentifier() and eraseCredentials()
- D. getId() and getPassword()

??? success "Answer Q3"
    **A**

    Symfony 8 trimmed UserInterface to two methods; eraseCredentials() and getUsername() were removed.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

**Q4.** Which of these are valid top-level keys under security: in Symfony 8? (choose 4)  <small>_(Security)_</small>

- A. providers
- B. firewalls
- C. access_control
- D. role_hierarchy
- E. enable_authenticator_manager

??? success "Answer Q4"
    **A, B, C, D**

    providers, firewalls, access_control, password_hashers and role_hierarchy are the core keys of security.yaml. enable_authenticator_manager was removed in Symfony 8 — the authenticator system is the only one — so it is not a valid key anymore.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/configuration/security.html)

**Q5.** On submit, which transformers run first?  <small>_(Forms)_</small>

- A. View transformers (view->norm), then model transformers (norm->model)
- B. Model transformers, then view transformers
- C. Only model transformers run on submit
- D. Order is undefined

??? success "Answer Q5"
    **A**

    On submission data flows view -> norm -> model, so view transformers' reverseTransform runs before model transformers' reverseTransform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

**Q6.** Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?  <small>_(Miscellaneous)_</small>

- A. null is returned as a cache hit; the callback is NOT run again
- B. The callback runs again because null means a miss
- C. A CacheException is thrown for storing null
- D. The item is deleted automatically

??? success "Answer Q6"
    **A**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q7.** For the router, which statement about id, class and autowiring alias is correct?  <small>_(Dependency Injection)_</small>

- A. The id is 'router', the class is a concrete Router, and an Alias maps RouterInterface to the id
- B. The id, class and alias are all the string 'router'
- C. The autowiring alias is the class FQCN pointing at the interface
- D. There is no alias; autowiring matches the id string directly

??? success "Answer Q7"
    **A**

    These are three distinct keys. FrameworkExtension registers the service under the id 'router' with a concrete class, then adds an autowiring alias from the interface FQCN (RouterInterface) to that id so type-hints resolve. debug:autowiring lists those aliases; debug:container inspects the id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

**Q8.** An admin deletes a user's account while that user is browsing under a stateful firewall. What happens on the user's next request?  <small>_(Security)_</small>

- A. refreshUser() can no longer load them and throws; the ContextListener discards the token, effectively logging them out
- B. Nothing changes until the PHP session cookie expires
- C. A fatal 500 error is returned on every request
- D. The user keeps full access until they click logout

??? success "Answer Q8"
    **A**

    On each stateful request the ContextListener calls refreshUser() to re-sync the session user. A now-missing account makes refreshUser() throw (UserNotFoundException / UnsupportedUserException), so the ContextListener treats the user as unloadable, discards the token and clears storage — an immediate, clean logout. It is not a fatal error, and access does not persist until the cookie expires precisely because the user is re-checked every request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

**Q9.** How does AbstractController obtain its helper services?  <small>_(Controllers)_</small>

- A. Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()
- B. Through constructor injection of each service
- C. The full application container is injected

??? success "Answer Q9"
    **A**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q10.** Which Finder method defines the directories to search?  <small>_(Miscellaneous)_</small>

- A. in()
- B. from()
- C. search()
- D. path()

??? success "Answer Q10"
    **A**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

**Q11.** With {% include '_card.html.twig' with { title: t } only %}, is the app global still available inside the partial?  <small>_(Twig)_</small>

- A. Yes — only isolates the parent's local variables but globals like app remain available
- B. No — only removes everything including globals
- C. Only if you also pass app in the with hash
- D. Globals are never available inside an include

??? success "Answer Q11"
    **A**

    only restricts the include to just the with variables from the caller's local scope, but Twig globals (such as app) are merged into every template's context independently, so app.user etc. still work. Assuming only strips globals is a common misconception.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q12.** What does the `only` keyword do on an include?  <small>_(Twig)_</small>

- A. Restricts the included template's scope to just the `with` variables
- B. Includes the template only once
- C. Makes the variables read-only
- D. Ignores a missing template

??? success "Answer Q12"
    **A**

    By default an include inherits the parent context; adding `only` isolates it so it sees only the variables passed via `with` (plus the app global).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q13.** A command's execute() throws a RuntimeException. What is the event sequence?  <small>_(Console)_</small>

- A. COMMAND → ERROR → TERMINATE (TERMINATE still runs after ERROR)
- B. COMMAND → TERMINATE only (ERROR is skipped for RuntimeException)
- C. ERROR → COMMAND → TERMINATE
- D. ERROR only; the process aborts before TERMINATE

??? success "Answer Q13"
    **A**

    COMMAND fires before execution; the thrown Throwable triggers ERROR (ConsoleErrorEvent, where a listener can change the exit code or swap the exception); TERMINATE always fires last, even after an error. ERROR never runs before COMMAND, and it does not suppress TERMINATE.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

**Q14.** For a form's _method field to influence which route matches, you must…  <small>_(Routing)_</small>

- A. Call Request::enableHttpMethodParameterOverride()
- B. Add methods: ['_method']
- C. Do nothing — it is enabled by default
- D. Set framework.http_method_override: false

??? success "Answer Q14"
    **A**

    Method override is opt-in; once enabled, getMethod() returns the overridden verb that the matcher uses. It is not on by default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q15.** A command returns 300 as its exit code. What does the process actually exit with?  <small>_(Console)_</small>

- A. 44 — exit codes are clamped to 0–255 via % 256 (300 % 256 = 44)
- B. 300 — Symfony passes it through unchanged
- C. 255 — anything above 255 becomes 255
- D. 1 — out-of-range codes fall back to FAILURE

??? success "Answer Q15"
    **A**

    POSIX exit codes are a single byte (0–255), so Symfony normalises out-of-range values with % 256; 300 % 256 = 44. It is not passed through, not capped at 255, and not coerced to FAILURE. By convention a signal-terminated process exits with 128 + signalNumber.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

**Q16.** Which snippet builds a 'next page' link for the current route, incrementing page?  <small>_(Twig)_</small>

- A. path(app.current_route, app.current_route_parameters|merge({ page: page + 1 }))
- B. path(app.request.uri, { page: page + 1 })
- C. url(app.route, { page: page + 1 })
- D. path('current', app.params + { page: page + 1 })

??? success "Answer Q16"
    **A**

    app.current_route and app.current_route_parameters expose the active route and its params; merging a new page value onto them and passing to path() rebuilds the current URL with one changed parameter. app.route/app.params are not real members, and + does not merge hashes (~ /merge do).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

**Q17.** What does autoconfigure: true do (as opposed to autowire)?  <small>_(Dependency Injection)_</small>

- A. Applies tags/flags based on implemented interfaces and attributes
- B. Fills constructor arguments by type
- C. Makes all services public
- D. Clears the compiled cache

??? success "Answer Q17"
    **A**

    Autoconfigure adds tags automatically (e.g. event subscriber); autowire is the separate flag that fills arguments by type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html#the-autoconfigure-option)

**Q18.** A kernel.exception listener inspects getThrowable() and builds a JsonResponse, but the custom page never appears. What is the most likely bug?  <small>_(Architecture)_</small>

- A. The listener forgot to call $event->setResponse() on its branch, so the event's response stays null and the default handler wins
- B. The listener has priority -128, which is impossible to register
- C. kernel.exception cannot produce JSON responses, only HTML

??? success "Answer Q18"
    **A**

    ExceptionEvent::getResponse() returns null until some listener calls setResponse(). Reading getThrowable() and constructing a response is not enough — you must actually set it on the event. If a branch forgets setResponse(), the response stays null, ErrorListener's default page (or a 500) is used instead, and your custom page never shows.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q19.** What happens at runtime when `Suit::from('Z')` is called and 'Z' is not a valid backing value?  <small>_(PHP & Web Security)_</small>

- A. It throws \ValueError
- B. It returns null
- C. It returns the first case
- D. It emits a warning and returns false

??? success "Answer Q19"
    **A**

    from() is the strict lookup: an unknown value throws \\ValueError. That is the mirror image of tryFrom(), which returns null. It never falls back to the first case nor warns-and-returns-false. Best practice: wrap from() in try/catch for untrusted input, or use tryFrom(). Misconception: assuming from() degrades gracefully like tryFrom() — it deliberately fails loud.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.enumerations.backed.php)

**Q20.** When does the Firewall listener run in the kernel lifecycle?  <small>_(Security)_</small>

- A. On kernel.request at priority 8 (after routing), it asks the FirewallMap for the first matching FirewallContext
- B. On kernel.controller, just before the controller is resolved
- C. On kernel.response, after the action has run
- D. On kernel.terminate, asynchronously after the response
- E. On kernel.request but before routing, at the highest priority

??? success "Answer Q20"
    **A**

    The Firewall listener subscribes to kernel.request at priority 8, which runs after the RouterListener (routing), then queries the FirewallMap for the matching FirewallContext and runs its listeners. It is a request-phase concern, not controller/response/terminate, and it deliberately runs after routing so route attributes are available.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall.php)

**Q21.** Which type is out of scope here because it belongs to the Doctrine bridge?  <small>_(Forms)_</small>

- A. EntityType
- B. ChoiceType
- C. MoneyType
- D. CollectionType

??? success "Answer Q21"
    **A**

    EntityType lives in the Doctrine bridge and is out of scope. Use ChoiceType with explicit choices for the non-Doctrine equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/choice.html)

**Q22.** When is %env(DATABASE_URL)% resolved?  <small>_(Dependency Injection)_</small>

- A. At runtime, via an env-var processor
- B. At compilation, frozen into the cache
- C. When .env is parsed at deploy time only
- D. Never; it is a literal string

??? success "Answer Q22"
    **A**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

**Q23.** Two passes are registered in the same phase with priorities 10 and 100. Which runs first?  <small>_(Dependency Injection)_</small>

- A. The priority-100 pass — higher priority runs earlier within a phase
- B. The priority-10 pass runs first
- C. The order is undefined
- D. They run simultaneously

??? success "Answer Q23"
    **A**

    Within a phase, addCompilerPass orders by priority with higher running first. The trap is assuming lower numbers run first (as some other Symfony orderings work); for compiler passes higher priority is earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

**Q24.** During matching, when is the host constraint checked?  <small>_(Routing)_</small>

- A. Before the path regex
- B. After the controller runs
- C. Only during URL generation
- D. Never; host is informational

??? success "Answer Q24"
    **A**

    matchCollection() tests the compiled host regex against RequestContext::getHost() first; only if it matches does it test the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#sub-domain-routing)

**Q25.** Which command rebuilds the compiled router after editing routes in prod?  <small>_(Routing)_</small>

- A. php bin/console cache:clear --env=prod
- B. php bin/console router:reload --env=prod
- C. php bin/console debug:router --refresh
- D. php bin/console routes:compile

??? success "Answer Q25"
    **A**

    cache:clear (or cache:warmup) in the prod env runs the RouterCacheWarmer and regenerates url_matching_routes.php / url_generating_routes.php. The other commands do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#debugging-routes)

**Q26.** How is an included template handled by Twig internally?  <small>_(Twig)_</small>

- A. It is a separate compiled class, loaded via the loader and invoked at runtime — not textually inlined
- B. Its source is pasted into the parent before compilation
- C. It is re-parsed from disk on every render with no caching
- D. It is merged into the parent's single block table

??? success "Answer Q26"
    **A**

    The include tag compiles to a call to Twig\Template::display()/render() on the sub-template, which the FilesystemLoader resolves and which is compiled and cached like any other template. Includes are separate compiled classes invoked at runtime, not inlined text.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Loader/FilesystemLoader.php)

**Q27.** Given AcceptHeader::fromString('text/html;q=0.9, application/json;q=1.0'), what does $accept->first()?->getQuality() return? (choose one)  <small>_(HTTP)_</small>

- A. 1.0 — first() returns the highest-quality item (application/json)
- B. 0.9 — items are returned in string order
- C. null — first() only works on a single-value header
- D. true — first() returns a boolean like has()

??? success "Answer Q27"
    **A**

    AcceptHeader parses and sorts items by quality (descending), so first() returns the AcceptHeaderItem for application/json (q=1.0) and getQuality() gives 1.0. The nullsafe operator guards the empty-header case where first() would return null.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/AcceptHeader.php)

**Q28.** A user uploads a file larger than `post_max_size` and the action crashes on a null `$request->files->get('avatar')`. What is the underlying cause?  <small>_(Controllers)_</small>

- A. Exceeding post_max_size can yield an empty files bag (no exception), so the get() returns null — always null-check
- B. move() threw a FileException that was swallowed
- C. getMimeType() returns null for large files
- D. Symfony automatically rejects the request with a 413

??? success "Answer Q28"
    **A**

    When post_max_size is exceeded, PHP may discard the POST data, leaving an empty files bag rather than raising an exception. Guard the result with an instanceof UploadedFile / isValid() check before using it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

**Q29.** What is the literal id of a named autowiring alias, e.g. for a Monolog channel logger?  <small>_(Dependency Injection)_</small>

- A. Literally 'Psr\Log\LoggerInterface $requestLogger' — matched by the parameter name
- B. requestLogger
- C. logger.requestLogger
- D. @requestLogger

??? success "Answer Q29"
    **A**

    A named autowiring alias id is the full type followed by the variable name, 'Type $paramName'. Autowiring matches it when your constructor parameter is named identically — which is fragile, so #[Target('requestLogger')] states the intent explicitly and survives parameter renames.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

**Q30.** A legacy suite emits hundreds of known deprecations, but you want CI to fail only on NEW ones. What do you do?  <small>_(Testing)_</small>

- A. Generate a baseline (baselineFile=...&generateBaseline=true), commit it, then run with baselineFile=... so only new deprecations fail
- B. Set disabled=1 permanently so nothing is reported
- C. Add #[IgnoreDeprecations] to every test in the suite
- D. Set weak so the build never turns red

??? success "Answer Q30"
    **A**

    A baseline records currently-known deprecations to a JSON file that later runs ignore, so only new deprecations fail the build — and you shrink it over time. disabled=1 and weak both remove the safety net for new deprecations, and blanket #[IgnoreDeprecations] hides everything, including regressions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#making-tests-fail)

**Q31.** Which of these are real WebTestCase assertion helpers? (choose 3)  <small>_(Testing)_</small>

- A. assertResponseStatusCodeSame(int $code)
- B. assertRouteSame(string $route)
- C. assertResponseHasCookie(string $name)
- D. assertResponseBodyEquals(string $body)
- E. assertControllerSame(string $fqcn)

??? success "Answer Q31"
    **A, B, C**

    assertResponseStatusCodeSame, assertRouteSame and assertResponseHasCookie all exist in the BrowserKit/WebTest assertion traits. There is no assertResponseBodyEquals (use getResponse()->getContent() with a PHPUnit string assertion) nor assertControllerSame helper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

**Q32.** In configureOptions(), which OptionsResolver call derives one option's value from the values of others?  <small>_(Forms)_</small>

- A. setNormalizer('opt', fn (Options $o, $value) => ...)
- B. setAllowedTypes('opt', 'string')
- C. setRequired('opt')
- D. setDefault('opt', fn () => ...) only

??? success "Answer Q32"
    **A**

    setNormalizer() receives the resolved Options plus the raw value, letting one option depend on others (e.g. force expanded when multiple is false). setAllowedTypes validates a type, setRequired marks an option mandatory, and a default closure cannot read sibling options the way a normalizer can.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/options_resolver.html)

**Q33.** When must $client->enableProfiler() be called?  <small>_(Testing)_</small>

- A. Before the request whose profile you want to read
- B. After the request, before getProfile()
- C. Only inside setUp()
- D. Never — profiling is always on in the test environment

??? success "Answer Q33"
    **A**

    enableProfiler() opts the next request into profiling; calling it after the request collects nothing and getProfile() returns false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

**Q34.** How does RouteCompiler represent /blog/{page<\d+>} in the CompiledRoute regex?  <small>_(Routing)_</small>

- A. As a named capture group, e.g. #^/blog/(?P<page>\d+)$#sD
- B. As an unnamed group #^/blog/(\d+)$#
- C. As two separate regexes joined at runtime
- D. It is not compiled; the requirement is checked in the controller

??? success "Answer Q34"
    **A**

    RouteCompiler::compile() extracts each {name} token and substitutes it with a named capture group using its requirement (or [^/]+ by default), producing a single anchored regex. Named groups are how the matcher maps captured values back to parameter names.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/RouteCompiler.php)

**Q35.** How does the argument `array $context` in the index.php closure get populated?  <small>_(Miscellaneous)_</small>

- A. The runtime's resolver autowires it from $_SERVER (env vars like APP_ENV/APP_DEBUG)
- B. You must call getenv() yourself inside the closure
- C. Symfony injects it from services.yaml parameters
- D. It is always an empty array in Symfony 8

??? success "Answer Q35"
    **A**

    RuntimeInterface::getResolver() builds a resolver that inspects the callable's typed arguments and supplies them — array $context comes from $_SERVER (env), and it can also inject Request, InputInterface, etc. You therefore never read $_SERVER manually in the entry point.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

**Q36.** What is the default phase for a compiler pass registered without one?  <small>_(Dependency Injection)_</small>

- A. TYPE_BEFORE_OPTIMIZATION
- B. TYPE_OPTIMIZE
- C. TYPE_REMOVE
- D. TYPE_AFTER_REMOVING

??? success "Answer Q36"
    **A**

    PassConfig runs passes in phase order; unspecified passes run in the before-optimization phase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

**Q37.** Which default group name does an unqualified constraint belong to?  <small>_(Validation)_</small>

- A. Default (capital D)
- B. default (lowercase)
- C. the fully qualified class name
- D. Base

??? success "Answer Q37"
    **A**

    The implicit group is 'Default' with a capital D; group names are case-sensitive, so 'default' would be a different (empty) group.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

**Q38.** During a successful login, in which order does the AuthenticatorManager dispatch these events?  <small>_(Security)_</small>

- A. CheckPassportEvent → AuthenticationTokenCreatedEvent → LoginSuccessEvent
- B. LoginSuccessEvent → CheckPassportEvent → AuthenticationTokenCreatedEvent
- C. AuthenticationTokenCreatedEvent → CheckPassportEvent → LoginSuccessEvent
- D. CheckPassportEvent → LoginSuccessEvent → AuthenticationTokenCreatedEvent

??? success "Answer Q38"
    **A**

    authenticate() builds the Passport; CheckPassportEvent listeners then resolve the badges; createToken() runs; AuthenticationTokenCreatedEvent is the last chance to swap/decorate the token; the token is stored; finally LoginSuccessEvent fires (invoking onAuthenticationSuccess()). On error a LoginFailureEvent is dispatched instead. Any ordering that runs LoginSuccessEvent before the passport is checked, or creates the token before CheckPassportEvent, contradicts the manager's pipeline.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Authentication/AuthenticatorManager.php)

**Q39.** Where are bundles enabled in a modern Symfony app?  <small>_(Architecture)_</small>

- A. config/bundles.php
- B. config/services.yaml
- C. Manually in src/Kernel.php

??? success "Answer Q39"
    **A**

    config/bundles.php maps each bundle class to the environments where it is enabled; the kernel reads it via MicroKernelTrait.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q40.** Which PSRs does Symfony IMPLEMENT (i.e. Symfony objects ARE valid PSR objects)? (choose all that apply)  <small>_(Architecture)_</small>

- A. PSR-6 (Cache pool)
- B. PSR-11 (Container)
- C. PSR-14 (Event Dispatcher)
- D. PSR-20 (Clock)
- E. PSR-3 (Logger)

??? success "Answer Q40"
    **A, B, C, D**

    Symfony implements PSR-6 (Cache pool), PSR-11 (Container), PSR-14 (EventDispatcher), PSR-16 (Simple Cache adapter) and PSR-20 (Clock) — its objects can be handed to any library expecting those interfaces. PSR-3 (Logger) is CONSUMED: Symfony type-hints LoggerInterface so you inject any implementation, but it does not ship the logger itself.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

**Q41.** For each firewall, what does SecurityExtension compile at container build time?  <small>_(Security)_</small>

- A. A FirewallContext bundling its listeners, the authenticator list, an AuthenticatorManager, and (unless stateless) a ContextListener — all indexed in a FirewallMap
- B. A single global Firewall service shared unchanged by every firewall
- C. One controller per firewall generated from the config
- D. Nothing at build time — firewalls are assembled lazily on the first request

??? success "Answer Q41"
    **A**

    SecurityExtension reads the security.yaml tree and, per firewall, compiles a dedicated FirewallContext (its listeners, the list of authenticators, an AuthenticatorManager, an exception listener, and a ContextListener unless the firewall is stateless). All contexts are registered in the FirewallMap; at runtime the single Firewall listener asks the map which context matches. The work happens at compile time, not lazily per request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/SecurityBundle/DependencyInjection/SecurityExtension.php)

**Q42.** What is the difference between PSR-6 and PSR-16 in Symfony's Cache?  <small>_(Architecture)_</small>

- A. PSR-6 is the pool/CacheItem model (CacheItemPoolInterface); PSR-16 is the simpler get/set SimpleCache API (Psr16Cache adapter)
- B. PSR-6 is for HTTP caching and PSR-16 is for the container
- C. They are the same interface at different versions

??? success "Answer Q42"
    **A**

    PSR-6 models caching as a pool of CacheItem objects (CacheItemPoolInterface::getItem()/save()); PSR-16 (Simple Cache) is a lighter get()/set()/delete() API, exposed by Symfony's Psr16Cache adapter. Confusing the pool/item model (PSR-6) with the simple key/value API (PSR-16) is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

**Q43.** You add the alias App\Report\ReporterInterface: '@App\Report\Missing' but the target service does not exist. What happens?  <small>_(Dependency Injection)_</small>

- A. A compile-time error — an alias to a non-existent target breaks the build; it is not a silent null
- B. The interface silently resolves to null at runtime
- C. The alias is quietly ignored
- D. A ServiceLocator is injected in its place

??? success "Answer Q43"
    **A**

    An alias must point at an existing service id; a dangling alias fails the container build. Optional dependencies use nullable constructor args or NULL_ON_INVALID_REFERENCE, not a broken alias. The misconception is expecting a missing target to become null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/alias_private.html)

**Q44.** What does #[AutowireIterator('app.handler')] on an iterable $handlers argument inject?  <small>_(Dependency Injection)_</small>

- A. An iterable of all app.handler-tagged services, ordered by descending priority
- B. A ServiceLocator keyed by name
- C. Only the single highest-priority handler
- D. An array of the tag's attribute sets

??? success "Answer Q44"
    **A**

    #[AutowireIterator] is the attribute form of tagged_iterator: it injects an iterable of the instantiated tagged services, ordered by descending priority. #[AutowireLocator] would give the lazy keyed locator; the attribute does not filter down to one service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

**Q45.** During a forwarded sub-request, what does Request::isMainRequest() return?  <small>_(Controllers)_</small>

- A. false
- B. true
- C. null

??? success "Answer Q45"
    **A**

    The sub-request is dispatched with HttpKernelInterface::SUB_REQUEST, so isMainRequest() is false and some listeners (e.g. the firewall) skip.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q46.** Which adapter keeps entries only for the current process (ideal for tests)?  <small>_(Miscellaneous)_</small>

- A. ArrayAdapter
- B. FilesystemAdapter
- C. RedisAdapter
- D. ApcuAdapter

??? success "Answer Q46"
    **A**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

**Q47.** For a mapped CollectionType to call the parent's adder/remover methods, set…  <small>_(Forms)_</small>

- A. by_reference => false
- B. allow_add => false
- C. prototype => false
- D. mapped => false

??? success "Answer Q47"
    **A**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/collection.html)

**Q48.** What does the __Host- cookie name prefix force the browser to require? (choose one)  <small>_(HTTP)_</small>

- A. Secure, no Domain attribute, and Path=/ — the strictest scoping the browser enforces
- B. HttpOnly and SameSite=Strict only
- C. A matching Domain attribute and Max-Age
- D. Nothing; the prefix is purely cosmetic

??? success "Answer Q48"
    **A**

    A cookie named __Host-... is accepted only if it is Secure, has no Domain attribute (so it is locked to the exact host), and uses Path=/. This is the strongest same-origin scoping the browser guarantees, preventing subdomain injection. The related __Secure- prefix only requires the Secure flag.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#cookie_prefixes)

**Q49.** $envelope->last(HandledStamp::class) returns null. Which situation explains this best?  <small>_(Miscellaneous)_</small>

- A. The message was routed to an async transport, so it has not been handled in this process yet
- B. The handler returned null, so no HandledStamp was created
- C. dispatch() failed and returned null instead of an Envelope
- D. HandledStamp only exists on the query bus

??? success "Answer Q49"
    **A**

    A handler that returns null still produces a HandledStamp (its result is null) — so last() returning null means no such stamp exists, i.e. the message was sent async and not handled here. dispatch() always returns an Envelope (never null), and HandledStamp is not query-bus-specific. This is why the nullsafe ?-> guards 'not handled here', distinct from 'handled, returned null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

**Q50.** What unit does StopwatchEvent::getDuration() use, and when is the debug.stopwatch service available?  <small>_(Miscellaneous)_</small>

- A. Milliseconds; the service exists only when debug/the profiler is enabled
- B. Seconds; always available in every environment
- C. Microseconds; only in prod
- D. Nanoseconds; only in tests

??? success "Answer Q50"
    **A**

    getDuration() returns milliseconds, and the autowirable debug.stopwatch service is only registered in debug (dev/test). Injecting Stopwatch in prod therefore causes a wiring error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

**Q51.** Why does InputBag (query/request/cookies) reject reading an array where a scalar is expected? (choose one)  <small>_(HTTP)_</small>

- A. InputBag restricts values to scalars/arrays-of-scalars/null and throws BadRequestException on a type mismatch, hardening against malicious nested input
- B. PHP forbids arrays in $_GET
- C. ParameterBag also throws in the same case
- D. It silently casts the array to its first element

??? success "Answer Q51"
    **A**

    InputBag extends ParameterBag but narrows the contract to user-supplied data: get() accepts only scalars/null and raises a BadRequestException (HTTP 400) when handed an unexpected array, blocking parameter-pollution style attacks. A plain ParameterBag (used by attributes) imposes no such restriction. Use all('key') to intentionally read array values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

**Q52.** What does MoneyType's divisor option do?  <small>_(Forms)_</small>

- A. Scales the model value (e.g. 100 lets you store integer cents)
- B. Sets the currency symbol
- C. Rounds to N decimals
- D. Limits the maximum amount

??? success "Answer Q52"
    **A**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/money.html)

**Q53.** How is #[Assert\...] attribute metadata turned into constraints at runtime?  <small>_(Validation)_</small>

- A. AttributeLoader builds ClassMetadata once, cached in a PSR-6 pool
- B. It is re-parsed by reflection on every validate() call
- C. It is compiled into the DI container and never changes
- D. It is read from a database mapping table

??? success "Answer Q53"
    **A**

    LazyLoadingMetadataFactory uses AttributeLoader to reflect over the class and build ClassMetadata, which is cached (validator.mapping.cache) so the reflection cost is paid once per class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q54.** A route allows only GET. A POST to that same path returns?  <small>_(Routing)_</small>

- A. 405 Method Not Allowed (with an Allow header)
- B. 404 Not Found
- C. 200 OK
- D. 301 redirect

??? success "Answer Q54"
    **A**

    When the path matches but the method is not allowed, the matcher throws MethodNotAllowedException, producing a 405 with an Allow header. It is not a 404 — the path did match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-http-methods)

**Q55.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(Miscellaneous)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q55"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

**Q56.** What does the default ErrorListener actually do when it handles a kernel.exception?  <small>_(Architecture)_</small>

- A. It logs the exception, forwards to the error controller as a sub-request, and sets the resulting Response on the event
- B. It immediately calls exit() with the HTTP status code
- C. It re-throws the exception so PHP's default handler renders it

??? success "Answer Q56"
    **A**

    ErrorListener (priority -128) logs the throwable, forwards to the error_controller (ErrorController) as a sub-request whose response carries the status/headers from HttpExceptionInterface, and sets that response on the ExceptionEvent. Because it runs last, any higher-priority listener that already set a response wins and ErrorListener does nothing.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/ErrorListener.php)

**Q57.** Which statements about Messenger buses are correct? (choose 2)  <small>_(Miscellaneous)_</small>

- A. The default bus service is messenger.bus.default
- B. You can define multiple buses, each with its own ordered middleware list
- C. All buses in an app must share a single global middleware list
- D. The command/query/event bus split is enforced by the component

??? success "Answer Q57"
    **A, B**

    Messenger ships one default bus (messenger.bus.default) but supports many, each configured with its own middleware — so a command bus can wrap handlers in a transaction while an event bus does not. The command/query/ event convention is just that: a convention, not enforced by the code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/multiple_buses.html)

**Q58.** A parent cascades into a child with #[Assert\Valid] and validate() is called with the Default group. The child has a constraint only in a custom 'strict' group. Does it run?  <small>_(Validation)_</small>

- A. No — only the Default group reaches the child, so its 'strict'-only constraint is skipped
- B. Yes — Valid runs all of the child's groups
- C. Yes — custom groups always run on cascade
- D. Only if the child defines a group sequence

??? success "Answer Q58"
    **A**

    The cascaded group is the current one (Default). A child's custom-group constraint runs only if that custom group actually propagates to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

**Q59.** A class has a #[Assert\NotBlank] attribute on $name, and a YAML mapping file adds Length to the same $name. Which constraints apply?  <small>_(Validation)_</small>

- A. Both — all enabled loaders are merged; attributes do not override YAML, the constraints accumulate
- B. Only the attribute; attributes take precedence
- C. Only the YAML; file mapping wins
- D. A MappingException is thrown for the conflict

??? success "Answer Q59"
    **A**

    LazyLoadingMetadataFactory merges every active loader's constraints for a class, so attribute and YAML constraints add up rather than one silently overriding the other.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q60.** Which tool lets you fail the test suite when new deprecations appear?  <small>_(Architecture)_</small>

- A. symfony/phpunit-bridge configured via SYMFONY_DEPRECATIONS_HELPER
- B. symfony/console
- C. symfony/flex

??? success "Answer Q60"
    **A**

    The PHPUnit bridge collects deprecations; SYMFONY_DEPRECATIONS_HELPER (e.g. max[total]=0) can make the suite fail on any deprecation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

**Q61.** What is the classic gotcha with `ctype_digit(123)` (passing an integer)?  <small>_(PHP & Web Security)_</small>

- A. Small integers are interpreted as ASCII codes, not their digits, giving surprising results
- B. It always returns true for any integer
- C. It throws a TypeError on integers
- D. It converts the integer to a string first

??? success "Answer Q61"
    **A**

    ctype functions treat an int argument in the range -128..255 as an ASCII character code, so ctype_digit(123) checks character code 123 ('{'), not the digits "123" — a false negative. It does not always return true, does not throw, and does not stringify (that is exactly the assumption that bites you). Pass strings: ctype_digit('123') is true. Misconception: assuming numeric arguments are auto-cast to their textual form.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.ctype-digit.php)

**Q62.** What does `json_validate($string)` return?  <small>_(PHP & Web Security)_</small>

- A. A bool indicating whether the string is valid JSON
- B. The decoded associative array
- C. A stdClass object
- D. null on success

??? success "Answer Q62"
    **A**

    json_validate() (8.3) only reports validity as a bool, using less memory than json_decode() for large payloads because it never materialises the structure. It never returns the decoded array or object — that is json_decode()'s job — and it does not return null on success. Misconception: expecting a decoded value; if you need the data, still call json_decode() afterwards.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.json-validate.php)

**Q63.** What is the result of ExpressionLanguage::compile('1 + a', ['a'])?  <small>_(Miscellaneous)_</small>

- A. The PHP source string "(1 + $a)"
- B. The integer 1
- C. A closure you can invoke
- D. An exception, because $a is undefined

??? success "Answer Q63"
    **A**

    compile() emits PHP source, turning the variable name a into $a: "(1 + $a)". It does not evaluate anything (so no undefined-variable error) — use evaluate('1 + a', ['a' => 5]) to get the value 6.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q64.** At the front controller, which call builds the Request object from PHP's superglobals? (choose one)  <small>_(HTTP)_</small>

- A. Request::createFromGlobals()
- B. Request::create()
- C. new Request($_SERVER)
- D. Request::createFromRequest()

??? success "Answer Q64"
    **A**

    public/index.php calls Request::createFromGlobals(), which reads $_GET, $_POST, $_SERVER, $_COOKIE and $_FILES once into the typed bags. Request::create() builds a synthetic request from explicit arguments (used in tests/sub-requests), and there is no createFromRequest() factory for this purpose.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q65.** How do you configure eraseCredentials behaviour in security.yaml in Symfony 8?  <small>_(Security)_</small>

- A. You don't — eraseCredentials() was removed in 8.0; strip secrets in the user's __serialize()
- B. Add erase_credentials: true under each firewall
- C. Set it inside the password_hashers map
- D. It is enabled by default via the erase_credentials key

??? success "Answer Q65"
    **A**

    There is no eraseCredentials configuration key, and there never was — it was a UserInterface method. In Symfony 8 both UserInterface::eraseCredentials() and TokenInterface::eraseCredentials() were removed; the documented replacement is to strip sensitive data (the password) in your user's __serialize() method, which is what runs when the token/user is stored in the session.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/UPGRADE-8.0.md)

**Q66.** Which is true about shortcuts like `-f`?  <small>_(Console)_</small>

- A. Shortcuts belong to options only; arguments have no shortcuts
- B. Every argument automatically gets a one-letter shortcut
- C. Shortcuts are only for VALUE_NONE options
- D. Shortcuts must be exactly two characters

??? success "Answer Q66"
    **A**

    Only options accept a shortcut (the 2nd argument of addOption); arguments are positional and have no shortcut. Shortcuts work for any option mode, not just VALUE_NONE, and are typically a single character (e.g. -f).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

**Q67.** Which event is responsible for turning an exception into a response?  <small>_(Architecture)_</small>

- A. kernel.exception
- B. kernel.view
- C. kernel.terminate

??? success "Answer Q67"
    **A**

    When an exception escapes handleRaw(), HttpKernel dispatches kernel.exception; listeners may set the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q68.** Which built-in controller renders a Twig template purely from route config?  <small>_(Controllers)_</small>

- A. TemplateController
- B. RenderController
- C. TwigController

??? success "Answer Q68"
    **A**

    TemplateController::__invoke() renders the 'template' default and can set HTTP cache headers, needing no custom class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#rendering-a-template-directly-from-a-route)

**Q69.** After adding { path: ^/, roles: PUBLIC_ACCESS } at the top of access_control, the ^/admin rule below stops protecting admin. Why?  <small>_(Security)_</small>

- A. First match wins; ^/ matches every path including /admin, so the catch-all is enforced and the admin rule is never reached
- B. PUBLIC_ACCESS globally disables all other access_control rules
- C. roles must be given as a list, not a string, to take effect
- D. The admin rule needs a requires_channel to be evaluated

??? success "Answer Q69"
    **A**

    access_control is first-match, top-to-bottom. ^/ matches all paths, so placing it first means /admin hits the PUBLIC_ACCESS rule and the ^/admin rule underneath is never evaluated — admin becomes public. Order specific rules before the ^/ catch-all. PUBLIC_ACCESS is a normal attribute (it does not disable other rules), and the roles syntax/requires_channel are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

**Q70.** A test does: $client = static::createClient(); then self::getContainer()->set(PaymentGateway::class, $mock); then $client->request('POST', '/checkout'); — but the real gateway still runs. What is the most likely fix?  <small>_(Testing)_</small>

- A. Call $client->disableReboot() before set(), so the replacement survives the reboot that createClient triggers on the next request
- B. Call set() again after the request
- C. Make PaymentGateway public in services.yaml
- D. Replace self::getContainer() with static::$kernel->getContainer()

??? success "Answer Q70"
    **A**

    By default the kernel reboots (rebuilding a fresh container) around requests, discarding any set() replacement. disableReboot() keeps the container — and your mock — alive across the request. Calling set() after the request is too late; the class already has visibility (getContainer exposes it); and $kernel->getContainer() hides private services entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q71.** Which version string should you pass as the second argument of trigger_deprecation()?  <small>_(Architecture)_</small>

- A. The version in which the API was DEPRECATED (e.g. '8.1'), not the current running version
- B. The current installed version at the time the notice fires
- C. The version in which the code will be REMOVED (the next major)

??? success "Answer Q71"
    **A**

    The version argument records when the deprecation was introduced, producing the \"Since <package> <version>: <message>\" format tooling parses. A common mistake is passing the current version, or the removal version — both are wrong. Use the version the API was deprecated in.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q72.** True or false: {# ... #} comments are removed at compile time and never reach the browser.  <small>_(Twig)_</small>

- A. True
- B. False

??? success "Answer Q72"
    **A**

    Twig {# #} comments are stripped during compilation and produce no output, unlike HTML <!-- --> comments which are sent to the client. Use {# #} for template notes you do not want leaking to users.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

**Q73.** Which lock store provides mutual exclusion across multiple servers?  <small>_(Miscellaneous)_</small>

- A. RedisStore
- B. FlockStore
- C. SemaphoreStore
- D. InMemoryStore

??? success "Answer Q73"
    **A**

    Flock and Semaphore stores are local to one machine, and InMemoryStore is per-process (tests). Shared stores like Redis (or a database store) coordinate locks across servers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#available-stores)

**Q74.** createNotFoundException() aborts the action as soon as it is called. True or false?  <small>_(Controllers)_</small>

- A. False
- B. True

??? success "Answer Q74"
    **A**

    It only returns a NotFoundHttpException object; nothing happens until you `throw` it. Treating it as self-aborting is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q75.** In Symfony's Cookie value object, `httpOnly` defaults to true. True or false?  <small>_(Controllers)_</small>

- A. True
- B. False

??? success "Answer Q75"
    **A**

    Cookie defaults are security-first: httpOnly=true (hidden from JS, mitigating XSS token theft) and sameSite='lax'. JS-readable cookies must opt out explicitly with withHttpOnly(false).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Cookie.php)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
