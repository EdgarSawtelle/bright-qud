"""Color logic shared by the Python build and the C# runtime (mod/BrightQud/BrightQud.cs).

Keep the two in sync: QUD, BRIGHT and ramp() are mirrored in C#.

Sprites mark recolorable pixels with digits:
    1 2 3  -> game Foreground color: light / mid / dark
    4 5 6  -> game Detail color:     light / mid / dark
At runtime the game's actual colors for each object (which vary by seed, faction, status effects,
lighting) are fed through BRIGHT + ramp(), so generated creatures keep their color identity.
"""
import colorsys

# The game's 18 colors (Base/Display.txt).
QUD = {
    "r": "a64a2e", "R": "d74200", "o": "f15f22", "O": "e99f10", "w": "98875f", "W": "cfc041",
    "g": "009403", "G": "00c420", "b": "0048bd", "B": "0096ff", "c": "40a4b9", "C": "77bfcf",
    "m": "b154cf", "M": "da5bd6", "k": "0f3b3a", "K": "155352", "y": "b1c9c3", "Y": "ffffff",
}

# Brighter, more saturated stand-ins (Bright Qud style). Same hue family as the original.
BRIGHT = {
    "r": "c8503a", "R": "f05a28", "o": "ff7030", "O": "ffb020", "w": "b08a5a", "W": "ffd23a",
    "g": "3fae3a", "G": "6fe04a", "b": "2a62d6", "B": "3fb4ff", "c": "4fc8d8", "C": "8fe4f0",
    "m": "c04ad8", "M": "ff7ae8", "k": "1a4a48", "K": "2e6a68", "y": "d0dcd8", "Y": "f8f8f0",
}

ROLE_DIGITS = {"1": ("fg", 0), "2": ("fg", 1), "3": ("fg", 2), "4": ("detail", 0), "5": ("detail", 1), "6": ("detail", 2)}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def brighten(rgb):
    """Map one of the game's 18 colors to its Bright Qud version; other colors pass through."""
    for k, h in QUD.items():
        q = hex_rgb(h)
        if all(abs(a - b) <= 3 for a, b in zip(rgb, q)):
            return hex_rgb(BRIGHT[k])
    return rgb


def ramp(rgb, shade):
    """shade 0 = light, 1 = mid, 2 = dark. HSV math, mirrored in C#."""
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    if shade == 0:
        s, v = s * 0.85, min(1.0, v * 1.2 + 0.06)
    elif shade == 2:
        s, v = min(1.0, s * 1.1), v * 0.62
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (round(r * 255), round(g * 255), round(b * 255))


def role_color(digit, fg_letter, detail_letter):
    which, shade = ROLE_DIGITS[digit]
    letter = fg_letter if which == "fg" else detail_letter
    return ramp(brighten(hex_rgb(QUD[letter])), shade)
