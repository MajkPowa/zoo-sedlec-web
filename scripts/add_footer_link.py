# -*- coding: utf-8 -*-
"""Insert the 'Vstupenky online' link into the footer of every page."""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OLD = '<a href="pred-navstevou.html">Před návštěvou</a>\n      <a href="mapa-zoo.html">Mapa ZOO</a>'
NEW = ('<a href="pred-navstevou.html">Před návštěvou</a>\n'
       '      <a href="vstupenky.html">Vstupenky online</a>\n'
       '      <a href="mapa-zoo.html">Mapa ZOO</a>')

count = 0
for fn in os.listdir(ROOT):
    if not fn.endswith(".html") or fn == "vstupenky.html":
        continue
    path = os.path.join(ROOT, fn)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if OLD in html and 'href="vstupenky.html">Vstupenky online' not in html:
        html = html.replace(OLD, NEW)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        count += 1
        print(fn, "updated")
print("total", count)
