#!/usr/bin/env python3
"""Verify the BUILT site renders every Mermaid diagram to a real reader.

`tools/validate_mermaid.py` proves a diagram parses and renders in isolation.
That is necessary but not sufficient: the site could still ship a broken
experience through wrong asset wiring, a version mismatch, or a blocked CDN.
This check serves `site/` over HTTP and drives real Chromium against it.

Per page, at a desktop **and** a mobile viewport, it asserts:

* one `<svg>` per `.mermaid` block — fewer means a diagram silently failed;
* no `.mermaid-error` node and no visible "Syntax error in text";
* no mermaid-related console error or uncaught page exception;
* **no request to an external mermaid CDN** — which is what proves the vendored,
  version-pinned copy is the one actually rendering.

Usage:
    python3 tools/check_mermaid_render.py                       # sample across the site
    python3 tools/check_mermaid_render.py --all                 # every page with a diagram
    python3 tools/check_mermaid_render.py --pages php-web-security/interfaces

Requires a built site (`mkdocs build`). Exit status 0 when every checked page
renders cleanly at both viewports, 1 otherwise.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import random
import socketserver
import subprocess
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DOCS = os.path.join(ROOT, "docs")
DRIVER = os.path.join(ROOT, "tools", "_mermaid_render_check.js")


def pages_with_diagrams() -> list[str]:
    """URL paths of built pages whose English source contains a mermaid block."""
    found = []
    for dirpath, dirnames, filenames in os.walk(DOCS):
        dirnames[:] = [d for d in dirnames if d not in {"_meta", "assets"}]
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn.endswith(".fr.md"):
                continue
            src = os.path.join(dirpath, fn)
            with open(src, encoding="utf-8") as fh:
                if "```mermaid" not in fh.read():
                    continue
            rel = os.path.relpath(src, DOCS)[:-3]
            url = "/" if rel == "index" else (
                "/" + rel[: -len("/index")] + "/" if rel.endswith("/index")
                else "/" + rel + "/"
            )
            if os.path.isdir(os.path.join(SITE, url.strip("/"))) or url == "/":
                found.append(url)
    return found


def serve(directory: str):
    class SilentHandler(http.server.SimpleHTTPRequestHandler):
        # The per-request access log would bury the actual result.
        def log_message(self, fmt, *a):
            pass

    handler = functools.partial(SilentHandler, directory=directory)

    class Quiet(socketserver.TCPServer):
        allow_reuse_address = True

        def handle_error(self, request, client_address):  # keep output clean
            pass

    httpd = Quiet(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="check every page with a diagram")
    ap.add_argument("--pages", nargs="*", help="explicit doc paths, e.g. twig/syntax")
    ap.add_argument("--sample", type=int, default=12, help="sample size when not --all")
    args = ap.parse_args()

    if not os.path.isdir(SITE):
        print("check_mermaid_render: FAIL — site/ not found. Run `mkdocs build` first.",
              file=sys.stderr)
        return 1

    if args.pages:
        pages = ["/" + p.strip("/") + "/" for p in args.pages]
    else:
        pages = pages_with_diagrams()
        if not args.all and len(pages) > args.sample:
            rng = random.Random(20260828)  # fixed seed: reproducible sample
            pages = sorted(rng.sample(pages, args.sample))

    if not pages:
        print("check_mermaid_render: no pages with diagrams found.")
        return 0

    httpd, port = serve(SITE)
    base = f"http://127.0.0.1:{port}"

    env = os.environ.copy()
    local_modules = os.path.join(ROOT, "tools", "node_modules")
    global_modules = subprocess.run(
        ["npm", "root", "-g"], capture_output=True, text=True
    ).stdout.strip() or "/usr/lib/node_modules"
    env["NODE_PATH"] = f"{local_modules}:{global_modules}"

    try:
        proc = subprocess.run(
            ["node", DRIVER],
            input=json.dumps({"base": base, "pages": pages}),
            capture_output=True, text=True, timeout=1800, env=env,
            cwd=os.path.join(ROOT, "tools"),
        )
    finally:
        httpd.shutdown()

    if proc.returncode != 0 or not proc.stdout.strip():
        print("check_mermaid_render: FAIL — driver returned nothing.", file=sys.stderr)
        print((proc.stderr or "")[:1500], file=sys.stderr)
        return 1

    try:
        out = json.loads(proc.stdout)
    except ValueError:
        print("check_mermaid_render: FAIL — driver output was not JSON.", file=sys.stderr)
        print(proc.stdout[:1500], file=sys.stderr)
        return 1

    if out.get("fatal"):
        print(f"check_mermaid_render: FAIL — {out['fatal']}", file=sys.stderr)
        return 1

    results = out.get("results", [])
    failures = [r for r in results if not r.get("ok")]
    total_blocks = sum(r.get("blocks", 0) for r in results if r["viewport"] == "desktop")

    if failures:
        print(f"check_mermaid_render: FAIL — {len(failures)} of {len(results)} "
              f"page/viewport checks failed\n", file=sys.stderr)
        for r in failures:
            print(f"  [{r['viewport']}] {r['path']} — {r.get('error')}", file=sys.stderr)
        return 1

    print(f"check_mermaid_render: OK — {len(pages)} page(s) x {len(results)//max(len(pages),1)} "
          f"viewport(s), {total_blocks} diagram(s) rendered, no error node, "
          f"no 'Syntax error in text', no external mermaid request.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
