# Flashcards — Miscellaneous

79 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. Symfony\Contracts\Cache\CacheInterface::get() runs its callback…"
    **✅ only on a cache miss, then stores and returns the value**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection. Running on every call would defeat caching, and unlike PSR-6 you do not call save() manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

??? question "2. Which statement about PSR-6 vs PSR-16 is correct?"
    **✅ PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

??? question "3. Cache stampede protection in Symfony Cache is implemented by…"
    **✅ probabilistic early expiration controlled by the $beta factor**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

??? question "4. Which adapter keeps entries only for the current process (ideal for tests)?"
    **✅ ArrayAdapter**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

??? question "5. Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?"
    **✅ null is returned as a cache hit; the callback is NOT run again**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

??? question "6. A pool is declared with `tags: true` in cache.yaml. What does this enable?"
    **✅ Tagging items with $item->tag([...]) and evicting groups via invalidateTags([...])**

    `tags: true` wraps the pool in a TagAwareAdapter implementing TagAwareCacheInterface, so items can carry tags and invalidateTags() evicts all items with a given tag — invalidation by concern rather than by key. Calling $item->tag() on a non-tag-aware pool errors.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#using-cache-tags)

??? question "7. True or False: passing $beta = INF to CacheInterface::get() forces the value to be recomputed immediately."
    **✅ True**

    True. $beta = INF forces early expiration, so the callback runs and the value is refreshed on this call. $beta = 0 disables early expiration entirely; the default (null) picks a sensible probabilistic value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

??? question "8. Using the raw PSR-6 API, how do you distinguish a stored null value from a missing key?"
    **✅ Check $item->isHit() — get() returns null for both cases**

    With PSR-6, CacheItemInterface::get() returns null both for an absent key and for a genuinely stored null, so you must call isHit() to tell them apart. The contracts callback API sidesteps this ambiguity; there is no hasKey() or miss exception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

??? question "9. In serialize(), which stage runs first?"
    **✅ The normalizer (object to array), then the encoder (array to string)**

    serialize() normalizes the object to an array/scalars, then encodes that to a string. deserialize() reverses it: decode then denormalize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/serializer.html)

??? question "10. #[Groups(['read'])] on a property takes effect when…"
    **✅ the context includes ['groups' => ['read']]**

    Group filtering only applies when matching groups are passed in the context; otherwise the group attribute has no effect and all fields are (de)serialized.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

??? question "11. Which normalizer reads and writes private properties directly via reflection?"
    **✅ PropertyNormalizer**

    PropertyNormalizer accesses object properties directly (including private), whereas ObjectNormalizer uses accessors and the constructor, and GetSetMethodNormalizer uses only get/set methods. JsonEncoder is an encoder, not a normalizer.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

??? question "12. By default, what is the Serializer's circular reference limit before it throws?"
    **✅ 1 (unless a circular reference handler or #[MaxDepth] is set)**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

??? question "13. A UserDto has #[Groups(['read'])] #[SerializedName('full_name')] on $name and #[Ignore] on $passwordHash. What is the JSON when serialized with context ['groups' => ['read']]?"
    **✅ {"full_name":"..."} plus any other read-group fields; passwordHash is omitted**

    With the read group in context, only read-group properties are emitted; $name is renamed to full_name by #[SerializedName], and #[Ignore] drops passwordHash entirely regardless of group. Groups are honoured only because they are passed in the context.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

??? question "14. What does the framework.serializer.default_context option skip_null_values: true do?"
    **✅ Omits properties whose value is null from the serialized output**

    By default a null property is serialized as \"key\":null. Setting AbstractObjectNormalizer::SKIP_NULL_VALUES (skip_null_values) omits those keys from the payload. The classic bug is a consumer treating an absent key as an error rather than 'the value was null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html)

??? question "15. A private property with no getter is missing from the JSON produced by the default ObjectNormalizer. Why, and how do you fix it?"
    **✅ ObjectNormalizer uses accessors; add a getter (or use PropertyNormalizer, which reads properties directly)**

    ObjectNormalizer reads via getters/issers/hassers and the constructor, so a private property without an accessor is invisible. Provide a getter or switch to PropertyNormalizer, which uses reflection to read properties directly. Groups filter fields but do not expose accessorless private properties.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

??? question "16. In which environment is .env.local NOT loaded?"
    **✅ test**

    .env.local is intentionally skipped in the test environment so tests run from committed defaults and stay reproducible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#selecting-the-active-environment)

??? question "17. What does `composer dump-env prod` produce, and what is the effect?"
    **✅ .env.local.php — Symfony loads it directly and skips parsing .env* files**

    The whole .env* cascade is compiled to a plain PHP array in .env.local.php, which Symfony loads directly, avoiding DotEnv parsing on each request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production)

??? question "18. ExpressionLanguage::compile() returns what?"
    **✅ A string of PHP source code**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

??? question "19. A .env file sets DATABASE_URL, but a real OS environment variable DATABASE_URL is also exported. Which wins?"
    **✅ The real OS environment variable — DotEnv never overrides an existing real env var**

    Real OS environment variables always take precedence; the DotEnv cascade (.env → .env.local → .env.<env> → .env.<env>.local) only fills values not already set in the real environment. Later .env* files override earlier ones but never a real env var.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#overriding-environment-values-via-env-local)

??? question "20. What is the result of ExpressionLanguage::compile('1 + a', ['a'])?"
    **✅ The PHP source string "(1 + $a)"**

    compile() emits PHP source, turning the variable name a into $a: "(1 + $a)". It does not evaluate anything (so no undefined-variable error) — use evaluate('1 + a', ['a' => 5]) to get the value 6.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

??? question "21. Which class merges every config source and validates it against a bundle's Configuration tree?"
    **✅ Processor (Processor::processConfiguration())**

    Processor::processConfiguration() merges all sources and validates them against the tree returned by the Configuration class, applying defaults and constraints. TreeBuilder only defines the schema; FileLocator finds files.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/config/definition.html)

??? question "22. Which composer flag excludes require-dev packages when deploying to production?"
    **✅ --no-dev**

    `composer install --no-dev` skips require-dev packages (profiler, PHPUnit, etc.). Add --optimize-autoloader (or --classmap-authoritative) to build an optimised classmap and cut per-class filesystem stat calls.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "23. You changed a YAML config file and redeployed to prod, but the change has no effect. Why?"
    **✅ Prod loads the compiled container as-is and does not auto-detect config changes; you must clear/warm the cache on deploy**

    In prod the compiled container in var/cache/prod is loaded as-is with no freshness checks (those exist only in debug), so config changes require cache:clear + cache:warmup on deploy. Enabling APP_DEBUG in prod is unsafe and not the fix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "24. Why set opcache.validate_timestamps=0 in production?"
    **✅ To skip per-request file-modification checks and always serve cached bytecode (reset opcache on deploy instead)**

    With immutable deploys, disabling timestamp validation maximises opcache hits by not stat-ing files each request. Because opcache then never notices new files, you must reset opcache (or the PHP process manager) on each deploy so the new bytecode is loaded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/performance.html)

??? question "25. Which ordered command sequence is correct for a from-scratch prod deploy?"
    **✅ composer install --no-dev --optimize-autoloader → composer dump-env prod → cache:clear → cache:warmup → reset opcache**

    You install prod deps first, compile the env cascade with dump-env prod, then clear and warm the cache so the first live request is fast, and finally reset opcache. Warming before installing, or shipping dev deps / APP_DEBUG=1, are wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "26. What does `cache:clear` run, by default, in addition to removing stale cache?"
    **✅ The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "27. True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled."
    **✅ False**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "28. Which Process constructor auto-escapes each argument?"
    **✅ new Process(['git', 'log', '--oneline'])**

    The array form escapes each element automatically. fromShellCommandline() runs a raw shell string and does not escape, risking command injection if you interpolate untrusted input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

??? question "29. What does Process::run() return?"
    **✅ The integer exit code**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

??? question "30. What is the default Process timeout?"
    **✅ 60 seconds**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#process-timeout)

??? question "31. You build a command from user input using Process::fromShellCommandline('convert '.$userInput). What is the risk and the fix?"
    **✅ Command injection — use the array constructor new Process(['convert', $userInput]) so each argument is auto-escaped**

    fromShellCommandline runs the string through /bin/sh with no escaping, so untrusted input can inject shell metacharacters. The array constructor escapes each element as a single argument, eliminating the injection vector. This is unrelated to timeouts or platform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

??? question "32. Which call runs a process and throws automatically on a non-zero exit code?"
    **✅ mustRun() — it throws ProcessFailedException on failure**

    mustRun() behaves like run() but throws ProcessFailedException when the process exits non-zero. run() simply returns the integer exit code and you check isSuccessful() yourself; start()/wait() are for async execution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

??? question "33. LockInterface::acquire() called with no argument is…"
    **✅ non-blocking — it returns false immediately if the lock is held**

    acquire() defaults to non-blocking; pass true to block until the resource becomes available (store permitting). It returns a boolean false when held, it does not throw, so `if (!$lock->acquire()) { return; }` is the correct guard.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html#blocking-locks)

??? question "34. Which lock store provides mutual exclusion across multiple servers?"
    **✅ RedisStore**

    Flock and Semaphore stores are local to one machine, and InMemoryStore is per-process (tests). Shared stores like Redis (or a database store) coordinate locks across servers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#available-stores)

??? question "35. Why call refresh() during a long critical section?"
    **✅ To extend the lock's TTL so it is not considered expired mid-job**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity; without it another process could acquire the lock after the TTL, breaking mutual exclusion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

??? question "36. Which is the correct guard to skip work another process is already doing?"
    **✅ if (!$lock->acquire()) { return; }**

    Non-blocking acquire() returns false when the resource is held, so !$lock->acquire() is the idiomatic early-return guard. It does not return null and does not throw on contention (only blocking acquire(true) may throw LockConflictedException). Forgetting to check the boolean means entering the critical section unprotected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html)

??? question "37. What is the default TTL of a lock created via LockFactory::createLock($resource)?"
    **✅ 300 seconds (5 minutes), with autoRelease on by default**

    createLock(string $resource, ?float $ttl = 300.0, bool $autoRelease = true) defaults to a 300 second TTL and releases the lock when the Lock object is destroyed. Long jobs should raise the TTL and call refresh() to avoid premature expiry.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

??? question "38. With Messenger routing configured for emails, MailerInterface::send() will…"
    **✅ dispatch a SendEmailMessage to be delivered by a worker**

    When SendEmailMessage is routed to a transport, send() enqueues it; a worker delivers it later, giving async sending plus retries. It does not throw if a worker is down — the message just waits in the queue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

??? question "39. Which class renders Twig templates into an email body?"
    **✅ Symfony\Bridge\Twig\Mime\TemplatedEmail**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending. Plain Email has no template support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

??? question "40. How is an inline (embedded) image referenced from an email's HTML body?"
    **✅ Via a cid: reference produced by embed()/embedFromPath()**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

??? question "41. In the Mailer, how does the Envelope differ from the message headers?"
    **✅ The Envelope holds the actual sender/recipients used for the SMTP conversation; headers (From/To) render in the visible message**

    Mailer's Envelope (sender + recipients) drives the transport's SMTP exchange, whereas the message headers (From, To, Subject) are what the recipient sees. They can legitimately differ (e.g. bounce address vs visible From), which is a common exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages)

??? question "42. Which configuration makes emails send asynchronously via Messenger?"
    **✅ Route Symfony\Component\Mailer\Messenger\SendEmailMessage to a transport in messenger routing (and run a worker)**

    Async delivery comes from routing SendEmailMessage to a Messenger transport and consuming it with a worker. MAILER_DSN chooses the delivery transport (SMTP/API), not sync-vs-async, and there is no framework.mailer.async flag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

??? question "43. What does public/index.php return under the Runtime component?"
    **✅ A callable that produces the application object (e.g. a Kernel)**

    index.php returns a callable; autoload_runtime.php resolves its arguments, invokes it, then a RunnerInterface handles/sends/terminates. It never calls handle() itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "44. Which environment variable selects the runtime class?"
    **✅ APP_RUNTIME**

    APP_RUNTIME (or composer.json extra.runtime.class) chooses the RuntimeInterface implementation; the default is SymfonyRuntime, which extends GenericRuntime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

??? question "45. Which class does the default SymfonyRuntime extend?"
    **✅ GenericRuntime**

    SymfonyRuntime extends the framework-agnostic GenericRuntime, adding Symfony-aware resolvers/runners (inject Request, SymfonyStyle, console Input/Output; run a Kernel or console Application). It is not a kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "46. How does the argument `array $context` in the index.php closure get populated?"
    **✅ The runtime's resolver autowires it from $_SERVER (env vars like APP_ENV/APP_DEBUG)**

    RuntimeInterface::getResolver() builds a resolver that inspects the callable's typed arguments and supplies them — array $context comes from $_SERVER (env), and it can also inject Request, InputInterface, etc. You therefore never read $_SERVER manually in the entry point.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

??? question "47. A teammate 'fixes' a bug by adding $kernel->handle($request)->send(); at the end of public/index.php, right after the file already returns its closure. What is wrong with this?"
    **✅ public/index.php must only return a callable; the Runtime component itself builds the kernel, handles the request and sends the response**

    The whole point of symfony/runtime is that the front controller only returns a callable (or an application object); the runtime resolves its arguments, invokes it, and — for the Symfony flavor — runs the kernel and sends the response itself. Hand-calling handle()/send() after autoload_runtime.php has already done so double-processes the request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "48. ClockInterface::now() returns what type?"
    **✅ A \DateTimeImmutable (a DatePoint)**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "49. Which clock lets tests freeze or advance time without a real delay?"
    **✅ MockClock — you set the time and its sleep() advances virtual time**

    MockClock is constructed with a fixed time and its sleep() advances time virtually (no real waiting), perfect for TTL/expiry tests. NativeClock is the real prod clock; MonotonicClock is for durations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html#usage-in-tests)

??? question "50. Which clock is best for measuring elapsed durations and is immune to system clock changes?"
    **✅ MonotonicClock**

    MonotonicClock uses a high-resolution monotonic source unaffected by NTP or manual clock adjustments, so duration diffs stay accurate. Wall-clock NativeClock can jump; MockClock is for tests; DatePoint is a date type, not a clock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "51. True or False: you should guard ClockInterface::now() with a nullsafe operator because it may return null with a frozen MockClock."
    **✅ False**

    False. now() is typed : \\DateTimeImmutable and always returns a DatePoint, even with a frozen MockClock, so ?-> is unnecessary. The real bug is comparing a MockClock time against a live new \\DateTime() — read time from the clock on both sides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "52. Which object does VarDumper's VarCloner produce before rendering?"
    **✅ A Data object**

    The cloner captures the variable into an immutable, depth-limited Data object, which a CliDumper or HtmlDumper then renders — separating capture from output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

??? question "53. What does dd() do that dump() does not?"
    **✅ It stops execution (exit) after dumping**

    dd() means 'dump and die': it dumps then calls exit, halting the script. dump() records the variable and lets execution continue (the dump is shown in the toolbar/collector).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html#the-dump-function)

??? question "54. What unit does StopwatchEvent::getDuration() use, and when is the debug.stopwatch service available?"
    **✅ Milliseconds; the service exists only when debug/the profiler is enabled**

    getDuration() returns milliseconds, and the autowirable debug.stopwatch service is only registered in debug (dev/test). Injecting Stopwatch in prod therefore causes a wiring error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

??? question "55. A service that autowires Symfony\Component\Stopwatch\Stopwatch works in dev but fails to boot in prod. Why?"
    **✅ The debug.stopwatch service exists only in debug mode, so the dependency is missing in prod**

    Stopwatch's framework service is registered only when debug is enabled, so in prod there is nothing to inject and the container fails. Use it for ad-hoc dev profiling only; for prod metrics use real observability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

??? question "56. An uncaught exception that does NOT implement HttpExceptionInterface produces which status code?"
    **✅ 500**

    Only HttpExceptionInterface carries a custom status code; any other throwable defaults to HTTP 500 via the error controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "57. What does the ErrorHandler component do with a PHP warning or notice?"
    **✅ Converts it into a catchable \ErrorException via set_error_handler()**

    ErrorHandler registers set_error_handler() to throw \\ErrorException for PHP errors (warnings, notices, fatals via a shutdown function), making them catchable. It does not turn them into HttpExceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

??? question "58. Which serializable object represents a throwable for rendering and logging?"
    **✅ FlattenException**

    Throwables are normalised into a FlattenException — a serializable snapshot (class, message, status, trace) that error renderers (HTML/JSON/XML) turn into output and that is safe to log. HttpException is a throwable, not the snapshot.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

??? question "59. In a controller, which throw produces a 404 rendered by the framework error controller?"
    **✅ throw new NotFoundHttpException('...') — it implements HttpExceptionInterface with status 404**

    NotFoundHttpException implements HttpExceptionInterface, so the error controller maps it to 404 via getStatusCode(). A plain \\RuntimeException or \\InvalidArgumentException does not carry a status and becomes 500. You do not need to build the Response manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "60. When does the Web Profiler collect data for a request?"
    **✅ On kernel.response, with late collectors running at kernel.terminate**

    Profiler::collect() runs on kernel.response, invoking each DataCollector; LateDataCollectorInterface::lateCollect() runs later at terminate for data not complete during the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler.html)

??? question "61. Which service tag registers a custom data collector (with a toolbar/panel)?"
    **✅ data_collector (with a `template` attribute for the panel)**

    The data_collector tag wires a DataCollectorInterface; supplying a `template` attribute makes its toolbar badge and panel appear. Autoconfigure applies the tag automatically for services implementing the interface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

??? question "62. A custom collector storing a PDO connection in $this->data breaks profile storage. Why?"
    **✅ $this->data is serialized to storage (via VarDumper's cloner); a live connection/resource is not serializable**

    Profiles are persisted per token, so $this->data must be serializable — store scalar/array (VarDumper-clonable) data, not live resources like a PDO connection or an entity with a connection. Implement reset() for worker reuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

??? question "63. Your metric is only complete after the response is sent. Which interface should the collector implement?"
    **✅ LateDataCollectorInterface (its lateCollect() runs at kernel.terminate)**

    Normal collect() runs on kernel.response, too early for post-response data (final dumps, cache calls). LateDataCollectorInterface::lateCollect() runs later at terminate, when that data is complete.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

??? question "64. Which mechanism does Symfony 8 use for translation pluralization?"
    **✅ ICU MessageFormat, e.g. {count, plural, one {…} other {# …}}**

    ICU MessageFormat handles plural/select rules with locale-aware categories (one/few/many/other); the old pipe syntax is legacy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "65. What does the translator return when a message id has no translation in the active locale or its fallbacks?"
    **✅ The message id itself (and it is logged in dev)**

    A missing translation returns the untranslated id, not an error or empty string, so the UI degrades gracefully. In dev the miss is logged so you can fix the catalogue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

??? question "66. Which class returns the localized display name of a country code?"
    **✅ Symfony\Component\Intl\Countries (Countries::getName('FR'))**

    Countries::getName() reads the bundled ICU dataset and returns the name in the current/requested locale. Related classes are Languages, Locales, Currencies and Timezones. The other namespaces do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/intl.html)

??? question "67. What is the default translation domain, and what file naming applies ICU formatting?"
    **✅ Default domain is messages; the +intl-icu suffix (messages+intl-icu.<locale>.yaml) enables ICU formatting**

    When no domain is passed, trans() uses messages; validators and security are separate domains. ICU MessageFormat is applied to catalogues named with the +intl-icu suffix — forgetting it means ICU rules are not parsed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "68. What makes Filesystem::dumpFile() safe against partial reads?"
    **✅ It writes to a temporary file then atomically renames it into place**

    dumpFile() writes to a temp file and renames it, so a reader always sees either the old content or the complete new content, never a half-written file. appendToFile(), by contrast, is not atomic.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html)

??? question "69. Which Finder method defines the directories to search?"
    **✅ in()**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

??? question "70. How does Symfony\Component\Filesystem\Filesystem signal a failed operation (e.g. copy())?"
    **✅ It throws an IOExceptionInterface (it does not return false)**

    Unlike native file functions that return false, Filesystem methods throw IOExceptionInterface on failure, so errors cannot be silently ignored. Also note Path helpers manipulate path strings only and never touch the disk.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html#error-handling)

??? question "71. A Finder query returns directories as well as files. What is missing?"
    **✅ A ->files() call — without files() or directories() the Finder yields both**

    Finder yields both files and directories unless you narrow it with files() (or directories()). name()/in() do not restrict the entry type. Iterated results are Finder SplFileInfo objects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

??? question "72. Which of the following statements are true about the Symfony Cache component? (select all that apply)"
    **✅ CacheInterface::get($key, $callback) runs the callback only on a cache miss and stores its return value ; Cache tags require a tag-aware pool (TagAwareAdapter or tags: true); calling $item->tag() on a plain pool does not work ; If the callback returns null, that null is stored and later calls return it as a hit until it expires**

    The contracts get() computes-and-stores on miss, tags only work on a TagAwareAdapter/pool configured with tags: true, and a stored null is a valid cached value that counts as a hit. PSR-16 has no tags and no deferred saves (those are PSR-6 features), and get() never returns null to mean "miss" — on a miss it runs the callback and returns its result.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html)

??? question "73. Which of the following statements are true about the Symfony Clock component? (select all that apply)"
    **✅ ClockInterface::now() returns an immutable DatePoint (a \DateTimeImmutable subclass), never a mutable \DateTime ; MockClock::sleep() advances virtual time instantly, with no real delay — ideal for TTL/expiry tests**

    now() is typed to return a \DateTimeImmutable and yields a DatePoint, and MockClock advances time virtually so tests never wait. The default framework clock is NativeClock in every environment (tests swap in MockClock themselves), and MonotonicClock is for measuring durations precisely because it is immune to system clock changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "74. Which of the following statements are true about the Symfony Lock component? (select all that apply)"
    **✅ acquire() is non-blocking by default: it returns false immediately when the lock is already held ; FlockStore and SemaphoreStore only guarantee mutual exclusion on a single machine ; Locks have a TTL (300 seconds by default), and long jobs must call refresh() to extend it**

    The default acquire(false) returns a plain false when the resource is busy, local stores (flock/semaphore) never protect across machines, and the TTL expires mid-job unless refresh() extends it. Non-blocking acquire() does not throw on contention (only blocking acquisition can end in LockConflictedException), and multi-server exclusion needs a shared store such as Redis or a database.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html)

??? question "75. Which of the following statements are true about the Symfony Mailer and Mime components? (select all that apply)"
    **✅ When SendEmailMessage is routed to an async Messenger transport, MailerInterface::send() queues the email instead of delivering it inline ; Images embedded with embedFromPath() are referenced in the HTML body via a cid: reference**

    With Messenger routing configured, send() dispatches a SendEmailMessage that a worker delivers later, and embedded parts are addressed with cid: in the HTML body. TemplatedEmail is part of the Twig bridge (Symfony\Bridge\Twig\Mime), and the Envelope (sender/recipients used for the SMTP conversation) is distinct from the message headers rendered in the visible email.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html)

??? question "76. Which of the following statements are true about the Symfony Process component? (select all that apply)"
    **✅ new Process(['git', 'log', $input]) auto-escapes each array element, so $input cannot inject shell syntax ; The default process timeout is 60 seconds; setTimeout(null) disables it ; mustRun() throws a ProcessFailedException when the process exits with a non-zero code**

    The array constructor escapes every argument, the timeout defaults to 60 seconds (nullable to disable), and mustRun() throws ProcessFailedException on failure where run() only returns the exit code. fromShellCommandline() runs a raw string through the shell with no escaping (a command-injection risk), and stdout is read via getOutput(), not from run().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

??? question "77. Which of the following statements are true about the Symfony Serializer? (select all that apply)"
    **✅ serialize() works in two stages: normalizers turn objects into arrays, then an encoder turns the array into a string ; #[Groups] attributes only filter properties when a 'groups' key is passed in the serialization context**

    Serialization is normalize-then-encode, and group filtering is inert until you pass ['groups' => [...]] in the context — without it all readable fields are emitted. PropertyNormalizer accesses properties directly via reflection (ObjectNormalizer is the one using accessors), and null properties are serialized as null unless you enable the skip_null_values context option.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html)

??? question "78. A class exposes its data only through __call() (no real getX()/setX() methods). You read a path with the default PropertyAccessor. What happens?"
    **✅ It throws — __call fallback is not enabled by default, only __get/__set are**

    PropertyAccessorBuilder defaults to MAGIC_GET | MAGIC_SET only; __call is disabled unless enableMagicCall() is explicitly called. Without it, a class reachable only via __call() is not accessible through the default accessor, and getValue() throws rather than returning null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/property_access.html#magic-getters-and-setters)

??? question "79. getValue() throws UninitializedPropertyException for one object and NoSuchPropertyException for another, both accessed via the same path 'title'. What distinguishes the two cases?"
    **✅ The first object declares a typed $title property that was never assigned; the second has no title property/getter/setter at all**

    UninitializedPropertyException (a subtype of AccessException) means the property genuinely exists — typed, but never given a value — while NoSuchPropertyException means no getter, public property, or enabled magic method could resolve the path at all. isReadable() would have returned false for both without distinguishing them; only the thrown exception type tells them apart.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PropertyAccess/Exception/UninitializedPropertyException.php)

---

<small>Back to [Flashcards](index.md) · [Miscellaneous](../../miscellaneous/index.md)</small>
