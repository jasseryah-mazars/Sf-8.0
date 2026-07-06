# Flashcards — Miscellaneous

96 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. What does MessageBusInterface::dispatch() return?"
    **✅ An Envelope**

    dispatch() always returns the (possibly stamped) Envelope. A handler's return value is available via $envelope->last(HandledStamp::class)->getResult(). It never returns the value directly because a routed (async) message is not handled in this process at all — only the Envelope exists yet.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html)

??? question "2. A message is routed to an async transport. During dispatch() in the web process, the handler…"
    **✅ does not run — SendMessageMiddleware serializes and sends it, stopping the bus**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later. It is not handled twice, and a running worker is irrelevant to the dispatching process. NoHandlerForMessageException only occurs when no handler exists for a synchronously handled message.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages)

??? question "3. DelayStamp(5000) delays delivery by how long?"
    **✅ 5000 milliseconds (5 seconds)**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds. The classic trap is to read it as seconds; the retry strategy's initial delay is likewise in milliseconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#delaying-messages)

??? question "4. After a message exhausts its configured retries, where does it go?"
    **✅ To the configured failure transport**

    Once max_retries is reached the envelope is sent to the failure_transport, where messenger:failed:show/retry can inspect and requeue it. Without a failure transport the message would be lost, which is why configuring one is a best practice.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#saving-retrying-failed-messages)

??? question "5. Which middleware locates and invokes the handler(s), adding a HandledStamp?"
    **✅ HandleMessageMiddleware**

    HandleMessageMiddleware resolves handlers for the message type, calls them, and records each result in a HandledStamp. SendMessageMiddleware only routes/sends to transports (and may stop the bus before Handle runs).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#middleware)

??? question "6. How do you make a failing handler skip retries and go straight to the failure transport?"
    **✅ Throw UnrecoverableMessageHandlingException**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately. A handler's return value never influences retries, and there is no stopPropagation() on an Envelope.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

??? question "7. Which attribute marks a service as a message handler in Symfony 8?"
    **✅ #[AsMessageHandler]**

    Symfony\\Component\\Messenger\\Attribute\\AsMessageHandler registers an invokable service (or a specific method) as a handler for its typed message argument. The other names do not exist in the component.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#registering-handlers)

??? question "8. What is the purpose of DispatchAfterCurrentBusStamp?"
    **✅ Defer delivery of a message dispatched inside a handler until the current handling finishes successfully**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them. It has nothing to do with delays, multi-bus fan-out, or retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/dispatch_after_current_bus.html)

??? question "9. True or False: routing a message to the sync:// transport skips the middleware pipeline."
    **✅ False**

    False. sync:// still runs the full middleware stack (validation, transactions, handler discovery) — it simply handles the message immediately in the same process instead of enqueueing it. Treating sync:// as "no bus" is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transport-configuration)

??? question "10. A dispatched message throws NoHandlerForMessageException. What is the most likely cause?"
    **✅ The handler class is missing #[AsMessageHandler] (or its __invoke argument type does not match the message)**

    Handlers are discovered by autoconfiguration of the #[AsMessageHandler] attribute and matched by the typed argument of __invoke(). Missing the attribute (or a mismatched/imported type) means no handler is registered. Worker state, failure transport and message immutability are unrelated to handler resolution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#registering-handlers)

??? question "11. Which statements about Messenger buses are correct? (choose 2)"
    **✅ The default bus service is messenger.bus.default ; You can define multiple buses, each with its own ordered middleware list**

    Messenger ships one default bus (messenger.bus.default) but supports many, each configured with its own middleware — so a command bus can wrap handlers in a transaction while an event bus does not. The command/query/ event convention is just that: a convention, not enforced by the code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/multiple_buses.html)

??? question "12. During messenger:consume, which event is dispatched when a handler throws an exception?"
    **✅ WorkerMessageFailedEvent**

    The worker loop dispatches WorkerMessageReceivedEvent, then on success WorkerMessageHandledEvent (ack) or on exception WorkerMessageFailedEvent (reject/retry). WorkerRunningEvent fires between receives and WorkerStoppedEvent on shutdown — neither signals a handler failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-events)

??? question "13. With retry_strategy delay: 1000 and multiplier: 2, what are the delays before the 1st, 2nd and 3rd retry?"
    **✅ 1000 ms, 2000 ms, 4000 ms (delay × multiplier per attempt)**

    MultiplierRetryStrategy multiplies the initial delay by the multiplier for each successive attempt: 1000, 1000×2=2000, 2000×2=4000 (capped by max_delay if set). It is exponential, not constant or linear, and starts at the configured delay, not delay×multiplier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

??? question "14. An order handler dispatches an 'order confirmed' email message, but the email is sent even when the surrounding DB transaction rolls back. What fixes this?"
    **✅ Dispatch the email message with DispatchAfterCurrentBusStamp so it is delivered only after the current handler finishes successfully**

    DispatchAfterCurrentBusStamp defers the inner dispatch until the current message finishes handling successfully, so a rollback cancels the email. A delay only postpones sending, the unrecoverable exception affects the email's own retries, and sync routing would send it immediately during the transaction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/dispatch_after_current_bus.html)

??? question "15. $envelope->last(HandledStamp::class) returns null. Which situation explains this best?"
    **✅ The message was routed to an async transport, so it has not been handled in this process yet**

    A handler that returns null still produces a HandledStamp (its result is null) — so last() returning null means no such stamp exists, i.e. the message was sent async and not handled here. dispatch() always returns an Envelope (never null), and HandledStamp is not query-bus-specific. This is why the nullsafe ?-> guards 'not handled here', distinct from 'handled, returned null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

??? question "16. Which serializer does a Messenger transport use by default to serialize the envelope?"
    **✅ PhpSerializer (native PHP serialize())**

    By default transports use Transport\\Serialization\\PhpSerializer, which calls PHP's serialize(). The Symfony Serializer transport serializer is opt-in and recommended for cross-language/cross-app interop, but it is not the default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#serializing-messages)

??? question "17. In a custom middleware, code placed AFTER the $stack->next()->handle($envelope, $stack) call runs…"
    **✅ On the way out — after the inner middleware and the handler have executed**

    The middleware stack is a russian-doll chain: code before $stack->next()->handle() runs on the way in, and code after it runs on the way out once the rest of the pipeline (including the handler) has returned. This lets a middleware wrap the whole handling (e.g. open/commit a transaction).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#creating-your-own-middleware)

??? question "18. After a deploy, long-running workers keep executing the old code. Which approach fixes this for zero-downtime deploys?"
    **✅ Run messenger:stop-workers on deploy and let a supervisor restart workers, ideally combined with --time-limit/--memory-limit**

    Workers bootstrap the kernel once and keep it in memory, so new code is only picked up after a restart. messenger:stop-workers signals running workers to finish the current message and exit; a process manager then restarts them with the new code. --time-limit/--memory-limit make them recycle regularly. The other options don't reload the worker's code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

??? question "19. How do you retrieve a synchronous handler's return value after MessageBusInterface::dispatch()?"
    **✅ $envelope->last(HandledStamp::class)->getResult()**

    dispatch() returns an Envelope. For a single sync handler you read its result via the HandledStamp: $envelope->last(HandledStamp::class)->getResult(). Use HandleTrait to unwrap it in a query bus. Envelope has no getResult() and the bus does not cache a "last result".

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

??? question "20. What information does a RedeliveryStamp carry on a retried message?"
    **✅ The current retry count (and timing), so the retry strategy knows how many attempts have happened**

    RedeliveryStamp records the retry count (and redelivery timestamp). The worker reads it to compare against max_retries and to compute the next delay via the retry strategy. Handler identity is on HandlerFailedStamp, not here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

??? question "21. Inside a custom middleware, how do you pass the envelope on to the rest of the stack?"
    **✅ return $stack->next()->handle($envelope, $stack);**

    A MiddlewareInterface::handle() implementation calls $stack->next()->handle($envelope, $stack) to invoke the next middleware. Code before that call runs on the way in; code after it runs on the way out. Re-dispatching via the bus would restart the whole pipeline.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#creating-your-own-middleware)

??? question "22. Which built-in transport handles a message immediately in the same process, without a queue?"
    **✅ The sync transport (DSN sync://)**

    sync:// processes the message synchronously during dispatch. in-memory:// keeps messages in memory for tests, while doctrine/amqp/redis are real asynchronous transports consumed by a worker.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transport-configuration)

??? question "23. In framework.messenger.routing, mapping App\Message\SmsNotification to 'async' means…"
    **✅ SendMessageMiddleware sends that message class to the 'async' transport instead of handling it in-process**

    routing maps a message class (or interface/parent) to one or more transport names. A routed message is serialized and sent to that transport rather than handled synchronously. A message with no routing entry is handled immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#routing-messages-to-a-transport)

??? question "24. Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?"
    **✅ --limit (max messages) and --time-limit (max seconds), optionally with memory limits**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

??? question "25. Under a transport's retry_strategy, what does the 'multiplier' option control?"
    **✅ The factor by which the delay grows between successive retries (exponential backoff)**

    retry_strategy defines max_retries, delay (initial, ms), multiplier (delay is multiplied by this each attempt) and max_delay to cap it, producing exponential backoff before the failure transport is used.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

??? question "26. Which transport is intended specifically for functional tests, asserting dispatched messages without a broker?"
    **✅ The in-memory transport (in-memory://), inspected via getSent()**

    in-memory:// keeps envelopes in memory instead of sending them, so a test can fetch the transport from the container and assert on getSent(). It is reset between tests via the messenger reset behaviour.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#testing)

??? question "27. Symfony\Contracts\Cache\CacheInterface::get() runs its callback…"
    **✅ only on a cache miss, then stores and returns the value**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection. Running on every call would defeat caching, and unlike PSR-6 you do not call save() manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

??? question "28. Which statement about PSR-6 vs PSR-16 is correct?"
    **✅ PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

??? question "29. Cache stampede protection in Symfony Cache is implemented by…"
    **✅ probabilistic early expiration controlled by the $beta factor**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

??? question "30. Which adapter keeps entries only for the current process (ideal for tests)?"
    **✅ ArrayAdapter**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

??? question "31. Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?"
    **✅ null is returned as a cache hit; the callback is NOT run again**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

??? question "32. A pool is declared with `tags: true` in cache.yaml. What does this enable?"
    **✅ Tagging items with $item->tag([...]) and evicting groups via invalidateTags([...])**

    `tags: true` wraps the pool in a TagAwareAdapter implementing TagAwareCacheInterface, so items can carry tags and invalidateTags() evicts all items with a given tag — invalidation by concern rather than by key. Calling $item->tag() on a non-tag-aware pool errors.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#using-cache-tags)

??? question "33. True or False: passing $beta = INF to CacheInterface::get() forces the value to be recomputed immediately."
    **✅ True**

    True. $beta = INF forces early expiration, so the callback runs and the value is refreshed on this call. $beta = 0 disables early expiration entirely; the default (null) picks a sensible probabilistic value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

??? question "34. Using the raw PSR-6 API, how do you distinguish a stored null value from a missing key?"
    **✅ Check $item->isHit() — get() returns null for both cases**

    With PSR-6, CacheItemInterface::get() returns null both for an absent key and for a genuinely stored null, so you must call isHit() to tell them apart. The contracts callback API sidesteps this ambiguity; there is no hasKey() or miss exception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

??? question "35. In serialize(), which stage runs first?"
    **✅ The normalizer (object to array), then the encoder (array to string)**

    serialize() normalizes the object to an array/scalars, then encodes that to a string. deserialize() reverses it: decode then denormalize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/serializer.html)

??? question "36. #[Groups(['read'])] on a property takes effect when…"
    **✅ the context includes ['groups' => ['read']]**

    Group filtering only applies when matching groups are passed in the context; otherwise the group attribute has no effect and all fields are (de)serialized.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

??? question "37. Which normalizer reads and writes private properties directly via reflection?"
    **✅ PropertyNormalizer**

    PropertyNormalizer accesses object properties directly (including private), whereas ObjectNormalizer uses accessors and the constructor, and GetSetMethodNormalizer uses only get/set methods. JsonEncoder is an encoder, not a normalizer.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

??? question "38. By default, what is the Serializer's circular reference limit before it throws?"
    **✅ 1 (unless a circular reference handler or #[MaxDepth] is set)**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

??? question "39. A UserDto has #[Groups(['read'])] #[SerializedName('full_name')] on $name and #[Ignore] on $passwordHash. What is the JSON when serialized with context ['groups' => ['read']]?"
    **✅ {"full_name":"..."} plus any other read-group fields; passwordHash is omitted**

    With the read group in context, only read-group properties are emitted; $name is renamed to full_name by #[SerializedName], and #[Ignore] drops passwordHash entirely regardless of group. Groups are honoured only because they are passed in the context.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

??? question "40. What does the framework.serializer.default_context option skip_null_values: true do?"
    **✅ Omits properties whose value is null from the serialized output**

    By default a null property is serialized as \"key\":null. Setting AbstractObjectNormalizer::SKIP_NULL_VALUES (skip_null_values) omits those keys from the payload. The classic bug is a consumer treating an absent key as an error rather than 'the value was null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html)

??? question "41. A private property with no getter is missing from the JSON produced by the default ObjectNormalizer. Why, and how do you fix it?"
    **✅ ObjectNormalizer uses accessors; add a getter (or use PropertyNormalizer, which reads properties directly)**

    ObjectNormalizer reads via getters/issers/hassers and the constructor, so a private property without an accessor is invisible. Provide a getter or switch to PropertyNormalizer, which uses reflection to read properties directly. Groups filter fields but do not expose accessorless private properties.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

??? question "42. In which environment is .env.local NOT loaded?"
    **✅ test**

    .env.local is intentionally skipped in the test environment so tests run from committed defaults and stay reproducible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#selecting-the-active-environment)

??? question "43. What does `composer dump-env prod` produce, and what is the effect?"
    **✅ .env.local.php — Symfony loads it directly and skips parsing .env* files**

    The whole .env* cascade is compiled to a plain PHP array in .env.local.php, which Symfony loads directly, avoiding DotEnv parsing on each request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production)

??? question "44. ExpressionLanguage::compile() returns what?"
    **✅ A string of PHP source code**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

??? question "45. A .env file sets DATABASE_URL, but a real OS environment variable DATABASE_URL is also exported. Which wins?"
    **✅ The real OS environment variable — DotEnv never overrides an existing real env var**

    Real OS environment variables always take precedence; the DotEnv cascade (.env → .env.local → .env.<env> → .env.<env>.local) only fills values not already set in the real environment. Later .env* files override earlier ones but never a real env var.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#overriding-environment-values-via-env-local)

??? question "46. What is the result of ExpressionLanguage::compile('1 + a', ['a'])?"
    **✅ The PHP source string "(1 + $a)"**

    compile() emits PHP source, turning the variable name a into $a: "(1 + $a)". It does not evaluate anything (so no undefined-variable error) — use evaluate('1 + a', ['a' => 5]) to get the value 6.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

??? question "47. Which class merges every config source and validates it against a bundle's Configuration tree?"
    **✅ Processor (Processor::processConfiguration())**

    Processor::processConfiguration() merges all sources and validates them against the tree returned by the Configuration class, applying defaults and constraints. TreeBuilder only defines the schema; FileLocator finds files.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/config/definition.html)

??? question "48. Which composer flag excludes require-dev packages when deploying to production?"
    **✅ --no-dev**

    `composer install --no-dev` skips require-dev packages (profiler, PHPUnit, etc.). Add --optimize-autoloader (or --classmap-authoritative) to build an optimised classmap and cut per-class filesystem stat calls.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "49. You changed a YAML config file and redeployed to prod, but the change has no effect. Why?"
    **✅ Prod loads the compiled container as-is and does not auto-detect config changes; you must clear/warm the cache on deploy**

    In prod the compiled container in var/cache/prod is loaded as-is with no freshness checks (those exist only in debug), so config changes require cache:clear + cache:warmup on deploy. Enabling APP_DEBUG in prod is unsafe and not the fix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "50. Why set opcache.validate_timestamps=0 in production?"
    **✅ To skip per-request file-modification checks and always serve cached bytecode (reset opcache on deploy instead)**

    With immutable deploys, disabling timestamp validation maximises opcache hits by not stat-ing files each request. Because opcache then never notices new files, you must reset opcache (or the PHP process manager) on each deploy so the new bytecode is loaded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/performance.html)

??? question "51. Which ordered command sequence is correct for a from-scratch prod deploy?"
    **✅ composer install --no-dev --optimize-autoloader → composer dump-env prod → cache:clear → cache:warmup → reset opcache**

    You install prod deps first, compile the env cascade with dump-env prod, then clear and warm the cache so the first live request is fast, and finally reset opcache. Warming before installing, or shipping dev deps / APP_DEBUG=1, are wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "52. What does `cache:clear` run, by default, in addition to removing stale cache?"
    **✅ The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "53. True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled."
    **✅ False**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

??? question "54. Which Process constructor auto-escapes each argument?"
    **✅ new Process(['git', 'log', '--oneline'])**

    The array form escapes each element automatically. fromShellCommandline() runs a raw shell string and does not escape, risking command injection if you interpolate untrusted input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

??? question "55. What does Process::run() return?"
    **✅ The integer exit code**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

??? question "56. What is the default Process timeout?"
    **✅ 60 seconds**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#process-timeout)

??? question "57. You build a command from user input using Process::fromShellCommandline('convert '.$userInput). What is the risk and the fix?"
    **✅ Command injection — use the array constructor new Process(['convert', $userInput]) so each argument is auto-escaped**

    fromShellCommandline runs the string through /bin/sh with no escaping, so untrusted input can inject shell metacharacters. The array constructor escapes each element as a single argument, eliminating the injection vector. This is unrelated to timeouts or platform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

??? question "58. Which call runs a process and throws automatically on a non-zero exit code?"
    **✅ mustRun() — it throws ProcessFailedException on failure**

    mustRun() behaves like run() but throws ProcessFailedException when the process exits non-zero. run() simply returns the integer exit code and you check isSuccessful() yourself; start()/wait() are for async execution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

??? question "59. LockInterface::acquire() called with no argument is…"
    **✅ non-blocking — it returns false immediately if the lock is held**

    acquire() defaults to non-blocking; pass true to block until the resource becomes available (store permitting). It returns a boolean false when held, it does not throw, so `if (!$lock->acquire()) { return; }` is the correct guard.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html#blocking-locks)

??? question "60. Which lock store provides mutual exclusion across multiple servers?"
    **✅ RedisStore**

    Flock and Semaphore stores are local to one machine, and InMemoryStore is per-process (tests). Shared stores like Redis (or a database store) coordinate locks across servers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#available-stores)

??? question "61. Why call refresh() during a long critical section?"
    **✅ To extend the lock's TTL so it is not considered expired mid-job**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity; without it another process could acquire the lock after the TTL, breaking mutual exclusion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

??? question "62. Which is the correct guard to skip work another process is already doing?"
    **✅ if (!$lock->acquire()) { return; }**

    Non-blocking acquire() returns false when the resource is held, so !$lock->acquire() is the idiomatic early-return guard. It does not return null and does not throw on contention (only blocking acquire(true) may throw LockConflictedException). Forgetting to check the boolean means entering the critical section unprotected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html)

??? question "63. What is the default TTL of a lock created via LockFactory::createLock($resource)?"
    **✅ 300 seconds (5 minutes), with autoRelease on by default**

    createLock(string $resource, ?float $ttl = 300.0, bool $autoRelease = true) defaults to a 300 second TTL and releases the lock when the Lock object is destroyed. Long jobs should raise the TTL and call refresh() to avoid premature expiry.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

??? question "64. With Messenger routing configured for emails, MailerInterface::send() will…"
    **✅ dispatch a SendEmailMessage to be delivered by a worker**

    When SendEmailMessage is routed to a transport, send() enqueues it; a worker delivers it later, giving async sending plus retries. It does not throw if a worker is down — the message just waits in the queue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

??? question "65. Which class renders Twig templates into an email body?"
    **✅ Symfony\Bridge\Twig\Mime\TemplatedEmail**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending. Plain Email has no template support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

??? question "66. How is an inline (embedded) image referenced from an email's HTML body?"
    **✅ Via a cid: reference produced by embed()/embedFromPath()**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

??? question "67. In the Mailer, how does the Envelope differ from the message headers?"
    **✅ The Envelope holds the actual sender/recipients used for the SMTP conversation; headers (From/To) render in the visible message**

    Mailer's Envelope (sender + recipients) drives the transport's SMTP exchange, whereas the message headers (From, To, Subject) are what the recipient sees. They can legitimately differ (e.g. bounce address vs visible From), which is a common exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages)

??? question "68. Which configuration makes emails send asynchronously via Messenger?"
    **✅ Route Symfony\Component\Mailer\Messenger\SendEmailMessage to a transport in messenger routing (and run a worker)**

    Async delivery comes from routing SendEmailMessage to a Messenger transport and consuming it with a worker. MAILER_DSN chooses the delivery transport (SMTP/API), not sync-vs-async, and there is no framework.mailer.async flag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

??? question "69. What does public/index.php return under the Runtime component?"
    **✅ A callable that produces the application object (e.g. a Kernel)**

    index.php returns a callable; autoload_runtime.php resolves its arguments, invokes it, then a RunnerInterface handles/sends/terminates. It never calls handle() itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "70. Which environment variable selects the runtime class?"
    **✅ APP_RUNTIME**

    APP_RUNTIME (or composer.json extra.runtime.class) chooses the RuntimeInterface implementation; the default is SymfonyRuntime, which extends GenericRuntime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

??? question "71. Which class does the default SymfonyRuntime extend?"
    **✅ GenericRuntime**

    SymfonyRuntime extends the framework-agnostic GenericRuntime, adding Symfony-aware resolvers/runners (inject Request, SymfonyStyle, console Input/Output; run a Kernel or console Application). It is not a kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "72. How does the argument `array $context` in the index.php closure get populated?"
    **✅ The runtime's resolver autowires it from $_SERVER (env vars like APP_ENV/APP_DEBUG)**

    RuntimeInterface::getResolver() builds a resolver that inspects the callable's typed arguments and supplies them — array $context comes from $_SERVER (env), and it can also inject Request, InputInterface, etc. You therefore never read $_SERVER manually in the entry point.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

??? question "73. ClockInterface::now() returns what type?"
    **✅ A \DateTimeImmutable (a DatePoint)**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "74. Which clock lets tests freeze or advance time without a real delay?"
    **✅ MockClock — you set the time and its sleep() advances virtual time**

    MockClock is constructed with a fixed time and its sleep() advances time virtually (no real waiting), perfect for TTL/expiry tests. NativeClock is the real prod clock; MonotonicClock is for durations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html#usage-in-tests)

??? question "75. Which clock is best for measuring elapsed durations and is immune to system clock changes?"
    **✅ MonotonicClock**

    MonotonicClock uses a high-resolution monotonic source unaffected by NTP or manual clock adjustments, so duration diffs stay accurate. Wall-clock NativeClock can jump; MockClock is for tests; DatePoint is a date type, not a clock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "76. True or False: you should guard ClockInterface::now() with a nullsafe operator because it may return null with a frozen MockClock."
    **✅ False**

    False. now() is typed : \\DateTimeImmutable and always returns a DatePoint, even with a frozen MockClock, so ?-> is unnecessary. The real bug is comparing a MockClock time against a live new \\DateTime() — read time from the clock on both sides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "77. Which object does VarDumper's VarCloner produce before rendering?"
    **✅ A Data object**

    The cloner captures the variable into an immutable, depth-limited Data object, which a CliDumper or HtmlDumper then renders — separating capture from output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

??? question "78. What does dd() do that dump() does not?"
    **✅ It stops execution (exit) after dumping**

    dd() means 'dump and die': it dumps then calls exit, halting the script. dump() records the variable and lets execution continue (the dump is shown in the toolbar/collector).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html#the-dump-function)

??? question "79. What unit does StopwatchEvent::getDuration() use, and when is the debug.stopwatch service available?"
    **✅ Milliseconds; the service exists only when debug/the profiler is enabled**

    getDuration() returns milliseconds, and the autowirable debug.stopwatch service is only registered in debug (dev/test). Injecting Stopwatch in prod therefore causes a wiring error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

??? question "80. A service that autowires Symfony\Component\Stopwatch\Stopwatch works in dev but fails to boot in prod. Why?"
    **✅ The debug.stopwatch service exists only in debug mode, so the dependency is missing in prod**

    Stopwatch's framework service is registered only when debug is enabled, so in prod there is nothing to inject and the container fails. Use it for ad-hoc dev profiling only; for prod metrics use real observability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

??? question "81. An uncaught exception that does NOT implement HttpExceptionInterface produces which status code?"
    **✅ 500**

    Only HttpExceptionInterface carries a custom status code; any other throwable defaults to HTTP 500 via the error controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "82. What does the ErrorHandler component do with a PHP warning or notice?"
    **✅ Converts it into a catchable \ErrorException via set_error_handler()**

    ErrorHandler registers set_error_handler() to throw \\ErrorException for PHP errors (warnings, notices, fatals via a shutdown function), making them catchable. It does not turn them into HttpExceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

??? question "83. Which serializable object represents a throwable for rendering and logging?"
    **✅ FlattenException**

    Throwables are normalised into a FlattenException — a serializable snapshot (class, message, status, trace) that error renderers (HTML/JSON/XML) turn into output and that is safe to log. HttpException is a throwable, not the snapshot.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

??? question "84. In a controller, which throw produces a 404 rendered by the framework error controller?"
    **✅ throw new NotFoundHttpException('...') — it implements HttpExceptionInterface with status 404**

    NotFoundHttpException implements HttpExceptionInterface, so the error controller maps it to 404 via getStatusCode(). A plain \\RuntimeException or \\InvalidArgumentException does not carry a status and becomes 500. You do not need to build the Response manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "85. When does the Web Profiler collect data for a request?"
    **✅ On kernel.response, with late collectors running at kernel.terminate**

    Profiler::collect() runs on kernel.response, invoking each DataCollector; LateDataCollectorInterface::lateCollect() runs later at terminate for data not complete during the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler.html)

??? question "86. Which service tag registers a custom data collector (with a toolbar/panel)?"
    **✅ data_collector (with a `template` attribute for the panel)**

    The data_collector tag wires a DataCollectorInterface; supplying a `template` attribute makes its toolbar badge and panel appear. Autoconfigure applies the tag automatically for services implementing the interface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

??? question "87. A custom collector storing a PDO connection in $this->data breaks profile storage. Why?"
    **✅ $this->data is serialized to storage (via VarDumper's cloner); a live connection/resource is not serializable**

    Profiles are persisted per token, so $this->data must be serializable — store scalar/array (VarDumper-clonable) data, not live resources like a PDO connection or an entity with a connection. Implement reset() for worker reuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

??? question "88. Your metric is only complete after the response is sent. Which interface should the collector implement?"
    **✅ LateDataCollectorInterface (its lateCollect() runs at kernel.terminate)**

    Normal collect() runs on kernel.response, too early for post-response data (final dumps, cache calls). LateDataCollectorInterface::lateCollect() runs later at terminate, when that data is complete.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

??? question "89. Which mechanism does Symfony 8 use for translation pluralization?"
    **✅ ICU MessageFormat, e.g. {count, plural, one {…} other {# …}}**

    ICU MessageFormat handles plural/select rules with locale-aware categories (one/few/many/other); the old pipe syntax is legacy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "90. What does the translator return when a message id has no translation in the active locale or its fallbacks?"
    **✅ The message id itself (and it is logged in dev)**

    A missing translation returns the untranslated id, not an error or empty string, so the UI degrades gracefully. In dev the miss is logged so you can fix the catalogue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

??? question "91. Which class returns the localized display name of a country code?"
    **✅ Symfony\Component\Intl\Countries (Countries::getName('FR'))**

    Countries::getName() reads the bundled ICU dataset and returns the name in the current/requested locale. Related classes are Languages, Locales, Currencies and Timezones. The other namespaces do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/intl.html)

??? question "92. What is the default translation domain, and what file naming applies ICU formatting?"
    **✅ Default domain is messages; the +intl-icu suffix (messages+intl-icu.<locale>.yaml) enables ICU formatting**

    When no domain is passed, trans() uses messages; validators and security are separate domains. ICU MessageFormat is applied to catalogues named with the +intl-icu suffix — forgetting it means ICU rules are not parsed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "93. What makes Filesystem::dumpFile() safe against partial reads?"
    **✅ It writes to a temporary file then atomically renames it into place**

    dumpFile() writes to a temp file and renames it, so a reader always sees either the old content or the complete new content, never a half-written file. appendToFile(), by contrast, is not atomic.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html)

??? question "94. Which Finder method defines the directories to search?"
    **✅ in()**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

??? question "95. How does Symfony\Component\Filesystem\Filesystem signal a failed operation (e.g. copy())?"
    **✅ It throws an IOExceptionInterface (it does not return false)**

    Unlike native file functions that return false, Filesystem methods throw IOExceptionInterface on failure, so errors cannot be silently ignored. Also note Path helpers manipulate path strings only and never touch the disk.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html#error-handling)

??? question "96. A Finder query returns directories as well as files. What is missing?"
    **✅ A ->files() call — without files() or directories() the Finder yields both**

    Finder yields both files and directories unless you narrow it with files() (or directories()). name()/in() do not restrict the entry type. Iterated results are Finder SplFileInfo objects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

---

<small>Back to [Flashcards](index.md) · [Miscellaneous](../../miscellaneous/index.md)</small>
