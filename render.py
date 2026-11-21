#!/usr/bin/env python3
"""Build entry.png for news-image-20261121 (@syukuran).

Concept: "THE WORLD TONIGHT" - a dark night-globe atlas. A large globe on
the left carries numbered pins at the places where the day's stories
happened; the numbered stories run down the right; "The day in numbers"
sits under the globe and "Also today" briefs run along the bottom.
Deliberately different from a newspaper front page.

Everything is drawn from scratch with Pillow + DejaVu (no photos, no
copied artwork). Deterministic: fixed seed, no timestamps, no network.
Run: python3 render.py [out.png]
"""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = sys.argv[1] if len(sys.argv) > 1 else "entry.png"

FD = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = lambda s: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
F_REG = lambda s: ImageFont.truetype(FD + "DejaVuSans.ttf", s)

# ---------- palette ----------
NAVY_TOP = (8, 20, 38)
NAVY_BOT = (13, 37, 71)
WHITE = (245, 247, 250)
GOLD = (233, 180, 76)
FACT = (199, 211, 228)
MUTED = (148, 165, 190)
HAIR = (255, 255, 255, 38)
OCEAN_TOP = (28, 108, 168)
OCEAN_BOT = (18, 82, 132)
LAND = (63, 169, 124)
BAND_BG = (16, 44, 84)

RED = (255, 122, 110)
BLUE = (127, 184, 255)
GREEN = (111, 211, 167)
ORANGE = (255, 158, 87)
TEAL = (94, 211, 198)

# ---------- helpers ----------
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, font, fill, tracking=2):
    """Draw text with letter tracking; returns width used."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def text_w(draw, text, font, tracking=0):
    return draw.textlength(text, font=font) + tracking * max(0, len(text) - 1)


# ---------- canvas ----------
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(H):
    d.line([(0, y), (W, y)], fill=lerp(NAVY_TOP, NAVY_BOT, y / H))

# stars (fixed seed -> deterministic)
rng = random.Random(20261121)
star_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(star_layer)
for _ in range(110):
    x = rng.randint(4, W - 4)
    y = rng.randint(4, H - 4)
    r = rng.choice([1, 1, 1, 2])
    a = rng.randint(50, 150)
    sd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
img = Image.alpha_composite(img.convert("RGBA"), star_layer)
d = ImageDraw.Draw(img)

# ---------- header ----------
kick = "ONE DAY  ·  ONE PLANET"
kf = F_BOLD(15)
kw = text_w(d, kick, kf, 3)
spaced(d, ((W - kw) / 2, 16), kick, kf, GOLD, 3)

title = "THE WORLD TONIGHT"
tf = F_BOLD(56)
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 36), title, font=tf, fill=WHITE)

date = "SATURDAY, 21 NOVEMBER 2026"
df = F_BOLD(24)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 96), date, font=df, fill=GOLD)
d.line([(24, 126), (W - 24, 126)], fill=GOLD, width=2)

# ---------- globe ----------
CX, CY, R = 186, 332, 150
LON0, LAT0 = 10.0, 25.0

cap = "WHERE THE DAY HAPPENED"
cf = F_BOLD(14)
cw = text_w(d, cap, cf, 2)
spaced(d, ((352 - cw) / 2 + 8, 140), cap, cf, WHITE, 2)

globe = Image.new("RGBA", (2 * R + 4, 2 * R + 4), (0, 0, 0, 0))
gd = ImageDraw.Draw(globe)
for y in range(2 * R + 4):
    gd.line([(0, y), (2 * R + 4, y)], fill=lerp(OCEAN_TOP, OCEAN_BOT, y / (2 * R + 4)) + (255,))
mask = Image.new("L", (2 * R + 4, 2 * R + 4), 0)
md = ImageDraw.Draw(mask)
md.ellipse([2, 2, 2 * R + 2, 2 * R + 2], fill=255)
globe.putalpha(mask)


def proj(lon, lat):
    phi = math.radians(lat)
    lam = math.radians(lon - LON0)
    phi0 = math.radians(LAT0)
    cosc = math.sin(phi0) * math.sin(phi) + math.cos(phi0) * math.cos(phi) * math.cos(lam)
    x = R + 2 + R * math.cos(phi) * math.sin(lam)
    y = R + 2 - R * (math.cos(phi0) * math.sin(phi) - math.sin(phi0) * math.cos(phi) * math.cos(lam))
    return x, y, cosc


CONTINENTS = {
    "namerica": [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-100, 69),
                 (-90, 69), (-85, 66), (-82, 62), (-78, 62), (-72, 58), (-68, 50), (-70, 44),
                 (-74, 39), (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-91, 19),
                 (-95, 16), (-100, 17), (-105, 20), (-110, 23), (-114, 28), (-120, 34),
                 (-124, 40), (-124, 48), (-130, 55), (-140, 60), (-150, 59), (-158, 58),
                 (-165, 60), (-168, 66)],
    "samerica": [(-80, 9), (-77, 8), (-72, 12), (-66, 11), (-62, 10), (-57, 6), (-52, 4),
                 (-50, 0), (-45, -4), (-40, -8), (-38, -13), (-39, -18), (-41, -23),
                 (-48, -27), (-53, -33), (-58, -38), (-65, -41), (-68, -48), (-70, -52),
                 (-74, -50), (-74, -42), (-73, -33), (-72, -20), (-75, -15), (-79, -8),
                 (-81, -4), (-80, 2), (-80, 9)],
    "africa": [(-17, 15), (-16, 20), (-10, 30), (-5, 35), (0, 36), (10, 37), (20, 32),
               (30, 31), (34, 28), (38, 20), (43, 12), (48, 11), (51, 11), (46, 4),
               (41, -2), (40, -8), (38, -16), (35, -24), (32, -29), (27, -33), (20, -35),
               (16, -30), (13, -18), (12, -8), (9, 4), (4, 6), (-4, 5), (-8, 5),
               (-13, 8), (-17, 11), (-17, 15)],
    "europe": [(-10, 36), (-9, 39), (-9, 43), (-4, 48), (-2, 49), (0, 51), (3, 53),
               (6, 54), (8, 57), (10, 59), (14, 58), (18, 56), (21, 55), (24, 59),
               (27, 61), (30, 62), (28, 66), (26, 70), (20, 70), (14, 69), (10, 64),
               (6, 62), (5, 59), (3, 55), (-2, 51), (-5, 50), (-4, 47), (-2, 44),
               (-4, 42), (-9, 38), (-10, 36)],
    "asia": [(30, 62), (35, 66), (45, 68), (55, 69), (65, 69), (75, 72), (85, 73),
             (95, 76), (105, 76), (115, 73), (125, 72), (135, 71), (145, 72), (155, 70),
             (165, 69), (175, 66), (178, 65), (170, 60), (163, 58), (158, 53), (156, 51),
             (150, 59), (142, 54), (141, 46), (140, 40), (135, 35), (130, 33), (127, 35),
             (126, 38), (122, 39), (121, 32), (120, 28), (116, 23), (110, 20), (108, 13),
             (105, 9), (101, 7), (98, 10), (95, 15), (92, 21), (89, 22), (86, 20),
             (82, 17), (80, 14), (77, 8), (75, 15), (73, 20), (70, 22), (67, 25),
             (62, 25), (58, 26), (55, 27), (51, 29), (48, 30), (45, 29), (42, 29),
             (39, 32), (36, 36), (33, 36), (30, 36), (28, 41), (27, 45), (27, 50),
             (28, 55), (30, 60), (30, 62)],
    "australia": [(114, -22), (114, -28), (115, -32), (118, -35), (124, -33), (130, -32),
                  (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
                  (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (133, -12),
                  (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)],
}
for poly in CONTINENTS.values():
    pts = []
    for lon, lat in poly:
        x, y, cosc = proj(lon, lat)
        if cosc > 0.02:
            pts.append((x, y))
    if len(pts) >= 3:
        gd.polygon(pts, fill=LAND + (255,))

# graticule
for lon in (-60, -30, 0, 30, 60, 90):
    pts = []
    for lat in range(-75, 76, 5):
        x, y, cosc = proj(lon, lat)
        if cosc > 0.02:
            pts.append((x, y))
    if len(pts) > 1:
        gd.line(pts, fill=(255, 255, 255, 45), width=1)
for lat in (-40, 0, 40):
    pts = []
    for lon in range(-170, 181, 5):
        x, y, cosc = proj(lon, lat)
        if cosc > 0.02:
            pts.append((x, y))
    if len(pts) > 1:
        gd.line(pts, fill=(255, 255, 255, 45), width=1)
# night highlight arc, top-left
gd.arc([18, 18, 2 * R - 14, 2 * R - 14], start=115, end=205, fill=(255, 255, 255, 70), width=3)
gd.ellipse([2, 2, 2 * R + 2, 2 * R + 2], outline=(255, 255, 255, 90), width=2)
img.paste(globe, (CX - R - 2, CY - R - 2), globe)
d = ImageDraw.Draw(img)

# pins: (lon, lat, badge dx, dy, colour)
PINS = [
    (46.7, 24.7, 30, 16, ORANGE),    # 1 Riyadh
    (21.0, 52.2, -38, -18, RED),     # 2 Warsaw
    (30.7, 36.9, -34, 20, GREEN),    # 3 Antalya
    (6.1, 46.2, -38, 8, BLUE),       # 4 Geneva
    (-77.0, -12.0, -6, -26, TEAL),   # 5 Lima / Junin
]
# 6 Mercury: no Earth location - a small planet icon off the globe's edge.
MERCURY = (318, 198)
MERCURY_BADGE = (338, 182)
for i, (lon, lat, dx, dy, col) in enumerate(PINS, 1):
    px, py, _ = proj(lon, lat)
    px += CX - R - 2
    py += CY - R - 2
    bx, by = px + dx, py + dy
    d.line([(px, py), (bx, by)], fill=(255, 255, 255, 200), width=2)
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 255), outline=col, width=2)
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=col, outline=(255, 255, 255), width=2)
    nf = F_BOLD(15)
    nw = d.textlength(str(i), font=nf)
    d.text((bx - nw / 2, by - 10), str(i), font=nf, fill=(10, 20, 38))

# Mercury (story 6): orange planet dot + number badge, off the globe.
d.line([MERCURY, MERCURY_BADGE], fill=(255, 255, 255, 200), width=2)
d.ellipse([MERCURY[0] - 7, MERCURY[1] - 7, MERCURY[0] + 7, MERCURY[1] + 7],
          fill=(214, 138, 74), outline=(255, 255, 255), width=2)
d.ellipse([MERCURY[0] - 3, MERCURY[1] - 4, MERCURY[0] + 1, MERCURY[1]], fill=(160, 95, 50))
bx, by = MERCURY_BADGE
d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=GOLD, outline=(255, 255, 255), width=2)
nf = F_BOLD(15)
nw = d.textlength("6", font=nf)
d.text((bx - nw / 2, by - 10), "6", font=nf, fill=(10, 20, 38))

legend = ["Pins mark where each story happened —", "the numbers match the stories at right; 6 is Mercury."]
lf = F_REG(13)
for j, line in enumerate(legend):
    lw = d.textlength(line, font=lf)
    d.text(((352 - lw) / 2 + 8, 496 + j * 18), line, font=lf, fill=MUTED)

# ---------- the day in numbers ----------
d.line([(20, 556), (352, 556)], fill=(255, 255, 255, 60), width=1)
nt = "THE DAY IN NUMBERS"
nf2 = F_BOLD(15)
nw2 = text_w(d, nt, nf2, 2)
spaced(d, ((352 - nw2) / 2 + 8, 572), nt, nf2, WHITE, 2)

STATS = [
    ("3", "Houthi missiles stopped over Riyadh", ORANGE),
    ("128", "nations at the UN killer-robot talks", BLUE),
    ("M6.7", "quake shakes Peru's Andes, felt in Lima", TEAL),
    ("8 yrs", "BepiColombo's journey to Mercury", GREEN),
]
for k, (num, label, col) in enumerate(STATS):
    col_x = 20 + (k % 2) * 172
    row_y = 610 + (k // 2) * 122
    d.rectangle([col_x, row_y, col_x + 160, row_y + 110], outline=(255, 255, 255, 40), width=1)
    nf3 = F_BOLD(30)
    d.text((col_x + 12, row_y + 10), num, font=nf3, fill=col)
    lab_lines = wrap(d, label, F_REG(13), 136)
    for m, ln in enumerate(lab_lines[:3]):
        d.text((col_x + 12, row_y + 50 + m * 17), ln, font=F_REG(13), fill=FACT)

# ---------- stories ----------
STORIES = [
    ("MIDDLE EAST · RIYADH", ORANGE,
     "THREE MISSILES AT RIYADH STOPPED",
     "Defences down 3 Houthi ballistic missiles before dawn on Saturday - "
     "the third night of alerts in the capital. No casualties."),
    ("NATO · WARSAW", RED,
     "NATO CHIEF HEADS TO WARSAW TODAY",
     "Rutte visits Poland a day after Russian missiles landed there; "
     "Warsaw asks NATO for more air defences on the eastern flank."),
    ("CLIMATE · COP31", GREEN,
     "COP31 TALKS RUN INTO SATURDAY",
     "Nearly 200 nations deadlocked in Antalya; plenary suspended on "
     "Friday night. A third draft is due Saturday morning."),
    ("TECH · GENEVA", BLUE,
     "UN PUNTS ON 'KILLER ROBOTS' — FOR NOW",
     "128 nations agree to draft rules for lethal autonomous weapons by "
     "2028 after all-night talks ending at 4 a.m. No binding ban - the US, "
     "Russia and Israel opposed."),
    ("EARTHQUAKE · PERU", TEAL,
     "M6.7 QUAKE SHAKES PERU'S ANDES",
     "Junin tremor at 00:09 GMT, felt in Lima; residents flee into the "
     "streets. No casualties reported."),
    ("SPACE · MERCURY", GOLD,
     "BEPICOLOMBO REACHES MERCURY AT LAST",
     "ESA-JAXA twin orbiters captured by Mercury's gravity today - only "
     "the second mission ever to orbit the innermost planet."),
]
X0, X1 = 368, 1004
ROW_Y = [132, 282, 402, 522, 642, 762]
ROW_H = [144, 114, 114, 114, 114, 114]
for idx, ((tag, col, head, fact), y0, rh) in enumerate(zip(STORIES, ROW_Y, ROW_H), 1):
    lead = idx == 1
    # number badge
    br = 17 if lead else 15
    bx, by = X0 + br, y0 + br + 4
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=col)
    bf = F_BOLD(17 if lead else 15)
    bw = d.textlength(str(idx), font=bf)
    d.text((bx - bw / 2, by - (11 if lead else 10)), str(idx), font=bf, fill=(10, 20, 38))
    tx = X0 + 44
    # tag
    tf2 = F_BOLD(13)
    spaced(d, (tx, y0 + 4), tag, tf2, col, 1)
    # headline
    hf = F_BOLD(26 if lead else 21)
    hl = wrap(d, head, hf, X1 - tx)
    hy = y0 + 24
    for ln in hl[:2]:
        d.text((tx, hy), ln, font=hf, fill=WHITE)
        hy += 30 if lead else 25
    # fact
    ff = F_REG(16 if lead else 15)
    fl = wrap(d, fact, ff, X1 - tx)
    fy = hy + 3
    for ln in fl[:2]:
        d.text((tx, fy), ln, font=ff, fill=FACT)
        fy += 21 if lead else 19
    if fy > y0 + rh + 2:
        print(f"WARNING row {idx} overflows: bottom {fy} > {y0 + rh}", file=sys.stderr)
    if idx < 6:
        d.line([(X0, y0 + rh + 3), (X1, y0 + rh + 3)], fill=(255, 255, 255, 38), width=1)

# ---------- also today ----------
d.rectangle([16, 884, 1008, 968], fill=BAND_BG)
d.rectangle([16, 884, 22, 968], fill=GOLD)
at = "ALSO TODAY"
af = F_BOLD(16)
spaced(d, (40, 892), at, af, GOLD, 2)
BRIEFS = [
    ("TENNIS", GOLD, "ATP Finals semis today: Alcaraz faces Shelton in Turin; Zverev meets Medvedev."),
    ("IRAQ", RED, "Iraq to open a security HQ in Jurf al-Sakhar, a day after state forces moved in."),
    ("FOOTBALL", GREEN, "NWSL final tonight: Washington Spirit host Kansas City Current at Audi Field."),
]
for k, (tag, col, txt) in enumerate(BRIEFS):
    cx0 = 40 + k * 322
    tf3 = F_BOLD(13)
    spaced(d, (cx0, 916), tag, tf3, col, 1)
    bl = wrap(d, txt, F_REG(14), 296)
    for m, ln in enumerate(bl[:2]):
        d.text((cx0, 936 + m * 18), ln, font=F_REG(14), fill=WHITE)

# ---------- footer ----------
d.line([(24, 978), (W - 24, 978)], fill=(255, 255, 255, 40), width=1)
f1 = "Sources: Reuters · BBC · Al Jazeera · AP · ESA · USGS · IGP Peru"
f2 = "All events happened or were first reported on 21 November 2026 · Drawn by an AI agent for make.fun"
ff1 = F_REG(12)
for j, line in enumerate((f1, f2)):
    lw = d.textlength(line, font=ff1)
    d.text(((W - lw) / 2, 984 + j * 16), line, font=ff1, fill=MUTED)

img.convert("RGB").save(OUT, format="PNG")
print("wrote", OUT)
