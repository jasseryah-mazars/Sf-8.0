# Mock Exam B (Exam Mode)

!!! note "Three independent papers"
    This is **Mock B**. Also try: [Mock A](mock-exam.md) · [Mock C](mock-exam-c.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

## 🧠 Pour les nuls

**C'est quoi ?** Un **examen blanc complet** : 75 questions, 90 minutes, sans notes — les conditions exactes de l'examen officiel Symfony 8, sur un échantillon pondéré du même sujet que l'examen réel. Le Mock B est l'une de trois versions indépendantes (A, B, C) tirées de la même banque.

**Pourquoi ça existe ?** Connaître chaque notion séparément ne garantit pas de réussir un examen chronométré de 90 minutes qui mélange tout. Le mock exam entraîne spécifiquement la gestion du temps et l'endurance mentale, en plus des connaissances.

**🏠 Analogie de la vraie vie :** C'est le **concours blanc** que passent les lycéens avant le bac : mêmes conditions, même durée, une note à la fin — pour savoir vraiment où on en est, pas pour apprendre du nouveau contenu.

**Symfony dans la vraie vie :** 75 questions pondérées → même répartition que l'examen réel (Architecture/DI/Sécurité/Messenger plus présents) / 90 minutes chronométrées → même contrainte de temps que le jour J / Score final → indicateur direct de préparation, pas une note scolaire.

**⚠️ Erreur fréquente :** Consulter la réponse dès qu'une question semble difficile, au lieu de la flaguer et d'avancer. Cela fausse complètement le chronométrage et masque le vrai niveau de préparation.

**🧠 Comment le mémoriser :** *« Chronomètre en marche, pas de pause, pas de triche »* — un mock exam fait à moitié (avec pauses ou aide) ne prédit rien sur l'examen réel.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** You call $validator->validate(null). What happens?  <small>_(Validation)_</small>

- A. You get back an empty ConstraintViolationListInterface — no error, no TypeError
- B. A TypeError, because null is not an object
- C. A ValidationFailedException is thrown
- D. It returns null

??? success "Answer Q1"
    **A**

    Passing null is legal: the value is wrapped in a node, no class metadata is found, and an empty violation list comes back. Validation is values against constraints, and a bare null carries none. The trap is that a null object silently passes when you expected a required value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q2.** Which statements about Security::login() (SecurityBundle) are correct? (multiple)  <small>_(Security)_</small>

- A. It dispatches the same authentication events as an interactive login (e.g. LoginSuccessEvent)
- B. It accepts extra badges, e.g. new RememberMeBadge()
- C. It returns ?Response — the authenticator's success response, if any
- D. It silently writes a token into TokenStorage without running authenticators
- E. It verifies the user's password before logging in

??? success "Answer Q2"
    **A, B, C**

    login() delegates to the real authenticator pipeline, so badge listeners and events (CheckPassportEvent, LoginSuccessEvent) run exactly as for an interactive login, and the authenticator's onAuthenticationSuccess() response is returned. No credentials are checked — you assert the user is already trusted (e.g. just registered).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#login-programmatically)

**Q3.** Which service does FormInterface::handleRequest() delegate to under FrameworkBundle?  <small>_(Forms)_</small>

- A. HttpFoundationRequestHandler
- B. NativeRequestHandler
- C. FormFactory
- D. RequestStack

??? success "Answer Q3"
    **A**

    With HttpFoundation available, the form's request handler is HttpFoundationRequestHandler; NativeRequestHandler is the fallback when working with PHP superglobals directly.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/HttpFoundation/HttpFoundationRequestHandler.php)

**Q4.** Which method declares the types a form type extension applies to?  <small>_(Forms)_</small>

- A. public static function getExtendedTypes(): iterable
- B. public function getExtendedType(): string
- C. public function configureOptions()
- D. public function getParent(): string

??? success "Answer Q4"
    **A**

    getExtendedTypes() is static and returns an iterable of type FQCNs. It replaced the removed singular getExtendedType().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q5.** During matching, when is the host constraint checked?  <small>_(Routing)_</small>

- A. Before the path regex
- B. After the controller runs
- C. Only during URL generation
- D. Never; host is informational

??? success "Answer Q5"
    **A**

    matchCollection() tests the compiled host regex against RequestContext::getHost() first; only if it matches does it test the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q6.** What is the integer value of VERBOSITY_NORMAL?  <small>_(Console)_</small>

- A. 32
- B. 0
- C. 16
- D. 64

??? success "Answer Q6"
    **A**

    The constants are QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256. NORMAL is 32, not 0 (0 is not used) — memorising this 16/32/64/128/256 ladder is exam-critical.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q7.** Which YAML import type loads #[Route] attributes from a directory in Symfony 8?  <small>_(Routing)_</small>

- A. type: attribute
- B. type: annotation
- C. type: php
- D. type: directory

??? success "Answer Q7"
    **A**

    Attribute route loading uses `type: attribute`; the `annotation` type is gone in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q8.** What is the status of enable_authenticator_manager in Symfony 8?  <small>_(Security)_</small>

- A. Removed — the authenticator system is the only one
- B. Required and must be set to true
- C. Optional, defaults to false
- D. Renamed to authenticator_manager: true

??? success "Answer Q8"
    **A**

    The key existed and was deprecated in 7.x; Symfony 8 removed it entirely because the legacy authentication system is gone.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q9.** A controller runs $security->getUser()->getUserIdentifier() and fatals on some requests. What is the cause?  <small>_(Security)_</small>

- A. On an anonymous request getUser() returns null, so calling a method on null fatals; guard with ?->, ?? or an IsGranted check
- B. getUser() throws an AccessDeniedException for guests
- C. getUserIdentifier() was removed in Symfony 8
- D. TokenStorage is not registered as a service

??? success "Answer Q9"
    **A**

    Security::getUser() returns ?UserInterface — it is null whenever no token holds a user (a truly anonymous request, or a lazy firewall whose token was never read). Dereferencing null is a fatal error. Guard with $user?->…, a ?? fallback, or an earlier #[IsGranted('IS_AUTHENTICATED_FULLY')] / denyAccessUnlessGranted() so $user is guaranteed non-null past that point. getUserIdentifier() is very much part of the 8.0 interface, and getUser() never throws for guests — it simply returns null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q10.** What is the default Process timeout?  <small>_(Miscellaneous)_</small>

- A. 60 seconds
- B. Unlimited
- C. 30 seconds
- D. 300 seconds

??? success "Answer Q10"
    **A**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/process.html#process-timeout)

**Q11.** Why does InputBag (query/request/cookies) reject reading an array where a scalar is expected? (choose one)  <small>_(HTTP)_</small>

- A. InputBag restricts values to scalars/arrays-of-scalars/null and throws BadRequestException on a type mismatch, hardening against malicious nested input
- B. PHP forbids arrays in $_GET
- C. ParameterBag also throws in the same case
- D. It silently casts the array to its first element

??? success "Answer Q11"
    **A**

    InputBag extends ParameterBag but narrows the contract to user-supplied data: get() accepts only scalars/null and raises a BadRequestException (HTTP 400) when handed an unexpected array, blocking parameter-pollution style attacks. A plain ParameterBag (used by attributes) imposes no such restriction. Use all('key') to intentionally read array values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

**Q12.** In the test environment, framework.profiler.collect defaults to…  <small>_(Testing)_</small>

- A. false — profiles are collected only for requests opted in with enableProfiler()
- B. true — every request is profiled automatically
- C. true, but only for redirect responses
- D. It cannot be configured in the test environment

??? success "Answer Q12"
    **A**

    The test profiler config sets collect: false for speed, so profiling is off unless a test calls enableProfiler() before the request. It is fully configurable and is not limited to redirects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#profiler)

**Q13.** Which command prints a bundle's configuration reference tree?  <small>_(Dependency Injection)_</small>

- A. config:dump-reference
- B. debug:container
- C. debug:autowiring
- D. debug:router

??? success "Answer Q13"
    **A**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q14.** When does the Firewall listener run in the kernel lifecycle?  <small>_(Security)_</small>

- A. On kernel.request at priority 8 (after routing), it asks the FirewallMap for the first matching FirewallContext
- B. On kernel.controller, just before the controller is resolved
- C. On kernel.response, after the action has run
- D. On kernel.terminate, asynchronously after the response
- E. On kernel.request but before routing, at the highest priority

??? success "Answer Q14"
    **A**

    The Firewall listener subscribes to kernel.request at priority 8, which runs after the RouterListener (routing), then queries the FirewallMap for the matching FirewallContext and runs its listeners. It is a request-phase concern, not controller/response/terminate, and it deliberately runs after routing so route attributes are available.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall.php)

**Q15.** Which statements about resettable services are true? (select all that apply)  <small>_(Dependency Injection)_</small>

- A. Implementing Symfony\Contracts\Service\ResetInterface autoconfigures the kernel.reset tag
- B. Only services already instantiated during the request/message get reset
- C. The messenger:consume worker resets services between messages unless --no-reset is passed
- D. Resetting replaces the service with a brand-new instance
- E. A service must be public to be resettable

??? success "Answer Q15"
    **A, B, C**

    Autoconfiguration tags ResetInterface implementors with kernel.reset; the resetter only touches initialized services; and Messenger workers reset between messages by default (--no-reset opts out). Reset calls a method on the same instance — it does not rebuild it — and visibility is irrelevant since the resetter receives the services internally.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/dic_tags.html#kernel-reset)

**Q16.** In serialize(), which stage runs first?  <small>_(Miscellaneous)_</small>

- A. The normalizer (object to array), then the encoder (array to string)
- B. The encoder, then the normalizer
- C. Only the encoder runs
- D. They run concurrently

??? success "Answer Q16"
    **A**

    serialize() normalizes the object to an array/scalars, then encodes that to a string. deserialize() reverses it: decode then denormalize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html)

**Q17.** What does #[HasNamedArguments] do on a custom Constraint constructor?  <small>_(Validation)_</small>

- A. Passes attribute arguments as named constructor arguments (typed options)
- B. Marks the constraint as repeatable
- C. Automatically registers the validator service
- D. Enables group sequences for the constraint

??? success "Answer Q17"
    **A**

    #[HasNamedArguments] (Symfony\\Component\\Validator\\Attribute) opts into typed, named-argument construction instead of the legacy options-array style; remember to forward $groups and $payload to parent::__construct().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q18.** In phpunit.dist.xml, how is the bridge's extension registered in PHPUnit 11/12?  <small>_(Testing)_</small>

- A. <extensions><bootstrap class="Symfony\Bridge\PhpUnit\SymfonyExtension"/></extensions>
- B. <listeners><listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener"/></listeners>
- C. <php><extension name="symfony"/></php>
- D. It is auto-registered by Composer; no XML entry is needed

??? success "Answer Q18"
    **A**

    PHPUnit 10+ uses the <extensions><bootstrap .../></extensions> mechanism to load the SymfonyExtension. The old <listeners><listener> (SymfonyTestsListener) approach belongs to PHPUnit 9 and earlier; there is no <php><extension> tag, and the extension is not auto-registered.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

**Q19.** In the Mailer, how does the Envelope differ from the message headers?  <small>_(Miscellaneous)_</small>

- A. The Envelope holds the actual sender/recipients used for the SMTP conversation; headers (From/To) render in the visible message
- B. They are the same object with two names
- C. The Envelope stores the HTML body; headers store attachments
- D. The Envelope is only used for async delivery

??? success "Answer Q19"
    **A**

    Mailer's Envelope (sender + recipients) drives the transport's SMTP exchange, whereas the message headers (From, To, Subject) are what the recipient sees. They can legitimately differ (e.g. bounce address vs visible From), which is a common exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/mailer.html#sending-messages)

**Q20.** What status does RedirectController return when the target route/path is empty?  <small>_(Controllers)_</small>

- A. 410 Gone
- B. 404 Not Found
- C. 302 Found to /

??? success "Answer Q20"
    **A**

    An empty target signals the resource is permanently gone, so the controller responds 410.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

**Q21.** In a Symfony form, how do you tell the validator to validate the bound object with the 'registration' group?  <small>_(Validation)_</small>

- A. Set the form's 'validation_groups' option to ['registration']
- B. Pass the groups to $form->handleRequest()
- C. Call $validator->validate() manually in the controller
- D. Set 'groups' on the form type's constructor

??? success "Answer Q21"
    **A**

    Forms invoke the validator during handleRequest(); the validation_groups option selects which groups run (default ['Default']). It can also be a callback for dynamic group selection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q22.** A parent method is `handle(Cat $c)`. Which override signature is legal under contravariance?  <small>_(PHP & Web Security)_</small>

- A. handle(Animal $c) — widening the parameter is allowed
- B. handle(Kitten $c) — narrowing the parameter
- C. handle(string $c) — an unrelated type
- D. handle() — dropping the parameter

??? success "Answer Q22"
    **A**

    Parameter types are contravariant: a child may accept a wider (more general) type such as Animal, preserving substitutability. Narrowing to Kitten would reject values the parent accepted (illegal), an unrelated type breaks the contract, and dropping a required parameter changes arity. Misconception: applying the covariant (narrowing) rule to parameters — returns narrow, parameters widen.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.variance.php)

**Q23.** After the request locale is set, how does it reach services like the Translator? (choose one)  <small>_(HTTP)_</small>

- A. LocaleAwareListener pushes it into every service implementing LocaleAwareInterface
- B. Each service reads $_SERVER['HTTP_ACCEPT_LANGUAGE'] itself
- C. Twig broadcasts it during template rendering
- D. The Router injects it into the container parameters

??? success "Answer Q23"
    **A**

    LocaleListener sets the request locale; LocaleAwareListener then calls setLocale() on every service tagged/implementing Symfony\\Contracts\\Translation\\LocaleAwareInterface (e.g. the Translator). For a scoped switch you use LocaleSwitcher. Services do not read superglobals.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleAwareListener.php)

**Q24.** Between two requests in a long-running worker runtime, what does the services_resetter service do?  <small>_(Dependency Injection)_</small>

- A. Calls the configured reset method on every kernel.reset-tagged service that was instantiated
- B. Destroys the container and reboots the kernel
- C. Re-runs the constructor of every tagged service
- D. Instantiates all tagged services, then resets them

??? success "Answer Q24"
    **A**

    ServicesResetter iterates only the tagged services that were actually initialized during the request and invokes their configured method(s); the container and the instances themselves survive. Never-instantiated services are skipped so laziness is not defeated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/dic_tags.html#kernel-reset)

**Q25.** Which filter applies sprintf-style formatting in Twig?  <small>_(Twig)_</small>

- A. format
- B. sprintf
- C. printf
- D. interpolate

??? success "Answer Q25"
    **A**

    The format filter wraps vsprintf, e.g. \"%s scored %d\"|format(a, b).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/format.html)

**Q26.** True or false: a method declared public in PHP but annotated @internal is protected by the BC promise.  <small>_(Architecture)_</small>

- A. False
- B. True

??? success "Answer Q26"
    **A**

    False. @internal explicitly removes an element from the BC promise even when it is PHP-public. Such methods/classes can change or disappear in any release, so you must not depend on them. PHP visibility and BC coverage are independent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/contributing/code/bc.html)

**Q27.** With access_decision_manager.strategy set to priority, how is the decision made?  <small>_(Security)_</small>

- A. The first voter that does not abstain decides the outcome
- B. All voters must agree to grant
- C. The majority of grants over denies wins
- D. A single grant is always enough regardless of order

??? success "Answer Q27"
    **A**

    The priority strategy takes the vote of the first (highest-priority) non-abstaining voter as final, letting a high-priority voter short-circuit (e.g. a global "banned user" voter denying before feature voters run). "All must agree" describes unanimous, "majority" describes consensus, and "one grant is enough" describes affirmative.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html#changing-the-access-decision-strategy)

**Q28.** What is the key difference between tagged_iterator and tagged_locator?  <small>_(Dependency Injection)_</small>

- A. tagged_iterator yields already-instantiated services; tagged_locator gives a lazy ServiceLocator built on get()
- B. Both eagerly instantiate every tagged service
- C. tagged_iterator is lazy while tagged_locator is eager
- D. tagged_locator returns raw Definition objects

??? success "Answer Q28"
    **A**

    tagged_iterator injects an iterable of instances (use it when you always iterate all of them), while tagged_locator injects a ServiceLocator that builds each service lazily on get() and is keyed for pick-one-of-many. The trap is swapping their laziness.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q29.** Why must {% extends %} be the first tag, and what can a child template NOT do?  <small>_(Twig)_</small>

- A. A child that extends a parent cannot output markup outside blocks; rendering starts at the root ancestor
- B. Markup outside blocks is allowed and rendered before the parent
- C. extends may appear anywhere; order does not matter
- D. A child can define its own <html> wrapper around the parent

??? success "Answer Q29"
    **A**

    When a template extends another, rendering begins at the root ancestor and walks down, so any top-level text a child writes outside a block is ignored (or errors). extends can be a dynamic expression resolved at runtime, which is why it must be resolvable first. Put all child content inside blocks.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

**Q30.** A controller must extend `AbstractController` to be usable in Symfony 8. True or false?  <small>_(Controllers)_</small>

- A. False
- B. True

??? success "Answer Q30"
    **A**

    Extending `AbstractController` is optional convenience. A controller is any callable returning a Response; a plain invokable class with no base class is perfectly valid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

**Q31.** You tag a service #[AsRoutingConditionService(alias: 'feature_checker')]. How do you call its isEnabled() method in a condition?  <small>_(Routing)_</small>

- A. condition: "service('feature_checker').isEnabled(request)"
- B. condition: "feature_checker.isEnabled(request)"
- C. condition: "@feature_checker.isEnabled(request)"
- D. condition: "container.get('feature_checker').isEnabled(request)"

??? success "Answer Q31"
    **A**

    The alias becomes the argument to the service() function; you then call methods on the returned object and can pass request. There is no bare identifier, @ syntax or container variable in routing expressions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q32.** Which PSRs does Symfony IMPLEMENT (i.e. Symfony objects ARE valid PSR objects)? (choose all that apply)  <small>_(Architecture)_</small>

- A. PSR-6 (Cache pool)
- B. PSR-11 (Container)
- C. PSR-14 (Event Dispatcher)
- D. PSR-20 (Clock)
- E. PSR-3 (Logger)

??? success "Answer Q32"
    **A, B, C, D**

    Symfony implements PSR-6 (Cache pool), PSR-11 (Container), PSR-14 (EventDispatcher), PSR-16 (Simple Cache adapter) and PSR-20 (Clock) — its objects can be handed to any library expecting those interfaces. PSR-3 (Logger) is CONSUMED: Symfony type-hints LoggerInterface so you inject any implementation, but it does not ship the logger itself.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

**Q33.** What is the purpose of asset versioning?  <small>_(Twig)_</small>

- A. Cache busting so browsers refetch changed files
- B. Access control for static files
- C. Minifying assets
- D. Matching routes

??? success "Answer Q33"
    **A**

    Versioning changes the URL when a file changes (static version or a JSON manifest of content hashes) so clients do not serve a stale cached copy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/frontend.html)

**Q34.** What must a controller ultimately produce?  <small>_(Controllers)_</small>

- A. A Response object (or a value converted to one by a kernel.view listener)
- B. An array that Symfony auto-serializes to JSON
- C. A string that becomes the body

??? success "Answer Q34"
    **A**

    If a controller returns a non-Response, the kernel fires ViewEvent; if no listener produces a Response a LogicException is thrown.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

**Q35.** In which order does the renderer try candidate theme blocks?  <small>_(Forms)_</small>

- A. Most specific (unique field id) down to least specific (form_widget)
- B. Least specific to most specific
- C. Alphabetically
- D. Randomly per request

??? success "Answer Q35"
    **A**

    The block-prefix hierarchy is walked from the unique per-field name down to the root form_* block; the first existing block wins.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q36.** Which of the following statements are true about the Symfony Lock component? (select all that apply)  <small>_(Miscellaneous)_</small>

- A. acquire() is non-blocking by default: it returns false immediately when the lock is already held
- B. FlockStore and SemaphoreStore only guarantee mutual exclusion on a single machine
- C. Locks have a TTL (300 seconds by default), and long jobs must call refresh() to extend it
- D. acquire() throws a LockConflictedException whenever the lock is already held
- E. A FlockStore is a safe choice to serialise a cron job across multiple servers

??? success "Answer Q36"
    **A, B, C**

    The default acquire(false) returns a plain false when the resource is busy, local stores (flock/semaphore) never protect across machines, and the TTL expires mid-job unless refresh() extends it. Non-blocking acquire() does not throw on contention (only blocking acquisition can end in LockConflictedException), and multi-server exclusion needs a shared store such as Redis or a database.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/lock.html)

**Q37.** Which method returns the message with its {{ placeholders }} still unresolved?  <small>_(Validation)_</small>

- A. getMessageTemplate()
- B. getMessage()
- C. getParameters()
- D. getCode()

??? success "Answer Q37"
    **A**

    getMessage() returns the interpolated message; getMessageTemplate() keeps the raw template with {{ x }} placeholders, and getParameters() holds the substitution map.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q38.** Which set contains only idempotent methods? (choose one)  <small>_(HTTP)_</small>

- A. GET, PUT, DELETE
- B. GET, POST, PUT
- C. POST, PATCH, DELETE
- D. POST, PUT, PATCH

??? success "Answer Q38"
    **A**

    GET, PUT and DELETE are idempotent (repeating yields the same state); POST and PATCH are not.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)

**Q39.** How is the key of each tagged_locator entry determined?  <small>_(Dependency Injection)_</small>

- A. From an index_by tag attribute, a default_index_method static method (e.g. getName), or #[AsTaggedItem(index:)]
- B. It is always the service id
- C. It is always the class FQCN
- D. It is assigned randomly at compile time

??? success "Answer Q39"
    **A**

    The locator key comes from the index_by tag attribute, a static method named by default_index_method (commonly getName/getDefaultIndexName), or an #[AsTaggedItem(index:)] attribute — not the service id by default. If two services resolve to the same key, the later one silently overwrites the earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q40.** Which UrlGenerator reference types back path() and url() respectively?  <small>_(Twig)_</small>

- A. path() => ABSOLUTE_PATH; url() => ABSOLUTE_URL
- B. path() => RELATIVE_PATH; url() => NETWORK_PATH
- C. Both use ABSOLUTE_URL, differing only in caching
- D. path() => ABSOLUTE_URL; url() => ABSOLUTE_PATH

??? success "Answer Q40"
    **A**

    RoutingExtension calls UrlGenerator::generate() with ABSOLUTE_PATH for path() (a root-relative /path) and ABSOLUTE_URL for url() (scheme + host + path). The generator reads the RequestContext to build the host for absolute URLs.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

**Q41.** Every voter abstains and no access_decision_manager option was changed. What is the decision?  <small>_(Security)_</small>

- A. Denied — allow_if_all_abstain defaults to false for every strategy
- B. Granted — nobody objected
- C. An exception is thrown because no decision could be made
- D. Granted under affirmative, denied under the others

??? success "Answer Q41"
    **A**

    When no voter casts a real vote, all four strategies fall back to the allow_if_all_abstain flag, which defaults to false, so access is denied. No exception is thrown and the strategy choice does not change this default outcome.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html#changing-the-access-decision-strategy)

**Q42.** In an invokable command, `#[Option] array $tags = []` on the __invoke() parameter produces which InputOption mode?  <small>_(Console)_</small>

- A. VALUE_IS_ARRAY (repeatable, e.g. --tags=a --tags=b), optional via the [] default
- B. VALUE_NONE, because arrays are treated as flags
- C. VALUE_REQUIRED with a single string value
- D. It is rejected — arrays are only allowed for arguments

??? success "Answer Q42"
    **A**

    The invokable adapter maps an array-typed #[Option] to VALUE_IS_ARRAY, so the option is repeatable; the [] default makes it optional. A bool would map to VALUE_NONE, a scalar with no default to VALUE_REQUIRED. Arrays are valid for both options and (as the last) arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q43.** What is the key difference between a listener and a subscriber?  <small>_(Architecture)_</small>

- A. A listener is registered against one event; a subscriber declares all the events it handles in getSubscribedEvents()
- B. A subscriber can only handle one event; a listener handles many
- C. Listeners run at runtime while subscribers run at compile time

??? success "Answer Q43"
    **A**

    A listener is a callable attached to a single event name (via #[AsEventListener] or the kernel.event_listener tag). A subscriber implements EventSubscriberInterface and declares all its events (and priorities) in the static getSubscribedEvents() method — handy when one class handles several related events. Both are wired by RegisterListenersPass.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/event_dispatcher.html)

**Q44.** With autoconfiguration disabled, which services.yaml tag correctly registers an extension for FileType?  <small>_(Forms)_</small>

- A. tags: [{ name: form.type_extension, extended_type: Symfony\Component\Form\Extension\Core\Type\FileType }]
- B. tags: [{ name: form.type_extension }]  # extended_type inferred
- C. tags: [{ name: form.type, extended_type: FileType }]
- D. tags: [{ name: form.extension, class: FileType }]

??? success "Answer Q44"
    **A**

    Without autoconfiguration you must both use the form.type_extension tag and supply the extended_type attribute (the FQCN of the extended type) — it is not inferred from getExtendedTypes() in the manual case. form.type is for form types, and form.extension is not a real tag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_form_type_extension.html)

**Q45.** Which constant does forward() pass to HttpKernel::handle(), and what is a consequence for the security firewall?  <small>_(Controllers)_</small>

- A. HttpKernelInterface::SUB_REQUEST — the firewall does not re-authenticate (isMainRequest() is false)
- B. HttpKernelInterface::MASTER_REQUEST — the firewall re-runs
- C. HttpKernelInterface::MAIN_REQUEST — a fresh security context is built
- D. HttpKernelInterface::ASYNC_REQUEST — the request is queued

??? success "Answer Q45"
    **A**

    Sub-requests are dispatched with SUB_REQUEST (the old MASTER_REQUEST constant was removed; MAIN_REQUEST is used for the main request). Because isMainRequest() is false, listeners like the firewall skip re-authentication.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernelInterface.php)

**Q46.** Under the unanimous strategy, one voter denies while another grants. Outcome?  <small>_(Security)_</small>

- A. Access is denied — unanimous grants only if no voter denies
- B. Access is granted — one grant is enough
- C. The tie is resolved by roles
- D. An exception is thrown

??? success "Answer Q46"
    **A**

    unanimous requires that no voter denies. A single ACCESS_DENIED blocks access regardless of grants (unlike affirmative).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q47.** Inside a StreamedResponse callback, code echoes rows and then calls `$response->headers->set('Content-Type', 'text/csv')`. What is wrong?  <small>_(Controllers)_</small>

- A. Headers cannot be changed after output has started; set Content-Type before returning the response
- B. StreamedResponse ignores Content-Type entirely
- C. The callback must return the header array
- D. You must use JsonResponse for CSV

??? success "Answer Q47"
    **A**

    The callback runs at send time; once bytes are flushed the headers are already sent, so header changes are ineffective. Set headers on the StreamedResponse before returning it from the action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#streaming-a-response)

**Q48.** The App\: glob registers a class, and a later named block redefines the same id. Which definition wins?  <small>_(Dependency Injection)_</small>

- A. The later, more specific block overrides the glob for that id
- B. The glob always wins over named blocks
- C. They are merged field-by-field with the glob taking precedence
- D. It raises a duplicate-definition error

??? success "Answer Q48"
    **A**

    Registration order matters: the glob first registers everything, then a later, more specific entry for the same id overrides it. This is the idiomatic way to tweak one autowired service. It is not an error and the glob does not win.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q49.** Which version string should you pass as the second argument of trigger_deprecation()?  <small>_(Architecture)_</small>

- A. The version in which the API was DEPRECATED (e.g. '8.1'), not the current running version
- B. The current installed version at the time the notice fires
- C. The version in which the code will be REMOVED (the next major)

??? success "Answer Q49"
    **A**

    The version argument records when the deprecation was introduced, producing the \"Since <package> <version>: <message>\" format tooling parses. A common mistake is passing the current version, or the removal version — both are wrong. Use the version the API was deprecated in.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q50.** Which of the following statements are true about the Symfony Response object? (select all that apply)  <small>_(HTTP)_</small>

- A. prepare() strips the body for HEAD requests and for 204/304 responses
- B. A freshly created Response gets Cache-Control: no-cache, private by default
- C. send() delegates to sendHeaders() and then sendContent()
- D. $response->headers is a plain HeaderBag with no special cookie handling
- E. makeDisposition() is a method on ResponseHeaderBag

??? success "Answer Q50"
    **A, B, C**

    prepare() normalises the response against the request — including removing the body for HEAD/204/304 — the conservative default Cache-Control is no-cache, private, and send() is sendHeaders() followed by sendContent(). $response->headers is actually a ResponseHeaderBag that manages cookies and normalises Cache-Control, and makeDisposition() lives on HeaderUtils.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#response)

**Q51.** ClockInterface::now() returns what type?  <small>_(Miscellaneous)_</small>

- A. A \DateTimeImmutable (a DatePoint)
- B. A Unix timestamp int
- C. A mutable \DateTime
- D. A float of seconds

??? success "Answer Q51"
    **A**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/clock.html)

**Q52.** A route's condition expression evaluates to false. What is the result?  <small>_(Routing)_</small>

- A. 404 — the route is simply not matched
- B. 403 Forbidden
- C. 405 Method Not Allowed
- D. The controller runs anyway

??? success "Answer Q52"
    **A**

    A false condition means the route does not match; matching continues and may end in a 404. It is not authorization, so it never produces a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q53.** For /blog/{page<\d+>?1}, what does generateUrl('blog_list', ['page' => 3]) produce?  <small>_(Routing)_</small>

- A. /blog/3
- B. /blog
- C. /blog?page=3
- D. /blog/1

??? success "Answer Q53"
    **A**

    The segment is only omitted when the value equals the default (1). Since 3 differs, the generator emits the full /blog/3.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q54.** A UserDto has #[Groups(['read'])] #[SerializedName('full_name')] on $name and #[Ignore] on $passwordHash. What is the JSON when serialized with context ['groups' => ['read']]?  <small>_(Miscellaneous)_</small>

- A. {"full_name":"..."} plus any other read-group fields; passwordHash is omitted
- B. {"name":"...","passwordHash":"..."}
- C. All properties, because groups are ignored during serialization
- D. An empty object, because #[Ignore] hides everything

??? success "Answer Q54"
    **A**

    With the read group in context, only read-group properties are emitted; $name is renamed to full_name by #[SerializedName], and #[Ignore] drops passwordHash entirely regardless of group. Groups are honoured only because they are passed in the context.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html#using-serialization-groups-attributes)

**Q55.** Which features does constructor property promotion support?  <small>_(PHP & Web Security)_</small>

- A. Visibility, readonly, types, defaults and attributes
- B. Only public untyped parameters
- C. Promotion in any method, not just __construct
- D. callable-typed properties

??? success "Answer Q55"
    **A**

    A promoted parameter both declares and assigns the property and may carry visibility, readonly, a type, a default and attributes. It works only in __construct (not arbitrary methods), requires a valid property type (callable is not one), and untyped/public-only is not a limitation. Misconception: thinking promotion is a stripped-down shortcut — it is the full property declaration inline.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.decon.php)

**Q56.** What does the expression %env(int:MAX)% produce?  <small>_(Dependency Injection)_</small>

- A. The value of MAX cast to an integer
- B. The raw string value of MAX
- C. A parameter named int
- D. null when MAX is unset

??? success "Answer Q56"
    **A**

    The int: processor casts the raw env string to an integer. Processors chain right-to-left.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration/env_var_processors.html)

**Q57.** What does `cache:clear` run, by default, in addition to removing stale cache?  <small>_(Miscellaneous)_</small>

- A. The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata
- B. The database migrations
- C. The Messenger workers
- D. composer install

??? success "Answer Q57"
    **A**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q58.** For which HTTP status codes does assertResponseIsSuccessful() pass?  <small>_(Testing)_</small>

- A. Any 2xx status
- B. Only 200
- C. 2xx and 3xx
- D. Only 200 and 204

??? success "Answer Q58"
    **A**

    It asserts the response is in the successful (2xx) range. Use assertResponseStatusCodeSame(n) to check an exact code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#the-assertions)

**Q59.** An authenticator adds a badge that no CheckPassportEvent listener resolves. What happens?  <small>_(Security)_</small>

- A. Passport::checkIfCompletelyResolved() throws, so authentication fails — you cannot forget to validate a badge
- B. The badge is silently ignored and login proceeds
- C. The token is created with the unresolved badge attached
- D. A raw 500 with no security exception is produced

??? success "Answer Q59"
    **A**

    After CheckPassportEvent, the manager calls Passport::checkIfCompletelyResolved(), which throws if any badge was never marked resolved. This is a deliberate safety net: an unregistered/forgotten badge (e.g. a CsrfTokenBadge with no listener) fails authentication as an AuthenticationException rather than letting an unverified credential slip through. It is neither ignored nor attached to a successful token.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Security/Http/Authenticator/Passport)

**Q60.** What is the signature of HttpKernelInterface::handle() and the role of its $catch argument?  <small>_(Architecture)_</small>

- A. handle(Request $request, int $type = self::MAIN_REQUEST, bool $catch = true): Response — with $catch=true, exceptions are caught and turned into a response via kernel.exception; with $catch=false they propagate
- B. handle(Request $request): void — it prints the response directly and $catch controls output buffering
- C. handle(string $env, bool $debug): Response — $catch enables the profiler

??? success "Answer Q60"
    **A**

    The contract is handle(Request, int $type = MAIN_REQUEST, bool $catch = true): Response. handle() wraps the private handleRaw() in a try/catch when $catch is true, so an escaped exception is routed through handleThrowable()/kernel.exception into a Response. With $catch=false (common in sub-requests and tests) the exception simply propagates to the caller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html)

**Q61.** A test writes $client->request('GET', '/admin', ['PHP_AUTH_USER' => 'admin', 'PHP_AUTH_PW' => 'secret']) and authentication fails. What is wrong?  <small>_(Testing)_</small>

- A. Server params are the 5th argument of request(); the 3rd is $parameters (query/POST). The auth belongs in $server
- B. PHP_AUTH_USER must be HTTP_PHP_AUTH_USER
- C. Basic auth cannot be tested with the client at all
- D. You must call loginUser() instead; server params never carry credentials

??? success "Answer Q61"
    **A**

    request(string $method, string $uri, array $parameters = [], array $files = [], array $server = [], ...): the credentials were passed as $parameters (query/POST data) instead of the 5th $server argument. PHP_AUTH_USER is correctly unprefixed, and Basic auth is testable via server params — the position is the bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

**Q62.** Which of the following statements are true about the Symfony Serializer? (select all that apply)  <small>_(Miscellaneous)_</small>

- A. serialize() works in two stages: normalizers turn objects into arrays, then an encoder turns the array into a string
- B. #[Groups] attributes only filter properties when a 'groups' key is passed in the serialization context
- C. PropertyNormalizer reads and writes through getters and setters, respecting PropertyAccess
- D. By default, null-valued properties are omitted from the JSON output

??? success "Answer Q62"
    **A, B**

    Serialization is normalize-then-encode, and group filtering is inert until you pass ['groups' => [...]] in the context — without it all readable fields are emitted. PropertyNormalizer accesses properties directly via reflection (ObjectNormalizer is the one using accessors), and null properties are serialized as null unless you enable the skip_null_values context option.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html)

**Q63.** A controller passes a variable named `app` to the template. What happens?  <small>_(Twig)_</small>

- A. The local variable shadows the global, so app.user etc. refer to the passed value
- B. Symfony throws because 'app' is reserved
- C. The global always wins and the local value is ignored
- D. Both are merged into a single object

??? success "Answer Q63"
    **A**

    Globals are merged into the render context, so a local variable of the same name shadows the global. Passing your own `app` variable breaks app.user/app.request access inside that template — avoid reusing reserved global names.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#global-variables)

**Q64.** Which composer flag excludes require-dev packages when deploying to production?  <small>_(Miscellaneous)_</small>

- A. --no-dev
- B. --prod
- C. --production
- D. --optimize

??? success "Answer Q64"
    **A**

    `composer install --no-dev` skips require-dev packages (profiler, PHPUnit, etc.). Add --optimize-autoloader (or --classmap-authoritative) to build an optimised classmap and cut per-class filesystem stat calls.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q65.** Relative to argument resolution, when does kernel.controller_arguments fire?  <small>_(Architecture)_</small>

- A. After ArgumentResolver has built the argument array — listeners edit an already-resolved array via setArguments()
- B. Before argument resolution, so listeners provide the raw values the resolver will use
- C. During controller execution, once per argument

??? success "Answer Q65"
    **A**

    kernel.controller_arguments is dispatched AFTER ArgumentResolverInterface::getArguments() has produced the final ordered array; listeners receive a ControllerArgumentsEvent and may mutate the already-built array with setArguments(). Assuming it runs before resolution (to feed the resolver) is a common misconception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/events.html#kernel-controller-arguments)

**Q66.** At the front controller, which call builds the Request object from PHP's superglobals? (choose one)  <small>_(HTTP)_</small>

- A. Request::createFromGlobals()
- B. Request::create()
- C. new Request($_SERVER)
- D. Request::createFromRequest()

??? success "Answer Q66"
    **A**

    public/index.php calls Request::createFromGlobals(), which reads $_GET, $_POST, $_SERVER, $_COOKIE and $_FILES once into the typed bags. Request::create() builds a synthetic request from explicit arguments (used in tests/sub-requests), and there is no createFromRequest() factory for this purpose.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q67.** A class defines `save()`, and a trait it uses also defines `save()`. A developer expects the trait's version to run but gets the class's. Why?  <small>_(PHP & Web Security)_</small>

- A. The class's own method takes precedence over any trait method
- B. It is undefined behaviour
- C. The trait method should have won; this is a bug
- D. A fatal error should have occurred

??? success "Answer Q67"
    **A**

    Trait precedence is class > trait > inherited parent, so the class's own save() always overrides the trait's. This is defined, expected behaviour, not a bug or error. To use the trait's version, alias it with `as` (e.g. `Trait::save as saveViaTrait;`). Misconception: assuming a trait method overrides the host class's own method — it only overrides inherited ones.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.traits.php)

**Q68.** How should you customise a final Symfony class in a BC-safe way?  <small>_(Architecture)_</small>

- A. Decorate or compose it
- B. Subclass and override it
- C. Edit it in vendor/

??? success "Answer Q68"
    **A**

    final classes must not be subclassed; wrap them via decoration so Symfony can change internals without breaking you.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q69.** Why can't an invokable command call `$this->getHelper('question')`?  <small>_(Console)_</small>

- A. It does not extend Command, so it has no HelperSet accessor — inject services or use SymfonyStyle instead
- B. getHelper() was removed in Symfony 8
- C. Helpers only exist for progress bars
- D. Invokable commands run without an Application

??? success "Answer Q69"
    **A**

    getHelper() is a protected method on the Command base class; an invokable command extends nothing, so it has no HelperSet accessor. The idiomatic solution is to type-hint SymfonyStyle in __invoke() (which wraps QuestionHelper) or inject the collaborators you need. getHelper() still exists for classic commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

**Q70.** A user uploads a file larger than `post_max_size` and the action crashes on a null `$request->files->get('avatar')`. What is the underlying cause?  <small>_(Controllers)_</small>

- A. Exceeding post_max_size can yield an empty files bag (no exception), so the get() returns null — always null-check
- B. move() threw a FileException that was swallowed
- C. getMimeType() returns null for large files
- D. Symfony automatically rejects the request with a 413

??? success "Answer Q70"
    **A**

    When post_max_size is exceeded, PHP may discard the POST data, leaving an empty files bag rather than raising an exception. Guard the result with an instanceof UploadedFile / isValid() check before using it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q71.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(Miscellaneous)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q71"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/cache.html#stampede-prevention)

**Q72.** Which of the following statements are true about the expiration caching model? (select all that apply)  <small>_(HTTP Caching)_</small>

- A. setSharedMaxAge() also marks the response public — no separate setPublic() call is needed
- B. For a shared cache the freshness precedence is s-maxage > max-age > Expires
- C. no-cache instructs caches to never store the response
- D. Response provides a setMustRevalidate() setter for the must-revalidate directive
- E. The #[Cache] attribute overrides caching headers you set explicitly in the controller

??? success "Answer Q72"
    **A, B**

    setSharedMaxAge() implies public since s-maxage only makes sense for shared caches, and shared caches resolve freshness as s-maxage > max-age > Expires. no-cache means "revalidate before reuse" (never-store is no-store), mustRevalidate() is only a getter — emit the directive via setCache(['must_revalidate' => true]) or #[Cache] — and the #[Cache] attribute is applied late without overriding explicit controller headers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

**Q73.** What does MoneyType's divisor option do?  <small>_(Forms)_</small>

- A. Scales the model value (e.g. 100 lets you store integer cents)
- B. Sets the currency symbol
- C. Rounds to N decimals
- D. Limits the maximum amount

??? success "Answer Q73"
    **A**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/forms/types/money.html)

**Q74.** After ContainerBuilder::compile(), what happens to the parameter bag?  <small>_(Dependency Injection)_</small>

- A. It becomes a read-only FrozenParameterBag
- B. It stays mutable so parameters can change at runtime
- C. It is discarded and every parameter is inlined only
- D. It is serialized into the .env file

??? success "Answer Q74"
    **A**

    During build the ContainerBuilder uses a mutable ParameterBag; compile() freezes it into a FrozenParameterBag, after which parameters are read-only. This is why parameters are compile-time constants — the misconception is expecting to mutate parameters at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-parameters)

**Q75.** How do you augment a bundle service without replacing it?  <small>_(Architecture)_</small>

- A. Decorate it with #[AsDecorator] / the decorates: key
- B. Make it public and fetch it
- C. Use getParent()

??? success "Answer Q75"
    **A**

    Decoration wraps the original service (injected as .inner), letting you add behaviour and delegate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
