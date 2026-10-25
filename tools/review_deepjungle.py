"""Zone review #10 Deep jungle: a dense deep-jungle scene from the game's own objects (nimbus beams, nachash,
ziv bough, mangrove, star palm, urberry, mudroot, lagroot, yonderbrush, ogre ape, purple jell), as the
original game, Bright Qud today (green family, 0.21.4), the proposal by day (darker loam with braided
roots, small rare pinpricks of light) and at night (lagroot and yonderbrush glow gold and blue).

Usage: .venv/bin/python -I tools/review_deepjungle.py -> mockups/local/zones/review_deepjungle.png
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
from review_jungle import noise  # noqa: E402

GLOW = {"Lagroot": (230, 200, 90), "Yonderbrush": (110, 150, 255)}
FLECK = (74, 69, 40)


def is_plant(name):
    chain = MR._chain(name)
    return any(c in ("Tree", "Plant") for c in chain) and MR.bp().part(name, "Brain", "Factions") is None


def deeper(name, t):
    """As BrightQud.cs: jungle plants pulled toward a deeper, darker green (brightness x0.72, a little
    less saturated); ink outlines are untouched."""
    if not is_plant(name):
        return t
    import colorsys
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a < 200 or max(r, g, b) < 40:
                continue
            h, sat, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.15 < h < 0.45:                                # greens only: trunks and fruit keep their colour
                h = h + (0.36 - h) * 0.3
                sat, v = sat * 0.85, v * 0.72
            rr, gg, bb = colorsys.hsv_to_rgb(h, sat, v)
            px[x, y] = (int(rr * 255), int(gg * 255), int(bb * 255), a)
    return t


def pinpricks(fam):
    base = flat(fam, "dj")

    def f(x, y):
        k = max(0.0, noise(x, y, 3.0) - 0.72) / 0.28 * 0.6    # only small, rare patches
        return zm.lerp(base(x, y), FLECK, k)
    return f


def glow_night(ground, cells):
    srcs = [(x, y, GLOW[o[0]]) for (x, y), o in cells.items() if o and o[0] in GLOW]

    def f(x, y):
        g = tuple(int(c * 0.6) for c in ground(x, y))
        best, col = 0.0, None
        for sx, sy, c in srcs:
            d = math.hypot(x - sx, y - sy) / 2.5
            if d < 1 and (1 - d) ** 1.5 > best:
                best, col = (1 - d) ** 1.5, c
        if not col:
            return g
        k = best * 0.55
        return zm.lerp(tuple(min(255, int(c * (1 + k * 1.2))) for c in g), col, k * 0.4)
    return f


def scene():
    rnd = random.Random("deepjungle")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    veg = ["Nimbus Beam", "Nimbus Beam", "Nachash Tree", "Ziv Bough", "Ziv Bough", "Shimscale Mangrove Tree",
           "Star Palm", "Urberry Bush"]
    for y in range(H):
        for x in range(W):
            if rnd.random() < 0.62 and math.hypot((x - 13) / 4, (y - 5) / 2.2) > 1:
                cells[x, y] = [rnd.choice(veg)]
    for xy in ((0, 0), (1, 0), (0, 1), (24, 9), (25, 9), (25, 8)):
        cells[xy] = ["Mudroot"]
    for c, xy in (("Lagroot", (10, 4)), ("Lagroot", (17, 6)), ("Yonderbrush", (14, 3)), ("Yonderbrush", (6, 7)),
                  ("Ogre Ape", (13, 5)), ("Purple Jell", (16, 4))):
        cells[xy] = [c]
    return cells


def main():
    box = (0, 0, W, H)
    c = scene()
    panels = [("Original game", MR.render(c, "vanilla", box)),
              ("Bright Qud today (0.21.4: green family)", MR.render(c, "new", box, ground=flat("green", "a"), bare=bare("green"))),
              ("Proposal: dark loam, roots, pinpricks, deeper greens", MR.render(c, "new", box, ground=pinpricks("deepjungle"),
                                                                                 bare=bare("deepjungle"), post=deeper)),
              ("Proposal at night: lagroot and yonderbrush glow", MR.render(c, "new", box, ground=glow_night(pinpricks("deepjungle"), c),
                                                                            bare=bare("deepjungle"), post=deeper))]
    pw, ph = panels[0][1].size
    pad, head = 16, 30
    Wd = pad + 2 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + 2 * (ph + head + pad) + 110), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '10. Deep jungle - "thriving florae pack the loam with maze-dense roots, and a high-wreath canopy chokes off '
         'the last beams of light"', pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(panels):
        x = pad + (i % 2) * (pw + pad)
        y = 70 + (i // 2) * (ph + head + pad)
        d.text((x, y), label, font=font(16), fill=(225, 215, 185))
        out.paste(im.convert("RGB"), (x, y + head - 6))
    wrap(d, "Darker than the jungle (study: 'dense, dark, claustrophobic, wet; a roof of leaves with pinpricks of light'): "
         "loam with leaf litter and braided roots; sunflecks only as small rare patches; plant greens pulled deeper and "
         "darker (the jungle too). At night lagroot ('thorny roots "
         "furcate into neuronal likeness') glows soft gold and yonderbrush ('blueshifted panicles') soft blue - they are "
         "visible in the dark in the game; here they also light the ground a little. Low contrast; no animation unless on.",
         pad, 70 + 2 * (ph + head + pad) + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_deepjungle.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
