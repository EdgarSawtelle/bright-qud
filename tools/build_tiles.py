"""Render text pixel grids (art/src) to RGBA tiles plus role masks for the runtime recolor."""
import colorsys, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "art", "src"))
from PIL import Image  # noqa: E402
import colors, palette  # noqa: E402

N4 = ((0, -1), (1, 0), (0, 1), (-1, 0))
N8 = N4 + ((1, -1), (1, 1), (-1, 1), (-1, -1))

CHOSEN = "C_chunky"  # picked by the user at CHECKPOINT 1

# Style variants offered at CHECKPOINT 1. Same source art, different pipeline settings.
VARIANTS = {
    "A_bold": {"label": "A  Bold - crisp dark outline", "outline": "ink", "nbhd": N4, "sat": 1.0, "light": 1.0, "shadow": False},
    "B_soft": {"label": "B  Soft - colored outline, gentler palette", "outline": "selout", "nbhd": N4, "sat": 0.82, "light": 1.06, "shadow": False},
    "C_chunky": {"label": "C  Chunky - thick outline + drop shadow, max color", "outline": "ink", "nbhd": N8, "sat": 1.15, "light": 1.0, "shadow": True},
}

SHADOW_ALPHA = 120   # 'x' ground shadow
DROP_ALPHA = 110     # drop shadow (variant C)


def adjust(rgb, sat, light):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    r, g, b = colorsys.hls_to_rgb(h, min(1, l * light), min(1, s * sat))
    return (round(r * 255), round(g * 255), round(b * 255))


def darken(rgb, f=0.45):
    return tuple(round(c * f) for c in rgb)


def render(grid, kind, v=None, fg="y", detail="g", with_mask=False):
    """grid -> RGBA tile; digits take the given game colors (letters from colors.QUD).

    with_mask=True also returns the role mask: R = 100 (foreground) / 200 (detail),
    G = shade 0/127/254 (light/mid/dark), A = 255 on recolorable pixels.
    """
    v = v or VARIANTS[CHOSEN]
    assert len(grid) == 24 and all(len(r) == 16 for r in grid), "tiles must be 16x24"
    pal = {k: adjust(palette.rgb(h), v["sat"], v["light"]) for k, h in palette.PALETTE.items()}
    ink = pal["O"]
    img = Image.new("RGBA", (16, 24), (0, 0, 0, 0))
    mask = Image.new("RGBA", (16, 24), (0, 0, 0, 0))
    px, mpx = img.load(), mask.load()
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "x":
                px[x, y] = ink + (SHADOW_ALPHA,)
            elif ch in colors.ROLE_DIGITS:
                px[x, y] = colors.role_color(ch, fg, detail) + (255,)
                which, shade = colors.ROLE_DIGITS[ch]
                mpx[x, y] = (100 if which == "fg" else 200, shade * 127, 0, 255)
            elif ch != ".":
                px[x, y] = pal[ch] + (255,)
    if kind != "terrain":
        solid = {(x, y) for y in range(24) for x in range(16) if px[x, y][3] == 255}
        out = img.copy()
        opx = out.load()
        if v["shadow"] and kind == "object":
            for x, y in solid:
                for dx, dy in ((1, 1), (2, 2)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 16 and 0 <= ny < 24 and (nx, ny) not in solid:
                        opx[nx, ny] = ink + (DROP_ALPHA,)
        for x, y in solid:
            for dx, dy in v["nbhd"]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 16 and 0 <= ny < 24 and (nx, ny) not in solid and grid[ny][nx] != "x":
                    # Walk-through plants (tall) get a soft outline in their own darker shade: black
                    # ink is reserved for things you interact with (creatures, items, furniture).
                    soft = v["outline"] != "ink" or kind == "tall"
                    opx[nx, ny] = (darken(px[x, y][:3]) if soft else ink) + (255,)
        img = out
    return (img, mask) if with_mask else img
