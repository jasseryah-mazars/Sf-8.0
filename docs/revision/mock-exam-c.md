# Mock Exam C (Exam Mode)

!!! note "Three independent papers"
    This is **Mock C**. Also try: [Mock A](mock-exam.md) · [Mock B](mock-exam-b.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

## 🧠 Pour les nuls

**C'est quoi ?** Un **examen blanc complet** : 75 questions, 90 minutes, sans notes — les conditions exactes de l'examen officiel Symfony 8, sur un échantillon pondéré du même sujet que l'examen réel. Le Mock C est l'une de trois versions indépendantes (A, B, C) tirées de la même banque.

**Pourquoi ça existe ?** Connaître chaque notion séparément ne garantit pas de réussir un examen chronométré de 90 minutes qui mélange tout. Le mock exam entraîne spécifiquement la gestion du temps et l'endurance mentale, en plus des connaissances.

**🏠 Analogie de la vraie vie :** C'est le **concours blanc** que passent les lycéens avant le bac : mêmes conditions, même durée, une note à la fin — pour savoir vraiment où on en est, pas pour apprendre du nouveau contenu.

**Symfony dans la vraie vie :** 75 questions pondérées → même répartition que l'examen réel (Architecture/DI/Sécurité/Messenger plus présents) / 90 minutes chronométrées → même contrainte de temps que le jour J / Score final → indicateur direct de préparation, pas une note scolaire.

**⚠️ Erreur fréquente :** Consulter la réponse dès qu'une question semble difficile, au lieu de la flaguer et d'avancer. Cela fausse complètement le chronométrage et masque le vrai niveau de préparation.

**🧠 Comment le mémoriser :** *« Chronomètre en marche, pas de pause, pas de triche »* — un mock exam fait à moitié (avec pauses ou aide) ne prédit rien sur l'examen réel.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** How does AbstractController obtain its helper services?  <small>_(Controllers)_</small>

- A. Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()
- B. Through constructor injection of each service
- C. The full application container is injected

??? success "Answer Q1"
    **A**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q2.** When is a violation built with buildViolation() actually recorded?  <small>_(Validation)_</small>

- A. Only when addViolation() is called on the builder
- B. Immediately when buildViolation() is called
- C. When the validator method returns
- D. When setParameter() is called

??? success "Answer Q2"
    **A**

    buildViolation() returns a fluent builder; nothing is added to the list until addViolation() commits it. Forgetting it makes the validator pass silently.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/custom_constraint.html)

**Q3.** In phpunit.dist.xml, how is the bridge's extension registered in PHPUnit 11/12?  <small>_(Testing)_</small>

- A. <extensions><bootstrap class="Symfony\Bridge\PhpUnit\SymfonyExtension"/></extensions>
- B. <listeners><listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener"/></listeners>
- C. <php><extension name="symfony"/></php>
- D. It is auto-registered by Composer; no XML entry is needed

??? success "Answer Q3"
    **A**

    PHPUnit 10+ uses the <extensions><bootstrap .../></extensions> mechanism to load the SymfonyExtension. The old <listeners><listener> (SymfonyTestsListener) approach belongs to PHPUnit 9 and earlier; there is no <php><extension> tag, and the extension is not auto-registered.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

**Q4.** role_hierarchy maps ROLE_ADMIN: ROLE_USER. A user stores only [ROLE_ADMIN]. Which check FAILS for them?  <small>_(Security)_</small>

- A. in_array('ROLE_USER', $user->getRoles(), true) — getRoles() never expands the hierarchy
- B. isGranted('ROLE_USER') in a controller
- C. access_control with roles: ROLE_USER
- D. is_granted('ROLE_USER') in Twig

??? success "Answer Q4"
    **A**

    The hierarchy is applied only at authorization time by the RoleHierarchyVoter, so isGranted(), Twig is_granted() and access_control all pass. $user->getRoles() returns exactly the stored roles (['ROLE_ADMIN']), so raw in_array checks bypass the hierarchy — the classic exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#hierarchical-roles)

**Q5.** To reference service('x') in a routing condition, service x must…  <small>_(Routing)_</small>

- A. Be tagged routing.condition_service (e.g. via #[AsRoutingConditionService])
- B. Be public
- C. Implement RouterInterface
- D. Extend AbstractController

??? success "Answer Q5"
    **A**

    Only services tagged routing.condition_service are exposed to the routing expression language. Visibility/base class are irrelevant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q6.** A cookie sent with SameSite=None also requires which attribute?  <small>_(Controllers)_</small>

- A. Secure=true
- B. HttpOnly=false
- C. A domain attribute

??? success "Answer Q6"
    **A**

    Modern browsers reject SameSite=None cookies unless they are marked Secure (HTTPS-only).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#setting-cookies)

**Q7.** Using #[Cache(etag: 'post.getContent()')], what value is actually sent as the ETag?  <small>_(HTTP Caching)_</small>

- A. The SHA-256 hash of the evaluated expression
- B. The literal string 'post.getContent()'
- C. The raw return value of getContent()
- D. A weak ETag of the whole rendered body

??? success "Answer Q7"
    **A**

    CacheAttributeListener evaluates the expression on kernel.controller_arguments and SHA-256-hashes the result before using it as the ETag, so it can point at large content safely. The string is an expression (not a literal), and the raw value is never sent verbatim.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#the-cache-attribute)

**Q8.** What does $client->loginUser($user) do?  <small>_(Testing)_</small>

- A. Authenticates the session with the given UserInterface, skipping the login form
- B. Submits the login form with the user's credentials
- C. Creates the user record in the database
- D. Returns a signed JWT for the user

??? success "Answer Q8"
    **A**

    loginUser() injects a security token for a real user object so you can test authorized behaviour without driving the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#logging-in-users-authentication)

**Q9.** True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled.  <small>_(Miscellaneous)_</small>

- A. True
- B. False

??? success "Answer Q9"
    **B**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q10.** Which class renders Twig templates into an email body?  <small>_(Miscellaneous)_</small>

- A. Symfony\Bridge\Twig\Mime\TemplatedEmail
- B. Symfony\Component\Mime\Email
- C. Symfony\Component\Mailer\Mailer
- D. Symfony\Component\Mime\Message

??? success "Answer Q10"
    **A**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending. Plain Email has no template support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/mailer.html#twig-html-css)

**Q11.** When does a StreamedResponse produce its body?  <small>_(Controllers)_</small>

- A. During send(), by invoking its callback
- B. When it is constructed
- C. During the kernel.controller event

??? success "Answer Q11"
    **A**

    The callback runs at send time and streams output; you cannot change headers once streaming has begun.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#streaming-a-response)

**Q12.** What is the default TTL of a lock created via LockFactory::createLock($resource)?  <small>_(Miscellaneous)_</small>

- A. 300 seconds (5 minutes), with autoRelease on by default
- B. 60 seconds
- C. Unlimited (no TTL)
- D. 30 seconds

??? success "Answer Q12"
    **A**

    createLock(string $resource, ?float $ttl = 300.0, bool $autoRelease = true) defaults to a 300 second TTL and releases the lock when the Lock object is destroyed. Long jobs should raise the TTL and call refresh() to avoid premature expiry.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/lock.html#expiring-locks)

**Q13.** A route is declared as `#[Route('/', name: 'home')]` on the class `App\Controller\HomeController`, which defines a `public function __invoke(): Response`. Which YAML `controller:` value targets it correctly?  <small>_(Controllers)_</small>

- A. controller: App\Controller\HomeController
- B. controller: App\Controller\HomeController::__invokeAction
- C. controller: App\Controller\HomeController#invoke
- D. controller: home_controller.invoke

??? success "Answer Q13"
    **A**

    For an invokable controller the `_controller` value is the class name alone; the resolver detects `__invoke()`. Adding `::__invoke` also works but is not idiomatic, and `#invoke` / a made-up service id are invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

**Q14.** What does `composer dump-autoload --optimize` produce for production?  <small>_(PHP & Web Security)_</small>

- A. A static classmap so no per-class filesystem stat is needed
- B. A minified copy of every class file
- C. A pre-instantiated container of all services
- D. A stripped autoloader that disables PSR-4

??? success "Answer Q14"
    **A**

    --optimize converts PSR-4 rules into an explicit class-to-file map, so the loader looks up a path in an array instead of probing the filesystem — faster in production. It does not minify sources, does not build a service container (that is Symfony's job), and PSR-4 still works as a fallback for classes not in the map (unless --classmap-authoritative). Misconception: confusing autoload optimisation with application caching.

    :material-book-open-variant: [Docs](https://getcomposer.org/doc/articles/autoloader-optimization.md)

**Q15.** Which filter applies sprintf-style formatting in Twig?  <small>_(Twig)_</small>

- A. format
- B. sprintf
- C. printf
- D. interpolate

??? success "Answer Q15"
    **A**

    The format filter wraps vsprintf, e.g. \"%s scored %d\"|format(a, b).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/format.html)

**Q16.** Given AcceptHeader::fromString('text/html;q=0.9, application/json;q=1.0'), what does $accept->first()?->getQuality() return? (choose one)  <small>_(HTTP)_</small>

- A. 1.0 — first() returns the highest-quality item (application/json)
- B. 0.9 — items are returned in string order
- C. null — first() only works on a single-value header
- D. true — first() returns a boolean like has()

??? success "Answer Q16"
    **A**

    AcceptHeader parses and sorts items by quality (descending), so first() returns the AcceptHeaderItem for application/json (q=1.0) and getQuality() gives 1.0. The nullsafe operator guards the empty-header case where first() would return null.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/AcceptHeader.php)

**Q17.** What causes the validator to recurse into a nested object property?  <small>_(Validation)_</small>

- A. #[Assert\Valid] on the property holding the nested object
- B. Nothing — it always recurses automatically
- C. Calling validateProperty() on the nested object
- D. A class-level Valid constraint on the parent

??? success "Answer Q17"
    **A**

    Valid marks a property for cascading; the ValidValidator tells the context to descend so the nested object's own constraints (and, for collections, each element's) are validated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Valid.html)

**Q18.** HTTP is best described as: (choose one)  <small>_(HTTP)_</small>

- A. A stateless, application-layer request/response protocol
- B. A stateful transport-layer protocol
- C. A protocol that always requires TLS
- D. A binary-only protocol since HTTP/1.1

??? success "Answer Q18"
    **A**

    HTTP is a stateless application-layer protocol; state is layered on with cookies/sessions, and TLS is optional (HTTPS).

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

**Q19.** Which constant does forward() pass to HttpKernel::handle(), and what is a consequence for the security firewall?  <small>_(Controllers)_</small>

- A. HttpKernelInterface::SUB_REQUEST — the firewall does not re-authenticate (isMainRequest() is false)
- B. HttpKernelInterface::MASTER_REQUEST — the firewall re-runs
- C. HttpKernelInterface::MAIN_REQUEST — a fresh security context is built
- D. HttpKernelInterface::ASYNC_REQUEST — the request is queued

??? success "Answer Q19"
    **A**

    Sub-requests are dispatched with SUB_REQUEST (the old MASTER_REQUEST constant was removed; MAIN_REQUEST is used for the main request). Because isMainRequest() is false, listeners like the firewall skip re-authentication.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernelInterface.php)

**Q20.** A constructor arg is #[Autowire('%env(MAX)%')] int $max, but you hit a type error because a string was passed. What is wrong?  <small>_(Dependency Injection)_</small>

- A. %env(MAX)% yields a string; add a cast processor: %env(int:MAX)%
- B. Environment variables cannot be injected into constructors
- C. MAX must be declared as a parameter before it can be read
- D. #[Autowire] does not support env placeholders

??? success "Answer Q20"
    **A**

    Raw env values are always strings until a processor casts them, so %env(MAX)% is a string while the argument expects int. Use %env(int:MAX)%. #[Autowire] fully supports env placeholders and no prior parameter declaration is needed; the trap is assuming env values are already typed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration/env_var_processors.html)

**Q21.** Which variables/functions are available inside a routing condition expression?  <small>_(Routing)_</small>

- A. context, request, env(), service()
- B. session, token, user()
- C. kernel, container
- D. params, route()

??? success "Answer Q21"
    **A**

    The routing expression provider exposes the RequestContext (context), the Request (request), and the env()/service() functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q22.** A developer uses $violations[0] (works) but array_map(..., $violations) (fails). Why?  <small>_(Validation)_</small>

- A. The list is a Countable/IteratorAggregate/ArrayAccess object, not a plain array; use foreach/count() or iterator_to_array()
- B. The list is null when empty
- C. array_map only works on associative arrays
- D. Violations are stored as strings

??? success "Answer Q22"
    **A**

    ConstraintViolationList implements ArrayAccess (so [0] works) but is not an array. Iterate it, call count(), use findByCodes(), or convert via iterator_to_array() for array functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q23.** Calling $container->get() on a private service id results in what?  <small>_(Dependency Injection)_</small>

- A. A ServiceNotFoundException
- B. The service instance is returned
- C. null
- D. A fresh instance each call

??? success "Answer Q23"
    **A**

    Private services are not fetchable by id from the public container; they may only be injected. Fetching one throws ServiceNotFoundException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q24.** Which of the following statements are true about the special underscore routing attributes? (select all that apply)  <small>_(Routing)_</small>

- A. _route and _route_params are read-only outputs injected by the matcher into the request attributes
- B. _format sets the request format via Request::setRequestFormat(), influencing the response Content-Type
- C. _fragment only takes effect during URL generation (appended as #fragment); it plays no role in matching
- D. Setting _route in a route's defaults changes what $request->attributes->get('_route') returns
- E. stateless: true hard-blocks all session usage in production

??? success "Answer Q24"
    **A, B, C**

    The matcher injects _route/_route_params and RouterListener copies them into request attributes for you to read, _format drives content negotiation and the default Content-Type, and _fragment is honoured only by the generator. You never set _route yourself, and stateless: true is an assertion that raises an UnexpectedSessionUsageException warning in debug — not a hard production block.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q25.** Which is true about shortcuts like `-f`?  <small>_(Console)_</small>

- A. Shortcuts belong to options only; arguments have no shortcuts
- B. Every argument automatically gets a one-letter shortcut
- C. Shortcuts are only for VALUE_NONE options
- D. Shortcuts must be exactly two characters

??? success "Answer Q25"
    **A**

    Only options accept a shortcut (the 2nd argument of addOption); arguments are positional and have no shortcut. Shortcuts work for any option mode, not just VALUE_NONE, and are typically a single character (e.g. -f).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q26.** Which class collects the `console.command` tags and builds the lazy command loader?  <small>_(Console)_</small>

- A. AddConsoleCommandPass, which builds a ContainerCommandLoader (name → service id)
- B. ContainerBuilder::compile() instantiates each command eagerly
- C. The Kernel's registerCommands() method scans the filesystem
- D. CommandCompilerPass, building an ArrayCommandLoader

??? success "Answer Q26"
    **A**

    Symfony\\Component\\Console\\DependencyInjection\\AddConsoleCommandPass gathers every service tagged console.command and constructs a ContainerCommandLoader mapping each command name to its service id, so a command is instantiated only when its name is invoked. There is no CommandCompilerPass, commands are not instantiated eagerly at compile time, and Symfony 8 does not scan the filesystem for commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q27.** At the front controller, which call builds the Request object from PHP's superglobals? (choose one)  <small>_(HTTP)_</small>

- A. Request::createFromGlobals()
- B. Request::create()
- C. new Request($_SERVER)
- D. Request::createFromRequest()

??? success "Answer Q27"
    **A**

    public/index.php calls Request::createFromGlobals(), which reads $_GET, $_POST, $_SERVER, $_COOKIE and $_FILES once into the typed bags. Request::create() builds a synthetic request from explicit arguments (used in tests/sub-requests), and there is no createFromRequest() factory for this purpose.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q28.** Given:
```php
#[Assert\When(
    expression: 'this.getType() === "premium"',
    constraints: [new Assert\NotBlank()],
)]
public ?string $vatNumber = null;
```
For a non-premium object with $vatNumber = null, what happens?
  <small>_(Validation)_</small>

- A. No violation — the inner NotBlank runs only when the expression is true
- B. A violation, because NotBlank always runs
- C. A syntax error; When cannot wrap NotBlank
- D. The expression is ignored for null values

??? success "Answer Q28"
    **A**

    When applies its inner constraints only if the ExpressionLanguage expression evaluates to true. Here getType() is not 'premium', so NotBlank is skipped and null passes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/When.html)

**Q29.** An admin deletes a user's account while that user is browsing under a stateful firewall. What happens on the user's next request?  <small>_(Security)_</small>

- A. refreshUser() can no longer load them and throws; the ContextListener discards the token, effectively logging them out
- B. Nothing changes until the PHP session cookie expires
- C. A fatal 500 error is returned on every request
- D. The user keeps full access until they click logout

??? success "Answer Q29"
    **A**

    On each stateful request the ContextListener calls refreshUser() to re-sync the session user. A now-missing account makes refreshUser() throw (UserNotFoundException / UnsupportedUserException), so the ContextListener treats the user as unloadable, discards the token and clears storage — an immediate, clean logout. It is not a fatal error, and access does not persist until the cookie expires precisely because the user is re-checked every request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

**Q30.** True or False: adding a tag to a service changes its behaviour automatically, even with no collector consuming that tag.  <small>_(Dependency Injection)_</small>

- A. True
- B. False

??? success "Answer Q30"
    **B**

    A tag is inert build-time metadata; on its own it does nothing. Something — a tagged_iterator/tagged_locator argument or a compiler pass calling findTaggedServiceIds() — must consume the tag for it to have any effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q31.** A field with block prefix 'rating' (parent 'integer') ignores your integer_widget override, but rating_widget works. Why?  <small>_(Forms)_</small>

- A. The renderer tries rating_widget before integer_widget; the more specific block exists and wins, so integer_widget is never reached
- B. integer_widget is a reserved block that cannot be overridden
- C. Parent-prefix blocks are ignored unless you set inherit_data
- D. You must clear the Twig cache for parent blocks to apply

??? success "Answer Q31"
    **A**

    Block-name resolution goes most-specific to least-specific along the block-prefix chain (rating → integer → form). Since rating_widget exists, it wins and the more generic integer_widget is never consulted. Override rating_widget (or remove it to fall through). inherit_data and caching are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q32.** Which are valid places to register a compiler pass? (choose 2)  <small>_(Dependency Injection)_</small>

- A. Kernel::build(ContainerBuilder $c) via addCompilerPass()
- B. A bundle's build(ContainerBuilder $c) via addCompilerPass()
- C. A #[CompilerPass] attribute on the pass class
- D. A container.compiler_pass tag in services.yaml

??? success "Answer Q32"
    **A, B**

    Passes are registered programmatically with addCompilerPass() in the application Kernel::build() or a bundle's build(). There is no #[CompilerPass] attribute and no services.yaml tag that registers a pass — those are common invented answers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q33.** With two decorators on one id, a higher decoration_priority means the decorator is...  <small>_(Dependency Injection)_</small>

- A. Applied first and sits closer to the original (innermost)
- B. Applied last and is the outermost
- C. Ignored
- D. Made public automatically

??? success "Answer Q33"
    **A**

    Higher priority decorators are applied first and end up innermost; consumers receive the lowest-priority, outermost decorator.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html#decoration-priority)

**Q34.** An optional text field with a custom transformer reports 'invalid' whenever it is left blank. What is the likely cause?  <small>_(Forms)_</small>

- A. reverseTransform('') runs the parser on an empty string and throws TransformationFailedException; guard for ''/null and return the empty model value first
- B. The field needs a NotBlank constraint removed
- C. transform() must return null for empty values
- D. Model transformers cannot handle optional fields

??? success "Answer Q34"
    **A**

    An empty submission arrives as '' (or null) at reverseTransform(); if you parse it instead of short-circuiting, you raise a spurious TransformationFailedException and the field is marked invalid. Guard the first line for emptiness and return the model's empty value (null/[]/0). This is a format-handling bug, not a validation constraint issue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q35.** Which of the following statements are true about the Symfony Process component? (select all that apply)  <small>_(Miscellaneous)_</small>

- A. new Process(['git', 'log', $input]) auto-escapes each array element, so $input cannot inject shell syntax
- B. The default process timeout is 60 seconds; setTimeout(null) disables it
- C. mustRun() throws a ProcessFailedException when the process exits with a non-zero code
- D. Process::fromShellCommandline() escapes interpolated variables, making it safe with untrusted input
- E. run() returns the process standard output as a string

??? success "Answer Q35"
    **A, B, C**

    The array constructor escapes every argument, the timeout defaults to 60 seconds (nullable to disable), and mustRun() throws ProcessFailedException on failure where run() only returns the exit code. fromShellCommandline() runs a raw string through the shell with no escaping (a command-injection risk), and stdout is read via getOutput(), not from run().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/process.html)

**Q36.** What does requires_channel: https do, and when?  <small>_(Security)_</small>

- A. Redirects matching paths to HTTPS before authentication runs
- B. Rejects HTTPS requests
- C. Runs only after a successful login
- D. Encrypts the session cookie

??? success "Answer Q36"
    **A**

    The ChannelListener enforces requires_channel before authentication, so even the login page is redirected to HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q37.** A UserDto has #[Groups(['read'])] #[SerializedName('full_name')] on $name and #[Ignore] on $passwordHash. What is the JSON when serialized with context ['groups' => ['read']]?  <small>_(Miscellaneous)_</small>

- A. {"full_name":"..."} plus any other read-group fields; passwordHash is omitted
- B. {"name":"...","passwordHash":"..."}
- C. All properties, because groups are ignored during serialization
- D. An empty object, because #[Ignore] hides everything

??? success "Answer Q37"
    **A**

    With the read group in context, only read-group properties are emitted; $name is renamed to full_name by #[SerializedName], and #[Ignore] drops passwordHash entirely regardless of group. Groups are honoured only because they are passed in the context.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html#using-serialization-groups-attributes)

**Q38.** Which value should you trust to determine an uploaded file's real type?  <small>_(Controllers)_</small>

- A. getMimeType() (content-detected by the guesser)
- B. getClientMimeType()
- C. getClientOriginalExtension()

??? success "Answer Q38"
    **A**

    Client-supplied name/MIME are spoofable; getMimeType()/guessExtension() inspect the actual file content.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

**Q39.** For /blog/{page<\d+>?1}, what does generateUrl('blog_list', ['page' => 3]) produce?  <small>_(Routing)_</small>

- A. /blog/3
- B. /blog
- C. /blog?page=3
- D. /blog/1

??? success "Answer Q39"
    **A**

    The segment is only omitted when the value equals the default (1). Since 3 differs, the generator emits the full /blog/3.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q40.** In which order does the renderer try candidate theme blocks?  <small>_(Forms)_</small>

- A. Most specific (unique field id) down to least specific (form_widget)
- B. Least specific to most specific
- C. Alphabetically
- D. Randomly per request

??? success "Answer Q40"
    **A**

    The block-prefix hierarchy is walked from the unique per-field name down to the root form_* block; the first existing block wins.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_themes.html)

**Q41.** A kernel.exception listener inspects getThrowable() and builds a JsonResponse, but the custom page never appears. What is the most likely bug?  <small>_(Architecture)_</small>

- A. The listener forgot to call $event->setResponse() on its branch, so the event's response stays null and the default handler wins
- B. The listener has priority -128, which is impossible to register
- C. kernel.exception cannot produce JSON responses, only HTML

??? success "Answer Q41"
    **A**

    ExceptionEvent::getResponse() returns null until some listener calls setResponse(). Reading getThrowable() and constructing a response is not enough — you must actually set it on the event. If a branch forgets setResponse(), the response stays null, ErrorListener's default page (or a 500) is used instead, and your custom page never shows.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/events.html#kernel-exception)

**Q42.** Which statements about Twig output escaping in Symfony are correct? (select all that apply)  <small>_(Twig)_</small>

- A. The default escaping strategy is chosen from the template file extension, so a .txt.twig template escapes nothing
- B. Escaping is applied when a value is printed with {{ }}, not when it is assigned with {% set %}
- C. |raw and {% autoescape false %} disable protection, so they must only wrap trusted content
- D. The html_attr strategy is just an alias of html and produces identical output
- E. All templates always use the html strategy regardless of their extension

??? success "Answer Q42"
    **A, B, C**

    The auto-escaping context is derived from the file extension (html, js, css, url, html_attr are available), which is why a .txt.twig template gets no escaping at all — it is not a fixed html default. Escaping happens at print time via the escaper, and |raw / {% autoescape false %} switch the protection off entirely, making them XSS holes for untrusted data. The html_attr strategy is a stricter encoder than html, not an alias.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q43.** Which are valid ways to override parts of Symfony or a third-party bundle in an application? (select all that apply)  <small>_(Architecture)_</small>

- A. Override a bundle template by placing a file with the same path under templates/bundles/<BundleName>/
- B. Override a service by decorating it or replacing its definition, e.g. via a compiler pass
- C. Override translations by defining the same key in the application's translations/ directory, which wins over the bundle's
- D. Create a child bundle and point getParent() at the bundle you want to override
- E. Copy the entire bundle into src/ so your copy shadows the vendor code

??? success "Answer Q43"
    **A, B, C**

    Per-resource overriding is the supported model: templates placed under templates/bundles/<BundleName>/ shadow the bundle's own, application translations take precedence over bundle translations, and services can be redefined, decorated or altered through a compiler pass. Bundle inheritance via getParent() has been removed, and copying whole bundles into src/ is not an override mechanism at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/override.html)

**Q44.** What is the difference between weak and disabled=1?  <small>_(Testing)_</small>

- A. weak still collects and reports deprecations (just never fails); disabled=1 stops collection entirely
- B. They are identical — both hide deprecations
- C. weak stops collection; disabled=1 reports without failing
- D. weak fails on self deprecations only; disabled=1 fails on all

??? success "Answer Q44"
    **A**

    weak keeps collecting and printing the grouped report but never enforces a threshold, so you retain visibility. disabled=1 turns the handler off so nothing is collected or reported. The pair is a common trap when their behaviours are swapped; neither of them fails the build.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration)

**Q45.** Transparent password rehash on login requires…  <small>_(Security)_</small>

- A. Both migrate_from and a provider implementing PasswordUpgraderInterface
- B. Only migrate_from in security.yaml
- C. Only a PasswordUpgraderInterface provider
- D. Calling password_hash() manually in the controller

??? success "Answer Q45"
    **A**

    migrate_from lets needsRehash() detect the old hash; the PasswordUpgradeBadge triggers PasswordMigratingListener, which persists the new hash via upgradePassword().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q46.** A command's execute() throws a RuntimeException. What is the event sequence?  <small>_(Console)_</small>

- A. COMMAND → ERROR → TERMINATE (TERMINATE still runs after ERROR)
- B. COMMAND → TERMINATE only (ERROR is skipped for RuntimeException)
- C. ERROR → COMMAND → TERMINATE
- D. ERROR only; the process aborts before TERMINATE

??? success "Answer Q46"
    **A**

    COMMAND fires before execution; the thrown Throwable triggers ERROR (ConsoleErrorEvent, where a listener can change the exit code or swap the exception); TERMINATE always fires last, even after an error. ERROR never runs before COMMAND, and it does not suppress TERMINATE.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q47.** For each firewall, what does SecurityExtension compile at container build time?  <small>_(Security)_</small>

- A. A FirewallContext bundling its listeners, the authenticator list, an AuthenticatorManager, and (unless stateless) a ContextListener — all indexed in a FirewallMap
- B. A single global Firewall service shared unchanged by every firewall
- C. One controller per firewall generated from the config
- D. Nothing at build time — firewalls are assembled lazily on the first request

??? success "Answer Q47"
    **A**

    SecurityExtension reads the security.yaml tree and, per firewall, compiles a dedicated FirewallContext (its listeners, the list of authenticators, an AuthenticatorManager, an exception listener, and a ContextListener unless the firewall is stateless). All contexts are registered in the FirewallMap; at runtime the single Firewall listener asks the map which context matches. The work happens at compile time, not lazily per request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/SecurityBundle/DependencyInjection/SecurityExtension.php)

**Q48.** Why redirect after a successful POST (POST-redirect-GET)?  <small>_(Forms)_</small>

- A. So a browser refresh re-fetches a GET instead of re-submitting the form
- B. Because forms cannot render on a POST response
- C. To trigger CSRF validation
- D. It is required for isValid() to return true

??? success "Answer Q48"
    **A**

    Without the redirect, refreshing re-POSTs the data and duplicates side effects. Redirecting lands the browser on a safe GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/forms.html)

**Q49.** For {{ user.name }}, in which order does Twig try to resolve the attribute?  <small>_(Twig)_</small>

- A. $user['name'], then $user->name, then $user->name(), getName(), isName(), hasName()
- B. getName() first, then the public property, then array access
- C. Only $user->getName() is ever tried
- D. Only array access $user['name']

??? success "Answer Q49"
    **A**

    Twig's attribute resolver tries array/index access first, then a public property, then method calls name(), getName(), isName() and hasName(). Force pure array access with user['name'] and dynamic names with attribute(user, key). A missing attribute yields null unless strict_variables is on.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#variables)

**Q50.** What is the default Process timeout?  <small>_(Miscellaneous)_</small>

- A. 60 seconds
- B. Unlimited
- C. 30 seconds
- D. 300 seconds

??? success "Answer Q50"
    **A**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/process.html#process-timeout)

**Q51.** After cache warmup, which artifacts does the dumped container leave in var/cache/{env}/? (select all that apply)  <small>_(Dependency Injection)_</small>

- A. A Container{hash}/ directory with the compiled container class and per-service factory code
- B. A generated .preload.php file for OPcache preloading
- C. A serialized ContainerBuilder object loaded on each request
- D. Copies of every services.yaml re-parsed at runtime

??? success "Answer Q51"
    **A, B**

    PhpDumper writes plain PHP: the container class with its getXxxService() factories (split per service or inlined depending on the dump settings) plus a preload script to reference from opcache.preload. The ContainerBuilder and the YAML files are build-time inputs only — nothing re-parses or unserializes them at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dependency_injection/compilation.html)

**Q52.** What does the __Host- cookie name prefix force the browser to require? (choose one)  <small>_(HTTP)_</small>

- A. Secure, no Domain attribute, and Path=/ — the strictest scoping the browser enforces
- B. HttpOnly and SameSite=Strict only
- C. A matching Domain attribute and Max-Age
- D. Nothing; the prefix is purely cosmetic

??? success "Answer Q52"
    **A**

    A cookie named __Host-... is accepted only if it is Secure, has no Domain attribute (so it is locked to the exact host), and uses Path=/. This is the strongest same-origin scoping the browser guarantees, preventing subdomain injection. The related __Secure- prefix only requires the Secure flag.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#cookie_prefixes)

**Q53.** Can symfony/routing be used without FrameworkBundle?  <small>_(Architecture)_</small>

- A. Yes — it is a standalone component
- B. No — it requires the kernel
- C. Only in the dev environment

??? success "Answer Q53"
    **A**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/routing.html)

**Q54.** What does dispatch(object $event) return, and how do you read a listener's result?  <small>_(Architecture)_</small>

- A. It always returns the same event object you passed in; results reach you only by listeners mutating that event (e.g. setResponse), never as a listener return value
- B. It returns whatever the last listener returned
- C. It returns null when no listener set a value

??? success "Answer Q54"
    **A**

    dispatch() returns the exact event object passed in — even with no listeners, or when all left it untouched. Listeners themselves return void; the only way data flows back is by mutating the event, which you then read from the returned object. Expecting dispatch() to hand back a listener's return value is the classic bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/event_dispatcher.html)

**Q55.** What is the literal id of a named autowiring alias, e.g. for a Monolog channel logger?  <small>_(Dependency Injection)_</small>

- A. Literally 'Psr\Log\LoggerInterface $requestLogger' — matched by the parameter name
- B. requestLogger
- C. logger.requestLogger
- D. @requestLogger

??? success "Answer Q55"
    **A**

    A named autowiring alias id is the full type followed by the variable name, 'Type $paramName'. Autowiring matches it when your constructor parameter is named identically — which is fragile, so #[Target('requestLogger')] states the intent explicitly and survives parameter renames.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q56.** What does `cache:clear` run, by default, in addition to removing stale cache?  <small>_(Miscellaneous)_</small>

- A. The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata
- B. The database migrations
- C. The Messenger workers
- D. composer install

??? success "Answer Q56"
    **A**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment.html)

**Q57.** How does the argument `array $context` in the index.php closure get populated?  <small>_(Miscellaneous)_</small>

- A. The runtime's resolver autowires it from $_SERVER (env vars like APP_ENV/APP_DEBUG)
- B. You must call getenv() yourself inside the closure
- C. Symfony injects it from services.yaml parameters
- D. It is always an empty array in Symfony 8

??? success "Answer Q57"
    **A**

    RuntimeInterface::getResolver() builds a resolver that inspects the callable's typed arguments and supplies them — array $context comes from $_SERVER (env), and it can also inject Request, InputInterface, etc. You therefore never read $_SERVER manually in the entry point.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/runtime.html#using-the-runtime)

**Q58.** Which method loads a user by identifier in Symfony 8?  <small>_(Security)_</small>

- A. loadUserByIdentifier()
- B. loadUserByUsername()
- C. findUser()
- D. getUser()

??? success "Answer Q58"
    **A**

    loadUserByUsername() was removed; the UserProviderInterface loader is loadUserByIdentifier().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html)

**Q59.** Given `public float $fahrenheit { get => $this->celsius * 9/5 + 32; }` with `$celsius = 100.0`, what is `$obj->fahrenheit`?  <small>_(PHP & Web Security)_</small>

- A. 212.0 — a virtual property computed by the get hook
- B. 100.0 — the backing celsius value
- C. A TypeError, because fahrenheit has no backing store
- D. null, because no value was assigned

??? success "Answer Q59"
    **A**

    Property hooks (8.4) let a get hook compute a value on read; here it returns 100*9/5+32 = 212.0. There is no backing field for fahrenheit (it is virtual) yet reading it is valid — the hook supplies the value, so neither null nor a TypeError occurs. It returns the computed number, not the raw celsius. Misconception: assuming a hooked property still needs a stored value; a purely virtual property derives it each read.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.property-hooks.php)

**Q60.** Which is true about the tests `is null`, `is empty`, and `is defined`?  <small>_(Twig)_</small>

- A. is empty is broadest — true for null, false, 0, '' and []; is null is only for null; is defined checks existence
- B. All three are equivalent
- C. is empty is true only for '' (empty string)
- D. is defined is true only when the value is not null

??? success "Answer Q60"
    **A**

    is defined tests whether the variable exists at all (undefined is not the same as null); is null tests exact null; is empty is the broadest — true for null, false, 0, '' and []. Use is null when you must distinguish "no value" from "empty list", and combine with is defined for maybe-missing variables.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tests/empty.html)

**Q61.** Relative to argument resolution, when does kernel.controller_arguments fire?  <small>_(Architecture)_</small>

- A. After ArgumentResolver has built the argument array — listeners edit an already-resolved array via setArguments()
- B. Before argument resolution, so listeners provide the raw values the resolver will use
- C. During controller execution, once per argument

??? success "Answer Q61"
    **A**

    kernel.controller_arguments is dispatched AFTER ArgumentResolverInterface::getArguments() has produced the final ordered array; listeners receive a ControllerArgumentsEvent and may mutate the already-built array with setArguments(). Assuming it runs before resolution (to feed the resolver) is a common misconception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/events.html#kernel-controller-arguments)

**Q62.** What is the key difference between getPreferredFormat() and getAcceptableContentTypes()? (choose one)  <small>_(HTTP)_</small>

- A. getPreferredFormat() returns a Symfony format name (e.g. 'json'); getAcceptableContentTypes() returns raw MIME types
- B. They are aliases returning the same value
- C. getPreferredFormat() returns MIME types; getAcceptableContentTypes() returns formats
- D. getPreferredFormat() reads Accept-Language, not Accept

??? success "Answer Q62"
    **A**

    getPreferredFormat() maps the client's Accept header to a short Symfony format (html, json, xml, csv...), best for a match expression. getAcceptableContentTypes() returns the raw MIME strings ordered by preference. Confusing format names with MIME types is a classic trap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q63.** After ContainerBuilder::compile(), what happens to the parameter bag?  <small>_(Dependency Injection)_</small>

- A. It becomes a read-only FrozenParameterBag
- B. It stays mutable so parameters can change at runtime
- C. It is discarded and every parameter is inlined only
- D. It is serialized into the .env file

??? success "Answer Q63"
    **A**

    During build the ContainerBuilder uses a mutable ParameterBag; compile() freezes it into a FrozenParameterBag, after which parameters are read-only. This is why parameters are compile-time constants — the misconception is expecting to mutate parameters at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-parameters)

**Q64.** A bundle ships translations/messages.en.yaml and your app defines the same domain/locale in translations/. Whose strings win?  <small>_(Architecture)_</small>

- A. The application's translations/ take priority over the bundle's translations
- B. The bundle's translations always win because they load first
- C. They merge alphabetically and the last key alphabetically wins

??? success "Answer Q64"
    **A**

    The application's translations/ directory has higher priority than any bundle's translations. Providing a catalogue with the same domain and locale overrides the bundle's strings — the same convention-based precedence used for template overrides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html)

**Q65.** What is the correct order of the set-data-phase form events?  <small>_(Forms)_</small>

- A. PRE_SET_DATA -> POST_SET_DATA
- B. POST_SET_DATA -> PRE_SET_DATA
- C. PRE_SET_DATA -> SUBMIT
- D. SET_DATA -> POST_SET_DATA

??? success "Answer Q65"
    **A**

    Setting data (on create/populate) dispatches PRE_SET_DATA then POST_SET_DATA. There is no SET_DATA constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q66.** How many templates can a single template extend in Twig?  <small>_(Twig)_</small>

- A. Exactly one
- B. Up to three
- C. Unlimited
- D. Zero

??? success "Answer Q66"
    **A**

    Twig uses single vertical inheritance. For reusing blocks from several templates (horizontal reuse), use the {% use %} tag instead.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

**Q67.** In the template method pattern, why is the public skeleton method often marked `final`?  <small>_(PHP & Web Security)_</small>

- A. To stop subclasses overriding the algorithm skeleton, restricting them to the abstract hooks
- B. To allow subclasses to replace the whole algorithm
- C. Because abstract methods must be final
- D. To make the class instantiable

??? success "Answer Q67"
    **A**

    The template method fixes the invariant algorithm and defers only the variable steps to abstract hooks; marking it final protects those invariants from being overridden. It does the opposite of allowing full replacement; abstract methods cannot be final (they must be overridden); and final has nothing to do with instantiability. Misconception: leaving the skeleton overridable, which lets subclasses break the pattern.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.abstract.php)

**Q68.** At which point in a project's lifecycle does Symfony Flex actually run?  <small>_(Architecture)_</small>

- A. Only at Composer time — it subscribes to Composer events like post-install-cmd/post-update-cmd and package install/uninstall
- B. On every HTTP request, as a high-priority kernel.request listener
- C. At container compile time, as a Symfony compiler pass
- D. At kernel.terminate, after the response is sent

??? success "Answer Q68"
    **A**

    Flex is a Composer plugin that hooks Composer's event system; when a package is installed/updated/removed it resolves aliases and applies (or reverses) the matching recipe's configurators. It writes files (config/, .env, bundles.php) but plays no part in the HTTP runtime, the DI compiler, or terminate — those read the files Flex produced.

    :material-book-open-variant: [Docs](https://github.com/symfony/flex)

**Q69.** Which statement about PSR-6 vs PSR-16 is correct?  <small>_(Miscellaneous)_</small>

- A. PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not
- B. PSR-16 supports tags but PSR-6 does not
- C. Both are identical key/value APIs
- D. PSR-6 has no expiration support

??? success "Answer Q69"
    **A**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/cache.html)

**Q70.** A test does: $client = static::createClient(); then self::getContainer()->set(PaymentGateway::class, $mock); then $client->request('POST', '/checkout'); — but the real gateway still runs. What is the most likely fix?  <small>_(Testing)_</small>

- A. Call $client->disableReboot() before set(), so the replacement survives the reboot that createClient triggers on the next request
- B. Call set() again after the request
- C. Make PaymentGateway public in services.yaml
- D. Replace self::getContainer() with static::$kernel->getContainer()

??? success "Answer Q70"
    **A**

    By default the kernel reboots (rebuilding a fresh container) around requests, discarding any set() replacement. disableReboot() keeps the container — and your mock — alive across the request. Calling set() after the request is too late; the class already has visibility (getContainer exposes it); and $kernel->getContainer() hides private services entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#mocking-services)

**Q71.** Which methods does UserInterface declare in Symfony 8?  <small>_(Security)_</small>

- A. getRoles() and getUserIdentifier()
- B. getUsername() and getRoles()
- C. getRoles(), getUserIdentifier() and eraseCredentials()
- D. getId() and getPassword()

??? success "Answer Q71"
    **A**

    Symfony 8 trimmed UserInterface to two methods; eraseCredentials() and getUsername() were removed.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/UserInterface.php)

**Q72.** What does a higher listener priority mean?  <small>_(Architecture)_</small>

- A. It runs earlier
- B. It runs later
- C. It cannot be stopped

??? success "Answer Q72"
    **A**

    Listeners are sorted by priority in descending order, so higher priorities run first; the default priority is 0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/event_dispatcher.html)

**Q73.** isEqualTo() returns false when a stored user is refreshed. Effect?  <small>_(Security)_</small>

- A. The token is invalidated — the user is logged out
- B. Nothing happens
- C. The password is rehashed
- D. A 500 error is thrown

??? success "Answer Q73"
    **A**

    A negative EquatableInterface comparison on refresh tells the framework the stored identity is stale, so the token is dropped.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/User/EquatableInterface.php)

**Q74.** router:match /blog/hello reports no match, but the page works for real GET requests. What is the likely cause?  <small>_(Routing)_</small>

- A. You omitted --method=GET, so the default context did not reproduce the real request
- B. The compiled cache is corrupt
- C. router:match cannot test parameterized paths
- D. The route is missing from url_generating_routes.php

??? success "Answer Q74"
    **A**

    router:match builds a RequestContext from the options you pass; without --method/--host/--scheme it may not reproduce the real request and can report a no-match (or a method rejection) that does not happen in production. Pass the exact conditions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q75.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(Miscellaneous)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q75"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/cache.html#stampede-prevention)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
