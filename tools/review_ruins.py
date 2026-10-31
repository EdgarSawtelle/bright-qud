"""Zone review #15 Ruins, baroque ruins, rusted archway. Ruins are built by the game from Fulcrete (BuildingZoneTemplate);
baroque ruins roll one of five wall materials per region (HighTierRegionRuinWalls). Scenes are ruined rooms from those
objects: original, Bright Qud today, proposal. Local output only.

Usage: .venv/bin/python -I tools/review_ruins.py -> mockups/local/zones/review_ruins.png
"""
import os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import colors as C  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

W, H = 26, 10
MAT = {"Fulcrete": "fulcrete", "EbonFulcrete": "fulcrete", "Mudroot": "mudroot", "Shale": "shale", "CrysteelPlatedWall": "crysteel",
       "Star Orchid Marble": "starorchid", "MachineWallColdTubing": "tubing", "MachineWallHotTubing": "tubing"}
# name -> (roles 1-3 colour, roles 4-6 colour), as Ground.Apply will set them
TONE = {"Fulcrete": ("8a857c", "2a2826"), "EbonFulcrete": ("4a4844", "1e1d1c"), "Mudroot": ("6e5a3e", "3f4a2e"), "Shale": ("743028", "4c201c"),
        "CrysteelPlatedWall": ("7ca394", "3f5f55"), "Star Orchid Marble": ("8e4a72", "a2949a"),
        "MachineWallColdTubing": ("8f8a7e", "3f8a96"), "MachineWallHotTubing": ("8f8a7e", "96492f")}


def scene(wall, seed, extra=()):
    r = random.Random(seed)
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for (x0, y0, x1, y1) in ((1, 1, 10, 6), (12, 3, 20, 9), (22, 0, 25, 5)):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x in (x0, x1) or y in (y0, y1)) and r.random() > 0.2:
                    c[x, y] = [wall]
    empty = [k for k, v in c.items() if not v]
    r.shuffle(empty)
    for name in ("Rubble Grey", "Rubble Grey", "Rubble Grey") + tuple(extra):
        c[empty.pop()] = [name]
    return c


def mask(name, x, y, cells):
    same = lambda dx, dy: any(MAT.get(o) == MAT[name] for o in cells.get((x + dx, y + dy), []))
    return "".join("1" if same(*d) else "0" for d in ((0, -1), (1, 0), (0, 1), (-1, 0)))


def swap(name, x, y, cells):
    if name not in MAT:
        return None
    if name == "Fulcrete":                                 # only surface ruins are vine-swathed
        return "brightqudwall_vinefulcrete-" + mask(name, x, y, cells)
    return f"brightqudwall_{MAT[name]}-" + mask(name, x, y, cells)




def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


LAST = [None]


def real(name, t):
    """Rebuilds the swapped wall from its mask, as Recolor.Recolored does: masked pixels follow the two colours, fixed
    pixels (vines, gold) stay. The Rust role tiles keep their ink edge."""
    if name not in TONE or not LAST[0]:
        return t
    tex = os.path.join(ROOT, "mod/BrightQud/Textures")
    im = Image.open(os.path.join(tex, LAST[0] + ".png")).convert("RGBA")
    mask = Image.open(os.path.join(tex, "BrightQudMask", LAST[0] + ".png")).convert("RGBA")
    fg, det = (hexrgb(c) for c in TONE[name])
    a, m = im.load(), mask.load()
    for y in range(im.height):
        for x in range(im.width):
            if m[x, y][3] > 127:
                a[x, y] = tuple(C.ramp(fg if m[x, y][0] < 150 else det, round(m[x, y][1] / 127))) + (a[x, y][3],)
    return im.resize(t.size, Image.NEAREST)


def recording(name, x, y, cells):
    LAST[0] = swap(name, x, y, cells)
    return LAST[0]


def panel(c, fam, new):
    box = (0, 0, W, H)
    if new:
        return MR.render(c, "new", box, ground=flat(fam, "b"), bare=bare(fam), swap=recording, post=real)
    return MR.render(c, "new", box, ground=flat(fam, "a"), bare=bare(fam))


def main():
    ruins = scene("Fulcrete", "ruins", ("Sawhander", "ChaingunTurret", "Dogthorn Tree"))
    rows = [("Ruins (Fulcrete): today", panel(ruins, "earth", False)), ("Ruins: proposal", panel(ruins, "ruins", True))]
    for wall, label in (("CrysteelPlatedWall", "Baroque: crysteel"), ("Star Orchid Marble", "Baroque: star orchid marble"),
                        ("MachineWallColdTubing", "Baroque: machine wall"), ("EbonFulcrete", "Baroque: ebon fulcrete")):
        rows.append((label, panel(scene(wall, wall, ("Galgal",)), "deepjungle", True)))
    arch = scene("Shale", "arch", ("Dogthorn Tree", "Witchwood Tree"))
    rows.append(("Rusted archway: game text 'an arc of rust'", panel(arch, "rust", False)))
    rows.append(("Rusted archway: with the canyons' new shale (0.23.1), rust ground kept", panel(arch, "rust", True)))
    pw, ph = rows[0][1].size
    pad = 14
    cols = 2
    n = (len(rows) + 1) // 2
    out = Image.new("RGB", (pad + cols * (pw + pad), 60 + n * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '15. Ruins - "the mysterious Eaters\' vine-swathed works"', pad, 12, out.width - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        x, y = pad + (i % 2) * (pw + pad), 54 + (i // 2) * (ph + 32)
        d.text((x, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (x, y + 24))
    path = os.path.join(zm.OUT, "review_ruins.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
