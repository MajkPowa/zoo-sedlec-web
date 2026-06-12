# -*- coding: utf-8 -*-
"""Third asset batch: individual scenery ELEMENTS (transparent) used to compose
the section backgrounds in layers, like the reference design."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from gen_assets import call_model, chroma_key, MODEL, FALLBACK_MODEL, OUT, OUT_RAW, STYLE, MAGENTA, GREEN

# (name, aspect, bg, prompt)
ASSETS = [
    # --- forest trunks (stretched vertically in CSS, so straight columns) ---
    ("el-trunk-navy", "9:16", "magenta",
     "Single tall straight jungle tree trunk column filling the full image height, flat deep navy blue color "
     "#14374F with a few subtle darker vertical bark streaks and one lighter side edge, slightly irregular "
     "organic silhouette, no branches, no leaves, no roots"),
    ("el-trunk-green", "9:16", "magenta",
     "Single tall straight jungle tree trunk column filling the full image height, flat deep green color "
     "#1E5B49 with subtle darker vertical bark streaks and one lighter side edge, slightly irregular organic "
     "silhouette, no branches, no leaves, no roots"),
    ("el-trunk-teal", "9:16", "magenta",
     "Single tall straight jungle tree trunk column filling the full image height, flat sea-green color "
     "#2A7558 with subtle darker vertical bark streaks and one lighter side edge, slightly irregular organic "
     "silhouette, no branches, no leaves, no roots"),
    ("el-trunk-dark", "9:16", "magenta",
     "Single tall wide jungle tree trunk column filling the full image height, very dark navy color #0D2B3C, "
     "almost silhouette with barely visible bark streaks, slightly irregular organic silhouette, no branches, "
     "no leaves"),
    ("el-vine1", "9:16", "magenta",
     "Single long hanging jungle liana vine starting at the top edge and hanging down in a gentle S curve, "
     "thin green stem with small green leaves along it, delicate"),
    ("el-vine2", "9:16", "magenta",
     "Two thin hanging jungle liana vines starting at the top edge, gently curving, sparse small green "
     "leaves, delicate"),
    # --- swamp pieces ---
    ("el-trunk-base", "1:1", "green",
     "Bottom section of a dark teal mangrove tree trunk standing in turquoise water #3CC7B2, water ripple "
     "ring around the trunk at the waterline, small reflection below, flat dark blue-green trunk #1A5C55"),
    ("el-bank", "16:9", "green",
     "Lush mossy green river bank mound seen from the side, layered bright and darker green grass shapes "
     "with small grass tufts on top and a few tiny pink flowers, gently rounded, designed to sit at the "
     "edge of water"),
    ("el-islet", "3:2", "green",
     "Small mossy green islet floating in turquoise water, rounded moss mound with a few grass blades on "
     "top, thin turquoise water ripple around its base"),
    ("el-log", "3:2", "magenta",
     "Old brown wooden log floating horizontally in turquoise water, mossy patch on top, visible wood end "
     "ring, thin water ripple line along the waterline"),
    # --- meadow / hills ---
    ("el-hill", "16:9", "magenta",
     "Wide rounded bright green grassy hill seen from the side, smooth meadow silhouette in two layered "
     "shades of green #74B54A and #5DA23C, a few small grass tufts sticking up from the ridge"),
    ("el-mound", "3:2", "magenta",
     "Rounded grassy mound hump, bright green meadow grass #67AB41 with a darker green base shadow and a "
     "few grass tufts on top, smooth dome shape"),
    ("el-outcrop", "4:3", "green",
     "Grassy rocky outcrop ledge seen from the side: layered green grass shelf with a large flat smooth "
     "grey stone slab on top and a couple of smaller stones, designed as a corner element"),
    ("el-ledge", "4:3", "magenta",
     "Corner scenery element for the top-left corner of a scene: a lush green grassy bank ledge with one "
     "large flat smooth grey stone resting on it, the grass mass is CUT OFF by the top edge and the left "
     "edge of the canvas as if it continues beyond the image, only the bottom side and right side have an "
     "organic wavy grass outline with a few hanging grass tufts, magenta background visible only in the "
     "bottom right area"),
    # --- savanna ---
    ("el-rockslab", "3:2", "magenta",
     "Group of flat grey rock slabs stacked low on sandy ground, smooth rounded stone shapes in two grey "
     "tones with subtle highlights"),
    ("el-dry-grass", "1:1", "magenta",
     "Tuft of dry golden savanna grass, thin curved blades in warm ochre #C87F2A with a couple of seed "
     "stalks, small ground shadow"),
    # --- beach ---
    ("el-beach-set", "3:2", "magenta",
     "Small beach still life group: one orange starfish, two cream seashells and three small smooth "
     "pebbles arranged loosely on flat ground"),
    ("el-starfish", "1:1", "magenta",
     "Single orange starfish with five rounded arms and tiny dot texture, flat lay"),
    # --- underwater ---
    ("el-kelp", "3:4", "magenta",
     "Cluster of green kelp seaweed strands swaying gently upward, ribbon-like leaves in two shades of "
     "green, growing from a small rocky base"),
    ("el-reef-rock", "4:3", "green",
     "Underwater rocky reef ledge corner element: rounded grey-teal rocks stacked, with red tube corals "
     "#D4574E, one orange brain coral and a green kelp sprig growing on top"),
]


def main(only=None):
    todo = [a for a in ASSETS if only is None or a[0] in only]
    for i, (name, aspect, bgc, body) in enumerate(todo, 1):
        out_file = os.path.join(OUT, name + ".png")
        if os.path.exists(out_file):
            print(f"[{i}/{len(todo)}] {name} exists, skip", flush=True)
            continue
        bg = MAGENTA if bgc == "magenta" else GREEN
        prompt = f"{body}, {STYLE}, {bg}"
        raw_file = os.path.join(OUT_RAW, name + ".png")
        model = MODEL
        for attempt in range(5):
            try:
                png = call_model(model, prompt, aspect)
                with open(raw_file, "wb") as f:
                    f.write(png)
                chroma_key(raw_file, out_file, max_side=1000)
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
