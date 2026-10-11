(function () {
  "use strict";
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- WhatsApp: un solo número para todos los botones ---------- */
  var WA_NUMBER = "5491158465239";
  document.querySelectorAll(".js-wa").forEach(function (a) {
    var msg = a.getAttribute("data-msg") || "Hola, quisiera hacer una consulta.";
    a.href = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg);
    a.target = "_blank";
    a.rel = "noopener";
  });

  /* ---------- boceto: páginas internas todavía no construidas ---------- */
  document.querySelectorAll("[data-soon]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); });
  });

  /* ---------- header ---------- */
  var hdr = document.getElementById("hdr");
  function onScroll() { hdr.classList.toggle("sc", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- menú mobile (la hamburguesa se transforma en cruz) ---------- */
  var burger = document.getElementById("burger");
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  }
  burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  document.getElementById("mnavOv").addEventListener("click", function () { setNav(false); });
  document.querySelectorAll(".mnav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });

  /* ---------- título del hero: entra palabra por palabra (conserva el <em>) ---------- */
  var wordIdx = 0;
  function splitWords(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          var w = document.createElement("span");
          w.className = "w";
          w.textContent = part;
          w.style.animationDelay = (0.15 + wordIdx++ * 0.08) + "s";
          frag.appendChild(w);
        });
        node.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== "BR") {
        splitWords(n);
      }
    });
  }
  if (!reduce) document.querySelectorAll(".split-words").forEach(splitWords);

  /* ---------- contadores: suben hasta el número fijo ---------- */
  function runCount(el) {
    var to = parseFloat(el.getAttribute("data-to")), pre = el.getAttribute("data-prefix") || "";
    var dur = 1800, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - k, 4);
      el.textContent = pre + Math.round(to * e);
      if (k < 1) requestAnimationFrame(step);
    }
    el.textContent = pre + "0";
    requestAnimationFrame(step);
  }
  var counts = document.querySelectorAll(".count");
  if (!reduce && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counts.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- preguntas: acordeón con apertura suave (una abierta a la vez) ---------- */
  var faqs = document.querySelectorAll(".faq-list details");
  function closeFaq(d) {
    var a = d.querySelector(".faq-a");
    if (reduce) { d.open = false; return; }
    a.style.height = a.scrollHeight + "px";
    requestAnimationFrame(function () { a.style.transition = "height .45s cubic-bezier(.2,.7,.2,1)"; a.style.height = "0px"; });
    a.addEventListener("transitionend", function te() { a.removeEventListener("transitionend", te); d.open = false; a.style.cssText = ""; });
  }
  faqs.forEach(function (d) {
    d.querySelector("summary").addEventListener("click", function (e) {
      e.preventDefault();
      if (d.open) { closeFaq(d); return; }
      d.closest(".faq-list").querySelectorAll("details").forEach(function (o) { if (o !== d && o.open) closeFaq(o); });
      d.open = true;
      if (reduce) return;
      var a = d.querySelector(".faq-a"), h = a.scrollHeight;
      a.style.height = "0px";
      requestAnimationFrame(function () { a.style.transition = "height .45s cubic-bezier(.2,.7,.2,1)"; a.style.height = h + "px"; });
      a.addEventListener("transitionend", function te() { a.removeEventListener("transitionend", te); a.style.cssText = ""; });
    });
  });

  /* ---------- preguntas frecuentes: índice lateral activo ---------- */
  var sideLinks = document.querySelectorAll(".faqp-side a");
  if (sideLinks.length && "IntersectionObserver" in window) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        sideLinks.forEach(function (a) { a.classList.toggle("act", a.getAttribute("href") === "#" + en.target.id); });
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    document.querySelectorAll(".faq-grp").forEach(function (g) { sio.observe(g); });
  }

  /* ---------- reveals ---------- */
  var items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- parallax del hero + el eje del método que se dibuja con el scroll ---------- */
  var heroBg = document.querySelector(".hero-bg, .ph-bg"), eje = document.getElementById("eje");
  var ejeItems = eje ? eje.querySelectorAll("li") : [];
  var ticking = false;
  function onMotion() {
    ticking = false;
    var vh = window.innerHeight;
    if (heroBg && window.scrollY < vh * 1.2) heroBg.style.transform = "translate3d(0," + (window.scrollY * 0.25) + "px,0)";
    if (eje) {
      var r = eje.getBoundingClientRect(), mark = vh * 0.65;
      var p = Math.max(0, Math.min(1, (mark - r.top) / r.height));
      eje.style.setProperty("--p", p.toFixed(3));
      ejeItems.forEach(function (li) {
        var n = li.querySelector(".eje-n"), nr = (n || li).getBoundingClientRect();
        li.classList.toggle("on", nr.top + nr.height / 2 < mark);
      });
    }
  }
  if (reduce) {
    if (eje) { eje.style.setProperty("--p", "1"); ejeItems.forEach(function (li) { li.classList.add("on"); }); }
  } else {
    onMotion();
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onMotion); } }, { passive: true });
    window.addEventListener("resize", onMotion);
  }

  /* ---------- WhatsApp flotante: se oculta en la cabecera, el contacto y el footer ---------- */
  var fab = document.getElementById("waFloat");
  if ("IntersectionObserver" in window) {
    var hidden = new Set();
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) hidden.add(en.target); else hidden.delete(en.target); });
      fab.classList.toggle("hide", hidden.size > 0);
    });
    document.querySelectorAll(".hero, .ph, .nf, #contacto, .cta-band, #ftr").forEach(function (el) { fio.observe(el); });
  }

  /* ---------- formulario (FormSubmit + modal) ---------- */
  var form = document.getElementById("contactForm"), btn = document.getElementById("formSubmitBtn");
  var iframe = document.getElementById("formsubmit-iframe"), modal = document.getElementById("okModal"), sending = false;
  if (form) {
    var valid = function (input) {
      var v = input.value.trim();
      var ok = v !== "" && (input.type !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
      input.closest(".field").classList.toggle("err", !ok);
      return ok;
    };
    form.addEventListener("submit", function (e) {
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (i) { if (!valid(i)) ok = false; });
      if (!ok) { e.preventDefault(); var f = form.querySelector(".field.err input,.field.err select,.field.err textarea"); if (f) f.focus(); return; }
      sending = true; btn.disabled = true; btn.textContent = "Enviando...";
    });
    form.querySelectorAll("[required]").forEach(function (i) {
      i.addEventListener("input", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
      i.addEventListener("change", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
    });
    iframe.addEventListener("load", function () {
      if (!sending) return;
      sending = false; form.reset(); btn.disabled = false; btn.textContent = "Enviar consulta";
      modal.classList.add("show");
    });
    modal.addEventListener("click", function (e) { if (e.target === modal || e.target.hasAttribute("data-close")) modal.classList.remove("show"); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setNav(false); if (modal) modal.classList.remove("show"); }
  });

  document.getElementById("yr").textContent = new Date().getFullYear();
})();
