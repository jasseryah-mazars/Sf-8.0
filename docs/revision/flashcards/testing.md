# Flashcards — Automated Tests

71 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

## 🧠 Pour les nuls

**C'est quoi ?** Un jeu de **71 flashcards** (question au recto, réponse au verso) sur Automated Tests. On lit la question, on répond mentalement, puis on tape pour révéler la réponse.

**Pourquoi ça existe ?** Se tester activement (essayer de répondre avant de voir la réponse) ancre l'information bien mieux que relire passivement un chapitre. Répété à intervalles espacés, c'est la technique de mémorisation la plus efficace connue.

**🏠 Analogie de la vraie vie :** Ce sont les **cartes-vocabulaire** utilisées pour apprendre une langue étrangère : un mot d'un côté, sa traduction de l'autre — on ne progresse qu'en essayant de deviner avant de retourner la carte.

**Symfony dans la vraie vie :** Recto de la carte → une question précise sur Automated Tests / Verso → la réponse avec sa justification et un lien vers la doc officielle / Cartes marquées "ratées" → à revoir en priorité au prochain passage.

**⚠️ Erreur fréquente :** Taper pour révéler la réponse trop vite, sans avoir vraiment tenté de répondre — cela transforme l'exercice en simple lecture, avec un gain de mémorisation presque nul.

**🧠 Comment le mémoriser :** *« Je réponds avant de retourner la carte »* — et je note les cartes ratées pour les revoir plus souvent que les autres (répétition espacée).

??? question "1. Which base class do Symfony unit tests extend for pure, kernel-free logic?"
    **✅ PHPUnit\Framework\TestCase**

    Symfony ships no unit-test base class; pure unit tests extend PHPUnit's TestCase directly. No kernel is booted and no container is built.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#unit-tests)

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

??? question "5. A method referenced by #[DataProvider('provide')] must be…"
    **✅ public static and return an array or other iterable of argument sets**

    PHPUnit\Framework\Attributes\DataProvider names a public static method returning an iterable (array or Generator) of argument arrays; each set becomes one parameterised run of the test.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

??? question "6. A test method carries both #[TestWith([1000, 'FR', 1200])] and #[DataProvider('provideRates')], where provideRates() yields two rows. How many times does PHPUnit execute that test method?"
    **✅ Three times — the #[TestWith] row plus the two provider rows**

    #[TestWith] inlines one argument row and #[DataProvider] contributes its iterable rows; they are additive, so the method runs once per row across all data attributes (1 + 2 = 3). #[TestWith] is simply a provider that needs no separate method — it does not replace or disable #[DataProvider].

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

??? question "7. In PHPUnit 10+, a data-provider method declared non-static (public function provide()) results in…"
    **✅ An error — provider methods must be public static**

    PHPUnit 10+ requires data-provider methods to be public and static; a non-static provider is reported as an error, not a fallback or a mere deprecation. The provider is resolved before any test instance exists, so it cannot depend on instance state.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

??? question "8. True or False: PHPUnit creates a fresh instance of the test class for every test method, so state set in one test does not leak into another."
    **✅ True**

    PHPUnit reflects over the TestCase subclass and, for each test method, builds a new instance, runs setUp(), the test, then tearDown(). Instance properties therefore never carry over between test methods; only static properties (which you should avoid) can leak state.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html)

??? question "9. When is a mock expectation such as $mock->expects(self::once())->method('x') actually verified?"
    **✅ Automatically during the test's teardown, by PHPUnit's mock verification**

    A mock records its expectations and PHPUnit verifies them at teardown; an unmet expectation (e.g. never called when once() was required) then fails the test. This is exactly what distinguishes a mock from a stub, which asserts nothing. There is no manual verify() call in normal usage.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/test-doubles.html)

??? question "10. Why can self::getContainer()->get() return a private service in a test?"
    **✅ It returns the special test container (test.service_container) that exposes private/non-shared services**

    The test environment (framework.test: true) compiles a TestContainer that keeps references to used private/non-shared services so tests can fetch and replace them. static::$kernel->getContainer() does not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#accessing-the-container)

??? question "11. How are WebTestCase and KernelTestCase related?"
    **✅ WebTestCase extends KernelTestCase, adding the HTTP client (createClient())**

    WebTestCase adds the KernelBrowser client on top of the kernel-booting KernelTestCase. Use KernelTestCase when you need only the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#application-tests)

??? question "12. How many times may createClient() be called within a single test?"
    **✅ Once — a second call throws**

    Only one kernel/client may be booted per test; calling createClient() again throws a LogicException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#your-first-application-test)

??? question "13. You must test a service that needs the container but sends no HTTP requests. Which base class fits best?"
    **✅ KernelTestCase — boots the kernel and exposes the container, without an HTTP client**

    KernelTestCase boots the kernel and gives you self::getContainer() with no browser. WebTestCase adds the HTTP client and is reserved for tests that make requests; a plain TestCase boots no kernel at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#integration-tests)

??? question "14. Which utility tests a console command's output and exit code without a real terminal?"
    **✅ CommandTester — call execute([...]) then getDisplay() and getStatusCode()**

    Symfony\Component\Console\Tester\CommandTester wraps a single command: execute() supplies input, then getDisplay() returns captured output and getStatusCode() the exit code. ApplicationTester covers the whole app.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html#testing-commands)

??? question "15. Given config/packages/test/framework.yaml containing `framework: { test: true }`, what does the `test: true` flag enable?"
    **✅ The test.client (KernelBrowser) service and the special test container that exposes private services**

    framework.test: true registers the test.client service (returned by createClient()) and triggers the compiler passes that build the TestContainer exposing used private/non-shared services. Without it, createClient() cannot find test.client. It does not toggle redirect following (a client method) nor the profiler, and it only affects the test environment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#test)

??? question "16. What does static::createClient() do to the kernel before returning the client?"
    **✅ It reboots the kernel so the test starts from fresh container state**

    createClient() boots (or reboots) the kernel before handing back the KernelBrowser, guaranteeing clean state. The client also reboots the kernel after each request unless you call disableReboot(). It does not reuse a stale kernel, and it does not disable rebooting by default — that is an explicit opt-out.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#application-tests)

??? question "17. True or False: WebTestCase is a subclass of KernelTestCase, and its only substantive addition is the HTTP client."
    **✅ True**

    WebTestCase extends KernelTestCase; the browser client (createClient() returning a KernelBrowser) is what it adds on top of the kernel-booting and container-access behaviour it inherits. If you do not need HTTP, use KernelTestCase directly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#application-tests)

??? question "18. A private service is never injected anywhere. In the test environment it is…"
    **✅ Still removed — the test container only keeps services that are actually used**

    Unused private services are optimised away even in the test container; only used private/non-shared services remain reachable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#accessing-the-container)

??? question "19. To swap a real service for a mock before making a request in a functional test, you should…"
    **✅ Fetch the test container with self::getContainer() and call ->set('service.id', $mock) before the request**

    The test container returned by self::getContainer() allows ->set() to override a (used) service with a double. Do this before issuing the request so the kernel uses the replacement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#mocking-services)

??? question "20. What builds the TestContainer (id test.service_container) that keeps otherwise-private services reachable?"
    **✅ Compiler passes enabled by framework.test: true (the TestServiceContainer weak/real-ref passes)**

    When framework.test: true, dedicated compiler passes (TestServiceContainerWeakRefPass / RealRefPass) build a second container, TestContainer (test.service_container), that retains references to used private/non-shared services. It is a compile-time construct, not runtime reflection, and unused private services are still removed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#accessing-the-container)

??? question "21. A test does: $client = static::createClient(); then self::getContainer()->set(PaymentGateway::class, $mock); then $client->request('POST', '/checkout'); — but the real gateway still runs. What is the most likely fix?"
    **✅ Call $client->disableReboot() before set(), so the replacement survives the reboot that createClient triggers on the next request**

    By default the kernel reboots (rebuilding a fresh container) around requests, discarding any set() replacement. disableReboot() keeps the container — and your mock — alive across the request. Calling set() after the request is too late; the class already has visibility (getContainer exposes it); and $kernel->getContainer() hides private services entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#mocking-services)

??? question "22. How do you access the test container in a modern Symfony 8 test?"
    **✅ self::getContainer() — the old static::$container property was removed**

    The historical static::$container property is gone; call the self::getContainer() method, which returns the TestContainer. $this->container does not exist on the base test classes, and static::$kernel->getContainer() returns the normal container where private services are hidden.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#accessing-the-container)

??? question "23. Your controller depends on the current time and an external SMS gateway. What is the best testing approach?"
    **✅ Replace only the boundaries — swap in a MockClock via ClockInterface and a gateway double — keeping the rest of the graph real**

    Replace only external boundaries you must not hit (SMS) or must make deterministic (time via injected ClockInterface + MockClock), leaving the rest of the wiring real so the test proves integration. Mocking everything tests nothing; insulate() runs a subprocess and would still call the real gateway; hand-instantiating with nulls abandons the point of a functional test.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#mocking-services)

??? question "24. What does $client->request('GET', '/') return?"
    **✅ A Symfony\Component\DomCrawler\Crawler**

    Navigation methods return a Crawler over the response DOM. Fetch the response object with $client->getResponse().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#making-requests)

??? question "25. By default, after a controller returns a 302 redirect, the test client…"
    **✅ Stops on the redirect so you can assert the Location, until you call followRedirect()**

    Auto-follow is off by default. Use followRedirect() to follow the last redirect once, or followRedirects() to toggle auto-following.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#redirecting)

??? question "26. Which method keeps a service replaced via getContainer()->set() alive across multiple requests?"
    **✅ $client->disableReboot()**

    By default the kernel reboots after each request, discarding replacements. disableReboot() preserves the container between requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#mocking-services)

??? question "27. A test calls $client->followRedirect() and gets a LogicException. What is the cause?"
    **✅ The last response was not a redirect (no 3xx / Location to follow)**

    followRedirect() follows the last redirect once; if the previous response was not a 3xx there is nothing to follow and it throws a LogicException. It is unrelated to setUp(), css-selector, or the profiler. Assert the redirect first (assertResponseRedirects) before following it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#redirecting)

??? question "28. What is the difference between $client->followRedirect() and $client->followRedirects()?"
    **✅ followRedirect() follows the last redirect once; followRedirects() toggles automatic following for subsequent requests**

    followRedirect() (singular) acts once on the last redirect. followRedirects(true|false) (plural) switches auto-following on or off for the rest of the test. Swapping their meaning is a classic exam trap; followRedirects() is a mode toggle, not a one-shot action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#redirecting)

??? question "29. What is the signature of KernelBrowser::submitForm()?"
    **✅ submitForm(string $button, array $fieldValues = [], string $method = 'POST')**

    You identify the submit button by its text/name/id/value first, then pass the field values and optionally the HTTP method. submitForm() locates the enclosing form for you; if you already hold a Form object, use submit($form).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#submitting-forms)

??? question "30. How does the KernelBrowser actually perform a request?"
    **✅ It converts the BrowserKit request to an HttpFoundation request and calls HttpKernel::handle() in-process — no real network**

    KernelBrowser extends AbstractBrowser; doRequest() builds an HttpFoundation Request and passes it straight to HttpKernel::handle(), so the whole stack (routing, controllers, security) runs in-process with no network. The browser keeps a cookie jar and history from the responses.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#making-requests)

??? question "31. $crawler->filter('div.item') requires which component to be installed?"
    **✅ symfony/css-selector**

    filter() converts the CSS selector to XPath via CssSelectorConverter, so the css-selector component is required. filterXPath() works without it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dom_crawler.html)

??? question "32. $crawler->filter('.missing')->text() throws an InvalidArgumentException. Why, and how do you avoid it?"
    **✅ text() reads the first node and throws on an empty set; pass a default: ->text('') **

    Node-reading methods (text(), attr(), html(), nodeName()) operate on the first matched node and throw when the Crawler is empty, unless you supply a default argument, e.g. text(''). The selector is valid CSS and browser-kit is unrelated; html() would throw identically on an empty set.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dom_crawler.html#node-values)

??? question "33. Which Crawler methods return a NEW Crawler (a subset) rather than reading a scalar value? (choose 3)"
    **✅ filter('css') ; filterXPath('//x') ; first()**

    The Crawler is immutable: filter(), filterXPath(), first()/last()/eq() all return a new Crawler holding the matched subset. text() and attr() instead read a scalar from the first node (and throw on an empty set without a default), so they are not node-set operations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dom_crawler.html)

??? question "34. Internally, how does Crawler::filter() evaluate a CSS selector?"
    **✅ It converts the CSS to XPath via CssSelectorConverter, then delegates to filterXPath()**

    filter() uses Symfony\Component\CssSelector\CssSelectorConverter to turn the CSS selector into an XPath expression and then calls filterXPath(); this is why the css-selector component is required for filter() but not for filterXPath(). There is no regex-over-HTML or browser-kit involvement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/dom_crawler.html)

??? question "35. $crawler->selectButton('Save')->form(['title' => 'x']) returns…"
    **✅ A Form pre-filled with the page's current values, with 'title' overridden**

    form() builds a Symfony\Component\DomCrawler\Form seeded from the DOM's existing field values; the array argument overrides just the fields you name, leaving the rest at their rendered defaults. It is not a plain array, a Response, nor an empty form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#forms)

??? question "36. To follow an anchor with $client->click(), you first obtain a Link with…"
    **✅ $crawler->selectLink('Text')->link()**

    selectLink() matches anchors by their visible text (or image alt), and ->link() builds a DomCrawler\Link you pass to $client->click(). There is no href() or getLink() convenience returning a Link, and Link is not constructed directly from a Crawler in tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#clicking-links)

??? question "37. For which HTTP status codes does assertResponseIsSuccessful() pass?"
    **✅ Any 2xx status**

    It asserts the response is in the successful (2xx) range. Use assertResponseStatusCodeSame(n) to check an exact code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#the-assertions)

??? question "38. Which assertion checks that an element's text is exactly equal (not a substring)?"
    **✅ assertSelectorTextSame('h1', 'Hi')**

    The ...Same variant requires an exact match; ...Contains checks a substring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#the-assertions)

??? question "39. What does the WebTestCase helper assertResponseIsSuccessful() verify?"
    **✅ That the last response has a 2xx status code**

    assertResponseIsSuccessful() passes for any 2xx status. These assertResponse*/assertSelector* helpers come from the BrowserKit/DomCrawler assertion traits mixed into WebTestCase; assertSelectorTextContains() checks a CSS-selected element's text.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#testing-the-response-status-code-headers-and-content)

??? question "40. After a POST that returns a 302, a test does assertSelectorTextContains('h1', 'Welcome') and it fails even though the target page has that heading. Why?"
    **✅ The current DOM is the redirect (302) page, not the target; you must followRedirect() first**

    Redirects are not followed automatically, so the Crawler still holds the (near-empty) 302 response, not the destination page. Calling followRedirect() before the selector assertion loads the target DOM. The assertion works fine after POST and does not depend on a prior status assertion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#redirecting)

??? question "41. What does assertResponseRedirects() with no arguments assert?"
    **✅ Only that the response is a redirect (3xx) — pass a target URL and/or code to be specific**

    With no arguments it merely checks the response is a 3xx redirect. Provide assertResponseRedirects('/target', 302) to also assert the Location and/or the exact status. It does not follow the redirect nor assert success.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#the-assertions)

??? question "42. Which of these are real WebTestCase assertion helpers? (choose 3)"
    **✅ assertResponseStatusCodeSame(int $code) ; assertRouteSame(string $route) ; assertResponseHasCookie(string $name)**

    assertResponseStatusCodeSame, assertRouteSame and assertResponseHasCookie all exist in the BrowserKit/WebTest assertion traits. There is no assertResponseBodyEquals (use getResponse()->getContent() with a PHPUnit string assertion) nor assertControllerSame helper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#the-assertions)

??? question "43. A form submission with invalid data re-renders the form with HTTP 422. Which assertion best expresses "the response is a 422 Unprocessable Content"?"
    **✅ self::assertResponseIsUnprocessable()**

    assertResponseIsUnprocessable() is the dedicated helper for a 422 status, the conventional code for a form redisplayed with validation errors. assertResponseIsSuccessful() would fail (422 is not 2xx), redirects apply to 3xx, and asserting an error element checks content, not the status.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#the-assertions)

??? question "44. When must $client->enableProfiler() be called?"
    **✅ Before the request whose profile you want to read**

    enableProfiler() opts the next request into profiling; calling it after the request collects nothing and getProfile() returns false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing/profiling.html)

??? question "45. The recommended way to assert that an email was sent in a functional test is…"
    **✅ assertEmailCount() / getMailerMessage() from MailerAssertionsTrait**

    WebTestCase provides mailer assertions backed by the mailer data collector, so you rarely touch the raw collector.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/mailer.html#testing-emails)

??? question "46. $client->getProfile() when profiling was not enabled returns…"
    **✅ false**

    getProfile() returns boolean false (not null, not an empty Profile, and it does not throw) when no profile was collected — typically because enableProfiler() was not called before the request. Guard with assertNotFalse($profile) before reading collectors.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing/profiling.html)

??? question "47. In the test environment, framework.profiler.collect defaults to…"
    **✅ false — profiles are collected only for requests opted in with enableProfiler()**

    The test profiler config sets collect: false for speed, so profiling is off unless a test calls enableProfiler() before the request. It is fully configurable and is not limited to redirects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#profiler)

??? question "48. A test does: $client->request('GET', '/'); $client->enableProfiler(); $profile = $client->getProfile(); — what is $profile?"
    **✅ false — enableProfiler() was called after the request, so nothing was collected**

    enableProfiler() opts in the NEXT request; here it runs after the only request, so that request was never profiled and getProfile() returns false. The call order must be enableProfiler() then request() then getProfile().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing/profiling.html)

??? question "49. You need to assert which route matched and how long a request took — data not visible in the HTML. What do you do?"
    **✅ enableProfiler() before the request, then read $profile->getCollector('request') and getCollector('time')**

    The profiler exposes internals through named data collectors (request, time, events, mailer). Enable it before the request, then read the collectors from the Profile. assertRouteSame covers the route but not the duration; insulate() actually removes in-process profiler access.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing/profiling.html)

??? question "50. What is the second argument of static::createClient()?"
    **✅ An array of default server parameters (the $_SERVER bag)**

    createClient(array $options, array $server) — the second array models server parameters (HTTP_* headers, HTTPS, PHP_AUTH_USER, etc.).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

??? question "51. To simulate an 'Accept: application/json' request header via server parameters you set…"
    **✅ 'HTTP_ACCEPT' => 'application/json'**

    Request headers become HTTP_-prefixed server parameters. CONTENT_TYPE, HTTPS, PHP_AUTH_USER and PHP_AUTH_PW are the unprefixed exceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

??? question "52. What does $client->loginUser($user) do?"
    **✅ Authenticates the session with the given UserInterface, skipping the login form**

    loginUser() injects a security token for a real user object so you can test authorized behaviour without driving the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#logging-in-users-authentication)

??? question "53. What is the effect of $client->insulate()?"
    **✅ Each request runs in a separate PHP subprocess, so in-process profiler/container access is lost**

    Insulated requests run in a fresh subprocess to isolate global state, at the cost of losing in-process access to the profiler and container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/browser_kit.html)

??? question "54. Which server parameters are NOT written with the HTTP_ prefix? (choose 3)"
    **✅ CONTENT_TYPE ; PHP_AUTH_USER ; HTTPS**

    Following CGI conventions, request headers are exposed as HTTP_<NAME>, but CONTENT_TYPE, HTTPS, PHP_AUTH_USER and PHP_AUTH_PW are special-cased with no prefix. HTTP_ACCEPT and HTTP_X_REQUESTED_WITH are ordinary headers and keep the prefix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

??? question "55. A test writes $client->request('GET', '/admin', ['PHP_AUTH_USER' => 'admin', 'PHP_AUTH_PW' => 'secret']) and authentication fails. What is wrong?"
    **✅ Server params are the 5th argument of request(); the 3rd is $parameters (query/POST). The auth belongs in $server**

    request(string $method, string $uri, array $parameters = [], array $files = [], array $server = [], ...): the credentials were passed as $parameters (query/POST data) instead of the 5th $server argument. PHP_AUTH_USER is correctly unprefixed, and Basic auth is testable via server params — the position is the bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

??? question "56. $client->loginUser($user) has no effect (the page still redirects to /login). What is a likely cause?"
    **✅ There is no configured firewall for the path, or the wrong firewall name was targeted, so no token context is stored**

    loginUser() stores a pre-authenticated token in the session for a firewall; it needs a real UserInterface and a properly configured firewall covering the requested path (and, for multiple firewalls, the correct firewall name). It is independent of the profiler and insulate(), and its whole point is to skip the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#logging-in-users-authentication)

??? question "57. static::createClient(['debug' => false], ['HTTPS' => true, 'HTTP_HOST' => 'api.example.com']) configures what?"
    **✅ Kernel boot options (debug off) plus default server params (HTTPS + host) applied to every request from this client**

    The first array is kernel options (environment/debug); the second is default server parameters merged into every subsequent request(). No request is sent yet, 'debug' is a boolean option (not an environment name), and the values are defaults, not a one-off request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/testing.html#configuring-the-test-client)

??? question "58. Which class must be registered to enable the PHPUnit bridge's deprecation collection and clock/DNS mocking?"
    **✅ Symfony\Bridge\PhpUnit\SymfonyExtension**

    The bridge's PHPUnit extension (registered under <extensions><bootstrap .../>) wires the DeprecationErrorHandler, ClockMock and DnsMock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

??? question "59. How is SYMFONY_DEPRECATIONS_HELPER supplied to PHPUnit?"
    **✅ As an environment/server variable (e.g. in phpunit.dist.xml <php>)**

    It is read from the environment; commonly set via <php><server name="SYMFONY_DEPRECATIONS_HELPER" .../></php> or the shell.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration)

??? question "60. Which SYMFONY_DEPRECATIONS_HELPER value makes the build fail on the very first deprecation?"
    **✅ max[total]=0**

    max[total]=0 sets a zero threshold, so any deprecation fails the suite. weak reports without failing, and disabled=1 turns collection off entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration)

??? question "61. In phpunit.dist.xml, how is the bridge's extension registered in PHPUnit 11/12?"
    **✅ <extensions><bootstrap class="Symfony\Bridge\PhpUnit\SymfonyExtension"/></extensions>**

    PHPUnit 10+ uses the <extensions><bootstrap .../></extensions> mechanism to load the SymfonyExtension. The old <listeners><listener> (SymfonyTestsListener) approach belongs to PHPUnit 9 and earlier; there is no <php><extension> tag, and the extension is not auto-registered.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

??? question "62. Your test calls sleep(61) expecting it to be instant (mocked), but it actually sleeps. What is missing?"
    **✅ The test (or class) is not in the time-sensitive group, so ClockMock does not override the time functions**

    ClockMock only overrides time(), sleep(), microtime(), etc. for tests in the time-sensitive group (#[Group('time-sensitive')]); without that group the real functions run. The extension handles registration, sleep() IS among the mocked functions, and the deprecations helper is unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#time-sensitive-tests)

??? question "63. A service injects Symfony\Component\Clock\ClockInterface. What is the cleanest way to control time in its test?"
    **✅ Inject a Symfony\Component\Clock\MockClock and advance it, instead of using ClockMock and the time-sensitive group**

    For code that injects ClockInterface, swapping a MockClock (which you can advance deterministically) is cleaner and needs no group magic. ClockMock + time-sensitive is the tool for legacy code calling global time()/sleep() directly. Real sleep() is slow, and a one-shot createMock stub cannot model advancing time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/clock.html#writing-time-sensitive-tests)

??? question "64. True or False: the bin/simple-phpunit wrapper is the recommended way to run the suite in Symfony 8."
    **✅ False**

    The legacy simple-phpunit wrapper is deprecated in favour of registering SymfonyExtension in the PHPUnit config and running plain PHPUnit (bin/phpunit). The extension provides the same deprecation collection and clock/DNS mocking without the wrapper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

??? question "65. A deprecation triggered deep inside a vendor library's own internals is classified as…"
    **✅ indirect**

    self = your code, direct = a dependency you call directly, indirect = deep inside a dependency's internals, legacy = tests excluded from thresholds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail)

??? question "66. What does SYMFONY_DEPRECATIONS_HELPER=weak do?"
    **✅ Reports deprecations but never fails the build**

    weak collects and prints deprecations without enforcing thresholds. disabled=1 turns collection off; max[...] enforces limits.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration)

??? question "67. The modern way to silence a single test's expected deprecations is…"
    **✅ The #[IgnoreDeprecations] attribute**

    Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations replaces the old @group legacy for excluding a test's deprecations from the report.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html)

??? question "68. Match the deprecation buckets correctly. Which statements are TRUE? (choose 3)"
    **✅ self = triggered by your own code's namespace ; direct = triggered by a dependency you called directly ; legacy = deprecations from tests marked legacy, never counted against thresholds**

    self is your code, direct is a dependency you call directly, indirect is deep inside a dependency's internals, and legacy (marked tests) is excluded from thresholds. The two false options swap direct/indirect and mislabel indirect as your own setup.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail)

??? question "69. You want to assert that calling a method emits a specific deprecation. Which is correct in Symfony 8?"
    **✅ use ExpectUserDeprecationMessageTrait; then $this->expectUserDeprecationMessage('Since app 2.0: ...') before the call**

    ExpectUserDeprecationMessageTrait::expectUserDeprecationMessage() is the current API for asserting an emitted E_USER_DEPRECATED message. The old ExpectDeprecationTrait::expectDeprecation() and the @expectedDeprecation annotation were removed in Symfony 7.0, and deprecations are not exceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail)

??? question "70. What is the difference between weak and disabled=1?"
    **✅ weak still collects and reports deprecations (just never fails); disabled=1 stops collection entirely**

    weak keeps collecting and printing the grouped report but never enforces a threshold, so you retain visibility. disabled=1 turns the handler off so nothing is collected or reported. The pair is a common trap when their behaviours are swapped; neither of them fails the build.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#configuration)

??? question "71. A legacy suite emits hundreds of known deprecations, but you want CI to fail only on NEW ones. What do you do?"
    **✅ Generate a baseline (baselineFile=...&generateBaseline=true), commit it, then run with baselineFile=... so only new deprecations fail**

    A baseline records currently-known deprecations to a JSON file that later runs ignore, so only new deprecations fail the build — and you shrink it over time. disabled=1 and weak both remove the safety net for new deprecations, and blanket #[IgnoreDeprecations] hides everything, including regressions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/phpunit_bridge.html#making-tests-fail)

---

<small>Back to [Flashcards](index.md) · [Automated Tests](../../testing/index.md)</small>
