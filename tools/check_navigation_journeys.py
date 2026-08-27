#!/usr/bin/env python3
"""Real headless-Chromium validation of the guided-navigation journeys
(learner-experience redesign, this run). Not a static-file heuristic —
launches an actual browser (Playwright) and drives it through the 6
named journeys the mission defined: beginner, Advanced, Expert, quick
revision, mobile, and French. Same architecture as
tools/check_site_quality.py (Python orchestrator + Node/Playwright
driver) — see that tool's own docstring for why the split exists.

What this checks, for real:
  - Every step of every journey follows a REAL link/URL and loads
    successfully (no dead ends, no 404s).
  - The dashboard's primary CTA and quick-actions bar are actually
    present in the DOM.
  - `docs/assets/quiz.js`'s `?area=` deep link genuinely skips the
    config screen and starts a practice session (verified via DOM
    state, not assumed from the code).
  - `docs/assets/progress.js`'s "continue where you left off" widget
    and weak-area hint actually populate from real localStorage data
    (simulated prior activity, then checked after a fresh page load).
  - Mobile (375px): no visible horizontal overflow, keyboard
    reachability.
  - French: `<html lang="fr">`, the quick-actions bar renders in
    French on a French chapter.
  - axe-core accessibility audit on the dashboard (same tool as
    tools/check_site_quality.py's P2-03 audit — any violation here is
    either a new regression or, if it matches a `specs/
    SiteQualityReport.md` entry, an already-documented, deliberately-
    not-fixed finding restated here for visibility, not a new claim).

Run: python tools/check_navigation_journeys.py
Requires the same setup as tools/check_site_quality.py: `mkdocs build`
already run, Node.js with the global `playwright` package, and
`npm install --prefix tools` (axe-core) done once.
"""
from __future__ import annotations
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
NODE_SCRIPT = os.path.join(ROOT, "tools", "_navigation_journeys_check.js")
PORT = 8933


def serve_site():
    os.chdir(SITE)
    handler = http.server.SimpleHTTPRequestHandler

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    httpd = ReusableTCPServer(("127.0.0.1", PORT), handler)
    httpd.serve_forever()


def main() -> int:
    if not os.path.exists(os.path.join(SITE, "index.html")):
        print("check_navigation_journeys: site/ not built — run `mkdocs build` first. "
              "Not fabricating a result.")
        return 1
    if not os.path.exists(NODE_SCRIPT):
        print(f"check_navigation_journeys: {NODE_SCRIPT} missing.")
        return 1

    t = threading.Thread(target=serve_site, daemon=True)
    t.start()
    time.sleep(0.5)

    env = dict(os.environ)
    node_modules = os.path.join(ROOT, "tools", "node_modules")
    if not os.path.isdir(node_modules):
        print("check_navigation_journeys: tools/node_modules/ missing — run "
              "`npm install --prefix tools` first (installs axe-core). "
              "Not fabricating a result.")
        return 1
    global_modules = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env["NODE_PATH"] = f"{node_modules}:{global_modules}"
    env["SITE_BASE_URL"] = f"http://127.0.0.1:{PORT}"

    result = subprocess.run(["node", NODE_SCRIPT], capture_output=True, text=True, env=env, cwd=ROOT, timeout=150)
    print(result.stdout)
    if result.returncode != 0 and not result.stdout.strip():
        print(result.stderr, file=sys.stderr)
        return result.returncode

    try:
        report = json.loads(result.stdout.strip().splitlines()[-1])
    except Exception:
        print("check_navigation_journeys: could not parse JSON summary from Node script output.")
        return 1

    print(f"\ncheck_navigation_journeys: {report.get('total', '?')} checks, "
          f"{report.get('failures', '?')} failure(s). See output above for detail — "
          f"a failure matching an already-documented specs/SiteQualityReport.md "
          f"finding is not a new regression, restated here for visibility.")
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
