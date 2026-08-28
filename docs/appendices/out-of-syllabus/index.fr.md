# Appendices — Hors syllabus

!!! danger "Hors syllabus officiel Symfony 8.0"
    Chaque chapitre de cette section est explicitement **exclu du programme
    officiel de la certification Symfony 8**. Ils sont conservés ici —
    physiquement séparés du contenu de certification — comme lecture
    additionnelle/d'approfondissement optionnelle pour les lecteurs qui veulent
    une vue complète d'un composant Symfony connexe. Rien de tout cela n'est
    testé dans les examens générés, compté dans la couverture officielle du
    syllabus, ou noté dans les statistiques officielles de la banque de quiz.

## 🧠 Pour les nuls

**C'est quoi cette section ?** Une pièce à part, clairement étiquetée "hors examen", qui garde des chapitres intéressants mais **non testés** à la certification — pour ne jamais les confondre avec le contenu noté.

**Pourquoi ça existe ?** Certains sujets (ESI, Lock, PHPUnit Bridge) sont utiles à connaître en vrai projet Symfony, mais absents de la liste officielle du syllabus — les supprimer aurait perdu du contenu utile, les laisser mélangés aurait risqué de faire réviser du hors-programme comme si c'était noté.

**🏠 Analogie de la vraie vie :** Les annexes à la fin d'un manuel scolaire : utiles à lire, mais jamais interrogées à l'examen — clairement séparées du programme officiel pour qu'aucun élève ne s'y perde.

**Symfony dans la vraie vie :** Ces trois chapitres restent d'authentiques cours Symfony complets (théorie, exemples, quiz) — seule leur position (hors du dossier syllabus) et leur bandeau d'avertissement changent.

**⚠️ Erreur fréquente :** réviser ces chapitres en pensant qu'ils comptent pour l'examen — vérifie toujours le tag `🎯 Examen Symfony 8` en haut de chaque chapitre avant d'y consacrer du temps de révision.

**🧠 Comment le mémoriser :** "Si c'est dans les annexes, ce n'est pas noté — mais ça reste bon à savoir."


## Pourquoi ce contenu existe

Chaque sujet ci-dessous se situe juste à côté d'un chapitre du programme qui le
mentionne en passant (ESI est la troisième stratégie de rendu de fragment aux
côtés de `render()` et `render_hinclude()` ; le PHPUnit Bridge est ce
qu'utilise la propre suite de tests de Symfony pour la collecte des
dépréciations ; le composant Lock est une question naturelle sur le
verrouillage distribué après le Cache). Les déplacer ici — plutôt que de les
supprimer — satisfait cette curiosité sans jamais les mélanger au contenu noté
du programme. Voir la section « Out-of-scope / Additional Learning » de
`specs/TraceabilityMatrix.md` pour la justification ligne par ligne.

## Sommaire

| Sujet | Chapitre du programme associé | Pourquoi il est exclu |
|---|---|---|
| [Edge Side Includes (ESI)](esi.md) | [HTTP Caching](../../http-caching/index.md), [Templating (Twig) → Controller Rendering](../../twig/controller-rendering.md) | Non nommé dans les sous-sujets officiels du programme HTTP Caching |
| [PHPUnit Bridge](phpunit-bridge.md) | [Automated Tests](../../testing/index.md) | Non nommé dans les sous-sujets officiels du programme Automated Tests |
| [Lock Component](lock.md) | [Miscellaneous](../../miscellaneous/index.md) | Non nommé dans les sous-sujets officiels du programme Miscellaneous |

---

<small>Related: [Learning Dashboard](../../index.md) · [Traceability Matrix](https://github.com/jasseryah-mazars/Sf-8.0/blob/master/specs/TraceabilityMatrix.md)</small>
