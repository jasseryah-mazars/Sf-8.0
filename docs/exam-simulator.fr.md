# Interactive Exam Simulator

!!! tip "In a nutshell"
    Entraînez-vous sur la vraie banque de questions, exactement comme à la
    certification : **vous ne faites que sélectionner des réponses — jamais taper
    de texte ni de code.** Choisissez **Practice** pour un feedback immédiat avec
    explications, ou **Exam** pour le format officiel (75 questions, 90 minutes,
    réponses cachées jusqu'à la soumission) avec un rapport noté et révisable à la
    fin.

!!! example "Real-world analogy"
    Le mode Practice, c'est un sparring avec un coach qui s'arrête après chaque
    coup pour corriger votre garde ; le mode Exam, c'est le vrai combat : la cloche
    sonne, le chrono tourne, et vous ne découvrez la décision des juges qu'à la
    fin.

Les trois types d'interaction reproduisent exactement l'examen :

- **True / False** — choisissez l'une des deux options.
- **Single answer** — exactement une option est correcte (boutons radio).
- **Multiple choice** — deux options correctes ou plus ; vous devez *toutes* les
  sélectionner et rien d'autre pour marquer le point (cases à cocher).

!!! note "Les questions restent en anglais"
    L'examen officiel Symfony se passe en anglais : s'entraîner sur les questions
    en anglais fait partie de la préparation. L'interface et les explications de
    la plateforme sont disponibles en français, mais la banque de questions reste
    volontairement dans la langue de l'examen.

!!! danger "Pas un examen officiel"
    Chaque question de ce simulateur est une question d'entraînement, pas une
    question d'examen officielle. Cette banque est rédigée par la communauté et
    alignée sur le programme — elle n'est ni issue de, ni relue par, la
    certification Symfony 8 officielle.

## 🧠 Pour les nuls

**C'est quoi cette page ?** Un entraînement interactif qui te fait vivre l'examen en conditions proches du réel, avec les mêmes types de questions.

**Pourquoi ça existe ?** Lire de la théorie ne suffit pas — s'entraîner sous forme de questions, avec un minuteur en mode Exam, habitue ton cerveau au format réel avant le jour J.

**🏠 Analogie de la vraie vie :** Un simulateur de vol pour un pilote. Le mode Practice, c'est l'instructeur qui corrige chaque geste immédiatement ; le mode Exam, c'est le vol solo minuté, sans filet, avec le score révélé seulement à l'atterrissage.

**Symfony dans la vraie vie :** Filtrer par domaine (par ex. "Security seulement") et par difficulté permet de cibler précisément ta zone faible, plutôt que de réviser tout au hasard.

**⚠️ Erreur fréquente :** croire que ces questions sont "officielles" — ce sont des questions d'entraînement inspirées du syllabus, jamais des questions réellement posées à l'examen.

**🧠 Comment le mémoriser :** "Practice corrige à chaque coup ; Exam attend la fin du combat pour révéler le score."

Filtrez par topic area, difficulté et type de question, ou lancez **Full mock
exam** pour une simulation chronométrée de 75 questions tirées des 15 areas.

<div id="sf-quiz" data-src="../assets/quiz-data.json">
  <noscript>Le simulateur interactif nécessite JavaScript. Consultez plutôt le
  <a href="../revision/quiz/">Practice Quiz Bank</a> et les
  <a href="../revision/mock-exam/">Mock Exams</a>.</noscript>
</div>

!!! note "How scoring works"
    Les questions Multiple choice sont notées en tout-ou-rien, exactement comme au
    vrai examen : une sélection partiellement correcte vaut zéro. Le seuil de
    réussite affiché (65 %) est une estimation communautaire donnée à titre
    indicatif, pas un chiffre officiel — visez une marge confortable au-dessus.

!!! tip "Weak-area memory"
    Le simulateur mémorise votre précision par topic **dans ce navigateur**
    (`localStorage` — rien ne quitte votre machine). Après quelques questions,
    l'écran de configuration affiche vos areas les plus faibles et propose un
    bouton **Drill my weaknesses** qui construit une session de practice ciblée
    exactement sur ces topics. Utilisez *Reset stats* pour repartir de zéro.
