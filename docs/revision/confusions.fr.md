# Easily Confused

L'examen est construit sur des **quasi-réussites** : deux choses qui se ressemblent,
une seule bonne réponse. Cette page est l'antidote — les paires que les candidats
confondent, côte à côte. Parcourez-la le matin de l'examen.

!!! abstract "How to use"
    Masquez la colonne de droite, lisez la gauche et énoncez la différence à voix
    haute. Si vous hésitez, ouvrez le chapitre lié.

## HTTP & responses

| Ça se ressemble | La distinction |
|---|---|
| **301 vs 302** | 301 = permanent (mis en cache/réutilisé) ; 302 = temporaire. Le défaut de `RedirectResponse` est **302**. |
| **307/308 vs 301/302** | 307/308 **conservent la méthode HTTP et le body** ; 301/302 peuvent basculer en GET. |
| **401 vs 403** | 401 = *non authentifié* (qui êtes-vous ?) ; 403 = *authentifié mais interdit*. |
| **404 vs 410** | 404 = introuvable (peut-être plus tard) ; 410 = disparu définitivement. |
| **`max-age` vs `s-maxage`** | `max-age` = tout cache ; `s-maxage` = caches **partagés** uniquement (y prime sur `max-age`) et implique `public`. |
| **ETag vs Last-Modified** | ETag = empreinte du contenu (exacte) ; Last-Modified = horodatage (résolution de 1 s). ETag **l'emporte** si les deux sont présents. |
| **`no-cache` vs `no-store`** | `no-cache` = peut stocker mais doit revalider ; `no-store` = ne jamais stocker du tout. |

## Architecture & kernel

| Ça se ressemble | La distinction |
|---|---|
| **`kernel.request` vs `kernel.controller`** | request s'exécute **avant** la résolution du controller ; controller s'exécute **après** et peut changer le callable. |
| **`kernel.view` vs `kernel.response`** | `view` ne se déclenche **que** si le controller retourne autre chose qu'une **Response** ; `response` se déclenche pour **chaque** response. |
| **`kernel.terminate` vs `kernel.response`** | response = avant l'envoi ; terminate = **après** l'envoi de la response (travail compatible asynchrone). |
| **Listener vs Subscriber** | Le listener est câblé via config/attribut ; le subscriber déclare ses propres events via `getSubscribedEvents()`. |

## Dependency Injection

| Ça se ressemble | La distinction |
|---|---|
| **Compile time vs runtime** | Le container est **compilé une fois** (passes, autowiring) puis dumpé ; `get()` a lieu au runtime depuis le container compilé. |
| **Autowiring vs Autoconfiguration** | Autowiring = injecter les **arguments** par type ; autoconfigure = appliquer des **tags/attributs** par interface. |
| **`#[Autowire]` vs binding** | `#[Autowire]` cible un argument ; `bind` (dans `_defaults`) en cible plusieurs par nom/type. |
| **Compiler pass registration** | Il n'existe **pas d'attribut `#[CompilerPass]`** — enregistrez-la dans `Kernel::build()` / le `build()` du bundle. |
| **`decoration_priority` direction** | Priorité plus haute = appliquée en **premier** = enveloppe la plus **externe**. `.inner` = le service décoré. |
| **Service locator vs injecting all** | Le locator = **lazy**, récupération à la demande ; tout injecter instancie tout immédiatement. |

## Security

| Ça se ressemble | La distinction |
|---|---|
| **Authentication vs Authorization** | AuthN = *qui êtes-vous* (firewall/authenticator) ; AuthZ = *avez-vous le droit* (access_control/voters). |
| **Badge vs Credentials** | `PasswordCredentials`/`CustomCredentials` vérifient des secrets ; les autres badges (`UserBadge`, `CsrfTokenBadge`…) ajoutent du contexte. |
| **Voter strategies** | affirmative = un GRANT suffit ; unanimous = un seul DENY fait perdre ; consensus = majorité. Défaut = **affirmative**. |
| **`ROLE_*` vs `IS_AUTHENTICATED_*`** | les rôles sont assignés ; `IS_AUTHENTICATED_*`/`PUBLIC_ACCESS` sont des attributs de runtime, pas des rôles. |
| **`access_control` order** | **la première correspondance gagne** (de haut en bas) — placez les chemins spécifiques au-dessus des généraux. |
| **Abstain ≠ Deny** | Un voter qui retourne ABSTAIN ne bloque pas ; seul DENY bloque (selon la stratégie). |

## Forms & validation

| Ça se ressemble | La distinction |
|---|---|
| **`PRE_SUBMIT` vs `PRE_SET_DATA`** | SET_DATA = modèle → form (pré-remplissage) ; SUBMIT = request → modèle (données entrantes). |
| **Model vs view data** | Model = votre objet ; view = la chaîne dans l'input. Les transformers convertissent entre les deux. |
| **`addModelTransformer` vs `addViewTransformer`** | model↔norm vs norm↔view. L'ordre compte ; le view transformer s'exécute au plus près du widget. |
| **`Default` vs `{ClassName}` group** | valider `Default` ≠ le group de la classe quand une `GroupSequence` existe sur la classe. |
| **`NotNull` vs `NotBlank`** | `NotNull` n'échoue que sur `null` ; `NotBlank` échoue aussi sur `''`, `[]`, `false`. |

## Routing & Twig

| Ça se ressemble | La distinction |
|---|---|
| **`path()` vs `url()`** | `path()` = relative ; `url()` = absolue (scheme+host). |
| **Reference types** | `ABSOLUTE_PATH` (par défaut), `ABSOLUTE_URL`, `NETWORK_PATH`, `RELATIVE_PATH`. |
| **`render()` vs `render_esi()`** | `render` intègre en ligne (sub-request immédiate) ; `render_esi` délègue à une gateway de cache/ESI. |
| **`{{ }}` vs `{% %}`** | `{{ }}` affiche une expression ; `{% %}` exécute un tag (logique). |
| **`|raw` risk** | désactive l'autoescaping → XSS si la valeur vient de l'utilisateur. |

## Console & testing

| Ça se ressemble | La distinction |
|---|---|
| **`SUCCESS/FAILURE/INVALID`** | 0 / 1 / 2. À retourner depuis `execute()`/`__invoke()`. |
| **Verbosity integers** | QUIET 16, NORMAL 32, VERBOSE 64, VERY_VERBOSE 128, DEBUG 256. |
| **`KernelTestCase` vs `WebTestCase`** | Kernel = démarrer le container/les services ; Web = faire en plus des requêtes HTTP via le client. |
| **Test container privacy** | `self::getContainer()` expose les services **private** (le vrai container non). |

---

<small>Related: [Top Certification Traps](traps.md) · [Memory Aids](memory-aids.md) · [Cheat Sheet](cheat-sheet.md)</small>

## Official References

- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
