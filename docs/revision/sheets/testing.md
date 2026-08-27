# Revision Sheet — Automated Tests

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Automated Tests](../../testing/index.md).

## Client Configuration
- `createClient($options, $server)`: kernel options + default server parameters.
- Headers = `HTTP_*`; `HTTPS`, `PHP_AUTH_USER`, `PHP_AUTH_PW` are unprefixed.
- `loginUser($user)` authenticates without the login form.
- `insulate()` = subprocess per request; you lose profiler/container access.

**Cheat:** `createClient(['environment'=>'test','debug'=>false], ['HTTPS'=>true])`. Per-request server params: 5th arg of `request($m,$u,$p,$files,$server)`. `setServerParameter($k,$v)` for subsequent requests. Auth: `loginUser($user)` or `PHP_AUTH_USER`/`PHP_AUTH_PW`. `insulate(true)` / `insulate(false)`.

## The Test Client
- The client is a `KernelBrowser` (extends `AbstractBrowser`) hitting the kernel
  in-process, with a cookie jar + history.
- Navigation methods return a `Crawler`; the response comes from `getResponse()`.
- Redirects are **not** followed by default: `followRedirect()` (once) vs
  `followRedirects()` (toggle).
- `disableReboot()` preserves container state / mocks between requests.

**Cheat:** `request($method, $uri, $params, $files, $server, $content)` → Crawler. `submitForm($button, $values, $method)`, `clickLink($text)`, `click($link)`. `followRedirect()` = once; `followRedirects(true|false)` = toggle. `disableReboot()`, `getCookieJar()`, `getHistory()`, `back()`, `restart()`.

## The Crawler
- The Crawler is an immutable node set; `filter()`/`filterXPath()` return subsets.
- CSS `filter()` needs the css-selector component; `filterXPath()` does not.
- `text()`/`attr()` read the first node and throw on empty sets without a default.
- `->link()` and `->form()` produce navigable/submittable objects for the client.

**Cheat:** Query: `filter('css')`, `filterXPath('//x')`, `first()`, `last()`, `eq(n)`. Select: `selectLink('text')`, `selectButton('text|name|value')`. Read: `text($default)`, `attr('href')`, `html()`, `each(fn)`, `extract([...])`. Derive: `->link()`, `->form([$overrides])`, `->image()`.

## Handling Deprecated Code in Tests
- Buckets: **self** (you) · **direct** (dep you call) · **indirect** (dep
  internals) · **legacy** (excluded).
- Modes: `max[self|direct|indirect|total]=n`, `weak` (report only),
  `disabled=1` (off), baseline (ignore known).
- `#[IgnoreDeprecations]` silences a test; `expectUserDeprecationMessage()`
  asserts one.
- Keep `max[self]=0`; use a baseline to burn down legacy debt.

**Cheat:** Env var: `SYMFONY_DEPRECATIONS_HELPER`. `max[total]=0` (any) · `max[self]=0` (yours) · `weak` · `disabled=1`. Baseline: `baselineFile=…&generateBaseline=true`, then `baselineFile=…`. Attributes/traits: `#[IgnoreDeprecations]`, `ExpectUserDeprecationMessageTrait`.

## Accessing Framework Objects in Tests
- `self::getContainer()` = the test container; it exposes **used** private services.
- `$kernel->getContainer()` keeps private services hidden — don't use it in tests.
- Replace boundary services with `set()`; pair with `disableReboot()` to persist.
- `bootKernel(['environment' => ..., 'debug' => ...])` controls how the kernel boots.

**Cheat:** Fetch: `self::getContainer()->get(Foo::class)` (private OK if used). Replace: `self::getContainer()->set(Foo::class, $mock)`. Persist replacement: `$client->disableReboot()` first. Container id: `test.service_container` (`TestContainer`).

## Functional Tests
- `WebTestCase` (HTTP + client) extends `KernelTestCase` (kernel only).
- `static::createClient()` boots the kernel and returns a `KernelBrowser`.
- `self::getContainer()` is the **test container** — private services visible.
- `framework.test: true` enables the whole test wiring; only one client per test.

**Cheat:** `KernelTestCase` → `self::bootKernel()`, `self::getContainer()`, `static::$kernel`. `WebTestCase` → `static::createClient($options, $server)` → `KernelBrowser`. Test container id: `test.service_container` (`TestContainer`). Enable via `framework.test: true` in `config/packages/test/`.

## Request/Response Introspection
- `getResponse()`/`getRequest()` expose the raw HttpFoundation objects.
- Prefer `assertResponse*`, `assertSelector*`, `assertRoute*`, `assertBrowser*`.
- `IsSuccessful` = any 2xx; use `StatusCodeSame` for an exact code.
- `...Contains` = substring, `...Same` = exact; assert *after* following redirects.

**Cheat:** Status: `assertResponseIsSuccessful()`, `assertResponseStatusCodeSame(n)`, `assertResponseIsUnprocessable()`. Redirect: `assertResponseRedirects($to?, $code?)`. Headers/cookies: `assertResponseHasHeader`, `assertResponseHeaderSame`, `assertResponseHasCookie`. DOM: `assertSelectorExists`, `assertSelectorTextContains/Same`, `assertPageTitleContains`, `assertRouteSame`.

## The Profiler in Tests
- Enable per request with `enableProfiler()` **before** `request()`.
- `getProfile()` returns a `Profile` or `false`.
- Read collectors by name: `time`, `events`, `mailer`, `request`.
- Prefer `assertEmail*` helpers over the raw mailer collector.

**Cheat:** `$client->enableProfiler();` then `$profile = $client->getProfile();`. `$profile->getCollector('time'|'events'|'mailer'|'request')`. Emails: `assertEmailCount()`, `getMailerMessage()`, `assertEmailHtmlBodyContains()`. Test default: `framework.profiler.collect: false`.

## Unit Tests with PHPUnit
- Unit tests extend `PHPUnit\Framework\TestCase`; no kernel, no container.
- PHPUnit 11/12 is attribute-only: `#[DataProvider]`, `#[TestWith]`, `#[Test]`.
- **Stub** = values; **Mock** = values + verified `expects()`.
- One fresh instance per test method — state never leaks.

**Cheat:** Base class: `PHPUnit\Framework\TestCase`. Providers: `#[DataProvider('m')]` → `public static function m(): iterable`. Inline row: `#[TestWith([1, 2, 3])]`. Doubles: `createStub()` (values) vs `createMock()` + `expects()`. Matchers: `self::once()`, `self::never()`, `self::exactly(n)`.
