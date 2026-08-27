# HTTP

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[API Client (MockHttpClient)](../labs/http.md)** — un TD pas à pas avec une démarche test-first et une solution de référence.

Le protocole Hypertext Transfer Protocol est le contrat que parle toute application
Symfony. Avant de pouvoir raisonner sur le kernel, les controllers, la sécurité ou
le cache, vous devez avoir un modèle mental exact de la façon dont une **request**
devient une **response** — et de la manière dont les composants
`Symfony\Component\HttpFoundation` et `Symfony\Component\HttpClient` de Symfony
transforment ce protocole en objets PHP fortement typés.

Cette étape construit cette fondation. Toutes les étapes suivantes (Architecture,
Controllers, Routing, Security, HTTP Caching) supposent que vous la maîtrisez déjà
parfaitement.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [PHP & Web Security](../php-web-security/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stage 1 (PHP + threat model) |
    | **Revision priority** | **High** |
    | **Est. time** | 3–4 h |

## Why this stage matters

Symfony est, au fond, une machine qui transforme `Request → Response`. `HttpKernel`,
le routing, les controllers, les events et le cache ne sont que des couches
posées au-dessus des deux objets valeur
`Symfony\Component\HttpFoundation\Request` et
`Symfony\Component\HttpFoundation\Response`. L'examen teste les détails du
protocole (sémantique des status codes, méthodes safe/idempotent, attributs des
cookies, content negotiation) *et* l'API Symfony qui les modélise. Maîtrisez
cette étape et le reste du syllabus devient beaucoup plus facile.

## Micro-chapters

Travaillez-les dans l'ordre :

- [ ] [Client / Server Interaction](client-server.md) — le cycle
  request/response, TCP/TLS, HTTP/1.1 vs HTTP/2.
- [ ] [Status Codes](status-codes.md) — les classes 1xx–5xx et celles que
  l'examen adore (301/302/307/308, 401/403, 404/410, 422, 429).
- [ ] [HTTP Request](request.md) — l'anatomie de la request mise en
  correspondance avec les bags de la `Request` Symfony.
- [ ] [HTTP Response](response.md) — l'anatomie de la response mise en
  correspondance avec `Response` et ses sous-classes.
- [ ] [HTTP Methods](methods.md) — la sémantique safe/idempotent et le method
  override.
- [ ] [Cookies](cookies.md) — les attributs, la classe `Cookie`, la définition
  via la response.
- [ ] [Caching Overview](caching.md) — freshness vs validation (vue d'ensemble
  uniquement).
- [ ] [Content Negotiation](content-negotiation.md) — les headers `Accept*` et
  la gestion des formats.
- [ ] [Language Detection](language-detection.md) — deviner la locale de
  l'utilisateur.
- [ ] [HttpClient Component](httpclient.md) — `HttpClientInterface`, scoping,
  streaming, retry et mocking.

## How to study it

1. Lisez [Client / Server](client-server.md) et [Status Codes](status-codes.md)
   pour le protocole brut.
2. Projetez le protocole sur Symfony avec [Request](request.md) et
   [Response](response.md) — ces deux chapitres sont le cœur de toute l'étape.
3. Ajoutez ensuite [Methods](methods.md), [Cookies](cookies.md) et
   [Content Negotiation](content-negotiation.md).
4. Terminez avec le composant [HttpClient](httpclient.md) (le côté *sortant*).

---

<small>Related: [PHP & Web Security](../php-web-security/index.md) ·
[Symfony Architecture](../architecture/index.md) ·
[Controllers](../controllers/index.md) · [HTTP Caching](../http-caching/index.md)</small>

## Official References

- [Symfony documentation — HttpFoundation component](https://symfony.com/doc/8.0/components/http_foundation.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
