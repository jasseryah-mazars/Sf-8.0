# Mime & Mailer Components

!!! tip "In a nutshell"
    Mime construit un email sous forme d'arbre de parts ; Mailer l'envoie via un
    transport choisi par `MAILER_DSN`. Construisez un `Email`/`TemplatedEmail`,
    appelez `MailerInterface::send()`. Or de l'examen : dès que `SendEmailMessage`
    est routé via Messenger, `send()` met le mail en file d'attente au lieu de le
    livrer immédiatement.

!!! example "Real-world analogy"
    Pensez à une **salle de courrier**. Mime **assemble l'enveloppe et son
    contenu** — la lettre (texte/HTML), les photos et les pièces jointes
    imbriquées dans le bon ordre. Mailer est **l'employé qui la remet à un
    transporteur** choisi par `MAILER_DSN` (SMTP, une API de fournisseur…).
    Router `SendEmailMessage` via Messenger revient à la déposer dans la **boîte
    de départ** pour qu'un coursier la récupère plus tard, sans que vous
    attendiez au guichet.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Construire un `Email`/`TemplatedEmail` avec le modèle de parts de Mime.
    - [ ] Envoyer via `MailerInterface` à travers un DSN de transport.
    - [ ] Ajouter des pièces jointes/images embarquées et envoyer de manière asynchrone via Messenger.

    **Syllabus:** `Miscellaneous → Mailer` ·
    **Level:** Advanced ·
    **Est. time:** 40 min ·
    **Prerequisites:** [Twig](../twig/index.md), [Messenger](../messenger/index.md)

---

## Theory

Le composant **Mime** modélise un message email comme un arbre de **parts**
(texte, HTML, pièces jointes) qui se sérialisent en une chaîne MIME. Le
composant **Mailer** envoie ce message à travers un **transport** choisi par un
DSN. Vous construisez un message (`Email`), vous le confiez à
`MailerInterface::send()`, et le transport le livre.

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
    Messenger est configuré pour router `SendEmailMessage` vers `async`. Vous
    appelez `$mailer->send($email)`. L'email a-t-il quitté le bâtiment quand
    `send()` retourne ?

??? note "Reveal"
    Non. Avec le routing configuré, `send()` **dispatche** un `SendEmailMessage`
    vers la file d'attente et retourne ; un worker le livre plus tard. Si aucun
    worker ne tourne, le mail reste dans la file — rien n'a été envoyé
    immédiatement.

### The Mime part model

`Symfony\Component\Mime\Email` est un builder de haut niveau au-dessus de
`Symfony\Component\Mime\Message`. En interne, le corps d'un message est un arbre
de sous-classes de `Symfony\Component\Mime\Part\AbstractPart` :

- `TextPart` — un corps (texte ou html) avec un media type.
- `DataPart` — une pièce jointe ou une ressource embarquée.
- `Multipart\AlternativePart` / `Multipart\MixedPart` / `Multipart\RelatedPart`
  — des conteneurs qui combinent des parts (corps alternatifs, pièces jointes
  mixtes, éléments liés/embarqués), tous sous
  `Symfony\Component\Mime\Part\Multipart\`.

`Email::text()`/`html()`/`addPart()` assemblent cet arbre ; `attachFromPath()`
et `embedFromPath()` ajoutent des `DataPart`. Les images embarquées sont
référencées via `cid:`.

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
est le point d'entrée. `Symfony\Component\Mailer\Transport` construit un
`TransportInterface` à partir d'un **DSN** : `smtp://user:pass@host:port`,
`sendmail://default`, `native://default`, ou des fournisseurs tiers via des
bridges (hors du périmètre de ce cours). La variable d'environnement
`MAILER_DSN` le configure.

```php
use Symfony\Component\Mailer\Mailer;
use Symfony\Component\Mailer\Transport;

// Transport::fromDsn() builds a TransportInterface (usually from MAILER_DSN)
$transport = Transport::fromDsn('smtp://user:pass@mail.example.com:465');
$mailer = new Mailer($transport);
$mailer->send($email); // send(RawMessage $message, ?Envelope $envelope = null)
```

L'`Envelope` du Mailer (expéditeur + destinataires) est distincte des headers du
message ; le transport utilise l'envelope pour la conversation SMTP, tandis que
les headers apparaissent dans le message visible.

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

`Symfony\Bridge\Twig\Mime\TemplatedEmail` étend `Email` avec
`htmlTemplate()`/`textTemplate()` + `context()`. Un
`BodyRenderer`/`MessageListener` conscient de Twig rend les templates en parts
html/texte avant l'envoi — vous n'appelez donc jamais Twig vous-même.

```php
use Symfony\Bridge\Twig\Mime\TemplatedEmail;

$email = (new TemplatedEmail())
    ->to('ada@example.com')
    ->htmlTemplate('emails/welcome.html.twig') // rendered by the BodyRenderer
    ->textTemplate('emails/welcome.txt.twig')  // via MessageListener, before sending
    ->context(['name' => 'Ada']);              // variables exposed to Twig
```

### Async sending via Messenger

Si Messenger est configuré pour router
`Symfony\Component\Mailer\Messenger\SendEmailMessage` vers un transport,
`MailerInterface::send()` le **dispatche** au lieu de l'envoyer immédiatement ;
un worker le livre plus tard. Cela garde la latence de la request basse et
offre gratuitement les retries et la gestion des échecs. Voir
[Messenger](../messenger/index.md).

```yaml
# config/packages/messenger.yaml
framework:
    messenger:
        routing:
            # MailerInterface::send() now dispatches SendEmailMessage to "async"
            Symfony\Component\Mailer\Messenger\SendEmailMessage: async
```

!!! note "Source reference"
    `Symfony\Component\Mailer\Mailer::send()` et `Symfony\Component\Mime\Email` —
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
| Utiliser `TemplatedEmail` + Twig pour le mail HTML | Concaténer des chaînes MIME à la main |
| Router `SendEmailMessage` vers async | Bloquer la request sur SMTP |
| Embarquer les images via `embedFromPath()` (`cid:`) | Insérer manuellement des blobs base64 |
| Configurer `MAILER_DSN` par environnement | Coder en dur les identifiants SMTP |

## When (not) to use it / alternatives

Utilisez Mailer pour l'email transactionnel. Pour les canaux non-email (SMS,
chat, push), le composant Notifier est son pendant (non couvert ici). Envoyez
toujours en asynchrone en production, sauf si l'email doit être confirmé avant
de répondre.

!!! danger "Certification traps"
    - L'**`Envelope`** du Mailer (expéditeur/destinataires) diffère des headers du message.
    - Avec le routing Messenger, `send()` **met en file** `SendEmailMessage` — il n'est pas envoyé immédiatement.
    - Les images embarquées utilisent `embedFromPath()` et sont référencées par `cid:`.
    - `TemplatedEmail` vit dans le **bridge Twig** (`Symfony\Bridge\Twig\Mime`).

!!! warning "Common mistakes"
    - S'attendre à ce qu'un template soit rendu sans que `symfony/twig-bundle` soit présent.
    - Oublier de lancer un worker, si bien que les emails asynchrones ne quittent jamais la file.

## Exercises

1. **(Advanced)** Envoyez un `TemplatedEmail` avec une pièce jointe et un logo embarqué.
2. **(Advanced)** Configurez l'application pour envoyer les emails de manière asynchrone.

??? success "Solutions"

    **1.** Voir `WelcomeMailer::welcome()` — `attachFromPath()` + `embedFromPath()`.

    **2.** Routez `Symfony\Component\Mailer\Messenger\SendEmailMessage` vers un
    transport asynchrone dans `messenger.yaml` (voir le YAML ci-dessus) et lancez
    `messenger:consume`.

## Certification questions

??? question "Q1. `MailerInterface::send()` with Messenger routing configured…"
    - [x] A. dispatches a `SendEmailMessage` to be delivered by a worker ✅
    - [ ] B. always sends synchronously
    - [ ] C. throws if no worker is running

    **Why:** Router `SendEmailMessage` en asynchrone fait que `send()` le met en file d'attente.
    **Ref:** [Sending messages async](https://symfony.com/doc/8.0/mailer.html#sending-messages-async).

??? question "Q2. Which class renders Twig templates into an email?"
    - [x] A. `Symfony\Bridge\Twig\Mime\TemplatedEmail` ✅
    - [ ] B. `Symfony\Component\Mime\Email`
    - [ ] C. `Symfony\Component\Mailer\Mailer`

    **Why:** `TemplatedEmail` (bridge Twig) transporte le template + le context.
    **Ref:** [HTML content](https://symfony.com/doc/8.0/mailer.html#twig-html-css).

??? question "Q3. How are inline images referenced in the HTML body?"
    - [x] A. via a `cid:` reference from `embedFromPath()`/`embed()` ✅
    - [ ] B. as external URLs only
    - [ ] C. they cannot be inlined

    **Why:** Les parts embarquées sont adressées avec `cid:<name>`. **Ref:** [Embedding images](https://symfony.com/doc/8.0/mailer.html#embedding-images).

## Key takeaways

- Mime modélise un message comme un arbre de parts ; `Email` est le builder.
- Mailer envoie via un DSN de transport (`MAILER_DSN`) ; `Envelope` ≠ headers.
- `TemplatedEmail` (bridge Twig) rend les templates html/texte.
- Routez `SendEmailMessage` vers Messenger pour la livraison asynchrone + les retries.

## Last-minute revision

!!! tip "Cheat sheet"
    - `(new Email())->from()->to()->subject()->text()->html()`.
    - `attachFromPath()`, `embedFromPath()` (`cid:`), `addPart(new DataPart(...))`.
    - `MailerInterface::send($email)` ; DSN via `MAILER_DSN`.
    - Async : router `SendEmailMessage` → transport ; lancer `messenger:consume`.

## Connections

- **Depends on:** [Messenger](../messenger/index.md) — la livraison asynchrone route `SendEmailMessage` ; [Twig](../twig/index.md) rend `TemplatedEmail`.
- **Reused in:** [Console](../console/index.md) — `messenger:consume` est ce qui livre réellement le courrier en file d'attente.
- **Confused with:** l'`Envelope` du Mailer (expéditeur/destinataires pour la conversation SMTP) vs les headers visibles du message.

## Official References
- [Official docs — Mailer](https://symfony.com/doc/8.0/mailer.html)
- [Official docs — Mime](https://symfony.com/doc/8.0/components/mime.html)
- [Symfony source — Mailer](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Mailer/Mailer.php)

## Video references

!!! tip "Watch & learn"
    Voici des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    "Symfony components" pour renforcer ce chapitre. Nous lions des chaînes stables
    plutôt que des vidéos individuelles pour que les références ne périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — des tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences et keynotes SymfonyCon.
    - [Official docs for this topic](https://symfony.com/doc/8.0/mailer.html#sending-messages-async) — certaines pages de la doc Symfony embarquent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** l'arbre de parts Mime modélise des corps alternative/mixed/related
- [ ] construire et envoyer un `TemplatedEmail` avec une pièce jointe/un embed dans Symfony 8
- [ ] déboguer « l'email asynchrone n'arrive jamais » (aucun worker ne consomme le transport)
- [ ] repérer le piège : avec le routing, `send()` met `SendEmailMessage` en file, il ne l'envoie pas immédiatement
- [ ] décrire la sélection du DSN de transport et `Envelope` vs headers

---

<small>Related: [Messenger](../messenger/index.md) · [Twig](../twig/index.md) · [Serializer](serializer.md)</small>
