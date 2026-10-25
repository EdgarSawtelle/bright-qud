"""Zone review #9 Bey Lah (hand-made map BeyLah.rpm, inside the flower fields): the hindren village as the
original game, Bright Qud today (0.21.11 meadow ground, plain plank walls) and the proposal
(petal-strewn brinestalk walls; at night warm torch and clay-oven light). Local output only.

Usage: .venv/bin/python -I tools/review_beylah.py -> mockups/local/zones/review_beylah.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402
from review_gritgate import lit  # noqa: E402
from zone_review import night_for  # noqa: E402

MAP = "BeyLah"


def petal(name, x, y, cells):
    """As BrightQud.cs WallSwaps: petal-strewn walls drawn as the petal wall, N/E/S/W joined."""
    if name != "Petal-Strewn WoodWall":
        return None
    bit = lambda dx, dy: "1" if "Petal-Strewn WoodWall" in cells.get((x + dx, y + dy), []) else "0"
    return "brightqudwall_petal-" + bit(0, -1) + bit(1, 0) + bit(0, 1) + bit(-1, 0)


def night(ground, cells):
    base = lit(ground, cells)

    def f(x, y):
        g = ground(x, y)
        l = base(x, y)
        dim = tuple(int(c * 0.62) for c in g)
        boost = tuple(max(0, a - b) for a, b in zip(l, g))      # the light the lamps add
        return tuple(min(255, d + int(b * 1.6)) for d, b in zip(dim, boost))
    return f


def hut_box(cells, w=26, h=10):
    """The 26 x 10 window with the most petal-strewn walls (the huts)."""
    best, box = -1, (0, 0, w, h)
    for y0 in range(0, 25 - h + 1):
        for x0 in range(0, 80 - w + 1, 2):
            n = sum(1 for x in range(x0, x0 + w) for y in range(y0, y0 + h)
                    if "Petal-Strewn WoodWall" in cells.get((x, y), []))
            if n > best:
                best, box = n, (x0, y0, x0 + w, y0 + h)
    return box


def main():
    cells = MR.load(MAP)
    box = hut_box(cells)
    g = flat("meadow", "bl")
    panels = [("Original game", MR.render(MAP, "vanilla", box)),
              ("Bright Qud today (0.21.11)", MR.render(MAP, "new", box, ground=g, bare=bare("meadow"))),
              ("Proposal: petal-strewn huts", MR.render(MAP, "new", box, ground=g, bare=bare("meadow"), swap=petal)),
              ("Proposal at night: torches and the clay oven", MR.render(MAP, "new", box, ground=g, night=night_for(cells, box),
                                                                        bare=bare("meadow"), swap=petal))]
    pw, ph = panels[0][1].size
    pad, head = 16, 30
    Wd = pad + 2 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + 2 * (ph + head + pad) + 110), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '9. Bey Lah - "at the center of a particularly thick copse, the vegetation clears. Flower-bedecked huts huddle '
         'in the clearing within, surrounded by phalanxes of tidy watervine rows and carefully-tended lah."', pad, 14,
         Wd - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(panels):
        x = pad + (i % 2) * (pw + pad)
        y = 70 + (i // 2) * (ph + head + pad)
        d.text((x, y), label, font=font(16), fill=(225, 215, 185))
        out.paste(im.convert("RGB"), (x, y + head - 6))
    wrap(d, "The huts: 'stripped trunks of sallow brinestalk bonded with mud and strewn with flower petals' - upright pale "
         "trunks, mud seams and bands, a few pressed petals (pink, gold, violet) instead of plain planks. Ground: the flower "
         "fields' muted sage (already in 0.21.11); dirt floors and paths blend in. Night: warm pools around the 12 torch "
         "posts and the clay oven.", pad, 70 + 2 * (ph + head + pad) + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_beylah.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
