# Appendices — Hors syllabus

!!! danger "Hors syllabus officiel Symfony 8.0"
    Chaque chapitre de cette section est explicitement **exclu du programme
    officiel de la certification Symfony 8**. Ils sont conservés ici —
    physiquement séparés du contenu de certification — comme lecture
    additionnelle/d'approfondissement optionnelle pour les lecteurs qui veulent
    une vue complète d'un composant Symfony connexe. Rien de tout cela n'est
    testé dans les examens générés, compté dans la couverture officielle du
    syllabus, ou noté dans les statistiques officielles de la banque de quiz.

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
