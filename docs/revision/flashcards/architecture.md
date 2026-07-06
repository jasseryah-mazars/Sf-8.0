# Flashcards — Symfony Architecture

57 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

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

??? question "5. Under which license is Symfony released?"
    **✅ MIT**

    Symfony components are released under the permissive, non-copyleft MIT license.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/LICENSE)

??? question "6. What is the core obligation of the MIT license?"
    **✅ Retain the copyright and permission notice in copies**

    MIT only requires that the copyright and permission notice be kept in all copies or substantial portions; it is not copyleft.

    :material-book-open-variant: [Docs](https://opensource.org/license/mit)

??? question "7. Does the MIT license grant rights to use the Symfony name and logo?"
    **✅ No — those are governed by the separate trademark policy**

    The code license (MIT) and the trademark (name/logo) are separate legal instruments. Using the Symfony name/logo follows Symfony SAS's trademark policy.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

??? question "8. What best describes a Symfony component?"
    **✅ A standalone, reusable PHP library shipped as its own Composer package**

    Components are decoupled libraries, each independently versioned and usable without the full framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

??? question "9. What do the symfony/*-contracts packages contain?"
    **✅ Stable interfaces and traits to depend on**

    Contracts packages hold interface-only definitions so consumers can depend on a stable API decoupled from a concrete implementation.

    :material-book-open-variant: [Docs](https://github.com/symfony/contracts)

??? question "10. Can symfony/routing be used without FrameworkBundle?"
    **✅ Yes — it is a standalone component**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

??? question "11. What is a Symfony bridge?"
    **✅ An integration layer between a component and a specific third-party library**

    A bridge holds the glue coupling a Symfony component to one specific external library, keeping the component itself dependency-free.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

??? question "12. Where do bridges live in the Symfony monorepo?"
    **✅ src/Symfony/Bridge/**

    Bridges have their own top-level directory, distinct from Component and Bundle.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony)

??? question "13. What typically activates a bridge inside a framework application?"
    **✅ A bundle that registers the bridge's classes as services**

    Bridges provide classes; a bundle wires them into the container and exposes configuration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

??? question "14. Which directory is the web root of a Symfony application?"
    **✅ public/**

    public/ contains index.php and static assets and is the only web-accessible directory.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

??? question "15. Where are bundles enabled in a modern Symfony app?"
    **✅ config/bundles.php**

    config/bundles.php maps each bundle class to the environments where it is enabled; the kernel reads it via MicroKernelTrait.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

??? question "16. What supplies registerBundles() and registerContainerConfiguration() in a skeleton Kernel?"
    **✅ MicroKernelTrait**

    App\\Kernel uses MicroKernelTrait, which implements the boilerplate to load bundles from config/bundles.php and configuration from config/.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/micro_kernel_trait.html)

??? question "17. For a controller that returns a Response, in what order do the kernel events fire?"
    **✅ kernel.request -> kernel.controller -> kernel.controller_arguments -> kernel.response**

    kernel.view is skipped because a Response was returned; the remaining events follow the canonical order, then finish_request and terminate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "18. When is kernel.view dispatched?"
    **✅ Only when the controller returns a value that is not a Response**

    If the controller returns a non-Response value, kernel.view listeners must convert it into a Response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-view)

??? question "19. When is kernel.terminate dispatched?"
    **✅ After the response has been sent to the client, for the main request**

    terminate() runs after send() and is not called for sub-requests; it is ideal for slow post-response work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-terminate)

??? question "20. A listener calls setResponse() on kernel.request. What happens next?"
    **✅ The controller is skipped and flow continues at kernel.response**

    Setting a response on kernel.request short-circuits controller resolution; the response still passes through kernel.response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-request)

??? question "21. What is the value of HttpKernelInterface::MAIN_REQUEST?"
    **✅ 1 (and SUB_REQUEST is 2)**

    MAIN_REQUEST is 1 and SUB_REQUEST is 2; the old MASTER_REQUEST constant was removed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

??? question "22. Which event is responsible for turning an exception into a response?"
    **✅ kernel.exception**

    When an exception escapes handleRaw(), HttpKernel dispatches kernel.exception; listeners may set the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

??? question "23. What status code results from an uncaught plain \LogicException?"
    **✅ 500**

    Only exceptions implementing HttpExceptionInterface carry a status; any other exception defaults to 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "24. At what priority is the default ErrorListener registered on kernel.exception?"
    **✅ -128, so custom listeners run first**

    ErrorListener runs at a low priority (-128) so your own exception listeners get the first chance to handle the throwable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

??? question "25. Where do you override the default 404 error template?"
    **✅ templates/bundles/TwigBundle/Exception/error404.html.twig**

    TwigBundle resolves error templates from templates/bundles/TwigBundle/Exception/, falling back to error.html.twig.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "26. What does a higher listener priority mean?"
    **✅ It runs earlier**

    Listeners are sorted by priority in descending order, so higher priorities run first; the default priority is 0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "27. What is the dispatch() signature in Symfony 8 (PSR-14)?"
    **✅ dispatch(object $event, ?string $eventName = null)**

    Symfony follows PSR-14: the event object comes first, the name is optional (defaults to the event's class name).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "28. Which method must an event subscriber implement?"
    **✅ public static function getSubscribedEvents(): array**

    EventSubscriberInterface defines the static getSubscribedEvents() method returning event names mapped to handlers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

??? question "29. What does $event->stopPropagation() do?"
    **✅ Prevents the remaining listeners of this event from running**

    It sets a flag the dispatcher checks before each listener; only the current event's remaining listeners are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "30. Where should business logic live according to the best practices?"
    **✅ In autowired services**

    Controllers should be thin and delegate to services, which keeps logic reusable and testable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/best_practices.html)

??? question "31. What visibility should application services have by default?"
    **✅ Private**

    Private services let the DI compiler inline and remove them, and discourage the service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "32. Where do sensitive credentials belong?"
    **✅ The Secrets vault**

    Secrets should be stored in the encrypted Secrets vault, while infrastructure config uses env vars and behaviour uses parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/secrets.html)

??? question "33. How often does a new Symfony minor version ship?"
    **✅ Every six months, in May and November**

    Symfony uses a fixed time-based cadence: a minor every May and November, a major every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "34. Which Symfony 8.x version is the LTS?"
    **✅ 8.4**

    The last minor of each major (X.4) is the LTS; it ships alongside the next major (9.0).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

??? question "35. What may a MINOR release NOT do?"
    **✅ Break backward compatibility**

    Minors add features and deprecations but never break BC; breaks are reserved for major releases.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "36. What are the maintenance windows for a standard (non-LTS) release?"
    **✅ 8 months of bug fixes and 14 months of security fixes**

    Standard versions get 8 months bug fixes and 14 months security fixes; LTS versions get 3 years and 4 years respectively.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "37. When may Symfony break backward compatibility?"
    **✅ Only in a major release, and only after prior deprecation**

    BC breaks are reserved for majors and require the affected API to have been deprecated in the previous major line.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "38. What does the @internal marker mean for the BC promise?"
    **✅ The element is excluded from the BC promise and may change at any time**

    @internal marks implementation details not covered by BC, even if they are PHP-public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "39. How should you customise a final Symfony class in a BC-safe way?"
    **✅ Decorate or compose it**

    final classes must not be subclassed; wrap them via decoration so Symfony can change internals without breaking you.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "40. Which function emits a Symfony deprecation notice, and from which package?"
    **✅ trigger_deprecation() from symfony/deprecation-contracts**

    symfony/deprecation-contracts provides trigger_deprecation($package, $version, $message, ...$args), which formats an E_USER_DEPRECATED notice.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "41. When is deprecated code actually removed?"
    **✅ In the next major release**

    Deprecations survive the whole major line and are only removed in the next major, per the BC promise.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

??? question "42. Which tool lets you fail the test suite when new deprecations appear?"
    **✅ symfony/phpunit-bridge configured via SYMFONY_DEPRECATIONS_HELPER**

    The PHPUnit bridge collects deprecations; SYMFONY_DEPRECATIONS_HELPER (e.g. max[total]=0) can make the suite fail on any deprecation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

??? question "43. What is the argument order of trigger_deprecation()?"
    **✅ package, version, message, ...args**

    The signature is trigger_deprecation(string $package, string $version, string $message, mixed ...$args) with sprintf-style formatting.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

??? question "44. Where do you place a template that overrides a bundle template?"
    **✅ templates/bundles/<BundleName>/path.html.twig**

    Twig resolves overrides from templates/bundles/<BundleName>/, which takes precedence over the bundle's own templates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

??? question "45. What is the current mechanism to override an inherited bundle resource?"
    **✅ Per-resource overriding of templates, services, translations and config**

    Bundle inheritance via getParent() was deprecated in 4.4 and removed in 5.0; modern Symfony overrides each resource type individually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

??? question "46. How do you augment a bundle service without replacing it?"
    **✅ Decorate it with #[AsDecorator] / the decorates: key**

    Decoration wraps the original service (injected as .inner), letting you add behaviour and delegate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "47. In which months do Symfony minor releases ship?"
    **✅ May and November**

    The cadence is fixed: a new minor every May and every November.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "48. When does 8.4 (LTS) release relative to 9.0?"
    **✅ At the same time (both November 2027)**

    The LTS (X.4) always ships together with the next major (X+1).0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

??? question "49. How often is a new major (and its LTS) released?"
    **✅ Every two years**

    Majors, and the accompanying LTS, come every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

??? question "50. Which PSR does Symfony's EventDispatcher implement?"
    **✅ PSR-14 (Event Dispatcher)**

    Symfony's EventDispatcherInterface extends the PSR-14 Psr\\EventDispatcher\\EventDispatcherInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

??? question "51. Is HttpFoundation's Request a PSR-7 message?"
    **✅ No — a psr-http-message bridge converts between them**

    HttpFoundation predates and differs from PSR-7; the psr-http-message bridge converts between HttpFoundation and PSR-7/15/17.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/psr7.html)

??? question "52. Which PSR interface does Symfony's service container implement?"
    **✅ PSR-11 (Container)**

    Symfony's ContainerInterface extends Psr\\Container\\ContainerInterface (PSR-11).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "53. Which PSR does Symfony primarily consume (rather than implement) so you can inject any implementation?"
    **✅ PSR-3 (Logger) via Psr\Log\LoggerInterface**

    Components type-hint Psr\\Log\\LoggerInterface (PSR-3), so any compliant logger can be injected. PSR-11, PSR-14, PSR-6 and PSR-20 are implemented by Symfony.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

??? question "54. How are application service IDs written in modern Symfony?"
    **✅ As the fully-qualified class name (FQCN)**

    The service id is the FQCN; autowiring matches type-hints to these ids.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "55. What naming case do environment variables use?"
    **✅ UPPER_SNAKE_CASE, usually with an APP_ prefix**

    Env vars use upper snake case (APP_ENV, APP_DEBUG) and are read in config via processors such as %env(int:APP_PAGE_SIZE)%.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

??? question "56. Which is a correctly named route?"
    **✅ invoice_show**

    Route names use snake_case, conventionally entity_action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "57. How is an abstract class conventionally named?"
    **✅ With an Abstract prefix, e.g. AbstractController**

    Abstract classes take the Abstract prefix; interfaces use the Interface suffix and traits use the Trait suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

---

<small>Back to [Flashcards](index.md) · [Symfony Architecture](../../architecture/index.md)</small>
