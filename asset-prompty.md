# Prompty pro generování assetů — ZOO Sedlec web

Cíl: nahradit současná jednoduchá SVG kvalitními ilustracemi ve stylu plochého vektorového
„storybook" designu (vrstvené scény, měkké tvary, jemné tónování ploch).

---

## 1. Doporučený nástroj a workflow

**Primárně: Recraft.ai** — jediný velký generátor, který umí exportovat **přímo SVG vektor**
(styl „Vector art / Flat illustration") a podporuje **vlastní styl** (Custom Style) pro konzistenci.

Alternativy: Midjourney v6 (`--style raw` + `--sref` pro konzistenci, výstup PNG → vektorizace přes
vectorizer.ai), Ideogram, DALL-E. U PNG výstupů vždy generovat na **průhledném pozadí** (nebo
jednolitém a odstranit přes remove.bg).

**Postup pro konzistentní sadu:**
1. Vygeneruj nejdřív 3–4 klíčová zvířata (tukan, tygr, lenochod) a vyber nejlepší výsledky.
2. V Recraftu z nich vytvoř **Custom Style** (v Midjourney použij `--sref <url>` první schválené generace).
3. Všechny další assety generuj tímto stylem — jinak se sada rozpadne.
4. Drž **jeden směr světla (zprava shora)** a **boční pohled** u zvířat.

**Technická nastavení:**
- Zvířata/rekvizity: poměr 1:1, průhledné pozadí, min. 1024×1024
- Pozadí sekcí: 16:9 nebo na výšku 2:3 (lesní zóna), min. 2048 px delší strana
- Negativní prompt (SD/Recraft): `photo, 3D render, outlines, sketch, gradient mesh, text, watermark, realistic fur, shadows on ground`

**Sdílená stylová kotva** (je vepsaná v každém promptu níže):
> flat vector illustration, children's storybook style, smooth rounded organic shapes, soft flat
> colors with subtle two-tone shading, no outlines, clean minimal detail, matte finish

---

## 2. Barevná paleta (vkládej hexy do promptů)

| Scéna | Barvy |
|---|---|
| Les (hero) | navy `#0C2336`, tmavé zelenomodré kmeny `#175547 #1E5B49 #2A7558 #14374F`, listy `#6FB556`, světlušky `#FFE98A` |
| Mokřad | tyrkys `#3CC7B2 #2FB5A4`, mech `#4AA64B`, rákos `#2E7A4F` |
| Louka/kopce | zelené `#74B54A #5DA23C #67AB41` |
| Savana | jantarová `#F0A23A #E8902C`, suchá tráva `#C87F2A`, kameny `#A8ADA3` |
| Pláž | písek `#F5BF4E #F7CA5A`, moře `#35CBB4`, pěna bílá |
| Podmoří | teal přechod `#2BBFA4 → #0D7A6B`, korály `#D4574E #E08A3C` |
| Papír/lístky | pergamen `#F2E9D6 #ECE0C6`, hnědý text `#7A4A21` |

---

## 3. POZADÍ SEKCÍ

### 3.1 Tropický les — hero (cíl: `assets/img/bg-forest.png`, na výšku 2:3)
```
Tall tropical rainforest interior, view between giant tree trunks reaching from floor to canopy,
layered depth: dark navy #0C2336 trunks in front, teal-green #175547 #2A7558 trunks behind,
volumetric god rays of pale lime light falling diagonally from upper right, hanging lianas with
small leaves, tiny glowing yellow fireflies #FFE98A floating in strings, mysterious dusk mood,
flat vector illustration, children's storybook style, smooth rounded organic shapes, soft flat
colors with subtle two-tone shading, no outlines, clean minimal detail, matte finish,
vertical composition 2:3
```

### 3.2 Mangrovový mokřad (cíl: `bg-swamp.png`, 16:9)
```
Tropical mangrove swamp, calm turquoise water #3CC7B2 with horizontal light streaks, dark
tree trunks standing in the water with soft reflections, mossy green islets with grass tufts,
water lily pads with pink lotus flowers, cattail reeds, floating old log, dragonflies above
the surface, flat vector illustration, children's storybook style, smooth rounded organic
shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish, 16:9
```

### 3.3 Savana (cíl: `bg-savanna.png`, 16:9)
```
Warm African savanna at golden hour, amber sand #F0A23A with lighter and darker wavy sand
patches, scattered tufts of dry golden grass #C87F2A, flat grey rock slabs, sparse stones,
green grassland strip melting into the sand at the top edge, small blue waterhole at the
bottom right, flat vector illustration, children's storybook style, smooth rounded organic
shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish, 16:9
```

### 3.4 Pláž s mořem (cíl: `bg-beach.png`, 16:9)
```
Sunny sandy beach from slightly elevated view, warm yellow sand #F5BF4E with soft dune
ripples, scattered starfish and seashells, dry beach grass, rolling turquoise sea #35CBB4
entering from the bottom with a wavy white foam edge, flat vector illustration, children's
storybook style, smooth rounded organic shapes, soft flat colors with subtle two-tone
shading, no outlines, matte finish, 16:9
```

### 3.5 Podmořský svět (cíl: `bg-underwater.png`, na výšku 2:3)
```
Underwater ocean scene, teal gradient from bright #2BBFA4 surface to deep #0D7A6B bottom,
diagonal sun rays shafting down from the surface, rising air bubbles, distant rocky reef
silhouettes, red tube corals #D4574E and orange brain corals #E08A3C on the sea floor,
swaying green kelp, small fish silhouettes in the distance, flat vector illustration,
children's storybook style, smooth rounded organic shapes, soft flat colors with subtle
two-tone shading, no outlines, matte finish, vertical 2:3
```

---

## 4. ZVÍŘATA — LES (hero)

> U všech: *side view, perched/sitting, isolated on transparent background, 1:1* —
> ať jdou položit na vlastní větve.

### 4.1 Ara papoušek (`animal-macaw.png`)
```
Scarlet macaw parrot perched on a short mossy branch, side profile facing right, crimson red
body, bright blue and green layered wing feathers, long elegant tail, cream face patch, black
curved beak, one round dark eye, flat vector illustration, children's storybook style, smooth
rounded organic shapes, soft flat colors with subtle two-tone shading, no outlines, matte
finish, isolated on transparent background
```

### 4.2 Tukan (`animal-toucan.png`)
```
Toco toucan perched on a branch, side profile facing left, glossy black body, white chest,
oversized banana-orange beak with darker tip, small blue feet, friendly round eye, slight
head tilt, flat vector illustration, children's storybook style, smooth rounded organic
shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish, isolated
on transparent background
```

### 4.3 Opice (`animal-monkey.png`)
```
Cute capuchin monkey sitting on a horizontal branch, facing forward, warm orange-brown fur,
lighter cream face and belly, long curled tail hanging below the branch, small expressive
dark eyes, relaxed pose, flat vector illustration, children's storybook style, smooth rounded
organic shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish,
isolated on transparent background
```

### 4.4 Sova pálená (`animal-owl.png`)
```
Barn owl perched on a branch, facing slightly left, heart-shaped white facial disc, sandy
beige wings with delicate speckles, white chest, dark round eyes, compact upright pose,
flat vector illustration, children's storybook style, smooth rounded organic shapes, soft
flat colors with subtle two-tone shading, no outlines, matte finish, isolated on transparent
background
```

### 4.5 Drobní: žlutý ptáček, veverka (`animal-bird-yellow.png`, `animal-squirrel.png`)
```
Tiny round songbird perched on a reed, side profile, sunny yellow body, darker wing, small
orange beak, flat vector illustration, children's storybook style, smooth rounded shapes,
soft flat colors, no outlines, transparent background
```
```
Red squirrel clinging to a tree trunk, side view, fluffy oversized curved tail, orange fur
with cream belly, tiny paws, alert ears, flat vector illustration, children's storybook
style, smooth rounded shapes, soft flat colors, no outlines, transparent background
```

---

## 5. ZVÍŘATA — MOKŘAD

### 5.1 Lenochod (`animal-sloth.png`)
```
Adorable sloth hanging upside down from a horizontal mossy branch by all four hooked claws,
cream and tan shaggy fur suggested with soft shapes, brown eye patches, gentle sleepy smile,
relaxed dangling body, flat vector illustration, children's storybook style, smooth rounded
organic shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish,
isolated on transparent background, horizontal composition
```

### 5.2 Had — psohlavec (`animal-snake.png`)
```
Orange tree boa snake coiled in three loops around a vertical dark tree trunk, head hanging
down curiously with a small forked tongue, warm orange body with darker rust diamond
pattern, flat vector illustration, children's storybook style, smooth rounded organic
shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish, isolated
on transparent background, vertical composition
```

### 5.3 Laň / jelínek (`animal-deer.png`)
```
Young spotted fallow deer standing in profile facing right, warm caramel coat with white
spots on the back, white belly, slim legs, small antlers, alert ears, gentle dark eye,
flat vector illustration, children's storybook style, smooth rounded organic shapes, soft
flat colors with subtle two-tone shading, no outlines, matte finish, isolated on
transparent background
```

### 5.4 Krokodýl (`animal-crocodile.png`)
```
Crocodile floating low in water, only the top of the head, eyes, nostrils and ridged back
visible above the waterline, side view facing right, muted swamp green #4E8F3C with darker
back scutes, subtle water ripple line around the body, flat vector illustration, children's
storybook style, smooth rounded organic shapes, soft flat colors, no outlines, matte finish,
isolated on transparent background, wide horizontal composition
```

### 5.5 Žába + vážka (`animal-frog.png`, `animal-dragonfly.png`)
```
Cute green tree frog sitting on a smooth grey stone, facing forward, big round eyes on top
of the head, lighter belly, content smile, flat vector illustration, children's storybook
style, smooth rounded shapes, soft flat colors, no outlines, transparent background
```
```
Delicate dragonfly in flight, top-side view, slim teal body, two pairs of translucent
pale-blue wings, flat vector illustration, children's storybook style, smooth shapes, soft
flat colors, no outlines, transparent background
```

---

## 6. ZVÍŘATA — VODA A TRÁVA

### 6.1 Plameňáci — 2 pózy (`animal-flamingo-standing.png`, `animal-flamingo-feeding.png`)
```
Elegant pink flamingo standing in shallow water on one long leg, S-curved neck held high,
side profile facing left, rose pink body #F08AA6 with darker wing tips, white face, black
tipped beak, soft reflection in the water, flat vector illustration, children's storybook
style, smooth rounded organic shapes, soft flat colors with subtle two-tone shading, no
outlines, matte finish, isolated on transparent background
```
```
Pink flamingo feeding, neck curved down with beak dipped toward the water surface, side
profile, rose pink body #F08AA6, black tipped beak, both stick legs visible, flat vector
illustration, children's storybook style, smooth rounded shapes, soft flat colors, no
outlines, transparent background
```

### 6.2 Tygr (`animal-tiger.png`)
```
Bengal tiger sitting upright like a proud cat, side-front view facing left, warm orange coat
#EE8A3C with bold black brushstroke stripes, white chest, muzzle and paws, calm noble
expression, long tail curled beside the body, flat vector illustration, children's storybook
style, smooth rounded organic shapes, soft flat colors with subtle two-tone shading, no
outlines, matte finish, isolated on transparent background
```

### 6.3 Kajmanka / želva (`animal-snapping-turtle.png`)
```
Large alligator snapping turtle walking, side profile facing right, high domed moss-green
shell with rugged pointed scutes, sturdy clawed legs, wrinkled neck stretched forward,
small wise eye, flat vector illustration, children's storybook style, smooth rounded organic
shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish, isolated
on transparent background
```

---

## 7. ZVÍŘATA — SAVANA

### 7.1 Lev (`animal-lion.png`)
```
Majestic male lion lying relaxed on flat grey rocks, side view facing right, front paws
stretched forward, rich layered red-brown mane in soft rounded clumps, golden tan body
#E0913F, peaceful half-closed eyes, tail with dark tuft, flat vector illustration,
children's storybook style, smooth rounded organic shapes, soft flat colors with subtle
two-tone shading, no outlines, matte finish, isolated on transparent background, wide
horizontal composition
```

### 7.2 Jelen u napajedla (`animal-stag-drinking.png`)
```
Spotted deer stag drinking, head lowered to a small blue waterhole, side view facing left,
branched antlers, warm brown coat with white spots, one front leg slightly bent, small
ripples where the muzzle meets the water, flat vector illustration, children's storybook
style, smooth rounded organic shapes, soft flat colors with subtle two-tone shading, no
outlines, matte finish, isolated on transparent background
```

### 7.3 Motýl (`prop-butterfly.png`)
```
Small cream-yellow butterfly in flight, top view with wings open, soft two-tone wings,
slim dark body, flat vector illustration, children's storybook style, smooth shapes, soft
flat colors, no outlines, transparent background
```

---

## 8. ZVÍŘATA — PODMOŘÍ

### 8.1 Žralok obrovský (`animal-whale-shark.png`)
```
Gentle whale shark swimming, full side profile facing right, steel blue-grey body #6F93B0
covered with a grid of pale dots, white belly, wide flat friendly mouth, three gill slits,
tall dorsal fin and crescent tail, three tiny white pilot fish swimming alongside, flat
vector illustration, children's storybook style, smooth rounded organic shapes, soft flat
colors with subtle two-tone shading, no outlines, matte finish, isolated on transparent
background, very wide horizontal composition
```

### 8.2 Mořská želva (`animal-sea-turtle.png`)
```
Green sea turtle swimming gracefully, three-quarter side view facing right with front
flippers spread mid-stroke, olive-green hexagon-patterned shell, lighter green-grey skin,
gentle smiling face, flat vector illustration, children's storybook style, smooth rounded
organic shapes, soft flat colors with subtle two-tone shading, no outlines, matte finish,
isolated on transparent background
```

### 8.3 Medúza (`animal-jellyfish.png`)
```
Dreamy translucent pink jellyfish, dome-shaped bell with lighter inner glow, four long wavy
ribbon tentacles flowing downward, semi-transparent layers, flat vector illustration,
children's storybook style, smooth rounded shapes, soft flat colors, no outlines, matte
finish, isolated on transparent background, vertical composition
```

### 8.4 Sada útesových ryb (`fish-moorish-idol.png`, `fish-blue-tang.png`, `fish-lionfish.png`, `fish-spotted.png`, `fish-small-silver.png`)
```
Moorish idol reef fish, side profile facing right, white body with two bold black vertical
bands and a yellow saddle, long trailing white dorsal filament, flat vector illustration,
children's storybook style, smooth shapes, soft flat colors, no outlines, transparent
background
```
```
Blue tang surgeonfish, side profile facing right, vivid royal blue body with black palette
marking, bright yellow tail fin, flat vector illustration, children's storybook style,
smooth shapes, soft flat colors, no outlines, transparent background
```
```
Ornate orange reef wrasse with flowing striped fins, side profile facing right, warm orange
body #E2703A with thin dark vertical stripes, teal-blue translucent fan fins, flat vector
illustration, children's storybook style, smooth shapes, soft flat colors, no outlines,
transparent background
```
```
Round pufferfish-like reef fish, side profile, sandy cream body with brown polka dots,
small fins, friendly eye, flat vector illustration, children's storybook style, smooth
shapes, soft flat colors, no outlines, transparent background
```
```
Tiny minimal silver sardine, side profile, pale silver-blue body, simple fins, flat vector
illustration, children's storybook style, smooth shapes, soft flat colors, no outlines,
transparent background
```

### 8.5 Orangutan — maskot vstupenky (`animal-orangutan.png`)
```
Cute baby orangutan peeking over an edge, front view, round fuzzy rust-orange body, big
amber eyes, lighter face, long arms holding the edge, curious expression, flat vector
illustration, children's storybook style, smooth rounded organic shapes, soft flat colors
with subtle two-tone shading, no outlines, matte finish, isolated on transparent background
```

---

## 9. REKVIZITY A UI PRVKY

### 9.1 Pergamenová karta (`prop-paper-card.png`, 4:5)
```
Old parchment paper sheet with softly torn irregular edges and gentle crumple creases,
warm cream color #F2E9D6 with slightly darker aged corners, subtle paper grain, empty
surface ready for text, lying flat with a soft drop shadow, flat vector illustration,
storybook prop style, soft flat colors, no outlines, isolated on transparent background
```

### 9.2 Vstupenka (`prop-ticket.png`, 3:4)
```
Vintage paper admission ticket, vertical layout, cream parchment #F2E9D6 with torn top
edge, two semicircular punch notches on the sides, a horizontal perforated dashed line
across the upper third, subtle aged texture, empty surface for text, flat vector
illustration, storybook prop style, soft flat colors, no outlines, isolated on transparent
background
```

### 9.3 Drobné rekvizity (vždy 1:1, transparent)
```
Cluster of three orange forest mushrooms with cream stems growing on a piece of bark, flat
vector illustration, children's storybook style, smooth shapes, soft flat colors, no
outlines, transparent background
```
```
Water lily pad set: three green round lily pads with a notch, one blooming pink lotus
flower, top-side view, flat vector illustration, storybook style, soft flat colors, no
outlines, transparent background
```
```
Cattail reeds bundle, several tall green stems with brown velvet seed heads, flat vector
illustration, storybook style, soft flat colors, no outlines, transparent background
```
```
Coral reef decoration set: red tube coral cluster #D4574E, orange brain coral #E08A3C,
swaying green kelp strands, small grey reef rocks, flat vector illustration, storybook
style, soft flat colors, no outlines, transparent background
```
```
Beach props set: one orange starfish, two cream seashells, small smooth pebbles, flat
vector illustration, storybook style, soft flat colors, no outlines, transparent background
```
```
Mossy river bank ledge with grass tufts and tiny pink wildflowers, side view, layered green
shapes, flat vector illustration, storybook style, soft flat colors, no outlines,
transparent background
```

---

## 10. Nasazení do webu

1. Ulož assety do `assets/img/` pod jmény z nadpisů.
2. V HTML nahraď příslušné inline `<svg class="sprite animal a-…">` za
   `<img class="sprite animal a-…" src="assets/img/….png" alt="">` — **třídy zachovej**,
   GSAP animace i CSS pozicování fungují dál beze změny.
3. Výjimky — prvky animované „uvnitř" (křídla vážky/motýla, chapadla medúzy):
   - buď nech současné SVG,
   - nebo vygeneruj **tělo a křídla zvlášť** a polož je přes sebe jako dvě `<img>` ve
     společném `<div class="sprite …">` (CSS keyframes pak rotují jen křídla).
4. Pozadí sekcí: nahraď velké scene-bg SVG za `<img>`/`background-image` s `object-fit:cover`;
   u lesní zóny zachovej poměr na výšku (2:3) kvůli plynulému scrollu.
5. PNG → SVG: vectorizer.ai nebo v Recraftu rovnou export SVG (menší soubory, ostré hrany).
6. Po výměně zkontroluj velikosti: PNG komprimuj (tinypng), ideální je WebP fallback.
