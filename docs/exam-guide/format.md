# Exam Format & Scoring

What the Symfony 8 Certification looks like in practice, so there are no surprises
on the day.

!!! abstract "Key facts"
    | Fact | Value |
    |---|---|
    | Questions | **75**, randomly selected from a large pool |
    | Duration | **90 minutes** (~72 seconds per question) |
    | Question types | Single choice, multiple choice, true/false |
    | Levels | **Advanced** and **Expert**, decided by score |
    | PHP baseline | **PHP 8.4+** (Symfony 8 requirement) |
    | Delivery | Online, proctored |
    | Language | English |

!!! info "Confirm the specifics"
    Exact pricing, proctoring rules, and pass thresholds are defined by the
    certifying body — check [certification.symfony.com](https://certification.symfony.com/)
    before booking. This page explains the *shape* of the exam.

## 🧠 Pour les nuls

**C'est quoi cette page ?** Le détail concret de ce que tu vas voir à l'écran le jour de l'examen : combien de questions, combien de temps, et quels types de questions.

**Pourquoi ça existe ?** Sans ces détails précis, tu ne peux pas planifier ton temps — 90 minutes pour 75 questions n'est pas la même stratégie que 40 minutes pour 20 questions.

**🏠 Analogie de la vraie vie :** Une course à pied : savoir qu'il y a 10 km à parcourir en 60 minutes change complètement ton rythme de départ, comparé à ne pas savoir la distance du tout.

**Symfony dans la vraie vie :** Savoir qu'un **QCM à choix multiples** exige de cocher **toutes** les bonnes réponses (pas juste une) change ta façon de lire chaque question — tu dois évaluer chaque option séparément, pas chercher "la" bonne réponse.

**⚠️ Erreur fréquente :** traiter une question à choix multiples comme une question à choix unique — cocher une seule bonne réponse parmi plusieurs attendues donne un score de zéro sur cette question.

**🧠 Comment le mémoriser :** "Choix multiple = toutes les bonnes cases, pas juste une."

## Question types

=== "Single choice"

    Exactly one correct answer. Radio-button style. The safest points if you know
    the fact — but watch for two options that are both *nearly* right.

=== "Multiple choice"

    **Two or more** correct answers; you must select **all** of them. Partial
    selection is wrong. These are where careful reading and elimination matter most.

=== "True / false"

    A single statement to judge. Often hinges on one precise word (a default value,
    an execution order, "always" vs "by default").

## What is tested

Questions are drawn across the **15 official topic areas**. Two Symfony 8 emphasis
shifts to keep in mind:

- **Messenger is up-weighted** — expect more questions on buses, transports,
  middleware, stamps, retries, and the failure transport.
- **HTTP Caching is down-weighted** — still tested, but a smaller share than in
  Symfony 7.

Questions favour **precise, current** knowledge: exact class/interface names,
execution order (kernel and console events), config keys and their defaults,
attribute names, and Symfony 8 / PHP 8.4 behaviour. Deprecated APIs are not the
right answer.

## Tooling and environment

- The exam is **online and proctored**; you sit it from your own machine under
  monitoring. Expect webcam + screen-share requirements and a quiet, cleared room.
- It is **closed-book**: no IDE, no documentation, no second screen. Everything must
  be recalled.
- The interface lets you **flag questions** and navigate back and forth — use this
  (see [Exam-Day Strategy](strategy.md)).

## Scoring and levels

There is **one exam**. Your score determines the outcome:

- A passing score earns the **Advanced** certification.
- A higher score earns the **Expert** certification.

Aim for Expert-level mastery even if you target Advanced; the margin is your safety
buffer. How to position for each is covered in [Advanced vs Expert](levels.md).

## What to expect minute by minute

- **75 questions / 90 minutes** ≈ **72 seconds each**. Most questions take far less;
  bank the surplus for the hard ones.
- Some questions are short factual checks; others present a code or config snippet
  to interpret.
- You can revisit flagged questions until time expires.

!!! danger "Format traps"
    - **Multiple choice needs *every* correct option** — a single miss scores zero
      on that question.
    - **True/false hinges on one word** — "always", "by default", "must" change the
      answer. Read literally.
    - **Deprecated-but-familiar** options are classic distractors; the current
      Symfony 8 / PHP 8.4 answer is the right one.

---

<small>Related: [Advanced vs Expert](levels.md) · [Exam-Day Strategy](strategy.md) · [How to Use This Platform](how-to-use.md)</small>

## Official References

- [Official Symfony Certification](https://certification.symfony.com/)
- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
