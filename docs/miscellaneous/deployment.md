# Deployment Best Practices

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] List the mandatory prod steps: `--no-dev`, cache warmup, dotenv dump.
    - [ ] Explain `APP_ENV`/`APP_DEBUG` and opcache/preload's role in prod.
    - [ ] Apply a repeatable deployment checklist.

    **Syllabus:** `Miscellaneous → Deployment` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Configuration](configuration.md), [Runtime](runtime.md)

---

## Theory

Deploying Symfony means shipping code into an environment tuned for **speed and
safety**: production dependencies only, a warmed cache, real environment
variables, `APP_DEBUG=0`, and PHP's opcache/preload enabled. The goal is that no
per-request work parses YAML, scans files, or exposes internals.

## Deep Dive — how it works internally

### Environment & debug

`APP_ENV=prod` selects prod config; `APP_DEBUG=0` disables the profiler, the
debug ErrorHandler's verbose page, and cache freshness checks. In prod the
compiled container in `var/cache/prod/` is loaded as-is — Symfony assumes it is
fresh, so you **must** warm/clear the cache on deploy.

### Cache warmup

`cache:clear` removes stale cache and (by default) runs the **cache warmers**
(`CacheWarmerInterface`) that pre-build the container, routing matcher/generator,
Twig template cache, validator/serializer metadata. `cache:warmup` warms without
clearing. Warm during build so the first real request is fast and the web user
has no write access to `var/cache`.

### Dependencies & autoloader

`composer install --no-dev --optimize-autoloader` (or
`--classmap-authoritative`) skips dev packages and builds an optimised classmap,
avoiding filesystem stat calls per class load.

### DotEnv dump

`composer dump-env prod` compiles the `.env*` cascade into `.env.local.php`, so
production skips DotEnv parsing (see [Configuration](configuration.md)).

### Opcache & preload

Opcache caches compiled bytecode. Symfony generates
`var/cache/prod/App_KernelProdContainer.preload.php`; setting
`opcache.preload` to it loads core classes into shared memory once per PHP
process manager start, cutting per-request class loading. Ensure
`opcache.validate_timestamps=0` in prod and reset opcache on each deploy.

```mermaid
flowchart LR
    G[git pull / artifact] --> C[composer install --no-dev]
    C --> DE[dump-env prod]
    DE --> W[cache:clear + warmup]
    W --> OP[opcache reset / preload]
    OP --> L[go live]
```

!!! note "Source reference"
    `Symfony\Component\HttpKernel\CacheWarmer\CacheWarmerInterface` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/CacheWarmer/CacheWarmerInterface.php).

## Configuration & code

=== "Console"

    ```console
    $ APP_ENV=prod APP_DEBUG=0 composer install --no-dev --optimize-autoloader
    $ composer dump-env prod
    $ php bin/console cache:clear --env=prod
    $ php bin/console cache:warmup --env=prod
    $ php bin/console asset-map:compile   # if using AssetMapper (out of scope here)
    ```

=== "YAML"

    ```yaml
    # config/packages/prod/framework.yaml (example)
    when@prod:
        framework:
            router:
                strict_requirements: null
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `composer install --no-dev --optimize-autoloader` | Shipping dev deps (profiler, phpunit) to prod |
| Warm cache during build; make `var/` non-writable by web user | Warming on the first live request |
| `APP_DEBUG=0` and `dump-env prod` | Leaving `APP_DEBUG=1` (leaks + slow) |
| Enable opcache + preload, reset on deploy | `validate_timestamps=1` in prod |

## When (not) to use it / alternatives

These steps apply to any prod deploy (VM, container, PaaS). In immutable
container images, bake `composer install`, `dump-env` and `cache:warmup` into the
image build so the running container does zero setup.

!!! danger "Certification traps"
    - Prod does **not** auto-detect config changes — you must clear/warm cache.
    - `dump-env prod` → `.env.local.php`; when present `.env*` is not parsed.
    - `APP_DEBUG=1` in prod enables the profiler and exposes traces — never do it.
    - `--optimize-autoloader` / `--classmap-authoritative` speed class loading.

!!! warning "Common mistakes"
    - Forgetting to reset opcache after deploy → stale bytecode served.
    - Running `cache:warmup` as a different user than the web server, causing
      permission errors on `var/cache`.

## Exercises

1. **(Advanced)** Write the ordered command list for a from-scratch prod deploy.
2. **(Advanced)** Explain why prod must warm the cache but dev need not.

??? success "Solutions"

    **1.** `composer install --no-dev --optimize-autoloader` → `composer dump-env prod`
    → `cache:clear --env=prod` → `cache:warmup --env=prod` → reset opcache.

    **2.** In dev, `ConfigCache` checks resource freshness and rebuilds on change;
    prod skips those checks for speed and loads the compiled container as-is, so it
    must be (re)built explicitly on deploy.

## Certification questions

??? question "Q1. Which flag excludes dev dependencies during deploy?"
    - [x] A. `--no-dev` ✅
    - [ ] B. `--prod`
    - [ ] C. `--production`

    **Why:** `composer install --no-dev` skips `require-dev` packages.
    **Ref:** [Deploying Symfony](https://symfony.com/doc/current/deployment.html).

??? question "Q2. What does `composer dump-env prod` create?"
    - [x] A. `.env.local.php` ✅
    - [ ] B. `.env.prod`
    - [ ] C. `config/prod.php`

    **Why:** It compiles the cascade into `.env.local.php` for fast loading.
    **Ref:** [Configuring env vars in production](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production).

??? question "Q3. Why set `opcache.validate_timestamps=0` in prod?"
    - [x] A. To skip file-modification checks and serve cached bytecode ✅
    - [ ] B. To enable debug mode
    - [ ] C. To disable opcache

    **Why:** With immutable deploys, skipping timestamp checks maximises opcache
    hits (reset opcache on deploy instead). **Ref:** [Performance](https://symfony.com/doc/current/performance.html).

## Key takeaways

- `--no-dev --optimize-autoloader`, `dump-env prod`, `cache:warmup`, `APP_DEBUG=0`.
- Prod loads the compiled container as-is — clear/warm cache on every deploy.
- Opcache + preload + `validate_timestamps=0` cut per-request overhead.

## Last-minute revision

!!! tip "Cheat sheet"
    - Deploy order: install --no-dev → dump-env prod → cache:clear → cache:warmup → opcache reset.
    - `APP_ENV=prod APP_DEBUG=0`.
    - Preload file: `var/cache/prod/*.preload.php`.
    - Make `var/cache` warmed at build, web user read-only.

## References

- [Official docs — Deploying Symfony](https://symfony.com/doc/current/deployment.html)
- [Official docs — Performance](https://symfony.com/doc/current/performance.html)
- [Symfony source — CacheWarmerInterface](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/CacheWarmer/CacheWarmerInterface.php)

---

<small>Related: [Configuration](configuration.md) · [Runtime](runtime.md) · [Cache](cache.md)</small>
