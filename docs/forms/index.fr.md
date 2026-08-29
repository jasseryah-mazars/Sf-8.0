# Forms

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Data Transformer](../labs/forms.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Le **composant Form** est le point de rencontre de trois étapes précédentes : il
s'affiche via **Twig**, vérifie les saisies via la **Validation**, et est câblé via
le **service container** et l'**EventDispatcher**. Un form Symfony n'est pas un
simple helper HTML `<form>` — c'est un moteur de mapping de données bidirectionnel
qui transforme un objet PHP en chaînes compatibles HTTP, puis retransforme les
chaînes soumises en un objet typé, en dispatchant des events à chaque étape.

Cette étape enseigne le composant de l'extérieur vers l'intérieur : créer un form,
gérer une soumission, comprendre les *trois représentations des données*
(model / normalized / view), puis creuser les points d'extension — types,
transformers, events et type extensions — que l'examen Expert adore.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [Templating (Twig)](../twig/index.md) · [Validation](../validation/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★★ |
    | **Dependencies** | Twig (7), Validation (8), DI + Events (3–4) |
    | **Revision priority** | **High** |
    | **Est. time** | 5–6 h |

## Why this stage matters

Les forms composent presque tout ce que vous avez appris. `FormFactory` est un
service ; les form types sont des services taggés `form.type` ; le flux de
soumission est une chaîne de `FormEvents` ; la validation s'exécute via une form
extension ; le rendu est un thème Twig. L'examen sonde les **coutures** entre ces
éléments : l'ordre des form events, dans quel sens s'exécute un data transformer,
ce que `handleRequest` inspecte réellement, et comment les tokens CSRF sont
générés et vérifiés. Apprenez le modèle mental du flux de données et le reste
n'est que du détail.

## Micro-chapters

Parcourez-les à peu près dans l'ordre :

- [ ] [Creating forms](creation.md) — `createForm`, classes de form type,
  `buildForm`, `configureOptions`, `createFormBuilder`, `data_class`.
- [ ] [Handling submissions](handling.md) — `handleRequest`, `isSubmitted`,
  `isValid`, `getData`, le flux request→model, POST-redirect-GET.
- [ ] [Form types & the type hierarchy](types.md) — types intégrés vs personnalisés,
  `getParent`, résolution des options, `ResolvedFormType`.
- [ ] [Rendering with Twig](rendering.md) — `form()`, `form_start`/`form_end`,
  `form_row`/`form_widget`/`form_label`/`form_errors`/`form_help`, `form_rest`.
- [ ] [Form theming](theming.md) — `form_theme`, thèmes intégrés, surcharge de
  blocs, résolution des noms de blocs.
- [ ] [CSRF protection](csrf.md) — fonctionnement, les options, le **CSRF stateless**
  (8.x), tokens manuels.
- [ ] [File uploads](file-upload.md) — `FileType`, `UploadedFile`,
  `mapped => false`, déplacement des fichiers, constraints `File`/`Image`.
- [ ] [Built-in types catalogue](built-in-types.md) — les field types de base,
  hors Doctrine, et leurs options clés.
- [ ] [Data transformers](data-transformers.md) — `DataTransformerInterface`,
  model↔norm↔view, model transformers vs view transformers, `TransformationFailedException`.
- [ ] [Form events](events.md) — `FormEvents`, modification dynamique, subscribers.
- [ ] [Type extensions](type-extensions.md) — `AbstractTypeExtension`,
  `#[AsFormTypeExtension]`, `getExtendedTypes`.

## How to study it

1. Lisez [creation](creation.md) et [handling](handling.md) ensemble — ils vous
   donnent l'aller-retour complet.
2. Intériorisez les **trois représentations des données** (couvertes dans
   [handling](handling.md) et [transformers](data-transformers.md)) ; tout le
   reste en découle.
3. Mémorisez les **deux séquences d'events** dans [events](events.md) — une
   question d'examen garantie.
4. Survolez [rendering](rendering.md)/[theming](theming.md), puis terminez par les
   outils avancés : [transformers](data-transformers.md) et
   [type extensions](type-extensions.md).

---

<small>Related: [Templating](../twig/index.md) ·
[Validation](../validation/index.md) ·
[Web Security Fundamentals](../php-web-security/web-security.md) ·
[Controllers](../controllers/index.md)</small>

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Le composant Form transforme un objet PHP en champs HTML à remplir, puis reconvertit les données soumises en cet objet PHP — dans les deux sens, automatiquement.

**Pourquoi ça existe ?** Sans lui, il faudrait écrire à la main chaque `<input>`, relire chaque valeur postée, la valider, et la réassigner à un objet — pour chaque formulaire du site. Le composant Form automatise tout ce travail répétitif.

**🏠 Analogie de la vraie vie :** Un formulaire administratif papier pré-imprimé avec des cases à remplir. Tu le remplis (soumission), un employé le relit et reporte chaque case dans ton dossier (l'objet PHP) — et s'il manque une signature, il te le rend avec l'erreur surlignée (validation).

**Symfony dans la vraie vie :** Une classe `ProduitType` décrit les cases du formulaire ; `$form->handleRequest($request)` lit ce que le visiteur a rempli ; `$form->getData()` te rend l'objet `Produit` déjà rempli et validé.

**⚠️ Erreur fréquente :** appeler `$form->isValid()` sans avoir vérifié `$form->isSubmitted()` avant — ça plante sur un formulaire qui vient d'être affiché, pas encore soumis.

**🧠 Comment le mémoriser :** "Jamais `isValid()` seul — toujours `isSubmitted() && isValid()`, dans cet ordre."


## Official References

- [Symfony documentation — Forms](https://symfony.com/doc/8.0/forms.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
