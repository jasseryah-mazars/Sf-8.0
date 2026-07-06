# Flashcards — Templating (Twig)

43 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. Which Twig delimiter executes a statement without printing anything?"
    **✅ {% ... %}**

    {% %} runs tags/control flow, {{ }} prints an (escaped) expression, and {# #} is a comment that is stripped at compile time.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

??? question "2. What does {{ 7 // 2 }} output in Twig?"
    **✅ 3**

    // is integer (floor) division in Twig; / performs float division and would return 3.5.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#math)

??? question "3. What is the result of {{ "a" ~ 1 + 1 }}?"
    **✅ "a2"**

    + binds tighter than ~, so it evaluates as "a" ~ (1 + 1) => "a" ~ 2 => "a2". ~ is string concatenation, not addition.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

??? question "4. How do you strip whitespace between HTML tags in current Twig 3.x?"
    **✅ {% apply spaceless %}...{% endapply %}**

    The {% spaceless %} tag was removed in Twig 3; use the spaceless filter via {% apply spaceless %} (or the {{- -}} whitespace modifiers).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/spaceless.html)

??? question "5. In Symfony, how is the default auto-escaping strategy chosen for a template?"
    **✅ Guessed from the template file extension (e.g. .html.twig => html)**

    TwigBundle configures autoescape to 'name', using FileExtensionEscapingStrategy::guess() so .html.twig escapes as html, .js.twig as js, .txt.twig not at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#output-escaping)

??? question "6. A value is placed inside <script>const x = "...";</script>. Which escape filter is correct?"
    **✅ |e('js')**

    A JavaScript string context requires the 'js' strategy; HTML escaping does not neutralise the characters dangerous in JS.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

??? question "7. What does {% autoescape false %} ... {% endautoescape %} do?"
    **✅ Disables auto-escaping inside the block (use for trusted content only)**

    It turns escaping off within the block, exactly like piping every value through |raw. Only use it for trusted/sanitised content.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/autoescape.html)

??? question "8. Which escaping filter is required for a value used inside an HTML attribute?"
    **✅ |e('html_attr')**

    Attribute context needs the stricter html_attr encoder, which escapes spaces, =, backticks and other characters that html escaping leaves untouched.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

??? question "9. How many templates can a single template extend in Twig?"
    **✅ Exactly one**

    Twig uses single vertical inheritance. For reusing blocks from several templates (horizontal reuse), use the {% use %} tag instead.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

??? question "10. Inside an overridden block, what does {{ parent() }} render?"
    **✅ The parent template's version of that same block**

    parent() outputs the content of the same block from the parent template, letting a child extend rather than fully replace it.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/parent.html)

??? question "11. Which tag provides horizontal reuse of blocks (like a trait)?"
    **✅ {% use %}**

    {% use %} imports block definitions from another template without setting a parent, and multiple use statements are allowed.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/use.html)

??? question "12. What does app.user return when no one is authenticated?"
    **✅ null**

    AppVariable::getUser() reads the token from the token storage and returns its user, or null when there is no authenticated user.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "13. Which class backs the Twig `app` global in Symfony?"
    **✅ Symfony\Bridge\Twig\AppVariable**

    TwigBundle registers Symfony\Bridge\Twig\AppVariable as the `app` global; its getters expose user, request, session, flashes, etc.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/AppVariable.php)

??? question "14. Which of these is NOT a member of the `app` global?"
    **✅ app.controller**

    app exposes user, request, session, flashes, environment, debug, token, locale, current_route and current_route_parameters. There is no app.controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "15. What does app.environment return?"
    **✅ The kernel environment string, e.g. 'dev' or 'prod'**

    app.environment is the kernel environment (dev/prod/test); app.debug is the boolean debug flag. They are unrelated to OS env vars.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "16. How do you register a static global string in Twig?"
    **✅ Under twig.globals in config, or via a GlobalsInterface extension**

    Declare globals under twig.globals in twig.yaml, or return them from an extension implementing Twig\Extension\GlobalsInterface::getGlobals().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#global-variables)

??? question "17. Which attribute registers a custom Twig filter in current Twig 3.x?"
    **✅ #[AsTwigFilter]**

    Twig 3.x provides Twig\Attribute\AsTwigFilter and AsTwigFunction as an attribute-based alternative to returning TwigFilter/TwigFunction from an AbstractExtension.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#creating-a-twig-extension)

??? question "18. A custom filter returns '<b>x</b>' but the page shows escaped text. Why?"
    **✅ The filter must be declared with the is_safe => ['html'] option**

    Filter/function output is auto-escaped unless the TwigFilter/TwigFunction declares is_safe for the relevant context.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

??? question "19. What does the `default` filter replace?"
    **✅ Undefined, null AND empty values**

    default(x) substitutes x when the value is undefined, null or empty (unless you pass true as the second argument to only test 'defined').

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/default.html)

??? question "20. What does the `only` keyword do on an include?"
    **✅ Restricts the included template's scope to just the `with` variables**

    By default an include inherits the parent context; adding `only` isolates it so it sees only the variables passed via `with` (plus the app global).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

??? question "21. Which construct includes a template AND lets you override its blocks?"
    **✅ {% embed %}**

    embed combines include with extends-style block overriding, ideal for configurable components with slots.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/embed.html)

??? question "22. What does {% include ['a.html.twig', 'b.html.twig'] %} render?"
    **✅ The first template in the list that exists**

    Passing an array of names renders the first template that can be loaded, which is handy for theme overrides.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

??? question "23. What is loop.index on the first iteration of a for loop?"
    **✅ 1**

    loop.index is 1-based; loop.index0 is the 0-based counterpart.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

??? question "24. When does the `else` clause of a for loop execute?"
    **✅ When the collection is empty (zero iterations)**

    {% for ... else ... endfor %} renders the else block only when the loop produced no iterations.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-else-clause)

??? question "25. How do you skip iterations in a Twig for loop?"
    **✅ Filter the source, e.g. {% for x in items if x.active %}**

    Twig has no break/continue by design; filter the iterable inline or use an if inside the body.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

??? question "26. What is the difference between path() and url() in Twig?"
    **✅ path() returns a relative URL, url() returns an absolute URL**

    Both use UrlGeneratorInterface via RoutingExtension; path() uses ABSOLUTE_PATH (relative) and url() uses ABSOLUTE_URL (scheme + host).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-pages)

??? question "27. Given route 'search' => /search, what does path('search', {q: 'x', page: 2}) produce?"
    **✅ /search?q=x&page=2**

    Parameters not consumed by the route pattern are appended as the query string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "28. Which Twig extension provides path() and url()?"
    **✅ Symfony\Bridge\Twig\Extension\RoutingExtension**

    RoutingExtension wraps the UrlGeneratorInterface and reads the RequestContext to build relative and absolute URLs.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

??? question "29. How does render(controller('C::m')) execute the controller?"
    **✅ As a sub-request through HttpKernel (inline fragment)**

    The InlineFragmentRenderer issues a real HttpKernel sub-request, so the kernel events run again for the fragment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#embedding-controllers)

??? question "30. What happens with render_esi() when no ESI-capable reverse proxy is present?"
    **✅ It transparently falls back to inline rendering**

    Without a proxy that understands ESI, Symfony degrades render_esi to an inline sub-request so the page still works.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

??? question "31. Which service selects the fragment renderer for render()/render_esi()?"
    **✅ Symfony\Component\HttpKernel\Fragment\FragmentHandler**

    HttpKernelExtension delegates to FragmentHandler, which picks a FragmentRendererInterface (inline, esi, hinclude) by strategy name.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

??? question "32. What is the argument order of the `trans` filter?"
    **✅ (parameters, domain, locale)**

    The signature is message|trans(parameters = {}, domain = 'messages', locale = null).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html#translations-in-templates)

??? question "33. How do you pluralize a message in Symfony 8 templates?"
    **✅ Use ICU MessageFormat {count, plural, ...} in a +intl-icu domain**

    transchoice was removed; pluralization uses ICU MessageFormat, which is applied to catalogues whose domain ends with +intl-icu.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "34. A translation key has no entry for the current locale and no fallback. What is rendered?"
    **✅ The key string itself**

    The translator returns the untranslated message id when no translation is found.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

??? question "35. Where does #{...} string interpolation work in Twig?"
    **✅ Only inside double-quoted strings**

    The lexer only interpolates #{...} within double-quoted strings; single quotes render the text literally.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)

??? question "36. What is the result of {{ 1 + 2 ~ 3 }}?"
    **✅ "33"**

    + binds tighter than ~, so (1 + 2) ~ 3 => 3 ~ 3 => the string "33".

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

??? question "37. Which filter applies sprintf-style formatting in Twig?"
    **✅ format**

    The format filter wraps vsprintf, e.g. \"%s scored %d\"|format(a, b).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/format.html)

??? question "38. What does asset('css/app.css') return?"
    **✅ A public URL/path (relative to public/) with base path and version applied**

    asset() resolves a path relative to public/ through the Symfony\Component\Asset\Packages service, applying base path and versioning.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-css-and-javascript-assets)

??? question "39. What is the purpose of asset versioning?"
    **✅ Cache busting so browsers refetch changed files**

    Versioning changes the URL when a file changes (static version or a JSON manifest of content hashes) so clients do not serve a stale cached copy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/frontend.html)

??? question "40. Which build tools are OUT of scope when only using asset()?"
    **✅ AssetMapper and Webpack Encore**

    asset() only resolves the final public path/version. Bundling and hashing are done by AssetMapper or Webpack Encore, which are not covered here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/asset.html)

??? question "41. What does {{ dump() }} with no arguments do?"
    **✅ Dumps all variables available in the current template context**

    Called with no arguments, dump() outputs the entire render context (all passed variables plus globals).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

??? question "42. Why does dump() error in the prod environment?"
    **✅ The DumpExtension is only registered in debug mode**

    The dump function/tag come from the debug-only DumpExtension (backed by VarDumper); in prod the function is undefined, so leftover dumps throw.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

??? question "43. What is the difference between {{ dump(x) }} and {% dump x %}?"
    **✅ The function prints inline; the tag sends data to the collector without injecting markup**

    The dump() function outputs where called; the {% dump %} tag routes the data to the profiler/toolbar without adding markup to the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

---

<small>Back to [Flashcards](index.md) · [Templating (Twig)](../../twig/index.md)</small>
