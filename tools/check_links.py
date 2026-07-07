#!/usr/bin/env python3
"""Link-rot checker for the Symfony 8.0 cert-prep site.

Scans ``docs/**/*.md`` and ``quiz/*.yml`` for external ``http(s)`` links
(markdown ``[txt](url)``, bare URLs, and quiz ``documentation:`` values),
then checks each one over the network and writes a Markdown report.

Standard-library only (``urllib``, ``re``, ``concurrent.futures``, ``argparse``).
``pyyaml`` is used for quiz files *if available*, otherwise a regex fallback is
used, so the script never hard-depends on a third-party package.

Status model:
  * HTTP 200-399                     -> OK
  * HTTP 404 / 410, connection fail  -> DEAD
  * HTTP 429 / 5xx (transient)       -> WARN (flaky, not a hard failure)

Exit code: 0 if no DEAD links (or ``--offline``), 1 if any DEAD link found.

Usage:
    python3 tools/check_links.py                       # full network check
    python3 tools/check_links.py --offline             # parse + list only
    python3 tools/check_links.py --report path/to.md   # override report path
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(ROOT, "docs")
QUIZ_DIR = os.path.join(ROOT, "quiz")
DEFAULT_REPORT = os.path.join(ROOT, "specs", "LinkCheckReport.md")

# Hosts known to aggressively block bots. URLs on these hosts are skipped
# (reported as SKIPPED, never DEAD). Kept empty by default on purpose.
ALLOWLIST_SKIP_HOSTS: tuple[str, ...] = ()

TIMEOUT = 15
MAX_WORKERS = 8
RETRIES = 1  # one extra attempt on a network error
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "SymfonyCertPrep-LinkChecker/1.0"
)

# --- URL extraction ---------------------------------------------------------

# Markdown inline link: [text](http...)  -- capture the URL group.
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(\s*(https?://[^)\s]+?)\s*\)")
# Any bare http(s) URL. Trailing punctuation is trimmed afterwards.
BARE_URL_RE = re.compile(r"https?://[^\s)>\]\"'`]+")
# quiz `documentation:` value (quoted or bare) fallback when yaml is absent.
DOC_LINE_RE = re.compile(
    r'documentation:\s*["\']?(https?://[^\s"\']+)["\']?'
)

# Characters commonly glued to the end of an inline URL in prose.
_TRAILING = ".,;:!?)"

# Local / example / placeholder hosts that are not real external doc links and
# must never be reported as DEAD (they only appear in code samples & prose).
NON_CHECKABLE_HOSTS = (
    "localhost",
    "127.0.0.1",
    "example.com",
    "example.org",
    "example.net",
)


def _is_checkable(url: str) -> bool:
    """True if this looks like a real, resolvable external doc link."""
    # Placeholder URLs sometimes contain non-ASCII (e.g. an ellipsis) or no
    # domain dot at all — skip those, they are documentation shorthand.
    if any(ord(ch) > 127 for ch in url):
        return False
    host = _host(url)
    if not host or "." not in host:
        return False
    if host in NON_CHECKABLE_HOSTS:
        return False
    return True


def _clean(url: str) -> str:
    """Trim trailing punctuation / balance parens on a bare-scanned URL."""
    url = url.strip()
    while url and url[-1] in _TRAILING:
        # Keep a closing paren only if it balances an opening one in the URL.
        if url[-1] == ")" and url.count("(") > url.count(")"):
            break
        url = url[:-1]
    return url


def iter_markdown_files() -> list[str]:
    out: list[str] = []
    for dirpath, _dirs, files in os.walk(DOCS_DIR):
        for name in files:
            if name.endswith(".md"):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def iter_quiz_files() -> list[str]:
    if not os.path.isdir(QUIZ_DIR):
        return []
    return sorted(
        os.path.join(QUIZ_DIR, n)
        for n in os.listdir(QUIZ_DIR)
        if n.endswith(".yml") or n.endswith(".yaml")
    )


def extract_from_markdown(text: str) -> set[str]:
    urls: set[str] = set()
    for m in MD_LINK_RE.finditer(text):
        urls.add(_clean(m.group(1)))
    for m in BARE_URL_RE.finditer(text):
        urls.add(_clean(m.group(0)))
    return {u for u in urls if u}


def _yaml_docs(path: str) -> set[str] | None:
    """Return documentation URLs via pyyaml, or None if pyyaml is unavailable."""
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    urls: set[str] = set()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception:
        return None

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "documentation" and isinstance(v, str):
                    v = v.strip()
                    if v.startswith("http"):
                        urls.add(_clean(v))
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return urls


def extract_from_quiz(path: str, text: str) -> set[str]:
    via_yaml = _yaml_docs(path)
    if via_yaml is not None:
        return via_yaml
    # Regex fallback (no yaml dependency).
    return {_clean(m.group(1)) for m in DOC_LINE_RE.finditer(text)}


def collect_urls() -> dict[str, set[str]]:
    """Map each unique URL -> set of source file paths (repo-relative)."""
    url_sources: dict[str, set[str]] = defaultdict(set)
    for path in iter_markdown_files():
        try:
            text = open(path, "r", encoding="utf-8").read()
        except OSError:
            continue
        rel = os.path.relpath(path, ROOT)
        for url in extract_from_markdown(text):
            if _is_checkable(url):
                url_sources[url].add(rel)
    for path in iter_quiz_files():
        try:
            text = open(path, "r", encoding="utf-8").read()
        except OSError:
            continue
        rel = os.path.relpath(path, ROOT)
        for url in extract_from_quiz(path, text):
            if _is_checkable(url):
                url_sources[url].add(rel)
    return url_sources


# --- Network checking -------------------------------------------------------

def _host(url: str) -> str:
    try:
        return urllib.parse.urlsplit(url).hostname or ""
    except Exception:
        return ""


def _request(url: str, method: str) -> int:
    req = urllib.request.Request(url, method=method)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "*/*")
    opener = urllib.request.build_opener()  # follows redirects by default
    with opener.open(req, timeout=TIMEOUT) as resp:
        return getattr(resp, "status", None) or resp.getcode()


def classify(url: str) -> tuple[str, str]:
    """Return (status, detail) where status is OK / WARN / DEAD / SKIPPED."""
    host = _host(url)
    if host and any(
        host == h or host.endswith("." + h) for h in ALLOWLIST_SKIP_HOSTS
    ):
        return "SKIPPED", "allowlisted host"

    last_err = ""
    for attempt in range(RETRIES + 1):
        # Try HEAD first, fall back to GET on 403/405 (or on any HTTPError we
        # want to double-check with a real GET).
        for method in ("HEAD", "GET"):
            try:
                code = _request(url, method)
                if 200 <= code < 400:
                    return "OK", f"HTTP {code}"
                if code in (404, 410):
                    return "DEAD", f"HTTP {code}"
                if code == 429 or 500 <= code < 600:
                    return "WARN", f"HTTP {code}"
                # Other 4xx: treat as WARN (often bot-blocking, e.g. 401/406).
                return "WARN", f"HTTP {code}"
            except urllib.error.HTTPError as e:
                if method == "HEAD" and e.code in (403, 405):
                    continue  # retry same URL with GET
                if e.code in (404, 410):
                    return "DEAD", f"HTTP {e.code}"
                if e.code == 429 or 500 <= e.code < 600:
                    return "WARN", f"HTTP {e.code}"
                return "WARN", f"HTTP {e.code}"
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last_err = getattr(e, "reason", None) or str(e)
                last_err = str(last_err)
                break  # network error: don't try GET, go to retry loop
    return "DEAD", f"network error: {last_err}"


# --- Reporting --------------------------------------------------------------

def write_report(
    report_path: str,
    results: dict[str, tuple[str, str]],
    sources: dict[str, set[str]],
    totals: dict[str, int],
) -> None:
    dead = sorted(u for u, (s, _) in results.items() if s == "DEAD")
    warn = sorted(u for u, (s, _) in results.items() if s == "WARN")
    skipped = sorted(u for u, (s, _) in results.items() if s == "SKIPPED")

    lines: list[str] = []
    lines.append("# Link Check Report")
    lines.append("")
    lines.append(
        f"- Total unique URLs: **{totals['total']}**"
    )
    lines.append(f"- OK: **{totals['ok']}**")
    lines.append(f"- WARN (flaky, 429/5xx/other): **{totals['warn']}**")
    lines.append(f"- DEAD (404/410/connection failure): **{totals['dead']}**")
    if totals.get("skipped"):
        lines.append(f"- Skipped (allowlisted): **{totals['skipped']}**")
    lines.append("")

    def section(title: str, urls: list[str]) -> None:
        lines.append(f"## {title} ({len(urls)})")
        lines.append("")
        if not urls:
            lines.append("_None._")
            lines.append("")
            return
        for url in urls:
            status, detail = results[url]
            files = ", ".join(f"`{p}`" for p in sorted(sources.get(url, [])))
            lines.append(f"- {detail} — <{url}>")
            lines.append(f"    - in: {files}")
        lines.append("")

    section("DEAD links", dead)
    section("WARN links", warn)
    if skipped:
        section("Skipped links", skipped)

    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# --- Main -------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check for broken doc links.")
    parser.add_argument(
        "--report", default=DEFAULT_REPORT, help="Markdown report output path."
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip the network; just list URLs that would be checked. Exit 0.",
    )
    args = parser.parse_args(argv)

    sources = collect_urls()
    urls = sorted(sources)
    print(f"Found {len(urls)} unique external URL(s).")

    if args.offline:
        for url in urls:
            print(f"  {url}  <- {', '.join(sorted(sources[url]))}")
        print(f"[offline] {len(urls)} URL(s) would be checked. No network used.")
        return 0

    results: dict[str, tuple[str, str]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        future_to_url = {ex.submit(classify, u): u for u in urls}
        for fut in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[fut]
            try:
                results[url] = fut.result()
            except Exception as e:  # never let one URL crash the run
                results[url] = ("DEAD", f"checker error: {e}")

    totals = {
        "total": len(urls),
        "ok": sum(1 for s, _ in results.values() if s == "OK"),
        "warn": sum(1 for s, _ in results.values() if s == "WARN"),
        "dead": sum(1 for s, _ in results.values() if s == "DEAD"),
        "skipped": sum(1 for s, _ in results.values() if s == "SKIPPED"),
    }

    for url in urls:
        status, detail = results[url]
        if status in ("DEAD", "WARN"):
            print(f"  [{status}] {detail}  {url}")

    print(
        f"Summary: total={totals['total']} ok={totals['ok']} "
        f"warn={totals['warn']} dead={totals['dead']} "
        f"skipped={totals['skipped']}"
    )

    write_report(args.report, results, sources, totals)
    print(f"Report written to {args.report}")

    return 1 if totals["dead"] else 0


if __name__ == "__main__":
    sys.exit(main())
