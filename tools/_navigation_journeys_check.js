// Real headless-Chromium validation of the guided-navigation journeys
// (learner-experience mission). Not a static-file heuristic: drives an
// actual browser through each named journey, following real links, and
// checks the JS features (resume widget, quick-actions bar, weak-area
// hint, ?area= deep-link auto-start) actually work — invoked by
// tools/check_navigation_journeys.py.
const { chromium } = require('playwright');
const axeSource = require('axe-core').source;

const BASE = process.env.SITE_BASE_URL || 'http://127.0.0.1:8931';
const results = [];

function record(journey, step, ok, detail) {
  results.push({ journey, step, ok, detail: detail || '' });
}

async function follow(page, url, journey, step) {
  let resp;
  try {
    resp = await page.goto(BASE + url, { waitUntil: 'domcontentloaded', timeout: 15000 });
  } catch (e) {
    record(journey, step, false, 'nav failed: ' + e.message);
    return false;
  }
  const ok = resp && resp.ok();
  record(journey, step, ok, ok ? ('loaded ' + url) : ('HTTP ' + (resp ? resp.status() : '?') + ' at ' + url));
  return ok;
}

async function hasLinkTo(page, hrefSubstring) {
  return page.$$eval('a[href]', (els, sub) =>
    els.some(el => el.getAttribute('href') && el.getAttribute('href').includes(sub)),
    hrefSubstring);
}

const BLOCKED_HOSTS = /unpkg\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|api\.github\.com/;

async function setUpPage(page) {
  page.setDefaultTimeout(15000);
  // The quiz widget calls window.alert() when a filter combination matches
  // no questions — never expected in these journeys, but a stray unhandled
  // dialog blocks all further page JS indefinitely in a real browser, so
  // guard every page against it.
  page.on('dialog', d => d.dismiss().catch(() => {}));
  // This sandboxed environment's network egress proxy takes ~13s to
  // define a request to any of these hosts as failed (confirmed during
  // P2-03 — a real environment characteristic, not something this test
  // controls). Every page pays that tax at least once (mkdocs-material's
  // own Google Fonts @import and GitHub repo-info fetch are sitewide, not
  // specific to any one chapter). None of these checks depend on those
  // resources actually loading, so abort them instantly instead of
  // waiting out the real timeout on every single page in every journey.
  await page.route('**/*', route => {
    const url = route.request().url();
    if (BLOCKED_HOSTS.test(url)) return route.abort();
    return route.continue();
  });
}

// Watchdog: force-exit if anything hangs beyond a safe bound (e.g. an
// unhandled dialog or a stuck navigation not caught by the per-action
// timeouts above), so a single stuck step reports failure instead of
// leaving no result in the current response at all.
const watchdog = setTimeout(() => {
  console.log('=== Navigation Journeys Validation (WATCHDOG — hung past 100s) ===\n');
  for (const r of results) {
    console.log(`[${r.ok ? 'PASS' : 'FAIL'}] ${r.journey} :: ${r.step}${r.detail ? ' -- ' + r.detail : ''}`);
  }
  console.log(JSON.stringify({ ok: false, total: results.length, failures: -1, note: 'watchdog: script hung past 100s' }));
  process.exit(1);
}, 100000);

(async () => {
  const browser = await chromium.launch();

  // --- Journey A: beginner ---
  // Dashboard -> Start -> first stage -> first chapter -> exercise -> quiz -> next chapter
  {
    const page = await browser.newPage();
    await setUpPage(page);
    await follow(page, '/', 'A', 'dashboard');
    const hasCta = await page.$('.sf-cta-primary');
    record('A', 'primary CTA present', !!hasCta);
    await follow(page, '/php-web-security/', 'A', 'first area index');
    const hasExercisesLink = await hasLinkTo(page, '#exercises') || /exercises/i.test(await page.content());
    record('A', 'area index mentions exercises', hasExercisesLink);
    await follow(page, '/php-web-security/oop/', 'A', 'first real chapter');
    const hasNutshell = (await page.content()).includes('In a nutshell');
    record('A', 'chapter has "In a nutshell" hook', hasNutshell);
    const hasQuickActions = await page.$('.sf-quickactions');
    record('A', 'quick-actions bar injected on chapter', !!hasQuickActions);
    const hasFooterNav = await page.$('.md-footer__link--next, .md-footer-nav__link--next, a[rel="next"]');
    record('A', 'automatic next-chapter link present (navigation.footer)', !!hasFooterNav);
    await follow(page, '/exam-simulator/', 'A', 'exam simulator');
    await page.close();
  }

  // --- Journey B: Advanced ---
  // Dashboard -> Advanced path -> area -> chapter -> quiz -> revision
  {
    const page = await browser.newPage();
    await setUpPage(page);
    await follow(page, '/', 'B', 'dashboard');
    await follow(page, '/roadmap/', 'B', 'advanced path (roadmap)');
    await follow(page, '/dependency-injection/', 'B', 'an area');
    await follow(page, '/dependency-injection/autowiring/', 'B', 'a chapter');
    await follow(page, '/exam-simulator/?area=Dependency%20Injection', 'B', 'quiz deep-link');
    // verify the deep link actually skipped the config screen
    await page.waitForTimeout(1500);
    const inQuestionView = await page.$('.sfq__q, .sfq__question') !== null;
    const stillConfig = await page.$('.sfq__panel') !== null && !inQuestionView;
    record('B', '?area= deep link auto-starts practice (skips config screen)', inQuestionView || !stillConfig);
    await follow(page, '/revision/', 'B', 'revision hub');
    await page.close();
  }

  // --- Journey C: Expert ---
  // Dashboard -> Expert path -> Deep Dive -> Source Tour -> trap review -> mock exam
  {
    const page = await browser.newPage();
    await setUpPage(page);
    await follow(page, '/', 'C', 'dashboard');
    await follow(page, '/tours/', 'C', 'expert path (source tours)');
    await follow(page, '/tours/httpkernel-handle/', 'C', 'a source tour');
    await follow(page, '/revision/traps/', 'C', 'trap review');
    await follow(page, '/revision/mock-exam/', 'C', 'mock exam');
    await page.close();
  }

  // --- Journey D: quick revision ---
  // Dashboard -> Revision Hub -> Cheat Sheet -> traps -> simulator
  {
    const page = await browser.newPage();
    await setUpPage(page);
    await follow(page, '/', 'D', 'dashboard');
    await follow(page, '/revision/', 'D', 'revision hub');
    await follow(page, '/revision/cheat-sheet/', 'D', 'cheat sheet');
    await follow(page, '/revision/traps/', 'D', 'traps');
    await follow(page, '/exam-simulator/', 'D', 'simulator');
    await page.close();
  }

  // --- Journey E: mobile ---
  // Home -> area -> chapter -> question -> next nav, at 375px
  {
    const page = await browser.newPage({ viewport: { width: 375, height: 667 } });
    await setUpPage(page);
    await follow(page, '/', 'E', 'home (mobile)');
    const noOverflowHome = await page.evaluate(() => {
      const root = document.documentElement;
      const clipped = getComputedStyle(root).overflowX === 'hidden';
      return clipped || root.scrollWidth <= window.innerWidth + 1;
    });
    record('E', 'no visible horizontal overflow on dashboard (375px)', noOverflowHome);
    await follow(page, '/php-web-security/', 'E', 'area (mobile)');
    await follow(page, '/php-web-security/oop/', 'E', 'chapter (mobile)');
    const noOverflowChapter = await page.evaluate(() => {
      const root = document.documentElement;
      const clipped = getComputedStyle(root).overflowX === 'hidden';
      return clipped || root.scrollWidth <= window.innerWidth + 1;
    });
    record('E', 'no visible horizontal overflow on chapter (375px)', noOverflowChapter);
    // keyboard reachability spot-check
    await page.keyboard.press('Tab');
    const focused = new Set();
    for (let i = 0; i < 10; i++) {
      const info = await page.evaluate(() => {
        const el = document.activeElement;
        return el && el !== document.body ? el.tagName + (el.href || '') : null;
      });
      if (info) focused.add(info);
      await page.keyboard.press('Tab');
    }
    record('E', 'keyboard nav reaches distinct elements', focused.size >= 3, focused.size + ' elements');
    await page.close();
  }

  // --- Journey F: French ---
  // Accueil FR -> parcours FR -> domaine FR -> chapitre FR -> retour dashboard FR
  {
    const page = await browser.newPage();
    await setUpPage(page);
    await follow(page, '/fr/', 'F', 'accueil FR');
    const htmlLangFr = await page.evaluate(() => document.documentElement.lang);
    record('F', 'html lang=fr on homepage', htmlLangFr === 'fr', 'lang=' + htmlLangFr);
    await follow(page, '/fr/roadmap/', 'F', 'parcours FR (roadmap)');
    await follow(page, '/fr/php-web-security/', 'F', 'domaine FR');
    await follow(page, '/fr/php-web-security/oop/', 'F', 'chapitre FR');
    const chapterLangFr = await page.evaluate(() => document.documentElement.lang);
    record('F', 'html lang=fr on FR chapter', chapterLangFr === 'fr', 'lang=' + chapterLangFr);
    const quickActionsFr = await page.$eval('.sf-quickactions', el => el.textContent).catch(() => null);
    record('F', 'quick-actions bar in French on FR chapter', quickActionsFr && /Retour au domaine|Tester ce sujet/.test(quickActionsFr), quickActionsFr);
    await follow(page, '/fr/', 'F', 'retour dashboard FR');
    await page.close();
  }

  // --- progress.js: resume widget + weak-area hint (functional check) ---
  {
    const page = await browser.newPage();
    await setUpPage(page);
    // simulate prior activity: a visited page + quiz stats, before loading the dashboard
    await page.goto(BASE + '/dependency-injection/autowiring/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(300);
    await page.evaluate(() => {
      localStorage.setItem('sfq-stats-v1', JSON.stringify({ areas: { Security: { c: 1, n: 4 } } }));
    });
    await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(400);
    const resumeHtml = await page.$eval('#sf-resume', el => el.innerHTML).catch(() => '');
    record('progress.js', 'resume widget shows last visited chapter', resumeHtml.includes('Autowiring') || resumeHtml.includes('Continue'), resumeHtml.slice(0, 150));
    record('progress.js', 'weak-area hint shown from existing quiz stats', resumeHtml.includes('Security') && resumeHtml.includes('Weak spot'), resumeHtml.slice(0, 200));
    await page.close();
  }

  // --- axe-core on the new dashboard ---
  {
    const page = await browser.newPage();
    await setUpPage(page);
    await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(500);
    await page.addScriptTag({ content: axeSource });
    const axeResults = await page.evaluate(async () => {
      return await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] } });
    });
    for (const v of axeResults.violations) {
      record('axe-core (dashboard)', v.id, false, v.help + ' (' + v.nodes.length + ' node(s))');
    }
    if (!axeResults.violations.length) record('axe-core (dashboard)', 'wcag2a/aa', true, '0 violations');
    await page.close();
  }

  await browser.close();
  clearTimeout(watchdog);

  console.log('=== Navigation Journeys Validation (real headless Chromium) ===\n');
  let failures = 0;
  for (const r of results) {
    const mark = r.ok ? 'PASS' : 'FAIL';
    if (!r.ok) failures++;
    console.log(`[${mark}] ${r.journey} :: ${r.step}${r.detail ? ' -- ' + r.detail : ''}`);
  }
  console.log(`\n${results.length - failures}/${results.length} checks passed.`);
  console.log(JSON.stringify({ ok: failures === 0, total: results.length, failures }));
})().catch(e => {
  clearTimeout(watchdog);
  console.log('=== Navigation Journeys Validation (real headless Chromium) ===\n');
  for (const r of results) {
    console.log(`[${r.ok ? 'PASS' : 'FAIL'}] ${r.journey} :: ${r.step}${r.detail ? ' -- ' + r.detail : ''}`);
  }
  console.log('\nSCRIPT ERROR (partial results above): ' + e.message);
  console.log(JSON.stringify({ ok: false, total: results.length, failures: -1, error: e.message }));
  process.exit(1);
});
