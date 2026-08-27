# Chapter Exam — Dependency Injection

!!! abstract "How to use"
    81 questions spanning every subchapter of **Dependency Injection**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Dependency Injection](../dependency-injection/index.md).

---

**Q1.** Calling $container->get() on a private service id results in what?  <small>_(easy · single)_</small>

- A. A ServiceNotFoundException
- B. The service instance is returned
- C. null
- D. A fresh instance each call

??? success "Answer Q1"
    **A**

    Private services are not fetchable by id from the public container; they may only be injected. Fetching one throws ServiceNotFoundException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q2.** True or False: a service being public and a service being shared mean the same thing.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q2"
    **B**

    They are independent flags. Public means fetchable by id via get(); shared means the same instance is reused across get() calls. The default service is private and shared. A common trap confuses the two — a service can be public and non-shared, or private and shared, in any combination.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q3.** How should you access the current request inside a service?  <small>_(easy · single)_</small>

- A. Inject RequestStack and call getCurrentRequest()
- B. Type-hint Request in the constructor
- C. Inject HttpKernelInterface
- D. Call $container->get('request')

??? success "Answer Q3"
    **A**

    The Request is per-cycle and can change across sub-requests, so it is not injectable directly. Inject RequestStack and read the current request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/request.html)

**Q4.** Which command lists what a given type-hint autowires to?  <small>_(easy · single)_</small>

- A. debug:autowiring
- B. debug:config
- C. debug:router
- D. config:dump-reference

??? success "Answer Q4"
    **A**

    debug:autowiring shows the types you can type-hint and which service each resolves to; debug:container inspects a definition by id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/debug.html)

**Q5.** By default, debug:container hides which services?  <small>_(easy · single)_</small>

- A. Private services (shown only with --show-private)
- B. Public services
- C. Aliases
- D. Parameters

??? success "Answer Q5"
    **A**

    debug:container lists public services and aliases; add --show-private to include private ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/debug.html)

**Q6.** What does the expression %env(int:MAX)% produce?  <small>_(easy · single)_</small>

- A. The value of MAX cast to an integer
- B. The raw string value of MAX
- C. A parameter named int
- D. null when MAX is unset

??? success "Answer Q6"
    **A**

    The int: processor casts the raw env string to an integer. Processors chain right-to-left.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration/env_var_processors.html)

**Q7.** How do you write a literal percent sign inside a parameter value?  <small>_(easy · single)_</small>

- A. Double it: %%
- B. Escape it: \%
- C. URL-encode it: %25
- D. It is impossible

??? success "Answer Q7"
    **A**

    A doubled percent escapes to a single literal % so it is not treated as a parameter reference.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-parameters)

**Q8.** True or False: environment variables referenced with %env(...)% are frozen into the compiled container cache at compile time.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q8"
    **B**

    The compiler replaces %env(...)% with a placeholder and the EnvVarProcessor resolves it at runtime, which is exactly why one compiled container works across environments and changing an env var needs no cache rebuild. Only plain parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-based-on-environment-variables)

**Q9.** Using the App\: resource glob, what is a service's id?  <small>_(easy · single)_</small>

- A. Its fully-qualified class name (FQCN)
- B. A short snake_case name
- C. The relative file path
- D. A generated hash

??? success "Answer Q9"
    **A**

    PSR-4 auto-registration creates one definition per class using the FQCN as the service id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q10.** What does autoconfigure: true do (as opposed to autowire)?  <small>_(easy · single)_</small>

- A. Applies tags/flags based on implemented interfaces and attributes
- B. Fills constructor arguments by type
- C. Makes all services public
- D. Clears the compiled cache

??? success "Answer Q10"
    **A**

    Autoconfigure adds tags automatically (e.g. event subscriber); autowire is the separate flag that fills arguments by type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html#the-autoconfigure-option)

**Q11.** How do you make an interface type-hint resolve to a concrete class?  <small>_(easy · single)_</small>

- A. Define an alias, e.g. Interface: '@Class'
- B. Type-hint the class instead of the interface
- C. Make the class public
- D. Add a tag to the class

??? success "Answer Q11"
    **A**

    An alias from the interface id to the concrete service lets autowiring resolve the interface type-hint.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/alias_private.html)

**Q12.** In a decorator definition, what does @.inner reference?  <small>_(easy · single)_</small>

- A. The original (decorated) service, renamed by the compiler
- B. The decorator service itself
- C. The parent bundle service
- D. A private alias of the container

??? success "Answer Q12"
    **A**

    DecoratorServicePass renames the decorated service and exposes it as .inner so the decorator can delegate to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q13.** Which attribute injects the decorated (inner) service into a decorator?  <small>_(easy · trap)_</small>

- A. #[AutowireDecorated]
- B. #[AsDecorator]
- C. #[Inner]
- D. #[Decorated]

??? success "Answer Q13"
    **A**

    #[AsDecorator] declares the decoration; #[AutowireDecorated] resolves the parameter to the .inner service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q14.** What does a tagged_locator argument inject?  <small>_(easy · single)_</small>

- A. A lazy ServiceLocator keyed by an index
- B. An array of already-instantiated services
- C. A compiler pass
- D. The raw tag name string

??? success "Answer Q14"
    **A**

    tagged_locator injects a ServiceLocator that instantiates services on demand, keyed by the configured index; tagged_iterator yields instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q15.** A higher priority on a tag places the service where in the tagged iterator?  <small>_(easy · single)_</small>

- A. Earlier (tagged collections are sorted by descending priority)
- B. Later
- C. It has no effect on order
- D. Randomly

??? success "Answer Q15"
    **A**

    Tagged services are ordered by descending priority, so higher priority comes first.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html#tagged-services-with-priority)

**Q16.** True or False: adding a tag to a service changes its behaviour automatically, even with no collector consuming that tag.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q16"
    **B**

    A tag is inert build-time metadata; on its own it does nothing. Something — a tagged_iterator/tagged_locator argument or a compiler pass calling findTaggedServiceIds() — must consume the tag for it to have any effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q17.** Which class validates and defaults a bundle's configuration schema?  <small>_(easy · single)_</small>

- A. Configuration, via a TreeBuilder
- B. Extension::load()
- C. Kernel::build()
- D. ContainerBuilder

??? success "Answer Q17"
    **A**

    Configuration defines allowed keys, types, defaults and validation; Extension::load() only consumes the processed result.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q18.** Which command prints a bundle's configuration reference tree?  <small>_(easy · single)_</small>

- A. config:dump-reference
- B. debug:container
- C. debug:autowiring
- D. debug:router

??? success "Answer Q18"
    **A**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q19.** A bundle named AcmeBlogBundle exposes its configuration under which root key by convention?  <small>_(easy · single)_</small>

- A. acme_blog (snake_case of the bundle name minus 'Bundle')
- B. AcmeBlogBundle
- C. acme_blog_bundle
- D. blog

??? success "Answer Q19"
    **A**

    The root key is derived from the extension/bundle name: the class name minus the Bundle suffix, converted to snake_case, giving acme_blog. The misconception is using the class name verbatim or keeping the Bundle suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q20.** For a factory-built service, where are its arguments passed?  <small>_(easy · single)_</small>

- A. To the factory method
- B. To the class constructor
- C. To __invoke only
- D. They are ignored

??? success "Answer Q20"
    **A**

    With a factory, the container calls the factory and passes the definition's arguments to it, not to a constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q21.** What is the default phase for a compiler pass registered without one?  <small>_(easy · internals)_</small>

- A. TYPE_BEFORE_OPTIMIZATION
- B. TYPE_OPTIMIZE
- C. TYPE_REMOVE
- D. TYPE_AFTER_REMOVING

??? success "Answer Q21"
    **A**

    PassConfig runs passes in phase order; unspecified passes run in the before-optimization phase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q22.** What can autowiring resolve automatically?  <small>_(easy · single)_</small>

- A. Object dependencies identified by their type-hint
- B. Scalar and string arguments
- C. Array parameters
- D. Environment variables

??? success "Answer Q22"
    **A**

    Autowiring maps a type-hint to a service; scalars and env vars must be bound explicitly with bind or #[Autowire].

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q23.** How does a ServiceLocator differ from injecting the whole container?  <small>_(easy · single)_</small>

- A. It exposes only an explicitly declared, whitelisted set of services
- B. It is eager while the container is lazy
- C. It cannot instantiate services
- D. There is no real difference

??? success "Answer Q23"
    **A**

    A locator's set is explicit and analysable; injecting the whole container hides dependencies and is an anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q24.** When does a ServiceLocator instantiate the services it holds?  <small>_(easy · single)_</small>

- A. Lazily, on get()
- B. All of them at construction
- C. At container compilation
- D. On kernel boot

??? success "Answer Q24"
    **A**

    A locator defers construction until a service is actually requested, which is its main advantage over injecting all candidates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html#service-locators)

**Q25.** Why are Symfony services private by default?  <small>_(medium · internals)_</small>

- A. So the compiler can inline/remove them and to enforce proper dependency injection
- B. Because public services are deprecated in Symfony 8
- C. To make them read-only value objects
- D. So that get() runs faster at runtime

??? success "Answer Q25"
    **A**

    Private services can be inlined into their single consumer and pruned when unreferenced, shrinking the compiled container, and it discourages the service-locator anti-pattern of pulling from the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q26.** What is written to var/cache/prod/ after compilation?  <small>_(medium · internals)_</small>

- A. A dumped, optimised PHP container class produced by PhpDumper
- B. The ContainerBuilder instance serialized
- C. The raw YAML service definitions
- D. Serialized service instances

??? success "Answer Q26"
    **A**

    PhpDumper writes a compiled PHP class with a method per service; the runtime uses it directly, never the ContainerBuilder.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dependency_injection/compilation.html)

**Q27.** Which objects exist only at build time, not at runtime? (choose one)  <small>_(medium · internals)_</small>

- A. Definition, Reference, Alias and Parameter metadata objects
- B. The service instances themselves
- C. The compiled container class
- D. The RequestStack

??? success "Answer Q27"
    **A**

    Definition/Reference/Alias/Parameter are build-time recipes held by the ContainerBuilder; the runtime container holds instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dependency_injection/compilation.html)

**Q28.** A developer calls $this->container->get(MailerInterface::class) inside a service and gets a ServiceNotFoundException, even though the mailer works elsewhere. Why?  <small>_(medium · debug)_</small>

- A. MailerInterface resolves to a private service, which is not fetchable by id — inject it via the constructor instead
- B. MailerInterface is not registered anywhere in the container
- C. The container has not been compiled yet
- D. get() only accepts string literals, not ::class constants

??? success "Answer Q28"
    **A**

    The mailer service is private (the default), so it can only be injected, not fetched by id from the public container — get() therefore throws. The fix is constructor injection/autowiring, not making it public. It is registered and the container is compiled; the misconception is treating get() as a general-purpose lookup instead of using DI.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q29.** A service injects RequestStack and calls $this->requestStack->getCurrentRequest()->getLocale(); it fatals when run from a console command. Why?  <small>_(medium · trap)_</small>

- A. getCurrentRequest() returns null when there is no active request (e.g. CLI), so use the nullsafe operator ?->
- B. RequestStack is not autowirable in commands
- C. getLocale() does not exist on the Request object
- D. The request stack is cleared after the controller runs

??? success "Answer Q29"
    **A**

    Outside the HTTP cycle (console commands, Messenger workers) there is no current request, so getCurrentRequest() returns null and the method call fatals. Guard with getCurrentRequest()?->getLocale() or an early null check. RequestStack is autowirable everywhere; the trap is assuming a request always exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/request.html)

**Q30.** Which are correct ways to obtain framework services in your code? (choose 2)  <small>_(medium · multiple)_</small>

- A. Autowire by type-hinting the interface, e.g. LoggerInterface
- B. Use debug:autowiring to discover which type resolves to which service
- C. Type-hint a concrete Request to receive the current request
- D. Call $container->get('logger') from business code

??? success "Answer Q30"
    **A, B**

    Autowiring by interface is the idiomatic path, and debug:autowiring is the discovery tool for finding the right type-hint. A raw Request cannot be injected (use RequestStack), and pulling services with $container->get() in business code is the service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/debug.html)

**Q31.** When is %env(DATABASE_URL)% resolved?  <small>_(medium · internals)_</small>

- A. At runtime, via an env-var processor
- B. At compilation, frozen into the cache
- C. When .env is parsed at deploy time only
- D. Never; it is a literal string

??? success "Answer Q31"
    **A**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-based-on-environment-variables)

**Q32.** Which attribute injects the container parameter app.name into a constructor argument?  <small>_(medium · config)_</small>

- A. #[Autowire(param: 'app.name')]
- B. #[Autowire('app.name')]
- C. #[Parameter('app.name')]
- D. #[Autowire(env: 'app.name')]

??? success "Answer Q32"
    **A**

    param: names a container parameter; a bare string without %% is a literal, and env: reads an environment variable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q33.** What does ParameterBagInterface::get('app.missing') do for an undefined parameter?  <small>_(medium · debug)_</small>

- A. Throws ParameterNotFoundException — use has() first for optional lookups
- B. Returns null
- C. Returns an empty string
- D. Returns the parameter name unchanged

??? success "Answer Q33"
    **A**

    Reading a missing parameter throws ParameterNotFoundException; it never returns null. Guard optional lookups with has() before get(). The common bug is assuming an absent parameter silently becomes null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-parameters)

**Q34.** Given _defaults with autowire: true, autoconfigure: true, public: false and an App\: resource glob, what is true of a class under src/?  <small>_(medium · config)_</small>

- A. It is registered private, with arguments autowired by type and tags applied by interface
- B. It is public and must be fetched with get()
- C. Only classes carrying an attribute are registered
- D. Its id is a snake_case short name

??? success "Answer Q34"
    **A**

    _defaults sets the baseline: public: false makes it private, autowire fills constructor arguments by type, and autoconfigure applies tags based on implemented interfaces. The id is the FQCN. The glob registers every class in the directory, not just annotated ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q35.** The App\: glob registers a class, and a later named block redefines the same id. Which definition wins?  <small>_(medium · internals)_</small>

- A. The later, more specific block overrides the glob for that id
- B. The glob always wins over named blocks
- C. They are merged field-by-field with the glob taking precedence
- D. It raises a duplicate-definition error

??? success "Answer Q35"
    **A**

    Registration order matters: the glob first registers everything, then a later, more specific entry for the same id overrides it. This is the idiomatic way to tweak one autowired service. It is not an error and the glob does not win.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container.html)

**Q36.** Which argument cannot be supplied by autowiring and must come from bind, #[Autowire], or a parameter?  <small>_(medium · trap)_</small>

- A. A scalar string such as a directory path
- B. An object dependency identified by an interface type-hint
- C. A service aliased from its interface
- D. The single implementation of an interface

??? success "Answer Q36"
    **A**

    Autowiring resolves objects by type-hint; it can never guess scalars (strings, ints, arrays). Those must be bound explicitly via bind, #[Autowire], or a parameter. Objects, aliases, and single implementations all autowire fine.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q37.** decoration_on_invalid: ignore does what when the decorated service is missing?  <small>_(medium · single)_</small>

- A. Removes the decorator entirely
- B. Injects null as .inner
- C. Throws an exception
- D. Creates an empty stub service

??? success "Answer Q37"
    **A**

    ignore drops the decorator; null would inject null; exception (the default) throws when the target is absent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q38.** A decorator injects the service by its own (decorated) id instead of .inner and hits infinite recursion. What is the fix?  <small>_(medium · debug)_</small>

- A. Inject @.inner (or use #[AutowireDecorated]) to reference the renamed original
- B. Make the decorator public
- C. Lower the decoration_priority
- D. Set decoration_on_invalid: ignore

??? success "Answer Q38"
    **A**

    Because the decorator takes over the decorated service's public id, referencing that id inside the decorator injects the decorator itself, causing infinite recursion. You must reference the renamed original via .inner or #[AutowireDecorated]. Visibility and priority are unrelated to the loop.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q39.** How can every implementation of an interface receive a tag automatically?  <small>_(medium · single)_</small>

- A. Use #[AutoconfigureTag] on the interface or _instanceof in YAML
- B. It happens with no configuration
- C. Only by writing a compiler pass
- D. By adding #[AsTaggedItem] to each class

??? success "Answer Q39"
    **A**

    Autoconfiguration maps an interface to a tag so all implementers are tagged without manual annotation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q40.** What does #[AutowireIterator('app.handler')] on an iterable $handlers argument inject?  <small>_(medium · code)_</small>

- A. An iterable of all app.handler-tagged services, ordered by descending priority
- B. A ServiceLocator keyed by name
- C. Only the single highest-priority handler
- D. An array of the tag's attribute sets

??? success "Answer Q40"
    **A**

    #[AutowireIterator] is the attribute form of tagged_iterator: it injects an iterable of the instantiated tagged services, ordered by descending priority. #[AutowireLocator] would give the lazy keyed locator; the attribute does not filter down to one service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q41.** When does prepend() run relative to the extensions' load() calls?  <small>_(medium · internals)_</small>

- A. Before all load() calls
- B. After all load() calls
- C. At runtime on each request
- D. Only in the dev environment

??? success "Answer Q41"
    **A**

    Prepend runs first so a bundle can inject default configuration into other bundles before they load.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/prepend_extension.html)

**Q42.** Which command shows the currently resolved configuration values (not the schema) for a bundle?  <small>_(medium · trap)_</small>

- A. debug:config
- B. config:dump-reference
- C. debug:container
- D. debug:autowiring

??? success "Answer Q42"
    **A**

    debug:config prints the merged, resolved values in effect; config:dump-reference prints the schema (allowed keys, types, defaults) defined by Configuration. Confusing the two is a common trap — one shows what is set, the other what is allowed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q43.** How do you configure a factory produced value via attributes?  <small>_(medium · trap)_</small>

- A. #[Autowire(factory: [Factory::class, 'create'])]
- B. #[Factory([Factory::class, 'create'])]
- C. #[AsFactory]
- D. #[AsAlias(Factory::class)]

??? success "Answer Q43"
    **A**

    There is no dedicated #[Factory] attribute; factories are configured with #[Autowire(factory:)] or in YAML/PHP config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q44.** How is an instance-method factory referenced in YAML?  <small>_(medium · config)_</small>

- A. factory: ['@service_id', 'method']
- B. factory: '@service_id::method'
- C. factory: 'service_id.method'
- D. factory: @service_id

??? success "Answer Q44"
    **A**

    An array of [reference, method] denotes a method call on a service; a static factory uses the 'Class::method' string form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q45.** factory: '@svc::method' throws an error. What is the correct instance-method form?  <small>_(medium · debug)_</small>

- A. factory: ['@svc', 'method']
- B. factory: 'svc.method'
- C. factory: @svc.method
- D. factory: { service: svc, call: method }

??? success "Answer Q45"
    **A**

    The '@svc::method' string is invalid syntax for an instance-method factory; use the array form ['@svc', 'method']. The 'Class::method' string form is reserved for static factories. The other forms are not recognised.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q46.** How is an invokable factory service referenced in YAML?  <small>_(medium · single)_</small>

- A. factory: '@factory_service' (its __invoke method is called)
- B. factory: ['@factory_service', '__invoke'] only
- C. factory: 'factory_service()'
- D. factory: '@factory_service::__invoke'

??? success "Answer Q46"
    **A**

    A bare service reference '@service' as the factory means the container calls the service's __invoke() and stores the return value. Explicitly naming __invoke via the '::' string form is invalid; the array form is used for named instance methods, not required for invokables.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q47.** Which attribute registers a compiler pass? (choose one)  <small>_(medium · trap)_</small>

- A. There is no attribute; register it via addCompilerPass() in Kernel/bundle build()
- B. #[CompilerPass]
- C. #[AsCompilerPass]
- D. #[Autoconfigure(pass: true)]

??? success "Answer Q47"
    **A**

    Compiler passes are registered programmatically via ContainerBuilder::addCompilerPass(), typically in Kernel::build() or a bundle's build(). There is no core attribute for this.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q48.** What does ContainerBuilder::findTaggedServiceIds('t') return?  <small>_(medium · internals)_</small>

- A. A map of service id => array of that tag's attribute sets
- B. Instantiated service objects
- C. A ServiceLocator
- D. Only the first tagged id

??? success "Answer Q48"
    **A**

    It returns definitions' ids each mapped to the attributes of every occurrence of the tag, used to wire collectors at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q49.** Inside a compiler pass process() method, what should you manipulate?  <small>_(medium · internals)_</small>

- A. Definition objects (build-time metadata)
- B. Live service instances via get()
- C. The current HTTP request
- D. The runtime event dispatcher

??? success "Answer Q49"
    **A**

    Compilation deals only with definitions; nothing is instantiated yet, so calling get() inside a pass is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q50.** Inside process(), a pass calls $container->get(SomeService::class) and it fails. Why?  <small>_(medium · debug)_</small>

- A. Compilation deals only with Definitions; nothing is instantiated yet — use findDefinition()/Reference instead
- B. get() requires the service to be public first
- C. The service id is misspelled
- D. get() is only available inside the Kernel

??? success "Answer Q50"
    **A**

    A compiler pass runs before any service exists, so you manipulate build-time Definition objects (findDefinition, addMethodCall, new Reference), never live instances. Calling get() during compilation is the classic mistake; visibility and spelling are not the cause here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q51.** Which are valid places to register a compiler pass? (choose 2)  <small>_(medium · multiple)_</small>

- A. Kernel::build(ContainerBuilder $c) via addCompilerPass()
- B. A bundle's build(ContainerBuilder $c) via addCompilerPass()
- C. A #[CompilerPass] attribute on the pass class
- D. A container.compiler_pass tag in services.yaml

??? success "Answer Q51"
    **A, B**

    Passes are registered programmatically with addCompilerPass() in the application Kernel::build() or a bundle's build(). There is no #[CompilerPass] attribute and no services.yaml tag that registers a pass — those are common invented answers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q52.** In addCompilerPass(new MyPass(), PassConfig::TYPE_BEFORE_OPTIMIZATION, priority: 5), what do the 2nd and 3rd arguments control?  <small>_(medium · code)_</small>

- A. The compilation phase and the ordering priority within that phase
- B. The service id and its visibility
- C. The tag name and its index
- D. The environment and the debug flag

??? success "Answer Q52"
    **A**

    addCompilerPass(pass, phase, priority) takes the phase constant that determines when in PassConfig the pass runs, and a priority that orders passes within that phase (higher first). It has nothing to do with service ids, tags, or environments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q53.** Two services implement one interface with no default alias. Autowiring by that interface...  <small>_(medium · single)_</small>

- A. Throws an ambiguity error at compile time
- B. Silently picks the first candidate
- C. Injects null
- D. Picks the last candidate

??? success "Answer Q53"
    **A**

    Ambiguity is a hard build error; you disambiguate with a named alias, #[Target], #[Autowire(service:)] or bind.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q54.** What does the #[Target('requestLogger')] attribute do?  <small>_(medium · single)_</small>

- A. Selects the named autowiring alias explicitly, decoupled from the parameter name
- B. Creates a new service definition
- C. Adds a tag to the service
- D. Makes the service public

??? success "Answer Q54"
    **A**

    #[Target] binds to a named autowiring alias by name, so renaming the constructor parameter does not break wiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html#fixing-non-autowireable-arguments)

**Q55.** A parameter has #[Autowire('app.foo')] and receives the literal string "app.foo" instead of the service. Why?  <small>_(medium · trap)_</small>

- A. A bare string is a literal value; to inject a service use #[Autowire(service: 'app.foo')]
- B. The app.foo service must be made public first
- C. #[Autowire] cannot inject services at all
- D. Service ids need an @ prefix inside attributes

??? success "Answer Q55"
    **A**

    In #[Autowire], a bare string is interpreted as a literal value (or a %param% / %env()% expression), not a service reference. Use the named argument service: to pin a service id. Visibility is irrelevant and no @ prefix is used in attributes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q56.** A constructor type-hints an interface that has no implementation and no alias. What does the container build do?  <small>_(medium · debug)_</small>

- A. Fails with a compile-time 'Cannot autowire ... no such service' error — not a silent null
- B. Injects null
- C. Picks any registered class arbitrarily
- D. Defers resolution to runtime

??? success "Answer Q56"
    **A**

    Autowiring an unregistered type is a hard build failure. Silent null only happens if you explicitly opt in with a nullable argument and default (?Type $x = null). Autowiring never guesses an arbitrary class or defers to runtime — the misconception is expecting null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q57.** What interface does Symfony's ServiceLocator implement?  <small>_(medium · single)_</small>

- A. Psr\Container\ContainerInterface (PSR-11)
- B. Symfony's own ContainerInterface
- C. IteratorAggregate only
- D. CompilerPassInterface

??? success "Answer Q57"
    **A**

    ServiceLocator is a PSR-11 container exposing get() and has() over a fixed, compile-time set of services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html#service-locators)

**Q58.** What does ServiceSubscriberInterface::getSubscribedServices() declare?  <small>_(medium · single)_</small>

- A. The set of services the subscriber may lazily use, injected as a locator
- B. Instantiated services returned eagerly
- C. The compiler passes to register
- D. The whole container

??? success "Answer Q58"
    **A**

    It declares a whitelist; the container injects a matching ServiceLocator so services are built only when requested.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q59.** Which trait should a Symfony 8 service subscriber use with #[SubscribedService] methods?  <small>_(medium · trap)_</small>

- A. ServiceMethodsSubscriberTrait
- B. ServiceSubscriberTrait (deprecated in 7.1)
- C. ServiceLocatorTrait
- D. ContainerAwareTrait

??? success "Answer Q59"
    **A**

    The older ServiceSubscriberTrait was deprecated in 7.1 (symfony/contracts v3.5); Symfony 8 uses ServiceMethodsSubscriberTrait together with #[SubscribedService] methods whose return type names the service. ServiceLocatorTrait builds a locator class, and ContainerAwareTrait is the removed container-injection anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q60.** With #[AutowireLocator(['stripe' => StripeGateway::class, 'paypal' => PayPalGateway::class])] ContainerInterface $gateways, what happens on $gateways->get('stripe')?  <small>_(medium · code)_</small>

- A. Only StripeGateway is instantiated (lazily); PayPalGateway is never built
- B. Both gateways are instantiated up front
- C. It returns the class-name string 'stripe'
- D. It throws unless both gateways are public

??? success "Answer Q60"
    **A**

    #[AutowireLocator] builds a PSR-11 locator that instantiates a service only when get() requests it, so fetching 'stripe' builds StripeGateway and leaves PayPalGateway cold. Locators do not require member services to be public, and they build instances, not return strings.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q61.** A locator built for keys 'stripe' and 'paypal' is called with a user-supplied key 'unknown'. What happens?  <small>_(medium · debug)_</small>

- A. It throws ServiceNotFoundException — validate with has() before get()
- B. It returns null
- C. It returns the first declared service
- D. It builds a new empty service on the fly

??? success "Answer Q61"
    **A**

    A locator's set is fixed at compile time, so get() on a key outside the whitelist throws; unlike the main container there is no NULL_ON_INVALID mode. Guard untrusted keys with has() first. It never returns null or falls back to another service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

**Q62.** A service is defined with shared: false. What happens on repeated $container->get() calls for it?  <small>_(hard · internals)_</small>

- A. A brand-new instance is returned on every call
- B. The same cached instance is returned each time
- C. A ServiceNotFoundException after the first call
- D. It is inlined and can no longer be fetched

??? success "Answer Q62"
    **A**

    shared defaults to true, so the first get() builds and caches the instance and later calls return the same object. shared: false disables caching, so the container rebuilds the service on every request. This is orthogonal to public/private — the misconception is thinking non-shared implies private.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/shared.html)

**Q63.** Which sequence correctly describes container compilation?  <small>_(hard · internals)_</small>

- A. ContainerBuilder::compile() runs the PassConfig passes, freezes parameters, then PhpDumper writes the cached class
- B. PhpDumper runs first, then the compiler passes, then parameters freeze
- C. Parameters freeze before any pass runs, then the class is dumped, then passes run
- D. Passes run lazily at runtime on the first get() call

??? success "Answer Q63"
    **A**

    compile() executes the passes in PassConfig phase order, then freezes the parameter bag (making it a FrozenParameterBag), then PhpDumper writes the optimised class to var/cache. It all happens at build time; nothing about compilation is deferred to runtime, which is the key misconception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dependency_injection/compilation.html)

**Q64.** For the router, which statement about id, class and autowiring alias is correct?  <small>_(hard · internals)_</small>

- A. The id is 'router', the class is a concrete Router, and an Alias maps RouterInterface to the id
- B. The id, class and alias are all the string 'router'
- C. The autowiring alias is the class FQCN pointing at the interface
- D. There is no alias; autowiring matches the id string directly

??? success "Answer Q64"
    **A**

    These are three distinct keys. FrameworkExtension registers the service under the id 'router' with a concrete class, then adds an autowiring alias from the interface FQCN (RouterInterface) to that id so type-hints resolve. debug:autowiring lists those aliases; debug:container inspects the id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/debug.html)

**Q65.** What does %env(int:default:app.timeout:TIMEOUT)% do?  <small>_(hard · internals)_</small>

- A. Reads TIMEOUT, falls back to the app.timeout parameter when unset, then casts the result to int
- B. Casts app.timeout to int and ignores TIMEOUT entirely
- C. Reads a parameter literally named 'int'
- D. Casts TIMEOUT to int, then defaults to app.timeout only if the cast fails

??? success "Answer Q65"
    **A**

    Env processors chain right-to-left. The innermost segment reads the env var TIMEOUT; default:app.timeout supplies the app.timeout parameter as a fallback when TIMEOUT is unset; int: then casts the resolved value. The misconception is reading it left-to-right, which inverts the meaning.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration/env_var_processors.html)

**Q66.** A constructor arg is #[Autowire('%env(MAX)%')] int $max, but you hit a type error because a string was passed. What is wrong?  <small>_(hard · trap)_</small>

- A. %env(MAX)% yields a string; add a cast processor: %env(int:MAX)%
- B. Environment variables cannot be injected into constructors
- C. MAX must be declared as a parameter before it can be read
- D. #[Autowire] does not support env placeholders

??? success "Answer Q66"
    **A**

    Raw env values are always strings until a processor casts them, so %env(MAX)% is a string while the argument expects int. Use %env(int:MAX)%. #[Autowire] fully supports env placeholders and no prior parameter declaration is needed; the trap is assuming env values are already typed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration/env_var_processors.html)

**Q67.** After ContainerBuilder::compile(), what happens to the parameter bag?  <small>_(hard · internals)_</small>

- A. It becomes a read-only FrozenParameterBag
- B. It stays mutable so parameters can change at runtime
- C. It is discarded and every parameter is inlined only
- D. It is serialized into the .env file

??? success "Answer Q67"
    **A**

    During build the ContainerBuilder uses a mutable ParameterBag; compile() freezes it into a FrozenParameterBag, after which parameters are read-only. This is why parameters are compile-time constants — the misconception is expecting to mutate parameters at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/configuration.html#configuration-parameters)

**Q68.** You add the alias App\Report\ReporterInterface: '@App\Report\Missing' but the target service does not exist. What happens?  <small>_(hard · debug)_</small>

- A. A compile-time error — an alias to a non-existent target breaks the build; it is not a silent null
- B. The interface silently resolves to null at runtime
- C. The alias is quietly ignored
- D. A ServiceLocator is injected in its place

??? success "Answer Q68"
    **A**

    An alias must point at an existing service id; a dangling alias fails the container build. Optional dependencies use nullable constructor args or NULL_ON_INVALID_REFERENCE, not a broken alias. The misconception is expecting a missing target to become null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/alias_private.html)

**Q69.** With two decorators on one id, a higher decoration_priority means the decorator is...  <small>_(hard · trap)_</small>

- A. Applied first and sits closer to the original (innermost)
- B. Applied last and is the outermost
- C. Ignored
- D. Made public automatically

??? success "Answer Q69"
    **A**

    Higher priority decorators are applied first and end up innermost; consumers receive the lowest-priority, outermost decorator.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html#decoration-priority)

**Q70.** Two decorators target the same service. You need caching wrapped directly around the original and logging on the outside so consumers hit logging first. How do you set decoration_priority?  <small>_(hard · scenario)_</small>

- A. Caching gets the higher priority (e.g. 20), logging the lower (e.g. 10)
- B. Logging gets the higher priority, caching the lower
- C. Both must be equal so ordering is deterministic
- D. Priority has no effect on the chain order

??? success "Answer Q70"
    **A**

    Higher decoration_priority is applied first and ends up innermost (closest to the original), so caching needs the higher number to sit directly around the original, and logging the lower number to become the outermost wrapper consumers hit first. Assuming lower priority runs first inverts the chain.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html#decoration-priority)

**Q71.** decoration_on_invalid: null is set, but .inner is typed as non-nullable MailerInterface and the decorated target is absent. What happens?  <small>_(hard · config)_</small>

- A. A TypeError — null is injected as .inner but the non-nullable argument rejects it; type it ?MailerInterface and guard with ?->
- B. The decorator is silently removed
- C. An exception is thrown at compile time
- D. An empty stub mailer is created

??? success "Answer Q71"
    **A**

    With null, the compiler injects null as .inner; if the argument type is not nullable this becomes a TypeError at instantiation. The fix is a nullable type (?MailerInterface) and nullsafe delegation. ignore (not null) is what removes the decorator; exception is the default that throws at build.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_decoration.html)

**Q72.** What is the key difference between tagged_iterator and tagged_locator?  <small>_(hard · single)_</small>

- A. tagged_iterator yields already-instantiated services; tagged_locator gives a lazy ServiceLocator built on get()
- B. Both eagerly instantiate every tagged service
- C. tagged_iterator is lazy while tagged_locator is eager
- D. tagged_locator returns raw Definition objects

??? success "Answer Q72"
    **A**

    tagged_iterator injects an iterable of instances (use it when you always iterate all of them), while tagged_locator injects a ServiceLocator that builds each service lazily on get() and is keyed for pick-one-of-many. The trap is swapping their laziness.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q73.** How is the key of each tagged_locator entry determined?  <small>_(hard · config)_</small>

- A. From an index_by tag attribute, a default_index_method static method (e.g. getName), or #[AsTaggedItem(index:)]
- B. It is always the service id
- C. It is always the class FQCN
- D. It is assigned randomly at compile time

??? success "Answer Q73"
    **A**

    The locator key comes from the index_by tag attribute, a static method named by default_index_method (commonly getName/getDefaultIndexName), or an #[AsTaggedItem(index:)] attribute — not the service id by default. If two services resolve to the same key, the later one silently overwrites the earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/tags.html)

**Q74.** In a Symfony 8 AbstractBundle, where do the config schema and the service wiring live?  <small>_(hard · internals)_</small>

- A. configure() defines the tree and loadExtension() wires services — both on the bundle class, with no separate Extension file
- B. Only in a separate Extension class
- C. Exclusively in services.yaml
- D. In the Kernel::build() method

??? success "Answer Q74"
    **A**

    AbstractBundle streamlines bundles by folding the schema (configure) and the extension logic (loadExtension) onto the bundle class itself, so a separate Configuration/Extension pair is no longer required. Kernel::build() registers compiler passes, not bundle semantic config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/configuration.html)

**Q75.** Your bundle must set a default framework option before FrameworkBundle loads. What do you call, and when does it run?  <small>_(hard · code)_</small>

- A. prependExtensionConfig('framework', [...]) inside prepend()/prependExtension(), which runs before all load() calls
- B. setParameter() inside load(), which runs first
- C. prependExtensionConfig() inside load(), after the other bundles
- D. addCompilerPass() at runtime

??? success "Answer Q75"
    **A**

    PrependExtensionInterface::prepend() (or prependExtension() on AbstractBundle) runs before every extension's load(), and prependExtensionConfig() injects config into another bundle's namespace. Doing it in load() would be too late, and setParameter() sets a parameter, not another bundle's config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/prepend_extension.html)

**Q76.** Ledger has a private constructor and a static open(string $path). How do you register it as a service?  <small>_(hard · config)_</small>

- A. factory: 'App\Payment\Ledger::open' with the path in arguments passed to open()
- B. Pass the path in arguments to the constructor as usual
- C. factory: ['@App\Payment\Ledger', 'open']
- D. It cannot be registered as a service

??? success "Answer Q76"
    **A**

    A static factory in the 'Class::method' string form bypasses the private constructor, and arguments are passed to open(), not a constructor. The instance-method array form would require an existing service instance, which the private constructor prevents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/factories.html)

**Q77.** In which phase should a pass that removes a service run, and why not TYPE_BEFORE_OPTIMIZATION?  <small>_(hard · scenario)_</small>

- A. TYPE_REMOVE — removing earlier could delete a service that autowiring (the optimization phase) still needs to reference
- B. TYPE_BEFORE_OPTIMIZATION is fine; phase order never matters
- C. TYPE_AFTER_REMOVING, because removal always happens last
- D. TYPE_OPTIMIZE, alongside autowiring

??? success "Answer Q77"
    **A**

    Removal belongs in TYPE_REMOVE. Doing it before optimization would delete a service that the autowiring/optimization phase might still reference, breaking resolution. AFTER_REMOVING runs once pruning is done, and mixing it into OPTIMIZATION races with autowiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q78.** Two passes are registered in the same phase with priorities 10 and 100. Which runs first?  <small>_(hard · trap)_</small>

- A. The priority-100 pass — higher priority runs earlier within a phase
- B. The priority-10 pass runs first
- C. The order is undefined
- D. They run simultaneously

??? success "Answer Q78"
    **A**

    Within a phase, addCompilerPass orders by priority with higher running first. The trap is assuming lower numbers run first (as some other Symfony orderings work); for compiler passes higher priority is earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/compiler_passes.html)

**Q79.** What is the literal id of a named autowiring alias, e.g. for a Monolog channel logger?  <small>_(hard · internals)_</small>

- A. Literally 'Psr\Log\LoggerInterface $requestLogger' — matched by the parameter name
- B. requestLogger
- C. logger.requestLogger
- D. @requestLogger

??? success "Answer Q79"
    **A**

    A named autowiring alias id is the full type followed by the variable name, 'Type $paramName'. Autowiring matches it when your constructor parameter is named identically — which is fragile, so #[Target('requestLogger')] states the intent explicitly and survives parameter renames.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q80.** Which techniques resolve autowiring ambiguity when several services implement one interface? (choose 3)  <small>_(hard · multiple)_</small>

- A. #[Target('name')] on the parameter
- B. #[Autowire(service: 'id')] to pin an exact service
- C. A named autowiring alias 'Type $paramName'
- D. Making all candidate services public

??? success "Answer Q80"
    **A, B, C**

    Ambiguity is resolved by explicitly choosing an implementation: a named alias, #[Target], #[Autowire(service:)], or bind. Making services public only affects fetchability by id and does nothing to disambiguate autowiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/autowiring.html)

**Q81.** You have five heavy payment gateways but use exactly one per request, chosen by name. What is the best tool?  <small>_(hard · scenario)_</small>

- A. A service locator (e.g. #[AutowireLocator]) so only the chosen gateway is built
- B. A tagged_iterator, iterating all five every request
- C. Injecting all five gateways in the constructor
- D. Injecting the whole container

??? success "Answer Q81"
    **A**

    Pick-one-of-many with heavy dependencies is the textbook case for a lazy locator: only the selected gateway is instantiated. A tagged_iterator or constructor-injecting all five would eagerly build every gateway, and injecting the whole container is the anti-pattern the locator replaces.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/service_container/service_subscribers_locators.html)

---

<small>Back to [Chapter Exams](index.md) · [Dependency Injection](../dependency-injection/index.md)</small>
