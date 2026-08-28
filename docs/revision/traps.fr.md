# Top Certification Traps

L'examen récompense les **distinctions précises**, pas les définitions. Voici un
index transversal des subtilités, idées reçues et pièges liés aux versions qui
coûtent le plus souvent des points. Chaque chapitre a son propre bloc
`!!! danger "Certification traps"` ; cette page recense les plus connus et
renvoie au domaine complet.

!!! danger "Read every option literally"
    La plupart des pièges tiennent à un seul mot — **"always", "by default", "only",
    "never", "must"** — ou à une option ancienne mais familière (dépréciée) proposée
    à côté de l'option actuelle. Ralentissez sur celles-là.

## Architecture → [area](../architecture/index.md)

- **`kernel.view` ne se déclenche que si le controller retourne autre chose qu'une
  `Response`.** S'il retourne déjà une `Response`, `view` est sauté.
- **`kernel.terminate` s'exécute *après* l'envoi de la response** — pas avant. Le
  travail lourd va ici, pas dans un listener de response.
- **Nom** de l'event vs **classe** de l'event (`kernel.request` ↔ `RequestEvent`) —
  les questions les mélangent.
- La **LTS est la dernière mineure d'une majeure**, pas une branche à part.

## Dependency Injection → [area](../dependency-injection/index.md)

- **Les services sont private par défaut** — impossible de faire
  `$container->get()` dessus sauf s'ils sont rendus publics ou récupérés via un
  service locator / le container de test.
- **Les compiler passes n'ont pas d'attribut** — enregistrez-les dans `build()`.
- **L'autowiring résout par type, pas par nom de variable** (sauf avec `#[Autowire]`
  / des bindings nommés). Renommer un argument ne change pas le câblage.
- Les paramètres sont résolus à la **compilation** ; les variables d'environnement
  (`%env(...)%`) le sont au **runtime**.

## Security → [area](../security/index.md)

- **La stratégie de décision d'accès par défaut est `affirmative`** (un seul voter
  qui accorde suffit) — pas unanimous.
- **`IS_AUTHENTICATED_REMEMBERED` ≠ `IS_AUTHENTICATED_FULLY`.** Les utilisateurs en
  remember-me sont authentifiés mais pas « fully » ; les actions sensibles exigent
  FULLY.
- Un **`Passport` porte des badges** ; `authenticate()` retourne le passport, il ne
  retourne pas directement un token.
- **`access_control` est évalué de haut en bas ; la première correspondance gagne** —
  l'ordre compte.
- `PUBLIC_ACCESS` est la façon d'autoriser l'accès anonyme dans le système actuel.

## HTTP & HTTP Caching → [HTTP](../http/index.md) · [Caching](../http-caching/index.md)

- **`no-cache` ne signifie pas « ne pas mettre en cache »** — cela signifie
  « revalider avant usage ». **`no-store`** signifie ne jamais stocker.
- **`max-age` s'adresse aux navigateurs ; `s-maxage` aux caches partagés/proxy** et
  prime dans les caches partagés.
- **Expiration et validation sont deux modèles différents** — `Expires`/`max-age` vs
  `ETag`/`Last-Modified` ; la validation produit un **304 Not Modified**.
- **PUT est idempotent, POST ne l'est pas.** GET/HEAD sont safe *et* idempotentes.
- `302` vs `301` vs `307`/`308` — permanent vs temporaire, et préservation de la
  méthode.

## Console → [area](../console/index.md)

- **Drapeaux de verbosité :** `-v`, `-vv`, `-vvv` correspondent à verbose /
  very-verbose / debug — ne les intervertissez pas.
- **`execute()` doit retourner un int** (`Command::SUCCESS`/`FAILURE`/`INVALID`) ;
  ne rien retourner/`null` est incorrect avec le typage actuel.
- Les options **`VALUE_NONE`** sont des drapeaux booléens (présence = true) ; elles
  ne prennent pas de valeur.
- Noms des events de console (`console.command`, `console.error`, `console.terminate`,
  `console.signal`) vs events du kernel — dispatchers différents.

## Forms & Validation → [Forms](../forms/index.md) · [Validation](../validation/index.md)

- **Ordre des form events :** `PRE_SET_DATA` → `POST_SET_DATA` → `PRE_SUBMIT` → `SUBMIT`
  → `POST_SUBMIT`. `PRE_SUBMIT` voit les données brutes de la request ; `SUBMIT` les
  données normalisées.
- **CSRF est activé par défaut** pour les forms — le désactiver est un choix délibéré.
- **`isValid()` implique `isSubmitted()`** en interne, mais appelez d'abord
  `handleRequest()` ; valider un form non soumis n'a pas de sens.
- **Groups de validation :** le group par défaut est `Default` ; une `GroupSequence`
  change à la fois *quelles* constraints s'exécutent et *dans quel ordre* (s'arrête
  au premier group en échec).
- **Les data transformers** s'exécutent view→norm→model à la soumission et dans
  l'autre sens à l'affichage — la confusion de direction est un piège classique.

## Controllers & Routing → [Controllers](../controllers/index.md) · [Routing](../routing/index.md)

- **`forward()` est une sub-request interne** (côté serveur), **`redirect*()` envoie
  un 3xx au navigateur** — ce n'est pas la même chose.
- **La `priority` de route** départage les égalités ; les routes plus spécifiques
  ont besoin d'une priorité plus haute ou d'être déclarées en premier.
- **Le type de référence par défaut de `generateUrl()` est `ABSOLUTE_PATH`**, pas
  l'URL absolue.
- Le routing par attributs est le défaut actuel ; la syntaxe par annotations est
  héritée (legacy).

## Twig → [area](../twig/index.md)

- **L'auto-escaping est activé par défaut** (html) — `|raw` le désactive et
  constitue un risque de sécurité en cas de mauvais usage.
- **`{% include %}` vs `{% embed %}` vs `{% use %}`** — embed permet de surcharger
  des blocks ; use importe des blocks horizontalement.
- `path()` retourne une URL **relative**, `url()` une URL **absolue**.

## Miscellaneous / Messenger → [area](../miscellaneous/index.md)

- **Messenger a une pondération accrue** — maîtrisez buses vs transports vs
  middleware vs stamps, le flux **retry + failure transport**, et le cycle de vie du
  **worker** (`messenger:consume`).
- **Le transport `sync` traite les messages immédiatement**, dans le même processus ;
  l'asynchrone exige un worker en cours d'exécution.
- **`CacheInterface::get()` de Symfony Contracts** utilise un callback (protection
  contre le cache stampede) — différent du PSR-6 brut `getItem()`/`save()`.
- Serializer : le **normalizer** (objet ↔ tableau) et l'**encoder** (tableau ↔
  chaîne) sont des étapes distinctes.

## PHP & Web Security → [area](../php-web-security/index.md)

- **Les propriétés `readonly`** ne peuvent être initialisées qu'une fois
  (typiquement dans le constructeur) ; toute réaffectation lève une erreur.
- **`#[\Override]` (8.3)** échoue à la compilation si la méthode ne surcharge rien.
- **Les requêtes préparées stoppent les SQLi ; l'échappement stoppe les XSS** — ne
  mélangez pas les parades.

---

<small>Related: [Master Cheat Sheet](cheat-sheet.md) · [Memory Aids](memory-aids.md) · [Exam-Day Strategy](../exam-guide/strategy.md)</small>

## 🧠 Pour les nuls

**C'est quoi ?** Une liste, domaine par domaine, des **pièges classiques** que l'examen tend le plus souvent — des nuances subtiles ("toujours", "par défaut", "seulement") qui font basculer une bonne réponse apparente vers une mauvaise réponse réelle.

**Pourquoi ça existe ?** Certaines erreurs reviennent chez presque tous les candidats (ex. confondre `kernel.view` et `kernel.response`). Les rassembler en une seule page permet de les vérifier une dernière fois, juste avant l'examen, sans avoir à rouvrir chaque chapitre.

**🏠 Analogie de la vraie vie :** C'est la liste des **questions pièges classiques du code de la route** qu'une auto-école affiche en fin de formation : "attention, la priorité à droite ne s'applique pas sur un rond-point" — les pièges connus de tous les moniteurs, réunis en une fiche.

**Symfony dans la vraie vie :** Chaque puce → un piège précis, formulé comme une phrase-vérité à retenir (ex. "kernel.view ne se déclenche que si le contrôleur retourne un non-Response") / Le lien "area" → le chapitre complet si le piège ne fait pas encore sens.

**⚠️ Erreur fréquente :** Lire cette page comme une simple liste de curiosités, sans la relier au chapitre correspondant. Un piège compris sans le mécanisme sous-jacent se dissout vite ; un piège relié à sa cause réelle reste en mémoire.

**🧠 Comment le mémoriser :** *« Les mots absolus ("toujours", "jamais", "seulement") sont des signaux d'alerte »* — dès qu'une option d'examen en contient un, relis-la deux fois.


## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
