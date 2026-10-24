"""Ground texture sets, one per ground family (docs/ZONE_STUDY_ALL.md). The runtime draws one of a family's
16 tiles on every bare ground cell of a zone in that family.

User rule (2026-10-24): tiles of the same ground use LOW colour variation (no squares, no checkerboard),
each tile is RICH in small details so the zone looks organic and full, and the ground keeps a LOW presence.
So every detail colour is a small step from the family's ground colour, and every variant has about the
same amount of light and dark detail (its average stays the ground colour).

Tiles are drawn with exact colours (no role mask: they are never recoloured). Background is transparent:
the ground colour itself comes from the zone (BrightQud.cs).
"""
import colorsys, random

from PIL import Image

W, H, COUNT = 16, 24, 16

FAMILIES = {
    # name: (ground base, ground alt, accent for plants/minerals)
    "salt":  ("a2967e", "ab9f87", "c8c0ae"),   # A pale salt and sand
    "earth": ("6e5c42", "756247", "7e8a4a"),   # B warm earth (Joppa, villages)
    "rust":  ("8c4e36", "93543a", "c9b8a0"),   # C rust and red rock
    "green": ("3d3a28", "433f2b", "4f6a32"),   # D green shade (jungle, marsh)
    "teal":  ("1e2c2c", "233232", "4a6e6a"),   # E dark teal (caves, sacred, tech)
    "marsh": ("4e5040", "54564a", "8a8a5c"),   # D' salt marsh: olive mud, salt crust, tufted grass
    "redrock": ("9b3f2b", "a1452e", "d9a07a"), # C' Red Rock surface: redder than the plain canyon
    "redcave": ("3b2622", "412a25", "8a5a48"), # C'' Red Rock caves: dark red-brown rubble floor
    "rustwell": ("874a33", "8d4f37", "c8743c"),  # Rust Wells surface: rust dust with flaking iron
    "rustcave": ("2f2723", "352c27", "b0602e"),  # Rust Wells strata: bitumen-dark floor, rust flakes
}


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(rgb, v=1.0, s=1.0, hue=0.0):
    """Small step from a colour: v scales value, s scales saturation, hue shifts hue."""
    h, sa, va = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    r, g, b = colorsys.hsv_to_rgb((h + hue) % 1, min(1, sa * s), min(1, va * v))
    return (round(r * 255), round(g * 255), round(b * 255), 255)


class Tile:
    def __init__(self, seed):
        self.rnd = random.Random(seed)
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        self.px = self.img.load()

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[x, y] = c

    def grain(self, base, n, lo=0.88, hi=1.12):
        """Fine grain everywhere: balanced lighter and darker single pixels."""
        for i in range(n):
            v = hi if i % 2 else lo
            self.put(self.rnd.randrange(W), self.rnd.randrange(H), shade(base, v * self.rnd.uniform(0.97, 1.03)))

    def pebble(self, base, x, y, size=2):
        """Tiny stone: light top, body, dark under-shadow."""
        for dx in range(size):
            self.put(x + dx, y, shade(base, 1.16))
            self.put(x + dx, y + 1, shade(base, 1.06))
            self.put(x + dx, y + 2, shade(base, 0.82))

    def line(self, base, x, y, n, v, drift=(-1, 0, 0, 1), shadow=None):
        for _ in range(n):
            self.put(x, y, shade(base, v))
            if shadow:
                self.put(x, y + 1, shade(base, shadow))
            x += 1
            y += self.rnd.choice(drift)


def salt(t, base, acc):
    t.grain(base, 34, 0.92, 1.08)
    for _ in range(t.rnd.randrange(2, 4)):                 # salt-crust ridges (polygon crack edges)
        t.line(base, t.rnd.randrange(-2, 10), t.rnd.randrange(2, 22), t.rnd.randrange(4, 8), 1.07, shadow=0.93)
    for _ in range(t.rnd.randrange(2, 4)):                 # tiny crystals
        t.put(t.rnd.randrange(W), t.rnd.randrange(H), shade(acc, 1.0, 0.8))
    for _ in range(t.rnd.randrange(1, 3)):
        t.pebble(base, t.rnd.randrange(1, 14), t.rnd.randrange(2, 21), 1)


def earth(t, base, acc):
    t.grain(base, 30)
    for _ in range(t.rnd.randrange(2, 4)):
        t.pebble(base, t.rnd.randrange(1, 14), t.rnd.randrange(2, 21), t.rnd.choice((1, 2)))
    t.line(base, t.rnd.randrange(0, 10), t.rnd.randrange(3, 21), t.rnd.randrange(3, 6), 0.84)   # hairline crack
    for _ in range(t.rnd.randrange(1, 3)):                 # dry straw blades, a muted sprout
        x, y = t.rnd.randrange(2, 14), t.rnd.randrange(6, 22)
        straw = shade(base, 1.22, 0.9, 0.02)
        t.put(x, y, straw)
        t.put(x + 1, y - 1, straw)
        t.put(x - 1, y - 1, shade(base, 1.12, 0.9, 0.02))
    if t.rnd.random() < 0.6:
        x, y = t.rnd.randrange(2, 14), t.rnd.randrange(6, 22)
        t.put(x, y, shade(acc, 0.95, 0.7))
        t.put(x, y - 1, shade(acc, 1.05, 0.7))


def rust(t, base, acc):
    t.grain(base, 32)
    for _ in range(t.rnd.randrange(2, 4)):                 # shale flakes: short flat plates
        x, y, n = t.rnd.randrange(0, 12), t.rnd.randrange(2, 22), t.rnd.randrange(3, 6)
        for i in range(n):
            t.put(x + i, y, shade(base, 1.1))
            t.put(x + i, y + 1, shade(base, 0.86))
    for _ in range(t.rnd.randrange(1, 3)):
        t.pebble(base, t.rnd.randrange(1, 14), t.rnd.randrange(2, 21), t.rnd.choice((1, 2)))
    if t.rnd.random() < 0.5:                               # a faint salt scab
        x, y = t.rnd.randrange(2, 13), t.rnd.randrange(3, 21)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (2, 1)):
            t.put(x + dx, y + dy, tuple(round(base[i] + (acc[i] - base[i]) * 0.3) for i in range(3)) + (255,))


def green(t, base, acc):
    t.grain(base, 26)
    for _ in range(t.rnd.randrange(3, 6)):                 # leaf litter: little 2-3 px leaves
        x, y = t.rnd.randrange(1, 14), t.rnd.randrange(2, 22)
        c = t.rnd.choice((shade(acc, 0.85, 0.75), shade(base, 1.25, 1.1, 0.03), shade(acc, 0.7, 0.8, -0.04)))
        t.put(x, y, c)
        t.put(x + 1, y, c)
        if t.rnd.random() < 0.5:
            t.put(x + 1, y - 1, shade(c[:3], 1.08))
    if t.rnd.random() < 0.7:                               # a twig or root
        t.line(base, t.rnd.randrange(0, 9), t.rnd.randrange(3, 21), t.rnd.randrange(4, 7), 0.78)
    for _ in range(t.rnd.randrange(4, 8)):                 # moss dots
        t.put(t.rnd.randrange(W), t.rnd.randrange(H), shade(acc, 0.75, 0.6))


def teal(t, base, acc):
    t.grain(base, 36, 0.85, 1.15)
    for _ in range(t.rnd.randrange(2, 4)):                 # small grit clusters
        x, y = t.rnd.randrange(1, 14), t.rnd.randrange(2, 22)
        t.put(x, y, shade(base, 1.25))
        t.put(x + 1, y, shade(base, 0.8))
    for _ in range(1 if t.rnd.random() < 0.5 else 2):      # faint mineral seams
        t.line(base, t.rnd.randrange(0, 10), t.rnd.randrange(3, 21), t.rnd.randrange(4, 8), 1.22, shadow=0.85)
    for _ in range(t.rnd.randrange(1, 3)):
        t.pebble(base, t.rnd.randrange(1, 14), t.rnd.randrange(2, 21), 1)
    if t.rnd.random() < 0.35:                              # rare cold glint
        t.put(t.rnd.randrange(2, 14), t.rnd.randrange(2, 22), shade(acc, 1.1, 0.7))


def cave(t, base, acc):
    t.grain(base, 30, 0.9, 1.1)
    for _ in range(t.rnd.randrange(2, 4)):                 # rubble: small stones with an under-shadow
        t.pebble(base, t.rnd.randrange(1, 14), t.rnd.randrange(2, 21), t.rnd.choice((1, 2)))
    for _ in range(t.rnd.randrange(1, 3)):                 # shale chips
        x, y = t.rnd.randrange(0, 12), t.rnd.randrange(2, 22)
        for i in range(t.rnd.randrange(2, 4)):
            t.put(x + i, y, shade(base, 1.2))
            t.put(x + i, y + 1, shade(base, 0.8))
    if t.rnd.random() < 0.4:                               # red dust drift
        x, y = t.rnd.randrange(2, 12), t.rnd.randrange(3, 21)
        for dx in range(4):
            t.put(x + dx, y + (dx > 1), shade(acc, 0.62, 0.8))


def rustflake(t, base, acc):
    """Rust Wells: rust dust and flakes of 'moisture-sucked rust' shed by the qudzu."""
    rust(t, base, acc)
    for _ in range(t.rnd.randrange(3, 6)):                 # orange rust flakes, low contrast
        x, y = t.rnd.randrange(1, 15), t.rnd.randrange(1, 23)
        c = tuple(round(base[i] + (acc[i] - base[i]) * 0.45) for i in range(3)) + (255,)
        t.put(x, y, c)
        if t.rnd.random() < 0.5:
            t.put(x + 1, y, c)


def bitumen(t, base, acc):
    """Rust Wells strata: dark bitumen-and-gravel floor with pale gravel and rust flakes."""
    t.grain(base, 30, 0.88, 1.14)
    for _ in range(t.rnd.randrange(3, 6)):                 # pale carbon gravel islands
        x, y = t.rnd.randrange(1, 15), t.rnd.randrange(1, 23)
        t.put(x, y, shade(base, 1.35, 0.4))
        t.put(x, y + 1, shade(base, 0.85))
    for _ in range(t.rnd.randrange(2, 4)):                 # rust flakes
        x, y = t.rnd.randrange(1, 15), t.rnd.randrange(1, 23)
        t.put(x, y, tuple(round(base[i] + (acc[i] - base[i]) * 0.4) for i in range(3)) + (255,))
    if t.rnd.random() < 0.5:                               # a hairline trench
        t.line(base, t.rnd.randrange(0, 10), t.rnd.randrange(3, 21), t.rnd.randrange(4, 7), 0.78)


def marsh(t, base, acc):
    t.grain(base, 30)
    for _ in range(t.rnd.randrange(2, 4)):                 # tufted marsh grass: olive-golden blades
        x, y = t.rnd.randrange(2, 14), t.rnd.randrange(7, 22)
        for dx, h in ((-1, 2), (0, 3), (1, 2)):
            for i in range(h):
                t.put(x + dx + (i == h - 1) * dx, y - i, shade(acc, 0.82 + 0.06 * i, 0.75))
    for _ in range(t.rnd.randrange(2, 4)):                 # faint salt crust on the mud
        x, y = t.rnd.randrange(1, 14), t.rnd.randrange(2, 22)
        for dx in range(t.rnd.randrange(2, 4)):
            t.put(x + dx, y, shade(base, 1.18, 0.6))
    for _ in range(t.rnd.randrange(1, 3)):                 # damp darker hollows
        x, y = t.rnd.randrange(1, 14), t.rnd.randrange(2, 22)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 0)):
            t.put(x + dx, y + dy, shade(base, 0.86))


DRAW = {"salt": salt, "earth": earth, "rust": rust, "green": green, "teal": teal, "marsh": marsh, "redrock": rust, "redcave": cave, "rustwell": rustflake, "rustcave": bitumen}


def tiles(family):
    base, _, acc = (hx(h) for h in FAMILIES[family])
    out = []
    for i in range(COUNT):
        t = Tile(f"{family}{i}")
        DRAW[family](t, base, acc)
        out.append(t.img)
    return out


def all_tiles():
    """{tile key: image} for the build: brightqudground/<family>/<n>."""
    return {f"brightqudground/{fam}/{i}": im for fam in FAMILIES for i, im in enumerate(tiles(fam))}
