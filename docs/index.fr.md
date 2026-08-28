# Symfony 8 Expert Certification Prep

Une plateforme d'étude gratuite et autonome pour la **certification Symfony 8**
(Advanced & Expert). Suivez le parcours guidé ci-dessous : vous saurez toujours
quoi ouvrir ensuite, sans avoir besoin de comprendre la structure du site.

<a class="sf-cta-primary" href="php-web-security/">▶ Commencer ma préparation</a>

<div id="sf-resume"></div>

## Vous ne savez pas par où commencer ?

!!! tip "Une seule recommandation, pas une nouvelle liste"
    **Commencez par le domaine [PHP & Web Security](php-web-security/index.md), puis
    suivez la [Roadmap](roadmap.md) dans l'ordre.** Si vous connaissez déjà bien
    Symfony et voulez d'abord évaluer votre niveau, faites un
    **[petit tour de pratique](exam-simulator.md)** — 20 questions, feedback
    immédiat, aucune configuration.

## Choisissez votre parcours

<div class="sf-paths">

<a class="sf-path-card" href="php-web-security/">
<strong>🌱 Je débute avec Symfony</strong>
<span>Partez des fondamentaux PHP, puis suivez l'ordre recommandé complet.</span>
</a>

<a class="sf-path-card" href="roadmap/">
<strong>📘 Je prépare le niveau Advanced</strong>
<span>Suivez la roadmap complète — une couverture large et solide des 15
domaines.</span>
</a>

<a class="sf-path-card" href="tours/">
<strong>🎓 Je prépare le niveau Expert</strong>
<span>Allez directement aux mécanismes internes : Source Tours, Deep Dives
et pièges de certification.</span>
</a>

<a class="sf-path-card" href="revision/">
<strong>⏱ Je révise avant l'examen</strong>
<span>Fiche de révision, flashcards, pièges et examens blancs chronométrés —
le Revision Hub.</span>
</a>

<a class="sf-path-card" href="exam-simulator/">
<strong>🎯 Je veux tester mon niveau</strong>
<span>Lancez le simulateur interactif — mode Entraînement ou Examen complet.</span>
</a>

</div>

## Votre parcours pas à pas

<ol class="sf-steps">
<li><strong>Évaluer mon niveau.</strong> Lisez <a href="exam-guide/levels/">Advanced vs Expert</a> pour savoir ce que vous visez.</li>
<li><strong>Suivre le parcours conseillé.</strong> Ouvrez la <a href="roadmap/">Roadmap</a> — l'ordre d'étude qui évite d'utiliser une notion avant qu'elle soit enseignée.</li>
<li><strong>Étudier un domaine.</strong> Commencez par <a href="php-web-security/">PHP & Web Security</a> — chaque domaine suit la même anatomie (théorie, deep dive, exercices).</li>
<li><strong>Faire les exercices.</strong> Chaque domaine a un TP guidé : <a href="labs/">TP</a>.</li>
<li><strong>Tester mes connaissances.</strong> Faites une session d'entraînement dans l'<a href="exam-simulator/">Exam Simulator</a>.</li>
<li><strong>Réviser mes points faibles.</strong> Le <a href="revision/">Revision Hub</a> choisit le bon outil selon le temps disponible.</li>
<li><strong>Passer un examen blanc.</strong> Format complet, chronométré : <a href="revision/mock-exam/">Examen Blanc</a>.</li>
</ol>

## Domaines de certification

Chaque domaine officiel, dans l'ordre d'étude recommandé par la plateforme.
**Étudier** ouvre l'index du chapitre ; **Tester** lance directement des
questions de pratique pour ce domaine uniquement.

!!! tip "Ce que signifient les colonnes"
    **Statut** est le suivi de couverture automatisé propre à ce projet (voir
    la [Traceability Matrix](https://github.com/jasseryah-mazars/Sf-8.0/blob/master/specs/TraceabilityMatrix.md))
    — ce n'est pas une affirmation que toute question d'examen possible est
    couverte. **Flashcards / Examen / Fiche** sont des liens rapides vers le
    matériel de révision du domaine.

### 🧱 Fondations

Pas encore de Symfony — le langage et le protocole sur lesquels tout le reste
s'appuie.

| # | Domaine | Statut | Étudier | Tester | Flashcards | Examen | Fiche |
|---|---|---|---|---|---|---|---|
| 1 | [PHP & Web Security](php-web-security/index.md) | 9/9 PASS | [Étudier](php-web-security/index.md) | [Tester](exam-simulator.md?area=PHP%20%26%20Web%20Security) | [Cartes](revision/flashcards/php-web-security.md) | [Examen](exams/php-web-security.md) | [Fiche](revision/sheets/php-web-security.md) |
| 2 | [HTTP](http/index.md) | 11/11 PASS | [Étudier](http/index.md) | [Tester](exam-simulator.md?area=HTTP) | [Cartes](revision/flashcards/http.md) | [Examen](exams/http.md) | [Fiche](revision/sheets/http.md) |

### 🧠 Cœur Symfony (le modèle mental)

Le kernel et le container — les deux machines sur lesquelles tous les autres
composants se branchent. Rendement examen maximal ; ne jamais bâcler ces deux
domaines.

| # | Domaine | Statut | Étudier | Tester | Flashcards | Examen | Fiche |
|---|---|---|---|---|---|---|---|
| 3 | [Symfony Architecture](architecture/index.md) | 12/17 PASS · 5 TO VERIFY | [Étudier](architecture/index.md) | [Tester](exam-simulator.md?area=Symfony%20Architecture) | [Cartes](revision/flashcards/architecture.md) | [Examen](exams/architecture.md) | [Fiche](revision/sheets/architecture.md) |
| 4 | [Dependency Injection](dependency-injection/index.md) | 12/12 PASS | [Étudier](dependency-injection/index.md) | [Tester](exam-simulator.md?area=Dependency%20Injection) | [Cartes](revision/flashcards/dependency-injection.md) | [Examen](exams/dependency-injection.md) | [Fiche](revision/sheets/dependency-injection.md) |

### 🧩 Composants applicatifs (couche fonctionnelle et largeur)

La gestion des requêtes au quotidien, puis le bloc sécurité à fort coefficient,
puis la largeur. Chaque domaine ne liste que ses **vrais** prérequis —
plusieurs (Security, HTTP Caching, Console) sont techniquement débloqués plus
tôt qu'ils n'apparaissent ci-dessous ; ils sont séquencés plus tard pour des
raisons de poids d'examen expliquées dans la [Roadmap](roadmap.md).

| # | Domaine | Statut | Étudier | Tester | Flashcards | Examen | Fiche |
|---|---|---|---|---|---|---|---|
| 5 | [Controllers](controllers/index.md) | 15/15 PASS | [Étudier](controllers/index.md) | [Tester](exam-simulator.md?area=Controllers) | [Cartes](revision/flashcards/controllers.md) | [Examen](exams/controllers.md) | [Fiche](revision/sheets/controllers.md) |
| 6 | [Routing](routing/index.md) | 13/13 PASS | [Étudier](routing/index.md) | [Tester](exam-simulator.md?area=Routing) | [Cartes](revision/flashcards/routing.md) | [Examen](exams/routing.md) | [Fiche](revision/sheets/routing.md) |
| 7 | [Templating (Twig)](twig/index.md) | 14/14 PASS | [Étudier](twig/index.md) | [Tester](exam-simulator.md?area=Templating%20%28Twig%29) | [Cartes](revision/flashcards/twig.md) | [Examen](exams/twig.md) | [Fiche](revision/sheets/twig.md) |
| 8 | [Data Validation](validation/index.md) | 9/9 PASS | [Étudier](validation/index.md) | [Tester](exam-simulator.md?area=Data%20Validation) | [Cartes](revision/flashcards/validation.md) | [Examen](exams/validation.md) | [Fiche](revision/sheets/validation.md) |
| 9 | [Forms](forms/index.md) | 13/13 PASS | [Étudier](forms/index.md) | [Tester](exam-simulator.md?area=Forms) | [Cartes](revision/flashcards/forms.md) | [Examen](exams/forms.md) | [Fiche](revision/sheets/forms.md) |
| 10 | [Security](security/index.md) | 13/13 PASS | [Étudier](security/index.md) | [Tester](exam-simulator.md?area=Security) | [Cartes](revision/flashcards/security.md) | [Examen](exams/security.md) | [Fiche](revision/sheets/security.md) |
| 11 | [HTTP Caching](http-caching/index.md) | 5/5 PASS | [Étudier](http-caching/index.md) | [Tester](exam-simulator.md?area=HTTP%20Caching) | [Cartes](revision/flashcards/http-caching.md) | [Examen](exams/http-caching.md) | [Fiche](revision/sheets/http-caching.md) |
| 12 | [Console](console/index.md) | 9/9 PASS | [Étudier](console/index.md) | [Tester](exam-simulator.md?area=Console) | [Cartes](revision/flashcards/console.md) | [Examen](exams/console.md) | [Fiche](revision/sheets/console.md) |
| 13 | [Messenger](messenger/index.md) | 7/7 PASS | [Étudier](messenger/index.md) | [Tester](exam-simulator.md?area=Messenger) | [Cartes](revision/flashcards/messenger.md) | [Examen](exams/messenger.md) | [Fiche](revision/sheets/messenger.md) |
| 14 | [Automated Tests](testing/index.md) | 12/12 PASS | [Étudier](testing/index.md) | [Tester](exam-simulator.md?area=Automated%20Tests) | [Cartes](revision/flashcards/testing.md) | [Examen](exams/testing.md) | [Fiche](revision/sheets/testing.md) |
| 15 | [Miscellaneous](miscellaneous/index.md) | 15/15 PASS | [Étudier](miscellaneous/index.md) | [Tester](exam-simulator.md?area=Miscellaneous) | [Cartes](revision/flashcards/miscellaneous.md) | [Examen](exams/miscellaneous.md) | [Fiche](revision/sheets/miscellaneous.md) |
| — | [Internationalization and localization](miscellaneous/intl.md) | 1/1 PASS | [Étudier](miscellaneous/intl.md) | [Tester](exam-simulator.md?area=Miscellaneous) | — | — | — |

<small>L'internationalisation est un unique sous-sujet à l'intérieur du
chapitre Miscellaneous (aucun fichier flashcard/examen dédié n'existe encore
pour lui) — son lien "Étudier" va directement à cette section ; les cellules
vides sont des lacunes honnêtes, pas des liens cassés.</small>

### 🚫 Hors programme (exclu, non enseigné)

Nommé ici **uniquement** pour marquer la frontière — rien de tout cela n'est
enseigné ou évalué comme contenu substantiel. Trois composants existent dans
la navigation en tant que chapitres complets *parce que* le programme les
nomme explicitement comme exclus et qu'un candidat doit pouvoir le reconnaître
au premier coup d'œil ; chacun porte sa propre mention « Exclu de la
certification Symfony 8 ».

| Sujet | Où il est mentionné |
|---|---|
| Edge Side Includes (ESI) | [Chapitre exclu](appendices/out-of-syllabus/esi.md) |
| PHPUnit Bridge | [Chapitre exclu](appendices/out-of-syllabus/phpunit-bridge.md) |
| Lock Component | [Chapitre exclu](appendices/out-of-syllabus/lock.md) |
| Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore, PHP Polyfills, composants String/Uid/TypeInfo, Amazon SQS, transports Messenger tiers | Mentions de frontière uniquement (distracteurs, notes de périmètre) |

## Actions rapides

- [Roadmap](roadmap.md) — le graphe de dépendances complet et l'ordre d'étude.
- [Exam Simulator](exam-simulator.md) — modes interactifs Entraînement/Examen.
- [Chapter Exams](exams/index.md) — jeux de questions fixes par domaine.
- [Mock Exams](revision/mock-exam.md) — épreuves complètes chronométrées.
- [Revision Hub](revision/index.md) — tous les outils de révision de dernière minute.
- [Master Cheat Sheet](revision/cheat-sheet.md) — faits à plus fort rendement par domaine.
- [Top Certification Traps](revision/traps.md) — les distinctions subtiles que l'examen adore.
- [Study Planner](revision/study-planner.md) — choisissez un planning 8/4/1 semaine(s).
- [Glossary](glossary.md) — définitions en une ligne renvoyant au chapitre qui enseigne chaque terme.
- [Official Symfony Certification](https://certification.symfony.com/) — le site officiel de l'examen.

## À qui ça s'adresse

- **Le Praticien** — 2 à 5 ans de Symfony, visant **Advanced**. Vous voulez une
  couverture structurée et de la confiance sur les cas limites.
- **Le candidat Expert** — senior, visant **Expert**. Vous voulez les
  mécanismes internes, les compromis, et le repérage des pièges.

Les deux niveaux sont le *même examen*, noté différemment — voir
[Advanced vs Expert](exam-guide/levels.md).

## Faits sur l'examen (Symfony 8)

| Fait | Valeur |
|---|---|
| Questions | 75, sélectionnées aléatoirement |
| Durée | 90 minutes (~72 s/question) |
| Types de questions | Choix unique, choix multiple, vrai/faux |
| Niveaux | **Advanced** et **Expert** (déterminés par le score) |
| Base PHP | **PHP 8.4+** (exigence de Symfony 8) |
| Changement de poids | Messenger **renforcé** ; HTTP Caching **allégé** |

## Où aller ensuite

- [Exam Guide](exam-guide/index.md) — format, notation, Advanced vs Expert, stratégie.
- [Roadmap](roadmap.md) — le parcours d'étude ordonné et le graphe de dépendances.
- [Revision Hub](revision/index.md) — modes, fiches de révision, flashcards, confusions,
  examen blanc, pièges, aides mémoire, quiz.

---

<small>Sous licence MIT. Symfony est une marque déposée de Symfony SAS. Ceci est
un projet communautaire indépendant, non affilié à Symfony SAS et non
approuvé par elle. Le projet a commencé comme une réécriture de la
[liste de préparation communautaire de ThomasBerends](https://github.com/ThomasBerends/symfony-certification-preparation-list)
(une liste de liens, ciblant Symfony 7) et a été reconstruit en contenu
pédagogique complet pour Symfony 8. Une ressource d'étude à utiliser **en
complément de la documentation officielle Symfony** qu'elle référence, pas en
remplacement.</small>

## 🧠 Pour les nuls

**C'est quoi ce site ?** Un support de préparation complet et gratuit à la certification Symfony 8 — chaque page t'apprend un concept précis, avec des exemples et des questions d'entraînement.

**Pourquoi ça existe ?** Le syllabus officiel liste 15 domaines à connaître, mais ne fournit aucun contenu pédagogique lui-même — ce site comble ce vide avec des cours structurés, testés et vérifiés.

**🏠 Analogie de la vraie vie :** Une auto-école complète plutôt qu'une simple liste de règles du code de la route : ici, chaque règle est expliquée, illustrée, et suivie d'exercices — pas juste énumérée.

**Symfony dans la vraie vie :** Choisis une des trois cartes ci-dessous selon ton niveau (débutant, préparation Advanced, préparation Expert) — le site s'adapte à ton point de départ plutôt que de t'imposer un seul chemin.

**⚠️ Erreur fréquente :** essayer de tout lire dans l'ordre de la barre de navigation (alphabétique) au lieu de suivre le [Roadmap](roadmap.md) — l'ordre alphabétique ignore les prérequis entre domaines.

**🧠 Comment le mémoriser :** "Pas sûr par où commencer ? PHP & Web Security d'abord, puis le Roadmap dans l'ordre."


## Official References

- [Official Symfony Certification](https://certification.symfony.com/)
- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
