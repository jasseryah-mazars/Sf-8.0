# Flashcards — Controllers

46 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. How is an invokable single-action controller referenced in the `_controller` attribute? (choose one)"
    **✅ The fully-qualified class name only (Symfony calls __invoke)**

    For an invokable controller you reference only the class; the ControllerResolver detects the __invoke() method automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

??? question "2. Is the `Action` method suffix required for controller actions in Symfony 8?"
    **✅ No — it is a legacy convention with no meaning under attribute routing**

    Attribute routing binds a specific method explicitly, so the Action suffix is purely historical and can be dropped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

??? question "3. What visibility must a controller action method have to be invoked by the kernel?"
    **✅ public**

    The kernel invokes the controller callable externally, so the method must be public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

??? question "4. Which statement best defines a Symfony controller?"
    **✅ Any PHP callable that returns a Response**

    A controller is any callable (method, invokable object, closure) the kernel runs to produce a Response; extending AbstractController is optional.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

??? question "5. How does AbstractController obtain its helper services?"
    **✅ Via a lazy service locator injected through setContainer(), driven by getSubscribedServices()**

    AbstractController implements ServiceSubscriberInterface; the compiler builds a per-controller locator containing only the subscribed services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "6. What does `$this->container` hold inside an AbstractController?"
    **✅ Only the subscribed services (a restricted service locator)**

    The injected locator exposes exactly the services returned by getSubscribedServices(), not the whole container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "7. What happens if you call `$this->render()` without Twig installed?"
    **✅ A clear LogicException telling you Twig is required**

    The twig service is subscribed with the optional '?' prefix, so the helper guards its absence with a descriptive LogicException.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/AbstractController.php)

??? question "8. When overriding getSubscribedServices() to add a service, what must you do to keep the built-in helpers?"
    **✅ Spread parent::getSubscribedServices() into the returned array**

    Returning only your service replaces the list; merge the parent's subscriptions so render/getUser/etc. still resolve.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#the-base-controller-class-services)

??? question "9. Which value resolver supplies a `Request` type-hinted controller argument?"
    **✅ RequestValueResolver**

    RequestValueResolver (priority 120) injects the current Request; RequestAttributeValueResolver handles named route parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

??? question "10. In which parameter bag do matched route parameters appear?"
    **✅ $request->attributes**

    The router writes matched parameters into the attributes bag; query is GET data and request is the POST body.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "11. How should a service (not a controller) access the current Request?"
    **✅ Inject RequestStack and call getCurrentRequest()**

    The Request is request-scoped and cannot be injected directly; inject the RequestStack service instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

??? question "12. What must a controller ultimately produce?"
    **✅ A Response object (or a value converted to one by a kernel.view listener)**

    If a controller returns a non-Response, the kernel fires ViewEvent; if no listener produces a Response a LogicException is thrown.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html)

??? question "13. When does a StreamedResponse produce its body?"
    **✅ During send(), by invoking its callback**

    The callback runs at send time and streams output; you cannot change headers once streaming has begun.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#streaming-a-response)

??? question "14. Which response class best serves a resumable (range-request) file download?"
    **✅ BinaryFileResponse**

    BinaryFileResponse supports HTTP range requests and X-Sendfile/X-Accel offloading for efficient downloads.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#serving-files)

??? question "15. Where does a controller read incoming cookies from?"
    **✅ $request->cookies**

    The cookies ParameterBag wraps $_COOKIE; responses set cookies via $response->headers->setCookie().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "16. A cookie sent with SameSite=None also requires which attribute?"
    **✅ Secure=true**

    Modern browsers reject SameSite=None cookies unless they are marked Secure (HTTPS-only).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#setting-cookies)

??? question "17. Why might clearCookie('token') fail to delete the cookie?"
    **✅ The path/domain do not match those used when the cookie was set**

    Deletion sends an expired Set-Cookie scoped by path/domain; a mismatch targets a different cookie and leaves the original intact.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "18. What is the recommended way for a service to access the session?"
    **✅ Inject RequestStack and call getSession()**

    The session is request-scoped; RequestStack::getSession() is the stable entry point in services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

??? question "19. When does a lazy Symfony session actually start (session_start + Set-Cookie)?"
    **✅ Only when the session is first read or written**

    Lazy sessions avoid emitting a session cookie for requests that never touch the session, preserving cacheability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

??? question "20. Which method regenerates the session id after login to prevent session fixation?"
    **✅ migrate()**

    migrate() issues a new session id while keeping data; invalidate() also wipes data. Symfony authenticators call migrate() on login.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/session.html)

??? question "21. What is a caching side effect of touching the session on a public page?"
    **✅ A Set-Cookie header makes the response uncacheable by shared proxies**

    Shared caches must not store responses carrying a per-user Set-Cookie, so touching the session prevents shared caching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

??? question "22. What happens the first time you read a flash message (get/all or app.flashes)?"
    **✅ It is returned and removed (consumed)**

    Reading consumes flashes; use peek()/peekAll() to read without removing them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

??? question "23. `$this->addFlash('notice', 'Saved')` is shorthand for which call?"
    **✅ getSession()->getFlashBag()->add('notice', 'Saved')**

    addFlash() is an AbstractController convenience over the session flash bag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

??? question "24. Why are flash messages typically paired with a redirect?"
    **✅ They display on the next (GET) request, matching the Post/Redirect/Get pattern**

    Flashes are built to survive exactly one redirect and be shown on the following request, then discarded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#flash-messages)

??? question "25. What is the default HTTP status code of redirectToRoute()?"
    **✅ 302**

    RedirectResponse defaults to 302 Found; pass a status argument to change it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

??? question "26. Which redirect status codes preserve the original HTTP method and body?"
    **✅ 307 and 308**

    307/308 must not change the request method; 303 always forces GET and 301/302 may downgrade to GET.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

??? question "27. What is the difference between redirect() and redirectToRoute()?"
    **✅ redirect() takes a URL; redirectToRoute() takes a route name and parameters**

    redirect() is URL-based; redirectToRoute() builds the URL from the router. Both return a RedirectResponse (default 302).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#redirecting)

??? question "28. What does AbstractController::forward() do?"
    **✅ Runs another controller in a sub-request and returns its Response, without a new client request**

    forward() dispatches a sub-request through the kernel; the browser URL does not change and no 3xx is sent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#forwarding-to-another-controller)

??? question "29. During a forwarded sub-request, what does Request::isMainRequest() return?"
    **✅ false**

    The sub-request is dispatched with HttpKernelInterface::SUB_REQUEST, so isMainRequest() is false and some listeners (e.g. the firewall) skip.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "30. After a forward(), what does the user's address bar show?"
    **✅ The original URL, unchanged**

    Forwarding is server-internal within the same request, so no new client navigation occurs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#forwarding-to-another-controller)

??? question "31. How do you correctly produce a 404 from a controller?"
    **✅ throw $this->createNotFoundException()**

    createNotFoundException() returns a NotFoundHttpException you must throw; the kernel then renders the error page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller.html#managing-errors-and-404-pages)

??? question "32. A controller throws a plain \RuntimeException. What status code results?"
    **✅ 500**

    Only exceptions implementing HttpExceptionInterface set a specific status; any other exception becomes a 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "33. Where do you place a custom production 404 template?"
    **✅ templates/bundles/TwigBundle/Exception/error404.html.twig**

    The Twig error renderer looks up per-status templates in that path in the prod environment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "34. Which kernel event lets a listener turn an exception into a Response?"
    **✅ kernel.exception (ExceptionEvent)**

    ExceptionEvent listeners can call setResponse(); otherwise the error controller renders the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

??? question "35. Which value should you trust to determine an uploaded file's real type?"
    **✅ getMimeType() (content-detected by the guesser)**

    Client-supplied name/MIME are spoofable; getMimeType()/guessExtension() inspect the actual file content.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/upload_file.html)

??? question "36. What does UploadedFile::move() do when it fails?"
    **✅ Throws a FileException**

    move() throws FileException on failure rather than returning a status value.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

??? question "37. With #[MapUploadedFile] and a failing File constraint, what happens?"
    **✅ An HTTP exception is thrown before the action body runs**

    The resolver validates the upload and aborts with an HTTP error when a constraint fails, so the body never executes with invalid input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

??? question "38. Which built-in controller renders a Twig template purely from route config?"
    **✅ TemplateController**

    TemplateController::__invoke() renders the 'template' default and can set HTTP cache headers, needing no custom class.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#rendering-a-template-directly-from-a-route)

??? question "39. RedirectController configured with permanent: true returns which status?"
    **✅ 301 (or 308 when keepRequestMethod is true)**

    permanent selects the permanent status code; combined with keepRequestMethod it becomes 308 to preserve the method.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-to-urls-and-routes-directly-from-a-route)

??? question "40. What status does RedirectController return when the target route/path is empty?"
    **✅ 410 Gone**

    An empty target signals the resource is permanently gone, so the controller responds 410.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

??? question "41. Which interface does a custom value resolver implement in Symfony 8?"
    **✅ ValueResolverInterface (resolve(Request, ArgumentMetadata): iterable)**

    The split supports()/resolve() interface was removed; resolve() now returns an iterable and yielding nothing declines the argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

??? question "42. How does a value resolver signal that it does not handle an argument?"
    **✅ It yields nothing (returns an empty iterable)**

    Yielding no value passes the argument to the next resolver in priority order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

??? question "43. Which resolvers have the highest default priority (120) in Symfony 8?"
    **✅ RequestValueResolver and SessionValueResolver**

    Request and Session resolvers run first at priority 120; the attribute, enum, uid and datetime resolvers sit at 100.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Resources/config/web.php)

??? question "44. A #[MapRequestPayload] argument fails validation. Which status is thrown?"
    **✅ 422 Unprocessable Entity (400 if the body itself is malformed)**

    RequestPayloadValueResolver deserializes then validates; validation errors throw UnprocessableEntityHttpException (422).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html#mapping-the-whole-request-payload)

??? question "45. How do the #[MapRequestPayload]/#[MapQueryParameter] resolvers get activated?"
    **✅ They are targeted resolvers that run only when their attribute is present on the argument**

    These resolvers carry the controller.targeted_value_resolver tag and are invoked only for arguments bearing the matching attribute.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

??? question "46. What binds a single typed query parameter such as ?page=2 to an int argument?"
    **✅ #[MapQueryParameter]**

    #[MapQueryParameter] binds one query value with casting; #[MapQueryString] maps the whole query string into a DTO.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/value_resolver.html)

---

<small>Back to [Flashcards](index.md) · [Controllers](../../controllers/index.md)</small>
