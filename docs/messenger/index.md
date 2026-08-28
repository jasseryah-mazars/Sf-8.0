# Messenger

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Messenger Middleware](../labs/miscellaneous.md)** — a step-by-step TD with test-first guidance and a reference solution.

**Messenger** lets you send plain PHP objects (messages) through a bus to
handlers, so slow or side-effecting work can run later in a background
worker instead of during the request. It is one of the highest-weighted
topics on the Symfony 8 syllabus — expect several exam questions per
sub-topic below, not just one or two.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [DI & Tags](../dependency-injection/index.md), [Console](../console/index.md), [Events](../architecture/events.md) |
    | **Level** | Expert |
    | **Difficulty** | ★★★ |
    | **Dependencies** | DI (service discovery), Console (the worker *is* a command), Events (worker/dispatch events) |
    | **Revision priority** | **Critical** |
    | **Est. time** | 4–5 h |

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Messenger permet d'envoyer un "message" (un simple objet PHP) qui sera traité soit tout de suite, soit plus tard en arrière-plan par un worker — sans faire attendre le visiteur.

**Pourquoi ça existe ?** Certaines tâches (envoyer un email, générer un rapport) sont lentes. Sans Messenger, le visiteur attendrait que tout se termine avant de voir sa page s'afficher.

**🏠 Analogie de la vraie vie :** Un bureau de poste. Tu déposes une lettre (`dispatch()`) et reçois un reçu (l'`Envelope`) — pas une réponse immédiate. La lettre attend dans la salle de tri (le transport) jusqu'à ce qu'un facteur (le worker) la distribue enfin au destinataire (le handler).

**Symfony dans la vraie vie :** `$bus->dispatch(new EnvoyerEmailBienvenue($id))` répond instantanément à la requête HTTP ; l'email part réellement quelques secondes plus tard, traité par un worker en arrière-plan.

**⚠️ Erreur fréquente :** s'attendre à ce que `dispatch()` renvoie le résultat du traitement — il renvoie toujours une `Envelope` (un reçu), jamais la valeur calculée directement.

**🧠 Comment le mémoriser :** "Dispatch, c'est déposer une lettre — pas attendre la réponse au guichet."

## Why this stage matters

Messenger decouples *what* needs to happen from *when* and *where* it
happens: the same message can be handled synchronously in-process or
asynchronously by a worker consuming a queue, with zero change to the
message or handler code. The exam tests both the everyday API
(`dispatch()`, `#[AsMessageHandler]`) and the internals (the middleware
pipeline, stamps, retry strategy, worker events) — the certification traps
live almost entirely in the gap between "what `dispatch()` looks like" and
"what actually happens after it returns."

## Micro-chapters

Work through them in order:

- [ ] [Messenger Component](component.md) — messages, handlers, the bus, and
  the core classes that tie them together.
- [ ] [Messages & Handlers](messages-handlers.md) — `#[AsMessageHandler]`,
  command/query/event buses, reading a query result from a `HandledStamp`.
- [ ] [Middleware](middleware.md) — the middleware pipeline, envelopes and
  stamps, the two pivotal built-in middlewares.
- [ ] [Transports](transports.md) — DSN-configured transports, routing,
  serializers.
- [ ] [Workers](workers.md) — the `messenger:consume` lifecycle and
  graceful shutdown.
- [ ] [Retries & Failures](retries-failures.md) — retry strategies, the
  failure transport, `UnrecoverableMessageHandlingException`.
- [ ] [Events](events.md) — the worker and dispatch-side events Messenger
  fires around each step.

## How to study this stage

1. Read [Messenger Component](component.md) and
   [Messages & Handlers](messages-handlers.md) first — they establish the
   vocabulary (message, handler, bus, envelope) every later chapter assumes.
2. [Middleware](middleware.md) is the internals chapter the exam rewards
   most — know exactly what `SendMessageMiddleware` and
   `HandleMessageMiddleware` each do, and in what order.
3. [Transports](transports.md), [Workers](workers.md) and
   [Retries & Failures](retries-failures.md) form the operational trio:
   how a message gets queued, consumed, and recovered from failure.
4. Finish with [Events](events.md) — it ties the whole pipeline to the
   `EventDispatcher` you already know from
   [Architecture → Events](../architecture/index.md).

---

<small>Related: [Dependency Injection](../dependency-injection/index.md) ·
[Console](../console/index.md) · [Architecture → Events](../architecture/index.md) ·
[Mailer](../miscellaneous/mailer.md)</small>

## Official References

- [Symfony documentation — Messenger](https://symfony.com/doc/8.0/messenger.html)
- [Symfony source — Messenger component](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Component/Messenger)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
