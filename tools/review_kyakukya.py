"""Zone review #6 Kyakukya (hand-made map Kyakukya.rpm): the west houses around Mayor Nuntu and the east
side with the mud oven and the Oboroqoru statue, as the original game, Bright Qud today and the proposal
(the jungle's wet loam with sunflecks, darker trodden paths; at night warm torch and oven light).
Local output only.

Usage: .venv/bin/python -I tools/review_kyakukya.py -> mockups/local/zones/review_kyakukya.png
"""
import math, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import bare  # noqa: E402
from review_jungle import dappled  # noqa: E402

MAP = "Kyakukya"
LIGHTS = ("Torchpost", "KyakukyaOven")


def lit(ground, cells, night=True):
    """As BrightQud.cs: at night the ground is dimmer, and warm around torches and the oven."""
    srcs = [xy for xy, o in cells.items() if any(n in LIGHTS for n in o)]

    def f(x, y):
        g = ground(x, y)
        if not night:
            return g
        g = tuple(int(c * 0.62) for c in g)
        k = max((max(0, 1 - math.hypot(x - sx, y - sy) / 6) ** 1.5 for sx, sy in srcs), default=0) * 0.55
        b = tuple(min(255, int(c * (1 + k * 1.6))) for c in g)
        return zm.lerp(b, (255, 170, 90), k * 0.4)
    return f


def cage(name, x, y, cells):
    """As BrightQud.cs WallSwaps: mushroom flesh walls drawn as the cage-fungus wall, N/E/S/W joined."""
    if not name.startswith("MushroomWall"):
        return None
    bit = lambda dx, dy: "1" if any(o.startswith("MushroomWall") for o in cells.get((x + dx, y + dy), [])) else "0"
    return "brightqudwall_cage-" + bit(0, -1) + bit(1, 0) + bit(0, 1) + bit(-1, 0)


def main():
    cells = MR.load(MAP)
    rows = [("West: mushroom houses, Mayor Nuntu", (8, 9, 34, 19), False),
            ("East: the mud oven and the Oboroqoru statue (proposal at night)", (50, 6, 76, 16), True)]
    out_rows = []
    for title, box, night in rows:
        prop = MR.render(MAP, "new", box, ground=lit(dappled("jungle"), cells, night), bare=bare("jungle"), swap=cage)
        if night:
            prop = Image.eval(prop, lambda v: v)          # objects keep their colours (the game dims them only out of sight)
        out_rows.append((title, [("Original game", MR.render(MAP, "vanilla", box)),
                                 ("Bright Qud today (ground approximate)", MR.render(MAP, "now", box)),
                                 ("Proposal" + (" at night" if night else ""), prop)]))
    pw, ph = out_rows[0][1][0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + 2 * (ph + head + 40 + pad) + 120), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '6. Kyakukya - "the jungle village of ape god worshippers and their giant mushroom dwellings"', pad, 14,
         Wd - 2 * pad, font(22), (240, 236, 220))
    y = 70
    for title, panels in out_rows:
        d.text((pad, y), title, font=font(20), fill=(235, 205, 140))
        y += 36
        for i, (label, im) in enumerate(panels):
            x = pad + i * (pw + pad)
            d.text((x, y), label, font=font(16), fill=(225, 215, 185))
            out.paste(im.convert("RGB"), (x, y + head - 6))
        y += ph + head + pad
    wrap(d, "Mushroom houses: the walls become glossy cage-lattice fungus (red cage fungus), 'trimmed like a hedge', "
         "instead of the generic stone block the game reuses for them. "
         "Kyakukya sits in the jungle, so it takes the jungle's ground (wet loam, leaf litter, soft sunflecks) and "
         "its trodden paths are a little darker. At night the torch sconces and the mud oven ('warmth radiates from "
         "the crackling fire') cast warm pools. Low contrast, rich small detail; no animation unless turned on.",
         pad, y + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_kyakukya.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
