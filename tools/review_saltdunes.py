"""Zone review #13 salt dunes + liquid fixes (user test 2026-10-25): today | proposal.

Top: a salt desert patch with a small ruin (table, player). Today the bare cells carry the old dune tile (stripes
from edge to edge that line up into rows: "looks like a wall"), the dune objects are paler squares and the table
and player sit on a brown indoor square. Proposal: the new "dunes" ground family (short ripples, faint cracks)
everywhere, one ivory ground indoors and out.
Bottom: primordial soup in the Rainbow Wood. Today a mushroom in soup stands on plain-looking water and a few
dragged drams fill whole cells; proposal: soup under the mushroom, thin trickles for small amounts.

Usage: .venv/bin/python -I tools/review_saltdunes.py -> mockups/local/zones/review_saltdunes.png (local only)
"""
import colorsys, glob, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import groundsets as G  # noqa: E402
from colors import ramp, hex_rgb, QUD  # noqa: E402

TEX = os.path.join(ROOT, "mod", "BrightQud", "Textures")
REF = os.path.join(ROOT, "reference", "tiles")
OUT = os.path.join(ROOT, "mockups", "local", "zones")
Z = 2


def h(c):
    return hex_rgb(c)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def scale(c, k):
    return tuple(min(255, round(v * k)) for v in c[:3])


def ours(key, fg, det):
    """BrightQud.cs Recolored() with exact rgb colours."""
    p = os.path.join(TEX, key + ".png")
    if not os.path.exists(p):
        return None
    base = Image.open(p).convert("RGBA")
    mp = os.path.join(TEX, "BrightQudMask", key + ".png")
    if os.path.exists(mp):
        mask = Image.open(mp).convert("RGBA")
        bp, mpx = base.load(), mask.load()
        for y in range(base.height):
            for x in range(base.width):
                mr, mg, _, ma = mpx[x, y]
                if ma > 127:
                    bp[x, y] = ramp(fg if mr < 150 else det, round(mg / 127)) + (bp[x, y][3],)
    return base


def vanilla(key, fg, det):
    hits = glob.glob(os.path.join(REF, "assets_content_textures_" + key + ".*"))
    src = Image.open(hits[0]).convert("RGBA")
    out = Image.new("RGBA", src.size)
    sp, op = src.load(), out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, _, _, a = sp[x, y]
            op[x, y] = lerp(fg, det, r / 255) + (a,)
    return out


def tone_liquid(t):
    """BrightQud.cs ToneLiquid: non-blue liquids a little darker and less saturated."""
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.45 < hh < 0.72:
                continue
            rr, gg, bb = colorsys.hsv_to_rgb(hh, s * 0.75, v * 0.72)
            px[x, y] = (round(rr * 255), round(gg * 255), round(bb * 255), a)
    return t


def cellhash(x, y):
    return ((x * 73856093) ^ (y * 19349663)) & 0x7fffffff


def grid_image(w, hgt, draw):
    im = Image.new("RGBA", (w * 16, hgt * 24), (0, 0, 0, 255))
    for y in range(hgt):
        for x in range(w):
            bg, layers = draw(x, y)
            cell = Image.new("RGBA", (16, 24), bg + (255,))
            for t in layers:
                if t is not None:
                    cell.alpha_composite(t)
            im.paste(cell, (x * 16, y * 24))
    return im.resize((w * 16 * Z, hgt * 24 * Z), Image.NEAREST)


# ---------------------------------------------------------------- salt desert
W, H = 22, 9
SALT_DARK, SALT_LIGHT, SALT_SHADOW, INDOOR = h("a2967e"), h("ab9f87"), h("877c66"), h("54402c")
RUIN = {(x, y) for x in range(12, 19) for y in range(3, 7)}
WALL = {(x, y) for x in range(11, 20) for y in range(2, 8)} - RUIN - {(15, 7)}
TABLE, PLAYER = (13, 4), (16, 5)
rnd = random.Random("dunes")
DUNE_OBJ = {(x, y) for x in range(W) for y in range(H) if rnd.random() < 0.06}


def ground(x, y):
    return lerp(SALT_DARK, SALT_LIGHT, (cellhash(x, y) % 5) / 4)


def first(pattern):
    hits = sorted(glob.glob(os.path.join(TEX, pattern)))
    return os.path.splitext(os.path.basename(hits[0]))[0] if hits else None


TABLE_KEY = first("tiles_sw_table*.png") or first("*table*.png")
PLAYER_KEY = "creatures_sw_farmer"
WALL_COL = (h("8a857c"), h("2a2826"))
WALL_KEY = "brightqudwall_rock-1111" if os.path.exists(os.path.join(TEX, "brightqudwall_rock-1111.png")) else first("tiles_tile-0-13.png")
zone_ground = lerp(SALT_DARK, SALT_LIGHT, 0.5)


def salt_today(x, y):
    if (x, y) in WALL:
        return ground(x, y), [ours(WALL_KEY, *WALL_COL)]
    if (x, y) in (TABLE, PLAYER):
        key = TABLE_KEY if (x, y) == TABLE else PLAYER_KEY
        return INDOOR, [ours(key, h(QUD["w"]), h(QUD["W"]))]
    bg = ground(x, y)
    if (x, y) in DUNE_OBJ and (x, y) not in RUIN:
        n = cellhash(x, y) % 12 + 1
        return bg, [ours(f"terrain_sw_ground_dune_{n}", scale(zone_ground, 1.14), scale(zone_ground, 0.86))]
    n = cellhash(x, y) % 12 + 1
    return bg, [ours(f"terrain_sw_ground_dune_{n}", SALT_SHADOW, SALT_SHADOW)]


DUNES = G.tiles("dunes")


def salt_new(x, y):
    bg = lerp(h("a5997f"), h("a89c83"), (cellhash(x, y) % 5) / 4)
    if (x, y) in WALL:
        return bg, [ours(WALL_KEY, *WALL_COL)]
    layers = [DUNES[cellhash(x, y) % 16]]
    if (x, y) in (TABLE, PLAYER):
        key = TABLE_KEY if (x, y) == TABLE else PLAYER_KEY
        layers = [ours(key, h(QUD["w"]), h(QUD["W"]))]
    return bg, layers


# ---------------------------------------------------------------- primordial soup
LW, LH = 14, 6
MOSS = (h("202116"), h("2a2b1c"))
SOUP_TEAL, LAVA = h("2f6e66"), h("d8843c")
SOUP_FG, SOUP_DET = lerp(h(QUD["c"]), SOUP_TEAL, 0.55), lerp(h(QUD["C"]), LAVA, 0.6)
POOL = {(x, y) for x in range(1, 6) for y in range(1, 5) if (x - 3) ** 2 / 6.5 + (y - 2.5) ** 2 / 3 < 1}
SHROOMS = {(2, 2), (4, 3), (3, 1)}
TRAIL = [(6, 3), (7, 3), (8, 3), (8, 2), (9, 2), (10, 2), (11, 2), (11, 3), (12, 3)]


def mask8(cells, x, y, diag=True):
    bits = ""
    for dx, dy in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
        bits += "1" if (x + dx, y + dy) in cells and (diag or dx == 0 or dy == 0) else "0"
    return bits


def blob47(cells, x, y):
    m = list(mask8(cells, x, y))
    for i, (a, b) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (m[a] == "1" and m[b] == "1"):
            m[i] = "0"
    return "".join(m)


def moss(x, y):
    return lerp(*MOSS, (cellhash(x, y) % 7) / 6)


def gunk(x, y):
    return tone_liquid(vanilla("liquids_gunk_deep-" + blob47(POOL, x, y), SOUP_FG, SOUP_DET))


def shroom():
    return ours("creatures_sw_shroom1", h(QUD["R"]), h(QUD["Y"])) or ours("creatures_sw_mushroom", h(QUD["R"]), h(QUD["Y"]))


def soup_today(x, y):
    bg = moss(x, y)
    if (x, y) in POOL:
        if (x, y) in SHROOMS:   # underlay: our shallow-water tile, one colour (the cyan "water" look)
            under = tone_liquid(ours("liquids_water_shallow-" + mask8(POOL, x, y, False), SOUP_FG, SOUP_FG))
            return bg, [under, shroom()]
        return h(QUD["C"]), [gunk(x, y)]
    if (x, y) in TRAIL:
        t = ours("liquids_water_shallow-" + mask8(set(TRAIL) | POOL, x, y, False), SOUP_FG, SOUP_DET)
        return h(QUD["C"]), [tone_liquid(t)]
    return bg, []


def soup_new(x, y):
    bg = moss(x, y)
    if (x, y) in POOL:
        return (bg if (x, y) in SHROOMS else h(QUD["C"])), [gunk(x, y)] + ([shroom()] if (x, y) in SHROOMS else [])
    if (x, y) in TRAIL:
        wet = set(TRAIL) | POOL
        m = sum(b for (dx, dy), b in (((0, -1), 8), ((1, 0), 4), ((0, 1), 2), ((-1, 0), 1)) if (x + dx, y + dy) in wet)
        return bg, [tone_liquid(ours(f"liquids_trickle_{m}", SOUP_FG, SOUP_DET))]
    return bg, []


def main():
    f, fs = font(22), font(16)
    panels = [("Salt desert - today", grid_image(W, H, salt_today)), ("Salt desert - proposal", grid_image(W, H, salt_new)),
              ("Primordial soup - today", grid_image(LW, LH, soup_today)), ("Primordial soup - proposal", grid_image(LW, LH, soup_new))]
    pw = panels[0][1].width
    sw = panels[2][1].width
    gap, top = 24, 44
    out = Image.new("RGB", (pw * 2 + gap * 3, top + panels[0][1].height + top + panels[2][1].height + gap + 60), (24, 26, 30))
    d = ImageDraw.Draw(out)
    for i, (title, im) in enumerate(panels[:2]):
        x = gap + i * (pw + gap)
        d.text((x, 10), title, font=f, fill=(235, 230, 220))
        out.paste(im, (x, top))
    y2 = top + panels[0][1].height + top
    for i, (title, im) in enumerate(panels[2:]):
        x = gap + i * (pw + gap)
        d.text((x, y2 - 34), title, font=f, fill=(235, 230, 220))
        out.paste(im, (x, y2))
    note = ("Dunes: short ripples that end inside each cell, faint cool cracks, same ivory indoors and out "
            "(table and player no longer on a brown square). Soup: mushrooms stand in soup; a few drams = a trickle.")
    d.text((gap, out.height - 46), note, font=fs, fill=(200, 196, 186))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "review_saltdunes.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
