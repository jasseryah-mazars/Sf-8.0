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

      // mkdocs-material renders each diagram into a CLOSED shadow root:
      //   r = div.mermaid; {svg} = await mermaid.render(id, text);
      //   a = r.attachShadow({mode:"closed"}); a.innerHTML = svg; e.replaceWith(r)
      // A closed root is unreachable from page scripts and from Playwright, so
      // `.mermaid svg` can never match and a naive check reports a false failure.
      // Forcing the mode to "open" for the test is behaviour-identical for the page
      // and lets us assert on the real rendered SVG instead of guessing from proxies.
      await page.addInitScript(() => {
        const orig = Element.prototype.attachShadow;
        Element.prototype.attachShadow = function (init) {
          return orig.call(this, { ...init, mode: 'open' });
        };
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

        // Success is `pre.mermaid` becoming `div.mermaid` carrying a shadow root with
        // an <svg>: replaceWith only runs after mermaid.render() resolves, so an
        // unreplaced <pre> means the render threw.
        try {
          await page.waitForFunction((n) => {
            const rendered = [...document.querySelectorAll('div.mermaid')]
              .filter((d) => d.shadowRoot && d.shadowRoot.querySelector('svg'));
            return rendered.length >= n;
          }, blocks, { timeout: 25000 });
        } catch { /* fall through to the counted assertion below */ }

        const probe = await page.evaluate(() => {
          const divs = [...document.querySelectorAll('div.mermaid')];
          const withSvg = divs.filter((d) => d.shadowRoot && d.shadowRoot.querySelector('svg'));
          const shadowText = divs
            .map((d) => (d.shadowRoot ? d.shadowRoot.textContent || '' : ''))
            .join('\n');
          const errInShadow = divs.filter(
            (d) => d.shadowRoot && d.shadowRoot.querySelector('.error-text, .mermaid-error')
          ).length;
          return {
            svgs: withSvg.length,
            unrendered: document.querySelectorAll('pre.mermaid').length,
            errInShadow,
            shadowSyntaxError: /Syntax error in text/i.test(shadowText),
            zeroHeight: withSvg.filter((d) => d.getBoundingClientRect().height < 2).length,
          };
        });

        const svgs = probe.svgs;
        const bodyText = await page.evaluate(() => document.body.innerText || '');
        const hasSyntaxError = /Syntax error in text/i.test(bodyText) || probe.shadowSyntaxError;

        const problems = [];
        if (blocks === 0) problems.push('no .mermaid blocks found on a page expected to have one');
        if (probe.unrendered > 0)
          problems.push(`${probe.unrendered} block(s) left as <pre> — mermaid.render() threw`);
        if (svgs < blocks) problems.push(`${blocks} block(s) but only ${svgs} rendered <svg>`);
        if (probe.zeroHeight > 0)
          problems.push(`${probe.zeroHeight} diagram(s) rendered with no height`);
        if (probe.errInShadow > 0)
          problems.push(`${probe.errInShadow} mermaid error node(s) in the rendered SVG`);
        if (hasSyntaxError) problems.push('"Syntax error in text" is present in the rendered output');
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
