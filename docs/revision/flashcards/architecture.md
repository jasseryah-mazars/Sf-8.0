# Flashcards — Symfony Architecture

116 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. What kind of tool is Symfony Flex?"
    **✅ A Composer plugin that resolves aliases and applies recipes**

    Flex is a Composer plugin. It runs at Composer install/update time, resolving package aliases and applying recipes; it has no role during HTTP request handling.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

??? question "2. What does the symfony.lock file track?"
    **✅ Which recipes are installed and their versions**

    symfony.lock records applied recipes so Flex can detect updates and reverse them; it is distinct from composer.lock (package versions).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

??? question "3. How does a recipe auto-register a bundle?"
    **✅ By writing an entry into config/bundles.php**

    The bundles configurator adds the bundle class to config/bundles.php, which the kernel reads at boot via MicroKernelTrait::registerBundles().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

??? question "4. Which repository holds the community (opt-in) recipes?"
    **✅ symfony/recipes-contrib**

    Curated recipes live in symfony/recipes; community recipes live in symfony/recipes-contrib and require enabling extra.symfony.allow-contrib.

    :material-book-open-variant: [Docs](https://github.com/symfony/recipes-contrib)

??? question "5. Which statement about symfony.lock vs composer.lock is correct?"
    **✅ symfony.lock records applied recipes; composer.lock records resolved package versions — both are committed**

    The two files are complementary, not interchangeable. composer.lock pins resolved package versions (Composer's job); symfony.lock pins which recipe versions were applied (Flex's job) so every teammate/CI reproduces the same config and Flex can detect/rollback recipe changes. Both must be committed. The common trap is thinking one supersedes the other or that they should be ignored.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

??? question "6. At which point in a project's lifecycle does Symfony Flex actually run?"
    **✅ Only at Composer time — it subscribes to Composer events like post-install-cmd/post-update-cmd and package install/uninstall**

    Flex is a Composer plugin that hooks Composer's event system; when a package is installed/updated/removed it resolves aliases and applies (or reverses) the matching recipe's configurators. It writes files (config/, .env, bundles.php) but plays no part in the HTTP runtime, the DI compiler, or terminate — those read the files Flex produced.

    :material-book-open-variant: [Docs](https://github.com/symfony/flex)

??? question "7. In Flex terminology, what is the difference between an alias and a recipe?"
    **✅ An alias is a short name that maps to a real package; a recipe is the automation (configurators) applied when that package is installed**

    `composer require orm` uses the alias `orm`, which resolves to the real package `doctrine/orm`; the alias only affects the name written to composer.json. The recipe is the separate automation (bundles, copy-from-recipe, env, container configurators described in manifest.json) that wires the package into your app. Aliases are convenience; recipes are the work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

??? question "8. Under which license is Symfony released?"
    **✅ MIT**

    Symfony components are released under the permissive, non-copyleft MIT license.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/LICENSE)

??? question "9. What is the core obligation of the MIT license?"
    **✅ Retain the copyright and permission notice in copies**

    MIT only requires that the copyright and permission notice be kept in all copies or substantial portions; it is not copyleft.

    :material-book-open-variant: [Docs](https://opensource.org/license/mit)

??? question "10. Does the MIT license grant rights to use the Symfony name and logo?"
    **✅ No — those are governed by the separate trademark policy**

    The code license (MIT) and the trademark (name/logo) are separate legal instruments. Using the Symfony name/logo follows Symfony SAS's trademark policy.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

??? question "11. True or false: because Symfony is MIT-licensed, you must open-source any application you build on it."
    **✅ False**

    False. MIT is permissive, not copyleft (unlike the GPL). You may ship Symfony inside closed-source, proprietary products without releasing your own source; the only condition is retaining the copyright/permission notice.

    :material-book-open-variant: [Docs](https://opensource.org/license/mit)

??? question "12. A startup ships a closed-source SaaS built on Symfony and wants to market it as "SymfonyCloud". Which part is a problem?"
    **✅ The closed-source SaaS is fine under MIT, but naming it "SymfonyCloud" risks trademark infringement**

    MIT permits commercial, closed-source use, so building the SaaS is fine. But the code license says nothing about names/logos: using \"Symfony\" in a product name is governed by Symfony SAS's trademark policy, so \"SymfonyCloud\" is the risky part. You may say \"built with Symfony\" but not brand as Symfony.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

??? question "13. What best describes a Symfony component?"
    **✅ A standalone, reusable PHP library shipped as its own Composer package**

    Components are decoupled libraries, each independently versioned and usable without the full framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

??? question "14. What do the symfony/*-contracts packages contain?"
    **✅ Stable interfaces and traits to depend on**

    Contracts packages hold interface-only definitions so consumers can depend on a stable API decoupled from a concrete implementation.

    :material-book-open-variant: [Docs](https://github.com/symfony/contracts)

??? question "15. Can symfony/routing be used without FrameworkBundle?"
    **✅ Yes — it is a standalone component**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

??? question "16. Which mapping of term to definition is entirely correct?"
    **✅ Contract = interfaces/traits; Component = standalone library; Bridge = glue to a third-party lib; Bundle = framework wiring**

    The four layers are distinct: contracts (e.g. symfony/service-contracts) ship only interfaces/traits; components (e.g. symfony/routing) are standalone implementations; bridges (e.g. symfony/twig-bridge) glue a component to one specific third-party library; bundles (e.g. symfony/framework-bundle) wire things into the framework with services and config. Confusing bridge with bundle, or contract with component, is the classic exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

??? question "17. Using only the Routing component standalone, what does $matcher->match('/hello/sf') return for a route defined as new Route('/hello/{name}') named 'hello'?"
    **✅ ['_route' => 'hello', 'name' => 'sf']**

    UrlMatcher::match() returns an array of the matched route's parameters, including the special _route key with the route name and any placeholder values. No framework or kernel is involved — the component works standalone with a RouteCollection and a RequestContext. It returns parameters, never a Response (that is the framework's job).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

??? question "18. For a modern application, how should you depend on Symfony code?"
    **✅ Require the individual packages you need (e.g. symfony/routing); the symfony/symfony metapackage is discouraged**

    You should require only the individual component/bundle packages you use so the dependency graph stays minimal and each package versions independently. The old symfony/symfony monolithic metapackage is discouraged. Type-hinting contracts/interfaces further decouples you from concrete implementations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

??? question "19. What is a Symfony bridge?"
    **✅ An integration layer between a component and a specific third-party library**

    A bridge holds the glue coupling a Symfony component to one specific external library, keeping the component itself dependency-free.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

??? question "20. Where do bridges live in the Symfony monorepo?"
    **✅ src/Symfony/Bridge/**

    Bridges have their own top-level directory, distinct from Component and Bundle.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony)

??? question "21. What typically activates a bridge inside a framework application?"
    **✅ A bundle that registers the bridge's classes as services**

    Bridges provide classes; a bundle wires them into the container and exposes configuration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

??? question "22. Which statement distinguishes a bridge from a bundle correctly?"
    **✅ A bridge is a glue library (classes) coupling a component to one third-party lib; a bundle registers services and config in the framework**

    A bridge is just a Composer library of adapter/glue classes that depends on a component plus one specific external library; it does not wire itself into any app. A bundle is the framework-integration layer that registers those classes as services and exposes configuration. Expecting a bridge to configure itself is the trap — that is a bundle's job.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

??? question "23. Why is the external library an optional dependency of the component but a required dependency of the bridge?"
    **✅ Keeping it optional on the component preserves the component's minimal, reusable dependency graph; the bridge exists precisely to depend on that library, so it requires it**

    A component must stay usable by everyone, so it must not hard-require any particular third-party library — that coupling is pushed into a separate bridge package. The bridge's whole reason to exist is to integrate that specific library, so it declares it as a required dependency. This keeps the component's graph minimal and the integration independently versioned.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

??? question "24. Which directory is the web root of a Symfony application?"
    **✅ public/**

    public/ contains index.php and static assets and is the only web-accessible directory.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

??? question "25. Where are bundles enabled in a modern Symfony app?"
    **✅ config/bundles.php**

    config/bundles.php maps each bundle class to the environments where it is enabled; the kernel reads it via MicroKernelTrait.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

??? question "26. What supplies registerBundles() and registerContainerConfiguration() in a skeleton Kernel?"
    **✅ MicroKernelTrait**

    App\\Kernel uses MicroKernelTrait, which implements the boilerplate to load bundles from config/bundles.php and configuration from config/.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/micro_kernel_trait.html)

??? question "27. In config/bundles.php an entry reads `WebProfilerBundle::class => ['dev' => true, 'test' => true]`. What does this mean?"
    **✅ The bundle is enabled only in the dev and test environments, not in prod**

    config/bundles.php maps each bundle class to an array of environment => bool. The kernel enables the bundle only in the listed environments whose value is true. `['all' => true]` means every environment; `['dev' => true, 'test' => true]` means dev and test only (typical for debugging/profiling bundles).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

??? question "28. In prod, why is public/index.php fast and free of YAML parsing on the hot path?"
    **✅ config/ is parsed at compile time into a dumped container in var/cache/<env>/; runtime only loads that compiled container**

    Configuration is compiled once into a dumped PHP container under var/cache/<env>/. In prod the kernel simply loads that compiled container, so no YAML parsing happens per request — that is why the front controller stays tiny and the hot path is fast. In dev, ConfigCache checks freshness and rebuilds when source config changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/micro_kernel_trait.html)

??? question "29. How does a modern (Symfony 8) bundle inherit and override another bundle's resources?"
    **✅ It doesn't — bundle inheritance via getParent() was removed; you override each resource type individually**

    The getParent() bundle-inheritance mechanism was deprecated in 4.4 and removed in 5.0; it does not exist in Symfony 8. Modern apps override each resource type on its own (templates via templates/bundles/<Name>/, services via decoration/redefinition, config via config/packages/). Mentioning getParent() as a current mechanism is a planted trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

??? question "30. What does the default `App\:` service definition with `resource: '../src/'` and `exclude: '../src/{Kernel.php}'` achieve?"
    **✅ It auto-registers every class under src/ as a service (with autowire/autoconfigure defaults), excluding Kernel.php**

    The resource glob discovers classes under src/ and registers each as a service whose id is its FQCN, inheriting the _defaults (autowire: true, autoconfigure: true). exclude keeps non-service classes (like Kernel.php, entities, DTOs) out. Unused private services are then pruned by the compiler. It does not make them public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "31. For a controller that returns a Response, in what order do the kernel events fire?"
    **✅ kernel.request -> kernel.controller -> kernel.controller_arguments -> kernel.response**

    kernel.view is skipped because a Response was returned; the remaining events follow the canonical order, then finish_request and terminate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "32. When is kernel.view dispatched?"
    **✅ Only when the controller returns a value that is not a Response**

    If the controller returns a non-Response value, kernel.view listeners must convert it into a Response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-view)

??? question "33. When is kernel.terminate dispatched?"
    **✅ After the response has been sent to the client, for the main request**

    terminate() runs after send() and is not called for sub-requests; it is ideal for slow post-response work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-terminate)

??? question "34. A listener calls setResponse() on kernel.request. What happens next?"
    **✅ The controller is skipped and flow continues at kernel.response**

    Setting a response on kernel.request short-circuits controller resolution; the response still passes through kernel.response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-request)

??? question "35. What is the value of HttpKernelInterface::MAIN_REQUEST?"
    **✅ 1 (and SUB_REQUEST is 2)**

    MAIN_REQUEST is 1 and SUB_REQUEST is 2; the old MASTER_REQUEST constant was removed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "36. What is the full firing order of the linear kernel events when a controller returns a non-Response value that a listener then converts?"
    **✅ request → controller → controller_arguments → view → response → finish_request → (after send) terminate**

    The canonical order is request, controller, controller_arguments, view (only when a non-Response is returned), response, finish_request; then after the response is sent, terminate. kernel.exception is the eighth KernelEvents constant but fires out of band, only on error. controller_arguments runs AFTER argument resolution, and view sits between the controller call and response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "37. What are the respective jobs of ControllerResolverInterface and ArgumentResolverInterface?"
    **✅ ControllerResolver reads the _controller attribute and returns a callable; ArgumentResolver builds the ordered argument array via value resolvers**

    ControllerResolverInterface::getController(Request) reads the _controller request attribute (set by the router) and returns a PHP callable. ArgumentResolverInterface::getArguments() then runs a chain of ValueResolverInterface resolvers (request attributes, the Request object, #[MapRequestPayload], services, variadics, defaults) to build the ordered argument list passed to the controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "38. Relative to argument resolution, when does kernel.controller_arguments fire?"
    **✅ After ArgumentResolver has built the argument array — listeners edit an already-resolved array via setArguments()**

    kernel.controller_arguments is dispatched AFTER ArgumentResolverInterface::getArguments() has produced the final ordered array; listeners receive a ControllerArgumentsEvent and may mutate the already-built array with setArguments(). Assuming it runs before resolution (to feed the resolver) is a common misconception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-controller-arguments)

??? question "39. A controller does its work but has no return statement (returns null) and no kernel.view listener handles it. What happens?"
    **✅ The kernel dispatches kernel.view; since no response is set, it throws ControllerDoesNotReturnResponseException**

    After the controller runs, handleRaw() checks whether the return value is a Response; if not, it dispatches kernel.view carrying the value. If no listener calls setResponse(), the kernel throws ControllerDoesNotReturnResponseException (a LogicException) with the familiar \"The controller must return a Response object but it returned null\" message. The fix is to return a real Response or register a view listener.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "40. Which statement about sub-requests is correct?"
    **✅ They run the same request→...→finish_request flow but never fire kernel.terminate; RequestStack push/pop restores parent state**

    A sub-request (HttpKernelInterface::SUB_REQUEST) runs the full linear flow from kernel.request through kernel.response and kernel.finish_request, but kernel.terminate fires only for the main request after send. handleRaw() pushes the sub-request onto the RequestStack before kernel.request and pops it after kernel.finish_request, restoring the parent request/locale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "41. What is the signature of HttpKernelInterface::handle() and the role of its $catch argument?"
    **✅ handle(Request $request, int $type = self::MAIN_REQUEST, bool $catch = true): Response — with $catch=true, exceptions are caught and turned into a response via kernel.exception; with $catch=false they propagate**

    The contract is handle(Request, int $type = MAIN_REQUEST, bool $catch = true): Response. handle() wraps the private handleRaw() in a try/catch when $catch is true, so an escaped exception is routed through handleThrowable()/kernel.exception into a Response. With $catch=false (common in sub-requests and tests) the exception simply propagates to the caller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "42. A listener is annotated #[AsEventListener(event: KernelEvents::RESPONSE, priority: -10)] and sets an X-Frame-Options header. When does it run?"
    **✅ On every response passing through kernel.response, after listeners with higher priority (since -10 is below the default 0)**

    kernel.response fires for every response (whether from the controller, a view listener, or a short-circuit). Listeners run high priority first; priority -10 is below the default 0, so this header listener runs relatively late. The #[AsEventListener] attribute is wired by RegisterListenersPass at compile time, replacing manual tagging.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-response)

??? question "43. Which event is responsible for turning an exception into a response?"
    **✅ kernel.exception**

    When an exception escapes handleRaw(), HttpKernel dispatches kernel.exception; listeners may set the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

??? question "44. What status code results from an uncaught plain \LogicException?"
    **✅ 500**

    Only exceptions implementing HttpExceptionInterface carry a status; any other exception defaults to 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "45. At what priority is the default ErrorListener registered on kernel.exception?"
    **✅ -128, so custom listeners run first**

    ErrorListener runs at a low priority (-128) so your own exception listeners get the first chance to handle the throwable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

??? question "46. Where do you override the default 404 error template?"
    **✅ templates/bundles/TwigBundle/Exception/error404.html.twig**

    TwigBundle resolves error templates from templates/bundles/TwigBundle/Exception/, falling back to error.html.twig.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "47. What does the default ErrorListener actually do when it handles a kernel.exception?"
    **✅ It logs the exception, forwards to the error controller as a sub-request, and sets the resulting Response on the event**

    ErrorListener (priority -128) logs the throwable, forwards to the error_controller (ErrorController) as a sub-request whose response carries the status/headers from HttpExceptionInterface, and sets that response on the ExceptionEvent. Because it runs last, any higher-priority listener that already set a response wins and ErrorListener does nothing.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/ErrorListener.php)

??? question "48. How do Security's AccessDeniedException and HttpKernel's AccessDeniedHttpException differ?"
    **✅ AccessDeniedHttpException implements HttpExceptionInterface (→ 403 directly); AccessDeniedException is a Security exception the firewall translates to 403 or a redirect to login**

    They are different classes. Symfony\\Component\\HttpKernel\\Exception\\AccessDeniedHttpException implements HttpExceptionInterface and yields a 403 through the normal error flow. Symfony\\Component\\Security\\Core\\Exception\\AccessDeniedException is a Security exception that does NOT implement HttpExceptionInterface; the firewall's exception listener catches it and turns it into a 403 (or a redirect to the login page for unauthenticated users).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "49. A kernel.exception listener inspects getThrowable() and builds a JsonResponse, but the custom page never appears. What is the most likely bug?"
    **✅ The listener forgot to call $event->setResponse() on its branch, so the event's response stays null and the default handler wins**

    ExceptionEvent::getResponse() returns null until some listener calls setResponse(). Reading getThrowable() and constructing a response is not enough — you must actually set it on the event. If a branch forgets setResponse(), the response stays null, ErrorListener's default page (or a 500) is used instead, and your custom page never shows.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

??? question "50. After kernel.exception is dispatched, what does the kernel do if no listener set a response?"
    **✅ handleThrowable() sees hasResponse() is false and re-throws the original throwable (which surfaces as a 500 when catch is true)**

    If ExceptionEvent has no response after dispatch, handleThrowable() re-throws the original exception. In practice ErrorListener (priority -128) fills the gap, so this null case only bites when you replace or disable it. With catch:true the re-thrown error becomes a 500 to the client.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernel.php)

??? question "51. Which built-in exception produces a 404 response?"
    **✅ NotFoundHttpException**

    NotFoundHttpException maps to 404. AccessDeniedHttpException maps to 403 and BadRequestHttpException to 400. All implement HttpExceptionInterface, so their status code and headers flow through to the produced response; a generic HttpException takes any status code from its constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "52. What does a higher listener priority mean?"
    **✅ It runs earlier**

    Listeners are sorted by priority in descending order, so higher priorities run first; the default priority is 0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "53. What is the dispatch() signature in Symfony 8 (PSR-14)?"
    **✅ dispatch(object $event, ?string $eventName = null)**

    Symfony follows PSR-14: the event object comes first, the name is optional (defaults to the event's class name).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "54. Which method must an event subscriber implement?"
    **✅ public static function getSubscribedEvents(): array**

    EventSubscriberInterface defines the static getSubscribedEvents() method returning event names mapped to handlers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

??? question "55. What does $event->stopPropagation() do?"
    **✅ Prevents the remaining listeners of this event from running**

    It sets a flag the dispatcher checks before each listener; only the current event's remaining listeners are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "56. How does EventDispatcher store and order listeners internally?"
    **✅ It keeps listeners[eventName][priority][] and sorts by priority descending on first dispatch, memoising the sorted list until a listener is added/removed**

    Internally the dispatcher stores listeners keyed by event name then priority. On the first dispatch of an event it sorts by priority descending (higher first; equal priorities preserve registration order) and caches the result in a sorted[] map, invalidated only when listeners change. This memoisation keeps repeated dispatches cheap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php)

??? question "57. How are tagged listeners/subscribers and #[AsEventListener] attributes wired into the dispatcher?"
    **✅ RegisterListenersPass wires them at container compile time, and listener services are instantiated lazily only when their event fires**

    The RegisterListenersPass compiler pass scans services tagged kernel.event_listener/kernel.event_subscriber and #[AsEventListener] attributes and wires them into the dispatcher at compile time. Listeners are registered lazily — the service is only constructed when its event actually fires — which keeps boot cheap. You rarely call addListener() at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

??? question "58. Which are valid return values from getSubscribedEvents() for a single event? (choose all that apply)"
    **✅ [KernelEvents::RESPONSE => 'onResponse'] ; [KernelEvents::RESPONSE => ['onResponse', -10]] ; [KernelEvents::RESPONSE => [['onFirst', 10], ['onSecond', -10]]]**

    getSubscribedEvents() maps event NAMES to handlers. The value may be a method name string, a [method, priority] pair, or a list of such pairs to register several handlers for the same event. Mapping method → event name (reversed) is wrong and a frequent mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

??? question "59. What does dispatch(object $event) return, and how do you read a listener's result?"
    **✅ It always returns the same event object you passed in; results reach you only by listeners mutating that event (e.g. setResponse), never as a listener return value**

    dispatch() returns the exact event object passed in — even with no listeners, or when all left it untouched. Listeners themselves return void; the only way data flows back is by mutating the event, which you then read from the returned object. Expecting dispatch() to hand back a listener's return value is the classic bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "60. Two listeners for the same event both use the default priority. In what order do they run?"
    **✅ In registration order — the default priority is 0 and equal priorities preserve the order they were added**

    The default priority is 0. Listeners are sorted by priority descending, and ties (equal priority) keep their registration order. So two default-priority listeners run first-registered-first. To force an order, set explicit priorities rather than relying on registration order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "61. What is the key difference between a listener and a subscriber?"
    **✅ A listener is registered against one event; a subscriber declares all the events it handles in getSubscribedEvents()**

    A listener is a callable attached to a single event name (via #[AsEventListener] or the kernel.event_listener tag). A subscriber implements EventSubscriberInterface and declares all its events (and priorities) in the static getSubscribedEvents() method — handy when one class handles several related events. Both are wired by RegisterListenersPass.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

??? question "62. Where should business logic live according to the best practices?"
    **✅ In autowired services**

    Controllers should be thin and delegate to services, which keeps logic reusable and testable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/best_practices.html)

??? question "63. What visibility should application services have by default?"
    **✅ Private**

    Private services let the DI compiler inline and remove them, and discourage the service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "64. Where do sensitive credentials belong?"
    **✅ The Secrets vault**

    Secrets should be stored in the encrypted Secrets vault, while infrastructure config uses env vars and behaviour uses parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/secrets.html)

??? question "65. What does this services.yaml _defaults block enable: autowire: true, autoconfigure: true, public: false?"
    **✅ Constructor deps are injected by type, services are auto-tagged by the interfaces they implement, and services are private by default**

    autowire resolves constructor arguments by type-hint; autoconfigure auto-tags services based on implemented interfaces/attributes (e.g. subscribers get kernel.event_subscriber); public: false keeps them private so the compiler can inline/prune them and you inject rather than fetch. This is the idiomatic Symfony 8 default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "66. Where should each belong: a database URL, a feature toggle, and a third-party API private key?"
    **✅ Database URL → env var; feature toggle → parameter (or env var if it varies per env); API private key → Secrets vault**

    Infrastructure config that varies per environment (database URL) goes in env vars; application behaviour (feature toggle) goes in parameters, or an env var if it changes per environment; sensitive credentials (API private key) go in the encrypted Secrets vault — never committed as plain config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/secrets.html)

??? question "67. Why is making application services public "to be safe" discouraged?"
    **✅ Public services block the DI compiler from inlining/removing them and invite the service-locator anti-pattern; private + injected is preferred**

    Marking services public prevents the compiler from optimising them away or inlining them, and encourages fetching from the container (service location) instead of dependency injection. The best practice is private, autowired services injected via the constructor. Public visibility is only needed in a few edge cases (e.g. legacy get() calls).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "68. How often does a new Symfony minor version ship?"
    **✅ Every six months, in May and November**

    Symfony uses a fixed time-based cadence: a minor every May and November, a major every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "69. Which Symfony 8.x version is the LTS?"
    **✅ 8.4**

    The last minor of each major (X.4) is the LTS; it ships alongside the next major (9.0).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

??? question "70. What may a MINOR release NOT do?"
    **✅ Break backward compatibility**

    Minors add features and deprecations but never break BC; breaks are reserved for major releases.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "71. What are the maintenance windows for a standard (non-LTS) release?"
    **✅ 8 months of bug fixes and 14 months of security fixes**

    Standard versions get 8 months bug fixes and 14 months security fixes; LTS versions get 3 years and 4 years respectively.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "72. How are bug fixes propagated across Symfony's maintained branches?"
    **✅ Fixes are merged UP from the oldest maintained branch to newer ones, so a patch to 8.0 also lands in 8.1, 8.2, etc.**

    Symfony uses a merge-up model: a fix is committed to the lowest maintained branch that needs it and then merged upward into every newer branch. This keeps behaviour consistent across all maintained versions and avoids a fix being present in an old branch but missing in a newer one.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

??? question "73. What is the difference between a PATCH and a MINOR release?"
    **✅ A patch (8.0.1 → 8.0.2) contains bug fixes only; a minor (8.0 → 8.1) adds new features and deprecations but is still BC-safe**

    Patch releases carry bug fixes only — no new features, no deprecations, no BC breaks. Minor releases add features and may introduce deprecations, but never break BC. Only majors break BC (by removing previously deprecated code). Confusing patch (bugs only) with minor (features) is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "74. What is a MAJOR release uniquely allowed to do?"
    **✅ Remove deprecated code and break backward compatibility (only for APIs deprecated in the previous major line)**

    A major (e.g. 8.x → 9.0) is the only release level permitted to break BC, and only for code that was deprecated during the previous major line. This is what lets you upgrade safely within a major and plan the jump across a major once you have cleared deprecations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "75. When may Symfony break backward compatibility?"
    **✅ Only in a major release, and only after prior deprecation**

    BC breaks are reserved for majors and require the affected API to have been deprecated in the previous major line.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "76. What does the @internal marker mean for the BC promise?"
    **✅ The element is excluded from the BC promise and may change at any time**

    @internal marks implementation details not covered by BC, even if they are PHP-public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "77. How should you customise a final Symfony class in a BC-safe way?"
    **✅ Decorate or compose it**

    final classes must not be subclassed; wrap them via decoration so Symfony can change internals without breaking you.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "78. Is @experimental code covered by the BC promise?"
    **✅ No — experimental features (often whole components in their first release) are explicitly excluded until marked stable**

    @experimental features are excluded from the BC promise until they are stabilised; they may change in any release. Building critical paths on experimental code is risky. Along with @internal and final, @experimental is one of the markers that carve exceptions out of the promise.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/experimental.html)

??? question "79. Symfony adds a new method to one of its own interfaces in a minor release. Is this a BC break?"
    **✅ Not for code that only USES the interface, but it can break code that IMPLEMENTS it — so only implement interfaces Symfony marks as safe to implement**

    The promise is written from two viewpoints. For USING code (calling methods, reading returns) adding a method is safe. For EXTENDING code (your class implementing that interface) a new method is a break, because your class no longer satisfies the contract. Symfony reserves the right to add methods to its interfaces, so you should only implement interfaces meant for implementation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "80. Which of the following are covered by the BC promise? (choose all that apply)"
    **✅ A public method with no special annotation ; The stable public constructor of a non-final, non-internal class**

    Stable public API without @internal/@experimental is covered — regardless of being a method or constructor. @internal is excluded even though PHP-public, and @experimental is excluded until stabilised. The classic misconception is equating PHP `public` with \"covered\"; @internal overrides that.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "81. True or false: a method declared public in PHP but annotated @internal is protected by the BC promise."
    **✅ False**

    False. @internal explicitly removes an element from the BC promise even when it is PHP-public. Such methods/classes can change or disappear in any release, so you must not depend on them. PHP visibility and BC coverage are independent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "82. Which function emits a Symfony deprecation notice, and from which package?"
    **✅ trigger_deprecation() from symfony/deprecation-contracts**

    symfony/deprecation-contracts provides trigger_deprecation($package, $version, $message, ...$args), which formats an E_USER_DEPRECATED notice.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "83. When is deprecated code actually removed?"
    **✅ In the next major release**

    Deprecations survive the whole major line and are only removed in the next major, per the BC promise.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "84. Which tool lets you fail the test suite when new deprecations appear?"
    **✅ symfony/phpunit-bridge configured via SYMFONY_DEPRECATIONS_HELPER**

    The PHPUnit bridge collects deprecations; SYMFONY_DEPRECATIONS_HELPER (e.g. max[total]=0) can make the suite fail on any deprecation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

??? question "85. What is the argument order of trigger_deprecation()?"
    **✅ package, version, message, ...args**

    The signature is trigger_deprecation(string $package, string $version, string $message, mixed ...$args) with sprintf-style formatting.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "86. Which call correctly deprecates ReportBuilder::generate() (deprecated in your app version 8.1)?"
    **✅ trigger_deprecation('app/reports', '8.1', 'Using "%s::generate()" is deprecated, use "build()".', self::class);**

    The signature is (package, version, message, ...args) with sprintf-style formatting for the message. The first option passes the package, the version it was deprecated IN, a message with a %s placeholder, and self::class as the arg. Putting the message first, or misusing trigger_error with these arguments, is wrong.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "87. How do you mark a service as deprecated in config/services.yaml?"
    **✅ Add a `deprecated:` key with package, version and message under the service definition**

    A service is deprecated via the `deprecated:` key (package/version/message), which maps to Definition::setDeprecated() and triggers a deprecation when the service is referenced. Container-level deprecations like this surface during cache:clear/compile time, whereas method-call deprecations fire at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection.html)

??? question "88. At what error level are Symfony deprecations emitted, and do they throw?"
    **✅ They are E_USER_DEPRECATED notices — they do not throw unless your test suite/CI is configured to fail on them**

    trigger_deprecation() ultimately calls @trigger_error(..., E_USER_DEPRECATED), producing a notice that is logged/collected but does not interrupt execution. Only when tooling (e.g. the PHPUnit bridge via SYMFONY_DEPRECATIONS_HELPER) is configured to fail on deprecations does a deprecation cause a failure.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "89. Which version string should you pass as the second argument of trigger_deprecation()?"
    **✅ The version in which the API was DEPRECATED (e.g. '8.1'), not the current running version**

    The version argument records when the deprecation was introduced, producing the \"Since <package> <version>: <message>\" format tooling parses. A common mistake is passing the current version, or the removal version — both are wrong. Use the version the API was deprecated in.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "90. Where do you place a template that overrides a bundle template?"
    **✅ templates/bundles/<BundleName>/path.html.twig**

    Twig resolves overrides from templates/bundles/<BundleName>/, which takes precedence over the bundle's own templates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

??? question "91. What is the current mechanism to override an inherited bundle resource?"
    **✅ Per-resource overriding of templates, services, translations and config**

    Bundle inheritance via getParent() was deprecated in 4.4 and removed in 5.0; modern Symfony overrides each resource type individually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

??? question "92. How do you augment a bundle service without replacing it?"
    **✅ Decorate it with #[AsDecorator] / the decorates: key**

    Decoration wraps the original service (injected as .inner), letting you add behaviour and delegate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "93. When you decorate a service with #[AsDecorator(decorates: 'acme.mailer')], how do you access the original?"
    **✅ Inject the renamed original (the .inner service) via #[AutowireDecorated] and delegate to it**

    Decoration renames the original service to a .inner id and injects it into the decorator. The #[AutowireDecorated] attribute (or the special .inner reference in YAML) gives you that original instance so you can add behaviour and delegate. Re-creating it with `new` or fetching it publicly defeats the decoration pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "94. A bundle ships translations/messages.en.yaml and your app defines the same domain/locale in translations/. Whose strings win?"
    **✅ The application's translations/ take priority over the bundle's translations**

    The application's translations/ directory has higher priority than any bundle's translations. Providing a catalogue with the same domain and locale overrides the bundle's strings — the same convention-based precedence used for template overrides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

??? question "95. What happened to bundle inheritance (getParent()) and the legacy Resources/ folder?"
    **✅ getParent() inheritance was deprecated in 4.4 and removed in 5.0; modern bundles use top-level config/, templates/, translations/ instead of Resources/**

    Bundle inheritance via getParent() is gone (deprecated 4.4, removed 5.0) and must not be presented as current. Modern bundles also drop the legacy Resources/ layout in favour of top-level config/, templates/ and translations/. Overriding is done per resource type instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

??? question "96. In which months do Symfony minor releases ship?"
    **✅ May and November**

    The cadence is fixed: a new minor every May and every November.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "97. When does 8.4 (LTS) release relative to 9.0?"
    **✅ At the same time (both November 2027)**

    The LTS (X.4) always ships together with the next major (X+1).0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

??? question "98. How often is a new major (and its LTS) released?"
    **✅ Every two years**

    Majors, and the accompanying LTS, come every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "99. Which sequence correctly lists the Symfony 8.x release dates?"
    **✅ 8.0 Nov 2025, 8.1 May 2026, 8.2 Nov 2026, 8.3 May 2027, 8.4 LTS Nov 2027**

    8.0 opened the cycle in Nov 2025; a minor lands every six months (May/Nov): 8.1 May 2026, 8.2 Nov 2026, 8.3 May 2027, and 8.4 (LTS) Nov 2027 alongside 9.0. The pattern repeats for every major: X.0 opens, four minors follow, X.4 is the LTS shipping with (X+1).0.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "100. Which statement about the LTS timing is correct?"
    **✅ The LTS (X.4) ships at the same time as the next major (X+1).0, not before it**

    A frequent misconception is that the LTS precedes the next major. In fact X.4 (the LTS) and (X+1).0 release together (8.4 and 9.0 both Nov 2027). Another trap: 8.0 is a standard release, not the LTS — 8.4 is.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

??? question "101. A product must run 3+ years without a major upgrade. Which 8.x version should you target and why?"
    **✅ 8.4 (LTS) — it provides 3 years of bug fixes and 4 years of security fixes, the longest support window in 8.x**

    Only the LTS (X.4) offers the long maintenance windows (3 years bug fixes, 4 years security fixes). Standard minors get 8 months bug + 14 months security, far short of 3 years. So a long-lived product should pin to 8.4 and plan the jump to the next major deliberately.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "102. Which PSR does Symfony's EventDispatcher implement?"
    **✅ PSR-14 (Event Dispatcher)**

    Symfony's EventDispatcherInterface extends the PSR-14 Psr\\EventDispatcher\\EventDispatcherInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "103. Is HttpFoundation's Request a PSR-7 message?"
    **✅ No — a psr-http-message bridge converts between them**

    HttpFoundation predates and differs from PSR-7; the psr-http-message bridge converts between HttpFoundation and PSR-7/15/17.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/psr7.html)

??? question "104. Which PSR interface does Symfony's service container implement?"
    **✅ PSR-11 (Container)**

    Symfony's ContainerInterface extends Psr\\Container\\ContainerInterface (PSR-11).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "105. Which PSR does Symfony primarily consume (rather than implement) so you can inject any implementation?"
    **✅ PSR-3 (Logger) via Psr\Log\LoggerInterface**

    Components type-hint Psr\\Log\\LoggerInterface (PSR-3), so any compliant logger can be injected. PSR-11, PSR-14, PSR-6 and PSR-20 are implemented by Symfony.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

??? question "106. Which PSRs does Symfony IMPLEMENT (i.e. Symfony objects ARE valid PSR objects)? (choose all that apply)"
    **✅ PSR-6 (Cache pool) ; PSR-11 (Container) ; PSR-14 (Event Dispatcher) ; PSR-20 (Clock)**

    Symfony implements PSR-6 (Cache pool), PSR-11 (Container), PSR-14 (EventDispatcher), PSR-16 (Simple Cache adapter) and PSR-20 (Clock) — its objects can be handed to any library expecting those interfaces. PSR-3 (Logger) is CONSUMED: Symfony type-hints LoggerInterface so you inject any implementation, but it does not ship the logger itself.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

??? question "107. What is the difference between PSR-6 and PSR-16 in Symfony's Cache?"
    **✅ PSR-6 is the pool/CacheItem model (CacheItemPoolInterface); PSR-16 is the simpler get/set SimpleCache API (Psr16Cache adapter)**

    PSR-6 models caching as a pool of CacheItem objects (CacheItemPoolInterface::getItem()/save()); PSR-16 (Simple Cache) is a lighter get()/set()/delete() API, exposed by Symfony's Psr16Cache adapter. Confusing the pool/item model (PSR-6) with the simple key/value API (PSR-16) is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

??? question "108. Which PSR does Symfony's Clock component implement, and why inject its interface?"
    **✅ PSR-20 via Psr\Clock\ClockInterface — injecting it makes time testable instead of calling new \DateTime() directly**

    Symfony\\Component\\Clock\\Clock implements Psr\\Clock\\ClockInterface (PSR-20). Type-hinting ClockInterface lets you inject a MockClock in tests and control time deterministically, instead of hard-coding new \\DateTime()/now() calls that are impossible to freeze.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "109. What is the practical difference between Symfony implementing a PSR and consuming a PSR?"
    **✅ Implementing means a Symfony object satisfies the PSR (hand it to any PSR consumer); consuming means Symfony type-hints the PSR so you can inject any implementation**

    Implements: Symfony's class IS a valid PSR object (e.g. its Container is a PSR-11 container), usable by any library expecting that interface. Consumes: Symfony depends on the PSR interface as a type-hint (e.g. PSR-3 LoggerInterface) so you can plug in any compliant implementation. The direction of the dependency is what differs.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

??? question "110. How are application service IDs written in modern Symfony?"
    **✅ As the fully-qualified class name (FQCN)**

    The service id is the FQCN; autowiring matches type-hints to these ids.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "111. What naming case do environment variables use?"
    **✅ UPPER_SNAKE_CASE, usually with an APP_ prefix**

    Env vars use upper snake case (APP_ENV, APP_DEBUG) and are read in config via processors such as %env(int:APP_PAGE_SIZE)%.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

??? question "112. Which is a correctly named route?"
    **✅ invoice_show**

    Route names use snake_case, conventionally entity_action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "113. How is an abstract class conventionally named?"
    **✅ With an Abstract prefix, e.g. AbstractController**

    Abstract classes take the Abstract prefix; interfaces use the Interface suffix and traits use the Trait suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

??? question "114. Which set correctly fixes these names: httpClientInterface, Abstract_Controller, blogShow (route), app-page-size (parameter), app_env (env var)?"
    **✅ HttpClientInterface, AbstractController, blog_show, app.page_size, APP_ENV**

    Interfaces are PascalCase with the Interface suffix (HttpClientInterface); abstract classes take the Abstract prefix in PascalCase (AbstractController); routes are snake_case (blog_show); parameters are snake/dot-separated lowercase (app.page_size); env vars are UPPER_SNAKE with APP_ prefix (APP_ENV).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

??? question "115. Why is the Interface suffix more than cosmetic in Symfony?"
    **✅ Autoconfiguration inspects implemented interfaces (e.g. EventSubscriberInterface) to auto-tag services, so correct interface naming/implementation is part of a working contract**

    When autoconfigure is on, Symfony auto-tags services based on the interfaces they implement — e.g. implementing EventSubscriberInterface auto-adds the kernel.event_subscriber tag, and ServiceSubscriberInterface, and voter/command interfaces behave similarly. So the Interface suffix marks a real, functional contract that drives wiring, not just style.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "116. Which casing pair is correct for PHP class constants and bundle config keys?"
    **✅ Constants are UPPER_SNAKE_CASE (e.g. MAIN_REQUEST); bundle config keys are snake_case (e.g. framework.http_method_override)**

    PHP constants follow UPPER_SNAKE_CASE (HttpKernelInterface::MAIN_REQUEST) and enum cases are PascalCase. Bundle configuration keys are snake_case under the extension's alias (e.g. framework.http_method_override). Mixing these up — camelCase config keys, for instance — is a planted mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

---

<small>Back to [Flashcards](index.md) · [Symfony Architecture](../../architecture/index.md)</small>
