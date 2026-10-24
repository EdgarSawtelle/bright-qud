"""Zone review #4 Rust Wells: the surface well (a round pit ringed by fulcrete sectors, red qudzu, wires)
and a lower stratum (solid shale with the round pit carved out), each as the original game, Bright Qud
today and the proposal. Scenes use the game's own Rust Wells objects. Local output only.

Usage: .venv/bin/python -I tools/review_rustwells.py -> mockups/local/zones/review_rustwells.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare, torch_lit, stone, W, H  # noqa: E402

CX, CY = 13, 5


def ring(cells, rnd, rx, ry):
    """Fulcrete sectors around the pit, with angular gaps, as Rustwells.cs builds them."""
    for y in range(H):
        for x in range(W):
            d = math.hypot((x - CX) / rx, (y - CY) / ry)
            ang = math.atan2(y - CY, x - CX)
            if 0.85 < d < 1.15 and int((ang + math.pi) / (math.pi / 4)) % 2 == 0:
                cells[x, y] = ["Fulcrete"]


def surface():
    rnd = random.Random("rustwells-surface")
    cells = {(x, y): [] for x in range(W) for y in range(H)}
    ring(cells, rnd, 9, 4.2)
    for x in range(CX - 2, CX + 3):                        # a narrow salty channel to the centre
        cells[x, CY] = ["SaltyWaterPuddle"]
    for _ in range(14):
        x, y = rnd.randrange(W), rnd.randrange(H)
        if not cells[x, y]:
            cells[x, y] = [rnd.choice(["Dogthorn Tree", "Witchwood Tree", "Starapple Tree", "Wire Strand", "Wire Strand"])]
    for xy in [(xy) for xy, o in cells.items() if o == ["Fulcrete"]][::4]:
        cells[xy] = ["Qudzu"]
    for c, xy in (("Goat", (2, 2)), ("Scrap-clad Hermit", (22, 8)), ("Baboon", (4, 7))):
        cells[xy] = [c]
    return cells


def stratum():
    rnd = random.Random("rustwells-cave")
    cells = {(x, y): ["Shale"] for x in range(W) for y in range(H)}
    for y in range(H):
        for x in range(W):
            if math.hypot((x - CX) / 10.5, (y - CY) / 4.6) < 1:
                cells[x, y] = []
    ring(cells, rnd, 8.5, 3.8)
    for y in range(H):                                     # qudzu clings to the cave walls
        for x in range(W):
            if not cells[x, y] and any(cells.get((x + dx, y + dy)) == ["Shale"] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) \
                    and rnd.random() < 0.35:
                cells[x, y] = ["Qudzu"]
    for c, xy in (("Rustacean", (10, 4)), ("Eyeless Crab", (16, 6)), ("Wire Strand", (12, 7)), ("RustLocker", (6, 5)),
                  ("Garbage", (19, 3)), ("Electrofuge", (14, 2)), ("Torchpost", (5, 3))):
        cells[xy] = [c]
    return cells


def fulcrete(name, fg, dt, key):
    """Proposal: fulcrete as bitumen-black with pale gravel (as BrightQud.cs recolours it)."""
    if "Fulcrete" in name:
        return (zm.hex_rgb("#8a857c"), zm.hex_rgb("#2a2826"))
    return None


def main():
    box = (0, 0, W, H)
    s, c = surface(), stratum()
    rows = [
        ("Surface: the well and its fulcrete rings", [
            ("Original game", MR.render(s, "vanilla", box)),
            ("Bright Qud today (0.21.4: canyon rust ground)", MR.render(s, "new", box, ground=flat("rust", "a"), bare=bare("rust"))),
            ("Proposal: rust dust, bitumen-black fulcrete", MR.render(s, "new", box, ground=flat("rustwell", "b"), bare=bare("rustwell"), tone=fulcrete))]),
        ("Lower strata: the pit carved in solid shale", [
            ("Original game", MR.render(c, "vanilla", box)),
            ("Bright Qud today (flat grey stone floor)", MR.render(c, "new", box, ground=torch_lit(stone, c))),
            ("Proposal: dark bitumen floor, gravel and rust flakes", MR.render(c, "new", box, ground=torch_lit(flat("rustcave", "c"), c),
                                                                           bare=bare("rustcave"), tone=fulcrete))]),
    ]
    pw, ph = rows[0][1][0][1].size
    pad, head = 16, 30
    Wd = pad + 3 * (pw + pad)
    out = Image.new("RGB", (Wd, 70 + 2 * (ph + head + 40 + pad) + 120), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '4. Rust Wells - "red qudzu vines take as their trellises chrome wells bored into the earth"', pad, 14,
         Wd - 2 * pad, font(22), (240, 236, 220))
    y = 70
    for title, panels in rows:
        d.text((pad, y), title, font=font(20), fill=(235, 205, 140))
        y += 36
        for i, (label, im) in enumerate(panels):
            x = pad + i * (pw + pad)
            d.text((x, y), label, font=font(16), fill=(225, 215, 185))
            out.paste(im.convert("RGB"), (x, y + head - 6))
        y += ph + head + pad
    wrap(d, "Low contrast, rich small detail. Surface: rust dust with flakes shed by the qudzu ('speckle the ground with "
         "flakes of moisture-sucked rust'). Strata: the fulcrete look ('islands of carbon gravel in an ocean of bitumen') "
         "carried onto the floor. Torch pools as in Red Rock.", pad, y + 6, Wd - 2 * pad, font(16))
    path = os.path.join(zm.OUT, "review_rustwells.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
