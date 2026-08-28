# Flashcards — Messenger

28 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

## 🧠 Pour les nuls

**C'est quoi ?** Un jeu de **28 flashcards** (question au recto, réponse au verso) sur Messenger. On lit la question, on répond mentalement, puis on tape pour révéler la réponse.

**Pourquoi ça existe ?** Se tester activement (essayer de répondre avant de voir la réponse) ancre l'information bien mieux que relire passivement un chapitre. Répété à intervalles espacés, c'est la technique de mémorisation la plus efficace connue.

**🏠 Analogie de la vraie vie :** Ce sont les **cartes-vocabulaire** utilisées pour apprendre une langue étrangère : un mot d'un côté, sa traduction de l'autre — on ne progresse qu'en essayant de deviner avant de retourner la carte.

**Symfony dans la vraie vie :** Recto de la carte → une question précise sur Messenger / Verso → la réponse avec sa justification et un lien vers la doc officielle / Cartes marquées "ratées" → à revoir en priorité au prochain passage.

**⚠️ Erreur fréquente :** Taper pour révéler la réponse trop vite, sans avoir vraiment tenté de répondre — cela transforme l'exercice en simple lecture, avec un gain de mémorisation presque nul.

**🧠 Comment le mémoriser :** *« Je réponds avant de retourner la carte »* — et je note les cartes ratées pour les revoir plus souvent que les autres (répétition espacée).

??? question "1. What does MessageBusInterface::dispatch() return?"
    **✅ An Envelope**

    dispatch() always returns the (possibly stamped) Envelope. A handler's return value is available via $envelope->last(HandledStamp::class)->getResult(). It never returns the value directly because a routed (async) message is not handled in this process at all — only the Envelope exists yet.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html)

??? question "2. Which attribute marks a service as a message handler in Symfony 8?"
    **✅ #[AsMessageHandler]**

    Symfony\\Component\\Messenger\\Attribute\\AsMessageHandler registers an invokable service (or a specific method) as a handler for its typed message argument. The other names do not exist in the component.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#registering-handlers)

??? question "3. Which of the following statements are true about Symfony Messenger? (select all that apply)"
    **✅ MessageBusInterface::dispatch() always returns an Envelope, never the handler's return value directly ; When a message is routed to an async transport, SendMessageMiddleware enqueues it and stops the bus, so no handler runs in the dispatching process ; DelayStamp(5000) delays delivery by 5000 milliseconds (5 seconds)**

    dispatch() returns the (possibly stamped) Envelope, routed-async messages are serialized and sent without invoking the handler in-process, and DelayStamp is expressed in milliseconds. A query result must be read from the HandledStamp via $envelope->last(HandledStamp::class)->getResult(), and messages that exhaust max_retries go to the configured failure transport, not into the void.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html)

??? question "4. What is the purpose of DispatchAfterCurrentBusStamp?"
    **✅ Defer delivery of a message dispatched inside a handler until the current handling finishes successfully**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them. It has nothing to do with delays, multi-bus fan-out, or retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/dispatch_after_current_bus.html)

??? question "5. A dispatched message throws NoHandlerForMessageException. What is the most likely cause?"
    **✅ The handler class is missing #[AsMessageHandler] (or its __invoke argument type does not match the message)**

    Handlers are discovered by autoconfiguration of the #[AsMessageHandler] attribute and matched by the typed argument of __invoke(). Missing the attribute (or a mismatched/imported type) means no handler is registered. Worker state, failure transport and message immutability are unrelated to handler resolution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#registering-handlers)

??? question "6. Which statements about Messenger buses are correct? (choose 2)"
    **✅ The default bus service is messenger.bus.default ; You can define multiple buses, each with its own ordered middleware list**

    Messenger ships one default bus (messenger.bus.default) but supports many, each configured with its own middleware — so a command bus can wrap handlers in a transaction while an event bus does not. The command/query/ event convention is just that: a convention, not enforced by the code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/multiple_buses.html)

??? question "7. An order handler dispatches an 'order confirmed' email message, but the email is sent even when the surrounding DB transaction rolls back. What fixes this?"
    **✅ Dispatch the email message with DispatchAfterCurrentBusStamp so it is delivered only after the current handler finishes successfully**

    DispatchAfterCurrentBusStamp defers the inner dispatch until the current message finishes handling successfully, so a rollback cancels the email. A delay only postpones sending, the unrecoverable exception affects the email's own retries, and sync routing would send it immediately during the transaction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/dispatch_after_current_bus.html)

??? question "8. $envelope->last(HandledStamp::class) returns null. Which situation explains this best?"
    **✅ The message was routed to an async transport, so it has not been handled in this process yet**

    A handler that returns null still produces a HandledStamp (its result is null) — so last() returning null means no such stamp exists, i.e. the message was sent async and not handled here. dispatch() always returns an Envelope (never null), and HandledStamp is not query-bus-specific. This is why the nullsafe ?-> guards 'not handled here', distinct from 'handled, returned null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-getting-handler-results)

??? question "9. How do you retrieve a synchronous handler's return value after MessageBusInterface::dispatch()?"
    **✅ $envelope->last(HandledStamp::class)->getResult()**

    dispatch() returns an Envelope. For a single sync handler you read its result via the HandledStamp: $envelope->last(HandledStamp::class)->getResult(). Use HandleTrait to unwrap it in a query bus. Envelope has no getResult() and the bus does not cache a "last result".

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-getting-handler-results)

??? question "10. A message is routed to an async transport. During dispatch() in the web process, the handler…"
    **✅ does not run — SendMessageMiddleware serializes and sends it, stopping the bus**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later. It is not handled twice, and a running worker is irrelevant to the dispatching process. NoHandlerForMessageException only occurs when no handler exists for a synchronously handled message.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transports-async-queued-messages)

??? question "11. Which middleware locates and invokes the handler(s), adding a HandledStamp?"
    **✅ HandleMessageMiddleware**

    HandleMessageMiddleware resolves handlers for the message type, calls them, and records each result in a HandledStamp. SendMessageMiddleware only routes/sends to transports (and may stop the bus before Handle runs).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#middleware)

??? question "12. True or False: routing a message to the sync:// transport skips the middleware pipeline."
    **✅ False**

    False. sync:// still runs the full middleware stack (validation, transactions, handler discovery) — it simply handles the message immediately in the same process instead of enqueueing it. Treating sync:// as "no bus" is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transport-configuration)

??? question "13. In a custom middleware, code placed AFTER the $stack->next()->handle($envelope, $stack) call runs…"
    **✅ On the way out — after the inner middleware and the handler have executed**

    The middleware stack is a russian-doll chain: code before $stack->next()->handle() runs on the way in, and code after it runs on the way out once the rest of the pipeline (including the handler) has returned. This lets a middleware wrap the whole handling (e.g. open/commit a transaction).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#creating-your-own-middleware)

??? question "14. Inside a custom middleware, how do you pass the envelope on to the rest of the stack?"
    **✅ return $stack->next()->handle($envelope, $stack);**

    A MiddlewareInterface::handle() implementation calls $stack->next()->handle($envelope, $stack) to invoke the next middleware. Code before that call runs on the way in; code after it runs on the way out. Re-dispatching via the bus would restart the whole pipeline.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#creating-your-own-middleware)

??? question "15. DelayStamp(5000) delays delivery by how long?"
    **✅ 5000 milliseconds (5 seconds)**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds. The classic trap is to read it as seconds; the retry strategy's initial delay is likewise in milliseconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#delaying-messages)

??? question "16. Which serializer does a Messenger transport use by default to serialize the envelope?"
    **✅ PhpSerializer (native PHP serialize())**

    By default transports use Transport\\Serialization\\PhpSerializer, which calls PHP's serialize(). The Symfony Serializer transport serializer is opt-in and recommended for cross-language/cross-app interop, but it is not the default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#serializing-messages)

??? question "17. Which built-in transport handles a message immediately in the same process, without a queue?"
    **✅ The sync transport (DSN sync://)**

    sync:// processes the message synchronously during dispatch. in-memory:// keeps messages in memory for tests, while doctrine/amqp/redis are real asynchronous transports consumed by a worker.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transport-configuration)

??? question "18. In framework.messenger.routing, mapping App\Message\SmsNotification to 'async' means…"
    **✅ SendMessageMiddleware sends that message class to the 'async' transport instead of handling it in-process**

    routing maps a message class (or interface/parent) to one or more transport names. A routed message is serialized and sent to that transport rather than handled synchronously. A message with no routing entry is handled immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#routing-messages-to-a-transport)

??? question "19. Which transport is intended specifically for functional tests, asserting dispatched messages without a broker?"
    **✅ The in-memory transport (in-memory://), inspected via getSent()**

    in-memory:// keeps envelopes in memory instead of sending them, so a test can fetch the transport from the container and assert on getSent(). It is reset between tests via the messenger reset behaviour.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#testing)

??? question "20. After a deploy, long-running workers keep executing the old code. Which approach fixes this for zero-downtime deploys?"
    **✅ Run messenger:stop-workers on deploy and let a supervisor restart workers, ideally combined with --time-limit/--memory-limit**

    Workers bootstrap the kernel once and keep it in memory, so new code is only picked up after a restart. messenger:stop-workers signals running workers to finish the current message and exit; a process manager then restarts them with the new code. --time-limit/--memory-limit make them recycle regularly. The other options don't reload the worker's code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#deploying-to-production)

??? question "21. Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?"
    **✅ --limit (max messages) and --time-limit (max seconds), optionally with memory limits**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#deploying-to-production)

??? question "22. After a message exhausts its configured retries, where does it go?"
    **✅ To the configured failure transport**

    Once max_retries is reached the envelope is sent to the failure_transport, where messenger:failed:show/retry can inspect and requeue it. Without a failure transport the message would be lost, which is why configuring one is a best practice.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#saving-retrying-failed-messages)

??? question "23. How do you make a failing handler skip retries and go straight to the failure transport?"
    **✅ Throw UnrecoverableMessageHandlingException**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately. A handler's return value never influences retries, and there is no stopPropagation() on an Envelope.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

??? question "24. With retry_strategy delay: 1000 and multiplier: 2, what are the delays before the 1st, 2nd and 3rd retry?"
    **✅ 1000 ms, 2000 ms, 4000 ms (delay × multiplier per attempt)**

    MultiplierRetryStrategy multiplies the initial delay by the multiplier for each successive attempt: 1000, 1000×2=2000, 2000×2=4000 (capped by max_delay if set). It is exponential, not constant or linear, and starts at the configured delay, not delay×multiplier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

??? question "25. What information does a RedeliveryStamp carry on a retried message?"
    **✅ The current retry count (and timing), so the retry strategy knows how many attempts have happened**

    RedeliveryStamp records the retry count (and redelivery timestamp). The worker reads it to compare against max_retries and to compute the next delay via the retry strategy. Handler identity is on HandlerFailedStamp, not here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

??? question "26. Under a transport's retry_strategy, what does the 'multiplier' option control?"
    **✅ The factor by which the delay grows between successive retries (exponential backoff)**

    retry_strategy defines max_retries, delay (initial, ms), multiplier (delay is multiplied by this each attempt) and max_delay to cap it, producing exponential backoff before the failure transport is used.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

??? question "27. During messenger:consume, which event is dispatched when a handler throws an exception?"
    **✅ WorkerMessageFailedEvent**

    The worker loop dispatches WorkerMessageReceivedEvent, then on success WorkerMessageHandledEvent (ack) or on exception WorkerMessageFailedEvent (reject/retry). WorkerRunningEvent fires between receives and WorkerStoppedEvent on shutdown — neither signals a handler failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-events)

??? question "28. You need to tag every outgoing async message with a stamp right before it is handed to its transport, without touching every call site that dispatches it. Which event do you listen to, and why not a Worker* event?"
    **✅ SendMessageToTransportsEvent — it fires on the dispatch side, before the envelope reaches a transport, and setEnvelope() lets you rewrite it**

    SendMessageToTransportsEvent is raised by SendMessageMiddleware on the dispatching side, before the message is actually sent to any transport, and exposes setEnvelope() to rewrite it (e.g. add a stamp). The Worker* events all fire on the consuming side, inside a `messenger:consume` worker process — too late to affect what gets sent, and irrelevant for synchronous (non-transport) messages.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Messenger/Event/SendMessageToTransportsEvent.php)

---

<small>Back to [Flashcards](index.md) · [Messenger](../../messenger/index.md)</small>
