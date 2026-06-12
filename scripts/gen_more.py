# -*- coding: utf-8 -*-
"""Second asset batch: full scene backgrounds, coral/plant props and parchment
paper textures. Backgrounds are saved as-is (no chroma key), props and papers
are keyed like the animals."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from gen_assets import call_model, chroma_key, MODEL, FALLBACK_MODEL, OUT, OUT_RAW, STYLE, MAGENTA

SCENE_STYLE = ("flat vector illustration, children's storybook style, smooth rounded organic shapes, "
               "soft flat colors with subtle two-tone shading, no outlines, clean minimal detail, "
               "matte finish, rich layered scenery, no text, no animals, no people")

# (name, aspect, kind: bg|prop|paper, prompt)
ASSETS = [
    ("bg-forest-swamp", "9:16", "bg",
     "Tall tropical rainforest interior seen between giant tree trunks: upper two thirds are dense vertical "
     "trunks in deep navy #0C2336 and dark teal greens #175547 #1E5B49 #2A7558 reaching top to bottom, pale "
     "lime god rays falling diagonally from the upper right, hanging lianas with small leaves, tiny glowing "
     "yellow firefly dots; lower third is a calm turquoise mangrove swamp #3CC7B2 where the dark trunk bases "
     "stand in the water with soft horizontal reflections, a mossy green bank with grass tufts and tiny pink "
     "flowers in the bottom left corner, small mossy islet with grass on the bottom right, a few lily pads and "
     "cattail reeds, an old floating log; center of the image stays calm and uncluttered"),
    ("bg-lake-meadow", "5:4", "bg",
     "Calm turquoise lake #3CC7B2 #2FB5A4 filling most of the scene with subtle lighter horizontal water "
     "streaks, scattered lily pads with one pink lotus, clumps of cattail reeds; a grassy rocky outcrop with a "
     "flat grey stone juts in from the top left corner, a smaller grassy ledge from the top right; the bottom "
     "fifth is rolling bright green meadow hills #74B54A #5DA23C with grass tufts, with a rounded grassy mound "
     "rising in the bottom right corner; middle of the scene stays open and calm"),
    ("bg-savanna", "5:4", "bg",
     "Warm amber African savanna ground #F0A23A #E8902C viewed flat, gentle wavy bands of lighter and darker "
     "sand, scattered tufts of dry golden grass #C87F2A, a few small grey rocks, a group of flat grey rock "
     "slabs in the middle left area, a bright green grass strip running along the very top edge melting into "
     "the sand; bottom right corner has a small patch of dry grass; center stays open and calm"),
    ("bg-beach", "4:3", "bg",
     "Sunny warm sandy beach seen from above at a gentle angle, yellow sand #F5BF4E #F7CA5A with soft dune "
     "ripple bands, a few orange starfish, cream seashells and small pebbles scattered near the edges, sparse "
     "dry beach grass in the top corners, soft warm light, no water no sea, only sand, center stays open"),
    ("bg-underwater-light", "5:4", "bg",
     "Bright underwater ocean scene, clear teal water gradient from #2BBFA4 at the top to #1BA88E below, wide "
     "diagonal sun rays shafting down from the upper left, small rising air bubbles, a rocky reef ledge with "
     "red tube corals #D4574E, orange coral and green kelp in the bottom right corner, faint distant reef "
     "silhouette along the bottom, large calm open water in the center"),
    ("bg-underwater-deep", "1:1", "bg",
     "Deep underwater ocean scene, teal gradient from #1BA88E down to #149280, soft faint light rays from "
     "above, layered rocky ridge silhouettes in darker teal across the lower half, sandy sea floor along the "
     "bottom edge decorated with red tube corals #D4574E, orange corals, swaying green kelp and small rocks, "
     "tiny bubbles, distant whale silhouette far in the background left, calm open water in the center"),
    ("bg-underwater-deep2", "1:1", "bg",
     "Deepest underwater ocean scene, teal gradient from #149280 down to #0D7A6B, very soft light rays, a "
     "dark rocky ridge silhouette crossing the upper third, sandy sea floor along the bottom with a large "
     "cluster of red tube corals #D4574E on the right, orange brain corals, green kelp strands and rounded "
     "rocks, tiny bubbles, calm open water in the center left"),
    ("prop-coral-cluster", "4:3", "prop",
     "Vibrant coral reef cluster on a grey rock base: tall red tube corals #D4574E, round orange brain coral "
     "#E08A3C, pink fan coral, a few green kelp strands swaying upward, small pebbles"),
    ("prop-coral-small", "1:1", "prop",
     "Small coral group: three red tube corals #D4574E of different heights with one small orange coral and "
     "a green seaweed sprig on a tiny rock"),
    ("prop-lilypads", "4:3", "prop",
     "Group of three green water lily pads with notches floating on water surface seen from a low angle, one "
     "blooming pink lotus flower, tiny water ripples around them"),
    ("prop-reeds", "3:4", "prop",
     "Clump of cattail reeds, five tall green stems with brown velvet seed heads and slim leaves, slightly "
     "swaying, growing from a small grassy base"),
    ("prop-flower-bush", "1:1", "prop",
     "Small lush green bush covered with pink blossom flowers #E86FA0 and lighter pink buds, rounded organic "
     "silhouette"),
    ("paper-landscape", "4:3", "paper",
     "Blank sheet of old parchment paper, landscape orientation, softly torn irregular edges all around, "
     "gentle crumple creases and folds catching soft light, warm cream color #F2E9D6 with slightly darker "
     "aged tone near the edges and corners, completely blank empty surface with no text and no drawings, "
     "flat lay, subtle paper grain"),
    ("paper-portrait", "4:5", "paper",
     "Blank sheet of old parchment paper, portrait orientation, softly torn irregular edges all around, "
     "gentle crumple creases catching soft light, warm cream color #F2E9D6 with slightly darker aged tone "
     "near the edges and corners, completely blank empty surface with no text and no drawings, flat lay, "
     "subtle paper grain"),
]


def main(only=None):
    todo = [a for a in ASSETS if only is None or a[0] in only]
    for i, (name, aspect, kind, body) in enumerate(todo, 1):
        out_file = os.path.join(OUT, name + ".png")
        if os.path.exists(out_file):
            print(f"[{i}/{len(todo)}] {name} exists, skip", flush=True)
            continue
        if kind == "bg":
            prompt = f"{body}, {SCENE_STYLE}"
        else:
            prompt = f"{body}, {STYLE}, {MAGENTA}"
        raw_file = os.path.join(OUT_RAW, name + ".png")
        model = MODEL
        for attempt in range(5):
            try:
                png = call_model(model, prompt, aspect)
                with open(raw_file, "wb") as f:
                    f.write(png)
                if kind == "bg":
                    from PIL import Image
                    img = Image.open(raw_file)
                    if max(img.size) > 1600:
                        r = 1600 / max(img.size)
                        img = img.resize((round(img.size[0] * r), round(img.size[1] * r)), Image.LANCZOS)
                    img.save(out_file, optimize=True)
                else:
                    chroma_key(raw_file, out_file, max_side=1100)
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
