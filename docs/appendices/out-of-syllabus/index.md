# Appendices — Out of Syllabus

!!! danger "Hors syllabus officiel Symfony 8.0"
    Every chapter under this section is explicitly **excluded from the official
    Symfony 8 certification syllabus**. They are kept here — physically separated
    from the certification content — as optional, additional/enrichment reading
    for readers who want the full picture of a related Symfony component. None
    of it is tested in generated exams, counted toward official syllabus
    coverage, or scored in the quiz bank's official statistics.

## 🧠 Pour les nuls

**C'est quoi cette section ?** Une pièce à part, clairement étiquetée "hors examen", qui garde des chapitres intéressants mais **non testés** à la certification — pour ne jamais les confondre avec le contenu noté.

**Pourquoi ça existe ?** Certains sujets (ESI, Lock, PHPUnit Bridge) sont utiles à connaître en vrai projet Symfony, mais absents de la liste officielle du syllabus — les supprimer aurait perdu du contenu utile, les laisser mélangés aurait risqué de faire réviser du hors-programme comme si c'était noté.

**🏠 Analogie de la vraie vie :** Les annexes à la fin d'un manuel scolaire : utiles à lire, mais jamais interrogées à l'examen — clairement séparées du programme officiel pour qu'aucun élève ne s'y perde.

**Symfony dans la vraie vie :** Ces trois chapitres restent d'authentiques cours Symfony complets (théorie, exemples, quiz) — seule leur position (hors du dossier syllabus) et leur bandeau d'avertissement changent.

**⚠️ Erreur fréquente :** réviser ces chapitres en pensant qu'ils comptent pour l'examen — vérifie toujours le tag `🎯 Examen Symfony 8` en haut de chaque chapitre avant d'y consacrer du temps de révision.

**🧠 Comment le mémoriser :** "Si c'est dans les annexes, ce n'est pas noté — mais ça reste bon à savoir."

## Why these exist at all

Each topic below sits right next to an in-scope chapter that mentions it in
passing (ESI is the third fragment-rendering strategy alongside `render()` and
`render_hinclude()`; the PHPUnit Bridge is what Symfony's own test suite uses
for deprecation collection; the Lock component is a natural "what about
distributed locking" question after Cache). Moving them here — rather than
deleting them — keeps that curiosity satisfied without ever mixing them into
graded, in-scope material. See `specs/TraceabilityMatrix.md`'s
"Out-of-scope / Additional Learning" section for the row-by-row justification.

## Contents

| Topic | Related in-scope chapter | Why it's excluded |
|---|---|---|
| [Edge Side Includes (ESI)](esi.md) | [HTTP Caching](../../http-caching/index.md), [Templating (Twig) → Controller Rendering](../../twig/controller-rendering.md) | Not named in the official syllabus's HTTP Caching sub-topics |
| [PHPUnit Bridge](phpunit-bridge.md) | [Automated Tests](../../testing/index.md) | Not named in the official syllabus's Automated Tests sub-topics |
| [Lock Component](lock.md) | [Miscellaneous](../../miscellaneous/index.md) | Not named in the official syllabus's Miscellaneous sub-topics |

---

<small>Related: [Learning Dashboard](../../index.md) · [Traceability Matrix](https://github.com/jasseryah-mazars/Sf-8.0/blob/master/specs/TraceabilityMatrix.md)</small>
