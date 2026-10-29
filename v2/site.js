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

  // Contact form: validates on the page but sends nothing until a backend is hooked up
  document.querySelectorAll('form[data-placeholder="form"]').forEach(function (f) {
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
      status.textContent = "This form isn't connected yet. Please email info@mitregate.com for now.";
    });
    f.addEventListener("input", function (e) { if (e.target.getAttribute("aria-invalid") === "true" && e.target.checkValidity() && e.target.value.trim()) e.target.setAttribute("aria-invalid", "false"); });
  });

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
