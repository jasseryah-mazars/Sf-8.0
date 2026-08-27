# URL Generation

!!! tip "In a nutshell"
    Generate links from route names, never hard-code them: `path()` gives a relative
    URL, `url()` an absolute one. Exam hook: use `url()` whenever the link leaves the
    page (emails, canonical tags, RSS); extra params become the query string.

!!! example "Real-world analogy"
    Generating a URL is like giving someone directions. `path()` is the in-building
    shorthand — "room 204, third door on the left" — perfectly clear once you are already
    inside the same building (on the same site), but meaningless to anyone standing
    elsewhere. `url()` is the full postal address with street, city and country: the only
    form that still works when the note is carried far away and read somewhere else — an
    email, an RSS feed, a canonical tag. Either way you name the destination by its label
    (the route name), never by hand-copying the raw address, and any extra details you
    tack on that the address doesn't need become the "apt/notes" line (the query string).

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Generate relative URLs with `path()` and absolute ones with `url()`.
    - [ ] Pass route parameters and understand extra-params-as-query behaviour.
    - [ ] Explain which Symfony extension and generator back these functions.

    **Syllabus:** `Templating (Twig) → URL generation` ·
    **Level:** Advanced ·
    **Est. time:** 20 min ·
    **Prerequisites:** [Routing](../routing/index.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
`path()` donne une URL relative utile *à l'intérieur* du site ; `url()` donne une URL absolue utile *en dehors* (email, flux RSS).

### Imagine dans la vraie vie
Générer une URL, c'est donner des indications à quelqu'un. `path()` est le raccourci "interne au bâtiment" — "salle 204, troisième porte à gauche" — parfaitement clair une fois qu'on est déjà dans le même bâtiment (le même site), mais incompréhensible pour quelqu'un ailleurs. `url()` est l'adresse postale complète avec rue, ville et pays : la seule forme qui fonctionne encore quand le mot est emporté au loin et lu ailleurs.

### Dans Symfony
Un email envoyé à un utilisateur doit toujours utiliser `url()`, jamais `path()` — un lien relatif dans un email n'a aucun sens hors du contexte d'un navigateur déjà sur ton site.

### Exemple simple
```twig
<a href="{{ path('produit_show', {id: p.id}) }}">Voir</a>  {# lien interne au site #}
<!-- Dans un email : {{ url('produit_show', {id: p.id}) }} -->
```

### Comment le mémoriser 🧠
"Si le lien quitte la page (email, RSS, balise canonique), utilise `url()`." Sinon, `path()` suffit et reste plus léger.

## Theory

Never hard-code URLs. Generate them from **route names** so paths stay correct
when routes change:

```twig
<a href="{{ path('article_show', { slug: article.slug }) }}">Read</a>
<link rel="canonical" href="{{ url('article_show', { slug: article.slug }) }}">
```

| Function | Returns | Example |
|---|---|---|
| `path(name, params)` | **relative** URL | `/articles/hello` |
| `url(name, params)` | **absolute** URL | `https://ex.com/articles/hello` |

Use `path()` for on-site links; use `url()` when the URL leaves the page —
emails, RSS, canonical tags, redirects consumed elsewhere.

```twig
{# path(): relative URL — fine for on-site navigation #}
<a href="{{ path('order_show', { id: order.id }) }}">Your order</a>

{# url(): absolute URL — required when the link leaves the page (email, RSS) #}
<a href="{{ url('order_show', { id: order.id }) }}">View your order</a>
```

!!! question "Predict first"
    You build an email body with `{{ path('order_show', { id: order.id }) }}`.
    Why do recipients complain the link is broken?

??? note "Reveal"
    `path()` produces a **relative** URL (`/order/42`) — fine on-page, useless in a
    mail client that has no host to resolve it against. Use `url()` for anything
    that leaves the page (emails, canonical tags, RSS): it emits an **absolute**
    URL built from the request context.

## Deep Dive — how it works internally

Both functions come from **`Symfony\Bridge\Twig\Extension\RoutingExtension`**,
which delegates to the **`Symfony\Component\Routing\Generator\UrlGeneratorInterface`**
(the same generator controllers use via `generateUrl()`).

```php
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;

// RoutingExtension receives this generator and exposes it as path()/url()
public function __construct(private UrlGeneratorInterface $generator) {}

// generateUrl() in a controller uses the very same service
$relative = $this->generateUrl('article_show', ['slug' => 'hello']);
```

```mermaid
flowchart LR
    T["path('r', {id:1})"] --> RE[RoutingExtension::getPath]
    T2["url('r', {id:1})"] --> RE2[RoutingExtension::getUrl]
    RE --> G["UrlGenerator::generate(…, RELATIVE_PATH/ABSOLUTE_PATH)"]
    RE2 --> G2["UrlGenerator::generate(…, ABSOLUTE_URL)"]
    G --> P[/relative path/]
    G2 --> U[/absolute url/]
```

- `path()` → generator reference type `ABSOLUTE_PATH` (a root-relative path like
  `/foo`); `url()` → `ABSOLUTE_URL` (scheme + host + path).
- **Extra parameters** not consumed by the route pattern are appended as the
  **query string**: `path('search', { q: 'a', page: 2 })` when `search` is `/search`
  → `/search?q=a&page=2`.
- The generator reads the **request context** (`RequestContext`: scheme, host,
  base URL) to build absolute URLs — so `url()` produces the right host per
  environment.
- `RoutingExtension` marks its output `is_safe: ['html']` for the appropriate
  context; the generated URL is still properly encoded by the generator.

```php
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;
use Symfony\Component\Routing\RequestContext;

// path() → ABSOLUTE_PATH; extra params ('page') go to the query string
$rel = $generator->generate('search', ['q' => 'a', 'page' => 2], UrlGeneratorInterface::ABSOLUTE_PATH);
// $rel = '/search?q=a&page=2'

// url() → ABSOLUTE_URL; scheme + host come from the RequestContext
$generator->setContext(new RequestContext(host: 'example.com', scheme: 'https'));
$abs = $generator->generate('search', ['q' => 'a'], UrlGeneratorInterface::ABSOLUTE_URL);
// $abs = 'https://example.com/search?q=a'

// RoutingExtension declares these functions is_safe: ['html'] — no double escaping
```

!!! note "Source reference"
    `Symfony\Bridge\Twig\Extension\RoutingExtension`,
    `Symfony\Component\Routing\Generator\UrlGeneratorInterface` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php).

See [URL generation (Routing)](../routing/url-generation.md) for the generator
internals, `RequestContext`, and reference types.

## Configuration & code

=== "Twig"

    ```twig
    {# named params, extra ones become query string #}
    <a href="{{ path('product_list', { category: 'books', page: 2 }) }}">Books</a>

    {# absolute, for an email/canonical #}
    <a href="{{ url('homepage') }}">Home</a>

    {# link to the current route with a changed param #}
    <a href="{{ path(app.current_route, app.current_route_parameters|merge({ page: 3 })) }}">Next</a>
    ```

=== "Controller (equivalent)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;
    use Symfony\Component\Routing\Generator\UrlGeneratorInterface;

    final class LinkController extends AbstractController
    {
        #[Route('/go', name: 'go')]
        public function go(): Response
        {
            $rel = $this->generateUrl('homepage');
            $abs = $this->generateUrl('homepage', [], UrlGeneratorInterface::ABSOLUTE_URL);

            return $this->redirect($abs);
        }
    }
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `path()`/`url()` from route names | Hard-coded `/articles/1` |
| `url()` for emails/canonical/RSS | `path()` in an email (relative, breaks) |
| Merge `app.current_route_parameters` | Rebuilding the current URL by hand |
| Pass params as a hash | String-concatenating query params |

## When (not) to use it / alternatives

Always prefer these over literals. Choose `url()` when the link may be viewed
**off-site** (email, feed, API payload, `Location` header consumed by another
host). Choose `path()` for normal in-page navigation to keep pages host-agnostic.

!!! danger "Certification traps"
    - `path()` is **relative**, `url()` is **absolute** — the single most common
      exam question here.
    - Extra params become the **query string**, they are not silently dropped.
    - An unknown route name throws `RouteNotFoundException` at render time.
    - `path()` in an email body yields a **relative** link that breaks in a mail
      client — use `url()`.

!!! warning "Common mistakes"
    - Forgetting a **required** route parameter → `MissingMandatoryParametersException`.
    - Assuming `url()` uses `localhost` in prod — it uses the request context /
      configured default host.

## Exercises

1. **(Basic)** Link to route `blog_show` with `slug`.
2. **(Intermediate)** Build a canonical `<link>` with an absolute URL.
3. **(Advanced)** Produce a "next page" link for the current route, incrementing
   `page`.

??? success "Solutions"

    **1.** `<a href="{{ path('blog_show', { slug: post.slug }) }}">…</a>`.

    **2.** `<link rel="canonical" href="{{ url('blog_show', { slug: post.slug }) }}">`.

    **3.** `{{ path(app.current_route, app.current_route_parameters|merge({ page: page + 1 })) }}`.

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. What is the difference between `path()` and `url()`?"
    - [x] A. `path()` is relative, `url()` is absolute ✅
    - [ ] B. `url()` is relative, `path()` is absolute
    - [ ] C. They are identical
    - [ ] D. `path()` only works in controllers

    **Why:** `path()` = `ABSOLUTE_PATH`, `url()` = `ABSOLUTE_URL`. **Ref:**
    [Linking to pages](https://symfony.com/doc/8.0/templates.html#linking-to-pages).

??? question "Q2. `path('search', { q: 'x', extra: 1 })` where `search` is `/search`. Result?"
    - [x] A. `/search?q=x&extra=1` ✅
    - [ ] B. `/search/x/1`
    - [ ] C. `/search` (extras dropped)
    - [ ] D. Error

    **Why:** Parameters not in the route pattern become the query string. **Ref:**
    [URL generation](https://symfony.com/doc/8.0/routing.html#generating-urls).

??? question "Q3. Which extension provides `path()`/`url()`?"
    - [x] A. `Symfony\Bridge\Twig\Extension\RoutingExtension` ✅
    - [ ] B. `Twig\Extension\CoreExtension`
    - [ ] C. `Symfony\Bridge\Twig\Extension\AssetExtension`
    - [ ] D. `HttpKernelExtension`

    **Why:** `RoutingExtension` wraps `UrlGeneratorInterface`. **Ref:**
    [RoutingExtension](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php).

## Key takeaways

- `path()` = relative, `url()` = absolute; both from route names.
- Backed by `RoutingExtension` → `UrlGeneratorInterface` + `RequestContext`.
- Extra params → query string; missing required params throw.
- Use `url()` when the link leaves the page (email, canonical, RSS).

## Last-minute revision

!!! tip "Cheat sheet"
    - `path('name', {params})` → `/rel`.
    - `url('name', {params})` → `https://host/rel`.
    - Extras → `?query`. Missing required → exception.
    - `app.current_route` + `app.current_route_parameters` to rebuild.

## Connections

- **Depends on:** [Routing](../routing/index.md) — `path()`/`url()` turn a defined route name into a link.
- **Reused in:** [URL generation (Routing)](../routing/url-generation.md) — the same `UrlGeneratorInterface`, `RequestContext` and reference types drive both Twig and controllers.
- **Confused with:** [Assets](assets.md) — `path()`/`url()` are for routes; `asset()` is for static files under `public/`.

## Official References
- [Official — Linking to pages](https://symfony.com/doc/8.0/templates.html#linking-to-pages)
- [Official — Generating URLs](https://symfony.com/doc/8.0/routing.html#generating-urls)
- [Symfony source — RoutingExtension](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Bridge/Twig/Extension/RoutingExtension.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Twig templating" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/templates.html#linking-to-pages) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** to generate URLs from route names instead of hard-coding them
- [ ] use `path()` vs `url()` and pass route params in Symfony 8
- [ ] debug a broken relative link in an email that should have used `url()`
- [ ] spot the trick answer swapping relative/absolute or dropping extra params
- [ ] explain how `RoutingExtension` delegates to `UrlGeneratorInterface` + `RequestContext`

---

<small>Related: [URL generation (Routing)](../routing/url-generation.md) · [Assets](assets.md) · [Global Variables](globals.md)</small>
