# -*- coding: utf-8 -*-
"""Generate flat-vector zoo assets via Gemini image model (Nano Banana 2),
chroma-key the solid background away and autocrop to content."""
import base64
import json
import os
import sys
import time
import urllib.request
from collections import deque
from PIL import Image

KEY = os.environ.get("GEMINI_KEY")
if not KEY:
    sys.exit("GEMINI_KEY env var missing")

MODEL = "gemini-3-pro-image"
FALLBACK_MODEL = "gemini-2.5-flash-image"
OUT_RAW = os.path.join(os.path.dirname(__file__), "..", "assets", "img_raw")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT_RAW, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

STYLE = ("flat vector illustration, children's storybook style, smooth rounded organic shapes, "
         "soft flat colors with subtle two-tone shading, no outlines, clean minimal detail, "
         "matte finish, no drop shadow on the ground, single subject centered")

MAGENTA = "plain solid uniform magenta #FF00FF background filling the whole canvas"
GREEN = "plain solid uniform bright green #00FF00 background filling the whole canvas"

# name, aspect, bg ("magenta"/"green"), prompt body
ASSETS = [
    ("animal-macaw", "4:5", "green",
     "Scarlet macaw parrot perched on a short dark mossy branch, side profile facing left, crimson red body, "
     "bright blue and green layered wing feathers, long elegant tail hanging below the branch, cream face patch, "
     "black curved beak, one round dark eye"),
    ("animal-toucan", "5:4", "magenta",
     "Toco toucan perched on a short dark mossy branch, side profile facing left, glossy black body, white chest, "
     "oversized banana-orange beak with darker tip, small blue feet, friendly round eye"),
    ("animal-monkey", "4:5", "magenta",
     "Cute capuchin monkey sitting on a short horizontal dark branch, facing forward, warm orange-brown fur, "
     "lighter cream face and belly, long curled tail hanging below the branch, small dark eyes, relaxed pose"),
    ("animal-owl", "1:1", "magenta",
     "Barn owl perched on a short dark branch, facing slightly left, heart-shaped white facial disc, sandy beige "
     "wings with delicate speckles, white chest, dark round eyes, compact upright pose"),
    ("animal-bird-yellow", "1:1", "magenta",
     "Tiny round songbird perched on a green reed stem, side profile facing right, sunny yellow body, darker wing, "
     "small orange beak"),
    ("animal-squirrel", "1:1", "magenta",
     "Red squirrel clinging to the side of a dark teal tree trunk, side view facing left, fluffy oversized curved "
     "tail, orange fur with cream belly, tiny paws, alert ears"),
    ("animal-sloth", "4:3", "magenta",
     "Adorable sloth hanging upside down from a horizontal mossy green branch by all four hooked claws, cream and "
     "tan soft fur, brown eye patches, gentle sleepy smile, relaxed dangling round body"),
    ("animal-snake", "3:4", "green",
     "Orange tree boa snake coiled in three loops around a section of vertical dark navy tree trunk #0D2B3C, head "
     "hanging down curiously with small forked tongue, warm orange body with darker rust pattern"),
    ("animal-deer", "1:1", "magenta",
     "Young spotted fallow deer standing in profile facing right, warm caramel coat with white spots on the back, "
     "white belly, slim legs, small antlers, alert ears, gentle dark eye"),
    ("animal-crocodile", "21:9", "magenta",
     "Crocodile floating low in turquoise swamp water, only the top of the head, eyes, nostrils and ridged back "
     "visible above the waterline, side view facing left, muted green #4E8F3C body, thin turquoise #35C7B2 water "
     "ripple band along the body"),
    ("animal-frog", "4:3", "magenta",
     "Cute green tree frog sitting on a smooth grey round stone, facing forward, big round eyes on top of the "
     "head, lighter belly, content smile"),
    ("animal-flamingo-standing", "9:16", "green",
     "Elegant pink flamingo standing in shallow water, S-curved neck held high, side profile facing left, rose "
     "pink body, darker pink wing, white face, black tipped beak, long thin legs"),
    ("animal-flamingo-feeding", "9:16", "green",
     "Pink flamingo feeding, long neck curved down with black-tipped beak dipped toward the water, side profile "
     "facing left, rose pink body, both thin stick legs visible"),
    ("animal-tiger", "4:5", "magenta",
     "Bengal tiger sitting upright like a proud cat, side-front view facing left, warm orange coat with bold "
     "black brushstroke stripes, white chest, muzzle and paws, calm noble expression, long tail curled beside "
     "the body"),
    ("animal-snapping-turtle", "16:9", "magenta",
     "Large alligator snapping turtle walking, side profile facing right, high domed moss-green shell with rugged "
     "pointed scutes, sturdy clawed legs, wrinkled neck stretched forward, small wise eye"),
    ("animal-lion", "3:2", "magenta",
     "Majestic male lion lying relaxed on flat grey rock slabs, side view facing right, front paws stretched "
     "forward, rich layered red-brown rounded mane, golden tan body, peaceful half-closed eyes, tail with dark "
     "tuft"),
    ("animal-stag-drinking", "4:3", "magenta",
     "Spotted deer stag drinking, head lowered to a small oval blue waterhole in amber sand, side view facing "
     "left, branched antlers, warm brown coat with white spots, small ripples where the muzzle meets the water"),
    ("animal-whale-shark", "21:9", "magenta",
     "Gentle whale shark swimming, full side profile facing right, steel blue-grey body covered with a grid of "
     "pale dots, white belly, wide flat friendly mouth, gill slits, tall dorsal fin and crescent tail, three tiny "
     "white pilot fish swimming alongside"),
    ("animal-sea-turtle", "4:3", "magenta",
     "Green sea turtle swimming gracefully, three-quarter side view facing right with front flippers spread "
     "mid-stroke, olive-green hexagon patterned shell, lighter green-grey skin, gentle smiling face"),
    ("fish-moorish-idol", "4:3", "magenta",
     "Moorish idol reef fish, side profile facing right, white body with two bold black vertical bands and a "
     "yellow saddle, long trailing white dorsal filament"),
    ("fish-blue-tang", "3:2", "magenta",
     "Blue tang surgeonfish, side profile facing right, vivid royal blue body with black palette marking, bright "
     "yellow tail fin"),
    ("fish-wrasse", "3:2", "magenta",
     "Ornate orange reef wrasse with flowing striped fan fins, side profile facing right, warm orange body with "
     "thin dark vertical stripes, teal-blue translucent fins"),
    ("fish-spotted", "3:2", "magenta",
     "Round reef fish, side profile facing right, sandy cream body with brown polka dots, small fins, friendly "
     "eye"),
    ("animal-orangutan", "1:1", "magenta",
     "Cute baby orangutan sitting, full body, front view, round fuzzy rust-orange body, big amber eyes, lighter "
     "cream face and belly, long arms resting on the ground, curious friendly expression"),
    ("prop-mushrooms", "4:3", "magenta",
     "Cluster of three orange forest mushrooms with cream stems growing on a small piece of dark bark"),
]


def call_model(model, prompt, aspect, size="1K"):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": size},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError("no image in response")


def chroma_key(path_in, path_out, max_side=900):
    img = Image.open(path_in).convert("RGBA")
    px = img.load()
    w, h = img.size
    # background colour = median of corners
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))

    def close(p, tol):
        return (p[0] - bg[0]) ** 2 + (p[1] - bg[1]) ** 2 + (p[2] - bg[2]) ** 2 <= tol * tol

    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if close(px[x, y], 70):
                q.append((x, y)); seen[y * w + x] = 1
    for y in range(h):
        for x in (0, w - 1):
            if close(px[x, y], 70) and not seen[y * w + x]:
                q.append((x, y)); seen[y * w + x] = 1
    while q:
        x, y = q.popleft()
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                if close(px[nx, ny], 70):
                    seen[ny * w + nx] = 1
                    q.append((nx, ny))
    # global pass: kill enclosed pockets of the key colour (pure chroma keys only,
    # stylized illustration colours stay far from #FF00FF / #00FF00 at tol 70)
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] != 0 and close(p, 70):
                px[x, y] = (0, 0, 0, 0)
    # soften 1px halo: clear opaque pixels touching >=3 transparent neighbours that are near bg colour
    to_clear = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            p = px[x, y]
            if p[3] == 0:
                continue
            n = sum(1 for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if px[nx, ny][3] == 0)
            if n >= 3 and close(p, 160):
                to_clear.append((x, y))
    for x, y in to_clear:
        px[x, y] = (0, 0, 0, 0)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    if max(img.size) > max_side:
        r = max_side / max(img.size)
        img = img.resize((round(img.size[0] * r), round(img.size[1] * r)), Image.LANCZOS)
    img.save(path_out, optimize=True)


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
                chroma_key(raw_file, out_file)
                print(f"[{i}/{len(todo)}] {name} OK ({model})", flush=True)
                break
            except Exception as e:
                msg = str(e)
                print(f"[{i}/{len(todo)}] {name} attempt {attempt+1} failed: {msg[:160]}", flush=True)
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    time.sleep(30)
                    if attempt >= 2:
                        model = FALLBACK_MODEL
                else:
                    time.sleep(8)
                    if attempt >= 2:
                        model = FALLBACK_MODEL
        time.sleep(2)


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
