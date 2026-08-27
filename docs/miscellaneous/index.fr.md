# Miscellaneous Components

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Messenger Middleware](../labs/miscellaneous.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Les composants avancés qui complètent une boîte à outils Symfony de niveau
Expert : Serializer, PropertyAccess, Mailer & Mime, Cache, Process, Lock,
Intl/Translation, Runtime, Clock, Config/DotEnv/ExpressionLanguage, plus la
gestion des erreurs, le débogage et les bonnes pratiques de déploiement. Chacun
est un composant découplé, utilisable de manière autonome ou via l'autowiring du
framework. **Messenger** — qui faisait auparavant partie de cette étape — a
désormais sa propre étape dédiée : voir [Messenger](../messenger/index.md),
le sujet le plus testé du programme.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [Architecture](../architecture/index.md) (le kernel, les events),
      [Dependency Injection](../dependency-injection/index.md) (autowiring, tags)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★☆
    - **Est. time:** 5–6 h
    - **Dependencies:** s'appuie sur Architecture + DI
    - **Revision priority:** **Élevée** dans l'ensemble.

## Chapters

- [Configuration (Config, DotEnv, ExpressionLanguage)](configuration.md) — TreeBuilder,
  Processor, la cascade `.env` + `.env.local.php`, la syntaxe des expressions.
- [Error Handling](error-handling.md) — le composant ErrorHandler, la conversion
  erreur/exception, l'error controller, prod vs dev.
- [Code Debugging](debugging.md) — VarDumper (`dump`/`dd`, cloners/dumpers, `Data`),
  l'outillage Debug, Stopwatch.
- [Deployment Best Practices](deployment.md) — l'environnement de prod, le cache warmup, `--no-dev`,
  opcache/preload, le dump dotenv, la checklist.
- [Cache Component](cache.md) — PSR-6 vs PSR-16 vs les contrats Symfony, les adapters,
  les tags, la protection contre les stampedes.
- [Process Component](process.md) — `Process`, `run` vs `start`/`wait`, les timeouts,
  le streaming, les codes de sortie, les pièges de `fromShellCommandline`.
- [Serializer Component](serializer.md) — normalizers + encoders, les groups,
  `#[SerializedName]`, `#[Ignore]`, le context, les références circulaires.
- [PropertyAccess Component](property-access.md) — chemins de propriété
  dynamiques, l'ordre de recherche des getters, les fallbacks magiques.
- [Mime & Mailer Components](mailer.md) — `Email`/`TemplatedEmail`, les transports,
  pièces jointes/intégration, l'envoi async via Messenger, le modèle de parts Mime.
- [Filesystem & Finder Components](filesystem-finder.md) — les opérations sur fichiers et
  l'itérateur de fichiers fluide.
- [Lock Component](../appendices/out-of-syllabus/lock.md) — `LockFactory`, blocking vs non-blocking, les stores,
  les locks expirants/auto-rafraîchissants et partagés.
- [Web Profiler & Data Collectors](profiler.md) — la toolbar, un
  `DataCollectorInterface` personnalisé, quand il s'exécute, sa désactivation en prod.
- [Internationalization and localization](intl.md) — le Translator, l'ICU MessageFormat,
  les domains, le fallback de locale, le composant de données Intl.
- [Runtime Component](runtime.md) — le flux du point d'entrée, `RuntimeInterface`,
  `SymfonyRuntime`, `autoload_runtime.php`.
- [Clock Component](clock.md) — `ClockInterface`, `now()`, les clocks
  mock/monotonic/native, `DatePoint`, tester le temps.

## Suggested reading order

Commencez par les composants de mise en forme des données —
[Serializer](serializer.md), [PropertyAccess](property-access.md) et
[Mailer](mailer.md) — puis l'ensemble
infrastructure ([Cache](cache.md), [Lock](../appendices/out-of-syllabus/lock.md), [Process](process.md),
[Filesystem & Finder](filesystem-finder.md)). Intégrez
[Config](configuration.md), [Runtime](runtime.md), [Clock](clock.md) et
[Intl](intl.md), et terminez par le trio opérationnel
[Error Handling](error-handling.md), [Debugging](debugging.md),
[Profiler](profiler.md) et [Deployment](deployment.md).

## Official References

- [Symfony documentation — Symfony Components](https://symfony.com/doc/8.0/components/index.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
