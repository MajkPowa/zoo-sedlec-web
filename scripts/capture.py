# -*- coding: utf-8 -*-
"""Capture the running site at several scroll positions with Playwright."""
import os
import sys
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "_cmp", "cur")
os.makedirs(OUT, exist_ok=True)

# fraction of total scrollable height OR absolute px (int)
STOPS = {
    "hero": 0,
    "sanctuary": "sel:.sec-sanctuary",
    "swamp-card": "sel+:.sec-sanctuary:300",
    "protect": "sel:.sec-protect",
    "protect-mid": "sel+:.sec-protect:380",
    "savanna": "sel:.sec-savanna",
    "savanna-mid": "sel+:.sec-savanna:380",
    "pricing": "sel:.sec-pricing",
    "wave": "sel+:.sec-pricing:560",
    "things": "sel:.sec-things",
    "things-mid": "sel+:.sec-things:380",
    "love": "sel:.sec-love",
    "love-mid": "sel+:.sec-love:420",
    "deep": "sel:.sec-deep",
    "footer": "end",
}

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 960})
    page.goto("http://127.0.0.1:8487/index.html")
    page.wait_for_timeout(3500)
    for name, stop in STOPS.items():
        if stop == "end":
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        elif isinstance(stop, str) and stop.startswith("sel+:"):
            _, sel, extra = stop.split(":")
            page.evaluate(
                "([s, e]) => { const t = document.querySelector(s).getBoundingClientRect().top + scrollY; window.scrollTo(0, t + parseInt(e)); }",
                [sel, extra],
            )
        elif isinstance(stop, str) and stop.startswith("sel:"):
            sel = stop[4:]
            page.evaluate(
                "(s) => { const t = document.querySelector(s).getBoundingClientRect().top + scrollY; window.scrollTo(0, t); }",
                sel,
            )
        else:
            page.evaluate(f"window.scrollTo(0, {stop})")
        page.wait_for_timeout(1800)
        page.screenshot(path=os.path.join(OUT, f"{name}.png"))
        print(name, "captured", flush=True)
    b.close()
print("done")
