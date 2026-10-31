"""Zone review #16 Golgotha: the surface (rotting jungle, a verdigris building, slimy shafts) and a trash chute level
(verdigris walls, conveyor belts, puddles, trash), from the objects GolgothaChutes places: today and proposal.
Local output only.

Usage: .venv/bin/python -I tools/review_golgotha.py -> mockups/local/zones/review_golgotha.png
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
RR.MAT["Verdigris"] = "verdigris"
RR.TONE["Verdigris"] = ("6f8c80", "a4502b")


def surface():
    r = random.Random("golgotha")
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for x in range(9, 18):
        for y in range(2, 8):
            if x in (9, 17) or y in (2, 7):
                c[x, y] = ["Verdigris"]
    for x in (11, 13, 15):
        c[x, 4] = ["SlimyShaft"]
    empty = [k for k, v in c.items() if not v and not (9 < k[0] < 17 and 2 < k[1] < 7)]
    r.shuffle(empty)
    for n in ("Swarmshade Tree", "Swarmshade Tree", "Swarmshade Tree", "Ziv Bough", "Star Palm", "Shimscale Mangrove Tree", "Boar", "Salamander"):
        c[empty.pop()] = [n]
    return c


def chutes():
    r = random.Random("chutes")
    c = {(x, y): ["Verdigris"] for x in range(W) for y in range(H)}
    for x in range(1, 25):
        for y in range(2, 8):
            c[x, y] = []
    for x in range(3, 23):
        for y in (3, 4, 5):
            c[x, y] = ["ConveyorPadE"]
    c[2, 4] = ["ConveyorDrive"]
    for x in (23, 24):
        for y in (3, 4, 5):
            c[x, y] = ["SlimyShaft"]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for n in ("Garbage", "Garbage", "Garbage", "Garbage", "GooPuddle", "SludgePuddle", "OozePuddle"):
        c[empty.pop()] = [n]
    return c


def today(name, t):
    """As Ground.Apply today: Verdigris is already pulled to a dull green-grey."""
    return zm.recolor_to(t, (0x5f, 0x85, 0x7e), (0x4a, 0x6a, 0x4c), True) if name == "Verdigris" else t


def main():
    box = (0, 0, W, H)
    rows = [("Surface today", MR.render(surface(), "new", box, ground=flat("green", "a"), bare=bare("green"), post=today)),
            ("Surface proposal", MR.render(surface(), "new", box, ground=flat("jungle", "b"), bare=bare("jungle"), swap=RR.recording, post=RR.real)),
            ("Trash chutes today", MR.render(chutes(), "new", box, ground=lambda x, y: (44, 47, 53), bare=None, post=today)),
            ("Trash chutes proposal", MR.render(chutes(), "new", box, ground=flat("chute", "b"), bare=bare("chute"), swap=RR.recording, post=RR.real))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pad + 2 * (pw + pad), 60 + 2 * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '16. Golgotha - "the mouths of the rust-caves of Golgotha, chrome\'s graveyard"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + (i % 2) * (pw + pad), 54 + (i // 2) * (ph + 32)
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_golgotha.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
