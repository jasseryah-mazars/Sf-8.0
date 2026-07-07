# Les fondamentaux de la sécurité web

!!! tip "In a nutshell"
    Chaque fonctionnalité de sécurité de Symfony défend contre une menace web
    concrète — apprenez les paires (XSS→échappement Twig, CSRF→token+SameSite,
    SQLi→requêtes préparées). Stockez les mots de passe uniquement avec
    `password_hash()` (bcrypt/argon2id), jamais avec de simples hachages.

!!! example "Real-world analogy"
    Sécuriser une application web, c'est comme sécuriser une maison, où chaque
    défense contre une intrusion précise. Vous ne répétez jamais mot pour mot ce
    qu'un inconnu crie par la boîte aux lettres (XSS contré par l'échappement
    Twig), vous vérifiez la pièce d'identité de quiconque prétend agir en votre
    nom (CSRF contré par le token plus SameSite), et vous posez des serrures
    inviolables au lieu de faire confiance à qui secoue la porte (injection SQL
    contrée par les requêtes préparées). Et vous conservez la clé non pas telle
    quelle mais sous forme d'empreinte à sens unique (`password_hash`), si bien
    qu'un cambrioleur qui photographie vos registres ne peut toujours pas la
    reconstituer.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Décrire XSS, CSRF, l'injection SQL, la fixation de session et le clickjacking.
    - [ ] Associer chaque menace à la fonctionnalité Symfony qui l'atténue.
    - [ ] Configurer les en-têtes de sécurité, HTTPS/HSTS et un stockage correct des mots de passe.

    **Syllabus:** `Web Security → Fundamentals` ·
    **Level:** Advanced / Expert ·
    **Est. time:** 40 min ·
    **Prerequisites:** [Exceptions](exceptions.md)

---

## Theory

Chaque fonctionnalité de sécurité de Symfony existe pour contrer une menace web
concrète. Connaître l'**attaque** rend la **défense** évidente. Ce chapitre pose
le modèle de menaces sur lequel s'appuie le reste de la plateforme ; la
configuration approfondie se trouve dans le
[Security stage](../security/index.md) et le [CSRF chapter](../forms/csrf.md).

| Menace | Définition en une ligne | Défense Symfony |
|---|---|---|
| XSS | Injecter un script dans une page | Auto-échappement Twig |
| CSRF | Request forgée depuis un utilisateur connecté | Tokens CSRF / SameSite |
| Injection SQL | Injecter du SQL via une entrée | Requêtes paramétrées |
| Fixation de session | Imposer un id de session connu | Régénération de l'id de session |
| Détournement de session | Voler un cookie de session | `Secure`/`HttpOnly`, HTTPS |
| Clickjacking | Encadrer le site de façon invisible | `X-Frame-Options`/CSP |

!!! question "Predict first"
    Un commentaire `<script>alert(1)</script>` est rendu avec `{{ comment }}`
    dans Twig. L'alerte se déclenche-t-elle ?

??? note "Reveal"
    Non. Twig l'auto-échappe en `&lt;script&gt;…`, affiché comme du texte
    littéral. Seul `{{ comment|raw }}` réintroduirait la XSS — réservez donc
    `|raw` au contenu que vous avez généré et assaini.

## Deep Dive — threats and mitigations

### XSS (Cross-Site Scripting)

Des données contrôlées par l'attaquant sont rendues comme du HTML/JS. Il existe
des variantes **réfléchies** (depuis la request), **stockées** (depuis la base
de données) et **DOM-based**. Le remède est un **encodage de sortie sensible au
contexte**. Twig auto-échappe pour le HTML par défaut ; `|raw` le désactive (à
n'utiliser que sur du contenu fiable et déjà sûr). Choisissez le bon contexte
d'échappement (`html`, `js`, `url`) — l'échappement HTML ne suffit **pas** à
l'intérieur d'un `<script>` ou d'une URL.

```twig
{# safe: auto-escaped #}
<p>{{ comment }}</p>
{# dangerous: only when the value is truly trusted #}
<p>{{ trustedHtml|raw }}</p>
```

### CSRF (Cross-Site Request Forgery)

Un site malveillant déclenche une request modifiant l'état en utilisant les
cookies de la victime. Défenses : un **token CSRF** imprévisible, validé côté
serveur (les Forms Symfony en ajoutent un automatiquement) et des cookies avec
**`SameSite=Lax/Strict`**. Les requests GET, sûres et idempotentes, ne doivent
jamais modifier l'état — cela seul supprime une grande surface d'attaque. Voir
[CSRF Protection](../forms/csrf.md).

### SQL injection

Concaténer une entrée dans du SQL permet à l'attaquant d'altérer la requête. Le
remède : les **requêtes préparées / le binding de paramètres** — jamais
d'interpolation de chaînes. Les applications Symfony utilisent PDO/DBAL avec des
paramètres liés, si bien que l'entrée est envoyée séparément du texte de la
requête et ne peut jamais en changer la structure.

```php
<?php
declare(strict_types=1);

// Parameterised — input can never alter the query structure.
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => $email]);
```

### Session fixation & hijacking

**Fixation :** l'attaquant fixe l'id de session de la victime avant le login,
puis le réutilise. Défense : **régénérer l'id de session à tout changement de
privilège** (login) — Symfony le fait automatiquement à l'authentification.
**Détournement (hijacking) :** vol du cookie ; atténué par `Secure` (HTTPS
uniquement), `HttpOnly` (pas d'accès JS) et `SameSite`.

```php
// Defeat fixation: new session id on login (Symfony does this for you)
$request->getSession()->migrate();

// Mitigate hijacking with cookie flags:
session_set_cookie_params([
    'secure'   => true,   // Secure: sent over HTTPS only
    'httponly' => true,   // HttpOnly: invisible to JavaScript
    'samesite' => 'Lax',  // SameSite: withheld on cross-site requests
]);
```

```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    U->>A: POST /login (valid creds)
    A->>A: authenticate()
    A->>A: session->migrate() (new id)
    A-->>U: Set-Cookie: PHPSESSID=NEW; Secure; HttpOnly; SameSite=Lax
```

### Clickjacking

Le site est chargé dans une `<iframe>` invisible superposée à une interface
appât. Défense : `X-Frame-Options: DENY` ou une Content-Security-Policy
`frame-ancestors 'none'`.

```php
// Either response header blocks framing:
$response->headers->set('X-Frame-Options', 'DENY');
$response->headers->set('Content-Security-Policy', "frame-ancestors 'none'");
```

### HTTPS, HSTS & security headers

Servez tout en TLS. **HSTS** (`Strict-Transport-Security`) indique aux
navigateurs de refuser le HTTP en clair pendant une période donnée. En-têtes de
response essentiels :

| En-tête | Rôle |
|---|---|
| `Strict-Transport-Security` | Forcer HTTPS (HSTS) |
| `Content-Security-Policy` | Restreindre les sources de scripts/styles/frames |
| `X-Content-Type-Options: nosniff` | Empêcher le MIME sniffing |
| `X-Frame-Options: DENY` | Anti-clickjacking |
| `Referrer-Policy` | Limiter la fuite du referer |

```php
$h = $response->headers;
$h->set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
$h->set('Content-Security-Policy', "default-src 'self'");
$h->set('X-Content-Type-Options', 'nosniff');
$h->set('X-Frame-Options', 'DENY');
$h->set('Referrer-Policy', 'same-origin');
```

### Password storage

Ne stockez jamais de texte en clair ni de hachages rapides (MD5/SHA1). Utilisez
un algorithme **lent, salé et adaptatif** — `password_hash()` avec
`PASSWORD_BCRYPT` ou `PASSWORD_ARGON2ID`. Le password hasher `'auto'` de Symfony
choisit le meilleur algorithme disponible et prend en charge le re-hachage
quand le coût change. Vérifiez avec `password_verify()` (temps constant).

```php
<?php
declare(strict_types=1);

$hash = password_hash($plain, PASSWORD_ARGON2ID);
$ok   = password_verify($plain, $hash);           // constant-time compare
```

!!! note "Source reference"
    Le `Symfony\Component\PasswordHasher\Hasher\SodiumPasswordHasher` de Symfony
    et les drapeaux de cookies CSRF de `HttpFoundation` implémentent ces
    défenses —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher).

## Configuration & code

=== "YAML"

    ```yaml
    # config/packages/framework.yaml
    framework:
        session:
            cookie_secure: auto      # Secure when on HTTPS
            cookie_httponly: true    # no JS access
            cookie_samesite: lax     # CSRF mitigation
    ```

=== "PHP (headers)"

    ```php
    <?php
    declare(strict_types=1);

    use Symfony\Component\HttpFoundation\Response;

    $response = new Response('OK');
    $response->headers->set('X-Frame-Options', 'DENY');
    $response->headers->set('X-Content-Type-Options', 'nosniff');
    ```

## Best practices & anti-patterns

| ✅ À faire | ❌ À éviter |
|---|---|
| Échapper la sortie dans le bon contexte | `|raw` sur une entrée utilisateur |
| Requêtes préparées/liées | Du SQL construit par chaînes |
| `password_hash` (bcrypt/argon2id) | MD5/SHA1/texte en clair |
| `SameSite` + tokens CSRF | Des requests GET modifiant l'état |

## When (not) to use it / alternatives

- Ne désactivez l'échappement Twig (`|raw`) que pour du contenu que vous avez
  généré et assaini.
- N'assouplissez `SameSite` à `None` que pour de véritables flux cross-site, et
  alors toujours avec `Secure`.
- La CSP est puissante mais facile à casser ; commencez en mode report-only
  avant de l'imposer.

!!! danger "Certification traps"
    - L'échappement HTML ne protège **pas** une valeur placée dans un `<script>`
      ou une URL — utilisez le bon contexte d'échappement.
    - Les tokens CSRF protègent les requests **modifiant l'état** ; ce n'est pas
      un mécanisme d'authentification.
    - L'id de session doit être **régénéré au login** pour bloquer la fixation
      (Symfony le fait automatiquement).
    - `HttpOnly` bloque l'accès JS au cookie (anti-vol par XSS) ; `Secure`
      impose HTTPS — ils résolvent des problèmes différents.
    - `password_hash()` intègre le sel dans le résultat — n'ajoutez pas le vôtre.

!!! warning "Common mistakes"
    - Comparer des hachages avec `==` (attaque temporelle) au lieu de
      `password_verify`/`hash_equals`.
    - Faire confiance au `Referer` ou à des champs cachés comme protection CSRF
      sans véritable token.

## Exercises

1. **(Advanced)** Étant donné `"<script>alert(1)</script>"` rendu via `{{ x }}`
   dans Twig, quelle est la sortie, et pourquoi est-elle sûre ?
2. **(Expert)** Réécrivez de façon sûre une requête vulnérable
   `"... WHERE id = $id"`.

??? success "Solutions"

    **1.** Twig auto-échappe en `&lt;script&gt;alert(1)&lt;/script&gt;`, que le
    navigateur affiche comme du texte littéral — le script ne s'exécute jamais.
    Seul `|raw` réintroduirait la vulnérabilité.

    **2.**
    ```php
    <?php
    $stmt = $pdo->prepare('SELECT * FROM item WHERE id = :id');
    $stmt->execute(['id' => $id]);   // structure fixed; input bound separately
    ```

## Certification questions

??? question "Q1. Twig's default protection against XSS is…"
    - [x] A. Context auto-escaping of variables ✅
    - [ ] B. Stripping all HTML tags
    - [ ] C. A CSP header
    - [ ] D. Encrypting output

    **Why:** Twig échappe la sortie en HTML par défaut ; `|raw` permet de s'en
    exclure.
    **Ref:** [Twig escaping](https://symfony.com/doc/current/templates.html#output-escaping).

??? question "Q2. Which best prevents SQL injection?"
    - [x] A. Prepared statements with bound parameters ✅
    - [ ] B. Escaping quotes with `addslashes`
    - [ ] C. A WAF only
    - [ ] D. HTML-escaping input

    **Why:** Le binding envoie les données séparément du SQL, si bien que
    l'entrée ne peut pas altérer la structure de la requête. **Ref:** [OWASP SQLi](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).

??? question "Q3. Session fixation is mitigated primarily by…"
    - [x] A. Regenerating the session id on login ✅
    - [ ] B. Longer session ids
    - [ ] C. Deleting cookies on logout only
    - [ ] D. Base64-encoding the id

    **Why:** Un nouvel id à l'authentification invalide tout id planté par un
    attaquant.
    **Ref:** [OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

??? question "Q4. Which header defends against clickjacking?"
    - [x] A. `X-Frame-Options: DENY` (or CSP `frame-ancestors`) ✅
    - [ ] B. `X-Content-Type-Options`
    - [ ] C. `Referrer-Policy`
    - [ ] D. `Accept-Language`

    **Why:** Il interdit que la page soit encadrée dans une frame. **Ref:** [OWASP clickjacking](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html).

??? question "Q5. The correct way to store passwords is…"
    - [x] A. `password_hash()` with bcrypt/argon2id ✅
    - [ ] B. SHA-256 with a static salt
    - [ ] C. MD5
    - [ ] D. Reversible encryption

    **Why:** Un hachage adaptatif et salé résiste à la force brute ; le sel est
    intégré au résultat.
    **Ref:** [password_hash](https://www.php.net/manual/en/function.password-hash.php).

## Key takeaways

- Chaque menace correspond à une défense Symfony — apprenez les paires.
- Échappez la sortie **selon le contexte** ; liez les paramètres SQL ;
  régénérez les sessions au login.
- Cookies : `Secure` + `HttpOnly` + `SameSite` ; ajoutez HSTS + CSP + `nosniff`.
- Stockez les mots de passe avec `password_hash` (bcrypt/argon2id), vérifiez en
  temps constant.

## Last-minute revision

!!! tip "Cheat sheet"
    - XSS→échappement Twig · CSRF→token+SameSite · SQLi→requêtes préparées.
    - Fixation→session migrate au login · Détournement→Secure/HttpOnly/HTTPS.
    - Clickjacking→`X-Frame-Options`/CSP `frame-ancestors`.
    - Mots de passe→`PASSWORD_ARGON2ID`/`BCRYPT` ; vérification avec `password_verify`.

## Connections

- **Depends on:** [Exceptions](exceptions.md) — une gestion d'erreurs maîtrisée évite de divulguer des détails internes aux attaquants.
- **Reused in:** [Security stage](../security/index.md) & [CSRF Protection](../forms/csrf.md) — là où ces menaces reçoivent une configuration Symfony concrète.
- **Confused with:** [authentication](../security/authentication.md) — les tokens CSRF protègent les requests modifiant l'état, ils n'identifient pas l'utilisateur.

## Official References
- [Symfony — Security](https://symfony.com/doc/current/security.html)
- [Symfony — CSRF](https://symfony.com/doc/current/security/csrf.html)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [PHP — password_hash](https://www.php.net/manual/en/function.password-hash.php)
- [Symfony source — PasswordHasher](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/PasswordHasher)

## Video references

!!! tip "Watch & learn"
    Voici des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « PHP & web security » pour consolider ce chapitre. Nous lions des chaînes
    stables plutôt que des vidéos individuelles afin que les références ne se
    périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — des tutoriels scénarisés à coder en suivant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences et keynotes des SymfonyCon.
    - [Official docs for this topic](https://symfony.com/doc/current/templates.html#output-escaping) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** chaque menace existe et la défense Symfony qui lui correspond
- [ ] configurer les drapeaux du cookie de session, les en-têtes de sécurité et `password_hash` dans Symfony 8
- [ ] déboguer une XSS causée par `|raw` ou un mauvais contexte d'échappement
- [ ] repérer le piège : échapper en HTML une valeur placée dans `<script>` ou une URL
- [ ] expliquer comment la régénération de l'id de session au login bloque la fixation

---

<small>Related: [Security stage](../security/index.md) · [CSRF Protection](../forms/csrf.md) · [Exceptions](exceptions.md)</small>
