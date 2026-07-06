# Flashcards — Automated Tests

31 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. Which base class do Symfony unit tests extend for pure, kernel-free logic?"
    **✅ PHPUnit\Framework\TestCase**

    Symfony ships no unit-test base class; pure unit tests extend PHPUnit's TestCase directly. No kernel is booted and no container is built.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#unit-tests)

??? question "2. In PHPUnit 11/12, how do you bind a test to a data provider?"
    **✅ #[DataProvider('methodName')] naming a public static method**

    The @dataProvider annotation is removed; use the PHPUnit\Framework\Attributes\DataProvider attribute pointing at a public static iterable-returning method.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

??? question "3. You need only canned return values, with no verification of how a collaborator is called. Which double do you create?"
    **✅ A stub via $this->createStub(Foo::class)**

    A stub supplies return values but never asserts interactions. A mock adds verifiable expectations you do not need here.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/test-doubles.html)

??? question "4. What does assertSame(1, '1') do?"
    **✅ Fails, because the types differ (strict === comparison)**

    assertSame uses ===, so int 1 and string '1' are not the same. Use assertEquals for loose (==) comparison.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/assertions.html#assertsame)

??? question "5. Why can self::getContainer()->get() return a private service in a test?"
    **✅ It returns the special test container (test.service_container) that exposes private/non-shared services**

    The test environment (framework.test: true) compiles a TestContainer that keeps references to used private/non-shared services so tests can fetch and replace them. static::$kernel->getContainer() does not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

??? question "6. How are WebTestCase and KernelTestCase related?"
    **✅ WebTestCase extends KernelTestCase, adding the HTTP client (createClient())**

    WebTestCase adds the KernelBrowser client on top of the kernel-booting KernelTestCase. Use KernelTestCase when you need only the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#application-tests)

??? question "7. A private service is never injected anywhere. In the test environment it is…"
    **✅ Still removed — the test container only keeps services that are actually used**

    Unused private services are optimised away even in the test container; only used private/non-shared services remain reachable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

??? question "8. How many times may createClient() be called within a single test?"
    **✅ Once — a second call throws**

    Only one kernel/client may be booted per test; calling createClient() again throws a LogicException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#your-first-application-test)

??? question "9. What does $client->request('GET', '/') return?"
    **✅ A Symfony\Component\DomCrawler\Crawler**

    Navigation methods return a Crawler over the response DOM. Fetch the response object with $client->getResponse().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#making-requests)

??? question "10. By default, after a controller returns a 302 redirect, the test client…"
    **✅ Stops on the redirect so you can assert the Location, until you call followRedirect()**

    Auto-follow is off by default. Use followRedirect() to follow the last redirect once, or followRedirects() to toggle auto-following.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#redirecting)

??? question "11. Which method keeps a service replaced via getContainer()->set() alive across multiple requests?"
    **✅ $client->disableReboot()**

    By default the kernel reboots after each request, discarding replacements. disableReboot() preserves the container between requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

??? question "12. $crawler->filter('div.item') requires which component to be installed?"
    **✅ symfony/css-selector**

    filter() converts the CSS selector to XPath via CssSelectorConverter, so the css-selector component is required. filterXPath() works without it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dom_crawler.html)

??? question "13. For which HTTP status codes does assertResponseIsSuccessful() pass?"
    **✅ Any 2xx status**

    It asserts the response is in the successful (2xx) range. Use assertResponseStatusCodeSame(n) to check an exact code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

??? question "14. Which assertion checks that an element's text is exactly equal (not a substring)?"
    **✅ assertSelectorTextSame('h1', 'Hi')**

    The ...Same variant requires an exact match; ...Contains checks a substring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

??? question "15. When must $client->enableProfiler() be called?"
    **✅ Before the request whose profile you want to read**

    enableProfiler() opts the next request into profiling; calling it after the request collects nothing and getProfile() returns false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

??? question "16. The recommended way to assert that an email was sent in a functional test is…"
    **✅ assertEmailCount() / getMailerMessage() from MailerAssertionsTrait**

    WebTestCase provides mailer assertions backed by the mailer data collector, so you rarely touch the raw collector.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#testing-emails)

??? question "17. What is the second argument of static::createClient()?"
    **✅ An array of default server parameters (the $_SERVER bag)**

    createClient(array $options, array $server) — the second array models server parameters (HTTP_* headers, HTTPS, PHP_AUTH_USER, etc.).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

??? question "18. To simulate an 'Accept: application/json' request header via server parameters you set…"
    **✅ 'HTTP_ACCEPT' => 'application/json'**

    Request headers become HTTP_-prefixed server parameters. CONTENT_TYPE, HTTPS, PHP_AUTH_USER and PHP_AUTH_PW are the unprefixed exceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

??? question "19. What does $client->loginUser($user) do?"
    **✅ Authenticates the session with the given UserInterface, skipping the login form**

    loginUser() injects a security token for a real user object so you can test authorized behaviour without driving the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#logging-in-users-authentication)

??? question "20. What is the effect of $client->insulate()?"
    **✅ Each request runs in a separate PHP subprocess, so in-process profiler/container access is lost**

    Insulated requests run in a fresh subprocess to isolate global state, at the cost of losing in-process access to the profiler and container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/browser_kit.html)

??? question "21. Which class must be registered to enable the PHPUnit bridge's deprecation collection and clock/DNS mocking?"
    **✅ Symfony\Bridge\PhpUnit\SymfonyExtension**

    The bridge's PHPUnit extension (registered under <extensions><bootstrap .../>) wires the DeprecationErrorHandler, ClockMock and DnsMock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

??? question "22. A deprecation triggered deep inside a vendor library's own internals is classified as…"
    **✅ indirect**

    self = your code, direct = a dependency you call directly, indirect = deep inside a dependency's internals, legacy = tests excluded from thresholds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#making-tests-fail)

??? question "23. What does SYMFONY_DEPRECATIONS_HELPER=weak do?"
    **✅ Reports deprecations but never fails the build**

    weak collects and prints deprecations without enforcing thresholds. disabled=1 turns collection off; max[...] enforces limits.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

??? question "24. The modern way to silence a single test's expected deprecations is…"
    **✅ The #[IgnoreDeprecations] attribute**

    Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations replaces the old @group legacy for excluding a test's deprecations from the report.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

??? question "25. How is SYMFONY_DEPRECATIONS_HELPER supplied to PHPUnit?"
    **✅ As an environment/server variable (e.g. in phpunit.dist.xml <php>)**

    It is read from the environment; commonly set via <php><server name="SYMFONY_DEPRECATIONS_HELPER" .../></php> or the shell.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

??? question "26. You must test a service that needs the container but sends no HTTP requests. Which base class fits best?"
    **✅ KernelTestCase — boots the kernel and exposes the container, without an HTTP client**

    KernelTestCase boots the kernel and gives you self::getContainer() with no browser. WebTestCase adds the HTTP client and is reserved for tests that make requests; a plain TestCase boots no kernel at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#integration-tests)

??? question "27. To swap a real service for a mock before making a request in a functional test, you should…"
    **✅ Fetch the test container with self::getContainer() and call ->set('service.id', $mock) before the request**

    The test container returned by self::getContainer() allows ->set() to override a (used) service with a double. Do this before issuing the request so the kernel uses the replacement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

??? question "28. What does the WebTestCase helper assertResponseIsSuccessful() verify?"
    **✅ That the last response has a 2xx status code**

    assertResponseIsSuccessful() passes for any 2xx status. These assertResponse*/assertSelector* helpers come from the BrowserKit/DomCrawler assertion traits mixed into WebTestCase; assertSelectorTextContains() checks a CSS-selected element's text.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#testing-the-response-status-code-headers-and-content)

??? question "29. A method referenced by #[DataProvider('provide')] must be…"
    **✅ public static and return an array or other iterable of argument sets**

    PHPUnit\Framework\Attributes\DataProvider names a public static method returning an iterable (array or Generator) of argument arrays; each set becomes one parameterised run of the test.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

??? question "30. Which utility tests a console command's output and exit code without a real terminal?"
    **✅ CommandTester — call execute([...]) then getDisplay() and getStatusCode()**

    Symfony\Component\Console\Tester\CommandTester wraps a single command: execute() supplies input, then getDisplay() returns captured output and getStatusCode() the exit code. ApplicationTester covers the whole app.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html#testing-commands)

??? question "31. Which SYMFONY_DEPRECATIONS_HELPER value makes the build fail on the very first deprecation?"
    **✅ max[total]=0**

    max[total]=0 sets a zero threshold, so any deprecation fails the suite. weak reports without failing, and disabled=1 turns collection off entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

---

<small>Back to [Flashcards](index.md) · [Automated Tests](../../testing/index.md)</small>
