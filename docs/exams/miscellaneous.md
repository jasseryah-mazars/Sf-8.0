# Chapter Exam — Miscellaneous

!!! abstract "How to use"
    79 questions spanning every subchapter of **Miscellaneous**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Miscellaneous](../miscellaneous/index.md).

---

**Q1.** Which adapter keeps entries only for the current process (ideal for tests)?  <small>_(easy · single)_</small>

- A. ArrayAdapter
- B. FilesystemAdapter
- C. RedisAdapter
- D. ApcuAdapter

??? success "Answer Q1"
    **A**

    ArrayAdapter stores items in memory for the current request/process only, so nothing persists across requests — useful for deterministic tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache/adapters/memcached_adapter.html)

**Q2.** Which composer flag excludes require-dev packages when deploying to production?  <small>_(easy · single)_</small>

- A. --no-dev
- B. --prod
- C. --production
- D. --optimize

??? success "Answer Q2"
    **A**

    `composer install --no-dev` skips require-dev packages (profiler, PHPUnit, etc.). Add --optimize-autoloader (or --classmap-authoritative) to build an optimised classmap and cut per-class filesystem stat calls.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q3.** True or False: leaving APP_DEBUG=1 in production is acceptable as long as the profiler is disabled.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q3"
    **B**

    False. APP_DEBUG=1 enables verbose error pages that leak stack traces and internals, re-enables freshness checks and other overhead, and generally exposes the app. Production must run APP_DEBUG=0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q4.** What does Process::run() return?  <small>_(easy · internals)_</small>

- A. The integer exit code
- B. The stdout as a string
- C. void
- D. A boolean success flag

??? success "Answer Q4"
    **A**

    run() blocks until completion and returns the exit code; use getOutput() for stdout and mustRun() to throw a ProcessFailedException on failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

**Q5.** What is the default Process timeout?  <small>_(easy · trap)_</small>

- A. 60 seconds
- B. Unlimited
- C. 30 seconds
- D. 300 seconds

??? success "Answer Q5"
    **A**

    The default timeout is 60 seconds; pass null to setTimeout() to disable it. Exceeding it throws a ProcessTimedOutException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#process-timeout)

**Q6.** Which lock store provides mutual exclusion across multiple servers?  <small>_(easy · single)_</small>

- A. RedisStore
- B. FlockStore
- C. SemaphoreStore
- D. InMemoryStore

??? success "Answer Q6"
    **A**

    Flock and Semaphore stores are local to one machine, and InMemoryStore is per-process (tests). Shared stores like Redis (or a database store) coordinate locks across servers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#available-stores)

**Q7.** Which class renders Twig templates into an email body?  <small>_(easy · single)_</small>

- A. Symfony\Bridge\Twig\Mime\TemplatedEmail
- B. Symfony\Component\Mime\Email
- C. Symfony\Component\Mailer\Mailer
- D. Symfony\Component\Mime\Message

??? success "Answer Q7"
    **A**

    TemplatedEmail (in the Twig bridge) carries htmlTemplate()/textTemplate() and context(); a body renderer turns them into MIME parts before sending. Plain Email has no template support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#twig-html-css)

**Q8.** Which environment variable selects the runtime class?  <small>_(easy · single)_</small>

- A. APP_RUNTIME
- B. APP_ENV
- C. SYMFONY_RUNTIME
- D. RUNTIME_CLASS

??? success "Answer Q8"
    **A**

    APP_RUNTIME (or composer.json extra.runtime.class) chooses the RuntimeInterface implementation; the default is SymfonyRuntime, which extends GenericRuntime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

**Q9.** Which class does the default SymfonyRuntime extend?  <small>_(easy · single)_</small>

- A. GenericRuntime
- B. HttpKernel
- C. Kernel
- D. SymfonyStyle

??? success "Answer Q9"
    **A**

    SymfonyRuntime extends the framework-agnostic GenericRuntime, adding Symfony-aware resolvers/runners (inject Request, SymfonyStyle, console Input/Output; run a Kernel or console Application). It is not a kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

**Q10.** ClockInterface::now() returns what type?  <small>_(easy · internals)_</small>

- A. A \DateTimeImmutable (a DatePoint)
- B. A Unix timestamp int
- C. A mutable \DateTime
- D. A float of seconds

??? success "Answer Q10"
    **A**

    now() returns an immutable DatePoint (a \\DateTimeImmutable subclass). Tests swap the NativeClock for a MockClock to freeze or advance time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q11.** Which clock lets tests freeze or advance time without a real delay?  <small>_(easy · single)_</small>

- A. MockClock — you set the time and its sleep() advances virtual time
- B. NativeClock
- C. MonotonicClock
- D. SystemClock

??? success "Answer Q11"
    **A**

    MockClock is constructed with a fixed time and its sleep() advances time virtually (no real waiting), perfect for TTL/expiry tests. NativeClock is the real prod clock; MonotonicClock is for durations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html#usage-in-tests)

**Q12.** Which clock is best for measuring elapsed durations and is immune to system clock changes?  <small>_(easy · single)_</small>

- A. MonotonicClock
- B. NativeClock
- C. MockClock
- D. DatePoint

??? success "Answer Q12"
    **A**

    MonotonicClock uses a high-resolution monotonic source unaffected by NTP or manual clock adjustments, so duration diffs stay accurate. Wall-clock NativeClock can jump; MockClock is for tests; DatePoint is a date type, not a clock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q13.** What does dd() do that dump() does not?  <small>_(easy · trap)_</small>

- A. It stops execution (exit) after dumping
- B. It writes the dump to a log file
- C. It serializes the value to JSON
- D. It dumps only scalar values

??? success "Answer Q13"
    **A**

    dd() means 'dump and die': it dumps then calls exit, halting the script. dump() records the variable and lets execution continue (the dump is shown in the toolbar/collector).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html#the-dump-function)

**Q14.** Which serializable object represents a throwable for rendering and logging?  <small>_(easy · single)_</small>

- A. FlattenException
- B. HttpException
- C. ErrorEvent
- D. ExceptionListener

??? success "Answer Q14"
    **A**

    Throwables are normalised into a FlattenException — a serializable snapshot (class, message, status, trace) that error renderers (HTML/JSON/XML) turn into output and that is safe to log. HttpException is a throwable, not the snapshot.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

**Q15.** Which service tag registers a custom data collector (with a toolbar/panel)?  <small>_(easy · single)_</small>

- A. data_collector (with a `template` attribute for the panel)
- B. kernel.collector
- C. profiler.panel
- D. web_profiler.collector

??? success "Answer Q15"
    **A**

    The data_collector tag wires a DataCollectorInterface; supplying a `template` attribute makes its toolbar badge and panel appear. Autoconfigure applies the tag automatically for services implementing the interface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

**Q16.** What does the translator return when a message id has no translation in the active locale or its fallbacks?  <small>_(easy · trap)_</small>

- A. The message id itself (and it is logged in dev)
- B. An empty string
- C. A TranslationException
- D. null

??? success "Answer Q16"
    **A**

    A missing translation returns the untranslated id, not an error or empty string, so the UI degrades gracefully. In dev the miss is logged so you can fix the catalogue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

**Q17.** Which class returns the localized display name of a country code?  <small>_(easy · single)_</small>

- A. Symfony\Component\Intl\Countries (Countries::getName('FR'))
- B. Symfony\Component\Locale\Country
- C. Symfony\Component\Translation\Countries
- D. Symfony\Component\Intl\Locale

??? success "Answer Q17"
    **A**

    Countries::getName() reads the bundled ICU dataset and returns the name in the current/requested locale. Related classes are Languages, Locales, Currencies and Timezones. The other namespaces do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/intl.html)

**Q18.** Which Finder method defines the directories to search?  <small>_(easy · single)_</small>

- A. in()
- B. from()
- C. search()
- D. path()

??? success "Answer Q18"
    **A**

    Finder::in() sets the search directories; without it the Finder throws. It yields Symfony SplFileInfo objects with helpers like getRelativePathname().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

**Q19.** Symfony\Contracts\Cache\CacheInterface::get() runs its callback…  <small>_(medium · internals)_</small>

- A. only on a cache miss, then stores and returns the value
- B. on every call
- C. never — you must call save() yourself
- D. only when the beta factor is INF

??? success "Answer Q19"
    **A**

    The callback computes the value on a miss; the result is persisted and returned. It also provides probabilistic early-expiration stampede protection. Running on every call would defeat caching, and unlike PSR-6 you do not call save() manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q20.** A pool is declared with `tags: true` in cache.yaml. What does this enable?  <small>_(medium · config)_</small>

- A. Tagging items with $item->tag([...]) and evicting groups via invalidateTags([...])
- B. Automatic compression of cached values
- C. Sharing the pool across all servers
- D. Disabling stampede protection

??? success "Answer Q20"
    **A**

    `tags: true` wraps the pool in a TagAwareAdapter implementing TagAwareCacheInterface, so items can carry tags and invalidateTags() evicts all items with a given tag — invalidation by concern rather than by key. Calling $item->tag() on a non-tag-aware pool errors.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#using-cache-tags)

**Q21.** True or False: passing $beta = INF to CacheInterface::get() forces the value to be recomputed immediately.  <small>_(medium · true-false)_</small>

- A. True
- B. False

??? success "Answer Q21"
    **A**

    True. $beta = INF forces early expiration, so the callback runs and the value is refreshed on this call. $beta = 0 disables early expiration entirely; the default (null) picks a sensible probabilistic value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

**Q22.** Using the raw PSR-6 API, how do you distinguish a stored null value from a missing key?  <small>_(medium · internals)_</small>

- A. Check $item->isHit() — get() returns null for both cases
- B. Compare $item->get() to null
- C. Call $pool->hasKey($key)
- D. Catch a CacheMissException

??? success "Answer Q22"
    **A**

    With PSR-6, CacheItemInterface::get() returns null both for an absent key and for a genuinely stored null, so you must call isHit() to tell them apart. The contracts callback API sidesteps this ambiguity; there is no hasKey() or miss exception.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

**Q23.** In serialize(), which stage runs first?  <small>_(medium · internals)_</small>

- A. The normalizer (object to array), then the encoder (array to string)
- B. The encoder, then the normalizer
- C. Only the encoder runs
- D. They run concurrently

??? success "Answer Q23"
    **A**

    serialize() normalizes the object to an array/scalars, then encodes that to a string. deserialize() reverses it: decode then denormalize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/serializer.html)

**Q24.** #[Groups(['read'])] on a property takes effect when…  <small>_(medium · trap)_</small>

- A. the context includes ['groups' => ['read']]
- B. always, regardless of context
- C. only during deserialization
- D. the property is public

??? success "Answer Q24"
    **A**

    Group filtering only applies when matching groups are passed in the context; otherwise the group attribute has no effect and all fields are (de)serialized.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

**Q25.** Which normalizer reads and writes private properties directly via reflection?  <small>_(medium · single)_</small>

- A. PropertyNormalizer
- B. ObjectNormalizer
- C. GetSetMethodNormalizer
- D. JsonEncoder

??? success "Answer Q25"
    **A**

    PropertyNormalizer accesses object properties directly (including private), whereas ObjectNormalizer uses accessors and the constructor, and GetSetMethodNormalizer uses only get/set methods. JsonEncoder is an encoder, not a normalizer.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

**Q26.** What does the framework.serializer.default_context option skip_null_values: true do?  <small>_(medium · config)_</small>

- A. Omits properties whose value is null from the serialized output
- B. Throws when a property is null
- C. Converts null to an empty string
- D. Only affects deserialization of missing keys

??? success "Answer Q26"
    **A**

    By default a null property is serialized as \"key\":null. Setting AbstractObjectNormalizer::SKIP_NULL_VALUES (skip_null_values) omits those keys from the payload. The classic bug is a consumer treating an absent key as an error rather than 'the value was null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html)

**Q27.** A private property with no getter is missing from the JSON produced by the default ObjectNormalizer. Why, and how do you fix it?  <small>_(medium · debug)_</small>

- A. ObjectNormalizer uses accessors; add a getter (or use PropertyNormalizer, which reads properties directly)
- B. The property must be marked #[Groups] to appear
- C. You must call serialize() with the 'private' => true context
- D. Private properties can never be serialized in Symfony 8

??? success "Answer Q27"
    **A**

    ObjectNormalizer reads via getters/issers/hassers and the constructor, so a private property without an accessor is invisible. Provide a getter or switch to PropertyNormalizer, which uses reflection to read properties directly. Groups filter fields but do not expose accessorless private properties.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#normalizers)

**Q28.** In which environment is .env.local NOT loaded?  <small>_(medium · trap)_</small>

- A. test
- B. dev
- C. prod
- D. staging

??? success "Answer Q28"
    **A**

    .env.local is intentionally skipped in the test environment so tests run from committed defaults and stay reproducible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#selecting-the-active-environment)

**Q29.** What does `composer dump-env prod` produce, and what is the effect?  <small>_(medium · config)_</small>

- A. .env.local.php — Symfony loads it directly and skips parsing .env* files
- B. .env.prod — parsed on every request
- C. config/prod.php overriding all bundles
- D. Nothing; it only validates env vars

??? success "Answer Q29"
    **A**

    The whole .env* cascade is compiled to a plain PHP array in .env.local.php, which Symfony loads directly, avoiding DotEnv parsing on each request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production)

**Q30.** ExpressionLanguage::compile() returns what?  <small>_(medium · internals)_</small>

- A. A string of PHP source code
- B. The evaluated result value
- C. An AST node object
- D. A boolean success flag

??? success "Answer Q30"
    **A**

    compile() transpiles an expression to PHP source you can cache/reuse, while evaluate() interprets the expression and returns its value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q31.** A .env file sets DATABASE_URL, but a real OS environment variable DATABASE_URL is also exported. Which wins?  <small>_(medium · trap)_</small>

- A. The real OS environment variable — DotEnv never overrides an existing real env var
- B. .env, because it is loaded last
- C. Whichever value is longer
- D. They are concatenated

??? success "Answer Q31"
    **A**

    Real OS environment variables always take precedence; the DotEnv cascade (.env → .env.local → .env.<env> → .env.<env>.local) only fills values not already set in the real environment. Later .env* files override earlier ones but never a real env var.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/configuration.html#overriding-environment-values-via-env-local)

**Q32.** Which class merges every config source and validates it against a bundle's Configuration tree?  <small>_(medium · internals)_</small>

- A. Processor (Processor::processConfiguration())
- B. TreeBuilder
- C. FileLocator
- D. ContainerBuilder

??? success "Answer Q32"
    **A**

    Processor::processConfiguration() merges all sources and validates them against the tree returned by the Configuration class, applying defaults and constraints. TreeBuilder only defines the schema; FileLocator finds files.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/config/definition.html)

**Q33.** You changed a YAML config file and redeployed to prod, but the change has no effect. Why?  <small>_(medium · trap)_</small>

- A. Prod loads the compiled container as-is and does not auto-detect config changes; you must clear/warm the cache on deploy
- B. Prod re-reads YAML on every request, so a restart is needed
- C. YAML config is ignored in prod; only PHP config works
- D. APP_DEBUG must be 1 for config to reload

??? success "Answer Q33"
    **A**

    In prod the compiled container in var/cache/prod is loaded as-is with no freshness checks (those exist only in debug), so config changes require cache:clear + cache:warmup on deploy. Enabling APP_DEBUG in prod is unsafe and not the fix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q34.** Why set opcache.validate_timestamps=0 in production?  <small>_(medium · config)_</small>

- A. To skip per-request file-modification checks and always serve cached bytecode (reset opcache on deploy instead)
- B. To enable debug mode
- C. To disable opcache entirely
- D. To force recompilation on every request

??? success "Answer Q34"
    **A**

    With immutable deploys, disabling timestamp validation maximises opcache hits by not stat-ing files each request. Because opcache then never notices new files, you must reset opcache (or the PHP process manager) on each deploy so the new bytecode is loaded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/performance.html)

**Q35.** Which ordered command sequence is correct for a from-scratch prod deploy?  <small>_(medium · scenario)_</small>

- A. composer install --no-dev --optimize-autoloader → composer dump-env prod → cache:clear → cache:warmup → reset opcache
- B. cache:warmup → composer install → dump-env prod → go live
- C. composer update → APP_DEBUG=1 → cache:clear
- D. cache:clear → composer install --dev → dump-env dev

??? success "Answer Q35"
    **A**

    You install prod deps first, compile the env cascade with dump-env prod, then clear and warm the cache so the first live request is fast, and finally reset opcache. Warming before installing, or shipping dev deps / APP_DEBUG=1, are wrong.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q36.** Which Process constructor auto-escapes each argument?  <small>_(medium · trap)_</small>

- A. new Process(['git', 'log', '--oneline'])
- B. Process::fromShellCommandline('git log --oneline')
- C. Both escape equally
- D. Neither escapes anything

??? success "Answer Q36"
    **A**

    The array form escapes each element automatically. fromShellCommandline() runs a raw shell string and does not escape, risking command injection if you interpolate untrusted input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

**Q37.** You build a command from user input using Process::fromShellCommandline('convert '.$userInput). What is the risk and the fix?  <small>_(medium · debug)_</small>

- A. Command injection — use the array constructor new Process(['convert', $userInput]) so each argument is auto-escaped
- B. None; fromShellCommandline escapes arguments for you
- C. A timeout error; raise setTimeout()
- D. It only fails on Windows; add a shebang

??? success "Answer Q37"
    **A**

    fromShellCommandline runs the string through /bin/sh with no escaping, so untrusted input can inject shell metacharacters. The array constructor escapes each element as a single argument, eliminating the injection vector. This is unrelated to timeouts or platform.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

**Q38.** Which call runs a process and throws automatically on a non-zero exit code?  <small>_(medium · code)_</small>

- A. mustRun() — it throws ProcessFailedException on failure
- B. run() — it throws ProcessFailedException on failure
- C. start() — it throws immediately on failure
- D. wait() — it converts the exit code into an exception

??? success "Answer Q38"
    **A**

    mustRun() behaves like run() but throws ProcessFailedException when the process exits non-zero. run() simply returns the integer exit code and you check isSuccessful() yourself; start()/wait() are for async execution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html#usage)

**Q39.** LockInterface::acquire() called with no argument is…  <small>_(medium · trap)_</small>

- A. non-blocking — it returns false immediately if the lock is held
- B. blocking — it waits until the lock is free
- C. throwing an exception if the lock is held
- D. always successful

??? success "Answer Q39"
    **A**

    acquire() defaults to non-blocking; pass true to block until the resource becomes available (store permitting). It returns a boolean false when held, it does not throw, so `if (!$lock->acquire()) { return; }` is the correct guard.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html#blocking-locks)

**Q40.** Why call refresh() during a long critical section?  <small>_(medium · scenario)_</small>

- A. To extend the lock's TTL so it is not considered expired mid-job
- B. To release then reacquire the lock
- C. To switch to a different store
- D. To convert it to a shared lock

??? success "Answer Q40"
    **A**

    Locks have a TTL to avoid deadlocks after crashes. refresh() prolongs it so a still-working owner keeps exclusivity; without it another process could acquire the lock after the TTL, breaking mutual exclusion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

**Q41.** Which is the correct guard to skip work another process is already doing?  <small>_(medium · code)_</small>

- A. if (!$lock->acquire()) { return; }
- B. try { $lock->acquire(); } catch (LockConflictedException) { return; }
- C. if ($lock->acquire() === null) { return; }
- D. if ($lock->isLocked()) { return; }

??? success "Answer Q41"
    **A**

    Non-blocking acquire() returns false when the resource is held, so !$lock->acquire() is the idiomatic early-return guard. It does not return null and does not throw on contention (only blocking acquire(true) may throw LockConflictedException). Forgetting to check the boolean means entering the critical section unprotected.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html)

**Q42.** What is the default TTL of a lock created via LockFactory::createLock($resource)?  <small>_(medium · internals)_</small>

- A. 300 seconds (5 minutes), with autoRelease on by default
- B. 60 seconds
- C. Unlimited (no TTL)
- D. 30 seconds

??? success "Answer Q42"
    **A**

    createLock(string $resource, ?float $ttl = 300.0, bool $autoRelease = true) defaults to a 300 second TTL and releases the lock when the Lock object is destroyed. Long jobs should raise the TTL and call refresh() to avoid premature expiry.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/lock.html#expiring-locks)

**Q43.** With Messenger routing configured for emails, MailerInterface::send() will…  <small>_(medium · scenario)_</small>

- A. dispatch a SendEmailMessage to be delivered by a worker
- B. always send synchronously over SMTP
- C. throw if no worker is running
- D. render but not send the email

??? success "Answer Q43"
    **A**

    When SendEmailMessage is routed to a transport, send() enqueues it; a worker delivers it later, giving async sending plus retries. It does not throw if a worker is down — the message just waits in the queue.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

**Q44.** How is an inline (embedded) image referenced from an email's HTML body?  <small>_(medium · single)_</small>

- A. Via a cid: reference produced by embed()/embedFromPath()
- B. Only as an absolute external URL
- C. As a base64 data: URI hand-written by the developer
- D. Inline images are not supported

??? success "Answer Q44"
    **A**

    embed()/embedFromPath() add a DataPart addressed with cid:<name>, which the HTML body references (e.g. <img src="cid:logo">).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#embedding-images)

**Q45.** Which configuration makes emails send asynchronously via Messenger?  <small>_(medium · config)_</small>

- A. Route Symfony\Component\Mailer\Messenger\SendEmailMessage to a transport in messenger routing (and run a worker)
- B. Set MAILER_DSN to async://default
- C. Add async: true under framework.mailer
- D. Wrap send() in a try/catch

??? success "Answer Q45"
    **A**

    Async delivery comes from routing SendEmailMessage to a Messenger transport and consuming it with a worker. MAILER_DSN chooses the delivery transport (SMTP/API), not sync-vs-async, and there is no framework.mailer.async flag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages-async)

**Q46.** What does public/index.php return under the Runtime component?  <small>_(medium · internals)_</small>

- A. A callable that produces the application object (e.g. a Kernel)
- B. A Response object
- C. Nothing — it echoes the output directly
- D. The exit code as an int

??? success "Answer Q46"
    **A**

    index.php returns a callable; autoload_runtime.php resolves its arguments, invokes it, then a RunnerInterface handles/sends/terminates. It never calls handle() itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

**Q47.** A teammate 'fixes' a bug by adding $kernel->handle($request)->send(); at the end of public/index.php, right after the file already returns its closure. What is wrong with this?  <small>_(medium · trap)_</small>

- A. public/index.php must only return a callable; the Runtime component itself builds the kernel, handles the request and sends the response
- B. Nothing — calling handle()/send() manually is required in Symfony 8
- C. It is wrong only when APP_RUNTIME is unset
- D. It is wrong only under SymfonyRuntime, not GenericRuntime

??? success "Answer Q47"
    **A**

    The whole point of symfony/runtime is that the front controller only returns a callable (or an application object); the runtime resolves its arguments, invokes it, and — for the Symfony flavor — runs the kernel and sends the response itself. Hand-calling handle()/send() after autoload_runtime.php has already done so double-processes the request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html)

**Q48.** True or False: you should guard ClockInterface::now() with a nullsafe operator because it may return null with a frozen MockClock.  <small>_(medium · trap)_</small>

- A. False
- B. True

??? success "Answer Q48"
    **A**

    False. now() is typed : \\DateTimeImmutable and always returns a DatePoint, even with a frozen MockClock, so ?-> is unnecessary. The real bug is comparing a MockClock time against a live new \\DateTime() — read time from the clock on both sides.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q49.** Which object does VarDumper's VarCloner produce before rendering?  <small>_(medium · internals)_</small>

- A. A Data object
- B. A Response
- C. A FlattenException
- D. A StopwatchEvent

??? success "Answer Q49"
    **A**

    The cloner captures the variable into an immutable, depth-limited Data object, which a CliDumper or HtmlDumper then renders — separating capture from output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

**Q50.** What unit does StopwatchEvent::getDuration() use, and when is the debug.stopwatch service available?  <small>_(medium · internals)_</small>

- A. Milliseconds; the service exists only when debug/the profiler is enabled
- B. Seconds; always available in every environment
- C. Microseconds; only in prod
- D. Nanoseconds; only in tests

??? success "Answer Q50"
    **A**

    getDuration() returns milliseconds, and the autowirable debug.stopwatch service is only registered in debug (dev/test). Injecting Stopwatch in prod therefore causes a wiring error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

**Q51.** A service that autowires Symfony\Component\Stopwatch\Stopwatch works in dev but fails to boot in prod. Why?  <small>_(medium · debug)_</small>

- A. The debug.stopwatch service exists only in debug mode, so the dependency is missing in prod
- B. Stopwatch requires the profiler bundle in prod
- C. getDuration() throws in prod
- D. Autowiring is disabled in prod

??? success "Answer Q51"
    **A**

    Stopwatch's framework service is registered only when debug is enabled, so in prod there is nothing to inject and the container fails. Use it for ad-hoc dev profiling only; for prod metrics use real observability.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/stopwatch.html)

**Q52.** An uncaught exception that does NOT implement HttpExceptionInterface produces which status code?  <small>_(medium · trap)_</small>

- A. 500
- B. 404
- C. 400
- D. 200

??? success "Answer Q52"
    **A**

    Only HttpExceptionInterface carries a custom status code; any other throwable defaults to HTTP 500 via the error controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q53.** What does the ErrorHandler component do with a PHP warning or notice?  <small>_(medium · internals)_</small>

- A. Converts it into a catchable \ErrorException via set_error_handler()
- B. Silently ignores it
- C. Writes it directly into the response body
- D. Converts it into an HttpException

??? success "Answer Q53"
    **A**

    ErrorHandler registers set_error_handler() to throw \\ErrorException for PHP errors (warnings, notices, fatals via a shutdown function), making them catchable. It does not turn them into HttpExceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/error_handler.html)

**Q54.** In a controller, which throw produces a 404 rendered by the framework error controller?  <small>_(medium · scenario)_</small>

- A. throw new NotFoundHttpException('...') — it implements HttpExceptionInterface with status 404
- B. return new Response('', 404) is required; exceptions always give 500
- C. throw new \RuntimeException('not found')
- D. throw new \InvalidArgumentException('404')

??? success "Answer Q54"
    **A**

    NotFoundHttpException implements HttpExceptionInterface, so the error controller maps it to 404 via getStatusCode(). A plain \\RuntimeException or \\InvalidArgumentException does not carry a status and becomes 500. You do not need to build the Response manually.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/controller/error_pages.html)

**Q55.** When does the Web Profiler collect data for a request?  <small>_(medium · internals)_</small>

- A. On kernel.response, with late collectors running at kernel.terminate
- B. On kernel.request only
- C. During container compilation
- D. Only in the CLI

??? success "Answer Q55"
    **A**

    Profiler::collect() runs on kernel.response, invoking each DataCollector; LateDataCollectorInterface::lateCollect() runs later at terminate for data not complete during the response.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler.html)

**Q56.** A custom collector storing a PDO connection in $this->data breaks profile storage. Why?  <small>_(medium · debug)_</small>

- A. $this->data is serialized to storage (via VarDumper's cloner); a live connection/resource is not serializable
- B. PDO is banned from all services
- C. Collectors may only store strings
- D. The data_collector tag rejects objects

??? success "Answer Q56"
    **A**

    Profiles are persisted per token, so $this->data must be serializable — store scalar/array (VarDumper-clonable) data, not live resources like a PDO connection or an entity with a connection. Implement reset() for worker reuse.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

**Q57.** Which mechanism does Symfony 8 use for translation pluralization?  <small>_(medium · single)_</small>

- A. ICU MessageFormat, e.g. {count, plural, one {…} other {# …}}
- B. The singular|plural pipe syntax
- C. A %count% placeholder only
- D. Separate keys per number

??? success "Answer Q57"
    **A**

    ICU MessageFormat handles plural/select rules with locale-aware categories (one/few/many/other); the old pipe syntax is legacy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

**Q58.** What is the default translation domain, and what file naming applies ICU formatting?  <small>_(medium · config)_</small>

- A. Default domain is messages; the +intl-icu suffix (messages+intl-icu.<locale>.yaml) enables ICU formatting
- B. Default domain is default; ICU is always applied to every file
- C. Default domain is translations; ICU needs a .icu extension
- D. There is no default domain; you must always pass one

??? success "Answer Q58"
    **A**

    When no domain is passed, trans() uses messages; validators and security are separate domains. ICU MessageFormat is applied to catalogues named with the +intl-icu suffix — forgetting it means ICU rules are not parsed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

**Q59.** What makes Filesystem::dumpFile() safe against partial reads?  <small>_(medium · internals)_</small>

- A. It writes to a temporary file then atomically renames it into place
- B. It acquires an flock on the file
- C. It compresses the content
- D. It buffers writes in memory forever

??? success "Answer Q59"
    **A**

    dumpFile() writes to a temp file and renames it, so a reader always sees either the old content or the complete new content, never a half-written file. appendToFile(), by contrast, is not atomic.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html)

**Q60.** How does Symfony\Component\Filesystem\Filesystem signal a failed operation (e.g. copy())?  <small>_(medium · trap)_</small>

- A. It throws an IOExceptionInterface (it does not return false)
- B. It returns false, like the native PHP functions
- C. It returns null
- D. It triggers a PHP warning only

??? success "Answer Q60"
    **A**

    Unlike native file functions that return false, Filesystem methods throw IOExceptionInterface on failure, so errors cannot be silently ignored. Also note Path helpers manipulate path strings only and never touch the disk.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/filesystem.html#error-handling)

**Q61.** A Finder query returns directories as well as files. What is missing?  <small>_(medium · debug)_</small>

- A. A ->files() call — without files() or directories() the Finder yields both
- B. A ->name() filter — name() restricts to files
- C. A ->in() call — in() excludes directories
- D. Nothing; Finder always returns files only

??? success "Answer Q61"
    **A**

    Finder yields both files and directories unless you narrow it with files() (or directories()). name()/in() do not restrict the entry type. Iterated results are Finder SplFileInfo objects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/finder.html)

**Q62.** Which of the following statements are true about the Symfony Cache component? (select all that apply)  <small>_(medium · multiple)_</small>

- A. CacheInterface::get($key, $callback) runs the callback only on a cache miss and stores its return value
- B. Cache tags require a tag-aware pool (TagAwareAdapter or tags: true); calling $item->tag() on a plain pool does not work
- C. If the callback returns null, that null is stored and later calls return it as a hit until it expires
- D. PSR-16 (SimpleCache) supports cache tags and deferred saves just like PSR-6
- E. CacheInterface::get() returns null to signal a cache miss

??? success "Answer Q62"
    **A, B, C**

    The contracts get() computes-and-stores on miss, tags only work on a TagAwareAdapter/pool configured with tags: true, and a stored null is a valid cached value that counts as a hit. PSR-16 has no tags and no deferred saves (those are PSR-6 features), and get() never returns null to mean "miss" — on a miss it runs the callback and returns its result.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html)

**Q63.** Which of the following statements are true about the Symfony Clock component? (select all that apply)  <small>_(medium · multiple)_</small>

- A. ClockInterface::now() returns an immutable DatePoint (a \DateTimeImmutable subclass), never a mutable \DateTime
- B. MockClock::sleep() advances virtual time instantly, with no real delay — ideal for TTL/expiry tests
- C. The framework autowires MockClock as the default clock in the dev environment
- D. MonotonicClock is meant for reading the wall-clock time and is affected by system clock (NTP) adjustments

??? success "Answer Q63"
    **A, B**

    now() is typed to return a \DateTimeImmutable and yields a DatePoint, and MockClock advances time virtually so tests never wait. The default framework clock is NativeClock in every environment (tests swap in MockClock themselves), and MonotonicClock is for measuring durations precisely because it is immune to system clock changes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html)

**Q64.** Which of the following statements are true about the Symfony Mailer and Mime components? (select all that apply)  <small>_(medium · multiple)_</small>

- A. When SendEmailMessage is routed to an async Messenger transport, MailerInterface::send() queues the email instead of delivering it inline
- B. Images embedded with embedFromPath() are referenced in the HTML body via a cid: reference
- C. TemplatedEmail lives in the Symfony\Component\Mime namespace, so no Twig bridge is needed to render templates
- D. The Mailer Envelope is just another name for the visible message headers

??? success "Answer Q64"
    **A, B**

    With Messenger routing configured, send() dispatches a SendEmailMessage that a worker delivers later, and embedded parts are addressed with cid: in the HTML body. TemplatedEmail is part of the Twig bridge (Symfony\Bridge\Twig\Mime), and the Envelope (sender/recipients used for the SMTP conversation) is distinct from the message headers rendered in the visible email.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html)

**Q65.** A class exposes its data only through __call() (no real getX()/setX() methods). You read a path with the default PropertyAccessor. What happens?  <small>_(medium · trap)_</small>

- A. It throws — __call fallback is not enabled by default, only __get/__set are
- B. It works — all magic methods are enabled by default
- C. It returns null silently
- D. It works only for reading, never for writing

??? success "Answer Q65"
    **A**

    PropertyAccessorBuilder defaults to MAGIC_GET | MAGIC_SET only; __call is disabled unless enableMagicCall() is explicitly called. Without it, a class reachable only via __call() is not accessible through the default accessor, and getValue() throws rather than returning null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/property_access.html#magic-getters-and-setters)

**Q66.** Which statement about PSR-6 vs PSR-16 is correct?  <small>_(hard · trap)_</small>

- A. PSR-6 (pools/items) supports deferred saves and, via TagAwareAdapter, tags; PSR-16 (SimpleCache) does not
- B. PSR-16 supports tags but PSR-6 does not
- C. Both are identical key/value APIs
- D. PSR-6 has no expiration support

??? success "Answer Q66"
    **A**

    PSR-16 SimpleCache is a thin key/value API with no items, deferred saves or tags. PSR-6 uses CacheItem objects and supports tags through a TagAwareAdapter as well as expiration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/cache.html)

**Q67.** Cache stampede protection in Symfony Cache is implemented by…  <small>_(hard · internals)_</small>

- A. probabilistic early expiration controlled by the $beta factor
- B. a global mutex acquired on every key
- C. disabling TTLs entirely
- D. duplicating the value across all adapters

??? success "Answer Q67"
    **A**

    As an item nears expiry, one request is probabilistically chosen to recompute early while others serve the cached value ($beta=INF forces it, 0 disables it). There is no per-key mutex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#stampede-prevention)

**Q68.** Your CacheInterface::get() callback returns null on the first call. What happens on the next call before expiry?  <small>_(hard · trap)_</small>

- A. null is returned as a cache hit; the callback is NOT run again
- B. The callback runs again because null means a miss
- C. A CacheException is thrown for storing null
- D. The item is deleted automatically

??? success "Answer Q68"
    **A**

    null is a valid cached value: the contracts API stores whatever the callback returns and treats it as a hit until it expires. get() never uses null to mean 'miss' — that is exactly the PSR-6 footgun (getItem()->get() returning null for both absent and stored-null) that the callback API avoids. Caching 'no result' as null is fine, but it counts as a hit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/cache.html#cache-contracts)

**Q69.** By default, what is the Serializer's circular reference limit before it throws?  <small>_(hard · trap)_</small>

- A. 1 (unless a circular reference handler or #[MaxDepth] is set)
- B. 0 — it never throws
- C. Unlimited
- D. 10

??? success "Answer Q69"
    **A**

    The default circular reference limit is 1; beyond it a CircularReferenceException is thrown unless a CIRCULAR_REFERENCE_HANDLER or MaxDepth is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#handling-circular-references)

**Q70.** A UserDto has #[Groups(['read'])] #[SerializedName('full_name')] on $name and #[Ignore] on $passwordHash. What is the JSON when serialized with context ['groups' => ['read']]?  <small>_(hard · code)_</small>

- A. {"full_name":"..."} plus any other read-group fields; passwordHash is omitted
- B. {"name":"...","passwordHash":"..."}
- C. All properties, because groups are ignored during serialization
- D. An empty object, because #[Ignore] hides everything

??? success "Answer Q70"
    **A**

    With the read group in context, only read-group properties are emitted; $name is renamed to full_name by #[SerializedName], and #[Ignore] drops passwordHash entirely regardless of group. Groups are honoured only because they are passed in the context.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html#using-serialization-groups-attributes)

**Q71.** What is the result of ExpressionLanguage::compile('1 + a', ['a'])?  <small>_(hard · code)_</small>

- A. The PHP source string "(1 + $a)"
- B. The integer 1
- C. A closure you can invoke
- D. An exception, because $a is undefined

??? success "Answer Q71"
    **A**

    compile() emits PHP source, turning the variable name a into $a: "(1 + $a)". It does not evaluate anything (so no undefined-variable error) — use evaluate('1 + a', ['a' => 5]) to get the value 6.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/expression_language.html)

**Q72.** What does `cache:clear` run, by default, in addition to removing stale cache?  <small>_(hard · internals)_</small>

- A. The cache warmers (CacheWarmerInterface) that pre-build the container, routing, Twig cache and metadata
- B. The database migrations
- C. The Messenger workers
- D. composer install

??? success "Answer Q72"
    **A**

    cache:clear removes stale cache and then runs the CacheWarmerInterface warmers to pre-build the container, routing matcher/generator, Twig template cache and validator/serializer metadata. cache:warmup warms without clearing. Migrations, workers and composer are separate steps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/deployment.html)

**Q73.** In the Mailer, how does the Envelope differ from the message headers?  <small>_(hard · internals)_</small>

- A. The Envelope holds the actual sender/recipients used for the SMTP conversation; headers (From/To) render in the visible message
- B. They are the same object with two names
- C. The Envelope stores the HTML body; headers store attachments
- D. The Envelope is only used for async delivery

??? success "Answer Q73"
    **A**

    Mailer's Envelope (sender + recipients) drives the transport's SMTP exchange, whereas the message headers (From, To, Subject) are what the recipient sees. They can legitimately differ (e.g. bounce address vs visible From), which is a common exam distinction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#sending-messages)

**Q74.** How does the argument `array $context` in the index.php closure get populated?  <small>_(hard · internals)_</small>

- A. The runtime's resolver autowires it from $_SERVER (env vars like APP_ENV/APP_DEBUG)
- B. You must call getenv() yourself inside the closure
- C. Symfony injects it from services.yaml parameters
- D. It is always an empty array in Symfony 8

??? success "Answer Q74"
    **A**

    RuntimeInterface::getResolver() builds a resolver that inspects the callable's typed arguments and supplies them — array $context comes from $_SERVER (env), and it can also inject Request, InputInterface, etc. You therefore never read $_SERVER manually in the entry point.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/runtime.html#using-the-runtime)

**Q75.** Your metric is only complete after the response is sent. Which interface should the collector implement?  <small>_(hard · internals)_</small>

- A. LateDataCollectorInterface (its lateCollect() runs at kernel.terminate)
- B. DataCollectorInterface only; collect() runs after terminate
- C. EventSubscriberInterface on kernel.request
- D. CacheWarmerInterface

??? success "Answer Q75"
    **A**

    Normal collect() runs on kernel.response, too early for post-response data (final dumps, cache calls). LateDataCollectorInterface::lateCollect() runs later at terminate, when that data is complete.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/profiler/data_collector.html)

**Q76.** Which of the following statements are true about the Symfony Lock component? (select all that apply)  <small>_(hard · multiple)_</small>

- A. acquire() is non-blocking by default: it returns false immediately when the lock is already held
- B. FlockStore and SemaphoreStore only guarantee mutual exclusion on a single machine
- C. Locks have a TTL (300 seconds by default), and long jobs must call refresh() to extend it
- D. acquire() throws a LockConflictedException whenever the lock is already held
- E. A FlockStore is a safe choice to serialise a cron job across multiple servers

??? success "Answer Q76"
    **A, B, C**

    The default acquire(false) returns a plain false when the resource is busy, local stores (flock/semaphore) never protect across machines, and the TTL expires mid-job unless refresh() extends it. Non-blocking acquire() does not throw on contention (only blocking acquisition can end in LockConflictedException), and multi-server exclusion needs a shared store such as Redis or a database.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/lock.html)

**Q77.** Which of the following statements are true about the Symfony Process component? (select all that apply)  <small>_(hard · multiple)_</small>

- A. new Process(['git', 'log', $input]) auto-escapes each array element, so $input cannot inject shell syntax
- B. The default process timeout is 60 seconds; setTimeout(null) disables it
- C. mustRun() throws a ProcessFailedException when the process exits with a non-zero code
- D. Process::fromShellCommandline() escapes interpolated variables, making it safe with untrusted input
- E. run() returns the process standard output as a string

??? success "Answer Q77"
    **A, B, C**

    The array constructor escapes every argument, the timeout defaults to 60 seconds (nullable to disable), and mustRun() throws ProcessFailedException on failure where run() only returns the exit code. fromShellCommandline() runs a raw string through the shell with no escaping (a command-injection risk), and stdout is read via getOutput(), not from run().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/process.html)

**Q78.** Which of the following statements are true about the Symfony Serializer? (select all that apply)  <small>_(hard · multiple)_</small>

- A. serialize() works in two stages: normalizers turn objects into arrays, then an encoder turns the array into a string
- B. #[Groups] attributes only filter properties when a 'groups' key is passed in the serialization context
- C. PropertyNormalizer reads and writes through getters and setters, respecting PropertyAccess
- D. By default, null-valued properties are omitted from the JSON output

??? success "Answer Q78"
    **A, B**

    Serialization is normalize-then-encode, and group filtering is inert until you pass ['groups' => [...]] in the context — without it all readable fields are emitted. PropertyNormalizer accesses properties directly via reflection (ObjectNormalizer is the one using accessors), and null properties are serialized as null unless you enable the skip_null_values context option.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/serializer.html)

**Q79.** getValue() throws UninitializedPropertyException for one object and NoSuchPropertyException for another, both accessed via the same path 'title'. What distinguishes the two cases?  <small>_(hard · scenario)_</small>

- A. The first object declares a typed $title property that was never assigned; the second has no title property/getter/setter at all
- B. Both exceptions mean exactly the same thing; the name is arbitrary
- C. UninitializedPropertyException means the path syntax itself is malformed
- D. NoSuchPropertyException only happens with array paths, never objects

??? success "Answer Q79"
    **A**

    UninitializedPropertyException (a subtype of AccessException) means the property genuinely exists — typed, but never given a value — while NoSuchPropertyException means no getter, public property, or enabled magic method could resolve the path at all. isReadable() would have returned false for both without distinguishing them; only the thrown exception type tells them apart.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PropertyAccess/Exception/UninitializedPropertyException.php)

---

<small>Back to [Chapter Exams](index.md) · [Miscellaneous](../miscellaneous/index.md)</small>
