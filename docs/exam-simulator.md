# Interactive Exam Simulator

!!! tip "In a nutshell"
    Practice against the real question bank the same way the certification works:
    **you only ever select answers — never type text or code.** Choose **Practice**
    for instant feedback and explanations, or **Exam** for the official shape
    (75 questions, 90 minutes, answers hidden until you submit) with a scored,
    reviewable report at the end.

!!! example "Real-world analogy"
    Think of Practice mode as sparring with a coach who stops after every punch to
    show you what to fix, and Exam mode as the real match: the bell rings, the clock
    runs, and you only hear the judges' scorecard once it's over.

!!! danger "Not an official exam"
    Every question in this simulator is a practice question, not an official exam
    question. This bank is community-authored and aligned with the syllabus — it
    is not sourced from, or reviewed by, the official Symfony 8 certification.

## 🧠 Pour les nuls

**C'est quoi cette page ?** Un entraînement interactif qui te fait vivre l'examen en conditions proches du réel, avec les mêmes types de questions.

**Pourquoi ça existe ?** Lire de la théorie ne suffit pas — s'entraîner sous forme de questions, avec un minuteur en mode Exam, habitue ton cerveau au format réel avant le jour J.

**🏠 Analogie de la vraie vie :** Un simulateur de vol pour un pilote. Le mode Practice, c'est l'instructeur qui corrige chaque geste immédiatement ; le mode Exam, c'est le vol solo minuté, sans filet, avec le score révélé seulement à l'atterrissage.

**Symfony dans la vraie vie :** Filtrer par domaine (par ex. "Security seulement") et par difficulté permet de cibler précisément ta zone faible, plutôt que de réviser tout au hasard.

**⚠️ Erreur fréquente :** croire que ces questions sont "officielles" — ce sont des questions d'entraînement inspirées du syllabus, jamais des questions réellement posées à l'examen.

**🧠 Comment le mémoriser :** "Practice corrige à chaque coup ; Exam attend la fin du combat pour révéler le score."

The three interaction types mirror the exam exactly:

- **True / False** — pick one of two options.
- **Single answer** — exactly one option is correct (radio buttons).
- **Multiple choice** — two or more options are correct; you must select *all* of
  them and nothing else to score the point (checkboxes).

Filter by topic area, difficulty, and question type, or hit **Full mock exam** to
jump straight into a timed 75-question simulation drawn from all 15 areas.

<div id="sf-quiz" data-src="../assets/quiz-data.json">
  <noscript>The interactive simulator needs JavaScript. Browse the
  <a href="../revision/quiz/">Practice Quiz Bank</a> and
  <a href="../revision/mock-exam/">Mock Exams</a> instead.</noscript>
</div>

!!! note "How scoring works"
    Multiple-choice questions are graded all-or-nothing, exactly like the real exam:
    a partially-correct selection earns zero. The pass mark shown (65%) is a
    community estimate for orientation, not an official figure — treat a comfortable
    margin above it as your target.

!!! tip "Weak-area memory"
    The simulator remembers your per-topic accuracy **in this browser**
    (`localStorage` — nothing leaves your device). Once you've answered a few
    questions, the setup screen shows your weakest areas and offers a
    **Drill my weaknesses** button that builds a practice session from exactly
    those topics. Use *Reset stats* to start fresh.
