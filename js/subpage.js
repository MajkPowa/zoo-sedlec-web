/* ============ ZOO SEDLEC — shared subpage animations ============ */
gsap.registerPlugin(ScrollTrigger);

/* split text into per-word groups of letter spans */
function splitLetters(el) {
  const text = el.textContent;
  el.textContent = "";
  const chars = [];
  text.split(" ").forEach((word, wi, arr) => {
    const wordEl = document.createElement("span");
    wordEl.className = "word";
    for (const c of word) {
      const span = document.createElement("span");
      span.className = "ch";
      span.textContent = c;
      wordEl.appendChild(span);
      chars.push(span);
    }
    el.appendChild(wordEl);
    if (wi < arr.length - 1) el.appendChild(document.createTextNode(" "));
  });
  return chars;
}

function letterConverge(chars, opts = {}) {
  const center = (chars.length - 1) / 2;
  return gsap.from(chars, {
    x: (i) => (i - center) * (opts.spread || 26),
    opacity: 0,
    ease: "power3.out",
    duration: opts.duration || 1.1,
    stagger: { each: 0.012, from: "center" },
    ...opts.tween,
  });
}

/* header slides in */
gsap.from(".site-header", { y: -60, opacity: 0, duration: 0.9, ease: "power3.out" });

/* hero title + sub */
document.querySelectorAll(".sub-hero [data-letters]").forEach((el, i) => {
  letterConverge(splitLetters(el), { spread: 30, tween: { delay: 0.25 + i * 0.15 } });
});
gsap.from(".sub-hero .crumb, .sub-hero .section-sub", {
  y: 26, opacity: 0, duration: 0.8, stagger: 0.15, delay: 0.7, ease: "power2.out",
});
gsap.from(".sub-hero .sprite", {
  scale: 0, opacity: 0, transformOrigin: "50% 90%",
  ease: "back.out(1.8)", duration: 0.8, stagger: 0.12, delay: 0.4,
});

/* titles elsewhere converge on scroll */
document.querySelectorAll(".sub-content [data-letters], .site-footer [data-letters]").forEach((el) => {
  letterConverge(splitLetters(el), {
    spread: 22,
    tween: { scrollTrigger: { trigger: el, start: "top 84%" } },
  });
});

/* paper cards + stat cards + reveal blocks */
document.querySelectorAll(".sub-content .paper-card, .stat-card, [data-reveal]").forEach((card, i) => {
  gsap.from(card, {
    y: 70, opacity: 0, scale: 0.94,
    rotate: () => gsap.utils.random(-5, 5),
    transformOrigin: "50% 0%",
    ease: "back.out(1.3)", duration: 0.85,
    delay: (i % 3) * 0.08,
    scrollTrigger: { trigger: card, start: "top 86%" },
  });
});

/* subtitles fade */
document.querySelectorAll(".sub-content .section-sub, .note-band").forEach((el) => {
  gsap.from(el, {
    y: 22, opacity: 0, duration: 0.8, ease: "power2.out",
    scrollTrigger: { trigger: el, start: "top 88%" },
  });
});

/* sprites: gentle idle float */
document.querySelectorAll("[data-float]").forEach((el, i) => {
  gsap.to(el, {
    y: "+=" + (10 + (i % 3) * 6),
    yoyo: true, repeat: -1,
    duration: 2.4 + (i % 4) * 0.6,
    ease: "sine.inOut",
  });
});

/* sprites: drift sideways with scroll */
document.querySelectorAll("[data-drift]").forEach((el) => {
  const dx = parseFloat(el.dataset.drift || "120");
  gsap.to(el, {
    x: dx, ease: "none",
    scrollTrigger: { trigger: el.closest("section") || el, start: "top bottom", end: "bottom top", scrub: 1 },
  });
});

/* bubbles for sections marked data-bubbles */
document.querySelectorAll("[data-bubbles]").forEach((sec) => {
  const count = parseInt(sec.dataset.bubbles || "14", 10);
  for (let i = 0; i < count; i++) {
    const b = document.createElement("span");
    b.className = "bubble";
    const size = 6 + Math.random() * 16;
    b.style.width = b.style.height = size + "px";
    b.style.left = 4 + Math.random() * 92 + "%";
    b.style.top = 30 + Math.random() * 65 + "%";
    b.style.animationDuration = 7 + Math.random() * 9 + "s";
    b.style.animationDelay = -Math.random() * 12 + "s";
    sec.appendChild(b);
  }
});

/* fireflies pulse via CSS (.ff) — nothing to do here */

/* footer reveal */
gsap.from(".footer-grid > *", {
  y: 40, opacity: 0, duration: 0.7, stagger: 0.1, ease: "power2.out",
  scrollTrigger: { trigger: ".site-footer", start: "top 88%" },
});
