# Chapter Exam — Symfony Architecture

!!! abstract "How to use"
    122 questions spanning every subchapter of **Symfony Architecture**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Symfony Architecture](../architecture/index.md).

---

**Q1.** What kind of tool is Symfony Flex?  <small>_(easy · single)_</small>

- A. A Composer plugin that resolves aliases and applies recipes
- B. A runtime kernel event listener
- C. A templating engine

??? success "Answer Q1"
    **A**

    Flex is a Composer plugin. It runs at Composer install/update time, resolving package aliases and applying recipes; it has no role during HTTP request handling.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

**Q2.** What does the symfony.lock file track?  <small>_(easy · single)_</small>

- A. Which recipes are installed and their versions
- B. The compiled service container
- C. Locked HTTP sessions

??? success "Answer Q2"
    **A**

    symfony.lock records applied recipes so Flex can detect updates and reverse them; it is distinct from composer.lock (package versions).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

**Q3.** In Flex terminology, what is the difference between an alias and a recipe?  <small>_(easy · trap)_</small>

- A. An alias is a short name that maps to a real package; a recipe is the automation (configurators) applied when that package is installed
- B. They are two words for the same lookup on the recipe server
- C. An alias applies config files; a recipe only renames the package

??? success "Answer Q3"
    **A**

    `composer require orm` uses the alias `orm`, which resolves to the real package `doctrine/orm`; the alias only affects the name written to composer.json. The recipe is the separate automation (bundles, copy-from-recipe, env, container configurators described in manifest.json) that wires the package into your app. Aliases are convenience; recipes are the work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

**Q4.** Under which license is Symfony released?  <small>_(easy · single)_</small>

- A. MIT
- B. GPLv3
- C. Apache 2.0

??? success "Answer Q4"
    **A**

    Symfony components are released under the permissive, non-copyleft MIT license.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/LICENSE)

**Q5.** What is the core obligation of the MIT license?  <small>_(easy · single)_</small>

- A. Retain the copyright and permission notice in copies
- B. Publish all your source code
- C. Pay a royalty per deployment

??? success "Answer Q5"
    **A**

    MIT only requires that the copyright and permission notice be kept in all copies or substantial portions; it is not copyleft.

    :material-book-open-variant: [Docs](https://opensource.org/license/mit)

**Q6.** True or false: because Symfony is MIT-licensed, you must open-source any application you build on it.  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q6"
    **A**

    False. MIT is permissive, not copyleft (unlike the GPL). You may ship Symfony inside closed-source, proprietary products without releasing your own source; the only condition is retaining the copyright/permission notice.

    :material-book-open-variant: [Docs](https://opensource.org/license/mit)

**Q7.** What best describes a Symfony component?  <small>_(easy · single)_</small>

- A. A standalone, reusable PHP library shipped as its own Composer package
- B. A configuration file loaded by the kernel
- C. A bundle that can only run inside the framework

??? success "Answer Q7"
    **A**

    Components are decoupled libraries, each independently versioned and usable without the full framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

**Q8.** Can symfony/routing be used without FrameworkBundle?  <small>_(easy · true-false)_</small>

- A. Yes — it is a standalone component
- B. No — it requires the kernel
- C. Only in the dev environment

??? success "Answer Q8"
    **A**

    Components are decoupled; Routing can be installed and used on its own via UrlMatcher/UrlGenerator without the framework.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

**Q9.** What is a Symfony bridge?  <small>_(easy · single)_</small>

- A. An integration layer between a component and a specific third-party library
- B. A configuration file format
- C. A replacement for the service container

??? success "Answer Q9"
    **A**

    A bridge holds the glue coupling a Symfony component to one specific external library, keeping the component itself dependency-free.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

**Q10.** Which directory is the web root of a Symfony application?  <small>_(easy · single)_</small>

- A. public/
- B. src/
- C. web/

??? success "Answer Q10"
    **A**

    public/ contains index.php and static assets and is the only web-accessible directory.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

**Q11.** Where are bundles enabled in a modern Symfony app?  <small>_(easy · single)_</small>

- A. config/bundles.php
- B. config/services.yaml
- C. Manually in src/Kernel.php

??? success "Answer Q11"
    **A**

    config/bundles.php maps each bundle class to the environments where it is enabled; the kernel reads it via MicroKernelTrait.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q12.** Which event is responsible for turning an exception into a response?  <small>_(easy · single)_</small>

- A. kernel.exception
- B. kernel.view
- C. kernel.terminate

??? success "Answer Q12"
    **A**

    When an exception escapes handleRaw(), HttpKernel dispatches kernel.exception; listeners may set the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q13.** Which built-in exception produces a 404 response?  <small>_(easy · single)_</small>

- A. NotFoundHttpException
- B. AccessDeniedHttpException
- C. BadRequestHttpException

??? success "Answer Q13"
    **A**

    NotFoundHttpException maps to 404. AccessDeniedHttpException maps to 403 and BadRequestHttpException to 400. All implement HttpExceptionInterface, so their status code and headers flow through to the produced response; a generic HttpException takes any status code from its constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q14.** What does a higher listener priority mean?  <small>_(easy · single)_</small>

- A. It runs earlier
- B. It runs later
- C. It cannot be stopped

??? success "Answer Q14"
    **A**

    Listeners are sorted by priority in descending order, so higher priorities run first; the default priority is 0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q15.** What is the key difference between a listener and a subscriber?  <small>_(easy · single)_</small>

- A. A listener is registered against one event; a subscriber declares all the events it handles in getSubscribedEvents()
- B. A subscriber can only handle one event; a listener handles many
- C. Listeners run at runtime while subscribers run at compile time

??? success "Answer Q15"
    **A**

    A listener is a callable attached to a single event name (via #[AsEventListener] or the kernel.event_listener tag). A subscriber implements EventSubscriberInterface and declares all its events (and priorities) in the static getSubscribedEvents() method — handy when one class handles several related events. Both are wired by RegisterListenersPass.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

**Q16.** Where should business logic live according to the best practices?  <small>_(easy · single)_</small>

- A. In autowired services
- B. In controllers
- C. In Twig templates

??? success "Answer Q16"
    **A**

    Controllers should be thin and delegate to services, which keeps logic reusable and testable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/best_practices.html)

**Q17.** How often does a new Symfony minor version ship?  <small>_(easy · single)_</small>

- A. Every six months, in May and November
- B. Every month
- C. Every two years

??? success "Answer Q17"
    **A**

    Symfony uses a fixed time-based cadence: a minor every May and November, a major every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q18.** Which Symfony 8.x version is the LTS?  <small>_(easy · single)_</small>

- A. 8.4
- B. 8.0
- C. 8.2

??? success "Answer Q18"
    **A**

    The last minor of each major (X.4) is the LTS; it ships alongside the next major (9.0).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

**Q19.** True or false: a method declared public in PHP but annotated @internal is protected by the BC promise.  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q19"
    **A**

    False. @internal explicitly removes an element from the BC promise even when it is PHP-public. Such methods/classes can change or disappear in any release, so you must not depend on them. PHP visibility and BC coverage are independent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q20.** When is deprecated code actually removed?  <small>_(easy · single)_</small>

- A. In the next major release
- B. In the next patch release
- C. Immediately

??? success "Answer Q20"
    **A**

    Deprecations survive the whole major line and are only removed in the next major, per the BC promise.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q21.** In which months do Symfony minor releases ship?  <small>_(easy · single)_</small>

- A. May and November
- B. January and July
- C. March and September

??? success "Answer Q21"
    **A**

    The cadence is fixed: a new minor every May and every November.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q22.** How often is a new major (and its LTS) released?  <small>_(easy · single)_</small>

- A. Every two years
- B. Every six months
- C. Every year

??? success "Answer Q22"
    **A**

    Majors, and the accompanying LTS, come every two years.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q23.** Which PSR does Symfony's EventDispatcher implement?  <small>_(easy · single)_</small>

- A. PSR-14 (Event Dispatcher)
- B. PSR-7 (HTTP Message)
- C. PSR-3 (Logger)

??? success "Answer Q23"
    **A**

    Symfony's EventDispatcherInterface extends the PSR-14 Psr\\EventDispatcher\\EventDispatcherInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q24.** Which PSR interface does Symfony's service container implement?  <small>_(easy · single)_</small>

- A. PSR-11 (Container)
- B. PSR-6 (Cache)
- C. PSR-16 (Simple Cache)

??? success "Answer Q24"
    **A**

    Symfony's ContainerInterface extends Psr\\Container\\ContainerInterface (PSR-11).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q25.** How are application service IDs written in modern Symfony?  <small>_(easy · single)_</small>

- A. As the fully-qualified class name (FQCN)
- B. As lowercase dotted strings only
- C. As random UUIDs

??? success "Answer Q25"
    **A**

    The service id is the FQCN; autowiring matches type-hints to these ids.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q26.** What naming case do environment variables use?  <small>_(easy · single)_</small>

- A. UPPER_SNAKE_CASE, usually with an APP_ prefix
- B. camelCase
- C. kebab-case

??? success "Answer Q26"
    **A**

    Env vars use upper snake case (APP_ENV, APP_DEBUG) and are read in config via processors such as %env(int:APP_PAGE_SIZE)%.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html)

**Q27.** How does a recipe auto-register a bundle?  <small>_(medium · single)_</small>

- A. By writing an entry into config/bundles.php
- B. Via an #[AsBundle] attribute
- C. By editing services.yaml

??? success "Answer Q27"
    **A**

    The bundles configurator adds the bundle class to config/bundles.php, which the kernel reads at boot via MicroKernelTrait::registerBundles().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q28.** Which repository holds the community (opt-in) recipes?  <small>_(medium · single)_</small>

- A. symfony/recipes-contrib
- B. symfony/recipes
- C. symfony/flex-recipes

??? success "Answer Q28"
    **A**

    Curated recipes live in symfony/recipes; community recipes live in symfony/recipes-contrib and require enabling extra.symfony.allow-contrib.

    :material-book-open-variant: [Docs](https://github.com/symfony/recipes-contrib)

**Q29.** Which statement about symfony.lock vs composer.lock is correct?  <small>_(medium · trap)_</small>

- A. symfony.lock records applied recipes; composer.lock records resolved package versions — both are committed
- B. symfony.lock replaces composer.lock and makes it optional
- C. Both files should be git-ignored because Flex regenerates them
- D. symfony.lock stores package versions and composer.lock stores recipes

??? success "Answer Q29"
    **A**

    The two files are complementary, not interchangeable. composer.lock pins resolved package versions (Composer's job); symfony.lock pins which recipe versions were applied (Flex's job) so every teammate/CI reproduces the same config and Flex can detect/rollback recipe changes. Both must be committed. The common trap is thinking one supersedes the other or that they should be ignored.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

**Q30.** At which point in a project's lifecycle does Symfony Flex actually run?  <small>_(medium · internals)_</small>

- A. Only at Composer time — it subscribes to Composer events like post-install-cmd/post-update-cmd and package install/uninstall
- B. On every HTTP request, as a high-priority kernel.request listener
- C. At container compile time, as a Symfony compiler pass
- D. At kernel.terminate, after the response is sent

??? success "Answer Q30"
    **A**

    Flex is a Composer plugin that hooks Composer's event system; when a package is installed/updated/removed it resolves aliases and applies (or reverses) the matching recipe's configurators. It writes files (config/, .env, bundles.php) but plays no part in the HTTP runtime, the DI compiler, or terminate — those read the files Flex produced.

    :material-book-open-variant: [Docs](https://github.com/symfony/flex)

**Q31.** Does the MIT license grant rights to use the Symfony name and logo?  <small>_(medium · single)_</small>

- A. No — those are governed by the separate trademark policy
- B. Yes — the license covers name and logo
- C. Only for non-commercial use

??? success "Answer Q31"
    **A**

    The code license (MIT) and the trademark (name/logo) are separate legal instruments. Using the Symfony name/logo follows Symfony SAS's trademark policy.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

**Q32.** A startup ships a closed-source SaaS built on Symfony and wants to market it as "SymfonyCloud". Which part is a problem?  <small>_(medium · scenario)_</small>

- A. The closed-source SaaS is fine under MIT, but naming it "SymfonyCloud" risks trademark infringement
- B. Both are forbidden: MIT bans commercial use and the name is trademarked
- C. Neither is a problem: MIT grants full rights to the Symfony name too

??? success "Answer Q32"
    **A**

    MIT permits commercial, closed-source use, so building the SaaS is fine. But the code license says nothing about names/logos: using \"Symfony\" in a product name is governed by Symfony SAS's trademark policy, so \"SymfonyCloud\" is the risky part. You may say \"built with Symfony\" but not brand as Symfony.

    :material-book-open-variant: [Docs](https://symfony.com/trademark)

**Q33.** What do the symfony/*-contracts packages contain?  <small>_(medium · single)_</small>

- A. Stable interfaces and traits to depend on
- B. Compiled service containers
- C. Twig templates

??? success "Answer Q33"
    **A**

    Contracts packages hold interface-only definitions so consumers can depend on a stable API decoupled from a concrete implementation.

    :material-book-open-variant: [Docs](https://github.com/symfony/contracts)

**Q34.** Which mapping of term to definition is entirely correct?  <small>_(medium · trap)_</small>

- A. Contract = interfaces/traits; Component = standalone library; Bridge = glue to a third-party lib; Bundle = framework wiring
- B. Contract = compiled container; Component = a bundle; Bridge = a config file; Bundle = a PSR
- C. Component = interfaces only; Contract = implementation; Bundle = third-party glue; Bridge = framework config

??? success "Answer Q34"
    **A**

    The four layers are distinct: contracts (e.g. symfony/service-contracts) ship only interfaces/traits; components (e.g. symfony/routing) are standalone implementations; bridges (e.g. symfony/twig-bridge) glue a component to one specific third-party library; bundles (e.g. symfony/framework-bundle) wire things into the framework with services and config. Confusing bridge with bundle, or contract with component, is the classic exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

**Q35.** Using only the Routing component standalone, what does $matcher->match('/hello/sf') return for a route defined as new Route('/hello/{name}') named 'hello'?  <small>_(medium · code)_</small>

- A. ['_route' => 'hello', 'name' => 'sf']
- B. A Response object with body 'sf'
- C. true
- D. Nothing — UrlMatcher needs the kernel to resolve routes

??? success "Answer Q35"
    **A**

    UrlMatcher::match() returns an array of the matched route's parameters, including the special _route key with the route name and any placeholder values. No framework or kernel is involved — the component works standalone with a RouteCollection and a RequestContext. It returns parameters, never a Response (that is the framework's job).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/routing.html)

**Q36.** For a modern application, how should you depend on Symfony code?  <small>_(medium · trap)_</small>

- A. Require the individual packages you need (e.g. symfony/routing); the symfony/symfony metapackage is discouraged
- B. Always require the symfony/symfony metapackage to get everything at once
- C. Require symfony/framework-bundle only, which contains every component's source

??? success "Answer Q36"
    **A**

    You should require only the individual component/bundle packages you use so the dependency graph stays minimal and each package versions independently. The old symfony/symfony monolithic metapackage is discouraged. Type-hinting contracts/interfaces further decouples you from concrete implementations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/index.html)

**Q37.** Where do bridges live in the Symfony monorepo?  <small>_(medium · single)_</small>

- A. src/Symfony/Bridge/
- B. src/Symfony/Component/
- C. src/Symfony/Bundle/

??? success "Answer Q37"
    **A**

    Bridges have their own top-level directory, distinct from Component and Bundle.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony)

**Q38.** What typically activates a bridge inside a framework application?  <small>_(medium · single)_</small>

- A. A bundle that registers the bridge's classes as services
- B. The bridge auto-registers itself at runtime
- C. A Twig template include

??? success "Answer Q38"
    **A**

    Bridges provide classes; a bundle wires them into the container and exposes configuration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q39.** Which statement distinguishes a bridge from a bundle correctly?  <small>_(medium · trap)_</small>

- A. A bridge is a glue library (classes) coupling a component to one third-party lib; a bundle registers services and config in the framework
- B. A bridge configures itself in the framework; a bundle only provides plain classes
- C. They are the same thing under two names

??? success "Answer Q39"
    **A**

    A bridge is just a Composer library of adapter/glue classes that depends on a component plus one specific external library; it does not wire itself into any app. A bundle is the framework-integration layer that registers those classes as services and exposes configuration. Expecting a bridge to configure itself is the trap — that is a bundle's job.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

**Q40.** What supplies registerBundles() and registerContainerConfiguration() in a skeleton Kernel?  <small>_(medium · single)_</small>

- A. MicroKernelTrait
- B. AbstractController
- C. The FrameworkBundle extension

??? success "Answer Q40"
    **A**

    App\\Kernel uses MicroKernelTrait, which implements the boilerplate to load bundles from config/bundles.php and configuration from config/.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/micro_kernel_trait.html)

**Q41.** In config/bundles.php an entry reads `WebProfilerBundle::class => ['dev' => true, 'test' => true]`. What does this mean?  <small>_(medium · config)_</small>

- A. The bundle is enabled only in the dev and test environments, not in prod
- B. The bundle runs in all environments because at least one is true
- C. The bundle is disabled everywhere until you add 'all' => true

??? success "Answer Q41"
    **A**

    config/bundles.php maps each bundle class to an array of environment => bool. The kernel enables the bundle only in the listed environments whose value is true. `['all' => true]` means every environment; `['dev' => true, 'test' => true]` means dev and test only (typical for debugging/profiling bundles).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles.html)

**Q42.** In prod, why is public/index.php fast and free of YAML parsing on the hot path?  <small>_(medium · internals)_</small>

- A. config/ is parsed at compile time into a dumped container in var/cache/<env>/; runtime only loads that compiled container
- B. The kernel re-parses config/packages/*.yaml on every request but caches the result in APCu
- C. index.php inlines all YAML as PHP arrays that are re-evaluated per request

??? success "Answer Q42"
    **A**

    Configuration is compiled once into a dumped PHP container under var/cache/<env>/. In prod the kernel simply loads that compiled container, so no YAML parsing happens per request — that is why the front controller stays tiny and the hot path is fast. In dev, ConfigCache checks freshness and rebuilds when source config changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/micro_kernel_trait.html)

**Q43.** How does a modern (Symfony 8) bundle inherit and override another bundle's resources?  <small>_(medium · trap)_</small>

- A. It doesn't — bundle inheritance via getParent() was removed; you override each resource type individually
- B. By implementing getParent() to return the parent bundle's name
- C. By extending the parent bundle class and calling parent::build()

??? success "Answer Q43"
    **A**

    The getParent() bundle-inheritance mechanism was deprecated in 4.4 and removed in 5.0; it does not exist in Symfony 8. Modern apps override each resource type on its own (templates via templates/bundles/<Name>/, services via decoration/redefinition, config via config/packages/). Mentioning getParent() as a current mechanism is a planted trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

**Q44.** What does the default `App\:` service definition with `resource: '../src/'` and `exclude: '../src/{Kernel.php}'` achieve?  <small>_(medium · config)_</small>

- A. It auto-registers every class under src/ as a service (with autowire/autoconfigure defaults), excluding Kernel.php
- B. It marks all src/ classes public so they can be fetched from the container
- C. It imports src/ as a Composer autoload path at runtime

??? success "Answer Q44"
    **A**

    The resource glob discovers classes under src/ and registers each as a service whose id is its FQCN, inheriting the _defaults (autowire: true, autoconfigure: true). exclude keeps non-service classes (like Kernel.php, entities, DTOs) out. Unused private services are then pruned by the compiler. It does not make them public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q45.** For a controller that returns a Response, in what order do the kernel events fire?  <small>_(medium · internals)_</small>

- A. kernel.request -> kernel.controller -> kernel.controller_arguments -> kernel.response
- B. kernel.request -> kernel.view -> kernel.controller -> kernel.response
- C. kernel.controller -> kernel.request -> kernel.response -> kernel.terminate

??? success "Answer Q45"
    **A**

    kernel.view is skipped because a Response was returned; the remaining events follow the canonical order, then finish_request and terminate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q46.** When is kernel.view dispatched?  <small>_(medium · single)_</small>

- A. Only when the controller returns a value that is not a Response
- B. On every request
- C. Only for sub-requests

??? success "Answer Q46"
    **A**

    If the controller returns a non-Response value, kernel.view listeners must convert it into a Response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-view)

**Q47.** When is kernel.terminate dispatched?  <small>_(medium · internals)_</small>

- A. After the response has been sent to the client, for the main request
- B. Before kernel.response
- C. Once for every sub-request

??? success "Answer Q47"
    **A**

    terminate() runs after send() and is not called for sub-requests; it is ideal for slow post-response work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-terminate)

**Q48.** A listener calls setResponse() on kernel.request. What happens next?  <small>_(medium · scenario)_</small>

- A. The controller is skipped and flow continues at kernel.response
- B. The controller still runs normally
- C. A kernel.view event becomes mandatory

??? success "Answer Q48"
    **A**

    Setting a response on kernel.request short-circuits controller resolution; the response still passes through kernel.response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-request)

**Q49.** What is the value of HttpKernelInterface::MAIN_REQUEST?  <small>_(medium · internals)_</small>

- A. 1 (and SUB_REQUEST is 2)
- B. 0
- C. It is still called MASTER_REQUEST

??? success "Answer Q49"
    **A**

    MAIN_REQUEST is 1 and SUB_REQUEST is 2; the old MASTER_REQUEST constant was removed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q50.** What are the respective jobs of ControllerResolverInterface and ArgumentResolverInterface?  <small>_(medium · internals)_</small>

- A. ControllerResolver reads the _controller attribute and returns a callable; ArgumentResolver builds the ordered argument array via value resolvers
- B. ControllerResolver builds the argument array; ArgumentResolver picks the route
- C. Both resolve the route; the controller is chosen by the router directly

??? success "Answer Q50"
    **A**

    ControllerResolverInterface::getController(Request) reads the _controller request attribute (set by the router) and returns a PHP callable. ArgumentResolverInterface::getArguments() then runs a chain of ValueResolverInterface resolvers (request attributes, the Request object, #[MapRequestPayload], services, variadics, defaults) to build the ordered argument list passed to the controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q51.** A controller does its work but has no return statement (returns null) and no kernel.view listener handles it. What happens?  <small>_(medium · debug)_</small>

- A. The kernel dispatches kernel.view; since no response is set, it throws ControllerDoesNotReturnResponseException
- B. The kernel silently sends an empty 200 response
- C. A fatal PHP TypeError is raised before any event fires

??? success "Answer Q51"
    **A**

    After the controller runs, handleRaw() checks whether the return value is a Response; if not, it dispatches kernel.view carrying the value. If no listener calls setResponse(), the kernel throws ControllerDoesNotReturnResponseException (a LogicException) with the familiar \"The controller must return a Response object but it returned null\" message. The fix is to return a real Response or register a view listener.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q52.** Which statement about sub-requests is correct?  <small>_(medium · internals)_</small>

- A. They run the same request→...→finish_request flow but never fire kernel.terminate; RequestStack push/pop restores parent state
- B. They fire kernel.terminate once per sub-request, like the main request
- C. They skip kernel.request and start directly at kernel.controller

??? success "Answer Q52"
    **A**

    A sub-request (HttpKernelInterface::SUB_REQUEST) runs the full linear flow from kernel.request through kernel.response and kernel.finish_request, but kernel.terminate fires only for the main request after send. handleRaw() pushes the sub-request onto the RequestStack before kernel.request and pops it after kernel.finish_request, restoring the parent request/locale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q53.** A listener is annotated #[AsEventListener(event: KernelEvents::RESPONSE, priority: -10)] and sets an X-Frame-Options header. When does it run?  <small>_(medium · code)_</small>

- A. On every response passing through kernel.response, after listeners with higher priority (since -10 is below the default 0)
- B. Only when the controller returns a non-Response value
- C. Before the controller is called, during kernel.request

??? success "Answer Q53"
    **A**

    kernel.response fires for every response (whether from the controller, a view listener, or a short-circuit). Listeners run high priority first; priority -10 is below the default 0, so this header listener runs relatively late. The #[AsEventListener] attribute is wired by RegisterListenersPass at compile time, replacing manual tagging.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-response)

**Q54.** What status code results from an uncaught plain \LogicException?  <small>_(medium · single)_</small>

- A. 500
- B. 404
- C. 400

??? success "Answer Q54"
    **A**

    Only exceptions implementing HttpExceptionInterface carry a status; any other exception defaults to 500.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q55.** At what priority is the default ErrorListener registered on kernel.exception?  <small>_(medium · internals)_</small>

- A. -128, so custom listeners run first
- B. 1024, so it always runs first
- C. 0

??? success "Answer Q55"
    **A**

    ErrorListener runs at a low priority (-128) so your own exception listeners get the first chance to handle the throwable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q56.** Where do you override the default 404 error template?  <small>_(medium · config)_</small>

- A. templates/bundles/TwigBundle/Exception/error404.html.twig
- B. templates/error/404.twig
- C. Directly in vendor/

??? success "Answer Q56"
    **A**

    TwigBundle resolves error templates from templates/bundles/TwigBundle/Exception/, falling back to error.html.twig.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q57.** After kernel.exception is dispatched, what does the kernel do if no listener set a response?  <small>_(medium · internals)_</small>

- A. handleThrowable() sees hasResponse() is false and re-throws the original throwable (which surfaces as a 500 when catch is true)
- B. It returns an empty Response with status 204
- C. It automatically retries the controller once more

??? success "Answer Q57"
    **A**

    If ExceptionEvent has no response after dispatch, handleThrowable() re-throws the original exception. In practice ErrorListener (priority -128) fills the gap, so this null case only bites when you replace or disable it. With catch:true the re-thrown error becomes a 500 to the client.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernel.php)

**Q58.** What is the dispatch() signature in Symfony 8 (PSR-14)?  <small>_(medium · internals)_</small>

- A. dispatch(object $event, ?string $eventName = null)
- B. dispatch(string $eventName, Event $event)
- C. dispatch(Event $event, string $eventName) with a required name

??? success "Answer Q58"
    **A**

    Symfony follows PSR-14: the event object comes first, the name is optional (defaults to the event's class name).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q59.** Which method must an event subscriber implement?  <small>_(medium · single)_</small>

- A. public static function getSubscribedEvents(): array
- B. public function subscribe(): array
- C. It only needs the #[AsEventSubscriber] attribute

??? success "Answer Q59"
    **A**

    EventSubscriberInterface defines the static getSubscribedEvents() method returning event names mapped to handlers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

**Q60.** What does $event->stopPropagation() do?  <small>_(medium · single)_</small>

- A. Prevents the remaining listeners of this event from running
- B. Cancels the whole request
- C. Removes the listener permanently

??? success "Answer Q60"
    **A**

    It sets a flag the dispatcher checks before each listener; only the current event's remaining listeners are skipped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q61.** Which are valid return values from getSubscribedEvents() for a single event? (choose all that apply)  <small>_(medium · code)_</small>

- A. [KernelEvents::RESPONSE => 'onResponse']
- B. [KernelEvents::RESPONSE => ['onResponse', -10]]
- C. [KernelEvents::RESPONSE => [['onFirst', 10], ['onSecond', -10]]]
- D. ['onResponse' => KernelEvents::RESPONSE]

??? success "Answer Q61"
    **A, B, C**

    getSubscribedEvents() maps event NAMES to handlers. The value may be a method name string, a [method, priority] pair, or a list of such pairs to register several handlers for the same event. Mapping method → event name (reversed) is wrong and a frequent mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

**Q62.** Two listeners for the same event both use the default priority. In what order do they run?  <small>_(medium · internals)_</small>

- A. In registration order — the default priority is 0 and equal priorities preserve the order they were added
- B. In reverse registration order (last added runs first)
- C. Alphabetically by service id

??? success "Answer Q62"
    **A**

    The default priority is 0. Listeners are sorted by priority descending, and ties (equal priority) keep their registration order. So two default-priority listeners run first-registered-first. To force an order, set explicit priorities rather than relying on registration order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q63.** What visibility should application services have by default?  <small>_(medium · single)_</small>

- A. Private
- B. Public
- C. Protected

??? success "Answer Q63"
    **A**

    Private services let the DI compiler inline and remove them, and discourage the service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q64.** Where do sensitive credentials belong?  <small>_(medium · single)_</small>

- A. The Secrets vault
- B. config/services.yaml
- C. Hard-coded parameters

??? success "Answer Q64"
    **A**

    Secrets should be stored in the encrypted Secrets vault, while infrastructure config uses env vars and behaviour uses parameters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/secrets.html)

**Q65.** What does this services.yaml _defaults block enable: autowire: true, autoconfigure: true, public: false?  <small>_(medium · config)_</small>

- A. Constructor deps are injected by type, services are auto-tagged by the interfaces they implement, and services are private by default
- B. All services become public singletons that can be fetched from the container
- C. It disables the compiler so services are resolved at runtime

??? success "Answer Q65"
    **A**

    autowire resolves constructor arguments by type-hint; autoconfigure auto-tags services based on implemented interfaces/attributes (e.g. subscribers get kernel.event_subscriber); public: false keeps them private so the compiler can inline/prune them and you inject rather than fetch. This is the idiomatic Symfony 8 default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q66.** Where should each belong: a database URL, a feature toggle, and a third-party API private key?  <small>_(medium · scenario)_</small>

- A. Database URL → env var; feature toggle → parameter (or env var if it varies per env); API private key → Secrets vault
- B. All three → hard-coded parameters in services.yaml
- C. All three → the Secrets vault, committed to git

??? success "Answer Q66"
    **A**

    Infrastructure config that varies per environment (database URL) goes in env vars; application behaviour (feature toggle) goes in parameters, or an env var if it changes per environment; sensitive credentials (API private key) go in the encrypted Secrets vault — never committed as plain config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/secrets.html)

**Q67.** Why is making application services public "to be safe" discouraged?  <small>_(medium · trap)_</small>

- A. Public services block the DI compiler from inlining/removing them and invite the service-locator anti-pattern; private + injected is preferred
- B. Public services cannot be autowired at all
- C. Public services are slower because they are re-instantiated on every request

??? success "Answer Q67"
    **A**

    Marking services public prevents the compiler from optimising them away or inlining them, and encourages fetching from the container (service location) instead of dependency injection. The best practice is private, autowired services injected via the constructor. Public visibility is only needed in a few edge cases (e.g. legacy get() calls).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q68.** What may a MINOR release NOT do?  <small>_(medium · single)_</small>

- A. Break backward compatibility
- B. Add new features
- C. Introduce deprecations

??? success "Answer Q68"
    **A**

    Minors add features and deprecations but never break BC; breaks are reserved for major releases.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q69.** What are the maintenance windows for a standard (non-LTS) release?  <small>_(medium · single)_</small>

- A. 8 months of bug fixes and 14 months of security fixes
- B. 3 years of bug fixes and 4 years of security fixes
- C. 1 month of everything

??? success "Answer Q69"
    **A**

    Standard versions get 8 months bug fixes and 14 months security fixes; LTS versions get 3 years and 4 years respectively.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q70.** What is the difference between a PATCH and a MINOR release?  <small>_(medium · trap)_</small>

- A. A patch (8.0.1 → 8.0.2) contains bug fixes only; a minor (8.0 → 8.1) adds new features and deprecations but is still BC-safe
- B. A patch can add small features; a minor is only for security fixes
- C. Both may break BC as long as deprecations were added

??? success "Answer Q70"
    **A**

    Patch releases carry bug fixes only — no new features, no deprecations, no BC breaks. Minor releases add features and may introduce deprecations, but never break BC. Only majors break BC (by removing previously deprecated code). Confusing patch (bugs only) with minor (features) is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q71.** What is a MAJOR release uniquely allowed to do?  <small>_(medium · single)_</small>

- A. Remove deprecated code and break backward compatibility (only for APIs deprecated in the previous major line)
- B. Add features without any deprecation path
- C. Ship bug fixes only

??? success "Answer Q71"
    **A**

    A major (e.g. 8.x → 9.0) is the only release level permitted to break BC, and only for code that was deprecated during the previous major line. This is what lets you upgrade safely within a major and plan the jump across a major once you have cleared deprecations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q72.** When may Symfony break backward compatibility?  <small>_(medium · single)_</small>

- A. Only in a major release, and only after prior deprecation
- B. In any minor release
- C. In patch releases

??? success "Answer Q72"
    **A**

    BC breaks are reserved for majors and require the affected API to have been deprecated in the previous major line.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q73.** What does the @internal marker mean for the BC promise?  <small>_(medium · single)_</small>

- A. The element is excluded from the BC promise and may change at any time
- B. The element is extra stable
- C. The element is deprecated

??? success "Answer Q73"
    **A**

    @internal marks implementation details not covered by BC, even if they are PHP-public.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q74.** How should you customise a final Symfony class in a BC-safe way?  <small>_(medium · single)_</small>

- A. Decorate or compose it
- B. Subclass and override it
- C. Edit it in vendor/

??? success "Answer Q74"
    **A**

    final classes must not be subclassed; wrap them via decoration so Symfony can change internals without breaking you.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q75.** Is @experimental code covered by the BC promise?  <small>_(medium · trap)_</small>

- A. No — experimental features (often whole components in their first release) are explicitly excluded until marked stable
- B. Yes — everything shipped in a stable Symfony release is covered
- C. Only their public methods are covered, not their properties

??? success "Answer Q75"
    **A**

    @experimental features are excluded from the BC promise until they are stabilised; they may change in any release. Building critical paths on experimental code is risky. Along with @internal and final, @experimental is one of the markers that carve exceptions out of the promise.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/experimental.html)

**Q76.** Which of the following are covered by the BC promise? (choose all that apply)  <small>_(medium · multiple)_</small>

- A. A public method with no special annotation
- B. A public method marked @internal
- C. A class marked @experimental
- D. The stable public constructor of a non-final, non-internal class

??? success "Answer Q76"
    **A, D**

    Stable public API without @internal/@experimental is covered — regardless of being a method or constructor. @internal is excluded even though PHP-public, and @experimental is excluded until stabilised. The classic misconception is equating PHP `public` with \"covered\"; @internal overrides that.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q77.** Which function emits a Symfony deprecation notice, and from which package?  <small>_(medium · internals)_</small>

- A. trigger_deprecation() from symfony/deprecation-contracts
- B. deprecate() from symfony/http-kernel
- C. There is no helper; you must call trigger_error() directly

??? success "Answer Q77"
    **A**

    symfony/deprecation-contracts provides trigger_deprecation($package, $version, $message, ...$args), which formats an E_USER_DEPRECATED notice.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q78.** What is the argument order of trigger_deprecation()?  <small>_(medium · internals)_</small>

- A. package, version, message, ...args
- B. message, package, version
- C. version, package, message

??? success "Answer Q78"
    **A**

    The signature is trigger_deprecation(string $package, string $version, string $message, mixed ...$args) with sprintf-style formatting.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q79.** Which call correctly deprecates ReportBuilder::generate() (deprecated in your app version 8.1)?  <small>_(medium · code)_</small>

- A. trigger_deprecation('app/reports', '8.1', 'Using "%s::generate()" is deprecated, use "build()".', self::class);
- B. trigger_deprecation('Using generate() is deprecated', 'app/reports', '8.1');
- C. trigger_error('app/reports', '8.1', 'generate() is deprecated');

??? success "Answer Q79"
    **A**

    The signature is (package, version, message, ...args) with sprintf-style formatting for the message. The first option passes the package, the version it was deprecated IN, a message with a %s placeholder, and self::class as the arg. Putting the message first, or misusing trigger_error with these arguments, is wrong.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q80.** How do you mark a service as deprecated in config/services.yaml?  <small>_(medium · config)_</small>

- A. Add a `deprecated:` key with package, version and message under the service definition
- B. Set `public: deprecated` on the service
- C. Prefix the service id with an underscore

??? success "Answer Q80"
    **A**

    A service is deprecated via the `deprecated:` key (package/version/message), which maps to Definition::setDeprecated() and triggers a deprecation when the service is referenced. Container-level deprecations like this surface during cache:clear/compile time, whereas method-call deprecations fire at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection.html)

**Q81.** At what error level are Symfony deprecations emitted, and do they throw?  <small>_(medium · trap)_</small>

- A. They are E_USER_DEPRECATED notices — they do not throw unless your test suite/CI is configured to fail on them
- B. They throw a DeprecationException that halts execution immediately
- C. They are E_USER_ERROR, so the request always dies with a fatal error

??? success "Answer Q81"
    **A**

    trigger_deprecation() ultimately calls @trigger_error(..., E_USER_DEPRECATED), producing a notice that is logged/collected but does not interrupt execution. Only when tooling (e.g. the PHPUnit bridge via SYMFONY_DEPRECATIONS_HELPER) is configured to fail on deprecations does a deprecation cause a failure.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q82.** Where do you place a template that overrides a bundle template?  <small>_(medium · config)_</small>

- A. templates/bundles/<BundleName>/path.html.twig
- B. templates/override/path.html.twig
- C. Inside vendor/

??? success "Answer Q82"
    **A**

    Twig resolves overrides from templates/bundles/<BundleName>/, which takes precedence over the bundle's own templates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

**Q83.** What is the current mechanism to override an inherited bundle resource?  <small>_(medium · single)_</small>

- A. Per-resource overriding of templates, services, translations and config
- B. getParent() bundle inheritance
- C. Editing the bundle in vendor/

??? success "Answer Q83"
    **A**

    Bundle inheritance via getParent() was deprecated in 4.4 and removed in 5.0; modern Symfony overrides each resource type individually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

**Q84.** How do you augment a bundle service without replacing it?  <small>_(medium · single)_</small>

- A. Decorate it with #[AsDecorator] / the decorates: key
- B. Make it public and fetch it
- C. Use getParent()

??? success "Answer Q84"
    **A**

    Decoration wraps the original service (injected as .inner), letting you add behaviour and delegate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q85.** A bundle ships translations/messages.en.yaml and your app defines the same domain/locale in translations/. Whose strings win?  <small>_(medium · trap)_</small>

- A. The application's translations/ take priority over the bundle's translations
- B. The bundle's translations always win because they load first
- C. They merge alphabetically and the last key alphabetically wins

??? success "Answer Q85"
    **A**

    The application's translations/ directory has higher priority than any bundle's translations. Providing a catalogue with the same domain and locale overrides the bundle's strings — the same convention-based precedence used for template overrides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

**Q86.** What happened to bundle inheritance (getParent()) and the legacy Resources/ folder?  <small>_(medium · internals)_</small>

- A. getParent() inheritance was deprecated in 4.4 and removed in 5.0; modern bundles use top-level config/, templates/, translations/ instead of Resources/
- B. getParent() is still the recommended way to override bundle resources in Symfony 8
- C. Resources/ is now mandatory and getParent() was reinstated in 8.0

??? success "Answer Q86"
    **A**

    Bundle inheritance via getParent() is gone (deprecated 4.4, removed 5.0) and must not be presented as current. Modern bundles also drop the legacy Resources/ layout in favour of top-level config/, templates/ and translations/. Overriding is done per resource type instead.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

**Q87.** When does 8.4 (LTS) release relative to 9.0?  <small>_(medium · single)_</small>

- A. At the same time (both November 2027)
- B. One year before 9.0
- C. After 9.0

??? success "Answer Q87"
    **A**

    The LTS (X.4) always ships together with the next major (X+1).0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

**Q88.** Which sequence correctly lists the Symfony 8.x release dates?  <small>_(medium · single)_</small>

- A. 8.0 Nov 2025, 8.1 May 2026, 8.2 Nov 2026, 8.3 May 2027, 8.4 LTS Nov 2027
- B. 8.0 Jan 2025, 8.1 Jul 2025, 8.2 Jan 2026, 8.3 Jul 2026, 8.4 Jan 2027
- C. 8.0 Nov 2025, 8.1 Nov 2026, 8.2 Nov 2027, 8.3 Nov 2028, 8.4 Nov 2029

??? success "Answer Q88"
    **A**

    8.0 opened the cycle in Nov 2025; a minor lands every six months (May/Nov): 8.1 May 2026, 8.2 Nov 2026, 8.3 May 2027, and 8.4 (LTS) Nov 2027 alongside 9.0. The pattern repeats for every major: X.0 opens, four minors follow, X.4 is the LTS shipping with (X+1).0.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q89.** Which statement about the LTS timing is correct?  <small>_(medium · trap)_</small>

- A. The LTS (X.4) ships at the same time as the next major (X+1).0, not before it
- B. The LTS ships one year before the next major so people can migrate
- C. 8.0 is the long-term support release of the 8.x line

??? success "Answer Q89"
    **A**

    A frequent misconception is that the LTS precedes the next major. In fact X.4 (the LTS) and (X+1).0 release together (8.4 and 9.0 both Nov 2027). Another trap: 8.0 is a standard release, not the LTS — 8.4 is.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

**Q90.** A product must run 3+ years without a major upgrade. Which 8.x version should you target and why?  <small>_(medium · scenario)_</small>

- A. 8.4 (LTS) — it provides 3 years of bug fixes and 4 years of security fixes, the longest support window in 8.x
- B. 8.0 — being the first release it is supported the longest
- C. 8.2 — mid-cycle releases get extended support

??? success "Answer Q90"
    **A**

    Only the LTS (X.4) offers the long maintenance windows (3 years bug fixes, 4 years security fixes). Standard minors get 8 months bug + 14 months security, far short of 3 years. So a long-lived product should pin to 8.4 and plan the jump to the next major deliberately.

    :material-book-open-variant: [Docs](https://symfony.com/releases)

**Q91.** Is HttpFoundation's Request a PSR-7 message?  <small>_(medium · single)_</small>

- A. No — a psr-http-message bridge converts between them
- B. Yes, natively
- C. Only in the prod environment

??? success "Answer Q91"
    **A**

    HttpFoundation predates and differs from PSR-7; the psr-http-message bridge converts between HttpFoundation and PSR-7/15/17.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/psr7.html)

**Q92.** Which PSR does Symfony primarily consume (rather than implement) so you can inject any implementation?  <small>_(medium · internals)_</small>

- A. PSR-3 (Logger) via Psr\Log\LoggerInterface
- B. PSR-11 (Container)
- C. PSR-20 (Clock)

??? success "Answer Q92"
    **A**

    Components type-hint Psr\\Log\\LoggerInterface (PSR-3), so any compliant logger can be injected. PSR-11, PSR-14, PSR-6 and PSR-20 are implemented by Symfony.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

**Q93.** What is the difference between PSR-6 and PSR-16 in Symfony's Cache?  <small>_(medium · trap)_</small>

- A. PSR-6 is the pool/CacheItem model (CacheItemPoolInterface); PSR-16 is the simpler get/set SimpleCache API (Psr16Cache adapter)
- B. PSR-6 is for HTTP caching and PSR-16 is for the container
- C. They are the same interface at different versions

??? success "Answer Q93"
    **A**

    PSR-6 models caching as a pool of CacheItem objects (CacheItemPoolInterface::getItem()/save()); PSR-16 (Simple Cache) is a lighter get()/set()/delete() API, exposed by Symfony's Psr16Cache adapter. Confusing the pool/item model (PSR-6) with the simple key/value API (PSR-16) is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

**Q94.** Which PSR does Symfony's Clock component implement, and why inject its interface?  <small>_(medium · single)_</small>

- A. PSR-20 via Psr\Clock\ClockInterface — injecting it makes time testable instead of calling new \DateTime() directly
- B. PSR-7 — the clock produces HTTP timestamps
- C. PSR-11 — the clock is fetched from the container by id

??? success "Answer Q94"
    **A**

    Symfony\\Component\\Clock\\Clock implements Psr\\Clock\\ClockInterface (PSR-20). Type-hinting ClockInterface lets you inject a MockClock in tests and control time deterministically, instead of hard-coding new \\DateTime()/now() calls that are impossible to freeze.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q95.** What is the practical difference between Symfony implementing a PSR and consuming a PSR?  <small>_(medium · internals)_</small>

- A. Implementing means a Symfony object satisfies the PSR (hand it to any PSR consumer); consuming means Symfony type-hints the PSR so you can inject any implementation
- B. Implementing is done at runtime; consuming is done at compile time
- C. There is no difference — both mean Symfony ships the concrete class

??? success "Answer Q95"
    **A**

    Implements: Symfony's class IS a valid PSR object (e.g. its Container is a PSR-11 container), usable by any library expecting that interface. Consumes: Symfony depends on the PSR interface as a type-hint (e.g. PSR-3 LoggerInterface) so you can plug in any compliant implementation. The direction of the dependency is what differs.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

**Q96.** Which is a correctly named route?  <small>_(medium · single)_</small>

- A. invoice_show
- B. InvoiceShow
- C. invoice show

??? success "Answer Q96"
    **A**

    Route names use snake_case, conventionally entity_action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

**Q97.** How is an abstract class conventionally named?  <small>_(medium · single)_</small>

- A. With an Abstract prefix, e.g. AbstractController
- B. With an Abstract suffix, e.g. ControllerAbstract
- C. With an _abstract suffix

??? success "Answer Q97"
    **A**

    Abstract classes take the Abstract prefix; interfaces use the Interface suffix and traits use the Trait suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

**Q98.** Which set correctly fixes these names: httpClientInterface, Abstract_Controller, blogShow (route), app-page-size (parameter), app_env (env var)?  <small>_(medium · debug)_</small>

- A. HttpClientInterface, AbstractController, blog_show, app.page_size, APP_ENV
- B. HTTPClientInterface, ControllerAbstract, BlogShow, app_page_size, appEnv
- C. httpClient, AbstractController, blog-show, app.pageSize, APP-ENV

??? success "Answer Q98"
    **A**

    Interfaces are PascalCase with the Interface suffix (HttpClientInterface); abstract classes take the Abstract prefix in PascalCase (AbstractController); routes are snake_case (blog_show); parameters are snake/dot-separated lowercase (app.page_size); env vars are UPPER_SNAKE with APP_ prefix (APP_ENV).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

**Q99.** Which casing pair is correct for PHP class constants and bundle config keys?  <small>_(medium · trap)_</small>

- A. Constants are UPPER_SNAKE_CASE (e.g. MAIN_REQUEST); bundle config keys are snake_case (e.g. framework.http_method_override)
- B. Constants are camelCase; config keys are PascalCase
- C. Both use kebab-case

??? success "Answer Q99"
    **A**

    PHP constants follow UPPER_SNAKE_CASE (HttpKernelInterface::MAIN_REQUEST) and enum cases are PascalCase. Bundle configuration keys are snake_case under the extension's alias (e.g. framework.http_method_override). Mixing these up — camelCase config keys, for instance — is a planted mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/standards.html)

**Q100.** Which of the following statements are true about Symfony Flex? (select all that apply)  <small>_(medium · multiple)_</small>

- A. Flex is a Composer plugin that resolves package aliases and applies recipes at install/update time
- B. symfony.lock records which recipes are installed and should be committed to version control
- C. Bundles enabled by recipes are registered in config/bundles.php, which the kernel reads at boot
- D. Flex hooks into the kernel at runtime to auto-register bundles on each HTTP request
- E. Installed recipes are recorded in composer.lock together with package versions

??? success "Answer Q100"
    **A, B, C**

    Flex is a Composer plugin that runs only at Composer install/update time, resolving aliases and applying recipes; it plays no role during request handling, so the runtime option is wrong. Applied recipes are tracked in symfony.lock (committed), not in composer.lock which only tracks package versions, and recipe configurators write bundle registrations into config/bundles.php for the kernel to read at boot.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/setup.html)

**Q101.** Which statements are true about Symfony's backward compatibility promise? (select all that apply)  <small>_(medium · multiple)_</small>

- A. Public API that is not marked @internal or @experimental stays stable within a major version
- B. Existing behavior is removed only in the next major version, and only after being deprecated first
- C. Classes marked @internal are covered by the promise as long as their methods are public
- D. Extending framework classes through inheritance is the recommended way to customize Symfony

??? success "Answer Q101"
    **A, B**

    The BC promise guarantees that public, non-@internal, non-@experimental API remains stable within a major, and removals happen only in the next major after a deprecation phase. @internal and @experimental annotations carve exceptions out of the promise regardless of method visibility, and the recommended extension mechanisms are events, decoration and dependency injection rather than inheriting framework classes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q102.** Which statements about Symfony's relationship to the PSR standards are true? (select all that apply)  <small>_(medium · multiple)_</small>

- A. The service container implements PSR-11 and the Clock component implements PSR-20
- B. Components type-hint the PSR-3 Psr\Log\LoggerInterface, so any PSR-3 logger can be injected
- C. The psr-http-message bridge converts between HttpFoundation objects and PSR-7 messages
- D. HttpFoundation's Request and Response natively implement the PSR-7 interfaces
- E. Symfony's autoloading follows PSR-0

??? success "Answer Q102"
    **A, B, C**

    Symfony implements PSR-6, PSR-11, PSR-14, PSR-16 and PSR-20 (the container is a PSR-11 ContainerInterface and Clock is PSR-20), and it consumes PSR-3 by type-hinting LoggerInterface so any compliant logger works. HttpFoundation predates and does not implement PSR-7 — the psr-http-message bridge converts between the two object models — and autoloading follows PSR-4, not PSR-0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/psr7.html)

**Q103.** Which statements about the EventDispatcher component are correct? (select all that apply)  <small>_(medium · multiple)_</small>

- A. Listeners for an event are invoked in descending priority order (highest priority first)
- B. stopPropagation() prevents only the remaining listeners of the current event from running
- C. Event subscribers must be registered manually with addListener() for every event they handle
- D. dispatch() takes the event name as the first argument and the event object as the second

??? success "Answer Q103"
    **A, B**

    The dispatcher sorts listeners by priority in descending order, and stopPropagation() halts only the not-yet-called listeners of the event currently being dispatched — other events are unaffected. Subscribers declare all their events in getSubscribedEvents() and are wired automatically (autoconfiguration tags them), and dispatch() follows the PSR-14 signature: the event object first, then an optional event name.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q104.** Why is the external library an optional dependency of the component but a required dependency of the bridge?  <small>_(hard · internals)_</small>

- A. Keeping it optional on the component preserves the component's minimal, reusable dependency graph; the bridge exists precisely to depend on that library, so it requires it
- B. Because Composer forbids components from having any required dependencies
- C. Because the bridge is loaded at runtime while the component is loaded at compile time

??? success "Answer Q104"
    **A**

    A component must stay usable by everyone, so it must not hard-require any particular third-party library — that coupling is pushed into a separate bridge package. The bridge's whole reason to exist is to integrate that specific library, so it declares it as a required dependency. This keeps the component's graph minimal and the integration independently versioned.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)

**Q105.** What is the full firing order of the linear kernel events when a controller returns a non-Response value that a listener then converts?  <small>_(hard · internals)_</small>

- A. request → controller → controller_arguments → view → response → finish_request → (after send) terminate
- B. request → controller_arguments → controller → response → view → terminate → finish_request
- C. request → controller → view → controller_arguments → response → terminate
- D. request → controller → response → view → finish_request → terminate

??? success "Answer Q105"
    **A**

    The canonical order is request, controller, controller_arguments, view (only when a non-Response is returned), response, finish_request; then after the response is sent, terminate. kernel.exception is the eighth KernelEvents constant but fires out of band, only on error. controller_arguments runs AFTER argument resolution, and view sits between the controller call and response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q106.** Relative to argument resolution, when does kernel.controller_arguments fire?  <small>_(hard · trap)_</small>

- A. After ArgumentResolver has built the argument array — listeners edit an already-resolved array via setArguments()
- B. Before argument resolution, so listeners provide the raw values the resolver will use
- C. During controller execution, once per argument

??? success "Answer Q106"
    **A**

    kernel.controller_arguments is dispatched AFTER ArgumentResolverInterface::getArguments() has produced the final ordered array; listeners receive a ControllerArgumentsEvent and may mutate the already-built array with setArguments(). Assuming it runs before resolution (to feed the resolver) is a common misconception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-controller-arguments)

**Q107.** What is the signature of HttpKernelInterface::handle() and the role of its $catch argument?  <small>_(hard · internals)_</small>

- A. handle(Request $request, int $type = self::MAIN_REQUEST, bool $catch = true): Response — with $catch=true, exceptions are caught and turned into a response via kernel.exception; with $catch=false they propagate
- B. handle(Request $request): void — it prints the response directly and $catch controls output buffering
- C. handle(string $env, bool $debug): Response — $catch enables the profiler

??? success "Answer Q107"
    **A**

    The contract is handle(Request, int $type = MAIN_REQUEST, bool $catch = true): Response. handle() wraps the private handleRaw() in a try/catch when $catch is true, so an escaped exception is routed through handleThrowable()/kernel.exception into a Response. With $catch=false (common in sub-requests and tests) the exception simply propagates to the caller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q108.** What does the default ErrorListener actually do when it handles a kernel.exception?  <small>_(hard · internals)_</small>

- A. It logs the exception, forwards to the error controller as a sub-request, and sets the resulting Response on the event
- B. It immediately calls exit() with the HTTP status code
- C. It re-throws the exception so PHP's default handler renders it

??? success "Answer Q108"
    **A**

    ErrorListener (priority -128) logs the throwable, forwards to the error_controller (ErrorController) as a sub-request whose response carries the status/headers from HttpExceptionInterface, and sets that response on the ExceptionEvent. Because it runs last, any higher-priority listener that already set a response wins and ErrorListener does nothing.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/ErrorListener.php)

**Q109.** How do Security's AccessDeniedException and HttpKernel's AccessDeniedHttpException differ?  <small>_(hard · trap)_</small>

- A. AccessDeniedHttpException implements HttpExceptionInterface (→ 403 directly); AccessDeniedException is a Security exception the firewall translates to 403 or a redirect to login
- B. They are aliases of the same class in different namespaces
- C. AccessDeniedException already carries a 403 status code via HttpExceptionInterface

??? success "Answer Q109"
    **A**

    They are different classes. Symfony\\Component\\HttpKernel\\Exception\\AccessDeniedHttpException implements HttpExceptionInterface and yields a 403 through the normal error flow. Symfony\\Component\\Security\\Core\\Exception\\AccessDeniedException is a Security exception that does NOT implement HttpExceptionInterface; the firewall's exception listener catches it and turns it into a 403 (or a redirect to the login page for unauthenticated users).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q110.** A kernel.exception listener inspects getThrowable() and builds a JsonResponse, but the custom page never appears. What is the most likely bug?  <small>_(hard · debug)_</small>

- A. The listener forgot to call $event->setResponse() on its branch, so the event's response stays null and the default handler wins
- B. The listener has priority -128, which is impossible to register
- C. kernel.exception cannot produce JSON responses, only HTML

??? success "Answer Q110"
    **A**

    ExceptionEvent::getResponse() returns null until some listener calls setResponse(). Reading getThrowable() and constructing a response is not enough — you must actually set it on the event. If a branch forgets setResponse(), the response stays null, ErrorListener's default page (or a 500) is used instead, and your custom page never shows.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/events.html#kernel-exception)

**Q111.** How does EventDispatcher store and order listeners internally?  <small>_(hard · internals)_</small>

- A. It keeps listeners[eventName][priority][] and sorts by priority descending on first dispatch, memoising the sorted list until a listener is added/removed
- B. It sorts listeners alphabetically by class name on every dispatch
- C. It runs listeners in random order to prevent coupling

??? success "Answer Q111"
    **A**

    Internally the dispatcher stores listeners keyed by event name then priority. On the first dispatch of an event it sorts by priority descending (higher first; equal priorities preserve registration order) and caches the result in a sorted[] map, invalidated only when listeners change. This memoisation keeps repeated dispatches cheap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php)

**Q112.** How are tagged listeners/subscribers and #[AsEventListener] attributes wired into the dispatcher?  <small>_(hard · internals)_</small>

- A. RegisterListenersPass wires them at container compile time, and listener services are instantiated lazily only when their event fires
- B. The kernel calls addListener() for each on every kernel.request
- C. They are registered at runtime the first time getSubscribedEvents() is called

??? success "Answer Q112"
    **A**

    The RegisterListenersPass compiler pass scans services tagged kernel.event_listener/kernel.event_subscriber and #[AsEventListener] attributes and wires them into the dispatcher at compile time. Listeners are registered lazily — the service is only constructed when its event actually fires — which keeps boot cheap. You rarely call addListener() at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/event_dispatcher.html)

**Q113.** What does dispatch(object $event) return, and how do you read a listener's result?  <small>_(hard · trap)_</small>

- A. It always returns the same event object you passed in; results reach you only by listeners mutating that event (e.g. setResponse), never as a listener return value
- B. It returns whatever the last listener returned
- C. It returns null when no listener set a value

??? success "Answer Q113"
    **A**

    dispatch() returns the exact event object passed in — even with no listeners, or when all left it untouched. Listeners themselves return void; the only way data flows back is by mutating the event, which you then read from the returned object. Expecting dispatch() to hand back a listener's return value is the classic bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/event_dispatcher.html)

**Q114.** How are bug fixes propagated across Symfony's maintained branches?  <small>_(hard · internals)_</small>

- A. Fixes are merged UP from the oldest maintained branch to newer ones, so a patch to 8.0 also lands in 8.1, 8.2, etc.
- B. Each branch is patched independently with no relationship between them
- C. Fixes are merged DOWN from the newest branch into older ones

??? success "Answer Q114"
    **A**

    Symfony uses a merge-up model: a fix is committed to the lowest maintained branch that needs it and then merged upward into every newer branch. This keeps behaviour consistent across all maintained versions and avoids a fix being present in an old branch but missing in a newer one.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

**Q115.** Symfony adds a new method to one of its own interfaces in a minor release. Is this a BC break?  <small>_(hard · internals)_</small>

- A. Not for code that only USES the interface, but it can break code that IMPLEMENTS it — so only implement interfaces Symfony marks as safe to implement
- B. Yes, always — adding anything to an interface is forbidden between minors
- C. No, never — interfaces are outside the BC promise entirely

??? success "Answer Q115"
    **A**

    The promise is written from two viewpoints. For USING code (calling methods, reading returns) adding a method is safe. For EXTENDING code (your class implementing that interface) a new method is a break, because your class no longer satisfies the contract. Symfony reserves the right to add methods to its interfaces, so you should only implement interfaces meant for implementation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/code/bc.html)

**Q116.** Which version string should you pass as the second argument of trigger_deprecation()?  <small>_(hard · trap)_</small>

- A. The version in which the API was DEPRECATED (e.g. '8.1'), not the current running version
- B. The current installed version at the time the notice fires
- C. The version in which the code will be REMOVED (the next major)

??? success "Answer Q116"
    **A**

    The version argument records when the deprecation was introduced, producing the \"Since <package> <version>: <message>\" format tooling parses. A common mistake is passing the current version, or the removal version — both are wrong. Use the version the API was deprecated in.

    :material-book-open-variant: [Docs](https://github.com/symfony/deprecation-contracts)

**Q117.** When you decorate a service with #[AsDecorator(decorates: 'acme.mailer')], how do you access the original?  <small>_(hard · config)_</small>

- A. Inject the renamed original (the .inner service) via #[AutowireDecorated] and delegate to it
- B. Instantiate a new copy of the original class with `new`
- C. Fetch it from the container by making acme.mailer public

??? success "Answer Q117"
    **A**

    Decoration renames the original service to a .inner id and injects it into the decorator. The #[AutowireDecorated] attribute (or the special .inner reference in YAML) gives you that original instance so you can add behaviour and delegate. Re-creating it with `new` or fetching it publicly defeats the decoration pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

**Q118.** Which PSRs does Symfony IMPLEMENT (i.e. Symfony objects ARE valid PSR objects)? (choose all that apply)  <small>_(hard · multiple)_</small>

- A. PSR-6 (Cache pool)
- B. PSR-11 (Container)
- C. PSR-14 (Event Dispatcher)
- D. PSR-20 (Clock)
- E. PSR-3 (Logger)

??? success "Answer Q118"
    **A, B, C, D**

    Symfony implements PSR-6 (Cache pool), PSR-11 (Container), PSR-14 (EventDispatcher), PSR-16 (Simple Cache adapter) and PSR-20 (Clock) — its objects can be handed to any library expecting those interfaces. PSR-3 (Logger) is CONSUMED: Symfony type-hints LoggerInterface so you inject any implementation, but it does not ship the logger itself.

    :material-book-open-variant: [Docs](https://www.php-fig.org/psr/)

**Q119.** Why is the Interface suffix more than cosmetic in Symfony?  <small>_(hard · internals)_</small>

- A. Autoconfiguration inspects implemented interfaces (e.g. EventSubscriberInterface) to auto-tag services, so correct interface naming/implementation is part of a working contract
- B. The router requires interface names to end in Interface to build URLs
- C. Composer's autoloader only loads classes whose interface ends in Interface

??? success "Answer Q119"
    **A**

    When autoconfigure is on, Symfony auto-tags services based on the interfaces they implement — e.g. implementing EventSubscriberInterface auto-adds the kernel.event_subscriber tag, and ServiceSubscriberInterface, and voter/command interfaces behave similarly. So the Interface suffix marks a real, functional contract that drives wiring, not just style.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

**Q120.** Which statements accurately describe the Symfony release process? (select all that apply)  <small>_(hard · multiple)_</small>

- A. Minor versions are released on a time-based schedule in May and November, and a new major arrives every two years
- B. 8.4 is the Symfony 8 LTS version and ships alongside 9.0
- C. A minor version may break backward compatibility as long as the change was deprecated first
- D. Standard (non-LTS) versions receive 3 years of bug fixes
- E. The LTS of each branch is always the X.0 release of the major

??? success "Answer Q120"
    **A, B**

    Symfony follows a time-based schedule: minors in May and November and a new major every two years, with the last minor of a branch (X.4, e.g. 8.4) being the LTS that ships alongside the next major. BC breaks happen only in major versions, never in minors even after deprecation, and standard versions get 8 months of bug fixes / 14 months of security fixes — the 3-year bug-fix window belongs to LTS releases only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/contributing/community/releases.html)

**Q121.** Which statements about HttpKernel's request handling and its events are correct? (select all that apply)  <small>_(hard · multiple)_</small>

- A. kernel.view is dispatched only when the controller returns something other than a Response
- B. kernel.terminate is dispatched after the response has been sent to the client
- C. When handle() is called with catch: true, exceptions are caught and kernel.exception is dispatched
- D. kernel.response is dispatched before kernel.controller so listeners can veto the controller
- E. The controller callable itself is resolved by the ArgumentResolverInterface

??? success "Answer Q121"
    **A, B, C**

    kernel.view fires only for non-Response controller return values, and kernel.terminate runs after the response was already sent, which makes it suitable for heavy post-response work; with catch: true, HttpKernel catches throwables and dispatches kernel.exception. The event order puts kernel.controller before kernel.response, and the controller callable is resolved by ControllerResolverInterface — ArgumentResolverInterface only resolves the controller's arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html)

**Q122.** Which are valid ways to override parts of Symfony or a third-party bundle in an application? (select all that apply)  <small>_(hard · multiple)_</small>

- A. Override a bundle template by placing a file with the same path under templates/bundles/<BundleName>/
- B. Override a service by decorating it or replacing its definition, e.g. via a compiler pass
- C. Override translations by defining the same key in the application's translations/ directory, which wins over the bundle's
- D. Create a child bundle and point getParent() at the bundle you want to override
- E. Copy the entire bundle into src/ so your copy shadows the vendor code

??? success "Answer Q122"
    **A, B, C**

    Per-resource overriding is the supported model: templates placed under templates/bundles/<BundleName>/ shadow the bundle's own, application translations take precedence over bundle translations, and services can be redefined, decorated or altered through a compiler pass. Bundle inheritance via getParent() has been removed, and copying whole bundles into src/ is not an override mechanism at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/override.html)

---

<small>Back to [Chapter Exams](index.md) · [Symfony Architecture](../architecture/index.md)</small>
