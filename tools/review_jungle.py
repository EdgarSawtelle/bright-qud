"""Zone review #5 Jungle: a dense jungle clearing with the game's own jungle objects (swarmshade, ziv
bough, mangrove, star palm, mudroot, chrome sinking in the green), as the original game, Bright Qud
today (green family, 0.21.4) and the proposal (wet loam, leaf litter, soft sunflecks). Local output only.

Usage: .venv/bin/python -I tools/review_jungle.py -> mockups/local/zones/review_jungle.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import groundsets as G  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare, W, H  # noqa: E402


def hashv(x, y):
    return ((((x * 73856093) ^ (y * 19349663)) & 0x7fffffff) % 1000) / 1000


def noise(x, y, s=5.0):
    """Smooth value noise over ~s cells (as BrightQud.cs Dapple)."""
    gx, gy = x / s, y / s
    x0, y0 = int(gx), int(gy)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = hashv(x0, y0), hashv(x0 + 1, y0)
    c, d = hashv(x0, y0 + 1), hashv(x0 + 1, y0 + 1)
    return (a + (b - a) * fx) * (1 - fy) + (c + (d - c) * fx) * fy


def dappled(fam):
    base = flat(fam, "j")
    fleck = G.hx(G.SUNFLECK)

    def f(x, y):
        k = max(0.0, noise(x, y) - 0.5) / 0.5 * 0.7       # the brighter patches, at most 70% of the way
        return zm.lerp(base(x, y), fleck, k)
    return f


def jungle():
    rnd = random.Random("jungle")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    trees = ["Swarmshade Tree", "Swarmshade Tree", "Ziv Bough", "Shimscale Mangrove Tree", "Star Palm", "Starapple Tree"]
    for y in range(H):
        for x in range(W):
            if math.hypot((x - 12) / 7, (y - 5) / 3.2) > 1 and rnd.random() < 0.5:   # a clearing in the middle
                cells[x, y] = [rnd.choice(trees)]
    for xy in ((2, 1), (3, 1), (3, 2), (22, 8), (23, 8)):
        cells[xy] = ["Mudroot"]
    for xy in ((9, 3), (10, 3), (16, 7)):                  # chrome swallowed by the green
        cells[xy] = ["Verdigris"]
    for c, xy in (("Albino ape", (14, 4)), ("Honey Skunk", (8, 6)), ("GiantDragonfly", (17, 3)), ("Horned Chameleon", (11, 7))):
        cells[xy] = [c]
    return cells


def main():
    box = (0, 0, W, H)
    c = jungle()
    panels = [("Original game", MR.render(c, "vanilla", box)),
              ("Bright Qud today (0.21.4: green family)", MR.render(c, "new", box, ground=flat("green", "a"), bare=bare("green"))),
              ("Proposal: wet loam, leaf litter, soft sunflecks", MR.render(c, "new", box, ground=dappled("jungle"), bare=bare("jungle")))]
    pw, ph = panels[0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + ph + head + pad + 110), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '5. Jungle - "braids of roots and ribbons of fronds dimensionalize the flat loam; something\'s home a discarded '
         'leaf makes"', pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(panels):
        x = pad + i * (pw + pad)
        d.text((x, 70), label, font=font(16), fill=(225, 215, 185))
        out.paste(im.convert("RGB"), (x, 70 + head - 6))
    wrap(d, "Low contrast, rich small detail. Dark wet loam (study palette #3b2f22) with leaf litter, twigs, roots and moss; "
         "sunflecks are large soft patches over several cells (no squares), only a little brighter and warmer. "
         "Chrome walls in the jungle use the dull verdigris look (0.21.2).", pad, 70 + head + ph + 10, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_jungle.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
