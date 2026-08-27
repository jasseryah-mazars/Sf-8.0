# Revision Sheet — Templating (Twig)

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Templating (Twig)](../../twig/index.md).

## Assets Management
- `asset('path')` → public URL relative to `public/`, with base path + version.
- Versioning = cache busting; strategies: static, JSON manifest, empty.
- Named packages target CDNs / alternate base URLs.
- AssetMapper & Encore are out of scope — only `asset()` here.

**Cheat:** `{{ asset('css/app.css') }}` · `{{ asset('logo.png', 'cdn') }}`. `framework.assets.version` / `json_manifest_path` / `packages`. `asset()` = static files; `path()`/`url()` = routes.

## Auto-Escaping
- Escaping is **on by default**, context chosen by **file extension**.
- Five strategies: `html`, `html_attr`, `js`, `css`, `url` — match the context.
- `|raw` / `{% autoescape false %}` disable protection: trusted content only.
- Escaping happens at print time via `EscaperExtension`.

**Cheat:** `.html.twig`→html · `.js.twig`→js · `.txt.twig`→none. `|e` = `|escape`; strategies `html|html_attr|js|css|url`. `|raw` = trust me. `{% autoescape 's' %}…{% endautoescape %}`. Escape at `{{ }}`, not at `{% set %}`.

## Controller Rendering
- `render(controller(...))` embeds a controller as a sub-request (inline).
- `render_hinclude` defers loading to the browser via a JS placeholder.
- Backed by `HttpKernelExtension` → `FragmentHandler` → a `FragmentRenderer`.
- Use it only when the fragment needs its own logic/data/cache.

**Cheat:** `render(controller('C::m', {a:1}))` = inline sub-request. `render_hinclude(...)` = async placeholder resolved by the browser. Enable direct fragment URLs via `framework.fragments`. `include` for cheap fragments; embed for isolated logic.

## Debugging Variables
- `dump()` prints a rich VarDumper view; `{% dump %}` sends it to the collector.
- No-arg `dump()` dumps the whole context.
- Dev/debug only — remove before prod (it errors there).
- Rich output = `DumpExtension` + VarDumper, not Twig's plain debug extension.

**Cheat:** `{{ dump(a, b) }}` inline · `{{ dump() }}` = all context. `{% dump x %}` = to toolbar, no page markup. Debug/dev only; unavailable in prod. Backed by VarDumper (`VarCloner` + `HtmlDumper`).

## Filters & Functions
- Filters (`|`) transform; functions (`f()`) return values.
- Built-ins live in `CoreExtension` + Symfony bridge extensions.
- Custom: `AbstractExtension` returning `TwigFilter`/`TwigFunction`, or
  `#[AsTwigFilter]`/`#[AsTwigFunction]`.
- Mark trusted HTML with `is_safe`; use runtimes for heavy deps.

**Cheat:** `value|filter(args)` · `function(args)`. Options: `is_safe`, `needs_environment`, `needs_context`, `is_variadic`. Register: `getFilters()`/`getFunctions()` or `#[AsTwigFilter/Function]`. `default` covers undefined **and** empty; `json_encode` is escaped.

## Global Variables
- `app` = `AppVariable`: `user`, `request`, `session`, `flashes`, `environment`,
  `debug`, `token`, `locale`, `current_route`.
- `app.user` may be `null`; identifier is `userIdentifier`.
- Register custom globals via `twig.globals` or `GlobalsInterface`.
- `app.session`/`app.flashes` have side effects (start / consume).

**Cheat:** `app.user` (null!), `app.request`, `app.session`, `app.flashes`. `app.environment` = dev/prod · `app.debug` = bool · `app.locale`. Custom: `twig.globals.X: value` or `implements GlobalsInterface`.

## Template Includes
- `include` drops a fragment; `include()` function returns a string.
- Context merges by default; `only` isolates; `with` adds/overrides.
- `ignore missing` skips a missing template (not internal errors).
- `embed` = include + override blocks; a list includes the first that exists.

**Cheat:** `{% include 'x' with {a:1} only %}` · `{{ include('x', {a:1}) }}`. `ignore missing` · list `['a','b']` → first existing. `{% embed 'x' %}{% block y %}…{% endblock %}{% endembed %}`.

## Template Inheritance
- `extends` = single vertical parent; blocks are the overridable holes.
- `parent()` extends a block; `block('x')` prints a named block.
- `use` mixes in blocks from many templates (horizontal), no parent set.
- Inheritance compiles to PHP method overriding on `Twig\Template`.

**Cheat:** `{% extends 'base.html.twig' %}` first, one parent only. `{% block x %}…{% endblock %}` → overridable region. `{{ parent() }}` parent block · `{{ block('x') }}` any block. `{% use '_t.html.twig' with x as y %}` horizontal, blocks only.

## String Interpolation
- `#{expr}` interpolates inside **double-quoted** strings only.
- `~` concatenates (string cast); `+` is arithmetic.
- `~` has lower precedence than arithmetic.
- `format` = sprintf; `replace` = keyed substitution.

**Cheat:** `"hi #{name}"` (double quotes) · `'hi #{name}'` = literal. `a ~ b` join · `a + b` add. `"%s %d"|format(a, b)` · `"%x%"|replace({'%x%': v})`.

## Loops & Conditions
- `for` → `foreach`; `loop` gives `index`, `first`, `last`, `length`, `parent`.
- `for … else` handles the empty case cleanly.
- No `break`/`continue` — filter (`for x in items if …`) instead.
- `loop.length`/`last` need a countable iterable.

**Cheat:** `loop.index`(1) `index0`(0) `first` `last` `length` `revindex` `parent`. `{% for k, v in map %}` · `{% for x in items if cond %}`. `for … else … endfor` = empty state. Tests: `is defined/null/empty/even/odd/iterable/same as/divisible by`.

## Twig Syntax
- Three delimiters: `{{ }}` print, `{% %}` do, `{# #}` comment.
- Twig **compiles to a PHP class** cached under `var/cache/`; runtime is cheap.
- `~` concatenates; `//` floors; filters bind tightest.
- Whitespace: `-` modifiers and `{% apply spaceless %}`.

**Cheat:** `{{ }}` echo · `{% %}` logic · `{# #}` comment. Attribute order: index → property → method → getX → isX → hasX. Precedence high→low: `**` > `* / // %` > `+ -` > `~` > compare > `and`/`or` > `?:`. Trim: `{{- -}}`. `{% apply spaceless %}`.

## Translations & Pluralization
- `message|trans(params, domain, locale)` — mind the order.
- Domains partition catalogues; `+intl-icu` unlocks ICU formatting.
- Pluralize with ICU `{n, plural, one{…} other{…}}`, not `transchoice`.
- Missing keys return the key, they do not error.

**Cheat:** `'k'|trans({'%x%': v}, 'domain', 'fr')`. `{% trans_default_domain 'admin' %}` then drop the domain arg. ICU: `messages+intl-icu.en.yaml`, `{n, plural, =0{} one{} other{#}}`. `transchoice` = removed.

## URL Generation
- `path()` = relative, `url()` = absolute; both from route names.
- Backed by `RoutingExtension` → `UrlGeneratorInterface` + `RequestContext`.
- Extra params → query string; missing required params throw.
- Use `url()` when the link leaves the page (email, canonical, RSS).

**Cheat:** `path('name', {params})` → `/rel`. `url('name', {params})` → `https://host/rel`. Extras → `?query`. Missing required → exception. `app.current_route` + `app.current_route_parameters` to rebuild.
