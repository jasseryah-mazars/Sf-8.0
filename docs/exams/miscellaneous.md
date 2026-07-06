# Chapter Exam — Miscellaneous

!!! abstract "How to use"
    96 questions spanning every subchapter of **Miscellaneous**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

Full theory: [Miscellaneous](../miscellaneous/index.md).

---

**Q1.** What does MessageBusInterface::dispatch() return?  <small>_(easy · internals)_</small>

- A. An Envelope
- B. The handler's return value
- C. void
- D. A HandledStamp

??? success "Answer Q1"
    **A**

    dispatch() always returns the (possibly stamped) Envelope. A handler's return value is available via $envelope->last(HandledStamp::class)->getResult(). It never returns the value directly because a routed (async) message is not handled in this process at all — only the Envelope exists yet.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html)

**Q2.** DelayStamp(5000) delays delivery by how long?  <small>_(easy · trap)_</small>

- A. 5000 milliseconds (5 seconds)
- B. 5000 seconds
- C. 5000 microseconds
- D. 5000 minutes

??? success "Answer Q2"
    **A**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds. The classic trap is to read it as seconds; the retry strategy's initial delay is likewise in milliseconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#delaying-messages)

**Q3.** Which attribute marks a service as a message handler in Symfony 8?  <small>_(easy · single)_</small>

- A. #[AsMessageHandler]
- B. #[MessageHandler]
- C. #[AsHandler]
- D. #[Handler]

??? success "Answer Q3"
    **A**

    Symfony\\Component\\Messenger\\Attribute\\AsMessageHandler registers an invokable service (or a specific method) as a handler for its typed message argument. The other names do not exist in the component.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#registering-handlers)

**Q4.** True or False: routing a message to the sync:// transport skips the middleware pipeline.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q4"
    **B**

    False. sync:// still runs the full middleware stack (validation, transactions, handler discovery) — it simply handles the message immediately in the same process instead of enqueueing it. Treating sync:// as "no bus" is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transport-configuration)

**Q5.** Which built-in transport handles a message immediately in the same process, without a queue?  <small>_(easy · single)_</small>

- A. The sync transport (DSN sync://)
- B. The in-memory transport (in-memory://)
- C. The doctrine transport (doctrine://default)
- D. The amqp transport (amqp://...)

??? success "Answer Q5"
    **A**

    sync:// processes the message synchronously during dispatch. in-memory:// keeps messages in memory for tests, while doctrine/amqp/redis are real asynchronous transports consumed by a worker.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transport-configuration)

**Q6.** Which adapter keeps entries only for the current process (ideal for tests)?  <small>_(easy · single)_</small>

- A. ArrayAdapter
- B. FilesystemAdapter
- C. RedisAdapter
- D. ApcuAdapter

??? success "Answer Q6"
    **A**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

**Q7.** Which composer flag excludes require-dev packages when deploying to production?  <small>_(easy · single)_</small>

- A. --no-dev
- B. --prod
- C. --production
- D. --optimize

??? success "Answer Q7"
    **A**

    `composer install --no-dev` skips require-dev packages (profiler, PHPUnit, etc.). Add --optimize-autoloader (or --classmap-authoritative) to build an optimised classmap and cut per-class filesystem stat calls.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q8.** True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q8"
    **B**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q9.** What does Process::run() return?  <small>_(easy · internals)_</small>

- A. The integer exit code
- B. The stdout as a string
- C. void
- D. A boolean success flag

??? success "Answer Q9"
    **A**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

**Q10.** What is the default Process timeout?  <small>_(easy · trap)_</small>

- A. 60 seconds
- B. Unlimited
- C. 30 seconds
- D. 300 seconds

??? success "Answer Q10"
    **A**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#process-timeout)

**Q11.** Which lock store provides mutual exclusion across multiple servers?  <small>_(easy · single)_</small>

- A. RedisStore
- B. FlockStore
- C. SemaphoreStore
- D. InMemoryStore

??? success "Answer Q11"
    **A**

    Flock and Semaphore stores are local to one machine, and InMemoryStore is per-process (tests). Shared stores like Redis (or a database store) coordinate locks across servers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#available-stores)

**Q12.** Which class renders Twig templates into an email body?  <small>_(easy · single)_</small>

- A. Symfony\Bridge\Twig\Mime\TemplatedEmail
- B. Symfony\Component\Mime\Email
- C. Symfony\Component\Mailer\Mailer
- D. Symfony\Component\Mime\Message

??? success "Answer Q12"
    **A**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending. Plain Email has no template support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

**Q13.** Which environment variable selects the runtime class?  <small>_(easy · single)_</small>

- A. APP_RUNTIME
- B. APP_ENV
- C. SYMFONY_RUNTIME
- D. RUNTIME_CLASS

??? success "Answer Q13"
    **A**

    APP_RUNTIME (or composer.json extra.runtime.class) chooses the RuntimeInterface implementation; the default is SymfonyRuntime, which extends GenericRuntime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

**Q14.** Which class does the default SymfonyRuntime extend?  <small>_(easy · single)_</small>

- A. GenericRuntime
- B. HttpKernel
- C. Kernel
- D. SymfonyStyle

??? success "Answer Q14"
    **A**

    SymfonyRuntime extends the framework-agnostic GenericRuntime, adding Symfony-aware resolvers/runners (inject Request, SymfonyStyle, console Input/Output; run a Kernel or console Application). It is not a kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

**Q15.** ClockInterface::now() returns what type?  <small>_(easy · internals)_</small>

- A. A \DateTimeImmutable (a DatePoint)
- B. A Unix timestamp int
- C. A mutable \DateTime
- D. A float of seconds

??? success "Answer Q15"
    **A**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q16.** Which clock lets tests freeze or advance time without a real delay?  <small>_(easy · single)_</small>

- A. MockClock — you set the time and its sleep() advances virtual time
- B. NativeClock
- C. MonotonicClock
- D. SystemClock

??? success "Answer Q16"
    **A**

    MockClock is constructed with a fixed time and its sleep() advances time virtually (no real waiting), perfect for TTL/expiry tests. NativeClock is the real prod clock; MonotonicClock is for durations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html#usage-in-tests)

**Q17.** Which clock is best for measuring elapsed durations and is immune to system clock changes?  <small>_(easy · single)_</small>

- A. MonotonicClock
- B. NativeClock
- C. MockClock
- D. DatePoint

??? success "Answer Q17"
    **A**

    MonotonicClock uses a high-resolution monotonic source unaffected by NTP or manual clock adjustments, so duration diffs stay accurate. Wall-clock NativeClock can jump; MockClock is for tests; DatePoint is a date type, not a clock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q18.** What does dd() do that dump() does not?  <small>_(easy · trap)_</small>

- A. It stops execution (exit) after dumping
- B. It writes the dump to a log file
- C. It serializes the value to JSON
- D. It dumps only scalar values

??? success "Answer Q18"
    **A**

    dd() means 'dump and die': it dumps then calls exit, halting the script. dump() records the variable and lets execution continue (the dump is shown in the toolbar/collector).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html#the-dump-function)

**Q19.** Which serializable object represents a throwable for rendering and logging?  <small>_(easy · single)_</small>

- A. FlattenException
- B. HttpException
- C. ErrorEvent
- D. ExceptionListener

??? success "Answer Q19"
    **A**

    Throwables are normalised into a FlattenException — a serializable snapshot (class, message, status, trace) that error renderers (HTML/JSON/XML) turn into output and that is safe to log. HttpException is a throwable, not the snapshot.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

**Q20.** Which service tag registers a custom data collector (with a toolbar/panel)?  <small>_(easy · single)_</small>

- A. data_collector (with a `template` attribute for the panel)
- B. kernel.collector
- C. profiler.panel
- D. web_profiler.collector

??? success "Answer Q20"
    **A**

    The data_collector tag wires a DataCollectorInterface; supplying a `template` attribute makes its toolbar badge and panel appear. Autoconfigure applies the tag automatically for services implementing the interface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

**Q21.** What does the translator return when a message id has no translation in the active locale or its fallbacks?  <small>_(easy · trap)_</small>

- A. The message id itself (and it is logged in dev)
- B. An empty string
- C. A TranslationException
- D. null

??? success "Answer Q21"
    **A**

    A missing translation returns the untranslated id, not an error or empty string, so the UI degrades gracefully. In dev the miss is logged so you can fix the catalogue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

**Q22.** Which class returns the localized display name of a country code?  <small>_(easy · single)_</small>

- A. Symfony\Component\Intl\Countries (Countries::getName('FR'))
- B. Symfony\Component\Locale\Country
- C. Symfony\Component\Translation\Countries
- D. Symfony\Component\Intl\Locale

??? success "Answer Q22"
    **A**

    Countries::getName() reads the bundled ICU dataset and returns the name in the current/requested locale. Related classes are Languages, Locales, Currencies and Timezones. The other namespaces do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/intl.html)

**Q23.** Which Finder method defines the directories to search?  <small>_(easy · single)_</small>

- A. in()
- B. from()
- C. search()
- D. path()

??? success "Answer Q23"
    **A**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

**Q24.** A message is routed to an async transport. During dispatch() in the web process, the handler…  <small>_(medium · internals)_</small>

- A. does not run — SendMessageMiddleware serializes and sends it, stopping the bus
- B. runs immediately and is also queued
- C. runs only if a worker is currently active
- D. throws NoHandlerForMessageException

??? success "Answer Q24"
    **A**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later. It is not handled twice, and a running worker is irrelevant to the dispatching process. NoHandlerForMessageException only occurs when no handler exists for a synchronously handled message.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages)

**Q25.** After a message exhausts its configured retries, where does it go?  <small>_(medium · single)_</small>

- A. To the configured failure transport
- B. To the sync transport
- C. It is silently discarded
- D. Back to the front of the same queue forever

??? success "Answer Q25"
    **A**

    Once max_retries is reached the envelope is sent to the failure_transport, where messenger:failed:show/retry can inspect and requeue it. Without a failure transport the message would be lost, which is why configuring one is a best practice.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#saving-retrying-failed-messages)

**Q26.** Which middleware locates and invokes the handler(s), adding a HandledStamp?  <small>_(medium · internals)_</small>

- A. HandleMessageMiddleware
- B. SendMessageMiddleware
- C. DispatchAfterCurrentBusMiddleware
- D. ValidationMiddleware

??? success "Answer Q26"
    **A**

    HandleMessageMiddleware resolves handlers for the message type, calls them, and records each result in a HandledStamp. SendMessageMiddleware only routes/sends to transports (and may stop the bus before Handle runs).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#middleware)

**Q27.** How do you make a failing handler skip retries and go straight to the failure transport?  <small>_(medium · scenario)_</small>

- A. Throw UnrecoverableMessageHandlingException
- B. Return false from the handler
- C. Add a DelayStamp(0)
- D. Call $envelope->stopPropagation()

??? success "Answer Q27"
    **A**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately. A handler's return value never influences retries, and there is no stopPropagation() on an Envelope.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

**Q28.** A dispatched message throws NoHandlerForMessageException. What is the most likely cause?  <small>_(medium · debug)_</small>

- A. The handler class is missing #[AsMessageHandler] (or its __invoke argument type does not match the message)
- B. The worker is not running
- C. The failure transport is not configured
- D. The message is not readonly

??? success "Answer Q28"
    **A**

    Handlers are discovered by autoconfiguration of the #[AsMessageHandler] attribute and matched by the typed argument of __invoke(). Missing the attribute (or a mismatched/imported type) means no handler is registered. Worker state, failure transport and message immutability are unrelated to handler resolution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#registering-handlers)

**Q29.** During messenger:consume, which event is dispatched when a handler throws an exception?  <small>_(medium · internals)_</small>

- A. WorkerMessageFailedEvent
- B. WorkerMessageHandledEvent
- C. WorkerStoppedEvent
- D. WorkerRunningEvent

??? success "Answer Q29"
    **A**

    The worker loop dispatches WorkerMessageReceivedEvent, then on success WorkerMessageHandledEvent (ack) or on exception WorkerMessageFailedEvent (reject/retry). WorkerRunningEvent fires between receives and WorkerStoppedEvent on shutdown — neither signals a handler failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-events)

**Q30.** An order handler dispatches an 'order confirmed' email message, but the email is sent even when the surrounding DB transaction rolls back. What fixes this?  <small>_(medium · scenario)_</small>

- A. Dispatch the email message with DispatchAfterCurrentBusStamp so it is delivered only after the current handler finishes successfully
- B. Add a DelayStamp so the email is sent 5 seconds later
- C. Throw UnrecoverableMessageHandlingException in the email handler
- D. Route the email to the sync:// transport

??? success "Answer Q30"
    **A**

    DispatchAfterCurrentBusStamp defers the inner dispatch until the current message finishes handling successfully, so a rollback cancels the email. A delay only postpones sending, the unrecoverable exception affects the email's own retries, and sync routing would send it immediately during the transaction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/dispatch_after_current_bus.html)

**Q31.** After a deploy, long-running workers keep executing the old code. Which approach fixes this for zero-downtime deploys?  <small>_(medium · scenario)_</small>

- A. Run messenger:stop-workers on deploy and let a supervisor restart workers, ideally combined with --time-limit/--memory-limit
- B. Restart the database so workers reconnect with new code
- C. Add a DelayStamp to every message
- D. Increase max_retries so old workers eventually give up

??? success "Answer Q31"
    **A**

    Workers bootstrap the kernel once and keep it in memory, so new code is only picked up after a restart. messenger:stop-workers signals running workers to finish the current message and exit; a process manager then restarts them with the new code. --time-limit/--memory-limit make them recycle regularly. The other options don't reload the worker's code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

**Q32.** How do you retrieve a synchronous handler's return value after MessageBusInterface::dispatch()?  <small>_(medium · code)_</small>

- A. $envelope->last(HandledStamp::class)->getResult()
- B. The value is returned directly by dispatch()
- C. $envelope->getResult()
- D. $bus->getLastResult()

??? success "Answer Q32"
    **A**

    dispatch() returns an Envelope. For a single sync handler you read its result via the HandledStamp: $envelope->last(HandledStamp::class)->getResult(). Use HandleTrait to unwrap it in a query bus. Envelope has no getResult() and the bus does not cache a "last result".

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

**Q33.** What information does a RedeliveryStamp carry on a retried message?  <small>_(medium · internals)_</small>

- A. The current retry count (and timing), so the retry strategy knows how many attempts have happened
- B. The DSN of the failure transport
- C. The fully-qualified class name of the handler that failed
- D. A cryptographic signature of the payload

??? success "Answer Q33"
    **A**

    RedeliveryStamp records the retry count (and redelivery timestamp). The worker reads it to compare against max_retries and to compute the next delay via the retry strategy. Handler identity is on HandlerFailedStamp, not here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

**Q34.** In framework.messenger.routing, mapping App\Message\SmsNotification to 'async' means…  <small>_(medium · config)_</small>

- A. SendMessageMiddleware sends that message class to the 'async' transport instead of handling it in-process
- B. The handler is renamed to 'async'
- C. The message is handled by every transport named async
- D. It only affects messages dispatched from the CLI

??? success "Answer Q34"
    **A**

    routing maps a message class (or interface/parent) to one or more transport names. A routed message is serialized and sent to that transport rather than handled synchronously. A message with no routing entry is handled immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#routing-messages-to-a-transport)

**Q35.** Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?  <small>_(medium · scenario)_</small>

- A. --limit (max messages) and --time-limit (max seconds), optionally with memory limits
- B. --kill and --restart
- C. --stop-now only
- D. --reload after each message

??? success "Answer Q35"
    **A**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#deploying-to-production)

**Q36.** Under a transport's retry_strategy, what does the 'multiplier' option control?  <small>_(medium · config)_</small>

- A. The factor by which the delay grows between successive retries (exponential backoff)
- B. The number of parallel workers spawned
- C. How many transports share the message
- D. The maximum number of messages fetched per poll

??? success "Answer Q36"
    **A**

    retry_strategy defines max_retries, delay (initial, ms), multiplier (delay is multiplied by this each attempt) and max_delay to cap it, producing exponential backoff before the failure transport is used.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

**Q37.** Which transport is intended specifically for functional tests, asserting dispatched messages without a broker?  <small>_(medium · single)_</small>

- A. The in-memory transport (in-memory://), inspected via getSent()
- B. The sync transport (sync://)
- C. The redis transport (redis://localhost)
- D. The doctrine transport

??? success "Answer Q37"
    **A**

    in-memory:// keeps envelopes in memory instead of sending them, so a test can fetch the transport from the container and assert on getSent(). It is reset between tests via the messenger reset behaviour.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#testing)

**Q38.** Symfony\Contracts\Cache\CacheInterface::get() runs its callback…  <small>_(medium · internals)_</small>

- A. only on a cache miss, then stores and returns the value
- B. on every call
- C. never — you must call save() yourself
- D. only when the beta factor is INF

??? success "Answer Q38"
    **A**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection. Running on every call would defeat caching, and unlike PSR-6 you do not call save() manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q39.** A pool is declared with `tags: true` in cache.yaml. What does this enable?  <small>_(medium · config)_</small>

- A. Tagging items with $item->tag([...]) and evicting groups via invalidateTags([...])
- B. Automatic compression of cached values
- C. Sharing the pool across all servers
- D. Disabling stampede protection

??? success "Answer Q39"
    **A**

    `tags: true` wraps the pool in a TagAwareAdapter implementing TagAwareCacheInterface, so items can carry tags and invalidateTags() evicts all items with a given tag — invalidation by concern rather than by key. Calling $item->tag() on a non-tag-aware pool errors.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#using-cache-tags)

**Q40.** True or False: passing $beta = INF to CacheInterface::get() forces the value to be recomputed immediately.  <small>_(medium · true-false)_</small>

- A. True
- B. False

??? success "Answer Q40"
    **A**

    True. $beta = INF forces early expiration, so the callback runs and the value is refreshed on this call. $beta = 0 disables early expiration entirely; the default (null) picks a sensible probabilistic value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

**Q41.** Using the raw PSR-6 API, how do you distinguish a stored null value from a missing key?  <small>_(medium · internals)_</small>

- A. Check $item->isHit() — get() returns null for both cases
- B. Compare $item->get() to null
- C. Call $pool->hasKey($key)
- D. Catch a CacheMissException

??? success "Answer Q41"
    **A**

    With PSR-6, CacheItemInterface::get() returns null both for an absent key and for a genuinely stored null, so you must call isHit() to tell them apart. The contracts callback API sidesteps this ambiguity; there is no hasKey() or miss exception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

**Q42.** In serialize(), which stage runs first?  <small>_(medium · internals)_</small>

- A. The normalizer (object to array), then the encoder (array to string)
- B. The encoder, then the normalizer
- C. Only the encoder runs
- D. They run concurrently

??? success "Answer Q42"
    **A**

    serialize() normalizes the object to an array/scalars, then encodes that to a string. deserialize() reverses it: decode then denormalize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/serializer.html)

**Q43.** #[Groups(['read'])] on a property takes effect when…  <small>_(medium · trap)_</small>

- A. the context includes ['groups' => ['read']]
- B. always, regardless of context
- C. only during deserialization
- D. the property is public

??? success "Answer Q43"
    **A**

    Group filtering only applies when matching groups are passed in the context; otherwise the group attribute has no effect and all fields are (de)serialized.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

**Q44.** Which normalizer reads and writes private properties directly via reflection?  <small>_(medium · single)_</small>

- A. PropertyNormalizer
- B. ObjectNormalizer
- C. GetSetMethodNormalizer
- D. JsonEncoder

??? success "Answer Q44"
    **A**

    PropertyNormalizer accesses object properties directly (including private), whereas ObjectNormalizer uses accessors and the constructor, and GetSetMethodNormalizer uses only get/set methods. JsonEncoder is an encoder, not a normalizer.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

**Q45.** What does the framework.serializer.default_context option skip_null_values: true do?  <small>_(medium · config)_</small>

- A. Omits properties whose value is null from the serialized output
- B. Throws when a property is null
- C. Converts null to an empty string
- D. Only affects deserialization of missing keys

??? success "Answer Q45"
    **A**

    By default a null property is serialized as \"key\":null. Setting AbstractObjectNormalizer::SKIP_NULL_VALUES (skip_null_values) omits those keys from the payload. The classic bug is a consumer treating an absent key as an error rather than 'the value was null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html)

**Q46.** A private property with no getter is missing from the JSON produced by the default ObjectNormalizer. Why, and how do you fix it?  <small>_(medium · debug)_</small>

- A. ObjectNormalizer uses accessors; add a getter (or use PropertyNormalizer, which reads properties directly)
- B. The property must be marked #[Groups] to appear
- C. You must call serialize() with the 'private' => true context
- D. Private properties can never be serialized in Symfony 8

??? success "Answer Q46"
    **A**

    ObjectNormalizer reads via getters/issers/hassers and the constructor, so a private property without an accessor is invisible. Provide a getter or switch to PropertyNormalizer, which uses reflection to read properties directly. Groups filter fields but do not expose accessorless private properties.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

**Q47.** In which environment is .env.local NOT loaded?  <small>_(medium · trap)_</small>

- A. test
- B. dev
- C. prod
- D. staging

??? success "Answer Q47"
    **A**

    .env.local is intentionally skipped in the test environment so tests run from committed defaults and stay reproducible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#selecting-the-active-environment)

**Q48.** What does `composer dump-env prod` produce, and what is the effect?  <small>_(medium · config)_</small>

- A. .env.local.php — Symfony loads it directly and skips parsing .env* files
- B. .env.prod — parsed on every request
- C. config/prod.php overriding all bundles
- D. Nothing; it only validates env vars

??? success "Answer Q48"
    **A**

    The whole .env* cascade is compiled to a plain PHP array in .env.local.php, which Symfony loads directly, avoiding DotEnv parsing on each request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production)

**Q49.** ExpressionLanguage::compile() returns what?  <small>_(medium · internals)_</small>

- A. A string of PHP source code
- B. The evaluated result value
- C. An AST node object
- D. A boolean success flag

??? success "Answer Q49"
    **A**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q50.** A .env file sets DATABASE_URL, but a real OS environment variable DATABASE_URL is also exported. Which wins?  <small>_(medium · trap)_</small>

- A. The real OS environment variable — DotEnv never overrides an existing real env var
- B. .env, because it is loaded last
- C. Whichever value is longer
- D. They are concatenated

??? success "Answer Q50"
    **A**

    Real OS environment variables always take precedence; the DotEnv cascade (.env → .env.local → .env.<env> → .env.<env>.local) only fills values not already set in the real environment. Later .env* files override earlier ones but never a real env var.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#overriding-environment-values-via-env-local)

**Q51.** Which class merges every config source and validates it against a bundle's Configuration tree?  <small>_(medium · internals)_</small>

- A. Processor (Processor::processConfiguration())
- B. TreeBuilder
- C. FileLocator
- D. ContainerBuilder

??? success "Answer Q51"
    **A**

    Processor::processConfiguration() merges all sources and validates them against the tree returned by the Configuration class, applying defaults and constraints. TreeBuilder only defines the schema; FileLocator finds files.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/config/definition.html)

**Q52.** You changed a YAML config file and redeployed to prod, but the change has no effect. Why?  <small>_(medium · trap)_</small>

- A. Prod loads the compiled container as-is and does not auto-detect config changes; you must clear/warm the cache on deploy
- B. Prod re-reads YAML on every request, so a restart is needed
- C. YAML config is ignored in prod; only PHP config works
- D. APP_DEBUG must be 1 for config to reload

??? success "Answer Q52"
    **A**

    In prod the compiled container in var/cache/prod is loaded as-is with no freshness checks (those exist only in debug), so config changes require cache:clear + cache:warmup on deploy. Enabling APP_DEBUG in prod is unsafe and not the fix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q53.** Why set opcache.validate_timestamps=0 in production?  <small>_(medium · config)_</small>

- A. To skip per-request file-modification checks and always serve cached bytecode (reset opcache on deploy instead)
- B. To enable debug mode
- C. To disable opcache entirely
- D. To force recompilation on every request

??? success "Answer Q53"
    **A**

    With immutable deploys, disabling timestamp validation maximises opcache hits by not stat-ing files each request. Because opcache then never notices new files, you must reset opcache (or the PHP process manager) on each deploy so the new bytecode is loaded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/performance.html)

**Q54.** Which ordered command sequence is correct for a from-scratch prod deploy?  <small>_(medium · scenario)_</small>

- A. composer install --no-dev --optimize-autoloader → composer dump-env prod → cache:clear → cache:warmup → reset opcache
- B. cache:warmup → composer install → dump-env prod → go live
- C. composer update → APP_DEBUG=1 → cache:clear
- D. cache:clear → composer install --dev → dump-env dev

??? success "Answer Q54"
    **A**

    You install prod deps first, compile the env cascade with dump-env prod, then clear and warm the cache so the first live request is fast, and finally reset opcache. Warming before installing, or shipping dev deps / APP_DEBUG=1, are wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q55.** Which Process constructor auto-escapes each argument?  <small>_(medium · trap)_</small>

- A. new Process(['git', 'log', '--oneline'])
- B. Process::fromShellCommandline('git log --oneline')
- C. Both escape equally
- D. Neither escapes anything

??? success "Answer Q55"
    **A**

    The array form escapes each element automatically. fromShellCommandline() runs a raw shell string and does not escape, risking command injection if you interpolate untrusted input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

**Q56.** You build a command from user input using Process::fromShellCommandline('convert '.$userInput). What is the risk and the fix?  <small>_(medium · debug)_</small>

- A. Command injection — use the array constructor new Process(['convert', $userInput]) so each argument is auto-escaped
- B. None; fromShellCommandline escapes arguments for you
- C. A timeout error; raise setTimeout()
- D. It only fails on Windows; add a shebang

??? success "Answer Q56"
    **A**

    fromShellCommandline runs the string through /bin/sh with no escaping, so untrusted input can inject shell metacharacters. The array constructor escapes each element as a single argument, eliminating the injection vector. This is unrelated to timeouts or platform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

**Q57.** Which call runs a process and throws automatically on a non-zero exit code?  <small>_(medium · code)_</small>

- A. mustRun() — it throws ProcessFailedException on failure
- B. run() — it throws ProcessFailedException on failure
- C. start() — it throws immediately on failure
- D. wait() — it converts the exit code into an exception

??? success "Answer Q57"
    **A**

    mustRun() behaves like run() but throws ProcessFailedException when the process exits non-zero. run() simply returns the integer exit code and you check isSuccessful() yourself; start()/wait() are for async execution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

**Q58.** LockInterface::acquire() called with no argument is…  <small>_(medium · trap)_</small>

- A. non-blocking — it returns false immediately if the lock is held
- B. blocking — it waits until the lock is free
- C. throwing an exception if the lock is held
- D. always successful

??? success "Answer Q58"
    **A**

    acquire() defaults to non-blocking; pass true to block until the resource becomes available (store permitting). It returns a boolean false when held, it does not throw, so `if (!$lock->acquire()) { return; }` is the correct guard.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html#blocking-locks)

**Q59.** Why call refresh() during a long critical section?  <small>_(medium · scenario)_</small>

- A. To extend the lock's TTL so it is not considered expired mid-job
- B. To release then reacquire the lock
- C. To switch to a different store
- D. To convert it to a shared lock

??? success "Answer Q59"
    **A**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity; without it another process could acquire the lock after the TTL, breaking mutual exclusion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

**Q60.** Which is the correct guard to skip work another process is already doing?  <small>_(medium · code)_</small>

- A. if (!$lock->acquire()) { return; }
- B. try { $lock->acquire(); } catch (LockConflictedException) { return; }
- C. if ($lock->acquire() === null) { return; }
- D. if ($lock->isLocked()) { return; }

??? success "Answer Q60"
    **A**

    Non-blocking acquire() returns false when the resource is held, so !$lock->acquire() is the idiomatic early-return guard. It does not return null and does not throw on contention (only blocking acquire(true) may throw LockConflictedException). Forgetting to check the boolean means entering the critical section unprotected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html)

**Q61.** What is the default TTL of a lock created via LockFactory::createLock($resource)?  <small>_(medium · internals)_</small>

- A. 300 seconds (5 minutes), with autoRelease on by default
- B. 60 seconds
- C. Unlimited (no TTL)
- D. 30 seconds

??? success "Answer Q61"
    **A**

    createLock(string $resource, ?float $ttl = 300.0, bool $autoRelease = true) defaults to a 300 second TTL and releases the lock when the Lock object is destroyed. Long jobs should raise the TTL and call refresh() to avoid premature expiry.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

**Q62.** With Messenger routing configured for emails, MailerInterface::send() will…  <small>_(medium · scenario)_</small>

- A. dispatch a SendEmailMessage to be delivered by a worker
- B. always send synchronously over SMTP
- C. throw if no worker is running
- D. render but not send the email

??? success "Answer Q62"
    **A**

    When SendEmailMessage is routed to a transport, send() enqueues it; a worker delivers it later, giving async sending plus retries. It does not throw if a worker is down — the message just waits in the queue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

**Q63.** How is an inline (embedded) image referenced from an email's HTML body?  <small>_(medium · single)_</small>

- A. Via a cid: reference produced by embed()/embedFromPath()
- B. Only as an absolute external URL
- C. As a base64 data: URI hand-written by the developer
- D. Inline images are not supported

??? success "Answer Q63"
    **A**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

**Q64.** Which configuration makes emails send asynchronously via Messenger?  <small>_(medium · config)_</small>

- A. Route Symfony\Component\Mailer\Messenger\SendEmailMessage to a transport in messenger routing (and run a worker)
- B. Set MAILER_DSN to async://default
- C. Add async: true under framework.mailer
- D. Wrap send() in a try/catch

??? success "Answer Q64"
    **A**

    Async delivery comes from routing SendEmailMessage to a Messenger transport and consuming it with a worker. MAILER_DSN chooses the delivery transport (SMTP/API), not sync-vs-async, and there is no framework.mailer.async flag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

**Q65.** What does public/index.php return under the Runtime component?  <small>_(medium · internals)_</small>

- A. A callable that produces the application object (e.g. a Kernel)
- B. A Response object
- C. Nothing — it echoes the output directly
- D. The exit code as an int

??? success "Answer Q65"
    **A**

    index.php returns a callable; autoload_runtime.php resolves its arguments, invokes it, then a RunnerInterface handles/sends/terminates. It never calls handle() itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

**Q66.** True or False: you should guard ClockInterface::now() with a nullsafe operator because it may return null with a frozen MockClock.  <small>_(medium · trap)_</small>

- A. False
- B. True

??? success "Answer Q66"
    **A**

    False. now() is typed : \\DateTimeImmutable and always returns a DatePoint, even with a frozen MockClock, so ?-> is unnecessary. The real bug is comparing a MockClock time against a live new \\DateTime() — read time from the clock on both sides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q67.** Which object does VarDumper's VarCloner produce before rendering?  <small>_(medium · internals)_</small>

- A. A Data object
- B. A Response
- C. A FlattenException
- D. A StopwatchEvent

??? success "Answer Q67"
    **A**

    The cloner captures the variable into an immutable, depth-limited Data object, which a CliDumper or HtmlDumper then renders — separating capture from output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

**Q68.** What unit does StopwatchEvent::getDuration() use, and when is the debug.stopwatch service available?  <small>_(medium · internals)_</small>

- A. Milliseconds; the service exists only when debug/the profiler is enabled
- B. Seconds; always available in every environment
- C. Microseconds; only in prod
- D. Nanoseconds; only in tests

??? success "Answer Q68"
    **A**

    getDuration() returns milliseconds, and the autowirable debug.stopwatch service is only registered in debug (dev/test). Injecting Stopwatch in prod therefore causes a wiring error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

**Q69.** A service that autowires Symfony\Component\Stopwatch\Stopwatch works in dev but fails to boot in prod. Why?  <small>_(medium · debug)_</small>

- A. The debug.stopwatch service exists only in debug mode, so the dependency is missing in prod
- B. Stopwatch requires the profiler bundle in prod
- C. getDuration() throws in prod
- D. Autowiring is disabled in prod

??? success "Answer Q69"
    **A**

    Stopwatch's framework service is registered only when debug is enabled, so in prod there is nothing to inject and the container fails. Use it for ad-hoc dev profiling only; for prod metrics use real observability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

**Q70.** An uncaught exception that does NOT implement HttpExceptionInterface produces which status code?  <small>_(medium · trap)_</small>

- A. 500
- B. 404
- C. 400
- D. 200

??? success "Answer Q70"
    **A**

    Only HttpExceptionInterface carries a custom status code; any other throwable defaults to HTTP 500 via the error controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q71.** What does the ErrorHandler component do with a PHP warning or notice?  <small>_(medium · internals)_</small>

- A. Converts it into a catchable \ErrorException via set_error_handler()
- B. Silently ignores it
- C. Writes it directly into the response body
- D. Converts it into an HttpException

??? success "Answer Q71"
    **A**

    ErrorHandler registers set_error_handler() to throw \\ErrorException for PHP errors (warnings, notices, fatals via a shutdown function), making them catchable. It does not turn them into HttpExceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

**Q72.** In a controller, which throw produces a 404 rendered by the framework error controller?  <small>_(medium · scenario)_</small>

- A. throw new NotFoundHttpException('...') — it implements HttpExceptionInterface with status 404
- B. return new Response('', 404) is required; exceptions always give 500
- C. throw new \RuntimeException('not found')
- D. throw new \InvalidArgumentException('404')

??? success "Answer Q72"
    **A**

    NotFoundHttpException implements HttpExceptionInterface, so the error controller maps it to 404 via getStatusCode(). A plain \\RuntimeException or \\InvalidArgumentException does not carry a status and becomes 500. You do not need to build the Response manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q73.** When does the Web Profiler collect data for a request?  <small>_(medium · internals)_</small>

- A. On kernel.response, with late collectors running at kernel.terminate
- B. On kernel.request only
- C. During container compilation
- D. Only in the CLI

??? success "Answer Q73"
    **A**

    Profiler::collect() runs on kernel.response, invoking each DataCollector; LateDataCollectorInterface::lateCollect() runs later at terminate for data not complete during the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler.html)

**Q74.** A custom collector storing a PDO connection in $this->data breaks profile storage. Why?  <small>_(medium · debug)_</small>

- A. $this->data is serialized to storage (via VarDumper's cloner); a live connection/resource is not serializable
- B. PDO is banned from all services
- C. Collectors may only store strings
- D. The data_collector tag rejects objects

??? success "Answer Q74"
    **A**

    Profiles are persisted per token, so $this->data must be serializable — store scalar/array (VarDumper-clonable) data, not live resources like a PDO connection or an entity with a connection. Implement reset() for worker reuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

**Q75.** Which mechanism does Symfony 8 use for translation pluralization?  <small>_(medium · single)_</small>

- A. ICU MessageFormat, e.g. {count, plural, one {…} other {# …}}
- B. The singular|plural pipe syntax
- C. A %count% placeholder only
- D. Separate keys per number

??? success "Answer Q75"
    **A**

    ICU MessageFormat handles plural/select rules with locale-aware categories (one/few/many/other); the old pipe syntax is legacy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

**Q76.** What is the default translation domain, and what file naming applies ICU formatting?  <small>_(medium · config)_</small>

- A. Default domain is messages; the +intl-icu suffix (messages+intl-icu.<locale>.yaml) enables ICU formatting
- B. Default domain is default; ICU is always applied to every file
- C. Default domain is translations; ICU needs a .icu extension
- D. There is no default domain; you must always pass one

??? success "Answer Q76"
    **A**

    When no domain is passed, trans() uses messages; validators and security are separate domains. ICU MessageFormat is applied to catalogues named with the +intl-icu suffix — forgetting it means ICU rules are not parsed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

**Q77.** What makes Filesystem::dumpFile() safe against partial reads?  <small>_(medium · internals)_</small>

- A. It writes to a temporary file then atomically renames it into place
- B. It acquires an flock on the file
- C. It compresses the content
- D. It buffers writes in memory forever

??? success "Answer Q77"
    **A**

    dumpFile() writes to a temp file and renames it, so a reader always sees either the old content or the complete new content, never a half-written file. appendToFile(), by contrast, is not atomic.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html)

**Q78.** How does Symfony\Component\Filesystem\Filesystem signal a failed operation (e.g. copy())?  <small>_(medium · trap)_</small>

- A. It throws an IOExceptionInterface (it does not return false)
- B. It returns false, like the native PHP functions
- C. It returns null
- D. It triggers a PHP warning only

??? success "Answer Q78"
    **A**

    Unlike native file functions that return false, Filesystem methods throw IOExceptionInterface on failure, so errors cannot be silently ignored. Also note Path helpers manipulate path strings only and never touch the disk.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html#error-handling)

**Q79.** A Finder query returns directories as well as files. What is missing?  <small>_(medium · debug)_</small>

- A. A ->files() call — without files() or directories() the Finder yields both
- B. A ->name() filter — name() restricts to files
- C. A ->in() call — in() excludes directories
- D. Nothing; Finder always returns files only

??? success "Answer Q79"
    **A**

    Finder yields both files and directories unless you narrow it with files() (or directories()). name()/in() do not restrict the entry type. Iterated results are Finder SplFileInfo objects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

**Q80.** What is the purpose of DispatchAfterCurrentBusStamp?  <small>_(hard · internals)_</small>

- A. Defer delivery of a message dispatched inside a handler until the current handling finishes successfully
- B. Send the message to every bus in the application
- C. Add a delay equal to the current bus latency
- D. Retry the message on the next bus in a chain

??? success "Answer Q80"
    **A**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them. It has nothing to do with delays, multi-bus fan-out, or retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/dispatch_after_current_bus.html)

**Q81.** Which statements about Messenger buses are correct? (choose 2)  <small>_(hard · multiple)_</small>

- A. The default bus service is messenger.bus.default
- B. You can define multiple buses, each with its own ordered middleware list
- C. All buses in an app must share a single global middleware list
- D. The command/query/event bus split is enforced by the component

??? success "Answer Q81"
    **A, B**

    Messenger ships one default bus (messenger.bus.default) but supports many, each configured with its own middleware — so a command bus can wrap handlers in a transaction while an event bus does not. The command/query/ event convention is just that: a convention, not enforced by the code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger/multiple_buses.html)

**Q82.** With retry_strategy delay: 1000 and multiplier: 2, what are the delays before the 1st, 2nd and 3rd retry?  <small>_(hard · config)_</small>

- A. 1000 ms, 2000 ms, 4000 ms (delay × multiplier per attempt)
- B. 1000 ms, 1000 ms, 1000 ms (constant)
- C. 2000 ms, 4000 ms, 8000 ms
- D. 1 s, 2 s, 3 s (linear)

??? success "Answer Q82"
    **A**

    MultiplierRetryStrategy multiplies the initial delay by the multiplier for each successive attempt: 1000, 1000×2=2000, 2000×2=4000 (capped by max_delay if set). It is exponential, not constant or linear, and starts at the configured delay, not delay×multiplier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#retries-failures)

**Q83.** $envelope->last(HandledStamp::class) returns null. Which situation explains this best?  <small>_(hard · trap)_</small>

- A. The message was routed to an async transport, so it has not been handled in this process yet
- B. The handler returned null, so no HandledStamp was created
- C. dispatch() failed and returned null instead of an Envelope
- D. HandledStamp only exists on the query bus

??? success "Answer Q83"
    **A**

    A handler that returns null still produces a HandledStamp (its result is null) — so last() returning null means no such stamp exists, i.e. the message was sent async and not handled here. dispatch() always returns an Envelope (never null), and HandledStamp is not query-bus-specific. This is why the nullsafe ?-> guards 'not handled here', distinct from 'handled, returned null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#messenger-getting-handler-results)

**Q84.** Which serializer does a Messenger transport use by default to serialize the envelope?  <small>_(hard · single)_</small>

- A. PhpSerializer (native PHP serialize())
- B. The Symfony Serializer component
- C. JsonEncoder
- D. igbinary

??? success "Answer Q84"
    **A**

    By default transports use Transport\\Serialization\\PhpSerializer, which calls PHP's serialize(). The Symfony Serializer transport serializer is opt-in and recommended for cross-language/cross-app interop, but it is not the default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#serializing-messages)

**Q85.** In a custom middleware, code placed AFTER the $stack->next()->handle($envelope, $stack) call runs…  <small>_(hard · internals)_</small>

- A. On the way out — after the inner middleware and the handler have executed
- B. Never — the call terminates the middleware
- C. Before any other middleware in the stack
- D. Only if the message was routed async

??? success "Answer Q85"
    **A**

    The middleware stack is a russian-doll chain: code before $stack->next()->handle() runs on the way in, and code after it runs on the way out once the rest of the pipeline (including the handler) has returned. This lets a middleware wrap the whole handling (e.g. open/commit a transaction).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#creating-your-own-middleware)

**Q86.** Inside a custom middleware, how do you pass the envelope on to the rest of the stack?  <small>_(hard · code)_</small>

- A. return $stack->next()->handle($envelope, $stack);
- B. return $this->bus->dispatch($envelope);
- C. return $stack->handle($envelope);
- D. $envelope->next();

??? success "Answer Q86"
    **A**

    A MiddlewareInterface::handle() implementation calls $stack->next()->handle($envelope, $stack) to invoke the next middleware. Code before that call runs on the way in; code after it runs on the way out. Re-dispatching via the bus would restart the whole pipeline.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/messenger.html#creating-your-own-middleware)

**Q87.** Which statement about PSR-6 vs PSR-16 is correct?  <small>_(hard · trap)_</small>

- A. PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not
- B. PSR-16 supports tags but PSR-6 does not
- C. Both are identical key/value APIs
- D. PSR-6 has no expiration support

??? success "Answer Q87"
    **A**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

**Q88.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(hard · internals)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q88"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

**Q89.** Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?  <small>_(hard · trap)_</small>

- A. null is returned as a cache hit; the callback is NOT run again
- B. The callback runs again because null means a miss
- C. A CacheException is thrown for storing null
- D. The item is deleted automatically

??? success "Answer Q89"
    **A**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q90.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(hard · trap)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q90"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

**Q91.** A UserDto has #[Groups(['read'])] #[SerializedName('full_name')] on $name and #[Ignore] on $passwordHash. What is the JSON when serialized with context ['groups' => ['read']]?  <small>_(hard · code)_</small>

- A. {"full_name":"..."} plus any other read-group fields; passwordHash is omitted
- B. {"name":"...","passwordHash":"..."}
- C. All properties, because groups are ignored during serialization
- D. An empty object, because #[Ignore] hides everything

??? success "Answer Q91"
    **A**

    With the read group in context, only read-group properties are emitted; $name is renamed to full_name by #[SerializedName], and #[Ignore] drops passwordHash entirely regardless of group. Groups are honoured only because they are passed in the context.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

**Q92.** What is the result of ExpressionLanguage::compile('1 + a', ['a'])?  <small>_(hard · code)_</small>

- A. The PHP source string "(1 + $a)"
- B. The integer 1
- C. A closure you can invoke
- D. An exception, because $a is undefined

??? success "Answer Q92"
    **A**

    compile() emits PHP source, turning the variable name a into $a: "(1 + $a)". It does not evaluate anything (so no undefined-variable error) — use evaluate('1 + a', ['a' => 5]) to get the value 6.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q93.** What does `cache:clear` run, by default, in addition to removing stale cache?  <small>_(hard · internals)_</small>

- A. The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata
- B. The database migrations
- C. The Messenger workers
- D. composer install

??? success "Answer Q93"
    **A**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q94.** In the Mailer, how does the Envelope differ from the message headers?  <small>_(hard · internals)_</small>

- A. The Envelope holds the actual sender/recipients used for the SMTP conversation; headers (From/To) render in the visible message
- B. They are the same object with two names
- C. The Envelope stores the HTML body; headers store attachments
- D. The Envelope is only used for async delivery

??? success "Answer Q94"
    **A**

    Mailer's Envelope (sender + recipients) drives the transport's SMTP exchange, whereas the message headers (From, To, Subject) are what the recipient sees. They can legitimately differ (e.g. bounce address vs visible From), which is a common exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages)

**Q95.** How does the argument `array $context` in the index.php closure get populated?  <small>_(hard · internals)_</small>

- A. The runtime's resolver autowires it from $_SERVER (env vars like APP_ENV/APP_DEBUG)
- B. You must call getenv() yourself inside the closure
- C. Symfony injects it from services.yaml parameters
- D. It is always an empty array in Symfony 8

??? success "Answer Q95"
    **A**

    RuntimeInterface::getResolver() builds a resolver that inspects the callable's typed arguments and supplies them — array $context comes from $_SERVER (env), and it can also inject Request, InputInterface, etc. You therefore never read $_SERVER manually in the entry point.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

**Q96.** Your metric is only complete after the response is sent. Which interface should the collector implement?  <small>_(hard · internals)_</small>

- A. LateDataCollectorInterface (its lateCollect() runs at kernel.terminate)
- B. DataCollectorInterface only; collect() runs after terminate
- C. EventSubscriberInterface on kernel.request
- D. CacheWarmerInterface

??? success "Answer Q96"
    **A**

    Normal collect() runs on kernel.response, too early for post-response data (final dumps, cache calls). LateDataCollectorInterface::lateCollect() runs later at terminate, when that data is complete.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

---

<small>Back to [Chapter Exams](index.md) · [Miscellaneous](../miscellaneous/index.md)</small>
