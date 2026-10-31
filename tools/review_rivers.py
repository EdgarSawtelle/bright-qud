"""Zone review #19 Rivers: one braided channel from the game's objects, today and one panel per river: same structure,
each river's own water tone and banks, from its world map text. Local output only.

Usage: .venv/bin/python -I tools/review_rivers.py -> mockups/local/zones/review_rivers.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import review_ruins as RR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from review_asphalt import liquid  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

W, H = 26, 10
LIQ = "SaltyWaterDeepPool"
RR.MAT["Gypsum"] = "gypsum"
RR.TONE["Gypsum"] = ("b89a58", "7a6438")
RIVERS = (("River Svy: 'vine-braided loam'", "gravel", "3f7f8c"), ("River Opal: 'crushed granite'", "gravel", "4a93ae"),
          ("Opal's Duskwaters: 'a shady pool'", "jungle", "26444f"), ("River Yonth: 'basalt chips'", "basalt", "33687c"),
          ("Mountain stream: 'a cool brine'", "gravel", "6fa8b4"))


def scene():
    r = random.Random("river")
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            mid = 4.5 + 2.4 * math.sin(x / 4.2)
            if abs(y - mid) < 2.2 + 0.9 * math.sin(x / 2.0 + 1):
                c[x, y] = [LIQ]
            elif (x - 22) ** 2 / 10 + (y - 9) ** 2 / 4 < 1:
                c[x, y] = ["Gypsum"]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for n in ("Shimscale Mangrove Tree", "Swarmshade Tree", "Ziv Bough", "Star Palm", "Rubble Grey"):
        c[empty.pop()] = [n]
    return c


def tinted(fg):
    def post(name, t):
        if name == LIQ:
            return liquid(t, tuple(int(fg[i:i + 2], 16) for i in (0, 2, 4)), None)
        return RR.real(name, t)
    return post


def main():
    box = (0, 0, W, H)
    c = scene()
    rows = [("Today", MR.render(c, "new", box, ground=flat("earth", "a"), bare=bare("earth")))]
    for label, fam, water in RIVERS:
        rows.append((label, MR.render(c, "new", box, ground=flat(fam, "b"), bare=bare(fam), swap=RR.recording, post=tinted(water))))
    pw, ph = rows[0][1].size
    pad = 14
    n = (len(rows) + 1) // 2
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + n * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '19. Rivers - five rivers, one structure, each with the tone of its own text', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + (i % 2) * (pw + pad), 54 + (i // 2) * (ph + 32)
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_rivers.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
