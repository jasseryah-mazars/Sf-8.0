# Mock Exam C (Exam Mode)

!!! note "Three independent papers"
    This is **Mock C**. Also try: [Mock A](mock-exam.md) · [Mock B](mock-exam-b.md). Each draws a different random sample from the bank — sit them on separate days and log every miss.

!!! danger "Exam-mode rules"
    **75 questions · 90 minutes.** Set a timer. No notes, no docs. Answer every question (there is no negative marking). Multiple answers may be correct — the stem says how many. Reveal a key only after you have committed to an answer.

!!! tip "Timing"
    90 min / 75 Q ≈ **72 seconds per question.** Flag hard ones, keep moving, and come back. Aim to finish with 10 minutes to review flags.

??? info "How this exam was built"
    75 questions sampled from the practice bank, weighted to mirror exam emphasis (Architecture, DI, Security, Messenger heavier; HTTP Caching lighter). Regenerate a fresh set with `python tools/mock_exam.py`.

---

**Q1.** What does {{ dump() }} with no arguments do?  <small>_(Twig)_</small>

- A. Dumps all variables available in the current template context
- B. Dumps nothing
- C. Throws an exception
- D. Dumps only the app global

??? success "Answer Q1"
    **A**

    Called with no arguments, dump() outputs the entire render context (all passed variables plus globals).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

**Q2.** Where is a login password actually verified?  <small>_(Security)_</small>

- A. In CheckCredentialsListener on CheckPassportEvent
- B. In the user's getPassword() method
- C. In the user provider
- D. In the controller action

??? success "Answer Q2"
    **A**

    The authenticator adds a PasswordCredentials badge; the listener verifies it against the hash using the configured hasher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

**Q3.** ExpressionLanguage::compile() returns what?  <small>_(Miscellaneous)_</small>

- A. A string of PHP source code
- B. The evaluated result value
- C. An AST node object
- D. A boolean success flag

??? success "Answer Q3"
    **A**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q4.** Which event is responsible for turning an exception into a response?  <small>_(Architecture)_</small>

- A. kernel.exception
- B. kernel.view
- C. kernel.terminate

??? success "Answer Q4"
    **A**

    When an exception escapes handleRaw(), HttpKernel dispatches kernel.exception; listeners may set the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q5.** With Messenger routing configured for emails, MailerInterface::send() will…  <small>_(Miscellaneous)_</small>

- A. dispatch a SendEmailMessage to be delivered by a worker
- B. always send synchronously over SMTP
- C. throw if no worker is running
- D. render but not send the email

??? success "Answer Q5"
    **A**

    When SendEmailMessage is routed to a transport, send() enqueues it; a worker delivers it later, giving async sending plus retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

**Q6.** Which value resolver supplies a `Request` type-hinted controller argument?  <small>_(Controllers)_</small>

- A. RequestValueResolver
- B. RequestAttributeValueResolver
- C. RequestPayloadValueResolver

??? success "Answer Q6"
    **A**

    RequestValueResolver (priority 120) injects the current Request; RequestAttributeValueResolver handles named route parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q7.** How is the hidden CSRF token normally emitted into the HTML?  <small>_(Forms)_</small>

- A. By form_rest, which form_end calls by default
- B. By form_start
- C. Only by hand-writing an <input name="_token">
- D. It is never rendered inside the form

??? success "Answer Q7"
    **A**

    The CSRF token is a hidden child rendered by form_rest; form_end triggers form_rest unless you pass render_rest: false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/csrf.html)

**Q8.** During a forwarded sub-request, what does Request::isMainRequest() return?  <small>_(Controllers)_</small>

- A. false
- B. true
- C. null

??? success "Answer Q8"
    **A**

    The sub-request is dispatched with HttpKernelInterface::SUB_REQUEST, so isMainRequest() is false and some listeners (e.g. the firewall) skip.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q9.** What typically activates a bridge inside a framework application?  <small>_(Architecture)_</small>

- A. A bundle that registers the bridge's classes as services
- B. The bridge auto-registers itself at runtime
- C. A Twig template include

??? success "Answer Q9"
    **A**

    Bridges provide classes; a bundle wires them into the container and exposes configuration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q10.** During matching, when is the host constraint checked?  <small>_(Routing)_</small>

- A. Before the path regex
- B. After the controller runs
- C. Only during URL generation
- D. Never; host is informational

??? success "Answer Q10"
    **A**

    matchCollection() tests the compiled host regex first, then the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#sub-domain-routing)

**Q11.** Which method keeps a service replaced via getContainer()->set() alive across multiple requests?  <small>_(Testing)_</small>

- A. $client->disableReboot()
- B. $client->followRedirects()
- C. $client->insulate()
- D. $client->restart()

??? success "Answer Q11"
    **A**

    By default the kernel reboots after each request, discarding replacements. disableReboot() preserves the container between requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q12.** isGranted() ultimately delegates the decision to which interface?  <small>_(Security)_</small>

- A. AccessDecisionManagerInterface
- B. AuthenticatorInterface
- C. UserProviderInterface
- D. TokenStorageInterface

??? success "Answer Q12"
    **A**

    AuthorizationChecker reads the current token from TokenStorage, then calls AccessDecisionManager::decide().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Security/Core/Authorization/AccessDecisionManager.php)

**Q13.** For a PATCH submission, handleRequest passes which clearMissing value?  <small>_(Forms)_</small>

- A. false, enabling partial updates (absent fields keep their value)
- B. true, clearing all absent fields
- C. It is undefined for PATCH
- D. It depends on data_class

??? success "Answer Q13"
    **A**

    handleRequest passes clearMissing: false for PATCH so fields missing from the payload retain their current value, enabling partial updates.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Form/Form.php)

**Q14.** Response::HTTP_UNPROCESSABLE_ENTITY corresponds to which numeric code? (choose one)  <small>_(HTTP)_</small>

- A. 422
- B. 400
- C. 409
- D. 429

??? success "Answer Q14"
    **A**

    The constant keeps the RFC 4918 name 'Unprocessable Entity' but is code 422, the correct code for validation errors on a well-formed body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q15.** How do you make a failing handler skip retries and go straight to the failure transport?  <small>_(Miscellaneous)_</small>

- A. Throw UnrecoverableMessageHandlingException
- B. Return false from the handler
- C. Add a DelayStamp(0)
- D. Call $envelope->stopPropagation()

??? success "Answer Q15"
    **A**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

**Q16.** Which method validates a hypothetical value without changing the object?  <small>_(Validation)_</small>

- A. validatePropertyValue($objectOrClass, $property, $value)
- B. validateProperty($object, $property)
- C. validate($object)
- D. startContext()

??? success "Answer Q16"
    **A**

    validatePropertyValue() takes an explicit value and validates it against the property's constraints without touching the object. validateProperty() uses the object's current value instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q17.** What status does RedirectController return when the target route/path is empty?  <small>_(Controllers)_</small>

- A. 410 Gone
- B. 404 Not Found
- C. 302 Found to /

??? success "Answer Q17"
    **A**

    An empty target signals the resource is permanently gone, so the controller responds 410.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

**Q18.** What does public/index.php return under the Runtime component?  <small>_(Miscellaneous)_</small>

- A. A callable that produces the application object (e.g. a Kernel)
- B. A Response object
- C. Nothing — it echoes the output directly
- D. The exit code as an int

??? success "Answer Q18"
    **A**

    index.php returns a callable; autoload_runtime.php resolves its arguments, invokes it, then a RunnerInterface handles/sends/terminates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

**Q19.** Using the App\: resource glob, what is a service's id?  <small>_(Dependency Injection)_</small>

- A. Its fully-qualified class name (FQCN)
- B. A short snake_case name
- C. The relative file path
- D. A generated hash

??? success "Answer Q19"
    **A**

    PSR-4 auto-registration creates one definition per class using the FQCN as the service id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q20.** Intersection types such as `A&B` may combine…  <small>_(PHP & Web Security)_</small>

- A. Only class or interface types
- B. Any mix of scalars and classes
- C. Only scalar types
- D. Only enums

??? success "Answer Q20"
    **A**

    Intersection types require object (class/interface) types; scalars are not permitted.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/language.types.declarations.php)

**Q21.** Given role_hierarchy ROLE_ADMIN: [ROLE_USER], a user with ROLE_ADMIN…  <small>_(Security)_</small>

- A. Is also granted ROLE_USER (reachable roles are expanded)
- B. Is not granted ROLE_USER
- C. Loses ROLE_ADMIN
- D. Must re-login to gain ROLE_USER

??? success "Answer Q21"
    **A**

    RoleHierarchyVoter expands reachable roles, so ROLE_ADMIN transitively includes ROLE_USER. Hierarchy flows downward.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#hierarchical-roles)

**Q22.** In the path /{a}/{b}, which placeholder can be made optional?  <small>_(Routing)_</small>

- A. b only, because it is the trailing placeholder
- B. a only
- C. Both, independently
- D. Neither

??? success "Answer Q22"
    **A**

    Only trailing placeholders can be optional; a gap in the middle cannot be located by the matcher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#optional-parameters)

**Q23.** What default value does the placeholder {slug?} declare?  <small>_(Routing)_</small>

- A. null
- B. An empty string ''
- C. The literal 'slug'
- D. 0

??? success "Answer Q23"
    **A**

    A bare ? with no value after it sets the default to null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#optional-parameters)

**Q24.** On submit, which transformers run first?  <small>_(Forms)_</small>

- A. View transformers (view->norm), then model transformers (norm->model)
- B. Model transformers, then view transformers
- C. Only model transformers run on submit
- D. Order is undefined

??? success "Answer Q24"
    **A**

    On submission data flows view -> norm -> model, so view transformers' reverseTransform runs before model transformers' reverseTransform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/form/data_transformers.html)

**Q25.** Inside an overridden block, what does {{ parent() }} render?  <small>_(Twig)_</small>

- A. The parent template's version of that same block
- B. The entire parent template
- C. The parent controller's output
- D. Nothing

??? success "Answer Q25"
    **A**

    parent() outputs the content of the same block from the parent template, letting a child extend rather than fully replace it.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/parent.html)

**Q26.** What is the effect of $client->insulate()?  <small>_(Testing)_</small>

- A. Each request runs in a separate PHP subprocess, so in-process profiler/container access is lost
- B. Redirects are followed automatically
- C. The same kernel instance is reused forever
- D. Responses are cached between tests

??? success "Answer Q26"
    **A**

    Insulated requests run in a fresh subprocess to isolate global state, at the cost of losing in-process access to the profiler and container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/browser_kit.html)

**Q27.** On the violation builder, which method attaches the error to a different property?  <small>_(Validation)_</small>

- A. atPath('otherField')
- B. setPropertyPath('otherField')
- C. setInvalidValue('otherField')
- D. setCode('otherField')

??? success "Answer Q27"
    **A**

    atPath() relocates the violation to a path relative to the current node, commonly used in class-level constraints to blame a specific field.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation/custom_constraint.html)

**Q28.** What is the fully-qualified class of the routing attribute in Symfony 8?  <small>_(Routing)_</small>

- A. Symfony\Component\Routing\Attribute\Route
- B. Symfony\Component\Routing\Annotation\Route
- C. Symfony\Component\HttpKernel\Attribute\Route
- D. Symfony\Routing\Route

??? success "Answer Q28"
    **A**

    The routing attribute lives in the Attribute namespace since 6.4; the old Annotation\Route alias is removed in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q29.** Why might clearCookie('token') fail to delete the cookie?  <small>_(Controllers)_</small>

- A. The path/domain do not match those used when the cookie was set
- B. clearCookie only works over HTTPS
- C. Cookies cannot be removed from the server side

??? success "Answer Q29"
    **A**

    Deletion sends an expired Set-Cookie scoped by path/domain; a mismatch targets a different cookie and leaves the original intact.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q30.** How is an instance-method factory referenced in YAML?  <small>_(Dependency Injection)_</small>

- A. factory: ['@service_id', 'method']
- B. factory: '@service_id::method'
- C. factory: 'service_id.method'
- D. factory: @service_id

??? success "Answer Q30"
    **A**

    An array of [reference, method] denotes a method call on a service; a static factory uses the 'Class::method' string form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

**Q31.** What must a command's execute()/__invoke() return in Symfony 8?  <small>_(Console)_</small>

- A. An int exit code
- B. void
- C. A Response object
- D. A bool

??? success "Answer Q31"
    **A**

    The returned int becomes the process exit code; returning void is invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

**Q32.** Which built-in authenticator uses a token_handler returning a UserBadge?  <small>_(Security)_</small>

- A. access_token
- B. form_login
- C. http_basic
- D. remember_me

??? success "Answer Q32"
    **A**

    The access_token authenticator delegates to an AccessTokenHandlerInterface whose getUserBadgeFrom() validates the bearer token and returns a UserBadge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/access_token.html)

**Q33.** How is an inline (embedded) image referenced from an email's HTML body?  <small>_(Miscellaneous)_</small>

- A. Via a cid: reference produced by embed()/embedFromPath()
- B. Only as an absolute external URL
- C. As a base64 data: URI hand-written by the developer
- D. Inline images are not supported

??? success "Answer Q33"
    **A**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

**Q34.** What interface does Symfony's ServiceLocator implement?  <small>_(Dependency Injection)_</small>

- A. Psr\Container\ContainerInterface (PSR-11)
- B. Symfony's own ContainerInterface
- C. IteratorAggregate only
- D. CompilerPassInterface

??? success "Answer Q34"
    **A**

    ServiceLocator is a PSR-11 container exposing get() and has() over a fixed, compile-time set of services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

**Q35.** A cookie with neither Expires nor Max-Age is: (choose one)  <small>_(HTTP)_</small>

- A. a session cookie deleted when the browser closes
- B. permanent
- C. rejected by the browser
- D. valid for exactly 24 hours

??? success "Answer Q35"
    **A**

    With no lifetime attribute a cookie is a session cookie, removed when the browser session ends.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

**Q36.** What does app.environment return?  <small>_(Twig)_</small>

- A. The kernel environment string, e.g. 'dev' or 'prod'
- B. The operating-system environment variables
- C. The APP_ENV file path
- D. A boolean debug flag

??? success "Answer Q36"
    **A**

    app.environment is the kernel environment (dev/prod/test); app.debug is the boolean debug flag. They are unrelated to OS env vars.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

**Q37.** By default, debug:container hides which services?  <small>_(Dependency Injection)_</small>

- A. Private services (shown only with --show-private)
- B. Public services
- C. Aliases
- D. Parameters

??? success "Answer Q37"
    **A**

    debug:container lists public services and aliases; add --show-private to include private ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

**Q38.** Which set contains only idempotent methods? (choose one)  <small>_(HTTP)_</small>

- A. GET, PUT, DELETE
- B. GET, POST, PUT
- C. POST, PATCH, DELETE
- D. POST, PUT, PATCH

??? success "Answer Q38"
    **A**

    GET, PUT and DELETE are idempotent (repeating yields the same state); POST and PATCH are not.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)

**Q39.** Under which license is Symfony released?  <small>_(Architecture)_</small>

- A. MIT
- B. GPLv3
- C. Apache 2.0

??? success "Answer Q39"
    **A**

    Symfony components are released under the permissive, non-copyleft MIT license.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/LICENSE)

**Q40.** How does a recipe auto-register a bundle?  <small>_(Architecture)_</small>

- A. By writing an entry into config/bundles.php
- B. Via an #[AsBundle] attribute
- C. By editing services.yaml

??? success "Answer Q40"
    **A**

    The bundles configurator adds the bundle class to config/bundles.php, which the kernel reads at boot via MicroKernelTrait::registerBundles().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q41.** How does a callback validator register an error?  <small>_(Validation)_</small>

- A. $context->buildViolation('...')->addViolation();
- B. return 'the error message';
- C. return false;
- D. throw new ValidationException('...');

??? success "Answer Q41"
    **A**

    Violations are built and committed through the execution context. The callback's return value is ignored.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/constraints/Callback.html)

**Q42.** What does the expression `trim(...)` produce?  <small>_(PHP & Web Security)_</small>

- A. A Closure wrapping the trim function
- B. The string 'trim'
- C. The trimmed result
- D. A parse error in PHP 8.4

??? success "Answer Q42"
    **A**

    First-class callable syntax (8.1+) creates a Closure from any callable.

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/functions.first_class_callable_syntax.php)

**Q43.** What does the #[Target('requestLogger')] attribute do?  <small>_(Dependency Injection)_</small>

- A. Selects the named autowiring alias explicitly, decoupled from the parameter name
- B. Creates a new service definition
- C. Adds a tag to the service
- D. Makes the service public

??? success "Answer Q43"
    **A**

    #[Target] binds to a named autowiring alias by name, so renaming the constructor parameter does not break wiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html#fixing-non-autowireable-arguments)

**Q44.** What does MoneyType's divisor option do?  <small>_(Forms)_</small>

- A. Scales the model value (e.g. 100 lets you store integer cents)
- B. Sets the currency symbol
- C. Rounds to N decimals
- D. Limits the maximum amount

??? success "Answer Q44"
    **A**

    The displayed amount is divided by divisor to form the model value, so 100 lets you store amounts in cents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/forms/types/money.html)

**Q45.** Which command lists what a given type-hint autowires to?  <small>_(Dependency Injection)_</small>

- A. debug:autowiring
- B. debug:config
- C. debug:router
- D. config:dump-reference

??? success "Answer Q45"
    **A**

    debug:autowiring shows the types you can type-hint and which service each resolves to; debug:container inspects a definition by id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

**Q46.** Which flag maps to VERBOSITY_VERY_VERBOSE?  <small>_(Console)_</small>

- A. -vv
- B. -v
- C. -vvv
- D. -q

??? success "Answer Q46"
    **A**

    -v is VERBOSE, -vv is VERY_VERBOSE, -vvv is DEBUG, -q is QUIET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console/verbosity.html)

**Q47.** What is a caching side effect of touching the session on a public page?  <small>_(Controllers)_</small>

- A. A Set-Cookie header makes the response uncacheable by shared proxies
- B. Nothing; sessions never affect HTTP caching
- C. It disables Twig template caching

??? success "Answer Q47"
    **A**

    Shared caches must not store responses carrying a per-user Set-Cookie, so touching the session prevents shared caching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q48.** How many firewalls are active for a given request?  <small>_(Security)_</small>

- A. Exactly one — the first whose matcher matches
- B. All firewalls that match
- C. One per HTTP method
- D. Zero or many

??? success "Answer Q48"
    **A**

    The FirewallMap returns the first matching FirewallContext; matching stops there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

**Q49.** By default in Symfony 8, is the _method parameter honoured? (choose one)  <small>_(HTTP)_</small>

- A. No — http_method_override defaults to false and must be enabled
- B. Yes, always
- C. Only for GET requests
- D. Only for JSON requests

??? success "Answer Q49"
    **A**

    You must enable framework.http_method_override (or call Request::enableHttpMethodParameterOverride()); it applies to POST only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q50.** What is the result of {{ "a" ~ 1 + 1 }}?  <small>_(Twig)_</small>

- A. "a2"
- B. "a11"
- C. 2
- D. An error

??? success "Answer Q50"
    **A**

    + binds tighter than ~, so it evaluates as "a" ~ (1 + 1) => "a" ~ 2 => "a2". ~ is string concatenation, not addition.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

**Q51.** Generating a URL for a route bound to a different host produces?  <small>_(Routing)_</small>

- A. An absolute (or network) URL
- B. A root-relative path
- C. An exception
- D. A URL on the current host

??? success "Answer Q51"
    **A**

    A path-only URL cannot switch host, so the generator upgrades the reference type automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

**Q52.** Which resolvers have the highest default priority (120) in Symfony 8?  <small>_(Controllers)_</small>

- A. RequestValueResolver and SessionValueResolver
- B. DefaultValueResolver and VariadicValueResolver
- C. RequestAttributeValueResolver and BackedEnumValueResolver

??? success "Answer Q52"
    **A**

    Request and Session resolvers run first at priority 120; the attribute, enum, uid and datetime resolvers sit at 100.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Resources/config/web.php)

**Q53.** What integer value does `Command::INVALID` represent?  <small>_(Console)_</small>

- A. 2
- B. 0
- C. 1
- D. 255

??? success "Answer Q53"
    **A**

    The return constants are SUCCESS=0, FAILURE=1, INVALID=2.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html)

**Q54.** Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?  <small>_(Miscellaneous)_</small>

- A. --limit (max messages) and --time-limit (max seconds), optionally with memory limits
- B. --kill and --restart
- C. --stop-now only
- D. --reload after each message

??? success "Answer Q54"
    **A**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

**Q55.** What does app.user return when no one is authenticated?  <small>_(Twig)_</small>

- A. null
- B. An empty User object
- C. The string 'anonymous'
- D. It throws an exception

??? success "Answer Q55"
    **A**

    AppVariable::getUser() reads the token from the token storage and returns its user, or null when there is no authenticated user.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

**Q56.** How do you read the value of an unmapped FileType field?  <small>_(Forms)_</small>

- A. $form->get('field')->getData()
- B. From the bound model object
- C. $request->request->get('field')
- D. $form->getViewData()

??? success "Answer Q56"
    **A**

    mapped => false excludes the field from the data mapper, so it is not written to the model; you fetch it directly from the child form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

**Q57.** Which Response class streams an on-disk file and supports HTTP range requests? (choose one)  <small>_(HTTP)_</small>

- A. BinaryFileResponse
- B. Response
- C. JsonResponse
- D. RedirectResponse

??? success "Answer Q57"
    **A**

    BinaryFileResponse streams a file without buffering it in memory and supports Range requests and X-Sendfile.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#serving-files)

**Q58.** What is a Symfony bridge?  <small>_(Architecture)_</small>

- A. An integration layer between a component and a specific third-party library
- B. A configuration file format
- C. A replacement for the service container

??? success "Answer Q58"
    **A**

    A bridge holds the glue coupling a Symfony component to one specific external library, keeping the component itself dependency-free.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

**Q59.** Why must the dev firewall (security: false) be listed first?  <small>_(Security)_</small>

- A. Firewalls are first-match, so it must precede protecting firewalls
- B. Alphabetical ordering is enforced
- C. It sets global defaults for later firewalls
- D. Order is irrelevant for firewalls

??? success "Answer Q59"
    **A**

    Firewall matching is top-to-bottom, first match wins. Listing the dev firewall first stops the profiler/assets being intercepted by login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-firewall)

**Q60.** How do you retrieve a synchronous handler's return value after MessageBusInterface::dispatch()?  <small>_(Miscellaneous)_</small>

- A. $envelope->last(HandledStamp::class)->getResult()
- B. The value is returned directly by dispatch()
- C. $envelope->getResult()
- D. $bus->getLastResult()

??? success "Answer Q60"
    **A**

    dispatch() returns an Envelope. For a single sync handler you read its result via the HandledStamp: $envelope->last(HandledStamp::class)->getResult(). Use HandleTrait to unwrap it in a query bus.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

**Q61.** A method referenced by #[DataProvider('provide')] must be…  <small>_(Testing)_</small>

- A. public static and return an array or other iterable of argument sets
- B. private and return void
- C. a protected instance method returning a Generator only
- D. annotated with #[Test] as well

??? success "Answer Q61"
    **A**

    PHPUnit\Framework\Attributes\DataProvider names a public static method returning an iterable (array or Generator) of argument arrays; each set becomes one parameterised run of the test.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

**Q62.** Where should business logic live according to the best practices?  <small>_(Architecture)_</small>

- A. In autowired services
- B. In controllers
- C. In Twig templates

??? success "Answer Q62"
    **A**

    Controllers should be thin and delegate to services, which keeps logic reusable and testable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/best_practices.html)

**Q63.** What does ValidatorInterface::validate() return when the value is invalid?  <small>_(Validation)_</small>

- A. A ConstraintViolationListInterface containing the violations
- B. false
- C. It throws a ValidationFailedException
- D. An array of error message strings

??? success "Answer Q63"
    **A**

    validate() always returns a ConstraintViolationListInterface. It never returns a bool and never throws on failure; you inspect the result with count() and by iterating it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/validation.html)

**Q64.** By default, after a controller returns a 302 redirect, the test client…  <small>_(Testing)_</small>

- A. Stops on the redirect so you can assert the Location, until you call followRedirect()
- B. Follows the redirect automatically
- C. Throws an exception
- D. Retries the original request

??? success "Answer Q64"
    **A**

    Auto-follow is off by default. Use followRedirect() to follow the last redirect once, or followRedirects() to toggle auto-following.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#redirecting)

**Q65.** What is the correct way to store user passwords?  <small>_(PHP & Web Security)_</small>

- A. password_hash() with bcrypt or argon2id
- B. SHA-256 with a single static salt
- C. MD5
- D. Reversible encryption

??? success "Answer Q65"
    **A**

    Adaptive, salted hashing (bcrypt/argon2id) resists brute-force; the salt is embedded in the hash and verified with password_verify().

    :material-book-open-variant: [Docs](https://www.php.net/manual/en/function.password-hash.php)

**Q66.** After a message exhausts its configured retries, where does it go?  <small>_(Miscellaneous)_</small>

- A. To the configured failure transport
- B. To the sync transport
- C. It is silently discarded
- D. Back to the front of the same queue forever

??? success "Answer Q66"
    **A**

    Once max_retries is reached the envelope is sent to the failure_transport, where messenger:failed:show/retry can inspect and requeue it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#saving-retrying-failed-messages)

**Q67.** What does security: false on a firewall do?  <small>_(Security)_</small>

- A. Disables the security layer for that zone (and still counts as the match)
- B. Denies all access to that zone
- C. Enables anonymous voting
- D. Makes the firewall stateless

??? success "Answer Q67"
    **A**

    It turns off all security listeners for matching requests (used for the profiler and dev assets) and, being first-match, prevents later firewalls from matching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html)

**Q68.** Which directory is the web root of a Symfony application?  <small>_(Architecture)_</small>

- A. public/
- B. src/
- C. web/

??? success "Answer Q68"
    **A**

    public/ contains index.php and static assets and is the only web-accessible directory.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

**Q69.** What does MessageBusInterface::dispatch() return?  <small>_(Miscellaneous)_</small>

- A. An Envelope
- B. The handler's return value
- C. void
- D. A HandledStamp

??? success "Answer Q69"
    **A**

    dispatch() always returns the (possibly stamped) Envelope. A handler's return value is available via $envelope->last(HandledStamp::class)->getResult().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html)

**Q70.** Does a user provider verify the user's password?  <small>_(Security)_</small>

- A. No — credentials are checked on CheckPassportEvent
- B. Yes, in loadUserByIdentifier()
- C. Yes, in refreshUser()
- D. Only the memory provider does

??? success "Answer Q70"
    **A**

    Providers only load and refresh users. CheckCredentialsListener verifies the PasswordCredentials badge.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security/custom_authenticator.html)

**Q71.** How should you customise a final Symfony class in a BC-safe way?  <small>_(Architecture)_</small>

- A. Decorate or compose it
- B. Subclass and override it
- C. Edit it in vendor/

??? success "Answer Q71"
    **A**

    final classes must not be subclassed; wrap them via decoration so Symfony can change internals without breaking you.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q72.** Which class renders Twig templates into an email body?  <small>_(Miscellaneous)_</small>

- A. Symfony\Bridge\Twig\Mime\TemplatedEmail
- B. Symfony\Component\Mime\Email
- C. Symfony\Component\Mailer\Mailer
- D. Symfony\Component\Mime\Message

??? success "Answer Q72"
    **A**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

**Q73.** Using #[Cache(etag: 'post.getContent()')], what value is actually sent as the ETag?  <small>_(HTTP Caching)_</small>

- A. The SHA-256 hash of the evaluated expression
- B. The literal string 'post.getContent()'
- C. The raw return value of getContent()
- D. A weak ETag of the whole rendered body

??? success "Answer Q73"
    **A**

    CacheAttributeListener evaluates the expression on kernel.controller_arguments and SHA-256-hashes the result before using it as the ETag, so it can point at large content safely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#the-cache-attribute)

**Q74.** Which attribute registers a compiler pass? (choose one)  <small>_(Dependency Injection)_</small>

- A. There is no attribute; register it via addCompilerPass() in Kernel/bundle build()
- B. #[CompilerPass]
- C. #[AsCompilerPass]
- D. #[Autoconfigure(pass: true)]

??? success "Answer Q74"
    **A**

    Compiler passes are registered programmatically via ContainerBuilder::addCompilerPass(), typically in Kernel::build() or a bundle's build(). There is no core attribute for this.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

**Q75.** How does a ServiceLocator differ from injecting the whole container?  <small>_(Dependency Injection)_</small>

- A. It exposes only an explicitly declared, whitelisted set of services
- B. It is eager while the container is lazy
- C. It cannot instantiate services
- D. There is no real difference

??? success "Answer Q75"
    **A**

    A locator's set is explicit and analysable; injecting the whole container hides dependencies and is an anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

---

<small>Back to [Revision Hub](index.md) · [Practice Quiz Bank](quiz.md)</small>
