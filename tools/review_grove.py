"""Zone review #18 Banana grove: a dense stand with an oolite outcrop, from the game's population: today and proposal
(rich soil, fallen fronds, deeper greens, oolite walls). Local output only.

Usage: .venv/bin/python -I tools/review_grove.py -> mockups/local/zones/review_grove.png
"""
import colorsys, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import review_ruins as RR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

W, H = 26, 10


def scene():
    r = random.Random("grove")
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            if (x - 22) ** 2 / 9 + (y - 2) ** 2 / 6 < 1 + r.uniform(-0.3, 0.3):
                c[x, y] = ["Oolite"]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for _ in range(46):
        c[empty.pop()] = ["Banana Tree"]
    for n in NAMES:
        c[empty.pop()] = [n]
    return c


NAMES = ["Yonderbrush", "Yonderbrush", "Yonderbrush", "Irritable Palm", "Irritable Palm", "Red Death Dacca", "Adiyy", "Cyclopean Gibbon"]
RR.MAT["Oolite"] = "oolite"
RR.TONE["Oolite"] = ("b4ad9c", "7c7668")


def deepen(name, t):
    """As BrightQud.cs Deepen for plants: green hues deeper and darker; trunks and fruit keep theirs."""
    if name == "Oolite":
        return RR.real(name, t)
    if "Tree" not in name and "Palm" not in name and "Dacca" not in name:
        return t
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a < 200:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.15 < h < 0.45:
                px[x, y] = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h + (0.36 - h) * 0.3, s * 0.85, v * 0.72)) + (a,)
    return t


def main():
    box = (0, 0, W, H)
    c = scene()
    rows = [("Today", MR.render(c, "new", box, ground=flat("green", "a"), bare=bare("green"))),
            ("Proposal", MR.render(c, "new", box, ground=flat("grove", "b"), bare=bare("grove"), post=deepen, swap=RR.recording))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + ph + 32), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '18. Banana grove - "the grove\'s million laced fingers sway in gentle opulence"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + i * (pw + pad), 54
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_grove.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
