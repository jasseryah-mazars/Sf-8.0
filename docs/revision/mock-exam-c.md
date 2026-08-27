# Mock Exam C (Exam Mode)

!!! note "Three independent papers"
    This is **Mock C**. Also try: [Mock A](mock-exam.md) · [Mock B](mock-exam-b.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** Why is the external library an optional dependency of the component but a required dependency of the bridge?  <small>_(Architecture)_</small>

- A. Keeping it optional on the component preserves the component's minimal, reusable dependency graph; the bridge exists precisely to depend on that library, so it requires it
- B. Because Composer forbids components from having any required dependencies
- C. Because the bridge is loaded at runtime while the component is loaded at compile time

??? success "Answer Q1"
    **A**

    A component must stay usable by everyone, so it must not hard-require any particular third-party library — that coupling is pushed into a separate bridge package. The bridge's whole reason to exist is to integrate that specific library, so it declares it as a required dependency. This keeps the component's graph minimal and the integration independently versioned.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

**Q2.** Consider: $response->setEtag(sha1($post->getContent())); if ($response->isNotModified($request)) { return $response; } return $this->render('post.html.twig', ['post' => $post], $response); — what is the benefit when If-None-Match matches?  <small>_(HTTP Caching)_</small>

- A. A bodyless 304 is returned and the template is never rendered
- B. The template is rendered, then discarded, and a 304 is sent
- C. A 200 with the full body is always returned
- D. The response is sent twice

??? success "Answer Q2"
    **A**

    isNotModified() sets 304 and strips the body when the ETag matches, and the early return short-circuits before render() runs — so no template work happens at all. If you called render() first you would lose that saving. It never sends twice; you return the response once.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

**Q3.** You set migrate_from and needsRehash() returns true, yet stored hashes are never upgraded. What is missing?  <small>_(Security)_</small>

- A. The user provider does not implement PasswordUpgraderInterface, so upgradePassword() is never called to persist the new hash
- B. migrate_from only works with the plaintext algorithm
- C. You must call password_hash() yourself in the controller
- D. needsRehash() is not supported in Symfony 8

??? success "Answer Q3"
    **A**

    migrate_from + needsRehash() computes a fresh hash, but persisting it is the provider's job: only a provider implementing PasswordUpgraderInterface's upgradePassword() actually stores it (triggered by the PasswordUpgradeBadge / PasswordMigratingListener). Without it, the rehash is computed and discarded every login. migrate_from is not plaintext-only, you must not hash manually, and needsRehash() is fully supported.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html#password-migration)

**Q4.** generateUrl('blog_show', ['id' => 42, 'utm' => 'x']) produces what?  <small>_(Routing)_</small>

- A. /blog/42?utm=x
- B. /blog/42/x
- C. /blog/42
- D. an InvalidParameterException

??? success "Answer Q4"
    **A**

    Parameters that are not route placeholders are appended as query string arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q5.** Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?  <small>_(Miscellaneous)_</small>

- A. null is returned as a cache hit; the callback is NOT run again
- B. The callback runs again because null means a miss
- C. A CacheException is thrown for storing null
- D. The item is deleted automatically

??? success "Answer Q5"
    **A**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/cache.html#cache-contracts)

**Q6.** What can autowiring resolve automatically?  <small>_(Dependency Injection)_</small>

- A. Object dependencies identified by their type-hint
- B. Scalar and string arguments
- C. Array parameters
- D. Environment variables

??? success "Answer Q6"
    **A**

    Autowiring maps a type-hint to a service; scalars and env vars must be bound explicitly with bind or #[Autowire].

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q7.** Which Twig call is wrong for rendering a single field's widget?  <small>_(Forms)_</small>

- A. form(form.email) — form() is for the whole form; use form_widget/form_row for a field
- B. form_widget(form.email)
- C. form_row(form.email)
- D. form_label(form.email)

??? success "Answer Q7"
    **A**

    form() renders an entire form (start, rows, end). For an individual field use form_row (label+widget+errors+help) or the granular form_widget/form_label/ form_errors/form_help. Calling form() on a child view is a common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/form_customization.html)

**Q8.** How does EventDispatcher store and order listeners internally?  <small>_(Architecture)_</small>

- A. It keeps listeners[eventName][priority][] and sorts by priority descending on first dispatch, memoising the sorted list until a listener is added/removed
- B. It sorts listeners alphabetically by class name on every dispatch
- C. It runs listeners in random order to prevent coupling

??? success "Answer Q8"
    **A**

    Internally the dispatcher stores listeners keyed by event name then priority. On the first dispatch of an event it sorts by priority descending (higher first; equal priorities preserve registration order) and caches the result in a sorted[] map, invalidated only when listeners change. This memoisation keeps repeated dispatches cheap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php)

**Q9.** Which accessor returns each of a field's three data representations after submit?  <small>_(Forms)_</small>

- A. getData() = model, getNormData() = normalized, getViewData() = view
- B. getData() = view, getViewData() = model, getNormData() = raw
- C. getModelData(), getNormalizedData(), getRenderedData()
- D. All three return the same array

??? success "Answer Q9"
    **A**

    A field holds data in three shapes: model (your PHP value), normalized (transport-neutral canonical), and view (strings for HTML). They are read with getData()/getNormData()/getViewData() respectively; transformers convert between adjacent shapes. There are no getModelData()/getRenderedData() methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/data_transformers.html)

**Q10.** True or False: an interface may declare (non-constant) properties.  <small>_(PHP & Web Security)_</small>

- A. False
- B. True

??? success "Answer Q10"
    **A**

    Interfaces are pure contracts: they may declare method signatures and constants (typed since 8.3) but never properties, because they carry no state. If you need shared state, use an abstract class. Misconception: treating an interface like an abstract class — only abstract classes hold properties and a constructor.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

**Q11.** With two decorators on one id, a higher decoration_priority means the decorator is...  <small>_(Dependency Injection)_</small>

- A. Applied first and sits closer to the original (innermost)
- B. Applied last and is the outermost
- C. Ignored
- D. Made public automatically

??? success "Answer Q11"
    **A**

    Higher priority decorators are applied first and end up innermost; consumers receive the lowest-priority, outermost decorator.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html#decoration-priority)

**Q12.** A class defines #[Assert\GroupSequence(['User','Strong'])]. You call validate($user, groups: ['User']). What runs?  <small>_(Validation)_</small>

- A. The class's Default-group constraints flat, WITHOUT the sequence (bypassing stop-on-first-fail)
- B. The full sequence, stopping on the first failing group
- C. Nothing, because 'User' is remapped to the sequence
- D. Only the 'Strong' group

??? success "Answer Q12"
    **A**

    Validating the {ClassName} group ('User') runs the class's Default constraints flat, bypassing the sequence. Only validating 'Default' triggers the sequence.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/sequence_provider.html)

**Q13.** In phpunit.dist.xml, how is the bridge's extension registered in PHPUnit 11/12?  <small>_(Testing)_</small>

- A. <extensions><bootstrap class="Symfony\Bridge\PhpUnit\SymfonyExtension"/></extensions>
- B. <listeners><listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener"/></listeners>
- C. <php><extension name="symfony"/></php>
- D. It is auto-registered by Composer; no XML entry is needed

??? success "Answer Q13"
    **A**

    PHPUnit 10+ uses the <extensions><bootstrap .../></extensions> mechanism to load the SymfonyExtension. The old <listeners><listener> (SymfonyTestsListener) approach belongs to PHPUnit 9 and earlier; there is no <php><extension> tag, and the extension is not auto-registered.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

**Q14.** Which password algorithm is the recommended default?  <small>_(Security)_</small>

- A. auto
- B. plaintext
- C. md5
- D. pbkdf2

??? success "Answer Q14"
    **A**

    'auto' selects the best available algorithm (currently bcrypt) and can adapt over time; it also enables automatic rehash on cost changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/passwords.html)

**Q15.** When is refreshUser() called?  <small>_(Security)_</small>

- A. On every stateful request, to re-sync the session user
- B. Only during the login request
- C. Never for custom providers
- D. Only on logout

??? success "Answer Q15"
    **A**

    The ContextListener refreshes the stored user on each request of a stateful firewall; a stateless firewall never calls it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

**Q16.** With retry_strategy delay: 1000 and multiplier: 2, what are the delays before the 1st, 2nd and 3rd retry?  <small>_(Miscellaneous)_</small>

- A. 1000 ms, 2000 ms, 4000 ms (delay × multiplier per attempt)
- B. 1000 ms, 1000 ms, 1000 ms (constant)
- C. 2000 ms, 4000 ms, 8000 ms
- D. 1 s, 2 s, 3 s (linear)

??? success "Answer Q16"
    **A**

    MultiplierRetryStrategy multiplies the initial delay by the multiplier for each successive attempt: 1000, 1000×2=2000, 2000×2=4000 (capped by max_delay if set). It is exponential, not constant or linear, and starts at the configured delay, not delay×multiplier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

**Q17.** Which caching model can avoid contacting the server entirely? (choose one)  <small>_(HTTP)_</small>

- A. Expiration (freshness)
- B. Validation
- C. Both always
- D. Neither

??? success "Answer Q17"
    **A**

    While a copy is fresh (within max-age), the cache serves it with no request; validation always sends a conditional request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

**Q18.** What is the signature of HttpKernelInterface::handle() and the role of its $catch argument?  <small>_(Architecture)_</small>

- A. handle(Request $request, int $type = self::MAIN_REQUEST, bool $catch = true): Response — with $catch=true, exceptions are caught and turned into a response via kernel.exception; with $catch=false they propagate
- B. handle(Request $request): void — it prints the response directly and $catch controls output buffering
- C. handle(string $env, bool $debug): Response — $catch enables the profiler

??? success "Answer Q18"
    **A**

    The contract is handle(Request, int $type = MAIN_REQUEST, bool $catch = true): Response. handle() wraps the private handleRaw() in a try/catch when $catch is true, so an escaped exception is routed through handleThrowable()/kernel.exception into a Response. With $catch=false (common in sub-requests and tests) the exception simply propagates to the caller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html)

**Q19.** What do the symfony/*-contracts packages contain?  <small>_(Architecture)_</small>

- A. Stable interfaces and traits to depend on
- B. Compiled service containers
- C. Twig templates

??? success "Answer Q19"
    **A**

    Contracts packages hold interface-only definitions so consumers can depend on a stable API decoupled from a concrete implementation.

    :material-book-open-variant: [Docs](https://github.com/symfony/contracts)

**Q20.** A parent method is `handle(Cat $c)`. Which override signature is legal under contravariance?  <small>_(PHP & Web Security)_</small>

- A. handle(Animal $c) — widening the parameter is allowed
- B. handle(Kitten $c) — narrowing the parameter
- C. handle(string $c) — an unrelated type
- D. handle() — dropping the parameter

??? success "Answer Q20"
    **A**

    Parameter types are contravariant: a child may accept a wider (more general) type such as Animal, preserving substitutability. Narrowing to Kitten would reject values the parent accepted (illegal), an unrelated type breaks the contract, and dropping a required parameter changes arity. Misconception: applying the covariant (narrowing) rule to parameters — returns narrow, parameters widen.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.variance.php)

**Q21.** Where does a controller read incoming cookies from?  <small>_(Controllers)_</small>

- A. $request->cookies
- B. $request->headers
- C. $_SESSION

??? success "Answer Q21"
    **A**

    The cookies ParameterBag wraps $_COOKIE; responses set cookies via $response->headers->setCookie().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q22.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(Miscellaneous)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q22"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/cache.html#stampede-prevention)

**Q23.** How is an abstract class conventionally named?  <small>_(Architecture)_</small>

- A. With an Abstract prefix, e.g. AbstractController
- B. With an Abstract suffix, e.g. ControllerAbstract
- C. With an _abstract suffix

??? success "Answer Q23"
    **A**

    Abstract classes take the Abstract prefix; interfaces use the Interface suffix and traits use the Trait suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/contributing/code/standards.html)

**Q24.** How are custom form types made available by their FQCN and able to receive injected services?  <small>_(Forms)_</small>

- A. FrameworkBundle autoconfigures FormTypeInterface implementers with the form.type tag
- B. You must register each type manually in config/services.yaml with form.type
- C. Types are discovered by a #[AsFormType] attribute
- D. The FormFactory scans the Form/ directory at runtime

??? success "Answer Q24"
    **A**

    Service autoconfiguration tags any class implementing FormTypeInterface with form.type, so it is usable by FQCN and can autowire constructor dependencies. There is no #[AsFormType] attribute and no runtime directory scan; manual tagging is only needed when autoconfiguration is disabled.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/create_custom_field_type.html)

**Q25.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(Miscellaneous)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q25"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/serializer.html#handling-circular-references)

**Q26.** How many times may createClient() be called within a single test?  <small>_(Testing)_</small>

- A. Once — a second call throws
- B. Twice
- C. Any number of times
- D. Once per HTTP request

??? success "Answer Q26"
    **A**

    Only one kernel/client may be booted per test; calling createClient() again throws a LogicException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#your-first-application-test)

**Q27.** Which two arguments does SymfonyStyle require?  <small>_(Console)_</small>

- A. An InputInterface and an OutputInterface
- B. An Application and a Command
- C. A QuestionHelper and an OutputInterface
- D. Only an OutputInterface

??? success "Answer Q27"
    **A**

    SymfonyStyle wraps both input (for prompts like ask/confirm) and output (for styled writing), so its constructor is (InputInterface, OutputInterface). It creates its own QuestionHelper internally and needs neither an Application nor a Command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/style.html)

**Q28.** How are route conditions executed at request time?  <small>_(Routing)_</small>

- A. As pre-compiled PHP closures baked into the dumped matcher (not runtime eval)
- B. Via eval() of the expression string on each request
- C. By calling a Twig template
- D. They are evaluated once at boot and cached as booleans

??? success "Answer Q28"
    **A**

    The framework compiles all conditions ahead of time through ExpressionLanguage and the routing ExpressionLanguageProvider, so the dumped matcher contains compiled closures. UrlMatcher::handleRouteRequirements() runs them after host/path match — no per-request eval, and they cannot be reduced to a constant because they depend on the live request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Matcher/UrlMatcher.php)

**Q29.** Why does InputBag (query/request/cookies) reject reading an array where a scalar is expected? (choose one)  <small>_(HTTP)_</small>

- A. InputBag restricts values to scalars/arrays-of-scalars/null and throws BadRequestException on a type mismatch, hardening against malicious nested input
- B. PHP forbids arrays in $_GET
- C. ParameterBag also throws in the same case
- D. It silently casts the array to its first element

??? success "Answer Q29"
    **A**

    InputBag extends ParameterBag but narrows the contract to user-supplied data: get() accepts only scalars/null and raises a BadRequestException (HTTP 400) when handed an unexpected array, blocking parameter-pollution style attacks. A plain ParameterBag (used by attributes) imposes no such restriction. Use all('key') to intentionally read array values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

**Q30.** Two decorators target the same service. You need caching wrapped directly around the original and logging on the outside so consumers hit logging first. How do you set decoration_priority?  <small>_(Dependency Injection)_</small>

- A. Caching gets the higher priority (e.g. 20), logging the lower (e.g. 10)
- B. Logging gets the higher priority, caching the lower
- C. Both must be equal so ordering is deterministic
- D. Priority has no effect on the chain order

??? success "Answer Q30"
    **A**

    Higher decoration_priority is applied first and ends up innermost (closest to the original), so caching needs the higher number to sit directly around the original, and logging the lower number to become the outermost wrapper consumers hit first. Assuming lower priority runs first inverts the chain.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html#decoration-priority)

**Q31.** DelayStamp(5000) delays delivery by how long?  <small>_(Miscellaneous)_</small>

- A. 5000 milliseconds (5 seconds)
- B. 5000 seconds
- C. 5000 microseconds
- D. 5000 minutes

??? success "Answer Q31"
    **A**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds. The classic trap is to read it as seconds; the retry strategy's initial delay is likewise in milliseconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#delaying-messages)

**Q32.** A parent declares `serialize(): string`. Is overriding it with `serialize(): never` legal?  <small>_(PHP & Web Security)_</small>

- A. Yes — never is the bottom type and is a valid covariant return
- B. No — never is unrelated to string
- C. No — never can only be used on void methods
- D. Only if the parent also returns never

??? success "Answer Q32"
    **A**

    never is the bottom type: a method that always throws or exits satisfies any return contract, so `: never` is a valid covariant narrowing of `: string`. never is not unrelated (it is a subtype of every type), it is not restricted to void methods, and the parent need not also return never. Misconception: thinking never only marks infinite loops/exit; it is a genuine type in the variance lattice.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

**Q33.** Which response class best serves a resumable (range-request) file download?  <small>_(Controllers)_</small>

- A. BinaryFileResponse
- B. StreamedResponse
- C. JsonResponse

??? success "Answer Q33"
    **A**

    BinaryFileResponse supports HTTP range requests and X-Sendfile/X-Accel offloading for efficient downloads.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

**Q34.** decoration_on_invalid: null is set, but .inner is typed as non-nullable MailerInterface and the decorated target is absent. What happens?  <small>_(Dependency Injection)_</small>

- A. A TypeError — null is injected as .inner but the non-nullable argument rejects it; type it ?MailerInterface and guard with ?->
- B. The decorator is silently removed
- C. An exception is thrown at compile time
- D. An empty stub mailer is created

??? success "Answer Q34"
    **A**

    With null, the compiler injects null as .inner; if the argument type is not nullable this becomes a TypeError at instantiation. The fix is a nullable type (?MailerInterface) and nullsafe delegation. ignore (not null) is what removes the decorator; exception is the default that throws at build.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q35.** You want to assert that calling a method emits a specific deprecation. Which is correct in Symfony 8?  <small>_(Testing)_</small>

- A. use ExpectUserDeprecationMessageTrait; then $this->expectUserDeprecationMessage('Since app 2.0: ...') before the call
- B. use ExpectDeprecationTrait; then $this->expectDeprecation('...')
- C. Annotate the test with @expectedDeprecation '...'
- D. $this->expectException(DeprecationException::class)

??? success "Answer Q35"
    **A**

    ExpectUserDeprecationMessageTrait::expectUserDeprecationMessage() is the current API for asserting an emitted E_USER_DEPRECATED message. The old ExpectDeprecationTrait::expectDeprecation() and the @expectedDeprecation annotation were removed in Symfony 7.0, and deprecations are not exceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail)

**Q36.** In the path /{a}/{b}, which placeholder can be made optional?  <small>_(Routing)_</small>

- A. b only, because it is the trailing placeholder
- B. a only
- C. Both, independently
- D. Neither

??? success "Answer Q36"
    **A**

    Only trailing placeholders can be optional; a gap in the middle cannot be located by the matcher. RouteCompiler emits nested optional groups from the tail, so an optional a with a required b is impossible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q37.** How often does a new Symfony minor version ship?  <small>_(Architecture)_</small>

- A. Every six months, in May and November
- B. Every month
- C. Every two years

??? success "Answer Q37"
    **A**

    Symfony uses a fixed time-based cadence: a minor every May and November, a major every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q38.** Which object does VarDumper's VarCloner produce before rendering?  <small>_(Miscellaneous)_</small>

- A. A Data object
- B. A Response
- C. A FlattenException
- D. A StopwatchEvent

??? success "Answer Q38"
    **A**

    The cloner captures the variable into an immutable, depth-limited Data object, which a CliDumper or HtmlDumper then renders — separating capture from output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/var_dumper.html)

**Q39.** 401 Unauthorized means the user is authenticated but lacks permission. True or false?  <small>_(HTTP)_</small>

- A. False
- B. True

??? success "Answer Q39"
    **A**

    401 actually means *not authenticated* — credentials are missing or invalid, and the server must send a WWW-Authenticate header. The 'authenticated but not allowed' case is 403 Forbidden, where re-authenticating will not help. The name 'Unauthorized' is a long-standing misnomer.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401)

**Q40.** Which class collects the `console.command` tags and builds the lazy command loader?  <small>_(Console)_</small>

- A. AddConsoleCommandPass, which builds a ContainerCommandLoader (name → service id)
- B. ContainerBuilder::compile() instantiates each command eagerly
- C. The Kernel's registerCommands() method scans the filesystem
- D. CommandCompilerPass, building an ArrayCommandLoader

??? success "Answer Q40"
    **A**

    Symfony\\Component\\Console\\DependencyInjection\\AddConsoleCommandPass gathers every service tagged console.command and constructs a ContainerCommandLoader mapping each command name to its service id, so a command is instantiated only when its name is invoked. There is no CommandCompilerPass, commands are not instantiated eagerly at compile time, and Symfony 8 does not scan the filesystem for commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q41.** You call $validator->validate(null). What happens?  <small>_(Validation)_</small>

- A. You get back an empty ConstraintViolationListInterface — no error, no TypeError
- B. A TypeError, because null is not an object
- C. A ValidationFailedException is thrown
- D. It returns null

??? success "Answer Q41"
    **A**

    Passing null is legal: the value is wrapped in a node, no class metadata is found, and an empty violation list comes back. Validation is values against constraints, and a bare null carries none. The trap is that a null object silently passes when you expected a required value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation.html)

**Q42.** A controller runs $security->getUser()->getUserIdentifier() and fatals on some requests. What is the cause?  <small>_(Security)_</small>

- A. On an anonymous request getUser() returns null, so calling a method on null fatals; guard with ?->, ?? or an IsGranted check
- B. getUser() throws an AccessDeniedException for guests
- C. getUserIdentifier() was removed in Symfony 8
- D. TokenStorage is not registered as a service

??? success "Answer Q42"
    **A**

    Security::getUser() returns ?UserInterface — it is null whenever no token holds a user (a truly anonymous request, or a lazy firewall whose token was never read). Dereferencing null is a fatal error. Guard with $user?->…, a ?? fallback, or an earlier #[IsGranted('IS_AUTHENTICATED_FULLY')] / denyAccessUnlessGranted() so $user is guaranteed non-null past that point. getUserIdentifier() is very much part of the 8.0 interface, and getUser() never throws for guests — it simply returns null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html)

**Q43.** Which resolvers have the highest default priority (120) in Symfony 8?  <small>_(Controllers)_</small>

- A. RequestValueResolver and SessionValueResolver
- B. DefaultValueResolver and VariadicValueResolver
- C. RequestAttributeValueResolver and BackedEnumValueResolver

??? success "Answer Q43"
    **A**

    Request and Session resolvers run first at priority 120; the attribute, enum, uid and datetime resolvers sit at 100.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Resources/config/web.php)

**Q44.** Your metric is only complete after the response is sent. Which interface should the collector implement?  <small>_(Miscellaneous)_</small>

- A. LateDataCollectorInterface (its lateCollect() runs at kernel.terminate)
- B. DataCollectorInterface only; collect() runs after terminate
- C. EventSubscriberInterface on kernel.request
- D. CacheWarmerInterface

??? success "Answer Q44"
    **A**

    Normal collect() runs on kernel.response, too early for post-response data (final dumps, cache calls). LateDataCollectorInterface::lateCollect() runs later at terminate, when that data is complete.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/profiler/data_collector.html)

**Q45.** Which version string should you pass as the second argument of trigger_deprecation()?  <small>_(Architecture)_</small>

- A. The version in which the API was DEPRECATED (e.g. '8.1'), not the current running version
- B. The current installed version at the time the notice fires
- C. The version in which the code will be REMOVED (the next major)

??? success "Answer Q45"
    **A**

    The version argument records when the deprecation was introduced, producing the \"Since <package> <version>: <message>\" format tooling parses. A common mistake is passing the current version, or the removal version — both are wrong. Use the version the API was deprecated in.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q46.** Can an access_control rule pass the matched entity to a voter as the subject?  <small>_(Security)_</small>

- A. No — access_control has no subject; it calls AccessDecisionManager with only roles/allow_if. Use #[IsGranted] with a subject for per-object rules
- B. Yes, via a subject: key on the rule
- C. Yes, the matched path parameter is passed as the subject
- D. Only when allow_if is also set

??? success "Answer Q46"
    **A**

    access_control routes through the same AccessDecisionManager and voters as isGranted(), but it is purely URL-driven: the AccessListener calls decide() with the rule's roles/expression and no subject. There is no subject: key and path parameters are not passed as subjects. Per-object decisions require #[IsGranted]/denyAccessUnlessGranted() with an explicit subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/voters.html)

**Q47.** Which service does FormInterface::handleRequest() delegate to under FrameworkBundle?  <small>_(Forms)_</small>

- A. HttpFoundationRequestHandler
- B. NativeRequestHandler
- C. FormFactory
- D. RequestStack

??? success "Answer Q47"
    **A**

    With HttpFoundation available, the form's request handler is HttpFoundationRequestHandler; NativeRequestHandler is the fallback when working with PHP superglobals directly.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/HttpFoundation/HttpFoundationRequestHandler.php)

**Q48.** What does the #[Target('requestLogger')] attribute do?  <small>_(Dependency Injection)_</small>

- A. Selects the named autowiring alias explicitly, decoupled from the parameter name
- B. Creates a new service definition
- C. Adds a tag to the service
- D. Makes the service public

??? success "Answer Q48"
    **A**

    #[Target] binds to a named autowiring alias by name, so renaming the constructor parameter does not break wiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html#fixing-non-autowireable-arguments)

**Q49.** An admin deletes a user's account while that user is browsing under a stateful firewall. What happens on the user's next request?  <small>_(Security)_</small>

- A. refreshUser() can no longer load them and throws; the ContextListener discards the token, effectively logging them out
- B. Nothing changes until the PHP session cookie expires
- C. A fatal 500 error is returned on every request
- D. The user keeps full access until they click logout

??? success "Answer Q49"
    **A**

    On each stateful request the ContextListener calls refreshUser() to re-sync the session user. A now-missing account makes refreshUser() throw (UserNotFoundException / UnsupportedUserException), so the ContextListener treats the user as unloadable, discards the token and clears storage — an immediate, clean logout. It is not a fatal error, and access does not persist until the cookie expires precisely because the user is re-checked every request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Http/Firewall/ContextListener.php)

**Q50.** A command returns 300 as its exit code. What does the process actually exit with?  <small>_(Console)_</small>

- A. 44 — exit codes are clamped to 0–255 via % 256 (300 % 256 = 44)
- B. 300 — Symfony passes it through unchanged
- C. 255 — anything above 255 becomes 255
- D. 1 — out-of-range codes fall back to FAILURE

??? success "Answer Q50"
    **A**

    POSIX exit codes are a single byte (0–255), so Symfony normalises out-of-range values with % 256; 300 % 256 = 44. It is not passed through, not capped at 255, and not coerced to FAILURE. By convention a signal-terminated process exits with 128 + signalNumber.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q51.** What is true about kernel events when an inline fragment is rendered?  <small>_(Twig)_</small>

- A. The full request lifecycle runs again for the sub-request (kernel.request, kernel.controller, kernel.response, etc.)
- B. No events fire because it is an internal call
- C. Only kernel.response fires for the fragment
- D. The parent request's events are re-dispatched for the fragment

??? success "Answer Q51"
    **A**

    Inline rendering calls HttpKernel::handle(..., SUB_REQUEST), so the whole listener chain (request, controller, response) runs independently for the fragment. The sub-request has its own Request object; parent attributes are not automatically shared.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html#handling-requests)

**Q52.** In a .html.twig file, what does {{ '<b>hi</b>' }} render to the browser?  <small>_(Twig)_</small>

- A. &lt;b&gt;hi&lt;/b&gt; (escaped, shown as literal text)
- B. Bold text 'hi'
- C. An empty string
- D. A RuntimeError

??? success "Answer Q52"
    **A**

    Auto-escaping (html strategy for .html.twig) converts the angle brackets to entities, so the literal markup is displayed as text rather than rendered as bold. To output real markup you would need |raw (only for trusted content).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q53.** Under the unanimous strategy, a voter returns false from voteOnAttribute() for an attribute it does not actually care about. Effect?  <small>_(Security)_</small>

- A. false is ACCESS_DENIED, which blocks access under unanimous; unrelated attributes must be filtered out in supports() so the voter abstains
- B. false is treated as abstain and has no effect on the outcome
- C. false grants access under unanimous
- D. It throws because the attribute is unsupported

??? success "Answer Q53"
    **A**

    Returning false from voteOnAttribute() maps to ACCESS_DENIED, not abstain. Under unanimous a single deny blocks access, so a voter that "says no to what isn't mine" silently breaks authorization. The correct pattern is to reject unrelated attributes/subjects in supports(), which makes the base Voter abstain (ACCESS_ABSTAIN, no effect). abstain and deny are distinct, and an unsupported attribute does not throw.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

**Q54.** What is the correct order of the submit-phase form events?  <small>_(Forms)_</small>

- A. PRE_SUBMIT -> SUBMIT -> POST_SUBMIT
- B. SUBMIT -> PRE_SUBMIT -> POST_SUBMIT
- C. PRE_SUBMIT -> POST_SUBMIT -> SUBMIT
- D. PRE_SET_DATA -> SUBMIT -> POST_SUBMIT

??? success "Answer Q54"
    **A**

    Submission dispatches PRE_SUBMIT (raw view data), SUBMIT (normalized), then POST_SUBMIT (bound model), in that order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/form/events.html)

**Q55.** What is the fully-qualified class of the routing attribute in Symfony 8?  <small>_(Routing)_</small>

- A. Symfony\Component\Routing\Attribute\Route
- B. Symfony\Component\Routing\Annotation\Route
- C. Symfony\Component\HttpKernel\Attribute\Route
- D. Symfony\Routing\Route

??? success "Answer Q55"
    **A**

    The routing attribute lives in the Attribute namespace since 6.4; the old Annotation\Route alias is removed in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q56.** Two services implement one interface with no default alias. Autowiring by that interface...  <small>_(Dependency Injection)_</small>

- A. Throws an ambiguity error at compile time
- B. Silently picks the first candidate
- C. Injects null
- D. Picks the last candidate

??? success "Answer Q56"
    **A**

    Ambiguity is a hard build error; you disambiguate with a named alias, #[Target], #[Autowire(service:)] or bind.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q57.** What is the signature of KernelBrowser::submitForm()?  <small>_(Testing)_</small>

- A. submitForm(string $button, array $fieldValues = [], string $method = 'POST')
- B. submitForm(array $fieldValues, string $button)
- C. submitForm(Form $form)
- D. submitForm(string $uri, array $data)

??? success "Answer Q57"
    **A**

    You identify the submit button by its text/name/id/value first, then pass the field values and optionally the HTTP method. submitForm() locates the enclosing form for you; if you already hold a Form object, use submit($form).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#submitting-forms)

**Q58.** For the URL `/search` (no `?page=`), what does `(int) $request->query->get('page')` evaluate to, and what is the safer call?  <small>_(Controllers)_</small>

- A. 0, because get() returns null which casts to 0; use getInt('page', 1) instead
- B. 1, because get() defaults to 1
- C. null, and the cast is skipped
- D. It throws because 'page' is missing

??? success "Answer Q58"
    **A**

    InputBag::get() returns null for a missing key (default default is null), and (int) null is 0 — rarely the intended fallback. getInt('page', 1) coerces and guarantees the type with an explicit default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q59.** Which clock is best for measuring elapsed durations and is immune to system clock changes?  <small>_(Miscellaneous)_</small>

- A. MonotonicClock
- B. NativeClock
- C. MockClock
- D. DatePoint

??? success "Answer Q59"
    **A**

    MonotonicClock uses a high-resolution monotonic source unaffected by NTP or manual clock adjustments, so duration diffs stay accurate. Wall-clock NativeClock can jump; MockClock is for tests; DatePoint is a date type, not a clock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/clock.html)

**Q60.** At which point is auto-escaping applied to a value?  <small>_(Twig)_</small>

- A. At print time on {{ }}, via EscaperExtension adding an implicit |escape
- B. When the variable is assigned with {% set %}
- C. When the controller passes the variable to the template
- D. During template compilation, once, on the source string

??? success "Answer Q60"
    **A**

    EscaperExtension inserts an implicit |escape(strategy) on every {{ }} output node that is not already marked safe — escaping happens when a value is printed, not when it is set. So {% set x = untrusted %} stores it raw; the escaping occurs only when you later print {{ x }}.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Extension/EscaperExtension.php)

**Q61.** What does the __Host- cookie name prefix force the browser to require? (choose one)  <small>_(HTTP)_</small>

- A. Secure, no Domain attribute, and Path=/ — the strictest scoping the browser enforces
- B. HttpOnly and SameSite=Strict only
- C. A matching Domain attribute and Max-Age
- D. Nothing; the prefix is purely cosmetic

??? success "Answer Q61"
    **A**

    A cookie named __Host-... is accepted only if it is Secure, has no Domain attribute (so it is locked to the exact host), and uses Path=/. This is the strongest same-origin scoping the browser guarantees, preventing subdomain injection. The related __Secure- prefix only requires the Secure flag.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#cookie_prefixes)

**Q62.** You have five heavy payment gateways but use exactly one per request, chosen by name. What is the best tool?  <small>_(Dependency Injection)_</small>

- A. A service locator (e.g. #[AutowireLocator]) so only the chosen gateway is built
- B. A tagged_iterator, iterating all five every request
- C. Injecting all five gateways in the constructor
- D. Injecting the whole container

??? success "Answer Q62"
    **A**

    Pick-one-of-many with heavy dependencies is the textbook case for a lazy locator: only the selected gateway is instantiated. A tagged_iterator or constructor-injecting all five would eagerly build every gateway, and injecting the whole container is the anti-pattern the locator replaces.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q63.** Which statement about PSR-6 vs PSR-16 is correct?  <small>_(Miscellaneous)_</small>

- A. PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not
- B. PSR-16 supports tags but PSR-6 does not
- C. Both are identical key/value APIs
- D. PSR-6 has no expiration support

??? success "Answer Q63"
    **A**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/cache.html)

**Q64.** A POST to /blog when the route is defined as /blog/ yields?  <small>_(Routing)_</small>

- A. 405 Method Not Allowed
- B. 301 redirect
- C. 200 OK
- D. 308 redirect

??? success "Answer Q64"
    **A**

    Redirecting a POST would alter the method, so the matcher returns 405 rather than a trailing-slash redirect. The auto-redirect is GET/HEAD only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-urls-with-trailing-slashes)

**Q65.** What does dd() do that dump() does not?  <small>_(Miscellaneous)_</small>

- A. It stops execution (exit) after dumping
- B. It writes the dump to a log file
- C. It serializes the value to JSON
- D. It dumps only scalar values

??? success "Answer Q65"
    **A**

    dd() means 'dump and die': it dumps then calls exit, halting the script. dump() records the variable and lets execution continue (the dump is shown in the toolbar/collector).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/var_dumper.html#the-dump-function)

**Q66.** For a factory-built service, where are its arguments passed?  <small>_(Dependency Injection)_</small>

- A. To the factory method
- B. To the class constructor
- C. To __invoke only
- D. They are ignored

??? success "Answer Q66"
    **A**

    With a factory, the container calls the factory and passes the definition's arguments to it, not to a constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q67.** What does app.environment return?  <small>_(Twig)_</small>

- A. The kernel environment string, e.g. 'dev' or 'prod'
- B. The operating-system environment variables
- C. The APP_ENV file path
- D. A boolean debug flag

??? success "Answer Q67"
    **A**

    app.environment is the kernel environment (dev/prod/test); app.debug is the boolean debug flag. They are unrelated to OS env vars.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q68.** What gives Symfony's dump() its rich, collapsible HTML output rather than plain var_dump?  <small>_(Twig)_</small>

- A. Symfony's DumpExtension backed by VarDumper (VarCloner + HtmlDumper), replacing Twig's plain DebugExtension
- B. Twig's core DebugExtension already produces collapsible HTML
- C. PHP's native var_dump() with an ini setting
- D. The Profiler rewrites var_dump output

??? success "Answer Q68"
    **A**

    Twig core ships DebugExtension with a plain var_dump-based dump(). Symfony augments it with DumpExtension wired to VarDumper (VarCloner clones the variable, HtmlDumper renders collapsible, syntax-highlighted output and routes dumps to the toolbar). Cloning first also makes dumping large graphs safe (depth-limited).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/DumpExtension.php)

**Q69.** What does #[Assert\Email] report for an empty string value?  <small>_(Validation)_</small>

- A. No violation — empty and null values pass most constraints
- B. A violation, because '' is not a valid email
- C. A PHP TypeError
- D. It depends on the charset option

??? success "Answer Q69"
    **A**

    Like Url, Regex and most value constraints, Email skips empty/null values. Combine it with NotBlank when an empty value must be rejected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/constraints/Email.html)

**Q70.** What is the key difference between getPreferredFormat() and getAcceptableContentTypes()? (choose one)  <small>_(HTTP)_</small>

- A. getPreferredFormat() returns a Symfony format name (e.g. 'json'); getAcceptableContentTypes() returns raw MIME types
- B. They are aliases returning the same value
- C. getPreferredFormat() returns MIME types; getAcceptableContentTypes() returns formats
- D. getPreferredFormat() reads Accept-Language, not Accept

??? success "Answer Q70"
    **A**

    getPreferredFormat() maps the client's Accept header to a short Symfony format (html, json, xml, csv...), best for a match expression. getAcceptableContentTypes() returns the raw MIME strings ordered by preference. Confusing format names with MIME types is a classic trap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q71.** How are application service IDs written in modern Symfony?  <small>_(Architecture)_</small>

- A. As the fully-qualified class name (FQCN)
- B. As lowercase dotted strings only
- C. As random UUIDs

??? success "Answer Q71"
    **A**

    The service id is the FQCN; autowiring matches type-hints to these ids.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q72.** What binds a single typed query parameter such as ?page=2 to an int argument?  <small>_(Controllers)_</small>

- A. #[MapQueryParameter]
- B. #[MapQueryString]
- C. #[MapRequestPayload]

??? success "Answer Q72"
    **A**

    #[MapQueryParameter] binds one query value with casting; #[MapQueryString] maps the whole query string into a DTO.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

**Q73.** True or False: a firewall with stateless: true still calls refreshUser() on every request.  <small>_(Security)_</small>

- A. True
- B. False

??? success "Answer Q73"
    **B**

    False. refreshUser() is invoked by the ContextListener, which only exists on stateful firewalls. A stateless firewall stores no token in the session, so there is nothing to refresh — the user is re-loaded from scratch by the authenticator on each request instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security/user_providers.html)

**Q74.** When does a lazy Symfony session actually start (session_start + Set-Cookie)?  <small>_(Controllers)_</small>

- A. Only when the session is first read or written
- B. On every request automatically
- C. When the kernel boots

??? success "Answer Q74"
    **A**

    Lazy sessions avoid emitting a session cookie for requests that never touch the session, preserving cacheability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

**Q75.** Which default group name does an unqualified constraint belong to?  <small>_(Validation)_</small>

- A. Default (capital D)
- B. default (lowercase)
- C. the fully qualified class name
- D. Base

??? success "Answer Q75"
    **A**

    The implicit group is 'Default' with a capital D; group names are case-sensitive, so 'default' would be a different (empty) group.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/validation/groups.html)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
