"""Zone review #24 Bethesda Susa, second try, closer to FuzzyJuzzy's fan art: rust terraces giving way to a green valley, pale marble
with no corners on the surface. Below ground the fan art says nothing: the game paints every level with cold blue dots and gets colder
with depth (BethesdaColdZone), so wards are cold stone and marble "ribbons of impurity", and the cryobarrios follow the ice cave photo. Local output only.

Usage: .venv/bin/python -I tools/review_bethesda.py -> mockups/local/zones/review_bethesda.png
"""
import os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import review_ruins as RR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402
import numpy as np  # noqa: E402
import groundsets as G  # noqa: E402
import susawall  # noqa: E402
from review_worldmap import noise  # noqa: E402

W, H = 26, 10
RR.MAT["Marble"] = "stiltmarble"
RR.TONE["Marble"] = ("e6e1d4", "b9b4a8")
RR.MAT["Fulcrete"] = "fulcrete"


def rooms(wall, seed, extra):
    r = random.Random(seed)
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for (x0, y0, x1, y1) in ((2, 1, 11, 7), (14, 2, 23, 8)):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x in (x0, x1) or y in (y0, y1)) and r.random() > 0.22:
                    c[x, y] = [wall]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for n in extra:
        c[empty.pop()] = [n]
    return c


def valley():
    """Rust, mixed or green per cell, so the valley comes in with loose edges and a mixed band between."""
    n = noise(W * 2 + 2, H * 2 + 2, 12, 71)[::2, ::2] * 1.6 + np.linspace(-.42, .42, W + 1)[None, :]
    green = n > 0
    rust_tile, green_tile = bare("susa"), bare("susagreen")
    rust_flat, green_flat = flat("susa", "b"), flat("susagreen", "b")

    def corners(x, y):
        return tuple(int(v) for v in (green[y, x], green[y, x + 1], green[y + 1, x + 1], green[y + 1, x]))

    def solid(colour, tile):
        out = Image.new("RGBA", (16, 24), colour + (255,))
        out.alpha_composite(tile)
        return out

    def floor(x, y):
        return G.corner_blend(solid(rust_flat(x, y), rust_tile(x, y)), solid(green_flat(x, y), green_tile(x, y)), corners(x, y), (x, y))
    return (lambda x, y: (green_flat if sum(corners(x, y)) > 2 else rust_flat)(x, y)), floor


def marble(palette):
    def post(name, t):
        if name != "Marble" or not RR.LAST[0]:
            return RR.real(name, t)
        return susawall.wall(RR.LAST[0].rsplit("-", 1)[1], palette)
    return post


def mist(cells):
    """Cryogenic mist around one chamber, as the wiki describes: the game's own gas object."""
    for (x, y), v in cells.items():
        if not v and ((x - 8) ** 2 / 9 + (y - 4) ** 2 / 4) < 1:
            cells[x, y] = ["CryoGas80"]
    return cells


def main():
    box = (0, 0, W, H)
    ground, floor = valley()
    surf = rooms("Marble", "s", ("Swarmshade Tree", "Swarmshade Tree", "Ziv Bough", "Ziv Bough", "Star Palm"))
    ward = rooms("Marble", "w", ("Rubble Grey", "Rubble Grey"))
    cryo = mist(rooms("Marble", "w", ("Rubble Grey", "Rubble Grey")))
    rows = [("Surface today", MR.render(surf, "new", box, ground=flat("rust", "a"), bare=bare("rust"))),
            ("Surface proposal: rust terraces into green, angleless marble", MR.render(surf, "new", box, ground=ground, bare=floor, swap=RR.recording, post=marble("surface"))),
            ("Ward proposal: cold stone, marble with ribbons of impurity", MR.render(ward, "new", box, ground=flat("ward", "b"), bare=bare("ward"), swap=RR.recording, post=marble("ward"))),
            ("Cryobarrio proposal: iced marble, frost, cryogenic mist", MR.render(cryo, "new", box, ground=flat("rime", "b"), bare=bare("rime"), swap=RR.recording, post=marble("ice")))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + 2 * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '24. Bethesda Susa - "eons-shifted stone entombs the angleless architecture of Bethsaida\'s lair"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + (i % 2) * (pw + pad), 54 + (i // 2) * (ph + 32)
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_bethesda.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
