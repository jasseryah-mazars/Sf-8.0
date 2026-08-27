# Chapter Exam — Templating (Twig)

!!! abstract "How to use"
    109 questions spanning every subchapter of **Templating (Twig)**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Templating (Twig)](../twig/index.md).

---

**Q1.** Which Twig delimiter executes a statement without printing anything?  <small>_(easy · single)_</small>

- A. {% ... %}
- B. {{ ... }}
- C. {# ... #}
- D. #{ ... }

??? success "Answer Q1"
    **A**

    {% %} runs tags/control flow, {{ }} prints an (escaped) expression, and {# #} is a comment that is stripped at compile time.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

**Q2.** What does {{ 7 // 2 }} output in Twig?  <small>_(easy · code)_</small>

- A. 3
- B. 3.5
- C. 4
- D. An error

??? success "Answer Q2"
    **A**

    // is integer (floor) division in Twig; / performs float division and would return 3.5.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#math)

**Q3.** True or false: {# ... #} comments are removed at compile time and never reach the browser.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q3"
    **A**

    Twig {# #} comments are stripped during compilation and produce no output, unlike HTML <!-- --> comments which are sent to the client. Use {# #} for template notes you do not want leaking to users.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#twig-language-references)

**Q4.** A value is placed inside <script>const x = "...";</script>. Which escape filter is correct?  <small>_(easy · single)_</small>

- A. |e('js')
- B. |e('html')
- C. |e('html_attr')
- D. |raw

??? success "Answer Q4"
    **A**

    A JavaScript string context requires the 'js' strategy; HTML escaping does not neutralise the characters dangerous in JS.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

**Q5.** What does {% autoescape false %} ... {% endautoescape %} do?  <small>_(easy · single)_</small>

- A. Disables auto-escaping inside the block (use for trusted content only)
- B. Escapes the content as plain text
- C. Escapes the content as a URL
- D. Throws an exception

??? success "Answer Q5"
    **A**

    It turns escaping off within the block, exactly like piping every value through |raw. Only use it for trusted/sanitised content.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/autoescape.html)

**Q6.** Which escaping filter is required for a value used inside an HTML attribute?  <small>_(easy · single)_</small>

- A. |e('html_attr')
- B. |e('html')
- C. |e('url')
- D. |e('css')

??? success "Answer Q6"
    **A**

    Attribute context needs the stricter html_attr encoder, which escapes spaces, =, backticks and other characters that html escaping leaves untouched.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

**Q7.** In a .html.twig file, what does {{ '<b>hi</b>' }} render to the browser?  <small>_(easy · code)_</small>

- A. &lt;b&gt;hi&lt;/b&gt; (escaped, shown as literal text)
- B. Bold text 'hi'
- C. An empty string
- D. A RuntimeError

??? success "Answer Q7"
    **A**

    Auto-escaping (html strategy for .html.twig) converts the angle brackets to entities, so the literal markup is displayed as text rather than rendered as bold. To output real markup you would need |raw (only for trusted content).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q8.** True or false: in Symfony, Twig output escaping is enabled by default.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q8"
    **A**

    Auto-escaping is on by default (autoescape: name) as a baseline XSS defence; every {{ }} is escaped for its context unless the value is marked safe or passed through |raw. You opt out per value, not opt in.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q9.** How many templates can a single template extend in Twig?  <small>_(easy · single)_</small>

- A. Exactly one
- B. Up to three
- C. Unlimited
- D. Zero

??? success "Answer Q9"
    **A**

    Twig uses single vertical inheritance. For reusing blocks from several templates (horizontal reuse), use the {% use %} tag instead.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

**Q10.** Inside an overridden block, what does {{ parent() }} render?  <small>_(easy · single)_</small>

- A. The parent template's version of that same block
- B. The entire parent template
- C. The parent controller's output
- D. Nothing

??? success "Answer Q10"
    **A**

    parent() outputs the content of the same block from the parent template, letting a child extend rather than fully replace it.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/parent.html)

**Q11.** Which tag provides horizontal reuse of blocks (like a trait)?  <small>_(easy · single)_</small>

- A. {% use %}
- B. {% extends %}
- C. {% include %}
- D. {% embed %}

??? success "Answer Q11"
    **A**

    {% use %} imports block definitions from another template without setting a parent, and multiple use statements are allowed.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/use.html)

**Q12.** What does app.environment return?  <small>_(easy · single)_</small>

- A. The kernel environment string, e.g. 'dev' or 'prod'
- B. The operating-system environment variables
- C. The APP_ENV file path
- D. A boolean debug flag

??? success "Answer Q12"
    **A**

    app.environment is the kernel environment (dev/prod/test); app.debug is the boolean debug flag. They are unrelated to OS env vars.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q13.** Which snippet safely greets an authenticated user and falls back to 'Guest'?  <small>_(easy · code)_</small>

- A. {{ app.user ? app.user.userIdentifier : 'Guest' }}
- B. {{ app.user.userIdentifier }}
- C. {{ app.user.userIdentifier ?? Guest }}
- D. {{ app.userIdentifier|default('Guest') }}

??? success "Answer Q13"
    **A**

    Because app.user is null for anonymous requests, you must guard it before dereferencing. The ternary checks app.user first. Reading app.user.userIdentifier directly throws under strict_variables (and is the classic anonymous-page crash); Guest is a bareword not a string in the third option; app.userIdentifier is not a member.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q14.** Which attribute registers a custom Twig filter in Twig up to 3.22?  <small>_(easy · single)_</small>

- A. #[AsTwigFilter]
- B. #[TwigFilter]
- C. #[AsFilter]
- D. #[Filter]

??? success "Answer Q14"
    **A**

    Twig 3.x provides Twig\Attribute\AsTwigFilter and AsTwigFunction as an attribute-based alternative to returning TwigFilter/TwigFunction from an AbstractExtension.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#creating-a-twig-extension)

**Q15.** What does the `default` filter replace?  <small>_(easy · single)_</small>

- A. Undefined, null AND empty values
- B. Only undefined variables
- C. Only null values
- D. Only empty strings

??? success "Answer Q15"
    **A**

    default(x) substitutes x when the value is undefined, null or empty (unless you pass true as the second argument to only test 'defined').

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/default.html)

**Q16.** What does the `only` keyword do on an include?  <small>_(easy · single)_</small>

- A. Restricts the included template's scope to just the `with` variables
- B. Includes the template only once
- C. Makes the variables read-only
- D. Ignores a missing template

??? success "Answer Q16"
    **A**

    By default an include inherits the parent context; adding `only` isolates it so it sees only the variables passed via `with` (plus the app global).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q17.** Which construct includes a template AND lets you override its blocks?  <small>_(easy · single)_</small>

- A. {% embed %}
- B. {% include %}
- C. {% use %}
- D. {% extends %}

??? success "Answer Q17"
    **A**

    embed combines include with extends-style block overriding, ideal for configurable components with slots.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/embed.html)

**Q18.** What does {% include ['a.html.twig', 'b.html.twig'] %} render?  <small>_(easy · single)_</small>

- A. The first template in the list that exists
- B. Both templates concatenated
- C. The last template
- D. An error

??? success "Answer Q18"
    **A**

    Passing an array of names renders the first template that can be loaded, which is handy for theme overrides.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q19.** What is loop.index on the first iteration of a for loop?  <small>_(easy · single)_</small>

- A. 1
- B. 0
- C. null
- D. -1

??? success "Answer Q19"
    **A**

    loop.index is 1-based; loop.index0 is the 0-based counterpart.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

**Q20.** When does the `else` clause of a for loop execute?  <small>_(easy · single)_</small>

- A. When the collection is empty (zero iterations)
- B. On the last item
- C. On every iteration
- D. When an error occurs

??? success "Answer Q20"
    **A**

    {% for ... else ... endfor %} renders the else block only when the loop produced no iterations.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-else-clause)

**Q21.** Which loop iterates a hash by key and value?  <small>_(easy · code)_</small>

- A. {% for key, value in map %}
- B. {% for value, key in map %} always
- C. {% foreach key => value in map %}
- D. {% for map as key, value %}

??? success "Answer Q21"
    **A**

    Twig's key/value form is {% for key, value in map %} (key first). There is no foreach tag and no PHP-style => or 'as' syntax in Twig loops.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

**Q22.** True or false: Twig provides a {% break %} tag to exit a loop early.  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q22"
    **A**

    Twig deliberately has no break or continue tag to keep templates declarative. Filter the iterable (for x in items if ...) or slice it (items|slice(0, n)) to limit iterations instead.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

**Q23.** What is the difference between path() and url() in Twig?  <small>_(easy · single)_</small>

- A. path() returns a relative URL, url() returns an absolute URL
- B. url() is relative, path() is absolute
- C. They are identical
- D. path() only works inside controllers

??? success "Answer Q23"
    **A**

    Both use UrlGeneratorInterface via RoutingExtension; path() uses ABSOLUTE_PATH (relative) and url() uses ABSOLUTE_URL (scheme + host).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#linking-to-pages)

**Q24.** A translation key has no entry for the current locale and no fallback. What is rendered?  <small>_(easy · single)_</small>

- A. The key string itself
- B. An empty string
- C. A 500 error
- D. null

??? success "Answer Q24"
    **A**

    The translator returns the untranslated message id when no translation is found.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html)

**Q25.** Where does #{...} string interpolation work in Twig?  <small>_(easy · single)_</small>

- A. Only inside double-quoted strings
- B. Inside any string literal
- C. Only inside single-quoted strings
- D. Only inside {% %} tags

??? success "Answer Q25"
    **A**

    The lexer only interpolates #{...} within double-quoted strings; single quotes render the text literally.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)

**Q26.** Which filter applies sprintf-style formatting in Twig?  <small>_(easy · single)_</small>

- A. format
- B. sprintf
- C. printf
- D. interpolate

??? success "Answer Q26"
    **A**

    The format filter wraps vsprintf, e.g. \"%s scored %d\"|format(a, b).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/format.html)

**Q27.** Which filter performs keyed placeholder substitution like {{ '%who%'|replace({'%who%': name}) }}?  <small>_(easy · single)_</small>

- A. replace
- B. format
- C. substitute
- D. translate

??? success "Answer Q27"
    **A**

    The replace filter takes a hash of search => replacement pairs and does keyed substitution, unlike format which uses positional sprintf placeholders. Translation strings commonly use this %name% placeholder style.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/replace.html)

**Q28.** What does asset('css/app.css') return?  <small>_(easy · single)_</small>

- A. A public URL/path (relative to public/) with base path and version applied
- B. A route-generated URL
- C. The file's contents
- D. An absolute filesystem path

??? success "Answer Q28"
    **A**

    asset() resolves a path relative to public/ through the Symfony\Component\Asset\Packages service, applying base path and versioning.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#linking-to-css-and-javascript-assets)

**Q29.** What is the purpose of asset versioning?  <small>_(easy · single)_</small>

- A. Cache busting so browsers refetch changed files
- B. Access control for static files
- C. Minifying assets
- D. Matching routes

??? success "Answer Q29"
    **A**

    Versioning changes the URL when a file changes (static version or a JSON manifest of content hashes) so clients do not serve a stale cached copy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/frontend.html)

**Q30.** Which build tools are OUT of scope when only using asset()?  <small>_(easy · trap)_</small>

- A. AssetMapper and Webpack Encore
- B. The Routing component
- C. The Translation component
- D. The Twig EscaperExtension

??? success "Answer Q30"
    **A**

    asset() only resolves the final public path/version. Bundling and hashing are done by AssetMapper or Webpack Encore, which are not covered here.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/asset.html)

**Q31.** What does {{ dump() }} with no arguments do?  <small>_(easy · single)_</small>

- A. Dumps all variables available in the current template context
- B. Dumps nothing
- C. Throws an exception
- D. Dumps only the app global

??? success "Answer Q31"
    **A**

    Called with no arguments, dump() outputs the entire render context (all passed variables plus globals).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-dump-twig-utilities)

**Q32.** What is the result of {{ "a" ~ 1 + 1 }}?  <small>_(medium · code)_</small>

- A. "a2"
- B. "a11"
- C. 2
- D. An error

??? success "Answer Q32"
    **A**

    + binds tighter than ~, so it evaluates as "a" ~ (1 + 1) => "a" ~ 2 => "a2". ~ is string concatenation, not addition.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

**Q33.** How do you strip whitespace between HTML tags in Twig up to 3.22?  <small>_(medium · trap)_</small>

- A. {% apply spaceless %}...{% endapply %}
- B. {% spaceless %}...{% endspaceless %}
- C. {{ strip }}
- D. {% trim %}...{% endtrim %}

??? success "Answer Q33"
    **A**

    The {% spaceless %} tag was removed in Twig 3; use the spaceless filter via {% apply spaceless %} (or the {{- -}} whitespace modifiers).

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/spaceless.html)

**Q34.** How is a Twig template turned into something executable, and what is cached?  <small>_(medium · internals)_</small>

- A. It is lexed, parsed and compiled to a PHP class extending Twig\Template, cached under var/cache
- B. It is interpreted line by line on every request, nothing is cached
- C. It is transpiled to JavaScript and cached in the browser
- D. It is stored as a serialized AST and re-parsed each request

??? success "Answer Q34"
    **A**

    Twig is a compiler: Environment::render() runs lex -> parse -> compile, emitting a PHP class extending Twig\Template whose doDisplay() contains echo statements. It is written once to var/cache/<env>/twig via FilesystemCache and reused, so runtime parsing cost is zero after the first compile.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/api.html)

**Q35.** With strict_variables enabled, what happens when you print an undefined variable {{ missing }}?  <small>_(medium · trap)_</small>

- A. It throws a RuntimeError; without strict_variables it would silently print empty
- B. It always prints the string 'null'
- C. It prints empty regardless of strict_variables
- D. It throws only in the prod environment

??? success "Answer Q35"
    **A**

    With strict_variables on (recommended in dev), an undefined variable throws so typos surface early. In lenient mode (the default) it prints an empty string. Note a variable that resolves to null still prints empty even under strict_variables — strict_variables catches undefined, not null.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/api.html#environment-options)

**Q36.** In Symfony, how is the default auto-escaping strategy chosen for a template?  <small>_(medium · internals)_</small>

- A. Guessed from the template file extension (e.g. .html.twig => html)
- B. It is always 'html'
- C. From the HTTP Accept header
- D. Auto-escaping is disabled by default

??? success "Answer Q36"
    **A**

    TwigBundle configures autoescape to 'name', using FileExtensionEscapingStrategy::guess() so .html.twig escapes as html, .js.twig as js, .txt.twig not at all.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q37.** How much of a .txt.twig template's {{ }} output is auto-escaped by Symfony's default strategy?  <small>_(medium · trap)_</small>

- A. None — the .txt.twig extension maps to no escaping (false)
- B. All values are html-escaped like any other template
- C. Values are escaped as URLs
- D. Twig throws because .txt.twig has no strategy

??? success "Answer Q37"
    **A**

    FileExtensionEscapingStrategy::guess() maps .txt.twig to false (no escaping), which is correct because plain-text output has no HTML context. The trap is assuming escaping is always html — it is chosen per extension, and .txt.twig escapes nothing.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q38.** A template renders user-submitted comment HTML with {{ comment|raw }}. What is the risk?  <small>_(medium · trap)_</small>

- A. Stored XSS: |raw disables escaping, so untrusted markup/scripts run unfiltered
- B. Nothing — |raw still escapes script tags
- C. It only affects performance, not security
- D. Twig sanitizes |raw output automatically in prod

??? success "Answer Q38"
    **A**

    |raw marks the value safe and skips auto-escaping, so any <script> in a user comment executes — a classic stored XSS hole. Only use |raw on HTML you generated or ran through the HtmlSanitizer component; never on raw user input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/html_sanitizer.html)

**Q39.** What is the difference between {{ parent() }} and {{ block('sidebar') }}?  <small>_(medium · trap)_</small>

- A. parent() renders the parent's version of the current block; block('x') renders block x of the current hierarchy
- B. They are aliases and do the same thing
- C. parent() renders any named block; block('x') renders the whole parent template
- D. block('x') only works in the parent template, parent() only in the child

??? success "Answer Q39"
    **A**

    parent() is contextual — it renders the same block one level up in the inheritance chain. block('name') prints a named block resolved from the current template hierarchy (and block('name', 'other.html.twig') from another template). Confusing the two is a common exam distractor.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/block.html)

**Q40.** What does {% extends request.isXmlHttpRequest ? '_ajax.html.twig' : 'base.html.twig' %} demonstrate?  <small>_(medium · code)_</small>

- A. extends accepts a dynamic expression, resolved at runtime to choose the parent
- B. A syntax error — extends only accepts a string literal
- C. It extends both templates at once
- D. It includes the ajax template rather than extending it

??? success "Answer Q40"
    **A**

    The parent name in extends can be any expression, evaluated at runtime, so you can pick a layout conditionally (e.g. a bare layout for AJAX requests). This is why extends is resolved at runtime rather than purely at compile time.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

**Q41.** Which statements about {% use %} are correct? (choose 2)  <small>_(medium · multiple)_</small>

- A. It imports block definitions only, not surrounding markup
- B. Multiple use statements are allowed in one template
- C. It sets the template's parent like extends
- D. It can override the parent's <html> skeleton

??? success "Answer Q41"
    **A, B**

    {% use %} performs horizontal reuse: it pulls in block definitions (like a PHP trait) without setting a parent, and you may use several templates, aliasing name clashes with 'as'. It does not import non-block markup and does not establish inheritance — that is what extends is for.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/use.html)

**Q42.** What does app.user return when no one is authenticated?  <small>_(medium · single)_</small>

- A. null
- B. An empty User object
- C. The string 'anonymous'
- D. It throws an exception

??? success "Answer Q42"
    **A**

    AppVariable::getUser() reads the token from the token storage and returns its user, or null when there is no authenticated user.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q43.** Which class backs the Twig `app` global in Symfony?  <small>_(medium · internals)_</small>

- A. Symfony\Bridge\Twig\AppVariable
- B. Symfony\Component\HttpFoundation\Request
- C. Twig\Environment
- D. Symfony\Component\HttpKernel\Kernel

??? success "Answer Q43"
    **A**

    TwigBundle registers Symfony\Bridge\Twig\AppVariable as the `app` global; its getters expose user, request, session, flashes, etc.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/AppVariable.php)

**Q44.** Which of these is NOT a member of the `app` global?  <small>_(medium · trap)_</small>

- A. app.controller
- B. app.request
- C. app.environment
- D. app.flashes

??? success "Answer Q44"
    **A**

    app exposes user, request, session, flashes, environment, debug, token, locale, current_route and current_route_parameters. There is no app.controller.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q45.** How do you register a static global string in Twig?  <small>_(medium · config)_</small>

- A. Under twig.globals in config, or via a GlobalsInterface extension
- B. With a #[AsGlobal] attribute
- C. With {% global x = 'y' %}
- D. It cannot be done

??? success "Answer Q45"
    **A**

    Declare globals under twig.globals in twig.yaml, or return them from an extension implementing Twig\Extension\GlobalsInterface::getGlobals().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#global-variables)

**Q46.** In Symfony 8, which expression prints the current user's identifier?  <small>_(medium · trap)_</small>

- A. {{ app.user.userIdentifier }}
- B. {{ app.user.username }}
- C. {{ app.username }}
- D. {{ app.user.getUsername }}

??? success "Answer Q46"
    **A**

    UserInterface exposes getUserIdentifier(), so the Twig accessor is app.user.userIdentifier. The legacy getUsername()/username idiom is gone in modern Symfony. Remember to guard app.user first — it is null for anonymous requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/security.html#the-user)

**Q47.** A custom filter returns '<b>x</b>' but the page shows escaped text. Why?  <small>_(medium · debug)_</small>

- A. The filter must be declared with the is_safe => ['html'] option
- B. Twig never escapes filter output
- C. You must call |raw on the input
- D. It is a Twig bug

??? success "Answer Q47"
    **A**

    Filter/function output is auto-escaped unless the TwigFilter/TwigFunction declares is_safe for the relevant context.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

**Q48.** Which statement about filters vs functions is correct?  <small>_(medium · trap)_</small>

- A. A filter is applied with the pipe (value|f) and a function is called by name f(args); date exists as both
- B. Filters and functions are interchangeable syntaxes for the same registration
- C. Only functions can take arguments
- D. path() is a filter and lower is a function

??? success "Answer Q48"
    **A**

    value|filter transforms a piped value while function(args) is called by name; they are registered as distinct TwigFilter/TwigFunction objects. A name like date is registered both as a filter (now|date('Y')) and a function (date()). path()/lower are function and filter respectively — the reversed option is wrong.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#filters)

**Q49.** Which method definition correctly registers a `vat` function via attributes?  <small>_(medium · code)_</small>

- A. #[AsTwigFunction('vat')] public function vat(float $n, float $rate = 0.20): float
- B. #[TwigFunction('vat')] public function vat(float $n): float
- C. #[AsFunction('vat')] public function vat(float $n): float
- D. public function vat(float $n): float // auto-detected by name

??? success "Answer Q49"
    **A**

    Twig\Attribute\AsTwigFunction('vat') on a method registers the function; Symfony autoconfiguration wires the class. There is no #[TwigFunction] or #[AsFunction] attribute, and functions are not auto-detected by method name without an attribute or getFunctions() registration.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#creating-a-twig-extension)

**Q50.** Why put a filter's heavy-dependency logic in a runtime class rather than the extension itself?  <small>_(medium · internals)_</small>

- A. The runtime is lazily instantiated only when the filter is actually used, so heavy services are not built every request
- B. Runtimes are the only way to register a filter in Twig 3
- C. Extensions cannot have a constructor
- D. Runtime classes bypass auto-escaping

??? success "Answer Q50"
    **A**

    An AbstractExtension is instantiated on every request, so injecting a costly dependency into it slows all requests. Moving the logic to a runtime (RuntimeExtensionInterface / the attribute style) makes it lazy — built only when the filter is invoked. Auto-escaping is unaffected by this choice.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#lazy-loading-nodes)

**Q51.** Given an empty string, what do {{ ''|default('x') }} and {{ '' ?? 'x' }} produce?  <small>_(medium · code)_</small>

- A. 'x' and '' — default replaces empty values, ?? only replaces null/undefined
- B. 'x' and 'x' — both replace empty strings
- C. '' and '' — neither treats empty as replaceable
- D. '' and 'x' — default keeps empty, ?? replaces it

??? success "Answer Q51"
    **A**

    The default filter substitutes for undefined, null AND empty values ('', [], false), so ''|default('x') yields 'x'. The ?? operator only replaces null/undefined, so '' ?? 'x' keeps the empty string. This difference is a frequent exam trap.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/default.html)

**Q52.** A template exists but throws inside itself. Does `ignore missing` on the include suppress that error?  <small>_(medium · trap)_</small>

- A. No — ignore missing only suppresses LoaderError for a missing template, not errors thrown while rendering an existing one
- B. Yes — ignore missing swallows any error inside the include
- C. Yes, but only in prod
- D. It converts the error into an empty string always

??? success "Answer Q52"
    **A**

    ignore missing guards only against the template not being found (LoaderError). Once a template is loaded, any runtime/compile error inside it still propagates. Treating ignore missing as a catch-all is a trap that hides real bugs.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q53.** What does {{ include('_card.html.twig', { title: t }, with_context = false) }} do?  <small>_(medium · code)_</small>

- A. Renders the partial with only { title: t } (no parent context) and returns it as a string usable in an expression
- B. Includes the template inline but keeps the full parent context
- C. Throws because the function form does not accept with_context
- D. Renders it only if the template is missing

??? success "Answer Q53"
    **A**

    The include() function returns a string (so it composes in expressions) and takes named options; with_context = false is the function-form equivalent of the only keyword, isolating the partial to the passed variables. Globals remain available.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/functions/include.html)

**Q54.** How do you skip iterations in a Twig for loop?  <small>_(medium · trap)_</small>

- A. Filter the source, e.g. {% for x in items if x.active %}
- B. Use {% continue %}
- C. Use {% break %}
- D. Call loop.skip()

??? success "Answer Q54"
    **A**

    Twig has no break/continue by design; filter the iterable inline or use an if inside the body.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html)

**Q55.** Inside a nested loop, how do you access the outer loop's current index?  <small>_(medium · code)_</small>

- A. loop.parent.loop.index
- B. loop.outer.index
- C. parent.loop.index
- D. loop.index.parent

??? success "Answer Q55"
    **A**

    loop.parent gives the enclosing loop's context, so loop.parent.loop.index is the outer loop's 1-based index. A bare loop.index inside the inner loop refers to the inner loop only.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

**Q56.** What happens with {% for x in items %}...{% else %}Empty{% endfor %} when items is null?  <small>_(medium · code)_</small>

- A. Zero iterations run and the else block renders 'Empty' (no error in lenient mode)
- B. A RuntimeError because you cannot iterate null
- C. The loop body runs once with x = null
- D. Nothing at all is rendered

??? success "Answer Q56"
    **A**

    Iterating null in lenient mode is safe — it produces zero iterations and falls through to the for...else block. That makes for...else the natural guard for a possibly-null collection, so you rarely need a wrapping {% if items %}.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-else-clause)

**Q57.** Given route 'search' => /search, what does path('search', {q: 'x', page: 2}) produce?  <small>_(medium · code)_</small>

- A. /search?q=x&page=2
- B. /search/x/2
- C. /search (extra params are dropped)
- D. An error

??? success "Answer Q57"
    **A**

    Parameters not consumed by the route pattern are appended as the query string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q58.** Which Twig extension provides path() and url()?  <small>_(medium · internals)_</small>

- A. Symfony\Bridge\Twig\Extension\RoutingExtension
- B. Twig\Extension\CoreExtension
- C. Symfony\Bridge\Twig\Extension\AssetExtension
- D. Symfony\Bridge\Twig\Extension\HttpKernelExtension

??? success "Answer Q58"
    **A**

    RoutingExtension wraps the UrlGeneratorInterface and reads the RequestContext to build relative and absolute URLs.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

**Q59.** You are building an HTML email template with a link back to the site. Which function should you use?  <small>_(medium · scenario)_</small>

- A. url() — an email needs an absolute URL (scheme + host); path() yields a relative link that breaks in mail clients
- B. path() — it is shorter and mail clients resolve it against the site
- C. asset() — it produces the right host for emails
- D. Either works identically in an email

??? success "Answer Q59"
    **A**

    When a link leaves the page (emails, RSS, canonical tags, redirects consumed elsewhere) it must be absolute, so use url(). A relative path() link has no host and breaks once opened in a mail client. asset() is for static files, not routes.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#linking-to-pages)

**Q60.** path('article_show') is called but the route requires a {slug}. What happens at render time?  <small>_(medium · debug)_</small>

- A. A MissingMandatoryParametersException is thrown
- B. The slug defaults to an empty string and the URL renders
- C. The link is silently omitted
- D. It returns /article_show as a literal

??? success "Answer Q60"
    **A**

    The generator throws MissingMandatoryParametersException when a required route parameter is not supplied. (An unknown route name instead throws RouteNotFoundException.) Both surface at render time, not silently.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html#generating-urls)

**Q61.** How does render(controller('C::m')) execute the controller?  <small>_(medium · single)_</small>

- A. As a sub-request through HttpKernel (inline fragment)
- B. As a plain static method call with no request
- C. As an HTTP redirect
- D. As a console command

??? success "Answer Q61"
    **A**

    The InlineFragmentRenderer issues a real HttpKernel sub-request, so the kernel events run again for the fragment.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#embedding-controllers)

**Q62.** A sidebar just needs variables the parent already has. include or render(controller())?  <small>_(medium · scenario)_</small>

- A. include — it is the cheapest option when no extra logic/data is needed
- B. render(controller()) — always prefer embedding controllers
- C. render_esi — fragments should always be cached separately
- D. render_hinclude — load everything asynchronously by default

??? success "Answer Q62"
    **A**

    Each inline embed is a real sub-request with its own overhead. If the fragment only needs data you already have, a plain include is far cheaper. Reserve render(controller()) for fragments that need their own services/data/cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#embedding-controllers)

**Q63.** What does render_hinclude() do differently from inline rendering?  <small>_(medium · single)_</small>

- A. It emits a placeholder that the browser resolves asynchronously via JavaScript
- B. It renders the fragment inline but caches it in the profiler
- C. It always requires a reverse proxy
- D. It renders nothing until the page reloads

??? success "Answer Q63"
    **A**

    HIncludeFragmentRenderer outputs a placeholder tag resolved by the browser with JavaScript, so the main page renders immediately and the fragment loads asynchronously afterwards. Inline instead blocks on a synchronous sub-request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

**Q64.** What is the argument order of the `trans` filter?  <small>_(medium · single)_</small>

- A. (parameters, domain, locale)
- B. (domain, parameters, locale)
- C. (locale, domain, parameters)
- D. (parameters, locale, domain)

??? success "Answer Q64"
    **A**

    The signature is message|trans(parameters = {}, domain = 'messages', locale = null).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html#translations-in-templates)

**Q65.** How do you pluralize a message in Symfony 8 templates?  <small>_(medium · trap)_</small>

- A. Use ICU MessageFormat {count, plural, ...} in a +intl-icu domain
- B. Use the removed transchoice() function
- C. Use the |plural filter
- D. Use a {% pluralize %} tag

??? success "Answer Q65"
    **A**

    transchoice was removed; pluralization uses ICU MessageFormat, which is applied to catalogues whose domain ends with +intl-icu.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation/message_format.html)

**Q66.** What replaced the removed transchoice() for count-based messages?  <small>_(medium · trap)_</small>

- A. ICU MessageFormat plural syntax in a +intl-icu domain
- B. The |transchoice filter, which is still available
- C. The trans filter's fourth 'count' argument
- D. A dedicated Pluralizer service you call in the controller

??? success "Answer Q66"
    **A**

    Both transchoice() and the |transchoice filter were removed. Pluralization is now expressed with ICU MessageFormat ({count, plural, one{...} other{...}}) in a +intl-icu domain. trans has no separate count argument — you pass count as an ICU parameter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation/message_format.html)

**Q67.** After {% trans_default_domain 'admin' %}, what does {{ 'dashboard.title'|trans }} use?  <small>_(medium · code)_</small>

- A. The 'admin' domain, because trans_default_domain sets it for the rest of the template
- B. The 'messages' domain, since the filter did not name one
- C. It errors because a domain is required
- D. The 'dashboard' domain, inferred from the key prefix

??? success "Answer Q67"
    **A**

    {% trans_default_domain 'admin' %} changes the default domain for the remainder of the template, so a trans call without an explicit domain uses 'admin'. Domains are never inferred from the key's dotted prefix.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html#translations-in-templates)

**Q68.** What is the result of {{ 1 + 2 ~ 3 }}?  <small>_(medium · code)_</small>

- A. "33"
- B. "123"
- C. 6
- D. "15"

??? success "Answer Q68"
    **A**

    + binds tighter than ~, so (1 + 2) ~ 3 => 3 ~ 3 => the string "33".

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

**Q69.** Given {% set name = 'Ada' %}, what does {{ 'Hi #{name}' }} render?  <small>_(medium · trap)_</small>

- A. Hi #{name} — single quotes are literal, so no interpolation happens
- B. Hi Ada — interpolation works in any string
- C. An error about #{ in a single-quoted string
- D. Hi  — the #{name} is stripped

??? success "Answer Q69"
    **A**

    Interpolation with #{...} works only in double-quoted strings. In a single-quoted literal the sequence is printed verbatim, so you get the raw text 'Hi #{name}'. Use double quotes ("Hi #{name}") for interpolation.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#string-interpolation)

**Q70.** What are the results of {{ "1" + "2" }} and {{ "1" ~ "2" }}?  <small>_(medium · code)_</small>

- A. 3 and "12" — + is numeric addition, ~ is string concatenation
- B. "12" and "12" — both concatenate
- C. 3 and 3 — both add numerically
- D. An error, because + cannot be used on strings

??? success "Answer Q70"
    **A**

    In Twig, + is arithmetic addition (numeric strings are coerced), so "1" + "2" is 3. ~ concatenates after casting operands to string, so "1" ~ "2" is "12". Using + to "join" strings is a classic mistake.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#other-operators)

**Q71.** Which service does the Twig asset() function delegate to?  <small>_(medium · internals)_</small>

- A. Symfony\Component\Asset\Packages
- B. Symfony\Component\Routing\Generator\UrlGenerator
- C. Symfony\Contracts\Translation\TranslatorInterface
- D. Symfony\Component\HttpKernel\Fragment\FragmentHandler

??? success "Answer Q71"
    **A**

    AssetExtension wraps the Packages service. Each package pairs a base path/URL with a VersionStrategyInterface (Empty, Static, or JsonManifest), and Packages::getUrl() applies the version.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Asset/Packages.php)

**Q72.** How do you point image assets at a CDN while CSS stays local?  <small>_(medium · config)_</small>

- A. Define a named package with base_urls and call asset('img/x.png', 'cdn')
- B. Hard-code the CDN URL in the template
- C. Use url('cdn', {path: 'img/x.png'})
- D. Set framework.assets.cdn: true

??? success "Answer Q72"
    **A**

    framework.assets.packages lets you declare a named package (e.g. cdn with base_urls). asset('img/x.png', 'cdn') uses that package while the default package still serves CSS locally. There is no framework.assets.cdn flag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/asset.html)

**Q73.** True or false: you should use asset() to generate a link to a route-controlled page.  <small>_(medium · trap)_</small>

- A. False — asset() is for static files under public/; use path()/url() for routes
- B. True — asset() works for both routes and files

??? success "Answer Q73"
    **A**

    asset() only resolves a public file path (with base path + version); it does not know about routes. Route-controlled URLs come from path()/url() via the RoutingExtension. Swapping the two is a common confusion.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#linking-to-css-and-javascript-assets)

**Q74.** Why does dump() error in the prod environment?  <small>_(medium · debug)_</small>

- A. The DumpExtension is only registered in debug mode
- B. It is a syntax error
- C. VarDumper is never installed
- D. It has been deprecated

??? success "Answer Q74"
    **A**

    The dump function/tag come from the debug-only DumpExtension (backed by VarDumper); in prod the function is undefined, so leftover dumps throw.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/var_dumper.html)

**Q75.** What is the difference between {{ dump(x) }} and {% dump x %}?  <small>_(medium · single)_</small>

- A. The function prints inline; the tag sends data to the collector without injecting markup
- B. They are identical
- C. The tag works in prod, the function does not
- D. The function only works in prod

??? success "Answer Q75"
    **A**

    The dump() function outputs where called; the {% dump %} tag routes the data to the profiler/toolbar without adding markup to the page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-dump-twig-utilities)

**Q76.** You add {% dump items %} but see nothing in the page HTML. Why?  <small>_(medium · trap)_</small>

- A. The tag form intentionally injects no page markup; it sends data to the collector/toolbar
- B. The tag only works in prod
- C. items must be a scalar for {% dump %} to work
- D. {% dump %} was removed; only dump() exists

??? success "Answer Q76"
    **A**

    Unlike the dump() function, the {% dump %} tag does not print inline — by design it routes the data to the dump destination (profiler/toolbar) so it does not pollute the page. Look in the web debug toolbar, not the page source.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-dump-twig-utilities)

**Q77.** A deploy fails with 'Unknown "dump" function' on a page. What is the cause and fix?  <small>_(medium · debug)_</small>

- A. A stray {{ dump() }} left in a template; dump is undefined in prod, so remove it
- B. VarDumper is missing from require-dev; move it to require
- C. The Twig cache is stale; clear it and dump will work in prod
- D. dump was renamed in Symfony 8; use var_dump instead

??? success "Answer Q77"
    **A**

    dump tooling is registered only in debug mode, so a leftover dump() in a committed template throws 'Unknown "dump" function' in prod. The fix is to remove debug dumps before deploy (use logging/profiler in non-prod envs) — not to enable the extension in production.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/var_dumper.html)

**Q78.** Which of the following statements are true about Twig syntax? (select all that apply)  <small>_(medium · multiple)_</small>

- A. {{ }} prints (and escapes) a value, {% %} executes logic without printing, {# #} is a comment
- B. // performs floor division, so {{ 7 // 2 }} outputs 3
- C. Filters bind tighter than arithmetic: {{ 1 + 2|abs }} is evaluated as 1 + (2|abs)
- D. {% %} statements also print their result into the output
- E. {% spaceless %} is still the recommended tag for stripping whitespace

??? success "Answer Q78"
    **A, B, C**

    The three delimiters split cleanly into print/do/comment: only {{ }} produces (escaped) output while {% %} never prints. // is floor division (7 // 2 gives 3, unlike / which yields a float), and filters have higher precedence than arithmetic operators, so 1 + 2|abs applies abs to 2 first. The standalone {% spaceless %} tag no longer exists — the modern form is {% apply spaceless %}.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#twig-templating-language)

**Q79.** Which statements about Twig template inheritance are true? (select all that apply)  <small>_(medium · multiple)_</small>

- A. A template can extend exactly one parent, but can pull in blocks from many templates with {% use %}
- B. A child template that extends a parent cannot output markup outside of blocks
- C. parent() inside a block renders the parent template's version of that block
- D. A template may list several parents in a single {% extends %} tag to combine layouts
- E. {% use %} sets the referenced template as an additional parent for the hierarchy

??? success "Answer Q79"
    **A, B, C**

    Inheritance is single and vertical: one parent per template, with blocks as the overridable holes, and any child markup outside blocks is invalid. parent() extends rather than replaces a block by rendering the parent's version. {% use %} is horizontal reuse — it imports blocks only and does not set a parent, and {% extends %} accepts a single parent, never several to combine.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#template-inheritance-and-layouts)

**Q80.** Which statements about {{ include() }} in Twig are correct? (select all that apply)  <small>_(medium · multiple)_</small>

- A. Without the only keyword, the included template inherits the whole context of the parent template
- B. With only, the local context is isolated, but the app global variable is still available
- C. ignore missing skips a missing template but does not swallow errors raised inside an existing template
- D. include can override blocks defined in the included template
- E. Passing a list of templates renders every template in the list that exists

??? success "Answer Q80"
    **A, B, C**

    By default the full parent context is merged into the include; only isolates the local variables while globals such as app remain accessible. ignore missing only prevents the error for a template that does not exist — exceptions thrown inside the included template still propagate. Overriding blocks is the job of {% embed %}, not include, and a template list renders only the first template that exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#including-templates)

**Q81.** Which statements about generating URLs in Twig are correct? (select all that apply)  <small>_(medium · multiple)_</small>

- A. path() generates a relative URL while url() generates an absolute URL, both from route names
- B. Parameters that are not part of the route definition are appended to the URL as a query string
- C. Using an unknown route name throws a RouteNotFoundException when the template is rendered
- D. Extra parameters not defined in the route are silently dropped from the generated URL
- E. path() is the right choice for links inside emails since mail clients resolve relative URLs

??? success "Answer Q81"
    **A, B, C**

    path() and url() both take a route name (plus parameters): path() yields a relative URL, url() an absolute one, and any parameter the route does not declare ends up in the query string rather than being dropped. An unknown route name fails at render time with RouteNotFoundException. Email bodies, canonical links and feeds leave the page context, so they need url() — relative links from path() break in mail clients.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#linking-to-pages)

**Q82.** For {{ user.name }}, in which order does Twig try to resolve the attribute?  <small>_(hard · internals)_</small>

- A. $user['name'], then $user->name, then $user->name(), getName(), isName(), hasName()
- B. getName() first, then the public property, then array access
- C. Only $user->getName() is ever tried
- D. Only array access $user['name']

??? success "Answer Q82"
    **A**

    Twig's attribute resolver tries array/index access first, then a public property, then method calls name(), getName(), isName() and hasName(). Force pure array access with user['name'] and dynamic names with attribute(user, key). A missing attribute yields null unless strict_variables is on.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#variables)

**Q83.** What does {{ -5|abs }} produce, given filters bind tighter than any operator?  <small>_(hard · code)_</small>

- A. -5, because it parses as -(5|abs)
- B. 5, because abs is applied to -5
- C. An error about applying a filter to a negative literal
- D. 0

??? success "Answer Q83"
    **A**

    The pipe binds tighter than the unary minus, so the expression is -(5|abs) = -(5) = -5, not (-5)|abs. Wrap in parentheses — (-5)|abs — to get 5. This tight binding of filters is a recurring exam trap.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/templates.html#math)

**Q84.** At which point is auto-escaping applied to a value?  <small>_(hard · internals)_</small>

- A. At print time on {{ }}, via EscaperExtension adding an implicit |escape
- B. When the variable is assigned with {% set %}
- C. When the controller passes the variable to the template
- D. During template compilation, once, on the source string

??? success "Answer Q84"
    **A**

    EscaperExtension inserts an implicit |escape(strategy) on every {{ }} output node that is not already marked safe — escaping happens when a value is printed, not when it is set. So {% set x = untrusted %} stores it raw; the escaping occurs only when you later print {{ x }}.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Extension/EscaperExtension.php)

**Q85.** Which PHP function backs Twig's default 'html' escaping strategy?  <small>_(hard · internals)_</small>

- A. htmlspecialchars() with ENT_QUOTES | ENT_SUBSTITUTE
- B. strip_tags()
- C. htmlentities() with ENT_NOQUOTES
- D. addslashes()

??? success "Answer Q85"
    **A**

    The EscaperRuntime maps 'html' to htmlspecialchars() with ENT_QUOTES|ENT_SUBSTITUTE (encoding single and double quotes and substituting invalid code units). html_attr uses a stricter attribute encoder, js uses \\xNN hex, css uses CSS hex and url uses rawurlencode — each context has its own encoder because escaping is context-specific.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/filters/escape.html)

**Q86.** Why must {% extends %} be the first tag, and what can a child template NOT do?  <small>_(hard · internals)_</small>

- A. A child that extends a parent cannot output markup outside blocks; rendering starts at the root ancestor
- B. Markup outside blocks is allowed and rendered before the parent
- C. extends may appear anywhere; order does not matter
- D. A child can define its own <html> wrapper around the parent

??? success "Answer Q86"
    **A**

    When a template extends another, rendering begins at the root ancestor and walks down, so any top-level text a child writes outside a block is ignored (or errors). extends can be a dynamic expression resolved at runtime, which is why it must be resolvable first. Put all child content inside blocks.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/extends.html)

**Q87.** How does template inheritance work at the compiled-PHP level?  <small>_(hard · internals)_</small>

- A. Each {% block %} becomes a block_<name>() method; extends makes the child class override the parent's methods
- B. Blocks are stored as strings and concatenated at runtime
- C. The child template is textually copied into the parent before compilation
- D. Inheritance is resolved by regular expressions on the source

??? success "Answer Q87"
    **A**

    Every template compiles to a class extending Twig\Template; a block becomes a block_<name>() method and extends wires up parentage so child methods override parent ones — exactly like PHP method overriding. A block table ($this->blocks) lets an override anywhere in the chain win.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Template.php)

**Q88.** Which app.* accesses have a side effect? (choose 2)  <small>_(hard · multiple)_</small>

- A. app.session — accessing it can start the session
- B. app.flashes — reading flash messages consumes (clears) them
- C. app.environment — pure read, no side effect
- D. app.debug — pure read, no side effect

??? success "Answer Q88"
    **A, B**

    Accessing app.session may start the session (which can defeat HTTP caching), and reading app.flashes consumes the messages so they are cleared after display — both have side effects. app.environment and app.debug are plain reads with no side effect.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q89.** You need a global whose value is computed from an injected service. Which approach fits best?  <small>_(hard · internals)_</small>

- A. An extension implementing GlobalsInterface::getGlobals() returning the computed value
- B. A {% set %} at the top of base.html.twig
- C. A #[AsGlobal] attribute on the service
- D. Hard-coding it in every controller's render() call

??? success "Answer Q89"
    **A**

    GlobalsInterface::getGlobals() lets an extension inject a service and return computed values, resolved lazily when the extension is instantiated. A static YAML twig.globals entry (even '@service') is fine for simple references, but computed/lazy values belong in a GlobalsInterface extension. There is no #[AsGlobal] attribute.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#global-variables)

**Q90.** A controller passes a variable named `app` to the template. What happens?  <small>_(hard · trap)_</small>

- A. The local variable shadows the global, so app.user etc. refer to the passed value
- B. Symfony throws because 'app' is reserved
- C. The global always wins and the local value is ignored
- D. Both are merged into a single object

??? success "Answer Q90"
    **A**

    Globals are merged into the render context, so a local variable of the same name shadows the global. Passing your own `app` variable breaks app.user/app.request access inside that template — avoid reusing reserved global names.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#global-variables)

**Q91.** A TwigFilter is declared with needs_environment: true. What changes about the callable?  <small>_(hard · internals)_</small>

- A. Twig passes the Environment as the first argument, shifting the user arguments right
- B. Nothing changes; it is only documentation metadata
- C. The filter can only be used inside {% apply %} blocks
- D. The callable must return a Twig\Environment

??? success "Answer Q91"
    **A**

    needs_environment injects Twig\Environment as the first callable argument (and needs_context injects the render context array), so your declared parameters come after it. Forgetting this argument shift is a common cause of TypeErrors when writing extensions.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/advanced.html#automatic-escaping)

**Q92.** With {% include '_card.html.twig' with { title: t } only %}, is the app global still available inside the partial?  <small>_(hard · trap)_</small>

- A. Yes — only isolates the parent's local variables but globals like app remain available
- B. No — only removes everything including globals
- C. Only if you also pass app in the with hash
- D. Globals are never available inside an include

??? success "Answer Q92"
    **A**

    only restricts the include to just the with variables from the caller's local scope, but Twig globals (such as app) are merged into every template's context independently, so app.user etc. still work. Assuming only strips globals is a common misconception.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/include.html)

**Q93.** How is an included template handled by Twig internally?  <small>_(hard · internals)_</small>

- A. It is a separate compiled class, loaded via the loader and invoked at runtime — not textually inlined
- B. Its source is pasted into the parent before compilation
- C. It is re-parsed from disk on every render with no caching
- D. It is merged into the parent's single block table

??? success "Answer Q93"
    **A**

    The include tag compiles to a call to Twig\Template::display()/render() on the sub-template, which the FilesystemLoader resolves and which is compiled and cached like any other template. Includes are separate compiled classes invoked at runtime, not inlined text.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Loader/FilesystemLoader.php)

**Q94.** Why might loop.length and loop.last be unavailable inside a for loop?  <small>_(hard · internals)_</small>

- A. The iterable is not countable (e.g. a bare Generator), so Twig cannot know the total up front
- B. They are only available under strict_variables
- C. They never work in nested loops
- D. They require the collection to be an array of objects

??? success "Answer Q94"
    **A**

    loop.length, loop.last and loop.revindex require a countable iterable (array or Countable/Traversable Twig can count). For a non-countable Generator, Twig cannot determine the total without buffering, so those members may be omitted; loop.index and loop.first are always available.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tags/for.html#the-loop-variable)

**Q95.** Which is true about the tests `is null`, `is empty`, and `is defined`?  <small>_(hard · trap)_</small>

- A. is empty is broadest — true for null, false, 0, '' and []; is null is only for null; is defined checks existence
- B. All three are equivalent
- C. is empty is true only for '' (empty string)
- D. is defined is true only when the value is not null

??? success "Answer Q95"
    **A**

    is defined tests whether the variable exists at all (undefined is not the same as null); is null tests exact null; is empty is the broadest — true for null, false, 0, '' and []. Use is null when you must distinguish "no value" from "empty list", and combine with is defined for maybe-missing variables.

    :material-book-open-variant: [Docs](https://twig.symfony.com/doc/3.x/tests/empty.html)

**Q96.** Which UrlGenerator reference types back path() and url() respectively?  <small>_(hard · internals)_</small>

- A. path() => ABSOLUTE_PATH; url() => ABSOLUTE_URL
- B. path() => RELATIVE_PATH; url() => NETWORK_PATH
- C. Both use ABSOLUTE_URL, differing only in caching
- D. path() => ABSOLUTE_URL; url() => ABSOLUTE_PATH

??? success "Answer Q96"
    **A**

    RoutingExtension calls UrlGenerator::generate() with ABSOLUTE_PATH for path() (a root-relative /path) and ABSOLUTE_URL for url() (scheme + host + path). The generator reads the RequestContext to build the host for absolute URLs.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

**Q97.** Which snippet builds a 'next page' link for the current route, incrementing page?  <small>_(hard · code)_</small>

- A. path(app.current_route, app.current_route_parameters|merge({ page: page + 1 }))
- B. path(app.request.uri, { page: page + 1 })
- C. url(app.route, { page: page + 1 })
- D. path('current', app.params + { page: page + 1 })

??? success "Answer Q97"
    **A**

    app.current_route and app.current_route_parameters expose the active route and its params; merging a new page value onto them and passing to path() rebuilds the current URL with one changed parameter. app.route/app.params are not real members, and + does not merge hashes (~ /merge do).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q98.** Which service selects the fragment renderer for render()/render_esi()?  <small>_(hard · internals)_</small>

- A. Symfony\Component\HttpKernel\Fragment\FragmentHandler
- B. Symfony\Component\Routing\Generator\UrlGenerator
- C. Twig\Extension\EscaperExtension
- D. Symfony\Bridge\Twig\AppVariable

??? success "Answer Q98"
    **A**

    HttpKernelExtension delegates to FragmentHandler, which picks a FragmentRendererInterface (inline, esi, hinclude) by strategy name.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/Fragment/FragmentHandler.php)

**Q99.** What is true about kernel events when an inline fragment is rendered?  <small>_(hard · internals)_</small>

- A. The full request lifecycle runs again for the sub-request (kernel.request, kernel.controller, kernel.response, etc.)
- B. No events fire because it is an internal call
- C. Only kernel.response fires for the fragment
- D. The parent request's events are re-dispatched for the fragment

??? success "Answer Q99"
    **A**

    Inline rendering calls HttpKernel::handle(..., SUB_REQUEST), so the whole listener chain (request, controller, response) runs independently for the fragment. The sub-request has its own Request object; parent attributes are not automatically shared.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_kernel.html#handling-requests)

**Q100.** By default, can a browser hit an embedded controller's fragment URL directly?  <small>_(hard · trap)_</small>

- A. No — embedded controllers are exposed to direct URLs only when fragments are enabled, and the URL is signed
- B. Yes — every embedded controller has a public URL automatically
- C. Yes, but only in dev
- D. No, direct fragment URLs are impossible in Symfony

??? success "Answer Q100"
    **A**

    Inline embedding uses internal sub-requests, not public URLs. Direct fragment access requires enabling framework.fragments, and Symfony signs the fragment URL (URI signer) so attackers cannot forge arbitrary controller calls. Assuming embeds are publicly routable is a security trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

**Q101.** Which catalogue file name enables ICU MessageFormat parsing for English?  <small>_(hard · config)_</small>

- A. messages+intl-icu.en.yaml
- B. messages.icu.en.yaml
- C. messages.en.icu.yaml
- D. icu-messages.en.yaml

??? success "Answer Q101"
    **A**

    A domain suffixed +intl-icu (e.g. messages+intl-icu.en.yaml) is parsed with the IntlFormatter, unlocking plural/select and locale-aware formatting. Putting ICU syntax in a plain messages.en.yaml file makes the braces render literally.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation/message_format.html)

**Q102.** For the ICU message '{count, plural, =0 {none} one {# item} other {# items}}', what does count=1 render?  <small>_(hard · code)_</small>

- A. 1 item
- B. # item
- C. one item
- D. none

??? success "Answer Q102"
    **A**

    count=1 matches the CLDR 'one' category in English, and # inside the branch is replaced by the number, giving '1 item'. # prints the value (not a literal hash), 'one' is a category label not output, and =0 only matches the exact value 0.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation/message_format.html)

**Q103.** Which service does the Twig trans filter ultimately call?  <small>_(hard · internals)_</small>

- A. Symfony\Contracts\Translation\TranslatorInterface::trans() (via TranslationExtension)
- B. Twig\Extension\CoreExtension::translate()
- C. Symfony\Component\Intl\Locale directly
- D. Symfony\Bridge\Twig\AppVariable::trans()

??? success "Answer Q103"
    **A**

    TranslationExtension provides the trans filter/tag and delegates to TranslatorInterface::trans(), which loads catalogues, resolves the message, substitutes parameters, and runs ICU messages through the IntlFormatter.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/TranslationExtension.php)

**Q104.** How does Twig implement #{...} interpolation internally?  <small>_(hard · internals)_</small>

- A. It is a lexer feature: #{expr} in a double-quoted string is tokenised and compiled into ~ concatenation
- B. It is a runtime str_replace over the rendered output
- C. It calls PHP's built-in string interpolation on the template
- D. It is a filter applied after escaping

??? success "Answer Q104"
    **A**

    Inside a "..." string the lexer detects #{, tokenises the embedded expression, and the parser compiles the whole literal into a ~ (string concatenation) chain — so "a #{x} b" becomes 'a ' ~ x ~ ' b'. It has nothing to do with PHP's own interpolation.

    :material-book-open-variant: [Docs](https://github.com/twigphp/Twig/blob/3.x/src/Lexer.php)

**Q105.** With a JSON manifest configured, what does asset('app.css') resolve to?  <small>_(hard · trap)_</small>

- A. The content-hashed name looked up in manifest.json (e.g. app.7f3c.css), not the literal path
- B. The literal /app.css path with ?v appended
- C. An error if app.css is not physically present
- D. The manifest.json file itself

??? success "Answer Q105"
    **A**

    JsonManifestVersionStrategy maps the logical name to its hashed filename from manifest.json, so asset('app.css') returns the resolved hashed path. Expecting the literal path with a ?v query (that is StaticVersionStrategy) is the trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/asset.html)

**Q106.** What gives Symfony's dump() its rich, collapsible HTML output rather than plain var_dump?  <small>_(hard · internals)_</small>

- A. Symfony's DumpExtension backed by VarDumper (VarCloner + HtmlDumper), replacing Twig's plain DebugExtension
- B. Twig's core DebugExtension already produces collapsible HTML
- C. PHP's native var_dump() with an ini setting
- D. The Profiler rewrites var_dump output

??? success "Answer Q106"
    **A**

    Twig core ships DebugExtension with a plain var_dump-based dump(). Symfony augments it with DumpExtension wired to VarDumper (VarCloner clones the variable, HtmlDumper renders collapsible, syntax-highlighted output and routes dumps to the toolbar). Cloning first also makes dumping large graphs safe (depth-limited).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/DumpExtension.php)

**Q107.** Which statements about Twig output escaping in Symfony are correct? (select all that apply)  <small>_(hard · multiple)_</small>

- A. The default escaping strategy is chosen from the template file extension, so a .txt.twig template escapes nothing
- B. Escaping is applied when a value is printed with {{ }}, not when it is assigned with {% set %}
- C. |raw and {% autoescape false %} disable protection, so they must only wrap trusted content
- D. The html_attr strategy is just an alias of html and produces identical output
- E. All templates always use the html strategy regardless of their extension

??? success "Answer Q107"
    **A, B, C**

    The auto-escaping context is derived from the file extension (html, js, css, url, html_attr are available), which is why a .txt.twig template gets no escaping at all — it is not a fixed html default. Escaping happens at print time via the escaper, and |raw / {% autoescape false %} switch the protection off entirely, making them XSS holes for untrusted data. The html_attr strategy is a stricter encoder than html, not an alias.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#output-escaping)

**Q108.** Which statements about the app global variable are true? (select all that apply)  <small>_(hard · multiple)_</small>

- A. app.user is null for anonymous/unauthenticated requests, so templates must not assume it exists
- B. Reading app.flashes consumes the flash messages, so they are gone after being displayed
- C. Accessing app.session can start the session as a side effect
- D. app.environment exposes the operating-system environment variables
- E. The app global can never be shadowed by a local template variable

??? success "Answer Q108"
    **A, B, C**

    app is an AppVariable instance: app.user is null when nobody is authenticated, app.flashes consumes messages when read, and app.session starts the session on access (which can defeat HTTP caching). The distractors are wrong because app.environment is the kernel environment (dev/prod), not OS variables, and defining a local variable named app shadows the global.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/templates.html#the-app-global-variable)

**Q109.** Which statements about translations in Twig are correct? (select all that apply)  <small>_(hard · multiple)_</small>

- A. The trans filter arguments are ordered (parameters, domain, locale)
- B. A missing translation key does not throw; the key string itself is returned
- C. ICU MessageFormat pluralization is only parsed for catalogues in domains with the +intl-icu suffix
- D. transchoice is the recommended filter for pluralization in current Symfony versions
- E. Requesting a missing translation key raises an exception at render time

??? success "Answer Q109"
    **A, B, C**

    The trans filter signature is message|trans(parameters, domain, locale) — passing the domain first is a classic mistake. Missing keys fall back to returning the key itself instead of erroring, and ICU {n, plural, ...} syntax is only interpreted for domains suffixed with +intl-icu. The transchoice filter was removed; ICU MessageFormat is the modern way to pluralize.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html)

---

<small>Back to [Chapter Exams](index.md) · [Templating (Twig)](../twig/index.md)</small>
