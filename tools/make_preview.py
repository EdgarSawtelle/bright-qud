"""Build mod/BrightQud/preview.png (512x512) from the mod's own tiles only.

Never reads from reference/ (original game art). Run with:
    .venv/bin/python -I tools/make_preview.py

Map markers (feet rings, health bar, speech bubble) are drawn on the native
16x24 tile before scaling, using the same geometry as the game's markers.
"""
import glob
import os
import random
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "mod", "BrightQud", "Textures")
OUT = os.path.join(ROOT, "mod", "BrightQud", "preview.png")

SIZE = 512
SCALE = 3
NATIVE = (16, 24)
CELL = (NATIVE[0] * SCALE, NATIVE[1] * SCALE)  # 48x72
GROUND = (0x3B, 0x33, 0x26, 255)
OUTLINE = (0x10, 0x14, 0x1F, 255)
SCENE_TOP = 120  # tile rows start below the title band
COLS = 10
ROWS = 5
GRID_X = (SIZE - COLS * CELL[0]) // 2  # 16px side gutters

RED = (255, 64, 56, 255)
GREEN = (77, 255, 107, 255)
WARM = (255, 237, 153, 255)
HP_FULL = (255, 217, 51, 255)
HP_EMPTY = (15, 20, 31, 255)
WHITE = (255, 255, 255, 255)
BUBBLE_DARK = (13, 13, 20, 255)

BUBBLE = [
    ".ooooo.",
    "owwwwwo",
    "owowowo",
    "owwwwwo",
    ".owoooo",
    ".oo....",
]


def tex_path(pattern):
    hits = sorted(glob.glob(os.path.join(TEX, pattern)))
    return hits[0] if hits else None


def load_native(pattern):
    """Load a texture as RGBA at native size, or None if it is missing."""
    path = tex_path(pattern)
    if path is None:
        print(f"skip (missing): {pattern}")
        return None
    return Image.open(path).convert("RGBA")


def ring(tile, color):
    """Feet ring: paint where the creature is transparent-ish (alpha < 153)."""
    px = tile.load()
    for row in range(19, 24):
        for x in range(16):
            dx = (x - 7.5) / 7
            dy = (row - 21.2) / 1.9
            d = dx * dx + dy * dy
            if 0.62 <= d <= 1.05 and px[x, row][3] < 153:
                px[x, row] = color


def health_bar(tile, fraction_px=4):
    px = tile.load()
    for x in range(3, 13):
        px[x, 0] = HP_FULL if x - 3 < fraction_px else HP_EMPTY


def ring_with_health(tile, color):
    ring(tile, color)
    health_bar(tile, fraction_px=4)


def speech_bubble(tile):
    colors = {"w": WHITE, "o": BUBBLE_DARK, ".": None}
    px = tile.load()
    for y, line in enumerate(BUBBLE):
        for x, ch in enumerate(line):
            if colors[ch] is not None:
                px[x, y] = colors[ch]


def place(canvas, pattern, col, row, marker=None, **marker_kw):
    tile = load_native(pattern)
    if tile is None:
        return
    if marker is not None:
        marker(tile, **marker_kw)
    big = tile.resize(CELL, Image.NEAREST)
    canvas.alpha_composite(big, (GRID_X + col * CELL[0], SCENE_TOP + row * CELL[1]))


def load_font(size):
    candidates = ["/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]
    try:
        out = subprocess.run(["fc-list", ":", "file"], capture_output=True,
                             text=True, timeout=10).stdout
        candidates += [line.split(":")[0].strip() for line in out.splitlines()
                       if line.strip().lower().endswith((".ttf", ".otf"))]
    except Exception:
        pass
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def main():
    canvas = Image.new("RGBA", (SIZE, SIZE), GROUND)
    rng = random.Random(7)  # fixed seed: the preview is reproducible

    # Hand-placed layout: (col, row) per object.
    trees = [(0, 0, "terrain_sw_fattree1.png"), (9, 0, "terrain_sw_starappletree.png")]
    wall = [(3, 1, "brightqudwall_wood-0100.png"), (4, 1, "brightqudwall_wood-0101.png"),
            (5, 1, "tiles_sw_doorclosed.png"), (6, 1, "brightqudwall_wood-0101.png"),
            (7, 1, "brightqudwall_wood-0001.png")]
    pond = [(7, 2, "liquids_water_deep-11111111.png"), (8, 2, "liquids_water_deep-11111111.png"),
            (7, 3, "liquids_water_deep-11111111.png"), (8, 3, "liquids_water_deep-11111111.png")]
    plants = [(6, 2, "tiles_sw_watervine1.png"), (6, 3, "tiles_sw_watervine1.png"),
              (9, 2, "tiles_tile-brinestalk.png")]
    items = [(0, 4, "items_sw_shortblade_1.png"), (3, 3, "items_sw_injector.png"),
             (7, 4, "tiles_sw_chest.png")]

    occupied = {(c, r) for c, r, _ in trees + wall + pond + plants + items}
    creatures = [
        (1, 2, "creatures_sw_snapjaw.png", ring_with_health, {"color": RED}),
        (2, 4, "creatures_sw_goatfolk.png", ring, {"color": RED}),
        (4, 3, "brightqudlook_adventurer.png", ring, {"color": WARM}),
        (5, 4, "creatures_sw_dog.png", ring, {"color": GREEN}),
        (9, 1, "creatures_npc-mehmet.png", speech_bubble, {}),
    ]
    occupied |= {(c, r) for c, r, *_ in creatures}

    # Grass and floor dots on most empty cells.
    for row in range(ROWS):
        for col in range(COLS):
            if (col, row) in occupied or rng.random() < 0.2:
                continue
            if rng.random() < 0.7:
                pat = rng.choice(["terrain_sw_grass1.png", "terrain_sw_grass2.png",
                                  "terrain_sw_grass3.png"])
            else:
                pat = "terrain_sw_ground_dots1.png"
            place(canvas, pat, col, row)

    for c, r, pat in trees + wall + pond + plants + items:
        place(canvas, pat, c, r)
    for c, r, pat, marker, kw in creatures:
        place(canvas, pat, c, r, marker=marker, **kw)

    # Darker translucent band behind the title.
    band_h = SCENE_TOP - 6
    band = Image.new("RGBA", (SIZE, band_h), (16, 20, 31, 170))
    canvas.alpha_composite(band, (0, 0))

    draw = ImageDraw.Draw(canvas)
    title_font = load_font(60)
    sub_font = load_font(20)

    def outlined(xy, text, font, fill, width):
        x, y = xy
        for dx in (-width, 0, width):
            for dy in (-width, 0, width):
                if dx or dy:
                    draw.text((x + dx, y + dy), text, font=font, fill=OUTLINE, anchor="ma")
        draw.text((x, y), text, font=font, fill=fill, anchor="ma")

    outlined((SIZE // 2, 8), "Bright Qud", title_font, WHITE, width=4)
    draw.text((SIZE // 2, 80), "bold, bright & readable", font=sub_font,
              fill=(255, 214, 102, 255), anchor="ma")

    canvas.convert("RGB").save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {canvas.size}")


if __name__ == "__main__":
    main()
