# Console

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[CommandTester](../labs/console.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Le composant **Console** transforme une classe PHP en une véritable application en
ligne de commande. Dans une application Symfony, chaque invocation de
`php bin/console …` passe par lui : il analyse l'input, résout une `Command`,
pilote le cycle de vie **configure → initialize → interact → execute**, dispatche
les events console et retourne un code de sortie Unix. Il est en grande partie
autonome, mais il s'appuie sur le [service container](../dependency-injection/index.md)
pour l'enregistrement des commandes et le chargement lazy, ce qui explique sa place
après la DI dans la feuille de route.

!!! info "Stage at a glance"
    | Propriété | Valeur |
    |---|---|
    | **Prerequisites** | [Dependency Injection](../dependency-injection/index.md) |
    | **Level** | Advanced |
    | **Difficulty** | ★☆☆ |
    | **Dependencies** | Stage 4 (autoconfiguration, tags, lazy services) |
    | **Revision priority** | Medium |
    | **Est. time** | 2–3 h |

## Why this stage matters

L'outillage CLI est le territoire des cron jobs, des workers, des migrations et des
scripts de maintenance. L'examen teste la *mécanique* : quelle constante de retour
signifie le succès, en quoi les modes d'option diffèrent, dans quel ordre les
méthodes du cycle de vie se déclenchent, et quelle constante de verbosité correspond
à `-vv`. Ce sont des faits précis et mémorisables — des points faciles si vous les
révisez, faciles à perdre si vous devinez.

Symfony 8 moderne privilégie les **commandes invokables** (`#[AsCommand]` sur une
classe avec une méthode `__invoke()` et des paramètres `#[Argument]` / `#[Option]`)
aux côtés du style classique `extends Command`. Les deux compilent vers le même
objet `Command` et le même cycle de vie, vous devez donc reconnaître l'une et
l'autre forme.

## Micro-chapters

Travaillez-les dans l'ordre :

- [ ] [Built-in commands & the Application](built-in-commands.md) — `about`,
  `list`, `help`, `cache:clear`, `debug:*`, comment `bin/console` démarre
  l'`Application`.
- [ ] [Custom commands](custom-commands.md) — `#[AsCommand]`, extension de `Command`,
  style invokable, `SUCCESS`/`FAILURE`/`INVALID`, autoconfiguration.
- [ ] [Command configuration](configuration.md) — nom, description, aide,
  alias, hidden ; `configure()` vs attribut ; chargement lazy.
- [ ] [Arguments & options](options-arguments.md) — modes `InputArgument` /
  `InputOption`, raccourcis, valeurs par défaut, flags négables.
- [ ] [Input & output](input-output.md) — `InputInterface`, `OutputInterface`,
  `SymfonyStyle`, sections de sortie, STDERR.
- [ ] [Helpers](helpers.md) — `QuestionHelper`, `ProgressBar`, `Table`,
  `FormatterHelper`, `Cursor`, le `HelperSet`.
- [ ] [Console events](events.md) — `ConsoleEvents::COMMAND` / `SIGNAL` / `ERROR`
  / `TERMINATE`, listeners, codes de sortie, gestion des signaux.
- [ ] [Verbosity levels](verbosity.md) — `-q`/`-v`/`-vv`/`-vvv`, les constantes
  `VERBOSITY_*`, `isVerbose()` et consorts.

## How to study it

1. Prenez vos repères avec les [built-in commands](built-in-commands.md) et le
   fonctionnement de l'`Application`.
2. Écrivez les vôtres avec les [custom commands](custom-commands.md) et la
   [configuration](configuration.md).
3. Maîtrisez le contrat d'entrée : [arguments & options](options-arguments.md).
4. Maîtrisez le contrat de sortie : [input & output](input-output.md) et
   [helpers](helpers.md).
5. Terminez par la mécanique transversale : [events](events.md) et
   [verbosity](verbosity.md).

---

<small>Related: [Dependency Injection](../dependency-injection/index.md) ·
[Symfony Architecture](../architecture/index.md) ·
[Automated Tests](../testing/index.md)</small>

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Le composant Console transforme une classe PHP en commande exécutable dans le terminal — `php bin/console ma:commande`.

**Pourquoi ça existe ?** Toute application a besoin de tâches qu'on lance à la main ou depuis un script (vider un cache, importer des données) — le composant Console fournit un cadre commun pour toutes ces tâches, avec arguments, options et retours d'erreur cohérents.

**🏠 Analogie de la vraie vie :** Un distributeur automatique. Tu tapes un code (la commande), éventuellement des options (grande taille, sans sucre), et la machine exécute une procédure fixe et prévisible, puis affiche un message de succès ou d'échec.

**Symfony dans la vraie vie :** `php bin/console app:envoyer-rappels --limite=50` — `app:envoyer-rappels` est la commande, `--limite=50` est une option, et la classe `#[AsCommand]` correspondante exécute le travail.

**⚠️ Erreur fréquente :** renvoyer un entier arbitraire au lieu de `Command::SUCCESS`/`FAILURE`/`INVALID` — les scripts qui enchaînent des commandes (CI/CD) dépendent de ces codes précis.

**🧠 Comment le mémoriser :** "Une commande, c'est configure → initialize → interact → execute — toujours dans cet ordre."


## Official References

- [Symfony documentation — Console](https://symfony.com/doc/8.0/console.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
