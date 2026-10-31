"""Zone review #17 Asphalt mines: surface (Tarland: shale and asphalt pools) and an upper shaft, today and proposal.
The asphalt is the game's K colour, a dark teal, so it reads as water; the proposal draws it black with a dull blue-green
sheen. Keep SHEEN in sync with Recolor.Strands use in BrightQud.cs. Local output only.

Usage: .venv/bin/python -I tools/review_asphalt.py -> mockups/local/zones/review_asphalt.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import colors as C  # noqa: E402
import map_render as MR  # noqa: E402
import review_ruins as RR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from review_hinnom import STRANDS  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

W, H = 26, 10
LIQ = "AsphaltPuddle"


def noise(seed, wall, walls_at):
    r = random.Random(seed)
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            v = math.sin(x / 3.1 + 1) + math.cos(y / 2.2 + x / 6) + r.uniform(-0.5, 0.5)
            if v > walls_at:
                c[x, y] = [wall]
            elif v < -0.15:
                c[x, y] = [LIQ]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for n in ("Rubble Grey", "Rubble Grey"):
        c[empty.pop()] = [n]
    return c


def liquid(t, fg, sheen, x=0, y=0):
    t = t.copy()
    px = t.load()
    vs = [sum(px[i, j][:3]) for i in range(t.width) for j in range(t.height) if px[i, j][3] > 0]
    lo, hi = min(vs), max(max(vs), min(vs) + 1)
    for j in range(t.height):
        for i in range(t.width):
            r, g, b, a = px[i, j]
            if a:
                k = (r + g + b - lo) / (hi - lo)
                px[i, j] = tuple(int(c * (0.7 + 0.6 * k)) for c in fg) + (a,)
    return t


def today(name, t):
    return liquid(t, (0x2e, 0x6a, 0x68), None) if name == LIQ else t


def proposal(name, t):
    if name == LIQ:
        t = liquid(t, (0x1f, 0x1f, 0x24), None)
        z = t.width // 16
        px = t.load()
        s = STRANDS[proposal.n % 4]
        proposal.n += 1
        for sx, row, n in s[:4]:
            for i in range(n):
                for a in range(z):
                    for b in range(z):
                        px[min(t.width - 1, (sx + i) * z + a), min(t.height - 1, (row + (i // 2) % 2) * z + b)] = (0x33, 0x47, 0x4a, 255)
        return t
    return RR.real(name, t)


proposal.n = 0


def walls(name, x, y, cells):
    """Vines belong to the surface ruins only."""
    k = RR.recording(name, x, y, cells)
    if k and "vinefulcrete" in k:
        k = RR.LAST[0] = k.replace("vinefulcrete", "fulcrete")
    return k


def main():
    box = (0, 0, W, H)
    surf, shaft = noise("tar", "Shale", 1.0), noise("shaft", "Fulcrete", 0.8)
    rows = [("Surface today", MR.render(surf, "new", box, ground=flat("earth", "a"), bare=bare("earth"), post=today)),
            ("Surface proposal", MR.render(surf, "new", box, ground=flat("tar", "b"), bare=bare("tar"), swap=walls, post=proposal)),
            ("Upper shaft today", MR.render(shaft, "new", box, ground=lambda x, y: (44, 47, 53), post=today)),
            ("Upper shaft proposal", MR.render(shaft, "new", box, ground=flat("tar", "c"), bare=bare("tar"), swap=walls, post=proposal))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + 2 * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '17. Asphalt mines - "ancient tribes siphoned the black blood"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + (i % 2) * (pw + pad), 54 + (i // 2) * (ph + 32)
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_asphalt.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
