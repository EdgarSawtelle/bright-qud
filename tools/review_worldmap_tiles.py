"""World map, last attempt, on Qud's own logic: every cell stays its own tile with the game's glyph. Only two things change: each
cell's background is its biome's calm colour eased toward its neighbours', so borders stop clashing, and the glyph colours follow
the approved palettes. Corners where a biome meets another are eased too, which rounds the steps. Works per cell, so it needs no
generated textures in the game. Local output only.

Usage: .venv/bin/python tools/review_worldmap_tiles.py <vanilla png 2560x1200> <out.png>
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import map_render as MR  # noqa: E402
from review_worldmap import biome, rgb  # noqa: E402

# biome: background, glyph colour (the glyph's own light and dark stay relative)
T = {"jungle": ("24392a", "5a9a50"), "deep": ("192c26", "3f8058"), "hills": ("4a4434", "b09c6c"), "mount": ("3e424a", "c4c4bc"),
     "dunes": ("6c6450", "d8c89c"), "canyon": ("7c6a60", "e8c8b0"), "marsh": ("38443a", "90b070"), "flowers": ("3f4c38", "b8c070"),
     "grove": ("3c4426", "c8c048"), "ruins": ("383c34", "d0d8d0"), "moon": ("2c2848", "b8a4e8"), "fungal": ("2c2030", None),
     "reef": ("183c40", None), "water": ("1f3a48", None)}
ORDER = list(T)
GLYPH = 0.45


def main():
    cells = MR.top_objects(MR.load("QudWorldMap"))
    van = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=float)
    teal = np.array([0x0f, 0x3b, 0x3a], dtype=float)
    grid = np.full((25, 80), -1)
    for (x, y), n in cells.items():
        b = biome(n or "")
        if re.search(r"River|Stream|Duskwaters|LakeHinnom", n or ""):
            b = "water"
        grid[y, x] = ORDER.index(b) if b else -1
    for _ in range(6):
        for y in range(25):
            for x in range(80):
                if grid[y, x] < 0:
                    near = [grid[y + b, x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < 80 and 0 <= y + b < 25 and grid[y + b, x + a] >= 0]
                    if near:
                        grid[y, x] = near[0]
    grid[grid < 0] = ORDER.index("dunes")
    bgc = np.array([[rgb(T[ORDER[grid[y, x]]][0]) for x in range(80)] for y in range(25)])
    eased = bgc.copy()
    for _ in range(2):                                      # each cell leans toward its neighbours, per cell
        p = np.pad(eased, ((1, 1), (1, 1), (0, 0)), mode="edge")
        eased = (p[1:-1, 1:-1] * 2 + p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 6
    out = np.zeros((25 * 24, 80 * 16, 3))
    for y in range(25):
        for x in range(80):
            tile = van[y * 48:(y + 1) * 48:2, x * 32:(x + 1) * 32:2]
            solid = np.abs(tile - teal).sum(axis=2) > 40
            view = out[y * 24:(y + 1) * 24, x * 16:(x + 1) * 16]
            view[:] = eased[y, x]
            k = ORDER[grid[y, x]]
            g = T[k][1]
            name = cells.get((x, y)) or ""
            if g is not None and biome(name):
                lum = (tile.sum(axis=2) / 3 / 255)[..., None]
                col = rgb(g) * (0.55 + 0.75 * lum)
                view[solid] = col[solid]
            else:
                view[solid] = tile[solid]
    Image.fromarray(np.clip(out, 0, 255).astype("uint8")).resize((1920, 900), Image.NEAREST).save(sys.argv[2])


if __name__ == "__main__":
    main()
