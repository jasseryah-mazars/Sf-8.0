# Handling File Uploads

!!! tip "In a nutshell"
    A `FileType` field gives you an `UploadedFile`; uploads are usually
    `mapped => false`, so you fetch and move the file yourself. Never trust the
    client-sent name or MIME type — rename the file and validate with the `File`/`Image` constraint.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Add a `FileType` field and read the resulting `UploadedFile`.
    - [ ] Use the `mapped => false` pattern to keep the upload out of your entity/DTO.
    - [ ] Move an uploaded file safely and constrain it with `File`/`Image`.

    **Syllabus:** `Forms → File uploads` ·
    **Level:** Advanced → Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Handling submissions](handling.md) · [Validation](../validation/index.md)

---

## Theory

An HTML file input arrives in `$_FILES`, which Symfony exposes as
`Symfony\Component\HttpFoundation\File\UploadedFile` objects in
`$request->files`. `FileType` binds a form field to that object. Because a
binary upload is not something you usually store *as-is* on your model, the field
is frequently **unmapped** — the form validates it, you handle persistence.

## Deep Dive — how it works internally

### From request to `UploadedFile`

The `HttpFoundationRequestHandler` merges `$request->files` into the submitted
data. For a `FileType` field the "view data" is the `UploadedFile`; there is no
string transformation. The mapped model value (if mapped) becomes that
`UploadedFile` too.

`UploadedFile` extends `Symfony\Component\HttpFoundation\File\File` (which extends
`\SplFileInfo`) and adds:

- `getClientOriginalName()` / `getClientMimeType()` — **untrusted**, client-sent.
- `getMimeType()` — guessed from content (trustworthy).
- `getSize()`, `isValid()`, `getError()`.
- `move(string $dir, ?string $name = null): File` — relocate out of the temp dir.

!!! danger "Never trust the client filename"
    `getClientOriginalName()` can contain path traversal or scripts. Always
    generate a safe name (e.g. slug + `uniqid()` + guessed extension) before
    `move()`.

```mermaid
flowchart LR
    A[HTML file input] --> B["$request->files → UploadedFile"]
    B --> C{mapped?}
    C -- false --> D["$form.get('file').getData()"]
    C -- true --> E[Model property]
    D --> F["safe rename + move()"]
```

!!! note "Source reference"
    `Symfony\Component\HttpFoundation\File\UploadedFile` and `FileType` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php).

### `mapped => false`

Setting `'mapped' => false` on a field:

- keeps it in the form (rendered, submitted, **validated**),
- but the data mapper does **not** read from or write to the model.

You retrieve it explicitly: `$form->get('brochure')->getData()`. This is the
standard pattern for uploads, plain-password fields, and "accept terms"
checkboxes.

### Constraints

Attach validation to the field via the `constraints` option (or to the model
property). Use:

- `Symfony\Component\Validator\Constraints\File` — `maxSize`, `mimeTypes`,
  `extensions`.
- `Symfony\Component\Validator\Constraints\Image` — plus width/height/ratio.

## Configuration & code

=== "Form type"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Form;

    use Symfony\Component\Form\AbstractType;
    use Symfony\Component\Form\Extension\Core\Type\FileType;
    use Symfony\Component\Form\FormBuilderInterface;
    use Symfony\Component\Validator\Constraints\File;

    final class DocumentType extends AbstractType
    {
        public function buildForm(FormBuilderInterface $builder, array $options): void
        {
            $builder->add('brochure', FileType::class, [
                'label'    => 'Brochure (PDF)',
                'mapped'   => false,          // handled manually
                'required' => false,
                'constraints' => [
                    new File(
                        maxSize: '5m',
                        mimeTypes: ['application/pdf'],
                        mimeTypesMessage: 'Please upload a valid PDF.',
                    ),
                ],
            ]);
        }
    }
    ```

=== "Controller"

    ```php
    <?php
    declare(strict_types=1);

    use App\Form\DocumentType;
    use Symfony\Component\HttpFoundation\File\Exception\FileException;
    use Symfony\Component\HttpFoundation\File\UploadedFile;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\String\Slugger\SluggerInterface;

    public function upload(Request $request, SluggerInterface $slugger): Response
    {
        $form = $this->createForm(DocumentType::class);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            /** @var UploadedFile|null $file */
            $file = $form->get('brochure')->getData();

            if ($file instanceof UploadedFile) {
                $safe = $slugger->slug(pathinfo(
                    $file->getClientOriginalName(), PATHINFO_FILENAME,
                ));
                $name = \sprintf('%s-%s.%s', $safe, uniqid(), $file->guessExtension());

                try {
                    $file->move($this->getParameter('brochures_dir'), $name);
                } catch (FileException) {
                    $this->addFlash('error', 'Upload failed.');
                }
            }

            return $this->redirectToRoute('upload');
        }

        return $this->render('upload/index.html.twig', ['form' => $form]);
    }
    ```

=== "Twig"

    ```twig
    {# form_start emits enctype="multipart/form-data" automatically #}
    {{ form_start(form) }}
        {{ form_row(form.brochure) }}
    {{ form_end(form) }}
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| `mapped => false` for uploads | Storing an `UploadedFile` on your entity |
| Rename with slugger + `uniqid()` | Using `getClientOriginalName()` as the path |
| Validate with `File`/`Image` | Trusting the client MIME type |
| Store the path/filename on the model | Persisting the raw file object |

## When (not) to use it / alternatives

Use `FileType` for browser uploads through a form. For programmatic/streamed
uploads (chunked, S3 pre-signed) the Form component is not involved — handle the
`Request`/HttpClient directly. Symfony UX-based upload widgets are out of scope.

!!! danger "Certification traps"
    - `form_start` adds `enctype="multipart/form-data"` **only when the form has a
      file field** — omit `FileType` and multipart won't be set.
    - `getClientOriginalName()`/`getClientMimeType()` are **untrusted**; use
      `guessExtension()`/`getMimeType()` (content-based) for security.
    - An unmapped field is still **validated**; you fetch it with `->getData()`.
    - `File` constraint `maxSize` is a string like `'5m'`/`'1024k'`, capped by PHP
      `upload_max_filesize`/`post_max_size`.

!!! warning "Common mistakes"
    - Forgetting to check `$file instanceof UploadedFile` (null on optional
      fields) → fatal on `move()`.
    - Storing files in the public web root without validation → RCE risk.
    - Expecting a mapped `FileType` to auto-persist — it stores the object, not a
      path.

## Exercises

1. **(Advanced)** Add an avatar `FileType` (`Image` constraint, max 2 MB) as an
   unmapped field and move it to `%kernel.project_dir%/var/uploads`.
2. **(Expert)** Explain why relying on `getClientMimeType()` for an allow-list is
   insecure and what to use instead.

??? success "Solutions"

    **1.** Add `->add('avatar', FileType::class, ['mapped' => false, 'constraints'
    => [new Image(maxSize: '2m')]])`. In the controller, fetch
    `$form->get('avatar')->getData()`, rename via slugger, `move()` to the
    uploads dir parameter.

    **2.** `getClientMimeType()` is sent by the browser and trivially spoofed. Use
    the `File`/`Image` constraint (which calls `getMimeType()`, guessed from file
    content) so a `.pdf` renamed `.png` is rejected.

## Certification questions

??? question "Q1. Where do you read an unmapped `FileType` value?"
    - [ ] A. From the bound model object
    - [x] B. `$form->get('field')->getData()` ✅
    - [ ] C. `$request->request->get('field')`
    - [ ] D. `$form->getViewData()`

    **Why:** `mapped => false` excludes the field from the data mapper; you fetch
    it directly from the child form.
    **Ref:** [File uploads](https://symfony.com/doc/current/controller/upload_file.html).

??? question "Q2. Which value is safe to trust for validation?"
    - [ ] A. `getClientOriginalName()`
    - [ ] B. `getClientMimeType()`
    - [x] C. `getMimeType()` / `guessExtension()` (content-based) ✅
    - [ ] D. The HTML `accept` attribute

    **Why:** Client-provided name/MIME are spoofable; content-based guessing is
    authoritative.
    **Ref:** [UploadedFile](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php).

??? question "Q3. When does `form_start` emit `multipart/form-data`?"
    - [x] A. When the form contains a file field ✅
    - [ ] B. Always
    - [ ] C. Only if you set it manually
    - [ ] D. Never — you must add it yourself

    **Why:** The form's `multipart` view var is set when a child requires it (e.g.
    `FileType`), and `form_start` renders the enctype accordingly.
    **Ref:** [File type](https://symfony.com/doc/current/reference/forms/types/file.html).

## Key takeaways

- `FileType` → `UploadedFile`; read unmapped uploads via `->get('x')->getData()`.
- Rename with a slug + `uniqid()`; never trust client name/MIME.
- Validate with `File`/`Image` constraints (content-based checks).
- `form_start` sets multipart automatically when a file field is present.

## Last-minute revision

!!! tip "Cheat sheet"
    - `UploadedFile`: `move($dir, $name)`, `guessExtension()`, `getMimeType()`.
    - Untrusted: `getClientOriginalName()`, `getClientMimeType()`.
    - `mapped => false` → still validated; fetch via `->getData()`.
    - `File(maxSize: '5m', mimeTypes: [...])` / `Image(...)`.
    - See also [controllers/file-upload](../controllers/file-upload.md).

## Official References
- [Official Symfony docs — Uploading files](https://symfony.com/doc/current/controller/upload_file.html)
- [Official Symfony docs — File field type](https://symfony.com/doc/current/reference/forms/types/file.html)
- [Symfony source — UploadedFile](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

---

<small>Related: [Controllers — file upload](../controllers/file-upload.md) ·
[Handling submissions](handling.md) · [Built-in types](built-in-types.md)</small>
</content>
