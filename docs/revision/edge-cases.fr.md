# "What happens if…?" — les drills de cas limites

Les examens de niveau Expert vivent dans les cas limites : les situations où le
framework fait *autre chose* que ce que prédit la réponse naïve. Cette page est un
jeu de drills — 84 questions « What happens if…? » couvrant les 15 domaines du
syllabus, chacune cachant un comportement précis et vérifiable.

!!! tip "How to drill"
    Lisez la question, répondez **à voix haute** en une ou deux phrases —
    engagez-vous sur une réponse avant de regarder — puis cliquez pour révéler. Si
    votre réponse a manqué le mot clé (le code de statut, la classe d'exception, le
    défaut), ouvrez le chapitre lié et relisez-le. Se tromper puis se corriger bat
    à tous les coups l'à-peu-près correct.

## 🧠 Pour les nuls

**C'est quoi ?** Une série de questions **« Que se passe-t-il si… ? »** portant sur des situations limites — des cas où le comportement réel de Symfony/PHP surprend celui qui répondrait "logiquement" sans connaître l'implémentation.

**Pourquoi ça existe ?** Les questions de niveau Expert ne demandent pas "qu'est-ce que X" mais "que se passe-t-il quand X et Y se combinent d'une façon inhabituelle". Cette page entraîne spécifiquement ce réflexe.

**🏠 Analogie de la vraie vie :** C'est l'entraînement d'un **pilote d'avion en simulateur de panne** : on ne répète pas le vol normal, on répète des scénarios rares et précis (un moteur qui tombe en panne à tel moment) pour que la bonne réaction devienne un réflexe.

**Symfony dans la vraie vie :** Chaque question → un scénario limite précis (ex. deux `return` dans `try`/`finally`) / La réponse dépliable → le comportement réel de PHP/Symfony, avec le mécanisme qui l'explique, pas juste le résultat.

**⚠️ Erreur fréquente :** Répondre "au feeling" sans avoir formulé sa réponse à voix haute avant de cliquer. Le format encourage explicitement à s'engager sur une réponse d'abord — sauter cette étape réduit l'efficacité de l'entraînement à presque zéro.

**🧠 Comment le mémoriser :** *« Je réponds avant de cliquer, jamais après »* — un cas limite mal deviné puis corrigé se retient bien mieux qu'un cas limite lu passivement.


## PHP & Web Security

??? question "What happens if a `TypeError` is thrown inside a `catch (\Exception $e)` block's `try`?"
    Il n'est **pas attrapé** — `TypeError` étend `\Error`, qui se trouve sur une
    branche de la hiérarchie séparée de `\Exception`. Seul `catch (\Throwable)` (ou
    `\Error`/`TypeError` explicitement) l'attrape ; l'erreur non attrapée devient
    fatale.
    **Ref:** [Exceptions](../php-web-security/exceptions.md)

??? question "What happens if both `try` and `finally` contain a `return` statement?"
    Le `return` du `finally` **gagne** — il écrase la valeur déjà calculée dans le
    `try`. `finally` s'exécute toujours, même après un `return` ou une exception
    levée, donc un `return` à cet endroit avale silencieusement les deux.
    **Ref:** [Exceptions](../php-web-security/exceptions.md)

??? question "What happens if two traits used by the same class define a method with the same name?"
    Une **erreur fatale de collision** — PHP refuse de deviner. Vous devez la
    résoudre explicitement avec `insteadof` (en choisir un) ou `as` (aliaser
    l'autre) ; `as` peut aussi changer la visibilité. Notez que la méthode *propre*
    de la classe l'emporterait sur les deux traits.
    **Ref:** [Traits](../php-web-security/traits.md)

??? question "What happens if you call `new DateTime()` inside a namespaced file without importing it?"
    Une erreur fatale **"Class App\\…\\DateTime not found"**. Les noms de *classes*
    non qualifiés ne retombent jamais sur le namespace global — seuls les fonctions
    et les constantes le font. Utilisez `use DateTime;` ou écrivez `new \DateTime()`.
    **Ref:** [Namespaces](../php-web-security/namespaces.md)

??? question "What happens if a `match` expression receives a value no arm covers?"
    Elle lève **`\UnhandledMatchError`** — contrairement à `switch`, qui ne fait
    silencieusement rien sans `default`. Rappelez-vous que `match` compare aussi
    **strictement** (`===`), donc `match(0)` n'entrera pas dans une branche `'0'`.
    **Ref:** [PHP API & language features](../php-web-security/php-api.md)

??? question "What happens if you HTML-escape a user value and then print it inside a `<script>` block?"
    Vous pouvez toujours subir une XSS. L'échappement HTML ne neutralise que le
    contexte du balisage ; dans du JavaScript (ou une URL), ce sont d'autres
    caractères qui sont dangereux, il vous faut donc l'escaper **adapté au
    contexte** (p. ex. `|e('js')` de Twig).
    **Ref:** [Web security](../php-web-security/web-security.md)

## HTTP

??? question "What happens if you set a cookie after the body has started being output — native PHP vs HttpFoundation?"
    Le `setcookie()` natif échoue avec un avertissement **"headers already sent"**
    et le cookie n'est jamais envoyé. Avec HttpFoundation, les cookies sont mis en
    file dans le `ResponseHeaderBag` de la `Response` et n'émis qu'au moment de
    `Response::send()`, donc l'ordre de vos appels n'a pas d'importance — tant que
    rien n'affiche de sortie avant `send()`.
    **Ref:** [Cookies](../http/cookies.md)

??? question "What happens if you create a cookie with `SameSite=None` but without the `Secure` flag?"
    Les navigateurs **rejettent/abandonnent le cookie** — `SameSite=None` n'est
    accepté qu'en HTTPS avec `Secure=true`. C'est un piège favori parce que le code
    côté serveur s'exécute sans aucune erreur ; le cookie ne revient juste jamais.
    **Ref:** [Cookies](../http/cookies.md)

??? question "What happens if you call `$cookie->withSecure(true)` and don't reassign the result?"
    Rien — un **no-op silencieux**. L'objet `Cookie` de Symfony est immuable ;
    chaque méthode `with*()` retourne une **nouvelle instance** et laisse l'original
    intact. Vous devez écrire `$cookie = $cookie->withSecure(true)`.
    **Ref:** [Cookies](../http/cookies.md)

??? question "What happens to the response body when `prepare()` runs for a HEAD request or a 204/304 response?"
    Le body est **retiré** — ces responses ne doivent pas porter de contenu.
    `prepare()` (appelée par le kernel, rarement par vous) corrige aussi les
    incohérences de `Content-Type`/charset par rapport à la request.
    **Ref:** [Response](../http/response.md)

??? question "What happens if you call `getContent()` on an HttpClient response that returned a 404?"
    Il **lève une exception** (une `ClientException` pour les 4xx ; les 3xx/5xx
    lèvent leurs propres familles) — `getContent()`/`toArray()` lèvent sur tout
    3xx/4xx/5xx par défaut. Seule `getStatusCode()` ne lève jamais ; passez
    `false`/`throw: false` pour lire un body d'erreur.
    **Ref:** [HttpClient](../http/httpclient.md)

??? question "What happens if a POST request carries `_method=PUT` in its body by default?"
    Rien — la request reste un POST. `http_method_override` vaut **`false`** par
    défaut, donc `_method` est ignoré tant que vous ne l'activez pas ; même activé,
    le contournement ne s'applique qu'aux requests POST. `getMethod()` respecte le
    contournement, `getRealMethod()` jamais.
    **Ref:** [HTTP methods](../http/methods.md)

## Symfony Architecture

??? question "What happens if a `kernel.request` listener sets a response?"
    Le traitement de la request **court-circuite** : le controller n'est jamais
    résolu, et `kernel.controller`, `kernel.controller_arguments` et `kernel.view`
    sont tous sautés. La response passe quand même par `kernel.response` avant
    d'être envoyée.
    **Ref:** [Request handling](../architecture/request-handling.md)

??? question "What happens if a controller returns a non-`Response` value and no `kernel.view` listener converts it?"
    Le kernel lève une **`LogicException`** ("The controller must return a
    Response…") — pas un 200 silencieux. `kernel.view` ne fait qu'*offrir* la
    possibilité de construire une `Response` à partir de la valeur ; encore faut-il
    que quelqu'un la saisisse.
    **Ref:** [Request handling](../architecture/request-handling.md)

??? question "What happens if an exception is thrown and no `kernel.exception` listener sets a response?"
    L'exception est **relancée** et se manifeste en 500. En pratique, l'
    `ErrorListener` intégré (priorité **−128**, donc après vos listeners) rend une
    response d'erreur ; une response définie sur `kernel.exception` passe quand
    même par `kernel.response`.
    **Ref:** [Exception handling](../architecture/exception-handling.md)

??? question "What happens if your code extends a Symfony class marked `final` or relies on `@internal` API?"
    Cela peut casser à **n'importe quelle release** — le code `@internal` n'a
    **aucune garantie de BC** même quand il est `public` au sens PHP, et contourner
    `final` par héritage sort entièrement de la promesse. La promesse de BC ne
    couvre que l'API documentée, non interne et non expérimentale.
    **Ref:** [Backward-compatibility promise](../architecture/bc-promise.md)

??? question "What happens to the generated config files when you `composer remove` a package installed via Flex?"
    Flex **inverse la recipe** : l'enregistrement du bundle, les fichiers de config
    et les placeholders d'env qu'elle avait ajoutés sont retirés. `symfony.lock`
    (recipes) est mis à jour — ce fichier suit les recipes, tandis que
    `composer.lock` suit les versions des packages.
    **Ref:** [Flex](../architecture/flex.md)

## Controllers

??? question "What happens if a controller returns a plain string?"
    Une chaîne n'est pas une `Response`, donc **`kernel.view`** se déclenche ; sans
    listener pour la convertir vous obtenez une **`LogicException`**, pas une page
    contenant la chaîne. Retournez `new Response($string)` ou installez un listener
    de view.
    **Ref:** [Response](../controllers/response.md)

??? question "What happens if you call `$this->createNotFoundException()` but forget to `throw` it?"
    Rien ne s'interrompt — la méthode ne fait que **retourner** un objet
    `NotFoundHttpException` et l'exécution continue à la ligne suivante. Le 404
    n'arrive que quand vous le `throw` vous-même.
    **Ref:** [Error pages](../controllers/error-pages.md)

??? question "What happens to the firewall and the URL when you `forward()` to another controller?"
    Ni l'un ni l'autre ne change. `forward()` exécute une **sub-request interne** —
    `isMainRequest()` vaut `false`, le firewall de sécurité ne se ré-authentifie
    **pas**, aucun 3xx n'est envoyé, et l'URL du navigateur reste la même. Les
    données voyagent via les *attributes* de la sub-request, pas la query string.
    **Ref:** [Internal redirects (forwarding)](../controllers/internal-redirects.md)

??? question "What happens if you `addFlash()` and then `render()` in the same action instead of redirecting?"
    Le flash n'est pas consommé par ce render si le template ne le lit pas — il
    **persiste et apparaît à la request suivante**, apparemment sorti de nulle
    part. Les flashes sont conçus pour le motif redirect-puis-affichage ; c'est
    leur lecture (p. ex. `app.flashes`) qui les consomme.
    **Ref:** [Flash messages](../controllers/flash-messages.md)

??? question "What happens if you type-hint `Request` in a service's constructor?"
    Une erreur du container — `Request` a la **portée d'une request**, ce n'est pas
    un service, donc il ne peut pas être injecté par constructeur. Injectez
    **`RequestStack`** et appelez `getCurrentRequest()` au moment de l'usage (les
    controllers sont spéciaux : leurs *arguments d'action* peuvent recevoir la
    `Request` via un value resolver).
    **Ref:** [The Request](../controllers/request.md)

??? question "What happens if an uploaded file exceeds PHP's `post_max_size`?"
    Vous pouvez obtenir un **bag `files` vide sans aucune exception** — PHP jette
    le body trop volumineux avant que Symfony ne le voie. Vérifiez toujours que
    l'`UploadedFile` n'est pas null ; rappelez-vous aussi que
    `getClientOriginalName()`/`getClientMimeType()` sont contrôlés par le client et
    falsifiables.
    **Ref:** [File upload](../controllers/file-upload.md)

## Routing

??? question "What happens if two routes match the same URL?"
    Le router teste les routes dans l'ordre de déclaration et la **première
    correspondance gagne** — la seconde route n'est silencieusement jamais
    atteinte. Avec les attributs, utilisez `priority` pour réordonner ;
    `debug:router` montre l'ordre effectif.
    **Ref:** [Routing configuration](../routing/configuration.md)

??? question "What happens if the path matches a route but the HTTP method doesn't?"
    Un **405 Method Not Allowed** avec un header `Allow` listant les méthodes
    valides — pas un 404. Nuance bonus : `methods: ['GET']` correspond aussi
    automatiquement à **HEAD**, et un décalage de *scheme* déclenche une
    redirection au lieu d'un 405.
    **Ref:** [Routing methods](../routing/methods.md)

??? question "What happens if a URL matches a route's path but fails its `requirements` regex?"
    La route **ne correspond simplement pas** — vous obtenez un **404** (ou une
    autre route a sa chance), jamais un 400. Les requirements sont implicitement
    ancrées, donc ajouter `^`/`$` vous-même est une erreur ; la regex par défaut
    des placeholders, `[^/]+`, ne franchit jamais un slash.
    **Ref:** [Route requirements](../routing/requirements.md)

??? question "What happens if a route's `condition` expression evaluates to false?"
    La route est traitée comme **non correspondante → 404**, pas 403. Les
    conditions n'affectent que la **correspondance** — la *génération* d'URL les
    ignore complètement, donc `path()` générera volontiers une URL que le matcher
    refusera ensuite.
    **Ref:** [Route conditions](../routing/conditions.md)

??? question "What happens if you POST to `/blog/` when the route is defined as `/blog`?"
    Un **405** — la redirection automatique du slash final (301) ne s'applique
    qu'à **GET et HEAD**. Seules les requests à méthode safe sont redirigées vers
    la forme canonique ; les autres méthodes échouent plutôt que de perdre leur
    body dans une redirection.
    **Ref:** [Routing redirects](../routing/redirects.md)

??? question "What happens if you pass `generateUrl()` a parameter that isn't a route placeholder?"
    Il est ajouté en **query string** — les paramètres en trop ne sont jamais
    silencieusement abandonnés. Rappelez-vous aussi que le type de référence par
    défaut est **`ABSOLUTE_PATH`** (un chemin relatif à la racine), pas une URL
    complète.
    **Ref:** [URL generation](../routing/url-generation.md)

## Templating (Twig)

??? question "What happens if `path()` is called with a route name that doesn't exist?"
    Une **`RouteNotFoundException` au moment du rendu** — la génération d'URL dans
    les templates n'est pas vérifiée à la compilation. Et dans le corps d'un email,
    `path()` produit une URL *relative* qui casse dans les clients mail ; utilisez
    `url()` à cet endroit.
    **Ref:** [URLs in templates](../twig/urls.md)

??? question "What happens if an `{% include %}` with `ignore missing` hits an error *inside* the included template?"
    L'erreur **se propage quand même** — `ignore missing` ne supprime que la
    `LoaderError` d'un template inexistant, pas les erreurs de runtime dans un
    template qui existe. Passer une *liste* de templates rend le premier qui
    existe.
    **Ref:** [Includes](../twig/includes.md)

??? question "What happens to auto-escaping if the template is named `report.txt.twig`?"
    **Rien n'est échappé** — la stratégie d'échappement est choisie d'après
    l'*extension du fichier*, et `txt` correspond à aucun échappement.
    L'auto-escaping s'applique à l'**affichage** (`{{ }}`), pas quand une variable
    est définie avec `set`.
    **Ref:** [Auto-escaping](../twig/auto-escaping.md)

??? question "What happens if a child template that `extends` a parent prints markup outside of any block?"
    Une **erreur Twig** — un template qui en étend un autre ne peut définir que des
    blocks (`{% extends %}` doit venir en premier). De plus, un template ne peut
    faire `extends` que d'**un seul** parent mais `use` de plusieurs.
    **Ref:** [Template inheritance](../twig/inheritance.md)

??? question "What happens if you `{% set app = ... %}` in a template?"
    Votre variable locale **masque la globale `app`** pour le reste du template —
    `app.user`, `app.request`, etc. deviennent ce que vous avez défini.
    Rappelez-vous aussi que `app.user` vaut `null` pour les requests non
    authentifiées et que lire `app.session` *démarre* la session.
    **Ref:** [Twig globals](../twig/globals.md)

## Forms

??? question "What happens if you call `isValid()` on a form that was never submitted?"
    Une **`LogicException`** ("Cannot check if an unsubmitted form is valid") — pas
    `false`. Protégez toujours avec `$form->isSubmitted() && $form->isValid()`
    après `handleRequest()`.
    **Ref:** [Form handling](../forms/handling.md)

??? question "What happens if `handleRequest()` receives a request whose HTTP method doesn't match the form's `method` option?"
    La request est **silencieusement ignorée** — le form reste simplement non
    soumis, sans aucune erreur pour vous signaler le décalage. Bonus : pour PATCH,
    `clearMissing` vaut `false`, donc les champs absents du payload conservent leur
    valeur actuelle.
    **Ref:** [Form handling](../forms/handling.md)

??? question "What happens if you call `submit()` on a form that has already been submitted?"
    Il lève une **`AlreadySubmittedException`** — un form ne peut être soumis
    qu'une seule fois. Il en va de même pour la mutation d'un form soumis, p. ex.
    faire `add()` d'un enfant après la soumission.
    **Ref:** [Symfony Forms — direct submit](https://symfony.com/doc/8.0/forms.html)

??? question "What happens if you render fields manually and forget `form_rest()` (so no `_token` is printed)?"
    La soumission suivante échoue à la validation CSRF — une erreur **"invalid
    token"** garantie, parce que la protection CSRF est activée par défaut et que
    le token est validé sur **PRE_SUBMIT**. `form_end()` vous sauve normalement en
    rendant les champs restants, sauf si vous avez passé `render_rest: false`.
    **Ref:** [Forms & CSRF](../forms/csrf.md)

??? question "What happens if a data transformer's `reverseTransform()` throws a `TransformationFailedException`?"
    Le form devient **invalide** avec l'`invalid_message` du champ — ce n'est *pas*
    un 500. Rappel de direction : `transform()` va du modèle vers la view
    (affichage) ; `reverseTransform()` de la view vers le modèle (soumission).
    **Ref:** [Data transformers](../forms/data-transformers.md)

??? question "What happens if a form listener tries to `add()` a field during `POST_SUBMIT`?"
    Cela échoue — on ne peut pas ajouter d'enfants à un form déjà soumis (une
    `AlreadySubmittedException`). Les champs dynamiques doivent être ajoutés en
    **PRE_SET_DATA ou PRE_SUBMIT**, avant le binding ; la validation elle-même
    s'exécute comme un listener de POST_SUBMIT.
    **Ref:** [Form events](../forms/events.md)

## Data Validation

??? question "What happens if a property has `#[Assert\Email]` and the value is `null` or an empty string?"
    Elle **passe** — `Email`, `Url` et la plupart des constraints de format
    acceptent délibérément vide/null pour se composer avec des champs optionnels.
    Rejeter les vides est le travail de `NotBlank` (et `NotBlank ≠ NotNull` : `''`,
    `[]`, `'   '` échouent `NotBlank` mais passent `NotNull`).
    **Ref:** [Built-in constraints](../validation/built-in-constraints.md)

??? question "What happens if you validate with a group that no constraint on the object belongs to?"
    **Zéro violation** — l'objet semble valide parce que rien ne s'est exécuté.
    Passer un group custom n'inclut **pas** implicitement `Default` ; listez les
    deux (`['Default', 'registration']`) si vous voulez les deux. Les noms de
    groups sont sensibles à la casse.
    **Ref:** [Validation groups](../validation/groups.md)

??? question "What happens to a nested object's constraints if the parent property lacks `#[Assert\Valid]`?"
    Elles sont **entièrement sautées** — la validation ne cascade pas par défaut,
    même si la classe imbriquée est couverte de constraints. `Valid` n'est pas un
    group et ne change pas les groups ; il ne fait qu'activer la cascade.
    **Ref:** [Validation scopes](../validation/scopes.md)

??? question "What happens when the first group of a `GroupSequence` has a failing constraint?"
    Toutes les constraints **de ce group** s'exécutent quand même, puis la séquence
    **s'arrête** — les groups suivants ne sont jamais validés. Et la séquence est
    déclenchée en validant `Default` ; valider le group `{ClassName}` la contourne
    avec une exécution à plat.
    **Ref:** [Group sequence](../validation/group-sequence.md)

??? question "What happens if a custom validator calls `buildViolation()` but never `addViolation()`?"
    **Rien n'est enregistré** — `buildViolation()` retourne un builder et reste
    inerte tant que `addViolation()` ne le finalise pas. Rappelez-vous aussi que
    `atPath()` *ajoute* au chemin de propriété courant ; il ne réinitialise pas la
    racine.
    **Ref:** [Violations builder](../validation/violations-builder.md)

## Dependency Injection

??? question "What happens if you call `$container->get()` with the id of a private service?"
    Une **`ServiceNotFoundException`** — les services sont private par défaut
    depuis Symfony 4, et le container compilé ne les expose pas. Utilisez
    l'injection par constructeur, un service locator, ou le container de *test*
    (`self::getContainer()`) dans les tests.
    **Ref:** [The container](../dependency-injection/container.md)

??? question "What happens if autowiring finds two services implementing the type-hinted interface?"
    Une **erreur d'ambiguïté à la compilation** — jamais de choix silencieux.
    Corrigez avec un alias par défaut, un alias d'autowiring nommé (dont l'id est
    littéralement `Type $paramName`, donc le nom du paramètre doit correspondre),
    ou `#[Target]`.
    **Ref:** [Autowiring](../dependency-injection/autowiring.md)

??? question "What happens if a service constructor type-hints `string $apiKey` with autowiring on?"
    Une **erreur de compilation** — l'autowiring résout des *objets par type* et ne
    peut jamais deviner des scalaires. Fournissez la valeur via `bind`,
    `#[Autowire]`, ou un argument explicite. Et `%env(MAX)%` reste une **string**
    tant que vous n'ajoutez pas le processeur `int:`.
    **Ref:** [Parameters](../dependency-injection/parameters.md)

??? question "What happens if service A's constructor needs B and B's constructor needs A?"
    Le container lève une **`ServiceCircularReferenceException`** — les cycles par
    constructeur ne peuvent pas être instanciés. Cassez le cycle en rendant un côté
    `lazy` (un proxy diffère l'instanciation), en injectant un service locator, ou
    en passant une arête en injection par setter.
    **Ref:** [Lazy services](https://symfony.com/doc/8.0/service_container/lazy_services.html)

??? question "What happens if you tag a service with a custom tag and nothing else?"
    **Rien** — un tag est une métadonnée inerte tant qu'un consommateur (un
    argument `tagged_iterator`/`tagged_locator` ou une compiler pass) ne le
    collecte pas. Une `priority` de tag plus haute signifie plus tôt dans
    l'iterator.
    **Ref:** [Tags](../dependency-injection/tags.md)

??? question "What happens to the original service when another service decorates it?"
    Il est **renommé** et devient disponible via la référence spéciale `.inner`,
    tandis que le décorateur **reprend l'id d'origine** — les consommateurs n'en
    savent rien. Avec plusieurs décorateurs, la `decoration_priority` la plus haute
    est appliquée en premier, c'est-à-dire finit *au plus près de l'original*.
    **Ref:** [Decoration](../dependency-injection/decoration.md)

## Security

??? question "What happens if you call `getUser()` in a controller on a route with no authenticated user?"
    Elle retourne **`null`** — pas d'exception. Pareil en Twig : `app.user` vaut
    `null` pour les requests anonymes, protégez donc avant de déréférencer. Forcer
    l'authentification est le travail d'`access_control`/`#[IsGranted]`, pas de
    `getUser()`.
    **Ref:** [Users](../security/users.md)

??? question "What happens if every voter abstains on an `isGranted()` check?"
    L'accès est **refusé** — sauf si `allow_if_all_abstain: true` est configuré.
    Avec la stratégie `affirmative` par défaut, un seul grant suffit, mais zéro
    grant avec uniquement des abstentions retombe sur le refus ; et un
    `Voter::supports()` qui retourne `false` compte comme une abstention, pas un
    refus.
    **Ref:** [Voters](../security/voters.md)

??? question "What happens when an `AccessDeniedException` is thrown for a user who isn't authenticated at all?"
    L'**entry point** du firewall entre en jeu (p. ex. redirection vers le
    formulaire de login) — pas un 403 brut. Le 403 est réservé aux utilisateurs qui
    *sont* authentifiés mais n'ont pas la permission.
    **Ref:** [Authorization](../security/authorization.md)

??? question "What happens if you check `isGranted('ADMIN')` — without the `ROLE_` prefix — against a user who has `ROLE_ADMIN`?"
    **Refusé.** Le `RoleVoter` ignore silencieusement les attributs sans le préfixe
    `ROLE_` (il s'abstient), et sans rien pour accorder, la décision retombe sur le
    refus. `IS_AUTHENTICATED_*` et `PUBLIC_ACCESS` sont gérés par
    l'`AuthenticatedVoter` séparé, pas par le `RoleVoter`.
    **Ref:** [Roles](../security/roles.md)

??? question "What happens to a request whose URL matches no `access_control` rule?"
    L'accès est **autorisé** — aucune règle correspondante signifie aucune
    restriction, pas un refus implicite. Les règles sont évaluées de haut en bas et
    seule la **première correspondance** s'applique, donc l'ordre (et une règle
    fourre-tout finale, si vous voulez du refus par défaut) compte.
    **Ref:** [Access control](../security/access-control.md)

??? question "What happens on the next request if your user class's `isEqualTo()` returns `false` during refresh?"
    Le token est **invalidé** — une déconnexion silencieuse. `refreshUser()`
    s'exécute à **chaque request avec état** (jamais sur les firewalls
    `stateless: true`), et la vérification d'égalité est la façon dont Symfony
    décide si l'utilisateur en session est toujours le même.
    **Ref:** [User providers](../security/providers.md)

## HTTP Caching

??? question "What happens if you send a response without setting any `Cache-Control` header?"
    Symfony lui donne **`Cache-Control: no-cache, private`** — sûr par défaut, mais
    invisible pour les caches partagés. Vous devez opter explicitement avec
    `setPublic()` + `setMaxAge()`/`setSharedMaxAge()` pour la rendre cacheable.
    **Ref:** [Cache types](../http-caching/cache-types.md)

??? question "What happens if you call `setPublic()` and later `setPrivate()` on the same response?"
    Le **dernier appel gagne** et retire l'autre directive — vous ne pouvez jamais
    vous retrouver avec `public, private` ensemble. Nuance liée :
    `setSharedMaxAge()` marque aussi la response `public` pour vous.
    **Ref:** [Expiration](../http-caching/expiration.md)

??? question "What happens when `isNotModified($request)` finds the client's validators still match?"
    Elle **modifie la response en place** : le statut devient **304**, le body et
    les headers de contenu sont retirés — et elle retourne un `bool`, donc vous
    devez quand même faire `return $response` vous-même.
    **Ref:** [Validation](../http-caching/validation.md)

??? question "What happens if a conditional request carries both `If-None-Match` and `If-Modified-Since`?"
    L'**ETag prime** — un `Last-Modified` correspondant seul est ignoré si l'ETag
    diffère. De plus, les expressions d'ETag de `#[Cache]` sont hachées en
    SHA-256 ; la valeur brute de l'expression n'est jamais l'ETag.
    **Ref:** [Validation](../http-caching/validation.md)

??? question "What happens when a request with a session cookie reaches Symfony's `HttpCache`?"
    Elle **contourne le cache partagé** — `Cookie` et `Authorization` sont les
    `private_headers` par défaut, donc de telles requests sont traitées comme
    privées et vont au backend. C'est pourquoi un seul cookie de session peut
    discrètement tuer votre taux de hit.
    **Ref:** [Server-side caching (HttpCache)](../http-caching/server-side.md)

## Console

??? question "What happens to the exit code when a failing command is run with `-q`?"
    Rien — `-q` ne supprime que la sortie ; la commande s'exécute quand même et
    **retourne son vrai code de sortie**, donc la détection d'échec en CI continue
    de fonctionner. La verbosité vit sur l'objet de *sortie* (constantes
    16/32/64/128/256).
    **Ref:** [Verbosity](../console/verbosity.md)

??? question "What happens if `execute()` returns nothing?"
    Une erreur — en Symfony 8, `execute()` **doit retourner un `int`**
    (`Command::SUCCESS` = 0, `FAILURE` = 1, `INVALID` = 2) ; retourner `null`/void
    viole le type de retour. Les classes invokables `#[AsCommand]` n'étendent pas
    `Command` mais utilisent quand même ses constantes.
    **Ref:** [Custom commands](../console/custom-commands.md)

??? question "What happens if a command returns an exit code greater than 255?"
    Il **boucle modulo 256** — les codes de sortie sont bornés à la plage 0–255,
    donc retourner 256 ressemble à un succès (0) pour le shell. Aussi :
    `console.terminate` se déclenche même après une erreur, et `disableCommand()`
    produit le code **113**.
    **Ref:** [Console events](../console/events.md)

??? question "What happens to `interact()` when a command runs with `--no-interaction`?"
    Elle est **entièrement sautée** — `interact()` ne s'exécute que pour l'entrée
    interactive, et les arguments requis manquants échouent alors à la validation
    au lieu d'être demandés. Ordre du cycle de vie : `configure` → `initialize` →
    `interact` → validation → `execute`.
    **Ref:** [Command lifecycle](../console/configuration.md)

??? question "What happens if you give an `InputOption::VALUE_NONE` option a default value?"
    Une **`LogicException`** — une option `VALUE_NONE` est un pur drapeau
    (présence = `true`) et ne peut porter ni défaut ni valeur. Constantes de mode :
    `VALUE_NONE` 1, `VALUE_REQUIRED` 2, `VALUE_OPTIONAL` 4, `VALUE_IS_ARRAY` 8,
    `VALUE_NEGATABLE` 16.
    **Ref:** [Options & arguments](../console/options-arguments.md)

## Automated Tests

??? question "What happens if a test calls `createClient()` twice?"
    Le second appel **lève une exception** — un client par test (démarrer un second
    kernel entrerait en conflit). S'il vous faut plusieurs « navigateurs »,
    réutilisez le client ou séparez les méthodes de test.
    **Ref:** [Functional tests](../testing/functional-tests.md)

??? question "What happens after the client receives a 302 — does the next assertion see the target page?"
    Non — le client de test ne suit **pas les redirections par défaut**. Vous
    assertez la redirection (`assertResponseRedirects()`), puis appelez
    explicitement `$client->followRedirect()` (ou activez `followRedirects()` en
    amont).
    **Ref:** [The test client](../testing/client.md)

??? question "What happens to a service you replaced with `$container->set()` when the test makes a second request?"
    Il est **perdu** — le kernel redémarre entre les requests et reconstruit le
    container, jetant votre remplacement. Associez le remplacement à
    `$client->disableReboot()` pour le garder vivant d'une request à l'autre.
    **Ref:** [Framework objects in tests](../testing/framework-objects.md)

??? question "What happens if you call `getProfile()` without having called `enableProfiler()` before the request?"
    Elle retourne **`false`** (pas `null`, pas une exception) — dans
    l'environnement `test`, `profiler.collect` est désactivé par défaut, donc les
    profils n'existent que pour les requests qui ont opté avant.
    **Ref:** [Profiler in tests](../testing/profiler.md)

??? question "What happens if you call `text()` on a Crawler whose filter matched zero nodes?"
    Elle **lève une exception** — `text()`/`attr()` opèrent sur le premier nœud et
    échouent sur un ensemble vide, sauf si vous passez un argument par défaut. Le
    Crawler est immuable : `filter()` retourne une nouvelle instance, et le
    filtrage CSS nécessite le composant css-selector.
    **Ref:** [The Crawler](../testing/crawler.md)

## Miscellaneous

??? question "What happens to the callback passed to `CacheInterface::get()` when the item is already cached?"
    Il n'est **jamais exécuté** — le callback ne s'exécute que sur un miss, et sa
    valeur de retour est ce qui est mis en cache. La protection contre le stampede
    vient gratuitement via l'expiration anticipée probabiliste (`$beta` ; `INF`
    force le recalcul).
    **Ref:** [Cache](../miscellaneous/cache.md)

??? question "What happens when you translate a message id that has no translation in the current locale?"
    L'**id du message lui-même est retourné** — pas d'exception, pas
    d'avertissement dans la sortie. Le domaine par défaut est `messages`
    (`validators`/`security` sont séparés), et Symfony 8 utilise le format ICU
    MessageFormat pour les pluriels.
    **Ref:** [Translations & Intl](../miscellaneous/intl.md)

??? question "What happens if a `Process` started with `run()` takes longer than 60 seconds?"
    Il est tué avec une **`ProcessTimedOutException`** — le timeout par défaut est
    de 60 s ; passez `null` pour le désactiver. Aussi : les arguments en tableau
    sont auto-échappés, mais `fromShellCommandline()` ne l'est pas (risque
    d'injection), et `mustRun()` lève en cas d'échec là où `run()` retourne le code
    de sortie.
    **Ref:** [Process](../miscellaneous/process.md)

??? question "What happens to `.env.local` when the app runs in the `test` environment?"
    Il est **ignoré** — les tests doivent être reproductibles, donc les
    surcharges locales à la machine ne s'appliquent pas (utilisez
    `.env.test`/`.env.test.local`). Aussi : les vraies variables d'environnement de
    l'OS battent toujours les valeurs des `.env*`, et si `.env.local.php` existe,
    les fichiers `.env*` ne sont pas du tout analysés.
    **Ref:** [Configuration & environments](../miscellaneous/configuration.md)

??? question "What happens if you call `$lock->acquire()` while another process holds the lock?"
    Elle retourne **`false` immédiatement** — `acquire()` est non bloquante par
    défaut ; passez `true` pour bloquer. Les locks portent aussi un TTL (300 s par
    défaut), donc les longs jobs doivent `refresh()`, et
    `FlockStore`/`SemaphoreStore` ne protègent qu'une seule machine.
    **Ref:** [Lock](../appendices/out-of-syllabus/lock.md)

## Messenger

??? question "Que se passe-t-il si une classe de message n'a aucune entrée de routage dans `framework.messenger.transports` ?"
    Ce n'est **pas une erreur** — le message est traité **synchroniquement,
    en place**, exactement comme s'il était routé vers `sync://`
    explicitement. Le pipeline de middleware complet s'exécute quand même ;
    seul le saut vers un transport est sauté.
    **Réf. :** [Transports](../messenger/transports.md)

??? question "Que se passe-t-il avec le délai de retry calculé quand `retry_strategy.jitter` reste à sa valeur par défaut ?"
    Il est **randomisé de ±10 % environ** (la valeur par défaut du framework
    est `jitter: 0.1`), en plus du backoff exponentiel
    `delay × multiplier^tentative` — seul `jitter: 0` rend une progression
    `1000/2000/4000 ms` exacte.
    **Réf. :** [Retries & failures](../messenger/retries-failures.md)

??? question "Que se passe-t-il quand un handler lance `UnrecoverableMessageHandlingException` ?"
    Les retries sont **entièrement sautés** — l'enveloppe part directement
    vers le **transport d'échec**, quel que soit le nombre de tentatives
    restantes. À réserver aux erreurs structurelles qui échoueront toujours
    de la même façon, jamais aux erreurs transitoires.
    **Réf. :** [Retries & failures](../messenger/retries-failures.md)

??? question "Que se passe-t-il si on lit `$envelope->last(RedeliveryStamp::class)?->getRetryCount()` sur un message qui n'a jamais échoué ?"
    Cela vaut **`null`**, pas `0` — un message sans échec préalable ne porte
    aucun `RedeliveryStamp` du tout, donc son absence signifie elle-même
    « première tentative », jamais « zéro retry enregistré ».
    **Réf. :** [Retries & failures](../messenger/retries-failures.md)

??? question "Que se passe-t-il si le même message est délivré deux fois à un handler parce que la fenêtre de visibilité d'un worker lent a expiré en cours de traitement ?"
    C'est **prévu par conception** — le contrat de livraison de Messenger est
    **au moins une fois**, jamais exactement une fois. Rien dans le framework
    n'empêche une redélivrance ; seul un handler **idempotent** empêche un
    effet de bord dupliqué.
    **Réf. :** [Retries & failures](../messenger/retries-failures.md)

## Official References

- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Routing](https://symfony.com/doc/8.0/routing.html) · [Controllers](https://symfony.com/doc/8.0/controller.html) · [Forms](https://symfony.com/doc/8.0/forms.html) · [Validation](https://symfony.com/doc/8.0/validation.html)
- [Service container](https://symfony.com/doc/8.0/service_container.html) · [Security](https://symfony.com/doc/8.0/security.html) · [HTTP cache](https://symfony.com/doc/8.0/http_cache.html)
- [Console](https://symfony.com/doc/8.0/console.html) · [Testing](https://symfony.com/doc/8.0/testing.html) · [Twig](https://twig.symfony.com/doc/3.x/)
- [PHP manual](https://www.php.net/manual/en/) · [Certification syllabus](https://certification.symfony.com/exams/symfony.html)

---

<small>Related: [Top Certification Traps](traps.md) · [Easily Confused](confusions.md) · [Revision Hub](index.md)</small>
