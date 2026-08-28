# Flashcards — Console

66 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

## 🧠 Pour les nuls

**C'est quoi ?** Un jeu de **66 flashcards** (question au recto, réponse au verso) sur Console. On lit la question, on répond mentalement, puis on tape pour révéler la réponse.

**Pourquoi ça existe ?** Se tester activement (essayer de répondre avant de voir la réponse) ancre l'information bien mieux que relire passivement un chapitre. Répété à intervalles espacés, c'est la technique de mémorisation la plus efficace connue.

**🏠 Analogie de la vraie vie :** Ce sont les **cartes-vocabulaire** utilisées pour apprendre une langue étrangère : un mot d'un côté, sa traduction de l'autre — on ne progresse qu'en essayant de deviner avant de retourner la carte.

**Symfony dans la vraie vie :** Recto de la carte → une question précise sur Console / Verso → la réponse avec sa justification et un lien vers la doc officielle / Cartes marquées "ratées" → à revoir en priorité au prochain passage.

**⚠️ Erreur fréquente :** Taper pour révéler la réponse trop vite, sans avoir vraiment tenté de répondre — cela transforme l'exercice en simple lecture, avec un gain de mémorisation presque nul.

**🧠 Comment le mémoriser :** *« Je réponds avant de retourner la carte »* — et je note les cartes ratées pour les revoir plus souvent que les autres (répétition espacée).

??? question "1. Which command runs when you execute `php bin/console` with no arguments?"
    **✅ list**

    The Application's default command is `list`, which prints all available commands grouped by namespace. `help` shows usage for a single command and must be given a name; `about` prints an environment summary; `debug:container` is a FrameworkBundle command. The classic trap is to assume `help` is the default — it is not.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "2. Which command is provided by an optional bundle (MakerBundle), not by Symfony core?"
    **✅ make:command**

    `make:*` generators ship with the optional symfony/maker-bundle dev dependency. `cache:clear` and `debug:router` come from FrameworkBundle, and `about` is a core Console command. Expecting `make:*` to be part of the core framework is a classic certification trick.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/bundles/SymfonyMakerBundle/index.html)

??? question "3. How does `bin/console` obtain the console Application in Symfony 8?"
    **✅ It returns a closure that the Runtime component executes to build the kernel and Application**

    bin/console requires vendor/autoload_runtime.php and returns a closure; the Runtime component reads $context (APP_ENV/APP_DEBUG), runs the closure to build the Kernel and FrameworkBundle Application, then calls Application::run(). There is no Application::create() factory, and the web front controller boots the HTTP kernel, not the console one.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/runtime.html)

??? question "4. What does `php bin/console ca:cl` do when the abbreviation is unambiguous?"
    **✅ Runs cache:clear via command-name abbreviation**

    Application::find() resolves unambiguous abbreviations (per namespace segment) to the full command name, so `ca:cl` maps to `cache:clear`. If more than one command matched, it would raise an ambiguity error instead — abbreviations only work when the prefix resolves to exactly one command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "5. Which commands exist in *every* Console application, independent of FrameworkBundle? (choose 2)"
    **✅ list ; completion**

    `list`, `help`, `about` and `completion` are core Console commands present in any Application, even a standalone one. `cache:clear` and `debug:container` are added by FrameworkBundle and only exist in a full-stack Symfony app. A frequent trap is believing `about` is a FrameworkBundle command — it is core Console.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "6. You want to inspect which service is registered for an autowired interface without rebuilding the cache. Which command fits?"
    **✅ debug:autowiring**

    `debug:autowiring` lists the types you can type-hint for autowiring and the service each resolves to — pure inspection, no cache rebuild. `cache:clear` rebuilds the container (a mutation, not inspection), `cache:warmup` fills caches without clearing, and `make:command` is a MakerBundle generator. Confusing the inspecting `debug:*` family with the rebuilding `cache:*` family is a common error.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "7. In Symfony 8 `bin/console` ends with `return static function (array $context): Application { ... };`. What consumes this returned closure?"
    **✅ The Runtime component (loaded via vendor/autoload_runtime.php), which invokes it with $context and calls run()**

    `require vendor/autoload_runtime.php` installs the SymfonyRuntime, which captures the closure the file returns, builds a runner, injects $context (from $_SERVER / env), invokes the closure to get the Application, and calls its run() method. PHP does not auto-run returned closures, the Kernel does not, and Composer's autoloader only maps classes to files. This inversion is what lets the same Runtime handle web and console entry points.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/runtime.html)

??? question "8. What integer value does `Command::INVALID` represent?"
    **✅ 2**

    The return constants are SUCCESS=0, FAILURE=1, INVALID=2. INVALID signals bad input/usage as opposed to a runtime failure (FAILURE=1). 255 is a shell convention for a general error but is not a Command constant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "9. In Symfony 8, what does an invokable command class require?"
    **✅ The #[AsCommand] attribute and an __invoke() method returning int**

    Invokable commands only need #[AsCommand] plus an __invoke() method returning int; they do not extend Command, yet still use its SUCCESS/FAILURE/INVALID constants for return codes. Autoconfiguration registers them, so no manual services.yaml tag is needed.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "10. How is a command normally registered in the service container?"
    **✅ Autoconfiguration tags #[AsCommand]/Command subclasses with 'console.command'**

    Autoconfiguration applies the console.command tag to any service carrying #[AsCommand] or extending Command; AddConsoleCommandPass then builds a ContainerCommandLoader mapping name→service id for lazy loading. Manual tagging is redundant, filename plays no role, and you do not call Application::add() yourself in a framework app.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

??? question "11. What must a command's execute()/__invoke() return in Symfony 8?"
    **✅ An int exit code**

    The returned int becomes the process exit code; returning void/null triggers a type error in Symfony 8. A Response belongs to HTTP controllers, and a bool is not accepted — use Command::SUCCESS/FAILURE/INVALID.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "12. Given an invokable command `public function __invoke(SymfonyStyle $io, #[Argument] string $name, #[Option] bool $force = false): int`, how are `$name` and `$force` mapped to the input definition?"
    **✅ $name becomes a REQUIRED argument; $force becomes a VALUE_NONE (boolean flag) option**

    The invokable adapter derives modes from the parameter: a #[Argument] with no default is REQUIRED; a #[Option] typed bool becomes a VALUE_NONE flag (present = true, absent = its default false). $name is not optional because it lacks a default, and $force is an option (declared with #[Option]), never an argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "13. Which statement about a modern invokable command is TRUE?"
    **✅ It does not extend Command, yet still uses Command::SUCCESS for the return value**

    An invokable command is a plain class; it does not extend Command, but the SUCCESS/FAILURE/INVALID constants are public class constants you can reference from anywhere. SymfonyStyle is injected by type-hint into __invoke(), and __invoke() is a normal (non-static) method. Assuming you must extend Command to reach the constants is the trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "14. A command's execute() ends with `$io->success('done');` and no return statement. What happens when it runs?"
    **✅ A TypeError — execute() is declared `: int` but returns null**

    execute() is typed `: int`, so falling off the end (returning null) is a fatal TypeError. SymfonyStyle::success() returns void, so it cannot supply the exit code. There is no implicit SUCCESS/INVALID default — you must explicitly `return Command::SUCCESS;`. Forgetting the return is a very common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "15. Which class collects the `console.command` tags and builds the lazy command loader?"
    **✅ AddConsoleCommandPass, which builds a ContainerCommandLoader (name → service id)**

    Symfony\\Component\\Console\\DependencyInjection\\AddConsoleCommandPass gathers every service tagged console.command and constructs a ContainerCommandLoader mapping each command name to its service id, so a command is instantiated only when its name is invoked. There is no CommandCompilerPass, commands are not instantiated eagerly at compile time, and Symfony 8 does not scan the filesystem for commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

??? question "16. When unit-testing a command with `CommandTester`, which call executes it and how do you assert the exit code?"
    **✅ $tester->execute([...]); then $tester->assertCommandIsSuccessful() or check $tester->getStatusCode()**

    CommandTester::execute(array $input) runs the command in-memory; getStatusCode() returns the int exit code and getDisplay() returns the captured output. assertCommandIsSuccessful() is the convenience assertion. There is no run() returning a Response (that is HTTP) nor a handle()/getExitCode() pair, and testing a command does not require the HTTP kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html#testing-commands)

??? question "17. What is the correct command lifecycle order?"
    **✅ configure → initialize → interact → execute**

    configure() runs in the constructor; then run() binds input and calls initialize(), interact() (only if interactive), input validation, and finally execute(). initialize() always precedes interact() so shared state is ready before prompting.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "18. When is interact() called?"
    **✅ Only when the input is interactive**

    interact() is skipped for non-interactive input (e.g. -n / --no-interaction), so it is the wrong place for mandatory logic. It runs after initialize(), never before it, and always before execute() — never after.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "19. Why declare the command name in #[AsCommand] rather than only in configure()?"
    **✅ It lets the command loader know the name without instantiating the class (lazy loading)**

    The attribute exposes name/aliases at compile time so ContainerCommandLoader maps name→id and instantiates the command only when invoked. Putting the name only in configure() (via setName()) would force the Application to construct every command just to learn its name, defeating lazy loading.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

??? question "20. A command declared with hidden: true …"
    **✅ Does not appear in `list` but can still be executed**

    The hidden flag only affects listing; the command stays registered and fully runnable by name or alias. It is not removed from the container and is not environment-scoped.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "21. Why can't you read an argument value inside configure()?"
    **✅ configure() runs in the constructor, before any input is bound**

    configure() is invoked from the Command constructor, long before run() binds the ArgvInput to the definition, so no argument values exist yet — configure() may only declare structure (name, arguments, options, help). Reading input there is a classic mistake; to act on values use initialize()/interact()/execute().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "22. A command sets `$this->io = new SymfonyStyle(...)` in initialize() and, in interact(), prompts for a missing `name` argument. Under `--no-interaction` with no `name` given, what happens?"
    **✅ interact() is skipped, so name stays null and validation fails for the required argument**

    With --no-interaction, interact() is not called, so the prompt never fills the missing value; input->validate() then throws for the missing REQUIRED argument. initialize() always runs regardless of interactivity, so $this->io is set. This is why prompts belong in interact() but must not be the only way to satisfy required input.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "23. What does `#[AsCommand(name: 'app:report:generate', aliases: ['app:report'], hidden: false)]` configure?"
    **✅ The primary name, an alternative name (alias), and that it appears in `list`**

    #[AsCommand] declares metadata: the canonical name, aliases (extra names that invoke the same command), and hidden (false = shown in list). It defines one command reachable by several names, not multiple commands, and aliases are names — not arguments or namespace filters.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "24. After moving the command name from #[AsCommand] into `setName()` in configure(), `bin/console list` becomes noticeably slower on a large app. Why?"
    **✅ The Application must now instantiate every command to learn its name, defeating lazy loading**

    When the name lives only in configure(), the ContainerCommandLoader can no longer map name→id at compile time, so the Application constructs each command just to read its name — eager instantiation. Keeping the name in #[AsCommand] preserves lazy loading. configure() is not called twice, and setName() does not touch the container cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/commands_as_services.html)

??? question "25. Which mode declares a valueless boolean flag option?"
    **✅ InputOption::VALUE_NONE**

    VALUE_NONE takes no value; the option is false unless present, then true. It cannot carry a default. VALUE_OPTIONAL/REQUIRED expect a value, and InputArgument::OPTIONAL is an argument mode, not an option mode.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "26. What is the integer value of InputOption::VALUE_IS_ARRAY?"
    **✅ 8**

    Option modes are VALUE_NONE=1, VALUE_REQUIRED=2, VALUE_OPTIONAL=4, VALUE_IS_ARRAY=8, VALUE_NEGATABLE=16. They are powers of two so they can be combined with a bitmask (e.g. VALUE_REQUIRED | VALUE_IS_ARRAY = 10).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "27. Which statement about an IS_ARRAY argument is correct?"
    **✅ There can be only one and it must be declared last**

    An array argument greedily consumes all remaining tokens, so only one is allowed and it must come last. It may be combined as IS_ARRAY | REQUIRED or IS_ARRAY | OPTIONAL. Declaring it first or having several would make positional parsing ambiguous.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "28. Which option mode adds a `--no-foo` counterpart to `--foo`?"
    **✅ InputOption::VALUE_NEGATABLE**

    VALUE_NEGATABLE (16) generates the --no- twin: the value is true with --foo, false with --no-foo, and its default otherwise. VALUE_NONE is a plain flag with no negation, and the array/optional modes are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "29. Which InputArgument mode value is OPTIONAL?"
    **✅ 2**

    Argument modes are REQUIRED=1, OPTIONAL=2, IS_ARRAY=4. Note these differ from option modes (where 2 is VALUE_REQUIRED) — mixing the two integer scales is a common exam trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "30. `$this->addOption('force', 'f', InputOption::VALUE_NONE, 'Force it', true);` throws when the command is built. Why?"
    **✅ A VALUE_NONE option cannot have a default value**

    A VALUE_NONE option is always false unless present (then true), so providing a default is meaningless and InputOption's constructor throws a LogicException. Passing null (or omitting the default) is correct. Shortcuts and descriptions are perfectly allowed together.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "31. In an invokable command, `#[Option] array $tags = []` on the __invoke() parameter produces which InputOption mode?"
    **✅ VALUE_IS_ARRAY (repeatable, e.g. --tags=a --tags=b), optional via the [] default**

    The invokable adapter maps an array-typed #[Option] to VALUE_IS_ARRAY, so the option is repeatable; the [] default makes it optional. A bool would map to VALUE_NONE, a scalar with no default to VALUE_REQUIRED. Arrays are valid for both options and (as the last) arguments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "32. Which is true about shortcuts like `-f`?"
    **✅ Shortcuts belong to options only; arguments have no shortcuts**

    Only options accept a shortcut (the 2nd argument of addOption); arguments are positional and have no shortcut. Shortcuts work for any option mode, not just VALUE_NONE, and are typically a single character (e.g. -f).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "33. What role does InputDefinition play during a command run?"
    **✅ $input->bind(definition) maps raw ArgvInput tokens to args/options; $input->validate() then throws if a REQUIRED value is missing**

    InputDefinition is the ordered set of InputArguments plus the map of InputOptions. run() calls $input->bind($definition) to match raw tokens, then $input->validate() throws a Console RuntimeException if a REQUIRED argument or VALUE_REQUIRED option value is absent. It does not execute the command or hold exit codes; help rendering is a separate use of the same definition.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "34. Which argument declaration order is INVALID?"
    **✅ A REQUIRED argument declared after an OPTIONAL one**

    Because arguments are positional, a REQUIRED argument may not follow an OPTIONAL one — the parser could not tell which token filled which slot. Required-then- optional is fine, a lone optional is fine, and an array argument (last) may follow a required scalar.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/input.html)

??? question "35. Which method returns the STDERR stream in a CLI command?"
    **✅ ConsoleOutputInterface::getErrorOutput()**

    getErrorOutput() lives on ConsoleOutputInterface, not the base OutputInterface — so guard with `instanceof ConsoleOutputInterface` before calling it, or you risk a fatal type error. SymfonyStyle exposes getErrorStyle() (not stderr()), and input has nothing to do with error streams.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "36. Which two arguments does SymfonyStyle require?"
    **✅ An InputInterface and an OutputInterface**

    SymfonyStyle wraps both input (for prompts like ask/confirm) and output (for styled writing), so its constructor is (InputInterface, OutputInterface). It creates its own QuestionHelper internally and needs neither an Application nor a Command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/style.html)

??? question "37. What does $output->section() return?"
    **✅ A ConsoleSectionOutput that can be overwritten or cleared independently**

    Output sections are independently re-writable regions (ConsoleSectionOutput): you can overwrite() or clear() one without disturbing others — the basis for multiple live progress bars. section() is only available on ConsoleOutputInterface (real CLI output).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "38. What is the difference between write() and writeln()?"
    **✅ writeln() appends a newline; write() does not**

    writeln() is write() plus a trailing line break; neither changes the target stream (both go to STDOUT unless you fetch the error output) and neither toggles colours. Both accept an optional verbosity mask as a second argument.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "39. Why can a SymfonyStyle instance be passed to a method type-hinted OutputInterface?"
    **✅ SymfonyStyle implements OutputInterface (it decorates the underlying output)**

    SymfonyStyle implements both StyleInterface and OutputInterface, decorating the wrapped output, so it satisfies an OutputInterface type-hint directly — no cast needed. OutputInterface is a full contract (write/writeln/verbosity), not a marker.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/style.html)

??? question "40. A command exports CSV to STDOUT so users can run `bin/console app:export > data.csv`, yet you still want a live progress message on screen. Where should the progress message go?"
    **✅ To STDERR via getErrorOutput(), keeping STDOUT clean for the piped CSV**

    Data belongs on STDOUT (what the redirection captures); status/progress belongs on STDERR, which still displays on the terminal when STDOUT is piped to a file. Writing progress to STDOUT would corrupt the CSV. This split-stream design is why getErrorOutput() exists.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "41. `execute(InputInterface $input, OutputInterface $output)` calls `$output->getErrorOutput()`. It works locally but fatals in a test. Likely cause?"
    **✅ The test passes a plain OutputInterface (e.g. BufferedOutput) that has no getErrorOutput(); guard with instanceof ConsoleOutputInterface**

    getErrorOutput() is declared on ConsoleOutputInterface, not the base OutputInterface. Real CLI runs inject a ConsoleOutput (which implements it), but tests often inject a BufferedOutput, so the call fatals. Guarding with `if ($output instanceof ConsoleOutputInterface)` fixes it. The method still exists in Symfony 8 and needs no setter.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "42. Which InputInterface method reports whether the command may prompt the user?"
    **✅ isInteractive()**

    InputInterface::isInteractive() returns false under -n/--no-interaction, and the runner uses it to decide whether interact() runs; guard prompts with it. isVerbose() is an output verbosity check, not interactivity, and there is no built-in 'interactive' argument/option to read.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console.html)

??? question "43. How does a classic command obtain the QuestionHelper?"
    **✅ $this->getHelper('question')**

    Helpers are fetched by their string name from the command's HelperSet, so getHelper('question') returns the QuestionHelper. QuestionHelper's constructor takes no input, there is no Application::question(), and SymfonyStyle exposes ask()/confirm() rather than a helper() accessor.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

??? question "44. Which question class offers a fixed list of selectable answers?"
    **✅ ChoiceQuestion**

    ChoiceQuestion presents a list of options and supports single or multi-select. Question is free text, ConfirmationQuestion is yes/no, and there is no HiddenQuestion class — hidden input is Question::setHidden(true).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

??? question "45. What does ProgressBar::setRedrawFrequency(100) do?"
    **✅ Redraws the bar only every 100 steps to reduce terminal I/O**

    Redraw throttling avoids expensive terminal writes on every micro-step — a performance knob, not cosmetic. The total is set via the constructor/ start($max), width is a separate format setting, and it never sleeps.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/progressbar.html)

??? question "46. Which class moves or hides the terminal cursor?"
    **✅ Symfony\Component\Console\Cursor**

    Cursor issues ANSI escape sequences to move/hide/show the cursor and clear lines. FormatterHelper formats text blocks, Table renders data, and ProgressBar shows progress — none of them is the cursor primitive.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/index.html)

??? question "47. Why can't an invokable command call `$this->getHelper('question')`?"
    **✅ It does not extend Command, so it has no HelperSet accessor — inject services or use SymfonyStyle instead**

    getHelper() is a protected method on the Command base class; an invokable command extends nothing, so it has no HelperSet accessor. The idiomatic solution is to type-hint SymfonyStyle in __invoke() (which wraps QuestionHelper) or inject the collaborators you need. getHelper() still exists for classic commands.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

??? question "48. You need the user to pick several roles at once from a list. How do you configure a ChoiceQuestion?"
    **✅ Create the ChoiceQuestion and call setMultiselect(true) so it returns an array of selections**

    ChoiceQuestion::setMultiselect(true) lets the user choose comma-separated values and returns them as an array. Without it, only one selection is returned. There is no MultiChoiceQuestion class, and passing an array default does not enable multiselect on its own.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/questionhelper.html)

??? question "49. How is the HelperSet organised and populated for a classic command?"
    **✅ The Application populates it with default helpers keyed by name (question, formatter, process, debug_formatter)**

    The Application seeds each command's HelperSet with default helpers, addressable by short string keys (question, formatter, process, debug_formatter), which is why getHelper('question') works. They are keyed by name, not FQCN, and are not autowired container services.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/helpers/index.html)

??? question "50. What is the dispatch order for a successful framework command?"
    **✅ COMMAND then TERMINATE**

    COMMAND fires before execution and TERMINATE always fires last. ERROR fires only when a Throwable is raised, so a successful run dispatches just COMMAND → TERMINATE (no ERROR).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "51. Which event lets you change the exit code regardless of outcome?"
    **✅ ConsoleEvents::TERMINATE**

    ConsoleTerminateEvent::setExitCode() runs on every command (success or failure) and is the last chance to alter the process exit code. COMMAND runs before execution, and SIGNAL only fires when a subscribed OS signal arrives.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "52. What exit code results from ConsoleCommandEvent::disableCommand()?"
    **✅ 113**

    Disabling the command in the COMMAND event skips execution and returns ConsoleCommandEvent::RETURN_CODE_DISABLED, which is 113 — neither SUCCESS (0), FAILURE (1), nor 255.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "53. Which interface lets a command react to OS signals such as SIGTERM?"
    **✅ SignalableCommandInterface**

    Implement SignalableCommandInterface's getSubscribedSignals() and handleSignal(); it requires the pcntl extension. SignalHandlerInterface and TerminableInterface do not exist for this, and EventSubscriberInterface is generic event wiring, not signal handling.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "54. A command's execute() throws a RuntimeException. What is the event sequence?"
    **✅ COMMAND → ERROR → TERMINATE (TERMINATE still runs after ERROR)**

    COMMAND fires before execution; the thrown Throwable triggers ERROR (ConsoleErrorEvent, where a listener can change the exit code or swap the exception); TERMINATE always fires last, even after an error. ERROR never runs before COMMAND, and it does not suppress TERMINATE.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "55. What is the correct signature of handleSignal() in Symfony 8's SignalableCommandInterface?"
    **✅ handleSignal(int $signal, int|false $previousExitCode = 0): int|false**

    handleSignal receives the signal number and the previous exit code, returning an int to set the exit code or false to let the process continue running. The method is named handleSignal (not onSignal), takes an int signal (not a Signal object), and returns int|false rather than a plain bool/void.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "56. When are ConsoleEvents actually dispatched?"
    **✅ Only when the Application has an EventDispatcher (as in the framework); a bare Console app fires none**

    ConsoleEvents require an EventDispatcher wired into the Application via setDispatcher(). The full-stack framework does this automatically, but a bare Console app without a dispatcher fires no COMMAND/ERROR/TERMINATE events. It is not environment-scoped, and command interfaces do not gate dispatching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "57. A command returns 300 as its exit code. What does the process actually exit with?"
    **✅ 44 — exit codes are clamped to 0–255 via % 256 (300 % 256 = 44)**

    POSIX exit codes are a single byte (0–255), so Symfony normalises out-of-range values with % 256; 300 % 256 = 44. It is not passed through, not capped at 255, and not coerced to FAILURE. By convention a signal-terminated process exits with 128 + signalNumber.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "58. What does `#[AsEventListener(event: ConsoleEvents::TERMINATE)]` on an `__invoke(ConsoleTerminateEvent $event)` class achieve?"
    **✅ Registers the class as a listener that runs after every command, able to read/set the exit code**

    #[AsEventListener] autoconfigures the class as an event listener for ConsoleEvents::TERMINATE, so __invoke() runs after every command with a ConsoleTerminateEvent exposing getExitCode()/setExitCode(). It is a console event, distinct from kernel.terminate, runs on success and failure alike, and does not define a command.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/console/events.html)

??? question "59. Which flag maps to VERBOSITY_VERY_VERBOSE?"
    **✅ -vv**

    -v is VERBOSE (64), -vv is VERY_VERBOSE (128), -vvv is DEBUG (256), and -q is QUIET (16). The number of v's maps directly to the level.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "60. What is the integer value of VERBOSITY_NORMAL?"
    **✅ 32**

    The constants are QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256. NORMAL is 32, not 0 (0 is not used) — memorising this 16/32/64/128/256 ladder is exam-critical.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "61. Where is the current verbosity level stored?"
    **✅ On the OutputInterface, set by the Application from the flags**

    The Application parses -v/-vv/-vvv/-q before dispatching and calls $output->setVerbosity(); verbosity is a property of the output, queried via isVerbose()/isDebug(). Reading it from the input is a classic mistake — the input carries the raw flags, but the resolved level lives on the output.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "62. A message written with VERBOSITY_VERBOSE is displayed at which levels?"
    **✅ -v, -vv and -vvv**

    A message prints when the current level is >= the message's level. VERBOSE is 64, so it shows at -v (64), -vv (128) and -vvv (256), but not at normal (32) or quiet (16).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "63. Which of these VERBOSITY constant/value pairs are correct? (choose 2)"
    **✅ VERBOSITY_QUIET = 16 ; VERBOSITY_DEBUG = 256**

    The ladder is QUIET=16, NORMAL=32, VERBOSE=64, VERY_VERBOSE=128, DEBUG=256, so QUIET=16 and DEBUG=256 are correct. NORMAL is 32 (not 0) and VERBOSE is 64 (not 100). The values are powers of two starting at 16.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "64. `$output->writeln('trace', OutputInterface::VERBOSITY_DEBUG);` — when is 'trace' printed?"
    **✅ Only at -vvv (DEBUG), because the line prints only when the current level >= DEBUG**

    The second argument is a verbosity mask; the line prints only if the output's current level is >= the message level. DEBUG (256) is the highest, so 'trace' appears only under -vvv. writeln does honour the mask, and the mask governs visibility, not colour.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "65. What does passing -q (VERBOSITY_QUIET) actually do?"
    **✅ It silences normal output but the command still runs and returns its exit code**

    -q sets QUIET (16), which suppresses normal output; the command executes fully and returns its real exit code (scripts can still branch on it). It does not skip execution, does not change interactivity (that is -n), and does not alter the exit code. Assuming -q skips work is a common trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

??? question "66. Which guard should wrap a full payload dump so it only shows at -vvv?"
    **✅ if ($output->isDebug()) { ... }**

    isDebug() is true only at -vvv (DEBUG=256), the right guard for the most verbose diagnostics. isVerbose() is true from -v upward (too broad here), isInteractive() is about prompting not verbosity, and isQuiet() is the opposite end of the scale.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/console/verbosity.html)

---

<small>Back to [Flashcards](index.md) · [Console](../../console/index.md)</small>
