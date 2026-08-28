/**
 * Headless Mermaid syntax validator — driver for tools/validate_mermaid.py.
 *
 * Parses every supplied diagram with the EXACT Mermaid build the site ships
 * (tools/node_modules/mermaid, pinned in tools/package.json), inside real
 * Chromium. This is deliberately not a regex check: only the real engine can
 * tell whether a diagram renders, and only the site's own version can tell
 * whether it renders *here*.
 *
 * Two passes per diagram:
 *   1. mermaid.parse()  — the grammar gate. Raises on bad syntax.
 *   2. mermaid.render() — the rendering gate. Catches diagrams that parse but
 *      blow up while building the SVG, and proves an <svg> is actually produced.
 *
 * Input  (stdin, JSON): {"mermaidPath": "...", "blocks": [{"id","file","line","text"}]}
 * Output (stdout, JSON): {"version": "...", "results": [{"id","ok","stage","error"}]}
 * Exit code is always 0 — the Python wrapper owns pass/fail policy.
 */
'use strict';

const fs = require('fs');
const { chromium } = require(require.resolve('playwright', { paths: (process.env.NODE_PATH || '').split(':').filter(Boolean) }));

function readStdin() {
  return new Promise((resolve, reject) => {
    let buf = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (c) => { buf += c; });
    process.stdin.on('end', () => resolve(buf));
    process.stdin.on('error', reject);
  });
}

(async () => {
  let payload;
  try {
    payload = JSON.parse(await readStdin());
  } catch (e) {
    console.log(JSON.stringify({ fatal: `could not parse stdin JSON: ${e.message}` }));
    return;
  }

  const { mermaidPath, blocks } = payload;
  if (!fs.existsSync(mermaidPath)) {
    console.log(JSON.stringify({ fatal: `mermaid bundle not found at ${mermaidPath}` }));
    return;
  }
  const mermaidSrc = fs.readFileSync(mermaidPath, 'utf8');

  let browser;
  try {
    browser = await chromium.launch({ args: ['--no-sandbox'] });
  } catch (e) {
    console.log(JSON.stringify({ fatal: `could not launch Chromium: ${e.message}` }));
    return;
  }

  const page = await browser.newPage();
  const pageErrors = [];
  page.on('pageerror', (e) => pageErrors.push(String(e).slice(0, 300)));
  // A blank page keeps this fully offline — no CDN, no network, no site build needed.
  await page.setContent('<!doctype html><html><body><div id="sink"></div></body></html>');

  // Use the self-contained UMD bundle (dist/mermaid.min.js) — the same file the site
  // loads. The ESM build is a small stub that lazy-imports ./chunks/*.mjs, which cannot
  // resolve without a real HTTP origin; the UMD bundle has no such dependency.
  await page.addScriptTag({ content: mermaidSrc });

  const ready = await page.evaluate(() => {
    let m = window.mermaid
      || (window.__esbuild_esm_mermaid_nm && window.__esbuild_esm_mermaid_nm.mermaid);
    if (m && m.default) m = m.default;
    if (!m || typeof m.parse !== 'function' || typeof m.render !== 'function') return false;
    window.__mermaid = m;
    m.initialize({ startOnLoad: false, securityLevel: 'loose' });
    return true;
  });

  if (!ready) {
    await browser.close();
    console.log(JSON.stringify({
      fatal: 'mermaid bundle loaded but exposed no usable parse()/render() API'
             + (pageErrors.length ? ` — page errors: ${pageErrors.join(' | ')}` : ''),
    }));
    return;
  }

  // The bundle does not reliably expose a version accessor; the authoritative version is
  // the pinned one the Python wrapper already checked in package.json.
  const version = 'bundle loaded from tools/node_modules/mermaid';

  const results = [];
  for (const b of blocks) {
    const r = await page.evaluate(async ({ id, text }) => {
      const m = window.__mermaid;
      try {
        await m.parse(text);
      } catch (e) {
        return { id, ok: false, stage: 'parse', error: String(e && e.message ? e.message : e) };
      }
      try {
        // Unique id per render; mermaid injects a temp node keyed on it.
        const { svg } = await m.render('mmd_' + id.replace(/[^a-zA-Z0-9_]/g, '_'), text);
        if (!svg || !svg.includes('<svg')) {
          return { id, ok: false, stage: 'render', error: 'render() returned no <svg>' };
        }
        if (/Syntax error in text/i.test(svg)) {
          return { id, ok: false, stage: 'render', error: 'rendered SVG contains "Syntax error in text"' };
        }
        return { id, ok: true, stage: 'render', error: null };
      } catch (e) {
        return { id, ok: false, stage: 'render', error: String(e && e.message ? e.message : e) };
      }
    }, { id: b.id, text: b.text });
    results.push(r);
  }

  await browser.close();
  console.log(JSON.stringify({ version, results }));
})().catch((e) => {
  console.log(JSON.stringify({ fatal: String(e && e.stack ? e.stack : e) }));
});
