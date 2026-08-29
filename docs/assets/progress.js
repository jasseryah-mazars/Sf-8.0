// Guided-navigation support (learner-experience mission, this run):
//   1. Records the last content page visited, in localStorage, so the
//      dashboard can offer "Continue where you left off" — extends the
//      quiz tool's own existing sfq-stats-v1 mechanism rather than
//      inventing a second one. No backend, no cookies, static-site safe.
//   2. Injects a small, universal "quick actions" strip (back to this
//      chapter's domain / test this topic) on every page that lives
//      inside one of the 15 official topic-area directories — derived
//      purely from the URL, so it works on all ~176 chapters without
//      editing each one by hand.
//   3. Renders the dashboard's own "Continue" / weak-area widgets when a
//      placeholder container for them is present on the page (the
//      dashboard is the only page that has one).
(function () {
  "use strict";

  var LAST_PAGE_KEY = "sf-last-page-v1";
  var STATS_KEY = "sfq-stats-v1"; // shared with quiz.js — read-only here

  // slug (matches the docs/<slug>/ directory and mkdocs nav) -> the exact
  // display name used in docs/assets/quiz-data.json's `areas` list, so a
  // "test this topic" link can pre-filter the simulator by an exact match.
  var AREA_NAMES = {
    "php-web-security": "PHP & Web Security",
    "http": "HTTP",
    "architecture": "Symfony Architecture",
    "controllers": "Controllers",
    "routing": "Routing",
    "twig": "Templating (Twig)",
    "forms": "Forms",
    "validation": "Data Validation",
    "dependency-injection": "Dependency Injection",
    "security": "Security",
    "http-caching": "HTTP Caching",
    "console": "Console",
    "messenger": "Messenger",
    "testing": "Automated Tests",
    "miscellaneous": "Miscellaneous"
  };

  function pathParts() {
    var parts = location.pathname.split("/").filter(Boolean);
    var isFr = parts[0] === "fr";
    if (isFr) parts.shift();
    return { parts: parts, isFr: isFr };
  }

  function currentAreaSlug() {
    var p = pathParts().parts;
    return p.length && AREA_NAMES.hasOwnProperty(p[0]) ? p[0] : null;
  }

  function isAreaIndexPage(slug) {
    var p = pathParts().parts;
    return p.length === 1 && p[0] === slug;
  }

  function loadJSON(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }

  function saveJSON(key, value) {
    try { window.localStorage.setItem(key, JSON.stringify(value)); }
    catch (e) { /* private mode / quota — never break the page for this */ }
  }

  // --- 1. record the visit -------------------------------------------------
  function recordVisit() {
    var slug = currentAreaSlug();
    if (!slug) return;
    var h1 = document.querySelector(".md-content h1");
    saveJSON(LAST_PAGE_KEY, {
      path: location.pathname,
      title: h1 ? h1.textContent.trim() : document.title,
      area: slug,
      ts: Date.now()
    });
  }

  // --- 2. quick-actions strip on every area page --------------------------
  function injectQuickActions() {
    var slug = currentAreaSlug();
    if (!slug) return;
    var content = document.querySelector(".md-content__inner");
    if (!content || content.querySelector(".sf-quickactions")) return;

    var p = pathParts();
    var prefix = p.isFr ? "/fr" : "";
    var areaDisplay = AREA_NAMES[slug];
    var backHref = prefix + "/" + slug + "/";
    var testHref = prefix + "/exam-simulator/?area=" + encodeURIComponent(areaDisplay);

    var bar = document.createElement("p");
    bar.className = "sf-quickactions";
    var links = [];
    if (!isAreaIndexPage(slug)) {
      links.push('<a href="' + backHref + '">↑ ' +
        (p.isFr ? "Retour au domaine" : "Back to domain") + "</a>");
    }
    links.push('<a href="' + testHref + '">✓ ' +
      (p.isFr ? "Tester ce sujet" : "Test this topic") + "</a>");
    bar.innerHTML = links.join(" · ");

    var h1 = content.querySelector("h1");
    if (h1 && h1.nextSibling) content.insertBefore(bar, h1.nextSibling);
    else content.insertBefore(bar, content.firstChild);
  }

  // --- 3. dashboard widgets (only present where the container exists) -----
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function weakestArea(minAttempts) {
    var stats = loadJSON(STATS_KEY, { areas: {} });
    var best = null;
    Object.keys(stats.areas || {}).forEach(function (name) {
      var a = stats.areas[name];
      if (a.n >= minAttempts) {
        var pct = a.c / a.n;
        if (!best || pct < best.pct) best = { name: name, pct: pct, n: a.n };
      }
    });
    return best;
  }

  function renderDashboardWidget() {
    var box = document.getElementById("sf-resume");
    if (!box) return;
    var isFr = pathParts().isFr;
    var last = loadJSON(LAST_PAGE_KEY, null);
    var weak = weakestArea(3);
    var lines = [];

    if (last && last.path && last.path !== location.pathname) {
      lines.push(
        '<p class="sf-resume__line"><a class="sf-resume__cta" href="' + last.path + '">' +
        (isFr ? "▶ Continuer : " : "▶ Continue: ") +
        (last.title || last.path) + "</a></p>"
      );
    } else {
      lines.push(
        '<p class="sf-resume__line">' +
        (isFr
          ? "Aucune progression enregistrée sur cet appareil pour l'instant — ouvrez un chapitre pour commencer."
          : "No progress recorded on this device yet — open a chapter to get started.") +
        "</p>"
      );
    }

    if (weak) {
      var pctTxt = Math.round(weak.pct * 100) + "%";
      lines.push(
        '<p class="sf-resume__line sf-resume__weak">' +
        (isFr
          ? "Point faible détecté : <strong>" + weak.name + "</strong> (" + pctTxt +
            " sur " + weak.n + " tentatives) — "
          : "Weak spot detected: <strong>" + weak.name + "</strong> (" + pctTxt +
            " over " + weak.n + " attempts) — ") +
        '<a href="' + (isFr ? "/fr" : "") + "/exam-simulator/?area=" +
        encodeURIComponent(weak.name) + '">' +
        (isFr ? "réviser ce domaine" : "review this area") + "</a></p>"
      );
    }

    box.innerHTML = lines.join("");
  }

  function init() {
    recordVisit();
    injectQuickActions();
    renderDashboardWidget();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState !== "loading") {
    init();
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
