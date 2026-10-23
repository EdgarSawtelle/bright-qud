"""Mockups for review: zoomed tile sheet and a Joppa scene redrawn over the user's Deck screenshot.

Outputs go to mockups/. They may include the user's own game screenshot, so they stay local.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "art", "src"))
import build_tiles as B  # noqa: E402
import palette  # noqa: E402
import tiles  # noqa: E402


def all_tiles(v):
    """name -> RGBA tile for mockups, with the colors the game gives the Joppa objects."""
    S = tiles.SPRITES
    spec = {
        "player": (S["gunwing"], "object", "y", "K"), "farmer": (S["farmer"], "object", "y", "g"),
        "farmer_yellow": (S["farmer"], "object", "W", "g"), "farmer_white": (S["farmer"], "object", "Y", "g"),
        "farmer_cyan": (S["farmer"], "object", "C", "b"), "snapjaw": (S["snapjaw"], "object", "w", "R"),
        "glowfish": (S["glowfish"], "object", "m", "C"), "tree": (S["tree"], "tall", "G", "w"),
        "chest": (S["chest"], "object", "w", "W"), "torch": (S["torch_lit"], "object", "R", "w"),
        "watervine": (S["watervine"], "terrain", "w", "g"), "grass": (tiles.grass(2), "terrain", "g", "k"),
        "floor": (tiles.floor(1), "terrain", "w", "w"), "ground": (tiles.ground(1), "terrain", "w", "k"),
        "water": (tiles.water("11111111"), "terrain", "B", "b"), "wall": (tiles.wall("00000000"), "terrain", "w", "y"),
        "wall_top": (tiles.wall("10001000"), "terrain", "w", "y"), "door": (tiles.door(), "terrain", "w", "y"),
    }
    return {n: B.render(g, k, v, fg, d) for n, (g, k, fg, d) in spec.items()}

OUT = os.path.join(ROOT, "mockups")
BG = palette.rgb(palette.BACKGROUND)
EARTH = (0x3b, 0x33, 0x26)    # BrightQud.cs Ground: outdoor earth
INDOOR = (0x54, 0x40, 0x2c)   # BrightQud.cs Ground: enclosed rooms
SHEET_ORDER = ["player", "farmer", "farmer_yellow", "farmer_cyan", "glowfish", "chest", "snapjaw", "glowfish", "floor", "wall", "wall_top", "door",
               "watervine", "grass", "water", "tree", "chest", "torch", "ground"]
SHEET_ORDER.insert(4, "snapjaw")
SHEET_ORDER = list(dict.fromkeys(SHEET_ORDER))


def font(size):
    for p in ("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/noto/NotoSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def tile_sheet(scale=4, variants=None):
    cw, ch = 16 * scale, 24 * scale
    pad, head = 10, 36
    cols = len(SHEET_ORDER)
    w = pad + cols * (cw + pad)
    variants = variants or {B.CHOSEN: B.VARIANTS[B.CHOSEN]}
    h = len(variants) * (ch + head + pad) + pad
    sheet = Image.new("RGB", (w, h), (30, 30, 34))
    d = ImageDraw.Draw(sheet)
    y = pad
    for key, v in variants.items():
        d.text((pad, y + 4), v["label"], fill=(235, 235, 235), font=font(20))
        y += head
        ts = all_tiles(v)
        for i, name in enumerate(SHEET_ORDER):
            x = pad + i * (cw + pad)
            cell = Image.new("RGBA", (16, 24), EARTH + (255,))
            cell.alpha_composite(ts[name])
            sheet.paste(cell.resize((cw, ch), Image.NEAREST), (x, y))
        y += ch + pad
    d.text((pad, h - 4), "", fill=(0, 0, 0))
    return sheet


# --- Joppa scene, traced cell-by-cell from the user's Deck screenshot (2x zoom, 29x12 cells visible) ---
SHOT = os.path.join(ROOT, "reference", "screens", "Screenshot_20261018_134948.png")
GRID_X0, GRID_Y0, CELL_W, CELL_H = 19.5 - 31.85, 113.2, 31.85, 47.8  # column 0 starts off-screen left
MAP_BOX = (0, 112, 903, 688)
# . ground  : dirt path  " grass  V watervine  ~ water  # wall  + door  T torch  @ player  f farmer
def _build_scene():
    """(row, col) annotations read off the screenshot with a cell-grid overlay."""
    g = [["."] * 29 for _ in range(12)]
    for r in range(12):  # dirt path running north-south through the middle
        for c in range(12, 17):
            g[r][c] = ":"
    for r, c in [(2, 22), (2, 23), (2, 24), (2, 25), (2, 26), (2, 27), (3, 17), (3, 18), (3, 19), (3, 20),
                 (3, 21), (3, 22), (3, 23), (6, 3), (6, 4), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
                 (7, 9), (7, 10), (8, 10), (8, 11), (0, 27), (1, 27), (1, 17)]:
        g[r][c] = ":"
    for r, c in [(0, 18), (0, 20), (0, 25), (0, 26), (1, 20), (1, 24), (1, 26), (2, 11), (2, 20), (3, 11),
                 (4, 18), (4, 20), (5, 4), (5, 18), (6, 0), (6, 5), (6, 6), (8, 2), (8, 4), (8, 18), (8, 20),
                 (8, 22), (8, 23), (9, 2), (9, 5), (9, 7), (9, 17), (9, 20), (9, 21), (9, 28), (10, 3),
                 (10, 6), (10, 10), (10, 20), (10, 21)]:
        g[r][c] = '"'
    vine = [(3, 25), (3, 26), (6, 27), (6, 28), (7, 23), (7, 28)]
    vine += [(4, c) for c in range(21, 29)] + [(5, c) for c in range(20, 29)]
    vine += [(6, c) for c in range(19, 24)] + [(8, c) for c in range(25, 29)]
    for r, c in vine:
        g[r][c] = "V"
    for r, c in [(6, 24), (6, 25), (6, 26), (7, 25), (7, 26), (7, 27)]:
        g[r][c] = "~"
    for r, c in [(1, 10), (2, 10), (4, 10), (5, 8), (5, 9), (5, 10)]:
        g[r][c] = "#"
    g[3][10] = "+"
    g[1][12] = g[7][17] = "T"
    g[1][21], g[5][19], g[7][24] = "c", "y", "w"  # three villagers, colored as in the game
    g[8][14] = "@"
    return ["".join(r) for r in g]


# . ground  : dirt path  " grass  V watervine  ~ water  # wall  + door  T torch  @ player  f farmer
SCENE = _build_scene()
SYMBOL = {":": "floor", '"': "grass", "V": "watervine", "~": "water", "+": "door", "T": "torch",
          "@": "player", "f": "farmer",
          "y": "farmer_yellow", "w": "farmer_white", "c": "farmer_cyan", ".": "ground"}


def scene_layer(v, scene=SCENE):
    ts = all_tiles(v)
    shot = Image.open(SHOT).convert("RGBA")
    layer = Image.new("RGBA", shot.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle(MAP_BOX, fill=EARTH + (255,))
    for r, row in enumerate(scene):
        for c, ch in enumerate(row):
            if ch == "#":
                below = scene[r + 1][c] if r + 1 < len(scene) else "."
                name = "wall_top" if below in "#+" else "wall"
            else:
                name = SYMBOL[ch]
            x, y = round(GRID_X0 + c * CELL_W), round(GRID_Y0 + r * CELL_H)
            layer.alpha_composite(ts[name].resize((32, 48), Image.NEAREST), (max(x, 0), y),
                                  (max(0, -x), 0))
    clip = Image.new("L", shot.size, 0)
    ImageDraw.Draw(clip).rectangle(MAP_BOX, fill=255)
    shot.paste(layer, (0, 0), Image.composite(layer, Image.new("RGBA", shot.size), clip).getchannel("A"))
    return shot.convert("RGB")


def labeled(img, text):
    out = Image.new("RGB", (img.width, img.height + 40), (30, 30, 34))
    out.paste(img, (0, 40))
    ImageDraw.Draw(out).text((10, 8), text, fill=(235, 235, 235), font=font(22))
    return out


def side_by_side(*imgs, gap=12):
    w = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    out = Image.new("RGB", (w, max(i.height for i in imgs)), (30, 30, 34))
    x = 0
    for i in imgs:
        out.paste(i, (x, 0))
        x += i.width + gap
    return out


def stacked(*imgs, gap=12):
    h = sum(i.height for i in imgs) + gap * (len(imgs) - 1)
    out = Image.new("RGB", (max(i.width for i in imgs), h), (30, 30, 34))
    y = 0
    for i in imgs:
        out.paste(i, (0, y))
        y += i.height + gap
    return out


def legend(v, scale=3):
    """Walkability legend: one example per tier, labeled."""
    ts = all_tiles(v)
    tiers = [
        ("BLOCKS YOU", "raised block, dark base", ["wall", "wall_top"]),
        ("DOOR (walkable)", "plank face set in a wall", ["door"]),
        ("WALK-THROUGH, blocks sight", "outline, no drop shadow", ["tree"]),
        ("CREATURES & ITEMS", "outline + drop shadow", ["player", "snapjaw", "chest", "torch"]),
        ("OPEN GROUND", "flat, no outline", ["floor", "grass", "watervine", "ground", "water"]),
    ]
    cw, ch, pad = 16 * scale, 24 * scale, 10
    width = pad + max(len(t[2]) for t in tiers) * (cw + pad) + 420
    out = Image.new("RGB", (width, pad + len(tiers) * (ch + pad)), (30, 30, 34))
    d = ImageDraw.Draw(out)
    for r, (title, sub, names) in enumerate(tiers):
        y = pad + r * (ch + pad)
        for i, n in enumerate(names):
            cell = Image.new("RGBA", (16, 24), BG + (255,))
            cell.alpha_composite(ts[n])
            out.paste(cell.resize((cw, ch), Image.NEAREST), (pad + i * (cw + pad), y))
        tx = pad + max(len(t[2]) for t in tiers) * (cw + pad) + 10
        d.text((tx, y + 14), title, fill=(240, 240, 240), font=font(22))
        d.text((tx, y + 44), sub, fill=(170, 175, 180), font=font(18))
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    v = B.VARIANTS[B.CHOSEN]
    tile_sheet().save(os.path.join(OUT, "tilesheet.png"))
    legend(v).save(os.path.join(OUT, "walkability_legend.png"))
    before = Image.open(SHOT).convert("RGB")
    after = scene_layer(v)
    after.save(os.path.join(OUT, "joppa_after_fullscreen.png"))
    box = (560, 140, 903, 520)
    zoom = lambda im: im.crop(box).resize(((box[2] - box[0]) * 2, (box[3] - box[1]) * 2), Image.NEAREST)
    side_by_side(labeled(before.crop(MAP_BOX), "BEFORE  original game (your screenshot)"),
                 labeled(after.crop(MAP_BOX), "AFTER  style C, caricature characters")).save(
        os.path.join(OUT, "compare_before_after.png"))
    side_by_side(labeled(zoom(before), "BEFORE (close-up)"), labeled(zoom(after), "AFTER (close-up)")).save(
        os.path.join(OUT, "closeup_before_after.png"))
    print("ok")
