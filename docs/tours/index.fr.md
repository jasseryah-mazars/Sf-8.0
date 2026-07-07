# Source Tours

Le niveau expert signifie **« je l'ai lu »**, pas seulement « je l'ai utilisé ». La certification
adore les questions que seule la source peut trancher : *quel event est dispatché en premier*, *quelle
exception est levée quand aucun resolver ne correspond*, *ce que le firewall fait avant que les
authenticators ne s'exécutent*. Les Source Tours sont des visites guidées de la poignée de fichiers
où vivent ces réponses.

## What a tour is (and is not)

Un tour n'est **pas** un chapitre du syllabus. Il ne ré-enseigne pas la fonctionnalité — les
chapitres classiques s'en chargent. Un tour suit **un chemin concret à travers le vrai code
source de Symfony 8.0**, arrêt par arrêt, comme un debugger le parcourrait pas à pas.
Chaque arrêt nomme la méthode dans laquelle vous vous « trouvez », esquisse ce qu'elle fait, et
pointe le point d'extension disponible à cet endroit précis.

## How to read a tour

1. **Ouvrez le fichier source lié côte à côte.** Chaque tour s'ancre sur un ou
   deux fichiers de la branche `8.0` de `symfony/symfony` sur GitHub. Gardez le vrai
   fichier ouvert dans un second onglet ou panneau d'éditeur et faites défiler au fil de votre lecture.
2. **Le code du tour est une esquisse, le code sur GitHub est la vérité.** Les
   extraits des tours sont des *esquisses simplifiées* — élaguées, renommées pour la clarté, débarrassées
   des cas limites. Quand une question repose sur une signature exacte ou une classe d'exception,
   fiez-vous à la source liée.
3. **Avancez arrêt par arrêt.** Chaque tour est une séquence numérotée d'« arrêts ». Ne
   survolez pas : à chaque arrêt, prédisez ce qui se passe ensuite *avant* de poursuivre la lecture.

## The four tours

| Tour | Résumé en une ligne |
| --- | --- |
| [HttpKernel::handle()](httpkernel-handle.md) | Les ~100 lignes que traverse chaque response Symfony sans exception — les huit events du kernel dans leur habitat naturel. |
| [ControllerResolver & ArgumentResolver](argument-resolver.md) | Comment une chaîne `_controller` devient un callable, et comment chaque paramètre gagne (ou perd) sa valeur dans la chaîne de resolvers. |
| [A Form's life](form-lifecycle.md) | De `createForm()` à `createView()` : les trois représentations des données, les six events de form, et l'endroit où la validation a réellement lieu. |
| [A request crosses the Firewall](firewall-request-cycle.md) | La chaîne de listeners de sécurité sur `kernel.request` : correspondance de firewall, passports, badges, et la décision d'accès finale. |

## Reading tips

- **Suivez une request dans votre tête.** Choisissez un scénario concret (« POST /login
  avec un mauvais mot de passe », « GET /admin en anonyme ») et tracez *cette* request
  à travers chaque arrêt. La lecture abstraite ne tient pas ; une request tracée de bout en bout, si.
- **Lisez sans var_dump.** Résistez à l'envie d'exécuter le code. L'examen est un
  exercice de lecture et de raisonnement : entraînez-vous à déduire le comportement de la seule source —
  ce qui est dispatché, ce qui est retourné, ce qui est levé.
- **Guettez les points d'extension.** Chaque fois que le core dispatche un event, vérifie
  une interface, ou itère une collection de services tagués, c'est un hook — et
  les hooks sont de l'or pour l'examen. Chaque tour se termine par un tableau *Extension points recap* ;
  essayez de le reconstruire de mémoire après votre première lecture.
- **Notez l'ordre, toujours.** La plupart des questions pièges sont des questions d'ordre
  (events, transformers, listeners). Quand un tour numérote ses arrêts, cette
  numérotation *est* la réponse à une future question.

## Official References

- [symfony/symfony on GitHub (8.0 branch)](https://github.com/symfony/symfony/tree/8.0)
- [Symfony Docs — The HttpKernel Component](https://symfony.com/doc/current/components/http_kernel.html)
- [Symfony Docs — Events and Event Listeners](https://symfony.com/doc/current/event_dispatcher.html)

---
<small>Related: [Request Handling](../architecture/request-handling.md) ·
[Value Resolvers](../controllers/value-resolvers.md) ·
[Form Events](../forms/events.md) ·
[Firewalls](../security/firewalls.md)</small>
