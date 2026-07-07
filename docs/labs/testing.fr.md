---
tags:
  - Labs
  - Testing
---

# Lab : Tests automatisés — un service avec `KernelTestCase` et un endpoint avec `WebTestCase`

!!! abstract "Practical Lab"
    **Objective:** tester un service en intégration via le **test container** (services
    privés + un mock injecté par `set()`) et tester fonctionnellement un endpoint HTTP avec un
    `KernelBrowser` (`assertResponse*` / `assertSelector*`) ·
    **Difficulty:** Moyenne ·
    **Theory:** [Functional Tests](../testing/functional-tests.md) ·
    **Mode:** TDD

## Objective

À l'issue de ce lab, vous saurez, en mode test-first :

- Démarrer le kernel dans un `KernelTestCase`, récupérer un service **privé** depuis
  `self::getContainer()` et vérifier son comportement par des assertions.
- **Remplacer** un collaborateur par un mock dans le test container et prouver que votre
  service l'appelle.
- Piloter une route dans un `WebTestCase` avec `static::createClient()` et vérifier
  le statut, la redirection et le texte d'un sélecteur rendu — et vous authentifier avec
  `loginUser()` lorsque la route est protégée.

## Prerequisites

- Chapitres : [Functional Tests](../testing/functional-tests.md) ·
  [Accessing Framework Objects](../testing/framework-objects.md) ·
  [Introspection & Assertions](../testing/introspection.md)
- Compétences supposées acquises : écrire un controller avec `#[Route]`, l'injection par constructeur,
  lancer `php bin/phpunit`.

## TD Instructions

Vous allez construire une petite fonctionnalité de newsletter **en écrivant les tests d'abord**. N'écrivez pas les
classes de production tant qu'un test ne les exige pas.

1. Créez `tests/Newsletter/SubscriptionManagerTest.php` étendant
   `KernelTestCase`. Écrivez un premier test qui échoue : démarrez le kernel, récupérez
   `App\Newsletter\SubscriptionManager` depuis `self::getContainer()`, et vérifiez
   que `subscribe('not-an-email')` retourne `false`.
2. Ajoutez un deuxième test dans la même classe qui **remplace** la frontière du mailer :
   construisez un mock de `App\Newsletter\WelcomeMailerInterface`, attendez-vous à ce que `send()` soit
   appelé **une fois**, enregistrez-le avec `self::getContainer()->set(...)`, *puis*
   récupérez `SubscriptionManager` et vérifiez que `subscribe('ada@example.com')` retourne
   `true`.
3. Lancez la suite et observez les deux tests échouer (**rouge**) — les classes n'existent
   pas encore.
4. Écrivez le minimum de code de production pour passer au **vert** : la
   frontière `WelcomeMailerInterface`, une implémentation réelle, et le
   service `SubscriptionManager`.
5. Créez `tests/Controller/NewsletterControllerTest.php` étendant
   `WebTestCase`. Écrivez un test qui échoue : un `GET` sur `/newsletter` doit produire une
   response réussie, plus `assertSelectorTextContains('h1', 'Subscribe')`.
6. Ajoutez un deuxième test fonctionnel : un `POST` sur `/newsletter` avec un paramètre `email`
   valide doit produire une response qui **redirige** vers `/newsletter/thanks`.
   Remplacez d'abord le mailer par un mock (via le test container) afin que le test
   ne touche aucune frontière externe.
7. Faites-les passer au vert avec un `NewsletterController`. Refactorisez avec les tests comme
   filet de sécurité.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · PHPUnit 11/12 (métadonnées par attributs) · aucune bibliothèque
    hors du périmètre de la certification · respectez les bonnes pratiques (attributs, strict
    types, `readonly` quand c'est pertinent).

## Implementation Guide (partial)

- Deux classes de base, deux rôles :

    ```mermaid
    flowchart LR
        subgraph K["KernelTestCase"]
            A["self::bootKernel()"] --> B["self::getContainer()->get(Service)"]
            B --> C["assert behaviour"]
            B -.->|"set(Iface, mock)"| M["mock boundary"]
        end
        subgraph W["WebTestCase (extends KernelTestCase)"]
            D["static::createClient()"] --> E["request('GET'|'POST', ...)"]
            E --> F["assertResponse* / assertSelector*"]
        end
    ```

- Le service testé a besoin d'**une frontière** que vous pouvez mocker — une interface
  (`WelcomeMailerInterface`) pour que l'envoi réel ne soit jamais déclenché dans les tests.
- Dans un **`KernelTestCase` pur**, il n'y a pas de request, donc aucun redémarrage du kernel n'a lieu
  entre `set()` et votre appel — vous n'avez **pas** besoin de `disableReboot()` ici.
  L'ordre compte : appelez `set()` **avant** le premier `get()` du consommateur pour qu'il
  soit construit avec le mock.
- Dans un **`WebTestCase`**, un remplacement via `set()` est jeté quand le kernel
  redémarre à la request suivante — appelez `$client->disableReboot()` **avant** la
  request qui doit voir le mock.
- Vérifiez avec les helpers intégrés, pas avec `getResponse()` à la main :
  `assertResponseIsSuccessful()`, `assertResponseRedirects('/path')`,
  `assertSelectorTextContains('h1', '…')`. Ils affichent la response en cas d'échec.
- Pour une route protégée, authentifiez-vous avec `$client->loginUser($user)` — cela pose
  le token de sécurité sans rejouer le formulaire de connexion (un vrai firewall doit être
  configuré).

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez les tests ci-dessous qui échouent ; lancez-les, observez-les échouer.
    2. **Green :** écrivez le minimum de service + controller pour passer.
    3. **Refactor :** nettoyez avec les tests comme filet de sécurité.

**Comportement (Given/When/Then) :**

- **Given** un email valide, **When** `subscribe()` s'exécute, **Then** il retourne `true`
  et appelle le mailer une fois.
- **Given** un email invalide, **When** `subscribe()` s'exécute, **Then** il retourne
  `false` et n'appelle jamais le mailer.
- **Given** la route du formulaire de newsletter, **When** un navigateur fait un `GET` dessus, **Then** la
  response est 200 et affiche un `<h1>` contenant "Subscribe".
- **Given** un `POST` valide, **When** le formulaire est soumis, **Then** la response
  redirige vers `/newsletter/thanks`.

=== "KernelTestCase (service)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Tests\Newsletter;

    use App\Newsletter\SubscriptionManager;
    use App\Newsletter\WelcomeMailerInterface;
    use PHPUnit\Framework\Attributes\CoversClass;
    use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

    #[CoversClass(SubscriptionManager::class)]
    final class SubscriptionManagerTest extends KernelTestCase
    {
        public function testRejectsInvalidEmailFromRealContainer(): void
        {
            self::bootKernel();

            // Even if SubscriptionManager is private, the test container exposes it.
            $manager = self::getContainer()->get(SubscriptionManager::class);

            self::assertFalse($manager->subscribe('not-an-email'));
        }

        public function testNotifiesMailerForValidEmail(): void
        {
            self::bootKernel();

            $mailer = $this->createMock(WelcomeMailerInterface::class);
            $mailer->expects(self::once())
                ->method('send')
                ->with('ada@example.com');

            // Replace the boundary BEFORE the consumer is built.
            self::getContainer()->set(WelcomeMailerInterface::class, $mailer);

            $manager = self::getContainer()->get(SubscriptionManager::class);

            self::assertTrue($manager->subscribe('ada@example.com'));
        }
    }
    ```

=== "WebTestCase (endpoint)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Tests\Controller;

    use App\Newsletter\WelcomeMailerInterface;
    use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

    final class NewsletterControllerTest extends WebTestCase
    {
        public function testFormPageRenders(): void
        {
            $client = static::createClient();
            $client->request('GET', '/newsletter');

            self::assertResponseIsSuccessful();
            self::assertSelectorTextContains('h1', 'Subscribe');
        }

        public function testValidSubmissionRedirectsToThanks(): void
        {
            $client = static::createClient();
            $client->disableReboot(); // keep the mock alive across the request

            $mailer = $this->createMock(WelcomeMailerInterface::class);
            self::getContainer()->set(WelcomeMailerInterface::class, $mailer);

            $client->request('POST', '/newsletter', ['email' => 'ada@example.com']);

            self::assertResponseRedirects('/newsletter/thanks');
        }
    }
    ```

!!! tip "Setup hints"
    Lancez une classe à la fois pendant que vous itérez :
    `php bin/phpunit tests/Newsletter/SubscriptionManagerTest.php` puis
    `php bin/phpunit tests/Controller/NewsletterControllerTest.php`.
    Le service `test.client` et le test container n'existent que lorsque
    `framework.test: true` (valeur par défaut dans `config/packages/test/framework.yaml`).
    Utilisez `$this->createMock(WelcomeMailerInterface::class)` pour la frontière et
    `self::getContainer()->set(...)` pour l'injecter.

## Validation Steps

- [ ] `php bin/phpunit` est **rouge** avant que vous n'écriviez la moindre classe de production.
- [ ] Après avoir écrit le service, `SubscriptionManagerTest` est vert — y compris
      l'attente sur le mailer mocké `self::once()`.
- [ ] Après avoir écrit le controller, `NewsletterControllerTest` est vert ;
      `assertResponseRedirects('/newsletter/thanks')` passe.
- [ ] `php bin/console debug:container App\\Newsletter\\SubscriptionManager` montre
      que le service est enregistré (et probablement **privé** — et pourtant le test peut le
      récupérer).

## Review — Common Mistakes

- Appeler `self::getContainer()->set()` **après** avoir récupéré le consommateur → le
  service est déjà construit avec la vraie dépendance. **Correction :** `set()` d'abord, puis
  `get()`.
- S'attendre à ce qu'un mock posé par `set()` survive à une request dans un `WebTestCase` → le kernel
  redémarre et le jette. **Correction :** `$client->disableReboot()` avant la request.
- Utiliser `static::$kernel->getContainer()->get(PrivateService::class)` →
  lève une exception, les services privés y sont cachés. **Correction :** toujours `self::getContainer()`.
- Suivre la redirection puis vérifier une redirection → après
  `$client->followRedirect()`, le statut est 200. **Correction :** vérifiez
  `assertResponseRedirects()` **avant** de suivre.
- Faire des assertions sur `$client->getResponse()->getContent()` avec `str_contains` →
  fragile. **Correction :** `assertSelectorTextContains()` analyse le DOM et affiche la
  response en cas d'échec.

## Exam Connection

La certification martèle trois faits que ce lab fait travailler : (1) `WebTestCase`
**étend** `KernelTestCase`, le client est donc le seul ajout ; (2)
`self::getContainer()` retourne le **test container** (`test.service_container`)
qui expose les services **privés** — `$kernel->getContainer()` ne le fait pas ; et
(3) un remplacement via `set()` est perdu au redémarrage suivant du kernel sauf si vous appelez
`disableReboot()`. Elle vérifie aussi que vous connaissez les helpers `assertResponse*` / `assertSelector*`
par leur nom et que `loginUser()` authentifie sans passer par le formulaire de connexion.

## Ideal Solution

??? success "Reference solution (compare only after you try)"

    **La frontière + le service + le controller testés :**

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Newsletter;

    interface WelcomeMailerInterface
    {
        public function send(string $email): void;
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Newsletter;

    final readonly class SubscriptionManager
    {
        public function __construct(private WelcomeMailerInterface $mailer)
        {
        }

        public function subscribe(string $email): bool
        {
            if (false === filter_var($email, FILTER_VALIDATE_EMAIL)) {
                return false;
            }

            $this->mailer->send($email);

            return true;
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Newsletter;

    use Symfony\Component\Mime\Email;
    use Symfony\Component\Mailer\MailerInterface;

    final readonly class WelcomeMailer implements WelcomeMailerInterface
    {
        public function __construct(private MailerInterface $mailer)
        {
        }

        public function send(string $email): void
        {
            $this->mailer->send(
                (new Email())
                    ->to($email)
                    ->subject('Welcome to the newsletter')
                    ->text('Thanks for subscribing!'),
            );
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Newsletter\SubscriptionManager;
    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;

    #[Route('/newsletter', name: 'newsletter_')]
    final class NewsletterController extends AbstractController
    {
        #[Route('', name: 'form', methods: ['GET'])]
        public function form(): Response
        {
            return $this->render('newsletter/form.html.twig');
        }

        #[Route('', name: 'subscribe', methods: ['POST'])]
        public function subscribe(Request $request, SubscriptionManager $manager): Response
        {
            $email = (string) $request->request->get('email', '');

            if (!$manager->subscribe($email)) {
                $this->addFlash('error', 'Please enter a valid email address.');

                return $this->redirectToRoute('newsletter_form');
            }

            return $this->redirectToRoute('newsletter_thanks');
        }

        #[Route('/thanks', name: 'thanks', methods: ['GET'])]
        public function thanks(): Response
        {
            return $this->render('newsletter/thanks.html.twig');
        }
    }
    ```

    **Les templates minimaux** (pour que les assertions sur les sélecteurs aient quelque chose à trouver) :

    ```twig
    {# templates/newsletter/form.html.twig #}
    <h1>Subscribe to the newsletter</h1>
    <form method="post" action="{{ path('newsletter_subscribe') }}">
        <input type="email" name="email" required>
        <button type="submit">Subscribe</button>
    </form>
    ```

    ```twig
    {# templates/newsletter/thanks.html.twig #}
    <h1>Thanks for subscribing</h1>
    ```

    **Les deux classes de test** (identiques au bloc TDD, regroupées ici pour
    référence) :

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Tests\Newsletter;

    use App\Newsletter\SubscriptionManager;
    use App\Newsletter\WelcomeMailerInterface;
    use PHPUnit\Framework\Attributes\CoversClass;
    use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

    #[CoversClass(SubscriptionManager::class)]
    final class SubscriptionManagerTest extends KernelTestCase
    {
        public function testRejectsInvalidEmailFromRealContainer(): void
        {
            self::bootKernel();

            $manager = self::getContainer()->get(SubscriptionManager::class);

            self::assertFalse($manager->subscribe('not-an-email'));
        }

        public function testNotifiesMailerForValidEmail(): void
        {
            self::bootKernel();

            $mailer = $this->createMock(WelcomeMailerInterface::class);
            $mailer->expects(self::once())
                ->method('send')
                ->with('ada@example.com');

            self::getContainer()->set(WelcomeMailerInterface::class, $mailer);

            $manager = self::getContainer()->get(SubscriptionManager::class);

            self::assertTrue($manager->subscribe('ada@example.com'));
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Tests\Controller;

    use App\Newsletter\WelcomeMailerInterface;
    use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

    final class NewsletterControllerTest extends WebTestCase
    {
        public function testFormPageRenders(): void
        {
            $client = static::createClient();
            $client->request('GET', '/newsletter');

            self::assertResponseIsSuccessful();
            self::assertSelectorTextContains('h1', 'Subscribe');
        }

        public function testValidSubmissionRedirectsToThanks(): void
        {
            $client = static::createClient();
            $client->disableReboot();

            $mailer = $this->createMock(WelcomeMailerInterface::class);
            self::getContainer()->set(WelcomeMailerInterface::class, $mailer);

            $client->request('POST', '/newsletter', ['email' => 'ada@example.com']);

            self::assertResponseRedirects('/newsletter/thanks');
        }
    }
    ```

!!! tip "Level up — an authenticated route"
    Ajoutez une action `#[Route('/newsletter/admin')]` derrière un firewall et testez-la
    avec `loginUser()` :

    ```php
    $user = self::getContainer()->get(UserRepositoryInterface::class)->findAdmin();
    $client->loginUser($user);
    $client->request('GET', '/newsletter/admin');
    self::assertResponseIsSuccessful();
    ```

    `loginUser()` pose directement le token de sécurité — pas de rejeu du formulaire de connexion — mais un
    vrai firewall doit être configuré pour la request.

## Alternative Approaches (optional)

- **Option A (simple)** — Sautez l'interface de frontière et testez unitairement
  `SubscriptionManager` avec un stub écrit à la main dans un simple
  `PHPUnit\Framework\TestCase`. Rapide, mais ne prouve rien sur le câblage DI.
- **Option B (intégration)** — Gardez le vrai `WelcomeMailer` et vérifiez l'email envoyé
  via les assertions de test du mailer
  (`assertEmailCount`) plutôt qu'un mock ; plus lourd, mais exerce une plus grande partie de la pile.
- **Option C (exam-style)** — Récupérez le `router` depuis le test container et
  vérifiez que `generate('newsletter_thanks') === '/newsletter/thanks'`, ce qui relie les noms
  de routes à la cible de redirection vérifiée par le test fonctionnel.

---

<small>Theory: [Functional Tests](../testing/functional-tests.md) · Labs: [all labs](index.md)</small>
