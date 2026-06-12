/* ============ ZOO SEDLEC — demo checkout logic ============ */

const PRICES = { adult: 120, child: 60, baby: 0, tour: 500 };
const LABELS = {
  adult: "Dospělý",
  child: "Dítě 3–17 let",
  baby: "Dítě do 2 let",
  tour: "Komentovaná prohlídka",
};

const state = {
  step: 1,
  date: "",
  counts: { adult: 0, child: 0, baby: 0, tour: 0 },
  contact: { name: "", email: "", phone: "" },
  payMethod: "card",
};

const $ = (sel) => document.querySelector(sel);

/* the generic subpage scroll-reveals must not own the wizard cards —
   hidden steps would be stuck at opacity 0 when unhidden later */
if (window.gsap) {
  if (window.ScrollTrigger) {
    ScrollTrigger.getAll().forEach((st) => {
      const t = st.trigger;
      if (t && (t.closest && (t.closest(".co-main") || t.closest(".co-summary")) || t.classList && t.classList.contains("co-summary"))) {
        st.kill();
      }
    });
  }
  gsap.killTweensOf(".co-step, .co-summary");
  gsap.set(".co-step, .co-summary", { clearProps: "all" });
}
const fmt = (n) => n.toLocaleString("cs-CZ") + " Kč";
const total = () =>
  Object.entries(state.counts).reduce((sum, [k, n]) => sum + PRICES[k] * n, 0);

/* ---------- date ---------- */
const dateInput = $("#visitDate");
const today = new Date();
const iso = (d) => d.toISOString().slice(0, 10);
dateInput.min = iso(today);
const defaultDate = new Date(today);
defaultDate.setDate(defaultDate.getDate() + 1);
dateInput.value = iso(defaultDate);
state.date = dateInput.value;
dateInput.addEventListener("change", () => {
  state.date = dateInput.value;
  renderSummary();
});

const czDate = (isoStr) => {
  if (!isoStr) return "";
  const [y, m, d] = isoStr.split("-");
  return `${+d}. ${+m}. ${y}`;
};

/* ---------- counters ---------- */
document.querySelectorAll(".counter").forEach((c) => {
  const type = c.dataset.type;
  const out = c.querySelector("output");
  const minus = c.querySelector(".minus");
  const plus = c.querySelector(".plus");
  const max = type === "tour" ? 2 : 10;
  const update = () => {
    out.textContent = state.counts[type];
    minus.disabled = state.counts[type] === 0;
    plus.disabled = state.counts[type] >= max;
    renderSummary();
  };
  minus.addEventListener("click", () => { state.counts[type] = Math.max(0, state.counts[type] - 1); update(); });
  plus.addEventListener("click", () => { state.counts[type] = Math.min(max, state.counts[type] + 1); update(); });
  update();
});

/* ---------- summary ---------- */
function renderSummary() {
  $("#sumDate").textContent = state.date
    ? `Návštěva ${czDate(state.date)} · 9:00–18:00`
    : "Vyberte datum návštěvy";
  const lines = Object.entries(state.counts)
    .filter(([, n]) => n > 0)
    .map(([k, n]) =>
      `<div class="sum-line"><span>${n}× ${LABELS[k]}</span><span>${fmt(PRICES[k] * n)}</span></div>`
    );
  $("#sumLines").innerHTML = lines.length
    ? lines.join("")
    : '<div class="sum-line"><span>Zatím nic vybráno</span><span></span></div>';
  $("#sumTotal").textContent = fmt(total());
  $("#btnNext").textContent =
    state.step === 3
      ? (state.payMethod === "onsite" ? "Dokončit rezervaci" : `Zaplatit ${fmt(total())}`)
      : "Pokračovat";
}

/* ---------- step navigation ---------- */
function showError(id, msg) {
  const el = $(id);
  el.textContent = msg;
  el.classList.add("show");
}
function clearErrors() {
  document.querySelectorAll(".form-error").forEach((e) => e.classList.remove("show"));
  document.querySelectorAll(".field input").forEach((i) => i.classList.remove("invalid"));
}

function goTo(step) {
  clearErrors();
  state.step = step;
  for (let i = 1; i <= 4; i++) $("#step" + i).hidden = i !== step;
  document.querySelectorAll("#steps li").forEach((li, i) => {
    li.classList.toggle("active", i + 1 === step);
    li.classList.toggle("done", i + 1 < step);
  });
  $("#summaryCard").style.display = step === 4 ? "none" : "";
  renderSummary();
  if (window.gsap) {
    gsap.from("#step" + step, { y: 26, opacity: 0, duration: 0.5, ease: "power2.out" });
  }
  window.scrollTo({ top: $("#steps").getBoundingClientRect().top + scrollY - 90, behavior: "smooth" });
}

function validateStep1() {
  const persons = state.counts.adult + state.counts.child + state.counts.baby;
  if (!state.date) return "Vyberte prosím datum návštěvy.";
  if (state.date < dateInput.min) return "Datum návštěvy nemůže být v minulosti.";
  if (persons === 0) return "Přidejte alespoň jednoho návštěvníka.";
  if (state.counts.adult === 0 && (state.counts.child > 0 || state.counts.baby > 0))
    return "Děti mohou do zoo pouze v doprovodu dospělé osoby — přidejte alespoň jednoho dospělého.";
  return null;
}

function validateStep2() {
  const name = $("#fullName").value.trim();
  const email = $("#email").value.trim();
  state.contact = { name, email, phone: $("#phone").value.trim() };
  if (name.split(" ").filter(Boolean).length < 2) {
    $("#fullName").classList.add("invalid");
    return "Vyplňte prosím celé jméno a příjmení.";
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    $("#email").classList.add("invalid");
    return "Vyplňte prosím platný e-mail.";
  }
  return null;
}

function validateCard() {
  const num = $("#ccNum").value.replace(/\s+/g, "");
  const exp = $("#ccExp").value.trim();
  const cvc = $("#ccCvc").value.trim();
  if (!/^\d{16}$/.test(num)) { $("#ccNum").classList.add("invalid"); return "Číslo karty musí mít 16 číslic."; }
  const m = exp.match(/^(\d{2})\/(\d{2})$/);
  if (!m || +m[1] < 1 || +m[1] > 12) { $("#ccExp").classList.add("invalid"); return "Platnost zadejte ve formátu MM/RR."; }
  const expDate = new Date(2000 + +m[2], +m[1], 0);
  if (expDate < new Date()) { $("#ccExp").classList.add("invalid"); return "Karta má prošlou platnost."; }
  if (!/^\d{3,4}$/.test(cvc)) { $("#ccCvc").classList.add("invalid"); return "CVC má 3–4 číslice."; }
  return null;
}

$("#btnNext").addEventListener("click", () => {
  clearErrors();
  if (state.step === 1) {
    const err = validateStep1();
    if (err) return showError("#err1", err);
    goTo(2);
  } else if (state.step === 2) {
    const err = validateStep2();
    if (err) return showError("#err2", err);
    renderPayQR();
    goTo(3);
  } else if (state.step === 3) {
    if (state.payMethod === "card") {
      const err = validateCard();
      if (err) return showError("#err3", err);
    }
    pay();
  }
});

document.querySelectorAll("[data-back]").forEach((b) =>
  b.addEventListener("click", () => goTo(+b.dataset.back))
);

/* ---------- card input formatting ---------- */
$("#ccNum").addEventListener("input", (e) => {
  e.target.value = e.target.value.replace(/\D/g, "").slice(0, 16).replace(/(\d{4})(?=\d)/g, "$1 ");
});
$("#ccExp").addEventListener("input", (e) => {
  let v = e.target.value.replace(/\D/g, "").slice(0, 4);
  if (v.length > 2) v = v.slice(0, 2) + "/" + v.slice(2);
  e.target.value = v;
});

/* ---------- payment tabs ---------- */
document.querySelectorAll(".pay-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    state.payMethod = tab.dataset.pay;
    document.querySelectorAll(".pay-tab").forEach((t) => t.classList.toggle("active", t === tab));
    document.querySelectorAll(".pay-panel").forEach((p) =>
      p.classList.toggle("active", p.id === "pay-" + state.payMethod)
    );
    renderSummary();
  });
});

/* ---------- QR platba (demo SPD format) ---------- */
let qrPayObj = null;
function renderPayQR() {
  const target = $("#qrPay");
  target.innerHTML = "";
  const amount = total().toFixed(2);
  const spd = `SPD*1.0*ACC:CZ0000000000000000DEMO*AM:${amount}*CC:CZK*MSG:ZOO SEDLEC VSTUPENKY DEMO`;
  qrPayObj = new QRCode(target, { text: spd, width: 168, height: 168, correctLevel: QRCode.CorrectLevel.M });
}

/* ---------- pay & issue tickets ---------- */
function pay() {
  const spinner = $("#paySpinner");
  spinner.classList.add("show");
  $("#btnNext").disabled = true;
  setTimeout(() => {
    spinner.classList.remove("show");
    $("#btnNext").disabled = false;
    issueTickets();
    goTo(4);
  }, 1700);
}

function randomCode(len) {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  let s = "";
  for (let i = 0; i < len; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return s;
}

function issueTickets() {
  const order = "ZS-" + new Date().getFullYear() + "-" + randomCode(6);
  $("#orderCode").textContent = order;
  const paidLabel = {
    card: "zaplaceno kartou (demo)",
    qr: "zaplaceno QR platbou (demo)",
    onsite: "platba na pokladně",
  }[state.payMethod];
  $("#successMsg").innerHTML =
    `Objednávka pro <strong>${state.contact.name}</strong> na den <strong>${czDate(state.date)}</strong> — ` +
    `${fmt(total())}, ${paidLabel}. Vstupenky by dorazily na <strong>${state.contact.email}</strong>.`;

  const list = $("#ticketsList");
  list.innerHTML = "";
  const items = [];
  ["adult", "child", "baby"].forEach((k) => {
    for (let i = 0; i < state.counts[k]; i++) items.push(k);
  });
  for (let i = 0; i < state.counts.tour; i++) items.push("tour");

  items.forEach((k, idx) => {
    const code = order + "-" + String(idx + 1).padStart(2, "0") + "-" + randomCode(4);
    const el = document.createElement("div");
    el.className = "eticket";
    el.innerHTML =
      `<div class="qr-target"></div>` +
      `<div class="et-info">` +
      `<div class="et-type">${LABELS[k].toUpperCase()}</div>` +
      `<div class="et-meta">Faunapark ZOO Sedlec · ${czDate(state.date)} · 9:00–18:00<br>` +
      `${k === "tour" ? "Sraz u hlavního vchodu, čas dle domluvy na pokladně" : "U Mikulova, 691 21 Sedlec"} · ${fmt(PRICES[k])}</div>` +
      `<div class="et-code">${code}</div>` +
      `</div>`;
    list.appendChild(el);
    new QRCode(el.querySelector(".qr-target"), {
      text: `ZOOSEDLEC|${code}|${k.toUpperCase()}|${state.date}`,
      width: 92,
      height: 92,
      correctLevel: QRCode.CorrectLevel.M,
    });
  });

  try {
    localStorage.setItem("zs-demo-order", JSON.stringify({ order, state, when: Date.now() }));
  } catch (e) { /* private mode — ignore */ }

  if (window.gsap) {
    gsap.from("#ticketsList .eticket", {
      y: 40, opacity: 0, duration: 0.6, stagger: 0.12, delay: 0.3, ease: "back.out(1.4)",
    });
  }
}

$("#btnPrint").addEventListener("click", () => window.print());

renderSummary();
