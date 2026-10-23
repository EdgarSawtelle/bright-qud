"""Put each character style (art/src/style_*.py) into the same small Joppa-like scene at the Deck's
real 2x zoom, so styles can be compared in context.

Usage: .venv/bin/python -I tools/style_scene.py [ids...] [--out name]
  -> mockups/style_compare_<id>.png for each id (default: all) and the stacked mockups/<name>.png
     (default style_compare_all).
"""
import os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
from style_preview import render_all  # noqa: E402

TEX = os.path.join(ROOT, "mod", "BrightQud", "Textures")
EARTH = (0x3b, 0x33, 0x26)
W, H = 14, 6
STYLES = [("e", "E  Current: big-head caricature"), ("a", "A  Heroic proportions"),
          ("b", "B  Bold silhouette icons"), ("c", "C  Side-view action"), ("d", "D  Tabletop miniatures"),
          ("b1", "B1  True to the creature"), ("b2", "B2  Shape language"), ("b3", "B3  Weird retro sci-fi"),
          ("b4", "B4  Chunky action poses")]
# Where each character stands (x, y) and its ring (None, hostile, ally, player).
CAST = {
    "gunslinger": (5, 3, "player"), "winged": (3, 4, "ally"), "horned": (7, 4, None), "four_arms": (8, 2, None),
    "carapace": (2, 2, None), "mehmet": (1, 1, None), "farmer": (12, 1, None), "snapjaw": (10, 3, "hostile"),
    "snapjaw_hunter": (11, 4, "hostile"), "glowfish": (12, 5, None), "girshling": (9, 5, "hostile"),
    "dog": (6, 5, "ally"), "salthopper": (4, 1, None), "croc": (13, 3, "hostile"),
}
RING = {"hostile": (255, 64, 56), "ally": (77, 255, 107), "player": (255, 237, 153)}


def tex(name):
    p = os.path.join(TEX, name)
    return Image.open(p).convert("RGBA") if os.path.exists(p) else None


def ring(img, c):
    px = img.load()
    for row in range(19, 24):
        for x in range(16):
            dx, dy = (x - 7.5) / 7, (row - 21.2) / 1.9
            if 0.62 <= dx * dx + dy * dy <= 1.05 and px[x, row][3] < 153:
                px[x, row] = c + (242,)


def background():
    rnd = random.Random(4)
    bg = Image.new("RGBA", (W * 16, H * 24), EARTH + (255,))
    deco = [t for t in (tex("terrain_sw_grass1.png"), tex("terrain_sw_grass2.png"), tex("terrain_sw_grass3.png"),
                        tex("terrain_sw_ground_dots1.png")) if t]
    for y in range(H):
        for x in range(W):
            if deco and rnd.random() < 0.55:
                bg.alpha_composite(rnd.choice(deco), (x * 16, y * 24))
    wall = {"l": tex("brightqudwall_wood-0100.png"), "m": tex("brightqudwall_wood-0101.png"),
            "r": tex("brightqudwall_wood-0001.png"), "d": tex("tiles_sw_doorclosed.png")}
    for i, k in enumerate("lmmdmr"):
        if wall[k]:
            bg.alpha_composite(wall[k], ((i + 3) * 16, 0))
    for name, (x, y) in (("terrain_sw_fattree1.png", (0, 4)), ("terrain_sw_starappletree.png", (13, 0)),
                         ("tiles_tile-brinestalk.png", (10, 1)), ("tiles_tile-brinestalk.png", (11, 0))):
        t = tex(name)
        if t:
            bg.alpha_composite(t, (x * 16, y * 24))
    water = tex("liquids_water_deep-11111111.png")
    if water:
        for x, y in ((11, 5), (13, 5), (12, 4), (13, 4)):
            bg.alpha_composite(water, (x * 16, y * 24))
    return bg


def scene(letter, base):
    tiles, errors = render_all("style_" + letter)
    img = base.copy()
    for name, (x, y, r) in CAST.items():
        t = tiles.get(name)
        if t is None:
            continue
        t = t.copy()
        if r:
            ring(t, RING[r])
        img.alpha_composite(t, (x * 16, y * 24))
    return img.resize((W * 32, H * 48), Image.NEAREST), errors


def main():
    args = sys.argv[1:]
    out = "style_compare_all"
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    base = background()
    shots = []
    for letter, title in STYLES:
        if args and letter not in args:
            continue
        img, errors = scene(letter, base)
        for e in errors:
            print(letter, "ERROR", e)
        framed = Image.new("RGB", (img.width + 20, img.height + 46), (24, 24, 28))
        framed.paste(img, (10, 36))
        ImageDraw.Draw(framed).text((10, 8), title, fill=(255, 255, 255), font=font(20))
        framed.save(os.path.join(ROOT, "mockups", f"style_compare_{letter}.png"))
        shots.append(framed)
    allimg = Image.new("RGB", (shots[0].width, sum(s.height for s in shots)), (24, 24, 28))
    y = 0
    for s in shots:
        allimg.paste(s, (0, y))
        y += s.height
    allimg.save(os.path.join(ROOT, "mockups", out + ".png"))
    print("done")


if __name__ == "__main__":
    main()
