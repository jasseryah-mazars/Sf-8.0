# Handling File Uploads

!!! tip "In a nutshell"
    Uploads arrive as `UploadedFile` in `$request->files`; validate the
    content-detected `getMimeType()` (never the spoofable client name) and `move()`
    them to storage outside the web root. `#[MapUploadedFile]` binds and validates
    an upload straight into a controller argument.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Read an `UploadedFile` from the request and move it safely.
    - [ ] Validate uploads (size, MIME, error state) before persisting.
    - [ ] Use the `#[MapUploadedFile]` resolver for controller-argument uploads.

    **Syllabus:** `Controllers → File upload` ·
    **Level:** Advanced → Expert ·
    **Est. time:** 15 min ·
    **Prerequisites:** [The Request](request.md), [Web Security](../php-web-security/web-security.md)

---

## Theory

An uploaded file arrives in the `files` bag as
`Symfony\Component\HttpFoundation\File\UploadedFile`. The core steps:

1. Read it: `$request->files->get('avatar')`.
2. Validate: extension/MIME, size, and `->isValid()` / error code.
3. Move it: `$file->move($targetDir, $newName)` to permanent storage.

Never trust the client filename — generate a safe name.

!!! question "Predict first"
    To decide whether an upload is really a PDF, do you trust
    `getClientMimeType()`, the file extension, or `getMimeType()`?

??? note "Reveal"
    `getMimeType()` — it is detected from the file **content**. The client-supplied
    name, extension, and MIME are all spoofable. Then `move()` the file to storage
    outside the web root (it throws `FileException` on failure, never returns a bool).

## Deep Dive — how it works internally

`UploadedFile` extends `Symfony\Component\HttpFoundation\File\File` (itself a
`\SplFileInfo`). It wraps PHP's `$_FILES` entry and adds:

- `getClientOriginalName()` / `getClientMimeType()` — **client-supplied, spoofable**.
- `getMimeType()` — detected from content via the `MimeTypes` guesser (trust this).
- `getSize()`, `getError()` (a `UPLOAD_ERR_*` code), `isValid()`.
- `move($dir, $name)` — validates the temp file was truly uploaded, then moves it;
  throws `FileException` on failure.
- `getClientOriginalExtension()` vs `guessExtension()` (from real MIME).

```mermaid
flowchart LR
    Br[Browser multipart POST] --> F["$_FILES"]
    F --> UB[Request.files FileBag]
    UB --> UF[UploadedFile]
    UF -->|validate| V{valid & safe?}
    V -->|yes| MV["move(dir, safeName)"]
    V -->|no| ERR[reject]
```

### Security & limits

- Uploads are bounded by PHP's `upload_max_filesize` and `post_max_size`;
  exceeding them yields an error code (or an empty `files` bag), not an exception.
- Store uploads **outside** the web root or with execution disabled — an uploaded
  `.php` in a served directory is remote code execution.
- Sanitise the target name (e.g. slug + unique id); use `guessExtension()` from
  the detected MIME, not the client extension.

!!! note "Source reference"
    `Symfony\Component\HttpFoundation\File\UploadedFile` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php).

### `#[MapUploadedFile]` (Symfony 8)

The `RequestPayloadValueResolver` (the same targeted resolver behind
`#[MapRequestPayload]`/`#[MapQueryString]`) fills an `UploadedFile` (or array of them)
controller argument directly, and can apply `File`/`Image` constraints inline —
throwing an `HttpException` on validation failure. See
[Value Resolvers](value-resolvers.md).

For form-driven uploads, use the `FileType` field — see
[Forms → File Upload](../forms/file-upload.md).

## Configuration & code

=== "Manual (Request)"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\File\Exception\FileException;
    use Symfony\Component\HttpFoundation\File\UploadedFile;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;
    use Symfony\Component\String\Slugger\SluggerInterface;

    final class AvatarController extends AbstractController
    {
        #[Route('/avatar', name: 'avatar_upload', methods: ['POST'])]
        public function upload(Request $request, SluggerInterface $slugger): Response
        {
            $file = $request->files->get('avatar');
            if (!$file instanceof UploadedFile || !$file->isValid()) {
                throw $this->createNotFoundException('No valid upload.');
            }

            $safe = $slugger->slug(pathinfo($file->getClientOriginalName(), PATHINFO_FILENAME));
            $name = \sprintf('%s-%s.%s', $safe, uniqid(), $file->guessExtension());

            try {
                $file->move($this->getParameter('kernel.project_dir').'/var/uploads', $name);
            } catch (FileException) {
                throw $this->createNotFoundException('Upload failed.');
            }

            return $this->redirectToRoute('avatar_upload');
        }
    }
    ```

=== "#[MapUploadedFile]"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Component\HttpFoundation\File\UploadedFile;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\HttpKernel\Attribute\MapUploadedFile;
    use Symfony\Component\Routing\Attribute\Route;
    use Symfony\Component\Validator\Constraints\File as FileConstraint;

    final class DocController
    {
        #[Route('/doc', name: 'doc_upload', methods: ['POST'])]
        public function __invoke(
            #[MapUploadedFile([
                new FileConstraint(maxSize: '2M', mimeTypes: ['application/pdf']),
            ])]
            UploadedFile $document,
        ): Response {
            // $document is already validated; failures threw before this ran
            return new Response('Received '.$document->getClientOriginalName());
        }
    }
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Validate MIME via `getMimeType()`/constraints | Trusting `getClientMimeType()` |
| Generate a safe, unique target name | Using the raw client filename |
| Store outside web root or disable execution | Saving into `public/` unguarded |
| Check `isValid()`/`getError()` | Assuming the file is always present |

## When (not) to use it / alternatives

- **Raw `UploadedFile`** — simple, single-file endpoints or APIs.
- **`#[MapUploadedFile]`** — controller-argument uploads with inline validation.
- **Forms `FileType`** — when the upload is part of a larger form with CSRF,
  binding, and error rendering. See [Forms → File Upload](../forms/file-upload.md).

!!! danger "Certification traps"
    - `getClientOriginalName()`/`getClientMimeType()` are **client-controlled and
      spoofable**; use `getMimeType()`/`guessExtension()` for trust decisions.
    - Exceeding `post_max_size` can yield an **empty `files` bag** (no exception) —
      always null-check.
    - `move()` throws `FileException` on failure; it does not return a bool.
    - `UploadedFile` is a `\SplFileInfo`; after `move()` the temp file no longer
      exists at its original path.
    - `#[MapUploadedFile]` validation failure throws an HTTP exception **before**
      your action body runs.

!!! warning "Common mistakes"
    - Saving into a web-served directory, enabling script execution (RCE).
    - Forgetting that no file selected still submits an empty field — guard for null.

## Exercises

1. **(Basic)** Reject any upload that is not a JPEG/PNG under 1 MB, then move it.
2. **(Expert)** Rewrite the manual example using `#[MapUploadedFile]` with `Image`
   constraints and no manual validation.

??? success "Solutions"

    **1.** Check `in_array($file->getMimeType(), ['image/jpeg','image/png'], true)`
    and `$file->getSize() <= 1_048_576`, else throw a `BadRequestHttpException`.

    **2.**
    ```php
    public function __invoke(
        #[MapUploadedFile([new Image(maxSize: '1M')])]
        UploadedFile $photo,
    ): Response { /* already validated */ }
    ```

## Certification questions

??? question "Q1. Which value should you trust to decide a file's real type?"
    - [ ] A. `getClientMimeType()`
    - [x] B. `getMimeType()` (content-detected) ✅
    - [ ] C. `getClientOriginalExtension()`
    - [ ] D. the form field name

    **Why:** client-provided values are spoofable; the guesser inspects content.
    **Ref:** [file uploads](https://symfony.com/doc/current/controller/upload_file.html).

??? question "Q2. What does `UploadedFile::move()` do on failure?"
    - [ ] A. Returns false.
    - [x] B. Throws a `FileException`. ✅
    - [ ] C. Returns null and logs.
    - [ ] D. Retries automatically.

    **Why:** `move()` throws on error rather than returning a status. **Ref:** [UploadedFile](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php).

??? question "Q3. `#[MapUploadedFile]` with a failing constraint…"
    - [x] A. throws an HTTP exception before the action body executes ✅
    - [ ] B. sets the argument to null
    - [ ] C. adds a flash message
    - [ ] D. is ignored in prod

    **Why:** the resolver validates and aborts with an HTTP error on failure.
    **Ref:** [value resolvers](https://symfony.com/doc/current/controller/value_resolver.html).

## Key takeaways

- Uploads arrive as `UploadedFile` in `$request->files`; always null-check.
- Trust `getMimeType()`/`guessExtension()`, never the client-supplied name/MIME.
- `move()` throws `FileException`; store files outside the web root.
- `#[MapUploadedFile]` maps + validates uploads as controller arguments.

## Last-minute revision

!!! tip "Cheat sheet"
    - `$request->files->get('field')` → `?UploadedFile`.
    - Validate: `isValid()`, `getMimeType()`, `getSize()`.
    - `move($dir, $safeName)` (throws `FileException`).
    - `#[MapUploadedFile([new File(...)])] UploadedFile $x`.

## Connections

- **Depends on:** [The Request](request.md) — uploads arrive in the `files` bag of the current request.
- **Reused in:** [Value Resolvers](value-resolvers.md) — `#[MapUploadedFile]` binds and validates an upload as a controller argument.
- **Confused with:** [Forms → File Upload](../forms/file-upload.md) — the `FileType` field wraps this with CSRF, binding, and error rendering.

## Official References
- [Official Symfony docs — Uploading Files](https://symfony.com/doc/current/controller/upload_file.html)
- [Official Symfony docs — Value Resolvers](https://symfony.com/doc/current/controller/value_resolver.html)
- [Symfony source — UploadedFile](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)

## Confidence check

I'm ready when I can:

- [ ] explain **why** you must not trust the client-supplied filename/MIME
- [ ] read, validate, and `move()` an `UploadedFile` safely in Symfony 8
- [ ] debug an empty `files` bag after exceeding `post_max_size`
- [ ] spot that `move()` throws `FileException` rather than returning a bool
- [ ] explain how `#[MapUploadedFile]` validates before the action body runs

---

<small>Related: [The Request](request.md) · [Value Resolvers](value-resolvers.md) · [Forms → File Upload](../forms/file-upload.md)</small>
