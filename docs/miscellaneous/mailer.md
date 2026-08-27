# Mime & Mailer Components

!!! tip "In a nutshell"
    Mime builds an email as a tree of parts; Mailer sends it through a transport
    chosen by `MAILER_DSN`. Build an `Email`/`TemplatedEmail`, call
    `MailerInterface::send()`. Exam gold: once `SendEmailMessage` is routed via
    Messenger, `send()` queues the mail instead of delivering it inline.

!!! example "Real-world analogy"
    Think of a **mailroom**. Mime **assembles the envelope and its enclosures** —
    the letter (text/HTML), photos and attachments nested in the right order.
    Mailer is the **clerk who hands it to a carrier** chosen by `MAILER_DSN`
    (SMTP, a provider API…). Routing `SendEmailMessage` via Messenger is dropping
    it in the **outbox** for a courier to collect later, so you don't wait at the
    counter.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Build an `Email`/`TemplatedEmail` with the Mime part model.
    - [ ] Send via `MailerInterface` over a transport DSN.
    - [ ] Add attachments/embeds and send asynchronously via Messenger.

    **Syllabus:** `Miscellaneous → Mailer` ·
    **Level:** Advanced ·
    **Est. time:** 40 min ·
    **Prerequisites:** [Twig](../twig/index.md), [Messenger](../messenger/index.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
Mime construit l'email (texte, HTML, pièces jointes) ; Mailer l'envoie via un transport choisi par une seule variable d'environnement.

### Imagine dans la vraie vie
Une salle de courrier. Mime **assemble l'enveloppe et son contenu** — la lettre (texte/HTML), les photos et pièces jointes imbriquées dans le bon ordre. Mailer est le **commis qui la remet à un transporteur** choisi par `MAILER_DSN`.

### Dans Symfony
Changer `MAILER_DSN` de `smtp://...` à un service tiers ne nécessite **aucun** changement dans le code qui construit et envoie l'email — seule la configuration change, jamais le code métier.

### Exemple simple
```php
$email = (new TemplatedEmail())->to($destinataire)->htmlTemplate('email/bienvenue.html.twig');
$mailer->send($email);
```

### Comment le mémoriser 🧠
Une fois `SendEmailMessage` routé via Messenger, `send()` **met en file d'attente** au lieu d'envoyer immédiatement — l'email part seulement quand un worker consomme le message.

---

## Theory

The **Mime** component models an email message as a tree of **parts** (text,
HTML, attachments) that serialise to a MIME string. The **Mailer** component
sends that message through a **transport** chosen by a DSN. You build a message
(`Email`), hand it to `MailerInterface::send()`, and the transport delivers it.

```php
use Symfony\Component\Mailer\MailerInterface;
use Symfony\Component\Mime\Email;

$email = (new Email())           // Mime: build the message
    ->from('no-reply@example.com')
    ->to('ada@example.com')
    ->subject('Hello')
    ->text('Plain body')
    ->html('<p>HTML body</p>');

$mailer->send($email);           // Mailer: delivered by the MAILER_DSN transport
```

## Deep Dive — how it works internally

!!! question "Predict first"
    Messenger is configured to route `SendEmailMessage` to `async`. You call
    `$mailer->send($email)`. Has the email left the building when `send()` returns?

??? note "Reveal"
    No. With routing configured, `send()` **dispatches** a `SendEmailMessage` to the
    queue and returns; a worker delivers it later. If no worker runs, the mail sits
    in the queue — nothing was sent inline.

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

```php
use Symfony\Component\Mime\Email;
use Symfony\Component\Mime\Part\DataPart;
use Symfony\Component\Mime\Part\File;

$email = (new Email())
    ->text('Plain-text body')                             // TextPart (text/plain)
    ->html('<p>Hi <img src="cid:logo"></p>')              // TextPart (text/html)
    ->addPart(new DataPart(new File('/data/report.csv'))) // manual DataPart
    ->attachFromPath('/data/guide.pdf', 'guide.pdf')      // attachment DataPart
    ->embedFromPath('/img/logo.png', 'logo');             // embedded, used as cid:logo
```

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

```php
use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mailer\Transport;

// Transport::fromDsn() builds a TransportInterface (usually from MAILER_DSN)
$transport = Transport::fromDsn('smtp://user:pass@mail.example.com:465');
$mailer = new Mailer($transport);
$mailer->send($email); // send(RawMessage $message, ?Envelope $envelope = null)
```

The Mailer's `Envelope` (sender + recipients) is distinct from the message
headers; the transport uses the envelope for the SMTP conversation while headers
render in the visible message.

```php
use Symfony\Component\Mailer\Envelope;
use Symfony\Component\Mime\Address;

// The Envelope drives the SMTP conversation, not the visible headers
$envelope = new Envelope(
    new Address('bounces@example.com'),          // MAIL FROM
    [new Address('real-recipient@example.com')]  // RCPT TO (may differ from To:)
);
$mailer->send($email, $envelope);
```

### TemplatedEmail

`Symfony\Bridge\Twig\Mime\TemplatedEmail` extends `Email` with
`htmlTemplate()`/`textTemplate()` + `context()`. A Twig-aware
`BodyRenderer`/`MessageListener` renders the templates into html/text parts
before sending — so you never call Twig yourself.

```php
use Symfony\Bridge\Twig\Mime\TemplatedEmail;

$email = (new TemplatedEmail())
    ->to('ada@example.com')
    ->htmlTemplate('emails/welcome.html.twig') // rendered by the BodyRenderer
    ->textTemplate('emails/welcome.txt.twig')  // via MessageListener, before sending
    ->context(['name' => 'Ada']);              // variables exposed to Twig
```

### Async sending via Messenger

If Messenger is configured to route `Symfony\Component\Mailer\Messenger\SendEmailMessage`
to a transport, `MailerInterface::send()` **dispatches** it instead of sending
inline; a worker delivers it later. This keeps request latency low and gives
retries/failure handling for free. See [Messenger](../messenger/index.md).

```yaml
# config/packages/messenger.yaml
framework:
    messenger:
        routing:
            # MailerInterface::send() now dispatches SendEmailMessage to "async"
            Symfony\Component\Mailer\Messenger\SendEmailMessage: async
```

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

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. `MailerInterface::send()` with Messenger routing configured…"
    - [x] A. dispatches a `SendEmailMessage` to be delivered by a worker ✅
    - [ ] B. always sends synchronously
    - [ ] C. throws if no worker is running

    **Why:** Routing `SendEmailMessage` async makes `send()` enqueue it.
    **Ref:** [Sending messages async](https://symfony.com/doc/8.0/mailer.html#sending-messages-async).

??? question "Q2. Which class renders Twig templates into an email?"
    - [x] A. `Symfony\Bridge\Twig\Mime\TemplatedEmail` ✅
    - [ ] B. `Symfony\Component\Mime\Email`
    - [ ] C. `Symfony\Component\Mailer\Mailer`

    **Why:** `TemplatedEmail` (Twig bridge) carries the template + context.
    **Ref:** [HTML content](https://symfony.com/doc/8.0/mailer.html#twig-html-css).

??? question "Q3. How are inline images referenced in the HTML body?"
    - [x] A. via a `cid:` reference from `embedFromPath()`/`embed()` ✅
    - [ ] B. as external URLs only
    - [ ] C. they cannot be inlined

    **Why:** Embedded parts are addressed with `cid:<name>`. **Ref:** [Embedding images](https://symfony.com/doc/8.0/mailer.html#embedding-images).

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

## Connections

- **Depends on:** [Messenger](../messenger/index.md) — async delivery routes `SendEmailMessage`; [Twig](../twig/index.md) renders `TemplatedEmail`.
- **Reused in:** [Console](../console/index.md) — `messenger:consume` is what actually delivers queued mail.
- **Confused with:** the Mailer `Envelope` (sender/recipients for the SMTP conversation) vs the visible message headers.

## Official References
- [Official docs — Mailer](https://symfony.com/doc/8.0/mailer.html)
- [Official docs — Mime](https://symfony.com/doc/8.0/components/mime.html)
- [Symfony source — Mailer](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Mailer/Mailer.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony components" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/mailer.html#sending-messages-async) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** the Mime part tree models alternative/mixed/related bodies
- [ ] build and send a `TemplatedEmail` with an attachment/embed in Symfony 8
- [ ] debug "async email never arrives" (no worker consuming the transport)
- [ ] spot the trick: with routing, `send()` queues `SendEmailMessage`, not sends inline
- [ ] describe transport DSN selection and `Envelope` vs headers

---

<small>Related: [Messenger](../messenger/index.md) · [Twig](../twig/index.md) · [Serializer](serializer.md)</small>
