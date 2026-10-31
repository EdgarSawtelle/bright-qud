"""Zone review #20 Lake Hinnom: lake edge with reef plants, esh and coral rag, as of today (the algal water from 0.23.0
already applies) and the proposal (spongebed shore, pitted coral rag). Local output only.

Usage: .venv/bin/python -I tools/review_hinnom2.py -> mockups/local/zones/review_lakehinnom.png
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
from review_hinnom import STRANDS  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

W, H = 26, 10
LIQ = "AlgalWaterDeepPool"
RR.MAT["Coral Rag"] = "coralrag"
RR.TONE["Coral Rag"] = ("5f9c9e", "3f6e74")
n = [0]


def scene():
    r = random.Random("hinnom")
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            if y + 1.2 * math.sin(x / 3) > 5.2:
                c[x, y] = [LIQ]
            elif (x - 5) ** 2 / 9 + (y - 1) ** 2 / 3 < 1:
                c[x, y] = ["Coral Rag"]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for name in ["Finger Coral"] * 7 + ["Tunnel Sponge"] * 6 + ["Bop Sponge", "Junk Dollar", "White Esh", "White Esh", "White Esh", "Prism Perch"]:
        c[empty.pop()] = [name]
    return c


def post(name, t):
    if name == LIQ:
        t = liquid(t, (0x3a, 0x8f, 0xb4), None)
        z = t.width // 16
        px = t.load()
        for sx, row, length in STRANDS[n[0] % 4]:
            for i in range(length):
                col = (0x4f, 0x9a, 0x55, 255) if i == 1 else (0x37, 0x7a, 0x4c, 255)
                for a in range(z):
                    for b in range(z):
                        px[min(t.width - 1, (sx + i) * z + a), min(t.height - 1, (row + (i // 2) % 2) * z + b)] = col
        n[0] += 1
        return t
    return RR.real(name, t)


def main():
    box = (0, 0, W, H)
    c = scene()
    rows = [("Today", MR.render(c, "new", box, ground=flat("earth", "a"), bare=bare("earth"), post=lambda name, t: post(name, t) if name == LIQ else t)),
            ("Proposal", MR.render(c, "new", box, ground=flat("sponge", "b"), bare=bare("sponge"), swap=RR.recording, post=post))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + ph + 32), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '20. Lake Hinnom - "coral fingers poke out from the spongebed and pierce the algal bloom"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + i * (pw + pad), 54
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_lakehinnom.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
