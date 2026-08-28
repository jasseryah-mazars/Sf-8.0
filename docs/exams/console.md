# Chapter Exam — Console

!!! abstract "How to use"
    66 questions spanning every subchapter of **Console**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [Console](../console/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Cette page est une **banque de 66 questions type QCM** sur Console, avec correction dépliable sous chaque question. Ce n'est pas un cours : c'est un entraînement, à faire après avoir lu le chapitre.

**Pourquoi ça existe ?** Lire un chapitre donne l'impression d'avoir compris, mais répondre à une question sous forme d'examen (sans relire ses notes) révèle les vraies lacunes — c'est ce que fera l'examen officiel.

**🏠 Analogie de la vraie vie :** C'est le **permis de conduire**. Le code de la route (le cours) explique les règles ; les séries de questions du permis blanc (cette page) vérifient que tu sais les appliquer sous forme de question piège, sans l'aide du livre.

**Symfony dans la vraie vie :** Cours du chapitre → code de la route appris / Question du QCM → question du permis blanc / Réponse dépliable → correction avec explication / Score obtenu → indicateur "prêt à passer l'examen ou pas".

**⚠️ Erreur fréquente :** Déplier la réponse avant d'avoir vraiment tranché son choix. Le cerveau retient beaucoup mieux une explication lue *après* s'être trompé (ou avoir hésité) que lue en passant, sans effort de rappel préalable.

**🧠 Comment le mémoriser :** *« Je réponds d'abord, je vérifie ensuite »* — jamais l'inverse. Note les questions ratées : ce sont exactement les pièges que l'examinateur pose aussi.

---

**Q1.** Which command runs when you execute `php bin/console` with no arguments?  <small>_(easy · single)_</small>

- A. list
- B. help
- C. about
- D. debug:container

??? success "Answer Q1"
    **A**

    The Application's default command is `list`, which prints all available commands grouped by namespace. `help` shows usage for a single command and must be given a name; `about` prints an environment summary; `debug:container` is a FrameworkBundle command. The classic trap is to assume `help` is the default — it is not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q2.** Which command is provided by an optional bundle (MakerBundle), not by Symfony core?  <small>_(easy · trap)_</small>

- A. make:command
- B. cache:clear
- C. debug:router
- D. about

??? success "Answer Q2"
    **A**

    `make:*` generators ship with the optional symfony/maker-bundle dev dependency. `cache:clear` and `debug:router` come from FrameworkBundle, and `about` is a core Console command. Expecting `make:*` to be part of the core framework is a classic certification trick.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/SymfonyMakerBundle/index.html)

**Q3.** What integer value does `Command::INVALID` represent?  <small>_(easy · single)_</small>

- A. 2
- B. 0
- C. 1
- D. 255

??? success "Answer Q3"
    **A**

    The return constants are SUCCESS=0, FAILURE=1, INVALID=2. INVALID signals bad input/usage as opposed to a runtime failure (FAILURE=1). 255 is a shell convention for a general error but is not a Command constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q4.** What must a command's execute()/__invoke() return in Symfony 8?  <small>_(easy · single)_</small>

- A. An int exit code
- B. void
- C. A Response object
- D. A bool

??? success "Answer Q4"
    **A**

    The returned int becomes the process exit code; returning void/null triggers a type error in Symfony 8. A Response belongs to HTTP controllers, and a bool is not accepted — use Command::SUCCESS/FAILURE/INVALID.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q5.** A command declared with hidden: true …  <small>_(easy · single)_</small>

- A. Does not appear in `list` but can still be executed
- B. Cannot be executed at all
- C. Is removed from the container
- D. Only runs in the dev environment

??? success "Answer Q5"
    **A**

    The hidden flag only affects listing; the command stays registered and fully runnable by name or alias. It is not removed from the container and is not environment-scoped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q6.** What does `#[AsCommand(name: 'app:report:generate', aliases: ['app:report'], hidden: false)]` configure?  <small>_(easy · config)_</small>

- A. The primary name, an alternative name (alias), and that it appears in `list`
- B. Two independent commands sharing one class
- C. A required argument named app:report
- D. A namespace restriction so it only runs under app:report

??? success "Answer Q6"
    **A**

    #[AsCommand] declares metadata: the canonical name, aliases (extra names that invoke the same command), and hidden (false = shown in list). It defines one command reachable by several names, not multiple commands, and aliases are names — not arguments or namespace filters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q7.** Which mode declares a valueless boolean flag option?  <small>_(easy · single)_</small>

- A. InputOption::VALUE_NONE
- B. InputOption::VALUE_OPTIONAL
- C. InputOption::VALUE_REQUIRED
- D. InputArgument::OPTIONAL

??? success "Answer Q7"
    **A**

    VALUE_NONE takes no value; the option is false unless present, then true. It cannot carry a default. VALUE_OPTIONAL/REQUIRED expect a value, and InputArgument::OPTIONAL is an argument mode, not an option mode.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q8.** Which InputArgument mode value is OPTIONAL?  <small>_(easy · single)_</small>

- A. 2
- B. 1
- C. 4
- D. 8

??? success "Answer Q8"
    **A**

    Argument modes are REQUIRED=1, OPTIONAL=2, IS_ARRAY=4. Note these differ from option modes (where 2 is VALUE_REQUIRED) — mixing the two integer scales is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q9.** Which is true about shortcuts like `-f`?  <small>_(easy · trap)_</small>

- A. Shortcuts belong to options only; arguments have no shortcuts
- B. Every argument automatically gets a one-letter shortcut
- C. Shortcuts are only for VALUE_NONE options
- D. Shortcuts must be exactly two characters

??? success "Answer Q9"
    **A**

    Only options accept a shortcut (the 2nd argument of addOption); arguments are positional and have no shortcut. Shortcuts work for any option mode, not just VALUE_NONE, and are typically a single character (e.g. -f).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q10.** Which two arguments does SymfonyStyle require?  <small>_(easy · single)_</small>

- A. An InputInterface and an OutputInterface
- B. An Application and a Command
- C. A QuestionHelper and an OutputInterface
- D. Only an OutputInterface

??? success "Answer Q10"
    **A**

    SymfonyStyle wraps both input (for prompts like ask/confirm) and output (for styled writing), so its constructor is (InputInterface, OutputInterface). It creates its own QuestionHelper internally and needs neither an Application nor a Command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/style.html)

**Q11.** What is the difference between write() and writeln()?  <small>_(easy · single)_</small>

- A. writeln() appends a newline; write() does not
- B. write() sends to STDERR, writeln() to STDOUT
- C. writeln() disables ANSI colours
- D. They are identical aliases

??? success "Answer Q11"
    **A**

    writeln() is write() plus a trailing line break; neither changes the target stream (both go to STDOUT unless you fetch the error output) and neither toggles colours. Both accept an optional verbosity mask as a second argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q12.** Which InputInterface method reports whether the command may prompt the user?  <small>_(easy · single)_</small>

- A. isInteractive()
- B. isVerbose()
- C. hasArgument('interactive')
- D. getOption('interaction')

??? success "Answer Q12"
    **A**

    InputInterface::isInteractive() returns false under -n/--no-interaction, and the runner uses it to decide whether interact() runs; guard prompts with it. isVerbose() is an output verbosity check, not interactivity, and there is no built-in 'interactive' argument/option to read.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q13.** Which question class offers a fixed list of selectable answers?  <small>_(easy · single)_</small>

- A. ChoiceQuestion
- B. Question
- C. ConfirmationQuestion
- D. HiddenQuestion

??? success "Answer Q13"
    **A**

    ChoiceQuestion presents a list of options and supports single or multi-select. Question is free text, ConfirmationQuestion is yes/no, and there is no HiddenQuestion class — hidden input is Question::setHidden(true).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

**Q14.** Which class moves or hides the terminal cursor?  <small>_(easy · single)_</small>

- A. Symfony\Component\Console\Cursor
- B. FormatterHelper
- C. Table
- D. ProgressBar

??? success "Answer Q14"
    **A**

    Cursor issues ANSI escape sequences to move/hide/show the cursor and clear lines. FormatterHelper formats text blocks, Table renders data, and ProgressBar shows progress — none of them is the cursor primitive.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/index.html)

**Q15.** Which flag maps to VERBOSITY_VERY_VERBOSE?  <small>_(easy · single)_</small>

- A. -vv
- B. -v
- C. -vvv
- D. -q

??? success "Answer Q15"
    **A**

    -v is VERBOSE (64), -vv is VERY_VERBOSE (128), -vvv is DEBUG (256), and -q is QUIET (16). The number of v's maps directly to the level.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q16.** What is the integer value of VERBOSITY_NORMAL?  <small>_(easy · single)_</small>

- A. 32
- B. 0
- C. 16
- D. 64

??? success "Answer Q16"
    **A**

    The constants are QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256. NORMAL is 32, not 0 (0 is not used) — memorising this 16/32/64/128/256 ladder is exam-critical.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q17.** Which guard should wrap a full payload dump so it only shows at -vvv?  <small>_(easy · single)_</small>

- A. if ($output->isDebug()) { ... }
- B. if ($output->isVerbose()) { ... }
- C. if ($input->isInteractive()) { ... }
- D. if ($output->isQuiet()) { ... }

??? success "Answer Q17"
    **A**

    isDebug() is true only at -vvv (DEBUG=256), the right guard for the most verbose diagnostics. isVerbose() is true from -v upward (too broad here), isInteractive() is about prompting not verbosity, and isQuiet() is the opposite end of the scale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q18.** How does `bin/console` obtain the console Application in Symfony 8?  <small>_(medium · internals)_</small>

- A. It returns a closure that the Runtime component executes to build the kernel and Application
- B. It calls Application::create() statically
- C. The web front controller instantiates it
- D. It parses services.yaml directly

??? success "Answer Q18"
    **A**

    bin/console requires vendor/autoload_runtime.php and returns a closure; the Runtime component reads $context (APP_ENV/APP_DEBUG), runs the closure to build the Kernel and FrameworkBundle Application, then calls Application::run(). There is no Application::create() factory, and the web front controller boots the HTTP kernel, not the console one.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/runtime.html)

**Q19.** What does `php bin/console ca:cl` do when the abbreviation is unambiguous?  <small>_(medium · single)_</small>

- A. Runs cache:clear via command-name abbreviation
- B. Fails — abbreviations are not supported
- C. Lists commands starting with 'ca'
- D. Clears only the 'cl' namespace

??? success "Answer Q19"
    **A**

    Application::find() resolves unambiguous abbreviations (per namespace segment) to the full command name, so `ca:cl` maps to `cache:clear`. If more than one command matched, it would raise an ambiguity error instead — abbreviations only work when the prefix resolves to exactly one command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q20.** Which commands exist in *every* Console application, independent of FrameworkBundle? (choose 2)  <small>_(medium · trap)_</small>

- A. list
- B. completion
- C. cache:clear
- D. debug:container

??? success "Answer Q20"
    **A, B**

    `list`, `help`, `about` and `completion` are core Console commands present in any Application, even a standalone one. `cache:clear` and `debug:container` are added by FrameworkBundle and only exist in a full-stack Symfony app. A frequent trap is believing `about` is a FrameworkBundle command — it is core Console.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q21.** You want to inspect which service is registered for an autowired interface without rebuilding the cache. Which command fits?  <small>_(medium · single)_</small>

- A. debug:autowiring
- B. cache:clear
- C. cache:warmup
- D. make:command

??? success "Answer Q21"
    **A**

    `debug:autowiring` lists the types you can type-hint for autowiring and the service each resolves to — pure inspection, no cache rebuild. `cache:clear` rebuilds the container (a mutation, not inspection), `cache:warmup` fills caches without clearing, and `make:command` is a MakerBundle generator. Confusing the inspecting `debug:*` family with the rebuilding `cache:*` family is a common error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q22.** In Symfony 8, what does an invokable command class require?  <small>_(medium · single)_</small>

- A. The #[AsCommand] attribute and an __invoke() method returning int
- B. It must extend Command
- C. It must implement CommandInterface
- D. It must be registered manually in services.yaml

??? success "Answer Q22"
    **A**

    Invokable commands only need #[AsCommand] plus an __invoke() method returning int; they do not extend Command, yet still use its SUCCESS/FAILURE/INVALID constants for return codes. Autoconfiguration registers them, so no manual services.yaml tag is needed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q23.** How is a command normally registered in the service container?  <small>_(medium · internals)_</small>

- A. Autoconfiguration tags #[AsCommand]/Command subclasses with 'console.command'
- B. You always add the 'console.command' tag manually
- C. You call Application::add() inside bin/console
- D. It is discovered purely by filename

??? success "Answer Q23"
    **A**

    Autoconfiguration applies the console.command tag to any service carrying #[AsCommand] or extending Command; AddConsoleCommandPass then builds a ContainerCommandLoader mapping name→service id for lazy loading. Manual tagging is redundant, filename plays no role, and you do not call Application::add() yourself in a framework app.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q24.** Given an invokable command `public function __invoke(SymfonyStyle $io, #[Argument] string $name, #[Option] bool $force = false): int`, how are `$name` and `$force` mapped to the input definition?  <small>_(medium · code)_</small>

- A. $name becomes a REQUIRED argument; $force becomes a VALUE_NONE (boolean flag) option
- B. Both become options; $name is VALUE_REQUIRED
- C. $name becomes an OPTIONAL argument; $force becomes VALUE_OPTIONAL
- D. $force becomes a REQUIRED argument because it has no shortcut

??? success "Answer Q24"
    **A**

    The invokable adapter derives modes from the parameter: a #[Argument] with no default is REQUIRED; a #[Option] typed bool becomes a VALUE_NONE flag (present = true, absent = its default false). $name is not optional because it lacks a default, and $force is an option (declared with #[Option]), never an argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q25.** Which statement about a modern invokable command is TRUE?  <small>_(medium · trap)_</small>

- A. It does not extend Command, yet still uses Command::SUCCESS for the return value
- B. It must extend Command to access SUCCESS/FAILURE
- C. It cannot use SymfonyStyle because it has no HelperSet
- D. It must implement __invoke() as static

??? success "Answer Q25"
    **A**

    An invokable command is a plain class; it does not extend Command, but the SUCCESS/FAILURE/INVALID constants are public class constants you can reference from anywhere. SymfonyStyle is injected by type-hint into __invoke(), and __invoke() is a normal (non-static) method. Assuming you must extend Command to reach the constants is the trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q26.** A command's execute() ends with `$io->success('done');` and no return statement. What happens when it runs?  <small>_(medium · debug)_</small>

- A. A TypeError — execute() is declared `: int` but returns null
- B. It silently exits 0 because success() returns 0
- C. It exits 2 (INVALID) automatically
- D. It loops until a return is added

??? success "Answer Q26"
    **A**

    execute() is typed `: int`, so falling off the end (returning null) is a fatal TypeError. SymfonyStyle::success() returns void, so it cannot supply the exit code. There is no implicit SUCCESS/INVALID default — you must explicitly `return Command::SUCCESS;`. Forgetting the return is a very common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q27.** When unit-testing a command with `CommandTester`, which call executes it and how do you assert the exit code?  <small>_(medium · code)_</small>

- A. $tester->execute([...]); then $tester->assertCommandIsSuccessful() or check $tester->getStatusCode()
- B. $tester->run() returns a Response you inspect
- C. $tester->handle() and read $tester->getExitCode()
- D. You must boot the full HTTP kernel and issue a request

??? success "Answer Q27"
    **A**

    CommandTester::execute(array $input) runs the command in-memory; getStatusCode() returns the int exit code and getDisplay() returns the captured output. assertCommandIsSuccessful() is the convenience assertion. There is no run() returning a Response (that is HTTP) nor a handle()/getExitCode() pair, and testing a command does not require the HTTP kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html#testing-commands)

**Q28.** What is the correct command lifecycle order?  <small>_(medium · internals)_</small>

- A. configure → initialize → interact → execute
- B. initialize → configure → execute → interact
- C. configure → interact → initialize → execute
- D. execute → configure → initialize → interact

??? success "Answer Q28"
    **A**

    configure() runs in the constructor; then run() binds input and calls initialize(), interact() (only if interactive), input validation, and finally execute(). initialize() always precedes interact() so shared state is ready before prompting.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q29.** When is interact() called?  <small>_(medium · single)_</small>

- A. Only when the input is interactive
- B. Always, before initialize()
- C. Only when --no-interaction is passed
- D. After execute()

??? success "Answer Q29"
    **A**

    interact() is skipped for non-interactive input (e.g. -n / --no-interaction), so it is the wrong place for mandatory logic. It runs after initialize(), never before it, and always before execute() — never after.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q30.** Why declare the command name in #[AsCommand] rather than only in configure()?  <small>_(medium · internals)_</small>

- A. It lets the command loader know the name without instantiating the class (lazy loading)
- B. configure() cannot set a name at all
- C. Attributes execute faster at runtime
- D. It is required for execute() to run

??? success "Answer Q30"
    **A**

    The attribute exposes name/aliases at compile time so ContainerCommandLoader maps name→id and instantiates the command only when invoked. Putting the name only in configure() (via setName()) would force the Application to construct every command just to learn its name, defeating lazy loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q31.** A command sets `$this->io = new SymfonyStyle(...)` in initialize() and, in interact(), prompts for a missing `name` argument. Under `--no-interaction` with no `name` given, what happens?  <small>_(medium · code)_</small>

- A. interact() is skipped, so name stays null and validation fails for the required argument
- B. interact() still runs and blocks waiting for input
- C. initialize() is also skipped, causing a null $this->io
- D. The command silently exits SUCCESS

??? success "Answer Q31"
    **A**

    With --no-interaction, interact() is not called, so the prompt never fills the missing value; input->validate() then throws for the missing REQUIRED argument. initialize() always runs regardless of interactivity, so $this->io is set. This is why prompts belong in interact() but must not be the only way to satisfy required input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q32.** After moving the command name from #[AsCommand] into `setName()` in configure(), `bin/console list` becomes noticeably slower on a large app. Why?  <small>_(medium · debug)_</small>

- A. The Application must now instantiate every command to learn its name, defeating lazy loading
- B. configure() is called twice per command
- C. setName() disables the container cache
- D. list rebuilds the cache when names are dynamic

??? success "Answer Q32"
    **A**

    When the name lives only in configure(), the ContainerCommandLoader can no longer map name→id at compile time, so the Application constructs each command just to read its name — eager instantiation. Keeping the name in #[AsCommand] preserves lazy loading. configure() is not called twice, and setName() does not touch the container cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q33.** What is the integer value of InputOption::VALUE_IS_ARRAY?  <small>_(medium · single)_</small>

- A. 8
- B. 2
- C. 4
- D. 16

??? success "Answer Q33"
    **A**

    Option modes are VALUE_NONE=1, VALUE_REQUIRED=2, VALUE_OPTIONAL=4, VALUE_IS_ARRAY=8, VALUE_NEGATABLE=16. They are powers of two so they can be combined with a bitmask (e.g. VALUE_REQUIRED | VALUE_IS_ARRAY = 10).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q34.** Which statement about an IS_ARRAY argument is correct?  <small>_(medium · trap)_</small>

- A. There can be only one and it must be declared last
- B. It must be declared first
- C. You may declare several per command
- D. It cannot be combined with REQUIRED

??? success "Answer Q34"
    **A**

    An array argument greedily consumes all remaining tokens, so only one is allowed and it must come last. It may be combined as IS_ARRAY | REQUIRED or IS_ARRAY | OPTIONAL. Declaring it first or having several would make positional parsing ambiguous.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q35.** Which option mode adds a `--no-foo` counterpart to `--foo`?  <small>_(medium · single)_</small>

- A. InputOption::VALUE_NEGATABLE
- B. InputOption::VALUE_NONE
- C. InputOption::VALUE_OPTIONAL
- D. InputOption::VALUE_IS_ARRAY

??? success "Answer Q35"
    **A**

    VALUE_NEGATABLE (16) generates the --no- twin: the value is true with --foo, false with --no-foo, and its default otherwise. VALUE_NONE is a plain flag with no negation, and the array/optional modes are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q36.** `$this->addOption('force', 'f', InputOption::VALUE_NONE, 'Force it', true);` throws when the command is built. Why?  <small>_(medium · debug)_</small>

- A. A VALUE_NONE option cannot have a default value
- B. The shortcut 'f' collides with a reserved global shortcut
- C. VALUE_NONE options require an array default
- D. Options may not have both a shortcut and a description

??? success "Answer Q36"
    **A**

    A VALUE_NONE option is always false unless present (then true), so providing a default is meaningless and InputOption's constructor throws a LogicException. Passing null (or omitting the default) is correct. Shortcuts and descriptions are perfectly allowed together.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q37.** Which argument declaration order is INVALID?  <small>_(medium · single)_</small>

- A. A REQUIRED argument declared after an OPTIONAL one
- B. A REQUIRED argument followed by an OPTIONAL one
- C. A single OPTIONAL argument
- D. A REQUIRED argument followed by an IS_ARRAY argument

??? success "Answer Q37"
    **A**

    Because arguments are positional, a REQUIRED argument may not follow an OPTIONAL one — the parser could not tell which token filled which slot. Required-then- optional is fine, a lone optional is fine, and an array argument (last) may follow a required scalar.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q38.** Which method returns the STDERR stream in a CLI command?  <small>_(medium · trap)_</small>

- A. ConsoleOutputInterface::getErrorOutput()
- B. OutputInterface::getErrorOutput()
- C. SymfonyStyle::stderr()
- D. InputInterface::getError()

??? success "Answer Q38"
    **A**

    getErrorOutput() lives on ConsoleOutputInterface, not the base OutputInterface — so guard with `instanceof ConsoleOutputInterface` before calling it, or you risk a fatal type error. SymfonyStyle exposes getErrorStyle() (not stderr()), and input has nothing to do with error streams.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q39.** What does $output->section() return?  <small>_(medium · single)_</small>

- A. A ConsoleSectionOutput that can be overwritten or cleared independently
- B. A new Application
- C. A SymfonyStyle instance
- D. A boolean

??? success "Answer Q39"
    **A**

    Output sections are independently re-writable regions (ConsoleSectionOutput): you can overwrite() or clear() one without disturbing others — the basis for multiple live progress bars. section() is only available on ConsoleOutputInterface (real CLI output).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q40.** Why can a SymfonyStyle instance be passed to a method type-hinted OutputInterface?  <small>_(medium · trap)_</small>

- A. SymfonyStyle implements OutputInterface (it decorates the underlying output)
- B. The Console component casts it automatically
- C. OutputInterface is a marker interface with no methods
- D. It cannot — SymfonyStyle is unrelated to OutputInterface

??? success "Answer Q40"
    **A**

    SymfonyStyle implements both StyleInterface and OutputInterface, decorating the wrapped output, so it satisfies an OutputInterface type-hint directly — no cast needed. OutputInterface is a full contract (write/writeln/verbosity), not a marker.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/style.html)

**Q41.** A command exports CSV to STDOUT so users can run `bin/console app:export > data.csv`, yet you still want a live progress message on screen. Where should the progress message go?  <small>_(medium · scenario)_</small>

- A. To STDERR via getErrorOutput(), keeping STDOUT clean for the piped CSV
- B. To STDOUT interleaved with the CSV rows
- C. To a log file only; the terminal cannot show it
- D. Nowhere — progress bars break redirection entirely

??? success "Answer Q41"
    **A**

    Data belongs on STDOUT (what the redirection captures); status/progress belongs on STDERR, which still displays on the terminal when STDOUT is piped to a file. Writing progress to STDOUT would corrupt the CSV. This split-stream design is why getErrorOutput() exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q42.** `execute(InputInterface $input, OutputInterface $output)` calls `$output->getErrorOutput()`. It works locally but fatals in a test. Likely cause?  <small>_(medium · debug)_</small>

- A. The test passes a plain OutputInterface (e.g. BufferedOutput) that has no getErrorOutput(); guard with instanceof ConsoleOutputInterface
- B. getErrorOutput() was removed in Symfony 8
- C. STDERR is unavailable during PHPUnit runs
- D. You must call setErrorOutput() first

??? success "Answer Q42"
    **A**

    getErrorOutput() is declared on ConsoleOutputInterface, not the base OutputInterface. Real CLI runs inject a ConsoleOutput (which implements it), but tests often inject a BufferedOutput, so the call fatals. Guarding with `if ($output instanceof ConsoleOutputInterface)` fixes it. The method still exists in Symfony 8 and needs no setter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q43.** How does a classic command obtain the QuestionHelper?  <small>_(medium · single)_</small>

- A. $this->getHelper('question')
- B. new QuestionHelper($input)
- C. $this->getApplication()->question()
- D. SymfonyStyle::helper()

??? success "Answer Q43"
    **A**

    Helpers are fetched by their string name from the command's HelperSet, so getHelper('question') returns the QuestionHelper. QuestionHelper's constructor takes no input, there is no Application::question(), and SymfonyStyle exposes ask()/confirm() rather than a helper() accessor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

**Q44.** What does ProgressBar::setRedrawFrequency(100) do?  <small>_(medium · single)_</small>

- A. Redraws the bar only every 100 steps to reduce terminal I/O
- B. Sets the total number of steps to 100
- C. Caps the bar width at 100 characters
- D. Sleeps 100 ms between steps

??? success "Answer Q44"
    **A**

    Redraw throttling avoids expensive terminal writes on every micro-step — a performance knob, not cosmetic. The total is set via the constructor/ start($max), width is a separate format setting, and it never sleeps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/progressbar.html)

**Q45.** You need the user to pick several roles at once from a list. How do you configure a ChoiceQuestion?  <small>_(medium · code)_</small>

- A. Create the ChoiceQuestion and call setMultiselect(true) so it returns an array of selections
- B. Use ConfirmationQuestion in a loop
- C. Pass an array as the default; multiselect is automatic
- D. Multiselect requires a separate MultiChoiceQuestion class

??? success "Answer Q45"
    **A**

    ChoiceQuestion::setMultiselect(true) lets the user choose comma-separated values and returns them as an array. Without it, only one selection is returned. There is no MultiChoiceQuestion class, and passing an array default does not enable multiselect on its own.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

**Q46.** How is the HelperSet organised and populated for a classic command?  <small>_(medium · internals)_</small>

- A. The Application populates it with default helpers keyed by name (question, formatter, process, debug_formatter)
- B. Each command builds its own empty HelperSet in configure()
- C. Helpers are keyed by their FQCN, not a short name
- D. The container autowires helpers into command properties

??? success "Answer Q46"
    **A**

    The Application seeds each command's HelperSet with default helpers, addressable by short string keys (question, formatter, process, debug_formatter), which is why getHelper('question') works. They are keyed by name, not FQCN, and are not autowired container services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/index.html)

**Q47.** What is the dispatch order for a successful framework command?  <small>_(medium · internals)_</small>

- A. COMMAND then TERMINATE
- B. TERMINATE then COMMAND
- C. ERROR then COMMAND
- D. COMMAND then ERROR

??? success "Answer Q47"
    **A**

    COMMAND fires before execution and TERMINATE always fires last. ERROR fires only when a Throwable is raised, so a successful run dispatches just COMMAND → TERMINATE (no ERROR).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q48.** Which event lets you change the exit code regardless of outcome?  <small>_(medium · single)_</small>

- A. ConsoleEvents::TERMINATE
- B. ConsoleEvents::COMMAND
- C. ConsoleEvents::SIGNAL
- D. It cannot be changed after execution

??? success "Answer Q48"
    **A**

    ConsoleTerminateEvent::setExitCode() runs on every command (success or failure) and is the last chance to alter the process exit code. COMMAND runs before execution, and SIGNAL only fires when a subscribed OS signal arrives.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q49.** Which interface lets a command react to OS signals such as SIGTERM?  <small>_(medium · single)_</small>

- A. SignalableCommandInterface
- B. SignalHandlerInterface
- C. TerminableInterface
- D. EventSubscriberInterface

??? success "Answer Q49"
    **A**

    Implement SignalableCommandInterface's getSubscribedSignals() and handleSignal(); it requires the pcntl extension. SignalHandlerInterface and TerminableInterface do not exist for this, and EventSubscriberInterface is generic event wiring, not signal handling.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q50.** When are ConsoleEvents actually dispatched?  <small>_(medium · trap)_</small>

- A. Only when the Application has an EventDispatcher (as in the framework); a bare Console app fires none
- B. Always, even in a standalone Console component with no dispatcher
- C. Only in the prod environment
- D. Only for commands that implement EventSubscriberInterface

??? success "Answer Q50"
    **A**

    ConsoleEvents require an EventDispatcher wired into the Application via setDispatcher(). The full-stack framework does this automatically, but a bare Console app without a dispatcher fires no COMMAND/ERROR/TERMINATE events. It is not environment-scoped, and command interfaces do not gate dispatching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q51.** What does `#[AsEventListener(event: ConsoleEvents::TERMINATE)]` on an `__invoke(ConsoleTerminateEvent $event)` class achieve?  <small>_(medium · config)_</small>

- A. Registers the class as a listener that runs after every command, able to read/set the exit code
- B. Registers a new console command named terminate
- C. Subscribes the class to HTTP kernel.terminate instead
- D. Runs the listener only when a command fails

??? success "Answer Q51"
    **A**

    #[AsEventListener] autoconfigures the class as an event listener for ConsoleEvents::TERMINATE, so __invoke() runs after every command with a ConsoleTerminateEvent exposing getExitCode()/setExitCode(). It is a console event, distinct from kernel.terminate, runs on success and failure alike, and does not define a command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q52.** Where is the current verbosity level stored?  <small>_(medium · trap)_</small>

- A. On the OutputInterface, set by the Application from the flags
- B. On the InputInterface
- C. On the Command instance
- D. In an environment variable only

??? success "Answer Q52"
    **A**

    The Application parses -v/-vv/-vvv/-q before dispatching and calls $output->setVerbosity(); verbosity is a property of the output, queried via isVerbose()/isDebug(). Reading it from the input is a classic mistake — the input carries the raw flags, but the resolved level lives on the output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q53.** A message written with VERBOSITY_VERBOSE is displayed at which levels?  <small>_(medium · single)_</small>

- A. -v, -vv and -vvv
- B. only -v
- C. normal and above
- D. -q and above

??? success "Answer Q53"
    **A**

    A message prints when the current level is >= the message's level. VERBOSE is 64, so it shows at -v (64), -vv (128) and -vvv (256), but not at normal (32) or quiet (16).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q54.** Which of these VERBOSITY constant/value pairs are correct? (choose 2)  <small>_(medium · multiple)_</small>

- A. VERBOSITY_QUIET = 16
- B. VERBOSITY_DEBUG = 256
- C. VERBOSITY_NORMAL = 0
- D. VERBOSITY_VERBOSE = 100

??? success "Answer Q54"
    **A, B**

    The ladder is QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256, so QUIET=16 and DEBUG=256 are correct. NORMAL is 32 (not 0) and VERBOSE is 64 (not 100). The values are powers of two starting at 16.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q55.** `$output->writeln('trace', OutputInterface::VERBOSITY_DEBUG);` — when is 'trace' printed?  <small>_(medium · code)_</small>

- A. Only at -vvv (DEBUG), because the line prints only when the current level >= DEBUG
- B. At every level, since a mask only affects colour
- C. At -v and above
- D. Never, because writeln ignores the second argument

??? success "Answer Q55"
    **A**

    The second argument is a verbosity mask; the line prints only if the output's current level is >= the message level. DEBUG (256) is the highest, so 'trace' appears only under -vvv. writeln does honour the mask, and the mask governs visibility, not colour.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q56.** What does passing -q (VERBOSITY_QUIET) actually do?  <small>_(medium · trap)_</small>

- A. It silences normal output but the command still runs and returns its exit code
- B. It skips execution entirely
- C. It forces the command into non-interactive mode
- D. It suppresses the exit code so the shell always sees 0

??? success "Answer Q56"
    **A**

    -q sets QUIET (16), which suppresses normal output; the command executes fully and returns its real exit code (scripts can still branch on it). It does not skip execution, does not change interactivity (that is -n), and does not alter the exit code. Assuming -q skips work is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

**Q57.** In Symfony 8 `bin/console` ends with `return static function (array $context): Application { ... };`. What consumes this returned closure?  <small>_(hard · code)_</small>

- A. The Runtime component (loaded via vendor/autoload_runtime.php), which invokes it with $context and calls run()
- B. PHP itself auto-executes any returned closure at end of file
- C. The Kernel's boot() method executes it
- D. Composer's autoloader executes it during class discovery

??? success "Answer Q57"
    **A**

    `require vendor/autoload_runtime.php` installs the SymfonyRuntime, which captures the closure the file returns, builds a runner, injects $context (from $_SERVER / env), invokes the closure to get the Application, and calls its run() method. PHP does not auto-run returned closures, the Kernel does not, and Composer's autoloader only maps classes to files. This inversion is what lets the same Runtime handle web and console entry points.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/runtime.html)

**Q58.** Which class collects the `console.command` tags and builds the lazy command loader?  <small>_(hard · internals)_</small>

- A. AddConsoleCommandPass, which builds a ContainerCommandLoader (name → service id)
- B. ContainerBuilder::compile() instantiates each command eagerly
- C. The Kernel's registerCommands() method scans the filesystem
- D. CommandCompilerPass, building an ArrayCommandLoader

??? success "Answer Q58"
    **A**

    Symfony\\Component\\Console\\DependencyInjection\\AddConsoleCommandPass gathers every service tagged console.command and constructs a ContainerCommandLoader mapping each command name to its service id, so a command is instantiated only when its name is invoked. There is no CommandCompilerPass, commands are not instantiated eagerly at compile time, and Symfony 8 does not scan the filesystem for commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

**Q59.** Why can't you read an argument value inside configure()?  <small>_(hard · trap)_</small>

- A. configure() runs in the constructor, before any input is bound
- B. configure() runs after execute(), so input is already consumed
- C. Arguments are only available to interact()
- D. You can — getArgument() works in configure()

??? success "Answer Q59"
    **A**

    configure() is invoked from the Command constructor, long before run() binds the ArgvInput to the definition, so no argument values exist yet — configure() may only declare structure (name, arguments, options, help). Reading input there is a classic mistake; to act on values use initialize()/interact()/execute().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

**Q60.** In an invokable command, `#[Option] array $tags = []` on the __invoke() parameter produces which InputOption mode?  <small>_(hard · code)_</small>

- A. VALUE_IS_ARRAY (repeatable, e.g. --tags=a --tags=b), optional via the [] default
- B. VALUE_NONE, because arrays are treated as flags
- C. VALUE_REQUIRED with a single string value
- D. It is rejected — arrays are only allowed for arguments

??? success "Answer Q60"
    **A**

    The invokable adapter maps an array-typed #[Option] to VALUE_IS_ARRAY, so the option is repeatable; the [] default makes it optional. A bool would map to VALUE_NONE, a scalar with no default to VALUE_REQUIRED. Arrays are valid for both options and (as the last) arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q61.** What role does InputDefinition play during a command run?  <small>_(hard · internals)_</small>

- A. $input->bind(definition) maps raw ArgvInput tokens to args/options; $input->validate() then throws if a REQUIRED value is missing
- B. It renders help text only and has no effect on parsing
- C. It executes the command after parsing
- D. It stores the exit code after execution

??? success "Answer Q61"
    **A**

    InputDefinition is the ordered set of InputArguments plus the map of InputOptions. run() calls $input->bind($definition) to match raw tokens, then $input->validate() throws a Console RuntimeException if a REQUIRED argument or VALUE_REQUIRED option value is absent. It does not execute the command or hold exit codes; help rendering is a separate use of the same definition.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

**Q62.** Why can't an invokable command call `$this->getHelper('question')`?  <small>_(hard · trap)_</small>

- A. It does not extend Command, so it has no HelperSet accessor — inject services or use SymfonyStyle instead
- B. getHelper() was removed in Symfony 8
- C. Helpers only exist for progress bars
- D. Invokable commands run without an Application

??? success "Answer Q62"
    **A**

    getHelper() is a protected method on the Command base class; an invokable command extends nothing, so it has no HelperSet accessor. The idiomatic solution is to type-hint SymfonyStyle in __invoke() (which wraps QuestionHelper) or inject the collaborators you need. getHelper() still exists for classic commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

**Q63.** What exit code results from ConsoleCommandEvent::disableCommand()?  <small>_(hard · single)_</small>

- A. 113
- B. 0
- C. 1
- D. 255

??? success "Answer Q63"
    **A**

    Disabling the command in the COMMAND event skips execution and returns ConsoleCommandEvent::RETURN_CODE_DISABLED, which is 113 — neither SUCCESS (0), FAILURE (1), nor 255.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q64.** A command's execute() throws a RuntimeException. What is the event sequence?  <small>_(hard · internals)_</small>

- A. COMMAND → ERROR → TERMINATE (TERMINATE still runs after ERROR)
- B. COMMAND → TERMINATE only (ERROR is skipped for RuntimeException)
- C. ERROR → COMMAND → TERMINATE
- D. ERROR only; the process aborts before TERMINATE

??? success "Answer Q64"
    **A**

    COMMAND fires before execution; the thrown Throwable triggers ERROR (ConsoleErrorEvent, where a listener can change the exit code or swap the exception); TERMINATE always fires last, even after an error. ERROR never runs before COMMAND, and it does not suppress TERMINATE.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q65.** What is the correct signature of handleSignal() in Symfony 8's SignalableCommandInterface?  <small>_(hard · code)_</small>

- A. handleSignal(int $signal, int|false $previousExitCode = 0): int|false
- B. handleSignal(Signal $signal): void
- C. handleSignal(int $signal): bool
- D. onSignal(int $signal, OutputInterface $output): int

??? success "Answer Q65"
    **A**

    handleSignal receives the signal number and the previous exit code, returning an int to set the exit code or false to let the process continue running. The method is named handleSignal (not onSignal), takes an int signal (not a Signal object), and returns int|false rather than a plain bool/void.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

**Q66.** A command returns 300 as its exit code. What does the process actually exit with?  <small>_(hard · scenario)_</small>

- A. 44 — exit codes are clamped to 0–255 via % 256 (300 % 256 = 44)
- B. 300 — Symfony passes it through unchanged
- C. 255 — anything above 255 becomes 255
- D. 1 — out-of-range codes fall back to FAILURE

??? success "Answer Q66"
    **A**

    POSIX exit codes are a single byte (0–255), so Symfony normalises out-of-range values with % 256; 300 % 256 = 44. It is not passed through, not capped at 255, and not coerced to FAILURE. By convention a signal-terminated process exits with 128 + signalNumber.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

---

<small>Back to [Chapter Exams](index.md) · [Console](../console/index.md)</small>
