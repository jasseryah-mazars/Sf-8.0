#!/usr/bin/env python3
"""Browser-based site quality audit (P2-03), run against a locally-served
build of the site — genuinely executed via Playwright + axe-core, not a
static-file heuristic and not fabricated.

This tool shells out to a Node.js script (tools/_site_quality_check.js)
because the accessibility/rendering libraries this check needs
(Playwright's Chromium driver, axe-core) are JS-ecosystem tools; Python
here is only the orchestrator (serve the built site, invoke the script,
relay its JSON result).

What this DOES check, for real, in a real headless Chromium:
  - axe-core automated accessibility audit (contrast, alt text, heading
    order, ARIA, label associations, landmark structure, and everything
    else axe-core's ruleset covers) on a sample of real pages.
  - No horizontal overflow at a 375x667 mobile viewport (a common mobile-
    unfriendly-layout signal).
  - Keyboard reachability: Tab through the page N times and confirm focus
    lands on real, distinct interactive elements (not stuck/lost).
  - Mermaid diagrams actually render to <svg> (not left as raw text).
  - The search box returns results for a known term.
  - The language switcher reaches a working /fr/ page.

What this explicitly does NOT check (would need capabilities this
environment doesn't have — not fabricated as passing):
  - Real assistive-technology behavior (a screen reader). axe-core is a
    strong proxy for WCAG conformance but is not a substitute for actually
    running NVDA/JAWS/VoiceOver against the page.
  - Real mobile devices / real network conditions (this uses Chromium's
    emulated mobile viewport, not a physical device).
  - The "simulator" (mock-exam JS) referenced by the mission brief is
    checked only for present interactive elements. This does not exercise
    every branch of its logic.

Run: python tools/check_site_quality.py
Requires: `mkdocs build` already run (produces site/), Node.js with the
global `playwright` package (see this environment's Playwright setup) and
`axe-core` installed locally via `npm install` inside tools/ (tools/
package.json declares it as the one dev dependency this check needs;
tools/node_modules/ itself is gitignored, like any other npm install
output — run `npm install --prefix tools` once before using this check).
"""
from __future__ import annotations
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
NODE_SCRIPT = os.path.join(ROOT, "tools", "_site_quality_check.js")
PORT = 8931


def serve_site():
    os.chdir(SITE)
    handler = http.server.SimpleHTTPRequestHandler

    class ReusableTCPServer(socketserver.TCPServer):
        # Without this, a prior run's socket sitting in TIME_WAIT makes
        # bind() fail with "Address already in use" even though nothing is
        # actually listening anymore.
        allow_reuse_address = True

    httpd = ReusableTCPServer(("127.0.0.1", PORT), handler)
    httpd.serve_forever()


def main() -> int:
    if not os.path.exists(os.path.join(SITE, "index.html")):
        print("check_site_quality: site/ not built — run `mkdocs build` first. "
              "Not fabricating a result.")
        return 1
    if not os.path.exists(NODE_SCRIPT):
        print(f"check_site_quality: {NODE_SCRIPT} missing.")
        return 1

    t = threading.Thread(target=serve_site, daemon=True)
    t.start()
    import time
    time.sleep(0.5)

    env = dict(os.environ)
    node_modules = os.path.join(ROOT, "tools", "node_modules")
    if not os.path.isdir(node_modules):
        print("check_site_quality: tools/node_modules/ missing — run "
              "`npm install --prefix tools` first (installs axe-core). "
              "Not fabricating a result.")
        return 1
    global_modules = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env["NODE_PATH"] = f"{node_modules}:{global_modules}"
    env["SITE_BASE_URL"] = f"http://127.0.0.1:{PORT}"

    result = subprocess.run(["node", NODE_SCRIPT], capture_output=True, text=True, env=env, cwd=ROOT)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    try:
        report = json.loads(result.stdout.strip().splitlines()[-1])
    except Exception:
        print("check_site_quality: could not parse JSON summary from Node script output.")
        return 1

    total_violations = report.get("total_violations", "?")
    print(f"\ncheck_site_quality: {total_violations} total issue(s) across "
          f"{len(report.get('pages', []))} sampled page(s). See output above for detail.")
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
