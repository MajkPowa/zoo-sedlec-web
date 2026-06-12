# -*- coding: utf-8 -*-
"""Replace inline SVG sprites with generated <img> assets across all HTML files.
Keeps class, style and data-* attributes so CSS positioning and GSAP animations
continue to work unchanged."""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")

# sprite class token -> image file (order matters: more specific tokens first)
MAP = [
    ("a-toucan2", "animal-toucan.png"),
    ("a-toucan", "animal-toucan-flip.png"),
    ("a-parrot", "animal-macaw.png"),
    ("a-monkey", "animal-monkey.png"),
    ("a-owl", "animal-owl.png"),
    ("a-bird2", "animal-bird-yellow.png"),
    ("a-bird", "animal-bird-yellow.png"),
    ("a-squirrel", "animal-squirrel.png"),
    ("a-sloth", "animal-sloth.png"),
    ("a-snake", "animal-snake.png"),
    ("a-deer", "animal-deer.png"),
    ("a-croc", "animal-crocodile.png"),
    ("a-frog", "animal-frog.png"),
    ("a-flam1", "animal-flamingo-standing.png"),
    ("a-flam2", "animal-flamingo-feeding.png"),
    ("a-tiger", "animal-tiger.png"),
    ("a-turtle", "animal-snapping-turtle.png"),
    ("a-lion", "animal-lion.png"),
    ("a-whaleshark", "animal-whale-shark.png"),
    ("a-seaturtle", "animal-sea-turtle.png"),
    ("a-moorish", "fish-moorish-idol.png"),
    ("a-bluetang", "fish-blue-tang.png"),
    ("a-lionfish", "fish-wrasse.png"),
    ("a-wrasse", "fish-wrasse-flip.png"),
    ("a-spotfish", "fish-spotted.png"),
    ("s-mushrooms", "prop-mushrooms.png"),
    ("pet-toucan", "animal-toucan-flip.png"),
    ("pet-orangutan", "animal-orangutan.png"),
    ("pet-flamingo", "animal-flamingo-standing.png"),
]

KEEP_ATTRS = re.compile(r'(class|style|data-[a-z-]+)="[^"]*"')


def swap(html):
    count = 0
    for token, img in MAP:
        pattern = re.compile(
            r'<svg([^>]*\bclass="[^"]*\b' + re.escape(token) + r'\b[^"]*"[^>]*)>[\s\S]*?</svg>'
        )

        def repl(m):
            nonlocal count
            attrs = " ".join(a.group(0) for a in KEEP_ATTRS.finditer(m.group(1)))
            count += 1
            return f'<img src="assets/img/{img}" alt="" {attrs}>'

        html = pattern.sub(repl, html)
    return html, count


def main():
    total = 0
    for fn in os.listdir(ROOT):
        if not fn.endswith(".html"):
            continue
        path = os.path.join(ROOT, fn)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        new, n = swap(html)
        if n:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
        print(f"{fn}: {n} sprites swapped")
        total += n
    print(f"TOTAL: {total}")


if __name__ == "__main__":
    main()
