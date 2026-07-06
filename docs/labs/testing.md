# Lab: Automated Tests — A Service with `KernelTestCase` and an Endpoint with `WebTestCase`

!!! abstract "Practical Lab"
    **Objective:** integration-test a service through the **test container** (private
    services + a `set()` mock) and functional-test an HTTP endpoint with a
    `KernelBrowser` (`assertResponse*` / `assertSelector*`) ·
    **Difficulty:** Medium ·
    **Theory:** [Functional Tests](../testing/functional-tests.md) ·
    **Mode:** TDD

## Objective

After this lab you can, test-first:

- Boot the kernel in a `KernelTestCase`, pull a **private** service from
  `self::getContainer()`, and assert on its behaviour.
- **Replace** a collaborator with a mock in the test container and prove your
  service calls it.
- Drive a route in a `WebTestCase` with `static::createClient()` and assert
  status, redirect, and rendered selector text — and authenticate with
  `loginUser()` when the route is protected.

## Prerequisites

- Chapters: [Functional Tests](../testing/functional-tests.md) ·
  [Accessing Framework Objects](../testing/framework-objects.md) ·
  [Introspection & Assertions](../testing/introspection.md)
- Assumed skills: writing a controller with `#[Route]`, constructor injection,
  running `php bin/phpunit`.

## TD Instructions

You will build a tiny newsletter feature **test-first**. Do not write the
production classes until a test demands them.

1. Create `tests/Newsletter/SubscriptionManagerTest.php` extending
   `KernelTestCase`. Write a first failing test: boot the kernel, fetch
   `App\Newsletter\SubscriptionManager` from `self::getContainer()`, and assert
   that `subscribe('not-an-email')` returns `false`.
2. Add a second test in the same class that **replaces** the mailer boundary:
   build a mock of `App\Newsletter\WelcomeMailerInterface`, expect `send()` to be
   called **once**, register it with `self::getContainer()->set(...)`, *then*
   fetch `SubscriptionManager` and assert `subscribe('ada@example.com')` returns
   `true`.
3. Run the suite and watch both tests fail (**red**) — the classes do not exist
   yet.
4. Write the minimum production code to go **green**: the
   `WelcomeMailerInterface` boundary, a real implementation, and the
   `SubscriptionManager` service.
5. Create `tests/Controller/NewsletterControllerTest.php` extending
   `WebTestCase`. Write a failing test that `GET`s `/newsletter` and asserts a
   successful response plus `assertSelectorTextContains('h1', 'Subscribe')`.
6. Add a second functional test: `POST` `/newsletter` with a valid `email`
   parameter and assert the response **redirects** to `/newsletter/thanks`.
   Replace the mailer with a mock first (via the test container) so the test
   touches no external boundary.
7. Make them green with a `NewsletterController`. Refactor with the tests as your
   safety net.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · PHPUnit 11/12 (attribute metadata) · no libraries
    outside the certification scope · follow best practices (attributes, strict
    types, `readonly` where apt).

## Implementation Guide (partial)

- Two base classes, two jobs:

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

- The service under test needs **one boundary** you can mock — an interface
  (`WelcomeMailerInterface`) so the real send is never triggered in tests.
- In a **pure `KernelTestCase`** there is no request, so no kernel reboot happens
  between `set()` and your call — you do **not** need `disableReboot()` there.
  Order matters: call `set()` **before** the first `get()` of the consumer so it
  is built with the mock.
- In a **`WebTestCase`**, a `set()` replacement is discarded when the kernel
  reboots on the next request — call `$client->disableReboot()` **before** the
  request that must see the mock.
- Assert with the built-in helpers, not `getResponse()` by hand:
  `assertResponseIsSuccessful()`, `assertResponseRedirects('/path')`,
  `assertSelectorTextContains('h1', '…')`. They print the response on failure.
- For a protected route, authenticate with `$client->loginUser($user)` — it sets
  the security token without replaying the login form (a real firewall must be
  configured).

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing tests below; run them, watch them fail.
    2. **Green:** write the minimum service + controller to pass.
    3. **Refactor:** clean up with the tests as your safety net.

**Behaviour (Given/When/Then):**

- **Given** a valid email **When** `subscribe()` runs **Then** it returns `true`
  and calls the mailer once.
- **Given** an invalid email **When** `subscribe()` runs **Then** it returns
  `false` and never calls the mailer.
- **Given** the newsletter form route **When** a browser `GET`s it **Then** the
  response is 200 and shows an `<h1>` containing "Subscribe".
- **Given** a valid `POST` **When** the form is submitted **Then** the response
  redirects to `/newsletter/thanks`.

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
    Run one class at a time while iterating:
    `php bin/phpunit tests/Newsletter/SubscriptionManagerTest.php` then
    `php bin/phpunit tests/Controller/NewsletterControllerTest.php`.
    The `test.client` service and the test container exist only when
    `framework.test: true` (default in `config/packages/test/framework.yaml`).
    Use `$this->createMock(WelcomeMailerInterface::class)` for the boundary and
    `self::getContainer()->set(...)` to inject it.

## Validation Steps

- [ ] `php bin/phpunit` is **red** before you write any production class.
- [ ] After writing the service, `SubscriptionManagerTest` is green — including
      the mocked-mailer expectation `self::once()`.
- [ ] After writing the controller, `NewsletterControllerTest` is green;
      `assertResponseRedirects('/newsletter/thanks')` passes.
- [ ] `php bin/console debug:container App\\Newsletter\\SubscriptionManager` shows
      the service is registered (and likely **private** — yet the test can fetch
      it).

## Review — Common Mistakes

- Calling `self::getContainer()->set()` **after** fetching the consumer → the
  service is already built with the real dependency. **Fix:** `set()` first, then
  `get()`.
- Expecting a `set()` mock to survive in a `WebTestCase` request → the kernel
  reboots and discards it. **Fix:** `$client->disableReboot()` before the request.
- Reaching for `static::$kernel->getContainer()->get(PrivateService::class)` →
  throws, private services are hidden there. **Fix:** always `self::getContainer()`.
- Following the redirect and then asserting a redirect → after
  `$client->followRedirect()` the status is 200. **Fix:** assert
  `assertResponseRedirects()` **before** following.
- Asserting on `$client->getResponse()->getContent()` with `str_contains` →
  brittle. **Fix:** `assertSelectorTextContains()` parses the DOM and prints the
  response on failure.

## Exam Connection

The certification hammers three facts this lab drills: (1) `WebTestCase`
**extends** `KernelTestCase`, so the client is the only addition; (2)
`self::getContainer()` returns the **test container** (`test.service_container`)
which exposes **private** services — `$kernel->getContainer()` does not; and
(3) a `set()` replacement is lost on the next kernel reboot unless you
`disableReboot()`. It also tests knowing the `assertResponse*` / `assertSelector*`
helpers by name and that `loginUser()` authenticates without the login form.

## Ideal Solution

??? success "Reference solution (compare only after you try)"

    **The boundary + service + controller under test:**

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

    **The minimal templates** (so the selector assertions have something to match):

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

    **The two test classes** (identical to the TDD block, kept together for
    reference):

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
    Add a `#[Route('/newsletter/admin')]` action behind a firewall and test it
    with `loginUser()`:

    ```php
    $user = self::getContainer()->get(UserRepositoryInterface::class)->findAdmin();
    $client->loginUser($user);
    $client->request('GET', '/newsletter/admin');
    self::assertResponseIsSuccessful();
    ```

    `loginUser()` sets the security token directly — no login form replay — but a
    real firewall must be configured for the request.

## Alternative Approaches (optional)

- **Option A (simple)** — Skip the boundary interface and unit-test
  `SubscriptionManager` with a hand-written stub in a plain
  `PHPUnit\Framework\TestCase`. Fast, but proves nothing about DI wiring.
- **Option B (integration)** — Keep the real `WelcomeMailer` and assert the sent
  email via the mailer test assertions
  (`assertEmailCount`) instead of a mock; heavier but exercises more of the stack.
- **Option C (exam-style)** — Fetch the `router` from the test container and
  assert `generate('newsletter_thanks') === '/newsletter/thanks'`, tying route
  names to the redirect target the functional test checks.

---

<small>Theory: [Functional Tests](../testing/functional-tests.md) · Labs: [all labs](index.md)</small>
