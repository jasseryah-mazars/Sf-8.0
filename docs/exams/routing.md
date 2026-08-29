# Chapter Exam — Routing

!!! abstract "How to use"
    93 questions spanning every subchapter of **Routing**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Routing](../routing/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Cette page est une **banque de 87 questions type QCM** sur Routing, avec correction dépliable sous chaque question. Ce n'est pas un cours : c'est un entraînement, à faire après avoir lu le chapitre.

**Pourquoi ça existe ?** Lire un chapitre donne l'impression d'avoir compris, mais répondre à une question sous forme d'examen (sans relire ses notes) révèle les vraies lacunes — c'est ce que fera l'examen officiel.

**🏠 Analogie de la vraie vie :** C'est le **permis de conduire**. Le code de la route (le cours) explique les règles ; les séries de questions du permis blanc (cette page) vérifient que tu sais les appliquer sous forme de question piège, sans l'aide du livre.

**Symfony dans la vraie vie :** Cours du chapitre → code de la route appris / Question du QCM → question du permis blanc / Réponse dépliable → correction avec explication / Score obtenu → indicateur "prêt à passer l'examen ou pas".

**⚠️ Erreur fréquente :** Déplier la réponse avant d'avoir vraiment tranché son choix. Le cerveau retient beaucoup mieux une explication lue *après* s'être trompé (ou avoir hésité) que lue en passant, sans effort de rappel préalable.

**🧠 Comment le mémoriser :** *« Je réponds d'abord, je vérifie ensuite »* — jamais l'inverse. Note les questions ratées : ce sont exactement les pièges que l'examinateur pose aussi.

---

**Q1.** What is the fully-qualified class of the routing attribute in Symfony 8?  <small>_(easy · single)_</small>

- A. Symfony\Component\Routing\Attribute\Route
- B. Symfony\Component\Routing\Annotation\Route
- C. Symfony\Component\HttpKernel\Attribute\Route
- D. Symfony\Routing\Route

??? success "Answer Q1"
    **A**

    The routing attribute lives in the Attribute namespace since 6.4; the old Annotation\Route alias is removed in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q2.** Which YAML import type loads #[Route] attributes from a directory in Symfony 8?  <small>_(easy · config)_</small>

- A. type: attribute
- B. type: annotation
- C. type: php
- D. type: directory

??? success "Answer Q2"
    **A**

    Attribute route loading uses `type: attribute`; the `annotation` type is gone in Symfony 8.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q3.** What is the default regex applied to a placeholder that has no requirement?  <small>_(easy · single)_</small>

- A. [^/]+
- B. .+
- C. \w+
- D. .*

??? success "Answer Q3"
    **A**

    Placeholders match any characters except the / separator by default; use .+ to span multiple segments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q4.** In YAML, which block restricts a {slug} placeholder to lowercase letters, digits and hyphens?  <small>_(easy · config)_</small>

- A. requirements:\n    slug: '[a-z0-9\-]+'
- B. defaults:\n    slug: '[a-z0-9\-]+'
- C. constraints:\n    slug: '[a-z0-9\-]+'
- D. validation:\n    slug: '[a-z0-9\-]+'

??? success "Answer Q4"
    **A**

    The YAML key is `requirements`, a map of placeholder name to regex. `defaults` sets values, and there are no `constraints`/`validation` keys in a route definition — validation is a separate component.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

**Q5.** What default value does the placeholder {slug?} declare?  <small>_(easy · single)_</small>

- A. null
- B. An empty string ''
- C. The literal 'slug'
- D. 0

??? success "Answer Q5"
    **A**

    A bare ? with no value after it sets the default to null.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q6.** For /blog/{page<\d+>?1}, what does generateUrl('blog_list', ['page' => 3]) produce?  <small>_(easy · code)_</small>

- A. /blog/3
- B. /blog
- C. /blog?page=3
- D. /blog/1

??? success "Answer Q6"
    **A**

    The segment is only omitted when the value equals the default (1). Since 3 differs, the generator emits the full /blog/3.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q7.** What is the default reference type of UrlGeneratorInterface::generate() / generateUrl()?  <small>_(easy · single)_</small>

- A. ABSOLUTE_PATH (a root-relative path like /blog/42)
- B. ABSOLUTE_URL
- C. NETWORK_PATH
- D. RELATIVE_PATH

??? success "Answer Q7"
    **A**

    By default the generator returns a root-relative path; ABSOLUTE_URL adds the scheme and host.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q8.** generateUrl('blog_show', ['id' => 42, 'utm' => 'x']) produces what?  <small>_(easy · single)_</small>

- A. /blog/42?utm=x
- B. /blog/42/x
- C. /blog/42
- D. an InvalidParameterException

??? success "Answer Q8"
    **A**

    Parameters that are not route placeholders are appended as query string arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q9.** Which type defines the constants ABSOLUTE_URL, ABSOLUTE_PATH, NETWORK_PATH, RELATIVE_PATH?  <small>_(easy · single)_</small>

- A. Symfony\Component\Routing\Generator\UrlGeneratorInterface
- B. Symfony\Component\Routing\RequestContext
- C. Symfony\Component\Routing\Router
- D. Symfony\Component\Routing\Route

??? success "Answer Q9"
    **A**

    The reference-type constants are declared on UrlGeneratorInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q10.** Which Twig function outputs an absolute URL?  <small>_(easy · single)_</small>

- A. url()
- B. path()
- C. asset()
- D. absolute_url() only

??? success "Answer Q10"
    **A**

    url() maps to ABSOLUTE_URL; path() maps to the default ABSOLUTE_PATH.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls-in-templates)

**Q11.** What does UrlGeneratorInterface::NETWORK_PATH produce for blog_show id 42?  <small>_(easy · single)_</small>

- A. //example.com/blog/42 (protocol-relative)
- B. https://example.com/blog/42
- C. /blog/42
- D. ../42

??? success "Answer Q11"
    **A**

    NETWORK_PATH emits a scheme-relative URL beginning with //, letting the browser reuse the current scheme. ABSOLUTE_URL includes the scheme, ABSOLUTE_PATH is root-relative, and RELATIVE_PATH gives something like ../42.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q12.** Which RedirectController action redirects to another route by name?  <small>_(easy · single)_</small>

- A. redirectAction (uses a 'route' default)
- B. urlRedirectAction (uses a 'path' default)
- C. routeAction
- D. nameAction

??? success "Answer Q12"
    **A**

    redirectAction targets a route name and forwards parameters; urlRedirectAction targets a literal path or URL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q13.** In a RedirectController route config, permanent: true means which status code?  <small>_(easy · single)_</small>

- A. 301 Moved Permanently
- B. 302 Found
- C. 307 Temporary Redirect
- D. 308 Permanent Redirect

??? success "Answer Q13"
    **A**

    permanent toggles a 301; the default is a 302.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q14.** Which request attribute holds the name of the matched route?  <small>_(easy · single)_</small>

- A. _route
- B. _controller
- C. _route_name
- D. _name

??? success "Answer Q14"
    **A**

    The matcher injects _route (the matched name) and _route_params (the placeholder values) into the request attributes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q15.** What does the special _format parameter do when matched?  <small>_(easy · single)_</small>

- A. Sets the request format, influencing the response Content-Type
- B. Only appears in the URL with no effect
- C. Selects which controller runs
- D. Sets the HTTP method

??? success "Answer Q15"
    **A**

    RouterListener applies _format via Request::setRequestFormat(), driving content negotiation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q16.** What is the default regex applied to a host placeholder like {sub}?  <small>_(easy · single)_</small>

- A. [^.]+
- B. [^/]+
- C. .+
- D. \w+

??? success "Answer Q16"
    **A**

    Host labels are separated by dots, so a host token matches any non-dot characters by default (contrast with the path default [^/]+).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q17.** Which variables/functions are available inside a routing condition expression?  <small>_(easy · single)_</small>

- A. context, request, env(), service()
- B. session, token, user()
- C. kernel, container
- D. params, route()

??? success "Answer Q17"
    **A**

    The routing expression provider exposes the RequestContext (context), the Request (request), and the env()/service() functions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q18.** Do conditions affect URL generation with generateUrl()?  <small>_(easy · single)_</small>

- A. No — conditions are matching-only
- B. Yes, generation fails if the condition is false
- C. Only for absolute URLs
- D. Only in debug mode

??? success "Answer Q18"
    **A**

    There is no request to evaluate during generation, so conditions never influence generated URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q19.** A route allows only GET. A POST to that same path returns?  <small>_(easy · single)_</small>

- A. 405 Method Not Allowed (with an Allow header)
- B. 404 Not Found
- C. 200 OK
- D. 301 redirect

??? success "Answer Q19"
    **A**

    When the path matches but the method is not allowed, the matcher throws MethodNotAllowedException, producing a 405 with an Allow header. It is not a 404 — the path did match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

**Q20.** A route declared with methods: ['GET'] also matches which verb automatically?  <small>_(easy · single)_</small>

- A. HEAD
- B. POST
- C. OPTIONS
- D. PUT

??? success "Answer Q20"
    **A**

    HttpKernel handles HEAD as a bodyless GET, so GET routes also match HEAD. Declaring HEAD explicitly is redundant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

**Q21.** How do you generate the French variant of a localized route named app_about?  <small>_(easy · single)_</small>

- A. generateUrl('app_about', ['_locale' => 'fr'])
- B. generateUrl('app_about_fr')
- C. generateUrl('app_about', ['lang' => 'fr'])
- D. It is not possible

??? success "Answer Q21"
    **A**

    Pass the _locale special parameter to select a localized variant; omit it to reuse the current request locale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q22.** For route app_help at /{_locale}/help, what does generateUrl('app_help', ['_locale' => 'es']) produce?  <small>_(easy · code)_</small>

- A. /es/help
- B. /help?_locale=es
- C. /help/es
- D. /en/help

??? success "Answer Q22"
    **A**

    _locale is a real placeholder in the path, so it fills the {_locale} segment giving /es/help — not a query string, and not the default en.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q23.** Which console command simulates matching a specific URL and explains rejections?  <small>_(easy · single)_</small>

- A. router:match
- B. debug:router
- C. debug:route
- D. router:debug

??? success "Answer Q23"
    **A**

    router:match runs a TraceableUrlMatcher against the given path and reports which routes matched or why they failed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q24.** After changing route definitions in the prod environment you must…  <small>_(easy · single)_</small>

- A. Rebuild the cache (cache:clear / cache:warmup)
- B. Only restart PHP-FPM
- C. Do nothing — routes always reload
- D. Delete the vendor directory

??? success "Answer Q24"
    **A**

    The compiled router (url_matching_routes.php / url_generating_routes.php) is built at cache warmup and is not auto-refreshed in prod.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q25.** Which command rebuilds the compiled router after editing routes in prod?  <small>_(easy · config)_</small>

- A. php bin/console cache:clear --env=prod
- B. php bin/console router:reload --env=prod
- C. php bin/console debug:router --refresh
- D. php bin/console routes:compile

??? success "Answer Q25"
    **A**

    cache:clear (or cache:warmup) in the prod env runs the RouterCacheWarmer and regenerates url_matching_routes.php / url_generating_routes.php. The other commands do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q26.** Where in the web profiler can you see the matched _route for the current request?  <small>_(easy · single)_</small>

- A. The Routing panel (linked from the web debug toolbar)
- B. The Doctrine panel
- C. The Cache panel
- D. It is never shown in the profiler

??? success "Answer Q26"
    **A**

    The profiler's Routing panel shows the matched _route and its parameters for the current request, so you do not need dump() calls to find them.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q27.** Two routes can match the same request path. Which one wins?  <small>_(medium · internals)_</small>

- A. The first one declared in the RouteCollection
- B. The one with the most specific path
- C. The last one declared
- D. The one with the shortest name

??? success "Answer Q27"
    **A**

    The matcher iterates the collection in declaration order and returns the first route whose host and path match. It is first-match-wins, not most-specific-wins — so more specific routes must be declared before catch-all ones.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q28.** A class-level #[Route('/blog', name: 'app_blog_')] contributes what to its method routes?  <small>_(medium · single)_</small>

- A. A path prefix and a name prefix
- B. A full route named app_blog_
- C. A default controller for the class
- D. Nothing without a methods option

??? success "Answer Q28"
    **A**

    Class-level route data merges as prefixes: the path is prepended and the name becomes a prefix for each action's route. A class-level name is never a complete route name on its own.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#creating-routes-as-attributes)

**Q29.** With #[Route('/blog', name: 'app_blog_')] on the class and #[Route('/list', name: 'index')] on a method, what name and path result?  <small>_(medium · code)_</small>

- A. Name app_blog_index, path /blog/list
- B. Name index, path /list
- C. Name app_blog_, path /blog
- D. Name app_blog_index, path /list

??? success "Answer Q29"
    **A**

    The class path /blog is prepended to the method path /list (giving /blog/list) and the class name prefix app_blog_ is prepended to the method name index (giving app_blog_index). Both parts concatenate, not replace.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#creating-routes-as-attributes)

**Q30.** You omit the name: option on a #[Route]. What happens?  <small>_(medium · trap)_</small>

- A. Symfony auto-generates a name from the class and method (e.g. app_blog_index)
- B. The route is silently skipped
- C. A fatal error is thrown at compile time
- D. The path string is used verbatim as the name

??? success "Answer Q30"
    **A**

    A missing name is generated from the class + method. This works but is brittle — renaming the method breaks every generateUrl() call — so an explicit, stable name is recommended.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q31.** A YAML import declares `resource: routes/api.yaml`, `prefix: /api`, `name_prefix: api_`. What is the effect on the imported routes?  <small>_(medium · config)_</small>

- A. Every imported path is prepended with /api and every name with api_
- B. Only the first imported route gets the prefixes
- C. The prefixes replace the imported paths and names
- D. prefix affects the path but name_prefix is ignored for YAML

??? success "Answer Q31"
    **A**

    Import options cascade to every route in the resource: prefix is prepended to each path and name_prefix to each name. This is how you namespace a whole imported set without editing each definition.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q32.** A route path is /blog/{page<\d+>} and the request is /blog/latest. What happens?  <small>_(medium · trap)_</small>

- A. The route does not match; matching continues (likely a 404)
- B. The controller runs with page = 'latest'
- C. The router returns 400 Bad Request
- D. page is cast to 0

??? success "Answer Q32"
    **A**

    Requirements are compiled into the route regex, so a non-matching value means the route is skipped — it is a matching concern, not validation. There is no 400 from routing itself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

**Q33.** Which two declarations are exactly equivalent?  <small>_(medium · single)_</small>

- A. {id<\d+>} and requirements: {id: '\d+'}
- B. {id} and requirements: {id: '\d+'}
- C. {id<\d+>} and defaults: {id: '\d+'}
- D. {id} and {id<.+>}

??? success "Answer Q33"
    **A**

    The inline <...> syntax is sugar for a matching entry in the requirements array. defaults is unrelated (it sets values, not patterns).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

**Q34.** How do you allow a single parameter to capture several path segments (slashes)?  <small>_(medium · code)_</small>

- A. Override its requirement to .+, e.g. {path<.+>}
- B. Use {path<\w+>}
- C. Set defaults: {path: '/'}
- D. It is impossible

??? success "Answer Q34"
    **A**

    The default [^/]+ stops at a slash; requiring .+ lets the token match across path segments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#slash-in-parameters)

**Q35.** You write requirements: {id: '^\d+$'} to constrain an id. What is wrong?  <small>_(medium · trap)_</small>

- A. Requirement regexes are implicitly anchored; adding ^ and $ is wrong
- B. Nothing — anchors are required
- C. You must also add anchors to the path
- D. The regex must be double-quoted to work

??? success "Answer Q35"
    **A**

    RouteCompiler substitutes the placeholder with a named capture group over the whole token, so the requirement is already anchored. Adding ^/$ injects them inside the group and breaks matching. Likewise, avoid capturing groups — use (?:...) if grouping is needed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

**Q36.** Which placeholder is optional (matches /blog and /blog/N) with default 1 and digits only?  <small>_(medium · code)_</small>

- A. {page<\d+>?1}
- B. {page?1<\d+>}
- C. {page=1<\d+>}
- D. {page<\d+=1>}

??? success "Answer Q36"
    **A**

    The inline order is {name<requirement>?default}: the requirement comes first, then ? and the default value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q37.** generateUrl('blog', ['page' => 1]) where page defaults to 1 produces?  <small>_(medium · internals)_</small>

- A. /blog
- B. /blog/1
- C. /blog?page=1
- D. an exception

??? success "Answer Q37"
    **A**

    The generator omits a trailing segment whose value equals its default, yielding the canonical shortest URL. This keeps generated URLs stable and avoids duplicate-content variants.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q38.** Why is the inline placeholder {page?1<\d+>} wrong?  <small>_(medium · trap)_</small>

- A. The requirement must precede the ?: it should be {page<\d+>?1}
- B. Defaults cannot be numeric
- C. You cannot combine a requirement and a default
- D. The default must come before the placeholder name

??? success "Answer Q38"
    **A**

    The inline grammar is strictly {name<requirement>?default}. Putting ?1 before the <\\d+> requirement is a syntax error / misparse. Requirement and default can absolutely be combined — just in the right order.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q39.** For path /archive/{year<\\d+>}/{month}, which YAML makes month optional and null when absent?  <small>_(medium · config)_</small>

- A. defaults:\n    month: null
- B. requirements:\n    month: null
- C. optional:\n    - month
- D. defaults:\n    month: ''

??? success "Answer Q39"
    **A**

    A trailing placeholder becomes optional by having a default; setting it to null in the defaults array is the array-form equivalent of the inline {month?}. '' is an empty string, not null, and there is no `optional` key.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q40.** Why might a console command generate URLs like http://localhost/... ?  <small>_(medium · debug)_</small>

- A. There is no request context, and framework.router.default_uri is not set
- B. Because ABSOLUTE_PATH was requested
- C. Because the route lacks a methods option
- D. Because Twig is disabled

??? success "Answer Q40"
    **A**

    Outside a web request the generator falls back to the RequestContext defaults; configure router.default_uri for correct absolute URLs.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls-in-commands)

**Q41.** Generating a URL for a route name that does not exist throws which exception?  <small>_(medium · internals)_</small>

- A. RouteNotFoundException
- B. ResourceNotFoundException
- C. InvalidParameterException
- D. MethodNotAllowedException

??? success "Answer Q41"
    **A**

    generate() first looks up the route by name and throws RouteNotFoundException when it is missing. InvalidParameterException is thrown later, when a passed value fails a requirement. ResourceNotFoundException/MethodNotAllowedException belong to matching, not generation.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Generator/UrlGenerator.php)

**Q42.** What is framework.router.default_uri used for?  <small>_(medium · config)_</small>

- A. Supplying scheme/host/base-path to the RequestContext when there is no request (CLI, Messenger)
- B. Setting the application's homepage route
- C. Rewriting all generated paths to that URI
- D. Configuring the default HTTP method for routes

??? success "Answer Q42"
    **A**

    RequestContext is normally populated from the incoming Request. In CLI or a queue worker there is no request, so the generator uses default_uri to build correct absolute URLs instead of http://localhost.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls-in-commands)

**Q43.** A route path is /blog/. A GET request to /blog results in?  <small>_(medium · single)_</small>

- A. A 301 redirect to /blog/
- B. A 404 Not Found
- C. A 302 redirect to /blog/
- D. A direct match with no redirect

??? success "Answer Q43"
    **A**

    RedirectableUrlMatcher issues a 301 to the canonical trailing-slash URL for safe (GET/HEAD) methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-urls-with-trailing-slashes)

**Q44.** You want /docs to redirect (302) to the literal path /docs/intro via RedirectController. Which controller + default do you use?  <small>_(medium · config)_</small>

- A. urlRedirectAction with defaults: {path: /docs/intro, permanent: false}
- B. redirectAction with defaults: {route: /docs/intro}
- C. urlRedirectAction with defaults: {route: /docs/intro}
- D. redirectAction with defaults: {path: /docs/intro}

??? success "Answer Q44"
    **A**

    urlRedirectAction targets a literal path/URL via the `path` default; redirectAction targets a route name via the `route` default. Mixing the action with the wrong default key does not work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q45.** What status code does $this->redirectToRoute('blog_show', ['id' => $id]) return by default?  <small>_(medium · code)_</small>

- A. 302 Found
- B. 301 Moved Permanently
- C. 307 Temporary Redirect
- D. 303 See Other

??? success "Answer Q45"
    **A**

    redirectToRoute() builds a RedirectResponse with a 302 by default; pass a third status argument (e.g. 301) to change it. Use controller-level redirects when the target depends on logic/data.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/controller.html#redirecting)

**Q46.** What does #[Route(stateless: true)] primarily do?  <small>_(medium · internals)_</small>

- A. Asserts the route must not use the session (warns in debug if it does)
- B. Disables the routing cache
- C. Forces the HTTPS scheme
- D. Makes the route match any HTTP method

??? success "Answer Q46"
    **A**

    It flags accidental session usage during development, raising UnexpectedSessionUsageException in debug; important for cacheable and API endpoints. It is an assertion, not a hard prod block.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#stateless-routes)

**Q47.** Where does the special _fragment parameter take effect?  <small>_(medium · trap)_</small>

- A. During URL generation, appended as #fragment
- B. During matching
- C. In the response body
- D. In the session

??? success "Answer Q47"
    **A**

    _fragment is honoured by the generator and ignored by the matcher (a URL fragment is never sent to the server).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q48.** How do you read the matched route name inside a controller or listener?  <small>_(medium · code)_</small>

- A. $request->attributes->get('_route')
- B. $request->query->get('_route')
- C. $request->getRoute()
- D. $router->getMatchedRoute()

??? success "Answer Q48"
    **A**

    _route (and _route_params) are read-only outputs stored in the request attribute bag by RouterListener. There is no Request::getRoute() helper, and it is not a query parameter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q49.** For path /api/items.{_format} serving only JSON or XML defaulting to JSON, which config is correct?  <small>_(medium · config)_</small>

- A. defaults: {_format: json} + requirements: {_format: 'json|xml'}
- B. defaults: {_format: 'json|xml'}
- C. requirements: {_format: json}
- D. methods: [json, xml]

??? success "Answer Q49"
    **A**

    _format is a normal special parameter: a default gives it a value when the extension is absent, and a requirement whitelists the allowed formats. Without the requirement, items.exe would match. Formats are never HTTP methods.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q50.** Should you set _route or _route_params yourself in a route's defaults?  <small>_(medium · trap)_</small>

- A. No — they are read-only outputs injected by the matcher; you only read them
- B. Yes — _route sets the route name used for generation
- C. Yes — _route_params overrides captured placeholders
- D. Only _route_params may be set; _route is reserved

??? success "Answer Q50"
    **A**

    _route and _route_params are outputs the matcher writes; setting them in defaults is meaningless and would be overwritten. They exist for logging, subscribers and debugging.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q51.** Generating a URL for a route bound to a different host produces?  <small>_(medium · single)_</small>

- A. An absolute (or network) URL
- B. A root-relative path
- C. An exception
- D. A URL on the current host

??? success "Answer Q51"
    **A**

    A path-only URL cannot switch host, so the generator upgrades the reference type automatically.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q52.** Which config captures a subdomain {tenant} (lowercase alphanumerics/hyphen) on example.com, defaulting to www?  <small>_(medium · config)_</small>

- A. host: '{tenant}.example.com' + requirements: {tenant: '[a-z0-9\-]+'} + defaults: {tenant: www}
- B. path: '{tenant}.example.com'
- C. host: '{tenant}.example.com' with no requirement needed
- D. subdomain: '{tenant}' + domain: example.com

??? success "Answer Q52"
    **A**

    Host placeholders obey the same requirements/defaults rules as path ones; you set the constraint and a base default on the route's `host`. There is no `subdomain`/`domain` key, and the host belongs in `host`, not `path`.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q53.** For host '{tenant}.example.com', what does generateUrl('tenant_home', ['tenant' => 'acme'], UrlGeneratorInterface::ABSOLUTE_URL) produce (current host example.com)?  <small>_(medium · code)_</small>

- A. https://acme.example.com/
- B. /
- C. https://example.com/?tenant=acme
- D. https://www.example.com/

??? success "Answer Q53"
    **A**

    The tenant placeholder fills the host label, and because the requested host differs from the current one an absolute URL on acme.example.com is produced. tenant is a host placeholder, so it is not appended as a query arg.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q54.** How do you apply one host to a whole imported controller directory?  <small>_(medium · config)_</small>

- A. Set host: on the YAML resource import (alongside prefix/name_prefix)
- B. Set host: in services.yaml
- C. Use _host in each route's defaults
- D. It is not possible; host must be per-route

??? success "Answer Q54"
    **A**

    Import-level options — host, prefix, name_prefix — cascade to every route in the imported resource, so you avoid repeating host: on each action.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q55.** Why is a routing condition a poor substitute for a security voter/authorization check?  <small>_(medium · trap)_</small>

- A. A failed condition is a 404 (route not matched), not a 403, and cannot show a login page
- B. Conditions cannot read the request at all
- C. Conditions run after the controller, too late to deny access
- D. Conditions always return 403 on failure

??? success "Answer Q55"
    **A**

    Conditions are a matching filter: failing one just hides the route (404), so there is no 403 and no way to trigger authentication. Use Security voters for authorization.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q56.** A DELETE-only route /tags/{id} gets a GET. What does the 405 response's Allow header contain?  <small>_(medium · debug)_</small>

- A. DELETE — the verbs permitted by the matched path
- B. GET — the verb that was requested
- C. It has no Allow header
- D. */* — all methods

??? success "Answer Q56"
    **A**

    On a 405 the matcher collects the allowed methods of the matching path and returns them in the Allow header (DELETE here), telling the client which verbs are valid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

**Q57.** How do you make one route accept both PUT and PATCH?  <small>_(medium · config)_</small>

- A. methods: ['PUT', 'PATCH']
- B. methods: 'PUT|PATCH'
- C. Two separate routes are required
- D. methods: ['PUT'] with allowPatch: true

??? success "Answer Q57"
    **A**

    methods accepts a list of verbs; any listed verb matches. A single route can serve several verbs — no pipe syntax or extra flags needed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

**Q58.** Are HTTP method names in the methods option case-sensitive?  <small>_(medium · trap)_</small>

- A. No — matching is case-insensitive, though uppercase is conventional
- B. Yes — only uppercase verbs match
- C. Yes — only lowercase verbs match
- D. Only GET is case-insensitive

??? success "Answer Q58"
    **A**

    Method matching is case-insensitive, but you should write verbs in uppercase by convention for readability and debug:router clarity.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

**Q59.** A #[Route(path: ['en' => '/about', 'fr' => '/a-propos'])] produces what?  <small>_(medium · config)_</small>

- A. One route per locale, each carrying its _locale default
- B. A single route matching both paths
- C. A redirect between the two paths
- D. An error — arrays are not allowed

??? success "Answer Q59"
    **A**

    A localized path array expands at load time into one Route per locale, each with defaults['_locale'] set and a _locale requirement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q60.** Matching a route that sets the _locale parameter causes what?  <small>_(medium · internals)_</small>

- A. Request::setLocale() is called via the LocaleListener
- B. The session is destroyed
- C. A 301 redirect
- D. Nothing until you read the value

??? success "Answer Q60"
    **A**

    _locale is a special parameter applied by the LocaleListener on kernel.request, which calls Request::setLocale().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q61.** Which config exposes /{_locale}/blog restricted to en, fr or de and defaulting to en?  <small>_(medium · config)_</small>

- A. path '/{_locale}/blog' + requirements: {_locale: 'en|fr|de'} + defaults: {_locale: 'en'}
- B. path '/{_locale}/blog' with no requirement
- C. path '/blog' + locale: [en, fr, de]
- D. path '/{_locale<en|fr|de>}/blog' + defaults omitted

??? success "Answer Q61"
    **A**

    The _locale placeholder is constrained by a requirement whitelist and given a default. Omitting the requirement lets any /xx/blog match; there is no top-level locale: list on a route. (Inline requirement is valid too, but a default is still needed for it to be optional at the root.)

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q62.** What goes wrong if /{_locale}/blog has no _locale requirement?  <small>_(medium · trap)_</small>

- A. Any segment matches _locale, so /xx/blog or /foo/blog wrongly match
- B. The route fails to compile
- C. The default locale is ignored
- D. Symfony injects a default en|fr requirement automatically

??? success "Answer Q62"
    **A**

    Without a requirement, _locale keeps the default [^/]+ and matches any label, so invalid locales like /xx/blog match. Always whitelist _locale with a requirement.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q63.** Which files hold the compiled router in the cache directory?  <small>_(medium · single)_</small>

- A. url_matching_routes.php and url_generating_routes.php
- B. routes.php and router.php
- C. matcher.php and generator.php
- D. RouteCollection.php

??? success "Answer Q63"
    **A**

    The CompiledUrlMatcherDumper and CompiledUrlGeneratorDumper write these two files that the Router loads at runtime.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q64.** In debug:router output, a route shows Scheme=ANY and Host=ANY. What does that mean?  <small>_(medium · trap)_</small>

- A. The route has no scheme/host constraint, so it matches any scheme and host
- B. The route is disabled
- C. The route only matches literally the host 'ANY'
- D. The route requires both HTTP and HTTPS simultaneously

??? success "Answer Q64"
    **A**

    ANY is the compiled view's way of saying no constraint was set for that column; such a route matches regardless of scheme/host. It is not a literal value.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q65.** Why do new routes appear immediately in dev but not in prod?  <small>_(medium · internals)_</small>

- A. In dev the router tracks route files as cache resources and rebuilds when they change; prod does not
- B. Dev disables the compiled router entirely
- C. Prod reads routes from the database
- D. Dev and prod share the same cache, so it is a timing issue

??? success "Answer Q65"
    **A**

    In dev, route files are registered as cache resources so Symfony detects changes and rebuilds the compiled matcher/generator automatically. In prod the cache is warmed once (cache:clear/warmup) and not auto-refreshed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q66.** Which of the following statements are true about route parameter requirements? (select all that apply)  <small>_(medium · multiple)_</small>

- A. The inline syntax {id<\d+>} is exactly equivalent to requirements: {id: '\d+'}
- B. A URL that violates a requirement simply fails to match that route (typically ending in a 404), never a 400 from routing
- C. A placeholder without a requirement matches [^/]+ by default, so it cannot span path segments
- D. Requirement regexes must be anchored manually with ^ and $ to work
- E. A failing requirement makes the router return a 400 Bad Request

??? success "Answer Q66"
    **A, B, C**

    Inline <...> is syntactic sugar for a requirements entry, and because the requirement is compiled into the route regex a violating value just does not match — matching moves on and usually ends in a 404. The default token pattern is [^/]+ (use .+ to cross slashes). Requirements are implicitly anchored, so adding ^/$ is wrong, and routing never produces a 400 for a bad parameter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

**Q67.** Which of the following statements are true about HTTP method matching in Symfony routing? (select all that apply)  <small>_(medium · multiple)_</small>

- A. A request whose path matches but whose verb is not allowed gets a 405 Method Not Allowed with an Allow header
- B. A route declaring methods: ['GET'] also matches HEAD requests automatically
- C. A scheme mismatch on an https-only route also returns a 405
- D. A form's _method field overrides the HTTP method for routing by default, with no configuration

??? success "Answer Q67"
    **A, B**

    When host and path match but the verb does not, the matcher throws MethodNotAllowedException, surfaced as a 405 listing the allowed verbs, and GET routes match HEAD because HttpKernel serves HEAD as a bodyless GET. A scheme mismatch is handled differently — the redirectable matcher redirects to the correct scheme — and the _method override only works after calling Request::enableHttpMethodParameterOverride().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-http-methods)

**Q68.** Which of the following statements are true about localized routes and locale guessing? (select all that apply)  <small>_(medium · multiple)_</small>

- A. A #[Route] whose path is a locale => path map expands into one route per locale, each carrying the matching _locale default
- B. Symfony does not guess the locale from the Accept-Language header by default; that behaviour is opt-in
- C. framework.default_locale takes precedence over a _locale parameter matched in the URL
- D. generateUrl() always uses the default locale unless you rebuild the router

??? success "Answer Q68"
    **A, B**

    Localized path arrays are expanded at load time into per-locale routes with a _locale default, and Accept-Language parsing requires opting in via set_locale_from_accept_language (or reading getPreferredLanguage() yourself). The precedence is matched _locale first, then the sticky session locale, then default_locale, and generation reuses the current request's locale unless you pass _locale explicitly.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q69.** Which loader reads #[Route] attributes into the RouteCollection in a Symfony 8 app?  <small>_(hard · internals)_</small>

- A. AttributeRouteControllerLoader (built on AttributeClassLoader)
- B. YamlFileLoader
- C. AnnotationClassLoader (removed in Symfony 8)
- D. XmlFileLoader

??? success "Answer Q69"
    **A**

    Attribute routes are read by AttributeClassLoader, wrapped by the framework's AttributeRouteControllerLoader. YamlFileLoader/XmlFileLoader handle those formats, and AnnotationClassLoader no longer exists in Symfony 8. All loaders implement LoaderInterface and are orchestrated by a DelegatingLoader.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q70.** Two routes share the path shape /blog/{x}: blog_show has {slug} (default [^/]+) declared first, blog_paged has {page<\\d+>} declared second. Which route matches /blog/42?  <small>_(hard · code)_</small>

- A. blog_show — the first route matches /42 as a slug, shadowing the numeric route
- B. blog_paged — the numeric requirement always wins
- C. Neither — the ambiguity is a 404
- D. Both — the matcher runs both controllers

??? success "Answer Q70"
    **A**

    Matching is first-match-wins in declaration order. Because blog_show's {slug} defaults to [^/]+, it also matches 42, so it captures /blog/42 before the numeric route is ever tried. Declare the numeric route first to disambiguate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#parameters-validation)

**Q71.** How does RouteCompiler represent /blog/{page<\d+>} in the CompiledRoute regex?  <small>_(hard · internals)_</small>

- A. As a named capture group, e.g. #^/blog/(?P<page>\d+)$#sD
- B. As an unnamed group #^/blog/(\d+)$#
- C. As two separate regexes joined at runtime
- D. It is not compiled; the requirement is checked in the controller

??? success "Answer Q71"
    **A**

    RouteCompiler::compile() extracts each {name} token and substitutes it with a named capture group using its requirement (or [^/]+ by default), producing a single anchored regex. Named groups are how the matcher maps captured values back to parameter names.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/RouteCompiler.php)

**Q72.** In the path /{a}/{b}, which placeholder can be made optional?  <small>_(hard · trap)_</small>

- A. b only, because it is the trailing placeholder
- B. a only
- C. Both, independently
- D. Neither

??? success "Answer Q72"
    **A**

    Only trailing placeholders can be optional; a gap in the middle cannot be located by the matcher. RouteCompiler emits nested optional groups from the tail, so an optional a with a required b is impossible.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#optional-parameters)

**Q73.** A route declares schemes: ['https'], the current context is http, and you call generateUrl() with the default ABSOLUTE_PATH. What is returned?  <small>_(hard · trap)_</small>

- A. An absolute https URL — generation is upgraded because a path cannot switch scheme
- B. A root-relative path /... as requested
- C. An InvalidParameterException
- D. An http absolute URL

??? success "Answer Q73"
    **A**

    When the target route's scheme differs from the context, the generator must emit an absolute URL with the correct (https) scheme, overriding the requested ABSOLUTE_PATH — a path-only URL could not change scheme.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q74.** A POST to /blog when the route is defined as /blog/ yields?  <small>_(hard · trap)_</small>

- A. 405 Method Not Allowed
- B. 301 redirect
- C. 200 OK
- D. 308 redirect

??? success "Answer Q74"
    **A**

    Redirecting a POST would alter the method, so the matcher returns 405 rather than a trailing-slash redirect. The auto-redirect is GET/HEAD only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#redirecting-urls-with-trailing-slashes)

**Q75.** For a RedirectController route, where is the 30x response actually produced?  <small>_(hard · internals)_</small>

- A. In the controller — it returns a RedirectResponse like any normal action
- B. In the matcher, which emits the redirect before any controller runs
- C. In RouterListener during kernel.request
- D. In the HttpKernel before routing

??? success "Answer Q75"
    **A**

    A redirect route is an ordinary route whose _controller is RedirectController; the kernel runs it and it returns a RedirectResponse. The matcher only produces redirects itself in the special trailing-slash / scheme cases.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bundle/FrameworkBundle/Controller/RedirectController.php)

**Q76.** Why is permanent: true (301) a poor choice for a temporary or A/B redirect?  <small>_(hard · trap)_</small>

- A. Browsers cache 301s aggressively, so you cannot easily change the target later
- B. 301 is not a valid redirect status
- C. 301 strips query parameters automatically
- D. 301 requires HTTPS

??? success "Answer Q76"
    **A**

    A 301 tells clients the move is permanent, so browsers cache it hard and may not re-request the old URL. Use 302 (the default) while a target is still in flux.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q77.** Which component copies the matcher's output parameters into $request->attributes?  <small>_(hard · internals)_</small>

- A. RouterListener, on the kernel.request event
- B. ControllerResolver, when resolving _controller
- C. The UrlMatcher itself writes directly to the Request
- D. ArgumentResolver, on kernel.controller

??? success "Answer Q77"
    **A**

    UrlMatcher::match() returns an array (route defaults + captured placeholders + _route/_route_params); RouterListener, a kernel.request subscriber, copies each entry into the request attribute bag. ControllerResolver and ArgumentResolver then consume _controller and the args later.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/RouterListener.php)

**Q78.** During matching, when is the host constraint checked?  <small>_(hard · internals)_</small>

- A. Before the path regex
- B. After the controller runs
- C. Only during URL generation
- D. Never; host is informational

??? success "Answer Q78"
    **A**

    matchCollection() tests the compiled host regex against RequestContext::getHost() first; only if it matches does it test the path regex.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q79.** How is the host constraint stored on a CompiledRoute?  <small>_(hard · internals)_</small>

- A. As a second, separate regex (getHostRegex) and its own token list
- B. Merged into the single path regex
- C. As a plain string compared with ===
- D. It is not compiled; the host is checked at runtime by DNS

??? success "Answer Q79"
    **A**

    RouteCompiler compiles `host` into its own regex and token list on the CompiledRoute, kept separate from the path regex, so matchCollection() can test host and path independently at negligible cost.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/RouteCompiler.php)

**Q80.** Why should host constraints be written in lowercase?  <small>_(hard · trap)_</small>

- A. The context host is normalized to lowercase, so an uppercase regex will not match
- B. YAML requires lowercase host values
- C. Uppercase hosts are rejected with a 400
- D. Host matching is always case-insensitive, so it does not matter

??? success "Answer Q80"
    **A**

    RequestContext lowercases the incoming host. A case-sensitive constraint like Admin.Example.com would then fail against admin.example.com. Write host patterns in lowercase.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

**Q81.** A route's condition expression evaluates to false. What is the result?  <small>_(hard · trap)_</small>

- A. 404 — the route is simply not matched
- B. 403 Forbidden
- C. 405 Method Not Allowed
- D. The controller runs anyway

??? success "Answer Q81"
    **A**

    A false condition means the route does not match; matching continues and may end in a 404. It is not authorization, so it never produces a 403.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q82.** To reference service('x') in a routing condition, service x must…  <small>_(hard · internals)_</small>

- A. Be tagged routing.condition_service (e.g. via #[AsRoutingConditionService])
- B. Be public
- C. Implement RouterInterface
- D. Extend AbstractController

??? success "Answer Q82"
    **A**

    Only services tagged routing.condition_service are exposed to the routing expression language. Visibility/base class are irrelevant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q83.** Which condition matches only when the request query string contains a 'preview' key?  <small>_(hard · code)_</small>

- A. condition: "request.query.has('preview')"
- B. condition: "request.get('preview') == true"
- C. condition: "query.preview is defined"
- D. condition: "has('preview')"

??? success "Answer Q83"
    **A**

    Inside a condition, `request` is the HttpFoundation Request, so request.query.has('preview') is the idiomatic check. `query` alone is not a variable, and there is no bare has() function.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q84.** How are route conditions executed at request time?  <small>_(hard · internals)_</small>

- A. As pre-compiled PHP closures baked into the dumped matcher (not runtime eval)
- B. Via eval() of the expression string on each request
- C. By calling a Twig template
- D. They are evaluated once at boot and cached as booleans

??? success "Answer Q84"
    **A**

    The framework compiles all conditions ahead of time through ExpressionLanguage and the routing ExpressionLanguageProvider, so the dumped matcher contains compiled closures. UrlMatcher::handleRouteRequirements() runs them after host/path match — no per-request eval, and they cannot be reduced to a constant because they depend on the live request.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Matcher/UrlMatcher.php)

**Q85.** You tag a service #[AsRoutingConditionService(alias: 'feature_checker')]. How do you call its isEnabled() method in a condition?  <small>_(hard · config)_</small>

- A. condition: "service('feature_checker').isEnabled(request)"
- B. condition: "feature_checker.isEnabled(request)"
- C. condition: "@feature_checker.isEnabled(request)"
- D. condition: "container.get('feature_checker').isEnabled(request)"

??? success "Answer Q85"
    **A**

    The alias becomes the argument to the service() function; you then call methods on the returned object and can pass request. There is no bare identifier, @ syntax or container variable in routing expressions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-expressions)

**Q86.** An http request hits a route restricted with schemes: ['https']. What happens?  <small>_(hard · internals)_</small>

- A. It is redirected to the https URL
- B. 405 Method Not Allowed
- C. 403 Forbidden
- D. 404 Not Found

??? success "Answer Q86"
    **A**

    The RedirectableUrlMatcher redirects a scheme mismatch to the correct scheme rather than rejecting it — contrast with a wrong method, which is a 405.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#matching-the-http-scheme)

**Q87.** For a form's _method field to influence which route matches, you must…  <small>_(hard · trap)_</small>

- A. Call Request::enableHttpMethodParameterOverride()
- B. Add methods: ['_method']
- C. Do nothing — it is enabled by default
- D. Set framework.http_method_override: false

??? success "Answer Q87"
    **A**

    Method override is opt-in; once enabled, getMethod() returns the overridden verb that the matcher uses. It is not on by default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q88.** Does Symfony guess the user's locale from the Accept-Language header by default?  <small>_(hard · trap)_</small>

- A. No — you must enable set_locale_from_accept_language or do it manually
- B. Yes, always
- C. Only for API routes
- D. Only in the dev environment

??? success "Answer Q88"
    **A**

    Locale precedence is a matched _locale, then the sticky session locale, then default_locale; Accept-Language is opt-in. To honour it, read Request::getPreferredLanguage($available) or enable the option.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#localized-routes-i18n)

**Q89.** Which two listeners cooperate to apply and propagate the request locale?  <small>_(hard · internals)_</small>

- A. LocaleListener (sets Request locale from _locale) and LocaleAwareListener (propagates it to locale-aware services)
- B. RouterListener and ControllerListener
- C. TranslatorListener and SessionListener
- D. FirewallListener and LocaleListener

??? success "Answer Q89"
    **A**

    LocaleListener reads _locale on kernel.request and calls setLocale(); LocaleAwareListener then propagates the locale to locale-aware services such as the translator. RouterListener only copies matcher output into attributes.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleListener.php)

**Q90.** router:match /blog/hello reports no match, but the page works for real GET requests. What is the likely cause?  <small>_(hard · debug)_</small>

- A. You omitted --method=GET, so the default context did not reproduce the real request
- B. The compiled cache is corrupt
- C. router:match cannot test parameterized paths
- D. The route is missing from url_generating_routes.php

??? success "Answer Q90"
    **A**

    router:match builds a RequestContext from the options you pass; without --method/--host/--scheme it may not reproduce the real request and can report a no-match (or a method rejection) that does not happen in production. Pass the exact conditions.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#debugging-routes)

**Q91.** Which of the following statements are true about URL generation? (select all that apply)  <small>_(hard · multiple)_</small>

- A. The default reference type is ABSOLUTE_PATH, producing a root-relative path like /blog/42
- B. Parameters that do not correspond to a route placeholder are appended to the generated URL as a query string
- C. The reference-type constants (ABSOLUTE_URL, NETWORK_PATH, ...) are defined on UrlGeneratorInterface
- D. The Twig functions path() and url() are interchangeable — both emit absolute URLs
- E. In a console command, ABSOLUTE_URL automatically picks up the production host without any configuration

??? success "Answer Q91"
    **A, B, C**

    generateUrl() defaults to ABSOLUTE_PATH, left-over (non-placeholder) parameters become the ?key=value query string, and the constants live on UrlGeneratorInterface. In Twig, path() maps to ABSOLUTE_PATH while url() maps to ABSOLUTE_URL, and in CLI there is no request, so absolute URLs fall back to http://localhost unless framework.router.default_uri is configured.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q92.** Which of the following statements are true about the special underscore routing attributes? (select all that apply)  <small>_(hard · multiple)_</small>

- A. _route and _route_params are read-only outputs injected by the matcher into the request attributes
- B. _format sets the request format via Request::setRequestFormat(), influencing the response Content-Type
- C. _fragment only takes effect during URL generation (appended as #fragment); it plays no role in matching
- D. Setting _route in a route's defaults changes what $request->attributes->get('_route') returns
- E. stateless: true hard-blocks all session usage in production

??? success "Answer Q92"
    **A, B, C**

    The matcher injects _route/_route_params and RouterListener copies them into request attributes for you to read, _format drives content negotiation and the default Content-Type, and _fragment is honoured only by the generator. You never set _route yourself, and stateless: true is an assertion that raises an UnexpectedSessionUsageException warning in debug — not a hard production block.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#special-parameters)

**Q93.** Which of the following statements are true about host (domain) matching? (select all that apply)  <small>_(hard · multiple)_</small>

- A. A host placeholder like {tenant} matches [^.]+ by default — a single label that cannot contain dots
- B. The host regex is tested before the path regex when matching a route
- C. Generating a URL for a route on a different host produces an absolute (or network) URL automatically
- D. Host placeholders cannot have requirements or defaults; only path placeholders support them
- E. A path-only (relative) URL can switch subdomains as long as the route declares a host

??? success "Answer Q93"
    **A, B, C**

    Host tokens use the dot as separator, so they default to [^.]+ instead of [^/]+, and matchCollection() checks the compiled host regex before even trying the path. Because a path-only URL cannot change host, the generator upgrades cross-host links to absolute/network URLs. Host placeholders obey the same requirements/defaults rules as path placeholders — that is how a missing subdomain can default to www.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#sub-domain-routing)

---

<small>Back to [Chapter Exams](index.md) · [Routing](../routing/index.md)</small>
