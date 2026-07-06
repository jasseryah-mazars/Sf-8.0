# Flashcards — Miscellaneous

37 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. What does MessageBusInterface::dispatch() return?"
    **✅ An Envelope**

    dispatch() always returns the (possibly stamped) Envelope. A handler's return value is available via $envelope->last(HandledStamp::class)->getResult().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html)

??? question "2. A message is routed to an async transport. During dispatch() in the web process, the handler…"
    **✅ does not run — SendMessageMiddleware serializes and sends it, stopping the bus**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages)

??? question "3. DelayStamp(5000) delays delivery by how long?"
    **✅ 5000 milliseconds (5 seconds)**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#delaying-messages)

??? question "4. After a message exhausts its configured retries, where does it go?"
    **✅ To the configured failure transport**

    Once max_retries is reached the envelope is sent to the failure_transport, where messenger:failed:show/retry can inspect and requeue it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#saving-retrying-failed-messages)

??? question "5. Which middleware locates and invokes the handler(s), adding a HandledStamp?"
    **✅ HandleMessageMiddleware**

    HandleMessageMiddleware resolves handlers for the message type, calls them, and records each result in a HandledStamp.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#middleware)

??? question "6. How do you make a failing handler skip retries and go straight to the failure transport?"
    **✅ Throw UnrecoverableMessageHandlingException**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

??? question "7. Which attribute marks a service as a message handler in Symfony 8?"
    **✅ #[AsMessageHandler]**

    Symfony\Component\Messenger\Attribute\AsMessageHandler registers an invokable service (or a specific method) as a handler for its typed message argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#registering-handlers)

??? question "8. What is the purpose of DispatchAfterCurrentBusStamp?"
    **✅ Defer delivery of a message dispatched inside a handler until the current handling finishes successfully**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/dispatch_after_current_bus.html)

??? question "9. Symfony\Contracts\Cache\CacheInterface::get() runs its callback…"
    **✅ only on a cache miss, then stores and returns the value**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

??? question "10. Which statement about PSR-6 vs PSR-16 is correct?"
    **✅ PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

??? question "11. Cache stampede protection in Symfony Cache is implemented by…"
    **✅ probabilistic early expiration controlled by the $beta factor**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

??? question "12. Which adapter keeps entries only for the current process (ideal for tests)?"
    **✅ ArrayAdapter**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

??? question "13. In serialize(), which stage runs first?"
    **✅ The normalizer (object to array), then the encoder (array to string)**

    serialize() normalizes the object to an array/scalars, then encodes that to a string. deserialize() decodes then denormalizes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/serializer.html)

??? question "14. #[Groups(['read'])] on a property takes effect when…"
    **✅ the context includes ['groups' => ['read']]**

    Group filtering only applies when matching groups are passed in the context; otherwise the group attribute has no effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

??? question "15. Which normalizer reads and writes private properties directly via reflection?"
    **✅ PropertyNormalizer**

    PropertyNormalizer accesses object properties directly (including private), whereas ObjectNormalizer uses accessors and the constructor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

??? question "16. By default, what is the Serializer's circular reference limit before it throws?"
    **✅ 1 (unless a circular reference handler or #[MaxDepth] is set)**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

??? question "17. In which environment is .env.local NOT loaded?"
    **✅ test**

    .env.local is intentionally skipped in the test environment so tests run from committed defaults and stay reproducible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#selecting-the-active-environment)

??? question "18. What does `composer dump-env prod` produce, and what is the effect?"
    **✅ .env.local.php — Symfony loads it directly and skips parsing .env* files**

    The whole .env* cascade is compiled to a plain PHP array in .env.local.php, which Symfony loads directly, avoiding DotEnv parsing on each request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production)

??? question "19. ExpressionLanguage::compile() returns what?"
    **✅ A string of PHP source code**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

??? question "20. Which Process constructor auto-escapes each argument?"
    **✅ new Process(['git', 'log', '--oneline'])**

    The array form escapes each element automatically. fromShellCommandline() runs a raw shell string and does not escape, risking command injection.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

??? question "21. What does Process::run() return?"
    **✅ The integer exit code**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

??? question "22. What is the default Process timeout?"
    **✅ 60 seconds**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#process-timeout)

??? question "23. LockInterface::acquire() called with no argument is…"
    **✅ non-blocking — it returns false immediately if the lock is held**

    acquire() defaults to non-blocking; pass true to block until the resource becomes available (store permitting).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html#blocking-locks)

??? question "24. Which lock store provides mutual exclusion across multiple servers?"
    **✅ RedisStore**

    Flock and Semaphore stores are local to one machine. Shared stores like Redis (or a database store) coordinate locks across servers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#available-stores)

??? question "25. Why call refresh() during a long critical section?"
    **✅ To extend the lock's TTL so it is not considered expired mid-job**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

??? question "26. With Messenger routing configured for emails, MailerInterface::send() will…"
    **✅ dispatch a SendEmailMessage to be delivered by a worker**

    When SendEmailMessage is routed to a transport, send() enqueues it; a worker delivers it later, giving async sending plus retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

??? question "27. Which class renders Twig templates into an email body?"
    **✅ Symfony\Bridge\Twig\Mime\TemplatedEmail**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

??? question "28. How is an inline (embedded) image referenced from an email's HTML body?"
    **✅ Via a cid: reference produced by embed()/embedFromPath()**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

??? question "29. What does public/index.php return under the Runtime component?"
    **✅ A callable that produces the application object (e.g. a Kernel)**

    index.php returns a callable; autoload_runtime.php resolves its arguments, invokes it, then a RunnerInterface handles/sends/terminates.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

??? question "30. Which environment variable selects the runtime class?"
    **✅ APP_RUNTIME**

    APP_RUNTIME (or composer.json extra.runtime.class) chooses the RuntimeInterface implementation; the default is SymfonyRuntime, which extends GenericRuntime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

??? question "31. ClockInterface::now() returns what type?"
    **✅ A \DateTimeImmutable (a DatePoint)**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

??? question "32. Which object does VarDumper's VarCloner produce before rendering?"
    **✅ A Data object**

    The cloner captures the variable into an immutable, depth-limited Data object, which a CliDumper or HtmlDumper then renders — separating capture from output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

??? question "33. An uncaught exception that does NOT implement HttpExceptionInterface produces which status code?"
    **✅ 500**

    Only HttpExceptionInterface carries a custom status code; any other throwable defaults to HTTP 500 via the error controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

??? question "34. When does the Web Profiler collect data for a request?"
    **✅ On kernel.response, with late collectors running at kernel.terminate**

    Profiler::collect() runs on kernel.response, invoking each DataCollector; LateDataCollectorInterface::lateCollect() runs later at terminate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler.html)

??? question "35. Which mechanism does Symfony 8 use for translation pluralization?"
    **✅ ICU MessageFormat, e.g. {count, plural, one {…} other {# …}}**

    ICU MessageFormat handles plural/select rules with locale-aware categories (one/few/many/other); the old pipe syntax is legacy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "36. What makes Filesystem::dumpFile() safe against partial reads?"
    **✅ It writes to a temporary file then atomically renames it into place**

    dumpFile() writes to a temp file and renames it, so a reader always sees either the old content or the complete new content, never a half-written file.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html)

??? question "37. Which Finder method defines the directories to search?"
    **✅ in()**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

---

<small>Back to [Flashcards](index.md) · [Miscellaneous](../../miscellaneous/index.md)</small>
