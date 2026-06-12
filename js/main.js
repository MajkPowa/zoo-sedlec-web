/* ============ ORELY ZOO — animations ============ */
gsap.registerPlugin(ScrollTrigger);

/* ---------- helpers ---------- */

// split element text into letter spans, grouped per word so wrapping
// only ever happens between words
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

// the signature reveal: letters start spread wide & faded, converge into place
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

document.querySelectorAll("[data-letters]").forEach((el) => {
  el._chars = splitLetters(el);
});
// multi-line variant (CTA title)
document.querySelectorAll("[data-letters-lines]").forEach((el) => {
  const lines = el.textContent.split("\n").map((s) => s.trim());
  el.textContent = "";
  el._lineChars = lines.map((line) => {
    const lineEl = document.createElement("span");
    lineEl.style.display = "block";
    lineEl.textContent = line;
    el.appendChild(lineEl);
    return splitLetters(lineEl);
  });
});

/* ---------- hero intro ---------- */

const intro = gsap.timeline({ defaults: { ease: "power3.out" } });

intro
  .from(".site-header", { y: -60, opacity: 0, duration: 0.9 })
  .from(
    ".sec-hero .animal",
    {
      scale: 0,
      opacity: 0,
      transformOrigin: "50% 90%",
      ease: "back.out(1.8)",
      duration: 0.8,
      stagger: 0.09,
    },
    0.25
  );

document.querySelectorAll(".hero-title .line").forEach((line, i) => {
  intro.add(letterConverge(line._chars, { spread: 34, duration: 1.2 }), 0.45 + i * 0.18);
});

intro
  .from(".hero-sub", { y: 26, opacity: 0, duration: 0.8 }, 1.25)
  .from(".search-bar", { y: 44, opacity: 0, duration: 0.9 }, 1.4);

/* ---------- section titles (scroll) ---------- */

document.querySelectorAll(".big-title [data-letters], .big-title[data-letters]").forEach((el) => {
  letterConverge(el._chars, {
    spread: 30,
    tween: {
      scrollTrigger: { trigger: el, start: "top 82%" },
    },
  });
});
document.querySelectorAll("[data-letters-lines]").forEach((el) => {
  el._lineChars.forEach((chars, i) => {
    letterConverge(chars, {
      spread: 26,
      tween: {
        scrollTrigger: { trigger: el, start: "top 80%" },
        delay: i * 0.15,
      },
    });
  });
});

// card titles converge too
document.querySelectorAll(".card-title").forEach((el) => {
  letterConverge(el._chars, {
    spread: 18,
    tween: { scrollTrigger: { trigger: el.closest(".paper-card"), start: "top 75%" } },
  });
});

/* ---------- paper cards unfold ---------- */

document.querySelectorAll("[data-card]").forEach((card) => {
  const tl = gsap.timeline({
    scrollTrigger: { trigger: card, start: "top 80%" },
  });
  tl.from(card, {
    scale: 0.6,
    y: 70,
    rotate: () => gsap.utils.random(-9, 9),
    opacity: 0,
    transformOrigin: "50% 0%",
    ease: "back.out(1.4)",
    duration: 0.9,
  }).from(
    card.querySelectorAll(".card-kicker, .card-text"),
    { y: 22, opacity: 0, duration: 0.6, stagger: 0.12, ease: "power2.out" },
    "-=0.35"
  );
});

/* ---------- subtitle fades ---------- */

document.querySelectorAll(".section-sub").forEach((el) => {
  gsap.from(el, {
    y: 24,
    opacity: 0,
    duration: 0.8,
    ease: "power2.out",
    scrollTrigger: { trigger: el, start: "top 85%" },
  });
});

/* ---------- forest zone parallax + animals ---------- */

gsap.to(".hero-content", {
  y: -120,
  opacity: 0.15,
  ease: "none",
  scrollTrigger: { trigger: ".sec-hero", start: "top top", end: "bottom top", scrub: true },
});

// sloth gently swings forever
gsap.to(".a-sloth", {
  rotation: 2.4,
  transformOrigin: "50% 12%",
  yoyo: true,
  repeat: -1,
  duration: 2.6,
  ease: "sine.inOut",
});

// deer walks in from the left
gsap.from(".a-deer", {
  x: -180,
  opacity: 0,
  duration: 1.2,
  ease: "power2.out",
  scrollTrigger: { trigger: ".a-deer", start: "top 88%" },
});
// croc drifts in
gsap.from(".a-croc", {
  x: 140,
  opacity: 0,
  duration: 1.3,
  ease: "power2.out",
  scrollTrigger: { trigger: ".a-croc", start: "top 92%" },
});
gsap.to(".a-croc", {
  x: -26,
  yoyo: true,
  repeat: -1,
  duration: 4,
  ease: "sine.inOut",
  delay: 1.4,
});
// snake slithers down the trunk as you scroll
gsap.to(".a-snake", {
  y: 150,
  ease: "none",
  scrollTrigger: { trigger: ".sec-sanctuary", start: "top bottom", end: "center center", scrub: true },
});

// hero animals tiny parallax on scroll
gsap.to(".sec-hero .animal", {
  y: (i) => 40 + i * 14,
  ease: "none",
  scrollTrigger: { trigger: ".sec-hero", start: "top top", end: "bottom top", scrub: true },
});

/* ---------- protect section ---------- */

gsap.from(".a-flam1, .a-flam2", {
  y: 60,
  opacity: 0,
  duration: 1,
  stagger: 0.2,
  ease: "power2.out",
  scrollTrigger: { trigger: ".a-flam1", start: "top 85%" },
});
// feeding flamingo bobs its head (whole sprite dip)
gsap.to(".a-flam2", {
  y: 10,
  yoyo: true,
  repeat: -1,
  duration: 1.8,
  ease: "sine.inOut",
  delay: 1.5,
});
gsap.from(".a-tiger", {
  y: 90,
  opacity: 0,
  duration: 1,
  ease: "power2.out",
  scrollTrigger: { trigger: ".a-tiger", start: "top 88%" },
});
// turtle trudges in
gsap.from(".a-turtle", {
  x: -160,
  opacity: 0,
  duration: 1.4,
  ease: "power2.out",
  scrollTrigger: { trigger: ".a-turtle", start: "top 92%" },
});
gsap.from(".a-frog", {
  scale: 0,
  transformOrigin: "50% 100%",
  ease: "back.out(2)",
  duration: 0.7,
  scrollTrigger: { trigger: ".sec-protect", start: "top 60%" },
});

/* ---------- savanna ---------- */

gsap.from(".a-lion", {
  y: 70,
  opacity: 0,
  duration: 1.1,
  ease: "power2.out",
  scrollTrigger: { trigger: ".a-lion", start: "top 85%" },
});
// lion tail flick
gsap.to(".a-lion", {
  rotation: 0.6,
  transformOrigin: "70% 80%",
  yoyo: true,
  repeat: -1,
  duration: 3.2,
  ease: "sine.inOut",
});
gsap.from(".a-stag", {
  x: 160,
  opacity: 0,
  duration: 1.2,
  ease: "power2.out",
  scrollTrigger: { trigger: ".stag-scene", start: "top 88%" },
});
// stag sips: gentle rock
gsap.to(".a-stag", {
  rotation: 1.6,
  transformOrigin: "80% 60%",
  yoyo: true,
  repeat: -1,
  duration: 2.4,
  ease: "sine.inOut",
  delay: 1.4,
});
// butterfly flutters around the lion
gsap.to(".a-butterfly", {
  keyframes: [
    { x: 60, y: -34, rotation: 8, duration: 2.2 },
    { x: 130, y: 10, rotation: -6, duration: 2.4 },
    { x: 50, y: 44, rotation: 6, duration: 2.2 },
    { x: 0, y: 0, rotation: 0, duration: 2.4 },
  ],
  repeat: -1,
  ease: "sine.inOut",
});

/* ---------- pricing tickets ---------- */

gsap.from("[data-ticket]", {
  y: 110,
  opacity: 0,
  rotationX: -38,
  transformOrigin: "50% 0%",
  duration: 0.95,
  stagger: 0.22,
  ease: "back.out(1.3)",
  scrollTrigger: { trigger: ".ticket-row", start: "top 78%" },
});

// the sea rises as you scroll towards the underwater world
gsap.fromTo(
  ".sea-edge",
  { yPercent: 36 },
  {
    yPercent: -6,
    ease: "none",
    scrollTrigger: { trigger: ".sec-pricing", start: "top 60%", end: "bottom 70%", scrub: true },
  }
);
// foam keeps lapping
gsap.to(".sea-foam", {
  x: -38,
  yoyo: true,
  repeat: -1,
  duration: 3.4,
  ease: "sine.inOut",
});

/* ---------- things to do / whale shark ---------- */

gsap.fromTo(
  ".a-whaleshark",
  { x: () => -window.innerWidth * 0.55, y: 60 },
  {
    x: () => window.innerWidth * 0.16,
    y: -30,
    ease: "none",
    scrollTrigger: { trigger: ".sec-things", start: "top 80%", end: "bottom 30%", scrub: 0.6 },
  }
);
gsap.to(".a-whaleshark", {
  rotation: 1.6,
  yoyo: true,
  repeat: -1,
  duration: 3.6,
  ease: "sine.inOut",
});

gsap.from("[data-todo]", {
  x: 130,
  opacity: 0,
  duration: 0.85,
  stagger: 0.2,
  ease: "power3.out",
  scrollTrigger: { trigger: ".todo-list", start: "top 75%" },
});

/* ---------- testimonials ---------- */

// sea turtle swims across with the scroll
gsap.fromTo(
  ".a-seaturtle",
  { x: 220, y: -60, rotation: 6 },
  {
    x: -160,
    y: 90,
    rotation: -4,
    ease: "none",
    scrollTrigger: { trigger: ".sec-love", start: "top 90%", end: "center 20%", scrub: 0.7 },
  }
);

gsap.from("[data-review]", {
  y: 90,
  opacity: 0,
  scale: 0.92,
  duration: 0.8,
  stagger: 0.14,
  ease: "back.out(1.2)",
  scrollTrigger: { trigger: ".review-grid", start: "top 78%" },
});

// jellyfish bob
document.querySelectorAll(".a-jelly").forEach((j, i) => {
  gsap.to(j, {
    y: -34,
    x: i % 2 ? 18 : -14,
    yoyo: true,
    repeat: -1,
    duration: 3 + i,
    ease: "sine.inOut",
  });
});
// moorish idol cruises
gsap.to(".a-moorish", {
  x: -90,
  y: -20,
  yoyo: true,
  repeat: -1,
  duration: 5,
  ease: "sine.inOut",
});

/* ---------- deep section fish drift with scroll ---------- */

[
  [".a-bluetang", -150, 40],
  [".a-lionfish", 120, -30],
  [".a-spotfish", -110, 30],
  [".a-wrasse", 140, -40],
].forEach(([sel, dx, dy]) => {
  gsap.to(sel, {
    x: dx,
    y: dy,
    ease: "none",
    scrollTrigger: { trigger: ".sec-deep", start: "top bottom", end: "bottom top", scrub: 1 },
  });
});
// idle wiggle
document.querySelectorAll(".a-bluetang, .a-lionfish, .a-spotfish, .a-wrasse, .a-reeffish, .a-smallfish").forEach((f, i) => {
  gsap.to(f, {
    y: "+=" + (8 + (i % 3) * 5),
    yoyo: true,
    repeat: -1,
    duration: 2 + (i % 4) * 0.5,
    ease: "sine.inOut",
  });
});

gsap.from(".ghost-btn", {
  y: 24,
  opacity: 0,
  duration: 0.7,
  ease: "power2.out",
  scrollTrigger: { trigger: ".cta-block", start: "top 70%" },
});
gsap.from(".footer-grid > *", {
  y: 40,
  opacity: 0,
  duration: 0.7,
  stagger: 0.1,
  ease: "power2.out",
  scrollTrigger: { trigger: ".site-footer", start: "top 85%" },
});

/* ---------- bubbles ---------- */

function spawnBubbles(sectionSel, count) {
  const sec = document.querySelector(sectionSel);
  if (!sec) return;
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
}
spawnBubbles(".sec-things", 16);
spawnBubbles(".sec-love", 16);
spawnBubbles(".sec-deep", 12);

/* ---------- nav active state ---------- */

const navLinks = document.querySelectorAll(".main-nav a");
navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.forEach((l) => l.classList.remove("active"));
    link.classList.add("active");
  });
});
