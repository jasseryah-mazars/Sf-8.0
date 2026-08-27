// Small, focused accessibility fix (P2-03, verified with axe-core).
//
// pymdownx.tasklist (custom_checkbox: true) renders every "- [ ] ..." list
// item as <li><label class="task-list-control"><input type="checkbox"
// disabled/><span class="task-list-indicator"></span></label> text...</li>.
// The <label> wraps only the checkbox and a decorative icon span — it has
// no text content of its own — so axe-core's "label" rule correctly flags
// every one of these as an input with no accessible name.
//
// These checkboxes are always `disabled` and never meant to be toggled by
// a reader — they're a decorative bullet style for read-only checklists
// ("Learning objectives", exercise steps), not real form controls. The
// correct fix per WCAG (and what axe's own failure summary suggests) is
// to remove them from the accessibility tree entirely with aria-hidden,
// rather than inventing a label for a control nobody is meant to operate.
(function () {
  "use strict";
  function hideDecorativeTaskCheckboxes() {
    document
      .querySelectorAll(".task-list-control input[type=checkbox][disabled]")
      .forEach(function (el) {
        el.setAttribute("aria-hidden", "true");
      });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    // mkdocs-material's instant-navigation observable — re-run on every
    // page swap, same pattern quiz.js uses.
    window.document$.subscribe(hideDecorativeTaskCheckboxes);
  } else if (document.readyState !== "loading") {
    hideDecorativeTaskCheckboxes();
  } else {
    document.addEventListener("DOMContentLoaded", hideDecorativeTaskCheckboxes);
  }
})();
