"""Icons for the in-game legend (Options → Mods → "Bright Qud: show legend").

Markers are drawn the same way as Recolor.DrawHud in BrightQud.cs; keep the two in sync.
Icons ship with an empty role mask, so the runtime shows their pixels as they are.
"""
import os
from PIL import Image

HOSTILE, ALLY, PLAYER = (255, 64, 56), (77, 255, 107), (255, 237, 153)
YELLOW, GOLD, WHITE = (255, 217, 51), (255, 209, 64), (255, 255, 255)
INK = (13, 13, 20)
EARTH, INDOOR, STONE = (0x3b, 0x33, 0x26), (0x54, 0x40, 0x2c), (0x2c, 0x2f, 0x35)
BUBBLE = [".ooooo.", "owwwwwo", "owowowo", "owwwwwo", ".owoooo", ".oo...."]
CORNER = ["oooooo", ".wwwwo", "..wwwo", "...wwo", "....wo", ".....o"]
SPARKLE = [(12, 8), (11, 9), (12, 9), (13, 9), (12, 10)]  # (x, row from the bottom)


def ring(px, c, inner=0.62):
    for row in range(19, 24):
        for x in range(16):
            dx, dy = (x - 7.5) / 7, (row - 21.2) / 1.9
            if inner <= dx * dx + dy * dy <= 1.05 and px[x, row][3] < 153:
                px[x, row] = c + (242,)


def stamp(px, rows, x0, c, alpha=255, oalpha=255):
    for r, line in enumerate(rows):
        for x, ch in enumerate(line):
            if ch != ".":
                px[x0 + x, r] = (c + (alpha,)) if ch == "w" else (INK + (oalpha,))


def bar(px, health):
    fill = ALLY if health >= 4 else YELLOW if health >= 2 else HOSTILE
    for x in range(3, 13):
        px[x, 0] = (fill if x - 3 < health * 2 else (15, 20, 31)) + (255,)


def sparkle(px):
    for x, row in SPARKLE:
        px[x, 23 - row] = (255, 255, 217, 255)


def faded(img):
    """Same look as the runtime's 'clearer remembered areas'."""
    import colorsys
    px = img.load()
    K = (0x15, 0x53, 0x52)
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            c = colorsys.hsv_to_rgb(h, s * 0.3, v * 0.72)
            px[x, y] = tuple(round((c[i] * 255) * 0.7 + K[i] * 0.3) for i in range(3)) + (a,)
    return img


def build(textures):
    """textures: the mod's Textures folder (tiles already written). Returns {name: RGBA image}."""
    def tile(key):
        return Image.open(os.path.join(textures, key.replace("/", "_") + ".png")).convert("RGBA")

    def on(ground, img):
        bg = Image.new("RGBA", (16, 24), ground + (255,))
        bg.alpha_composite(img)
        return bg

    icons = {}
    me = tile("brightqudlook/adventurer")
    i = me.copy(); ring(i.load(), PLAYER); icons["player"] = on(EARTH, i)
    i = me.copy(); ring(i.load(), HOSTILE, 0.5); icons["lowhealth"] = on(EARTH, i)
    i = tile("creatures/sw/snapjaw"); ring(i.load(), HOSTILE); icons["enemy"] = on(EARTH, i)
    i = tile("creatures/sw/dog"); ring(i.load(), ALLY); icons["ally"] = on(EARTH, i)
    i = tile("creatures/sw/snapjaw"); bar(i.load(), 2); icons["hurt"] = on(EARTH, i)
    i = tile("items/sw/waterskin") if os.path.exists(os.path.join(textures, "items_sw_waterskin.png")) \
        else tile("tiles/sw/chest")
    sparkle(i.load()); icons["sparkle"] = on(EARTH, i)
    i = tile("creatures/npc-mehmet"); stamp(i.load(), BUBBLE, 0, WHITE); icons["talk"] = on(EARTH, i)
    i = tile("creatures/npc-mehmet"); stamp(i.load(), BUBBLE, 0, (191, 199, 204), 115, 90)
    icons["talked"] = on(EARTH, i)
    i = tile("tiles/sw/chest"); stamp(i.load(), CORNER, 10, GOLD); icons["interact"] = on(EARTH, i)
    icons["solid"] = on(EARTH, tile("items/sw/smallboulder"))
    icons["plant"] = on(EARTH, tile("tiles/tile-brinestalk"))
    icons["wall"] = on(STONE, tile("tiles/wall/rock-00000000"))
    g = Image.new("RGBA", (16, 24), EARTH + (255,))
    g.paste(INDOOR + (255,), (5, 0, 11, 24)); g.paste(STONE + (255,), (11, 0, 16, 24))
    icons["ground"] = g
    icons["memory"] = faded(on(STONE, tile("tiles/wall/rock-00000000")))
    d = Image.new("RGBA", (16, 24), EARTH + (255,))
    d.paste((217, 136, 40, 255), (0, 0, 16, 12)); d.paste((172, 48, 34, 255), (0, 12, 16, 24))
    icons["danger"] = d
    i = tile("creatures/sw/snapjaw")
    fl = ["...y..", "..yy..", ".yoy..", ".yooy.", "yooory", "yoorr.", "oorrr.", ".rrr.."]
    col = {"y": (255, 235, 90), "o": (255, 140, 30), "r": (217, 46, 26)}
    px = i.load()
    for x0, r0 in ((0, 11), (10, 7), (5, 0)):
        for r, line in enumerate(fl):
            for x, ch in enumerate(line):
                if ch != "." and px[x0 + x, r0 + r][3] < 153:
                    px[x0 + x, r0 + r] = col[ch] + (255,)
    icons["fire"] = on(EARTH, i)
    return icons
