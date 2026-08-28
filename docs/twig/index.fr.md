# Templating (Twig)

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Custom Extension](../labs/twig.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Twig est le moteur de templates par défaut de Symfony : un langage compilé,
sandboxé et à auto-escaping qui transforme les fichiers `.html.twig` en classes
PHP optimisées. Cette étape couvre la syntaxe, le modèle de sécurité
(auto-escaping), l'héritage et la réutilisation, la globale `app`, les
filtres/fonctions fournis par Symfony (`path`, `asset`, `trans`, `render`) et
l'outillage (`dump`) — toujours sous l'angle de *ce que le moteur compile et
pourquoi*.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | [Controllers](../controllers/index.md), [PHP API](../php-web-security/php-api.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stage 5 (Controllers) |
    | **Revision priority** | **Medium** |
    | **Est. time** | 3–4 h |

## Why this stage matters

L'examen vous demande rarement d'*écrire* un template complet ; il vous demande
si vous savez ce que **fait** une construction, quand l'auto-escaping se
déclenche, la différence entre `path()` et `url()`, ce que retourne `app.user`
quand personne n'est connecté, et comment `render(controller(...))` interagit
avec le sous-système de fragments. Comprendre que Twig **compile en PHP** (via
`Twig\Environment`, mis en cache sous `var/cache/`) démystifie d'un seul coup la
performance, l'échappement et le débogage.

## Micro-chapters

- [Twig Syntax](syntax.md) — `{{ }}`, `{% %}`, `{# #}`, variables, expressions,
  opérateurs, tests, précédence, contrôle des espaces.
- [Auto-Escaping](auto-escaping.md) — la stratégie HTML, les contextes
  d'échappement, `|raw`, `|e('js'|'css'|'url'|'html_attr')`, les blocs
  `autoescape`, la justification sécurité.
- [Template Inheritance](inheritance.md) — `extends`, `block`, `parent()`,
  héritage multi-niveaux, `use` (réutilisation horizontale) vs `extends`.
- [Global Variables](globals.md) — la globale `app` (`app.user`, `app.request`,
  `app.session`, `app.flashes`, `app.environment`, `app.debug`), globales
  personnalisées.
- [Filters & Functions](filters-functions.md) — les fonctions intégrées (`date`,
  `format`, `merge`, `default`, `json_encode`, `path`, `url`…) et les
  personnalisées via une extension Twig / `#[AsTwigFilter]` /
  `#[AsTwigFunction]`.
- [Template Includes](includes.md) — le tag/la fonction `include`, `embed`,
  `with`, `only`, `ignore missing`.
- [Loops & Conditions](loops-conditions.md) — `for` (la variable `loop`),
  `if`/`elseif`/`else`, la clause `for … else`, les tests.
- [URL Generation](urls.md) — `path()` vs `url()`, passage de paramètres.
- [Controller Rendering](controller-rendering.md) — `render(controller(...))`,
  `render_esi`, fragments, quand embarquer un controller.
- [Translations & Pluralization](translations.md) — le filtre/tag `trans`,
  paramètres, pluralisation ICU MessageFormat, domaines.
- [String Interpolation](interpolation.md) — `"#{...}"`, concaténation `~`,
  `format`/sprintf.
- [Assets Management](assets.md) — la fonction `asset()` et le versionnement des
  assets (AssetMapper et Encore sont hors périmètre).
- [Debugging Variables](debugging.md) — `dump()` / `{% dump %}`, l'extension de
  debug, `{{ dump() }}` vs le profiler.

## How to study this stage

1. Commencez par [Syntax](syntax.md) et [Auto-Escaping](auto-escaping.md) — les
   deux sujets les plus testés.
2. Apprenez la [globale `app`](globals.md) sur le bout des doigts ; ses membres
   apparaissent dans de nombreux énoncés.
3. Pratiquez l'[héritage](inheritance.md) + les [includes](includes.md) en
   conditions réelles.
4. Considérez la [génération d'URL](urls.md) et les [translations](translations.md)
   comme les ponts vers les étapes [Routing](../routing/index.md) et Intl.

---

<small>Previous stage: [Routing](../routing/index.md) · Next stage: [Forms](../forms/index.md)</small>

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Twig est le langage qui transforme des données PHP en pages HTML lisibles par un navigateur — sans jamais mélanger la logique métier avec l'affichage.

**Pourquoi ça existe ?** Écrire du HTML directement dans du PHP est illisible et dangereux (failles XSS). Twig sépare "ce qu'on affiche" de "comment on le calcule", et protège automatiquement contre les injections.

**🏠 Analogie de la vraie vie :** Un modèle de lettre type avec des champs à remplir ("Cher [NOM], votre commande [NUMÉRO] est prête"). Le modèle (le template Twig) reste toujours le même ; seules les données injectées changent à chaque envoi.

**Symfony dans la vraie vie :** Un contrôleur calcule les données (`$produits = ...`) et les passe au template (`return $this->render('produits.html.twig', ['produits' => $produits])`) — Twig ne fait que les afficher, jamais les calculer.

**⚠️ Erreur fréquente :** utiliser `|raw` sur du contenu saisi par un visiteur — ça désactive la protection automatique contre les scripts malveillants (XSS).

**🧠 Comment le mémoriser :** "PHP calcule, Twig affiche — jamais l'inverse."


## Official References

- [Symfony documentation — Creating and Using Templates (Twig)](https://symfony.com/doc/8.0/templates.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
