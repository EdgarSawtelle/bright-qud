"""Zone review #3 Red Rock: surface outcrop and a cave level (rooms and corridors), each as the original
game, Bright Qud today and the proposal (redder surface ground; dark red-brown cave floor with rubble
and warm torch pools). Scenes are built from the game's own Red Rock objects. Local output only.

Usage: .venv/bin/python -I tools/review_redrock.py -> mockups/local/zones/review_redrock.png
"""
import os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import groundsets as G  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import night_for, wrap  # noqa: E402

W, H = 26, 10


def surface():
    rnd = random.Random("redrock-surface")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    for y in range(H):                                     # the outcrop: a mass of shale on the right
        for x in range(W):
            if (x - 19) ** 2 / 36 + (y - 4) ** 2 / 9 < 1 + rnd.uniform(-0.25, 0.25):
                cells[x, y] = ["Shale"]
    for _ in range(18):
        x, y = rnd.randrange(W), rnd.randrange(H)
        if not cells[x, y]:
            cells[x, y] = [rnd.choice(["Dogthorn Tree", "Witchwood Tree", "Starapple Tree", "Dogthorn Tree"])]
    for c in ("Goat", "Goat", "Baboon", "Snapjaw Scavenger"):
        x, y = rnd.randrange(0, 12), rnd.randrange(H)
        cells[x, y] = [c]
    return cells


def caves():
    rnd = random.Random("redrock-caves")
    cells = {(x, y): ["Shale"] for x in range(W) for y in range(H)}
    rooms = [(1, 1, 7, 5), (10, 2, 17, 7), (19, 1, 24, 8)]
    for x0, y0, x1, y1 in rooms:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                cells[x, y] = []
    for x in range(7, 11):                                 # corridors
        cells[x, 3] = []
    for x in range(17, 20):
        cells[x, 5] = []
    for y in range(5, 9):
        cells[4, y] = []
    cells[4, 8] = ["FreshWaterPuddle"]
    furniture = {(1, 1): "Torchpost", (17, 2): "Torchpost", (24, 8): "Torchpost", (10, 7): "Torchpost",
                 (2, 4): "Bedroll", (3, 4): "Bedroll", (12, 6): "Bones", (15, 3): "Garbage", (21, 7): "Hammock",
                 (6, 1): "Dreadroot", (23, 2): "Dreadroot", (18, 5): "Brinestalk Gate",
                 (5, 2): "Snapjaw Hunter", (13, 4): "Snapjaw Scavenger", (21, 4): "Snapjaw"}
    for xy, o in furniture.items():
        cells[xy] = [o]
    return cells


def flat(fam, seed):
    base, alt, _ = (G.hx(h) for h in G.FAMILIES[fam])
    rnd, cache = random.Random(seed), {}

    def f(x, y):
        if (x, y) not in cache:
            cache[x, y] = zm.lerp(base, alt, 0.35 + rnd.random() * 0.3)
        return cache[x, y]
    return f


def bare(fam):
    ts = G.tiles(fam)
    return lambda x, y: ts[(((x * 73856093) ^ (y * 19349663)) & 0x7fffffff) % len(ts)]


def torch_lit(ground, cells):
    """As BrightQud.cs Lit(): only the ground under torch light gets brighter and warmer."""
    import math
    torches = [xy for xy, o in cells.items() if o and o[0] == "Torchpost"]

    def f(x, y):
        g = ground(x, y)
        k = max((max(0, 1 - math.hypot(x - tx, y - ty) / 6) ** 1.5 for tx, ty in torches), default=0) * 0.55
        b = tuple(min(255, int(c * (1 + k * 1.2))) for c in g)
        return zm.lerp(b, (255, 170, 90), k * 0.35)
    return f


def stone(x, y):
    return (0x2c, 0x2f, 0x35)                              # BrightQud.cs Ground.Stone (underground today)


def main():
    box = (0, 0, W, H)
    s, c = surface(), caves()
    rows = [
        ("Surface: the red outcrop", [
            ("Original game", MR.render(s, "vanilla", box)),
            ("Bright Qud today (0.21.4: canyon rust ground)", MR.render(s, "new", box, ground=flat("rust", "a"), bare=bare("rust"))),
            ("Proposal: redder Red Rock ground", MR.render(s, "new", box, ground=flat("redrock", "b"), bare=bare("redrock")))]),
        ("Caves (strata 1-4): snapjaw rooms and corridors", [
            ("Original game", MR.render(c, "vanilla", box)),
            ("Bright Qud today (flat grey stone floor)", MR.render(c, "new", box, ground=stone)),
            ("Proposal: red-brown rubble floor, warm torch pools", MR.render(c, "new", box,
                                                                              ground=torch_lit(flat("redcave", "c"), c),
                                                                              bare=bare("redcave")))]),
    ]
    pw, ph = rows[0][1][0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    Hd = 70 + 2 * (ph + head + 40 + pad) + 120
    out = Image.new("RGB", (Wd, Hd), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '3. Red Rock - "a naturally reddened outcropping of stone juts out of the salted crag"; below: four strata of '
         "snapjaw rooms and corridors ending at an underground river", pad, 14, Wd - 2 * pad, font(22), (240, 236, 220))
    y = 70
    for title, panels in rows:
        d.text((pad, y), title, font=font(20), fill=(235, 205, 140))
        y += 36
        for i, (label, im) in enumerate(panels):
            x = pad + i * (pw + pad)
            d.text((x, y), label, font=font(16), fill=(225, 215, 185))
            out.paste(im.convert("RGB"), (x, y + head - 6))
        y += ph + head + pad
    wrap(d, "Low contrast, rich small detail (user rule). Caves: in the game the cave floor is lit only near torches "
         "and your own light; the torch pools stay without animation unless 'animated tiles' is on. Underground "
         "Red Rock currently uses the generic blue-grey stone floor of every cave.", pad, y + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_redrock.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
