# Chapter Exam — Automated Tests

!!! abstract "How to use"
    71 questions spanning every subchapter of **Automated Tests**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Automated Tests](../testing/index.md).

---

**Q1.** Which base class do Symfony unit tests extend for pure, kernel-free logic?  <small>_(easy · single)_</small>

- A. PHPUnit\Framework\TestCase
- B. Symfony\Bundle\FrameworkBundle\Test\WebTestCase
- C. Symfony\Bundle\FrameworkBundle\Test\KernelTestCase
- D. Symfony\Component\Test\UnitTestCase

??? success "Answer Q1"
    **A**

    Symfony ships no unit-test base class; pure unit tests extend PHPUnit's TestCase directly. No kernel is booted and no container is built.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#unit-tests)

**Q2.** In PHPUnit 11/12, how do you bind a test to a data provider?  <small>_(easy · single)_</small>

- A. #[DataProvider('methodName')] naming a public static method
- B. @dataProvider methodName in the docblock
- C. #[Provider('methodName')] naming a private method
- D. $this->provide('methodName') inside the test

??? success "Answer Q2"
    **A**

    The @dataProvider annotation is removed; use the PHPUnit\Framework\Attributes\DataProvider attribute pointing at a public static iterable-returning method.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

**Q3.** You need only canned return values, with no verification of how a collaborator is called. Which double do you create?  <small>_(easy · single)_</small>

- A. A stub via $this->createStub(Foo::class)
- B. A mock via $this->createMock(Foo::class) with expects()
- C. A spy via $this->createSpy(Foo::class)
- D. A partial mock via getMockForTrait()

??? success "Answer Q3"
    **A**

    A stub supplies return values but never asserts interactions. A mock adds verifiable expectations you do not need here.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/test-doubles.html)

**Q4.** True or False: PHPUnit creates a fresh instance of the test class for every test method, so state set in one test does not leak into another.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q4"
    **A**

    PHPUnit reflects over the TestCase subclass and, for each test method, builds a new instance, runs setUp(), the test, then tearDown(). Instance properties therefore never carry over between test methods; only static properties (which you should avoid) can leak state.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html)

**Q5.** How are WebTestCase and KernelTestCase related?  <small>_(easy · single)_</small>

- A. WebTestCase extends KernelTestCase, adding the HTTP client (createClient())
- B. KernelTestCase extends WebTestCase
- C. They are unrelated base classes
- D. Both extend BrowserTestCase

??? success "Answer Q5"
    **A**

    WebTestCase adds the KernelBrowser client on top of the kernel-booting KernelTestCase. Use KernelTestCase when you need only the container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#application-tests)

**Q6.** How many times may createClient() be called within a single test?  <small>_(easy · single)_</small>

- A. Once — a second call throws
- B. Twice
- C. Any number of times
- D. Once per HTTP request

??? success "Answer Q6"
    **A**

    Only one kernel/client may be booted per test; calling createClient() again throws a LogicException.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#your-first-application-test)

**Q7.** True or False: WebTestCase is a subclass of KernelTestCase, and its only substantive addition is the HTTP client.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q7"
    **A**

    WebTestCase extends KernelTestCase; the browser client (createClient() returning a KernelBrowser) is what it adds on top of the kernel-booting and container-access behaviour it inherits. If you do not need HTTP, use KernelTestCase directly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#application-tests)

**Q8.** What does $client->request('GET', '/') return?  <small>_(easy · single)_</small>

- A. A Symfony\Component\DomCrawler\Crawler
- B. A Symfony\Component\HttpFoundation\Response
- C. A Symfony\Component\HttpFoundation\Request
- D. void

??? success "Answer Q8"
    **A**

    Navigation methods return a Crawler over the response DOM. Fetch the response object with $client->getResponse().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#making-requests)

**Q9.** By default, after a controller returns a 302 redirect, the test client…  <small>_(easy · single)_</small>

- A. Stops on the redirect so you can assert the Location, until you call followRedirect()
- B. Follows the redirect automatically
- C. Throws an exception
- D. Retries the original request

??? success "Answer Q9"
    **A**

    Auto-follow is off by default. Use followRedirect() to follow the last redirect once, or followRedirects() to toggle auto-following.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#redirecting)

**Q10.** Which method keeps a service replaced via getContainer()->set() alive across multiple requests?  <small>_(easy · single)_</small>

- A. $client->disableReboot()
- B. $client->followRedirects()
- C. $client->insulate()
- D. $client->restart()

??? success "Answer Q10"
    **A**

    By default the kernel reboots after each request, discarding replacements. disableReboot() preserves the container between requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q11.** To follow an anchor with $client->click(), you first obtain a Link with…  <small>_(easy · single)_</small>

- A. $crawler->selectLink('Text')->link()
- B. $crawler->filter('a')->href()
- C. $crawler->getLink('Text')
- D. new Link($crawler)

??? success "Answer Q11"
    **A**

    selectLink() matches anchors by their visible text (or image alt), and ->link() builds a DomCrawler\Link you pass to $client->click(). There is no href() or getLink() convenience returning a Link, and Link is not constructed directly from a Crawler in tests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#clicking-links)

**Q12.** For which HTTP status codes does assertResponseIsSuccessful() pass?  <small>_(easy · single)_</small>

- A. Any 2xx status
- B. Only 200
- C. 2xx and 3xx
- D. Only 200 and 204

??? success "Answer Q12"
    **A**

    It asserts the response is in the successful (2xx) range. Use assertResponseStatusCodeSame(n) to check an exact code.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

**Q13.** Which assertion checks that an element's text is exactly equal (not a substring)?  <small>_(easy · single)_</small>

- A. assertSelectorTextSame('h1', 'Hi')
- B. assertSelectorTextContains('h1', 'Hi')
- C. assertSelectorExists('h1')
- D. assertPageTitleContains('Hi')

??? success "Answer Q13"
    **A**

    The ...Same variant requires an exact match; ...Contains checks a substring.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

**Q14.** What does the WebTestCase helper assertResponseIsSuccessful() verify?  <small>_(easy · single)_</small>

- A. That the last response has a 2xx status code
- B. That the response body is non-empty
- C. That the response is exactly 200 OK
- D. That the response is a redirect

??? success "Answer Q14"
    **A**

    assertResponseIsSuccessful() passes for any 2xx status. These assertResponse*/assertSelector* helpers come from the BrowserKit/DomCrawler assertion traits mixed into WebTestCase; assertSelectorTextContains() checks a CSS-selected element's text.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#testing-the-response-status-code-headers-and-content)

**Q15.** What does assertResponseRedirects() with no arguments assert?  <small>_(easy · trap)_</small>

- A. Only that the response is a redirect (3xx) — pass a target URL and/or code to be specific
- B. That the response redirects specifically to '/' with a 302
- C. That the redirect has already been followed
- D. That the response is a successful 2xx

??? success "Answer Q15"
    **A**

    With no arguments it merely checks the response is a 3xx redirect. Provide assertResponseRedirects('/target', 302) to also assert the Location and/or the exact status. It does not follow the redirect nor assert success.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

**Q16.** When must $client->enableProfiler() be called?  <small>_(easy · single)_</small>

- A. Before the request whose profile you want to read
- B. After the request, before getProfile()
- C. Only inside setUp()
- D. Never — profiling is always on in the test environment

??? success "Answer Q16"
    **A**

    enableProfiler() opts the next request into profiling; calling it after the request collects nothing and getProfile() returns false.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

**Q17.** What is the second argument of static::createClient()?  <small>_(easy · single)_</small>

- A. An array of default server parameters (the $_SERVER bag)
- B. An array of request headers as raw strings
- C. The environment name
- D. A list of routes to register

??? success "Answer Q17"
    **A**

    createClient(array $options, array $server) — the second array models server parameters (HTTP_* headers, HTTPS, PHP_AUTH_USER, etc.).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

**Q18.** To simulate an 'Accept: application/json' request header via server parameters you set…  <small>_(easy · single)_</small>

- A. 'HTTP_ACCEPT' => 'application/json'
- B. 'ACCEPT' => 'application/json'
- C. 'HEADER_ACCEPT' => 'application/json'
- D. 'CONTENT_TYPE' => 'application/json'

??? success "Answer Q18"
    **A**

    Request headers become HTTP_-prefixed server parameters. CONTENT_TYPE, HTTPS, PHP_AUTH_USER and PHP_AUTH_PW are the unprefixed exceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

**Q19.** What does $client->loginUser($user) do?  <small>_(easy · single)_</small>

- A. Authenticates the session with the given UserInterface, skipping the login form
- B. Submits the login form with the user's credentials
- C. Creates the user record in the database
- D. Returns a signed JWT for the user

??? success "Answer Q19"
    **A**

    loginUser() injects a security token for a real user object so you can test authorized behaviour without driving the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#logging-in-users-authentication)

**Q20.** Which class must be registered to enable the PHPUnit bridge's deprecation collection and clock/DNS mocking?  <small>_(easy · single)_</small>

- A. Symfony\Bridge\PhpUnit\SymfonyExtension
- B. Symfony\Bridge\PhpUnit\PhpUnitBundle
- C. Symfony\Component\PhpUnit\Extension
- D. PHPUnit\Bridge\SymfonyExtension

??? success "Answer Q20"
    **A**

    The bridge's PHPUnit extension (registered under <extensions><bootstrap .../>) wires the DeprecationErrorHandler, ClockMock and DnsMock.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

**Q21.** What does SYMFONY_DEPRECATIONS_HELPER=weak do?  <small>_(easy · single)_</small>

- A. Reports deprecations but never fails the build
- B. Hides deprecations entirely and collects nothing
- C. Fails the build on the first deprecation
- D. Counts only self deprecations

??? success "Answer Q21"
    **A**

    weak collects and prints deprecations without enforcing thresholds. disabled=1 turns collection off; max[...] enforces limits.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

**Q22.** The modern way to silence a single test's expected deprecations is…  <small>_(easy · single)_</small>

- A. The #[IgnoreDeprecations] attribute
- B. The @group legacy docblock
- C. Calling error_reporting(0)
- D. Setting SYMFONY_DEPRECATIONS_HELPER=disabled globally

??? success "Answer Q22"
    **A**

    Symfony\Bridge\PhpUnit\Attribute\IgnoreDeprecations replaces the old @group legacy for excluding a test's deprecations from the report.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

**Q23.** What does assertSame(1, '1') do?  <small>_(medium · trap)_</small>

- A. Fails, because the types differ (strict === comparison)
- B. Passes, because the values are loosely equal
- C. Emits a deprecation
- D. Throws a TypeError

??? success "Answer Q23"
    **A**

    assertSame uses ===, so int 1 and string '1' are not the same. Use assertEquals for loose (==) comparison.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/assertions.html#assertsame)

**Q24.** A method referenced by #[DataProvider('provide')] must be…  <small>_(medium · single)_</small>

- A. public static and return an array or other iterable of argument sets
- B. private and return void
- C. a protected instance method returning a Generator only
- D. annotated with #[Test] as well

??? success "Answer Q24"
    **A**

    PHPUnit\Framework\Attributes\DataProvider names a public static method returning an iterable (array or Generator) of argument arrays; each set becomes one parameterised run of the test.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

**Q25.** In PHPUnit 10+, a data-provider method declared non-static (public function provide()) results in…  <small>_(medium · trap)_</small>

- A. An error — provider methods must be public static
- B. A silent fallback where PHPUnit instantiates the class to call it
- C. A deprecation notice but the test still runs
- D. Nothing — visibility and staticness are irrelevant to providers

??? success "Answer Q25"
    **A**

    PHPUnit 10+ requires data-provider methods to be public and static; a non-static provider is reported as an error, not a fallback or a mere deprecation. The provider is resolved before any test instance exists, so it cannot depend on instance state.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

**Q26.** When is a mock expectation such as $mock->expects(self::once())->method('x') actually verified?  <small>_(medium · internals)_</small>

- A. Automatically during the test's teardown, by PHPUnit's mock verification
- B. Immediately, the moment the mocked method is (or is not) called
- C. Only if you explicitly call $mock->verify() at the end
- D. At the start of the next test method

??? success "Answer Q26"
    **A**

    A mock records its expectations and PHPUnit verifies them at teardown; an unmet expectation (e.g. never called when once() was required) then fails the test. This is exactly what distinguishes a mock from a stub, which asserts nothing. There is no manual verify() call in normal usage.

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/test-doubles.html)

**Q27.** Why can self::getContainer()->get() return a private service in a test?  <small>_(medium · single)_</small>

- A. It returns the special test container (test.service_container) that exposes private/non-shared services
- B. All services become public in the test environment
- C. It uses reflection to bypass service visibility
- D. Private services are compiled as public only for WebTestCase

??? success "Answer Q27"
    **A**

    The test environment (framework.test: true) compiles a TestContainer that keeps references to used private/non-shared services so tests can fetch and replace them. static::$kernel->getContainer() does not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

**Q28.** You must test a service that needs the container but sends no HTTP requests. Which base class fits best?  <small>_(medium · scenario)_</small>

- A. KernelTestCase — boots the kernel and exposes the container, without an HTTP client
- B. WebTestCase — because only it can access the container
- C. PHPUnit\Framework\TestCase — the container is available by default
- D. DoctrineTestCase

??? success "Answer Q28"
    **A**

    KernelTestCase boots the kernel and gives you self::getContainer() with no browser. WebTestCase adds the HTTP client and is reserved for tests that make requests; a plain TestCase boots no kernel at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#integration-tests)

**Q29.** Which utility tests a console command's output and exit code without a real terminal?  <small>_(medium · scenario)_</small>

- A. CommandTester — call execute([...]) then getDisplay() and getStatusCode()
- B. KernelBrowser::request()
- C. ApplicationTester::run() is the only option
- D. ProcessTester

??? success "Answer Q29"
    **A**

    Symfony\Component\Console\Tester\CommandTester wraps a single command: execute() supplies input, then getDisplay() returns captured output and getStatusCode() the exit code. ApplicationTester covers the whole app.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/console.html#testing-commands)

**Q30.** Given config/packages/test/framework.yaml containing `framework: { test: true }`, what does the `test: true` flag enable?  <small>_(medium · config)_</small>

- A. The test.client (KernelBrowser) service and the special test container that exposes private services
- B. Only automatic following of redirects for every request
- C. The web profiler toolbar in the browser
- D. Making every private service public across all environments

??? success "Answer Q30"
    **A**

    framework.test: true registers the test.client service (returned by createClient()) and triggers the compiler passes that build the TestContainer exposing used private/non-shared services. Without it, createClient() cannot find test.client. It does not toggle redirect following (a client method) nor the profiler, and it only affects the test environment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/configuration/framework.html#test)

**Q31.** To swap a real service for a mock before making a request in a functional test, you should…  <small>_(medium · single)_</small>

- A. Fetch the test container with self::getContainer() and call ->set('service.id', $mock) before the request
- B. Reassign the property on the kernel's compiled container
- C. Edit config/services.yaml from within the test
- D. Mocks cannot replace services in functional tests

??? success "Answer Q31"
    **A**

    The test container returned by self::getContainer() allows ->set() to override a (used) service with a double. Do this before issuing the request so the kernel uses the replacement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q32.** How do you access the test container in a modern Symfony 8 test?  <small>_(medium · trap)_</small>

- A. self::getContainer() — the old static::$container property was removed
- B. static::$container — still the recommended property
- C. $this->container, injected automatically into every TestCase
- D. static::$kernel->getContainer(), which exposes private services

??? success "Answer Q32"
    **A**

    The historical static::$container property is gone; call the self::getContainer() method, which returns the TestContainer. $this->container does not exist on the base test classes, and static::$kernel->getContainer() returns the normal container where private services are hidden.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

**Q33.** Your controller depends on the current time and an external SMS gateway. What is the best testing approach?  <small>_(medium · scenario)_</small>

- A. Replace only the boundaries — swap in a MockClock via ClockInterface and a gateway double — keeping the rest of the graph real
- B. Mock every collaborator the controller touches, including the class under test
- C. Use insulate() so the real gateway and real clock run in a subprocess
- D. Avoid the container and instantiate the controller manually with all-null dependencies

??? success "Answer Q33"
    **A**

    Replace only external boundaries you must not hit (SMS) or must make deterministic (time via injected ClockInterface + MockClock), leaving the rest of the wiring real so the test proves integration. Mocking everything tests nothing; insulate() runs a subprocess and would still call the real gateway; hand-instantiating with nulls abandons the point of a functional test.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q34.** A test calls $client->followRedirect() and gets a LogicException. What is the cause?  <small>_(medium · debug)_</small>

- A. The last response was not a redirect (no 3xx / Location to follow)
- B. followRedirect() may only be called inside setUp()
- C. The css-selector component is not installed
- D. The profiler was not enabled before the request

??? success "Answer Q34"
    **A**

    followRedirect() follows the last redirect once; if the previous response was not a 3xx there is nothing to follow and it throws a LogicException. It is unrelated to setUp(), css-selector, or the profiler. Assert the redirect first (assertResponseRedirects) before following it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#redirecting)

**Q35.** What is the difference between $client->followRedirect() and $client->followRedirects()?  <small>_(medium · trap)_</small>

- A. followRedirect() follows the last redirect once; followRedirects() toggles automatic following for subsequent requests
- B. They are aliases for the same behaviour
- C. followRedirect() toggles auto-follow; followRedirects() follows exactly one redirect
- D. followRedirects() follows all pending redirects immediately for the current response only

??? success "Answer Q35"
    **A**

    followRedirect() (singular) acts once on the last redirect. followRedirects(true|false) (plural) switches auto-following on or off for the rest of the test. Swapping their meaning is a classic exam trap; followRedirects() is a mode toggle, not a one-shot action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#redirecting)

**Q36.** What is the signature of KernelBrowser::submitForm()?  <small>_(medium · code)_</small>

- A. submitForm(string $button, array $fieldValues = [], string $method = 'POST')
- B. submitForm(array $fieldValues, string $button)
- C. submitForm(Form $form)
- D. submitForm(string $uri, array $data)

??? success "Answer Q36"
    **A**

    You identify the submit button by its text/name/id/value first, then pass the field values and optionally the HTTP method. submitForm() locates the enclosing form for you; if you already hold a Form object, use submit($form).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#submitting-forms)

**Q37.** $crawler->filter('div.item') requires which component to be installed?  <small>_(medium · single)_</small>

- A. symfony/css-selector
- B. symfony/browser-kit
- C. symfony/http-client
- D. None — CSS support is built into DomCrawler

??? success "Answer Q37"
    **A**

    filter() converts the CSS selector to XPath via CssSelectorConverter, so the css-selector component is required. filterXPath() works without it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dom_crawler.html)

**Q38.** $crawler->filter('.missing')->text() throws an InvalidArgumentException. Why, and how do you avoid it?  <small>_(medium · debug)_</small>

- A. text() reads the first node and throws on an empty set; pass a default: ->text('') 
- B. text() always throws; you must use html() instead
- C. The selector syntax is invalid; only XPath is allowed in text()
- D. text() requires the browser-kit component that is missing

??? success "Answer Q38"
    **A**

    Node-reading methods (text(), attr(), html(), nodeName()) operate on the first matched node and throw when the Crawler is empty, unless you supply a default argument, e.g. text(''). The selector is valid CSS and browser-kit is unrelated; html() would throw identically on an empty set.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dom_crawler.html#node-values)

**Q39.** $crawler->selectButton('Save')->form(['title' => 'x']) returns…  <small>_(medium · trap)_</small>

- A. A Form pre-filled with the page's current values, with 'title' overridden
- B. A raw array of POST data
- C. A Response
- D. A brand-new empty Form with only 'title' set

??? success "Answer Q39"
    **A**

    form() builds a Symfony\Component\DomCrawler\Form seeded from the DOM's existing field values; the array argument overrides just the fields you name, leaving the rest at their rendered defaults. It is not a plain array, a Response, nor an empty form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#forms)

**Q40.** A form submission with invalid data re-renders the form with HTTP 422. Which assertion best expresses "the response is a 422 Unprocessable Content"?  <small>_(medium · code)_</small>

- A. self::assertResponseIsUnprocessable()
- B. self::assertResponseRedirects()
- C. self::assertResponseIsSuccessful()
- D. self::assertSelectorExists('.error')

??? success "Answer Q40"
    **A**

    assertResponseIsUnprocessable() is the dedicated helper for a 422 status, the conventional code for a form redisplayed with validation errors. assertResponseIsSuccessful() would fail (422 is not 2xx), redirects apply to 3xx, and asserting an error element checks content, not the status.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

**Q41.** The recommended way to assert that an email was sent in a functional test is…  <small>_(medium · single)_</small>

- A. assertEmailCount() / getMailerMessage() from MailerAssertionsTrait
- B. Reading Doctrine's db data collector
- C. Parsing the response HTML for the email body
- D. Inspecting the SMTP server logs

??? success "Answer Q41"
    **A**

    WebTestCase provides mailer assertions backed by the mailer data collector, so you rarely touch the raw collector.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/mailer.html#testing-emails)

**Q42.** $client->getProfile() when profiling was not enabled returns…  <small>_(medium · trap)_</small>

- A. false
- B. null
- C. An empty Profile object
- D. It throws a LogicException

??? success "Answer Q42"
    **A**

    getProfile() returns boolean false (not null, not an empty Profile, and it does not throw) when no profile was collected — typically because enableProfiler() was not called before the request. Guard with assertNotFalse($profile) before reading collectors.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

**Q43.** In the test environment, framework.profiler.collect defaults to…  <small>_(medium · config)_</small>

- A. false — profiles are collected only for requests opted in with enableProfiler()
- B. true — every request is profiled automatically
- C. true, but only for redirect responses
- D. It cannot be configured in the test environment

??? success "Answer Q43"
    **A**

    The test profiler config sets collect: false for speed, so profiling is off unless a test calls enableProfiler() before the request. It is fully configurable and is not limited to redirects.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/reference/configuration/framework.html#profiler)

**Q44.** You need to assert which route matched and how long a request took — data not visible in the HTML. What do you do?  <small>_(medium · scenario)_</small>

- A. enableProfiler() before the request, then read $profile->getCollector('request') and getCollector('time')
- B. Parse the rendered HTML for a hidden debug comment
- C. Use assertRouteSame() and assertResponseIsSuccessful() only — collectors are unnecessary
- D. Call insulate() so the profiler data is serialized back to the test

??? success "Answer Q44"
    **A**

    The profiler exposes internals through named data collectors (request, time, events, mailer). Enable it before the request, then read the collectors from the Profile. assertRouteSame covers the route but not the duration; insulate() actually removes in-process profiler access.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

**Q45.** What is the effect of $client->insulate()?  <small>_(medium · single)_</small>

- A. Each request runs in a separate PHP subprocess, so in-process profiler/container access is lost
- B. Redirects are followed automatically
- C. The same kernel instance is reused forever
- D. Responses are cached between tests

??? success "Answer Q45"
    **A**

    Insulated requests run in a fresh subprocess to isolate global state, at the cost of losing in-process access to the profiler and container.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/browser_kit.html)

**Q46.** $client->loginUser($user) has no effect (the page still redirects to /login). What is a likely cause?  <small>_(medium · scenario)_</small>

- A. There is no configured firewall for the path, or the wrong firewall name was targeted, so no token context is stored
- B. loginUser() only works after calling enableProfiler()
- C. The user must be persisted with the profiler enabled
- D. loginUser() requires insulate() to propagate the token
- E. You must also submit the login form afterwards

??? success "Answer Q46"
    **A**

    loginUser() stores a pre-authenticated token in the session for a firewall; it needs a real UserInterface and a properly configured firewall covering the requested path (and, for multiple firewalls, the correct firewall name). It is independent of the profiler and insulate(), and its whole point is to skip the login form.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#logging-in-users-authentication)

**Q47.** static::createClient(['debug' => false], ['HTTPS' => true, 'HTTP_HOST' => 'api.example.com']) configures what?  <small>_(medium · code)_</small>

- A. Kernel boot options (debug off) plus default server params (HTTPS + host) applied to every request from this client
- B. Two sets of request headers merged into one request only
- C. The environment name 'false' and a route host constraint
- D. A single request to https://api.example.com issued immediately

??? success "Answer Q47"
    **A**

    The first array is kernel options (environment/debug); the second is default server parameters merged into every subsequent request(). No request is sent yet, 'debug' is a boolean option (not an environment name), and the values are defaults, not a one-off request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

**Q48.** How is SYMFONY_DEPRECATIONS_HELPER supplied to PHPUnit?  <small>_(medium · single)_</small>

- A. As an environment/server variable (e.g. in phpunit.dist.xml <php>)
- B. As a PHPUnit command-line flag
- C. As a composer.json script key
- D. As a php.ini directive

??? success "Answer Q48"
    **A**

    It is read from the environment; commonly set via <php><server name="SYMFONY_DEPRECATIONS_HELPER" .../></php> or the shell.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

**Q49.** Which SYMFONY_DEPRECATIONS_HELPER value makes the build fail on the very first deprecation?  <small>_(medium · single)_</small>

- A. max[total]=0
- B. weak
- C. disabled=1
- D. verbose=0

??? success "Answer Q49"
    **A**

    max[total]=0 sets a zero threshold, so any deprecation fails the suite. weak reports without failing, and disabled=1 turns collection off entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

**Q50.** Your test calls sleep(61) expecting it to be instant (mocked), but it actually sleeps. What is missing?  <small>_(medium · trap)_</small>

- A. The test (or class) is not in the time-sensitive group, so ClockMock does not override the time functions
- B. You forgot to call ClockMock::register() manually in every test
- C. sleep() can never be mocked; only microtime() can
- D. SYMFONY_DEPRECATIONS_HELPER must be set to weak for clock mocking

??? success "Answer Q50"
    **A**

    ClockMock only overrides time(), sleep(), microtime(), etc. for tests in the time-sensitive group (#[Group('time-sensitive')]); without that group the real functions run. The extension handles registration, sleep() IS among the mocked functions, and the deprecations helper is unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#time-sensitive-tests)

**Q51.** True or False: the bin/simple-phpunit wrapper is the recommended way to run the suite in Symfony 8.  <small>_(medium · true-false)_</small>

- A. False
- B. True

??? success "Answer Q51"
    **A**

    The legacy simple-phpunit wrapper is deprecated in favour of registering SymfonyExtension in the PHPUnit config and running plain PHPUnit (bin/phpunit). The extension provides the same deprecation collection and clock/DNS mocking without the wrapper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

**Q52.** A deprecation triggered deep inside a vendor library's own internals is classified as…  <small>_(medium · trap)_</small>

- A. indirect
- B. self
- C. direct
- D. legacy

??? success "Answer Q52"
    **A**

    self = your code, direct = a dependency you call directly, indirect = deep inside a dependency's internals, legacy = tests excluded from thresholds.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#making-tests-fail)

**Q53.** What is the difference between weak and disabled=1?  <small>_(medium · trap)_</small>

- A. weak still collects and reports deprecations (just never fails); disabled=1 stops collection entirely
- B. They are identical — both hide deprecations
- C. weak stops collection; disabled=1 reports without failing
- D. weak fails on self deprecations only; disabled=1 fails on all

??? success "Answer Q53"
    **A**

    weak keeps collecting and printing the grouped report but never enforces a threshold, so you retain visibility. disabled=1 turns the handler off so nothing is collected or reported. The pair is a common trap when their behaviours are swapped; neither of them fails the build.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#configuration)

**Q54.** A legacy suite emits hundreds of known deprecations, but you want CI to fail only on NEW ones. What do you do?  <small>_(medium · scenario)_</small>

- A. Generate a baseline (baselineFile=...&generateBaseline=true), commit it, then run with baselineFile=... so only new deprecations fail
- B. Set disabled=1 permanently so nothing is reported
- C. Add #[IgnoreDeprecations] to every test in the suite
- D. Set weak so the build never turns red

??? success "Answer Q54"
    **A**

    A baseline records currently-known deprecations to a JSON file that later runs ignore, so only new deprecations fail the build — and you shrink it over time. disabled=1 and weak both remove the safety net for new deprecations, and blanket #[IgnoreDeprecations] hides everything, including regressions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#making-tests-fail)

**Q55.** A test method carries both #[TestWith([1000, 'FR', 1200])] and #[DataProvider('provideRates')], where provideRates() yields two rows. How many times does PHPUnit execute that test method?  <small>_(hard · code)_</small>

- A. Three times — the #[TestWith] row plus the two provider rows
- B. Twice — #[TestWith] is ignored when a #[DataProvider] is present
- C. Once — the attributes conflict and PHPUnit uses only the first
- D. Two times — #[TestWith] must be the only data attribute or it errors

??? success "Answer Q55"
    **A**

    #[TestWith] inlines one argument row and #[DataProvider] contributes its iterable rows; they are additive, so the method runs once per row across all data attributes (1 + 2 = 3). #[TestWith] is simply a provider that needs no separate method — it does not replace or disable #[DataProvider].

    :material-book-open-variant: [Docs](https://docs.phpunit.de/en/11.0/writing-tests-for-phpunit.html#data-providers)

**Q56.** What does static::createClient() do to the kernel before returning the client?  <small>_(hard · internals)_</small>

- A. It reboots the kernel so the test starts from fresh container state
- B. It leaves any previously booted kernel untouched and reuses it
- C. It compiles the container from scratch on every request rather than at boot
- D. It permanently disables kernel rebooting for the whole test

??? success "Answer Q56"
    **A**

    createClient() boots (or reboots) the kernel before handing back the KernelBrowser, guaranteeing clean state. The client also reboots the kernel after each request unless you call disableReboot(). It does not reuse a stale kernel, and it does not disable rebooting by default — that is an explicit opt-out.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#application-tests)

**Q57.** A private service is never injected anywhere. In the test environment it is…  <small>_(hard · trap)_</small>

- A. Still removed — the test container only keeps services that are actually used
- B. Always available via getContainer()
- C. Automatically made public
- D. Available only after calling bootKernel(['debug' => true])

??? success "Answer Q57"
    **A**

    Unused private services are optimised away even in the test container; only used private/non-shared services remain reachable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

**Q58.** What builds the TestContainer (id test.service_container) that keeps otherwise-private services reachable?  <small>_(hard · internals)_</small>

- A. Compiler passes enabled by framework.test: true (the TestServiceContainer weak/real-ref passes)
- B. A runtime call to Container::compile() inside KernelTestCase::getContainer()
- C. Reflection performed by getContainer() each time it is called
- D. The web profiler bundle registering every service as public

??? success "Answer Q58"
    **A**

    When framework.test: true, dedicated compiler passes (TestServiceContainerWeakRefPass / RealRefPass) build a second container, TestContainer (test.service_container), that retains references to used private/non-shared services. It is a compile-time construct, not runtime reflection, and unused private services are still removed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#accessing-the-container)

**Q59.** A test does: $client = static::createClient(); then self::getContainer()->set(PaymentGateway::class, $mock); then $client->request('POST', '/checkout'); — but the real gateway still runs. What is the most likely fix?  <small>_(hard · code)_</small>

- A. Call $client->disableReboot() before set(), so the replacement survives the reboot that createClient triggers on the next request
- B. Call set() again after the request
- C. Make PaymentGateway public in services.yaml
- D. Replace self::getContainer() with static::$kernel->getContainer()

??? success "Answer Q59"
    **A**

    By default the kernel reboots (rebuilding a fresh container) around requests, discarding any set() replacement. disableReboot() keeps the container — and your mock — alive across the request. Calling set() after the request is too late; the class already has visibility (getContainer exposes it); and $kernel->getContainer() hides private services entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#mocking-services)

**Q60.** How does the KernelBrowser actually perform a request?  <small>_(hard · internals)_</small>

- A. It converts the BrowserKit request to an HttpFoundation request and calls HttpKernel::handle() in-process — no real network
- B. It opens a real TCP socket to a running web server
- C. It shells out to curl for each request
- D. It renders templates directly, bypassing routing and controllers

??? success "Answer Q60"
    **A**

    KernelBrowser extends AbstractBrowser; doRequest() builds an HttpFoundation Request and passes it straight to HttpKernel::handle(), so the whole stack (routing, controllers, security) runs in-process with no network. The browser keeps a cookie jar and history from the responses.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#making-requests)

**Q61.** Which Crawler methods return a NEW Crawler (a subset) rather than reading a scalar value? (choose 3)  <small>_(hard · multiple)_</small>

- A. filter('css')
- B. filterXPath('//x')
- C. first()
- D. text()
- E. attr('href')

??? success "Answer Q61"
    **A, B, C**

    The Crawler is immutable: filter(), filterXPath(), first()/last()/eq() all return a new Crawler holding the matched subset. text() and attr() instead read a scalar from the first node (and throw on an empty set without a default), so they are not node-set operations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dom_crawler.html)

**Q62.** Internally, how does Crawler::filter() evaluate a CSS selector?  <small>_(hard · internals)_</small>

- A. It converts the CSS to XPath via CssSelectorConverter, then delegates to filterXPath()
- B. It matches CSS against the DOM directly using a native querySelectorAll binding
- C. It compiles the CSS to a regular expression over the raw HTML
- D. It sends the selector to the browser-kit engine for evaluation

??? success "Answer Q62"
    **A**

    filter() uses Symfony\Component\CssSelector\CssSelectorConverter to turn the CSS selector into an XPath expression and then calls filterXPath(); this is why the css-selector component is required for filter() but not for filterXPath(). There is no regex-over-HTML or browser-kit involvement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/dom_crawler.html)

**Q63.** After a POST that returns a 302, a test does assertSelectorTextContains('h1', 'Welcome') and it fails even though the target page has that heading. Why?  <small>_(hard · debug)_</small>

- A. The current DOM is the redirect (302) page, not the target; you must followRedirect() first
- B. assertSelectorTextContains cannot be used after a POST request
- C. h1 selectors require assertPageTitleContains instead
- D. The response status must be asserted before any selector assertion

??? success "Answer Q63"
    **A**

    Redirects are not followed automatically, so the Crawler still holds the (near-empty) 302 response, not the destination page. Calling followRedirect() before the selector assertion loads the target DOM. The assertion works fine after POST and does not depend on a prior status assertion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#redirecting)

**Q64.** Which of these are real WebTestCase assertion helpers? (choose 3)  <small>_(hard · multiple)_</small>

- A. assertResponseStatusCodeSame(int $code)
- B. assertRouteSame(string $route)
- C. assertResponseHasCookie(string $name)
- D. assertResponseBodyEquals(string $body)
- E. assertControllerSame(string $fqcn)

??? success "Answer Q64"
    **A, B, C**

    assertResponseStatusCodeSame, assertRouteSame and assertResponseHasCookie all exist in the BrowserKit/WebTest assertion traits. There is no assertResponseBodyEquals (use getResponse()->getContent() with a PHPUnit string assertion) nor assertControllerSame helper.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#the-assertions)

**Q65.** A test does: $client->request('GET', '/'); $client->enableProfiler(); $profile = $client->getProfile(); — what is $profile?  <small>_(hard · code)_</small>

- A. false — enableProfiler() was called after the request, so nothing was collected
- B. A populated Profile for the GET / request
- C. null, because enableProfiler() resets the profile
- D. A Profile containing only the time collector

??? success "Answer Q65"
    **A**

    enableProfiler() opts in the NEXT request; here it runs after the only request, so that request was never profiled and getProfile() returns false. The call order must be enableProfiler() then request() then getProfile().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing/profiling.html)

**Q66.** Which server parameters are NOT written with the HTTP_ prefix? (choose 3)  <small>_(hard · multiple)_</small>

- A. CONTENT_TYPE
- B. PHP_AUTH_USER
- C. HTTPS
- D. HTTP_ACCEPT
- E. HTTP_X_REQUESTED_WITH

??? success "Answer Q66"
    **A, B, C**

    Following CGI conventions, request headers are exposed as HTTP_<NAME>, but CONTENT_TYPE, HTTPS, PHP_AUTH_USER and PHP_AUTH_PW are special-cased with no prefix. HTTP_ACCEPT and HTTP_X_REQUESTED_WITH are ordinary headers and keep the prefix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

**Q67.** A test writes $client->request('GET', '/admin', ['PHP_AUTH_USER' => 'admin', 'PHP_AUTH_PW' => 'secret']) and authentication fails. What is wrong?  <small>_(hard · debug)_</small>

- A. Server params are the 5th argument of request(); the 3rd is $parameters (query/POST). The auth belongs in $server
- B. PHP_AUTH_USER must be HTTP_PHP_AUTH_USER
- C. Basic auth cannot be tested with the client at all
- D. You must call loginUser() instead; server params never carry credentials

??? success "Answer Q67"
    **A**

    request(string $method, string $uri, array $parameters = [], array $files = [], array $server = [], ...): the credentials were passed as $parameters (query/POST data) instead of the 5th $server argument. PHP_AUTH_USER is correctly unprefixed, and Basic auth is testable via server params — the position is the bug.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/testing.html#configuring-the-test-client)

**Q68.** In phpunit.dist.xml, how is the bridge's extension registered in PHPUnit 11/12?  <small>_(hard · config)_</small>

- A. <extensions><bootstrap class="Symfony\Bridge\PhpUnit\SymfonyExtension"/></extensions>
- B. <listeners><listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener"/></listeners>
- C. <php><extension name="symfony"/></php>
- D. It is auto-registered by Composer; no XML entry is needed

??? success "Answer Q68"
    **A**

    PHPUnit 10+ uses the <extensions><bootstrap .../></extensions> mechanism to load the SymfonyExtension. The old <listeners><listener> (SymfonyTestsListener) approach belongs to PHPUnit 9 and earlier; there is no <php><extension> tag, and the extension is not auto-registered.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html)

**Q69.** A service injects Symfony\Component\Clock\ClockInterface. What is the cleanest way to control time in its test?  <small>_(hard · scenario)_</small>

- A. Inject a Symfony\Component\Clock\MockClock and advance it, instead of using ClockMock and the time-sensitive group
- B. Put the test in the time-sensitive group and rely on ClockMock overriding global time()
- C. Call sleep() with real durations to advance the clock
- D. Mock ClockInterface with createMock() and return a fixed DateTime once

??? success "Answer Q69"
    **A**

    For code that injects ClockInterface, swapping a MockClock (which you can advance deterministically) is cleaner and needs no group magic. ClockMock + time-sensitive is the tool for legacy code calling global time()/sleep() directly. Real sleep() is slow, and a one-shot createMock stub cannot model advancing time.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/clock.html#writing-time-sensitive-tests)

**Q70.** Match the deprecation buckets correctly. Which statements are TRUE? (choose 3)  <small>_(hard · multiple)_</small>

- A. self = triggered by your own code's namespace
- B. direct = triggered by a dependency you called directly
- C. legacy = deprecations from tests marked legacy, never counted against thresholds
- D. indirect = triggered by your own test setup code
- E. direct = deep inside a dependency's internals

??? success "Answer Q70"
    **A, B, C**

    self is your code, direct is a dependency you call directly, indirect is deep inside a dependency's internals, and legacy (marked tests) is excluded from thresholds. The two false options swap direct/indirect and mislabel indirect as your own setup.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#making-tests-fail)

**Q71.** You want to assert that calling a method emits a specific deprecation. Which is correct in Symfony 8?  <small>_(hard · code)_</small>

- A. use ExpectUserDeprecationMessageTrait; then $this->expectUserDeprecationMessage('Since app 2.0: ...') before the call
- B. use ExpectDeprecationTrait; then $this->expectDeprecation('...')
- C. Annotate the test with @expectedDeprecation '...'
- D. $this->expectException(DeprecationException::class)

??? success "Answer Q71"
    **A**

    ExpectUserDeprecationMessageTrait::expectUserDeprecationMessage() is the current API for asserting an emitted E_USER_DEPRECATED message. The old ExpectDeprecationTrait::expectDeprecation() and the @expectedDeprecation annotation were removed in Symfony 7.0, and deprecations are not exceptions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/phpunit_bridge.html#making-tests-fail)

---

<small>Back to [Chapter Exams](index.md) · [Automated Tests](../testing/index.md)</small>
