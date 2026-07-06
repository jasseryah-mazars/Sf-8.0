# Chapter Exam — Controllers

!!! abstract "How to use"
    94 questions spanning every subchapter of **Controllers**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

Full theory: [Controllers](../controllers/index.md).

---

**Q1.** How is an invokable single-action controller referenced in the `_controller` attribute? (choose one)  <small>_(easy · single)_</small>

- A. The fully-qualified class name only (Symfony calls __invoke)
- B. Class::__invokeAction
- C. class#invoke

??? success "Answer Q1"
    **A**

    For an invokable controller you reference only the class; the ControllerResolver detects the __invoke() method automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q2.** Is the `Action` method suffix required for controller actions in Symfony 8?  <small>_(easy · single)_</small>

- A. No — it is a legacy convention with no meaning under attribute routing
- B. Yes, the router matches methods ending in Action
- C. Yes, but only for invokable controllers

??? success "Answer Q2"
    **A**

    Attribute routing binds a specific method explicitly, so the Action suffix is purely historical and can be dropped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q3.** What visibility must a controller action method have to be invoked by the kernel?  <small>_(easy · single)_</small>

- A. public
- B. protected
- C. private

??? success "Answer Q3"
    **A**

    The kernel invokes the controller callable externally, so the method must be public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q4.** A controller must extend `AbstractController` to be usable in Symfony 8. True or false?  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q4"
    **A**

    Extending `AbstractController` is optional convenience. A controller is any callable returning a Response; a plain invokable class with no base class is perfectly valid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q5.** When overriding getSubscribedServices() to add a service, what must you do to keep the built-in helpers?  <small>_(easy · single)_</small>

- A. Spread parent::getSubscribedServices() into the returned array
- B. Nothing; helpers are always available
- C. Re-declare every core service manually

??? success "Answer Q5"
    **A**

    Returning only your service replaces the list; merge the parent's subscriptions so render/getUser/etc. still resolve.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#the-base-controller-class-services)

**Q6.** Which value resolver supplies a `Request` type-hinted controller argument?  <small>_(easy · single)_</small>

- A. RequestValueResolver
- B. RequestAttributeValueResolver
- C. RequestPayloadValueResolver

??? success "Answer Q6"
    **A**

    RequestValueResolver (priority 120) injects the current Request; RequestAttributeValueResolver handles named route parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q7.** In which parameter bag do matched route parameters appear?  <small>_(easy · single)_</small>

- A. $request->attributes
- B. $request->query
- C. $request->request

??? success "Answer Q7"
    **A**

    The router writes matched parameters into the attributes bag; query is GET data and request is the POST body.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q8.** The `Request` object can be autowired directly into a service constructor. True or false?  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q8"
    **A**

    The Request is request-scoped and created per HTTP call, so it is not an autowireable service. Inject RequestStack and call getCurrentRequest().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

**Q9.** What must a controller ultimately produce?  <small>_(easy · single)_</small>

- A. A Response object (or a value converted to one by a kernel.view listener)
- B. An array that Symfony auto-serializes to JSON
- C. A string that becomes the body

??? success "Answer Q9"
    **A**

    If a controller returns a non-Response, the kernel fires ViewEvent; if no listener produces a Response a LogicException is thrown.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q10.** Where does a controller read incoming cookies from?  <small>_(easy · single)_</small>

- A. $request->cookies
- B. $request->headers
- C. $_SESSION

??? success "Answer Q10"
    **A**

    The cookies ParameterBag wraps $_COOKIE; responses set cookies via $response->headers->setCookie().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q11.** A cookie sent with SameSite=None also requires which attribute?  <small>_(easy · single)_</small>

- A. Secure=true
- B. HttpOnly=false
- C. A domain attribute

??? success "Answer Q11"
    **A**

    Modern browsers reject SameSite=None cookies unless they are marked Secure (HTTPS-only).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#setting-cookies)

**Q12.** In Symfony's Cookie value object, `httpOnly` defaults to true. True or false?  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q12"
    **A**

    Cookie defaults are security-first: httpOnly=true (hidden from JS, mitigating XSS token theft) and sameSite='lax'. JS-readable cookies must opt out explicitly with withHttpOnly(false).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Cookie.php)

**Q13.** What is the recommended way for a service to access the session?  <small>_(easy · single)_</small>

- A. Inject RequestStack and call getSession()
- B. Inject SessionInterface in the constructor
- C. Use the $_SESSION superglobal

??? success "Answer Q13"
    **A**

    The session is request-scoped; RequestStack::getSession() is the stable entry point in services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

**Q14.** What happens the first time you read a flash message (get/all or app.flashes)?  <small>_(easy · single)_</small>

- A. It is returned and removed (consumed)
- B. It stays until the session expires
- C. It is copied to the next request

??? success "Answer Q14"
    **A**

    Reading consumes flashes; use peek()/peekAll() to read without removing them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q15.** `$this->addFlash('notice', 'Saved')` is shorthand for which call?  <small>_(easy · single)_</small>

- A. getSession()->getFlashBag()->add('notice', 'Saved')
- B. Setting a response header
- C. Writing a cookie

??? success "Answer Q15"
    **A**

    addFlash() is an AbstractController convenience over the session flash bag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q16.** Why are flash messages typically paired with a redirect?  <small>_(easy · single)_</small>

- A. They display on the next (GET) request, matching the Post/Redirect/Get pattern
- B. Redirects are required to write to the session
- C. Flashes cannot be added during a GET request

??? success "Answer Q16"
    **A**

    Flashes are built to survive exactly one redirect and be shown on the following request, then discarded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q17.** Which method reads flash messages WITHOUT consuming them?  <small>_(easy · trap)_</small>

- A. peek() / peekAll()
- B. get() / all()
- C. read() / readAll()
- D. keep() / keepAll()

??? success "Answer Q17"
    **A**

    peek()/peekAll() return messages while leaving them in the bag. get()/all() both return and remove. There are no read()/keep() methods on FlashBag.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Session/Flash/FlashBag.php)

**Q18.** Which Twig loop renders all flash types, consuming them once?  <small>_(easy · code)_</small>

- A. {% for label, messages in app.flashes %}{% for m in messages %}{{ m }}{% endfor %}{% endfor %}
- B. {% for m in app.session.flash %}{{ m }}{% endfor %}
- C. {{ app.flashes|raw }}
- D. {% for m in flashbag() %}{{ m }}{% endfor %}

??? success "Answer Q18"
    **A**

    app.flashes yields a map of type => messages; iterating it calls all() under the hood, which consumes the bag so each message shows exactly once.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q19.** What is the default HTTP status code of redirectToRoute()?  <small>_(easy · single)_</small>

- A. 302
- B. 301
- C. 307

??? success "Answer Q19"
    **A**

    RedirectResponse defaults to 302 Found; pass a status argument to change it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q20.** What is the difference between redirect() and redirectToRoute()?  <small>_(easy · single)_</small>

- A. redirect() takes a URL; redirectToRoute() takes a route name and parameters
- B. redirect() is 301 and redirectToRoute() is 302
- C. redirectToRoute() performs an internal forward

??? success "Answer Q20"
    **A**

    redirect() is URL-based; redirectToRoute() builds the URL from the router. Both return a RedirectResponse (default 302).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q21.** `redirect()` accepts a route name as its first argument. True or false?  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q21"
    **A**

    redirect() takes a URL (string). To redirect by route name (plus params), use redirectToRoute(), which builds the URL via the router.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q22.** What does AbstractController::forward() do?  <small>_(easy · single)_</small>

- A. Runs another controller in a sub-request and returns its Response, without a new client request
- B. Sends a 302 redirect to another route
- C. Includes a Twig template

??? success "Answer Q22"
    **A**

    forward() dispatches a sub-request through the kernel; the browser URL does not change and no 3xx is sent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#forwarding-to-another-controller)

**Q23.** After a forward(), what does the user's address bar show?  <small>_(easy · single)_</small>

- A. The original URL, unchanged
- B. The forwarded controller's route
- C. An internal /_fragment URL

??? success "Answer Q23"
    **A**

    Forwarding is server-internal within the same request, so no new client navigation occurs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#forwarding-to-another-controller)

**Q24.** Which value should you trust to determine an uploaded file's real type?  <small>_(easy · single)_</small>

- A. getMimeType() (content-detected by the guesser)
- B. getClientMimeType()
- C. getClientOriginalExtension()

??? success "Answer Q24"
    **A**

    Client-supplied name/MIME are spoofable; getMimeType()/guessExtension() inspect the actual file content.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

**Q25.** What does UploadedFile::move() do when it fails?  <small>_(easy · single)_</small>

- A. Throws a FileException
- B. Returns false
- C. Returns null and logs a warning

??? success "Answer Q25"
    **A**

    move() throws FileException on failure rather than returning a status value.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

**Q26.** Which built-in controller renders a Twig template purely from route config?  <small>_(easy · single)_</small>

- A. TemplateController
- B. RenderController
- C. TwigController

??? success "Answer Q26"
    **A**

    TemplateController::__invoke() renders the 'template' default and can set HTTP cache headers, needing no custom class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#rendering-a-template-directly-from-a-route)

**Q27.** How does a value resolver signal that it does not handle an argument?  <small>_(easy · single)_</small>

- A. It yields nothing (returns an empty iterable)
- B. It returns false
- C. It throws UnsupportedArgumentException

??? success "Answer Q27"
    **A**

    Yielding no value passes the argument to the next resolver in priority order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q28.** What binds a single typed query parameter such as ?page=2 to an int argument?  <small>_(easy · single)_</small>

- A. #[MapQueryParameter]
- B. #[MapQueryString]
- C. #[MapRequestPayload]

??? success "Answer Q28"
    **A**

    #[MapQueryParameter] binds one query value with casting; #[MapQueryString] maps the whole query string into a DTO.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q29.** Which statement best defines a Symfony controller?  <small>_(medium · single)_</small>

- A. Any PHP callable that returns a Response
- B. A class extending AbstractController
- C. A method whose name ends in Action

??? success "Answer Q29"
    **A**

    A controller is any callable (method, invokable object, closure) the kernel runs to produce a Response; extending AbstractController is optional.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q30.** A route is declared as `#[Route('/', name: 'home')]` on the class `App\Controller\HomeController`, which defines a `public function __invoke(): Response`. Which YAML `controller:` value targets it correctly?  <small>_(medium · code)_</small>

- A. controller: App\Controller\HomeController
- B. controller: App\Controller\HomeController::__invokeAction
- C. controller: App\Controller\HomeController#invoke
- D. controller: home_controller.invoke

??? success "Answer Q30"
    **A**

    For an invokable controller the `_controller` value is the class name alone; the resolver detects `__invoke()`. Adding `::__invoke` also works but is not idiomatic, and `#invoke` / a made-up service id are invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q31.** Which of these are valid `_controller` formats the ControllerResolver accepts? (choose 3)  <small>_(medium · multiple)_</small>

- A. App\Controller\ProductController::show (class + method)
- B. App\Controller\HomepageController (invokable class)
- C. service_id::method or service_id alone
- D. App\Controller\ProductController#show

??? success "Answer Q31"
    **A, B, C**

    The resolver normalises `Class::method`, an invokable `Class`, a `service_id::method`/`service_id`, or a closure into a callable. The `Class#method` syntax is not a recognised format.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/ControllerResolver.php)

**Q32.** What does `$this->container` hold inside an AbstractController?  <small>_(medium · trap)_</small>

- A. Only the subscribed services (a restricted service locator)
- B. The entire application service container
- C. Only container parameters

??? success "Answer Q32"
    **A**

    The injected locator exposes exactly the services returned by getSubscribedServices(), not the whole container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q33.** What happens if you call `$this->render()` without Twig installed?  <small>_(medium · single)_</small>

- A. A clear LogicException telling you Twig is required
- B. A container 'service not found' fatal error
- C. It silently returns an empty Response

??? success "Answer Q33"
    **A**

    The twig service is subscribed with the optional '?' prefix, so the helper guards its absence with a descriptive LogicException.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/AbstractController.php)

**Q34.** You extend AbstractController and override getSubscribedServices() to add a `ReportGenerator`. Which body keeps `render()`, `getUser()`, etc. working?  <small>_(medium · code)_</small>

- A. return [...parent::getSubscribedServices(), ReportGenerator::class];
- B. return [ReportGenerator::class];
- C. return array_merge([ReportGenerator::class]); // no parent call
- D. parent::getSubscribedServices(); return [ReportGenerator::class];

??? success "Answer Q34"
    **A**

    The subscription list fully replaces the inherited one, so you must spread `parent::getSubscribedServices()` alongside your own entry. Returning only your service drops router/twig/security and breaks every helper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q35.** In getSubscribedServices(), what does prefixing a service with `?` (e.g. `'?'.Environment::class`) mean?  <small>_(medium · trap)_</small>

- A. The service is optional; if absent the locator returns null instead of failing to compile
- B. The service is lazily proxied but always required
- C. The service is private and cannot be fetched
- D. It marks the service as deprecated

??? success "Answer Q35"
    **A**

    The `?` marks the subscription optional, letting the controller boot even when (say) Twig or the form factory is not installed; the helper then throws a clear LogicException rather than a container error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q36.** A developer fetches an application service with `$this->container->get(InvoiceMailer::class)` inside a controller and gets a 'service not found' error. What is the correct fix?  <small>_(medium · debug)_</small>

- A. Inject InvoiceMailer via the constructor — $this->container only holds subscribed helper services
- B. Call $this->get() instead of $this->container->get()
- C. Register InvoiceMailer as public in services.yaml
- D. Add InvoiceMailer to the kernel's global container

??? success "Answer Q36"
    **A**

    `$this->container` is the restricted subscriber locator; it only exposes the framework helper services, not your domain services. Inject your own dependencies through the constructor instead of using the locator as a service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#the-base-controller-class-services)

**Q37.** Which AbstractController helpers directly return a Response (or subclass)? (choose 3)  <small>_(medium · multiple)_</small>

- A. render() → Response
- B. json() → JsonResponse
- C. redirectToRoute() → RedirectResponse
- D. createNotFoundException() → Response

??? success "Answer Q37"
    **A, B, C**

    render/json/redirectToRoute (and file/stream/forward) return a Response or subclass. createNotFoundException() returns a NotFoundHttpException you must throw — it is not a Response and does not abort on its own.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q38.** On a public (no-firewall) route, `return new Response($this->getUser()->getEmail());` fatals with 'Call to a member function getEmail() on null'. Why?  <small>_(medium · debug)_</small>

- A. getUser() returns ?UserInterface and is null when no one is authenticated
- B. getUser() always throws on public routes
- C. The token storage service is not subscribed
- D. Response cannot accept a string built from getUser()

??? success "Answer Q38"
    **A**

    getUser() reads security.token_storage; with no authenticated token it returns null. Guard with denyAccessUnlessGranted()/#[IsGranted] first, or read defensively with `$this->getUser()?->getEmail()`.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/AbstractController.php)

**Q39.** How should a service (not a controller) access the current Request?  <small>_(medium · single)_</small>

- A. Inject RequestStack and call getCurrentRequest()
- B. Autowire Request in the constructor
- C. Call Request::createFromGlobals()

??? success "Answer Q39"
    **A**

    The Request is request-scoped and cannot be injected directly; inject the RequestStack service instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

**Q40.** What does the `$request->request` bag actually contain?  <small>_(medium · trap)_</small>

- A. The POST body parameters ($_POST)
- B. The Request object itself
- C. The query string parameters
- D. The matched route parameters

??? success "Answer Q40"
    **A**

    Despite the name, `$request->request` is the InputBag of POST body fields, not 'the request object'. Query lives in `$request->query`, route params in `$request->attributes`.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q41.** `$request->getContent()` is called on a JSON API request. What does it return?  <small>_(medium · code)_</small>

- A. The raw request body as a string — it is not JSON-decoded
- B. An associative array decoded from the JSON body
- C. The parsed $request->request InputBag
- D. A stdClass of the JSON payload

??? success "Answer Q41"
    **A**

    getContent() returns the raw body; it does not decode JSON. Use #[MapRequestPayload] (serializer + validator) or json_decode() yourself to get a structured value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q42.** Which response class best serves a resumable (range-request) file download?  <small>_(medium · single)_</small>

- A. BinaryFileResponse
- B. StreamedResponse
- C. JsonResponse

??? success "Answer Q42"
    **A**

    BinaryFileResponse supports HTTP range requests and X-Sendfile/X-Accel offloading for efficient downloads.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#serving-files)

**Q43.** An action does `return ['id' => 1, 'name' => 'Ada'];` expecting Symfony to auto-serialize it to JSON, but the request fails. Why?  <small>_(medium · debug)_</small>

- A. Symfony does not auto-serialize arrays by default; with no kernel.view listener the kernel throws a LogicException
- B. Arrays are silently rendered as a 200 with an empty body
- C. The array is cast to a string body
- D. It returns a 500 with the array var_dump()ed

??? success "Answer Q43"
    **A**

    A non-Response return fires ViewEvent; without a listener that builds a Response, the kernel throws 'The controller must return a Response'. Return $this->json($data) explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

**Q44.** You already hold a valid JSON string. Which avoids double-encoding it in a JsonResponse?  <small>_(medium · single)_</small>

- A. JsonResponse::fromJsonString($json)
- B. new JsonResponse($json)
- C. $this->json($json)
- D. new JsonResponse(json_decode($json))

??? success "Answer Q44"
    **A**

    new JsonResponse($json) / $this->json($json) would JSON-encode the string again (double-encoding). fromJsonString() sets the body verbatim and the application/json Content-Type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q45.** Why might clearCookie('token') fail to delete the cookie?  <small>_(medium · debug)_</small>

- A. The path/domain do not match those used when the cookie was set
- B. clearCookie only works over HTTPS
- C. Cookies cannot be removed from the server side

??? success "Answer Q45"
    **A**

    Deletion sends an expired Set-Cookie scoped by path/domain; a mismatch targets a different cookie and leaves the original intact.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q46.** `Cookie::create('t','v')->withSameSite(Cookie::SAMESITE_NONE)` is set without calling `withSecure(true)`. What is the effect in modern browsers?  <small>_(medium · code)_</small>

- A. Browsers reject the cookie because SameSite=None requires Secure
- B. The cookie is accepted but treated as SameSite=Lax
- C. Symfony throws at construction time
- D. The cookie is silently upgraded to Secure

??? success "Answer Q46"
    **A**

    SameSite=None mandates the Secure attribute; without it the browser drops the cookie. Chain ->withSecure(true) so it is sent only over HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#setting-cookies)

**Q47.** An action sets a `theme` cookie on the response, then in the same action reads `$request->cookies->get('theme')` and gets the old value. Why?  <small>_(medium · trap)_</small>

- A. A cookie set on the response is only sent to the browser and readable on subsequent requests
- B. You must call $request->cookies->refresh() first
- C. setCookie also updates the request bag synchronously
- D. clearCookie must be called before re-reading

??? success "Answer Q47"
    **A**

    Response cookies go out as Set-Cookie headers; the request's cookies bag reflects what the browser already sent. A newly set cookie is only visible on the next request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#setting-cookies)

**Q48.** Which method regenerates the session id after login to prevent session fixation?  <small>_(medium · single)_</small>

- A. migrate()
- B. clear()
- C. save()

??? success "Answer Q48"
    **A**

    migrate() issues a new session id while keeping data; invalidate() also wipes data. Symfony authenticators call migrate() on login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

**Q49.** A console command injects RequestStack and calls `getSession()`, which throws SessionNotFoundException. What is the cause and fix?  <small>_(medium · debug)_</small>

- A. There is no current request in the CLI; guard with getCurrentRequest() and hasSession() before reading
- B. getSession() returns null in CLI; check for null instead
- C. Sessions require enabling framework.session in the console
- D. You must call session_start() manually first

??? success "Answer Q49"
    **A**

    getSession() throws SessionNotFoundException (it does not return null) when called outside a request or on a request with no session. Guard the request first: check getCurrentRequest() and hasSession().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

**Q50.** Why is injecting `SessionInterface` directly into a service constructor discouraged in Symfony 8?  <small>_(medium · trap)_</small>

- A. The session is request-scoped; inject RequestStack and call getSession() so it resolves per request
- B. SessionInterface is deprecated in favour of $_SESSION
- C. It forces the session to start eagerly on boot, which is fine
- D. SessionInterface cannot be type-hinted anywhere

??? success "Answer Q50"
    **A**

    Directly autowiring the request-scoped session into a long-lived service is discouraged/removed; RequestStack::getSession() is the stable entry point. You can still type-hint SessionInterface on a controller action (resolved by SessionValueResolver, priority 120).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

**Q51.** Merely type-hinting SessionInterface on an action starts the session. True or false?  <small>_(medium · true-false)_</small>

- A. False
- B. True

??? success "Answer Q51"
    **A**

    Sessions are lazy: SessionValueResolver injects the session object, but session_start() and the Set-Cookie header only fire on the first read or write. Merely receiving the session does not start it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

**Q52.** A controller reads `app.session.flashbag.get('success')` for logging, then the Twig template shows no flash. What happened?  <small>_(medium · debug)_</small>

- A. get() consumed (drained) the messages, so nothing remains for Twig; use peek() to read without consuming
- B. Flashes only render on POST requests
- C. The template must call addFlash() again
- D. The session expired between the two reads

??? success "Answer Q52"
    **A**

    get()/all() consume the flash bag. Reading in the controller drains the messages before Twig can show them. Use peek()/peekAll() when you must read without removing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

**Q53.** Which redirect status codes preserve the original HTTP method and body?  <small>_(medium · single)_</small>

- A. 307 and 308
- B. 301 and 302
- C. 302 and 303

??? success "Answer Q53"
    **A**

    307/308 must not change the request method; 303 always forces GET and 301/302 may downgrade to GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q54.** After creating a resource in a POST action, you want the browser to issue a GET to the show page. Which call is correct?  <small>_(medium · code)_</small>

- A. return $this->redirectToRoute('resource_show', ['id' => $id], 303);
- B. return $this->redirectToRoute('resource_show', ['id' => $id], 307);
- C. return $this->forward('resource_show', ['id' => $id]);
- D. return $this->redirect('resource_show', ['id' => $id]);

??? success "Answer Q54"
    **A**

    303 See Other forces the follow-up request to GET, the strict form of Post/Redirect/Get. 307 would preserve POST; forward() is internal (no URL change); redirect() takes a URL, not a route name + params.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q55.** A checkout POST persists an order and redirects to the confirmation page to avoid duplicate submissions on refresh. Which status best fits?  <small>_(medium · scenario)_</small>

- A. 302 (or the stricter 303) — a temporary, non-cached redirect for PRG
- B. 301 Moved Permanently
- C. 308 Permanent Redirect
- D. 307 Temporary Redirect (keeps POST)

??? success "Answer Q55"
    **A**

    PRG needs a temporary redirect that ends on a GET. 302 (default) or 303 are correct; 301/308 are cached (wrong and hard to undo), and 307 would replay the POST.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q56.** Why is accidentally using 301 (or 308) for a temporary redirect dangerous?  <small>_(medium · trap)_</small>

- A. 301/308 are cached by browsers, so the redirect sticks and is hard to undo
- B. 301/308 are ignored by browsers
- C. 301/308 always force a GET, losing the body
- D. 301/308 require HTTPS to function

??? success "Answer Q56"
    **A**

    301 and 308 signal a permanent move and are cached by browsers; if used by mistake the client keeps redirecting even after you fix the server. Use 302/303 for temporary redirects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

**Q57.** How does `forward()` pass a `month` value so the target action can receive it as an `int $month` argument?  <small>_(medium · code)_</small>

- A. $this->forward(ReportController::class.'::monthly', ['month' => 3]); — passed via the sub-request attributes
- B. $this->forward('...', [], ['month' => 3]); — via the query bag
- C. $this->forward('...')->with('month', 3);
- D. $this->redirectToRoute('...', ['month' => 3]);

??? success "Answer Q57"
    **A**

    The second argument to forward() becomes the sub-request's attributes (the $path array), which the argument resolver then maps to the target's named parameters — not through query.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#forwarding-to-another-controller)

**Q58.** Two controllers need the same 'latest news' logic. Which reuse approach is usually preferable to forwarding?  <small>_(medium · scenario)_</small>

- A. Extract the logic into a shared service and inject it into both controllers
- B. forward() from one controller to the other
- C. redirect() between the two controllers
- D. Duplicate the code in both controllers

??? success "Answer Q58"
    **A**

    Forwarding runs a full kernel pass and couples controllers. A shared service reuses just the logic without routing/events/resolver overhead. Forward when you need another controller's whole Response embedded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#forwarding-to-another-controller)

**Q59.** How do you correctly produce a 404 from a controller?  <small>_(medium · single)_</small>

- A. throw $this->createNotFoundException()
- B. return new Response('', 404)
- C. return $this->notFound()

??? success "Answer Q59"
    **A**

    createNotFoundException() returns a NotFoundHttpException you must throw; the kernel then renders the error page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#managing-errors-and-404-pages)

**Q60.** A controller throws a plain \RuntimeException. What status code results?  <small>_(medium · single)_</small>

- A. 500
- B. 400
- C. 404

??? success "Answer Q60"
    **A**

    Only exceptions implementing HttpExceptionInterface set a specific status; any other exception becomes a 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q61.** Where do you place a custom production 404 template?  <small>_(medium · config)_</small>

- A. templates/bundles/TwigBundle/Exception/error404.html.twig
- B. public/404.html
- C. config/errors.yaml

??? success "Answer Q61"
    **A**

    The Twig error renderer looks up per-status templates in that path in the prod environment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q62.** Which one-liner raises a 404 when a repository lookup returns null?  <small>_(medium · code)_</small>

- A. $article = $repo->findOneBySlug($slug) ?? throw $this->createNotFoundException();
- B. $article = $repo->findOneBySlug($slug) ?: $this->createNotFoundException();
- C. $article = $repo->findOneBySlug($slug) ?? $this->createNotFoundException();
- D. $article = $repo->findOneBySlug($slug) or abort(404);

??? success "Answer Q62"
    **A**

    The throw expression (PHP 8) combines with `??` so a null lookup throws the 404. Without `throw` the exception is merely assigned/discarded; `?:` and `abort()` are wrong (abort() is not a Symfony helper).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q63.** createNotFoundException() aborts the action as soon as it is called. True or false?  <small>_(medium · trap)_</small>

- A. False
- B. True

??? success "Answer Q63"
    **A**

    It only returns a NotFoundHttpException object; nothing happens until you `throw` it. Treating it as self-aborting is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q64.** With #[MapUploadedFile] and a failing File constraint, what happens?  <small>_(medium · single)_</small>

- A. An HTTP exception is thrown before the action body runs
- B. The argument is set to null
- C. A flash message is added

??? success "Answer Q64"
    **A**

    The resolver validates the upload and aborts with an HTTP error when a constraint fails, so the body never executes with invalid input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q65.** Which signature binds and validates a PDF upload straight into a controller argument?  <small>_(medium · code)_</small>

- A. #[MapUploadedFile([new File(maxSize: '2M', mimeTypes: ['application/pdf'])])] UploadedFile $doc
- B. #[MapRequestPayload] UploadedFile $doc
- C. #[MapQueryParameter] UploadedFile $doc
- D. #[CurrentUser] UploadedFile $doc

??? success "Answer Q65"
    **A**

    #[MapUploadedFile] (handled by RequestPayloadValueResolver) binds the UploadedFile and applies inline File/Image constraints, throwing an HTTP exception on failure. The other attributes target payloads/query/user.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q66.** Why must uploaded files be stored outside the web root (or with execution disabled)?  <small>_(medium · trap)_</small>

- A. An uploaded .php in a served directory can be executed — remote code execution
- B. The web root has a strict file-count limit
- C. Symfony refuses to move files into public/
- D. Files in the web root are automatically deleted on cache clear

??? success "Answer Q66"
    **A**

    A script (e.g. .php) saved into a publicly served directory could be requested and executed, yielding RCE. Store uploads outside public/ or disable script execution there, and always use a safe generated name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

**Q67.** RedirectController configured with permanent: true returns which status?  <small>_(medium · config)_</small>

- A. 301 (or 308 when keepRequestMethod is true)
- B. 302
- C. 410

??? success "Answer Q67"
    **A**

    permanent selects the permanent status code; combined with keepRequestMethod it becomes 308 to preserve the method.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-to-urls-and-routes-directly-from-a-route)

**Q68.** What status does RedirectController return when the target route/path is empty?  <small>_(medium · trap)_</small>

- A. 410 Gone
- B. 404 Not Found
- C. 302 Found to /

??? success "Answer Q68"
    **A**

    An empty target signals the resource is permanently gone, so the controller responds 410.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

**Q69.** Which route config serves `/terms` from a template with a one-day shared cache and no PHP class?  <small>_(medium · config)_</small>

- A. controller: TemplateController with defaults { template: 'static/terms.html.twig', sharedAge: 86400 }
- B. controller: TemplateController with defaults { path: '/terms', ttl: 86400 }
- C. controller: RedirectController with defaults { template: 'static/terms.html.twig' }
- D. controller: CacheController with defaults { template: 'static/terms.html.twig' }

??? success "Answer Q69"
    **A**

    TemplateController accepts template plus optional maxAge/sharedAge/private to set HTTP cache headers. sharedAge sets the shared-cache TTL (s-maxage). RedirectController/CacheController are wrong for rendering.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#rendering-a-template-directly-from-a-route)

**Q70.** A route sets `controller: ...\\RedirectController` (class only) and the request errors. What is missing?  <small>_(medium · trap)_</small>

- A. RedirectController is not invokable; reference ::redirectAction (route) or ::urlRedirectAction (URL)
- B. It needs a permanent: true default to work
- C. RedirectController must be registered manually as a service
- D. You must add an __invoke default to the route

??? success "Answer Q70"
    **A**

    Unlike TemplateController, RedirectController has no __invoke; you must pick the matching action — redirectAction for a route target, urlRedirectAction for a path/URL target.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

**Q71.** A RedirectController route sets `permanent: true` and `keepRequestMethod: true`. What status does it return?  <small>_(medium · config)_</small>

- A. 308 Permanent Redirect (permanent + method-preserving)
- B. 301 Moved Permanently
- C. 307 Temporary Redirect
- D. 302 Found

??? success "Answer Q71"
    **A**

    permanent alone gives 301; adding keepRequestMethod upgrades it to 308 so the HTTP method (e.g. POST) is preserved across the permanent redirect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-to-urls-and-routes-directly-from-a-route)

**Q72.** Which interface does a custom value resolver implement in Symfony 8?  <small>_(medium · single)_</small>

- A. ValueResolverInterface (resolve(Request, ArgumentMetadata): iterable)
- B. ArgumentValueResolverInterface (supports() + resolve())
- C. ControllerResolverInterface

??? success "Answer Q72"
    **A**

    The split supports()/resolve() interface was removed; resolve() now returns an iterable and yielding nothing declines the argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q73.** In a custom resolver, an argument's type does not match. What should `resolve()` do to decline it correctly?  <small>_(medium · code)_</small>

- A. return []; (yield nothing) so the next resolver handles it
- B. return null; to indicate no value
- C. return false; to skip the argument
- D. throw new UnsupportedArgumentException();

??? success "Answer Q73"
    **A**

    resolve() is typed `: iterable`, so `return null` is a TypeError and `return false` is invalid. Decline by returning an empty array (or a generator that never yields).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q74.** Which tag registers a resolver in the ordered chain, and how is its order controlled?  <small>_(medium · config)_</small>

- A. controller.argument_value_resolver with an optional priority (higher runs first); autoconfigure adds it automatically
- B. controller.targeted_value_resolver, ordered alphabetically
- C. kernel.value_resolver, ordered by registration time
- D. container.resolver with a weight attribute

??? success "Answer Q74"
    **A**

    Chain resolvers are tagged controller.argument_value_resolver; a higher priority runs earlier. Autoconfiguration tags implementing classes; set an explicit priority only when ordering matters (targeted resolvers use the controller.targeted_value_resolver tag instead).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q75.** An action needs the authenticated user injected as an argument (not via $this->getUser()). Which attribute does this?  <small>_(medium · scenario)_</small>

- A. #[CurrentUser] User $user (resolved by UserValueResolver from security)
- B. #[MapRequestPayload] User $user
- C. #[MapEntity] User $user
- D. #[Autowire] User $user

??? success "Answer Q75"
    **A**

    #[CurrentUser] injects the authenticated user via the security UserValueResolver. MapRequestPayload builds a DTO from the body, MapEntity is Doctrine (out of scope), and Autowire is for services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q76.** Is #[MapEntity] a core HttpKernel value resolver you should study for this syllabus area?  <small>_(medium · trap)_</small>

- A. No — #[MapEntity] is a DoctrineBundle feature, not a core HttpKernel resolver
- B. Yes — it is one of the built-in HttpKernel resolvers at priority 100
- C. Yes — it is a targeted core resolver like MapRequestPayload
- D. No — because it was removed in Symfony 8

??? success "Answer Q76"
    **A**

    #[MapEntity] belongs to DoctrineBundle and is out of scope for the core HttpKernel resolver chain. The core built-ins are Request/Session (120), BackedEnum/Uid/DateTime/RequestAttribute (100), plus the targeted mapping attributes and #[CurrentUser].

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q77.** How does AbstractController obtain its helper services?  <small>_(hard · internals)_</small>

- A. Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()
- B. Through constructor injection of each service
- C. The full application container is injected

??? success "Answer Q77"
    **A**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

**Q78.** For the URL `/search` (no `?page=`), what does `(int) $request->query->get('page')` evaluate to, and what is the safer call?  <small>_(hard · debug)_</small>

- A. 0, because get() returns null which casts to 0; use getInt('page', 1) instead
- B. 1, because get() defaults to 1
- C. null, and the cast is skipped
- D. It throws because 'page' is missing

??? success "Answer Q78"
    **A**

    InputBag::get() returns null for a missing key (default default is null), and (int) null is 0 — rarely the intended fallback. getInt('page', 1) coerces and guarantees the type with an explicit default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

**Q79.** When does a StreamedResponse produce its body?  <small>_(hard · internals)_</small>

- A. During send(), by invoking its callback
- B. When it is constructed
- C. During the kernel.controller event

??? success "Answer Q79"
    **A**

    The callback runs at send time and streams output; you cannot change headers once streaming has begun.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#streaming-a-response)

**Q80.** Inside a StreamedResponse callback, code echoes rows and then calls `$response->headers->set('Content-Type', 'text/csv')`. What is wrong?  <small>_(hard · trap)_</small>

- A. Headers cannot be changed after output has started; set Content-Type before returning the response
- B. StreamedResponse ignores Content-Type entirely
- C. The callback must return the header array
- D. You must use JsonResponse for CSV

??? success "Answer Q80"
    **A**

    The callback runs at send time; once bytes are flushed the headers are already sent, so header changes are ineffective. Set headers on the StreamedResponse before returning it from the action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#streaming-a-response)

**Q81.** When does a lazy Symfony session actually start (session_start + Set-Cookie)?  <small>_(hard · internals)_</small>

- A. Only when the session is first read or written
- B. On every request automatically
- C. When the kernel boots

??? success "Answer Q81"
    **A**

    Lazy sessions avoid emitting a session cookie for requests that never touch the session, preserving cacheability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

**Q82.** What is a caching side effect of touching the session on a public page?  <small>_(hard · single)_</small>

- A. A Set-Cookie header makes the response uncacheable by shared proxies
- B. Nothing; sessions never affect HTTP caching
- C. It disables Twig template caching

??? success "Answer Q82"
    **A**

    Shared caches must not store responses carrying a per-user Set-Cookie, so touching the session prevents shared caching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q83.** During a forwarded sub-request, what does Request::isMainRequest() return?  <small>_(hard · internals)_</small>

- A. false
- B. true
- C. null

??? success "Answer Q83"
    **A**

    The sub-request is dispatched with HttpKernelInterface::SUB_REQUEST, so isMainRequest() is false and some listeners (e.g. the firewall) skip.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q84.** Which constant does forward() pass to HttpKernel::handle(), and what is a consequence for the security firewall?  <small>_(hard · internals)_</small>

- A. HttpKernelInterface::SUB_REQUEST — the firewall does not re-authenticate (isMainRequest() is false)
- B. HttpKernelInterface::MASTER_REQUEST — the firewall re-runs
- C. HttpKernelInterface::MAIN_REQUEST — a fresh security context is built
- D. HttpKernelInterface::ASYNC_REQUEST — the request is queued

??? success "Answer Q84"
    **A**

    Sub-requests are dispatched with SUB_REQUEST (the old MASTER_REQUEST constant was removed; MAIN_REQUEST is used for the main request). Because isMainRequest() is false, listeners like the firewall skip re-authentication.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernelInterface.php)

**Q85.** Which kernel event lets a listener turn an exception into a Response?  <small>_(hard · internals)_</small>

- A. kernel.exception (ExceptionEvent)
- B. kernel.view
- C. kernel.terminate

??? success "Answer Q85"
    **A**

    ExceptionEvent listeners can call setResponse(); otherwise the error controller renders the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q86.** `$this->createNotFoundException('Missing');` is written on its own line, then the action continues and fatals with 'member function on null'. Why?  <small>_(hard · debug)_</small>

- A. createNotFoundException() only builds and returns the exception; without throw the action keeps running with the null entity
- B. createNotFoundException() logs the error but never stops execution by design of the 404 flow
- C. The exception is thrown but caught silently by the kernel
- D. You must return the exception, not throw it

??? success "Answer Q86"
    **A**

    The helper is a factory: it returns a NotFoundHttpException and does not abort. You must `throw` it. Written alone, the exception is created, discarded, and execution continues on the null value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q87.** An API must return problem+json error bodies for every HttpException. What is the cleanest app-wide approach?  <small>_(hard · scenario)_</small>

- A. A kernel.exception listener (or a custom framework.error_controller) that maps exceptions to a JSON Response
- B. Wrap every action body in try/catch and build JSON manually
- C. Return new Response('', 404) from each action
- D. Override every errorXXX.html.twig template

??? success "Answer Q87"
    **A**

    A single kernel.exception listener calling setResponse(), or a custom error_controller, centralises error rendering with content negotiation — far cleaner than per-action try/catch or per-status Twig templates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q88.** A user uploads a file larger than `post_max_size` and the action crashes on a null `$request->files->get('avatar')`. What is the underlying cause?  <small>_(hard · debug)_</small>

- A. Exceeding post_max_size can yield an empty files bag (no exception), so the get() returns null — always null-check
- B. move() threw a FileException that was swallowed
- C. getMimeType() returns null for large files
- D. Symfony automatically rejects the request with a 413

??? success "Answer Q88"
    **A**

    When post_max_size is exceeded, PHP may discard the POST data, leaving an empty files bag rather than raising an exception. Guard the result with an instanceof UploadedFile / isValid() check before using it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

**Q89.** Which resolvers have the highest default priority (120) in Symfony 8?  <small>_(hard · internals)_</small>

- A. RequestValueResolver and SessionValueResolver
- B. DefaultValueResolver and VariadicValueResolver
- C. RequestAttributeValueResolver and BackedEnumValueResolver

??? success "Answer Q89"
    **A**

    Request and Session resolvers run first at priority 120; the attribute, enum, uid and datetime resolvers sit at 100.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Resources/config/web.php)

**Q90.** A #[MapRequestPayload] argument fails validation. Which status is thrown?  <small>_(hard · single)_</small>

- A. 422 Unprocessable Entity (400 if the body itself is malformed)
- B. 500 Internal Server Error
- C. 200 with a null argument

??? success "Answer Q90"
    **A**

    RequestPayloadValueResolver deserializes then validates; validation errors throw UnprocessableEntityHttpException (422).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html#mapping-the-whole-request-payload)

**Q91.** How do the #[MapRequestPayload]/#[MapQueryParameter] resolvers get activated?  <small>_(hard · internals)_</small>

- A. They are targeted resolvers that run only when their attribute is present on the argument
- B. They always run first in the priority chain
- C. They require manual registration in services.yaml

??? success "Answer Q91"
    **A**

    These resolvers carry the controller.targeted_value_resolver tag and are invoked only for arguments bearing the matching attribute.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q92.** In a resolver, what is the difference between yielding nothing and `yield null`?  <small>_(hard · trap)_</small>

- A. Yielding nothing declines (next resolver runs); yield null binds a real null value to a nullable parameter
- B. They are identical — both bind null
- C. yield null declines; yielding nothing binds null
- D. Both throw because null is not iterable

??? success "Answer Q92"
    **A**

    'Yields nothing' means 'not my argument' and passes control on; 'yield null' is a deliberate null bound to the parameter. Confusing them is the classic resolver bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q93.** Which resolvers/attributes are targeted (activated only by their attribute), not part of the priority chain? (choose 3)  <small>_(hard · multiple)_</small>

- A. #[MapRequestPayload] / #[MapQueryString] (RequestPayloadValueResolver)
- B. #[MapQueryParameter] (QueryParameterValueResolver)
- C. #[MapUploadedFile] (RequestPayloadValueResolver)
- D. RequestValueResolver (Request type-hint)

??? success "Answer Q93"
    **A, B, C**

    MapRequestPayload/MapQueryString, MapQueryParameter, MapUploadedFile (and #[CurrentUser]) are targeted resolvers, run only when the attribute is present. RequestValueResolver is a priority-120 chain resolver, not targeted.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

**Q94.** A resolver copied from an old project implements `ArgumentValueResolverInterface` with supports()+resolve() and no longer works in Symfony 8. Why?  <small>_(hard · debug)_</small>

- A. ArgumentValueResolverInterface was removed; implement ValueResolverInterface with a single resolve(): iterable
- B. supports() must now return an iterable
- C. The resolver just needs a higher priority
- D. resolve() must be renamed to __invoke()

??? success "Answer Q94"
    **A**

    The split supports()/resolve() interface no longer exists in Symfony 8. Use ValueResolverInterface::resolve(Request, ArgumentMetadata): iterable and decline by yielding nothing instead of a supports() check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

---

<small>Back to [Chapter Exams](index.md) · [Controllers](../controllers/index.md)</small>
