/*
 * Interactive exam player for the Symfony 8 Certification Prep platform.
 * Mounts into <div id="sf-quiz" data-src="…/quiz-data.json">.
 *
 * Mirrors the real Symfony exam: every question is answered by SELECTING
 * options — never by typing. Three interactions only:
 *   - True / False        (radio, 2 options)
 *   - Single answer       (radio, exactly one correct)
 *   - Multiple choice     (checkbox, two or more correct)
 * Multiple-choice is scored all-or-nothing: the selected set must equal the
 * correct set exactly, matching the certification's marking.
 *
 * Two modes:
 *   - Practice: instant feedback + explanation after each question.
 *   - Exam:     answers hidden, 90-minute countdown, score + review at the end.
 * No external dependencies; safe with Material's instant navigation.
 */
(function () {
  "use strict";

  var PASS_DEFAULT = 65;

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function setsEqual(a, b) {
    if (a.length !== b.length) return false;
    var s = {};
    a.forEach(function (x) { s[x] = 1; });
    return b.every(function (x) { return s[x]; });
  }

  function fmtTime(sec) {
    sec = Math.max(0, sec | 0);
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  // --- persistent per-topic stats (weak-area memory) ----------------------
  var STATS_KEY = "sfq-stats-v1";

  function loadStats() {
    try {
      var raw = window.localStorage.getItem(STATS_KEY);
      var s = raw ? JSON.parse(raw) : null;
      return (s && s.areas) ? s : { areas: {} };
    } catch (e) { return { areas: {} }; }
  }

  function saveStats(stats) {
    try { window.localStorage.setItem(STATS_KEY, JSON.stringify(stats)); }
    catch (e) { /* private mode / quota — stats are a bonus, never break */ }
  }

  function recordResult(area, correct) {
    var stats = loadStats();
    var a = stats.areas[area] || { c: 0, n: 0 };
    a.n += 1; if (correct) a.c += 1;
    stats.areas[area] = a;
    saveStats(stats);
  }

  function weakestAreas(minAttempts, howMany) {
    var stats = loadStats(), rows = [];
    Object.keys(stats.areas).forEach(function (name) {
      var a = stats.areas[name];
      if (a.n >= minAttempts) rows.push({ name: name, pct: a.c / a.n, n: a.n });
    });
    rows.sort(function (x, y) { return x.pct - y.pct; });
    return rows.slice(0, howMany);
  }

  // --- session state ------------------------------------------------------
  function Player(root, data) {
    this.root = root;
    this.data = data;
    this.pass = (data.exam && data.exam.passPercent) || PASS_DEFAULT;
    this.mode = "practice";
    this.renderConfig();
  }

  Player.prototype.clear = function () {
    if (this._timer) { clearInterval(this._timer); this._timer = null; }
    this.root.innerHTML = "";
  };

  // --- config screen ------------------------------------------------------
  Player.prototype.renderConfig = function () {
    this.clear();
    var self = this, d = this.data;
    var wrap = el("div", "sfq__panel");

    var h = el("div", "sfq__row");
    var modeField = el("div", "sfq__field");
    modeField.appendChild(el("label", null, "Mode"));
    var modes = el("div", "sfq__modes");
    [["practice", "Practice (instant feedback)"], ["exam", "Exam (timed, hidden answers)"]]
      .forEach(function (m) {
        var b = el("button", "sfq__mode", m[1]);
        b.type = "button";
        b.setAttribute("aria-pressed", self.mode === m[0] ? "true" : "false");
        b.addEventListener("click", function () {
          self.mode = m[0];
          Array.prototype.forEach.call(modes.children, function (c) {
            c.setAttribute("aria-pressed", c === b ? "true" : "false");
          });
          countField.style.display = self.mode === "exam" ? "none" : "";
          examNote.style.display = self.mode === "exam" ? "" : "none";
        });
        modes.appendChild(b);
      });
    modeField.appendChild(modes);
    h.appendChild(modeField);

    var countField = el("div", "sfq__field");
    countField.appendChild(el("label", null, "Questions"));
    var count = el("input");
    count.type = "number"; count.min = "5"; count.max = "150"; count.value = "20";
    count.id = "sfq-count";
    countField.appendChild(count);
    h.appendChild(countField);

    var diffField = el("div", "sfq__field");
    diffField.appendChild(el("label", null, "Difficulty"));
    var diff = el("select");
    [["", "All"], ["easy", "Easy"], ["medium", "Medium"], ["hard", "Hard"]]
      .forEach(function (o) { var op = el("option", null, o[1]); op.value = o[0]; diff.appendChild(op); });
    diffField.appendChild(diff);
    h.appendChild(diffField);

    var typeField = el("div", "sfq__field");
    typeField.appendChild(el("label", null, "Question type"));
    var type = el("select");
    [["", "All"], ["True / False", "True / False"], ["Single answer", "Single answer"],
      ["Multiple choice", "Multiple choice"]]
      .forEach(function (o) { var op = el("option", null, o[1]); op.value = o[0]; type.appendChild(op); });
    typeField.appendChild(type);
    h.appendChild(typeField);
    wrap.appendChild(h);

    var areaField = el("div", "sfq__field");
    areaField.style.minWidth = "100%";
    areaField.appendChild(el("label", null, "Topics (all selected by default)"));
    var areas = el("div", "sfq__areas");
    d.areas.forEach(function (a) {
      var lab = el("label");
      var cb = el("input"); cb.type = "checkbox"; cb.value = a; cb.checked = true;
      cb.className = "sfq-area";
      lab.appendChild(cb); lab.appendChild(document.createTextNode(a));
      areas.appendChild(lab);
    });
    areaField.appendChild(areas);
    wrap.appendChild(areaField);

    var examNote = el("p", "sfq__hint",
      "Exam mode runs the official shape: " + d.exam.questions + " questions in " +
      d.exam.minutes + " minutes, answers hidden until you submit, pass mark " + this.pass + "%.");
    examNote.style.display = "none";
    wrap.appendChild(examNote);

    var btns = el("div", "sfq__btns");
    var start = el("button", "sfq__btn", "Start session");
    start.type = "button";
    start.addEventListener("click", function () {
      var selAreas = Array.prototype.filter.call(areas.querySelectorAll(".sfq-area"),
        function (c) { return c.checked; }).map(function (c) { return c.value; });
      self.start({
        areas: selAreas, diff: diff.value, type: type.value,
        count: parseInt(count.value, 10) || 20
      });
    });
    var mock = el("button", "sfq__btn sfq__btn--ghost", "Full mock exam (" + d.exam.questions + "Q · " + d.exam.minutes + "min)");
    mock.type = "button";
    mock.addEventListener("click", function () {
      self.mode = "exam";
      self.start({ areas: d.areas.slice(), diff: "", type: "", count: d.exam.questions });
    });
    btns.appendChild(start); btns.appendChild(mock);

    // Weak-area memory: after ≥3 attempts in ≥1 area, offer a targeted drill.
    var weak = weakestAreas(3, 3);
    if (weak.length) {
      var drill = el("button", "sfq__btn sfq__btn--ghost", "Drill my weaknesses");
      drill.type = "button";
      drill.addEventListener("click", function () {
        self.mode = "practice";
        self.start({
          areas: weak.map(function (w) { return w.name; }),
          diff: "", type: "", count: 20
        });
      });
      btns.appendChild(drill);
    }
    wrap.appendChild(btns);

    if (weak.length) {
      var strip = el("p", "sfq__hint");
      strip.appendChild(el("b", null, "Your weakest areas so far: "));
      strip.appendChild(document.createTextNode(
        weak.map(function (w) {
          return w.name + " (" + Math.round(w.pct * 100) + "% over " + w.n + " Q)";
        }).join(" · ") + "  —  stats live only in this browser. "));
      var reset = el("a", null, "Reset stats");
      reset.href = "#"; reset.style.cursor = "pointer";
      reset.addEventListener("click", function (e) {
        e.preventDefault();
        try { window.localStorage.removeItem(STATS_KEY); } catch (err) {}
        self.renderConfig();
      });
      strip.appendChild(reset);
      wrap.appendChild(strip);
    }

    // Direct "test this topic" deep link: an area page or the dashboard's
    // quick-actions strip (docs/assets/progress.js) can link here with
    // ?area=<exact area name> to skip the config screen entirely and start
    // practicing that one area immediately — matching this mission's
    // "actions directes, un minimum de décisions" goal. Consumed at most
    // once per page load (flag on `self`) so returning to this config
    // screen after finishing that session doesn't re-trigger it, and the
    // param is stripped from the URL so a reload/back doesn't either.
    if (!self._autoStartChecked) {
      self._autoStartChecked = true;
      var urlArea = null;
      try { urlArea = new URLSearchParams(location.search).get("area"); } catch (e) {}
      if (urlArea && d.areas.indexOf(urlArea) !== -1) {
        try {
          var url = new URL(location.href);
          url.searchParams.delete("area");
          history.replaceState(null, "", url);
        } catch (e2) {}
        self.mode = "practice";
        self.start({ areas: [urlArea], diff: "", type: "", count: 20 });
        return;
      }
    }

    this.root.appendChild(wrap);
  };

  // --- start a session ----------------------------------------------------
  Player.prototype.start = function (opts) {
    var d = this.data;
    var areaSet = {};
    (opts.areas.length ? opts.areas : d.areas).forEach(function (a) { areaSet[a] = 1; });
    var pool = d.questions.filter(function (q) {
      if (!areaSet[q.area]) return false;
      if (opts.diff && q.diff !== opts.diff) return false;
      if (opts.type && q.examType !== opts.type) return false;
      return true;
    });
    if (!pool.length) { alert("No questions match those filters. Widen your selection."); return; }

    var n = this.mode === "exam" ? (d.exam.questions) : opts.count;
    n = Math.min(n, pool.length);
    this.questions = shuffle(pool).slice(0, n).map(function (q) {
      return { q: q, options: shuffle(q.a.map(function (o, i) { return { o: o, i: i }; })),
        picked: [], checked: false };
    });
    this.idx = 0;
    if (this.mode === "exam") {
      this.deadline = Date.now() + d.exam.minutes * 60 * 1000;
    }
    this.renderQuestion();
  };

  // --- one question -------------------------------------------------------
  Player.prototype.renderQuestion = function () {
    this.clear();
    var self = this;
    var state = this.questions[this.idx];
    var q = state.q;
    var total = this.questions.length;

    var wrap = el("div", "sfq__panel");

    var bar = el("div", "sfq__bar");
    bar.appendChild(el("span", null, "Question " + (this.idx + 1) + " of " + total));
    var prog = el("div", "sfq__progress");
    var fill = el("i"); fill.style.width = ((this.idx) / total * 100) + "%";
    prog.appendChild(fill); bar.appendChild(prog);
    if (this.mode === "exam") {
      var timer = el("span", "sfq__timer");
      bar.appendChild(timer);
      this._tick(timer);
    }
    wrap.appendChild(bar);

    var tags = el("div", "sfq__tags");
    tags.appendChild(el("span", "sfq__tag sfq__tag--type", q.examType));
    tags.appendChild(el("span", "sfq__tag", q.area));
    tags.appendChild(el("span", "sfq__tag", q.diff));
    if (q.input === "checkbox") tags.appendChild(el("span", "sfq__tag", "select all that apply"));
    wrap.appendChild(tags);

    wrap.appendChild(el("p", "sfq__q", q.q));

    var list = el("ul", "sfq__opts");
    var name = "sfq-q" + this.idx;
    state.options.forEach(function (entry) {
      var li = el("li");
      var lab = el("label", "sfq__opt");
      var inp = el("input");
      inp.type = q.input === "checkbox" ? "checkbox" : "radio";
      inp.name = name; inp.value = entry.i;
      inp.checked = state.picked.indexOf(entry.i) !== -1;
      inp.disabled = state.checked;
      inp.addEventListener("change", function () {
        if (q.input === "radio") state.picked = [entry.i];
        else if (inp.checked) state.picked.push(entry.i);
        else state.picked = state.picked.filter(function (x) { return x !== entry.i; });
        checkBtn.disabled = state.picked.length === 0;
      });
      lab.appendChild(inp);
      lab.appendChild(el("span", null, entry.o.t));
      li.appendChild(lab);
      list.appendChild(li);
      entry._li = li; entry._input = inp;
    });
    wrap.appendChild(list);

    var feedbackHost = el("div");
    wrap.appendChild(feedbackHost);

    var nav = el("div", "sfq__nav");
    var left = el("div", "sfq__btns");
    var right = el("div", "sfq__btns");

    var checkBtn = el("button", "sfq__btn", "Check answer");
    checkBtn.type = "button";
    checkBtn.disabled = state.picked.length === 0;

    if (this.mode === "practice") {
      checkBtn.addEventListener("click", function () {
        if (state.checked) return;
        self.grade(state);
        state.options.forEach(function (entry) {
          entry._input.disabled = true;
          entry._li.firstChild.classList.add("is-locked");
          if (entry.o.c) entry._li.firstChild.classList.add("is-correct");
          else if (state.picked.indexOf(entry.i) !== -1) entry._li.firstChild.classList.add("is-wrong");
        });
        feedbackHost.appendChild(self.feedback(state));
        fill.style.width = ((self.idx + 1) / total * 100) + "%";
        checkBtn.disabled = true;
      });
      left.appendChild(checkBtn);
    }

    var prevBtn = el("button", "sfq__btn sfq__btn--ghost", "Previous");
    prevBtn.type = "button"; prevBtn.disabled = this.idx === 0;
    prevBtn.addEventListener("click", function () { self.idx--; self.renderQuestion(); });

    var isLast = this.idx === total - 1;
    var nextBtn = el("button", "sfq__btn", isLast ? (this.mode === "exam" ? "Submit exam" : "See results") : "Next");
    nextBtn.type = "button";
    nextBtn.addEventListener("click", function () {
      if (self.mode === "practice" && !state.checked && !isLast) {
        // encourage checking, but allow skipping
      }
      if (isLast) { self.results(); }
      else { self.idx++; self.renderQuestion(); }
    });

    right.appendChild(prevBtn); right.appendChild(nextBtn);
    nav.appendChild(left); nav.appendChild(right);
    wrap.appendChild(nav);

    var quit = el("p", "sfq__hint");
    var ql = el("a", null, "↩ Back to setup"); ql.href = "#"; ql.style.cursor = "pointer";
    ql.addEventListener("click", function (e) { e.preventDefault(); self.renderConfig(); });
    quit.appendChild(ql);
    wrap.appendChild(quit);

    // re-show feedback if returning to an already-checked practice question
    if (this.mode === "practice" && state.checked) {
      state.options.forEach(function (entry) {
        entry._input.disabled = true;
        entry._li.firstChild.classList.add("is-locked");
        if (entry.o.c) entry._li.firstChild.classList.add("is-correct");
        else if (state.picked.indexOf(entry.i) !== -1) entry._li.firstChild.classList.add("is-wrong");
      });
      feedbackHost.appendChild(this.feedback(state));
      checkBtn.disabled = true;
    }

    this.root.appendChild(wrap);
  };

  Player.prototype._tick = function (node) {
    var self = this;
    function upd() {
      var left = Math.round((self.deadline - Date.now()) / 1000);
      node.textContent = "⏱ " + fmtTime(left);
      if (left <= 60) node.classList.add("is-low");
      if (left <= 0) { clearInterval(self._timer); self._timer = null; self.results(); }
    }
    upd();
    this._timer = setInterval(upd, 1000);
  };

  Player.prototype.grade = function (state) {
    var correctIdx = state.q.a.map(function (o, i) { return o.c ? i : -1; })
      .filter(function (i) { return i >= 0; });
    state.correct = setsEqual(state.picked, correctIdx);
    state.checked = true;
    recordResult(state.q.area, state.correct); // grade() runs exactly once per question
    return state.correct;
  };

  Player.prototype.feedback = function (state) {
    var box = el("div", "sfq__feedback " + (state.correct ? "is-correct" : "is-wrong"));
    box.appendChild(el("span", "sfq__verdict " + (state.correct ? "is-correct" : "is-wrong"),
      state.correct ? "✓ Correct" : "✗ Not quite"));
    if (state.q.exp) box.appendChild(el("p", null, state.q.exp));
    if (state.q.doc) {
      var p = el("p", "sfq__muted");
      var a = el("a", null, "Official documentation ↗");
      a.href = state.q.doc; a.target = "_blank"; a.rel = "noopener";
      p.appendChild(a); box.appendChild(p);
    }
    return box;
  };

  // --- results ------------------------------------------------------------
  Player.prototype.results = function () {
    this.clear();
    var self = this;
    var qs = this.questions;
    qs.forEach(function (s) { if (!s.checked) self.grade(s); });
    var correct = qs.filter(function (s) { return s.correct; }).length;
    var pct = Math.round(correct / qs.length * 100);
    var passed = pct >= this.pass;

    var wrap = el("div", "sfq__panel");
    var score = el("div", "sfq__score");
    var big = el("b", passed ? "is-pass" : "is-fail", pct + "%");
    score.appendChild(big);
    score.appendChild(el("div", null, correct + " / " + qs.length + " correct · " +
      (passed ? "PASS" : "below pass mark") + " (need " + this.pass + "%)"));
    wrap.appendChild(score);

    // per-area breakdown
    var byArea = {};
    qs.forEach(function (s) {
      var a = s.q.area;
      byArea[a] = byArea[a] || { c: 0, n: 0 };
      byArea[a].n++; if (s.correct) byArea[a].c++;
    });
    var table = el("table", "sfq__breakdown");
    var thead = el("tr");
    ["Topic", "Score", "%"].forEach(function (h) { thead.appendChild(el("th", null, h)); });
    table.appendChild(thead);
    Object.keys(byArea).sort().forEach(function (a) {
      var r = byArea[a], tr = el("tr");
      tr.appendChild(el("td", null, a));
      tr.appendChild(el("td", null, r.c + " / " + r.n));
      tr.appendChild(el("td", null, Math.round(r.c / r.n * 100) + "%"));
      table.appendChild(tr);
    });
    wrap.appendChild(table);

    // review — wrong first
    var review = el("div", "sfq__review");
    review.appendChild(el("h3", null, "Review"));
    var ordered = qs.slice().sort(function (a, b) { return (a.correct ? 1 : 0) - (b.correct ? 1 : 0); });
    ordered.forEach(function (s) {
      var det = el("details");
      var sum = el("summary", null, (s.correct ? "✓ " : "✗ ") + s.q.q);
      det.appendChild(sum);
      var yours = s.picked.map(function (i) { return s.q.a[i].t; });
      var right = s.q.a.filter(function (o) { return o.c; }).map(function (o) { return o.t; });
      det.appendChild(el("p", null, "Your answer: " + (yours.length ? yours.join("; ") : "(none)")));
      var rp = el("p"); rp.appendChild(el("b", null, "Correct: "));
      rp.appendChild(document.createTextNode(right.join("; "))); det.appendChild(rp);
      if (s.q.exp) det.appendChild(el("p", "sfq__muted", s.q.exp));
      if (s.q.doc) {
        var p = el("p", "sfq__muted");
        var a = el("a", null, "Documentation ↗"); a.href = s.q.doc; a.target = "_blank"; a.rel = "noopener";
        p.appendChild(a); det.appendChild(p);
      }
      review.appendChild(det);
    });
    wrap.appendChild(review);

    var btns = el("div", "sfq__btns");
    var again = el("button", "sfq__btn", "New session");
    again.type = "button";
    again.addEventListener("click", function () { self.renderConfig(); });
    btns.appendChild(again);
    wrap.appendChild(btns);

    this.root.appendChild(wrap);
    if (this.root.scrollIntoView) this.root.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  // --- bootstrap (Material instant-navigation aware) ----------------------
  function init() {
    var root = document.getElementById("sf-quiz");
    if (!root || root.dataset.mounted === "1") return;
    root.dataset.mounted = "1";
    var src = root.getAttribute("data-src");
    root.appendChild(el("p", "sfq__muted", "Loading question bank…"));
    // On localized pages (/fr/...), the dataset lives one level up — retry there.
    function load(url, canRetry) {
      return fetch(url).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      }).catch(function (e) {
        if (canRetry) return load("../" + url, false);
        throw e;
      });
    }
    load(src, true).then(function (data) {
      root.innerHTML = "";
      root.className = "sfq";
      new Player(root, data);
    }).catch(function (e) {
      root.innerHTML = "";
      root.appendChild(el("p", null, "Could not load the question bank (" + e.message + "). Try reloading."));
    });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(function () {
      var root = document.getElementById("sf-quiz");
      if (root) root.dataset.mounted = "";
      init();
    });
  } else if (document.readyState !== "loading") {
    init();
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
