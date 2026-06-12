# -*- coding: utf-8 -*-
"""Composed full-width scenery BANDS in 2K sharpness. The model arranges the
elements coherently inside each band; bands anchor to scene edges."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from gen_assets import call_model, chroma_key, MODEL, FALLBACK_MODEL, OUT, OUT_RAW, STYLE, MAGENTA

BAND_STYLE = ("flat vector illustration, children's storybook style, smooth rounded organic shapes, "
              "soft flat colors with subtle two-tone shading, no outlines, rich coherent composition, "
              "crisp clean edges, high detail, matte finish")

# (name, aspect, prompt)
ASSETS = [
    ("band-canopy", "21:9",
     "Jungle canopy border element hanging from the TOP edge of the canvas: overlapping layered clusters of "
     "dark green and deep teal leaves in varied sizes forming an organic scalloped fringe across the whole "
     "width, two thin liana vines with small leaves hanging lower, the foliage mass is cut off by the top "
     "edge as if it continues above, magenta background fills the lower two thirds"),
    ("band-swamp", "21:9",
     "Mangrove swamp shoreline band sitting on the BOTTOM edge of the canvas: a shallow strip of turquoise "
     "water #3CC7B2 along the bottom, a lush mossy green bank with grass tufts and tiny pink flowers rising "
     "on the left side, a smaller mossy islet on the right, clusters of cattail reeds growing FROM the banks "
     "and shallow water, two groups of floating water lily pads with one pink lotus bloom, everything "
     "naturally arranged and connected to the water line, magenta background above the band"),
    ("band-lake", "21:9",
     "Bright green meadow lake-shore band sitting on the BOTTOM edge of the canvas: gently rolling grass "
     "meadow strip #74B54A with darker green layers, grass tufts sticking up along the ridge, a cluster of "
     "cattail reeds rising at the left end and another at the right end, a few tiny white wildflowers, "
     "natural coherent arrangement, magenta background above"),
    ("band-savanna", "21:9",
     "Golden savanna ground band sitting on the BOTTOM edge of the canvas: clumps of tall dry golden grass "
     "#C87F2A in natural groups, two small grey rounded rocks nestled among the grass, subtle warm sand "
     "mounds, sparse and airy arrangement, magenta background above"),
    ("band-reef", "21:9",
     "Underwater coral reef floor band sitting on the BOTTOM edge of the canvas: teal-grey rounded rocks in "
     "varied sizes, red tube corals, one orange brain coral, a pink fan coral, swaying green kelp strands "
     "and short seagrass growing between the rocks, one small orange starfish on the sand, coherent natural "
     "reef arrangement across the width, the entire empty area above the reef must be filled with pure flat "
     "magenta #FF00FF, no dark background, no water color"),
    ("band-reef-deep", "21:9",
     "Deep sea floor band sitting on the BOTTOM edge of the canvas: dark teal rocks, a large cluster of red "
     "tube corals on the right, tall green kelp strands on the left, scattered small corals and seagrass "
     "between, slightly darker moodier palette, coherent arrangement, magenta background above"),
]


def main(only=None):
    todo = [a for a in ASSETS if only is None or a[0] in only]
    for i, (name, aspect, body) in enumerate(todo, 1):
        out_file = os.path.join(OUT, name + ".png")
        if os.path.exists(out_file):
            print(f"[{i}/{len(todo)}] {name} exists, skip", flush=True)
            continue
        prompt = f"{body}, {BAND_STYLE}, {MAGENTA}"
        raw_file = os.path.join(OUT_RAW, name + ".png")
        model = MODEL
        for attempt in range(5):
            try:
                png = call_model(model, prompt, aspect, size="2K")
                with open(raw_file, "wb") as f:
                    f.write(png)
                chroma_key(raw_file, out_file, max_side=2200)
                print(f"[{i}/{len(todo)}] {name} OK ({model})", flush=True)
                break
            except Exception as e:
                print(f"[{i}/{len(todo)}] {name} attempt {attempt+1} failed: {str(e)[:160]}", flush=True)
                time.sleep(20 if "429" in str(e) else 8)
                if attempt >= 2:
                    model = FALLBACK_MODEL
        time.sleep(2)


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
