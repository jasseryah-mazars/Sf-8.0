# Revision Sheet — Dependency Injection

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Dependency Injection](../../dependency-injection/index.md).

## Autowiring
- Autowiring injects objects by type-hint at compile time.
- Disambiguate with named aliases, `#[Target]`, `#[Autowire(service:)]`, or `bind`.
- Scalars are never autowired — bind them explicitly.
- Ambiguity is a build error, not a silent choice.

**Cheat:** `AutowirePass`: type-hint → service id / alias. Named alias id = `Type $paramName`; `#[Target('name')]` = explicit. `#[Autowire(service:/value:/env:/param:/expression:)]`. Debug: `debug:autowiring [--all]`.

## Built-in Services
- Autowire framework services by their **interface**, not their id.
- `debug:container` and `debug:autowiring` are your discovery tools.
- id ≠ class ≠ autowiring alias.
- Inject `RequestStack`, never a raw `Request`.

**Cheat:** `router`, `event_dispatcher`, `http_kernel`, `request_stack`, `parameter_bag`, `logger`, `serializer`, `validator`, `cache.app`. Find a type: `debug:autowiring <needle>`; inspect: `debug:container <id>`. `--show-private` reveals hidden services.

## Compiler Passes
- A pass runs at compile time and rewrites `Definition`s.
- Register with `addCompilerPass()` — **no attribute exists**.
- Phases: before-opt → opt → before-removing → removing → after-removing.
- Prefer tagged arguments/autoconfigure; use a pass for real transformation logic.

**Cheat:** `CompilerPassInterface::process(ContainerBuilder $c)`. Register: `Kernel::build()` / `Bundle::build()` → `addCompilerPass($pass, phase, priority)`. `PassConfig::TYPE_*`; default = `TYPE_BEFORE_OPTIMIZATION`. `findTaggedServiceIds()`, `findDefinition()`, `new Reference($id)`.

## The Service Container
- A service is a container-managed object; value objects are not services.
- Build time = `ContainerBuilder` + `Definition`s; runtime = dumped container +
  instances.
- Compilation runs passes, resolves autowiring, removes private/unused services,
  then dumps a PHP class to `var/cache/`.
- Services are **private** and **shared** by default.

**Cheat:** `ContainerBuilder.compile()` → `PassConfig` → freeze → `PhpDumper` → cache. Private ≠ shared: independent flags. Both default to a "hidden, one instance" state. `get()` on private id → `ServiceNotFoundException`. `Definition`/`Reference`/`Alias`/`Parameter` = build-time metadata only.

## Service Decoration
- Decoration wraps a service transparently; the decorator takes over the id.
- `.inner` / `#[AutowireDecorated]` gives you the original.
- `decoration_priority`: higher = innermost (applied first).
- `decoration_on_invalid`: `exception` | `ignore` | `null`.

**Cheat:** YAML: `decorates:`, `arguments: { $x: '@.inner' }`, `decoration_priority`, `decoration_on_invalid`. Attrs: `#[AsDecorator(decorates: X::class)]` + `#[AutowireDecorated]`. `DecoratorServicePass` renames original → `.inner`, decorator → public id. Higher priority = innermost.

## Factories
- Factories build services the container cannot `new` directly.
- Static `[Class, 'm']`, instance `['@svc', 'm']`, invokable `'@svc'`.
- `arguments:` feed the factory method.
- No `#[Factory]` attribute — use `#[Autowire(factory:)]` or config.

**Cheat:** Static: `factory: 'Class::method'`. Instance: `['@svc', 'method']`. Invokable: `factory: '@svc'`. Args → factory method, not constructor. Attribute: `#[Autowire(factory: [F::class, 'create'])]`.

## Configuration Parameters
- Parameters (`%x%`) are frozen at compile time; env vars resolve at runtime.
- Env **processors** cast/transform and chain right-to-left.
- Inject values via `bind`, `#[Autowire(param:/env:)]`, or `ParameterBagInterface`.
- Prefer injecting the single value over the whole parameter bag.

**Cheat:** `%param%` frozen · `%env(VAR)%` runtime · `%%` literal percent. Processors: `int bool float json csv default resolve file base64 enum`. `#[Autowire(param: 'x')]`, `#[Autowire(env: 'X')]`, `#[Autowire('%env(int:X)%')]`. `FrozenParameterBag` = read-only after `compile()`.

## Service Registration
- `_defaults` + `App\:` glob + `autowire`/`autoconfigure` covers most services.
- Service id = FQCN; a specific block overrides the glob.
- Manual `arguments`/`calls`/`aliases` for what conventions cannot express.
- `#[Autoconfigure]` puts per-class wiring on the class itself.

**Cheat:** `resource` = register glob; `exclude` = skip non-services. `autowire` args-by-type; `autoconfigure` tags-by-interface — independent. `arguments`, `calls` (setters), `aliases` (`Interface: '@Class'`). `#[Autoconfigure(lazy:, public:, tags:, bind:)]`.

## Semantic (Bundle) Configuration
- `Configuration` + `TreeBuilder` = schema; `Extension::load()` = acts on it.
- Config is merged, validated, defaulted, then passed to `load()`.
- `prepend()` runs first and configures other bundles.
- `AbstractBundle` folds configure/load onto the bundle class.

**Cheat:** `ConfigurationInterface::getConfigTreeBuilder()` / `AbstractBundle::configure()`. `Extension::load(array $configs, ContainerBuilder $c)`. `prependExtensionConfig('other_bundle', [...])`. `config:dump-reference` (schema) vs `debug:config` (values).

## Service Locators
- A locator lazily builds a fixed, declared set of services (PSR-11).
- Prefer it over injecting the whole container.
- `#[AutowireLocator]` is the quick way; subscribers declare via
  `getSubscribedServices()` / `#[SubscribedService]`.
- Use for pick-one-of-many or heavy, rarely-used deps.

**Cheat:** `#[AutowireLocator([...])]` → PSR-11 `ContainerInterface`. `!service_locator` in YAML. Subscriber: `ServiceSubscriberInterface` + `ServiceMethodsSubscriberTrait` + `#[SubscribedService]`. Lazy, whitelisted, not the whole container.

## Tags
- Tags are build-time labels; a collector must consume them.
- `tagged_iterator` = instances; `tagged_locator` = lazy keyed locator.
- `priority` orders (higher first); index via `default_index_method` /
  `#[AsTaggedItem]`.
- Autoconfigure a tag onto an interface to avoid manual tagging.

**Cheat:** Attrs: `#[AutowireIterator('tag')]`, `#[AutowireLocator('tag', defaultIndexMethod:)]`, `#[AutoconfigureTag('tag')]`, `#[AsTaggedItem(index:, priority:)]`. YAML: `!tagged_iterator`, `!tagged_locator`, `_instanceof`. Inspect: `debug:container --tag <name>`.
