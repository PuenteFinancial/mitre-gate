// Mitre site script: mobile menu and the homepage photo carousel.
(function () {
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- mobile menu ----------
  var btn = document.getElementById("navMenu"), menu = document.getElementById("mobileMenu");
  if (btn && menu) {
    var setMenu = function (open) {
      menu.classList.toggle("open", open);
      btn.textContent = open ? "✕" : "≡";
      btn.setAttribute("aria-expanded", String(open));
      menu.setAttribute("aria-hidden", String(!open));
    };
    btn.addEventListener("click", function () { setMenu(!menu.classList.contains("open")); });
    menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      setMenu(false);
      // close the Industries dropdown too
      if (document.activeElement && document.activeElement.closest(".island__group")) document.activeElement.blur();
    });
  }

  // Placeholder links go nowhere until their pages exist
  document.querySelectorAll('a[data-placeholder="link"]').forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); });
  });

  // Contact form: validates on the page, then posts to a Google Apps Script that logs the lead to a Sheet and emails it
  document.querySelectorAll('form[data-lead-form]').forEach(function (f) {
    var status = f.querySelector(".form__status");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = null;
      f.querySelectorAll(".field__input").forEach(function (el) {
        var ok = el.checkValidity() && el.value.trim() !== "";
        el.setAttribute("aria-invalid", String(!ok));
        if (!ok && !bad) bad = el;
      });
      if (bad) { status.textContent = "Please fill in every field with a valid email."; bad.focus(); return; }
      var btn = f.querySelector('button[type="submit"]');
      var fail = "Sorry, that didn't send. Please email info@mitre.global instead.";
      var data = {};
      new FormData(f).forEach(function (v, k) { data[k] = v; });
      btn.disabled = true;
      status.textContent = "Sending…";
      // text/plain keeps this a "simple" request, so no CORS preflight (Apps Script can't answer one)
      fetch(f.dataset.leadForm, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json(); })
        .then(function (r) {
          if (r.ok) { f.reset(); status.textContent = "Thanks, we got it. We'll be in touch soon."; }
          else status.textContent = fail;
        })
        .catch(function () { status.textContent = fail; })
        .then(function () { btn.disabled = false; });
    });
    f.addEventListener("input", function (e) { if (e.target.getAttribute("aria-invalid") === "true" && e.target.checkValidity() && e.target.value.trim()) e.target.setAttribute("aria-invalid", "false"); });
  });

  // ---------- services phase stepper ----------
  // Without JS (and under 861px) every phase is stacked and visible. On wide screens this turns the
  // stack into ARIA tabs over one panel, with arrow keys and previous/next buttons.
  document.querySelectorAll("[data-phases]").forEach(function (root) {
    var list = root.querySelector('[role="tablist"]');
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    var nav = root.querySelector(".phases__nav");
    var prev = root.querySelector("[data-phase-prev]"), next = root.querySelector("[data-phase-next]");
    var wide = matchMedia("(min-width: 861px)");
    var active = 0;

    function select(i, focus) {
      active = (i + tabs.length) % tabs.length;
      tabs.forEach(function (t, k) {
        var on = k === active;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        panels[k].classList.toggle("is-active", on);
      });
      prev.disabled = active === 0;
      next.disabled = active === tabs.length - 1;
      if (focus) tabs[active].focus();
    }
    function setMode() {
      var on = wide.matches;
      root.classList.toggle("is-tabs", on);
      list.hidden = !on;
      nav.hidden = !on;
      panels.forEach(function (p, k) {
        if (on) {
          p.setAttribute("role", "tabpanel");
          p.setAttribute("aria-labelledby", tabs[k].id);
          p.tabIndex = 0;
        } else {
          p.removeAttribute("role");
          p.setAttribute("aria-labelledby", p.id + "-title");
          p.removeAttribute("tabindex");
        }
      });
      select(active, false);
    }

    tabs.forEach(function (t, k) { t.addEventListener("click", function () { select(k, false); }); });
    list.addEventListener("keydown", function (e) {
      var k = { ArrowRight: active + 1, ArrowLeft: active - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (k == null) return;
      e.preventDefault();
      select(k, true);
    });
    prev.addEventListener("click", function () { select(active - 1, false); });
    next.addEventListener("click", function () { select(active + 1, false); });
    if (wide.addEventListener) wide.addEventListener("change", setMode); else wide.addListener(setMode);
    setMode();
  });

  // ---------- careers: filter and sort open roles ----------
  // Roles are <li data-job data-team data-location data-type data-date data-title> inside [data-jobs].
  // With no roles posted, the count reads 0 and the empty banner stays visible.
  document.querySelectorAll("[data-jobfilter]").forEach(function (form) {
    var list = document.querySelector("[data-jobs]");
    var count = form.querySelector("[data-job-count]");
    var empty = form.parentNode.querySelector(".phero__ph");
    var emptyLabel = empty && empty.querySelector(".ph__label");
    var baseLabel = emptyLabel ? emptyLabel.textContent : "";
    function apply() {
      var jobs = [].slice.call(list.querySelectorAll("[data-job]"));
      var q = form.q.value.trim().toLowerCase();
      var shown = 0;
      jobs.forEach(function (li) {
        var ok = (!q || li.textContent.toLowerCase().indexOf(q) !== -1) &&
          ["team", "location", "type"].every(function (k) { return !form[k].value || li.dataset[k] === form[k].value; });
        li.hidden = !ok;
        if (ok) shown++;
      });
      jobs.sort(function (a, b) {
        return form.sort.value === "title"
          ? (a.dataset.title || "").localeCompare(b.dataset.title || "")
          : (b.dataset.date || "").localeCompare(a.dataset.date || "");
      }).forEach(function (li) { list.appendChild(li); });
      count.textContent = shown;
      var noun = form.querySelector("[data-job-noun]");
      if (noun) noun.textContent = shown === 1 ? "role" : "roles";
      if (empty) {
        empty.hidden = shown > 0;
        if (emptyLabel) emptyLabel.textContent = jobs.length && !shown ? "No roles match these filters." : baseLabel;
      }
    }
    form.addEventListener("input", apply);
    form.addEventListener("change", apply);
    form.addEventListener("reset", function () { setTimeout(apply, 0); });
    apply();
  });

  // ---------- services animations ----------
  // Each .anim plays its sequence (CSS in site.css) every time it comes into view, including when its
  // phase tab is shown again. Reduced motion keeps the finished frame.
  var anims = document.querySelectorAll(".anim");
  if (anims.length && !reduced && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.intersectionRatio >= 0.5) e.target.classList.add("is-play");
        else if (!e.isIntersecting) e.target.classList.remove("is-play");
      });
    }, { threshold: [0, 0.5] });
    anims.forEach(function (a) { a.classList.add("is-armed"); io.observe(a); });
  }

  // ---------- carousel ----------
  // Every slide sits at the stage's center and is shifted by its distance from the active one.
  // The active photo is full size; neighbors step down small, medium, then full again at the edges.
  var root = document.querySelector("[data-carousel]");
  if (!root) return;
  var stage = root.querySelector(".car__stage");
  var slides = [].slice.call(stage.querySelectorAll(".slide"));
  var n = slides.length, active = 0, prevOff = [], hovering = false, paused = reduced;
  var pauseBtn = root.querySelector("[data-car-pause]");
  var SCALE = [1, 0.6, 0.8, 1];

  function layout() {
    var w = stage.clientWidth, narrow = w < 720;
    var gap = narrow ? 10 : 6;
    var cell = narrow ? Math.min(w * 0.64, 340) : (w - 4 * gap) / 5;
    stage.style.setProperty("--cell", cell + "px");
    stage.style.height = Math.round(cell * 4 / 3) + "px";
    slides.forEach(function (s, i) {
      var off = ((i - active) % n + n) % n;
      if (off > n / 2) off -= n;
      // a slide wrapping from one end to the other jumps instead of sliding across
      s.style.transition = prevOff[i] != null && Math.abs(off - prevOff[i]) > 1 ? "none" : "";
      s.style.transform = "translateX(calc(-50% + " + off * (cell + gap) + "px))";
      var d = Math.abs(off);
      s.style.setProperty("--s", narrow ? (d === 0 ? 1 : 0.72) : (SCALE[d] || 1));
      s.style.zIndex = d === 0 ? 2 : 1;
      s.classList.toggle("is-active", d === 0);
      s.setAttribute("aria-hidden", String(d !== 0));
      s.querySelectorAll("a, button").forEach(function (el) { el.tabIndex = d === 0 ? 0 : -1; });
      prevOff[i] = off;
    });
  }
  function go(i) { active = (i + n) % n; layout(); }

  root.querySelector("[data-car-prev]").addEventListener("click", function () { go(active - 1); });
  root.querySelector("[data-car-next]").addEventListener("click", function () { go(active + 1); });
  function setPaused(p) {
    paused = p;
    pauseBtn.textContent = p ? "▶" : "❚❚";
    pauseBtn.setAttribute("aria-label", p ? "Play carousel" : "Pause carousel");
  }
  pauseBtn.addEventListener("click", function () { setPaused(!paused); });
  setPaused(paused);

  // clicking a side photo brings it to the center
  stage.addEventListener("click", function (e) {
    var s = e.target.closest(".slide");
    if (!s || s.classList.contains("is-active")) return;
    e.preventDefault();
    go(slides.indexOf(s));
  });
  stage.addEventListener("mouseenter", function () { hovering = true; });
  stage.addEventListener("mouseleave", function () { hovering = false; });
  root.addEventListener("focusin", function () { hovering = true; });
  root.addEventListener("focusout", function () { hovering = false; });

  // swipe on touch screens
  var startX = null;
  stage.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") startX = e.clientX; });
  stage.addEventListener("pointerup", function (e) {
    if (startX == null) return;
    var dx = e.clientX - startX; startX = null;
    if (Math.abs(dx) > 40) go(active + (dx < 0 ? 1 : -1));
  });

  setInterval(function () { if (!paused && !hovering && !document.hidden) go(active + 1); }, 5000);
  new ResizeObserver(layout).observe(stage);
  layout();
  // turn transitions on only after the first layout, so the slides don't fly in on load
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add("is-ready"); }); });
})();
