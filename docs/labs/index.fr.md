# Practical Labs

La théorie vous explique *comment ça fonctionne* ; les labs vous rendent *capable de
construire et de déboguer en conditions d'examen*. Chaque lab est un TD de type
universitaire : un objectif, des instructions pas à pas, un cycle **test-first (TDD)**
lorsque le comportement du code s'y prête, et une solution de référence masquée pour
vous comparer.

!!! abstract "How to use a lab"
    1. Lisez d'abord le chapitre de **théorie** lié.
    2. Faites les **instructions du TD** par vous-même — résistez à l'envie d'ouvrir la solution.
    3. Pour les labs TDD : écrivez le **test qui échoue**, faites-le passer, puis refactorisez.
    4. Exécutez les **étapes de validation** ; relisez les **erreurs courantes**.
    5. Alors seulement, ouvrez la **solution idéale** et comparez.

## Lab modes

- :material-flask: **Lab TDD** — comportement du code : écrivez d'abord le test PHPUnit.
- :material-console: **Vérification manuelle** — config/infra : vérifiez via la CLI,
  le profiler ou `curl`.
- :material-thought-bubble: **Simulation conceptuelle** — théorie pure : prédisez
  la sortie, ordonnez les étapes, déboguez le scénario.

## Flagship labs (one per topic area)

| Domaine | Lab | Mode | Difficulté |
|---|---|---|---|
| [PHP & Web Security](php-web-security.md) | Une collection typée avec la SPL (`IteratorAggregate`, `Countable`, `ArrayAccess`) | TDD | Moyen |
| [HTTP](http.md) | Un client d'API testé avec `MockHttpClient` | TDD | Moyen |
| [Architecture](architecture.md) | Un event personnalisé + des subscribers priorisés sur l'`EventDispatcher` | TDD | Moyen |
| [Controllers](controllers.md) | Un argument resolver `ValueResolverInterface` personnalisé | TDD | Avancé |
| [Routing](routing.md) | Prédire et vérifier le matching des routes (`debug:router` / `router:match`) | Manuel | Moyen |
| [Templating (Twig)](twig.md) | Un filtre/une fonction d'extension Twig personnalisée | TDD | Facile |
| [Forms](forms.md) | Un form type personnalisé avec un `DataTransformer` | TDD | Avancé |
| [Data Validation](validation.md) | Une `Constraint` personnalisée + son `ConstraintValidator` | TDD | Moyen |
| [Dependency Injection](dependency-injection.md) | Un registre piloté par tags construit par un compiler pass | TDD | Avancé |
| [Security](security.md) | Un `Voter` pour une autorisation fine | TDD | Moyen |
| [HTTP Caching](http-caching.md) | Headers d'expiration et de validation, vérifiés avec `curl` | Manuel | Moyen |
| [Console](console.md) | Une commande testée avec `CommandTester` | TDD | Facile |
| [Automated Tests](testing.md) | Tests de service + tests fonctionnels (`KernelTestCase`/`WebTestCase`) | TDD | Moyen |
| [Miscellaneous](miscellaneous.md) | Un handler Messenger + un middleware personnalisé | TDD | Avancé |

!!! tip "Where labs fit in the study loop"
    Faites un lab juste après avoir terminé la théorie et les flashcards d'un domaine,
    avant l'examen blanc. Appliquer un concept une fois vaut mieux que le relire
    trois fois.

---

<small>Related: [Roadmap](../roadmap.md) · [Revision Hub](../revision/index.md)</small>

## 🧠 Pour les nuls

**C'est quoi cette page ?** Le point d'entrée vers les exercices pratiques (labs) — un par domaine — où tu construis réellement du code au lieu de juste lire de la théorie.

**Pourquoi ça existe ?** Lire "comment fonctionne un Voter" et être capable d'en écrire un soi-même sous pression sont deux compétences différentes — les labs entraînent la seconde, indispensable le jour de l'examen (et en vrai travail).

**🏠 Analogie de la vraie vie :** Les travaux pratiques (TD) à l'université, en complément du cours magistral : le cours explique la théorie, le TD te fait manipuler toi-même, avec un corrigé caché à consulter seulement après avoir essayé.

**Symfony dans la vraie vie :** Le lab Security te fait écrire un vrai `Voter` testé unitairement — pas juste lire sa définition, mais le construire, le tester, et le comparer à une solution de référence.

**⚠️ Erreur fréquente :** ouvrir la solution cachée avant d'avoir vraiment essayé — ça donne l'illusion de comprendre sans avoir consolidé la compétence pratique.

**🧠 Comment le mémoriser :** "Essaie d'abord, compare ensuite — jamais l'inverse."


## Official References

- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Testing](https://symfony.com/doc/8.0/testing.html)
