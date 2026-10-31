"""Effect tiles drawn procedurally (soft, partly transparent): gas clouds.

The game cycles a gas cell through Tiles2/gas_0..3 (one per 15 frames), colored with the gas's
foreground color. Ours: round puffs that drift a little between frames, so the cloud "breathes".
Pixels are foreground-role (mask R=100) with their own alpha, kept by the runtime recolor.
"""
import math

from PIL import Image


def gas(frame):
    """(RGBA image, role mask) for gas frame 0-3."""
    puffs = [(4, 5, 4.6), (11.5, 6, 4.2), (7, 11, 5.2), (12, 15, 4.4), (4, 18, 4.8), (10.5, 21, 4.2)]
    t = frame * math.pi / 2
    img = Image.new("RGBA", (16, 24), (0, 0, 0, 0))
    mask = Image.new("RGBA", (16, 24), (0, 0, 0, 0))
    px, mpx = img.load(), mask.load()
    for y in range(24):
        for x in range(16):
            best = 0.0
            light = False
            for i, (cx, cy, r) in enumerate(puffs):
                cx2 = cx + 1.2 * math.sin(t + i)
                cy2 = cy + 0.8 * math.cos(t + i * 1.7)
                d = math.hypot(x + 0.5 - cx2, y + 0.5 - cy2) / r
                v = max(0.0, 1.0 - d)
                if v > best:
                    best = v
                    light = (y + 0.5) < cy2 - r * 0.25  # upper part of each puff is lit
            if best <= 0.05:
                continue
            a = min(1.0, 0.25 + best * 0.9) * 0.62
            shade = 0 if light else 1
            px[x, y] = (200, 200, 200, round(a * 255))
            mpx[x, y] = (100, shade * 127, 0, 255)
    # Glints in the gas's secondary colour (detail role), near the heart of a puff; the same as the puff's
    # colour for gases that have none. They drift with the frame.
    for i, (cx, cy, r) in enumerate(puffs):
        gx = int(cx + 1.2 * math.sin(t + i) + (1 if i % 2 else -1))
        gy = int(cy + 0.8 * math.cos(t + i * 1.7) + (1 if i % 3 else -1))
        for (dx, dy) in ((0, 0), (1, 0)) if i % 2 else ((0, 0), (0, 1)):
            if 0 <= gx + dx < 16 and 0 <= gy + dy < 24:
                px[gx + dx, gy + dy] = (200, 200, 200, 190)
                mpx[gx + dx, gy + dy] = (200, 0, 0, 255)
    return img, mask
