/**
 * Browser-side Mermaid render check — driver for tools/check_mermaid_render.py.
 *
 * tools/validate_mermaid.py proves a diagram *parses and renders* in isolation.
 * This proves the built site actually renders it to the reader: correct asset
 * wiring, correct engine version, no CDN dependency, no error node in the DOM.
 *
 * Per page it asserts:
 *   - one <svg> per `.mermaid` block (fewer means a diagram silently failed);
 *   - no `.mermaid-error` node, and no "Syntax error in text" anywhere in the DOM;
 *   - no mermaid-related console error or page exception;
 *   - no request to an external mermaid CDN (proves the vendored copy is in use);
 * at both a desktop and a mobile viewport.
 *
 * Input  (stdin, JSON): {"base": "http://...", "pages": ["/path/", ...]}
 * Output (stdout, JSON): {"results": [...]}
 */
'use strict';

const { chromium } = require(require.resolve('playwright', {
  paths: (process.env.NODE_PATH || '').split(':').filter(Boolean),
}));

const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 900 },
  { name: 'mobile', width: 375, height: 667 },
];

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
    console.log(JSON.stringify({ fatal: `bad stdin JSON: ${e.message}` }));
    return;
  }
  const { base, pages } = payload;

  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const results = [];

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    for (const path of pages) {
      const page = await ctx.newPage();
      const consoleErrors = [];
      const cdnHits = [];

      page.on('console', (m) => {
        if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 200));
      });
      page.on('pageerror', (e) => consoleErrors.push('pageerror: ' + String(e).slice(0, 200)));
      page.on('request', (r) => {
        const u = r.url();
        if (/mermaid/i.test(u) && !u.startsWith(base)) cdnHits.push(u.slice(0, 160));
      });

      let entry = { viewport: vp.name, path, ok: false, error: null };
      try {
        await page.goto(base + path, { waitUntil: 'domcontentloaded', timeout: 30000 });

        // Material renders diagrams lazily; scroll to force every one into view.
        await page.evaluate(async () => {
          const els = document.querySelectorAll('.mermaid');
          for (const el of els) el.scrollIntoView();
          window.scrollTo(0, 0);
        });

        const blocks = await page.locator('.mermaid').count();

        // Wait until each block has an <svg>, or time out and report the shortfall.
        try {
          await page.waitForFunction((n) => {
            return document.querySelectorAll('.mermaid svg').length >= n;
          }, blocks, { timeout: 20000 });
        } catch { /* fall through to the counted assertion below */ }

        const svgs = await page.locator('.mermaid svg').count();
        const errNodes = await page.locator('.mermaid-error, .error-text').count();
        const bodyText = await page.evaluate(() => document.body.innerText || '');
        const hasSyntaxError = /Syntax error in text/i.test(bodyText);

        const problems = [];
        if (blocks === 0) problems.push('no .mermaid blocks found on a page expected to have one');
        if (svgs < blocks) problems.push(`${blocks} block(s) but only ${svgs} rendered <svg>`);
        if (errNodes > 0) problems.push(`${errNodes} mermaid error node(s) in the DOM`);
        if (hasSyntaxError) problems.push('"Syntax error in text" is visible on the page');
        if (cdnHits.length) problems.push(`external mermaid request: ${cdnHits[0]}`);
        const mermaidConsole = consoleErrors.filter((t) => /mermaid|svg|diagram/i.test(t));
        if (mermaidConsole.length) problems.push(`console error: ${mermaidConsole[0]}`);

        entry.blocks = blocks;
        entry.svgs = svgs;
        entry.ok = problems.length === 0;
        entry.error = problems.length ? problems.join(' | ') : null;
      } catch (e) {
        entry.error = String(e && e.message ? e.message : e).slice(0, 300);
      }
      results.push(entry);
      await page.close();
    }
    await ctx.close();
  }

  await browser.close();
  console.log(JSON.stringify({ results }));
})().catch((e) => {
  console.log(JSON.stringify({ fatal: String(e && e.stack ? e.stack : e).slice(0, 800) }));
});
