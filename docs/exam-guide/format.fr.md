# Format de l'examen et notation

À quoi ressemble concrètement la Certification Symfony 8, pour qu'il n'y ait aucune
surprise le jour J.

!!! abstract "Key facts"
    | Fait | Valeur |
    |---|---|
    | Questions | **75**, sélectionnées aléatoirement dans un large réservoir |
    | Durée | **90 minutes** (~72 secondes par question) |
    | Types de questions | Choix unique, choix multiple, vrai/faux |
    | Niveaux | **Advanced** et **Expert**, décidés par le score |
    | Version PHP requise | **PHP 8.4+** (exigence de Symfony 8) |
    | Modalité | En ligne, surveillé (proctored) |
    | Langue | Anglais |

!!! info "Confirm the specifics"
    Le tarif exact, les règles de surveillance et les seuils de réussite sont définis
    par l'organisme certificateur — consultez
    [certification.symfony.com](https://certification.symfony.com/) avant de
    réserver. Cette page explique la *forme* de l'examen.

## Question types

=== "Single choice"

    Exactement une bonne réponse. Style bouton radio. Les points les plus sûrs si
    vous connaissez le fait — mais méfiez-vous des paires d'options toutes deux
    *presque* justes.

=== "Multiple choice"

    **Deux bonnes réponses ou plus** ; vous devez **toutes** les sélectionner. Une
    sélection partielle est comptée fausse. C'est là que la lecture attentive et
    l'élimination comptent le plus.

=== "True / false"

    Une seule affirmation à juger. Elle repose souvent sur un mot précis (une valeur
    par défaut, un ordre d'exécution, « always » vs « by default »).

## What is tested

Les questions sont tirées des **15 domaines officiels**. Deux évolutions de
pondération propres à Symfony 8 à garder en tête :

- **Messenger est davantage pondéré** — attendez-vous à plus de questions sur les
  bus, transports, middlewares, stamps, retries et le failure transport.
- **HTTP Caching est moins pondéré** — toujours testé, mais avec une part plus
  réduite que dans Symfony 7.

Les questions privilégient une connaissance **précise et à jour** : noms exacts de
classes/interfaces, ordre d'exécution (kernel events et console events), clés de
configuration et leurs valeurs par défaut, noms d'attributs, et le comportement de
Symfony 8 / PHP 8.4. Les APIs dépréciées ne sont pas la bonne réponse.

## Tooling and environment

- L'examen est **en ligne et surveillé** ; vous le passez depuis votre propre
  machine, sous surveillance. Attendez-vous à des exigences de webcam + partage
  d'écran et à une pièce calme et dégagée.
- Il se passe **à livre fermé** : pas d'IDE, pas de documentation, pas de second
  écran. Tout doit être restitué de mémoire.
- L'interface permet de **marquer des questions** et de naviguer librement — servez-vous-en
  (voir l'[Exam-Day Strategy](strategy.md)).

## Scoring and levels

Il n'y a **qu'un seul examen**. Votre score détermine le résultat :

- Un score de réussite donne la certification **Advanced**.
- Un score plus élevé donne la certification **Expert**.

Visez la maîtrise de niveau Expert même si vous ciblez Advanced ; la marge est votre
filet de sécurité. La façon de se positionner pour chaque niveau est couverte dans
[Advanced vs Expert](levels.md).

## What to expect minute by minute

- **75 questions / 90 minutes** ≈ **72 secondes chacune**. La plupart des questions
  prennent bien moins ; mettez le surplus de côté pour les difficiles.
- Certaines questions sont de courtes vérifications factuelles ; d'autres présentent
  un extrait de code ou de config à interpréter.
- Vous pouvez revenir sur les questions marquées jusqu'à l'expiration du temps.

!!! danger "Format traps"
    - **Le choix multiple exige *toutes* les bonnes options** — une seule omission
      vaut zéro sur la question.
    - **Le vrai/faux se joue sur un mot** — « always », « by default », « must »
      changent la réponse. Lisez littéralement.
    - Les options **dépréciées mais familières** sont des distracteurs classiques ;
      la réponse Symfony 8 / PHP 8.4 actuelle est la bonne.

---

<small>Related: [Advanced vs Expert](levels.md) · [Exam-Day Strategy](strategy.md) · [How to Use This Platform](how-to-use.md)</small>

## Official References

- [Official Symfony Certification](https://certification.symfony.com/)
- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
