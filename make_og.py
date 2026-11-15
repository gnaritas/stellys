#!/usr/bin/env python3
"""og.png 1200x630 — Stelly's Sandwiches & Such: chalkboard-deli theme.
Chalk board, dashed border, chalk lettering, pastrami sandwich sketch, mustard accents.
Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

SLATE = (32, 38, 43); SLATE2 = (43, 51, 58)
CHALK = (244, 239, 226); CHALKDIM = (201, 194, 176)
MUSTARD = (217, 159, 44); PAPRIKA = (176, 57, 42); RYE = (138, 95, 56); PICKLE = (93, 122, 92)

def font(path_names, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in path_names:
            p = b + n
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

chalk = lambda s: font(["Chalkduster.ttf", "Bradley Hand ITC.ttf", "Trebuchet MS.ttf"], s)
cond  = lambda s: font(["Avenir Next Condensed Bold.ttf", "AvenirNextCondensed-Bold.ttf", "Futura.ttc", "HelveticaNeue-Bold.ttf"], s)
serif = lambda s: font(["Georgia.ttf", "Palatino.ttc"], s)

img = Image.new("RGB", (W, H), SLATE)
d = ImageDraw.Draw(img, "RGBA")

# board wash — slightly lighter toward the middle
for y in range(H):
    t = abs(y - H / 2) / (H / 2)
    v = int(14 * (1 - t))
    d.line([(0, y), (W, y)], fill=(SLATE[0] + v, SLATE[1] + v + 3, SLATE[2] + v + 6))

# chalk dust speckle (deterministic)
import random
rng = random.Random(502)
for _ in range(1400):
    x = rng.randint(0, W - 1); y = rng.randint(0, H - 1)
    d.point((x, y), fill=(255, 255, 255, rng.randint(5, 18)))

def dashed_rect(box, fill, dash=14, gap=9, w=3):
    x1, y1, x2, y2 = box
    edges = [((x1,y1),(x2,y1)), ((x2,y1),(x2,y2)), ((x2,y2),(x1,y2)), ((x1,y2),(x1,y1))]
    for (ax,ay),(bx,by) in edges:
        L = ((bx-ax)**2 + (by-ay)**2) ** .5
        n = int(L // (dash + gap))
        for k in range(n):
            s = k * (dash + gap); e = min(s + dash, L)
            t1, t2 = s / L, e / L
            d.line([(ax+(bx-ax)*t1, ay+(by-ay)*t1), (ax+(bx-ax)*t2, ay+(by-ay)*t2)], fill=fill, width=w)


# outer chalk frame
dashed_rect((26, 26, W-26, H-26), CHALK + (215,), dash=16, gap=11, w=3)

# left column text
d.text((72, 74), "LOGAN STREET MARKET  ·  SHELBY PARK", font=cond(24), fill=MUSTARD)

name_f = chalk(118)
d.text((66, 122), "Stelly's", font=name_f, fill=CHALK)

d.text((72, 286), "Sandwiches & Such", font=chalk(52), fill=CHALK)

tag_f = serif(30)
TAGC = (226, 220, 203)
d.text((72, 372), "House-made pastrami. Fun sandwiches.", font=tag_f, fill=TAGC)
d.text((72, 412), "Positive vibes.", font=tag_f, fill=TAGC)

# hours/price board rows (chalk dashed separators)
row_f = cond(27); rowv_f = chalk(27)
rows = [("TUE–SUN", "11:00 a.m. – 3:30 p.m."),
        ("MONDAY", "Closed"),
        ("SANDWICHES", "$14 – $16")]
y0 = 466
for idx, (lab, val) in enumerate(rows):
    d.text((72, y0), lab, font=row_f, fill=MUSTARD)
    d.text((320, y0 - 3), val, font=rowv_f, fill=CHALK)
    if idx < len(rows) - 1:
        d.line([(72, y0 + 36), (700, y0 + 36)], fill=(244, 239, 226, 46), width=1)
    y0 += 42

# chalk pastrami sandwich sketch, right side — aligned slices, contained folds
cx, cy = 950, 285
SLOPE = -0.09  # consistent tilt for every element
def yslant(x, base): return base + SLOPE * (x - cx)
# top slice
d.polygon([(cx-165, yslant(cx-165, cy-118)), (cx+165, yslant(cx+165, cy-118)),
           (cx+165, yslant(cx+165, cy-72)),  (cx-165, yslant(cx-165, cy-72))],
          outline=CHALK + (210,), width=4)
# meat folds: three gentle stacked waves, strictly inside the sandwich width
for i, base in enumerate([cy-46, cy-18, cy+10]):
    pts = []
    for x in range(-140, 141, 28):
        pts.append((cx + x, yslant(cx + x, base) + (7 if (x // 28) % 2 else -7)))
    d.line(pts, fill=PAPRIKA + (235,), width=4)
# bottom slice
d.polygon([(cx-165, yslant(cx-165, cy+34)), (cx+165, yslant(cx+165, cy+34)),
           (cx+165, yslant(cx+165, cy+80)),  (cx-165, yslant(cx-165, cy+80))],
          outline=CHALK + (210,), width=4)

# mustard corner stamp — box sized to the measured text
cta_f = cond(24)
cta_txt = "ORDER AHEAD · PICK UP"
tb = d.textbbox((0, 0), cta_txt, font=cta_f)
tw, th = tb[2] - tb[0], tb[3] - tb[1]
bx2, by2 = 1150, 556
bx1, by1 = bx2 - tw - 40, by2 - th - 26
d.rectangle([bx1, by1, bx2, by2], outline=MUSTARD, width=3)
d.text((bx1 + 20 - tb[0], by1 + 13 - tb[1]), cta_txt, font=cta_f, fill=MUSTARD)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
