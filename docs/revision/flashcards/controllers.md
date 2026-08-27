# Flashcards — Controllers

94 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

??? question "1. How is an invokable single-action controller referenced in the `_controller` attribute? (choose one)"
    **✅ The fully-qualified class name only (Symfony calls __invoke)**

    For an invokable controller you reference only the class; the ControllerResolver detects the __invoke() method automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "2. Is the `Action` method suffix required for controller actions in Symfony 8?"
    **✅ No — it is a legacy convention with no meaning under attribute routing**

    Attribute routing binds a specific method explicitly, so the Action suffix is purely historical and can be dropped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "3. What visibility must a controller action method have to be invoked by the kernel?"
    **✅ public**

    The kernel invokes the controller callable externally, so the method must be public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "4. Which statement best defines a Symfony controller?"
    **✅ Any PHP callable that returns a Response**

    A controller is any callable (method, invokable object, closure) the kernel runs to produce a Response; extending AbstractController is optional.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "5. A route is declared as `#[Route('/', name: 'home')]` on the class `App\Controller\HomeController`, which defines a `public function __invoke(): Response`. Which YAML `controller:` value targets it correctly?"
    **✅ controller: App\Controller\HomeController**

    For an invokable controller the `_controller` value is the class name alone; the resolver detects `__invoke()`. Adding `::__invoke` also works but is not idiomatic, and `#invoke` / a made-up service id are invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "6. Which of these are valid `_controller` formats the ControllerResolver accepts? (choose 3)"
    **✅ App\Controller\ProductController::show (class + method) ; App\Controller\HomepageController (invokable class) ; service_id::method or service_id alone**

    The resolver normalises `Class::method`, an invokable `Class`, a `service_id::method`/`service_id`, or a closure into a callable. The `Class#method` syntax is not a recognised format.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/ControllerResolver.php)

??? question "7. A controller must extend `AbstractController` to be usable in Symfony 8. True or false?"
    **✅ False**

    Extending `AbstractController` is optional convenience. A controller is any callable returning a Response; a plain invokable class with no base class is perfectly valid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "8. How does AbstractController obtain its helper services?"
    **✅ Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

??? question "9. What does `$this->container` hold inside an AbstractController?"
    **✅ Only the subscribed services (a restricted service locator)**

    The injected locator exposes exactly the services returned by getSubscribedServices(), not the whole container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

??? question "10. What happens if you call `$this->render()` without Twig installed?"
    **✅ A clear LogicException telling you Twig is required**

    The twig service is subscribed with the optional '?' prefix, so the helper guards its absence with a descriptive LogicException.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/AbstractController.php)

??? question "11. When overriding getSubscribedServices() to add a service, what must you do to keep the built-in helpers?"
    **✅ Spread parent::getSubscribedServices() into the returned array**

    Returning only your service replaces the list; merge the parent's subscriptions so render/getUser/etc. still resolve.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#the-base-controller-class-services)

??? question "12. You extend AbstractController and override getSubscribedServices() to add a `ReportGenerator`. Which body keeps `render()`, `getUser()`, etc. working?"
    **✅ return [...parent::getSubscribedServices(), ReportGenerator::class];**

    The subscription list fully replaces the inherited one, so you must spread `parent::getSubscribedServices()` alongside your own entry. Returning only your service drops router/twig/security and breaks every helper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

??? question "13. In getSubscribedServices(), what does prefixing a service with `?` (e.g. `'?'.Environment::class`) mean?"
    **✅ The service is optional; if absent the locator returns null instead of failing to compile**

    The `?` marks the subscription optional, letting the controller boot even when (say) Twig or the form factory is not installed; the helper then throws a clear LogicException rather than a container error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

??? question "14. A developer fetches an application service with `$this->container->get(InvoiceMailer::class)` inside a controller and gets a 'service not found' error. What is the correct fix?"
    **✅ Inject InvoiceMailer via the constructor — $this->container only holds subscribed helper services**

    `$this->container` is the restricted subscriber locator; it only exposes the framework helper services, not your domain services. Inject your own dependencies through the constructor instead of using the locator as a service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#the-base-controller-class-services)

??? question "15. Which AbstractController helpers directly return a Response (or subclass)? (choose 3)"
    **✅ render() → Response ; json() → JsonResponse ; redirectToRoute() → RedirectResponse**

    render/json/redirectToRoute (and file/stream/forward) return a Response or subclass. createNotFoundException() returns a NotFoundHttpException you must throw — it is not a Response and does not abort on its own.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "16. On a public (no-firewall) route, `return new Response($this->getUser()->getEmail());` fatals with 'Call to a member function getEmail() on null'. Why?"
    **✅ getUser() returns ?UserInterface and is null when no one is authenticated**

    getUser() reads security.token_storage; with no authenticated token it returns null. Guard with denyAccessUnlessGranted()/#[IsGranted] first, or read defensively with `$this->getUser()?->getEmail()`.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/AbstractController.php)

??? question "17. Which value resolver supplies a `Request` type-hinted controller argument?"
    **✅ RequestValueResolver**

    RequestValueResolver (priority 120) injects the current Request; RequestAttributeValueResolver handles named route parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "18. In which parameter bag do matched route parameters appear?"
    **✅ $request->attributes**

    The router writes matched parameters into the attributes bag; query is GET data and request is the POST body.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "19. How should a service (not a controller) access the current Request?"
    **✅ Inject RequestStack and call getCurrentRequest()**

    The Request is request-scoped and cannot be injected directly; inject the RequestStack service instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/request.html)

??? question "20. For the URL `/search` (no `?page=`), what does `(int) $request->query->get('page')` evaluate to, and what is the safer call?"
    **✅ 0, because get() returns null which casts to 0; use getInt('page', 1) instead**

    InputBag::get() returns null for a missing key (default default is null), and (int) null is 0 — rarely the intended fallback. getInt('page', 1) coerces and guarantees the type with an explicit default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "21. What does the `$request->request` bag actually contain?"
    **✅ The POST body parameters ($_POST)**

    Despite the name, `$request->request` is the InputBag of POST body fields, not 'the request object'. Query lives in `$request->query`, route params in `$request->attributes`.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "22. `$request->getContent()` is called on a JSON API request. What does it return?"
    **✅ The raw request body as a string — it is not JSON-decoded**

    getContent() returns the raw body; it does not decode JSON. Use #[MapRequestPayload] (serializer + validator) or json_decode() yourself to get a structured value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "23. The `Request` object can be autowired directly into a service constructor. True or false?"
    **✅ False**

    The Request is request-scoped and created per HTTP call, so it is not an autowireable service. Inject RequestStack and call getCurrentRequest().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/request.html)

??? question "24. What must a controller ultimately produce?"
    **✅ A Response object (or a value converted to one by a kernel.view listener)**

    If a controller returns a non-Response, the kernel fires ViewEvent; if no listener produces a Response a LogicException is thrown.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "25. When does a StreamedResponse produce its body?"
    **✅ During send(), by invoking its callback**

    The callback runs at send time and streams output; you cannot change headers once streaming has begun.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#streaming-a-response)

??? question "26. Which response class best serves a resumable (range-request) file download?"
    **✅ BinaryFileResponse**

    BinaryFileResponse supports HTTP range requests and X-Sendfile/X-Accel offloading for efficient downloads.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

??? question "27. An action does `return ['id' => 1, 'name' => 'Ada'];` expecting Symfony to auto-serialize it to JSON, but the request fails. Why?"
    **✅ Symfony does not auto-serialize arrays by default; with no kernel.view listener the kernel throws a LogicException**

    A non-Response return fires ViewEvent; without a listener that builds a Response, the kernel throws 'The controller must return a Response'. Return $this->json($data) explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html)

??? question "28. Inside a StreamedResponse callback, code echoes rows and then calls `$response->headers->set('Content-Type', 'text/csv')`. What is wrong?"
    **✅ Headers cannot be changed after output has started; set Content-Type before returning the response**

    The callback runs at send time; once bytes are flushed the headers are already sent, so header changes are ineffective. Set headers on the StreamedResponse before returning it from the action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#streaming-a-response)

??? question "29. You already hold a valid JSON string. Which avoids double-encoding it in a JsonResponse?"
    **✅ JsonResponse::fromJsonString($json)**

    new JsonResponse($json) / $this->json($json) would JSON-encode the string again (double-encoding). fromJsonString() sets the body verbatim and the application/json Content-Type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "30. Where does a controller read incoming cookies from?"
    **✅ $request->cookies**

    The cookies ParameterBag wraps $_COOKIE; responses set cookies via $response->headers->setCookie().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "31. A cookie sent with SameSite=None also requires which attribute?"
    **✅ Secure=true**

    Modern browsers reject SameSite=None cookies unless they are marked Secure (HTTPS-only).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#setting-cookies)

??? question "32. Why might clearCookie('token') fail to delete the cookie?"
    **✅ The path/domain do not match those used when the cookie was set**

    Deletion sends an expired Set-Cookie scoped by path/domain; a mismatch targets a different cookie and leaves the original intact.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "33. `Cookie::create('t','v')->withSameSite(Cookie::SAMESITE_NONE)` is set without calling `withSecure(true)`. What is the effect in modern browsers?"
    **✅ Browsers reject the cookie because SameSite=None requires Secure**

    SameSite=None mandates the Secure attribute; without it the browser drops the cookie. Chain ->withSecure(true) so it is sent only over HTTPS.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#setting-cookies)

??? question "34. In Symfony's Cookie value object, `httpOnly` defaults to true. True or false?"
    **✅ True**

    Cookie defaults are security-first: httpOnly=true (hidden from JS, mitigating XSS token theft) and sameSite='lax'. JS-readable cookies must opt out explicitly with withHttpOnly(false).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Cookie.php)

??? question "35. An action sets a `theme` cookie on the response, then in the same action reads `$request->cookies->get('theme')` and gets the old value. Why?"
    **✅ A cookie set on the response is only sent to the browser and readable on subsequent requests**

    Response cookies go out as Set-Cookie headers; the request's cookies bag reflects what the browser already sent. A newly set cookie is only visible on the next request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#setting-cookies)

??? question "36. What is the recommended way for a service to access the session?"
    **✅ Inject RequestStack and call getSession()**

    The session is request-scoped; RequestStack::getSession() is the stable entry point in services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "37. When does a lazy Symfony session actually start (session_start + Set-Cookie)?"
    **✅ Only when the session is first read or written**

    Lazy sessions avoid emitting a session cookie for requests that never touch the session, preserving cacheability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "38. Which method regenerates the session id after login to prevent session fixation?"
    **✅ migrate()**

    migrate() issues a new session id while keeping data; invalidate() also wipes data. Symfony authenticators call migrate() on login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "39. What is a caching side effect of touching the session on a public page?"
    **✅ A Set-Cookie header makes the response uncacheable by shared proxies**

    Shared caches must not store responses carrying a per-user Set-Cookie, so touching the session prevents shared caching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "40. A console command injects RequestStack and calls `getSession()`, which throws SessionNotFoundException. What is the cause and fix?"
    **✅ There is no current request in the CLI; guard with getCurrentRequest() and hasSession() before reading**

    getSession() throws SessionNotFoundException (it does not return null) when called outside a request or on a request with no session. Guard the request first: check getCurrentRequest() and hasSession().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "41. Why is injecting `SessionInterface` directly into a service constructor discouraged in Symfony 8?"
    **✅ The session is request-scoped; inject RequestStack and call getSession() so it resolves per request**

    Directly autowiring the request-scoped session into a long-lived service is discouraged/removed; RequestStack::getSession() is the stable entry point. You can still type-hint SessionInterface on a controller action (resolved by SessionValueResolver, priority 120).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "42. Merely type-hinting SessionInterface on an action starts the session. True or false?"
    **✅ False**

    Sessions are lazy: SessionValueResolver injects the session object, but session_start() and the Set-Cookie header only fire on the first read or write. Merely receiving the session does not start it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/session.html)

??? question "43. What happens the first time you read a flash message (get/all or app.flashes)?"
    **✅ It is returned and removed (consumed)**

    Reading consumes flashes; use peek()/peekAll() to read without removing them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#flash-messages)

??? question "44. `$this->addFlash('notice', 'Saved')` is shorthand for which call?"
    **✅ getSession()->getFlashBag()->add('notice', 'Saved')**

    addFlash() is an AbstractController convenience over the session flash bag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#flash-messages)

??? question "45. Why are flash messages typically paired with a redirect?"
    **✅ They display on the next (GET) request, matching the Post/Redirect/Get pattern**

    Flashes are built to survive exactly one redirect and be shown on the following request, then discarded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#flash-messages)

??? question "46. A controller reads `app.session.flashbag.get('success')` for logging, then the Twig template shows no flash. What happened?"
    **✅ get() consumed (drained) the messages, so nothing remains for Twig; use peek() to read without consuming**

    get()/all() consume the flash bag. Reading in the controller drains the messages before Twig can show them. Use peek()/peekAll() when you must read without removing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#flash-messages)

??? question "47. Which method reads flash messages WITHOUT consuming them?"
    **✅ peek() / peekAll()**

    peek()/peekAll() return messages while leaving them in the bag. get()/all() both return and remove. There are no read()/keep() methods on FlashBag.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Session/Flash/FlashBag.php)

??? question "48. Which Twig loop renders all flash types, consuming them once?"
    **✅ {% for label, messages in app.flashes %}{% for m in messages %}{{ m }}{% endfor %}{% endfor %}**

    app.flashes yields a map of type => messages; iterating it calls all() under the hood, which consumes the bag so each message shows exactly once.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#flash-messages)

??? question "49. What is the default HTTP status code of redirectToRoute()?"
    **✅ 302**

    RedirectResponse defaults to 302 Found; pass a status argument to change it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "50. Which redirect status codes preserve the original HTTP method and body?"
    **✅ 307 and 308**

    307/308 must not change the request method; 303 always forces GET and 301/302 may downgrade to GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "51. What is the difference between redirect() and redirectToRoute()?"
    **✅ redirect() takes a URL; redirectToRoute() takes a route name and parameters**

    redirect() is URL-based; redirectToRoute() builds the URL from the router. Both return a RedirectResponse (default 302).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "52. After creating a resource in a POST action, you want the browser to issue a GET to the show page. Which call is correct?"
    **✅ return $this->redirectToRoute('resource_show', ['id' => $id], 303);**

    303 See Other forces the follow-up request to GET, the strict form of Post/Redirect/Get. 307 would preserve POST; forward() is internal (no URL change); redirect() takes a URL, not a route name + params.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "53. A checkout POST persists an order and redirects to the confirmation page to avoid duplicate submissions on refresh. Which status best fits?"
    **✅ 302 (or the stricter 303) — a temporary, non-cached redirect for PRG**

    PRG needs a temporary redirect that ends on a GET. 302 (default) or 303 are correct; 301/308 are cached (wrong and hard to undo), and 307 would replay the POST.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "54. Why is accidentally using 301 (or 308) for a temporary redirect dangerous?"
    **✅ 301/308 are cached by browsers, so the redirect sticks and is hard to undo**

    301 and 308 signal a permanent move and are cached by browsers; if used by mistake the client keeps redirecting even after you fix the server. Use 302/303 for temporary redirects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "55. `redirect()` accepts a route name as its first argument. True or false?"
    **✅ False**

    redirect() takes a URL (string). To redirect by route name (plus params), use redirectToRoute(), which builds the URL via the router.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "56. What does AbstractController::forward() do?"
    **✅ Runs another controller in a sub-request and returns its Response, without a new client request**

    forward() dispatches a sub-request through the kernel; the browser URL does not change and no 3xx is sent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#forwarding-to-another-controller)

??? question "57. During a forwarded sub-request, what does Request::isMainRequest() return?"
    **✅ false**

    The sub-request is dispatched with HttpKernelInterface::SUB_REQUEST, so isMainRequest() is false and some listeners (e.g. the firewall) skip.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html)

??? question "58. After a forward(), what does the user's address bar show?"
    **✅ The original URL, unchanged**

    Forwarding is server-internal within the same request, so no new client navigation occurs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#forwarding-to-another-controller)

??? question "59. How does `forward()` pass a `month` value so the target action can receive it as an `int $month` argument?"
    **✅ $this->forward(ReportController::class.'::monthly', ['month' => 3]); — passed via the sub-request attributes**

    The second argument to forward() becomes the sub-request's attributes (the $path array), which the argument resolver then maps to the target's named parameters — not through query.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#forwarding-to-another-controller)

??? question "60. Two controllers need the same 'latest news' logic. Which reuse approach is usually preferable to forwarding?"
    **✅ Extract the logic into a shared service and inject it into both controllers**

    Forwarding runs a full kernel pass and couples controllers. A shared service reuses just the logic without routing/events/resolver overhead. Forward when you need another controller's whole Response embedded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#forwarding-to-another-controller)

??? question "61. Which constant does forward() pass to HttpKernel::handle(), and what is a consequence for the security firewall?"
    **✅ HttpKernelInterface::SUB_REQUEST — the firewall does not re-authenticate (isMainRequest() is false)**

    Sub-requests are dispatched with SUB_REQUEST (the old MASTER_REQUEST constant was removed; MAIN_REQUEST is used for the main request). Because isMainRequest() is false, listeners like the firewall skip re-authentication.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernelInterface.php)

??? question "62. How do you correctly produce a 404 from a controller?"
    **✅ throw $this->createNotFoundException()**

    createNotFoundException() returns a NotFoundHttpException you must throw; the kernel then renders the error page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#managing-errors-and-404-pages)

??? question "63. A controller throws a plain \RuntimeException. What status code results?"
    **✅ 500**

    Only exceptions implementing HttpExceptionInterface set a specific status; any other exception becomes a 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

??? question "64. Where do you place a custom production 404 template?"
    **✅ templates/bundles/TwigBundle/Exception/error404.html.twig**

    The Twig error renderer looks up per-status templates in that path in the prod environment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

??? question "65. Which kernel event lets a listener turn an exception into a Response?"
    **✅ kernel.exception (ExceptionEvent)**

    ExceptionEvent listeners can call setResponse(); otherwise the error controller renders the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/events.html#kernel-exception)

??? question "66. `$this->createNotFoundException('Missing');` is written on its own line, then the action continues and fatals with 'member function on null'. Why?"
    **✅ createNotFoundException() only builds and returns the exception; without throw the action keeps running with the null entity**

    The helper is a factory: it returns a NotFoundHttpException and does not abort. You must `throw` it. Written alone, the exception is created, discarded, and execution continues on the null value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

??? question "67. Which one-liner raises a 404 when a repository lookup returns null?"
    **✅ $article = $repo->findOneBySlug($slug) ?? throw $this->createNotFoundException();**

    The throw expression (PHP 8) combines with `??` so a null lookup throws the 404. Without `throw` the exception is merely assigned/discarded; `?:` and `abort()` are wrong (abort() is not a Symfony helper).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

??? question "68. createNotFoundException() aborts the action as soon as it is called. True or false?"
    **✅ False**

    It only returns a NotFoundHttpException object; nothing happens until you `throw` it. Treating it as self-aborting is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

??? question "69. An API must return problem+json error bodies for every HttpException. What is the cleanest app-wide approach?"
    **✅ A kernel.exception listener (or a custom framework.error_controller) that maps exceptions to a JSON Response**

    A single kernel.exception listener calling setResponse(), or a custom error_controller, centralises error rendering with content negotiation — far cleaner than per-action try/catch or per-status Twig templates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/error_pages.html)

??? question "70. Which value should you trust to determine an uploaded file's real type?"
    **✅ getMimeType() (content-detected by the guesser)**

    Client-supplied name/MIME are spoofable; getMimeType()/guessExtension() inspect the actual file content.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

??? question "71. What does UploadedFile::move() do when it fails?"
    **✅ Throws a FileException**

    move() throws FileException on failure rather than returning a status value.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

??? question "72. With #[MapUploadedFile] and a failing File constraint, what happens?"
    **✅ An HTTP exception is thrown before the action body runs**

    The resolver validates the upload and aborts with an HTTP error when a constraint fails, so the body never executes with invalid input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "73. A user uploads a file larger than `post_max_size` and the action crashes on a null `$request->files->get('avatar')`. What is the underlying cause?"
    **✅ Exceeding post_max_size can yield an empty files bag (no exception), so the get() returns null — always null-check**

    When post_max_size is exceeded, PHP may discard the POST data, leaving an empty files bag rather than raising an exception. Guard the result with an instanceof UploadedFile / isValid() check before using it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

??? question "74. Which signature binds and validates a PDF upload straight into a controller argument?"
    **✅ #[MapUploadedFile([new File(maxSize: '2M', mimeTypes: ['application/pdf'])])] UploadedFile $doc**

    #[MapUploadedFile] (handled by RequestPayloadValueResolver) binds the UploadedFile and applies inline File/Image constraints, throwing an HTTP exception on failure. The other attributes target payloads/query/user.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "75. Why must uploaded files be stored outside the web root (or with execution disabled)?"
    **✅ An uploaded .php in a served directory can be executed — remote code execution**

    A script (e.g. .php) saved into a publicly served directory could be requested and executed, yielding RCE. Store uploads outside public/ or disable script execution there, and always use a safe generated name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/upload_file.html)

??? question "76. Which built-in controller renders a Twig template purely from route config?"
    **✅ TemplateController**

    TemplateController::__invoke() renders the 'template' default and can set HTTP cache headers, needing no custom class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#rendering-a-template-directly-from-a-route)

??? question "77. RedirectController configured with permanent: true returns which status?"
    **✅ 301 (or 308 when keepRequestMethod is true)**

    permanent selects the permanent status code; combined with keepRequestMethod it becomes 308 to preserve the method.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-to-urls-and-routes-directly-from-a-route)

??? question "78. What status does RedirectController return when the target route/path is empty?"
    **✅ 410 Gone**

    An empty target signals the resource is permanently gone, so the controller responds 410.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

??? question "79. Which route config serves `/terms` from a template with a one-day shared cache and no PHP class?"
    **✅ controller: TemplateController with defaults { template: 'static/terms.html.twig', sharedAge: 86400 }**

    TemplateController accepts template plus optional maxAge/sharedAge/private to set HTTP cache headers. sharedAge sets the shared-cache TTL (s-maxage). RedirectController/CacheController are wrong for rendering.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#rendering-a-template-directly-from-a-route)

??? question "80. A route sets `controller: ...\\RedirectController` (class only) and the request errors. What is missing?"
    **✅ RedirectController is not invokable; reference ::redirectAction (route) or ::urlRedirectAction (URL)**

    Unlike TemplateController, RedirectController has no __invoke; you must pick the matching action — redirectAction for a route target, urlRedirectAction for a path/URL target.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

??? question "81. A RedirectController route sets `permanent: true` and `keepRequestMethod: true`. What status does it return?"
    **✅ 308 Permanent Redirect (permanent + method-preserving)**

    permanent alone gives 301; adding keepRequestMethod upgrades it to 308 so the HTTP method (e.g. POST) is preserved across the permanent redirect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-to-urls-and-routes-directly-from-a-route)

??? question "82. Which interface does a custom value resolver implement in Symfony 8?"
    **✅ ValueResolverInterface (resolve(Request, ArgumentMetadata): iterable)**

    The split supports()/resolve() interface was removed; resolve() now returns an iterable and yielding nothing declines the argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "83. How does a value resolver signal that it does not handle an argument?"
    **✅ It yields nothing (returns an empty iterable)**

    Yielding no value passes the argument to the next resolver in priority order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "84. Which resolvers have the highest default priority (120) in Symfony 8?"
    **✅ RequestValueResolver and SessionValueResolver**

    Request and Session resolvers run first at priority 120; the attribute, enum, uid and datetime resolvers sit at 100.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Resources/config/web.php)

??? question "85. A #[MapRequestPayload] argument fails validation. Which status is thrown?"
    **✅ 422 Unprocessable Entity (400 if the body itself is malformed)**

    RequestPayloadValueResolver deserializes then validates; validation errors throw UnprocessableEntityHttpException (422).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html#mapping-the-whole-request-payload)

??? question "86. How do the #[MapRequestPayload]/#[MapQueryParameter] resolvers get activated?"
    **✅ They are targeted resolvers that run only when their attribute is present on the argument**

    These resolvers carry the controller.targeted_value_resolver tag and are invoked only for arguments bearing the matching attribute.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "87. What binds a single typed query parameter such as ?page=2 to an int argument?"
    **✅ #[MapQueryParameter]**

    #[MapQueryParameter] binds one query value with casting; #[MapQueryString] maps the whole query string into a DTO.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "88. In a custom resolver, an argument's type does not match. What should `resolve()` do to decline it correctly?"
    **✅ return []; (yield nothing) so the next resolver handles it**

    resolve() is typed `: iterable`, so `return null` is a TypeError and `return false` is invalid. Decline by returning an empty array (or a generator that never yields).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "89. In a resolver, what is the difference between yielding nothing and `yield null`?"
    **✅ Yielding nothing declines (next resolver runs); yield null binds a real null value to a nullable parameter**

    'Yields nothing' means 'not my argument' and passes control on; 'yield null' is a deliberate null bound to the parameter. Confusing them is the classic resolver bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "90. Which tag registers a resolver in the ordered chain, and how is its order controlled?"
    **✅ controller.argument_value_resolver with an optional priority (higher runs first); autoconfigure adds it automatically**

    Chain resolvers are tagged controller.argument_value_resolver; a higher priority runs earlier. Autoconfiguration tags implementing classes; set an explicit priority only when ordering matters (targeted resolvers use the controller.targeted_value_resolver tag instead).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "91. Which resolvers/attributes are targeted (activated only by their attribute), not part of the priority chain? (choose 3)"
    **✅ #[MapRequestPayload] / #[MapQueryString] (RequestPayloadValueResolver) ; #[MapQueryParameter] (QueryParameterValueResolver) ; #[MapUploadedFile] (RequestPayloadValueResolver)**

    MapRequestPayload/MapQueryString, MapQueryParameter, MapUploadedFile (and #[CurrentUser]) are targeted resolvers, run only when the attribute is present. RequestValueResolver is a priority-120 chain resolver, not targeted.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "92. An action needs the authenticated user injected as an argument (not via $this->getUser()). Which attribute does this?"
    **✅ #[CurrentUser] User $user (resolved by UserValueResolver from security)**

    #[CurrentUser] injects the authenticated user via the security UserValueResolver. MapRequestPayload builds a DTO from the body, MapEntity is Doctrine (out of scope), and Autowire is for services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "93. A resolver copied from an old project implements `ArgumentValueResolverInterface` with supports()+resolve() and no longer works in Symfony 8. Why?"
    **✅ ArgumentValueResolverInterface was removed; implement ValueResolverInterface with a single resolve(): iterable**

    The split supports()/resolve() interface no longer exists in Symfony 8. Use ValueResolverInterface::resolve(Request, ArgumentMetadata): iterable and decline by yielding nothing instead of a supports() check.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

??? question "94. Is #[MapEntity] a core HttpKernel value resolver you should study for this syllabus area?"
    **✅ No — #[MapEntity] is a DoctrineBundle feature, not a core HttpKernel resolver**

    #[MapEntity] belongs to DoctrineBundle and is out of scope for the core HttpKernel resolver chain. The core built-ins are Request/Session (120), BackedEnum/Uid/DateTime/RequestAttribute (100), plus the targeted mapping attributes and #[CurrentUser].

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller/value_resolver.html)

---

<small>Back to [Flashcards](index.md) · [Controllers](../../controllers/index.md)</small>
