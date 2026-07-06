# Flashcards — Routing

43 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. What is the fully-qualified class of the routing attribute in Symfony 8?"
    **✅ Symfony\Component\Routing\Attribute\Route**

    The routing attribute lives in the Attribute namespace since 6.4; the old Annotation\Route alias is removed in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "2. Two routes can match the same request path. Which one wins?"
    **✅ The first one declared in the RouteCollection**

    The matcher iterates the collection in declaration order and returns the first route whose host and path match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "3. A class-level #[Route('/blog', name: 'app_blog_')] contributes what to its method routes?"
    **✅ A path prefix and a name prefix**

    Class-level route data merges as prefixes: the path is prepended and the name becomes a prefix for each action's route.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#creating-routes-as-attributes)

??? question "4. Which YAML import type loads #[Route] attributes from a directory in Symfony 8?"
    **✅ type: attribute**

    Attribute route loading uses `type: attribute`; the `annotation` type is gone in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "5. A route path is /blog/{page<\d+>} and the request is /blog/latest. What happens?"
    **✅ The route does not match; matching continues (likely a 404)**

    Requirements are compiled into the route regex, so a non-matching value means the route is skipped — it is a matching concern, not validation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#parameters-validation)

??? question "6. Which two declarations are exactly equivalent?"
    **✅ {id<\d+>} and requirements: {id: '\d+'}**

    The inline <...> syntax is sugar for a matching entry in the requirements array.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#parameters-validation)

??? question "7. What is the default regex applied to a placeholder that has no requirement?"
    **✅ [^/]+**

    Placeholders match any characters except the / separator by default; use .+ to span multiple segments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "8. How do you allow a single parameter to capture several path segments (slashes)?"
    **✅ Override its requirement to .+, e.g. {path<.+>}**

    The default [^/]+ stops at a slash; requiring .+ lets the token match across path segments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#slash-in-parameters)

??? question "9. Which placeholder is optional (matches /blog and /blog/N) with default 1 and digits only?"
    **✅ {page<\d+>?1}**

    The inline order is {name<requirement>?default}: the requirement comes first, then ? and the default value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#optional-parameters)

??? question "10. generateUrl('blog', ['page' => 1]) where page defaults to 1 produces?"
    **✅ /blog**

    The generator omits a trailing segment whose value equals its default, yielding the canonical shortest URL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "11. In the path /{a}/{b}, which placeholder can be made optional?"
    **✅ b only, because it is the trailing placeholder**

    Only trailing placeholders can be optional; a gap in the middle cannot be located by the matcher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#optional-parameters)

??? question "12. What default value does the placeholder {slug?} declare?"
    **✅ null**

    A bare ? with no value after it sets the default to null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#optional-parameters)

??? question "13. What is the default reference type of UrlGeneratorInterface::generate() / generateUrl()?"
    **✅ ABSOLUTE_PATH (a root-relative path like /blog/42)**

    By default the generator returns a root-relative path; ABSOLUTE_URL adds the scheme and host.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "14. generateUrl('blog_show', ['id' => 42, 'utm' => 'x']) produces what?"
    **✅ /blog/42?utm=x**

    Parameters that are not route placeholders are appended as query string arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "15. Which type defines the constants ABSOLUTE_URL, ABSOLUTE_PATH, NETWORK_PATH, RELATIVE_PATH?"
    **✅ Symfony\Component\Routing\Generator\UrlGeneratorInterface**

    The reference-type constants are declared on UrlGeneratorInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "16. Why might a console command generate URLs like http://localhost/... ?"
    **✅ There is no request context, and framework.router.default_uri is not set**

    Outside a web request the generator falls back to the RequestContext defaults; configure router.default_uri for correct absolute URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls-in-commands)

??? question "17. Which Twig function outputs an absolute URL?"
    **✅ url()**

    url() maps to ABSOLUTE_URL; path() maps to the default ABSOLUTE_PATH.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls-in-templates)

??? question "18. A route path is /blog/. A GET request to /blog results in?"
    **✅ A 301 redirect to /blog/**

    RedirectableUrlMatcher issues a 301 to the canonical trailing-slash URL for safe (GET/HEAD) methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-urls-with-trailing-slashes)

??? question "19. A POST to /blog when the route is defined as /blog/ yields?"
    **✅ 405 Method Not Allowed**

    Redirecting a POST would alter the method, so the matcher returns 405 rather than a trailing-slash redirect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#redirecting-urls-with-trailing-slashes)

??? question "20. Which RedirectController action redirects to another route by name?"
    **✅ redirectAction (uses a 'route' default)**

    redirectAction targets a route name and forwards parameters; urlRedirectAction targets a literal path or URL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "21. In a RedirectController route config, permanent: true means which status code?"
    **✅ 301 Moved Permanently**

    permanent toggles a 301; the default is a 302.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "22. Which request attribute holds the name of the matched route?"
    **✅ _route**

    The matcher injects _route (the matched name) and _route_params (the placeholder values) into the request attributes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#special-parameters)

??? question "23. What does the special _format parameter do when matched?"
    **✅ Sets the request format, influencing the response Content-Type**

    RouterListener applies _format via Request::setRequestFormat(), driving content negotiation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#special-parameters)

??? question "24. What does #[Route(stateless: true)] primarily do?"
    **✅ Asserts the route must not use the session (warns in debug if it does)**

    It flags accidental session usage during development; important for cacheable and API endpoints.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#stateless-routes)

??? question "25. Where does the special _fragment parameter take effect?"
    **✅ During URL generation, appended as #fragment**

    _fragment is honoured by the generator and ignored by the matcher.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#special-parameters)

??? question "26. What is the default regex applied to a host placeholder like {sub}?"
    **✅ [^.]+**

    Host labels are separated by dots, so a host token matches any non-dot characters by default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#sub-domain-routing)

??? question "27. During matching, when is the host constraint checked?"
    **✅ Before the path regex**

    matchCollection() tests the compiled host regex first, then the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#sub-domain-routing)

??? question "28. Generating a URL for a route bound to a different host produces?"
    **✅ An absolute (or network) URL**

    A path-only URL cannot switch host, so the generator upgrades the reference type automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "29. A route's condition expression evaluates to false. What is the result?"
    **✅ 404 — the route is simply not matched**

    A false condition means the route does not match; matching continues and may end in a 404. It is not authorization.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-expressions)

??? question "30. Which variables/functions are available inside a routing condition expression?"
    **✅ context, request, env(), service()**

    The routing expression provider exposes the RequestContext (context), the Request (request), and the env()/service() functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-expressions)

??? question "31. Do conditions affect URL generation with generateUrl()?"
    **✅ No — conditions are matching-only**

    There is no request to evaluate during generation, so conditions never influence generated URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-expressions)

??? question "32. To reference service('x') in a routing condition, service x must…"
    **✅ Be tagged routing.condition_service (e.g. via #[AsRoutingConditionService])**

    Only services tagged routing.condition_service are exposed to the routing expression language.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-expressions)

??? question "33. A route allows only GET. A POST to that same path returns?"
    **✅ 405 Method Not Allowed (with an Allow header)**

    When the path matches but the method is not allowed, the matcher throws MethodNotAllowedException, producing a 405 with an Allow header.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-http-methods)

??? question "34. A route declared with methods: ['GET'] also matches which verb automatically?"
    **✅ HEAD**

    HttpKernel handles HEAD as a bodyless GET, so GET routes also match HEAD.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-http-methods)

??? question "35. An http request hits a route restricted with schemes: ['https']. What happens?"
    **✅ It is redirected to the https URL**

    The redirectable matcher redirects a scheme mismatch to the correct scheme rather than rejecting it.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#matching-the-http-scheme)

??? question "36. For a form's _method field to influence which route matches, you must…"
    **✅ Call Request::enableHttpMethodParameterOverride()**

    Method override is opt-in; once enabled, getMethod() returns the overridden verb that the matcher uses.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "37. Does Symfony guess the user's locale from the Accept-Language header by default?"
    **✅ No — you must enable set_locale_from_accept_language or do it manually**

    Locale guessing precedence is matched _locale, then the sticky session locale, then default_locale; Accept-Language is opt-in.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#localized-routes-i18n)

??? question "38. A #[Route(path: ['en' => '/about', 'fr' => '/a-propos'])] produces what?"
    **✅ One route per locale, each carrying its _locale default**

    A localized path array expands at load time into one Route per locale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#localized-routes-i18n)

??? question "39. Matching a route that sets the _locale parameter causes what?"
    **✅ Request::setLocale() is called via the LocaleListener**

    _locale is a special parameter applied by the LocaleListener on kernel.request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#special-parameters)

??? question "40. How do you generate the French variant of a localized route named app_about?"
    **✅ generateUrl('app_about', ['_locale' => 'fr'])**

    Pass the _locale special parameter to select a localized variant; omit it to reuse the current request locale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#localized-routes-i18n)

??? question "41. Which console command simulates matching a specific URL and explains rejections?"
    **✅ router:match**

    router:match runs a TraceableUrlMatcher against the given path and reports which routes matched or why they failed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#debugging-routes)

??? question "42. After changing route definitions in the prod environment you must…"
    **✅ Rebuild the cache (cache:clear / cache:warmup)**

    The compiled router (url_matching_routes.php / url_generating_routes.php) is built at cache warmup and is not auto-refreshed in prod.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#debugging-routes)

??? question "43. Which files hold the compiled router in the cache directory?"
    **✅ url_matching_routes.php and url_generating_routes.php**

    The CompiledUrlMatcherDumper and CompiledUrlGeneratorDumper write these two files that the Router loads at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

---

<small>Back to [Flashcards](index.md) · [Routing](../../routing/index.md)</small>
