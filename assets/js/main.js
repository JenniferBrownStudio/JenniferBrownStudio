/* Jennifer Brown — site interactions: nav, hero carousel, lightbox, reveal */
(function () {
  "use strict";

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("primary-menu");
  var backdrop = document.querySelector(".nav-backdrop");

  function closeMenu() {
    if (!menu) return;
    menu.classList.remove("is-open");
    if (backdrop) backdrop.classList.remove("is-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      if (backdrop) backdrop.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    if (backdrop) backdrop.addEventListener("click", closeMenu);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* Accordion submenus on mobile */
  document.querySelectorAll(".menu > li.has-sub > a").forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (window.innerWidth <= 820) {
        e.preventDefault();
        link.parentElement.classList.toggle("is-expanded");
      }
    });
  });

  /* ---------- Hero carousel ---------- */
  var hero = document.querySelector(".hero__slides");
  if (hero) {
    var slides = Array.prototype.slice.call(hero.querySelectorAll(".hero__slide"));
    var dotWrap = document.querySelector(".hero__dots");
    var i = 0, timer = null;

    slides.forEach(function (s, idx) {
      var b = document.createElement("button");
      b.setAttribute("aria-label", "Go to slide " + (idx + 1));
      b.addEventListener("click", function () { go(idx); restart(); });
      dotWrap.appendChild(b);
    });
    var dots = Array.prototype.slice.call(dotWrap.children);

    function go(n) {
      slides[i].classList.remove("is-active");
      dots[i].classList.remove("is-active");
      i = (n + slides.length) % slides.length;
      slides[i].classList.add("is-active");
      dots[i].classList.add("is-active");
    }
    function next() { go(i + 1); }
    function restart() { clearInterval(timer); timer = setInterval(next, 5500); }

    go(0); restart();
    hero.addEventListener("mouseenter", function () { clearInterval(timer); });
    hero.addEventListener("mouseleave", restart);
  }

  /* ---------- Lightbox gallery ---------- */
  var galleryLinks = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
  if (galleryLinks.length) {
    var box = document.createElement("div");
    box.className = "lightbox";
    box.innerHTML =
      '<button class="lightbox__btn lightbox__close" aria-label="Close">&times;</button>' +
      '<button class="lightbox__btn lightbox__prev" aria-label="Previous">&#8249;</button>' +
      '<img alt="">' +
      '<button class="lightbox__btn lightbox__next" aria-label="Next">&#8250;</button>' +
      '<div class="lightbox__cap"></div>';
    document.body.appendChild(box);

    var lbImg = box.querySelector("img");
    var lbCap = box.querySelector(".lightbox__cap");
    var current = 0;

    function show(n) {
      current = (n + galleryLinks.length) % galleryLinks.length;
      var link = galleryLinks[current];
      lbImg.src = link.getAttribute("href");
      lbCap.textContent = link.getAttribute("data-caption") || "";
    }
    function open(n) { show(n); box.classList.add("is-open"); document.body.style.overflow = "hidden"; }
    function close() { box.classList.remove("is-open"); document.body.style.overflow = ""; lbImg.src = ""; }

    galleryLinks.forEach(function (link, idx) {
      link.addEventListener("click", function (e) { e.preventDefault(); open(idx); });
    });
    box.querySelector(".lightbox__close").addEventListener("click", close);
    box.querySelector(".lightbox__next").addEventListener("click", function () { show(current + 1); });
    box.querySelector(".lightbox__prev").addEventListener("click", function () { show(current - 1); });
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    document.addEventListener("keydown", function (e) {
      if (!box.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") show(current + 1);
      if (e.key === "ArrowLeft") show(current - 1);
    });
  }

  /* ---------- Reveal on scroll (progressive enhancement) ---------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  function revealAll() { reveals.forEach(function (el) { el.classList.add("is-visible"); }); }
  if (reveals.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -5% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
    // Safety net: never leave content hidden if the observer doesn't fire.
    window.addEventListener("load", function () { setTimeout(revealAll, 1400); });
  } else {
    revealAll();
  }

  /* ---------- Contact form (no backend: mailto fallback) ---------- */
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = document.getElementById("form-status");
      var name = encodeURIComponent(form.name.value || "");
      var email = encodeURIComponent(form.email.value || "");
      var subject = encodeURIComponent(form.subject.value || "Website inquiry");
      var message = encodeURIComponent(form.message.value || "");
      var body = "Name: " + name + "%0D%0AEmail: " + email + "%0D%0A%0D%0A" + message;
      window.location.href = "mailto:JenniferBrownStudio@gmail.com?subject=" + subject + "&body=" + body;
      if (status) status.textContent = "Opening your email app… if nothing happens, email JenniferBrownStudio@gmail.com directly.";
    });
  }

  /* ---------- Footer year ---------- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
