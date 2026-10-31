"""Zone review #24 Bethesda Susa: surface (jungle with marble ruins), a ward and a cold stratum, from the game's objects: today
and proposal. Local output only.

Usage: .venv/bin/python -I tools/review_bethesda.py -> mockups/local/zones/review_bethesda.png
"""
import os, random, sys

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
RR.MAT["Marble"] = "stiltmarble"
RR.TONE["Marble"] = ("e6e1d4", "b9b4a8")
RR.MAT["Fulcrete"] = "fulcrete"


def rooms(wall, seed, extra):
    r = random.Random(seed)
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for (x0, y0, x1, y1) in ((2, 1, 11, 7), (14, 2, 23, 8)):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x in (x0, x1) or y in (y0, y1)) and r.random() > 0.22:
                    c[x, y] = [wall]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for n in extra:
        c[empty.pop()] = [n]
    return c


def main():
    box = (0, 0, W, H)
    surf = rooms("Marble", "s", ("Swarmshade Tree", "Swarmshade Tree", "Ziv Bough", "Ziv Bough", "Star Palm"))
    ward = rooms("Marble", "w", ("Rubble Grey", "Rubble Grey"))
    rows = [("Surface today", MR.render(surf, "new", box, ground=flat("rust", "a"), bare=bare("rust"))),
            ("Surface proposal: jungle over white marble", MR.render(surf, "new", box, ground=flat("jungle", "b"), bare=bare("jungle"), swap=RR.recording, post=RR.real)),
            ("Ward proposal: cold stone", MR.render(ward, "new", box, ground=flat("ward", "b"), bare=bare("ward"), swap=RR.recording, post=RR.real)),
            ("Cold strata proposal: rime", MR.render(ward, "new", box, ground=flat("rime", "b"), bare=bare("rime"), swap=RR.recording, post=RR.real))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + 2 * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '24. Bethesda Susa - "eons-shifted stone entombs the angleless architecture of Bethsaida\'s lair"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + (i % 2) * (pw + pad), 54 + (i // 2) * (ph + 32)
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_bethesda.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
