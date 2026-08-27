# Flashcards — Templating (Twig)

109 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

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

??? question "4. How do you strip whitespace between HTML tags in Twig up to 3.22?"
    **✅ {% apply spaceless %}...{% endapply %}**

    The {% spaceless %} tag was removed in Twig 3; use the spaceless filter via {% apply spaceless %} (or the {{- -}} whitespace modifiers).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/spaceless.html)

??? question "5. For {{ user.name }}, in which order does Twig try to resolve the attribute?"
    **✅ $user['name'], then $user->name, then $user->name(), getName(), isName(), hasName()**

    Twig's attribute resolver tries array/index access first, then a public property, then method calls name(), getName(), isName() and hasName(). Force pure array access with user['name'] and dynamic names with attribute(user, key). A missing attribute yields null unless strict_variables is on.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#variables)

??? question "6. What does {{ -5|abs }} produce, given filters bind tighter than any operator?"
    **✅ -5, because it parses as -(5|abs)**

    The pipe binds tighter than the unary minus, so the expression is -(5|abs) = -(5) = -5, not (-5)|abs. Wrap in parentheses — (-5)|abs — to get 5. This tight binding of filters is a recurring exam trap.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#math)

??? question "7. How is a Twig template turned into something executable, and what is cached?"
    **✅ It is lexed, parsed and compiled to a PHP class extending Twig\Template, cached under var/cache**

    Twig is a compiler: Environment::render() runs lex -> parse -> compile, emitting a PHP class extending Twig\Template whose doDisplay() contains echo statements. It is written once to var/cache/<env>/twig via FilesystemCache and reused, so runtime parsing cost is zero after the first compile.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/api.html)

??? question "8. With strict_variables enabled, what happens when you print an undefined variable {{ missing }}?"
    **✅ It throws a RuntimeError; without strict_variables it would silently print empty**

    With strict_variables on (recommended in dev), an undefined variable throws so typos surface early. In lenient mode (the default) it prints an empty string. Note a variable that resolves to null still prints empty even under strict_variables — strict_variables catches undefined, not null.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/api.html#environment-options)

??? question "9. True or false: {# ... #} comments are removed at compile time and never reach the browser."
    **✅ True**

    Twig {# #} comments are stripped during compilation and produce no output, unlike HTML <!-- --> comments which are sent to the client. Use {# #} for template notes you do not want leaking to users.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

??? question "10. In Symfony, how is the default auto-escaping strategy chosen for a template?"
    **✅ Guessed from the template file extension (e.g. .html.twig => html)**

    TwigBundle configures autoescape to 'name', using FileExtensionEscapingStrategy::guess() so .html.twig escapes as html, .js.twig as js, .txt.twig not at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#output-escaping)

??? question "11. A value is placed inside <script>const x = "...";</script>. Which escape filter is correct?"
    **✅ |e('js')**

    A JavaScript string context requires the 'js' strategy; HTML escaping does not neutralise the characters dangerous in JS.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

??? question "12. What does {% autoescape false %} ... {% endautoescape %} do?"
    **✅ Disables auto-escaping inside the block (use for trusted content only)**

    It turns escaping off within the block, exactly like piping every value through |raw. Only use it for trusted/sanitised content.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/autoescape.html)

??? question "13. Which escaping filter is required for a value used inside an HTML attribute?"
    **✅ |e('html_attr')**

    Attribute context needs the stricter html_attr encoder, which escapes spaces, =, backticks and other characters that html escaping leaves untouched.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

??? question "14. How much of a .txt.twig template's {{ }} output is auto-escaped by Symfony's default strategy?"
    **✅ None — the .txt.twig extension maps to no escaping (false)**

    FileExtensionEscapingStrategy::guess() maps .txt.twig to false (no escaping), which is correct because plain-text output has no HTML context. The trap is assuming escaping is always html — it is chosen per extension, and .txt.twig escapes nothing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#output-escaping)

??? question "15. A template renders user-submitted comment HTML with {{ comment|raw }}. What is the risk?"
    **✅ Stored XSS: |raw disables escaping, so untrusted markup/scripts run unfiltered**

    |raw marks the value safe and skips auto-escaping, so any <script> in a user comment executes — a classic stored XSS hole. Only use |raw on HTML you generated or ran through the HtmlSanitizer component; never on raw user input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/html_sanitizer.html)

??? question "16. At which point is auto-escaping applied to a value?"
    **✅ At print time on {{ }}, via EscaperExtension adding an implicit |escape**

    EscaperExtension inserts an implicit |escape(strategy) on every {{ }} output node that is not already marked safe — escaping happens when a value is printed, not when it is set. So {% set x = untrusted %} stores it raw; the escaping occurs only when you later print {{ x }}.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Extension/EscaperExtension.php)

??? question "17. Which PHP function backs Twig's default 'html' escaping strategy?"
    **✅ htmlspecialchars() with ENT_QUOTES | ENT_SUBSTITUTE**

    The EscaperRuntime maps 'html' to htmlspecialchars() with ENT_QUOTES|ENT_SUBSTITUTE (encoding single and double quotes and substituting invalid code units). html_attr uses a stricter attribute encoder, js uses \\xNN hex, css uses CSS hex and url uses rawurlencode — each context has its own encoder because escaping is context-specific.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

??? question "18. In a .html.twig file, what does {{ '<b>hi</b>' }} render to the browser?"
    **✅ &lt;b&gt;hi&lt;/b&gt; (escaped, shown as literal text)**

    Auto-escaping (html strategy for .html.twig) converts the angle brackets to entities, so the literal markup is displayed as text rather than rendered as bold. To output real markup you would need |raw (only for trusted content).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#output-escaping)

??? question "19. True or false: in Symfony, Twig output escaping is enabled by default."
    **✅ True**

    Auto-escaping is on by default (autoescape: name) as a baseline XSS defence; every {{ }} is escaped for its context unless the value is marked safe or passed through |raw. You opt out per value, not opt in.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#output-escaping)

??? question "20. How many templates can a single template extend in Twig?"
    **✅ Exactly one**

    Twig uses single vertical inheritance. For reusing blocks from several templates (horizontal reuse), use the {% use %} tag instead.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

??? question "21. Inside an overridden block, what does {{ parent() }} render?"
    **✅ The parent template's version of that same block**

    parent() outputs the content of the same block from the parent template, letting a child extend rather than fully replace it.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/parent.html)

??? question "22. Which tag provides horizontal reuse of blocks (like a trait)?"
    **✅ {% use %}**

    {% use %} imports block definitions from another template without setting a parent, and multiple use statements are allowed.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/use.html)

??? question "23. What is the difference between {{ parent() }} and {{ block('sidebar') }}?"
    **✅ parent() renders the parent's version of the current block; block('x') renders block x of the current hierarchy**

    parent() is contextual — it renders the same block one level up in the inheritance chain. block('name') prints a named block resolved from the current template hierarchy (and block('name', 'other.html.twig') from another template). Confusing the two is a common exam distractor.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/block.html)

??? question "24. Why must {% extends %} be the first tag, and what can a child template NOT do?"
    **✅ A child that extends a parent cannot output markup outside blocks; rendering starts at the root ancestor**

    When a template extends another, rendering begins at the root ancestor and walks down, so any top-level text a child writes outside a block is ignored (or errors). extends can be a dynamic expression resolved at runtime, which is why it must be resolvable first. Put all child content inside blocks.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

??? question "25. How does template inheritance work at the compiled-PHP level?"
    **✅ Each {% block %} becomes a block_<name>() method; extends makes the child class override the parent's methods**

    Every template compiles to a class extending Twig\Template; a block becomes a block_<name>() method and extends wires up parentage so child methods override parent ones — exactly like PHP method overriding. A block table ($this->blocks) lets an override anywhere in the chain win.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Template.php)

??? question "26. What does {% extends request.isXmlHttpRequest ? '_ajax.html.twig' : 'base.html.twig' %} demonstrate?"
    **✅ extends accepts a dynamic expression, resolved at runtime to choose the parent**

    The parent name in extends can be any expression, evaluated at runtime, so you can pick a layout conditionally (e.g. a bare layout for AJAX requests). This is why extends is resolved at runtime rather than purely at compile time.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

??? question "27. Which statements about {% use %} are correct? (choose 2)"
    **✅ It imports block definitions only, not surrounding markup ; Multiple use statements are allowed in one template**

    {% use %} performs horizontal reuse: it pulls in block definitions (like a PHP trait) without setting a parent, and you may use several templates, aliasing name clashes with 'as'. It does not import non-block markup and does not establish inheritance — that is what extends is for.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/use.html)

??? question "28. What does app.user return when no one is authenticated?"
    **✅ null**

    AppVariable::getUser() reads the token from the token storage and returns its user, or null when there is no authenticated user.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "29. Which class backs the Twig `app` global in Symfony?"
    **✅ Symfony\Bridge\Twig\AppVariable**

    TwigBundle registers Symfony\Bridge\Twig\AppVariable as the `app` global; its getters expose user, request, session, flashes, etc.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/AppVariable.php)

??? question "30. Which of these is NOT a member of the `app` global?"
    **✅ app.controller**

    app exposes user, request, session, flashes, environment, debug, token, locale, current_route and current_route_parameters. There is no app.controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "31. What does app.environment return?"
    **✅ The kernel environment string, e.g. 'dev' or 'prod'**

    app.environment is the kernel environment (dev/prod/test); app.debug is the boolean debug flag. They are unrelated to OS env vars.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "32. How do you register a static global string in Twig?"
    **✅ Under twig.globals in config, or via a GlobalsInterface extension**

    Declare globals under twig.globals in twig.yaml, or return them from an extension implementing Twig\Extension\GlobalsInterface::getGlobals().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#global-variables)

??? question "33. In Symfony 8, which expression prints the current user's identifier?"
    **✅ {{ app.user.userIdentifier }}**

    UserInterface exposes getUserIdentifier(), so the Twig accessor is app.user.userIdentifier. The legacy getUsername()/username idiom is gone in modern Symfony. Remember to guard app.user first — it is null for anonymous requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/security.html#the-user)

??? question "34. Which app.* accesses have a side effect? (choose 2)"
    **✅ app.session — accessing it can start the session ; app.flashes — reading flash messages consumes (clears) them**

    Accessing app.session may start the session (which can defeat HTTP caching), and reading app.flashes consumes the messages so they are cleared after display — both have side effects. app.environment and app.debug are plain reads with no side effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "35. You need a global whose value is computed from an injected service. Which approach fits best?"
    **✅ An extension implementing GlobalsInterface::getGlobals() returning the computed value**

    GlobalsInterface::getGlobals() lets an extension inject a service and return computed values, resolved lazily when the extension is instantiated. A static YAML twig.globals entry (even '@service') is fine for simple references, but computed/lazy values belong in a GlobalsInterface extension. There is no #[AsGlobal] attribute.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#global-variables)

??? question "36. A controller passes a variable named `app` to the template. What happens?"
    **✅ The local variable shadows the global, so app.user etc. refer to the passed value**

    Globals are merged into the render context, so a local variable of the same name shadows the global. Passing your own `app` variable breaks app.user/app.request access inside that template — avoid reusing reserved global names.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#global-variables)

??? question "37. Which snippet safely greets an authenticated user and falls back to 'Guest'?"
    **✅ {{ app.user ? app.user.userIdentifier : 'Guest' }}**

    Because app.user is null for anonymous requests, you must guard it before dereferencing. The ternary checks app.user first. Reading app.user.userIdentifier directly throws under strict_variables (and is the classic anonymous-page crash); Guest is a bareword not a string in the third option; app.userIdentifier is not a member.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "38. Which attribute registers a custom Twig filter in Twig up to 3.22?"
    **✅ #[AsTwigFilter]**

    Twig 3.x provides Twig\Attribute\AsTwigFilter and AsTwigFunction as an attribute-based alternative to returning TwigFilter/TwigFunction from an AbstractExtension.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#creating-a-twig-extension)

??? question "39. A custom filter returns '<b>x</b>' but the page shows escaped text. Why?"
    **✅ The filter must be declared with the is_safe => ['html'] option**

    Filter/function output is auto-escaped unless the TwigFilter/TwigFunction declares is_safe for the relevant context.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

??? question "40. What does the `default` filter replace?"
    **✅ Undefined, null AND empty values**

    default(x) substitutes x when the value is undefined, null or empty (unless you pass true as the second argument to only test 'defined').

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/default.html)

??? question "41. Which statement about filters vs functions is correct?"
    **✅ A filter is applied with the pipe (value|f) and a function is called by name f(args); date exists as both**

    value|filter transforms a piped value while function(args) is called by name; they are registered as distinct TwigFilter/TwigFunction objects. A name like date is registered both as a filter (now|date('Y')) and a function (date()). path()/lower are function and filter respectively — the reversed option is wrong.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#filters)

??? question "42. A TwigFilter is declared with needs_environment: true. What changes about the callable?"
    **✅ Twig passes the Environment as the first argument, shifting the user arguments right**

    needs_environment injects Twig\Environment as the first callable argument (and needs_context injects the render context array), so your declared parameters come after it. Forgetting this argument shift is a common cause of TypeErrors when writing extensions.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

??? question "43. Which method definition correctly registers a `vat` function via attributes?"
    **✅ #[AsTwigFunction('vat')] public function vat(float $n, float $rate = 0.20): float**

    Twig\Attribute\AsTwigFunction('vat') on a method registers the function; Symfony autoconfiguration wires the class. There is no #[TwigFunction] or #[AsFunction] attribute, and functions are not auto-detected by method name without an attribute or getFunctions() registration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#creating-a-twig-extension)

??? question "44. Why put a filter's heavy-dependency logic in a runtime class rather than the extension itself?"
    **✅ The runtime is lazily instantiated only when the filter is actually used, so heavy services are not built every request**

    An AbstractExtension is instantiated on every request, so injecting a costly dependency into it slows all requests. Moving the logic to a runtime (RuntimeExtensionInterface / the attribute style) makes it lazy — built only when the filter is invoked. Auto-escaping is unaffected by this choice.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#lazy-loading-nodes)

??? question "45. Given an empty string, what do {{ ''|default('x') }} and {{ '' ?? 'x' }} produce?"
    **✅ 'x' and '' — default replaces empty values, ?? only replaces null/undefined**

    The default filter substitutes for undefined, null AND empty values ('', [], false), so ''|default('x') yields 'x'. The ?? operator only replaces null/undefined, so '' ?? 'x' keeps the empty string. This difference is a frequent exam trap.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/default.html)

??? question "46. What does the `only` keyword do on an include?"
    **✅ Restricts the included template's scope to just the `with` variables**

    By default an include inherits the parent context; adding `only` isolates it so it sees only the variables passed via `with` (plus the app global).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

??? question "47. Which construct includes a template AND lets you override its blocks?"
    **✅ {% embed %}**

    embed combines include with extends-style block overriding, ideal for configurable components with slots.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/embed.html)

??? question "48. What does {% include ['a.html.twig', 'b.html.twig'] %} render?"
    **✅ The first template in the list that exists**

    Passing an array of names renders the first template that can be loaded, which is handy for theme overrides.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

??? question "49. With {% include '_card.html.twig' with { title: t } only %}, is the app global still available inside the partial?"
    **✅ Yes — only isolates the parent's local variables but globals like app remain available**

    only restricts the include to just the with variables from the caller's local scope, but Twig globals (such as app) are merged into every template's context independently, so app.user etc. still work. Assuming only strips globals is a common misconception.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

??? question "50. A template exists but throws inside itself. Does `ignore missing` on the include suppress that error?"
    **✅ No — ignore missing only suppresses LoaderError for a missing template, not errors thrown while rendering an existing one**

    ignore missing guards only against the template not being found (LoaderError). Once a template is loaded, any runtime/compile error inside it still propagates. Treating ignore missing as a catch-all is a trap that hides real bugs.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

??? question "51. What does {{ include('_card.html.twig', { title: t }, with_context = false) }} do?"
    **✅ Renders the partial with only { title: t } (no parent context) and returns it as a string usable in an expression**

    The include() function returns a string (so it composes in expressions) and takes named options; with_context = false is the function-form equivalent of the only keyword, isolating the partial to the passed variables. Globals remain available.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/include.html)

??? question "52. How is an included template handled by Twig internally?"
    **✅ It is a separate compiled class, loaded via the loader and invoked at runtime — not textually inlined**

    The include tag compiles to a call to Twig\Template::display()/render() on the sub-template, which the FilesystemLoader resolves and which is compiled and cached like any other template. Includes are separate compiled classes invoked at runtime, not inlined text.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Loader/FilesystemLoader.php)

??? question "53. What is loop.index on the first iteration of a for loop?"
    **✅ 1**

    loop.index is 1-based; loop.index0 is the 0-based counterpart.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

??? question "54. When does the `else` clause of a for loop execute?"
    **✅ When the collection is empty (zero iterations)**

    {% for ... else ... endfor %} renders the else block only when the loop produced no iterations.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-else-clause)

??? question "55. How do you skip iterations in a Twig for loop?"
    **✅ Filter the source, e.g. {% for x in items if x.active %}**

    Twig has no break/continue by design; filter the iterable inline or use an if inside the body.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

??? question "56. Why might loop.length and loop.last be unavailable inside a for loop?"
    **✅ The iterable is not countable (e.g. a bare Generator), so Twig cannot know the total up front**

    loop.length, loop.last and loop.revindex require a countable iterable (array or Countable/Traversable Twig can count). For a non-countable Generator, Twig cannot determine the total without buffering, so those members may be omitted; loop.index and loop.first are always available.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

??? question "57. Inside a nested loop, how do you access the outer loop's current index?"
    **✅ loop.parent.loop.index**

    loop.parent gives the enclosing loop's context, so loop.parent.loop.index is the outer loop's 1-based index. A bare loop.index inside the inner loop refers to the inner loop only.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

??? question "58. Which is true about the tests `is null`, `is empty`, and `is defined`?"
    **✅ is empty is broadest — true for null, false, 0, '' and []; is null is only for null; is defined checks existence**

    is defined tests whether the variable exists at all (undefined is not the same as null); is null tests exact null; is empty is the broadest — true for null, false, 0, '' and []. Use is null when you must distinguish "no value" from "empty list", and combine with is defined for maybe-missing variables.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tests/empty.html)

??? question "59. What happens with {% for x in items %}...{% else %}Empty{% endfor %} when items is null?"
    **✅ Zero iterations run and the else block renders 'Empty' (no error in lenient mode)**

    Iterating null in lenient mode is safe — it produces zero iterations and falls through to the for...else block. That makes for...else the natural guard for a possibly-null collection, so you rarely need a wrapping {% if items %}.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-else-clause)

??? question "60. Which loop iterates a hash by key and value?"
    **✅ {% for key, value in map %}**

    Twig's key/value form is {% for key, value in map %} (key first). There is no foreach tag and no PHP-style => or 'as' syntax in Twig loops.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

??? question "61. True or false: Twig provides a {% break %} tag to exit a loop early."
    **✅ False**

    Twig deliberately has no break or continue tag to keep templates declarative. Filter the iterable (for x in items if ...) or slice it (items|slice(0, n)) to limit iterations instead.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

??? question "62. What is the difference between path() and url() in Twig?"
    **✅ path() returns a relative URL, url() returns an absolute URL**

    Both use UrlGeneratorInterface via RoutingExtension; path() uses ABSOLUTE_PATH (relative) and url() uses ABSOLUTE_URL (scheme + host).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-pages)

??? question "63. Given route 'search' => /search, what does path('search', {q: 'x', page: 2}) produce?"
    **✅ /search?q=x&page=2**

    Parameters not consumed by the route pattern are appended as the query string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "64. Which Twig extension provides path() and url()?"
    **✅ Symfony\Bridge\Twig\Extension\RoutingExtension**

    RoutingExtension wraps the UrlGeneratorInterface and reads the RequestContext to build relative and absolute URLs.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

??? question "65. You are building an HTML email template with a link back to the site. Which function should you use?"
    **✅ url() — an email needs an absolute URL (scheme + host); path() yields a relative link that breaks in mail clients**

    When a link leaves the page (emails, RSS, canonical tags, redirects consumed elsewhere) it must be absolute, so use url(). A relative path() link has no host and breaks once opened in a mail client. asset() is for static files, not routes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-pages)

??? question "66. path('article_show') is called but the route requires a {slug}. What happens at render time?"
    **✅ A MissingMandatoryParametersException is thrown**

    The generator throws MissingMandatoryParametersException when a required route parameter is not supplied. (An unknown route name instead throws RouteNotFoundException.) Both surface at render time, not silently.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html#generating-urls)

??? question "67. Which UrlGenerator reference types back path() and url() respectively?"
    **✅ path() => ABSOLUTE_PATH; url() => ABSOLUTE_URL**

    RoutingExtension calls UrlGenerator::generate() with ABSOLUTE_PATH for path() (a root-relative /path) and ABSOLUTE_URL for url() (scheme + host + path). The generator reads the RequestContext to build the host for absolute URLs.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

??? question "68. Which snippet builds a 'next page' link for the current route, incrementing page?"
    **✅ path(app.current_route, app.current_route_parameters|merge({ page: page + 1 }))**

    app.current_route and app.current_route_parameters expose the active route and its params; merging a new page value onto them and passing to path() rebuilds the current URL with one changed parameter. app.route/app.params are not real members, and + does not merge hashes (~ /merge do).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "69. How does render(controller('C::m')) execute the controller?"
    **✅ As a sub-request through HttpKernel (inline fragment)**

    The InlineFragmentRenderer issues a real HttpKernel sub-request, so the kernel events run again for the fragment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#embedding-controllers)

??? question "70. Which service selects the fragment renderer for render()/render_esi()?"
    **✅ Symfony\Component\HttpKernel\Fragment\FragmentHandler**

    HttpKernelExtension delegates to FragmentHandler, which picks a FragmentRendererInterface (inline, esi, hinclude) by strategy name.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

??? question "71. A sidebar just needs variables the parent already has. include or render(controller())?"
    **✅ include — it is the cheapest option when no extra logic/data is needed**

    Each inline embed is a real sub-request with its own overhead. If the fragment only needs data you already have, a plain include is far cheaper. Reserve render(controller()) for fragments that need their own services/data/cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#embedding-controllers)

??? question "72. What does render_hinclude() do differently from inline rendering?"
    **✅ It emits a placeholder that the browser resolves asynchronously via JavaScript**

    HIncludeFragmentRenderer outputs a placeholder tag resolved by the browser with JavaScript, so the main page renders immediately and the fragment loads asynchronously afterwards. Inline instead blocks on a synchronous sub-request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

??? question "73. What is true about kernel events when an inline fragment is rendered?"
    **✅ The full request lifecycle runs again for the sub-request (kernel.request, kernel.controller, kernel.response, etc.)**

    Inline rendering calls HttpKernel::handle(..., SUB_REQUEST), so the whole listener chain (request, controller, response) runs independently for the fragment. The sub-request has its own Request object; parent attributes are not automatically shared.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_kernel.html#handling-requests)

??? question "74. By default, can a browser hit an embedded controller's fragment URL directly?"
    **✅ No — embedded controllers are exposed to direct URLs only when fragments are enabled, and the URL is signed**

    Inline embedding uses internal sub-requests, not public URLs. Direct fragment access requires enabling framework.fragments, and Symfony signs the fragment URL (URI signer) so attackers cannot forge arbitrary controller calls. Assuming embeds are publicly routable is a security trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

??? question "75. What is the argument order of the `trans` filter?"
    **✅ (parameters, domain, locale)**

    The signature is message|trans(parameters = {}, domain = 'messages', locale = null).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html#translations-in-templates)

??? question "76. How do you pluralize a message in Symfony 8 templates?"
    **✅ Use ICU MessageFormat {count, plural, ...} in a +intl-icu domain**

    transchoice was removed; pluralization uses ICU MessageFormat, which is applied to catalogues whose domain ends with +intl-icu.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "77. A translation key has no entry for the current locale and no fallback. What is rendered?"
    **✅ The key string itself**

    The translator returns the untranslated message id when no translation is found.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

??? question "78. What replaced the removed transchoice() for count-based messages?"
    **✅ ICU MessageFormat plural syntax in a +intl-icu domain**

    Both transchoice() and the |transchoice filter were removed. Pluralization is now expressed with ICU MessageFormat ({count, plural, one{...} other{...}}) in a +intl-icu domain. trans has no separate count argument — you pass count as an ICU parameter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "79. Which catalogue file name enables ICU MessageFormat parsing for English?"
    **✅ messages+intl-icu.en.yaml**

    A domain suffixed +intl-icu (e.g. messages+intl-icu.en.yaml) is parsed with the IntlFormatter, unlocking plural/select and locale-aware formatting. Putting ICU syntax in a plain messages.en.yaml file makes the braces render literally.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "80. After {% trans_default_domain 'admin' %}, what does {{ 'dashboard.title'|trans }} use?"
    **✅ The 'admin' domain, because trans_default_domain sets it for the rest of the template**

    {% trans_default_domain 'admin' %} changes the default domain for the remainder of the template, so a trans call without an explicit domain uses 'admin'. Domains are never inferred from the key's dotted prefix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html#translations-in-templates)

??? question "81. For the ICU message '{count, plural, =0 {none} one {# item} other {# items}}', what does count=1 render?"
    **✅ 1 item**

    count=1 matches the CLDR 'one' category in English, and # inside the branch is replaced by the number, giving '1 item'. # prints the value (not a literal hash), 'one' is a category label not output, and =0 only matches the exact value 0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation/message_format.html)

??? question "82. Which service does the Twig trans filter ultimately call?"
    **✅ Symfony\Contracts\Translation\TranslatorInterface::trans() (via TranslationExtension)**

    TranslationExtension provides the trans filter/tag and delegates to TranslatorInterface::trans(), which loads catalogues, resolves the message, substitutes parameters, and runs ICU messages through the IntlFormatter.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/TranslationExtension.php)

??? question "83. Where does #{...} string interpolation work in Twig?"
    **✅ Only inside double-quoted strings**

    The lexer only interpolates #{...} within double-quoted strings; single quotes render the text literally.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)

??? question "84. What is the result of {{ 1 + 2 ~ 3 }}?"
    **✅ "33"**

    + binds tighter than ~, so (1 + 2) ~ 3 => 3 ~ 3 => the string "33".

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

??? question "85. Which filter applies sprintf-style formatting in Twig?"
    **✅ format**

    The format filter wraps vsprintf, e.g. \"%s scored %d\"|format(a, b).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/format.html)

??? question "86. Given {% set name = 'Ada' %}, what does {{ 'Hi #{name}' }} render?"
    **✅ Hi #{name} — single quotes are literal, so no interpolation happens**

    Interpolation with #{...} works only in double-quoted strings. In a single-quoted literal the sequence is printed verbatim, so you get the raw text 'Hi #{name}'. Use double quotes ("Hi #{name}") for interpolation.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)

??? question "87. What are the results of {{ "1" + "2" }} and {{ "1" ~ "2" }}?"
    **✅ 3 and "12" — + is numeric addition, ~ is string concatenation**

    In Twig, + is arithmetic addition (numeric strings are coerced), so "1" + "2" is 3. ~ concatenates after casting operands to string, so "1" ~ "2" is "12". Using + to "join" strings is a classic mistake.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

??? question "88. How does Twig implement #{...} interpolation internally?"
    **✅ It is a lexer feature: #{expr} in a double-quoted string is tokenised and compiled into ~ concatenation**

    Inside a "..." string the lexer detects #{, tokenises the embedded expression, and the parser compiles the whole literal into a ~ (string concatenation) chain — so "a #{x} b" becomes 'a ' ~ x ~ ' b'. It has nothing to do with PHP's own interpolation.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Lexer.php)

??? question "89. Which filter performs keyed placeholder substitution like {{ '%who%'|replace({'%who%': name}) }}?"
    **✅ replace**

    The replace filter takes a hash of search => replacement pairs and does keyed substitution, unlike format which uses positional sprintf placeholders. Translation strings commonly use this %name% placeholder style.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/replace.html)

??? question "90. What does asset('css/app.css') return?"
    **✅ A public URL/path (relative to public/) with base path and version applied**

    asset() resolves a path relative to public/ through the Symfony\Component\Asset\Packages service, applying base path and versioning.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-css-and-javascript-assets)

??? question "91. What is the purpose of asset versioning?"
    **✅ Cache busting so browsers refetch changed files**

    Versioning changes the URL when a file changes (static version or a JSON manifest of content hashes) so clients do not serve a stale cached copy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/frontend.html)

??? question "92. Which build tools are OUT of scope when only using asset()?"
    **✅ AssetMapper and Webpack Encore**

    asset() only resolves the final public path/version. Bundling and hashing are done by AssetMapper or Webpack Encore, which are not covered here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/asset.html)

??? question "93. Which service does the Twig asset() function delegate to?"
    **✅ Symfony\Component\Asset\Packages**

    AssetExtension wraps the Packages service. Each package pairs a base path/URL with a VersionStrategyInterface (Empty, Static, or JsonManifest), and Packages::getUrl() applies the version.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Asset/Packages.php)

??? question "94. How do you point image assets at a CDN while CSS stays local?"
    **✅ Define a named package with base_urls and call asset('img/x.png', 'cdn')**

    framework.assets.packages lets you declare a named package (e.g. cdn with base_urls). asset('img/x.png', 'cdn') uses that package while the default package still serves CSS locally. There is no framework.assets.cdn flag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/asset.html)

??? question "95. With a JSON manifest configured, what does asset('app.css') resolve to?"
    **✅ The content-hashed name looked up in manifest.json (e.g. app.7f3c.css), not the literal path**

    JsonManifestVersionStrategy maps the logical name to its hashed filename from manifest.json, so asset('app.css') returns the resolved hashed path. Expecting the literal path with a ?v query (that is StaticVersionStrategy) is the trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/asset.html)

??? question "96. True or false: you should use asset() to generate a link to a route-controlled page."
    **✅ False — asset() is for static files under public/; use path()/url() for routes**

    asset() only resolves a public file path (with base path + version); it does not know about routes. Route-controlled URLs come from path()/url() via the RoutingExtension. Swapping the two is a common confusion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-css-and-javascript-assets)

??? question "97. What does {{ dump() }} with no arguments do?"
    **✅ Dumps all variables available in the current template context**

    Called with no arguments, dump() outputs the entire render context (all passed variables plus globals).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

??? question "98. Why does dump() error in the prod environment?"
    **✅ The DumpExtension is only registered in debug mode**

    The dump function/tag come from the debug-only DumpExtension (backed by VarDumper); in prod the function is undefined, so leftover dumps throw.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

??? question "99. What is the difference between {{ dump(x) }} and {% dump x %}?"
    **✅ The function prints inline; the tag sends data to the collector without injecting markup**

    The dump() function outputs where called; the {% dump %} tag routes the data to the profiler/toolbar without adding markup to the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

??? question "100. What gives Symfony's dump() its rich, collapsible HTML output rather than plain var_dump?"
    **✅ Symfony's DumpExtension backed by VarDumper (VarCloner + HtmlDumper), replacing Twig's plain DebugExtension**

    Twig core ships DebugExtension with a plain var_dump-based dump(). Symfony augments it with DumpExtension wired to VarDumper (VarCloner clones the variable, HtmlDumper renders collapsible, syntax-highlighted output and routes dumps to the toolbar). Cloning first also makes dumping large graphs safe (depth-limited).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/DumpExtension.php)

??? question "101. You add {% dump items %} but see nothing in the page HTML. Why?"
    **✅ The tag form intentionally injects no page markup; it sends data to the collector/toolbar**

    Unlike the dump() function, the {% dump %} tag does not print inline — by design it routes the data to the dump destination (profiler/toolbar) so it does not pollute the page. Look in the web debug toolbar, not the page source.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-dump-twig-utilities)

??? question "102. A deploy fails with 'Unknown "dump" function' on a page. What is the cause and fix?"
    **✅ A stray {{ dump() }} left in a template; dump is undefined in prod, so remove it**

    dump tooling is registered only in debug mode, so a leftover dump() in a committed template throws 'Unknown "dump" function' in prod. The fix is to remove debug dumps before deploy (use logging/profiler in non-prod envs) — not to enable the extension in production.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/var_dumper.html)

??? question "103. Which of the following statements are true about Twig syntax? (select all that apply)"
    **✅ {{ }} prints (and escapes) a value, {% %} executes logic without printing, {# #} is a comment ; // performs floor division, so {{ 7 // 2 }} outputs 3 ; Filters bind tighter than arithmetic: {{ 1 + 2|abs }} is evaluated as 1 + (2|abs)**

    The three delimiters split cleanly into print/do/comment: only {{ }} produces (escaped) output while {% %} never prints. // is floor division (7 // 2 gives 3, unlike / which yields a float), and filters have higher precedence than arithmetic operators, so 1 + 2|abs applies abs to 2 first. The standalone {% spaceless %} tag no longer exists — the modern form is {% apply spaceless %}.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#twig-templating-language)

??? question "104. Which statements about Twig output escaping in Symfony are correct? (select all that apply)"
    **✅ The default escaping strategy is chosen from the template file extension, so a .txt.twig template escapes nothing ; Escaping is applied when a value is printed with {{ }}, not when it is assigned with {% set %} ; |raw and {% autoescape false %} disable protection, so they must only wrap trusted content**

    The auto-escaping context is derived from the file extension (html, js, css, url, html_attr are available), which is why a .txt.twig template gets no escaping at all — it is not a fixed html default. Escaping happens at print time via the escaper, and |raw / {% autoescape false %} switch the protection off entirely, making them XSS holes for untrusted data. The html_attr strategy is a stricter encoder than html, not an alias.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#output-escaping)

??? question "105. Which statements about Twig template inheritance are true? (select all that apply)"
    **✅ A template can extend exactly one parent, but can pull in blocks from many templates with {% use %} ; A child template that extends a parent cannot output markup outside of blocks ; parent() inside a block renders the parent template's version of that block**

    Inheritance is single and vertical: one parent per template, with blocks as the overridable holes, and any child markup outside blocks is invalid. parent() extends rather than replaces a block by rendering the parent's version. {% use %} is horizontal reuse — it imports blocks only and does not set a parent, and {% extends %} accepts a single parent, never several to combine.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#template-inheritance-and-layouts)

??? question "106. Which statements about {{ include() }} in Twig are correct? (select all that apply)"
    **✅ Without the only keyword, the included template inherits the whole context of the parent template ; With only, the local context is isolated, but the app global variable is still available ; ignore missing skips a missing template but does not swallow errors raised inside an existing template**

    By default the full parent context is merged into the include; only isolates the local variables while globals such as app remain accessible. ignore missing only prevents the error for a template that does not exist — exceptions thrown inside the included template still propagate. Overriding blocks is the job of {% embed %}, not include, and a template list renders only the first template that exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#including-templates)

??? question "107. Which statements about the app global variable are true? (select all that apply)"
    **✅ app.user is null for anonymous/unauthenticated requests, so templates must not assume it exists ; Reading app.flashes consumes the flash messages, so they are gone after being displayed ; Accessing app.session can start the session as a side effect**

    app is an AppVariable instance: app.user is null when nobody is authenticated, app.flashes consumes messages when read, and app.session starts the session on access (which can defeat HTTP caching). The distractors are wrong because app.environment is the kernel environment (dev/prod), not OS variables, and defining a local variable named app shadows the global.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#the-app-global-variable)

??? question "108. Which statements about generating URLs in Twig are correct? (select all that apply)"
    **✅ path() generates a relative URL while url() generates an absolute URL, both from route names ; Parameters that are not part of the route definition are appended to the URL as a query string ; Using an unknown route name throws a RouteNotFoundException when the template is rendered**

    path() and url() both take a route name (plus parameters): path() yields a relative URL, url() an absolute one, and any parameter the route does not declare ends up in the query string rather than being dropped. An unknown route name fails at render time with RouteNotFoundException. Email bodies, canonical links and feeds leave the page context, so they need url() — relative links from path() break in mail clients.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/templates.html#linking-to-pages)

??? question "109. Which statements about translations in Twig are correct? (select all that apply)"
    **✅ The trans filter arguments are ordered (parameters, domain, locale) ; A missing translation key does not throw; the key string itself is returned ; ICU MessageFormat pluralization is only parsed for catalogues in domains with the +intl-icu suffix**

    The trans filter signature is message|trans(parameters, domain, locale) — passing the domain first is a classic mistake. Missing keys fall back to returning the key itself instead of erroring, and ICU {n, plural, ...} syntax is only interpreted for domains suffixed with +intl-icu. The transchoice filter was removed; ICU MessageFormat is the modern way to pluralize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

---

<small>Back to [Flashcards](index.md) · [Templating (Twig)](../../twig/index.md)</small>
