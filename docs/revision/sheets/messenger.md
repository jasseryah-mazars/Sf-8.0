# Revision Sheet — Messenger

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Messenger](../../messenger/index.md).

## Messenger Component
- Three roles: message (DTO), handler (`#[AsMessageHandler]`), bus
  (`MessageBusInterface::dispatch()`).
- `dispatch()` always returns an `Envelope`, never the handler's raw value.
- A message needs no interface or base class — any plain object works.
- The seven core FQCNs above map to the rest of this stage's chapters.

**Cheat:** `#[AsMessageHandler]` on an `__invoke(MessageType $m)` service. `dispatch($msg): Envelope` — never `null`, never the raw handler value. Message = plain object, no interface required. Core FQCNs: `MessageBusInterface`, `Envelope`, `StampInterface`, `AsMessageHandler`, `MiddlewareInterface`, `TransportInterface`, `Worker`.

## Events
- Six worker events (`Started`/`MessageReceived`/`MessageHandled`/
  `MessageFailed`/`Running`/`Stopped`), plus `WorkerRateLimitedEvent`, fire
  inside a `messenger:consume` process.
- `SendMessageToTransportsEvent` is the odd one out: dispatch-side, before
  any worker, and rewritable via `setEnvelope()`.
- `WorkerMessageFailedEvent` exposes `getThrowable()`/`willRetry()`/`setForRetry()`.
- All `Worker*` events share `getEnvelope()`/`getReceiverName()`/`addStamps()`
  via `AbstractWorkerMessageEvent`.

**Cheat:** Worker events: `Started → MessageReceived → (MessageHandled | MessageFailed)`, `Running` per loop iteration, `Stopped` on shutdown, `RateLimited` when throttled. `SendMessageToTransportsEvent` — dispatch-side, pre-send, `setEnvelope()` to rewrite. `WorkerMessageFailedEvent`: `getThrowable()`, `willRetry()`, `setForRetry()`. Shared base: `AbstractWorkerMessageEvent` (`getEnvelope`, `getReceiverName`, `addStamps`).

## Messages & Handlers
- Command bus: 1 handler, no return value. Query bus: 1 handler, result via
  `HandledStamp`. Event bus: 0–N handlers.
- `dispatch()` never returns the handler's value directly, on any bus kind.
- `DispatchAfterCurrentBusStamp` defers a nested dispatch until the current
  message succeeds — the standard fix for "event fired before commit."
- A missing handler is a hard error (`NoHandlerForMessageException`) unless
  the bus explicitly allows zero handlers.

**Cheat:** Command: 1 handler, no result. Query: 1 handler, result via `->last(HandledStamp::class)?->getResult()`. Event: 0–N handlers. `DispatchAfterCurrentBusStamp` — defer until current message succeeds. No handler → `NoHandlerForMessageException` unless `allow_no_handlers: true`. Buses have **independent** middleware lists.

## Middleware
- The middleware stack is a russian-doll chain: `$stack->next()->handle()`
  runs the rest, and code after it runs on the way back out.
- `SendMessageMiddleware` (routes/sends, may stop the chain) and
  `HandleMessageMiddleware` (calls handlers) are the two pivotal built-ins.
- `Envelope` is immutable; `with()` returns a new instance, `last()` reads
  the most recent stamp of a type (or `null`).
- `sync://` still runs the full pipeline — it just never diverts away from
  the handler.

**Cheat:** Chain: `$stack->next()->handle($envelope, $stack)` — russian-doll. `SendMessageMiddleware` → may add `SentStamp` + stop. `HandleMessageMiddleware` → adds `HandledStamp`. `Envelope::with()` = new instance. `Envelope::last(Class::class)` = most recent stamp or `null`. `DelayStamp` unit = **milliseconds**.

## Retries & Failures
- Retries follow exponential backoff: `delay × multiplier^attempt`.
- `HandlerFailedStamp` wraps the exception; `RedeliveryStamp` tracks retry
  count; exhausted retries land in the failure transport.
- `UnrecoverableMessageHandlingException` skips retries entirely.
- Messenger's delivery contract is at-least-once — handlers must be idempotent.

**Cheat:** `retry_strategy: { max_retries, delay, multiplier, jitter }` — exponential backoff, ±`jitter` randomization (default `0.1`; set `0` for exact delays). Exhausted → `failure_transport`; inspect with `messenger:failed:show|retry|remove`. `UnrecoverableMessageHandlingException` = no retry, straight to failure transport. `RedeliveryStamp` absent = first attempt, not "0 retries." Delivery guarantee: **at-least-once**, never exactly-once.

## Transports
- A transport is a DSN-configured `TransportInterface`; routing maps a
  message class to one or more transport names.
- `sync://` still runs the full pipeline, just in-process; unrouted
  messages behave the same way implicitly.
- Default serializer: `PhpSerializer`; Symfony Serializer is the
  interoperable alternative.
- Doctrine/Redis/AMQP/Amazon SQS transports are excluded from the exam.

**Cheat:** DSN schemes: `sync://`, `doctrine://`, `amqp://`, `redis://`, `in-memory://` (tests). `framework.messenger.routing`: `FQCN: transport-name`. Default serializer: `PhpSerializer`; opt-in: `messenger.transport.symfony_serializer`. No routing entry ⇒ handled synchronously, not an error. Third-party transports (Doctrine/Redis/AMQP/SQS) — **out of scope**.

## Workers
- The worker loop: receive → dispatch (with `ReceivedStamp`) → ack/reject.
- Workers never auto-reload code; recycle them on every deploy.
- `--limit`/`--time-limit`/`--memory-limit` and `messenger:stop-workers` are
  the graceful recycling tools; none of them interrupt an in-flight message.
- A worker with nothing to consume is a normal steady state, not an error.

**Cheat:** `messenger:consume <transport> --limit --time-limit --memory-limit`. `messenger:stop-workers` — graceful, between-message stop signal. Worker adds `ReceivedStamp`; loop is receive → dispatch → ack/reject. Old code keeps running until the worker process is recycled.
