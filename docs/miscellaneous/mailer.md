# Mime & Mailer Components

!!! tip "In a nutshell"
    Mime builds an email as a tree of parts; Mailer sends it through a transport
    chosen by `MAILER_DSN`. Build an `Email`/`TemplatedEmail`, call
    `MailerInterface::send()`. Exam gold: once `SendEmailMessage` is routed via
    Messenger, `send()` queues the mail instead of delivering it inline.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Build an `Email`/`TemplatedEmail` with the Mime part model.
    - [ ] Send via `MailerInterface` over a transport DSN.
    - [ ] Add attachments/embeds and send asynchronously via Messenger.

    **Syllabus:** `Miscellaneous → Mailer` ·
    **Level:** Advanced ·
    **Est. time:** 40 min ·
    **Prerequisites:** [Twig](../twig/index.md), [Messenger](messenger.md)

---

## Theory

The **Mime** component models an email message as a tree of **parts** (text,
HTML, attachments) that serialise to a MIME string. The **Mailer** component
sends that message through a **transport** chosen by a DSN. You build a message
(`Email`), hand it to `MailerInterface::send()`, and the transport delivers it.

## Deep Dive — how it works internally

### The Mime part model

`Symfony\Component\Mime\Email` is a high-level builder over
`Symfony\Component\Mime\Message`. Internally a message body is a tree of
`Symfony\Component\Mime\Part\AbstractPart` subclasses:

- `TextPart` — a body (text or html) with a media type.
- `DataPart` — an attachment or embedded resource.
- `Multipart\AlternativePart` / `Multipart\MixedPart` / `Multipart\RelatedPart`
  — containers that combine parts (alternative bodies, mixed attachments,
  related/embedded), all under `Symfony\Component\Mime\Part\Multipart\`.

`Email::text()`/`html()`/`addPart()` assemble this tree; `attachFromPath()` and
`embedFromPath()` add `DataPart`s. Embedded images are referenced via `cid:`.

```mermaid
flowchart LR
    E[Email] --> M[Mailer::send]
    M --> Env{async?}
    Env -->|routed| MSG[Messenger transport]
    Env -->|sync| T[Transport DSN]
    MSG -.worker.-> T
    T --> S[SMTP / API]
```

### Mailer + transports

`Symfony\Component\Mailer\MailerInterface::send(RawMessage $message, ?Envelope $envelope = null)`
is the entry point. `Symfony\Component\Mailer\Transport` builds a
`TransportInterface` from a **DSN**: `smtp://user:pass@host:port`,
`sendmail://default`, `native://default`, or third-party providers via bridges
(out of scope to teach). The `MAILER_DSN` env var configures it.

The Mailer's `Envelope` (sender + recipients) is distinct from the message
headers; the transport uses the envelope for the SMTP conversation while headers
render in the visible message.

### TemplatedEmail

`Symfony\Bridge\Twig\Mime\TemplatedEmail` extends `Email` with
`htmlTemplate()`/`textTemplate()` + `context()`. A Twig-aware
`BodyRenderer`/`MessageListener` renders the templates into html/text parts
before sending — so you never call Twig yourself.

### Async sending via Messenger

If Messenger is configured to route `Symfony\Component\Mailer\Messenger\SendEmailMessage`
to a transport, `MailerInterface::send()` **dispatches** it instead of sending
inline; a worker delivers it later. This keeps request latency low and gives
retries/failure handling for free. See [Messenger](messenger.md).

!!! note "Source reference"
    `Symfony\Component\Mailer\Mailer::send()` and `Symfony\Component\Mime\Email` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Mailer/Mailer.php).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Notifier;

    use Symfony\Bridge\Twig\Mime\TemplatedEmail;
    use Symfony\Component\Mailer\MailerInterface;
    use Symfony\Component\Mime\Address;

    final class WelcomeMailer
    {
        public function __construct(private readonly MailerInterface $mailer) {}

        public function welcome(string $to): void
        {
            $email = (new TemplatedEmail())
                ->from(new Address('no-reply@example.com', 'Acme'))
                ->to($to)
                ->subject('Welcome')
                ->htmlTemplate('emails/welcome.html.twig')
                ->context(['name' => 'Ada'])
                ->attachFromPath('/data/guide.pdf', 'guide.pdf')
                ->embedFromPath('/img/logo.png', 'logo');

            $this->mailer->send($email);
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/packages/mailer.yaml
    framework:
        mailer:
            dsn: '%env(MAILER_DSN)%'
    # config/packages/messenger.yaml — send emails async
    framework:
        messenger:
            routing:
                Symfony\Component\Mailer\Messenger\SendEmailMessage: async
    ```

=== "Console"

    ```console
    $ php bin/console messenger:consume async   # delivers queued emails
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Use `TemplatedEmail` + Twig for HTML mail | Hand-concatenating MIME strings |
| Route `SendEmailMessage` to async | Blocking the request on SMTP |
| Embed images via `embedFromPath()` (`cid:`) | Inlining base64 blobs manually |
| Configure `MAILER_DSN` per env | Hardcoding SMTP credentials |

## When (not) to use it / alternatives

Use Mailer for transactional email. For non-email channels (SMS, chat, push) the
Notifier component is the counterpart (not covered here). Always send async in
production unless the email must be confirmed before responding.

!!! danger "Certification traps"
    - The Mailer **`Envelope`** (sender/recipients) differs from message headers.
    - With Messenger routing, `send()` **queues** `SendEmailMessage` — it is not sent inline.
    - Embedded images use `embedFromPath()` and are referenced by `cid:`.
    - `TemplatedEmail` lives in the **Twig bridge** (`Symfony\Bridge\Twig\Mime`).

!!! warning "Common mistakes"
    - Expecting a template to render without `symfony/twig-bundle` present.
    - Forgetting to run a worker, so async emails never leave the queue.

## Exercises

1. **(Advanced)** Send a `TemplatedEmail` with an attachment and an embedded logo.
2. **(Advanced)** Configure the app to send emails asynchronously.

??? success "Solutions"

    **1.** See `WelcomeMailer::welcome()` — `attachFromPath()` + `embedFromPath()`.

    **2.** Route `Symfony\Component\Mailer\Messenger\SendEmailMessage` to an async
    transport in `messenger.yaml` (see YAML above) and run `messenger:consume`.

## Certification questions

??? question "Q1. `MailerInterface::send()` with Messenger routing configured…"
    - [x] A. dispatches a `SendEmailMessage` to be delivered by a worker ✅
    - [ ] B. always sends synchronously
    - [ ] C. throws if no worker is running

    **Why:** Routing `SendEmailMessage` async makes `send()` enqueue it.
    **Ref:** [Sending messages async](https://symfony.com/doc/current/mailer.html#sending-messages-async).

??? question "Q2. Which class renders Twig templates into an email?"
    - [x] A. `Symfony\Bridge\Twig\Mime\TemplatedEmail` ✅
    - [ ] B. `Symfony\Component\Mime\Email`
    - [ ] C. `Symfony\Component\Mailer\Mailer`

    **Why:** `TemplatedEmail` (Twig bridge) carries the template + context.
    **Ref:** [HTML content](https://symfony.com/doc/current/mailer.html#twig-html-css).

??? question "Q3. How are inline images referenced in the HTML body?"
    - [x] A. via a `cid:` reference from `embedFromPath()`/`embed()` ✅
    - [ ] B. as external URLs only
    - [ ] C. they cannot be inlined

    **Why:** Embedded parts are addressed with `cid:<name>`. **Ref:** [Embedding images](https://symfony.com/doc/current/mailer.html#embedding-images).

## Key takeaways

- Mime models a message as a tree of parts; `Email` is the builder.
- Mailer sends via a transport DSN (`MAILER_DSN`); `Envelope` ≠ headers.
- `TemplatedEmail` (Twig bridge) renders html/text templates.
- Route `SendEmailMessage` to Messenger for async delivery + retries.

## Last-minute revision

!!! tip "Cheat sheet"
    - `(new Email())->from()->to()->subject()->text()->html()`.
    - `attachFromPath()`, `embedFromPath()` (`cid:`), `addPart(new DataPart(...))`.
    - `MailerInterface::send($email)`; DSN via `MAILER_DSN`.
    - Async: route `SendEmailMessage` → transport; run `messenger:consume`.

## Official References
- [Official docs — Mailer](https://symfony.com/doc/current/mailer.html)
- [Official docs — Mime](https://symfony.com/doc/current/components/mime.html)
- [Symfony source — Mailer](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Mailer/Mailer.php)

---

<small>Related: [Messenger](messenger.md) · [Twig](../twig/index.md) · [Serializer](serializer.md)</small>
