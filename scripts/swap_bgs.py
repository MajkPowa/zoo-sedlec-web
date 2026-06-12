# -*- coding: utf-8 -*-
"""Replace the big inline scene-background SVGs in index.html with generated
scene images (stretched exactly like preserveAspectRatio=none did)."""
import os
import re

PATH = os.path.join(os.path.dirname(__file__), "..", "index.html")

SWAPS = [
    ("forest-bg", "bg-forest-swamp.png"),
    ("protect-bg", "bg-lake-meadow.png"),
    ("savanna-bg", "bg-savanna.png"),
    ("beach-bg", "bg-beach.png"),
    ("things-bg", "bg-underwater-light.png"),
    ("love-bg", "bg-underwater-deep.png"),
    ("deep-bg", "bg-underwater-deep2.png"),
]

with open(PATH, encoding="utf-8") as f:
    html = f.read()

for cls, img in SWAPS:
    pattern = re.compile(r'<svg[^>]*\bclass="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*>[\s\S]*?</svg>\n?')
    repl = f'<img class="scene-bg {cls}" src="assets/img/{img}" alt="">\n'
    html, n = pattern.subn(repl, html)
    print(f"{cls}: {n} replaced")

with open(PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("done")
