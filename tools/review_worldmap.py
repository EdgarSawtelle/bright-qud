"""World map proposal: every pixel looks up its biome at a position bent by smooth noise, so biomes interlace with organic
edges instead of meeting along cell squares. Colours come from the zone decisions. Water keeps the game's curved shapes (taken
from the original tile pixels), sites keep their icons. Everything is computed per cell, so it can run in the game.
Local output only.

Usage: .venv/bin/python -I tools/review_worldmap.py <vanilla map png> <out.png>
"""
import os, random, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import map_render as MR  # noqa: E402

CW, CH = 16, 24
# biome: (ground, dark detail, light detail, kind of mark, density)
B = {"jungle": ("2f4530", "22352a", "3f5a38", "canopy", 0.9), "deep": ("1f3128", "16251f", "2b4232", "canopy", 1.0),
     "hills": ("7d7460", "625a4a", "948a72", "hump", 0.5), "mount": ("8a8d84", "5a5e5a", "bdbcb0", "peak", 0.8),
     "dunes": ("a5997f", "8f8369", "b8ad95", "ripple", 0.7), "canyon": ("d0c6b8", "a4503c", "e0d8cc", "mesa", 0.45),
     "marsh": ("4e5040", "3c4034", "6a7050", "reed", 0.6), "flowers": ("66705a", "565e4c", "a89070", "fleck", 1.0),
     "grove": ("3a4026", "2c3120", "6a6a30", "canopy", 0.7), "ruins": ("5e5b48", "47453a", "a8aea8", "spire", 0.45),
     "moon": ("2b2a3c", "1f1e2e", "9c8fc4", "crystal", 0.7), "fungal": ("2c2820", "1f1c16", "b060a8", "cap", 0.7),
     "reef": ("1d3536", "152828", "c8503a", "coral", 0.5), "water": ("3a6f8c", "2c5a74", "5a93ae", "none", 0)}


def biome(name):
    n = name or ""
    for k, v in (("Saltdunes", "dunes"), ("DeepJungle", "deep"), ("BaroqueRuins", "deep"), ("Jungle", "jungle"), ("Golgotha", "jungle"),
                 ("Mountain", "mount"), ("Hills", "hills"), ("DesertCanyon", "canyon"), ("RustWell", "canyon"), ("RedRock", "canyon"),
                 ("Saltmarsh", "marsh"), ("Watervine", "marsh"), ("Joppa", "marsh"), ("Flowerfields", "flowers"), ("BananaGrove", "grove"),
                 ("Ruins", "ruins"), ("MoonStair", "moon"), ("Fungal", "fungal"), ("PalladiumReef", "reef"), ("Hinnom", "reef")):
        if k in n:
            return v
    return None


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def noise(w, h, step, seed):
    r = np.random.RandomState(seed).rand(h // step + 3, w // step + 3)
    im = Image.fromarray((r * 255).astype("uint8")).resize((w + 2 * step, h + 2 * step), Image.BICUBIC)
    return np.asarray(im, dtype=float)[:h, :w] / 255 - 0.5


def mark(canvas, kind, x, y, a, b, c, r):
    """Small marks: never a repeating tile; size, place and shade all vary."""
    def p(px, py, col):
        if 0 <= px < canvas.shape[1] and 0 <= py < canvas.shape[0]:
            canvas[py, px] = col
    if kind == "canopy":
        s = r.randint(3, 6)
        for dy in range(-s, s + 1):
            for dx in range(-s - 1, s + 2):
                if dx * dx + dy * dy * 1.3 <= s * s:
                    p(x + dx, y + dy, c if dx + dy < -s // 2 else (b if dx + dy > s // 2 else a))
    elif kind == "peak":
        s = r.randint(4, 8)
        for i in range(s):
            for dx in range(-i, i + 1):
                p(x + dx, y + i, c if dx < 0 and i < s * 0.6 else (b if dx > 0 else a))
    elif kind == "hump":
        s = r.randint(5, 9)
        for dx in range(-s, s + 1):
            p(x + dx, y - int((1 - (dx / s) ** 2) * 3), c)
            p(x + dx, y + 1 - int((1 - (dx / s) ** 2) * 3), b)
    elif kind == "ripple":
        s = r.randint(6, 12)
        for dx in range(s):
            p(x + dx, y + int(1.6 * np.sin(dx / 2.2)), b)
    elif kind == "mesa":
        s = r.randint(3, 6)                                # a low rounded red outcrop, lit from above
        for dy in range(-s // 2 - 1, s // 2 + 2):
            for dx in range(-s, s + 1):
                if dx * dx / (s * s) + dy * dy * 4 / (s * s) <= 1 + r.uniform(-0.25, 0.1):
                    p(x + dx, y + dy, (0xa4, 0x50, 0x3c) if dy < 0 else (0x74, 0x30, 0x28))
    elif kind in ("reed", "fleck", "crystal", "cap", "coral", "spire"):
        h = {"reed": 3, "fleck": 1, "crystal": 5, "cap": 2, "coral": 3, "spire": 7}[kind]
        for dy in range(h):
            p(x, y - dy, c)
        if kind in ("cap", "fleck"):
            p(x + 1, y, c)


def main():
    cells = MR.top_objects(MR.load("QudWorldMap"))
    W, H = 80 * CW, 25 * CH
    src = np.asarray(Image.open(sys.argv[1]).convert("RGB").resize((W, H), Image.NEAREST), dtype=float)
    kinds, names = {}, {}
    grid = np.full((25, 80), -1)
    order = list(B)
    for (x, y), n in cells.items():
        b = biome(n)
        name = n or ""
        water = re.search(r"River|Stream|Duskwaters", name) or "LakeHinnom" in name
        kinds[x, y] = "water" if water else b
        grid[y, x] = order.index(kinds[x, y]) if kinds[x, y] else -1
    for y in range(25):                                    # sites sit on whatever is around them
        for x in range(80):
            if grid[y, x] < 0:
                around = [grid[y + b, x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < 80 and 0 <= y + b < 25 and grid[y + b, x + a] >= 0]
                grid[y, x] = around[0] if around else order.index("dunes")
    land = np.where(grid == order.index("water"), order.index("jungle"), grid)
    nx, ny = noise(W, H, 28, 1) + 0.5 * noise(W, H, 9, 2), noise(W, H, 28, 3) + 0.5 * noise(W, H, 9, 4)
    X, Y = np.meshgrid(np.arange(W), np.arange(H))
    u = np.clip(((X + nx * 46) / CW).astype(int), 0, 79)
    v = np.clip(((Y + ny * 62) / CH).astype(int), 0, 24)
    which = land[v, u]
    img = np.zeros((H, W, 3))
    grain = np.random.RandomState(5).rand(H, W) * 0.08 + 0.96
    for i, k in enumerate(order):
        img[which == i] = rgb(B[k][0])
    img *= grain[..., None]
    r = random.Random(7)
    for _ in range(26000):
        x, y = r.randrange(W), r.randrange(H)
        k = order[which[y, x]]
        g, dk, lt, kind, dens = B[k]
        if kind == "none" or r.random() > dens * 0.5:
            continue
        mark(img, kind, x, y, tuple(rgb(g) * r.uniform(0.92, 1.08)), tuple(rgb(dk)), tuple(rgb(lt)), r)
    bg = np.array([0x0f, 0x3b, 0x3a], dtype=float)
    for (x, y), name in cells.items():                      # water shapes and site icons: the game's own pixels
        px, py = x * CW, y * CH
        tile = src[py:py + CH, px:px + CW]
        solid = np.abs(tile - bg).sum(axis=2) > 40
        if kinds.get((x, y)) == "water" or "PalladiumReef" in (name or ""):
            lake = "Hinnom" in (name or "") or "PalladiumReef" in (name or "")
            col = rgb("2f7a9c") if lake else rgb("3f7f8c" if "Svy" in name else "33687c" if "Yonth" in name else "26444f" if "Dusk" in name else "4a93ae")
            lit = tile.sum(axis=2) > 330
            img[py:py + CH, px:px + CW][solid] = col * 0.95
            img[py:py + CH, px:px + CW][solid & lit] = col * 1.2
        elif kinds.get((x, y)) is None:
            img[py:py + CH, px:px + CW][solid] = tile[solid]
    Image.fromarray(np.clip(img, 0, 255).astype("uint8")).resize((W * 3 // 2, H * 3 // 2), Image.NEAREST).save(sys.argv[2])


if __name__ == "__main__":
    main()
