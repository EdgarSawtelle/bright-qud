"""Bright Qud master palette (27 colors). One letter per color; '.' is transparent.

Value hierarchy (readability rule): creatures > items > obstacles > floor/water.
Floors live in the darkest band, characters in the brightest/most saturated.
"""

PALETTE = {
    "O": "#10141f",  # outline / ink (also eyes, nostrils)
    "w": "#f4f4e8",  # white (teeth, thorns, eye whites)
    "l": "#a8b0b8",  # steel light
    "L": "#5c6470",  # steel dark / stone
    "s": "#f2b98a",  # skin
    "S": "#c97f5a",  # skin shadow
    "t": "#d8b26a",  # straw / tan / reed light
    "n": "#8a5a32",  # wood / fur
    "N": "#53321c",  # dark wood / hair / boots
    "y": "#ffd23a",  # gold / brass
    "g": "#3fae3a",  # leaf green
    "G": "#8ee05a",  # leaf highlight
    "h": "#1f6b3a",  # leaf shadow
    "b": "#2a62d6",  # cloth / water blue
    "B": "#5fc0ff",  # blue highlight
    "d": "#1b3a7a",  # deep blue
    "r": "#e04a3a",  # red
    "R": "#9a2632",  # dark red
    "m": "#c04ad8",  # magenta
    "M": "#ff8ae8",  # magenta highlight
    "c": "#5ff0e0",  # cyan glow
    "e": "#2a2420",  # dirt dark (floor base)
    "E": "#43372c",  # dirt light (floor specks)
    "p": "#7c7ccc",  # periwinkle: cool crystal shadow (Moon Stair)
    "P": "#4a4888",  # deep blue-violet: crystal deep shade
    "u": "#655238",  # earth shade: soft darker patches (Joppa ground)
    "U": "#857052",  # earth light: soft lighter patches
}

# Cell background the game paints behind every tile: Display.txt color "k".
# Measured in a Deck screenshot as ~(15, 59, 58) under the scanline shader.
BACKGROUND = "#0f3b3a"


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
