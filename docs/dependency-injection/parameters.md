# Configuration Parameters

!!! tip "In a nutshell"
    Parameters (`%app.name%`) are static config **frozen at compile time**; env
    vars (`%env(DATABASE_URL)%`) resolve **at runtime**, so one compiled cache
    works across environments. Highest-yield fact: env **processors** like
    `%env(int:MAX)%` cast/transform the raw string and chain right-to-left.

!!! example "Real-world analogy"
    Parameters are the recipe's printed measurements — fixed when the cookbook is
    printed (compile time). Environment variables are the "salt to taste" note:
    filled in at the stove (runtime), so the same printed recipe works in every
    kitchen. Env **processors** are the prep steps on that note — "dice", "convert
    to grams" — applied to the raw value before it hits the pan.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Define parameters and reference them with the `%param%` syntax.
    - [ ] Read environment variables and transform them with **env processors**
          (`%env(int:FOO)%`).
    - [ ] Inject parameters/env into services via **binding** and `#[Autowire]`,
          and read them at runtime through `ParameterBagInterface`.

    **Syllabus:** `Dependency Injection → Configuration Parameters` ·
    **Level:** Advanced / Expert ·
    **Est. time:** 35 min ·
    **Prerequisites:** [The Service Container](container.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
Un paramètre est figé une fois pour toutes à la compilation ; une variable d'environnement est lue à chaque démarrage — deux mécanismes, deux moments différents.

### Imagine dans la vraie vie
Les paramètres sont les mesures imprimées d'une recette — fixées au moment où le livre de cuisine est imprimé (compile time). Les variables d'environnement sont la note "sel à volonté" : remplie devant les fourneaux (runtime), pour que la même recette imprimée fonctionne dans chaque cuisine.

### Dans Symfony
`%env(DATABASE_URL)%` permet au **même** container compilé de fonctionner en local, en test et en production — seule la valeur de la variable d'environnement change, jamais le code ni la config compilée.

### Exemple simple
```yaml
parameters:
    app.page_size: '%env(int:APP_PAGE_SIZE)%' # processeur "int" convertit la chaîne
```

### Comment le mémoriser 🧠
Les processeurs d'env (`%env(int:MAX)%`) s'enchaînent **de droite à gauche** — comme des étapes de préparation appliquées une par une avant que le plat n'arrive à table.
---

## Theory

A **parameter** is a named configuration value stored in the container:
scalars, arrays, booleans. Parameters keep configuration out of your code and let
you reuse values. They are referenced with percent signs: `%app.timezone%`.

Environment variables are different: they are resolved **at runtime**, not baked
into the compiled container, so the same compiled cache works across environments.
You read them with `%env(VAR)%` and can pipe them through **processors** to cast
and transform.

| Kind | Syntax | Resolved |
|---|---|---|
| Parameter | `%app.name%` | Compile time (frozen) |
| Env var | `%env(APP_SECRET)%` | Runtime |
| Processed env | `%env(int:MAX)%` | Runtime |

!!! question "Predict first"
    You change `%env(DATABASE_URL)%` in production. Must you rebuild the compiled
    container for the new value to take effect? What about changing a `%parameter%`?

??? note "Reveal"
    Env vars resolve at **runtime**, so no rebuild is needed. A `%parameter%` is
    frozen into the compiled container at build time — changing it *does* require a
    cache rebuild.

## Deep Dive — how it works internally

### The parameter bag

Parameters live in a `Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface`.
During build the `ContainerBuilder` uses a mutable
`ParameterBag`; on `compile()` it is **frozen** into a
`FrozenParameterBag` — after that, parameters are read-only. A leading/trailing
`%` references a parameter; a literal percent is escaped by doubling: `%%`.

```php
// ContainerBuilder starts with a mutable ParameterBag
$container = new ContainerBuilder(new ParameterBag());
$container->setParameter('app.ratio', 'ratio: 90%%'); // %% escapes a literal %

$container->compile(); // freezes the bag

$bag = $container->getParameterBag(); // ParameterBagInterface
$bag instanceof FrozenParameterBag;   // true — read-only after compile()
```

### Environment variables are lazy placeholders

`%env(FOO)%` does **not** read `$_ENV` at compile time. The compiler replaces it
with a placeholder; at runtime the container resolves it through
`Symfony\Component\DependencyInjection\EnvVarProcessor`. This is why changing an
env var needs no cache rebuild. Env values may be sourced from real environment
variables, a `.env` file (via `symfony/dotenv`), or `secrets`.

```yaml
# config/services.yaml
parameters:
    # '%env(FOO)%' stays a placeholder at compile time — $_ENV is NOT read here.
    app.foo: '%env(FOO)%'
    # At runtime EnvVarProcessor resolves FOO from the real environment,
    # from a .env file (loaded by symfony/dotenv), or from the secrets vault.
```

### Env processors

A processor casts/transforms the raw string: `int:`, `float:`, `bool:`, `string:`,
`json:`, `csv:`, `trim:`, `default:`, `resolve:`, `file:`, `base64:`, `url:`,
`query_string:`, `require:`, `not:`, `key:`, `enum:`. They chain right-to-left:
`%env(int:default:fallback_param:MAX_ITEMS)%` reads `MAX_ITEMS`, falls back to a
parameter, then casts to int. Processors implement
`EnvVarProcessorInterface`; you can add your own.

```yaml
parameters:
    app.max: '%env(int:MAX_ITEMS)%'               # int: cast
    app.rate: '%env(float:RATE)%'                 # float: cast
    app.debug: '%env(bool:APP_DEBUG)%'            # bool: cast (not: negates it)
    app.name: '%env(string:trim:APP_NAME)%'       # trim: first, then string:
    app.opts: '%env(json:OPTIONS)%'               # json: decode
    app.hosts: '%env(csv:HOSTS)%'                 # csv: split
    app.dsn: '%env(resolve:DB_DSN)%'              # resolve: %params% inside value
    app.cert: '%env(base64:file:CERT_PATH)%'      # file: read it, base64: decode
    app.db: '%env(key:path:url:DATABASE_URL)%'    # url: parse, key: pick one part
    app.qs: '%env(query_string:QS)%'              # query_string: parse
    app.cfg: '%env(require:PHP_FILE)%'            # require: the PHP file
    app.level: '%env(enum:App\Enum\Level:LEVEL)%' # enum: backed enum case
    # default: chains right-to-left — read MAX_ITEMS, else the parameter, cast:
    app.limit: '%env(int:default:fallback_param:MAX_ITEMS)%'
    # Custom processors implement EnvVarProcessorInterface.
```

```mermaid
flowchart LR
    R["raw env string"] --> P1["default: (fallback)"]
    P1 --> P2["int: (cast)"]
    P2 --> V["typed value at runtime"]
```

### Injecting values into services

Three ways, all resolved at compile time into the definition:

1. **`bind`** in `_defaults` / a service — bind a named arg like
   `$projectDir` to a value for all services.
2. **`#[Autowire]`** on a constructor parameter — `#[Autowire('%kernel.debug%')]`
   or `#[Autowire(env: 'DATABASE_URL')]` or `#[Autowire(param: 'app.name')]`.
3. **`ParameterBagInterface`** injected as a service, read at runtime with
   `->get('app.name')` — for when the value must vary or be dynamic.

```php
// bind (services.yaml): _defaults: { bind: { $projectDir: '%kernel.project_dir%' } }
public function __construct(
    string $projectDir,                              // 1. filled by bind
    #[Autowire('%kernel.debug%')] bool $debug,       // 2. parameter expression
    #[Autowire(env: 'DATABASE_URL')] string $dsn,    //    env var
    #[Autowire(param: 'app.name')] string $appName,  //    named parameter
    private ParameterBagInterface $params,           // 3. runtime bag
) {}

public function dynamic(): mixed
{
    return $this->params->get('app.name');           // runtime read
}
```

!!! note "Source reference"
    `Symfony\Component\DependencyInjection\EnvVarProcessor` implements the
    built-in processors —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/EnvVarProcessor.php).

### Null behavior

An **unset** env var with no fallback makes resolution fail, so nullability is
explicit: `%env(default::SOME_VAR)%` yields **`null`** when `SOME_VAR` is missing
(the empty middle segment names *no* fallback parameter), and
`%env(default:app.fallback:SOME_VAR)%` falls back to a parameter first. A parameter
can be declared `null` directly (`app.optional: null`). Reading a *missing*
parameter with `ParameterBagInterface::get('nope')` throws
`ParameterNotFoundException` — it never returns `null` — so use `has()` first for
optional lookups. Watch the casts: `%env(int:MISSING)%` with no default errors, and
`%env(int:default::MISSING)%` casts empty/`null` to `0`, which can hide a
misconfiguration. The common bug is assuming an absent env var silently becomes
`null` everywhere; without a `default:` processor it is a hard failure.

```php
// Env fallbacks (resolved at runtime):
'%env(default::SOME_VAR)%';             // null when SOME_VAR is unset
'%env(default:app.fallback:SOME_VAR)%'; // falls back to the app.fallback parameter
'%env(int:MISSING)%';                   // unset + no default: -> hard failure
'%env(int:default::MISSING)%';          // unset -> null -> cast to 0 (careful!)

// Parameter bag at runtime (app.optional: null declared in YAML):
$params->get('app.optional');           // null — parameter declared as null
$params->has('nope');                   // false — check first for optional lookups
$params->get('nope');                   // throws ParameterNotFoundException
```

!!! note "Null in real life"
    A recipe step reading "salt to taste" with the jar missing (unset env): either
    the dish stalls (error) or you note "skip if none" (`default::`) and plate it
    unseasoned (null).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Service;

    use Symfony\Component\DependencyInjection\Attribute\Autowire;
    use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;

    final class Mailer
    {
        public function __construct(
            #[Autowire(param: 'app.sender')]     // container parameter
            private readonly string $sender,
            #[Autowire(env: 'MAILER_DSN')]        // raw env var
            private readonly string $dsn,
            #[Autowire('%env(int:MAILER_RETRIES)%')] // processed env
            private readonly int $retries,
            private readonly ParameterBagInterface $params,
        ) {}

        public function debug(): bool
        {
            return (bool) $this->params->get('kernel.debug');
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/services.yaml
    parameters:
        app.sender: 'no-reply@example.com'
        app.max_items: '%env(int:MAX_ITEMS)%'

    services:
        _defaults:
            autowire: true
            bind:
                $projectDir: '%kernel.project_dir%'
                string $sender: '%app.sender%'
    ```

=== "Console"

    ```console
    $ php bin/console debug:container --parameters
    $ php bin/console debug:container --parameter=kernel.debug
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `#[Autowire(env: 'X')]` for secrets/DSNs | Baking secrets into parameters |
| Cast env with processors (`int:`, `bool:`) | Treating env as already-typed |
| `bind` for shared named args | Repeating the same arg per service |
| Inject `ParameterBagInterface` when dynamic | Injecting whole bag "just in case" |

## When (not) to use it / alternatives

Use **parameters** for static app config that can be frozen. Use **env vars** for
anything that changes per environment or must stay secret. Prefer injecting the
*single value* via `#[Autowire]` over injecting the whole `ParameterBagInterface`
— narrower dependency, easier to test.

!!! danger "Certification traps"
    - `%env(FOO)%` is resolved **at runtime**, so it is *not* frozen into the cache;
      parameters *are* frozen at compile time.
    - Env **processors** chain right-to-left: `%env(int:default:p:VAR)%`.
    - Escape a literal `%` by doubling it: `%%`.
    - You cannot inject a scalar by type; use `bind`, `#[Autowire]` or a parameter.

!!! warning "Common mistakes"
    - Expecting `%env(MAX)%` to be an int — it is a **string** until you add `int:`.
    - Changing a parameter and forgetting it needs a cache rebuild (env vars do not).
    - Using `getParameter()` in a controller for values better injected.

## Exercises

1. **(Advanced)** Write the `%env(...)%` expression that reads `TIMEOUT`, defaults
   to the `app.timeout` parameter, and casts to `int`.
2. **(Expert)** Inject the boolean `kernel.debug` into a service two different
   ways.

??? success "Solutions"

    **1.** `%env(int:default:app.timeout:TIMEOUT)%` — reads `TIMEOUT`, falls back to
    the `app.timeout` parameter if unset, then casts to `int`.

    **2.** (a) `#[Autowire('%kernel.debug%')] private bool $debug`; (b) inject
    `ParameterBagInterface $params` and call `$params->get('kernel.debug')`. The
    first is preferred (narrower dependency).

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. When is `%env(DATABASE_URL)%` resolved?"
    - [ ] A. At container compilation, frozen into the cache
    - [x] B. At runtime, via an env-var processor ✅
    - [ ] C. When `.env` is parsed at deploy
    - [ ] D. Never; it is a literal string

    **Why:** Env placeholders resolve at runtime so one compiled container works
    across environments. **Ref:** [Env vars](https://symfony.com/doc/8.0/configuration.html#configuration-based-on-environment-variables).

??? question "Q2. What does `%env(int:MAX)%` return?"
    - [ ] A. The string value of `MAX`
    - [x] B. `MAX` cast to an integer ✅
    - [ ] C. `null` if `MAX` is unset
    - [ ] D. A parameter named `int`

    **Why:** The `int:` processor casts the raw env string to an integer.
    **Ref:** [Env var processors](https://symfony.com/doc/8.0/configuration/env_var_processors.html).

??? question "Q3. Which injects the `app.name` parameter into a constructor arg?"
    - [x] A. `#[Autowire(param: 'app.name')]` ✅
    - [ ] B. `#[Autowire('app.name')]`
    - [ ] C. `#[Parameter('app.name')]`
    - [ ] D. Type-hinting `string`

    **Why:** `param:` names a container parameter; a bare string without `%%` is a
    literal. **Ref:** [Autowire attribute](https://symfony.com/doc/8.0/service_container/autowiring.html).

??? question "Q4. How do you write a literal percent sign in a parameter value?"
    - [ ] A. `\%`
    - [x] B. `%%` ✅
    - [ ] C. `%25`
    - [ ] D. You cannot

    **Why:** A doubled percent escapes to a single literal `%`.
    **Ref:** [Parameters](https://symfony.com/doc/8.0/configuration.html#configuration-parameters).

## Key takeaways

- Parameters (`%x%`) are frozen at compile time; env vars resolve at runtime.
- Env **processors** cast/transform and chain right-to-left.
- Inject values via `bind`, `#[Autowire(param:/env:)]`, or `ParameterBagInterface`.
- Prefer injecting the single value over the whole parameter bag.

## Last-minute revision

!!! tip "Cheat sheet"
    - `%param%` frozen · `%env(VAR)%` runtime · `%%` literal percent.
    - Processors: `int bool float json csv default resolve file base64 enum`.
    - `#[Autowire(param: 'x')]`, `#[Autowire(env: 'X')]`, `#[Autowire('%env(int:X)%')]`.
    - `FrozenParameterBag` = read-only after `compile()`.

## Connections

- **Depends on:** [The Service Container](container.md) — parameters live in the
  (frozen) parameter bag.
- **Reused in:** [Autowiring](autowiring.md),
  [Miscellaneous — Configuration](../miscellaneous/configuration.md) — values are
  injected via `#[Autowire]` / `bind`.
- **Confused with:** [Semantic Configuration](semantic-config.md) — bundle config is
  validated then *turned into* parameters.

## Official References
- [Official Symfony docs — Configuration & Parameters](https://symfony.com/doc/8.0/configuration.html)
- [Official Symfony docs — Env Var Processors](https://symfony.com/doc/8.0/configuration/env_var_processors.html)
- [Symfony source — EnvVarProcessor](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/EnvVarProcessor.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "dependency injection" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/configuration.html#configuration-based-on-environment-variables) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** env vars resolve at runtime but parameters are frozen
- [ ] read and cast env vars with processors (`%env(int:default:p:VAR)%`)
- [ ] debug an unset env var that errors instead of becoming `null`
- [ ] spot that `%env(MAX)%` is a string until `int:` and `%%` escapes a percent
- [ ] explain the `FrozenParameterBag` and where `%env()%` is resolved

---

<small>Related: [The Service Container](container.md) · [Autowiring](autowiring.md) ·
[Registration](registration.md)</small>
