"""Zone mood mockups: the same small scene drawn as the original game, Bright Qud now, and a proposed
per-zone palette, by day and as remembered/night cells.

Uses the extracted vanilla tiles (reference/tiles), so the output stays local: mockups/local/zones/.
Usage: .venv/bin/python -I tools/zone_mockup.py [zone ...]
"""
import colorsys, glob, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
from colors import QUD, BRIGHT, hex_rgb, ramp  # noqa: E402

TEX = os.path.join(ROOT, "mod", "BrightQud", "Textures")
REF = os.path.join(ROOT, "reference", "tiles")
OUT = os.path.join(ROOT, "mockups", "local", "zones")
W, H = 14, 7
Z = 2  # Deck zoom

# ---------------------------------------------------------------- tiles


def key_of(tile):
    k = tile.replace("\\", "/").lower()
    if k.startswith("assets_content_textures_"):
        k = k[len("assets_content_textures_"):]
    return os.path.splitext(k)[0].replace("/", "_")


def ref_tile(key):
    hits = glob.glob(os.path.join(REF, "assets_content_textures_" + key + ".*"))
    return Image.open(hits[0]).convert("RGBA") if hits else None


def q(letter):
    return hex_rgb(QUD[letter])


def vanilla(key, fg, detail):
    """Game's 3-color shader: rgb = mix(fg, detail, r), alpha = a."""
    src = ref_tile(key)
    if src is None:
        return None
    f, d = q(fg), q(detail)
    out = Image.new("RGBA", src.size)
    sp, op = src.load(), out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, _, _, a = sp[x, y]
            t = r / 255
            op[x, y] = tuple(round(f[i] + (d[i] - f[i]) * t) for i in range(3)) + (a,)
    return out


def ours(key, fg, detail):
    """BrightQud.cs Recolored(): masked pixels = ramp(brighten(game color), shade)."""
    p = os.path.join(TEX, key + ".png")
    if not os.path.exists(p):
        return None
    base = Image.open(p).convert("RGBA")
    mp = os.path.join(TEX, "BrightQudMask", key + ".png")
    if not os.path.exists(mp):
        return base
    mask = Image.open(mp).convert("RGBA")
    bp, mpx = base.load(), mask.load()
    f, d = hex_rgb(BRIGHT[fg]), hex_rgb(BRIGHT[detail])
    for y in range(base.height):
        for x in range(base.width):
            mr, mg, _, ma = mpx[x, y]
            if ma > 127:
                shade = round(mg / 127)
                bp[x, y] = ramp(f if mr < 150 else d, shade) + (bp[x, y][3],)
    return base


# ---------------------------------------------------------------- colour helpers


def hsv(c):
    return colorsys.rgb_to_hsv(*(v / 255 for v in c[:3]))


def rgb(h, s, v):
    return tuple(round(x * 255) for x in colorsys.hsv_to_rgb(h, max(0, min(1, s)), max(0, min(1, v))))


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def current_ground(paint):
    """BrightQud.cs FromPaint(): same hue, low saturation, value fixed at 0.25."""
    if paint is None:
        return (0x3B, 0x33, 0x26)
    h, s, v = hsv(q(paint))
    if s < 0.15:
        return (0x3B, 0x33, 0x26)
    return rgb(h, min(s, 0.6) * 0.55, 0.25)


def memory_now(img):
    """Default remembered look: teal monochrome (QudColor K scaled by luminance)."""
    k = q("K")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            f = 0.45 + lum * 0.9
            px[x, y] = tuple(min(255, round(c * f)) for c in k) + (a,)
    return img


def memory_new(img, tint, amount=0.2):
    """Proposal: keep each colour's hue at reduced saturation/brightness, pulled toward the zone's
    night/memory tint, so a remembered reef still reads as a reef."""
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            h, s, v = hsv((r, g, b))
            c = rgb(h, s * 0.78, v * 0.86)
            px[x, y] = lerp(c, tint, amount) + (a,)
    return img


def grade(img, hue_rgb, amount):
    """Pull a terrain tile a little toward the zone's key colour (creatures are never graded)."""
    if amount <= 0:
        return img
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = lerp((r, g, b), hue_rgb, amount) + (a,)
    return img


# ---------------------------------------------------------------- scenes
# Legend: char -> (tile, fg, detail, kind). kind: "creature" (never graded), "terrain".
# Ground chars: "." painted dirt, "," painted grass, "~" liquid, " " plain.

ZONES = {}


def zone(name, **kw):
    ZONES[name] = kw


zone(
    "lake_hinnom",
    title="Lake Hinnom - a still, sacred, algae-choked lake",
    paint=("w", "W"),             # Kelpy paints shore grass/dirt tan and yellow
    liquid=("g", "C"),            # algal water: green on pale cyan
    rows=[
        ",,,,M..~~~~~~~",
        ",T,,..~~~e~~~~",
        ",,,.~~~~~~~~c~",
        "M,..~~~p~~~~~~",
        ",,..~~~~~~Pz~~",
        ",@.~~e~~~~~~~~",
        ",,..~~~~~~~~s~",
    ],
    legend={
        "M": ("terrain/sw_mangrove1.bmp", "w", "g", "terrain"),
        "T": ("terrain/sw_fattree2.bmp", "g", "c", "terrain"),
        "P": ("Creatures/sw_palm.bmp", "G", "w", "terrain"),
        "e": ("Creatures/sw_fish_school_1.bmp", "Y", "w", "creature"),
        "c": ("Creatures/sw_clam_1.bmp", "Y", "y", "creature"),
        "p": ("Creatures/sw_fish_school_1.bmp", "Y", "y", "creature"),
        "z": ("Creatures/sw_sultan_croc.bmp", "g", "M", "creature"),
        "s": ("Creatures/sw_svardym_jut.bmp", "G", "w", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    proposal=dict(
        ground=("2c3a22", "3a4628"), speck="b8b07a", liquid="16685a", liquid_detail="9fd84a",
        key="2f8f6a", grade=0.12, night="0c2a2a",
        mood="Deep jade-green algae water with bright lime scum, bone-pale reeds and olive mud. "
             "Humid, still, sacred and a little sickly. White esh and clams are the brightest things.",
    ),
)

zone(
    "palladium_reef",
    title="Palladium Reef - an arcology of bright polyps on old chrome struts",
    paint=("r", "C"),
    liquid=("g", "C"),
    rows=[
        "SSoo~~SSooSS~~",
        "So.f~~So..fS~~",
        "o..h..o.@.oo~~",
        "SS.....b..SS~~",
        "So..t..S..o~~~",
        "oo.u..Soo..j~~",
        "SSoo..SSoo~~~~",
    ],
    legend={
        "S": ("terrain/sw_mangrove2.bmp", "C", "C", "terrain"),
        "o": ("terrain/sw_reef_organic_even_1.bmp", "r", "r", "terrain"),
        "f": ("terrain/sw_reef_organic_even_1.bmp", "r", "R", "terrain"),
        "b": ("terrain/sw_coral_ball_1.bmp", "W", "r", "terrain"),
        "h": ("creatures/sw_reef_hermit.bmp", "r", "y", "creature"),
        "t": ("Creatures/sw_anemone_1.bmp", "m", "W", "creature"),
        "u": ("creatures/sw_cone_snail.bmp", "B", "W", "creature"),
        "j": ("Creatures/sw_jelly.bmp", "Y", "g", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    proposal=dict(
        ground=("1c2050", "2a1f5a"), speck="7fe0ff", liquid="1640a0", liquid_detail="5ad0ff",
        key="5a6cff", grade=0.0, night="141238",
        mood="A jewel box: deep ultramarine/indigo sea-floor so coral pink, orange and gold polyps "
             "and silver-cyan struts glow. Rich, wondrous and dangerous.",
    ),
)

zone(
    "rainbow_wood",
    title="Rainbow Wood - kaleidoscopic fungus, spores and lava-lit primordial soup",
    paint=("c", "C"),             # Mushroomy paints cyan
    liquid=("c", "C"),            # protean gunk pools
    rows=[
        "A..B..C..A,,~~",
        ".,..p.....,~~~",
        "B..D...@..A~~~",
        "..,...,..,..~~",
        "C..A..q..B..D,",
        ".,..,......,..",
        "A..C..B..D..A.",
    ],
    legend={
        "A": ("Creatures/sw_shroom1.bmp", "M", "c", "glow"),
        "B": ("Creatures/sw_shroom3.bmp", "W", "R", "terrain"),
        "C": ("Creatures/sw_shroom1.bmp", "G", "W", "terrain"),
        "D": ("Creatures/sw_shroom3.bmp", "B", "M", "glow"),
        "p": ("Creatures/sw_mushroom.bmp", "R", "M", "creature"),
        "q": ("creatures/sw_slynth.bmp", "g", "m", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    proposal=dict(
        ground=("4a2a18", "5c3620"), speck="5fe0e8", speck_mix=0.25, liquid="1b8a8a", liquid_detail="ff9ae8",
        key="ff8a3a", grade=0.0, night="3a1c2a",
        mood="Option A, lava-lit loam: warm umber ground in the orange light of lava (the game colours the Rainbow Wood amber on the world map), with the game's own cyan fungal grass as tufts. Caps stay full colour; some keep glowing at night.",
    ),
)

zone(
    "rainbow_wood_b",
    title="Rainbow Wood (option B) - kaleidoscopic fungus, spores and lava-lit primordial soup",
    paint=("c", "C"),             # Mushroomy paints cyan
    liquid=("c", "C"),            # protean gunk pools
    rows=[
        "A..B..C..A,,~~",
        ".,..p.....,~~~",
        "B..D...@..A~~~",
        "..,...,..,..~~",
        "C..A..q..B..D,",
        ".,..,......,..",
        "A..C..B..D..A.",
    ],
    legend={
        "A": ("Creatures/sw_shroom1.bmp", "M", "c", "glow"),
        "B": ("Creatures/sw_shroom3.bmp", "W", "R", "terrain"),
        "C": ("Creatures/sw_shroom1.bmp", "G", "W", "terrain"),
        "D": ("Creatures/sw_shroom3.bmp", "B", "M", "glow"),
        "p": ("Creatures/sw_mushroom.bmp", "R", "M", "creature"),
        "q": ("creatures/sw_slynth.bmp", "g", "m", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    proposal=dict(
        ground=("5e5262", "6a5c6a"), speck="f4ecff", speck_mix=0.35, liquid="1b8a8a", liquid_detail="ff9ae8",
        key="e0d0ff", grade=0.0, night="2a2040",
        mood="Option B, mycelium mat: a pale lilac-grey felt of fungus threads with white spore specks, like walking on the inside of a mushroom. Lighter and dreamier; caps pop on it.",
    ),
)

zone(
    "salt_dunes",
    title="Moghra'yi, the salt dunes - an ivory sea frozen in place",
    paint=("Y", "y"),
    liquid=("B", "b"),
    rows=[
        "..............",
        "....d.........",
        "..........h...",
        "...@..........",
        "........h.....",
        "..D...........",
        "..............",
    ],
    legend={
        "d": ("Assets_Content_Textures_Creatures_sw_dromad.bmp", "W", "w", "creature"),
        "D": ("Assets_Content_Textures_Creatures_sw_dromad.bmp", "W", "w", "creature"),
        "h": ("Assets_Content_Textures_Creatures_sw_salthopper.bmp", "Y", "w", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    dune=True,
    proposal=dict(
        ground=("cfc4a4", "bdb397"), speck="9a8fb0", liquid="3fb4ff", liquid_detail="d0f0ff",
        key="e8dcb8", grade=0.0, night="2a2a5a", night_amount=0.3,
        mood="Light ground for once: sun-bleached ivory with lavender shadow ripples. Glaring, empty, "
             "beautiful. Night turns it a cold blue-violet, not black.",
    ),
)

zone(
    "jungle",
    title="Jungle (Kyakukya) - braids of roots, ribbons of fronds, ape-god worshippers",
    paint=("g", "G"),
    liquid=("B", "b"),
    rows=[
        "TT,,W,,TT,,qq,",
        "T,,,,,,,T,,,q,",
        ",,a,,,,,,,,W,,",
        ",W,,,,@,,,,,,T",
        ",,,,,,,,,a,,,T",
        "TT,,q,,,,,,,TT",
        "T,,,qq,,W,,,,T",
    ],
    legend={
        "T": ("terrain/sw_fattree1.bmp", "G", "w", "terrain"),
        "W": ("terrain/sw_talltree1.bmp", "W", "g", "terrain"),
        "q": ("Creatures/sw_qudzu.bmp", "r", "w", "creature"),
        "a": ("Creatures/albino-ape.png", "Y", "w", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    proposal=dict(
        ground=("1a3418", "22401c"), speck="9be05a", liquid="2a62d6", liquid_detail="8fe4f0",
        key="2f7a2a", grade=0.08, night="0c1c14",
        mood="Deep moss-green floor in shade, lime frond specks, so red qudzu and white apes jump out. "
             "Humid and crowded. Deep jungle goes darker still.",
    ),
)

zone(
    "omonporch",
    title="Omonporch - funerary marble arcades at the foot of the maya-blue Spindle",
    paint=("g", "G"),
    liquid=("B", "b"),
    rows=[
        "E,bbbbbbbbbb,E",
        ",,bb,,,,,,bb,,",
        "E,b,,s,,a,,b,E",
        ",,b,,,@,,,,b,,",
        "E,b,,a,,s,,b,E",
        ",,bb,,,,,,bb,,",
        "E,bbbbbbbbbb,E",
    ],
    legend={
        "E": ("Terrain/sw_ueater1.bmp", "W", "w", "terrain"),
        "b": ("tiles/sw_floor_brick1.bmp", "w", "r", "terrain"),
        "s": ("Creatures/sw_flower.bmp", "M", "G", "creature"),
        "a": ("Creatures/sw_flower.bmp", "G", "r", "creature"),
        "@": ("Creatures/sw_gunwing.bmp", "y", "K", "creature"),
    },
    proposal=dict(
        ground=("2a3a2c", "33402e"), speck="8fd08a", liquid="2a62d6", liquid_detail="8fe4f0",
        key="4a7fd8", grade=0.10, night="10183a",
        mood="Overgrown terracotta brick and moss in a cool maya-blue light from the Spindle; gold "
             "statues stay warm. Hallowed, ceremonial, quiet.",
    ),
)

# ---------------------------------------------------------------- Moon Stair (custom scene)
# The game builds giant hexagonal crystals 3 cells wide x 2 tall in a honeycomb (MoonStair.cs) and picks
# one of 25 'cryshex' part tiles per cell (ZoneManager.PaintCrystalWall). Bright Qud has no art for
# them: they are auto-styled cell by cell, which chops each prism into boxes.

MOON_BLOCKS = [(0, 0), (1, 1), (3, 0), (4, 1), (4, 2)]   # (block column n, block row k)
MOON_LIFE = {(7, 4): ("Creatures/sw_pyramid4.bmp", "y", "b"), (2, 5): ("terrain/sw_talltree1.bmp", "C", "y"),
             (12, 5): ("terrain/sw_talltree1.bmp", "y", "K"), (8, 6): ("Creatures/sw_gunwing.bmp", "y", "K")}
MOON_POOLS = {(5, 5), (6, 5), (5, 6), (10, 6)}
INK = (16, 20, 31)


def moon_grid():
    g = [[None] * W for _ in range(H)]
    for i, (n, k) in enumerate(MOON_BLOCKS):
        y0 = k * 2 + n % 2
        for dx in range(3):
            for dy in range(2):
                x, y = n * 3 + dx, y0 + dy
                if x < W and y < H:
                    g[y][x] = "M" if i % 2 == 0 else "Y"
    return g


def cryshex_name(g, x, y):
    """ZoneManager.PaintCrystalWall, ported."""
    def check(cx, cy):
        if cx < 0 or cy < 0 or cx >= W or cy >= H:
            return True
        return g[cy][cx] is not None
    num, num3 = x % 3, (y + (x // 3) % 2) % 2
    table = {(0, 0): ("nw", (x - 1, y + 1), (x - 1, y), (x, y - 1)), (1, 0): ("n", (x - 2, y - 1), (x, y - 1), (x + 2, y - 1)),
             (2, 0): ("ne", (x, y - 1), (x + 1, y), (x + 1, y + 1)), (0, 1): ("sw", (x, y + 1), (x - 1, y), (x - 1, y - 1)),
             (1, 1): ("s", (x + 2, y + 1), (x, y + 1), (x - 2, y + 1)), (2, 1): ("se", (x + 1, y - 1), (x + 1, y), (x, y + 1))}
    part, a, b, c = table[(num, num3)]
    f, f2, f3 = check(*a), check(*b), check(*c)
    if not f2:
        v = "0"
    elif not f3 and not f:
        v = "1"
    elif f and not f3:
        v = "2"
    elif f3 and not f:
        v = "3"
    else:
        return "tiles_cryshex_full"
    return "tiles_cryshex_%s_%s" % (part, v)


def auto_style(t):
    """Approximation of BrightQud.cs Stylize for a flat/wall tile: ink outline where the tile's own
    pixels meet transparency."""
    t = t.copy()
    src = t.load()
    out = t.copy()
    op = out.load()
    for y in range(24):
        for x in range(16):
            if src[x, y][3] < 128:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 16 and 0 <= ny < 24 and src[nx, ny][3] >= 128:
                            op[x, y] = INK + (255,)
    return out


def bright_vanilla(key, fg, detail):
    t = vanilla(key, fg, detail)
    if t is None:
        return None
    f, d = q(fg), q(detail)
    bf, bd = hex_rgb(BRIGHT[fg]), hex_rgb(BRIGHT[detail])
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a:
                # same mix position, brighter endpoints
                tt = 0.0
                den = sum((d[i] - f[i]) ** 2 for i in range(3))
                if den:
                    tt = max(0, min(1, sum(((r, g, b)[i] - f[i]) * (d[i] - f[i]) for i in range(3)) / den))
                px[x, y] = lerp(bf, bd, tt) + (a,)
    return t


def prism(colour, night=False):
    """One giant hex crystal, 48 x 48 px (3 x 2 cells), drawn whole: top face, two side facets,
    inner glow and glints. colour: 'M' magenta or 'Y' pearl."""
    base = {"M": (214, 92, 230), "Y": (226, 232, 255)}[colour]
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    hexagon = [(12, 1), (35, 1), (47, 24), (35, 47), (12, 47), (0, 24)]
    top = [(14, 4), (33, 4), (41, 17), (33, 28), (14, 28), (6, 17)]
    h, sat, v = hsv(base)
    dark, mid, light = rgb(h, sat, v * 0.45), rgb(h, sat * 0.95, v * 0.75), rgb(h, sat * 0.55, min(1, v * 1.1))
    d.polygon(hexagon, fill=mid + (255,))
    d.polygon([(6, 17), (14, 28), (12, 47), (0, 24)], fill=rgb(h, sat, v * 0.6) + (255,))
    d.polygon([(41, 17), (47, 24), (35, 47), (33, 28)], fill=dark + (255,))
    d.polygon([(14, 28), (33, 28), (35, 47), (12, 47)], fill=rgb(h, sat, v * 0.52) + (255,))
    d.polygon(top, fill=light + (255,))
    d.polygon([(18, 8), (29, 8), (35, 17), (29, 24), (18, 24), (12, 17)], fill=lerp(light, (255, 255, 255), 0.35) + (255,))
    d.line([(15, 6), (21, 6)], fill=(255, 255, 255, 255))
    d.line([(8, 18), (12, 12)], fill=(255, 255, 255, 230))
    d.line([(36, 30), (40, 36)], fill=lerp(light, (255, 255, 255), 0.5) + (255,))
    for y in range(48):          # 1 px ink rim on the silhouette only (never between cells)
        for x in range(48):
            pass
    return img


def moon_floor(rnd, mode, colour):
    if mode == "vanilla":
        return q("k")
    if mode == "now":
        return (0x2C, 0x2F, 0x35) if False else current_ground(None)
    return lerp((24, 20, 34), (34, 28, 46), rnd.random())


def build_moon(mode, remembered=False):
    rnd = random.Random("moon")
    g = moon_grid()
    img = Image.new("RGBA", (W * 16, H * 24), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for y in range(H):
        for x in range(W):
            bg = moon_floor(rnd, mode, None)
            cell = Image.new("RGBA", (16, 24), bg + (255,))
            if (x, y) in MOON_POOLS:
                if mode == "new":
                    pool = Image.new("RGBA", (16, 24), (255, 214, 140, 255))
                    pd = ImageDraw.Draw(pool)
                    for _ in range(6):
                        px_, py_ = rnd.randrange(16), rnd.randrange(24)
                        pd.point((px_, py_), fill=(255, 255, 230, 255))
                    cell = Image.blend(cell, pool, 0.55)
                else:
                    t = (vanilla if mode == "vanilla" else ours)(key_of(WATER), "Y", "y" if mode == "vanilla" else "Y")
                    if t:
                        cell.alpha_composite(t)
            elif g[y][x] is None:
                t = (vanilla if mode == "vanilla" else ours)("terrain_sw_hex_dotted_1", "m", "m")
                if t and rnd.random() < 0.7:
                    if mode == "new":
                        t = recolor_to(t, lerp(bg, (120, 70, 140), 0.35), lerp(bg, (120, 70, 140), 0.35))
                    cell.alpha_composite(t)
                if mode == "new" and rnd.random() < 0.35:   # faint white filigree of the black marble
                    cd = ImageDraw.Draw(cell)
                    x0 = rnd.randrange(2, 12)
                    cd.line([(x0, rnd.randrange(4, 20)), (x0 + 3, rnd.randrange(4, 20))], fill=(150, 140, 170, 255))
            if g[y][x] is not None and mode != "new":
                name = cryshex_name(g, x, y)
                colour = g[y][x]
                t = vanilla(name, "K", colour) if mode == "vanilla" else bright_vanilla(name, "K", colour)
                if t is not None:
                    if mode == "now":
                        t = auto_style(t)
                    cell.alpha_composite(t)
                else:
                    print("missing", name)
            if (x, y) in MOON_LIFE:
                tile, fg, dt = MOON_LIFE[(x, y)]
                t = (vanilla if mode == "vanilla" else ours)(key_of(tile), fg, dt)
                if t:
                    cell.alpha_composite(t)
            if remembered and (x, y) != (8, 6):
                cell = memory_now(cell) if mode == "now" else memory_new(cell, (40, 30, 70)) if mode == "new" else cell
            img.alpha_composite(cell, (x * 16, y * 24))
    if mode == "new":
        # whole prisms, drawn over their 3x2 blocks, with a soft glow spilling on the floor
        for i, (n, k) in enumerate(MOON_BLOCKS):
            x0, y0 = n * 3 * 16, (k * 2 + n % 2) * 24
            colour = "M" if i % 2 == 0 else "Y"
            glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gc = {"M": (220, 100, 240), "Y": (210, 220, 255)}[colour]
            gd.ellipse((x0 - 10, y0 + 30, x0 + 58, y0 + 60), fill=gc + (60,))
            img.alpha_composite(glow)
            pr = prism(colour)
            if remembered:
                pr = memory_new(pr, (40, 30, 70))
            # ink rim around the silhouette
            rim = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
            for dx, dy in ((0, 1), (2, 1), (1, 0), (1, 2)):
                rim.alpha_composite(Image.new("RGBA", (48, 48), INK + (255,)), (dx, dy)) if False else None
            mask = pr.split()[3]
            ink = Image.new("RGBA", (48, 48), INK + (255,))
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                img.paste(ink, (x0 + dx, y0 + dy), mask)
            img.alpha_composite(pr, (x0, y0))
    return img.resize((W * 16 * Z, H * 24 * Z), Image.NEAREST)


zone(
    "moon_stair",
    title="Moon Stair - hex prisms bursting from black marble; the Stair purrs",
    custom=build_moon,
    proposal=dict(
        ground=("181422", "221c2e"), speck="785090", liquid="ffd68c", liquid_detail="fffbe6",
        key="d65ce6", grade=0.0, night="281e46",
        mood="Each giant crystal drawn WHOLE (one prism over its 3x2 cells, never chopped into boxes), "
             "faceted magenta or pearl with a glow on the floor; black marble with faint white filigree; "
             "warm static pools glowing gold. Uncanny and holy, the strangest place on the map.",
    ),
)

# ---------------------------------------------------------------- drawing

GRASS = ["terrain/sw_grass1.bmp", "terrain/sw_grass2.bmp", "terrain/sw_grass3.bmp"]
DIRT = ["terrain/sw_ground_dots1.png", "terrain/sw_ground_dots2.png", "terrain/sw_ground_dots3.png"]
DUNE = ["terrain/sw_ground_dune_%d.png" % i for i in range(1, 13)]
WATER = "liquids/water/deep-11111111.png"


def ground_tile(ch, z, rnd):
    if ch == "~":
        return WATER
    if z.get("dune"):
        return rnd.choice(DUNE) if rnd.random() < 0.5 else None
    if ch == ",":
        return rnd.choice(GRASS)
    if ch == ".":
        return rnd.choice(DIRT) if rnd.random() < 0.6 else None
    return None


def under_of(row, x):
    """Ground under an object: the nearest ground character in its row."""
    for d in range(1, len(row)):
        for nx in (x - d, x + d):
            if 0 <= nx < len(row) and row[nx] in ".,~":
                return row[nx]
    return "."


def tone_liquid(t):
    """BrightQud.cs ToneLiquid(): non-blue liquids get 75% saturation, 72% brightness."""
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            h, s, v = hsv((r, g, b))
            if a and not (0.45 < h < 0.72):
                px[x, y] = rgb(h, s * 0.75, v * 0.72) + (a,)
    return t


def build(zname, mode, remembered=False):
    """mode: vanilla | now | new"""
    z = ZONES[zname]
    if z.get("custom"):
        return z["custom"](mode, remembered)
    p = z["proposal"]
    rnd = random.Random(zname)
    img = Image.new("RGBA", (W * 16, H * 24), (0, 0, 0, 255))
    tex = vanilla if mode == "vanilla" else ours
    for y, row in enumerate(z["rows"]):
        for x, ch in enumerate(row):
            paint = z["paint"][rnd.random() < 0.5]
            gt = ground_tile(ch if ch in ".,~ " else under_of(row, x), z, rnd)
            # background
            if mode == "vanilla":
                bg = q("C") if gt == WATER and z["liquid"] == ("g", "C") else q("k")
            elif mode == "now":
                bg = current_ground(paint)
            else:
                a, b = (hex_rgb(c) for c in p["ground"])
                bg = lerp(a, b, 0.5 + (rnd.random() - 0.5) * 0.5)
            cell = Image.new("RGBA", (16, 24), bg + (255,))
            if gt:
                key = key_of(gt)
                if gt == WATER:
                    fg, dt = z["liquid"]
                    if mode == "new":
                        t = ours(key, "B", "b")
                        t = recolor_to(t, hex_rgb(p["liquid"]), hex_rgb(p["liquid_detail"]))
                    else:
                        t = tex(key, fg, dt if mode == "vanilla" else fg)
                        if mode == "now" and t:
                            t = tone_liquid(t)
                else:
                    if mode == "vanilla":
                        t = vanilla(key, paint, "k")
                    elif mode == "now":
                        t = ours(key, paint, paint)
                    else:
                        t = ours(key, paint, paint)
                        if z.get("dune"):
                            t = recolor_to(t, lerp(bg, (255, 250, 235), 0.35), hex_rgb(p["speck"]))
                        else:
                            sp = lerp(hex_rgb(p["speck"]), bg, p.get("speck_mix", 0.45))
                            t = recolor_to(t, sp, sp)
                if t:
                    cell.alpha_composite(t)
            if ch in z["legend"]:
                tile, fg, dt, kind = z["legend"][ch]
                t = tex(key_of(tile), fg, dt)
                if t is None:
                    print("missing", mode, tile)
                else:
                    if mode != "new" and kind == "glow":
                        kind = "terrain"
                    if mode == "new" and kind == "terrain":
                        t = grade(t, hex_rgb(p["key"]), p["grade"])
                    cell.alpha_composite(t)
            glow = ch in z["legend"] and z["legend"][ch][3] == "glow"
            if remembered and ch != "@" and not (mode == "new" and glow):
                if mode == "now":
                    cell = memory_now(cell)
                elif mode == "new":
                    cell = memory_new(cell, hex_rgb(p["night"]), p.get("night_amount", 0.2))
            img.alpha_composite(cell, (x * 16, y * 24))
    return img.resize((W * 16 * Z, H * 24 * Z), Image.NEAREST)


def recolor_to(t, light, dark, keep_alpha=False):
    """Map a ground/water tile's pixels onto a two-colour ramp by brightness."""
    if t is None:
        return None
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a:
                v = hsv((r, g, b))[2]
                px[x, y] = lerp(dark, light, min(1, v * 1.3)) + (a,)
    return t


def sheet(zname):
    z = ZONES[zname]
    panels = [("Original game", build(zname, "vanilla")), ("Bright Qud now", build(zname, "now")),
              ("Proposal", build(zname, "new")),
              ("Now: remembered / night", build(zname, "now", True)),
              ("Proposal: remembered / night (lighter)", build(zname, "new", True))]
    pw, ph = panels[0][1].size
    pad, head = 16, 34
    cols = 3
    sw = pad + cols * (pw + pad)
    sh = 60 + 2 * (ph + head + pad) + 70
    out = Image.new("RGB", (sw, sh), (24, 24, 28))
    d = ImageDraw.Draw(out)
    d.text((pad, 14), z["title"], font=font(26), fill=(240, 236, 220))
    for i, (label, img) in enumerate(panels):
        c, r = i % cols, i // cols
        if i >= 3:
            c = i - 3
        x = pad + c * (pw + pad)
        y = 60 + r * (ph + head + pad)
        d.text((x, y), label, font=font(18), fill=(200, 200, 190))
        out.paste(img.convert("RGB"), (x, y + head - 6))
    # swatches + mood in the free slot
    p = z["proposal"]
    x = pad + 2 * (pw + pad)
    y = 60 + (ph + head + pad)
    d.text((x, y), "Proposed palette", font=font(18), fill=(200, 200, 190))
    sw_cols = [("ground", p["ground"][0]), ("ground 2", p["ground"][1]), ("specks", p["speck"]),
               ("liquid", p["liquid"]), ("liquid hi", p["liquid_detail"]), ("key light", p["key"]),
               ("night", p["night"])]
    for i, (n, hx) in enumerate(sw_cols):
        bx = x + i * 62
        d.rectangle((bx, y + 30, bx + 54, y + 84), fill=hex_rgb(hx), outline=(90, 90, 90))
        d.text((bx, y + 88), n, font=font(12), fill=(180, 180, 170))
    wrap(d, p["mood"], x, y + 116, pw, font(16))
    path = os.path.join(OUT, zname + ".png")
    out.save(path)
    return path


def wrap(d, text, x, y, width, f):
    line = ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=f) > width:
            d.text((x, y), line, font=f, fill=(225, 220, 205))
            y += 22
            line = word
        else:
            line = trial
    if line:
        d.text((x, y), line, font=f, fill=(225, 220, 205))


def main():
    os.makedirs(OUT, exist_ok=True)
    for zname in sys.argv[1:] or ZONES:
        print(sheet(zname))


if __name__ == "__main__":
    main()
