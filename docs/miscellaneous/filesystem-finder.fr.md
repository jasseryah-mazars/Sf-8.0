# Filesystem & Finder Components

!!! tip "In a nutshell"
    Filesystem enveloppe les fonctions fichier de PHP avec des méthodes
    multiplateformes qui lèvent une exception en cas d'échec ; Finder est un
    builder fluide qui renvoie les fichiers correspondants sous forme de
    `SplFileInfo`. Point d'or pour l'examen : `dumpFile()` écrit de manière
    atomique (fichier temporaire + rename), et Finder exige toujours des
    répertoires via `in()`.

!!! example "Real-world analogy"
    Filesystem est un déménageur soigneux qui crie dès que quelque chose tourne mal
    plutôt que de laisser tomber un carton en silence (il lève une exception au lieu de
    retourner `false`). Son `dumpFile()` est comme un chef qui dresse entièrement un plat
    sur une assiette de côté et ne l'échange sur la table qu'ensuite, si bien qu'un
    convive n'aperçoit jamais une assiette à moitié dressée (l'écriture atomique
    fichier temporaire + rename). Finder est le bibliothécaire que vous envoyez chercher
    des livres : vous devez lui indiquer des salles et des rayons (`in()`), pas un livre
    unique, puis il filtre par titre, date ou taille et vous rend chaque correspondance
    sous forme de fiche étiquetée (un `SplFileInfo`).

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Effectuer des opérations fichier sûres avec la classe `Filesystem` et les helpers `Path`.
    - [ ] Construire des requêtes de fichiers fluides avec `Finder` (name/date/size/sort).
    - [ ] Itérer les résultats `SplFileInfo` et connaître les limites de Finder.

    **Syllabus:** `Miscellaneous → Filesystem & Finder` ·
    **Level:** Advanced ·
    **Est. time:** 30 min ·
    **Prerequisites:** [PHP](../php-web-security/index.md)

---

## Theory

**Filesystem** enveloppe les fonctions fichier de PHP avec des méthodes
multiplateformes levant des exceptions (écritures atomiques, copie/suppression
récursives). **Finder** est un builder fluide qui trouve les fichiers et
répertoires correspondant à des critères et les renvoie sous forme d'objets
`SplFileInfo`.

```php
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\Finder\Finder;

// Filesystem: cross-platform operations that throw on failure
$fs = new Filesystem();
$fs->mkdir('/tmp/reports');                    // recursive create
$fs->dumpFile('/tmp/reports/r.txt', 'done');   // atomic write

// Finder: fluent query yielding SplFileInfo objects
foreach ((new Finder())->files()->in('/tmp/reports')->name('*.txt') as $file) {
    echo $file->getFilename();
}
```

## Deep Dive — how it works internally

!!! question "Predict first"
    Vous pointez `Finder::in()` vers le chemin d'un **fichier** unique et vous
    itérez. Que se passe-t-il ?

??? note "Reveal"
    Une exception est levée — `Finder` cherche dans des **répertoires**, pas dans
    un fichier unique. Donnez-lui un répertoire et affinez avec `name()`/`path()` ;
    il n'existe pas de mode « chercher dans un seul fichier ».

### Filesystem

Les méthodes de `Symfony\Component\Filesystem\Filesystem` lèvent
`Symfony\Component\Filesystem\Exception\IOExceptionInterface` en cas d'échec au
lieu de retourner `false` :

| Method | Does |
|---|---|
| `exists($path)` | Teste l'existence (accepte array/iterable) |
| `mkdir($dirs, $mode)` | Création récursive |
| `copy($src, $dst, $overwrite)` | Copie un fichier |
| `remove($files)` | Suppression récursive |
| `dumpFile($path, $content)` | Écriture **atomique** (fichier temporaire + rename) |
| `appendToFile($path, $content)` | Ajout en fin de fichier |
| `rename($origin, $target)` | Déplacement/renommage |
| `symlink`, `chmod`, `chown` | Liens/permissions |

```php
use Symfony\Component\Filesystem\Exception\IOExceptionInterface;
use Symfony\Component\Filesystem\Filesystem;

$fs = new Filesystem();

try {
    $fs->mkdir('/srv/app/exports');                       // recursive create
    $fs->copy('in.csv', '/srv/app/exports/in.csv', true); // overwrite = true
    $fs->dumpFile('/srv/app/exports/status.txt', 'ok');   // atomic write
    $fs->remove(['/srv/app/exports/tmp', '/srv/old.lock']); // recursive delete
} catch (IOExceptionInterface $e) {
    echo 'Failed at '.$e->getPath(); // no silent false returns
}
```

`dumpFile()` écrit dans un fichier temporaire puis le renomme — les lecteurs ne
voient donc jamais un fichier à moitié écrit. Le helper statique
`Symfony\Component\Filesystem\Path` normalise et manipule des **chaînes** de
chemins sans toucher au disque : `Path::canonicalize()`, `Path::makeAbsolute()`,
`Path::makeRelative()`, `Path::join()`, `Path::isAbsolute()`.

```php
use Symfony\Component\Filesystem\Path;

// Pure string manipulation — nothing on disk is read or written
Path::canonicalize('/var/www/../log/./app.log'); // "/var/log/app.log"
Path::makeAbsolute('config/app.yaml', '/srv');   // "/srv/config/app.yaml"
Path::makeRelative('/srv/config', '/srv');       // "config"
Path::join('/srv', 'config', 'app.yaml');        // "/srv/config/app.yaml"
Path::isAbsolute('C:\\Programs');                // true (cross-platform aware)
```

### Finder

`Symfony\Component\Finder\Finder` construit une requête quasi immuable puis se
comporte comme un `IteratorAggregate` de
`Symfony\Component\Finder\SplFileInfo` :

```php
<?php
declare(strict_types=1);

use Symfony\Component\Finder\Finder;

$finder = (new Finder())
    ->files()
    ->in(__DIR__.'/var/log')
    ->name('*.log')
    ->notName('debug.log')
    ->size('> 1K')
    ->date('since yesterday')
    ->sortByModifiedTime();

foreach ($finder as $file) {
    // $file is a Finder SplFileInfo
    echo $file->getRelativePathname().' '.$file->getContents();
}
```

Builders clés : `files()`/`directories()`, `in($dirs)`, `name()/notName()`,
`contains()`, `path()`, `size()`, `date()`, `depth()`, `exclude()`,
`ignoreDotFiles()`, `ignoreVCS()`, `sortByName()/sortByModifiedTime()`,
`filter(callable)`. `count($finder)` donne le nombre de correspondances ;
`hasResults()` teste la non-vacuité.

```php
$finder = (new Finder())
    ->files()                                 // or directories()
    ->in([__DIR__.'/src', __DIR__.'/config']) // in() is mandatory
    ->name('*.php')->notName('*Test.php')
    ->contains('interface')                   // filter on file content
    ->path('Controller')                      // filter on the relative path
    ->depth('< 3')->exclude('vendor')
    ->ignoreDotFiles(true)->ignoreVCS(true)
    ->sortByName()                            // or sortByModifiedTime()
    ->filter(fn (\SplFileInfo $f) => $f->getSize() > 0);

count($finder);        // number of matches (Finder is Countable)
$finder->hasResults(); // true if anything matched
```

```mermaid
flowchart LR
    F[Finder] --> IN[in dirs] --> FL[filters: name/size/date] --> IT[iterate SplFileInfo]
```

!!! note "Source reference"
    `Symfony\Component\Finder\Finder` and `Filesystem::dumpFile()` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Finder.php).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    use Symfony\Component\Filesystem\Filesystem;
    use Symfony\Component\Filesystem\Path;

    $fs = new Filesystem();
    $target = Path::join(sys_get_temp_dir(), 'reports', 'r.txt');
    $fs->mkdir(Path::getDirectory($target));
    $fs->dumpFile($target, "generated\n"); // atomic
    ```

=== "Console"

    ```console
    $ php bin/console debug:container filesystem
    ```

=== "YAML"

    ```yaml
    # No YAML: these components are used in PHP, not configured via YAML.
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `dumpFile()` pour les écritures atomiques | `file_put_contents` pour les fichiers critiques |
| Attraper `IOExceptionInterface` | Ignorer les retours `false` silencieux |
| Utiliser `Path::join`/`canonicalize` pour la portabilité | Concaténer les chemins avec des `/` en dur |
| Délimiter le `Finder` avec `in()` + filtres | Charger des arborescences entières dans des tableaux |

## When (not) to use it / alternatives

Utilisez Filesystem/Finder pour les étapes de build, la rotation de logs, le
scan d'imports. `Finder` fonctionne sur le filesystem **local** (et les
streams) ; pour un stockage distant, utilisez une bibliothèque dédiée de type
flysystem (hors périmètre). Finder ne peut pas chercher dans un fichier unique —
il lui faut des répertoires via `in()`.

!!! danger "Certification traps"
    - Les méthodes de `Filesystem` **lèvent une exception** en cas d'erreur ; elles ne retournent pas `false`.
    - `dumpFile()` est **atomique** (fichier temporaire + rename) ; `appendToFile()` ne l'est pas.
    - `Path` manipule uniquement des chaînes — il ne touche **pas** au disque.
    - `Finder` renvoie son propre `SplFileInfo` avec `getRelativePathname()` ; vous devez appeler `in()`.
    - Un `Finder` ne peut pas être ré-itéré dans certains modes de source — reconstruisez-le si besoin.

!!! warning "Common mistakes"
    - Appeler `Finder::in()` sur le chemin d'un fichier au lieu d'un répertoire.
    - Oublier `files()`/`directories()` et obtenir les deux.

## Exercises

1. **(Advanced)** Écrivez atomiquement un fichier, en créant d'abord son répertoire parent.
2. **(Advanced)** Trouvez tous les fichiers `*.log` de plus de 1 Ko modifiés depuis hier,
   les plus récents en premier.

??? success "Solutions"

    **1.** Voir l'extrait `dumpFile()` ci-dessus (`mkdir` + `dumpFile`).

    **2.** Voir l'extrait `Finder` : `->files()->name('*.log')->size('> 1K')->date('since yesterday')->sortByModifiedTime()`.

## Certification questions

??? question "Q1. What makes `dumpFile()` safe against partial reads?"
    - [x] A. It writes to a temp file then atomically renames ✅
    - [ ] B. It locks the file with flock
    - [ ] C. It compresses the content

    **Why:** L'écriture temporaire + rename garantit que les lecteurs voient soit l'ancien contenu, soit le nouveau contenu complet.
    **Ref:** [Filesystem](https://symfony.com/doc/current/components/filesystem.html).

??? question "Q2. `Finder` requires which call to define where to search?"
    - [x] A. `in($dirs)` ✅
    - [ ] B. `from($dirs)`
    - [ ] C. `search($dirs)`

    **Why:** `in()` définit les répertoires de recherche ; sans lui, Finder lève une exception.
    **Ref:** [Finder](https://symfony.com/doc/current/components/finder.html).

??? question "Q3. On failure, `Filesystem::copy()`…"
    - [x] A. throws an `IOExceptionInterface` ✅
    - [ ] B. returns `false`
    - [ ] C. returns `null`

    **Why:** Les méthodes de Filesystem signalent les erreurs via des exceptions. **Ref:** [Filesystem](https://symfony.com/doc/current/components/filesystem.html#error-handling).

## Key takeaways

- Filesystem : opérations fichier multiplateformes qui lèvent des exceptions ; `dumpFile()` est atomique.
- Les helpers `Path` normalisent/joignent les chemins sans accès disque.
- Finder : `in()` + filtres fluides, renvoie des `SplFileInfo` ; exige des répertoires.

## Last-minute revision

!!! tip "Cheat sheet"
    - FS : `exists`, `mkdir`, `copy`, `remove`, `dumpFile`, `appendToFile`, `rename`.
    - `Path::canonicalize/join/makeAbsolute/makeRelative`.
    - Finder : `files()->in()->name()->size('> 1K')->date('since yesterday')->sortByModifiedTime()`.
    - `count()`, `hasResults()`, `getRelativePathname()`.

## Connections

- **Depends on:** les fonctions fichier de PHP — `Filesystem` les enveloppe avec des exceptions au lieu de retours `false`.
- **Reused in:** [Deployment](deployment.md) — étapes de build/scan ; [Process](process.md) — souvent associé pour lancer des commandes shell sur les fichiers découverts.
- **Confused with:** les fonctions brutes `glob()`/`scandir()` — Finder ajoute des filtres fluides et renvoie des `SplFileInfo`.

## Official References
- [Official docs — Filesystem](https://symfony.com/doc/current/components/filesystem.html)
- [Official docs — Finder](https://symfony.com/doc/current/components/finder.html)
- [Symfony source — Finder](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Finder/Finder.php)

## Video references

!!! tip "Watch & learn"
    Voici des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    "Symfony components" pour consolider ce chapitre. Nous lions des chaînes stables
    plutôt que des vidéos individuelles afin que les références ne se périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences SymfonyCon et keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/components/filesystem.html) — certaines pages de la doc Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** `dumpFile()` est atomique (fichier temporaire + rename)
- [ ] écrire des fichiers en toute sécurité et construire une requête `Finder` dans Symfony 8
- [ ] déboguer un `Finder` qui n'a rien trouvé (`in()` manquant, mauvais `files()`/`directories()`)
- [ ] repérer le piège : `Filesystem` lève une exception, il ne retourne pas `false` ; `Path` ne touche jamais au disque
- [ ] décrire comment Finder renvoie son propre `SplFileInfo` avec `getRelativePathname()`

---

<small>Related: [Process](process.md) · [Lock](lock.md) · [Deployment](deployment.md)</small>
