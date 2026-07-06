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

**Q1.** What is the default Process timeout?  <small>_(Miscellaneous)_</small>

- A. 60 seconds
- B. Unlimited
- C. 30 seconds
- D. 300 seconds

??? success "Answer Q1"
    **A**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#process-timeout)

**Q2.** After `$b = clone $a;` where `$a->list` is an object, what is `$b->list`?  <small>_(PHP & Web Security)_</small>

- A. The same object as $a->list unless __clone() copies it
- B. Always an independent deep copy
- C. null
- D. A fatal error

??? success "Answer Q2"
    **A**

    clone performs a shallow copy; object-typed properties remain shared until __clone() deep-copies them.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.cloning.php)

**Q3.** Under the unanimous strategy, one voter denies while another grants. Outcome?  <small>_(Security)_</small>

- A. Access is denied — unanimous grants only if no voter denies
- B. Access is granted — one grant is enough
- C. The tie is resolved by roles
- D. An exception is thrown

??? success "Answer Q3"
    **A**

    unanimous requires that no voter denies. A single ACCESS_DENIED blocks access regardless of grants (unlike affirmative).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

**Q4.** What does ServiceSubscriberInterface::getSubscribedServices() declare?  <small>_(Dependency Injection)_</small>

- A. The set of services the subscriber may lazily use, injected as a locator
- B. Instantiated services returned eagerly
- C. The compiler passes to register
- D. The whole container

??? success "Answer Q4"
    **A**

    It declares a whitelist; the container injects a matching ServiceLocator so services are built only when requested.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q5.** Which method keeps a service replaced via getContainer()->set() alive across multiple requests?  <small>_(Testing)_</small>

- A. $client->disableReboot()
- B. $client->followRedirects()
- C. $client->insulate()
- D. $client->restart()

??? success "Answer Q5"
    **A**

    By default the kernel reboots after each request, discarding replacements. disableReboot() preserves the container between requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q6.** How do you read the value of an unmapped FileType field?  <small>_(Forms)_</small>

- A. $form->get('field')->getData()
- B. From the bound model object
- C. $request->request->get('field')
- D. $form->getViewData()

??? success "Answer Q6"
    **A**

    mapped => false excludes the field from the data mapper, so it is not written to the model; you fetch it directly from the child form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

**Q7.** Which two methods do you typically override in an AbstractType?  <small>_(Forms)_</small>

- A. buildForm(FormBuilderInterface, array) and configureOptions(OptionsResolver)
- B. build() and getOptions()
- C. getName() and buildView()
- D. configureFields() and setDefaults()

??? success "Answer Q7"
    **A**

    buildForm() adds fields to the builder; configureOptions() declares the type's options via OptionsResolver. getName() was removed; buildView() exists but is not the primary pair.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

**Q8.** Two services implement one interface with no default alias. Autowiring by that interface...  <small>_(Dependency Injection)_</small>

- A. Throws an ambiguity error at compile time
- B. Silently picks the first candidate
- C. Injects null
- D. Picks the last candidate

??? success "Answer Q8"
    **A**

    Ambiguity is a hard build error; you disambiguate with a named alias, #[Target], #[Autowire(service:)] or bind.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

**Q9.** How is a command normally registered in the service container?  <small>_(Console)_</small>

- A. Autoconfiguration tags #[AsCommand]/Command subclasses with 'console.command'
- B. You always add the 'console.command' tag manually
- C. You call Application::add() inside bin/console
- D. It is discovered purely by filename

??? success "Answer Q9"
    **A**

    Autoconfiguration applies the console.command tag; a compiler pass builds a ContainerCommandLoader mapping name to service id for lazy loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/commands_as_services.html)

**Q10.** In which parameter bag do matched route parameters appear?  <small>_(Controllers)_</small>

- A. $request->attributes
- B. $request->query
- C. $request->request

??? success "Answer Q10"
    **A**

    The router writes matched parameters into the attributes bag; query is GET data and request is the POST body.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q11.** LockInterface::acquire() called with no argument is…  <small>_(Miscellaneous)_</small>

- A. non-blocking — it returns false immediately if the lock is held
- B. blocking — it waits until the lock is free
- C. throwing an exception if the lock is held
- D. always successful

??? success "Answer Q11"
    **A**

    acquire() defaults to non-blocking; pass true to block until the resource becomes available (store permitting).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html#blocking-locks)

**Q12.** What is the primary benefit of ESI over full-page caching?  <small>_(HTTP Caching)_</small>

- A. Each fragment can be cached with its own independent lifetime
- B. It encrypts fragments end to end
- C. It removes the need for any reverse proxy
- D. It compresses the HTML automatically

??? success "Answer Q12"
    **A**

    ESI caches fragments as separate entries, so a long-lived shell can coexist with short-lived or per-user fragments on one page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q13.** When is %env(DATABASE_URL)% resolved?  <small>_(Dependency Injection)_</small>

- A. At runtime, via an env-var processor
- B. At compilation, frozen into the cache
- C. When .env is parsed at deploy time only
- D. Never; it is a literal string

??? success "Answer Q13"
    **A**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

**Q14.** In which months do Symfony minor releases ship?  <small>_(Architecture)_</small>

- A. May and November
- B. January and July
- C. March and September

??? success "Answer Q14"
    **A**

    The cadence is fixed: a new minor every May and every November.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q15.** Which environment variable selects the runtime class?  <small>_(Miscellaneous)_</small>

- A. APP_RUNTIME
- B. APP_ENV
- C. SYMFONY_RUNTIME
- D. RUNTIME_CLASS

??? success "Answer Q15"
    **A**

    APP_RUNTIME (or composer.json extra.runtime.class) chooses the RuntimeInterface implementation; the default is SymfonyRuntime, which extends GenericRuntime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

**Q16.** When is kernel.terminate dispatched?  <small>_(Architecture)_</small>

- A. After the response has been sent to the client, for the main request
- B. Before kernel.response
- C. Once for every sub-request

??? success "Answer Q16"
    **A**

    terminate() runs after send() and is not called for sub-requests; it is ideal for slow post-response work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-terminate)

**Q17.** Where do bridges live in the Symfony monorepo?  <small>_(Architecture)_</small>

- A. src/Symfony/Bridge/
- B. src/Symfony/Component/
- C. src/Symfony/Bundle/

??? success "Answer Q17"
    **A**

    Bridges have their own top-level directory, distinct from Component and Bundle.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony)

**Q18.** How does AbstractController obtain its helper services?  <small>_(Controllers)_</small>

- A. Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()
- B. Through constructor injection of each service
- C. The full application container is injected

??? success "Answer Q18"
    **A**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q19.** In a RedirectController route config, permanent: true means which status code?  <small>_(Routing)_</small>

- A. 301 Moved Permanently
- B. 302 Found
- C. 307 Temporary Redirect
- D. 308 Permanent Redirect

??? success "Answer Q19"
    **A**

    permanent toggles a 301; the default is a 302.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q20.** Which command prints a bundle's configuration reference tree?  <small>_(Dependency Injection)_</small>

- A. config:dump-reference
- B. debug:container
- C. debug:autowiring
- D. debug:router

??? success "Answer Q20"
    **A**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

**Q21.** Where should field-adding logic live in a form type?  <small>_(Forms)_</small>

- A. In buildForm(), using the FormBuilderInterface
- B. In configureOptions(), returning an array of fields
- C. In the constructor
- D. In buildView()

??? success "Answer Q21"
    **A**

    buildForm() receives the builder and is where ->add() calls belong. configureOptions() only declares options via OptionsResolver.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/forms.html)

**Q22.** When overriding getSubscribedServices() to add a service, what must you do to keep the built-in helpers?  <small>_(Controllers)_</small>

- A. Spread parent::getSubscribedServices() into the returned array
- B. Nothing; helpers are always available
- C. Re-declare every core service manually

??? success "Answer Q22"
    **A**

    Returning only your service replaces the list; merge the parent's subscriptions so render/getUser/etc. still resolve.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#the-base-controller-class-services)

**Q23.** Two providers are defined and a firewall omits the provider key. Result?  <small>_(Security)_</small>

- A. Configuration error — the provider is ambiguous
- B. It silently uses the first provider
- C. It merges both providers
- D. The firewall becomes anonymous

??? success "Answer Q23"
    **A**

    With multiple providers there is no implicit default; each firewall must name its provider explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/user_providers.html)

**Q24.** ExpressionLanguage::compile() returns what?  <small>_(Miscellaneous)_</small>

- A. A string of PHP source code
- B. The evaluated result value
- C. An AST node object
- D. A boolean success flag

??? success "Answer Q24"
    **A**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q25.** Which class renders Twig templates into an email body?  <small>_(Miscellaneous)_</small>

- A. Symfony\Bridge\Twig\Mime\TemplatedEmail
- B. Symfony\Component\Mime\Email
- C. Symfony\Component\Mailer\Mailer
- D. Symfony\Component\Mime\Message

??? success "Answer Q25"
    **A**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

**Q26.** Which two declarations are exactly equivalent?  <small>_(Routing)_</small>

- A. {id<\d+>} and requirements: {id: '\d+'}
- B. {id} and requirements: {id: '\d+'}
- C. {id<\d+>} and defaults: {id: '\d+'}
- D. {id} and {id<.+>}

??? success "Answer Q26"
    **A**

    The inline <...> syntax is sugar for a matching entry in the requirements array.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#parameters-validation)

**Q27.** Which service selects the fragment renderer for render()/render_esi()?  <small>_(Twig)_</small>

- A. Symfony\Component\HttpKernel\Fragment\FragmentHandler
- B. Symfony\Component\Routing\Generator\UrlGenerator
- C. Twig\Extension\EscaperExtension
- D. Symfony\Bridge\Twig\AppVariable

??? success "Answer Q27"
    **A**

    HttpKernelExtension delegates to FragmentHandler, which picks a FragmentRendererInterface (inline, esi, hinclude) by strategy name.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

**Q28.** Which InputArgument mode value is OPTIONAL?  <small>_(Console)_</small>

- A. 2
- B. 1
- C. 4
- D. 8

??? success "Answer Q28"
    **A**

    Argument modes are REQUIRED=1, OPTIONAL=2, IS_ARRAY=4.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/input.html)

**Q29.** Under which license is Symfony released?  <small>_(Architecture)_</small>

- A. MIT
- B. GPLv3
- C. Apache 2.0

??? success "Answer Q29"
    **A**

    Symfony components are released under the permissive, non-copyleft MIT license.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/LICENSE)

**Q30.** A controller throws a plain \RuntimeException. What status code results?  <small>_(Controllers)_</small>

- A. 500
- B. 400
- C. 404

??? success "Answer Q30"
    **A**

    Only exceptions implementing HttpExceptionInterface set a specific status; any other exception becomes a 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q31.** Which set contains only idempotent methods? (choose one)  <small>_(HTTP)_</small>

- A. GET, PUT, DELETE
- B. GET, POST, PUT
- C. POST, PATCH, DELETE
- D. POST, PUT, PATCH

??? success "Answer Q31"
    **A**

    GET, PUT and DELETE are idempotent (repeating yields the same state); POST and PATCH are not.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)

**Q32.** generateUrl('blog', ['page' => 1]) where page defaults to 1 produces?  <small>_(Routing)_</small>

- A. /blog
- B. /blog/1
- C. /blog?page=1
- D. an exception

??? success "Answer Q32"
    **A**

    The generator omits a trailing segment whose value equals its default, yielding the canonical shortest URL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

**Q33.** Which built-in authenticator uses a token_handler returning a UserBadge?  <small>_(Security)_</small>

- A. access_token
- B. form_login
- C. http_basic
- D. remember_me

??? success "Answer Q33"
    **A**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/access_token.html)

**Q34.** RedirectController configured with permanent: true returns which status?  <small>_(Controllers)_</small>

- A. 301 (or 308 when keepRequestMethod is true)
- B. 302
- C. 410

??? success "Answer Q34"
    **A**

    permanent selects the permanent status code; combined with keepRequestMethod it becomes 308 to preserve the method.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-to-urls-and-routes-directly-from-a-route)

**Q35.** The user is authenticated but lacks permission for a resource. Which status? (choose one)  <small>_(HTTP)_</small>

- A. 403 Forbidden
- B. 401 Unauthorized
- C. 400 Bad Request
- D. 422 Unprocessable Content

??? success "Answer Q35"
    **A**

    401 means unauthenticated (send WWW-Authenticate); 403 means authenticated but not authorized — re-authenticating will not help.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

**Q36.** Which check can pass a subject to voters?  <small>_(Security)_</small>

- A. isGranted('EDIT', $post)
- B. An access_control rule
- C. role_hierarchy configuration
- D. The firewall pattern

??? success "Answer Q36"
    **A**

    Only the isGranted()/#[IsGranted]/denyAccessUnlessGranted() path carries a subject. access_control is URL-based and cannot pass a subject.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/voters.html)

**Q37.** What is the correct command lifecycle order?  <small>_(Console)_</small>

- A. configure → initialize → interact → execute
- B. initialize → configure → execute → interact
- C. configure → interact → initialize → execute
- D. execute → configure → initialize → interact

??? success "Answer Q37"
    **A**

    configure() runs in the constructor; then run() calls initialize(), interact() (if interactive), input validation, and finally execute().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

**Q38.** Which component decides whether a request is served over HTTP/2? (choose one)  <small>_(HTTP)_</small>

- A. The web server / reverse proxy via ALPN negotiation
- B. The Symfony Request object
- C. public/index.php
- D. The PHP engine

??? success "Answer Q38"
    **A**

    Protocol negotiation happens at the TLS/web-server layer (ALPN). PHP only observes the negotiated version via $request->getProtocolVersion().

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

**Q39.** Inside a parent factory method, how do `new static()` and `new self()` differ?  <small>_(PHP & Web Security)_</small>

- A. static respects the called subclass (late static binding); self is fixed to the defining class
- B. They are identical
- C. self respects the subclass
- D. Both resolve only at compile time

??? success "Answer Q39"
    **A**

    Late static binding makes static:: resolve to the runtime class, so new static() returns a subclass instance where new self() would not.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

**Q40.** In a decorator definition, what does @.inner reference?  <small>_(Dependency Injection)_</small>

- A. The original (decorated) service, renamed by the compiler
- B. The decorator service itself
- C. The parent bundle service
- D. A private alias of the container

??? success "Answer Q40"
    **A**

    DecoratorServicePass renames the decorated service and exposes it as .inner so the decorator can delegate to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q41.** Which password algorithm is the recommended default?  <small>_(Security)_</small>

- A. auto
- B. plaintext
- C. md5
- D. pbkdf2

??? success "Answer Q41"
    **A**

    'auto' selects the best available algorithm (currently bcrypt) and can adapt over time; it also enables automatic rehash on cost changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/passwords.html)

**Q42.** Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?  <small>_(Miscellaneous)_</small>

- A. --limit (max messages) and --time-limit (max seconds), optionally with memory limits
- B. --kill and --restart
- C. --stop-now only
- D. --reload after each message

??? success "Answer Q42"
    **A**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

**Q43.** What does ValidatorInterface::validate() return when the value is invalid?  <small>_(Validation)_</small>

- A. A ConstraintViolationListInterface containing the violations
- B. false
- C. It throws a ValidationFailedException
- D. An array of error message strings

??? success "Answer Q43"
    **A**

    validate() always returns a ConstraintViolationListInterface. It never returns a bool and never throws on failure; you inspect the result with count() and by iterating it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q44.** You put #[Assert\Valid] on a property holding a Collection/array of Address objects. What happens on validate()?  <small>_(Validation)_</small>

- A. Each element is traversed and its own constraints are validated (cascade)
- B. Only the first element is validated
- C. The collection count is validated but not the elements
- D. Nothing — Valid works only on single objects

??? success "Answer Q44"
    **A**

    Assert\Valid cascades into nested objects, and for a traversable/array it validates every element's constraints. Without it, nested objects are not validated at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Valid.html)

**Q45.** Can symfony/routing be used without FrameworkBundle?  <small>_(Architecture)_</small>

- A. Yes — it is a standalone component
- B. No — it requires the kernel
- C. Only in the dev environment

??? success "Answer Q45"
    **A**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

**Q46.** Which feature can an abstract class have that an interface cannot?  <small>_(PHP & Web Security)_</small>

- A. Properties and a constructor
- B. Multiple parents
- C. Public method signatures
- D. Constants

??? success "Answer Q46"
    **A**

    Abstract classes can hold state and a constructor; interfaces are pure contracts (constants only).

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.oop5.interfaces.php)

**Q47.** Which Twig delimiter executes a statement without printing anything?  <small>_(Twig)_</small>

- A. {% ... %}
- B. {{ ... }}
- C. {# ... #}
- D. #{ ... }

??? success "Answer Q47"
    **A**

    {% %} runs tags/control flow, {{ }} prints an (escaped) expression, and {# #} is a comment that is stripped at compile time.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

**Q48.** For a PATCH submission, handleRequest passes which clearMissing value?  <small>_(Forms)_</small>

- A. false, enabling partial updates (absent fields keep their value)
- B. true, clearing all absent fields
- C. It is undefined for PATCH
- D. It depends on data_class

??? success "Answer Q48"
    **A**

    handleRequest passes clearMissing: false for PATCH so fields missing from the payload retain their current value, enabling partial updates.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

**Q49.** What does `composer dump-env prod` produce, and what is the effect?  <small>_(Miscellaneous)_</small>

- A. .env.local.php — Symfony loads it directly and skips parsing .env* files
- B. .env.prod — parsed on every request
- C. config/prod.php overriding all bundles
- D. Nothing; it only validates env vars

??? success "Answer Q49"
    **A**

    The whole .env* cascade is compiled to a plain PHP array in .env.local.php, which Symfony loads directly, avoiding DotEnv parsing on each request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production)

**Q50.** Which passport type suits a valid-API-token flow with no password to verify?  <small>_(Security)_</small>

- A. SelfValidatingPassport with a UserBadge
- B. Passport with an empty PasswordCredentials
- C. PreAuthenticatedToken
- D. UsernamePasswordToken

??? success "Answer Q50"
    **A**

    When the credential itself proves identity, use SelfValidatingPassport, which carries only a UserBadge — there is nothing further to check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html#the-passport)

**Q51.** What may a MINOR release NOT do?  <small>_(Architecture)_</small>

- A. Break backward compatibility
- B. Add new features
- C. Introduce deprecations

??? success "Answer Q51"
    **A**

    Minors add features and deprecations but never break BC; breaks are reserved for major releases.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q52.** After a successful method override, what does getRealMethod() return for a POST+_method=PUT request? (choose one)  <small>_(HTTP)_</small>

- A. POST
- B. PUT
- C. GET
- D. An empty string

??? success "Answer Q52"
    **A**

    getMethod() returns the overridden verb (PUT) while getRealMethod() returns the raw transport method (POST).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q53.** Symfony\Contracts\Cache\CacheInterface::get() runs its callback…  <small>_(Miscellaneous)_</small>

- A. only on a cache miss, then stores and returns the value
- B. on every call
- C. never — you must call save() yourself
- D. only when the beta factor is INF

??? success "Answer Q53"
    **A**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q54.** How should a service (not a controller) access the current Request?  <small>_(Controllers)_</small>

- A. Inject RequestStack and call getCurrentRequest()
- B. Autowire Request in the constructor
- C. Call Request::createFromGlobals()

??? success "Answer Q54"
    **A**

    The Request is request-scoped and cannot be injected directly; inject the RequestStack service instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

**Q55.** What does security: false on a firewall do?  <small>_(Security)_</small>

- A. Disables the security layer for that zone (and still counts as the match)
- B. Denies all access to that zone
- C. Enables anonymous voting
- D. Makes the firewall stateless

??? success "Answer Q55"
    **A**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

**Q56.** In an Accept header, what does q=0 mean for an option? (choose one)  <small>_(HTTP)_</small>

- A. Not acceptable (rejected)
- B. Highest priority
- C. The default weight
- D. A wildcard match

??? success "Answer Q56"
    **A**

    A quality value of 0 explicitly marks that media type or language as unacceptable.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Quality_values)

**Q57.** For class App\Entity\User with no group sequence, what is the {ClassName} group?  <small>_(Validation)_</small>

- A. 'User' (the short class name), equivalent to 'Default' here
- B. 'App\Entity\User' (the FQCN)
- C. 'app_entity_user'
- D. There is no such group

??? success "Answer Q57"
    **A**

    The {ClassName} group uses the short class name. Every Default-group constraint is also in it, so with no sequence 'User' and 'Default' are equivalent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/groups.html)

**Q58.** How do you register a static global string in Twig?  <small>_(Twig)_</small>

- A. Under twig.globals in config, or via a GlobalsInterface extension
- B. With a #[AsGlobal] attribute
- C. With {% global x = 'y' %}
- D. It cannot be done

??? success "Answer Q58"
    **A**

    Declare globals under twig.globals in twig.yaml, or return them from an extension implementing Twig\Extension\GlobalsInterface::getGlobals().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#global-variables)

**Q59.** Which request attribute holds the name of the matched route?  <small>_(Routing)_</small>

- A. _route
- B. _controller
- C. _route_name
- D. _name

??? success "Answer Q59"
    **A**

    The matcher injects _route (the matched name) and _route_params (the placeholder values) into the request attributes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#special-parameters)

**Q60.** Which files hold the compiled router in the cache directory?  <small>_(Routing)_</small>

- A. url_matching_routes.php and url_generating_routes.php
- B. routes.php and router.php
- C. matcher.php and generator.php
- D. RouteCollection.php

??? success "Answer Q60"
    **A**

    The CompiledUrlMatcherDumper and CompiledUrlGeneratorDumper write these two files that the Router loads at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q61.** What does a form type's getParent() return?  <small>_(Forms)_</small>

- A. The parent type's fully-qualified class name (a string)
- B. A FormBuilderInterface instance
- C. A ResolvedFormType instance
- D. null for all custom types

??? success "Answer Q61"
    **A**

    getParent() returns a class string (default FormType::class). The registry resolves it into the parent chain of a ResolvedFormType.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/create_custom_field_type.html)

**Q62.** What interface does Symfony's ServiceLocator implement?  <small>_(Dependency Injection)_</small>

- A. Psr\Container\ContainerInterface (PSR-11)
- B. Symfony's own ContainerInterface
- C. IteratorAggregate only
- D. CompilerPassInterface

??? success "Answer Q62"
    **A**

    ServiceLocator is a PSR-11 container exposing get() and has() over a fixed, compile-time set of services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

**Q63.** Does the MIT license grant rights to use the Symfony name and logo?  <small>_(Architecture)_</small>

- A. No — those are governed by the separate trademark policy
- B. Yes — the license covers name and logo
- C. Only for non-commercial use

??? success "Answer Q63"
    **A**

    The code license (MIT) and the trademark (name/logo) are separate legal instruments. Using the Symfony name/logo follows Symfony SAS's trademark policy.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

**Q64.** How many access_control rules apply to a request?  <small>_(Security)_</small>

- A. Only the first matching rule
- B. All rules that match
- C. The most specific match
- D. The last matching rule

??? success "Answer Q64"
    **A**

    AccessMap returns the first match and evaluation stops. Order rules from specific to general.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#securing-url-patterns-access-control)

**Q65.** A method referenced by #[DataProvider('provide')] must be…  <small>_(Testing)_</small>

- A. public static and return an array or other iterable of argument sets
- B. private and return void
- C. a protected instance method returning a Generator only
- D. annotated with #[Test] as well

??? success "Answer Q65"
    **A**

    PHPUnit\Framework\Attributes\DataProvider names a public static method returning an iterable (array or Generator) of argument arrays; each set becomes one parameterised run of the test.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

**Q66.** How do you strip whitespace between HTML tags in current Twig 3.x?  <small>_(Twig)_</small>

- A. {% apply spaceless %}...{% endapply %}
- B. {% spaceless %}...{% endspaceless %}
- C. {{ strip }}
- D. {% trim %}...{% endtrim %}

??? success "Answer Q66"
    **A**

    The {% spaceless %} tag was removed in Twig 3; use the spaceless filter via {% apply spaceless %} (or the {{- -}} whitespace modifiers).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/spaceless.html)

**Q67.** What is written to var/cache/prod/ after compilation?  <small>_(Dependency Injection)_</small>

- A. A dumped, optimised PHP container class produced by PhpDumper
- B. The ContainerBuilder instance serialized
- C. The raw YAML service definitions
- D. Serialized service instances

??? success "Answer Q67"
    **A**

    PhpDumper writes a compiled PHP class with a method per service; the runtime uses it directly, never the ContainerBuilder.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection/compilation.html)

**Q68.** Which of these is NOT a member of the `app` global?  <small>_(Twig)_</small>

- A. app.controller
- B. app.request
- C. app.environment
- D. app.flashes

??? success "Answer Q68"
    **A**

    app exposes user, request, session, flashes, environment, debug, token, locale, current_route and current_route_parameters. There is no app.controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

**Q69.** Which method returns the message with its {{ placeholders }} still unresolved?  <small>_(Validation)_</small>

- A. getMessageTemplate()
- B. getMessage()
- C. getParameters()
- D. getCode()

??? success "Answer Q69"
    **A**

    getMessage() returns the interpolated message; getMessageTemplate() keeps the raw template with {{ x }} placeholders, and getParameters() holds the substitution map.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q70.** DelayStamp(5000) delays delivery by how long?  <small>_(Miscellaneous)_</small>

- A. 5000 milliseconds (5 seconds)
- B. 5000 seconds
- C. 5000 microseconds
- D. 5000 minutes

??? success "Answer Q70"
    **A**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#delaying-messages)

**Q71.** What is the effect of $client->insulate()?  <small>_(Testing)_</small>

- A. Each request runs in a separate PHP subprocess, so in-process profiler/container access is lost
- B. Redirects are followed automatically
- C. The same kernel instance is reused forever
- D. Responses are cached between tests

??? success "Answer Q71"
    **A**

    Insulated requests run in a fresh subprocess to isolate global state, at the cost of losing in-process access to the profiler and container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/browser_kit.html)

**Q72.** What does $client->request('GET', '/') return?  <small>_(Testing)_</small>

- A. A Symfony\Component\DomCrawler\Crawler
- B. A Symfony\Component\HttpFoundation\Response
- C. A Symfony\Component\HttpFoundation\Request
- D. void

??? success "Answer Q72"
    **A**

    Navigation methods return a Crawler over the response DOM. Fetch the response object with $client->getResponse().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#making-requests)

**Q73.** Why are Symfony services private by default?  <small>_(Dependency Injection)_</small>

- A. So the compiler can inline/remove them and to enforce proper dependency injection
- B. Because public services are deprecated in Symfony 8
- C. To make them read-only value objects
- D. So that get() runs faster at runtime

??? success "Answer Q73"
    **A**

    Private services can be inlined into their single consumer and pruned when unreferenced, shrinking the compiled container, and it discourages the service-locator anti-pattern of pulling from the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q74.** What is the dispatch() signature in Symfony 8 (PSR-14)?  <small>_(Architecture)_</small>

- A. dispatch(object $event, ?string $eventName = null)
- B. dispatch(string $eventName, Event $event)
- C. dispatch(Event $event, string $eventName) with a required name

??? success "Answer Q74"
    **A**

    Symfony follows PSR-14: the event object comes first, the name is optional (defaults to the event's class name).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q75.** Under a transport's retry_strategy, what does the 'multiplier' option control?  <small>_(Miscellaneous)_</small>

- A. The factor by which the delay grows between successive retries (exponential backoff)
- B. The number of parallel workers spawned
- C. How many transports share the message
- D. The maximum number of messages fetched per poll

??? success "Answer Q75"
    **A**

    retry_strategy defines max_retries, delay (initial, ms), multiplier (delay is multiplied by this each attempt) and max_delay to cap it, producing exponential backoff before the failure transport is used.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
