# Flashcards — Routing

93 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

## 🧠 Pour les nuls

**C'est quoi ?** Un jeu de **87 flashcards** (question au recto, réponse au verso) sur Routing. On lit la question, on répond mentalement, puis on tape pour révéler la réponse.

**Pourquoi ça existe ?** Se tester activement (essayer de répondre avant de voir la réponse) ancre l'information bien mieux que relire passivement un chapitre. Répété à intervalles espacés, c'est la technique de mémorisation la plus efficace connue.

**🏠 Analogie de la vraie vie :** Ce sont les **cartes-vocabulaire** utilisées pour apprendre une langue étrangère : un mot d'un côté, sa traduction de l'autre — on ne progresse qu'en essayant de deviner avant de retourner la carte.

**Symfony dans la vraie vie :** Recto de la carte → une question précise sur Routing / Verso → la réponse avec sa justification et un lien vers la doc officielle / Cartes marquées "ratées" → à revoir en priorité au prochain passage.

**⚠️ Erreur fréquente :** Taper pour révéler la réponse trop vite, sans avoir vraiment tenté de répondre — cela transforme l'exercice en simple lecture, avec un gain de mémorisation presque nul.

**🧠 Comment le mémoriser :** *« Je réponds avant de retourner la carte »* — et je note les cartes ratées pour les revoir plus souvent que les autres (répétition espacée).

??? question "1. What is the fully-qualified class of the routing attribute in Symfony 8?"
    **✅ Symfony\Component\Routing\Attribute\Route**

    The routing attribute lives in the Attribute namespace since 6.4; the old Annotation\Route alias is removed in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "2. Two routes can match the same request path. Which one wins?"
    **✅ The first one declared in the RouteCollection**

    The matcher iterates the collection in declaration order and returns the first route whose host and path match. It is first-match-wins, not most-specific-wins — so more specific routes must be declared before catch-all ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "3. A class-level #[Route('/blog', name: 'app_blog_')] contributes what to its method routes?"
    **✅ A path prefix and a name prefix**

    Class-level route data merges as prefixes: the path is prepended and the name becomes a prefix for each action's route. A class-level name is never a complete route name on its own.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#creating-routes-as-attributes)

??? question "4. Which YAML import type loads #[Route] attributes from a directory in Symfony 8?"
    **✅ type: attribute**

    Attribute route loading uses `type: attribute`; the `annotation` type is gone in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "5. With #[Route('/blog', name: 'app_blog_')] on the class and #[Route('/list', name: 'index')] on a method, what name and path result?"
    **✅ Name app_blog_index, path /blog/list**

    The class path /blog is prepended to the method path /list (giving /blog/list) and the class name prefix app_blog_ is prepended to the method name index (giving app_blog_index). Both parts concatenate, not replace.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#creating-routes-as-attributes)

??? question "6. Which loader reads #[Route] attributes into the RouteCollection in a Symfony 8 app?"
    **✅ AttributeRouteControllerLoader (built on AttributeClassLoader)**

    Attribute routes are read by AttributeClassLoader, wrapped by the framework's AttributeRouteControllerLoader. YamlFileLoader/XmlFileLoader handle those formats, and AnnotationClassLoader no longer exists in Symfony 8. All loaders implement LoaderInterface and are orchestrated by a DelegatingLoader.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "7. You omit the name: option on a #[Route]. What happens?"
    **✅ Symfony auto-generates a name from the class and method (e.g. app_blog_index)**

    A missing name is generated from the class + method. This works but is brittle — renaming the method breaks every generateUrl() call — so an explicit, stable name is recommended.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "8. A YAML import declares `resource: routes/api.yaml`, `prefix: /api`, `name_prefix: api_`. What is the effect on the imported routes?"
    **✅ Every imported path is prepended with /api and every name with api_**

    Import options cascade to every route in the resource: prefix is prepended to each path and name_prefix to each name. This is how you namespace a whole imported set without editing each definition.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "9. A route path is /blog/{page<\d+>} and the request is /blog/latest. What happens?"
    **✅ The route does not match; matching continues (likely a 404)**

    Requirements are compiled into the route regex, so a non-matching value means the route is skipped — it is a matching concern, not validation. There is no 400 from routing itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

??? question "10. Which two declarations are exactly equivalent?"
    **✅ {id<\d+>} and requirements: {id: '\d+'}**

    The inline <...> syntax is sugar for a matching entry in the requirements array. defaults is unrelated (it sets values, not patterns).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

??? question "11. What is the default regex applied to a placeholder that has no requirement?"
    **✅ [^/]+**

    Placeholders match any characters except the / separator by default; use .+ to span multiple segments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "12. How do you allow a single parameter to capture several path segments (slashes)?"
    **✅ Override its requirement to .+, e.g. {path<.+>}**

    The default [^/]+ stops at a slash; requiring .+ lets the token match across path segments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#slash-in-parameters)

??? question "13. You write requirements: {id: '^\d+$'} to constrain an id. What is wrong?"
    **✅ Requirement regexes are implicitly anchored; adding ^ and $ is wrong**

    RouteCompiler substitutes the placeholder with a named capture group over the whole token, so the requirement is already anchored. Adding ^/$ injects them inside the group and breaks matching. Likewise, avoid capturing groups — use (?:...) if grouping is needed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

??? question "14. Two routes share the path shape /blog/{x}: blog_show has {slug} (default [^/]+) declared first, blog_paged has {page<\\d+>} declared second. Which route matches /blog/42?"
    **✅ blog_show — the first route matches /42 as a slug, shadowing the numeric route**

    Matching is first-match-wins in declaration order. Because blog_show's {slug} defaults to [^/]+, it also matches 42, so it captures /blog/42 before the numeric route is ever tried. Declare the numeric route first to disambiguate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

??? question "15. In YAML, which block restricts a {slug} placeholder to lowercase letters, digits and hyphens?"
    **✅ requirements:\n    slug: '[a-z0-9\-]+'**

    The YAML key is `requirements`, a map of placeholder name to regex. `defaults` sets values, and there are no `constraints`/`validation` keys in a route definition — validation is a separate component.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

??? question "16. How does RouteCompiler represent /blog/{page<\d+>} in the CompiledRoute regex?"
    **✅ As a named capture group, e.g. #^/blog/(?P<page>\d+)$#sD**

    RouteCompiler::compile() extracts each {name} token and substitutes it with a named capture group using its requirement (or [^/]+ by default), producing a single anchored regex. Named groups are how the matcher maps captured values back to parameter names.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/RouteCompiler.php)

??? question "17. Which placeholder is optional (matches /blog and /blog/N) with default 1 and digits only?"
    **✅ {page<\d+>?1}**

    The inline order is {name<requirement>?default}: the requirement comes first, then ? and the default value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

??? question "18. generateUrl('blog', ['page' => 1]) where page defaults to 1 produces?"
    **✅ /blog**

    The generator omits a trailing segment whose value equals its default, yielding the canonical shortest URL. This keeps generated URLs stable and avoids duplicate-content variants.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "19. In the path /{a}/{b}, which placeholder can be made optional?"
    **✅ b only, because it is the trailing placeholder**

    Only trailing placeholders can be optional; a gap in the middle cannot be located by the matcher. RouteCompiler emits nested optional groups from the tail, so an optional a with a required b is impossible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

??? question "20. What default value does the placeholder {slug?} declare?"
    **✅ null**

    A bare ? with no value after it sets the default to null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

??? question "21. Why is the inline placeholder {page?1<\d+>} wrong?"
    **✅ The requirement must precede the ?: it should be {page<\d+>?1}**

    The inline grammar is strictly {name<requirement>?default}. Putting ?1 before the <\\d+> requirement is a syntax error / misparse. Requirement and default can absolutely be combined — just in the right order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

??? question "22. For path /archive/{year<\\d+>}/{month}, which YAML makes month optional and null when absent?"
    **✅ defaults:\n    month: null**

    A trailing placeholder becomes optional by having a default; setting it to null in the defaults array is the array-form equivalent of the inline {month?}. '' is an empty string, not null, and there is no `optional` key.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

??? question "23. For /blog/{page<\d+>?1}, what does generateUrl('blog_list', ['page' => 3]) produce?"
    **✅ /blog/3**

    The segment is only omitted when the value equals the default (1). Since 3 differs, the generator emits the full /blog/3.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

??? question "24. What is the default reference type of UrlGeneratorInterface::generate() / generateUrl()?"
    **✅ ABSOLUTE_PATH (a root-relative path like /blog/42)**

    By default the generator returns a root-relative path; ABSOLUTE_URL adds the scheme and host.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "25. generateUrl('blog_show', ['id' => 42, 'utm' => 'x']) produces what?"
    **✅ /blog/42?utm=x**

    Parameters that are not route placeholders are appended as query string arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "26. Which type defines the constants ABSOLUTE_URL, ABSOLUTE_PATH, NETWORK_PATH, RELATIVE_PATH?"
    **✅ Symfony\Component\Routing\Generator\UrlGeneratorInterface**

    The reference-type constants are declared on UrlGeneratorInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "27. Why might a console command generate URLs like http://localhost/... ?"
    **✅ There is no request context, and framework.router.default_uri is not set**

    Outside a web request the generator falls back to the RequestContext defaults; configure router.default_uri for correct absolute URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls-in-commands)

??? question "28. Which Twig function outputs an absolute URL?"
    **✅ url()**

    url() maps to ABSOLUTE_URL; path() maps to the default ABSOLUTE_PATH.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls-in-templates)

??? question "29. What does UrlGeneratorInterface::NETWORK_PATH produce for blog_show id 42?"
    **✅ //example.com/blog/42 (protocol-relative)**

    NETWORK_PATH emits a scheme-relative URL beginning with //, letting the browser reuse the current scheme. ABSOLUTE_URL includes the scheme, ABSOLUTE_PATH is root-relative, and RELATIVE_PATH gives something like ../42.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "30. Generating a URL for a route name that does not exist throws which exception?"
    **✅ RouteNotFoundException**

    generate() first looks up the route by name and throws RouteNotFoundException when it is missing. InvalidParameterException is thrown later, when a passed value fails a requirement. ResourceNotFoundException/MethodNotAllowedException belong to matching, not generation.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Generator/UrlGenerator.php)

??? question "31. A route declares schemes: ['https'], the current context is http, and you call generateUrl() with the default ABSOLUTE_PATH. What is returned?"
    **✅ An absolute https URL — generation is upgraded because a path cannot switch scheme**

    When the target route's scheme differs from the context, the generator must emit an absolute URL with the correct (https) scheme, overriding the requested ABSOLUTE_PATH — a path-only URL could not change scheme.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "32. What is framework.router.default_uri used for?"
    **✅ Supplying scheme/host/base-path to the RequestContext when there is no request (CLI, Messenger)**

    RequestContext is normally populated from the incoming Request. In CLI or a queue worker there is no request, so the generator uses default_uri to build correct absolute URLs instead of http://localhost.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls-in-commands)

??? question "33. A route path is /blog/. A GET request to /blog results in?"
    **✅ A 301 redirect to /blog/**

    RedirectableUrlMatcher issues a 301 to the canonical trailing-slash URL for safe (GET/HEAD) methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-urls-with-trailing-slashes)

??? question "34. A POST to /blog when the route is defined as /blog/ yields?"
    **✅ 405 Method Not Allowed**

    Redirecting a POST would alter the method, so the matcher returns 405 rather than a trailing-slash redirect. The auto-redirect is GET/HEAD only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-urls-with-trailing-slashes)

??? question "35. Which RedirectController action redirects to another route by name?"
    **✅ redirectAction (uses a 'route' default)**

    redirectAction targets a route name and forwards parameters; urlRedirectAction targets a literal path or URL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "36. In a RedirectController route config, permanent: true means which status code?"
    **✅ 301 Moved Permanently**

    permanent toggles a 301; the default is a 302.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "37. You want /docs to redirect (302) to the literal path /docs/intro via RedirectController. Which controller + default do you use?"
    **✅ urlRedirectAction with defaults: {path: /docs/intro, permanent: false}**

    urlRedirectAction targets a literal path/URL via the `path` default; redirectAction targets a route name via the `route` default. Mixing the action with the wrong default key does not work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "38. What status code does $this->redirectToRoute('blog_show', ['id' => $id]) return by default?"
    **✅ 302 Found**

    redirectToRoute() builds a RedirectResponse with a 302 by default; pass a third status argument (e.g. 301) to change it. Use controller-level redirects when the target depends on logic/data.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

??? question "39. For a RedirectController route, where is the 30x response actually produced?"
    **✅ In the controller — it returns a RedirectResponse like any normal action**

    A redirect route is an ordinary route whose _controller is RedirectController; the kernel runs it and it returns a RedirectResponse. The matcher only produces redirects itself in the special trailing-slash / scheme cases.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

??? question "40. Why is permanent: true (301) a poor choice for a temporary or A/B redirect?"
    **✅ Browsers cache 301s aggressively, so you cannot easily change the target later**

    A 301 tells clients the move is permanent, so browsers cache it hard and may not re-request the old URL. Use 302 (the default) while a target is still in flux.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "41. Which request attribute holds the name of the matched route?"
    **✅ _route**

    The matcher injects _route (the matched name) and _route_params (the placeholder values) into the request attributes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "42. What does the special _format parameter do when matched?"
    **✅ Sets the request format, influencing the response Content-Type**

    RouterListener applies _format via Request::setRequestFormat(), driving content negotiation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "43. What does #[Route(stateless: true)] primarily do?"
    **✅ Asserts the route must not use the session (warns in debug if it does)**

    It flags accidental session usage during development, raising UnexpectedSessionUsageException in debug; important for cacheable and API endpoints. It is an assertion, not a hard prod block.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#stateless-routes)

??? question "44. Where does the special _fragment parameter take effect?"
    **✅ During URL generation, appended as #fragment**

    _fragment is honoured by the generator and ignored by the matcher (a URL fragment is never sent to the server).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "45. Which component copies the matcher's output parameters into $request->attributes?"
    **✅ RouterListener, on the kernel.request event**

    UrlMatcher::match() returns an array (route defaults + captured placeholders + _route/_route_params); RouterListener, a kernel.request subscriber, copies each entry into the request attribute bag. ControllerResolver and ArgumentResolver then consume _controller and the args later.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/RouterListener.php)

??? question "46. How do you read the matched route name inside a controller or listener?"
    **✅ $request->attributes->get('_route')**

    _route (and _route_params) are read-only outputs stored in the request attribute bag by RouterListener. There is no Request::getRoute() helper, and it is not a query parameter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "47. For path /api/items.{_format} serving only JSON or XML defaulting to JSON, which config is correct?"
    **✅ defaults: {_format: json} + requirements: {_format: 'json|xml'}**

    _format is a normal special parameter: a default gives it a value when the extension is absent, and a requirement whitelists the allowed formats. Without the requirement, items.exe would match. Formats are never HTTP methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "48. Should you set _route or _route_params yourself in a route's defaults?"
    **✅ No — they are read-only outputs injected by the matcher; you only read them**

    _route and _route_params are outputs the matcher writes; setting them in defaults is meaningless and would be overwritten. They exist for logging, subscribers and debugging.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "49. What is the default regex applied to a host placeholder like {sub}?"
    **✅ [^.]+**

    Host labels are separated by dots, so a host token matches any non-dot characters by default (contrast with the path default [^/]+).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

??? question "50. During matching, when is the host constraint checked?"
    **✅ Before the path regex**

    matchCollection() tests the compiled host regex against RequestContext::getHost() first; only if it matches does it test the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

??? question "51. Generating a URL for a route bound to a different host produces?"
    **✅ An absolute (or network) URL**

    A path-only URL cannot switch host, so the generator upgrades the reference type automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "52. Which config captures a subdomain {tenant} (lowercase alphanumerics/hyphen) on example.com, defaulting to www?"
    **✅ host: '{tenant}.example.com' + requirements: {tenant: '[a-z0-9\-]+'} + defaults: {tenant: www}**

    Host placeholders obey the same requirements/defaults rules as path ones; you set the constraint and a base default on the route's `host`. There is no `subdomain`/`domain` key, and the host belongs in `host`, not `path`.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

??? question "53. How is the host constraint stored on a CompiledRoute?"
    **✅ As a second, separate regex (getHostRegex) and its own token list**

    RouteCompiler compiles `host` into its own regex and token list on the CompiledRoute, kept separate from the path regex, so matchCollection() can test host and path independently at negligible cost.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/RouteCompiler.php)

??? question "54. Why should host constraints be written in lowercase?"
    **✅ The context host is normalized to lowercase, so an uppercase regex will not match**

    RequestContext lowercases the incoming host. A case-sensitive constraint like Admin.Example.com would then fail against admin.example.com. Write host patterns in lowercase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

??? question "55. For host '{tenant}.example.com', what does generateUrl('tenant_home', ['tenant' => 'acme'], UrlGeneratorInterface::ABSOLUTE_URL) produce (current host example.com)?"
    **✅ https://acme.example.com/**

    The tenant placeholder fills the host label, and because the requested host differs from the current one an absolute URL on acme.example.com is produced. tenant is a host placeholder, so it is not appended as a query arg.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

??? question "56. How do you apply one host to a whole imported controller directory?"
    **✅ Set host: on the YAML resource import (alongside prefix/name_prefix)**

    Import-level options — host, prefix, name_prefix — cascade to every route in the imported resource, so you avoid repeating host: on each action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

??? question "57. A route's condition expression evaluates to false. What is the result?"
    **✅ 404 — the route is simply not matched**

    A false condition means the route does not match; matching continues and may end in a 404. It is not authorization, so it never produces a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "58. Which variables/functions are available inside a routing condition expression?"
    **✅ context, request, env(), service()**

    The routing expression provider exposes the RequestContext (context), the Request (request), and the env()/service() functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "59. Do conditions affect URL generation with generateUrl()?"
    **✅ No — conditions are matching-only**

    There is no request to evaluate during generation, so conditions never influence generated URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "60. To reference service('x') in a routing condition, service x must…"
    **✅ Be tagged routing.condition_service (e.g. via #[AsRoutingConditionService])**

    Only services tagged routing.condition_service are exposed to the routing expression language. Visibility/base class are irrelevant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "61. Which condition matches only when the request query string contains a 'preview' key?"
    **✅ condition: "request.query.has('preview')"**

    Inside a condition, `request` is the HttpFoundation Request, so request.query.has('preview') is the idiomatic check. `query` alone is not a variable, and there is no bare has() function.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "62. How are route conditions executed at request time?"
    **✅ As pre-compiled PHP closures baked into the dumped matcher (not runtime eval)**

    The framework compiles all conditions ahead of time through ExpressionLanguage and the routing ExpressionLanguageProvider, so the dumped matcher contains compiled closures. UrlMatcher::handleRouteRequirements() runs them after host/path match — no per-request eval, and they cannot be reduced to a constant because they depend on the live request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Matcher/UrlMatcher.php)

??? question "63. Why is a routing condition a poor substitute for a security voter/authorization check?"
    **✅ A failed condition is a 404 (route not matched), not a 403, and cannot show a login page**

    Conditions are a matching filter: failing one just hides the route (404), so there is no 403 and no way to trigger authentication. Use Security voters for authorization.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "64. You tag a service #[AsRoutingConditionService(alias: 'feature_checker')]. How do you call its isEnabled() method in a condition?"
    **✅ condition: "service('feature_checker').isEnabled(request)"**

    The alias becomes the argument to the service() function; you then call methods on the returned object and can pass request. There is no bare identifier, @ syntax or container variable in routing expressions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

??? question "65. A route allows only GET. A POST to that same path returns?"
    **✅ 405 Method Not Allowed (with an Allow header)**

    When the path matches but the method is not allowed, the matcher throws MethodNotAllowedException, producing a 405 with an Allow header. It is not a 404 — the path did match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

??? question "66. A route declared with methods: ['GET'] also matches which verb automatically?"
    **✅ HEAD**

    HttpKernel handles HEAD as a bodyless GET, so GET routes also match HEAD. Declaring HEAD explicitly is redundant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

??? question "67. An http request hits a route restricted with schemes: ['https']. What happens?"
    **✅ It is redirected to the https URL**

    The RedirectableUrlMatcher redirects a scheme mismatch to the correct scheme rather than rejecting it — contrast with a wrong method, which is a 405.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-the-http-scheme)

??? question "68. For a form's _method field to influence which route matches, you must…"
    **✅ Call Request::enableHttpMethodParameterOverride()**

    Method override is opt-in; once enabled, getMethod() returns the overridden verb that the matcher uses. It is not on by default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "69. A DELETE-only route /tags/{id} gets a GET. What does the 405 response's Allow header contain?"
    **✅ DELETE — the verbs permitted by the matched path**

    On a 405 the matcher collects the allowed methods of the matching path and returns them in the Allow header (DELETE here), telling the client which verbs are valid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

??? question "70. How do you make one route accept both PUT and PATCH?"
    **✅ methods: ['PUT', 'PATCH']**

    methods accepts a list of verbs; any listed verb matches. A single route can serve several verbs — no pipe syntax or extra flags needed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

??? question "71. Are HTTP method names in the methods option case-sensitive?"
    **✅ No — matching is case-insensitive, though uppercase is conventional**

    Method matching is case-insensitive, but you should write verbs in uppercase by convention for readability and debug:router clarity.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

??? question "72. Does Symfony guess the user's locale from the Accept-Language header by default?"
    **✅ No — you must enable set_locale_from_accept_language or do it manually**

    Locale precedence is a matched _locale, then the sticky session locale, then default_locale; Accept-Language is opt-in. To honour it, read Request::getPreferredLanguage($available) or enable the option.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "73. A #[Route(path: ['en' => '/about', 'fr' => '/a-propos'])] produces what?"
    **✅ One route per locale, each carrying its _locale default**

    A localized path array expands at load time into one Route per locale, each with defaults['_locale'] set and a _locale requirement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "74. Matching a route that sets the _locale parameter causes what?"
    **✅ Request::setLocale() is called via the LocaleListener**

    _locale is a special parameter applied by the LocaleListener on kernel.request, which calls Request::setLocale().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "75. How do you generate the French variant of a localized route named app_about?"
    **✅ generateUrl('app_about', ['_locale' => 'fr'])**

    Pass the _locale special parameter to select a localized variant; omit it to reuse the current request locale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "76. Which config exposes /{_locale}/blog restricted to en, fr or de and defaulting to en?"
    **✅ path '/{_locale}/blog' + requirements: {_locale: 'en|fr|de'} + defaults: {_locale: 'en'}**

    The _locale placeholder is constrained by a requirement whitelist and given a default. Omitting the requirement lets any /xx/blog match; there is no top-level locale: list on a route. (Inline requirement is valid too, but a default is still needed for it to be optional at the root.)

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "77. What goes wrong if /{_locale}/blog has no _locale requirement?"
    **✅ Any segment matches _locale, so /xx/blog or /foo/blog wrongly match**

    Without a requirement, _locale keeps the default [^/]+ and matches any label, so invalid locales like /xx/blog match. Always whitelist _locale with a requirement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "78. Which two listeners cooperate to apply and propagate the request locale?"
    **✅ LocaleListener (sets Request locale from _locale) and LocaleAwareListener (propagates it to locale-aware services)**

    LocaleListener reads _locale on kernel.request and calls setLocale(); LocaleAwareListener then propagates the locale to locale-aware services such as the translator. RouterListener only copies matcher output into attributes.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleListener.php)

??? question "79. For route app_help at /{_locale}/help, what does generateUrl('app_help', ['_locale' => 'es']) produce?"
    **✅ /es/help**

    _locale is a real placeholder in the path, so it fills the {_locale} segment giving /es/help — not a query string, and not the default en.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "80. Which console command simulates matching a specific URL and explains rejections?"
    **✅ router:match**

    router:match runs a TraceableUrlMatcher against the given path and reports which routes matched or why they failed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "81. After changing route definitions in the prod environment you must…"
    **✅ Rebuild the cache (cache:clear / cache:warmup)**

    The compiled router (url_matching_routes.php / url_generating_routes.php) is built at cache warmup and is not auto-refreshed in prod.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "82. Which files hold the compiled router in the cache directory?"
    **✅ url_matching_routes.php and url_generating_routes.php**

    The CompiledUrlMatcherDumper and CompiledUrlGeneratorDumper write these two files that the Router loads at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "83. router:match /blog/hello reports no match, but the page works for real GET requests. What is the likely cause?"
    **✅ You omitted --method=GET, so the default context did not reproduce the real request**

    router:match builds a RequestContext from the options you pass; without --method/--host/--scheme it may not reproduce the real request and can report a no-match (or a method rejection) that does not happen in production. Pass the exact conditions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "84. In debug:router output, a route shows Scheme=ANY and Host=ANY. What does that mean?"
    **✅ The route has no scheme/host constraint, so it matches any scheme and host**

    ANY is the compiled view's way of saying no constraint was set for that column; such a route matches regardless of scheme/host. It is not a literal value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "85. Why do new routes appear immediately in dev but not in prod?"
    **✅ In dev the router tracks route files as cache resources and rebuilds when they change; prod does not**

    In dev, route files are registered as cache resources so Symfony detects changes and rebuilds the compiled matcher/generator automatically. In prod the cache is warmed once (cache:clear/warmup) and not auto-refreshed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "86. Which command rebuilds the compiled router after editing routes in prod?"
    **✅ php bin/console cache:clear --env=prod**

    cache:clear (or cache:warmup) in the prod env runs the RouterCacheWarmer and regenerates url_matching_routes.php / url_generating_routes.php. The other commands do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "87. Where in the web profiler can you see the matched _route for the current request?"
    **✅ The Routing panel (linked from the web debug toolbar)**

    The profiler's Routing panel shows the matched _route and its parameters for the current request, so you do not need dump() calls to find them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

??? question "88. Which of the following statements are true about route parameter requirements? (select all that apply)"
    **✅ The inline syntax {id<\d+>} is exactly equivalent to requirements: {id: '\d+'} ; A URL that violates a requirement simply fails to match that route (typically ending in a 404), never a 400 from routing ; A placeholder without a requirement matches [^/]+ by default, so it cannot span path segments**

    Inline <...> is syntactic sugar for a requirements entry, and because the requirement is compiled into the route regex a violating value just does not match — matching moves on and usually ends in a 404. The default token pattern is [^/]+ (use .+ to cross slashes). Requirements are implicitly anchored, so adding ^/$ is wrong, and routing never produces a 400 for a bad parameter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

??? question "89. Which of the following statements are true about HTTP method matching in Symfony routing? (select all that apply)"
    **✅ A request whose path matches but whose verb is not allowed gets a 405 Method Not Allowed with an Allow header ; A route declaring methods: ['GET'] also matches HEAD requests automatically**

    When host and path match but the verb does not, the matcher throws MethodNotAllowedException, surfaced as a 405 listing the allowed verbs, and GET routes match HEAD because HttpKernel serves HEAD as a bodyless GET. A scheme mismatch is handled differently — the redirectable matcher redirects to the correct scheme — and the _method override only works after calling Request::enableHttpMethodParameterOverride().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

??? question "90. Which of the following statements are true about URL generation? (select all that apply)"
    **✅ The default reference type is ABSOLUTE_PATH, producing a root-relative path like /blog/42 ; Parameters that do not correspond to a route placeholder are appended to the generated URL as a query string ; The reference-type constants (ABSOLUTE_URL, NETWORK_PATH, ...) are defined on UrlGeneratorInterface**

    generateUrl() defaults to ABSOLUTE_PATH, left-over (non-placeholder) parameters become the ?key=value query string, and the constants live on UrlGeneratorInterface. In Twig, path() maps to ABSOLUTE_PATH while url() maps to ABSOLUTE_URL, and in CLI there is no request, so absolute URLs fall back to http://localhost unless framework.router.default_uri is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

??? question "91. Which of the following statements are true about the special underscore routing attributes? (select all that apply)"
    **✅ _route and _route_params are read-only outputs injected by the matcher into the request attributes ; _format sets the request format via Request::setRequestFormat(), influencing the response Content-Type ; _fragment only takes effect during URL generation (appended as #fragment); it plays no role in matching**

    The matcher injects _route/_route_params and RouterListener copies them into request attributes for you to read, _format drives content negotiation and the default Content-Type, and _fragment is honoured only by the generator. You never set _route yourself, and stateless: true is an assertion that raises an UnexpectedSessionUsageException warning in debug — not a hard production block.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

??? question "92. Which of the following statements are true about localized routes and locale guessing? (select all that apply)"
    **✅ A #[Route] whose path is a locale => path map expands into one route per locale, each carrying the matching _locale default ; Symfony does not guess the locale from the Accept-Language header by default; that behaviour is opt-in**

    Localized path arrays are expanded at load time into per-locale routes with a _locale default, and Accept-Language parsing requires opting in via set_locale_from_accept_language (or reading getPreferredLanguage() yourself). The precedence is matched _locale first, then the sticky session locale, then default_locale, and generation reuses the current request's locale unless you pass _locale explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

??? question "93. Which of the following statements are true about host (domain) matching? (select all that apply)"
    **✅ A host placeholder like {tenant} matches [^.]+ by default — a single label that cannot contain dots ; The host regex is tested before the path regex when matching a route ; Generating a URL for a route on a different host produces an absolute (or network) URL automatically**

    Host tokens use the dot as separator, so they default to [^.]+ instead of [^/]+, and matchCollection() checks the compiled host regex before even trying the path. Because a path-only URL cannot change host, the generator upgrades cross-host links to absolute/network URLs. Host placeholders obey the same requirements/defaults rules as path placeholders — that is how a missing subdomain can default to www.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

---

<small>Back to [Flashcards](index.md) · [Routing](../../routing/index.md)</small>
