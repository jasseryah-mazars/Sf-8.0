# Mock Exam (Exam Mode)

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** Which check can pass a subject to voters?  <small>_(Security)_</small>

- A. isGranted('EDIT', $post)
- B. An access_control rule
- C. role_hierarchy configuration
- D. The firewall pattern

??? success "Answer Q1"
    **A**

    Only the isGranted()/#[IsGranted]/denyAccessUnlessGranted() path carries a subject. access_control is URL-based and cannot pass a subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

**Q2.** How is an inline (embedded) image referenced from an email's HTML body?  <small>_(Miscellaneous)_</small>

- A. Via a cid: reference produced by embed()/embedFromPath()
- B. Only as an absolute external URL
- C. As a base64 data: URI hand-written by the developer
- D. Inline images are not supported

??? success "Answer Q2"
    **A**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

**Q3.** A compound form with no data_class set returns what from getData()?  <small>_(Forms)_</small>

- A. An associative array keyed by child field name
- B. Always null
- C. A stdClass instance
- D. A FormInterface

??? success "Answer Q3"
    **A**

    Without data_class the data mapper maps children into and out of an array. Set data_class to bind the form to an object instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_class.html)

**Q4.** A custom filter returns '<b>x</b>' but the page shows escaped text. Why?  <small>_(Twig)_</small>

- A. The filter must be declared with the is_safe => ['html'] option
- B. Twig never escapes filter output
- C. You must call |raw on the input
- D. It is a Twig bug

??? success "Answer Q4"
    **A**

    Filter/function output is auto-escaped unless the TwigFilter/TwigFunction declares is_safe for the relevant context.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

**Q5.** Does Symfony guess the user's locale from the Accept-Language header by default?  <small>_(Routing)_</small>

- A. No — you must enable set_locale_from_accept_language or do it manually
- B. Yes, always
- C. Only for API routes
- D. Only in the dev environment

??? success "Answer Q5"
    **A**

    Locale guessing precedence is matched _locale, then the sticky session locale, then default_locale; Accept-Language is opt-in.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#localized-routes-i18n)

**Q6.** How do you make a failing handler skip retries and go straight to the failure transport?  <small>_(Miscellaneous)_</small>

- A. Throw UnrecoverableMessageHandlingException
- B. Return false from the handler
- C. Add a DelayStamp(0)
- D. Call $envelope->stopPropagation()

??? success "Answer Q6"
    **A**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

**Q7.** Which built-in authenticator uses a token_handler returning a UserBadge?  <small>_(Security)_</small>

- A. access_token
- B. form_login
- C. http_basic
- D. remember_me

??? success "Answer Q7"
    **A**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/access_token.html)

**Q8.** ClockInterface::now() returns what type?  <small>_(Miscellaneous)_</small>

- A. A \DateTimeImmutable (a DatePoint)
- B. A Unix timestamp int
- C. A mutable \DateTime
- D. A float of seconds

??? success "Answer Q8"
    **A**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q9.** Two providers are defined and a firewall omits the provider key. Result?  <small>_(Security)_</small>

- A. Configuration error — the provider is ambiguous
- B. It silently uses the first provider
- C. It merges both providers
- D. The firewall becomes anonymous

??? success "Answer Q9"
    **A**

    With multiple providers there is no implicit default; each firewall must name its provider explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

**Q10.** A cookie sent with SameSite=None also requires which attribute?  <small>_(Controllers)_</small>

- A. Secure=true
- B. HttpOnly=false
- C. A domain attribute

??? success "Answer Q10"
    **A**

    Modern browsers reject SameSite=None cookies unless they are marked Secure (HTTPS-only).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#setting-cookies)

**Q11.** Two services implement one interface with no default alias. Autowiring by that interface...  <small>_(Dependency Injection)_</small>

- A. Throws an ambiguity error at compile time
- B. Silently picks the first candidate
- C. Injects null
- D. Picks the last candidate

??? success "Answer Q11"
    **A**

    Ambiguity is a hard build error; you disambiguate with a named alias, #[Target], #[Autowire(service:)] or bind.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

**Q12.** What is written to var/cache/prod/ after compilation?  <small>_(Dependency Injection)_</small>

- A. A dumped, optimised PHP container class produced by PhpDumper
- B. The ContainerBuilder instance serialized
- C. The raw YAML service definitions
- D. Serialized service instances

??? success "Answer Q12"
    **A**

    PhpDumper writes a compiled PHP class with a method per service; the runtime uses it directly, never the ContainerBuilder.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection/compilation.html)

**Q13.** What does ServiceSubscriberInterface::getSubscribedServices() declare?  <small>_(Dependency Injection)_</small>

- A. The set of services the subscriber may lazily use, injected as a locator
- B. Instantiated services returned eagerly
- C. The compiler passes to register
- D. The whole container

??? success "Answer Q13"
    **A**

    It declares a whitelist; the container injects a matching ServiceLocator so services are built only when requested.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q14.** Why might clearCookie('token') fail to delete the cookie?  <small>_(Controllers)_</small>

- A. The path/domain do not match those used when the cookie was set
- B. clearCookie only works over HTTPS
- C. Cookies cannot be removed from the server side

??? success "Answer Q14"
    **A**

    Deletion sends an expired Set-Cookie scoped by path/domain; a mismatch targets a different cookie and leaves the original intact.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q15.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(Miscellaneous)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q15"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

**Q16.** What happens the first time you read a flash message (get/all or app.flashes)?  <small>_(Controllers)_</small>

- A. It is returned and removed (consumed)
- B. It stays until the session expires
- C. It is copied to the next request

??? success "Answer Q16"
    **A**

    Reading consumes flashes; use peek()/peekAll() to read without removing them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q17.** $response->headers is an instance of which class? (choose one)  <small>_(HTTP)_</small>

- A. ResponseHeaderBag
- B. HeaderBag
- C. ParameterBag
- D. InputBag

??? success "Answer Q17"
    **A**

    ResponseHeaderBag extends HeaderBag and adds cookie management plus Cache-Control normalisation.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

**Q18.** Which statement about NotBlank and NotNull is correct?  <small>_(Validation)_</small>

- A. NotBlank rejects an empty string; NotNull accepts an empty string
- B. They are aliases for the same check
- C. NotNull rejects an empty string; NotBlank accepts it
- D. Both reject the integer 0

??? success "Answer Q18"
    **A**

    NotBlank fails on '', [], and blank strings; NotNull only fails on a strict null, so '' and 0 pass NotNull. This is a classic exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/NotBlank.html)

**Q19.** Which kernel event lets a listener turn an exception into a Response?  <small>_(Controllers)_</small>

- A. kernel.exception (ExceptionEvent)
- B. kernel.view
- C. kernel.terminate

??? success "Answer Q19"
    **A**

    ExceptionEvent listeners can call setResponse(); otherwise the error controller renders the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q20.** What is the signature of an instance-method #[Assert\Callback]?  <small>_(Validation)_</small>

- A. public function m(ExecutionContextInterface $context, mixed $payload): void
- B. public function m(mixed $value): bool
- C. public function m(ExecutionContextInterface $context): string
- D. public function m(object $object, mixed $payload): void

??? success "Answer Q20"
    **A**

    An instance callback receives the ExecutionContext and the optional payload and returns void; violations are added through the context. The static form additionally receives the object as the first argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

**Q21.** When is %env(DATABASE_URL)% resolved?  <small>_(Dependency Injection)_</small>

- A. At runtime, via an env-var processor
- B. At compilation, frozen into the cache
- C. When .env is parsed at deploy time only
- D. Never; it is a literal string

??? success "Answer Q21"
    **A**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

**Q22.** Under PSR-4 rule `"App\\": "src/"`, where does `App\Foo\Bar` live?  <small>_(PHP & Web Security)_</small>

- A. src/Foo/Bar.php
- B. src/App/Foo/Bar.php
- C. src/foo/bar.php
- D. App/Foo/Bar.php

??? success "Answer Q22"
    **A**

    The prefix App\\ maps to src/, so only the remaining segments form the path; PSR-4 is case-sensitive on Linux.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/psr-4/)

**Q23.** What is the difference between {{ dump(x) }} and {% dump x %}?  <small>_(Twig)_</small>

- A. The function prints inline; the tag sends data to the collector without injecting markup
- B. They are identical
- C. The tag works in prod, the function does not
- D. The function only works in prod

??? success "Answer Q23"
    **A**

    The dump() function outputs where called; the {% dump %} tag routes the data to the profiler/toolbar without adding markup to the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

**Q24.** What does Response::prepare() do? (choose one)  <small>_(HTTP)_</small>

- A. Makes the response compliant with the request (charset, body for HEAD/304, protocol version)
- B. Sends the headers and body to the client
- C. Validates that the status code is in range
- D. JSON-encodes the content

??? success "Answer Q24"
    **A**

    prepare() normalises the response against the incoming Request; send() (sendHeaders + sendContent) actually transmits it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q25.** For a form's _method field to influence which route matches, you must…  <small>_(Routing)_</small>

- A. Call Request::enableHttpMethodParameterOverride()
- B. Add methods: ['_method']
- C. Do nothing — it is enabled by default
- D. Set framework.http_method_override: false

??? success "Answer Q25"
    **A**

    Method override is opt-in; once enabled, getMethod() returns the overridden verb that the matcher uses.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q26.** A cookie with neither Expires nor Max-Age is: (choose one)  <small>_(HTTP)_</small>

- A. a session cookie deleted when the browser closes
- B. permanent
- C. rejected by the browser
- D. valid for exactly 24 hours

??? success "Answer Q26"
    **A**

    With no lifetime attribute a cookie is a session cookie, removed when the browser session ends.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

**Q27.** What is the effect of $client->insulate()?  <small>_(Testing)_</small>

- A. Each request runs in a separate PHP subprocess, so in-process profiler/container access is lost
- B. Redirects are followed automatically
- C. The same kernel instance is reused forever
- D. Responses are cached between tests

??? success "Answer Q27"
    **A**

    Insulated requests run in a fresh subprocess to isolate global state, at the cost of losing in-process access to the profiler and container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/browser_kit.html)

**Q28.** In a decorator definition, what does @.inner reference?  <small>_(Dependency Injection)_</small>

- A. The original (decorated) service, renamed by the compiler
- B. The decorator service itself
- C. The parent bundle service
- D. A private alias of the container

??? success "Answer Q28"
    **A**

    DecoratorServicePass renames the decorated service and exposes it as .inner so the decorator can delegate to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q29.** By default in Symfony 8, is the _method parameter honoured? (choose one)  <small>_(HTTP)_</small>

- A. No — http_method_override defaults to false and must be enabled
- B. Yes, always
- C. Only for GET requests
- D. Only for JSON requests

??? success "Answer Q29"
    **A**

    You must enable framework.http_method_override (or call Request::enableHttpMethodParameterOverride()); it applies to POST only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q30.** Which class renders Twig templates into an email body?  <small>_(Miscellaneous)_</small>

- A. Symfony\Bridge\Twig\Mime\TemplatedEmail
- B. Symfony\Component\Mime\Email
- C. Symfony\Component\Mailer\Mailer
- D. Symfony\Component\Mime\Message

??? success "Answer Q30"
    **A**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

**Q31.** Which event lets you change the exit code regardless of outcome?  <small>_(Console)_</small>

- A. ConsoleEvents::TERMINATE
- B. ConsoleEvents::COMMAND
- C. ConsoleEvents::SIGNAL
- D. It cannot be changed after execution

??? success "Answer Q31"
    **A**

    ConsoleTerminateEvent::setExitCode() runs on every command and is the last chance to alter the exit code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/events.html)

**Q32.** How many access_control rules apply to a request?  <small>_(Security)_</small>

- A. Only the first matching rule
- B. All rules that match
- C. The most specific match
- D. The last matching rule

??? success "Answer Q32"
    **A**

    AccessMap returns the first match and evaluation stops. Order rules from specific to general.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

**Q33.** What does assertSame(1, '1') do?  <small>_(Testing)_</small>

- A. Fails, because the types differ (strict === comparison)
- B. Passes, because the values are loosely equal
- C. Emits a deprecation
- D. Throws a TypeError

??? success "Answer Q33"
    **A**

    assertSame uses ===, so int 1 and string '1' are not the same. Use assertEquals for loose (==) comparison.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/assertions.html#assertsame)

**Q34.** Which service selects the fragment renderer for render()/render_esi()?  <small>_(Twig)_</small>

- A. Symfony\Component\HttpKernel\Fragment\FragmentHandler
- B. Symfony\Component\Routing\Generator\UrlGenerator
- C. Twig\Extension\EscaperExtension
- D. Symfony\Bridge\Twig\AppVariable

??? success "Answer Q34"
    **A**

    HttpKernelExtension delegates to FragmentHandler, which picks a FragmentRendererInterface (inline, esi, hinclude) by strategy name.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

**Q35.** A class-level #[Route('/blog', name: 'app_blog_')] contributes what to its method routes?  <small>_(Routing)_</small>

- A. A path prefix and a name prefix
- B. A full route named app_blog_
- C. A default controller for the class
- D. Nothing without a methods option

??? success "Answer Q35"
    **A**

    Class-level route data merges as prefixes: the path is prepended and the name becomes a prefix for each action's route.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#creating-routes-as-attributes)

**Q36.** Which flag maps to VERBOSITY_VERY_VERBOSE?  <small>_(Console)_</small>

- A. -vv
- B. -v
- C. -vvv
- D. -q

??? success "Answer Q36"
    **A**

    -v is VERBOSE, -vv is VERY_VERBOSE, -vvv is DEBUG, -q is QUIET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

**Q37.** After `$b = clone $a;` where `$a->list` is an object, what is `$b->list`?  <small>_(PHP & Web Security)_</small>

- A. The same object as $a->list unless __clone() copies it
- B. Always an independent deep copy
- C. null
- D. A fatal error

??? success "Answer Q37"
    **A**

    clone performs a shallow copy; object-typed properties remain shared until __clone() deep-copies them.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.cloning.php)

**Q38.** For a mapped CollectionType to call the parent's adder/remover methods, set…  <small>_(Forms)_</small>

- A. by_reference => false
- B. allow_add => false
- C. prototype => false
- D. mapped => false

??? success "Answer Q38"
    **A**

    by_reference => false forces the form to call add/remove methods instead of mutating the returned collection in place, keeping associations in sync.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/collection.html)

**Q39.** The modern way to silence a single test's expected deprecations is…  <small>_(Testing)_</small>

- A. The #[IgnoreDeprecations] attribute
- B. The @group legacy docblock
- C. Calling error_reporting(0)
- D. Setting SYMFONY_DEPRECATIONS_HELPER=disabled globally

??? success "Answer Q39"
    **A**

    Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations replaces the old @group legacy for excluding a test's deprecations from the report.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

**Q40.** What does security: false on a firewall do?  <small>_(Security)_</small>

- A. Disables the security layer for that zone (and still counts as the match)
- B. Denies all access to that zone
- C. Enables anonymous voting
- D. Makes the firewall stateless

??? success "Answer Q40"
    **A**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

**Q41.** In which direction does reverseTransform() run?  <small>_(Forms)_</small>

- A. View to model (on submission)
- B. Model to view (on display)
- C. Norm to view only
- D. It never runs for view transformers

??? success "Answer Q41"
    **A**

    transform() converts toward the view (display); reverseTransform() converts toward the model (submission). Reversing these is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

**Q42.** Does the MIT license grant rights to use the Symfony name and logo?  <small>_(Architecture)_</small>

- A. No — those are governed by the separate trademark policy
- B. Yes — the license covers name and logo
- C. Only for non-commercial use

??? success "Answer Q42"
    **A**

    The code license (MIT) and the trademark (name/logo) are separate legal instruments. Using the Symfony name/logo follows Symfony SAS's trademark policy.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

**Q43.** What interface does Symfony's ServiceLocator implement?  <small>_(Dependency Injection)_</small>

- A. Psr\Container\ContainerInterface (PSR-11)
- B. Symfony's own ContainerInterface
- C. IteratorAggregate only
- D. CompilerPassInterface

??? success "Answer Q43"
    **A**

    ServiceLocator is a PSR-11 container exposing get() and has() over a fixed, compile-time set of services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

**Q44.** Which build tools are OUT of scope when only using asset()?  <small>_(Twig)_</small>

- A. AssetMapper and Webpack Encore
- B. The Routing component
- C. The Translation component
- D. The Twig EscaperExtension

??? success "Answer Q44"
    **A**

    asset() only resolves the final public path/version. Bundling and hashing are done by AssetMapper or Webpack Encore, which are not covered here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/asset.html)

**Q45.** How is #[Assert\...] attribute metadata turned into constraints at runtime?  <small>_(Validation)_</small>

- A. AttributeLoader builds ClassMetadata once, cached in a PSR-6 pool
- B. It is re-parsed by reflection on every validate() call
- C. It is compiled into the DI container and never changes
- D. It is read from a database mapping table

??? success "Answer Q45"
    **A**

    LazyLoadingMetadataFactory uses AttributeLoader to reflect over the class and build ClassMetadata, which is cached (validator.mapping.cache) so the reflection cost is paid once per class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q46.** Where do bridges live in the Symfony monorepo?  <small>_(Architecture)_</small>

- A. src/Symfony/Bridge/
- B. src/Symfony/Component/
- C. src/Symfony/Bundle/

??? success "Answer Q46"
    **A**

    Bridges have their own top-level directory, distinct from Component and Bundle.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony)

**Q47.** Which type should you type-hint to autowire an HTTP client? (choose one)  <small>_(HTTP)_</small>

- A. Symfony\Contracts\HttpClient\HttpClientInterface
- B. Symfony\Component\HttpClient\CurlHttpClient
- C. Symfony\Component\HttpClient\NativeHttpClient
- D. Symfony\Component\HttpClient\Psr18Client

??? success "Answer Q47"
    **A**

    Depend on the HttpClientInterface contract; the framework selects the concrete transport (curl or native).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_client.html)

**Q48.** Two routes can match the same request path. Which one wins?  <small>_(Routing)_</small>

- A. The first one declared in the RouteCollection
- B. The one with the most specific path
- C. The last one declared
- D. The one with the shortest name

??? success "Answer Q48"
    **A**

    The matcher iterates the collection in declaration order and returns the first route whose host and path match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q49.** A POST to /blog when the route is defined as /blog/ yields?  <small>_(Routing)_</small>

- A. 405 Method Not Allowed
- B. 301 redirect
- C. 200 OK
- D. 308 redirect

??? success "Answer Q49"
    **A**

    Redirecting a POST would alter the method, so the matcher returns 405 rather than a trailing-slash redirect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-urls-with-trailing-slashes)

**Q50.** A message is routed to an async transport. During dispatch() in the web process, the handler…  <small>_(Miscellaneous)_</small>

- A. does not run — SendMessageMiddleware serializes and sends it, stopping the bus
- B. runs immediately and is also queued
- C. runs only if a worker is currently active
- D. throws NoHandlerForMessageException

??? success "Answer Q50"
    **A**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages)

**Q51.** Why are Symfony services private by default?  <small>_(Dependency Injection)_</small>

- A. So the compiler can inline/remove them and to enforce proper dependency injection
- B. Because public services are deprecated in Symfony 8
- C. To make them read-only value objects
- D. So that get() runs faster at runtime

??? success "Answer Q51"
    **A**

    Private services can be inlined into their single consumer and pruned when unreferenced, shrinking the compiled container, and it discourages the service-locator anti-pattern of pulling from the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q52.** #[Groups(['read'])] on a property takes effect when…  <small>_(Miscellaneous)_</small>

- A. the context includes ['groups' => ['read']]
- B. always, regardless of context
- C. only during deserialization
- D. the property is public

??? success "Answer Q52"
    **A**

    Group filtering only applies when matching groups are passed in the context; otherwise the group attribute has no effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

**Q53.** What does Process::run() return?  <small>_(Miscellaneous)_</small>

- A. The integer exit code
- B. The stdout as a string
- C. void
- D. A boolean success flag

??? success "Answer Q53"
    **A**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

**Q54.** Under which license is Symfony released?  <small>_(Architecture)_</small>

- A. MIT
- B. GPLv3
- C. Apache 2.0

??? success "Answer Q54"
    **A**

    Symfony components are released under the permissive, non-copyleft MIT license.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/LICENSE)

**Q55.** Where should field-adding logic live in a form type?  <small>_(Forms)_</small>

- A. In buildForm(), using the FormBuilderInterface
- B. In configureOptions(), returning an array of fields
- C. In the constructor
- D. In buildView()

??? success "Answer Q55"
    **A**

    buildForm() receives the builder and is where ->add() calls belong. configureOptions() only declares options via OptionsResolver.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

**Q56.** Which question class offers a fixed list of selectable answers?  <small>_(Console)_</small>

- A. ChoiceQuestion
- B. Question
- C. ConfirmationQuestion
- D. HiddenQuestion

??? success "Answer Q56"
    **A**

    ChoiceQuestion presents options and supports single or multi-select.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/console/helpers/questionhelper.html)

**Q57.** What does ValidatorInterface::validate() return when the value is invalid?  <small>_(Validation)_</small>

- A. A ConstraintViolationListInterface containing the violations
- B. false
- C. It throws a ValidationFailedException
- D. An array of error message strings

??? success "Answer Q57"
    **A**

    validate() always returns a ConstraintViolationListInterface. It never returns a bool and never throws on failure; you inspect the result with count() and by iterating it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q58.** Which command prints a bundle's configuration reference tree?  <small>_(Dependency Injection)_</small>

- A. config:dump-reference
- B. debug:container
- C. debug:autowiring
- D. debug:router

??? success "Answer Q58"
    **A**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

**Q59.** Symfony\Contracts\Cache\CacheInterface::get() runs its callback…  <small>_(Miscellaneous)_</small>

- A. only on a cache miss, then stores and returns the value
- B. on every call
- C. never — you must call save() yourself
- D. only when the beta factor is INF

??? success "Answer Q59"
    **A**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q60.** How are WebTestCase and KernelTestCase related?  <small>_(Testing)_</small>

- A. WebTestCase extends KernelTestCase, adding the HTTP client (createClient())
- B. KernelTestCase extends WebTestCase
- C. They are unrelated base classes
- D. Both extend BrowserTestCase

??? success "Answer Q60"
    **A**

    WebTestCase adds the KernelBrowser client on top of the kernel-booting KernelTestCase. Use KernelTestCase when you need only the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#application-tests)

**Q61.** Where does #{...} string interpolation work in Twig?  <small>_(Twig)_</small>

- A. Only inside double-quoted strings
- B. Inside any string literal
- C. Only inside single-quoted strings
- D. Only inside {% %} tags

??? success "Answer Q61"
    **A**

    The lexer only interpolates #{...} within double-quoted strings; single quotes render the text literally.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)

**Q62.** Which password algorithm is the recommended default?  <small>_(Security)_</small>

- A. auto
- B. plaintext
- C. md5
- D. pbkdf2

??? success "Answer Q62"
    **A**

    'auto' selects the best available algorithm (currently bcrypt) and can adapt over time; it also enables automatic rehash on cost changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

**Q63.** Under the unanimous strategy, one voter denies while another grants. Outcome?  <small>_(Security)_</small>

- A. Access is denied — unanimous grants only if no voter denies
- B. Access is granted — one grant is enough
- C. The tie is resolved by roles
- D. An exception is thrown

??? success "Answer Q63"
    **A**

    unanimous requires that no voter denies. A single ACCESS_DENIED blocks access regardless of grants (unlike affirmative).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

**Q64.** How do you emit a must-revalidate directive from a Response object?  <small>_(HTTP Caching)_</small>

- A. $response->setCache(['must_revalidate' => true])
- B. $response->setMustRevalidate()
- C. $response->mustRevalidate(true)
- D. It is added automatically by no-cache

??? success "Answer Q64"
    **A**

    There is no dedicated setter; Response::mustRevalidate() is a getter returning bool. Use setCache(['must_revalidate' => true]) or #[Cache(mustRevalidate: true)].

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q65.** In which months do Symfony minor releases ship?  <small>_(Architecture)_</small>

- A. May and November
- B. January and July
- C. March and September

??? success "Answer Q65"
    **A**

    The cadence is fixed: a new minor every May and every November.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q66.** Can symfony/routing be used without FrameworkBundle?  <small>_(Architecture)_</small>

- A. Yes — it is a standalone component
- B. No — it requires the kernel
- C. Only in the dev environment

??? success "Answer Q66"
    **A**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

**Q67.** How does AbstractController obtain its helper services?  <small>_(Controllers)_</small>

- A. Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()
- B. Through constructor injection of each service
- C. The full application container is injected

??? success "Answer Q67"
    **A**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q68.** Which redirect status codes preserve the original HTTP method and body?  <small>_(Controllers)_</small>

- A. 307 and 308
- B. 301 and 302
- C. 302 and 303

??? success "Answer Q68"
    **A**

    307/308 must not change the request method; 303 always forces GET and 301/302 may downgrade to GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q69.** Which passport type suits a valid-API-token flow with no password to verify?  <small>_(Security)_</small>

- A. SelfValidatingPassport with a UserBadge
- B. Passport with an empty PasswordCredentials
- C. PreAuthenticatedToken
- D. UsernamePasswordToken

??? success "Answer Q69"
    **A**

    When the credential itself proves identity, use SelfValidatingPassport, which carries only a UserBadge — there is nothing further to check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html#the-passport)

**Q70.** When is kernel.terminate dispatched?  <small>_(Architecture)_</small>

- A. After the response has been sent to the client, for the main request
- B. Before kernel.response
- C. Once for every sub-request

??? success "Answer Q70"
    **A**

    terminate() runs after send() and is not called for sub-requests; it is ideal for slow post-response work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-terminate)

**Q71.** What is the dispatch() signature in Symfony 8 (PSR-14)?  <small>_(Architecture)_</small>

- A. dispatch(object $event, ?string $eventName = null)
- B. dispatch(string $eventName, Event $event)
- C. dispatch(Event $event, string $eventName) with a required name

??? success "Answer Q71"
    **A**

    Symfony follows PSR-14: the event object comes first, the name is optional (defaults to the event's class name).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q72.** What may a MINOR release NOT do?  <small>_(Architecture)_</small>

- A. Break backward compatibility
- B. Add new features
- C. Introduce deprecations

??? success "Answer Q72"
    **A**

    Minors add features and deprecations but never break BC; breaks are reserved for major releases.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q73.** Which SPL structure maps data keyed by an object instance?  <small>_(PHP & Web Security)_</small>

- A. SplObjectStorage
- B. SplStack
- C. SplFixedArray
- D. SplQueue

??? success "Answer Q73"
    **A**

    SplObjectStorage keys by object identity and can attach arbitrary data per object.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/class.splobjectstorage.php)

**Q74.** Which two methods do you typically override in an AbstractType?  <small>_(Forms)_</small>

- A. buildForm(FormBuilderInterface, array) and configureOptions(OptionsResolver)
- B. build() and getOptions()
- C. getName() and buildView()
- D. configureFields() and setDefaults()

??? success "Answer Q74"
    **A**

    buildForm() adds fields to the builder; configureOptions() declares the type's options via OptionsResolver. getName() was removed; buildView() exists but is not the primary pair.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

**Q75.** Why call refresh() during a long critical section?  <small>_(Miscellaneous)_</small>

- A. To extend the lock's TTL so it is not considered expired mid-job
- B. To release then reacquire the lock
- C. To switch to a different store
- D. To convert it to a shared lock

??? success "Answer Q75"
    **A**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
