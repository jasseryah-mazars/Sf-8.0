# Mock Exam B (Exam Mode)

!!! note "Three independent papers"
    This is **Mock B**. Also try: [Mock A](mock-exam.md) · [Mock C](mock-exam-c.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** Where does a controller read incoming cookies from?  <small>_(Controllers)_</small>

- A. $request->cookies
- B. $request->headers
- C. $_SESSION

??? success "Answer Q1"
    **A**

    The cookies ParameterBag wraps $_COOKIE; responses set cookies via $response->headers->setCookie().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q2.** What does {% include ['a.html.twig', 'b.html.twig'] %} render?  <small>_(Twig)_</small>

- A. The first template in the list that exists
- B. Both templates concatenated
- C. The last template
- D. An error

??? success "Answer Q2"
    **A**

    Passing an array of names renders the first template that can be loaded, which is handy for theme overrides.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q3.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(Miscellaneous)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q3"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

**Q4.** What are the integer values of the voter constants?  <small>_(Security)_</small>

- A. ACCESS_GRANTED = 1, ACCESS_ABSTAIN = 0, ACCESS_DENIED = -1
- B. GRANTED = 0, DENIED = 1, ABSTAIN = 2
- C. GRANTED = true, DENIED = false
- D. All three are 0

??? success "Answer Q4"
    **A**

    These integer constants drive the strategy arithmetic in the AccessDecisionManager.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/VoterInterface.php)

**Q5.** What does the special _format parameter do when matched?  <small>_(Routing)_</small>

- A. Sets the request format, influencing the response Content-Type
- B. Only appears in the URL with no effect
- C. Selects which controller runs
- D. Sets the HTTP method

??? success "Answer Q5"
    **A**

    RouterListener applies _format via Request::setRequestFormat(), driving content negotiation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#special-parameters)

**Q6.** Under `declare(strict_types=1)`, passing a string to an int parameter throws…  <small>_(PHP & Web Security)_</small>

- A. TypeError (a subclass of Error)
- B. InvalidArgumentException
- C. Only a warning
- D. ValueError

??? success "Answer Q6"
    **A**

    Strict typing rejects the wrong scalar type with a TypeError, which is an Error, not an Exception.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

**Q7.** Can symfony/routing be used without FrameworkBundle?  <small>_(Architecture)_</small>

- A. Yes — it is a standalone component
- B. No — it requires the kernel
- C. Only in the dev environment

??? success "Answer Q7"
    **A**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

**Q8.** Do conditions affect URL generation with generateUrl()?  <small>_(Routing)_</small>

- A. No — conditions are matching-only
- B. Yes, generation fails if the condition is false
- C. Only for absolute URLs
- D. Only in debug mode

??? success "Answer Q8"
    **A**

    There is no request to evaluate during generation, so conditions never influence generated URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-expressions)

**Q9.** How often does a new Symfony minor version ship?  <small>_(Architecture)_</small>

- A. Every six months, in May and November
- B. Every month
- C. Every two years

??? success "Answer Q9"
    **A**

    Symfony uses a fixed time-based cadence: a minor every May and November, a major every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q10.** Which files hold the compiled router in the cache directory?  <small>_(Routing)_</small>

- A. url_matching_routes.php and url_generating_routes.php
- B. routes.php and router.php
- C. matcher.php and generator.php
- D. RouteCollection.php

??? success "Answer Q10"
    **A**

    The CompiledUrlMatcherDumper and CompiledUrlGeneratorDumper write these two files that the Router loads at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q11.** What is the safe way to pick a locale from the browser's Accept-Language? (choose one)  <small>_(HTTP)_</small>

- A. getPreferredLanguage(['en','fr']) with a whitelist
- B. getLocale()
- C. getLanguages()[0]
- D. reading $_SERVER['HTTP_ACCEPT_LANGUAGE']

??? success "Answer Q11"
    **A**

    The whitelist form guarantees a supported locale; the others may return one you do not support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html#the-locale-used-in-translations)

**Q12.** Which class backs $request->query, $request->request and $request->cookies? (choose one)  <small>_(HTTP)_</small>

- A. InputBag
- B. ParameterBag
- C. HeaderBag
- D. ServerBag

??? success "Answer Q12"
    **A**

    query, request and cookies are InputBag (scalar-restricted); attributes is a plain ParameterBag, server is ServerBag, headers is HeaderBag.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

**Q13.** When is %env(DATABASE_URL)% resolved?  <small>_(Dependency Injection)_</small>

- A. At runtime, via an env-var processor
- B. At compilation, frozen into the cache
- C. When .env is parsed at deploy time only
- D. Never; it is a literal string

??? success "Answer Q13"
    **A**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

**Q14.** Where do you place a custom production 404 template?  <small>_(Controllers)_</small>

- A. templates/bundles/TwigBundle/Exception/error404.html.twig
- B. public/404.html
- C. config/errors.yaml

??? success "Answer Q14"
    **A**

    The Twig error renderer looks up per-status templates in that path in the prod environment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q15.** Which two methods do you typically override in an AbstractType?  <small>_(Forms)_</small>

- A. buildForm(FormBuilderInterface, array) and configureOptions(OptionsResolver)
- B. build() and getOptions()
- C. getName() and buildView()
- D. configureFields() and setDefaults()

??? success "Answer Q15"
    **A**

    buildForm() adds fields to the builder; configureOptions() declares the type's options via OptionsResolver. getName() was removed; buildView() exists but is not the primary pair.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

**Q16.** Which built-in authenticator uses a token_handler returning a UserBadge?  <small>_(Security)_</small>

- A. access_token
- B. form_login
- C. http_basic
- D. remember_me

??? success "Answer Q16"
    **A**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/access_token.html)

**Q17.** What should a transformer throw when input cannot be converted?  <small>_(Forms)_</small>

- A. TransformationFailedException
- B. InvalidArgumentException
- C. ValidatorException
- D. Nothing — return null

??? success "Answer Q17"
    **A**

    TransformationFailedException is caught by the form and turned into a field-level invalid state showing the field's invalid_message, not a 500.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

**Q18.** Which option mode adds a `--no-foo` counterpart to `--foo`?  <small>_(Console)_</small>

- A. InputOption::VALUE_NEGATABLE
- B. InputOption::VALUE_NONE
- C. InputOption::VALUE_OPTIONAL
- D. InputOption::VALUE_IS_ARRAY

??? success "Answer Q18"
    **A**

    VALUE_NEGATABLE (16) generates the --no- twin; the value is true, false, or its default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

**Q19.** The user is authenticated but lacks permission for a resource. Which status? (choose one)  <small>_(HTTP)_</small>

- A. 403 Forbidden
- B. 401 Unauthorized
- C. 400 Bad Request
- D. 422 Unprocessable Content

??? success "Answer Q19"
    **A**

    401 means unauthenticated (send WWW-Authenticate); 403 means authenticated but not authorized — re-authenticating will not help.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

**Q20.** No access_control rule matches the request. What happens?  <small>_(Security)_</small>

- A. Access is allowed (deferred to controller-level guards)
- B. 403 Forbidden
- C. 401 Unauthorized
- D. The firewall re-authenticates

??? success "Answer Q20"
    **A**

    access_control only restricts on a matching rule; with no match there is no URL-level restriction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

**Q21.** Which Finder method defines the directories to search?  <small>_(Miscellaneous)_</small>

- A. in()
- B. from()
- C. search()
- D. path()

??? success "Answer Q21"
    **A**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

**Q22.** What visibility should application services have by default?  <small>_(Architecture)_</small>

- A. Private
- B. Public
- C. Protected

??? success "Answer Q22"
    **A**

    Private services let the DI compiler inline and remove them, and discourage the service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q23.** Which service selects the fragment renderer for render()/render_esi()?  <small>_(Twig)_</small>

- A. Symfony\Component\HttpKernel\Fragment\FragmentHandler
- B. Symfony\Component\Routing\Generator\UrlGenerator
- C. Twig\Extension\EscaperExtension
- D. Symfony\Bridge\Twig\AppVariable

??? success "Answer Q23"
    **A**

    HttpKernelExtension delegates to FragmentHandler, which picks a FragmentRendererInterface (inline, esi, hinclude) by strategy name.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

**Q24.** How is an abstract class conventionally named?  <small>_(Architecture)_</small>

- A. With an Abstract prefix, e.g. AbstractController
- B. With an Abstract suffix, e.g. ControllerAbstract
- C. With an _abstract suffix

??? success "Answer Q24"
    **A**

    Abstract classes take the Abstract prefix; interfaces use the Interface suffix and traits use the Trait suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

**Q25.** Inside a compiler pass process() method, what should you manipulate?  <small>_(Dependency Injection)_</small>

- A. Definition objects (build-time metadata)
- B. Live service instances via get()
- C. The current HTTP request
- D. The runtime event dispatcher

??? success "Answer Q25"
    **A**

    Compilation deals only with definitions; nothing is instantiated yet, so calling get() inside a pass is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

**Q26.** To apply constraints to every element of an indexed array, which constraint do you use?  <small>_(Validation)_</small>

- A. All
- B. Collection
- C. Count
- D. Unique

??? success "Answer Q26"
    **A**

    All applies the given constraints to each element of a collection. Collection validates the keys of an associative array; they are not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/All.html)

**Q27.** Which ChoiceType options render checkboxes?  <small>_(Forms)_</small>

- A. expanded => true, multiple => true
- B. expanded => false, multiple => true
- C. expanded => true, multiple => false
- D. widget => 'checkbox'

??? success "Answer Q27"
    **A**

    expanded + multiple renders checkboxes; expanded + single renders radios; collapsed renders a select element.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/choice.html)

**Q28.** The base Voter's supports() returns false. What is the resulting vote?  <small>_(Security)_</small>

- A. ACCESS_ABSTAIN
- B. ACCESS_DENIED
- C. ACCESS_GRANTED
- D. An exception is thrown

??? success "Answer Q28"
    **A**

    The abstract Voter abstains for unsupported attributes/subjects; it never calls voteOnAttribute() in that case.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/Voter/Voter.php)

**Q29.** A message is routed to an async transport. During dispatch() in the web process, the handler…  <small>_(Miscellaneous)_</small>

- A. does not run — SendMessageMiddleware serializes and sends it, stopping the bus
- B. runs immediately and is also queued
- C. runs only if a worker is currently active
- D. throws NoHandlerForMessageException

??? success "Answer Q29"
    **A**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages)

**Q30.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(Miscellaneous)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q30"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

**Q31.** Which adapter keeps entries only for the current process (ideal for tests)?  <small>_(Miscellaneous)_</small>

- A. ArrayAdapter
- B. FilesystemAdapter
- C. RedisAdapter
- D. ApcuAdapter

??? success "Answer Q31"
    **A**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

**Q32.** What does $client->loginUser($user) do?  <small>_(Testing)_</small>

- A. Authenticates the session with the given UserInterface, skipping the login form
- B. Submits the login form with the user's credentials
- C. Creates the user record in the database
- D. Returns a signed JWT for the user

??? success "Answer Q32"
    **A**

    loginUser() injects a security token for a real user object so you can test authorized behaviour without driving the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#logging-in-users-authentication)

**Q33.** With #[MapUploadedFile] and a failing File constraint, what happens?  <small>_(Controllers)_</small>

- A. An HTTP exception is thrown before the action body runs
- B. The argument is set to null
- C. A flash message is added

??? success "Answer Q33"
    **A**

    The resolver validates the upload and aborts with an HTTP error when a constraint fails, so the body never executes with invalid input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q34.** You must test a service that needs the container but sends no HTTP requests. Which base class fits best?  <small>_(Testing)_</small>

- A. KernelTestCase — boots the kernel and exposes the container, without an HTTP client
- B. WebTestCase — because only it can access the container
- C. PHPUnit\Framework\TestCase — the container is available by default
- D. DoctrineTestCase

??? success "Answer Q34"
    **A**

    KernelTestCase boots the kernel and gives you self::getContainer() with no browser. WebTestCase adds the HTTP client and is reserved for tests that make requests; a plain TestCase boots no kernel at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#integration-tests)

**Q35.** How do you retrieve a synchronous handler's return value after MessageBusInterface::dispatch()?  <small>_(Miscellaneous)_</small>

- A. $envelope->last(HandledStamp::class)->getResult()
- B. The value is returned directly by dispatch()
- C. $envelope->getResult()
- D. $bus->getLastResult()

??? success "Answer Q35"
    **A**

    dispatch() returns an Envelope. For a single sync handler you read its result via the HandledStamp: $envelope->last(HandledStamp::class)->getResult(). Use HandleTrait to unwrap it in a query bus.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

**Q36.** What does requires_channel: https do, and when?  <small>_(Security)_</small>

- A. Redirects matching paths to HTTPS before authentication runs
- B. Rejects HTTPS requests
- C. Runs only after a successful login
- D. Encrypts the session cookie

??? success "Answer Q36"
    **A**

    The ChannelListener enforces requires_channel before authentication, so even the login page is redirected to HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

**Q37.** To reference service('x') in a routing condition, service x must…  <small>_(Routing)_</small>

- A. Be tagged routing.condition_service (e.g. via #[AsRoutingConditionService])
- B. Be public
- C. Implement RouterInterface
- D. Extend AbstractController

??? success "Answer Q37"
    **A**

    Only services tagged routing.condition_service are exposed to the routing expression language.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-expressions)

**Q38.** What does a tagged_locator argument inject?  <small>_(Dependency Injection)_</small>

- A. A lazy ServiceLocator keyed by an index
- B. An array of already-instantiated services
- C. A compiler pass
- D. The raw tag name string

??? success "Answer Q38"
    **A**

    tagged_locator injects a ServiceLocator that instantiates services on demand, keyed by the configured index; tagged_iterator yields instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q39.** Which special attribute is broader?  <small>_(Security)_</small>

- A. IS_AUTHENTICATED_REMEMBERED (fully-authenticated users also satisfy it)
- B. IS_AUTHENTICATED_FULLY
- C. They are equal
- D. Neither implies the other

??? success "Answer Q39"
    **A**

    Fully-authenticated users satisfy IS_AUTHENTICATED_REMEMBERED, but remember-me users do NOT satisfy IS_AUTHENTICATED_FULLY.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#security-authorization-access-decision)

**Q40.** When does a StreamedResponse produce its body?  <small>_(Controllers)_</small>

- A. During send(), by invoking its callback
- B. When it is constructed
- C. During the kernel.controller event

??? success "Answer Q40"
    **A**

    The callback runs at send time and streams output; you cannot change headers once streaming has begun.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#streaming-a-response)

**Q41.** Which objects exist only at build time, not at runtime? (choose one)  <small>_(Dependency Injection)_</small>

- A. Definition, Reference, Alias and Parameter metadata objects
- B. The service instances themselves
- C. The compiled container class
- D. The RequestStack

??? success "Answer Q41"
    **A**

    Definition/Reference/Alias/Parameter are build-time recipes held by the ContainerBuilder; the runtime container holds instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection/compilation.html)

**Q42.** How is an instance-method factory referenced in YAML?  <small>_(Dependency Injection)_</small>

- A. factory: ['@service_id', 'method']
- B. factory: '@service_id::method'
- C. factory: 'service_id.method'
- D. factory: @service_id

??? success "Answer Q42"
    **A**

    An array of [reference, method] denotes a method call on a service; a static factory uses the 'Class::method' string form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

**Q43.** What does MoneyType's divisor option do?  <small>_(Forms)_</small>

- A. Scales the model value (e.g. 100 lets you store integer cents)
- B. Sets the currency symbol
- C. Rounds to N decimals
- D. Limits the maximum amount

??? success "Answer Q43"
    **A**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/money.html)

**Q44.** Which service does FormInterface::handleRequest() delegate to under FrameworkBundle?  <small>_(Forms)_</small>

- A. HttpFoundationRequestHandler
- B. NativeRequestHandler
- C. FormFactory
- D. RequestStack

??? success "Answer Q44"
    **A**

    With HttpFoundation available, the form's request handler is HttpFoundationRequestHandler; NativeRequestHandler is the fallback when working with PHP superglobals directly.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Extension/HttpFoundation/HttpFoundationRequestHandler.php)

**Q45.** What does the #[Target('requestLogger')] attribute do?  <small>_(Dependency Injection)_</small>

- A. Selects the named autowiring alias explicitly, decoupled from the parameter name
- B. Creates a new service definition
- C. Adds a tag to the service
- D. Makes the service public

??? success "Answer Q45"
    **A**

    #[Target] binds to a named autowiring alias by name, so renaming the constructor parameter does not break wiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html#fixing-non-autowireable-arguments)

**Q46.** What must a class annotated with #[Assert\GroupSequenceProvider] provide?  <small>_(Validation)_</small>

- A. An implementation of GroupSequenceProviderInterface::getGroupSequence()
- B. A static groupSequence() method
- C. It must extend the GroupSequence class
- D. A compiler pass registration

??? success "Answer Q46"
    **A**

    The provider attribute delegates to getGroupSequence() from GroupSequenceProviderInterface, evaluated on each validation so the sequence can depend on the object's state.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/sequence_provider.html)

**Q47.** What is the purpose of DispatchAfterCurrentBusStamp?  <small>_(Miscellaneous)_</small>

- A. Defer delivery of a message dispatched inside a handler until the current handling finishes successfully
- B. Send the message to every bus in the application
- C. Add a delay equal to the current bus latency
- D. Retry the message on the next bus in a chain

??? success "Answer Q47"
    **A**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/dispatch_after_current_bus.html)

**Q48.** What does lazy: true achieve on a firewall?  <small>_(Security)_</small>

- A. Authentication is deferred until the token is actually read
- B. It disables the session entirely
- C. It caches the authenticated token forever
- D. It runs all authenticators eagerly on every request

??? success "Answer Q48"
    **A**

    A lazy firewall only authenticates when the token is accessed (e.g. is_granted/getUser), so fully public pages skip auth and session loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

**Q49.** Which statement about NotBlank and NotNull is correct?  <small>_(Validation)_</small>

- A. NotBlank rejects an empty string; NotNull accepts an empty string
- B. They are aliases for the same check
- C. NotNull rejects an empty string; NotBlank accepts it
- D. Both reject the integer 0

??? success "Answer Q49"
    **A**

    NotBlank fails on '', [], and blank strings; NotNull only fails on a strict null, so '' and 0 pass NotNull. This is a classic exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/NotBlank.html)

**Q50.** What is the correct way to store user passwords?  <small>_(PHP & Web Security)_</small>

- A. password_hash() with bcrypt or argon2id
- B. SHA-256 with a single static salt
- C. MD5
- D. Reversible encryption

??? success "Answer Q50"
    **A**

    Adaptive, salted hashing (bcrypt/argon2id) resists brute-force; the salt is embedded in the hash and verified with password_verify().

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.password-hash.php)

**Q51.** Where do you override the default 404 error template?  <small>_(Architecture)_</small>

- A. templates/bundles/TwigBundle/Exception/error404.html.twig
- B. templates/error/404.twig
- C. Directly in vendor/

??? success "Answer Q51"
    **A**

    TwigBundle resolves error templates from templates/bundles/TwigBundle/Exception/, falling back to error.html.twig.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q52.** What is loop.index on the first iteration of a for loop?  <small>_(Twig)_</small>

- A. 1
- B. 0
- C. null
- D. -1

??? success "Answer Q52"
    **A**

    loop.index is 1-based; loop.index0 is the 0-based counterpart.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

**Q53.** How does a ServiceLocator differ from injecting the whole container?  <small>_(Dependency Injection)_</small>

- A. It exposes only an explicitly declared, whitelisted set of services
- B. It is eager while the container is lazy
- C. It cannot instantiate services
- D. There is no real difference

??? success "Answer Q53"
    **A**

    A locator's set is explicit and analysable; injecting the whole container hides dependencies and is an anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q54.** How does a recipe auto-register a bundle?  <small>_(Architecture)_</small>

- A. By writing an entry into config/bundles.php
- B. Via an #[AsBundle] attribute
- C. By editing services.yaml

??? success "Answer Q54"
    **A**

    The bundles configurator adds the bundle class to config/bundles.php, which the kernel reads at boot via MicroKernelTrait::registerBundles().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q55.** Why can self::getContainer()->get() return a private service in a test?  <small>_(Testing)_</small>

- A. It returns the special test container (test.service_container) that exposes private/non-shared services
- B. All services become public in the test environment
- C. It uses reflection to bypass service visibility
- D. Private services are compiled as public only for WebTestCase

??? success "Answer Q55"
    **A**

    The test environment (framework.test: true) compiles a TestContainer that keeps references to used private/non-shared services so tests can fetch and replace them. static::$kernel->getContainer() does not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

**Q56.** Why declare the command name in #[AsCommand] rather than only in configure()?  <small>_(Console)_</small>

- A. It lets the command loader know the name without instantiating the class (lazy loading)
- B. configure() cannot set a name at all
- C. Attributes execute faster at runtime
- D. It is required for execute() to run

??? success "Answer Q56"
    **A**

    The attribute exposes name/aliases at compile time so ContainerCommandLoader maps name→id and instantiates the command only when invoked.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/commands_as_services.html)

**Q57.** Which class moves or hides the terminal cursor?  <small>_(Console)_</small>

- A. Symfony\Component\Console\Cursor
- B. FormatterHelper
- C. Table
- D. ProgressBar

??? success "Answer Q57"
    **A**

    Cursor issues ANSI escape sequences to move/hide/show the cursor and clear lines.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/helpers/index.html)

**Q58.** How is an invokable single-action controller referenced in the `_controller` attribute? (choose one)  <small>_(Controllers)_</small>

- A. The fully-qualified class name only (Symfony calls __invoke)
- B. Class::__invokeAction
- C. class#invoke

??? success "Answer Q58"
    **A**

    For an invokable controller you reference only the class; the ControllerResolver detects the __invoke() method automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q59.** How do you skip iterations in a Twig for loop?  <small>_(Twig)_</small>

- A. Filter the source, e.g. {% for x in items if x.active %}
- B. Use {% continue %}
- C. Use {% break %}
- D. Call loop.skip()

??? success "Answer Q59"
    **A**

    Twig has no break/continue by design; filter the iterable inline or use an if inside the body.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

**Q60.** Two providers are defined and a firewall omits the provider key. Result?  <small>_(Security)_</small>

- A. Configuration error — the provider is ambiguous
- B. It silently uses the first provider
- C. It merges both providers
- D. The firewall becomes anonymous

??? success "Answer Q60"
    **A**

    With multiple providers there is no implicit default; each firewall must name its provider explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

**Q61.** How is #[Assert\...] attribute metadata turned into constraints at runtime?  <small>_(Validation)_</small>

- A. AttributeLoader builds ClassMetadata once, cached in a PSR-6 pool
- B. It is re-parsed by reflection on every validate() call
- C. It is compiled into the DI container and never changes
- D. It is read from a database mapping table

??? success "Answer Q61"
    **A**

    LazyLoadingMetadataFactory uses AttributeLoader to reflect over the class and build ClassMetadata, which is cached (validator.mapping.cache) so the reflection cost is paid once per class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q62.** Which function emits a Symfony deprecation notice, and from which package?  <small>_(Architecture)_</small>

- A. trigger_deprecation() from symfony/deprecation-contracts
- B. deprecate() from symfony/http-kernel
- C. There is no helper; you must call trigger_error() directly

??? success "Answer Q62"
    **A**

    symfony/deprecation-contracts provides trigger_deprecation($package, $version, $message, ...$args), which formats an E_USER_DEPRECATED notice.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q63.** Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?  <small>_(Miscellaneous)_</small>

- A. --limit (max messages) and --time-limit (max seconds), optionally with memory limits
- B. --kill and --restart
- C. --stop-now only
- D. --reload after each message

??? success "Answer Q63"
    **A**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

**Q64.** What sets the request locale when a route defines {_locale}? (choose one)  <small>_(HTTP)_</small>

- A. LocaleListener calls Request::setLocale() on kernel.request
- B. The Router sets it directly
- C. Twig sets it during rendering
- D. The Translator sets it

??? success "Answer Q64"
    **A**

    LocaleListener reads the _locale attribute and calls setLocale(); LocaleAwareListener then propagates it to LocaleAware services.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleListener.php)

**Q65.** Which catch clause catches BOTH a TypeError and a RuntimeException?  <small>_(PHP & Web Security)_</small>

- A. catch (\Throwable $e)
- B. catch (\Exception $e)
- C. catch (\Error $e)
- D. catch (\LogicException $e)

??? success "Answer Q65"
    **A**

    Throwable is the only common ancestor of both Error (TypeError) and Exception (RuntimeException).

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.throwable.php)

**Q66.** Why call refresh() during a long critical section?  <small>_(Miscellaneous)_</small>

- A. To extend the lock's TTL so it is not considered expired mid-job
- B. To release then reacquire the lock
- C. To switch to a different store
- D. To convert it to a shared lock

??? success "Answer Q66"
    **A**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

**Q67.** What supplies registerBundles() and registerContainerConfiguration() in a skeleton Kernel?  <small>_(Architecture)_</small>

- A. MicroKernelTrait
- B. AbstractController
- C. The FrameworkBundle extension

??? success "Answer Q67"
    **A**

    App\\Kernel uses MicroKernelTrait, which implements the boilerplate to load bundles from config/bundles.php and configuration from config/.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/micro_kernel_trait.html)

**Q68.** `$this->addFlash('notice', 'Saved')` is shorthand for which call?  <small>_(Controllers)_</small>

- A. getSession()->getFlashBag()->add('notice', 'Saved')
- B. Setting a response header
- C. Writing a cookie

??? success "Answer Q68"
    **A**

    addFlash() is an AbstractController convenience over the session flash bag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q69.** Does Symfony guess the user's locale from the Accept-Language header by default?  <small>_(Routing)_</small>

- A. No — you must enable set_locale_from_accept_language or do it manually
- B. Yes, always
- C. Only for API routes
- D. Only in the dev environment

??? success "Answer Q69"
    **A**

    Locale guessing precedence is matched _locale, then the sticky session locale, then default_locale; Accept-Language is opt-in.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#localized-routes-i18n)

**Q70.** With #[Cache(lastModified: 'post.getUpdatedAt()')], when can a 304 be returned?  <small>_(HTTP Caching)_</small>

- A. Before the controller body runs, during kernel.controller_arguments
- B. Only after the controller has fully rendered the response
- C. Only inside a kernel.terminate listener
- D. Never — expressions cannot short-circuit

??? success "Answer Q70"
    **A**

    CacheAttributeListener evaluates the expression on CONTROLLER_ARGUMENTS (priority 10) and, if the request is up to date, replaces the controller so a 304 is returned without running the body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

**Q71.** Which attribute marks a service as a message handler in Symfony 8?  <small>_(Miscellaneous)_</small>

- A. #[AsMessageHandler]
- B. #[MessageHandler]
- C. #[AsHandler]
- D. #[Handler]

??? success "Answer Q71"
    **A**

    Symfony\Component\Messenger\Attribute\AsMessageHandler registers an invokable service (or a specific method) as a handler for its typed message argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#registering-handlers)

**Q72.** When must $client->enableProfiler() be called?  <small>_(Testing)_</small>

- A. Before the request whose profile you want to read
- B. After the request, before getProfile()
- C. Only inside setUp()
- D. Never — profiling is always on in the test environment

??? success "Answer Q72"
    **A**

    enableProfiler() opts the next request into profiling; calling it after the request collects nothing and getProfile() returns false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

**Q73.** Which attribute injects the decorated (inner) service into a decorator?  <small>_(Dependency Injection)_</small>

- A. #[AutowireDecorated]
- B. #[AsDecorator]
- C. #[Inner]
- D. #[Decorated]

??? success "Answer Q73"
    **A**

    #[AsDecorator] declares the decoration; #[AutowireDecorated] resolves the parameter to the .inner service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q74.** What does {{ 7 // 2 }} output in Twig?  <small>_(Twig)_</small>

- A. 3
- B. 3.5
- C. 4
- D. An error

??? success "Answer Q74"
    **A**

    // is integer (floor) division in Twig; / performs float division and would return 3.5.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#math)

**Q75.** What does ResponseInterface::getContent() do on a 500 response by default? (choose one)  <small>_(HTTP)_</small>

- A. Throws a ServerExceptionInterface
- B. Returns the response body
- C. Returns an empty string
- D. Returns null

??? success "Answer Q75"
    **A**

    By default getContent()/toArray() throw on 3xx/4xx/5xx; pass false (or the throw option) to read the body without throwing. getStatusCode() never throws.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_client.html#handling-exceptions)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
