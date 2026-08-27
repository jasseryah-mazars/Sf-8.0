# Flashcards — Dependency Injection

81 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

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

??? question "5. True or False: a service being public and a service being shared mean the same thing."
    **✅ False**

    They are independent flags. Public means fetchable by id via get(); shared means the same instance is reused across get() calls. The default service is private and shared. A common trap confuses the two — a service can be public and non-shared, or private and shared, in any combination.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "6. A service is defined with shared: false. What happens on repeated $container->get() calls for it?"
    **✅ A brand-new instance is returned on every call**

    shared defaults to true, so the first get() builds and caches the instance and later calls return the same object. shared: false disables caching, so the container rebuilds the service on every request. This is orthogonal to public/private — the misconception is thinking non-shared implies private.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/shared.html)

??? question "7. A developer calls $this->container->get(MailerInterface::class) inside a service and gets a ServiceNotFoundException, even though the mailer works elsewhere. Why?"
    **✅ MailerInterface resolves to a private service, which is not fetchable by id — inject it via the constructor instead**

    The mailer service is private (the default), so it can only be injected, not fetched by id from the public container — get() therefore throws. The fix is constructor injection/autowiring, not making it public. It is registered and the container is compiled; the misconception is treating get() as a general-purpose lookup instead of using DI.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "8. Which sequence correctly describes container compilation?"
    **✅ ContainerBuilder::compile() runs the PassConfig passes, freezes parameters, then PhpDumper writes the cached class**

    compile() executes the passes in PassConfig phase order, then freezes the parameter bag (making it a FrozenParameterBag), then PhpDumper writes the optimised class to var/cache. It all happens at build time; nothing about compilation is deferred to runtime, which is the key misconception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dependency_injection/compilation.html)

??? question "9. How should you access the current request inside a service?"
    **✅ Inject RequestStack and call getCurrentRequest()**

    The Request is per-cycle and can change across sub-requests, so it is not injectable directly. Inject RequestStack and read the current request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

??? question "10. Which command lists what a given type-hint autowires to?"
    **✅ debug:autowiring**

    debug:autowiring shows the types you can type-hint and which service each resolves to; debug:container inspects a definition by id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

??? question "11. By default, debug:container hides which services?"
    **✅ Private services (shown only with --show-private)**

    debug:container lists public services and aliases; add --show-private to include private ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

??? question "12. A service injects RequestStack and calls $this->requestStack->getCurrentRequest()->getLocale(); it fatals when run from a console command. Why?"
    **✅ getCurrentRequest() returns null when there is no active request (e.g. CLI), so use the nullsafe operator ?->**

    Outside the HTTP cycle (console commands, Messenger workers) there is no current request, so getCurrentRequest() returns null and the method call fatals. Guard with getCurrentRequest()?->getLocale() or an early null check. RequestStack is autowirable everywhere; the trap is assuming a request always exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/request.html)

??? question "13. For the router, which statement about id, class and autowiring alias is correct?"
    **✅ The id is 'router', the class is a concrete Router, and an Alias maps RouterInterface to the id**

    These are three distinct keys. FrameworkExtension registers the service under the id 'router' with a concrete class, then adds an autowiring alias from the interface FQCN (RouterInterface) to that id so type-hints resolve. debug:autowiring lists those aliases; debug:container inspects the id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

??? question "14. Which are correct ways to obtain framework services in your code? (choose 2)"
    **✅ Autowire by type-hinting the interface, e.g. LoggerInterface ; Use debug:autowiring to discover which type resolves to which service**

    Autowiring by interface is the idiomatic path, and debug:autowiring is the discovery tool for finding the right type-hint. A raw Request cannot be injected (use RequestStack), and pulling services with $container->get() in business code is the service-locator anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/debug.html)

??? question "15. When is %env(DATABASE_URL)% resolved?"
    **✅ At runtime, via an env-var processor**

    Env placeholders resolve at runtime so a single compiled container works across environments; parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

??? question "16. What does the expression %env(int:MAX)% produce?"
    **✅ The value of MAX cast to an integer**

    The int: processor casts the raw env string to an integer. Processors chain right-to-left.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/env_var_processors.html)

??? question "17. Which attribute injects the container parameter app.name into a constructor argument?"
    **✅ #[Autowire(param: 'app.name')]**

    param: names a container parameter; a bare string without %% is a literal, and env: reads an environment variable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "18. How do you write a literal percent sign inside a parameter value?"
    **✅ Double it: %%**

    A doubled percent escapes to a single literal % so it is not treated as a parameter reference.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-parameters)

??? question "19. What does %env(int:default:app.timeout:TIMEOUT)% do?"
    **✅ Reads TIMEOUT, falls back to the app.timeout parameter when unset, then casts the result to int**

    Env processors chain right-to-left. The innermost segment reads the env var TIMEOUT; default:app.timeout supplies the app.timeout parameter as a fallback when TIMEOUT is unset; int: then casts the resolved value. The misconception is reading it left-to-right, which inverts the meaning.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/env_var_processors.html)

??? question "20. A constructor arg is #[Autowire('%env(MAX)%')] int $max, but you hit a type error because a string was passed. What is wrong?"
    **✅ %env(MAX)% yields a string; add a cast processor: %env(int:MAX)%**

    Raw env values are always strings until a processor casts them, so %env(MAX)% is a string while the argument expects int. Use %env(int:MAX)%. #[Autowire] fully supports env placeholders and no prior parameter declaration is needed; the trap is assuming env values are already typed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration/env_var_processors.html)

??? question "21. After ContainerBuilder::compile(), what happens to the parameter bag?"
    **✅ It becomes a read-only FrozenParameterBag**

    During build the ContainerBuilder uses a mutable ParameterBag; compile() freezes it into a FrozenParameterBag, after which parameters are read-only. This is why parameters are compile-time constants — the misconception is expecting to mutate parameters at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-parameters)

??? question "22. What does ParameterBagInterface::get('app.missing') do for an undefined parameter?"
    **✅ Throws ParameterNotFoundException — use has() first for optional lookups**

    Reading a missing parameter throws ParameterNotFoundException; it never returns null. Guard optional lookups with has() before get(). The common bug is assuming an absent parameter silently becomes null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-parameters)

??? question "23. True or False: environment variables referenced with %env(...)% are frozen into the compiled container cache at compile time."
    **✅ False**

    The compiler replaces %env(...)% with a placeholder and the EnvVarProcessor resolves it at runtime, which is exactly why one compiled container works across environments and changing an env var needs no cache rebuild. Only plain parameters (%x%) are frozen at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuration-based-on-environment-variables)

??? question "24. Using the App\: resource glob, what is a service's id?"
    **✅ Its fully-qualified class name (FQCN)**

    PSR-4 auto-registration creates one definition per class using the FQCN as the service id.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "25. What does autoconfigure: true do (as opposed to autowire)?"
    **✅ Applies tags/flags based on implemented interfaces and attributes**

    Autoconfigure adds tags automatically (e.g. event subscriber); autowire is the separate flag that fills arguments by type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html#the-autoconfigure-option)

??? question "26. How do you make an interface type-hint resolve to a concrete class?"
    **✅ Define an alias, e.g. Interface: '@Class'**

    An alias from the interface id to the concrete service lets autowiring resolve the interface type-hint.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/alias_private.html)

??? question "27. Given _defaults with autowire: true, autoconfigure: true, public: false and an App\: resource glob, what is true of a class under src/?"
    **✅ It is registered private, with arguments autowired by type and tags applied by interface**

    _defaults sets the baseline: public: false makes it private, autowire fills constructor arguments by type, and autoconfigure applies tags based on implemented interfaces. The id is the FQCN. The glob registers every class in the directory, not just annotated ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "28. The App\: glob registers a class, and a later named block redefines the same id. Which definition wins?"
    **✅ The later, more specific block overrides the glob for that id**

    Registration order matters: the glob first registers everything, then a later, more specific entry for the same id overrides it. This is the idiomatic way to tweak one autowired service. It is not an error and the glob does not win.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container.html)

??? question "29. Which argument cannot be supplied by autowiring and must come from bind, #[Autowire], or a parameter?"
    **✅ A scalar string such as a directory path**

    Autowiring resolves objects by type-hint; it can never guess scalars (strings, ints, arrays). Those must be bound explicitly via bind, #[Autowire], or a parameter. Objects, aliases, and single implementations all autowire fine.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "30. You add the alias App\Report\ReporterInterface: '@App\Report\Missing' but the target service does not exist. What happens?"
    **✅ A compile-time error — an alias to a non-existent target breaks the build; it is not a silent null**

    An alias must point at an existing service id; a dangling alias fails the container build. Optional dependencies use nullable constructor args or NULL_ON_INVALID_REFERENCE, not a broken alias. The misconception is expecting a missing target to become null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/alias_private.html)

??? question "31. In a decorator definition, what does @.inner reference?"
    **✅ The original (decorated) service, renamed by the compiler**

    DecoratorServicePass renames the decorated service and exposes it as .inner so the decorator can delegate to it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "32. Which attribute injects the decorated (inner) service into a decorator?"
    **✅ #[AutowireDecorated]**

    #[AsDecorator] declares the decoration; #[AutowireDecorated] resolves the parameter to the .inner service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "33. With two decorators on one id, a higher decoration_priority means the decorator is..."
    **✅ Applied first and sits closer to the original (innermost)**

    Higher priority decorators are applied first and end up innermost; consumers receive the lowest-priority, outermost decorator.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html#decoration-priority)

??? question "34. decoration_on_invalid: ignore does what when the decorated service is missing?"
    **✅ Removes the decorator entirely**

    ignore drops the decorator; null would inject null; exception (the default) throws when the target is absent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "35. Two decorators target the same service. You need caching wrapped directly around the original and logging on the outside so consumers hit logging first. How do you set decoration_priority?"
    **✅ Caching gets the higher priority (e.g. 20), logging the lower (e.g. 10)**

    Higher decoration_priority is applied first and ends up innermost (closest to the original), so caching needs the higher number to sit directly around the original, and logging the lower number to become the outermost wrapper consumers hit first. Assuming lower priority runs first inverts the chain.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html#decoration-priority)

??? question "36. A decorator injects the service by its own (decorated) id instead of .inner and hits infinite recursion. What is the fix?"
    **✅ Inject @.inner (or use #[AutowireDecorated]) to reference the renamed original**

    Because the decorator takes over the decorated service's public id, referencing that id inside the decorator injects the decorator itself, causing infinite recursion. You must reference the renamed original via .inner or #[AutowireDecorated]. Visibility and priority are unrelated to the loop.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "37. decoration_on_invalid: null is set, but .inner is typed as non-nullable MailerInterface and the decorated target is absent. What happens?"
    **✅ A TypeError — null is injected as .inner but the non-nullable argument rejects it; type it ?MailerInterface and guard with ?->**

    With null, the compiler injects null as .inner; if the argument type is not nullable this becomes a TypeError at instantiation. The fix is a nullable type (?MailerInterface) and nullsafe delegation. ignore (not null) is what removes the decorator; exception is the default that throws at build.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_decoration.html)

??? question "38. What does a tagged_locator argument inject?"
    **✅ A lazy ServiceLocator keyed by an index**

    tagged_locator injects a ServiceLocator that instantiates services on demand, keyed by the configured index; tagged_iterator yields instances.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "39. A higher priority on a tag places the service where in the tagged iterator?"
    **✅ Earlier (tagged collections are sorted by descending priority)**

    Tagged services are ordered by descending priority, so higher priority comes first.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html#tagged-services-with-priority)

??? question "40. How can every implementation of an interface receive a tag automatically?"
    **✅ Use #[AutoconfigureTag] on the interface or _instanceof in YAML**

    Autoconfiguration maps an interface to a tag so all implementers are tagged without manual annotation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "41. What is the key difference between tagged_iterator and tagged_locator?"
    **✅ tagged_iterator yields already-instantiated services; tagged_locator gives a lazy ServiceLocator built on get()**

    tagged_iterator injects an iterable of instances (use it when you always iterate all of them), while tagged_locator injects a ServiceLocator that builds each service lazily on get() and is keyed for pick-one-of-many. The trap is swapping their laziness.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "42. How is the key of each tagged_locator entry determined?"
    **✅ From an index_by tag attribute, a default_index_method static method (e.g. getName), or #[AsTaggedItem(index:)]**

    The locator key comes from the index_by tag attribute, a static method named by default_index_method (commonly getName/getDefaultIndexName), or an #[AsTaggedItem(index:)] attribute — not the service id by default. If two services resolve to the same key, the later one silently overwrites the earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "43. True or False: adding a tag to a service changes its behaviour automatically, even with no collector consuming that tag."
    **✅ False**

    A tag is inert build-time metadata; on its own it does nothing. Something — a tagged_iterator/tagged_locator argument or a compiler pass calling findTaggedServiceIds() — must consume the tag for it to have any effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "44. What does #[AutowireIterator('app.handler')] on an iterable $handlers argument inject?"
    **✅ An iterable of all app.handler-tagged services, ordered by descending priority**

    #[AutowireIterator] is the attribute form of tagged_iterator: it injects an iterable of the instantiated tagged services, ordered by descending priority. #[AutowireLocator] would give the lazy keyed locator; the attribute does not filter down to one service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "45. Which class validates and defaults a bundle's configuration schema?"
    **✅ Configuration, via a TreeBuilder**

    Configuration defines allowed keys, types, defaults and validation; Extension::load() only consumes the processed result.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "46. When does prepend() run relative to the extensions' load() calls?"
    **✅ Before all load() calls**

    Prepend runs first so a bundle can inject default configuration into other bundles before they load.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/prepend_extension.html)

??? question "47. Which command prints a bundle's configuration reference tree?"
    **✅ config:dump-reference**

    config:dump-reference dumps the schema defined by Configuration; debug:config shows the currently resolved values.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "48. In a Symfony 8 AbstractBundle, where do the config schema and the service wiring live?"
    **✅ configure() defines the tree and loadExtension() wires services — both on the bundle class, with no separate Extension file**

    AbstractBundle streamlines bundles by folding the schema (configure) and the extension logic (loadExtension) onto the bundle class itself, so a separate Configuration/Extension pair is no longer required. Kernel::build() registers compiler passes, not bundle semantic config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "49. Which command shows the currently resolved configuration values (not the schema) for a bundle?"
    **✅ debug:config**

    debug:config prints the merged, resolved values in effect; config:dump-reference prints the schema (allowed keys, types, defaults) defined by Configuration. Confusing the two is a common trap — one shows what is set, the other what is allowed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "50. Your bundle must set a default framework option before FrameworkBundle loads. What do you call, and when does it run?"
    **✅ prependExtensionConfig('framework', [...]) inside prepend()/prependExtension(), which runs before all load() calls**

    PrependExtensionInterface::prepend() (or prependExtension() on AbstractBundle) runs before every extension's load(), and prependExtensionConfig() injects config into another bundle's namespace. Doing it in load() would be too late, and setParameter() sets a parameter, not another bundle's config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/prepend_extension.html)

??? question "51. A bundle named AcmeBlogBundle exposes its configuration under which root key by convention?"
    **✅ acme_blog (snake_case of the bundle name minus 'Bundle')**

    The root key is derived from the extension/bundle name: the class name minus the Bundle suffix, converted to snake_case, giving acme_blog. The misconception is using the class name verbatim or keeping the Bundle suffix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/bundles/configuration.html)

??? question "52. For a factory-built service, where are its arguments passed?"
    **✅ To the factory method**

    With a factory, the container calls the factory and passes the definition's arguments to it, not to a constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "53. How do you configure a factory produced value via attributes?"
    **✅ #[Autowire(factory: [Factory::class, 'create'])]**

    There is no dedicated #[Factory] attribute; factories are configured with #[Autowire(factory:)] or in YAML/PHP config.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "54. How is an instance-method factory referenced in YAML?"
    **✅ factory: ['@service_id', 'method']**

    An array of [reference, method] denotes a method call on a service; a static factory uses the 'Class::method' string form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "55. factory: '@svc::method' throws an error. What is the correct instance-method form?"
    **✅ factory: ['@svc', 'method']**

    The '@svc::method' string is invalid syntax for an instance-method factory; use the array form ['@svc', 'method']. The 'Class::method' string form is reserved for static factories. The other forms are not recognised.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "56. How is an invokable factory service referenced in YAML?"
    **✅ factory: '@factory_service' (its __invoke method is called)**

    A bare service reference '@service' as the factory means the container calls the service's __invoke() and stores the return value. Explicitly naming __invoke via the '::' string form is invalid; the array form is used for named instance methods, not required for invokables.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "57. Ledger has a private constructor and a static open(string $path). How do you register it as a service?"
    **✅ factory: 'App\Payment\Ledger::open' with the path in arguments passed to open()**

    A static factory in the 'Class::method' string form bypasses the private constructor, and arguments are passed to open(), not a constructor. The instance-method array form would require an existing service instance, which the private constructor prevents.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/factories.html)

??? question "58. Which attribute registers a compiler pass? (choose one)"
    **✅ There is no attribute; register it via addCompilerPass() in Kernel/bundle build()**

    Compiler passes are registered programmatically via ContainerBuilder::addCompilerPass(), typically in Kernel::build() or a bundle's build(). There is no core attribute for this.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "59. What is the default phase for a compiler pass registered without one?"
    **✅ TYPE_BEFORE_OPTIMIZATION**

    PassConfig runs passes in phase order; unspecified passes run in the before-optimization phase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "60. What does ContainerBuilder::findTaggedServiceIds('t') return?"
    **✅ A map of service id => array of that tag's attribute sets**

    It returns definitions' ids each mapped to the attributes of every occurrence of the tag, used to wire collectors at compile time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/tags.html)

??? question "61. Inside a compiler pass process() method, what should you manipulate?"
    **✅ Definition objects (build-time metadata)**

    Compilation deals only with definitions; nothing is instantiated yet, so calling get() inside a pass is wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "62. In which phase should a pass that removes a service run, and why not TYPE_BEFORE_OPTIMIZATION?"
    **✅ TYPE_REMOVE — removing earlier could delete a service that autowiring (the optimization phase) still needs to reference**

    Removal belongs in TYPE_REMOVE. Doing it before optimization would delete a service that the autowiring/optimization phase might still reference, breaking resolution. AFTER_REMOVING runs once pruning is done, and mixing it into OPTIMIZATION races with autowiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "63. Two passes are registered in the same phase with priorities 10 and 100. Which runs first?"
    **✅ The priority-100 pass — higher priority runs earlier within a phase**

    Within a phase, addCompilerPass orders by priority with higher running first. The trap is assuming lower numbers run first (as some other Symfony orderings work); for compiler passes higher priority is earlier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "64. Inside process(), a pass calls $container->get(SomeService::class) and it fails. Why?"
    **✅ Compilation deals only with Definitions; nothing is instantiated yet — use findDefinition()/Reference instead**

    A compiler pass runs before any service exists, so you manipulate build-time Definition objects (findDefinition, addMethodCall, new Reference), never live instances. Calling get() during compilation is the classic mistake; visibility and spelling are not the cause here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "65. Which are valid places to register a compiler pass? (choose 2)"
    **✅ Kernel::build(ContainerBuilder $c) via addCompilerPass() ; A bundle's build(ContainerBuilder $c) via addCompilerPass()**

    Passes are registered programmatically with addCompilerPass() in the application Kernel::build() or a bundle's build(). There is no #[CompilerPass] attribute and no services.yaml tag that registers a pass — those are common invented answers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "66. In addCompilerPass(new MyPass(), PassConfig::TYPE_BEFORE_OPTIMIZATION, priority: 5), what do the 2nd and 3rd arguments control?"
    **✅ The compilation phase and the ordering priority within that phase**

    addCompilerPass(pass, phase, priority) takes the phase constant that determines when in PassConfig the pass runs, and a priority that orders passes within that phase (higher first). It has nothing to do with service ids, tags, or environments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/compiler_passes.html)

??? question "67. What can autowiring resolve automatically?"
    **✅ Object dependencies identified by their type-hint**

    Autowiring maps a type-hint to a service; scalars and env vars must be bound explicitly with bind or #[Autowire].

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "68. Two services implement one interface with no default alias. Autowiring by that interface..."
    **✅ Throws an ambiguity error at compile time**

    Ambiguity is a hard build error; you disambiguate with a named alias, #[Target], #[Autowire(service:)] or bind.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "69. What does the #[Target('requestLogger')] attribute do?"
    **✅ Selects the named autowiring alias explicitly, decoupled from the parameter name**

    #[Target] binds to a named autowiring alias by name, so renaming the constructor parameter does not break wiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html#fixing-non-autowireable-arguments)

??? question "70. What is the literal id of a named autowiring alias, e.g. for a Monolog channel logger?"
    **✅ Literally 'Psr\Log\LoggerInterface $requestLogger' — matched by the parameter name**

    A named autowiring alias id is the full type followed by the variable name, 'Type $paramName'. Autowiring matches it when your constructor parameter is named identically — which is fragile, so #[Target('requestLogger')] states the intent explicitly and survives parameter renames.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "71. A parameter has #[Autowire('app.foo')] and receives the literal string "app.foo" instead of the service. Why?"
    **✅ A bare string is a literal value; to inject a service use #[Autowire(service: 'app.foo')]**

    In #[Autowire], a bare string is interpreted as a literal value (or a %param% / %env()% expression), not a service reference. Use the named argument service: to pin a service id. Visibility is irrelevant and no @ prefix is used in attributes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "72. A constructor type-hints an interface that has no implementation and no alias. What does the container build do?"
    **✅ Fails with a compile-time 'Cannot autowire ... no such service' error — not a silent null**

    Autowiring an unregistered type is a hard build failure. Silent null only happens if you explicitly opt in with a nullable argument and default (?Type $x = null). Autowiring never guesses an arbitrary class or defers to runtime — the misconception is expecting null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "73. Which techniques resolve autowiring ambiguity when several services implement one interface? (choose 3)"
    **✅ #[Target('name')] on the parameter ; #[Autowire(service: 'id')] to pin an exact service ; A named autowiring alias 'Type $paramName'**

    Ambiguity is resolved by explicitly choosing an implementation: a named alias, #[Target], #[Autowire(service:)], or bind. Making services public only affects fetchability by id and does nothing to disambiguate autowiring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/autowiring.html)

??? question "74. How does a ServiceLocator differ from injecting the whole container?"
    **✅ It exposes only an explicitly declared, whitelisted set of services**

    A locator's set is explicit and analysable; injecting the whole container hides dependencies and is an anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "75. When does a ServiceLocator instantiate the services it holds?"
    **✅ Lazily, on get()**

    A locator defers construction until a service is actually requested, which is its main advantage over injecting all candidates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

??? question "76. What interface does Symfony's ServiceLocator implement?"
    **✅ Psr\Container\ContainerInterface (PSR-11)**

    ServiceLocator is a PSR-11 container exposing get() and has() over a fixed, compile-time set of services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators)

??? question "77. What does ServiceSubscriberInterface::getSubscribedServices() declare?"
    **✅ The set of services the subscriber may lazily use, injected as a locator**

    It declares a whitelist; the container injects a matching ServiceLocator so services are built only when requested.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "78. Which trait should a Symfony 8 service subscriber use with #[SubscribedService] methods?"
    **✅ ServiceMethodsSubscriberTrait**

    The older ServiceSubscriberTrait was deprecated in 7.1 (symfony/contracts v3.5); Symfony 8 uses ServiceMethodsSubscriberTrait together with #[SubscribedService] methods whose return type names the service. ServiceLocatorTrait builds a locator class, and ContainerAwareTrait is the removed container-injection anti-pattern.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "79. With #[AutowireLocator(['stripe' => StripeGateway::class, 'paypal' => PayPalGateway::class])] ContainerInterface $gateways, what happens on $gateways->get('stripe')?"
    **✅ Only StripeGateway is instantiated (lazily); PayPalGateway is never built**

    #[AutowireLocator] builds a PSR-11 locator that instantiates a service only when get() requests it, so fetching 'stripe' builds StripeGateway and leaves PayPalGateway cold. Locators do not require member services to be public, and they build instances, not return strings.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "80. A locator built for keys 'stripe' and 'paypal' is called with a user-supplied key 'unknown'. What happens?"
    **✅ It throws ServiceNotFoundException — validate with has() before get()**

    A locator's set is fixed at compile time, so get() on a key outside the whitelist throws; unlike the main container there is no NULL_ON_INVALID mode. Guard untrusted keys with has() first. It never returns null or falls back to another service.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

??? question "81. You have five heavy payment gateways but use exactly one per request, chosen by name. What is the best tool?"
    **✅ A service locator (e.g. #[AutowireLocator]) so only the chosen gateway is built**

    Pick-one-of-many with heavy dependencies is the textbook case for a lazy locator: only the selected gateway is instantiated. A tagged_iterator or constructor-injecting all five would eagerly build every gateway, and injecting the whole container is the anti-pattern the locator replaces.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)

---

<small>Back to [Flashcards](index.md) · [Dependency Injection](../../dependency-injection/index.md)</small>
