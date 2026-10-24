"""Ground family examples: each texture set (art/src/groundsets.py) shown in a real or typical place,
Bright Qud today vs with the new ground. Local output: mockups/local/zones/ground_families.png.

Usage: .venv/bin/python -I tools/family_examples.py
"""
import os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import groundsets as G  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402

BOX_W, BOX_H = 26, 10


def busiest_box(cells):
    best, box = -1, (0, 0, BOX_W, BOX_H)
    for y0 in range(0, 25 - BOX_H + 1, 2):
        for x0 in range(0, 80 - BOX_W + 1, 3):
            n = sum(1 for x in range(x0, x0 + BOX_W) for y in range(y0, y0 + BOX_H) if cells.get((x, y)))
            # want a mix: objects AND open ground
            score = n if n < BOX_W * BOX_H * 0.55 else BOX_W * BOX_H - n
            if score > best:
                best, box = score, (x0, y0, x0 + BOX_W, y0 + BOX_H)
    return box


def scene(rnd, plants, rocks, creatures, water=None):
    cells = {}
    for y in range(BOX_H):
        for x in range(BOX_W):
            r = rnd.random()
            cells[x, y] = ([rnd.choice(rocks)] if rocks and r < 0.06 else [rnd.choice(plants)] if r < 0.16
                           else [water] if water and 3 < x < 8 and 2 < y < 6 else [])
    for c in creatures:
        cells[rnd.randrange(BOX_W), rnd.randrange(BOX_H)] = [c]
    return cells


def examples():
    rnd = random.Random("families")
    return [
        ("A. Salt and sand - Six Day Stilt (game map)", "salt", "StiltGroundFloor", None),
        ("B. Warm earth - Joppa (game map)", "earth", "Joppa", (20, 0, 46, 10)),
        ("C. Rust and red rock - desert canyon (typical objects)", "rust",
         scene(rnd, ["Dogthorn Tree", "Witchwood Tree", "Starapple Tree", "Qudzu"], ["Shale", "Sandstone"],
               ["Salamander", "Salthopper", "GiantDragonfly"]), (0, 0, BOX_W, BOX_H)),
        ("D. Green shade - jungle (typical objects)", "green",
         scene(rnd, ["Swarmshade Tree", "Star Palm", "Shimscale Mangrove Tree", "Starapple Tree"], None,
               ["Chitinous Puma", "Horned Chameleon", "GiantDragonfly"], "FreshWaterPuddle"), (0, 0, BOX_W, BOX_H)),
        ("E. Dark teal - Grit Gate (game map)", "teal", "GritGate", None),
    ]


def main():
    panels = []
    for label, fam, src, box in examples():
        cells = MR.load(src)
        box = box or busiest_box(cells)
        base, alt, _ = (G.hx(h) for h in G.FAMILIES[fam])
        ts = G.tiles(fam)
        rnd = random.Random(fam)
        cache = {}

        def ground(x, y):
            if (x, y) not in cache:
                cache[x, y] = zm.lerp(base, alt, 0.35 + rnd.random() * 0.3)
            return cache[x, y]

        def bare(x, y):
            return ts[(((x * 73856093) ^ (y * 19349663)) & 0x7fffffff) % len(ts)]
        now = MR.render(src, "now", box)
        new = MR.render(src, "new", box, ground=ground, bare=bare)
        panels.append((label, now, new))
    pw, ph = panels[0][1].size
    pad, head = 16, 30
    W = pad + 2 * (pw + pad)
    H = 70 + len(panels) * (ph + head + pad)
    out = Image.new("RGB", (W, H), (24, 24, 28))
    d = ImageDraw.Draw(out)
    d.text((pad, 14), "Ground families: Bright Qud today (left) vs new textured ground (right) - low contrast, "
           "rich small detail, no animation", font=font(22), fill=(240, 236, 220))
    for i, (label, now, new) in enumerate(panels):
        y = 60 + i * (ph + head + pad)
        d.text((pad, y), label, font=font(18), fill=(225, 215, 185))
        out.paste(now.convert("RGB"), (pad, y + head - 4))
        out.paste(new.convert("RGB"), (pad + pw + pad, y + head - 4))
    path = os.path.join(zm.OUT, "ground_families.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
