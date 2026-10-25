"""Zone review #8 Flower fields: a meadow built from the game's own flower-field objects (random-colour
flowers, sandstone outcrops with jilted lover and qudzu, equimax herd, glowcrow, salthopper, dragonfly),
as the original game, Bright Qud today and the proposal (salted pale green-grey ground with prismatic
filaments in the cracks). Local output only.

Usage: .venv/bin/python -I tools/review_flowerfields.py -> mockups/local/zones/review_flowerfields.png
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


def meadow():
    rnd = random.Random("flowers")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            if math.hypot((x - 21) / 3.5, (y - 2) / 2) < 1:
                cells[x, y] = ["Sandstone"]
            elif rnd.random() < 0.3:
                cells[x, y] = ["Flowers"]
    for xy in ((17, 2), (24, 3), (20, 4)):
        cells[xy] = ["Jilted Lover"]
    for c, xy in (("Equimax", (6, 6)), ("Equimax", (8, 7)), ("Equimax", (5, 8)), ("Glowcrow", (14, 3)),
                  ("Salthopper", (11, 5)), ("GiantDragonfly", (18, 7))):
        cells[xy] = [c]
    return cells


def main():
    box = (0, 0, W, H)
    c = meadow()
    panels = [("Original game", MR.render(c, "vanilla", box)),
              ("Bright Qud today (ground approximate)", MR.render(c, "now", box)),
              ("Proposal: muted sage meadow, prismatic filaments", MR.render(c, "new", box, ground=flat("meadow", "m"), bare=bare("meadow")))]
    pw, ph = panels[0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + ph + head + pad + 110), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '8. Flower fields - "prismatic filament colonizes the cracks between the salted rot. There are meadows here, '
         'She says."', pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(panels):
        x = pad + i * (pw + pad)
        d.text((x, 70), label, font=font(16), fill=(225, 215, 185))
        out.paste(im.convert("RGB"), (x, 70 + head - 6))
    wrap(d, "Low contrast, rich small detail: a muted sage ground (darker than the study #a9b39a so it stays quiet and creatures "
         "still pop), salt cracks with faint threads of pink, violet, blue and gold growing in them, short grass. In the game "
         "every flower takes one of 7 random colours (this mockup shows them all in the blueprint colour).",
         pad, 70 + head + ph + 10, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_flowerfields.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
