# Aides-mémoire

Des moyens mnémotechniques pour les **ordres et énumérations** que l'examen attend
de vous par cœur. Les faits isolés s'effacent ; une accroche les fait tenir.

!!! abstract "How to use these"
    Apprenez d'abord le mécanisme sous-jacent (dans les chapitres du domaine), puis
    utilisez ces accroches pour ancrer l'*ordre* et la *composition des ensembles*
    en mémoire. Vérifiez avec la [Master Cheat Sheet](cheat-sheet.md).

## Kernel event order

`kernel.request` → `kernel.controller` → `kernel.controller_arguments` →
*(`kernel.view`)* → `kernel.response` → `kernel.finish_request` → `kernel.terminate`.

!!! tip "Mnemonic: **R-C-A-V-R-F-T**"
    "**R**eally **C**ool **A**pps **V**alidate **R**esponses, **F**inish,
    **T**erminate."

    - **V**iew est entre parenthèses — il **ne se déclenche que si le controller
      retourne autre chose qu'une `Response`**.
    - **Terminate** s'exécute **après** l'envoi de la response (`kernel.terminate`).
    - **Exception** est hors bande : il se déclenche dès que quelque chose lève une
      exception.

## HTTP status classes

`1xx info · 2xx success · 3xx redirect · 4xx client error · 5xx server error`.

!!! tip "Hook"
    "**1** Information, **2** it worked, **3** go elsewhere, **4** you messed up,
    **5** we messed up."

    - **304** Not Modified = la victoire de la validation de cache.
    - **401** = *non authentifié* (qui êtes-vous ?) ; **403** = *non autorisé*
      (on vous connaît, mais vous n'avez pas le droit). "401 before 403."

## Safe vs idempotent methods

- **Safe** (aucun changement d'état) : **GET, HEAD, OPTIONS, TRACE**.
- **Idempotentes** (répétables, même effet) : les méthodes safe **+ PUT, DELETE**.
- **Ni l'une ni l'autre :** **POST, PATCH**.

!!! tip "Hook"
    "**POST creates, PUT replaces**" — remplacer deux fois donne la même chose,
    poster deux fois en donne deux. (PUT idempotente, POST non.)

## Cache-Control directives

!!! tip "The two that flip people"
    - **`no-cache`** = *stocker mais revalider avant chaque usage* (PAS « ne pas
      mettre en cache »).
    - **`no-store`** = *ne jamais rien écrire*.
    - **`max-age`** = durée de vie côté navigateur ; **`s-maxage`** = durée de vie
      côté cache partagé/proxy (le « s » veut dire **s**hared).

    "**no-cache** asks first; **no-store** forgets."

## Cache: expiration vs validation

- **Expiration** = basée sur le temps : `Expires`, `Cache-Control: max-age`/`s-maxage`.
- **Validation** = basée sur le contenu : `ETag` ↔ `If-None-Match`, `Last-Modified` ↔
  `If-Modified-Since`, avec un **304** en réponse.

!!! tip "Hook"
    "**E**xpiration = **E**gg timer; **V**alidation = **V**erify with a fingerprint
    (ETag)."

## Security passport badges

`UserBadge · PasswordCredentials · CsrfTokenBadge · RememberMeBadge ·
PasswordUpgradeBadge · PreAuthenticatedUserBadge`.

!!! tip "Mnemonic: **U-P-C-R-P-P**"
    "**U**sers **P**resent **C**redentials, **R**emember, then **P**assword-upgrade
    or **P**re-auth."

    - **`UserBadge`** est le seul toujours requis (il identifie l'utilisateur).
    - `CsrfTokenBadge` + `RememberMeBadge` sont des comportements optionnels.

## Access-decision strategies

`affirmative (default) · consensus · unanimous · priority`.

!!! tip "Hook"
    "**A**ny grants (affirmative), **most** wins (consensus), **all** must agree
    (unanimous), **first** to speak (priority)." **Défaut = affirmative.**

## Console verbosity ladder

`-q quiet (16) · normal (32) · -v verbose (64) · -vv very-verbose (128) ·
-vvv debug (256)`.

!!! tip "Hook"
    Comptez les **v** : **1 v = verbose, 2 = very, 3 = debug**. Les valeurs
    **doublent** à chaque cran (16→32→64→128→256).

## Console event order

`console.command` → *(run)* → `console.error` (on throw) → `console.terminate`
(always). `console.signal` on OS signals.

!!! tip "Hook"
    "**Command** starts, **Error** if it breaks, **Terminate** always ends." (Le
    miroir de la règle « terminate toujours » du kernel.)

## Form event order

`PRE_SET_DATA` → `POST_SET_DATA` → `PRE_SUBMIT` → `SUBMIT` → `POST_SUBMIT`.

!!! tip "Hook"
    Deux phases : **SET** (remplir le form depuis le modèle) puis **SUBMIT** (mapper
    la request dans le modèle). "**Set before Submit; Pre before Post.**"
    `PRE_SUBMIT` = données brutes de la request ; `SUBMIT` = normalisées.

## Data transformer direction

- **Affichage :** model → normalized → **view** (la chaîne dans l'input).
- **Soumission :** view → normalized → **model**.

!!! tip "Hook"
    "**Out to the eye, back to the model.**" (La view sort, le modèle rentre.)

## URL reference types

`ABSOLUTE_URL · ABSOLUTE_PATH (default) · RELATIVE_PATH · NETWORK_PATH`.

!!! tip "Hook"
    Le défaut est **ABSOLUTE_PATH** (`/blog/1`). "URL = full `https://…`; PATH = from
    root `/…`."

## IS_AUTHENTICATED ladder

`PUBLIC_ACCESS < IS_AUTHENTICATED_LAZILY < _REMEMBERED < _FULLY`.

!!! tip "Hook"
    "**Public → Lazy → Remembered → Fully.**" Les actions sensibles exigent **FULLY** ;
    remember-me n'atteint que **REMEMBERED**.

---

<small>Related: [Master Cheat Sheet](cheat-sheet.md) · [Top Certification Traps](traps.md) · [Revision Hub](index.md)</small>

## 🧠 Pour les nuls

**C'est quoi ?** Une collection de **mnémoniques** — des phrases ou acronymes faciles à retenir — pour graver dans la mémoire les ordres et listes que l'examen exige de connaître par cœur (ordre des événements, classes de statuts HTTP…).

**Pourquoi ça existe ?** Le cerveau retient mal une liste brute ("request, controller, controller_arguments, view, response…") mais retient très bien une phrase qui a du sens ("Really Cool Apps Validate Responses"). Un mnémonique transforme une liste arbitraire en une chose mémorisable.

**🏠 Analogie de la vraie vie :** C'est la technique qu'on utilise pour retenir l'ordre des **planètes du système solaire** ("Mon Vieux Tu M'as Jeté Sur Une Nouvelle Planète") : la phrase n'a aucun rapport avec l'astronomie, mais son ordre de mots colle exactement à l'ordre à retenir.

**Symfony dans la vraie vie :** Séquence Symfony brute (ex. les 7 événements du kernel) → phrase mnémonique associée (ex. "R-C-A-V-R-F-T") → au moment de l'examen, on se récite la phrase et on retrouve l'ordre exact.

**⚠️ Erreur fréquente :** Retenir la phrase mnémonique sans avoir compris ce que chaque lettre représente. Le mnémonique est un raccourci vers une compréhension déjà acquise, pas un substitut à cette compréhension — sinon, à l'examen, la phrase ne "débloque" plus rien.

**🧠 Comment le mémoriser :** *« Le mnémonique vient après la compréhension, jamais avant »* — apprends d'abord le mécanisme dans le chapitre, puis viens chercher ici l'accroche qui le fige en mémoire.


## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
