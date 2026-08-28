# Automated Tests

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Kernel/Web Tests](../labs/testing.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Symfony fournit une pile de test complète au-dessus de **PHPUnit** : des tests
unitaires pour les services isolés, et des tests *fonctionnels* (au niveau HTTP)
qui démarrent le vrai kernel, envoient des requests à travers un navigateur
synthétique et vérifient la response, le DOM et l'état interne du framework.
Cette étape enseigne l'outillage qui intéresse l'examen — `KernelTestCase`,
`WebTestCase`, le **Client** de test, le **Crawler**, le **Profiler**, et les
assertions de response. Le bridge PHPUnit est couvert ici par souci
d'exhaustivité mais est **exclu de la certification Symfony 8**.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [Controllers](../controllers/index.md),
      [Routing](../routing/index.md), [Forms](../forms/index.md),
      [Dependency Injection](../dependency-injection/index.md)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★☆
    - **Est. time:** 3–4 h
    - **Dependencies:** vous testez ce que les étapes précédentes vous ont
      permis de construire ; le chapitre sur le Profiler s'appuie sur
      [HTTP](../http/index.md) et le chapitre sur les dépréciations renvoie vers
      [Architecture → Deprecations](../architecture/deprecations.md)
    - **Revision priority:** **Medium** — poids stable à l'examen ; les points
      fiables sont la visibilité de `self::getContainer()`, les helpers
      `assertResponse*` et les modes du deprecation helper.

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Tester une application Symfony, c'est vérifier automatiquement qu'une classe isolée fonctionne (test unitaire) ou qu'une page entière répond correctement (test fonctionnel) — sans jamais tester à la main dans un navigateur.

**Pourquoi ça existe ?** Sans tests automatisés, chaque changement de code risque de casser silencieusement une fonctionnalité existante ailleurs dans l'application.

**🏠 Analogie de la vraie vie :** Tester une seule pièce détachée sur un établi (test unitaire) contre faire rouler la voiture entière sur circuit (test fonctionnel) — les deux ont leur utilité, à des échelles différentes.

**Symfony dans la vraie vie :** `KernelTestCase` démarre juste le kernel pour tester un service isolé ; `WebTestCase` démarre tout et simule un vrai visiteur naviguant sur le site via un `Client`.

**⚠️ Erreur fréquente :** écrire uniquement des tests fonctionnels lourds là où un test unitaire rapide suffirait — ça ralentit inutilement toute la suite de tests.

**🧠 Comment le mémoriser :** "Test unitaire = une pièce sur l'établi. Test fonctionnel = la voiture entière sur circuit."


## Why this stage matters

Le testing est l'endroit où tout le framework se rejoint : un test fonctionnel
exerce le routing, le controller, Twig, la sécurité et le système d'events en
une seule passe. La certification ne vous demande pas d'écrire de grandes
suites — elle vérifie si vous savez *quelle classe fait quoi*, *quel service est
disponible dans un test* et *quelle assertion utiliser*. Ce sont des faits
précis et mémorisables, ce qui rend cette étape très rentable par minute
d'étude.

## Chapters

- [Unit Tests with PHPUnit](unit-tests.md) — `TestCase`, assertions, `#[DataProvider]`,
  mocks vs stubs, attributs PHPUnit 11/12, tester un service isolément.
- [Functional Tests](functional-tests.md) — `WebTestCase` vs `KernelTestCase`,
  `createClient()`, l'environnement `test`, `self::getContainer()`.
- [The Client Object](client.md) — `request()`, `submitForm()`, `clickLink()`,
  redirections, `disableReboot()`, cookies et historique.
- [The Crawler Object](crawler.md) — `filter()`/`filterXPath()`, `selectLink()`/
  `selectButton()`, extraction de texte/attributs, `form()`/`link()`.
- [The Profiler Object](profiler.md) — `enableProfiler()`, `getProfile()`, lecture
  des data collectors, assertions sur les emails et les events.
- [Framework Objects Access](framework-objects.md) — le container de test, démarrer
  le kernel, remplacer/mocker des services dans les tests.
- [Client Configuration](client-configuration.md) — paramètres serveur, authentification HTTP,
  headers, environnement/debug, requests isolées.
- [Request/Response Introspection](introspection.md) — `getRequest()`/`getResponse()`
  et les helpers `assertResponse*` / `assertSelector*`.
- [PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md) — collecte des dépréciations, mocking de l'horloge/du DNS,
  `SYMFONY_DEPRECATIONS_HELPER`, l'extension PHPUnit de Symfony. **Exclu de la
  certification Symfony 8.**
- [Handling Deprecated Code](deprecations.md) — `#[IgnoreDeprecations]`, modes du
  helper (`max`, `disabled`, `weak`), baselines.

## Suggested reading order

Commencez par [Unit Tests](unit-tests.md) pour les bases de PHPUnit, puis
[Functional Tests](functional-tests.md) pour la couche qui démarre le kernel.
Apprenez le trio [Client](client.md), [Crawler](crawler.md) et
[Introspection](introspection.md) ensemble — c'est ainsi qu'un test fonctionnel
pilote et vérifie réellement. Terminez par le groupe intégration framework et
diagnostics : [Framework Objects](framework-objects.md),
[Client Configuration](client-configuration.md), [Profiler](profiler.md),
[PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md) et [Deprecations](deprecations.md).

## Official References

- [Symfony documentation — Testing](https://symfony.com/doc/8.0/testing.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
