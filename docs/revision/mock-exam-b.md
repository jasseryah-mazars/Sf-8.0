# Mock Exam B (Exam Mode)

!!! note "Three independent papers"
    This is **Mock B**. Also try: [Mock A](mock-exam.md) · [Mock C](mock-exam-c.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

## 🧠 Pour les nuls

**C'est quoi ?** Un **examen blanc complet** : 75 questions, 90 minutes, sans notes — les conditions exactes de l'examen officiel Symfony 8, sur un échantillon pondéré du même sujet que l'examen réel. Le Mock B est l'une de trois versions indépendantes (A, B, C) tirées de la même banque.

**Pourquoi ça existe ?** Connaître chaque notion séparément ne garantit pas de réussir un examen chronométré de 90 minutes qui mélange tout. Le mock exam entraîne spécifiquement la gestion du temps et l'endurance mentale, en plus des connaissances.

**🏠 Analogie de la vraie vie :** C'est le **concours blanc** que passent les lycéens avant le bac : mêmes conditions, même durée, une note à la fin — pour savoir vraiment où on en est, pas pour apprendre du nouveau contenu.

**Symfony dans la vraie vie :** 75 questions pondérées → même répartition que l'examen réel (Architecture/DI/Sécurité/Messenger plus présents) / 90 minutes chronométrées → même contrainte de temps que le jour J / Score final → indicateur direct de préparation, pas une note scolaire.

**⚠️ Erreur fréquente :** Consulter la réponse dès qu'une question semble difficile, au lieu de la flaguer et d'avancer. Cela fausse complètement le chronométrage et masque le vrai niveau de préparation.

**🧠 Comment le mémoriser :** *« Chronomètre en marche, pas de pause, pas de triche »* — un mock exam fait à moitié (avec pauses ou aide) ne prédit rien sur l'examen réel.

---

**Q1.** In Symfony 8, how do you allow everyone (including not-logged-in) on a path?  <small>_(Security)_</small>

- A. PUBLIC_ACCESS
- B. IS_AUTHENTICATED_ANONYMOUSLY
- C. ROLE_ANONYMOUS
- D. IS_ANONYMOUS

??? success "Answer Q1"
    **A**

    Anonymous tokens were removed; PUBLIC_ACCESS is the attribute that opts a path out of authentication.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q2.** What is the default Process timeout?  <small>_(Miscellaneous)_</small>

- A. 60 seconds
- B. Unlimited
- C. 30 seconds
- D. 300 seconds

??? success "Answer Q2"
    **A**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/process.html#process-timeout)

**Q3.** How do you access the test container in a modern Symfony 8 test?  <small>_(Testing)_</small>

- A. self::getContainer() — the old static::$container property was removed
- B. static::$container — still the recommended property
- C. $this->container, injected automatically into every TestCase
- D. static::$kernel->getContainer(), which exposes private services

??? success "Answer Q3"
    **A**

    The historical static::$container property is gone; call the self::getContainer() method, which returns the TestContainer. $this->container does not exist on the base test classes, and static::$kernel->getContainer() returns the normal container where private services are hidden.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#accessing-the-container)

**Q4.** Which YAML import type loads #[Route] attributes from a directory in Symfony 8?  <small>_(Routing)_</small>

- A. type: attribute
- B. type: annotation
- C. type: php
- D. type: directory

??? success "Answer Q4"
    **A**

    Attribute route loading uses `type: attribute`; the `annotation` type is gone in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q5.** Which value should you trust to determine an uploaded file's real type?  <small>_(Controllers)_</small>

- A. getMimeType() (content-detected by the guesser)
- B. getClientMimeType()
- C. getClientOriginalExtension()

??? success "Answer Q5"
    **A**

    Client-supplied name/MIME are spoofable; getMimeType()/guessExtension() inspect the actual file content.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q6.** In Symfony 8, where are a Passport's badges validated?  <small>_(Security)_</small>

- A. Inside the authenticator's authenticate() method
- B. By listeners on the CheckPassportEvent
- C. In createToken()
- D. In the Firewall listener before routing

??? success "Answer Q6"
    **B**

    authenticate() only builds the Passport. Badge resolution and credential verification happen on CheckPassportEvent (UserProviderListener, CheckCredentialsListener, CsrfProtectionListener…).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/custom_authenticator.html)

**Q7.** A locator built for keys 'stripe' and 'paypal' is called with a user-supplied key 'unknown'. What happens?  <small>_(Dependency Injection)_</small>

- A. It throws ServiceNotFoundException — validate with has() before get()
- B. It returns null
- C. It returns the first declared service
- D. It builds a new empty service on the fly

??? success "Answer Q7"
    **A**

    A locator's set is fixed at compile time, so get() on a key outside the whitelist throws; unlike the main container there is no NULL_ON_INVALID mode. Guard untrusted keys with has() first. It never returns null or falls back to another service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q8.** You set migrate_from and needsRehash() returns true, yet stored hashes are never upgraded. What is missing?  <small>_(Security)_</small>

- A. The user provider does not implement PasswordUpgraderInterface, so upgradePassword() is never called to persist the new hash
- B. migrate_from only works with the plaintext algorithm
- C. You must call password_hash() yourself in the controller
- D. needsRehash() is not supported in Symfony 8

??? success "Answer Q8"
    **A**

    migrate_from + needsRehash() computes a fresh hash, but persisting it is the provider's job: only a provider implementing PasswordUpgraderInterface's upgradePassword() actually stores it (triggered by the PasswordUpgradeBadge / PasswordMigratingListener). Without it, the rehash is computed and discarded every login. migrate_from is not plaintext-only, you must not hash manually, and needsRehash() is fully supported.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q9.** What is Twig's default defence against XSS?  <small>_(PHP & Web Security)_</small>

- A. Context-aware auto-escaping of output variables
- B. Stripping all HTML tags
- C. Sending a CSP header
- D. Encrypting the output

??? success "Answer Q9"
    **A**

    Twig HTML-escapes variables by default (context-aware), so injected markup renders as inert text. It does not strip tags (it encodes them), does not send CSP (a separate, complementary defence), and does not encrypt output. The |raw filter opts out and reintroduces the risk. Misconception: thinking escaping removes content — it encodes it so the browser treats it as data.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html)

**Q10.** How is an invokable single-action controller referenced in the `_controller` attribute? (choose one)  <small>_(Controllers)_</small>

- A. The fully-qualified class name only (Symfony calls __invoke)
- B. Class::__invokeAction
- C. class#invoke

??? success "Answer Q10"
    **A**

    For an invokable controller you reference only the class; the ControllerResolver detects the __invoke() method automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

**Q11.** A command's execute() throws a RuntimeException. What is the event sequence?  <small>_(Console)_</small>

- A. COMMAND → ERROR → TERMINATE (TERMINATE still runs after ERROR)
- B. COMMAND → TERMINATE only (ERROR is skipped for RuntimeException)
- C. ERROR → COMMAND → TERMINATE
- D. ERROR only; the process aborts before TERMINATE

??? success "Answer Q11"
    **A**

    COMMAND fires before execution; the thrown Throwable triggers ERROR (ConsoleErrorEvent, where a listener can change the exit code or swap the exception); TERMINATE always fires last, even after an error. ERROR never runs before COMMAND, and it does not suppress TERMINATE.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q12.** For the router, which statement about id, class and autowiring alias is correct?  <small>_(Dependency Injection)_</small>

- A. The id is 'router', the class is a concrete Router, and an Alias maps RouterInterface to the id
- B. The id, class and alias are all the string 'router'
- C. The autowiring alias is the class FQCN pointing at the interface
- D. There is no alias; autowiring matches the id string directly

??? success "Answer Q12"
    **A**

    These are three distinct keys. FrameworkExtension registers the service under the id 'router' with a concrete class, then adds an autowiring alias from the interface FQCN (RouterInterface) to that id so type-hints resolve. debug:autowiring lists those aliases; debug:container inspects the id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/debug.html)

**Q13.** For each firewall, what does SecurityExtension compile at container build time?  <small>_(Security)_</small>

- A. A FirewallContext bundling its listeners, the authenticator list, an AuthenticatorManager, and (unless stateless) a ContextListener — all indexed in a FirewallMap
- B. A single global Firewall service shared unchanged by every firewall
- C. One controller per firewall generated from the config
- D. Nothing at build time — firewalls are assembled lazily on the first request

??? success "Answer Q13"
    **A**

    SecurityExtension reads the security.yaml tree and, per firewall, compiles a dedicated FirewallContext (its listeners, the list of authenticators, an AuthenticatorManager, an exception listener, and a ContextListener unless the firewall is stateless). All contexts are registered in the FirewallMap; at runtime the single Firewall listener asks the map which context matches. The work happens at compile time, not lazily per request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/SecurityBundle/DependencyInjection/SecurityExtension.php)

**Q14.** Which command prints a bundle's configuration reference tree?  <small>_(Dependency Injection)_</small>

- A. config:dump-reference
- B. debug:container
- C. debug:autowiring
- D. debug:router

??? success "Answer Q14"
    **A**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q15.** You need a global whose value is computed from an injected service. Which approach fits best?  <small>_(Twig)_</small>

- A. An extension implementing GlobalsInterface::getGlobals() returning the computed value
- B. A {% set %} at the top of base.html.twig
- C. A #[AsGlobal] attribute on the service
- D. Hard-coding it in every controller's render() call

??? success "Answer Q15"
    **A**

    GlobalsInterface::getGlobals() lets an extension inject a service and return computed values, resolved lazily when the extension is instantiated. A static YAML twig.globals entry (even '@service') is fine for simple references, but computed/lazy values belong in a GlobalsInterface extension. There is no #[AsGlobal] attribute.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#global-variables)

**Q16.** With two decorators on one id, a higher decoration_priority means the decorator is...  <small>_(Dependency Injection)_</small>

- A. Applied first and sits closer to the original (innermost)
- B. Applied last and is the outermost
- C. Ignored
- D. Made public automatically

??? success "Answer Q16"
    **A**

    Higher priority decorators are applied first and end up innermost; consumers receive the lowest-priority, outermost decorator.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html#decoration-priority)

**Q17.** A .env file sets DATABASE_URL, but a real OS environment variable DATABASE_URL is also exported. Which wins?  <small>_(Miscellaneous)_</small>

- A. The real OS environment variable — DotEnv never overrides an existing real env var
- B. .env, because it is loaded last
- C. Whichever value is longer
- D. They are concatenated

??? success "Answer Q17"
    **A**

    Real OS environment variables always take precedence; the DotEnv cascade (.env → .env.local → .env.<env> → .env.<env>.local) only fills values not already set in the real environment. Later .env* files override earlier ones but never a real env var.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#overriding-environment-values-via-env-local)

**Q18.** With autoconfiguration disabled, which services.yaml tag correctly registers an extension for FileType?  <small>_(Forms)_</small>

- A. tags: [{ name: form.type_extension, extended_type: Symfony\Component\Form\Extension\Core\Type\FileType }]
- B. tags: [{ name: form.type_extension }]  # extended_type inferred
- C. tags: [{ name: form.type, extended_type: FileType }]
- D. tags: [{ name: form.extension, class: FileType }]

??? success "Answer Q18"
    **A**

    Without autoconfiguration you must both use the form.type_extension tag and supply the extended_type attribute (the FQCN of the extended type) — it is not inferred from getExtendedTypes() in the manual case. form.type is for form types, and form.extension is not a real tag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q19.** Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?  <small>_(Miscellaneous)_</small>

- A. null is returned as a cache hit; the callback is NOT run again
- B. The callback runs again because null means a miss
- C. A CacheException is thrown for storing null
- D. The item is deleted automatically

??? success "Answer Q19"
    **A**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/cache.html#cache-contracts)

**Q20.** What does dispatch(object $event) return, and how do you read a listener's result?  <small>_(Architecture)_</small>

- A. It always returns the same event object you passed in; results reach you only by listeners mutating that event (e.g. setResponse), never as a listener return value
- B. It returns whatever the last listener returned
- C. It returns null when no listener set a value

??? success "Answer Q20"
    **A**

    dispatch() returns the exact event object passed in — even with no listeners, or when all left it untouched. Listeners themselves return void; the only way data flows back is by mutating the event, which you then read from the returned object. Expecting dispatch() to hand back a listener's return value is the classic bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/event_dispatcher.html)

**Q21.** Can an access_control rule pass the matched entity to a voter as the subject?  <small>_(Security)_</small>

- A. No — access_control has no subject; it calls AccessDecisionManager with only roles/allow_if. Use #[IsGranted] with a subject for per-object rules
- B. Yes, via a subject: key on the rule
- C. Yes, the matched path parameter is passed as the subject
- D. Only when allow_if is also set

??? success "Answer Q21"
    **A**

    access_control routes through the same AccessDecisionManager and voters as isGranted(), but it is purely URL-driven: the AccessListener calls decide() with the rule's roles/expression and no subject. There is no subject: key and path parameters are not passed as subjects. Per-object decisions require #[IsGranted]/denyAccessUnlessGranted() with an explicit subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q22.** What does the symfony.lock file track?  <small>_(Architecture)_</small>

- A. Which recipes are installed and their versions
- B. The compiled service container
- C. Locked HTTP sessions

??? success "Answer Q22"
    **A**

    symfony.lock records applied recipes so Flex can detect updates and reverse them; it is distinct from composer.lock (package versions).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/setup.html)

**Q23.** In phpunit.dist.xml, how is the bridge's extension registered in PHPUnit 11/12?  <small>_(Testing)_</small>

- A. <extensions><bootstrap class="Symfony\Bridge\PhpUnit\SymfonyExtension"/></extensions>
- B. <listeners><listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener"/></listeners>
- C. <php><extension name="symfony"/></php>
- D. It is auto-registered by Composer; no XML entry is needed

??? success "Answer Q23"
    **A**

    PHPUnit 10+ uses the <extensions><bootstrap .../></extensions> mechanism to load the SymfonyExtension. The old <listeners><listener> (SymfonyTestsListener) approach belongs to PHPUnit 9 and earlier; there is no <php><extension> tag, and the extension is not auto-registered.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

**Q24.** True or False: routing a message to the sync:// transport skips the middleware pipeline.  <small>_(Miscellaneous)_</small>

- A. True
- B. False

??? success "Answer Q24"
    **B**

    False. sync:// still runs the full middleware stack (validation, transactions, handler discovery) — it simply handles the message immediately in the same process instead of enqueueing it. Treating sync:// as "no bus" is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transport-configuration)

**Q25.** Which condition matches only when the request query string contains a 'preview' key?  <small>_(Routing)_</small>

- A. condition: "request.query.has('preview')"
- B. condition: "request.get('preview') == true"
- C. condition: "query.preview is defined"
- D. condition: "has('preview')"

??? success "Answer Q25"
    **A**

    Inside a condition, `request` is the HttpFoundation Request, so request.query.has('preview') is the idiomatic check. `query` alone is not a variable, and there is no bare has() function.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q26.** A #[Assert\Callback(groups: ['checkout'])] never fires during a plain validate($obj). Why, and does it join sequences?  <small>_(Validation)_</small>

- A. It runs only when the 'checkout' group is validated; being class-scoped, it also participates in group sequences like any constraint
- B. Callbacks ignore groups; the attribute is malformed
- C. Callbacks can never run inside groups
- D. It runs only in the Default group regardless of the option

??? success "Answer Q26"
    **A**

    Callback honours its groups option (default Default). A non-Default callback runs only when that group is validated, and it participates in group sequences exactly like any other constraint.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Callback.html)

**Q27.** Which statement about PSR-6 vs PSR-16 is correct?  <small>_(Miscellaneous)_</small>

- A. PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not
- B. PSR-16 supports tags but PSR-6 does not
- C. Both are identical key/value APIs
- D. PSR-6 has no expiration support

??? success "Answer Q27"
    **A**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/cache.html)

**Q28.** What integer value does `Command::INVALID` represent?  <small>_(Console)_</small>

- A. 2
- B. 0
- C. 1
- D. 255

??? success "Answer Q28"
    **A**

    The return constants are SUCCESS=0, FAILURE=1, INVALID=2. INVALID signals bad input/usage as opposed to a runtime failure (FAILURE=1). 255 is a shell convention for a general error but is not a Command constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q29.** For a factory-built service, where are its arguments passed?  <small>_(Dependency Injection)_</small>

- A. To the factory method
- B. To the class constructor
- C. To __invoke only
- D. They are ignored

??? success "Answer Q29"
    **A**

    With a factory, the container calls the factory and passes the definition's arguments to it, not to a constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q30.** The password_hashers map in security.yaml is keyed by…  <small>_(Security)_</small>

- A. A user class or interface name
- B. A firewall name
- C. A provider name
- D. An algorithm name

??? success "Answer Q30"
    **A**

    You map a user class (commonly PasswordAuthenticatedUserInterface) to an algorithm such as 'auto'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q31.** Which Request method returns the negotiated HTTP protocol version (e.g. HTTP/2)? (choose one)  <small>_(HTTP)_</small>

- A. getProtocolVersion()
- B. getScheme()
- C. getMethod()
- D. getContentTypeFormat()

??? success "Answer Q31"
    **A**

    getScheme() returns http/https; getProtocolVersion() returns the version string from SERVER_PROTOCOL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q32.** What does `cache:clear` run, by default, in addition to removing stale cache?  <small>_(Miscellaneous)_</small>

- A. The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata
- B. The database migrations
- C. The Messenger workers
- D. composer install

??? success "Answer Q32"
    **A**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q33.** Given AcceptHeader::fromString('text/html;q=0.9, application/json;q=1.0'), what does $accept->first()?->getQuality() return? (choose one)  <small>_(HTTP)_</small>

- A. 1.0 — first() returns the highest-quality item (application/json)
- B. 0.9 — items are returned in string order
- C. null — first() only works on a single-value header
- D. true — first() returns a boolean like has()

??? success "Answer Q33"
    **A**

    AcceptHeader parses and sorts items by quality (descending), so first() returns the AcceptHeaderItem for application/json (q=1.0) and getQuality() gives 1.0. The nullsafe operator guards the empty-header case where first() would return null.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/AcceptHeader.php)

**Q34.** What is the purpose of DispatchAfterCurrentBusStamp?  <small>_(Miscellaneous)_</small>

- A. Defer delivery of a message dispatched inside a handler until the current handling finishes successfully
- B. Send the message to every bus in the application
- C. Add a delay equal to the current bus latency
- D. Retry the message on the next bus in a chain

??? success "Answer Q34"
    **A**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them. It has nothing to do with delays, multi-bus fan-out, or retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/dispatch_after_current_bus.html)

**Q35.** What does security: false on a firewall do?  <small>_(Security)_</small>

- A. Disables the security layer for that zone (and still counts as the match)
- B. Denies all access to that zone
- C. Enables anonymous voting
- D. Makes the firewall stateless

??? success "Answer Q35"
    **A**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q36.** Your metric is only complete after the response is sent. Which interface should the collector implement?  <small>_(Miscellaneous)_</small>

- A. LateDataCollectorInterface (its lateCollect() runs at kernel.terminate)
- B. DataCollectorInterface only; collect() runs after terminate
- C. EventSubscriberInterface on kernel.request
- D. CacheWarmerInterface

??? success "Answer Q36"
    **A**

    Normal collect() runs on kernel.response, too early for post-response data (final dumps, cache calls). LateDataCollectorInterface::lateCollect() runs later at terminate, when that data is complete.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/profiler/data_collector.html)

**Q37.** How is an included template handled by Twig internally?  <small>_(Twig)_</small>

- A. It is a separate compiled class, loaded via the loader and invoked at runtime — not textually inlined
- B. Its source is pasted into the parent before compilation
- C. It is re-parsed from disk on every render with no caching
- D. It is merged into the parent's single block table

??? success "Answer Q37"
    **A**

    The include tag compiles to a call to Twig\Template::display()/render() on the sub-template, which the FilesystemLoader resolves and which is compiled and cached like any other template. Includes are separate compiled classes invoked at runtime, not inlined text.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Loader/FilesystemLoader.php)

**Q38.** For a mapped CollectionType to call the parent's adder/remover methods, set…  <small>_(Forms)_</small>

- A. by_reference => false
- B. allow_add => false
- C. prototype => false
- D. mapped => false

??? success "Answer Q38"
    **A**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/collection.html)

**Q39.** With #[Cache(lastModified: 'post.getUpdatedAt()')], when can a 304 be returned?  <small>_(HTTP Caching)_</small>

- A. Before the controller body runs, during kernel.controller_arguments
- B. Only after the controller has fully rendered the response
- C. Only inside a kernel.terminate listener
- D. Never — expressions cannot short-circuit

??? success "Answer Q39"
    **A**

    CacheAttributeListener evaluates the expression on CONTROLLER_ARGUMENTS (priority 10) and, if the request is up to date, replaces the controller so a 304 is returned without running the body. That is precisely the CPU/render saving the model exists for; it does not wait for RESPONSE or terminate.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

**Q40.** Symfony's session cookie defaults to HttpOnly: true and SameSite: lax. True or false?  <small>_(HTTP)_</small>

- A. True
- B. False

??? success "Answer Q40"
    **A**

    Symfony ships secure session-cookie defaults: HttpOnly is true (JavaScript cannot read the session id) and SameSite is lax (mitigating most CSRF via cookies while still allowing top-level GET navigations). cookie_secure typically defaults to 'auto' (Secure when the request is HTTPS).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#cookie-httponly)

**Q41.** What is the full firing order of the linear kernel events when a controller returns a non-Response value that a listener then converts?  <small>_(Architecture)_</small>

- A. request → controller → controller_arguments → view → response → finish_request → (after send) terminate
- B. request → controller_arguments → controller → response → view → terminate → finish_request
- C. request → controller → view → controller_arguments → response → terminate
- D. request → controller → response → view → finish_request → terminate

??? success "Answer Q41"
    **A**

    The canonical order is request, controller, controller_arguments, view (only when a non-Response is returned), response, finish_request; then after the response is sent, terminate. kernel.exception is the eighth KernelEvents constant but fires out of band, only on error. controller_arguments runs AFTER argument resolution, and view sits between the controller call and response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html)

**Q42.** On a logged-out request, what does isGranted('ROLE_ADMIN') do internally?  <small>_(Security)_</small>

- A. The AuthorizationChecker substitutes a NullToken and voters run; RoleVoter finds no matching role and it returns a clean false
- B. It throws because the token in storage is null
- C. It returns true because no access_control rule restricts it
- D. It redirects to the firewall entry point

??? success "Answer Q42"
    **A**

    When TokenStorage holds no token, AuthorizationChecker substitutes a NullToken rather than crashing, and voting proceeds normally. RoleVoter finds ROLE_ADMIN is not present, so the decision is false — not an exception. (AuthenticatedVoter denies the IS_AUTHENTICATED_* attributes for a NullToken, while PUBLIC_ACCESS still grants.) Authorization never starts authentication by itself; only an AccessDeniedException handled by the firewall triggers the entry point.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authentication/Token/NullToken.php)

**Q43.** Which two methods do you typically override in an AbstractType?  <small>_(Forms)_</small>

- A. buildForm(FormBuilderInterface, array) and configureOptions(OptionsResolver)
- B. build() and getOptions()
- C. getName() and buildView()
- D. configureFields() and setDefaults()

??? success "Answer Q43"
    **A**

    buildForm() adds fields to the builder; configureOptions() declares the type's options via OptionsResolver. getName() was removed; buildView() exists but is not the primary pair.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q44.** What is the signature of HttpKernelInterface::handle() and the role of its $catch argument?  <small>_(Architecture)_</small>

- A. handle(Request $request, int $type = self::MAIN_REQUEST, bool $catch = true): Response — with $catch=true, exceptions are caught and turned into a response via kernel.exception; with $catch=false they propagate
- B. handle(Request $request): void — it prints the response directly and $catch controls output buffering
- C. handle(string $env, bool $debug): Response — $catch enables the profiler

??? success "Answer Q44"
    **A**

    The contract is handle(Request, int $type = MAIN_REQUEST, bool $catch = true): Response. handle() wraps the private handleRaw() in a try/catch when $catch is true, so an escaped exception is routed through handleThrowable()/kernel.exception into a Response. With $catch=false (common in sub-requests and tests) the exception simply propagates to the caller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html)

**Q45.** Why is permanent: true (301) a poor choice for a temporary or A/B redirect?  <small>_(Routing)_</small>

- A. Browsers cache 301s aggressively, so you cannot easily change the target later
- B. 301 is not a valid redirect status
- C. 301 strips query parameters automatically
- D. 301 requires HTTPS

??? success "Answer Q45"
    **A**

    A 301 tells clients the move is permanent, so browsers cache it hard and may not re-request the old URL. Use 302 (the default) while a target is still in flux.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q46.** A user uploads a file larger than `post_max_size` and the action crashes on a null `$request->files->get('avatar')`. What is the underlying cause?  <small>_(Controllers)_</small>

- A. Exceeding post_max_size can yield an empty files bag (no exception), so the get() returns null — always null-check
- B. move() threw a FileException that was swallowed
- C. getMimeType() returns null for large files
- D. Symfony automatically rejects the request with a 413

??? success "Answer Q46"
    **A**

    When post_max_size is exceeded, PHP may discard the POST data, leaving an empty files bag rather than raising an exception. Guard the result with an instanceof UploadedFile / isValid() check before using it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q47.** You need only canned return values, with no verification of how a collaborator is called. Which double do you create?  <small>_(Testing)_</small>

- A. A stub via $this->createStub(Foo::class)
- B. A mock via $this->createMock(Foo::class) with expects()
- C. A spy via $this->createSpy(Foo::class)
- D. A partial mock via getMockForTrait()

??? success "Answer Q47"
    **A**

    A stub supplies return values but never asserts interactions. A mock adds verifiable expectations you do not need here.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/test-doubles.html)

**Q48.** A request handler crashes with a TypeError only when the X-Trace-Id header is absent, on the line strtoupper($request->headers->get('X-Trace-Id')). What is the cause and fix? (choose one)  <small>_(HTTP)_</small>

- A. HeaderBag::get() returns null for a missing key; guard with ?? or supply a default before calling a string function
- B. get() throws when the header is missing; wrap it in try/catch
- C. Headers are only readable via $_SERVER; the bag is empty
- D. get() returns an empty array, breaking strtoupper()

??? success "Answer Q48"
    **A**

    HeaderBag::get(string $key, mixed $default = null) returns null when the key is absent — a normal lookup miss, not an error. Passing null to strtoupper() triggers the TypeError. Guard with $request->headers->get('X-Trace-Id') ?? '' or pass a default. Typed InputBag getters (getString etc.) coalesce to a zero value, but HeaderBag::get() is nullable.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/HeaderBag.php)

**Q49.** Which are valid places to register a compiler pass? (choose 2)  <small>_(Dependency Injection)_</small>

- A. Kernel::build(ContainerBuilder $c) via addCompilerPass()
- B. A bundle's build(ContainerBuilder $c) via addCompilerPass()
- C. A #[CompilerPass] attribute on the pass class
- D. A container.compiler_pass tag in services.yaml

??? success "Answer Q49"
    **A, B**

    Passes are registered programmatically with addCompilerPass() in the application Kernel::build() or a bundle's build(). There is no #[CompilerPass] attribute and no services.yaml tag that registers a pass — those are common invented answers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q50.** For route app_help at /{_locale}/help, what does generateUrl('app_help', ['_locale' => 'es']) produce?  <small>_(Routing)_</small>

- A. /es/help
- B. /help?_locale=es
- C. /help/es
- D. /en/help

??? success "Answer Q50"
    **A**

    _locale is a real placeholder in the path, so it fills the {_locale} segment giving /es/help — not a query string, and not the default en.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q51.** `$request->getContent()` is called on a JSON API request. What does it return?  <small>_(Controllers)_</small>

- A. The raw request body as a string — it is not JSON-decoded
- B. An associative array decoded from the JSON body
- C. The parsed $request->request InputBag
- D. A stdClass of the JSON payload

??? success "Answer Q51"
    **A**

    getContent() returns the raw body; it does not decode JSON. Use #[MapRequestPayload] (serializer + validator) or json_decode() yourself to get a structured value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

**Q52.** $envelope->last(HandledStamp::class) returns null. Which situation explains this best?  <small>_(Miscellaneous)_</small>

- A. The message was routed to an async transport, so it has not been handled in this process yet
- B. The handler returned null, so no HandledStamp was created
- C. dispatch() failed and returned null instead of an Envelope
- D. HandledStamp only exists on the query bus

??? success "Answer Q52"
    **A**

    A handler that returns null still produces a HandledStamp (its result is null) — so last() returning null means no such stamp exists, i.e. the message was sent async and not handled here. dispatch() always returns an Envelope (never null), and HandledStamp is not query-bus-specific. This is why the nullsafe ?-> guards 'not handled here', distinct from 'handled, returned null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-getting-handler-results)

**Q53.** A constraint declared without any explicit 'groups' option belongs to which validation group?  <small>_(Validation)_</small>

- A. The special 'Default' group
- B. No group at all, so it is never validated
- C. A group named after the property
- D. The 'Strict' group

??? success "Answer Q53"
    **A**

    Every constraint with no explicit groups is placed in the Default group, which is the group used when you call validate() without specifying groups.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q54.** A startup ships a closed-source SaaS built on Symfony and wants to market it as "SymfonyCloud". Which part is a problem?  <small>_(Architecture)_</small>

- A. The closed-source SaaS is fine under MIT, but naming it "SymfonyCloud" risks trademark infringement
- B. Both are forbidden: MIT bans commercial use and the name is trademarked
- C. Neither is a problem: MIT grants full rights to the Symfony name too

??? success "Answer Q54"
    **A**

    MIT permits commercial, closed-source use, so building the SaaS is fine. But the code license says nothing about names/logos: using \"Symfony\" in a product name is governed by Symfony SAS's trademark policy, so \"SymfonyCloud\" is the risky part. You may say \"built with Symfony\" but not brand as Symfony.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

**Q55.** With a JSON manifest configured, what does asset('app.css') resolve to?  <small>_(Twig)_</small>

- A. The content-hashed name looked up in manifest.json (e.g. app.7f3c.css), not the literal path
- B. The literal /app.css path with ?v appended
- C. An error if app.css is not physically present
- D. The manifest.json file itself

??? success "Answer Q55"
    **A**

    JsonManifestVersionStrategy maps the logical name to its hashed filename from manifest.json, so asset('app.css') returns the resolved hashed path. Expecting the literal path with a ?v query (that is StaticVersionStrategy) is the trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/asset.html)

**Q56.** Inside a StreamedResponse callback, code echoes rows and then calls `$response->headers->set('Content-Type', 'text/csv')`. What is wrong?  <small>_(Controllers)_</small>

- A. Headers cannot be changed after output has started; set Content-Type before returning the response
- B. StreamedResponse ignores Content-Type entirely
- C. The callback must return the header array
- D. You must use JsonResponse for CSV

??? success "Answer Q56"
    **A**

    The callback runs at send time; once bytes are flushed the headers are already sent, so header changes are ineffective. Set headers on the StreamedResponse before returning it from the action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#streaming-a-response)

**Q57.** A parent cascades into a child with #[Assert\Valid] and validate() is called with the Default group. The child has a constraint only in a custom 'strict' group. Does it run?  <small>_(Validation)_</small>

- A. No — only the Default group reaches the child, so its 'strict'-only constraint is skipped
- B. Yes — Valid runs all of the child's groups
- C. Yes — custom groups always run on cascade
- D. Only if the child defines a group sequence

??? success "Answer Q57"
    **A**

    The cascaded group is the current one (Default). A child's custom-group constraint runs only if that custom group actually propagates to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q58.** To cache a public page in a CDN for 10 minutes without letting the browser cache it long-term, which setter do you use? (choose one)  <small>_(HTTP)_</small>

- A. setSharedMaxAge(600) (plus setPublic()), which emits s-maxage honoured only by shared caches
- B. setMaxAge(600), which targets shared caches only
- C. setPrivate(), which enables CDN caching
- D. setExpires(), which only affects the browser

??? success "Answer Q58"
    **A**

    setSharedMaxAge() writes s-maxage, obeyed only by shared caches (CDN/proxy) and it implies public. setMaxAge() targets any cache including the browser, so it is the wrong tool here. setPrivate() would forbid shared caching entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

**Q59.** Where are bundles enabled in a modern Symfony app?  <small>_(Architecture)_</small>

- A. config/bundles.php
- B. config/services.yaml
- C. Manually in src/Kernel.php

??? success "Answer Q59"
    **A**

    config/bundles.php maps each bundle class to the environments where it is enabled; the kernel reads it via MicroKernelTrait.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles.html)

**Q60.** Which of these is NOT a real FormEvents constant?  <small>_(Forms)_</small>

- A. FormEvents::PRE_VALIDATE
- B. FormEvents::PRE_SET_DATA
- C. FormEvents::PRE_SUBMIT
- D. FormEvents::POST_SUBMIT

??? success "Answer Q60"
    **A**

    There is no PRE_VALIDATE (nor POST_VALIDATE) in FormEvents. The five constants are PRE_SET_DATA, POST_SET_DATA, PRE_SUBMIT, SUBMIT and POST_SUBMIT; validation is simply a POST_SUBMIT listener registered by the validator extension.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/FormEvents.php)

**Q61.** A #[MapRequestPayload] argument fails validation. Which status is thrown?  <small>_(Controllers)_</small>

- A. 422 Unprocessable Entity (400 if the body itself is malformed)
- B. 500 Internal Server Error
- C. 200 with a null argument

??? success "Answer Q61"
    **A**

    RequestPayloadValueResolver deserializes then validates; validation errors throw UnprocessableEntityHttpException (422).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html#mapping-the-whole-request-payload)

**Q62.** An optional text field with a custom transformer reports 'invalid' whenever it is left blank. What is the likely cause?  <small>_(Forms)_</small>

- A. reverseTransform('') runs the parser on an empty string and throws TransformationFailedException; guard for ''/null and return the empty model value first
- B. The field needs a NotBlank constraint removed
- C. transform() must return null for empty values
- D. Model transformers cannot handle optional fields

??? success "Answer Q62"
    **A**

    An empty submission arrives as '' (or null) at reverseTransform(); if you parse it instead of short-circuiting, you raise a spurious TransformationFailedException and the field is marked invalid. Guard the first line for emptiness and return the model's empty value (null/[]/0). This is a format-handling bug, not a validation constraint issue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q63.** Why is HTML auto-escaping insufficient when a value is placed inside a `<script>` block or a URL attribute?  <small>_(PHP & Web Security)_</small>

- A. Each context needs its own encoding (js/url); HTML escaping does not neutralise script or URL payloads
- B. HTML escaping is always sufficient everywhere
- C. Because Twig disables escaping inside script tags
- D. Because URLs cannot contain user data at all

??? success "Answer Q63"
    **A**

    XSS defence must be context-aware: a value safe as HTML text can still break out inside JavaScript or a URL, so you need the js or url escaping strategy there. HTML escaping is not universally sufficient, Twig does not silently disable escaping in script tags, and URLs routinely carry user data (which must be url-encoded). Misconception: treating one escaping strategy as a cure-all across all output contexts.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html)

**Q64.** You add the alias App\Report\ReporterInterface: '@App\Report\Missing' but the target service does not exist. What happens?  <small>_(Dependency Injection)_</small>

- A. A compile-time error — an alias to a non-existent target breaks the build; it is not a silent null
- B. The interface silently resolves to null at runtime
- C. The alias is quietly ignored
- D. A ServiceLocator is injected in its place

??? success "Answer Q64"
    **A**

    An alias must point at an existing service id; a dangling alias fails the container build. Optional dependencies use nullable constructor args or NULL_ON_INVALID_REFERENCE, not a broken alias. The misconception is expecting a missing target to become null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/alias_private.html)

**Q65.** How does EventDispatcher store and order listeners internally?  <small>_(Architecture)_</small>

- A. It keeps listeners[eventName][priority][] and sorts by priority descending on first dispatch, memoising the sorted list until a listener is added/removed
- B. It sorts listeners alphabetically by class name on every dispatch
- C. It runs listeners in random order to prevent coupling

??? success "Answer Q65"
    **A**

    Internally the dispatcher stores listeners keyed by event name then priority. On the first dispatch of an event it sorts by priority descending (higher first; equal priorities preserve registration order) and caches the result in a sorted[] map, invalidated only when listeners change. This memoisation keeps repeated dispatches cheap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php)

**Q66.** During matching, when is the host constraint checked?  <small>_(Routing)_</small>

- A. Before the path regex
- B. After the controller runs
- C. Only during URL generation
- D. Never; host is informational

??? success "Answer Q66"
    **A**

    matchCollection() tests the compiled host regex against RequestContext::getHost() first; only if it matches does it test the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q67.** True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled.  <small>_(Miscellaneous)_</small>

- A. True
- B. False

??? success "Answer Q67"
    **B**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q68.** True or false: {# ... #} comments are removed at compile time and never reach the browser.  <small>_(Twig)_</small>

- A. True
- B. False

??? success "Answer Q68"
    **A**

    Twig {# #} comments are stripped during compilation and produce no output, unlike HTML <!-- --> comments which are sent to the client. Use {# #} for template notes you do not want leaking to users.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

**Q69.** A translation key has no entry for the current locale and no fallback. What is rendered?  <small>_(Twig)_</small>

- A. The key string itself
- B. An empty string
- C. A 500 error
- D. null

??? success "Answer Q69"
    **A**

    The translator returns the untranslated message id when no translation is found.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html)

**Q70.** A test writes $client->request('GET', '/admin', ['PHP_AUTH_USER' => 'admin', 'PHP_AUTH_PW' => 'secret']) and authentication fails. What is wrong?  <small>_(Testing)_</small>

- A. Server params are the 5th argument of request(); the 3rd is $parameters (query/POST). The auth belongs in $server
- B. PHP_AUTH_USER must be HTTP_PHP_AUTH_USER
- C. Basic auth cannot be tested with the client at all
- D. You must call loginUser() instead; server params never carry credentials

??? success "Answer Q70"
    **A**

    request(string $method, string $uri, array $parameters = [], array $files = [], array $server = [], ...): the credentials were passed as $parameters (query/POST data) instead of the 5th $server argument. PHP_AUTH_USER is correctly unprefixed, and Basic auth is testable via server params — the position is the bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

**Q71.** A parent declares `serialize(): string`. Is overriding it with `serialize(): never` legal?  <small>_(PHP & Web Security)_</small>

- A. Yes — never is the bottom type and is a valid covariant return
- B. No — never is unrelated to string
- C. No — never can only be used on void methods
- D. Only if the parent also returns never

??? success "Answer Q71"
    **A**

    never is the bottom type: a method that always throws or exits satisfies any return contract, so `: never` is a valid covariant narrowing of `: string`. never is not unrelated (it is a subtype of every type), it is not restricted to void methods, and the parent need not also return never. Misconception: thinking never only marks infinite loops/exit; it is a genuine type in the variance lattice.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

**Q72.** You call validate($obj, groups: ['edit']). Which constraints run?  <small>_(Validation)_</small>

- A. Only constraints assigned to the 'edit' group
- B. The 'Default' group plus the 'edit' group
- C. All constraints, regardless of group
- D. Only the 'Default' group

??? success "Answer Q72"
    **A**

    Only the requested groups run. Passing a custom group does NOT implicitly include Default; list ['Default', 'edit'] if you need both.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q73.** What does $event->stopPropagation() do?  <small>_(Architecture)_</small>

- A. Prevents the remaining listeners of this event from running
- B. Cancels the whole request
- C. Removes the listener permanently

??? success "Answer Q73"
    **A**

    It sets a flag the dispatcher checks before each listener; only the current event's remaining listeners are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/event_dispatcher.html)

**Q74.** A command returns 300 as its exit code. What does the process actually exit with?  <small>_(Console)_</small>

- A. 44 — exit codes are clamped to 0–255 via % 256 (300 % 256 = 44)
- B. 300 — Symfony passes it through unchanged
- C. 255 — anything above 255 becomes 255
- D. 1 — out-of-range codes fall back to FAILURE

??? success "Answer Q74"
    **A**

    POSIX exit codes are a single byte (0–255), so Symfony normalises out-of-range values with % 256; 300 % 256 = 44. It is not passed through, not capped at 255, and not coerced to FAILURE. By convention a signal-terminated process exits with 128 + signalNumber.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q75.** After ContainerBuilder::compile(), what happens to the parameter bag?  <small>_(Dependency Injection)_</small>

- A. It becomes a read-only FrozenParameterBag
- B. It stays mutable so parameters can change at runtime
- C. It is discarded and every parameter is inlined only
- D. It is serialized into the .env file

??? success "Answer Q75"
    **A**

    During build the ContainerBuilder uses a mutable ParameterBag; compile() freezes it into a FrozenParameterBag, after which parameters are read-only. This is why parameters are compile-time constants — the misconception is expecting to mutate parameters at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-parameters)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
