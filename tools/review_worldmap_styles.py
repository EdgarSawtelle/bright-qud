"""World map style sheet: ten cartoon directions on the game's real layout, with rounded borders. Each biome is filled by big motifs
(trees, peaks, mushrooms...) drawn into the tiles themselves, clipped by the biome's rounded shape. Local output only.

Usage: .venv/bin/python tools/review_worldmap_styles.py <map today png> <vanilla png> <out dir>
"""
import colorsys, os, random, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402
import map_render as MR  # noqa: E402
from mockup import font  # noqa: E402
from review_worldmap import biome, rgb  # noqa: E402

CW, CH = 16, 24
K = 4                                                       # motifs are drawn large and reduced, for clean curves
GENERIC = re.compile(r"^Terrain(Jungle|DeepJungle|Mountains|Hills|Saltdunes|DesertCanyon|River|Mountain|Flowerfields|Saltmarsh|Watervine|"
                     r"BananaGrove|Ruins|BaroqueRuins|MoonStair|Fungal|PalladiumReef|LakeHinnom|OpalDuskwaters)")
# ground, main, shade, light, accent
C = {"jungle": ("2e6a3a", "3f9a4a", "2a7238", "6cc45a", "2a4a2a"), "deep": ("183f30", "22644a", "164a3a", "3a8a5a", "102a24"),
     "hills": ("b89a5c", "c8ae6c", "a08650", "e0cc8c", "8a7040"), "mount": ("6c7078", "8a8e98", "5a5e6a", "f0f0e8", "3e424c"),
     "dunes": ("e4cf94", "ecdba8", "c8b078", "f6eccc", "b89a60"), "canyon": ("e8dccc", "c0523a", "8a3428", "e88a60", "a4503c"),
     "marsh": ("5e8c52", "4a7a44", "3e6438", "8ab464", "c8d890"), "flowers": ("86b264", "6c9a50", "54803e", "f0c850", "e87890"),
     "grove": ("7a9030", "a8b82c", "6a7c20", "f0d840", "4a5a18"), "ruins": ("5a6a4c", "c8d4d0", "808c88", "f0f4f0", "4a7a44"),
     "moon": ("3a2f6a", "8a70d8", "5a48a8", "d8c8ff", "2a2250"), "fungal": ("2e1a3c", "e04ca8", "8a2a70", "f8d0ec", "40d0d8"),
     "reef": ("14646a", "e0604a", "a03a30", "f8a888", "2a9aa0"), "water": ("2f8ac0", "2f8ac0", "2670a0", "6cc0e4", "2670a0")}
ORDER = list(C)


def motif(k, ink, width, v):
    """(canvas size in cells, RGBA) for a biome, variant v. Big shapes, a clear silhouette."""
    pal = {n: tuple(int(x) for x in rgb(c)) for n, c in zip(("g", "m", "s", "l", "a"), C[k])}
    m, s, l, a = pal["m"], pal["s"], pal["l"], pal["a"]
    w, h = CW * K * 2, CH * K * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    o = {"outline": ink, "width": width} if ink else {}

    def blob(x, y, rx, ry, col, hi=None):
        d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=col, **o)
        if hi:
            d.ellipse((x - rx * 0.55, y - ry * 0.7, x + rx * 0.05, y - ry * 0.1), fill=hi)

    def tri(x, y, b, t, col, side, cap=None):
        d.polygon([(x - b, y), (x, y - t), (x + b, y)], fill=col, **o)
        d.polygon([(x, y - t), (x + b, y), (x + b * 0.15, y)], fill=side)
        if cap:
            d.polygon([(x, y - t), (x - b * 0.3, y - t * 0.68), (x - b * 0.1, y - t * 0.74), (x + b * 0.05, y - t * 0.63), (x + b * 0.3, y - t * 0.7)], fill=cap)
    if k in ("jungle", "deep", "grove"):
        for x, y, r in ((w * .28, h * .4, 34), (w * .68, h * .36, 38), (w * .48, h * .66, 40)):
            d.rectangle((x - 5, y, x + 5, y + r * 1.3), fill=(90, 60, 40))
            blob(x, y, r + (v % 2) * 5, r * .9, m, l)
        if k == "grove":
            d.ellipse((w * .4, h * .55, w * .5, h * .72), fill=l, **o)
    elif k == "mount":
        tri(w * .3, h * .95, 58, 120 + v * 8, m, s, l)
        tri(w * .68, h * .98, 66, 160 + v * 6, m, s, l)
    elif k == "hills":
        d.pieslice((w * .05, h * .35, w * .62, h * 1.2), 180, 360, fill=m, **o)
        d.pieslice((w * .42, h * .5, w * .98, h * 1.25), 180, 360, fill=l, **o)
    elif k == "dunes":
        for y in (h * .3, h * .6, h * .88):
            d.arc((w * .08, y - 20, w * .92, y + 40), 190, 350, fill=s, width=max(3, width))
    elif k == "canyon":
        d.polygon([(w * .14, h * .9), (w * .24, h * .4), (w * .78, h * .4), (w * .9, h * .9)], fill=m, **o)
        d.polygon([(w * .24, h * .4), (w * .78, h * .4), (w * .72, h * .5), (w * .3, h * .5)], fill=l)
        d.rectangle((w * .2, h * .66, w * .84, h * .72), fill=s)
    elif k == "marsh":
        for x in (.2, .4, .6, .8):
            d.line((w * x, h * .9, w * (x + .05), h * .3), fill=s, width=8)
            d.ellipse((w * (x + .02), h * .24, w * (x + .09), h * .42), fill=(120, 80, 50), **o)
    elif k == "flowers":
        for x, y in ((.3, .35), (.7, .5), (.42, .78)):
            for ang in range(5):
                import math
                cx, cy = w * x + 22 * math.cos(ang * 1.256), h * y + 22 * math.sin(ang * 1.256)
                d.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill=a if v % 2 else l, **o)
            d.ellipse((w * x - 11, h * y - 11, w * x + 11, h * y + 11), fill=(250, 240, 180))
    elif k == "ruins":
        d.rectangle((w * .24, h * .22, w * .46, h * .92), fill=m, **o)
        d.polygon([(w * .24, h * .22), (w * .34, h * .08), (w * .46, h * .22)], fill=l, **o)
        d.rectangle((w * .6, h * .5, w * .8, h * .92), fill=s, **o)
        d.arc((w * .15, h * .3, w * .55, h * .9), 200, 340, fill=a, width=9)
    elif k == "moon":
        for x, t in ((.3, .7), (.52, .9), (.74, .6)):
            d.polygon([(w * x, h * (.95 - t)), (w * (x + .1), h * .6), (w * x, h * .95), (w * (x - .1), h * .6)], fill=m, **o)
            d.polygon([(w * x, h * (.95 - t)), (w * (x - .1), h * .6), (w * x, h * .95)], fill=l)
    elif k == "fungal":
        caps = [(224, 76, 168), (64, 208, 216), (240, 200, 64), (120, 96, 240), (240, 96, 64)]
        for i, (x, y, r) in enumerate(((.3, .45, 42), (.72, .36, 50), (.52, .78, 36))):
            cap = caps[(v + i * 2) % 5]
            d.rectangle((w * x - 11, h * y, w * x + 11, h * y + r * 1.5), fill=(240, 230, 210), **o)
            d.pieslice((w * x - r, h * y - r, w * x + r, h * y + r), 180, 360, fill=cap, **o)
            for sx in (-.5, 0, .5):
                d.ellipse((w * x + r * sx - 7, h * y - r * .55 - 7, w * x + r * sx + 7, h * y - r * .55 + 7), fill=(250, 245, 230))
    elif k == "reef":
        for x in (.3, .68):
            d.line((w * x, h * .9, w * x, h * .4), fill=m, width=15)
            d.line((w * x, h * .6, w * (x + .15), h * .34), fill=m, width=11)
            d.line((w * x, h * .7, w * (x - .15), h * .46), fill=m, width=11)
    return im


def mod(col, sat, val, hue=0.0, tint=None):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in col[:3]))
    r, g, b = colorsys.hsv_to_rgb((h + hue) % 1, min(1, s * sat), min(1, v * val))
    out = np.array((r, g, b)) * 255
    return tuple(int(c) for c in (out if tint is None else out * 0.6 + np.array(tint) * 0.4))


# name: ink, width, scale in cells, saturation, value, border width, ground mode, border colour
STYLES = [("1 Bold cartoon", (24, 28, 40), 7, 2, 1.1, 1.0, 3, "flat", (24, 28, 40)),
          ("2 Soft storybook", None, 0, 2, 0.8, 1.08, 0, "flat", None),
          ("3 Giant motifs", (24, 28, 40), 8, 3, 1.15, 1.0, 3, "flat", (24, 28, 40)),
          ("4 Tiny dense motifs", (24, 28, 40), 7, 1, 1.05, 1.0, 2, "flat", (24, 28, 40)),
          ("5 Parchment and ink", (70, 44, 30), 7, 2, 0.35, 1.15, 2, "parchment", (70, 44, 30)),
          ("6 Neon night", (16, 18, 34), 6, 2, 1.3, 0.75, 2, "night", (150, 240, 220)),
          ("7 Stained glass", (20, 20, 26), 10, 2, 1.25, 1.0, 5, "flat", (20, 20, 26)),
          ("8 Classic Qud teal", (15, 59, 58), 6, 2, 1.1, 1.05, 2, "teal", (120, 200, 190)),
          ("9 Sticker", (250, 250, 240), 8, 2, 1.2, 1.05, 3, "flat", (250, 250, 240)),
          ("10 Sunset", (50, 24, 44), 7, 2, 1.0, 0.95, 3, "sunset", (50, 24, 44))]


def render(style, big, cells, water, sites, now, van):
    name, ink, width, scale, sat, val, bw, mode, bcol = style
    W, H = 80 * CW, 25 * CH
    bg = np.array([0x0f, 0x3b, 0x3a], dtype=float)
    strength = [np.asarray(Image.fromarray(((big == i) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(7.5)), dtype=float) for i in range(len(ORDER))]
    which = np.stack(strength).argmax(axis=0)
    tint = {"sunset": (240, 120, 90), "night": (40, 40, 110), "parchment": (225, 200, 150), "teal": (15, 80, 80)}.get(mode)
    img = Image.new("RGB", (W, H))
    arr = np.zeros((H, W, 3))
    for i, k in enumerate(ORDER):
        arr[which == i] = mod(rgb(C[k][0]), sat, val, tint=tint)
    img = Image.fromarray(arr.astype("uint8"))
    r = random.Random(3)
    for i, k in enumerate(ORDER):
        if k == "water":
            continue
        mask = Image.fromarray(((which == i) * 255).astype("uint8"))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        mots = []
        for v in range(5):
            m = motif(k, ink, width, v)
            px = np.asarray(m, dtype=float).copy()
            for row in range(0, px.shape[0], 1):
                pass
            mm = np.array(m)
            uniq = {}
            a = mm[..., 3] > 0
            flat = mm[a][:, :3]
            rec = np.array([mod(tuple(c), sat, val, tint=tint) for c in np.unique(flat, axis=0)]) if len(flat) else None
            if rec is not None:
                keys = np.unique(flat, axis=0)
                lut = {tuple(c): rec[j] for j, c in enumerate(keys)}
                mm[a, :3] = np.array([lut[tuple(c)] for c in flat])
            mots.append(Image.fromarray(mm).resize((CW * scale, CH * scale), Image.LANCZOS))
        sy, sx = CH * scale * 2 // 3, CW * scale
        for row, y in enumerate(range(-CH * scale, H + CH, sy)):
            for x in range(-CW * scale + (row % 2) * sx // 2, W + CW, sx):
                cx, cy = min(W - 1, max(0, x + sx // 2)), min(H - 1, max(0, y + sy))
                if which[cy, cx] == i or which[min(H - 1, cy + 6), cx] == i:
                    m = mots[r.randrange(5)]
                    layer.alpha_composite(m, (max(0, x), max(0, y))) if x >= 0 and y >= 0 else layer.paste(m, (x, y), m)
        img.paste(layer, (0, 0), Image.composite(layer.getchannel("A"), Image.new("L", (W, H), 0), mask))
    arr = np.array(img, dtype=float)
    solid = np.zeros((H, W), bool)
    for (x, y) in water:
        tile = van[y * 48:(y + 1) * 48:2, x * 32:(x + 1) * 32:2]
        sol = np.abs(tile - bg).sum(axis=2) > 40
        col = np.array(mod(rgb("2f8ac0"), sat, val, tint=tint), dtype=float)
        v = arr[y * CH:(y + 1) * CH, x * CW:(x + 1) * CW]
        v[sol] = col
        v[sol & (tile.sum(axis=2) > 330)] = np.clip(col * 1.3, 0, 255)
        solid[y * CH:(y + 1) * CH, x * CW:(x + 1) * CW] = sol
    if bcol is not None and bw:
        e = (which != np.roll(which, 1, 0)) | (which != np.roll(which, 1, 1))
        e = np.asarray(Image.fromarray((e * 255).astype("uint8")).filter(ImageFilter.MaxFilter(bw | 1)), dtype=bool)
        arr[e] = bcol
        rim = (np.roll(solid, 1, 0) | np.roll(solid, -1, 0) | np.roll(solid, 1, 1) | np.roll(solid, -1, 1)) & ~solid
        arr[rim] = bcol
    for x, y in sorted(sites, key=lambda p: p[1]):
        sp = now[y * 48:(y + 1) * 48, x * 32:(x + 1) * 32]
        mask = np.abs(van[y * 48:(y + 1) * 48, x * 32:(x + 1) * 32] - bg).sum(axis=2) > 40
        grow = mask | np.roll(mask, 1, 0) | np.roll(mask, -1, 0) | np.roll(mask, 1, 1) | np.roll(mask, -1, 1)
        px, py = x * CW - 8, y * CH - 12
        for j in range(48):
            for i in range(32):
                ax, ay = px + i, py + j
                if 0 <= ax < W and 0 <= ay < H and grow[j, i]:
                    arr[ay, ax] = sp[j, i] if mask[j, i] else (24, 28, 40)
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))


def main():
    cells = MR.top_objects(MR.load("QudWorldMap"))
    now = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=float)
    van = np.asarray(Image.open(sys.argv[2]).convert("RGB"), dtype=float)
    grid = np.full((25, 80), -1)
    water, sites = set(), []
    for (x, y), n in cells.items():
        name = n or ""
        grid[y, x] = ORDER.index(biome(name)) if biome(name) else -1
        if re.search(r"River|Stream|Duskwaters|LakeHinnom|PalladiumReef", name):
            water.add((x, y))
            if biome(name) != "reef":
                grid[y, x] = -1
        if name and not GENERIC.match(name):
            sites.append((x, y))
    for _ in range(6):
        for y in range(25):
            for x in range(80):
                if grid[y, x] < 0:
                    near = [grid[y + b, x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < 80 and 0 <= y + b < 25 and grid[y + b, x + a] >= 0]
                    if near:
                        grid[y, x] = near[0]
    grid[grid < 0] = ORDER.index("dunes")
    big = np.kron(grid, np.ones((CH, CW), dtype=int))
    out = sys.argv[3]
    sheet = Image.new("RGB", (2 * 960 + 30, 5 * (450 + 34) + 10), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for n, st in enumerate(STYLES):
        im = render(st, big, cells, water, sites, now, van)
        im.resize((1920, 900), Image.NEAREST).save(f"{out}/map_{n + 1:02d}.png")
        x, y = 10 + (n % 2) * 970, 6 + (n // 2) * 484
        d.text((x, y), st[0], font=font(20), fill=(235, 205, 140))
        sheet.paste(im.resize((960, 450), Image.LANCZOS), (x, y + 30))
    sheet.save(f"{out}/sheet.png")


if __name__ == "__main__":
    main()
