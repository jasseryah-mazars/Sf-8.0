# Chapter Exam — Messenger

!!! abstract "How to use"
    28 questions spanning every subchapter of **Messenger**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Messenger](../messenger/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Cette page est une **banque de 28 questions type QCM** sur Messenger, avec correction dépliable sous chaque question. Ce n'est pas un cours : c'est un entraînement, à faire après avoir lu le chapitre.

**Pourquoi ça existe ?** Lire un chapitre donne l'impression d'avoir compris, mais répondre à une question sous forme d'examen (sans relire ses notes) révèle les vraies lacunes — c'est ce que fera l'examen officiel.

**🏠 Analogie de la vraie vie :** C'est le **permis de conduire**. Le code de la route (le cours) explique les règles ; les séries de questions du permis blanc (cette page) vérifient que tu sais les appliquer sous forme de question piège, sans l'aide du livre.

**Symfony dans la vraie vie :** Cours du chapitre → code de la route appris / Question du QCM → question du permis blanc / Réponse dépliable → correction avec explication / Score obtenu → indicateur "prêt à passer l'examen ou pas".

**⚠️ Erreur fréquente :** Déplier la réponse avant d'avoir vraiment tranché son choix. Le cerveau retient beaucoup mieux une explication lue *après* s'être trompé (ou avoir hésité) que lue en passant, sans effort de rappel préalable.

**🧠 Comment le mémoriser :** *« Je réponds d'abord, je vérifie ensuite »* — jamais l'inverse. Note les questions ratées : ce sont exactement les pièges que l'examinateur pose aussi.

---

**Q1.** What does MessageBusInterface::dispatch() return?  <small>_(easy · trap)_</small>

- A. An Envelope
- B. The handler's return value
- C. void
- D. A HandledStamp

??? success "Answer Q1"
    **A**

    dispatch() always returns the (possibly stamped) Envelope. A handler's return value is available via $envelope->last(HandledStamp::class)->getResult(). It never returns the value directly because a routed (async) message is not handled in this process at all — only the Envelope exists yet.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html)

**Q2.** Which attribute marks a service as a message handler in Symfony 8?  <small>_(easy · single)_</small>

- A. #[AsMessageHandler]
- B. #[MessageHandler]
- C. #[AsHandler]
- D. #[Handler]

??? success "Answer Q2"
    **A**

    Symfony\\Component\\Messenger\\Attribute\\AsMessageHandler registers an invokable service (or a specific method) as a handler for its typed message argument. The other names do not exist in the component.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#registering-handlers)

**Q3.** True or False: routing a message to the sync:// transport skips the middleware pipeline.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q3"
    **B**

    False. sync:// still runs the full middleware stack (validation, transactions, handler discovery) — it simply handles the message immediately in the same process instead of enqueueing it. Treating sync:// as "no bus" is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transport-configuration)

**Q4.** DelayStamp(5000) delays delivery by how long?  <small>_(easy · trap)_</small>

- A. 5000 milliseconds (5 seconds)
- B. 5000 seconds
- C. 5000 microseconds
- D. 5000 minutes

??? success "Answer Q4"
    **A**

    DelayStamp is expressed in milliseconds, so 5000 means 5 seconds. The classic trap is to read it as seconds; the retry strategy's initial delay is likewise in milliseconds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#delaying-messages)

**Q5.** Which built-in transport handles a message immediately in the same process, without a queue?  <small>_(easy · single)_</small>

- A. The sync transport (DSN sync://)
- B. The in-memory transport (in-memory://)
- C. The doctrine transport (doctrine://default)
- D. The amqp transport (amqp://...)

??? success "Answer Q5"
    **A**

    sync:// processes the message synchronously during dispatch. in-memory:// keeps messages in memory for tests, while doctrine/amqp/redis are real asynchronous transports consumed by a worker.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transport-configuration)

**Q6.** A dispatched message throws NoHandlerForMessageException. What is the most likely cause?  <small>_(medium · debug)_</small>

- A. The handler class is missing #[AsMessageHandler] (or its __invoke argument type does not match the message)
- B. The worker is not running
- C. The failure transport is not configured
- D. The message is not readonly

??? success "Answer Q6"
    **A**

    Handlers are discovered by autoconfiguration of the #[AsMessageHandler] attribute and matched by the typed argument of __invoke(). Missing the attribute (or a mismatched/imported type) means no handler is registered. Worker state, failure transport and message immutability are unrelated to handler resolution.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#registering-handlers)

**Q7.** An order handler dispatches an 'order confirmed' email message, but the email is sent even when the surrounding DB transaction rolls back. What fixes this?  <small>_(medium · scenario)_</small>

- A. Dispatch the email message with DispatchAfterCurrentBusStamp so it is delivered only after the current handler finishes successfully
- B. Add a DelayStamp so the email is sent 5 seconds later
- C. Throw UnrecoverableMessageHandlingException in the email handler
- D. Route the email to the sync:// transport

??? success "Answer Q7"
    **A**

    DispatchAfterCurrentBusStamp defers the inner dispatch until the current message finishes handling successfully, so a rollback cancels the email. A delay only postpones sending, the unrecoverable exception affects the email's own retries, and sync routing would send it immediately during the transaction.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/dispatch_after_current_bus.html)

**Q8.** How do you retrieve a synchronous handler's return value after MessageBusInterface::dispatch()?  <small>_(medium · code)_</small>

- A. $envelope->last(HandledStamp::class)->getResult()
- B. The value is returned directly by dispatch()
- C. $envelope->getResult()
- D. $bus->getLastResult()

??? success "Answer Q8"
    **A**

    dispatch() returns an Envelope. For a single sync handler you read its result via the HandledStamp: $envelope->last(HandledStamp::class)->getResult(). Use HandleTrait to unwrap it in a query bus. Envelope has no getResult() and the bus does not cache a "last result".

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-getting-handler-results)

**Q9.** A message is routed to an async transport. During dispatch() in the web process, the handler…  <small>_(medium · trap)_</small>

- A. does not run — SendMessageMiddleware serializes and sends it, stopping the bus
- B. runs immediately and is also queued
- C. runs only if a worker is currently active
- D. throws NoHandlerForMessageException

??? success "Answer Q9"
    **A**

    When a message is routed to a transport, SendMessageMiddleware adds a SentStamp, sends the envelope and stops the pipeline; a worker handles it later. It is not handled twice, and a running worker is irrelevant to the dispatching process. NoHandlerForMessageException only occurs when no handler exists for a synchronously handled message.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#transports-async-queued-messages)

**Q10.** Which middleware locates and invokes the handler(s), adding a HandledStamp?  <small>_(medium · internals)_</small>

- A. HandleMessageMiddleware
- B. SendMessageMiddleware
- C. DispatchAfterCurrentBusMiddleware
- D. ValidationMiddleware

??? success "Answer Q10"
    **A**

    HandleMessageMiddleware resolves handlers for the message type, calls them, and records each result in a HandledStamp. SendMessageMiddleware only routes/sends to transports (and may stop the bus before Handle runs).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#middleware)

**Q11.** In framework.messenger.routing, mapping App\Message\SmsNotification to 'async' means…  <small>_(medium · config)_</small>

- A. SendMessageMiddleware sends that message class to the 'async' transport instead of handling it in-process
- B. The handler is renamed to 'async'
- C. The message is handled by every transport named async
- D. It only affects messages dispatched from the CLI

??? success "Answer Q11"
    **A**

    routing maps a message class (or interface/parent) to one or more transport names. A routed message is serialized and sent to that transport rather than handled synchronously. A message with no routing entry is handled immediately.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#routing-messages-to-a-transport)

**Q12.** Which transport is intended specifically for functional tests, asserting dispatched messages without a broker?  <small>_(medium · single)_</small>

- A. The in-memory transport (in-memory://), inspected via getSent()
- B. The sync transport (sync://)
- C. The redis transport (redis://localhost)
- D. The doctrine transport

??? success "Answer Q12"
    **A**

    in-memory:// keeps envelopes in memory instead of sending them, so a test can fetch the transport from the container and assert on getSent(). It is reset between tests via the messenger reset behaviour.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#testing)

**Q13.** After a deploy, long-running workers keep executing the old code. Which approach fixes this for zero-downtime deploys?  <small>_(medium · scenario)_</small>

- A. Run messenger:stop-workers on deploy and let a supervisor restart workers, ideally combined with --time-limit/--memory-limit
- B. Restart the database so workers reconnect with new code
- C. Add a DelayStamp to every message
- D. Increase max_retries so old workers eventually give up

??? success "Answer Q13"
    **A**

    Workers bootstrap the kernel once and keep it in memory, so new code is only picked up after a restart. messenger:stop-workers signals running workers to finish the current message and exit; a process manager then restarts them with the new code. --time-limit/--memory-limit make them recycle regularly. The other options don't reload the worker's code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#deploying-to-production)

**Q14.** Which options let 'messenger:consume' stop a worker gracefully for zero-downtime deploys?  <small>_(medium · scenario)_</small>

- A. --limit (max messages) and --time-limit (max seconds), optionally with memory limits
- B. --kill and --restart
- C. --stop-now only
- D. --reload after each message

??? success "Answer Q14"
    **A**

    A long-running worker is stopped cleanly with --limit / --time-limit (and --memory-limit). Combined with a process manager and messenger:stop-workers, this enables graceful restarts on deploy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#deploying-to-production)

**Q15.** After a message exhausts its configured retries, where does it go?  <small>_(medium · single)_</small>

- A. To the configured failure transport
- B. To the sync transport
- C. It is silently discarded
- D. Back to the front of the same queue forever

??? success "Answer Q15"
    **A**

    Once max_retries is reached the envelope is sent to the failure_transport, where messenger:failed:show/retry can inspect and requeue it. Without a failure transport the message would be lost, which is why configuring one is a best practice.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#saving-retrying-failed-messages)

**Q16.** How do you make a failing handler skip retries and go straight to the failure transport?  <small>_(medium · scenario)_</small>

- A. Throw UnrecoverableMessageHandlingException
- B. Return false from the handler
- C. Add a DelayStamp(0)
- D. Call $envelope->stopPropagation()

??? success "Answer Q16"
    **A**

    UnrecoverableMessageHandlingException marks the failure as non-retryable, so the worker sends the message to the failure transport immediately. A handler's return value never influences retries, and there is no stopPropagation() on an Envelope.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

**Q17.** What information does a RedeliveryStamp carry on a retried message?  <small>_(medium · internals)_</small>

- A. The current retry count (and timing), so the retry strategy knows how many attempts have happened
- B. The DSN of the failure transport
- C. The fully-qualified class name of the handler that failed
- D. A cryptographic signature of the payload

??? success "Answer Q17"
    **A**

    RedeliveryStamp records the retry count (and redelivery timestamp). The worker reads it to compare against max_retries and to compute the next delay via the retry strategy. Handler identity is on HandlerFailedStamp, not here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

**Q18.** Under a transport's retry_strategy, what does the 'multiplier' option control?  <small>_(medium · config)_</small>

- A. The factor by which the delay grows between successive retries (exponential backoff)
- B. The number of parallel workers spawned
- C. How many transports share the message
- D. The maximum number of messages fetched per poll

??? success "Answer Q18"
    **A**

    retry_strategy defines max_retries, delay (initial, ms), multiplier (delay is multiplied by this each attempt) and max_delay to cap it, producing exponential backoff before the failure transport is used.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

**Q19.** During messenger:consume, which event is dispatched when a handler throws an exception?  <small>_(medium · internals)_</small>

- A. WorkerMessageFailedEvent
- B. WorkerMessageHandledEvent
- C. WorkerStoppedEvent
- D. WorkerRunningEvent

??? success "Answer Q19"
    **A**

    The worker loop dispatches WorkerMessageReceivedEvent, then on success WorkerMessageHandledEvent (ack) or on exception WorkerMessageFailedEvent (reject/retry). WorkerRunningEvent fires between receives and WorkerStoppedEvent on shutdown — neither signals a handler failure.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-events)

**Q20.** Which of the following statements are true about Symfony Messenger? (select all that apply)  <small>_(hard · multiple)_</small>

- A. MessageBusInterface::dispatch() always returns an Envelope, never the handler's return value directly
- B. When a message is routed to an async transport, SendMessageMiddleware enqueues it and stops the bus, so no handler runs in the dispatching process
- C. DelayStamp(5000) delays delivery by 5000 milliseconds (5 seconds)
- D. dispatch() returns the handler's result so a query bus needs no stamps
- E. Once a message exhausts its retries, it is silently discarded

??? success "Answer Q20"
    **A, B, C**

    dispatch() returns the (possibly stamped) Envelope, routed-async messages are serialized and sent without invoking the handler in-process, and DelayStamp is expressed in milliseconds. A query result must be read from the HandledStamp via $envelope->last(HandledStamp::class)->getResult(), and messages that exhaust max_retries go to the configured failure transport, not into the void.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html)

**Q21.** What is the purpose of DispatchAfterCurrentBusStamp?  <small>_(hard · internals)_</small>

- A. Defer delivery of a message dispatched inside a handler until the current handling finishes successfully
- B. Send the message to every bus in the application
- C. Add a delay equal to the current bus latency
- D. Retry the message on the next bus in a chain

??? success "Answer Q21"
    **A**

    It prevents dispatching side-effect messages (e.g. a confirmation email) before the surrounding work commits, so a failure/rollback cancels them. It has nothing to do with delays, multi-bus fan-out, or retries.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/dispatch_after_current_bus.html)

**Q22.** Which statements about Messenger buses are correct? (choose 2)  <small>_(hard · multiple)_</small>

- A. The default bus service is messenger.bus.default
- B. You can define multiple buses, each with its own ordered middleware list
- C. All buses in an app must share a single global middleware list
- D. The command/query/event bus split is enforced by the component

??? success "Answer Q22"
    **A, B**

    Messenger ships one default bus (messenger.bus.default) but supports many, each configured with its own middleware — so a command bus can wrap handlers in a transaction while an event bus does not. The command/query/ event convention is just that: a convention, not enforced by the code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger/multiple_buses.html)

**Q23.** $envelope->last(HandledStamp::class) returns null. Which situation explains this best?  <small>_(hard · trap)_</small>

- A. The message was routed to an async transport, so it has not been handled in this process yet
- B. The handler returned null, so no HandledStamp was created
- C. dispatch() failed and returned null instead of an Envelope
- D. HandledStamp only exists on the query bus

??? success "Answer Q23"
    **A**

    A handler that returns null still produces a HandledStamp (its result is null) — so last() returning null means no such stamp exists, i.e. the message was sent async and not handled here. dispatch() always returns an Envelope (never null), and HandledStamp is not query-bus-specific. This is why the nullsafe ?-> guards 'not handled here', distinct from 'handled, returned null'.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#messenger-getting-handler-results)

**Q24.** In a custom middleware, code placed AFTER the $stack->next()->handle($envelope, $stack) call runs…  <small>_(hard · internals)_</small>

- A. On the way out — after the inner middleware and the handler have executed
- B. Never — the call terminates the middleware
- C. Before any other middleware in the stack
- D. Only if the message was routed async

??? success "Answer Q24"
    **A**

    The middleware stack is a russian-doll chain: code before $stack->next()->handle() runs on the way in, and code after it runs on the way out once the rest of the pipeline (including the handler) has returned. This lets a middleware wrap the whole handling (e.g. open/commit a transaction).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#creating-your-own-middleware)

**Q25.** Inside a custom middleware, how do you pass the envelope on to the rest of the stack?  <small>_(hard · code)_</small>

- A. return $stack->next()->handle($envelope, $stack);
- B. return $this->bus->dispatch($envelope);
- C. return $stack->handle($envelope);
- D. $envelope->next();

??? success "Answer Q25"
    **A**

    A MiddlewareInterface::handle() implementation calls $stack->next()->handle($envelope, $stack) to invoke the next middleware. Code before that call runs on the way in; code after it runs on the way out. Re-dispatching via the bus would restart the whole pipeline.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#creating-your-own-middleware)

**Q26.** Which serializer does a Messenger transport use by default to serialize the envelope?  <small>_(hard · single)_</small>

- A. PhpSerializer (native PHP serialize())
- B. The Symfony Serializer component
- C. JsonEncoder
- D. igbinary

??? success "Answer Q26"
    **A**

    By default transports use Transport\\Serialization\\PhpSerializer, which calls PHP's serialize(). The Symfony Serializer transport serializer is opt-in and recommended for cross-language/cross-app interop, but it is not the default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#serializing-messages)

**Q27.** With retry_strategy delay: 1000 and multiplier: 2, what are the delays before the 1st, 2nd and 3rd retry?  <small>_(hard · config)_</small>

- A. 1000 ms, 2000 ms, 4000 ms (delay × multiplier per attempt)
- B. 1000 ms, 1000 ms, 1000 ms (constant)
- C. 2000 ms, 4000 ms, 8000 ms
- D. 1 s, 2 s, 3 s (linear)

??? success "Answer Q27"
    **A**

    MultiplierRetryStrategy multiplies the initial delay by the multiplier for each successive attempt: 1000, 1000×2=2000, 2000×2=4000 (capped by max_delay if set). It is exponential, not constant or linear, and starts at the configured delay, not delay×multiplier.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/messenger.html#retries-failures)

**Q28.** You need to tag every outgoing async message with a stamp right before it is handed to its transport, without touching every call site that dispatches it. Which event do you listen to, and why not a Worker* event?  <small>_(hard · scenario)_</small>

- A. SendMessageToTransportsEvent — it fires on the dispatch side, before the envelope reaches a transport, and setEnvelope() lets you rewrite it
- B. WorkerMessageReceivedEvent — it fires earliest, before anything else happens to the message
- C. WorkerRunningEvent — it fires once per worker loop iteration, covering every message
- D. WorkerMessageHandledEvent — tagging after handling still reaches the transport in time

??? success "Answer Q28"
    **A**

    SendMessageToTransportsEvent is raised by SendMessageMiddleware on the dispatching side, before the message is actually sent to any transport, and exposes setEnvelope() to rewrite it (e.g. add a stamp). The Worker* events all fire on the consuming side, inside a `messenger:consume` worker process — too late to affect what gets sent, and irrelevant for synchronous (non-transport) messages.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Messenger/Event/SendMessageToTransportsEvent.php)

---

<small>Back to [Chapter Exams](index.md) · [Messenger](../messenger/index.md)</small>
