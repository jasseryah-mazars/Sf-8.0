# Deployment Best Practices

!!! tip "In a nutshell"
    Un déploiement en prod embarque uniquement les dépendances de prod, un cache
    préchauffé, `APP_DEBUG=0`, et opcache/preload activés afin qu'aucun travail
    par request ne parse la configuration. Point d'or pour l'examen : la prod
    charge le container compilé tel quel et ne détecte jamais automatiquement les
    changements de configuration, vous devez donc vider et préchauffer le cache à
    chaque déploiement.

!!! example "Real-world analogy"
    Déployer en prod, c'est la mise en place d'un restaurant avant le service. Pendant
    le créneau calme de préparation, la cuisine découpe et portionne tout à l'avance
    (le cache warmup) afin qu'aucune préparation ne vole du temps pendant le coup de feu
    du dîner. Le menu imprimé est ensuite figé pour la soirée : le personnel le suit
    tel quel et ne revérifie jamais les prix des fournisseurs en plein service (le
    container compilé est chargé avec les vérifications de fraîcheur désactivées). Donc
    si vous changez une recette mais sautez la nouvelle préparation, la cuisine continue
    de servir l'ancien plat — c'est pourquoi vous devez vider et repréchauffer le cache
    à chaque déploiement.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Lister les étapes obligatoires en prod : `--no-dev`, cache warmup, dump du dotenv.
    - [ ] Expliquer `APP_ENV`/`APP_DEBUG` et le rôle d'opcache/preload en prod.
    - [ ] Appliquer une checklist de déploiement reproductible.

    **Syllabus:** `Miscellaneous → Deployment` ·
    **Level:** Advanced ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Configuration](configuration.md), [Runtime](runtime.md)

---

## Theory

Déployer Symfony consiste à livrer le code dans un environnement optimisé pour
la **vitesse et la sûreté** : uniquement les dépendances de production, un cache
préchauffé, de vraies variables d'environnement, `APP_DEBUG=0`, et
l'opcache/preload de PHP activés. L'objectif est qu'aucun travail par request ne
parse du YAML, ne scanne des fichiers ni n'expose l'interne de l'application.

## Deep Dive — how it works internally

!!! question "Predict first"
    Vous déployez du nouveau code en prod mais sautez `cache:clear`/`warmup`.
    L'application continue de servir l'ancien comportement. Pourquoi Symfony ne
    remarque-t-il pas simplement les fichiers modifiés ?

??? note "Reveal"
    En prod, le container compilé dans `var/cache/prod/` est chargé **tel quel** —
    les vérifications de fraîcheur sont désactivées pour la vitesse. Symfony
    suppose que le cache est à jour, vous **devez** donc le vider/préchauffer à
    chaque déploiement pour que les changements prennent effet.

### Environment & debug

`APP_ENV=prod` sélectionne la configuration de prod ; `APP_DEBUG=0` désactive le
profiler, la page verbeuse de l'ErrorHandler de debug, et les vérifications de
fraîcheur du cache. En prod, le container compilé dans `var/cache/prod/` est
chargé tel quel — Symfony le suppose à jour, vous **devez** donc
préchauffer/vider le cache au déploiement.

```ini
; real env vars (or .env.local.php) on the prod server
APP_ENV=prod   ; selects the prod config tree
APP_DEBUG=0    ; no profiler, no verbose errors, no freshness checks
```

### Cache warmup

`cache:clear` supprime le cache périmé et (par défaut) exécute les **cache
warmers** (`CacheWarmerInterface`) qui préconstruisent le container, le
matcher/generator de routing, le cache des templates Twig, les métadonnées du
validator/serializer. `cache:warmup` préchauffe sans vider. Préchauffez pendant
le build afin que la première vraie request soit rapide et que l'utilisateur web
n'ait aucun droit d'écriture sur `var/cache`.

```php
use Symfony\Component\HttpKernel\CacheWarmer\CacheWarmerInterface;

// Runs during cache:clear (by default) and cache:warmup
final class ReportCacheWarmer implements CacheWarmerInterface
{
    public function isOptional(): bool
    {
        return true; // optional warmers may be skipped and lazily built later
    }

    public function warmUp(string $cacheDir, ?string $buildDir = null): array
    {
        file_put_contents($cacheDir.'/report.meta', 'built at deploy');

        return []; // list of classes to preload
    }
}
```

### Dependencies & autoloader

`composer install --no-dev --optimize-autoloader` (ou
`--classmap-authoritative`) ignore les paquets de dev et construit une classmap
optimisée, évitant les appels stat au filesystem à chaque chargement de classe.

```console
# Skip require-dev packages and generate an optimized classmap
$ composer install --no-dev --optimize-autoloader

# Stricter: the classmap is the ONLY source, no filesystem checks at all
$ composer install --no-dev --classmap-authoritative
```

### DotEnv dump

`composer dump-env prod` compile la cascade `.env*` en `.env.local.php`, si bien
que la production évite le parsing DotEnv (voir [Configuration](configuration.md)).

```console
# Compile the .env* cascade once, at deploy time
$ composer dump-env prod
Successfully dumped .env files in .env.local.php
# When .env.local.php exists, the .env* files are no longer parsed
```

### Opcache & preload

Opcache met en cache le bytecode compilé. Symfony génère
`var/cache/prod/App_KernelProdContainer.preload.php` ; pointer
`opcache.preload` vers ce fichier charge les classes cœur en mémoire partagée
une seule fois au démarrage du process manager PHP, réduisant le chargement de
classes par request. Assurez-vous que `opcache.validate_timestamps=0` est activé
en prod et réinitialisez opcache à chaque déploiement.

```ini
; php.ini (prod)
opcache.preload=/srv/app/var/cache/prod/App_KernelProdContainer.preload.php
opcache.preload_user=www-data
opcache.validate_timestamps=0 ; never stat files — reset opcache on each deploy
```

```mermaid
flowchart LR
    G[git pull / artifact] --> C[composer install --no-dev]
    C --> DE[dump-env prod]
    DE --> W[cache:clear + warmup]
    W --> OP[opcache reset / preload]
    OP --> L[go live]
```

!!! note "Source reference"
    `Symfony\Component\HttpKernel\CacheWarmer\CacheWarmerInterface` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/CacheWarmer/CacheWarmerInterface.php).

## Configuration & code

=== "Console"

    ```console
    $ APP_ENV=prod APP_DEBUG=0 composer install --no-dev --optimize-autoloader
    $ composer dump-env prod
    $ php bin/console cache:clear --env=prod
    $ php bin/console cache:warmup --env=prod
    $ php bin/console asset-map:compile   # if using AssetMapper (out of scope here)
    ```

=== "YAML"

    ```yaml
    # config/packages/prod/framework.yaml (example)
    when@prod:
        framework:
            router:
                strict_requirements: null
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `composer install --no-dev --optimize-autoloader` | Livrer les dépendances de dev (profiler, phpunit) en prod |
| Préchauffer le cache pendant le build ; rendre `var/` non inscriptible par l'utilisateur web | Préchauffer lors de la première request en production |
| `APP_DEBUG=0` et `dump-env prod` | Laisser `APP_DEBUG=1` (fuites + lenteur) |
| Activer opcache + preload, réinitialiser au déploiement | `validate_timestamps=1` en prod |

## When (not) to use it / alternatives

Ces étapes s'appliquent à tout déploiement en prod (VM, conteneur, PaaS). Dans
des images de conteneurs immuables, intégrez `composer install`, `dump-env` et
`cache:warmup` dans le build de l'image afin que le conteneur en exécution n'ait
aucune mise en place à faire.

!!! danger "Certification traps"
    - La prod ne détecte **pas** automatiquement les changements de configuration — vous devez vider/préchauffer le cache.
    - `dump-env prod` → `.env.local.php` ; quand ce fichier existe, `.env*` n'est pas parsé.
    - `APP_DEBUG=1` en prod active le profiler et expose les traces — à ne jamais faire.
    - `--optimize-autoloader` / `--classmap-authoritative` accélèrent le chargement des classes.

!!! warning "Common mistakes"
    - Oublier de réinitialiser opcache après le déploiement → du bytecode périmé est servi.
    - Exécuter `cache:warmup` avec un utilisateur différent de celui du serveur
      web, causant des erreurs de permissions sur `var/cache`.

## Exercises

1. **(Advanced)** Écrivez la liste ordonnée des commandes pour un déploiement prod depuis zéro.
2. **(Advanced)** Expliquez pourquoi la prod doit préchauffer le cache alors que le dev n'en a pas besoin.

??? success "Solutions"

    **1.** `composer install --no-dev --optimize-autoloader` → `composer dump-env prod`
    → `cache:clear --env=prod` → `cache:warmup --env=prod` → réinitialisation d'opcache.

    **2.** En dev, `ConfigCache` vérifie la fraîcheur des ressources et reconstruit
    en cas de changement ; la prod saute ces vérifications pour la vitesse et charge
    le container compilé tel quel, il doit donc être (re)construit explicitement au
    déploiement.

## Certification questions

??? question "Q1. Which flag excludes dev dependencies during deploy?"
    - [x] A. `--no-dev` ✅
    - [ ] B. `--prod`
    - [ ] C. `--production`

    **Why:** `composer install --no-dev` ignore les paquets de `require-dev`.
    **Ref:** [Deploying Symfony](https://symfony.com/doc/current/deployment.html).

??? question "Q2. What does `composer dump-env prod` create?"
    - [x] A. `.env.local.php` ✅
    - [ ] B. `.env.prod`
    - [ ] C. `config/prod.php`

    **Why:** Il compile la cascade en `.env.local.php` pour un chargement rapide.
    **Ref:** [Configuring env vars in production](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production).

??? question "Q3. Why set `opcache.validate_timestamps=0` in prod?"
    - [x] A. To skip file-modification checks and serve cached bytecode ✅
    - [ ] B. To enable debug mode
    - [ ] C. To disable opcache

    **Why:** Avec des déploiements immuables, sauter les vérifications de timestamps
    maximise les hits d'opcache (réinitialisez plutôt opcache au déploiement).
    **Ref:** [Performance](https://symfony.com/doc/current/performance.html).

## Key takeaways

- `--no-dev --optimize-autoloader`, `dump-env prod`, `cache:warmup`, `APP_DEBUG=0`.
- La prod charge le container compilé tel quel — videz/préchauffez le cache à chaque déploiement.
- Opcache + preload + `validate_timestamps=0` réduisent le surcoût par request.

## Last-minute revision

!!! tip "Cheat sheet"
    - Ordre de déploiement : install --no-dev → dump-env prod → cache:clear → cache:warmup → opcache reset.
    - `APP_ENV=prod APP_DEBUG=0`.
    - Fichier de preload : `var/cache/prod/*.preload.php`.
    - `var/cache` préchauffé au build, en lecture seule pour l'utilisateur web.

## Connections

- **Depends on:** [Configuration](configuration.md) — `dump-env prod` et `APP_ENV`/`APP_DEBUG` pilotent le comportement en prod ; [Runtime](runtime.md) démarre le kernel.
- **Reused in:** [Cache](cache.md) — les cache warmers préconstruisent les pools et les métadonnées pendant le déploiement.
- **Confused with:** la reconstruction automatique du dev — la prod ne détecte jamais automatiquement les changements de configuration.

## Official References
- [Official docs — Deploying Symfony](https://symfony.com/doc/current/deployment.html)
- [Official docs — Performance](https://symfony.com/doc/current/performance.html)
- [Symfony source — CacheWarmerInterface](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/CacheWarmer/CacheWarmerInterface.php)

## Video references

!!! tip "Watch & learn"
    Voici des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    "Symfony components" pour consolider ce chapitre. Nous lions des chaînes stables
    plutôt que des vidéos individuelles afin que les références ne se périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences SymfonyCon et keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/deployment.html) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** la prod charge le container compilé sans vérifications de fraîcheur
- [ ] ordonner un déploiement prod : `--no-dev`, `dump-env prod`, `cache:warmup`, réinitialisation d'opcache
- [ ] déboguer un « ancien comportement après déploiement » (cache périmé / opcache non réinitialisé)
- [ ] repérer le piège : `APP_DEBUG=1` en prod fait fuiter les traces et ralentit tout
- [ ] décrire ce que les cache warmers préconstruisent et pourquoi

---

<small>Related: [Configuration](configuration.md) · [Runtime](runtime.md) · [Cache](cache.md)</small>
