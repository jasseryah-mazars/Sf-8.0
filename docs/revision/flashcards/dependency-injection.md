# Flashcards — Dependency Injection

38 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. Why are Symfony services private by default?"
    **✅ So the compiler can inline/remove them and to enforce proper dependency injection**

    Private services can be inlined into their single consumer and pruned when unreferenced, shrinking the compiled container, and it discourages the service-locator anti-pattern of pulling from the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "2. Calling $container->get() on a private service id results in what?"
    **✅ A ServiceNotFoundException**

    Private services are not fetchable by id from the public container; they may only be injected. Fetching one throws ServiceNotFoundException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "3. What is written to var/cache/prod/ after compilation?"
    **✅ A dumped, optimised PHP container class produced by PhpDumper**

    PhpDumper writes a compiled PHP class with a method per service; the runtime uses it directly, never the ContainerBuilder.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection/compilation.html)

??? question "4. Which objects exist only at build time, not at runtime? (choose one)"
    **✅ Definition, Reference, Alias and Parameter metadata objects**

    Definition/Reference/Alias/Parameter are build-time recipes held by the ContainerBuilder; the runtime container holds instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection/compilation.html)

??? question "5. How should you access the current request inside a service?"
    **✅ Inject RequestStack and call getCurrentRequest()**

    The Request is per-cycle and can change across sub-requests, so it is not injectable directly. Inject RequestStack and read the current request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

??? question "6. Which command lists what a given type-hint autowires to?"
    **✅ debug:autowiring**

    debug:autowiring shows the types you can type-hint and which service each resolves to; debug:container inspects a definition by id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

??? question "7. By default, debug:container hides which services?"
    **✅ Private services (shown only with --show-private)**

    debug:container lists public services and aliases; add --show-private to include private ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

??? question "8. When is %env(DATABASE_URL)% resolved?"
    **✅ At runtime, via an env-var processor**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

??? question "9. What does the expression %env(int:MAX)% produce?"
    **✅ The value of MAX cast to an integer**

    The int: processor casts the raw env string to an integer. Processors chain right-to-left.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/env_var_processors.html)

??? question "10. Which attribute injects the container parameter app.name into a constructor argument?"
    **✅ #[Autowire(param: 'app.name')]**

    param: names a container parameter; a bare string without %% is a literal, and env: reads an environment variable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "11. How do you write a literal percent sign inside a parameter value?"
    **✅ Double it: %%**

    A doubled percent escapes to a single literal % so it is not treated as a parameter reference.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-parameters)

??? question "12. Using the App\: resource glob, what is a service's id?"
    **✅ Its fully-qualified class name (FQCN)**

    PSR-4 auto-registration creates one definition per class using the FQCN as the service id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "13. What does autoconfigure: true do (as opposed to autowire)?"
    **✅ Applies tags/flags based on implemented interfaces and attributes**

    Autoconfigure adds tags automatically (e.g. event subscriber); autowire is the separate flag that fills arguments by type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html#the-autoconfigure-option)

??? question "14. How do you make an interface type-hint resolve to a concrete class?"
    **✅ Define an alias, e.g. Interface: '@Class'**

    An alias from the interface id to the concrete service lets autowiring resolve the interface type-hint.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/alias_private.html)

??? question "15. In a decorator definition, what does @.inner reference?"
    **✅ The original (decorated) service, renamed by the compiler**

    DecoratorServicePass renames the decorated service and exposes it as .inner so the decorator can delegate to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "16. Which attribute injects the decorated (inner) service into a decorator?"
    **✅ #[AutowireDecorated]**

    #[AsDecorator] declares the decoration; #[AutowireDecorated] resolves the parameter to the .inner service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "17. With two decorators on one id, a higher decoration_priority means the decorator is..."
    **✅ Applied first and sits closer to the original (innermost)**

    Higher priority decorators are applied first and end up innermost; consumers receive the lowest-priority, outermost decorator.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html#decoration-priority)

??? question "18. decoration_on_invalid: ignore does what when the decorated service is missing?"
    **✅ Removes the decorator entirely**

    ignore drops the decorator; null would inject null; exception (the default) throws when the target is absent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "19. What does a tagged_locator argument inject?"
    **✅ A lazy ServiceLocator keyed by an index**

    tagged_locator injects a ServiceLocator that instantiates services on demand, keyed by the configured index; tagged_iterator yields instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "20. A higher priority on a tag places the service where in the tagged iterator?"
    **✅ Earlier (tagged collections are sorted by descending priority)**

    Tagged services are ordered by descending priority, so higher priority comes first.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html#tagged-services-with-priority)

??? question "21. How can every implementation of an interface receive a tag automatically?"
    **✅ Use #[AutoconfigureTag] on the interface or _instanceof in YAML**

    Autoconfiguration maps an interface to a tag so all implementers are tagged without manual annotation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "22. Which class validates and defaults a bundle's configuration schema?"
    **✅ Configuration, via a TreeBuilder**

    Configuration defines allowed keys, types, defaults and validation; Extension::load() only consumes the processed result.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "23. When does prepend() run relative to the extensions' load() calls?"
    **✅ Before all load() calls**

    Prepend runs first so a bundle can inject default configuration into other bundles before they load.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/prepend_extension.html)

??? question "24. Which command prints a bundle's configuration reference tree?"
    **✅ config:dump-reference**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "25. For a factory-built service, where are its arguments passed?"
    **✅ To the factory method**

    With a factory, the container calls the factory and passes the definition's arguments to it, not to a constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "26. How do you configure a factory produced value via attributes?"
    **✅ #[Autowire(factory: [Factory::class, 'create'])]**

    There is no dedicated #[Factory] attribute; factories are configured with #[Autowire(factory:)] or in YAML/PHP config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "27. How is an instance-method factory referenced in YAML?"
    **✅ factory: ['@service_id', 'method']**

    An array of [reference, method] denotes a method call on a service; a static factory uses the 'Class::method' string form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "28. Which attribute registers a compiler pass? (choose one)"
    **✅ There is no attribute; register it via addCompilerPass() in Kernel/bundle build()**

    Compiler passes are registered programmatically via ContainerBuilder::addCompilerPass(), typically in Kernel::build() or a bundle's build(). There is no core attribute for this.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "29. What is the default phase for a compiler pass registered without one?"
    **✅ TYPE_BEFORE_OPTIMIZATION**

    PassConfig runs passes in phase order; unspecified passes run in the before-optimization phase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "30. What does ContainerBuilder::findTaggedServiceIds('t') return?"
    **✅ A map of service id => array of that tag's attribute sets**

    It returns definitions' ids each mapped to the attributes of every occurrence of the tag, used to wire collectors at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "31. Inside a compiler pass process() method, what should you manipulate?"
    **✅ Definition objects (build-time metadata)**

    Compilation deals only with definitions; nothing is instantiated yet, so calling get() inside a pass is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "32. What can autowiring resolve automatically?"
    **✅ Object dependencies identified by their type-hint**

    Autowiring maps a type-hint to a service; scalars and env vars must be bound explicitly with bind or #[Autowire].

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "33. Two services implement one interface with no default alias. Autowiring by that interface..."
    **✅ Throws an ambiguity error at compile time**

    Ambiguity is a hard build error; you disambiguate with a named alias, #[Target], #[Autowire(service:)] or bind.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "34. What does the #[Target('requestLogger')] attribute do?"
    **✅ Selects the named autowiring alias explicitly, decoupled from the parameter name**

    #[Target] binds to a named autowiring alias by name, so renaming the constructor parameter does not break wiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html#fixing-non-autowireable-arguments)

??? question "35. How does a ServiceLocator differ from injecting the whole container?"
    **✅ It exposes only an explicitly declared, whitelisted set of services**

    A locator's set is explicit and analysable; injecting the whole container hides dependencies and is an anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "36. When does a ServiceLocator instantiate the services it holds?"
    **✅ Lazily, on get()**

    A locator defers construction until a service is actually requested, which is its main advantage over injecting all candidates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

??? question "37. What interface does Symfony's ServiceLocator implement?"
    **✅ Psr\Container\ContainerInterface (PSR-11)**

    ServiceLocator is a PSR-11 container exposing get() and has() over a fixed, compile-time set of services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

??? question "38. What does ServiceSubscriberInterface::getSubscribedServices() declare?"
    **✅ The set of services the subscriber may lazily use, injected as a locator**

    It declares a whitelist; the container injects a matching ServiceLocator so services are built only when requested.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

---

<small>Back to [Flashcards](index.md) · [Dependency Injection](../../dependency-injection/index.md)</small>
