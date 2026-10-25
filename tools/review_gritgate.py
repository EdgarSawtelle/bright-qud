"""Zone review #7 Grit Gate (hand-made maps GritGate.rpm and Barathrums_Study.rpm, both underground): the
Barathrumite workshop and Barathrum's study, as the original game, Bright Qud today (flat grey stone) and
the proposal (carbon-black teal floor with hairline seams; every light casts a pool in its own colour:
cyan arc sconces, warm torches). Local output only.

Usage: .venv/bin/python -I tools/review_gritgate.py -> mockups/local/zones/review_gritgate.png
"""
import math, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from colors import BRIGHT, hex_rgb  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare, stone  # noqa: E402
from family_examples import busiest_box  # noqa: E402
from review_rustwells import fulcrete  # noqa: E402

WARM = (255, 170, 90)


def lights_of(cells):
    out = []
    for (x, y), objs in cells.items():
        for o in objs:
            r = MR.bp().part(o, "LightSource", "Radius") if o in MR.bp().objs else None
            if not r or MR.bp().part(o, "Brain", "Mobile") not in (None, "false"):
                continue
            fire = any(w in o for w in ("Torch", "Campfire", "Brazier", "Oven", "Forge", "Fire"))
            fg, _ = MR.color_letters(MR.bp(), o)
            col = WARM if fire else zm.lerp(hex_rgb(BRIGHT[fg]), (255, 255, 255), 0.3)
            out.append((x, y, min(max(int(r), 2), 6), col))
    return out


def lit(ground, cells):
    """As BrightQud.cs Lit(): the floor near each light gets brighter, tinted by the light's colour."""
    ls = lights_of(cells)

    def f(x, y):
        g = ground(x, y)
        best, col = 0.0, WARM
        for lx, ly, r, c in ls:
            d = math.hypot(x - lx, y - ly) / r
            if d < 1 and (1 - d) ** 1.5 > best:
                best, col = (1 - d) ** 1.5, c
        k = best * 0.55
        b = tuple(min(255, int(c * (1 + k * 1.2))) for c in g)
        return zm.lerp(b, col, k * 0.35)
    return f


def main():
    rows = []
    for title, m, box in (("The Barathrumite workshop (GritGate.rpm)", "GritGate", None),
                          ("Barathrum's study", "Barathrums_Study", None)):
        cells = MR.load(m)
        box = box or busiest_box(cells)
        rows.append((title, [("Original game", MR.render(m, "vanilla", box)),
                             ("Bright Qud today (flat grey stone floor)", MR.render(m, "new", box, ground=lit(stone, cells), tone=fulcrete)),
                             ("Proposal: carbon-black floor, coloured light", MR.render(m, "new", box, ground=lit(flat("teal", "g"), cells),
                                                                                         bare=bare("teal"), tone=fulcrete))]))
    pw, ph = rows[0][1][0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + 2 * (ph + head + 40 + pad) + 120), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '7. Grit Gate - "beneath its chrome palings a wide passage opens into the jungle loam": the hidden, orderly '
         "tinker workshop of the Barathrumites", pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    y = 70
    for title, panels in rows:
        d.text((pad, y), title, font=font(20), fill=(235, 205, 140))
        y += 36
        for i, (label, im) in enumerate(panels):
            x = pad + i * (pw + pad)
            d.text((x, y), label, font=font(16), fill=(225, 215, 185))
            out.paste(im.convert("RGB"), (x, y + head - 6))
        y += ph + head + pad
    wrap(d, "Low contrast, rich small detail. Floors: the carbon-black of fulcrete with hairline seams (study: 'cold "
         "carbon-black and chrome interior, warmed only by brass, torches'). Lights: arc sconces pool cool cyan, torches "
         "warm orange, the study's hoarshrooms and glowsphere their own colours. Fulcrete walls are already tar-dark "
         "(0.21.7). The cave-light change of 0.21.6 already shows today's warm pools.", pad, y + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_gritgate.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
