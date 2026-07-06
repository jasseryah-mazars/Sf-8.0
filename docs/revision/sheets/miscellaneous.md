# Revision Sheet — Miscellaneous

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Miscellaneous](../../miscellaneous/index.md).

## Cache Component
- Three APIs: PSR-6 (items), PSR-16 (simple), Symfony contracts (callback `get()`).
- Contracts `get($key, $cb, $beta)` = compute-on-miss + stampede protection.
- Adapters: filesystem, apcu, redis, array, chain, null, phpfiles.
- Tags via `TagAwareAdapter` → `invalidateTags()`.

**Cheat:** `CacheItemPoolInterface` (PSR-6) · `SimpleCache` (PSR-16) · `CacheInterface` (contracts). `get($key, fn(ItemInterface $i) => ..., $beta)`; `$i->expiresAfter()`, `$i->tag()`. Stampede = early expiration; `$beta=INF` forces recompute. `cache:pool:clear`, `pools:` with `tags: true`.

## Clock Component
- Inject `ClockInterface`/use `now()` instead of `new \DateTime()`.
- `NativeClock` (prod), `MockClock` (tests), `MonotonicClock` (durations).
- `now()` returns an immutable `DatePoint`; the `Clock` facade holds the global clock.
- `ClockSensitiveTrait`/`ClockAwareTrait` ease testing and adoption.

**Cheat:** `ClockInterface::now(): \DateTimeImmutable`; also `sleep()`, `withTimeZone()`. `new MockClock('2026-07-06 12:00')` → set/advance; `$c->sleep(3600)`. `Clock::set(new MockClock(...))`; `now()` reads the facade. `DatePoint` extends `\DateTimeImmutable`.

## Configuration (Config, DotEnv, ExpressionLanguage)
- Config = schema (`TreeBuilder`) + validation/merge (`Processor`).
- DotEnv cascade: `.env` → `.env.local` → `.env.<env>` → `.env.<env>.local`; `test` skips `.env.local`.
- `dump-env prod` → `.env.local.php`, no runtime `.env` parsing.
- ExpressionLanguage: `evaluate()` interprets, `compile()` emits PHP; extend via providers.

**Cheat:** Node types: `scalarNode`, `integerNode`, `booleanNode`, `enumNode`, `arrayNode`; `->isRequired()`, `->defaultValue()`. Env precedence: real env > `.env.<env>.local` > `.env.<env>` > `.env.local` > `.env`. `debug:dotenv`, `debug:config <bundle>`, `composer dump-env prod`. Providers implement `ExpressionFunctionProviderInterface`.

## Code Debugging (VarDumper, Debug, Stopwatch)
- VarDumper: `VarCloner` → `Data` → `CliDumper`/`HtmlDumper`; casters customise types.
- `dump()` continues; `dd()` exits. Dumps are collected into the profiler.
- Stopwatch measures named events/periods (ms + memory); `debug.stopwatch` in debug only.

**Cheat:** Clone (`VarCloner`) vs dump (`Cli`/`Html` `Dumper`); `Data` is the snapshot. `dump()` / `dd()`; `server:dump` to a TCP server. `Stopwatch::start()/stop()` → `StopwatchEvent::getDuration()` (ms).

## Deployment Best Practices
- `--no-dev --optimize-autoloader`, `dump-env prod`, `cache:warmup`, `APP_DEBUG=0`.
- Prod loads the compiled container as-is — clear/warm cache on every deploy.
- Opcache + preload + `validate_timestamps=0` cut per-request overhead.

**Cheat:** Deploy order: install --no-dev → dump-env prod → cache:clear → cache:warmup → opcache reset. `APP_ENV=prod APP_DEBUG=0`. Preload file: `var/cache/prod/*.preload.php`. Make `var/cache` warmed at build, web user read-only.

## Error Handling
- ErrorHandler converts PHP errors to exceptions and renders uncaught throwables.
- `FlattenException` + `ErrorRendererInterface` produce HTML/JSON/XML output.
- `error_controller` maps throwables to responses; non-HTTP exceptions → 500.
- Prod hides internals; dev shows the trace — driven by `APP_DEBUG`.

**Cheat:** `ErrorHandler` = `set_error_handler` + `set_exception_handler` + shutdown fn. Renderers: `HtmlErrorRenderer`, `SerializerErrorRenderer`. Status: `HttpExceptionInterface::getStatusCode()` else 500. Prod templates: `templates/bundles/TwigBundle/Exception/error{404,500}.html.twig`.

## Filesystem & Finder Components
- Filesystem: exception-throwing, cross-platform file ops; `dumpFile()` is atomic.
- `Path` helpers normalise/join paths without disk access.
- Finder: fluent `in()`+filters, yields `SplFileInfo`; needs directories.

**Cheat:** FS: `exists`, `mkdir`, `copy`, `remove`, `dumpFile`, `appendToFile`, `rename`. `Path::canonicalize/join/makeAbsolute/makeRelative`. Finder: `files()->in()->name()->size('> 1K')->date('since yesterday')->sortByModifiedTime()`. `count()`, `hasResults()`, `getRelativePathname()`.

## Internationalization (Translation & Intl)
- `trans($id, $params, $domain, $locale)`; default domain `messages`.
- ICU MessageFormat handles plural/select; categories are locale-specific.
- Fallback locales fill gaps; missing keys return the id.
- Intl (`Countries`/`Languages`/`Locales`/`Currencies`) exposes ICU data.

**Cheat:** `TranslatorInterface::trans()` from `Symfony\Contracts\Translation`. Files: `translations/<domain>[+intl-icu].<locale>.{yaml,xlf,php}`. ICU: `{count, plural, one {…} other {# …}}`, `{v, select, …}`. Intl: `Countries`, `Languages`, `Locales`, `Currencies`, `Timezones`.

## Lock Component
- `LockFactory::createLock($resource, $ttl)` → `acquire()`/`release()`/`refresh()`.
- Non-blocking by default; `acquire(true)` blocks.
- Store scope matters: local (Flock/Semaphore) vs shared (Redis/DB).
- TTL + `refresh()` prevent both deadlocks and premature expiry.

**Cheat:** `createLock(name, ttl=300, autoRelease=true)`. `acquire(bool $blocking=false)`, `release()`, `refresh()`, `isAcquired()`. Shared: `SharedLockInterface::acquireRead()`. DSN: `flock`, `semaphore`, `redis://…`, `%env(LOCK_DSN)%`.

## Mime & Mailer Components
- Mime models a message as a tree of parts; `Email` is the builder.
- Mailer sends via a transport DSN (`MAILER_DSN`); `Envelope` ≠ headers.
- `TemplatedEmail` (Twig bridge) renders html/text templates.
- Route `SendEmailMessage` to Messenger for async delivery + retries.

**Cheat:** `(new Email())->from()->to()->subject()->text()->html()`. `attachFromPath()`, `embedFromPath()` (`cid:`), `addPart(new DataPart(...))`. `MailerInterface::send($email)`; DSN via `MAILER_DSN`. Async: route `SendEmailMessage` → transport; run `messenger:consume`.

## Messenger Component
- Message (DTO) → bus → middleware stack → handler; everything wrapped in an `Envelope` + stamps.
- `SendMessageMiddleware` (routes/sends) and `HandleMessageMiddleware` (calls handlers) are the pivots.
- Transports are DSN-configured: `sync`, `doctrine`, `amqp`, `redis`, `in-memory`.
- Worker loops receive→dispatch→ack/reject and fires `WorkerMessage*` events.
- Retries use `RedeliveryStamp` + a `RetryStrategy`; exhausted → failure transport.

**Cheat:** `#[AsMessageHandler]` on an `__invoke(MessageType $m)` service. `dispatch($msg, [$stamps]): Envelope` — result via `->last(HandledStamp::class)->getResult()`. `DelayStamp` = **milliseconds**. Routed async ⇒ handler skipped in-process. Consume: `messenger:consume <transport> --limit --time-limit --memory-limit`. Failure: `messenger:failed:show|retry|remove`; `UnrecoverableMessageHandlingException` = no retry. Events: `WorkerStarted/MessageReceived/MessageHandled/MessageFailed/Running/Stopped`.

## Process Component
- Prefer the array constructor (auto-escaped) over `fromShellCommandline`.
- `run()` blocks; `start()`+`wait()` is async; `mustRun()` throws on failure.
- Read via `getOutput()`, `getIncrementalOutput()`, or stream with `getIterator()`.
- Default 60 s timeout; `ProcessTimedOutException` / `ProcessFailedException`.

**Cheat:** `new Process([...])` vs `Process::fromShellCommandline('...')` (unsafe with input). `run(): int`, `start()`/`wait()`, `mustRun()`. `getOutput()`, `getErrorOutput()`, `getExitCode()`, `isSuccessful()`, `getIterator()`. `setTimeout(120)` / `setIdleTimeout()` / default 60 s.

## Web Profiler & Data Collectors
- Collectors implement `DataCollectorInterface`; data stored in `$this->data`.
- Collection on `kernel.response`; `LateDataCollectorInterface` at terminate.
- Register with the `data_collector` tag + a Twig panel template.
- Dev-only; disable in prod for performance and safety.

**Cheat:** `collect(Request, Response, ?Throwable)`, `getName()`, `reset()`. Extend `DataCollector`; store serializable `$this->data`. Tag `data_collector` + `template:`; profiler UI at `/_profiler`. `LateDataCollectorInterface::lateCollect()` for post-response data.

## Runtime Component
- Entry points return a callable; `autoload_runtime.php` runs it.
- `RuntimeInterface`: `getResolver()` (autowire args) + `getRunner()` (execute).
- `SymfonyRuntime` (default) extends `GenericRuntime`; select via `APP_RUNTIME`.
- The runtime creates the `Request`, sends the `Response`, calls `terminate()`.

**Cheat:** `require vendor/autoload_runtime.php; return fn(array $context) => new Kernel(...)`. `RuntimeInterface::getResolver()` + `getRunner()`; `RunnerInterface::run(): int`. `APP_RUNTIME` env / `extra.runtime.class`. Default `SymfonyRuntime`.

## Serializer Component
- Two stages: normalizers (object↔array) + encoders (array↔string).
- `serialize` = normalize→encode; `deserialize` = decode→denormalize.
- `#[Groups]`, `#[SerializedName]`, `#[Ignore]`, context tune the output.
- `ObjectNormalizer` (accessors) vs `PropertyNormalizer` (properties).
- Circular refs: limit is 1 → use a handler or `#[MaxDepth]`.

**Cheat:** `serialize($data, 'json', $context)` / `deserialize($str, Type::class, 'json')`. Context keys: `groups`, `skip_null_values`, `datetime_format`, `enable_max_depth`. Attributes namespace: `Symfony\Component\Serializer\Attribute`. Encoders: `JsonEncoder`, `XmlEncoder`, `CsvEncoder`, `YamlEncoder`.
