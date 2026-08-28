# Mock Exam A (Exam Mode)

!!! note "Three independent papers"
    This is **Mock A**. Also try: [Mock B](mock-exam-b.md) · [Mock C](mock-exam-c.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

## 🧠 Pour les nuls

**C'est quoi ?** Un **examen blanc complet** : 75 questions, 90 minutes, sans notes — les conditions exactes de l'examen officiel Symfony 8, sur un échantillon pondéré du même sujet que l'examen réel. Le Mock A est l'une de trois versions indépendantes (A, B, C) tirées de la même banque.

**Pourquoi ça existe ?** Connaître chaque notion séparément ne garantit pas de réussir un examen chronométré de 90 minutes qui mélange tout. Le mock exam entraîne spécifiquement la gestion du temps et l'endurance mentale, en plus des connaissances.

**🏠 Analogie de la vraie vie :** C'est le **concours blanc** que passent les lycéens avant le bac : mêmes conditions, même durée, une note à la fin — pour savoir vraiment où on en est, pas pour apprendre du nouveau contenu.

**Symfony dans la vraie vie :** 75 questions pondérées → même répartition que l'examen réel (Architecture/DI/Sécurité/Messenger plus présents) / 90 minutes chronométrées → même contrainte de temps que le jour J / Score final → indicateur direct de préparation, pas une note scolaire.

**⚠️ Erreur fréquente :** Consulter la réponse dès qu'une question semble difficile, au lieu de la flaguer et d'avancer. Cela fausse complètement le chronométrage et masque le vrai niveau de préparation.

**🧠 Comment le mémoriser :** *« Chronomètre en marche, pas de pause, pas de triche »* — un mock exam fait à moitié (avec pauses ou aide) ne prédit rien sur l'examen réel.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** Why can you not implement `Traversable` directly, and what does `IteratorAggregate::getIterator()` return?  <small>_(PHP & Web Security)_</small>

- A. Traversable is an internal marker interface; getIterator() must return a Traversable (e.g. an Iterator or generator)
- B. Traversable requires five methods; getIterator() returns an array
- C. Traversable is abstract; getIterator() returns void
- D. You can implement Traversable; getIterator() returns a Countable

??? success "Answer Q1"
    **A**

    Traversable is an engine-internal marker (the base of Iterator and IteratorAggregate) that userland cannot implement directly — you implement one of its children. getIterator() must return a Traversable, commonly an Iterator or a generator (via yield). It does not return a plain array, void, or a Countable. Misconception: trying to `implements Traversable` directly, which is a fatal error.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.traversable.php)

**Q2.** Which of the following statements are true about handling file uploads with Symfony forms? (select all that apply)  <small>_(Forms)_</small>

- A. form_start() adds enctype="multipart/form-data" automatically, but only when the form contains a file field
- B. getClientOriginalName() and getClientMimeType() return untrusted, client-supplied values
- C. An unmapped FileType field is still validated, and you read it via $form->get('x')->getData()
- D. FileType fields provide the upload as a plain string path to the temporary file
- E. Setting maxSize on the File constraint raises PHP's upload_max_filesize ini limit

??? success "Answer Q2"
    **A, B, C**

    Multipart encoding is only set when a file field is present; the client-provided name and MIME type must never be trusted (use guessExtension()/getMimeType() instead); and unmapped fields are validated and fetched with ->get('x')->getData(). FileType yields an UploadedFile object (not a string path), and the File constraint is capped by — it can never override — PHP's upload_max_filesize/post_max_size limits.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q3.** What does the special _format parameter do when matched?  <small>_(Routing)_</small>

- A. Sets the request format, influencing the response Content-Type
- B. Only appears in the URL with no effect
- C. Selects which controller runs
- D. Sets the HTTP method

??? success "Answer Q3"
    **A**

    RouterListener applies _format via Request::setRequestFormat(), driving content negotiation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q4.** What does the expression `trim(...)` produce?  <small>_(PHP & Web Security)_</small>

- A. A Closure wrapping the trim function
- B. The string 'trim'
- C. The trimmed result
- D. A parse error in PHP 8.4

??? success "Answer Q4"
    **A**

    First-class callable syntax (8.1+) turns any callable into a Closure, so trim(...) yields a Closure object. It is not the string 'trim', it does not call trim (no argument is passed), and it is valid syntax in 8.4. It is the type-safe modern replacement for 'trim' or Closure::fromCallable('trim'). Misconception: reading `(...)` as an immediate call.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.first_class_callable_syntax.php)

**Q5.** In Symfony 8 (PHP 8.4), what does the container inject for a concrete service marked lazy: true?  <small>_(Dependency Injection)_</small>

- A. A native lazy ghost — an uninitialized instance whose constructor runs in place on first use
- B. A subclass generated by friendsofphp/proxy-manager
- C. null, replaced by the real instance on first get()
- D. A ServiceLocator wrapping the service

??? success "Answer Q5"
    **A**

    Symfony 8 runs on PHP 8.4, whose engine provides native lazy objects. For a concrete class the dumped container creates a lazy ghost: the very same instance, handed out uninitialized, with the real constructor run in place on first state access. No external proxy library is involved.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/lazy_services.html)

**Q6.** Which server parameters are NOT written with the HTTP_ prefix? (choose 3)  <small>_(Testing)_</small>

- A. CONTENT_TYPE
- B. PHP_AUTH_USER
- C. HTTPS
- D. HTTP_ACCEPT
- E. HTTP_X_REQUESTED_WITH

??? success "Answer Q6"
    **A, B, C**

    Following CGI conventions, request headers are exposed as HTTP_<NAME>, but CONTENT_TYPE, HTTPS, PHP_AUTH_USER and PHP_AUTH_PW are special-cased with no prefix. HTTP_ACCEPT and HTTP_X_REQUESTED_WITH are ordinary headers and keep the prefix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

**Q7.** 401 Unauthorized means the user is authenticated but lacks permission. True or false?  <small>_(HTTP)_</small>

- A. False
- B. True

??? success "Answer Q7"
    **A**

    401 actually means *not authenticated* — credentials are missing or invalid, and the server must send a WWW-Authenticate header. The 'authenticated but not allowed' case is 403 Forbidden, where re-authenticating will not help. The name 'Unauthorized' is a long-standing misnomer.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401)

**Q8.** Which of the following statements are true about the Symfony HttpClient component? (select all that apply)  <small>_(HTTP)_</small>

- A. request() is lazy/asynchronous — the transfer only completes when you first read the status, headers or content
- B. getContent() and toArray() throw on 3xx–5xx responses by default, while getStatusCode() never throws
- C. MockHttpClient with MockResponse lets you test HTTP interactions without any network access
- D. You should type-hint the concrete CurlHttpClient class in your services for best performance
- E. Options defined on a scoped client apply to every request the client makes, whatever the URL

??? success "Answer Q8"
    **A, B, C**

    Responses are lazy so firing several requests before reading gives free concurrency; the content readers throw HTTP exceptions by default (pass false / throw: false to read error bodies) while getStatusCode() is always safe; and MockHttpClient keeps tests offline. You should depend on the HttpClientInterface contract, not a concrete transport, and scoped-client options only apply to URLs matching the scope/base URI.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html)

**Q9.** Which kernel event lets a listener turn an exception into a Response?  <small>_(Controllers)_</small>

- A. kernel.exception (ExceptionEvent)
- B. kernel.view
- C. kernel.terminate

??? success "Answer Q9"
    **A**

    ExceptionEvent listeners can call setResponse(); otherwise the error controller renders the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/events.html#kernel-exception)

**Q10.** How are route conditions executed at request time?  <small>_(Routing)_</small>

- A. As pre-compiled PHP closures baked into the dumped matcher (not runtime eval)
- B. Via eval() of the expression string on each request
- C. By calling a Twig template
- D. They are evaluated once at boot and cached as booleans

??? success "Answer Q10"
    **A**

    The framework compiles all conditions ahead of time through ExpressionLanguage and the routing ExpressionLanguageProvider, so the dumped matcher contains compiled closures. UrlMatcher::handleRouteRequirements() runs them after host/path match — no per-request eval, and they cannot be reduced to a constant because they depend on the live request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Matcher/UrlMatcher.php)

**Q11.** A class defines `save()`, and a trait it uses also defines `save()`. A developer expects the trait's version to run but gets the class's. Why?  <small>_(PHP & Web Security)_</small>

- A. The class's own method takes precedence over any trait method
- B. It is undefined behaviour
- C. The trait method should have won; this is a bug
- D. A fatal error should have occurred

??? success "Answer Q11"
    **A**

    Trait precedence is class > trait > inherited parent, so the class's own save() always overrides the trait's. This is defined, expected behaviour, not a bug or error. To use the trait's version, alias it with `as` (e.g. `Trait::save as saveViaTrait;`). Misconception: assuming a trait method overrides the host class's own method — it only overrides inherited ones.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

**Q12.** With #[Cache(lastModified: 'post.getUpdatedAt()')], when can a 304 be returned?  <small>_(HTTP Caching)_</small>

- A. Before the controller body runs, during kernel.controller_arguments
- B. Only after the controller has fully rendered the response
- C. Only inside a kernel.terminate listener
- D. Never — expressions cannot short-circuit

??? success "Answer Q12"
    **A**

    CacheAttributeListener evaluates the expression on CONTROLLER_ARGUMENTS (priority 10) and, if the request is up to date, replaces the controller so a 304 is returned without running the body. That is precisely the CPU/render saving the model exists for; it does not wait for RESPONSE or terminate.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

**Q13.** Which class collects the `console.command` tags and builds the lazy command loader?  <small>_(Console)_</small>

- A. AddConsoleCommandPass, which builds a ContainerCommandLoader (name → service id)
- B. ContainerBuilder::compile() instantiates each command eagerly
- C. The Kernel's registerCommands() method scans the filesystem
- D. CommandCompilerPass, building an ArrayCommandLoader

??? success "Answer Q13"
    **A**

    Symfony\\Component\\Console\\DependencyInjection\\AddConsoleCommandPass gathers every service tagged console.command and constructs a ContainerCommandLoader mapping each command name to its service id, so a command is instantiated only when its name is invoked. There is no CommandCompilerPass, commands are not instantiated eagerly at compile time, and Symfony 8 does not scan the filesystem for commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q14.** Two passes are registered in the same phase with priorities 10 and 100. Which runs first?  <small>_(Dependency Injection)_</small>

- A. The priority-100 pass — higher priority runs earlier within a phase
- B. The priority-10 pass runs first
- C. The order is undefined
- D. They run simultaneously

??? success "Answer Q14"
    **A**

    Within a phase, addCompilerPass orders by priority with higher running first. The trap is assuming lower numbers run first (as some other Symfony orderings work); for compiler passes higher priority is earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q15.** What is the key difference between getPreferredFormat() and getAcceptableContentTypes()? (choose one)  <small>_(HTTP)_</small>

- A. getPreferredFormat() returns a Symfony format name (e.g. 'json'); getAcceptableContentTypes() returns raw MIME types
- B. They are aliases returning the same value
- C. getPreferredFormat() returns MIME types; getAcceptableContentTypes() returns formats
- D. getPreferredFormat() reads Accept-Language, not Accept

??? success "Answer Q15"
    **A**

    getPreferredFormat() maps the client's Accept header to a short Symfony format (html, json, xml, csv...), best for a match expression. getAcceptableContentTypes() returns the raw MIME strings ordered by preference. Confusing format names with MIME types is a classic trap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q16.** Which statements describe the DEFAULT login_throttling limiter? (multiple)  <small>_(Security)_</small>

- A. It counts failed attempts per username + IP up to max_attempts per interval
- B. It also enforces a wider limit of 5 × max_attempts per IP across all usernames
- C. A successful login resets the counter
- D. It counts per session ID so proxies are irrelevant
- E. It blocks the IP permanently after the first breach

??? success "Answer Q16"
    **A, B, C**

    DefaultLoginRateLimiter combines two limits: username+IP at max_attempts and IP alone at five times that, so attackers cannot bypass the first limit by spraying usernames. A successful login resets the counters; blocking is only for the configured interval and IP/username based, not session based.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#limiting-login-attempts)

**Q17.** Transparent password rehash on login requires…  <small>_(Security)_</small>

- A. Both migrate_from and a provider implementing PasswordUpgraderInterface
- B. Only migrate_from in security.yaml
- C. Only a PasswordUpgraderInterface provider
- D. Calling password_hash() manually in the controller

??? success "Answer Q17"
    **A**

    migrate_from lets needsRehash() detect the old hash; the PasswordUpgradeBadge triggers PasswordMigratingListener, which persists the new hash via upgradePassword().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q18.** Why redirect after a successful POST (POST-redirect-GET)?  <small>_(Forms)_</small>

- A. So a browser refresh re-fetches a GET instead of re-submitting the form
- B. Because forms cannot render on a POST response
- C. To trigger CSRF validation
- D. It is required for isValid() to return true

??? success "Answer Q18"
    **A**

    Without the redirect, refreshing re-POSTs the data and duplicates side effects. Redirecting lands the browser on a safe GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q19.** A controller passes a variable named `app` to the template. What happens?  <small>_(Twig)_</small>

- A. The local variable shadows the global, so app.user etc. refer to the passed value
- B. Symfony throws because 'app' is reserved
- C. The global always wins and the local value is ignored
- D. Both are merged into a single object

??? success "Answer Q19"
    **A**

    Globals are merged into the render context, so a local variable of the same name shadows the global. Passing your own `app` variable breaks app.user/app.request access inside that template — avoid reusing reserved global names.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#global-variables)

**Q20.** Which API expands ['ROLE_SUPER_ADMIN'] into every role it implies, transitively?  <small>_(Security)_</small>

- A. RoleHierarchyInterface::getReachableRoleNames(array $roles)
- B. UserInterface::getRoles(true)
- C. TokenInterface::getExpandedRoles()
- D. SecurityBundle's RoleExpander service

??? success "Answer Q20"
    **A**

    RoleHierarchy::getReachableRoleNames() walks the configured map recursively and is the very service the RoleHierarchyVoter uses, so results always match isGranted() behaviour. The other methods do not exist in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#hierarchical-roles)

**Q21.** For a property holding a collection of Address OBJECTS, how do you validate each element's own constraints?  <small>_(Validation)_</small>

- A. Put #[Assert\Valid] on the property; it cascades into every element
- B. Use #[Assert\All([new Assert\Valid()])]
- C. Use #[Assert\Collection]
- D. Nothing is needed; object collections cascade automatically

??? success "Answer Q21"
    **A**

    For a collection of objects, a single #[Assert\\Valid] on the property cascades into each element. All([new Valid()]) is a redundant anti-pattern; All is for applying scalar constraints to elements.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Valid.html)

**Q22.** Which statements about SYMFONY_DEPRECATIONS_HELPER modes are correct? (select all that apply)  <small>_(Testing)_</small>

- A. weak keeps collecting and reporting deprecations but never fails the build
- B. disabled=1 turns the handler off entirely, so nothing is collected or reported
- C. A committed baseline file makes only NEW deprecations fail, ignoring the known ones it records
- D. weak and disabled=1 are equivalent — both hide deprecations completely
- E. max[self]=0 fails the build on deprecations from any bucket, including indirect ones

??? success "Answer Q22"
    **A, B, C**

    weak still prints the grouped deprecation report and only removes the failure threshold, whereas disabled=1 stops collection completely, so the two are not equivalent. A baseline records currently-known deprecations so later runs fail only on new ones. max[self]=0 constrains only the self bucket — max[total]=0 is the mode that fails on any bucket.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration)

**Q23.** What does the default ErrorListener actually do when it handles a kernel.exception?  <small>_(Architecture)_</small>

- A. It logs the exception, forwards to the error controller as a sub-request, and sets the resulting Response on the event
- B. It immediately calls exit() with the HTTP status code
- C. It re-throws the exception so PHP's default handler renders it

??? success "Answer Q23"
    **A**

    ErrorListener (priority -128) logs the throwable, forwards to the error_controller (ErrorController) as a sub-request whose response carries the status/headers from HttpExceptionInterface, and sets that response on the ExceptionEvent. Because it runs last, any higher-priority listener that already set a response wins and ErrorListener does nothing.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/ErrorListener.php)

**Q24.** To reference service('x') in a routing condition, service x must…  <small>_(Routing)_</small>

- A. Be tagged routing.condition_service (e.g. via #[AsRoutingConditionService])
- B. Be public
- C. Implement RouterInterface
- D. Extend AbstractController

??? success "Answer Q24"
    **A**

    Only services tagged routing.condition_service are exposed to the routing expression language. Visibility/base class are irrelevant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q25.** A developer uses $violations[0] (works) but array_map(..., $violations) (fails). Why?  <small>_(Validation)_</small>

- A. The list is a Countable/IteratorAggregate/ArrayAccess object, not a plain array; use foreach/count() or iterator_to_array()
- B. The list is null when empty
- C. array_map only works on associative arrays
- D. Violations are stored as strings

??? success "Answer Q25"
    **A**

    ConstraintViolationList implements ArrayAccess (so [0] works) but is not an array. Iterate it, call count(), use findByCodes(), or convert via iterator_to_array() for array functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q26.** Which construct includes a template AND lets you override its blocks?  <small>_(Twig)_</small>

- A. {% embed %}
- B. {% include %}
- C. {% use %}
- D. {% extends %}

??? success "Answer Q26"
    **A**

    embed combines include with extends-style block overriding, ideal for configurable components with slots.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/embed.html)

**Q27.** Which of the following statements are true about the test client returned by static::createClient()? (select all that apply)  <small>_(Testing)_</small>

- A. It is a KernelBrowser (extending AbstractBrowser) that calls the kernel in-process, not over the network
- B. It does not follow redirects by default; you must call followRedirect() or followRedirects()
- C. request() returns a Crawler; the Response is fetched separately via $client->getResponse()
- D. It performs real HTTP requests against a running web server
- E. request() returns the Response object directly

??? success "Answer Q27"
    **A, B, C**

    The client is a KernelBrowser hitting the kernel in-process with a cookie jar and history, so no web server or network round-trip is involved. Navigation methods like request() return a Crawler — the Response must be read via getResponse() — and redirects are only followed after calling followRedirect() (once) or followRedirects() (toggle), never automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#making-requests)

**Q28.** True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled.  <small>_(Miscellaneous)_</small>

- A. True
- B. False

??? success "Answer Q28"
    **B**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q29.** Which are valid ways to override parts of Symfony or a third-party bundle in an application? (select all that apply)  <small>_(Architecture)_</small>

- A. Override a bundle template by placing a file with the same path under templates/bundles/<BundleName>/
- B. Override a service by decorating it or replacing its definition, e.g. via a compiler pass
- C. Override translations by defining the same key in the application's translations/ directory, which wins over the bundle's
- D. Create a child bundle and point getParent() at the bundle you want to override
- E. Copy the entire bundle into src/ so your copy shadows the vendor code

??? success "Answer Q29"
    **A, B, C**

    Per-resource overriding is the supported model: templates placed under templates/bundles/<BundleName>/ shadow the bundle's own, application translations take precedence over bundle translations, and services can be redefined, decorated or altered through a compiler pass. Bundle inheritance via getParent() has been removed, and copying whole bundles into src/ is not an override mechanism at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/override.html)

**Q30.** Which statements about PHP 8.4 native lazy objects as used by Symfony are true? (select all that apply)  <small>_(Dependency Injection)_</small>

- A. A lazy ghost is initialized in place, so it is === the initialized object
- B. final classes can be lazy ghosts, since no subclass is generated
- C. First interaction with the object's state triggers initialization
- D. Laziness requires installing friendsofphp/proxy-manager
- E. A lazy service's constructor never runs, even when used

??? success "Answer Q30"
    **A, B, C**

    Native ghosts are created from the class itself: identity is preserved, final classes work (unlike old inheritance-based proxies), and the engine runs the initializer on first state access. No external proxy package is needed, and the constructor does run — just later.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.lazy-objects.php)

**Q31.** A command's execute() throws a RuntimeException. What is the event sequence?  <small>_(Console)_</small>

- A. COMMAND → ERROR → TERMINATE (TERMINATE still runs after ERROR)
- B. COMMAND → TERMINATE only (ERROR is skipped for RuntimeException)
- C. ERROR → COMMAND → TERMINATE
- D. ERROR only; the process aborts before TERMINATE

??? success "Answer Q31"
    **A**

    COMMAND fires before execution; the thrown Throwable triggers ERROR (ConsoleErrorEvent, where a listener can change the exit code or swap the exception); TERMINATE always fires last, even after an error. ERROR never runs before COMMAND, and it does not suppress TERMINATE.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q32.** You extend AbstractController and override getSubscribedServices() to add a `ReportGenerator`. Which body keeps `render()`, `getUser()`, etc. working?  <small>_(Controllers)_</small>

- A. return [...parent::getSubscribedServices(), ReportGenerator::class];
- B. return [ReportGenerator::class];
- C. return array_merge([ReportGenerator::class]); // no parent call
- D. parent::getSubscribedServices(); return [ReportGenerator::class];

??? success "Answer Q32"
    **A**

    The subscription list fully replaces the inherited one, so you must spread `parent::getSubscribedServices()` alongside your own entry. Returning only your service drops router/twig/security and breaks every helper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q33.** A controller does its work but has no return statement (returns null) and no kernel.view listener handles it. What happens?  <small>_(Architecture)_</small>

- A. The kernel dispatches kernel.view; since no response is set, it throws ControllerDoesNotReturnResponseException
- B. The kernel silently sends an empty 200 response
- C. A fatal PHP TypeError is raised before any event fires

??? success "Answer Q33"
    **A**

    After the controller runs, handleRaw() checks whether the return value is a Response; if not, it dispatches kernel.view carrying the value. If no listener calls setResponse(), the kernel throws ControllerDoesNotReturnResponseException (a LogicException) with the familiar \"The controller must return a Response object but it returned null\" message. The fix is to return a real Response or register a view listener.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html)

**Q34.** A #[IsGranted] check fails for an unauthenticated user. What happens?  <small>_(Security)_</small>

- A. The entry point starts authentication (e.g. login redirect)
- B. An immediate 403 is always returned
- C. A 404 is returned
- D. The request continues unrestricted

??? success "Answer Q34"
    **A**

    An AccessDeniedException for an unauthenticated user is converted to the entry point response; an authenticated-but-unauthorized user gets a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#access-control)

**Q35.** A constraint declared without any explicit 'groups' option belongs to which validation group?  <small>_(Validation)_</small>

- A. The special 'Default' group
- B. No group at all, so it is never validated
- C. A group named after the property
- D. The 'Strict' group

??? success "Answer Q35"
    **A**

    Every constraint with no explicit groups is placed in the Default group, which is the group used when you call validate() without specifying groups.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

**Q36.** What does #[AutowireIterator('app.handler')] on an iterable $handlers argument inject?  <small>_(Dependency Injection)_</small>

- A. An iterable of all app.handler-tagged services, ordered by descending priority
- B. A ServiceLocator keyed by name
- C. Only the single highest-priority handler
- D. An array of the tag's attribute sets

??? success "Answer Q36"
    **A**

    #[AutowireIterator] is the attribute form of tagged_iterator: it injects an iterable of the instantiated tagged services, ordered by descending priority. #[AutowireLocator] would give the lazy keyed locator; the attribute does not filter down to one service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q37.** Which statements about AbstractController are correct? (select all that apply)  <small>_(Controllers)_</small>

- A. Extending AbstractController is optional — any callable can serve as a controller
- B. Its helpers get their services from a lazy service locator whose entries are listed in getSubscribedServices()
- C. Its helper methods like render() and redirectToRoute() are protected, usable only from within the controller
- D. It injects the full service container, so $this->container->get() can fetch any service in the app
- E. Extending it is required for constructor autowiring to work in a controller

??? success "Answer Q37"
    **A, B, C**

    AbstractController is optional convenience built on the service subscriber pattern: a lazy locator, scoped to the services declared in getSubscribedServices(), backs its protected helper methods. The container it holds is that limited locator, not the full application container, and autowiring works for any controller registered as a service — your own dependencies should be constructor-injected regardless of the base class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

**Q38.** How are application service IDs written in modern Symfony?  <small>_(Architecture)_</small>

- A. As the fully-qualified class name (FQCN)
- B. As lowercase dotted strings only
- C. As random UUIDs

??? success "Answer Q38"
    **A**

    The service id is the FQCN; autowiring matches type-hints to these ids.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q39.** What is the default phase for a compiler pass registered without one?  <small>_(Dependency Injection)_</small>

- A. TYPE_BEFORE_OPTIMIZATION
- B. TYPE_OPTIMIZE
- C. TYPE_REMOVE
- D. TYPE_AFTER_REMOVING

??? success "Answer Q39"
    **A**

    PassConfig runs passes in phase order; unspecified passes run in the before-optimization phase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q40.** A TwigFilter is declared with needs_environment: true. What changes about the callable?  <small>_(Twig)_</small>

- A. Twig passes the Environment as the first argument, shifting the user arguments right
- B. Nothing changes; it is only documentation metadata
- C. The filter can only be used inside {% apply %} blocks
- D. The callable must return a Twig\Environment

??? success "Answer Q40"
    **A**

    needs_environment injects Twig\Environment as the first callable argument (and needs_context injects the render context array), so your declared parameters come after it. Forgetting this argument shift is a common cause of TypeErrors when writing extensions.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

**Q41.** Which component copies the matcher's output parameters into $request->attributes?  <small>_(Routing)_</small>

- A. RouterListener, on the kernel.request event
- B. ControllerResolver, when resolving _controller
- C. The UrlMatcher itself writes directly to the Request
- D. ArgumentResolver, on kernel.controller

??? success "Answer Q41"
    **A**

    UrlMatcher::match() returns an array (route defaults + captured placeholders + _route/_route_params); RouterListener, a kernel.request subscriber, copies each entry into the request attribute bag. ControllerResolver and ArgumentResolver then consume _controller and the args later.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/RouterListener.php)

**Q42.** True or False: PHPUnit creates a fresh instance of the test class for every test method, so state set in one test does not leak into another.  <small>_(Testing)_</small>

- A. True
- B. False

??? success "Answer Q42"
    **A**

    PHPUnit reflects over the TestCase subclass and, for each test method, builds a new instance, runs setUp(), the test, then tearDown(). Instance properties therefore never carry over between test methods; only static properties (which you should avoid) can leak state.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html)

**Q43.** Which of the following statements are true about the Symfony Process component? (select all that apply)  <small>_(Miscellaneous)_</small>

- A. new Process(['git', 'log', $input]) auto-escapes each array element, so $input cannot inject shell syntax
- B. The default process timeout is 60 seconds; setTimeout(null) disables it
- C. mustRun() throws a ProcessFailedException when the process exits with a non-zero code
- D. Process::fromShellCommandline() escapes interpolated variables, making it safe with untrusted input
- E. run() returns the process standard output as a string

??? success "Answer Q43"
    **A, B, C**

    The array constructor escapes every argument, the timeout defaults to 60 seconds (nullable to disable), and mustRun() throws ProcessFailedException on failure where run() only returns the exit code. fromShellCommandline() runs a raw string through the shell with no escaping (a command-injection risk), and stdout is read via getOutput(), not from run().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/process.html)

**Q44.** Which statements about resettable services are true? (select all that apply)  <small>_(Dependency Injection)_</small>

- A. Implementing Symfony\Contracts\Service\ResetInterface autoconfigures the kernel.reset tag
- B. Only services already instantiated during the request/message get reset
- C. The messenger:consume worker resets services between messages unless --no-reset is passed
- D. Resetting replaces the service with a brand-new instance
- E. A service must be public to be resettable

??? success "Answer Q44"
    **A, B, C**

    Autoconfiguration tags ResetInterface implementors with kernel.reset; the resetter only touches initialized services; and Messenger workers reset between messages by default (--no-reset opts out). Reset calls a method on the same instance — it does not rebuild it — and visibility is irrelevant since the resetter receives the services internally.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/dic_tags.html#kernel-reset)

**Q45.** How do Security's AccessDeniedException and HttpKernel's AccessDeniedHttpException differ?  <small>_(Architecture)_</small>

- A. AccessDeniedHttpException implements HttpExceptionInterface (→ 403 directly); AccessDeniedException is a Security exception the firewall translates to 403 or a redirect to login
- B. They are aliases of the same class in different namespaces
- C. AccessDeniedException already carries a 403 status code via HttpExceptionInterface

??? success "Answer Q45"
    **A**

    They are different classes. Symfony\\Component\\HttpKernel\\Exception\\AccessDeniedHttpException implements HttpExceptionInterface and yields a 403 through the normal error flow. Symfony\\Component\\Security\\Core\\Exception\\AccessDeniedException is a Security exception that does NOT implement HttpExceptionInterface; the firewall's exception listener catches it and turns it into a 403 (or a redirect to the login page for unauthenticated users).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

**Q46.** Which of the following statements are true about the Symfony Lock component? (select all that apply)  <small>_(Miscellaneous)_</small>

- A. acquire() is non-blocking by default: it returns false immediately when the lock is already held
- B. FlockStore and SemaphoreStore only guarantee mutual exclusion on a single machine
- C. Locks have a TTL (300 seconds by default), and long jobs must call refresh() to extend it
- D. acquire() throws a LockConflictedException whenever the lock is already held
- E. A FlockStore is a safe choice to serialise a cron job across multiple servers

??? success "Answer Q46"
    **A, B, C**

    The default acquire(false) returns a plain false when the resource is busy, local stores (flock/semaphore) never protect across machines, and the TTL expires mid-job unless refresh() extends it. Non-blocking acquire() does not throw on contention (only blocking acquisition can end in LockConflictedException), and multi-server exclusion needs a shared store such as Redis or a database.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/lock.html)

**Q47.** A user with a very long passphrase can change the trailing characters and still log in. Which hasher is in use and why?  <small>_(Security)_</small>

- A. bcrypt — it truncates input at 72 bytes, so bytes beyond that are ignored
- B. sodium — Argon2id trims trailing whitespace
- C. auto — it hashes only the first word of the input
- D. pbkdf2 — it lowercases the input before hashing

??? success "Answer Q47"
    **A**

    bcrypt has a hard 72-byte input limit; any bytes past 72 are silently ignored, so two passphrases sharing the first 72 bytes verify identically. Very long passphrases therefore lose entropy under bcrypt. sodium (Argon2id) has no such truncation, which is one reason to prefer it for long secrets. The other options invent behaviour that does not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q48.** ClockInterface::now() returns what type?  <small>_(Miscellaneous)_</small>

- A. A \DateTimeImmutable (a DatePoint)
- B. A Unix timestamp int
- C. A mutable \DateTime
- D. A float of seconds

??? success "Answer Q48"
    **A**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/clock.html)

**Q49.** In configureOptions(), which OptionsResolver call derives one option's value from the values of others?  <small>_(Forms)_</small>

- A. setNormalizer('opt', fn (Options $o, $value) => ...)
- B. setAllowedTypes('opt', 'string')
- C. setRequired('opt')
- D. setDefault('opt', fn () => ...) only

??? success "Answer Q49"
    **A**

    setNormalizer() receives the resolved Options plus the raw value, letting one option depend on others (e.g. force expanded when multiple is false). setAllowedTypes validates a type, setRequired marks an option mandatory, and a default closure cannot read sibling options the way a normalizer can.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/options_resolver.html)

**Q50.** Which PHP function backs Twig's default 'html' escaping strategy?  <small>_(Twig)_</small>

- A. htmlspecialchars() with ENT_QUOTES | ENT_SUBSTITUTE
- B. strip_tags()
- C. htmlentities() with ENT_NOQUOTES
- D. addslashes()

??? success "Answer Q50"
    **A**

    The EscaperRuntime maps 'html' to htmlspecialchars() with ENT_QUOTES|ENT_SUBSTITUTE (encoding single and double quotes and substituting invalid code units). html_attr uses a stricter attribute encoder, js uses \\xNN hex, css uses CSS hex and url uses rawurlencode — each context has its own encoder because escaping is context-specific.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

**Q51.** What does `cache:clear` run, by default, in addition to removing stale cache?  <small>_(Miscellaneous)_</small>

- A. The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata
- B. The database migrations
- C. The Messenger workers
- D. composer install

??? success "Answer Q51"
    **A**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q52.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(Miscellaneous)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q52"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/cache.html#stampede-prevention)

**Q53.** Under FrankenPHP worker mode, a shared service memoizes the current user's preferences in a private array and users start seeing each other's data. What is the idiomatic fix?  <small>_(Dependency Injection)_</small>

- A. Implement ResetInterface (or tag kernel.reset with a method) that clears the memoized array between requests
- B. Nothing — PHP resets all objects after every request
- C. Mark the service lazy: true so it is rebuilt per request
- D. Call cache:clear at the end of every request

??? success "Answer Q53"
    **A**

    In worker runtimes the container — and thus shared service state — survives across requests; the PHP-FPM "everything dies" assumption no longer holds. The reset mechanism exists exactly for this: clear the request-scoped state in reset(). Laziness only defers construction and cache:clear rebuilds compiled artifacts, not in-memory service state.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/dic_tags.html#kernel-reset)

**Q54.** A #[MapRequestPayload] argument fails validation. Which status is thrown?  <small>_(Controllers)_</small>

- A. 422 Unprocessable Entity (400 if the body itself is malformed)
- B. 500 Internal Server Error
- C. 200 with a null argument

??? success "Answer Q54"
    **A**

    RequestPayloadValueResolver deserializes then validates; validation errors throw UnprocessableEntityHttpException (422).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html#mapping-the-whole-request-payload)

**Q55.** Response::HTTP_UNPROCESSABLE_ENTITY corresponds to which numeric code? (choose one)  <small>_(HTTP)_</small>

- A. 422
- B. 400
- C. 409
- D. 429

??? success "Answer Q55"
    **A**

    The constant keeps the RFC 4918 name 'Unprocessable Entity' but is code 422, the correct code for validation errors on a well-formed body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q56.** Which of the following statements are true about the Symfony Serializer? (select all that apply)  <small>_(Miscellaneous)_</small>

- A. serialize() works in two stages: normalizers turn objects into arrays, then an encoder turns the array into a string
- B. #[Groups] attributes only filter properties when a 'groups' key is passed in the serialization context
- C. PropertyNormalizer reads and writes through getters and setters, respecting PropertyAccess
- D. By default, null-valued properties are omitted from the JSON output

??? success "Answer Q56"
    **A, B**

    Serialization is normalize-then-encode, and group filtering is inert until you pass ['groups' => [...]] in the context — without it all readable fields are emitted. PropertyNormalizer accesses properties directly via reflection (ObjectNormalizer is the one using accessors), and null properties are serialized as null unless you enable the skip_null_values context option.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html)

**Q57.** What does app.environment return?  <small>_(Twig)_</small>

- A. The kernel environment string, e.g. 'dev' or 'prod'
- B. The operating-system environment variables
- C. The APP_ENV file path
- D. A boolean debug flag

??? success "Answer Q57"
    **A**

    app.environment is the kernel environment (dev/prod/test); app.debug is the boolean debug flag. They are unrelated to OS env vars.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q58.** Under the unanimous strategy, a voter returns false from voteOnAttribute() for an attribute it does not actually care about. Effect?  <small>_(Security)_</small>

- A. false is ACCESS_DENIED, which blocks access under unanimous; unrelated attributes must be filtered out in supports() so the voter abstains
- B. false is treated as abstain and has no effect on the outcome
- C. false grants access under unanimous
- D. It throws because the attribute is unsupported

??? success "Answer Q58"
    **A**

    Returning false from voteOnAttribute() maps to ACCESS_DENIED, not abstain. Under unanimous a single deny blocks access, so a voter that "says no to what isn't mine" silently breaks authorization. The correct pattern is to reject unrelated attributes/subjects in supports(), which makes the base Voter abstain (ACCESS_ABSTAIN, no effect). abstain and deny are distinct, and an unsupported attribute does not throw.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

**Q59.** A custom collector storing a PDO connection in $this->data breaks profile storage. Why?  <small>_(Miscellaneous)_</small>

- A. $this->data is serialized to storage (via VarDumper's cloner); a live connection/resource is not serializable
- B. PDO is banned from all services
- C. Collectors may only store strings
- D. The data_collector tag rejects objects

??? success "Answer Q59"
    **A**

    Profiles are persisted per token, so $this->data must be serializable — store scalar/array (VarDumper-clonable) data, not live resources like a PDO connection or an entity with a connection. Implement reset() for worker reuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/profiler/data_collector.html)

**Q60.** True or False: UserInterface::getUsername() still exists in Symfony 8.  <small>_(Security)_</small>

- A. True
- B. False

??? success "Answer Q60"
    **B**

    False. getUsername() was replaced by getUserIdentifier() (mandatory since 6.0) and no longer exists on UserInterface in Symfony 8. Use getUserIdentifier() for the login identifier the session stores and refreshUser() reloads from.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

**Q61.** For route app_help at /{_locale}/help, what does generateUrl('app_help', ['_locale' => 'es']) produce?  <small>_(Routing)_</small>

- A. /es/help
- B. /help?_locale=es
- C. /help/es
- D. /en/help

??? success "Answer Q61"
    **A**

    _locale is a real placeholder in the path, so it fills the {_locale} segment giving /es/help — not a query string, and not the default en.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q62.** What is the canonical order of the controller form-handling calls?  <small>_(Forms)_</small>

- A. handleRequest(), then isSubmitted() && isValid(), then getData()
- B. isValid(), then handleRequest()
- C. submit(), then handleRequest()
- D. createView(), then isSubmitted()

??? success "Answer Q62"
    **A**

    handleRequest() inspects the request and submits the form; only then are isSubmitted()/isValid() meaningful, after which getData() holds the model.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q63.** In Symfony 8, how do you allow everyone (including not-logged-in) on a path?  <small>_(Security)_</small>

- A. PUBLIC_ACCESS
- B. IS_AUTHENTICATED_ANONYMOUSLY
- C. ROLE_ANONYMOUS
- D. IS_ANONYMOUS

??? success "Answer Q63"
    **A**

    Anonymous tokens were removed; PUBLIC_ACCESS is the attribute that opts a path out of authentication.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q64.** You create new Response('hi') and set no cache headers. What Cache-Control does ResponseHeaderBag emit by default? (choose one)  <small>_(HTTP)_</small>

- A. no-cache, private
- B. public, max-age=0
- C. no-store
- D. no header is sent at all

??? success "Answer Q64"
    **A**

    When you set no cache directives, ResponseHeaderBag computes a sensible default of 'no-cache, private', so a bare response is never stored by shared caches. Calling setPublic()/setMaxAge()/setSharedMaxAge() changes this. It is not 'no-store', and a Cache-Control header is always present.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

**Q65.** How is a ConstraintValidator subclass wired so you can inject dependencies (e.g. a repository) into it?  <small>_(Validation)_</small>

- A. It is autoconfigured as a service tagged validator.constraint_validator (via ConstraintValidatorInterface), so normal autowiring applies
- B. You must register it manually in services.yaml with a factory
- C. Validators cannot have dependencies
- D. You register a compiler pass for each validator

??? success "Answer Q65"
    **A**

    Implementing ConstraintValidatorInterface (via ConstraintValidator) triggers autoconfiguration with the validator.constraint_validator tag, so validators are services and can have dependencies autowired.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q66.** A higher priority on a tag places the service where in the tagged iterator?  <small>_(Dependency Injection)_</small>

- A. Earlier (tagged collections are sorted by descending priority)
- B. Later
- C. It has no effect on order
- D. Randomly

??? success "Answer Q66"
    **A**

    Tagged services are ordered by descending priority, so higher priority comes first.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html#tagged-services-with-priority)

**Q67.** For a mapped CollectionType to call the parent's adder/remover methods, set…  <small>_(Forms)_</small>

- A. by_reference => false
- B. allow_add => false
- C. prototype => false
- D. mapped => false

??? success "Answer Q67"
    **A**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/collection.html)

**Q68.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(Miscellaneous)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q68"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html#handling-circular-references)

**Q69.** What does Process::run() return?  <small>_(Miscellaneous)_</small>

- A. The integer exit code
- B. The stdout as a string
- C. void
- D. A boolean success flag

??? success "Answer Q69"
    **A**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/process.html#usage)

**Q70.** What does AbstractController::forward() do?  <small>_(Controllers)_</small>

- A. Runs another controller in a sub-request and returns its Response, without a new client request
- B. Sends a 302 redirect to another route
- C. Includes a Twig template

??? success "Answer Q70"
    **A**

    forward() dispatches a sub-request through the kernel; the browser URL does not change and no 3xx is sent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#forwarding-to-another-controller)

**Q71.** `$this->addFlash('notice', 'Saved')` is shorthand for which call?  <small>_(Controllers)_</small>

- A. getSession()->getFlashBag()->add('notice', 'Saved')
- B. Setting a response header
- C. Writing a cookie

??? success "Answer Q71"
    **A**

    addFlash() is an AbstractController convenience over the session flash bag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#flash-messages)

**Q72.** Which PSR interface does Symfony's service container implement?  <small>_(Architecture)_</small>

- A. PSR-11 (Container)
- B. PSR-6 (Cache)
- C. PSR-16 (Simple Cache)

??? success "Answer Q72"
    **A**

    Symfony's ContainerInterface extends Psr\\Container\\ContainerInterface (PSR-11).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q73.** How are tagged listeners/subscribers and #[AsEventListener] attributes wired into the dispatcher?  <small>_(Architecture)_</small>

- A. RegisterListenersPass wires them at container compile time, and listener services are instantiated lazily only when their event fires
- B. The kernel calls addListener() for each on every kernel.request
- C. They are registered at runtime the first time getSubscribedEvents() is called

??? success "Answer Q73"
    **A**

    The RegisterListenersPass compiler pass scans services tagged kernel.event_listener/kernel.event_subscriber and #[AsEventListener] attributes and wires them into the dispatcher at compile time. Listeners are registered lazily — the service is only constructed when its event actually fires — which keeps boot cheap. You rarely call addListener() at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/event_dispatcher.html)

**Q74.** How does a recipe auto-register a bundle?  <small>_(Architecture)_</small>

- A. By writing an entry into config/bundles.php
- B. Via an #[AsBundle] attribute
- C. By editing services.yaml

??? success "Answer Q74"
    **A**

    The bundles configurator adds the bundle class to config/bundles.php, which the kernel reads at boot via MicroKernelTrait::registerBundles().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles.html)

**Q75.** Which command runs when you execute `php bin/console` with no arguments?  <small>_(Console)_</small>

- A. list
- B. help
- C. about
- D. debug:container

??? success "Answer Q75"
    **A**

    The Application's default command is `list`, which prints all available commands grouped by namespace. `help` shows usage for a single command and must be given a name; `about` prints an environment summary; `debug:container` is a FrameworkBundle command. The classic trap is to assume `help` is the default — it is not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
