# Source Tours

Expert level means **"I've read it"**, not just "I've used it". The certification
loves questions that only the source can settle: *which event fires first*, *what
exception is thrown when no resolver matches*, *what the firewall does before the
authenticators run*. Source Tours are guided walkthroughs of the handful of files
where those answers live.

## What a tour is (and is not)

A tour is **not** a syllabus chapter. It does not re-teach the feature — the
regular chapters do that. A tour follows **one concrete path through real
Symfony 8.0 source code**, stop by stop, the way a debugger would step through
it. Each stop names the method you are "standing in", sketches what it does, and
points at the extension hook available right there.

## How to read a tour

1. **Open the linked source file side-by-side.** Every tour anchors on one or
   two files in the `8.0` branch of `symfony/symfony` on GitHub. Keep the real
   file open in a second tab or editor pane and scroll along as you read.
2. **The code in the tour is a sketch, the code on GitHub is the truth.** Tour
   snippets are *simplified sketches* — trimmed, renamed-for-clarity, stripped of
   edge cases. When a question hinges on an exact signature or exception class,
   trust the linked source.
3. **Walk stop by stop.** Each tour is a numbered sequence of "stops". Don't
   skim: at each stop, predict what happens next *before* reading on.

## The four tours

| Tour | One-line pitch |
| --- | --- |
| [HttpKernel::handle()](httpkernel-handle.md) | The ~100 lines every single Symfony response passes through — all eight kernel events in their natural habitat. |
| [ControllerResolver & ArgumentResolver](argument-resolver.md) | How a `_controller` string becomes a callable, and how each parameter wins (or loses) its value in the resolver chain. |
| [A Form's life](form-lifecycle.md) | From `createForm()` to `createView()`: the three data representations, the six form events, and where validation actually happens. |
| [A request crosses the Firewall](firewall-request-cycle.md) | The security listener chain on `kernel.request`: firewall matching, passports, badges, and the final access decision. |

## Reading tips

- **Follow one request in your head.** Pick a concrete scenario ("POST /login
  with a bad password", "GET /admin as anonymous") and trace *that* request
  through every stop. Abstract reading doesn't stick; a single traced request does.
- **Read var_dump-free.** Resist the urge to run the code. The exam is a
  read-and-reason exercise: practice deducing behaviour from the source alone —
  what is dispatched, what is returned, what is thrown.
- **Watch for extension points.** Every time the core dispatches an event, checks
  an interface, or iterates a tagged-service collection, that's a hook — and
  hooks are exam gold. Each tour ends with an *Extension points recap* table;
  try to reconstruct it from memory after your first read.
- **Note the order, always.** Most trap questions are ordering questions
  (events, transformers, listeners). When a tour numbers its stops, that
  numbering *is* the answer to a future question.

## Official References

- [symfony/symfony on GitHub (8.0 branch)](https://github.com/symfony/symfony/tree/8.0)
- [Symfony Docs — The HttpKernel Component](https://symfony.com/doc/current/components/http_kernel.html)
- [Symfony Docs — Events and Event Listeners](https://symfony.com/doc/current/event_dispatcher.html)

---
<small>Related: [Request Handling](../architecture/request-handling.md) ·
[Value Resolvers](../controllers/value-resolvers.md) ·
[Form Events](../forms/events.md) ·
[Firewalls](../security/firewalls.md)</small>
