"""Animated zone mockups (GIF): a lush Rainbow Wood with breathing mini-mushrooms, and the Moon Stair
with twinkling marble diamonds. Same scenes as zone_mockup.py; output stays local (vanilla tiles).

Usage: .venv/bin/python -I tools/anim_mockup.py [rainbow] [moon]
  -> mockups/local/zones/rainbow_wood_lush.gif, moon_stair_twinkle.gif
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
from colors import hex_rgb  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_mockup import W, H, Z, OUT, INK, lerp, ours, key_of  # noqa: E402

FRAMES, MS = 32, 150          # one loop = 4.8 s: slow on purpose


def wave(phase, f):
    """0..1, one smooth cycle per loop."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * (f / FRAMES + phase))


def put(px, x, y, c, a=255):
    if 0 <= x < 16 and 0 <= y < 24:
        if a >= 255:
            px[x, y] = c + (255,)
        else:
            o = px[x, y][:3]
            px[x, y] = lerp(o, c, a / 255) + (255,)


# ---------------------------------------------------------------- Rainbow Wood

# tiny mushrooms: c cap, h cap highlight, s stem
MINI = [
    [".c.", "chc", ".s."],
    [".ccc.", "chccc", "..s..", "..s.."],
    [".c.", "chc", ".s.", ".s.", ".s."],
    [".cc.", "chcc", ".cc."],
    ["cc", "hc", ".s"],
]
CAPS = [(236, 92, 214), (92, 232, 232), (255, 168, 60), (190, 240, 80), (168, 120, 255), (255, 110, 120)]
STEM = (236, 226, 204)
MOSS = [(46, 78, 34), (70, 118, 46), (104, 160, 62), (150, 208, 92)]
FUNGAL_GRASS = (92, 210, 214)


def lush_cell(rnd):
    """Decoration plan for one ground cell: a list of (kind, data). About 65% of cells are busy."""
    items = []
    if rnd.random() > 0.65:
        return items
    r = rnd.random()
    if r < 0.7:                                    # moss patch
        cx, cy = rnd.randrange(3, 13), rnd.randrange(12, 21)
        items.append(("moss", [(cx + rnd.randint(-3, 3), cy + rnd.randint(-2, 2), rnd.randrange(3))
                               for _ in range(rnd.randrange(10, 20))]))
    for _ in range(rnd.choice((0, 1, 1, 2))):      # grass tufts, mostly green, some cyan fungal grass
        col = FUNGAL_GRASS if rnd.random() < 0.3 else MOSS[rnd.randrange(2, 4)]
        items.append(("tuft", (rnd.randrange(2, 14), rnd.randrange(10, 22), col)))
    for _ in range(rnd.choice((1, 1, 2, 2, 3))):   # mini mushrooms; only a sparse few move
        items.append(("mini", (rnd.randrange(len(MINI)), rnd.randrange(1, 12), rnd.randrange(6, 19),
                               rnd.choice(CAPS), rnd.random(), rnd.random() < 0.12)))
    return items


def draw_lush(cell, items, f):
    px = cell.load()
    for kind, data in items:
        if kind == "moss":
            for x, y, shade in data:
                put(px, x, y, MOSS[min(3, shade + 1)])
        elif kind == "tuft":
            x, y, col = data
            dark = lerp(col, (0, 0, 0), 0.35)
            for dx, h in ((-1, 2), (0, 3), (1, 2)):
                for i in range(h):
                    put(px, x + dx + (i == h - 1) * dx, y - i, col if i else dark)
    for kind, data in items:
        if kind != "mini":
            continue
        shape, x0, y0, cap, phase, alive = data
        w = wave(phase, f) if alive else 0.8
        lit = lerp(lerp(cap, (0, 0, 0), 0.3), cap, w)         # caps breathe: 70% -> 100%
        hi = lerp(cap, (255, 255, 255), 0.25 + 0.4 * w)
        grid = MINI[shape]
        for gy, row in enumerate(grid):
            for gx, ch in enumerate(row):
                c = {"c": lit, "h": hi, "s": STEM}.get(ch)
                if c:
                    put(px, x0 + gx, y0 + gy, c)
        if alive and w > 0.6:                                 # faint glow on the ground at the peak
            a = int(70 * (w - 0.6) / 0.4)
            for gx in range(-1, len(grid[0]) + 1):
                put(px, x0 + gx, y0 + len(grid), cap, a)
        if alive:                                             # one spore mote drifting up, fading
            t = (f / FRAMES + phase) % 1
            put(px, x0 + 1 + int(2 * math.sin(t * 6.28)), y0 - 1 - int(t * 9), lerp(cap, (255, 255, 255), 0.6),
                int(220 * (1 - t)))


# shaded forest floor: dark moss where the sun does not hit, a few warm lava-lit patches
GROUNDS = {"moss": ((28, 38, 22), (38, 50, 28)), "olive": ((32, 33, 22), (42, 43, 28))}
WARM = (74, 46, 26)


def rainbow_frames(variant):
    z = zm.ZONES["rainbow_wood"]
    p = z["proposal"]
    rnd = random.Random("lush")
    plan = []
    for y, row in enumerate(z["rows"]):
        for x, ch in enumerate(row):
            a, b = GROUNDS[variant]
            bg = lerp(a, b, rnd.random())
            if rnd.random() < 0.12:
                bg = lerp(bg, WARM, 0.5)
            plan.append((x, y, ch, bg, lush_cell(rnd) if ch in ".," else [], rnd.random()))
    frames = []
    for f in range(FRAMES):
        img = Image.new("RGBA", (W * 16, H * 24), (0, 0, 0, 255))
        for x, y, ch, bg, items, ph in plan:
            cell = Image.new("RGBA", (16, 24), bg + (255,))
            if ch == "~":
                t = zm.recolor_to(ours(key_of(zm.WATER), "B", "b"), hex_rgb(p["liquid"]), hex_rgb(p["liquid_detail"]))
                cell.alpha_composite(t)
            draw_lush(cell, items, f)
            if ch in z["legend"]:
                tile, fg, dt, kind = z["legend"][ch]
                t = ours(key_of(tile), fg, dt)
                if t:
                    cell.alpha_composite(t)
            img.alpha_composite(cell, (x * 16, y * 24))
        frames.append(img.resize((W * 16 * Z, H * 24 * Z), Image.NEAREST))
    return frames


# ---------------------------------------------------------------- Moon Stair

MARBLE = ((20, 17, 30), (30, 25, 42))
GLINT = [(236, 226, 255), (255, 214, 150), (230, 140, 245)]   # moonlight, warm dew, crystal magenta


def diamond(px, x, y, col, w):
    """Tiny 3x3 diamond: bright centre, soft points; w = 0..1 brightness."""
    if w < 0.08:
        return
    put(px, x, y, col, int(255 * w))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        put(px, x + dx, y + dy, col, int(110 * w))


def moon_frames():
    g = zm.moon_grid()
    rnd = random.Random("moon-twinkle")
    floor = {}
    for y in range(H):
        for x in range(W):
            bg = lerp(*MARBLE, rnd.random())
            veins = []
            if rnd.random() < 0.4:                    # faint white filigree of the marble
                x0 = rnd.randrange(1, 12)
                a_y = rnd.randrange(3, 21)
                veins.append(((x0, a_y), (x0 + rnd.randint(3, 6), a_y + rnd.randint(-2, 2))))
            # diamonds on a loose hex lattice, like the game's dotted hex floor
            dots = []
            for dy in (4, 12, 20):
                for dx in ((3, 11) if (dy // 8) % 2 == 0 else (7, 15)):
                    if rnd.random() < 0.55:
                        dots.append((dx + rnd.randint(-1, 1), dy + rnd.randint(-1, 1),
                                     GLINT[0 if rnd.random() < 0.6 else 1 if rnd.random() < 0.5 else 2],
                                     rnd.random(), rnd.random() < 0.25))
            floor[x, y] = (bg, veins, dots)
    frames = []
    for f in range(FRAMES):
        img = Image.new("RGBA", (W * 16, H * 24), (0, 0, 0, 255))
        for (x, y), (bg, veins, dots) in floor.items():
            cell = Image.new("RGBA", (16, 24), bg + (255,))
            cd = ImageDraw.Draw(cell)
            for a, b in veins:
                cd.line([a, b], fill=(40, 36, 54, 255))
            px = cell.load()
            if (x, y) in zm.MOON_POOLS:                  # warm static dew: gold, slowly shimmering
                for yy in range(24):
                    for xx in range(16):
                        s = 0.5 + 0.5 * math.sin(xx * 0.9 + yy * 0.5 + 2 * math.pi * f / FRAMES)
                        px[xx, yy] = lerp((196, 140, 70), (255, 222, 150), 0.35 + 0.4 * s) + (255,)
                for i in range(3):
                    t = (f / FRAMES + i / 3) % 1
                    diamond(px, (5 + i * 5) % 16, 4 + int(t * 16), (255, 252, 230), 1 - abs(2 * t - 1))
            elif g[y][x] is None:
                for dx, dy, col, ph, bright in dots:
                    w = wave(ph, f)
                    diamond(px, dx, dy, col, (0.15 + 0.85 * w ** 2) * (1.0 if bright else 0.55))
            if (x, y) in zm.MOON_LIFE:
                tile, fg, dt = zm.MOON_LIFE[(x, y)]
                t = ours(key_of(tile), fg, dt)
                if t:
                    cell.alpha_composite(t)
            img.alpha_composite(cell, (x * 16, y * 24))
        for i, (n, k) in enumerate(zm.MOON_BLOCKS):
            x0, y0 = n * 3 * 16, (k * 2 + n % 2) * 24
            colour = "M" if i % 2 == 0 else "Y"
            w = wave(i / len(zm.MOON_BLOCKS), f)
            gc = {"M": (220, 100, 240), "Y": (210, 220, 255)}[colour]
            glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(glow).ellipse((x0 - 10, y0 + 30, x0 + 58, y0 + 60), fill=gc + (int(35 + 45 * w),))
            img.alpha_composite(glow)
            pr = zm.prism(colour)
            mask = pr.split()[3]
            ink = Image.new("RGBA", (48, 48), INK + (255,))
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                img.paste(ink, (x0 + dx, y0 + dy), mask)
            img.alpha_composite(pr, (x0, y0))
            # the crystal "purrs": a slow glint slides down one facet
            gd = ImageDraw.Draw(img)
            t = (f / FRAMES + i * 0.37) % 1
            if t < 0.5:
                yy = y0 + 6 + int(t * 2 * 34)
                gd.line([(x0 + 8, yy), (x0 + 12, yy - 3)], fill=(255, 255, 255, 200))
        frames.append(img.resize((W * 16 * Z, H * 24 * Z), Image.NEAREST))
    return frames


# ---------------------------------------------------------------- Moon Stair, real tiles (art/src/moonstair.py)

MOON2_BLOCKS = [((0, 0), "M"), ((0, 1), "M"), ((1, 0), "M"), ((1, 1), "M"), ((2, 0), "Y"), ((3, 0), "Y"),
                ((4, 0), "m"), ((4, 1), "m")]
LAVENDER = (180, 160, 255)
MOON_GROUND = ((44, 40, 64), (53, 47, 76))


def moon2_grid():
    g = [[None] * W for _ in range(H)]
    for (n, k), col in MOON2_BLOCKS:
        for dx in range(3):
            for dy in range(2):
                x, y = n * 3 + dx, k * 2 + n % 2 + dy
                if x < W and y < H:
                    g[y][x] = col
    return g


def lavender(t, amount=0.35):
    """Runtime pull of crystal colours toward lavender (as BrightQud.cs does for the Moon Stair)."""
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = lerp((r, g, b), LAVENDER, amount) + (a,)
    return t


def moon_real_frames():
    import build_tiles as B
    import moonstair as MS
    g = moon2_grid()
    rnd = random.Random("moon2")
    ground = {(x, y): lerp(*MOON_GROUND, rnd.random()) for y in range(H) for x in range(W)}
    frames = []
    for f in range(FRAMES):
        img = Image.new("RGBA", (W * 16, H * 24), (0, 0, 0, 255))
        for y in range(H):
            for x in range(W):
                cell = Image.new("RGBA", (16, 24), ground[x, y] + (255,))
                if g[y][x] is not None:
                    part = zm.cryshex_name(g, x, y).replace("tiles_cryshex_", "cryshex_")
                    cell.alpha_composite(lavender(B.render(MS.SPRITES[part], "terrain", fg=g[y][x], detail="K")))
                elif (x, y) in zm.MOON_POOLS:
                    px = cell.load()
                    for yy in range(24):
                        for xx in range(16):
                            w = 0.5 + 0.5 * math.sin(xx * 0.9 + yy * 0.5 + 2 * math.pi * f / FRAMES)
                            px[xx, yy] = lerp((196, 150, 110), (255, 226, 170), 0.35 + 0.4 * w) + (255,)
                else:
                    step = (f // 8 + x * 3 + y * 5) % 4
                    grid = MS.SPRITES["moonfloor_1"] if step == 0 else MS.FRAMES["terrain/sw/hex/dotted/1"][step - 1]
                    cell.alpha_composite(lavender(B.render(grid, "terrain", fg="m", detail="m"), 0.3))
                if (x, y) in zm.MOON_LIFE:
                    tile, fg, dt = zm.MOON_LIFE[(x, y)]
                    t = ours(key_of(tile), fg, dt)
                    if t:
                        cell.alpha_composite(t)
                img.alpha_composite(cell, (x * 16, y * 24))
        frames.append(img.resize((W * 16 * Z, H * 24 * Z), Image.NEAREST))
    return frames


# ---------------------------------------------------------------- output


def gif(name, title, panels, note):
    """panels: [(label, [frames] or still image)]"""
    pw, ph = (panels[0][1][0] if isinstance(panels[0][1], list) else panels[0][1]).size
    pad, head = 16, 34
    sw = pad + len(panels) * (pw + pad)
    sh = 60 + ph + head + pad + 60
    out = []
    for f in range(FRAMES):
        img = Image.new("RGB", (sw, sh), (24, 24, 28))
        d = ImageDraw.Draw(img)
        d.text((pad, 14), title, font=font(26), fill=(240, 236, 220))
        for i, (label, fr) in enumerate(panels):
            x = pad + i * (pw + pad)
            d.text((x, 60), label, font=font(18), fill=(200, 200, 190))
            img.paste((fr[f] if isinstance(fr, list) else fr).convert("RGB"), (x, 60 + head - 6))
        zm.wrap(d, note, pad, 60 + head + ph + 6, sw - 2 * pad, font(16))
        out.append(img.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    path = os.path.join(OUT, name + ".gif")
    out[0].save(path, save_all=True, append_images=out[1:], duration=MS, loop=0, optimize=False)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ["rainbow", "moon"]
    if "rainbow" in which:
        print(gif("rainbow_wood_lush", "Rainbow Wood, lush: moss, tufts and tiny glowing mushrooms",
                  [("Bright Qud now", zm.build("rainbow_wood", "now")),
                   ("Dark moss", rainbow_frames("moss")),
                   ("Dark olive moss", rainbow_frames("olive"))],
                  "Shaded forest floor in dark moss, a few warm lava-lit patches. About 65% of the ground is "
                  "busy with moss, green and cyan tufts and tiny mushrooms; only about 1 in 8 tiny mushrooms "
                  "slowly breathes and lets a spore drift up (one cycle about every 5 s). The rest stay still."))
    if "moon2" in which:
        zm.moon_grid = moon2_grid          # same layout in the game / now panels
        print(gif("moon_stair_v2", "Moon Stair v2: leaning crystal shards, lavender and periwinkle",
                  [("Original game", zm.build("moon_stair", "vanilla")),
                   ("Bright Qud now", zm.build("moon_stair", "now")),
                   ("New tiles (animated)", moon_real_frames())],
                  "Real game layout. Each crystal is a cluster of shards leaning up to the right (like the "
                  "painting): bright edge, lit body, cool periwinkle underside; the lit front face and a "
                  "periwinkle shaded face. Crystal colours pulled toward lavender. Ground: dusky lavender "
                  "slate instead of black. Floor diamonds twinkle slowly; static pools shimmer."))
    if "moon" in which:
        print(gif("moon_stair_twinkle", "Moon Stair: moonlit diamonds in black marble",
                  [("Original game", zm.build("moon_stair", "vanilla")),
                   ("Bright Qud now", zm.build("moon_stair", "now")),
                   ("Proposal (animated)", moon_frames())],
                  "The game's dotted hex floor becomes tiny diamonds of moonlight and warm dew set in black "
                  "marble; each one slowly brightens and dims on its own rhythm. Whole prisms glow and "
                  "'purr' (soft pulse of the floor glow, a slow glint sliding down a facet); the static "
                  "pools shimmer gold."))


if __name__ == "__main__":
    main()
