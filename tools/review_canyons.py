"""Zone review #12 Desert canyons: a fissure of shale and sandstone with a dry wash, from the game's own objects, as
the original game, Bright Qud today (plain rust ground, generic block walls) and the proposal (crimson cracked clay
with salt in the cracks, flaking shale and cross-bedded sandstone walls). Local output only.

Usage: .venv/bin/python -I tools/review_canyons.py -> mockups/local/zones/review_canyons.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare, W, H  # noqa: E402
from review_hills import muted, MUTED  # noqa: E402

WALLS = {"Shale": "shale", "Sandstone": "sandstone"}
MUTED["Shale"] = ((0x74, 0x30, 0x28), 0.0)
MUTED["Sandstone"] = ((0xb0, 0x7a, 0x58), 0.0)


def stone(name, x, y, cells):
    """As BrightQud.cs WallSwaps: N/E/S/W joined with the same rock."""
    if name not in WALLS:
        return None
    bit = lambda dx, dy: "1" if name in cells.get((x + dx, y + dy), []) else "0"
    return f"brightqudwall_{WALLS[name]}-" + bit(0, -1) + bit(1, 0) + bit(0, 1) + bit(-1, 0)


def canyon_post(name, t):
    """Walls as muted(); dogthorn loses the lime: dusty olive, as a dry-country thorn tree (DogthornOlive in C#)."""
    if name.startswith("Dogthorn"):
        t = t.copy()
        px = t.load()
        for y in range(t.height):
            for x in range(t.width):
                r, g, b, a = px[x, y]
                if a > 200 and g > r and g > b:
                    v = g / 255
                    px[x, y] = (int(112 * v + 22), int(122 * v + 24), int(66 * v + 16), a)
        return t
    return muted(name, t)


def scene():
    rnd = random.Random("canyons")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            mid = 4.5 + 2.2 * math.sin(x / 4.5)                # the wash winds between two rock walls
            d = abs(y - mid)
            if d > 2.4 + rnd.uniform(-0.4, 0.5):
                cells[x, y] = ["Sandstone" if y > mid and x % 11 > 3 else "Shale"]
    open_cells = [k for k, v in cells.items() if not v]
    rnd.shuffle(open_cells)
    for name in ("Dogthorn Tree", "Dogthorn Tree", "Dogthorn Tree2", "Witchwood Tree", "Dog", "Boar"):
        cells[open_cells.pop()] = [name]
    return cells


def main():
    box = (0, 0, W, H)
    c = scene()
    panels = [("Original game", MR.render(c, "vanilla", box)),
              ("Bright Qud today", MR.render(c, "new", box, ground=flat("rust", "a"), bare=bare("rust"))),
              ("Approved (B, whiter)", MR.render(c, "new", box, ground=flat("canyon", "b"), bare=bare("canyon"), swap=stone, post=canyon_post))]
    pw, ph = panels[0][1].size
    pad = 16
    Wd = pad + pw + pad
    out = Image.new("RGB", (Wd, 70 + 3 * (ph + 34) + 110), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '12. Desert canyons - "the fissure-wounds have rotted to crimson and salt"', pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    y = 60
    for label, im in panels:
        d.text((pad, y), label, font=font(18), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (pad, y + 26))
        y += ph + 34
    wrap(d, "Ground: pale chalk and salt crust cracked into plates, crimson stain in the cracks, as in the fan art. Walls: shale as thin "
         "flaking plates, sandstone with slanted dune bedding; today both are the generic block. Dogthorn: dusty olive with a spiny crown.", pad, y + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_canyons.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
