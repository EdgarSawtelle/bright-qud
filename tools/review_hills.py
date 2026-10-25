"""Zone review #11 Hills and mountains: hills (marl outcrops, scrub, goats) and mountains (limestone ridges
with a pass), from the game's own objects, as the original game, Bright Qud today (0.21.4: pale salt ground,
generic block walls) and the proposal (dry dirt with scree and wind-flattened grass; chalk-white wavy marl
and fossil-pocked limestone walls). Local output only.

Usage: .venv/bin/python -I tools/review_hills.py -> mockups/local/zones/review_hills.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare, W, H  # noqa: E402

WALLS = {"Marl": "marl", "Limestone": "limestone"}


def stone(name, x, y, cells):
    """As BrightQud.cs WallSwaps: marl and limestone get their own walls, N/E/S/W joined."""
    if name not in WALLS:
        return None
    bit = lambda dx, dy: "1" if name in cells.get((x + dx, y + dy), []) else "0"
    return f"brightqudwall_{WALLS[name]}-" + bit(0, -1) + bit(1, 0) + bit(0, 1) + bit(-1, 0)


MUTED = {"Marl": ((0xb4, 0xad, 0x9a), 0.0), "Limestone": ((0x8a, 0x98, 0x93), 0.0)}


def muted(name, t):
    """As BrightQud.cs: marl a soft chalk, limestone glaucous grey-green (the game's y/Y/K glare white)."""
    if name not in MUTED:
        return t
    target, _ = MUTED[name]
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a < 200 or max(r, g, b) < 40:
                continue
            v = (r + g + b) / 3 / 255
            px[x, y] = tuple(int(c * (0.45 + 0.7 * v)) for c in target) + (a,)
    return t


def hills_scene():
    rnd = random.Random("hills")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    for cx, cy, rx, ry in ((5, 2, 4, 1.8), (20, 7, 5, 2.2)):
        for y in range(H):
            for x in range(W):
                if math.hypot((x - cx) / rx, (y - cy) / ry) < 1 + rnd.uniform(-0.2, 0.2):
                    cells[x, y] = ["Marl"]
    for _ in range(16):
        x, y = rnd.randrange(W), rnd.randrange(H)
        if not cells[x, y]:
            cells[x, y] = [rnd.choice(["Dogthorn Tree", "Dogthorn Tree", "Witchwood Tree", "Starapple Tree"])]
    for c, xy in (("Goat", (11, 5)), ("Goat", (12, 6)), ("Goat", (10, 6)), ("Slumberling", (15, 3))):
        cells[xy] = [c]
    return cells


def mountain_scene():
    rnd = random.Random("mountains")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            ridge = 3.5 + 2.5 * math.sin(x / 4.0) + rnd.uniform(-0.6, 0.6)
            if y < ridge or y > ridge + 4.5 + rnd.uniform(-0.5, 0.5):        # a pass between two ridges
                cells[x, y] = ["Limestone"]
    for c, xy in (("Goat", (6, 5)), ("Barkbiter", (17, 6)), ("Dogthorn Tree", (11, 6)), ("Witchwood Tree", (22, 5))):
        cells[xy] = [c]
    return cells


def main():
    box = (0, 0, W, H)
    rows = []
    for title, c in (("Hills: marl outcrops, dogthorn scrub, goats", hills_scene()),
                     ("Mountains: limestone ridges and a pass", mountain_scene())):
        rows.append((title, [("Original game", MR.render(c, "vanilla", box)),
                             ("Bright Qud today (0.21.4)", MR.render(c, "new", box, ground=flat("salt", "a"), bare=bare("salt"))),
                             ("Proposal", MR.render(c, "new", box, ground=flat("hills", "b"), bare=bare("hills"), swap=stone, post=muted))]))
    pw, ph = rows[0][1][0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + 2 * (ph + head + 40 + pad) + 120), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '11. Hills and mountains - "blips in the wave graph of stone over time" / "where the world plates once vexed '
         'themselves into war, a quiet peace has settled"', pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    y = 70
    for title, panels in rows:
        d.text((pad, y), title, font=font(20), fill=(235, 205, 140))
        y += 36
        for i, (label, im) in enumerate(panels):
            x = pad + i * (pw + pad)
            d.text((x, y), label, font=font(16), fill=(225, 215, 185))
            out.paste(im.convert("RGB"), (x, y + head - 6))
        y += ph + head + pad
    wrap(d, "Ground: dry dirt (darker and quieter than today's pale salt) with scree, wind-flattened grass and chalk flecks. "
         "Walls (the game reuses one generic block for both): marl becomes wavy chalk-white strata ('lime-rich mud ... in "
         "chalk-white shine'), limestone becomes bedded grey-green stone with small fossil pocks ('the glaucous rock is a "
         "necropolis'). Low contrast, rich small detail.", pad, y + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_hills.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
