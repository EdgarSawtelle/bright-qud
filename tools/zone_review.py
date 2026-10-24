"""Zone review sheets (docs/ZONE_REVIEW.md): one hand-made map shown as the original game, Bright Qud
today and proposals by day, plus a proposal at night with warm torch light. Local output only.

Usage: .venv/bin/python -I tools/zone_review.py joppa -> mockups/local/zones/review_joppa.png
"""
import math, os, random, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
from colors import hex_rgb  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402

LIGHTS = {"Torchpost"}            # objects that light the ground at night
WARM = (255, 170, 90)


def flat_ground(a, b, seed):
    a, b = hex_rgb(a), hex_rgb(b)
    rnd = random.Random(seed)
    cache = {}

    def f(x, y):
        if (x, y) not in cache:
            cache[x, y] = zm.lerp(a, b, 0.35 + rnd.random() * 0.3)   # small steps: no checkerboard
        return cache[x, y]
    return f


def earth_tiles():
    import build_tiles as B, earthground as E
    tiles = [B.render(E.SPRITES[k], "terrain", fg="w", detail="w") for k in E.SPRITES]
    return lambda x, y: tiles[(((x * 73856093) ^ (y * 19349663)) & 0x7fffffff) % len(tiles)]


def tone_for(p):
    """Proposal recolours by object name: name -> (light, dark) hex."""
    table = {k: (hex_rgb(v[0]), hex_rgb(v[1])) for k, v in p.get("tone", {}).items()}

    def tone(name, fg, dt, key):
        return table.get(name)
    return tone


def night_for(map_name, box):
    cells = MR.load(map_name)
    lights = [xy for xy, objs in cells.items() if any(o in LIGHTS for o in objs)]

    def night(cell, x, y):
        d = min((math.hypot(x - lx, (y - ly) * 1.5) for lx, ly in lights), default=99)
        cell = zm.memory_new(cell)                       # dim but coloured (as built)
        if d < 4:                                        # warm pool of torch light, fading out
            k = (1 - d / 4) ** 1.5 * 0.55
            px = cell.load()
            for yy in range(24):
                for xx in range(16):
                    r, g, b, a = px[xx, yy]
                    lit = tuple(min(255, int(c * (1 + k * 1.2))) for c in (r, g, b))
                    px[xx, yy] = zm.lerp(lit, WARM, k * 0.35) + (a,)
        return cell
    return night


REVIEWS = {
    "joppa": dict(
        map="Joppa", box=(20, 0, 49, 12),
        title="1. Joppa - \"ants in the viridian chaff, the farmers sap the last drops of pristine moisture "
              "out of the salt-spangled earth\"",
        a=dict(name="A. Salt-spangled earth", ground=("6e5c42", "786548"),
               tone={"DirtPath": ("8a7656", "5e4c36"), "DirtFloor": ("8a7656", "5e4c36")},
               note="Pale sun-dried earth flecked with salt, darker packed paths; viridian watervine and "
                    "sallow brinestalk huts stand out. Matches the key art's warm ochre path."),
        b=dict(name="B. Viridian marsh", ground=("3c4a30", "445436"),
               tone={"DirtPath": ("6e6448", "4a4232"), "DirtFloor": ("6e6448", "4a4232")},
               note="Greener, wetter ground (salt marsh chaff), brown packed paths. Lusher, less 'desert'."),
        light="Night: warm pools of light around every torch post with a slow flicker (G3). Animations: "
              "watervine sways gently, ponds shimmer (G4), a few salt glints twinkle by day.",
    ),
}


def wrap(d, text, x, y, width, f, fill=(205, 205, 195)):
    line = ""
    for w in text.split():
        if d.textlength(line + " " + w, font=f) > width:
            d.text((x, y), line, font=f, fill=fill)
            y += 21
            line = w
        else:
            line = (line + " " + w).strip()
    d.text((x, y), line, font=f, fill=fill)
    return y + 21


def sheet(key):
    r = REVIEWS[key]
    m, box = r["map"], r["box"]
    ga = flat_ground(*r["a"]["ground"], m + "a")
    gb = flat_ground(*r["b"]["ground"], m + "b")
    panels = [("Original game", MR.render(m, "vanilla", box)),
              ("Bright Qud today (ground approximate)", MR.render(m, "now", box)),
              (r["a"]["name"] + " (textured ground)", MR.render(m, "new", box, ground=ga, tone=tone_for(r["a"]), bare=earth_tiles())),
              (r["b"]["name"], MR.render(m, "new", box, ground=gb, tone=tone_for(r["b"]))),
              (r["a"]["name"] + " at night, torch light", MR.render(m, "new", box, ground=ga, tone=tone_for(r["a"]),
                                                                   night=night_for(m, box), bare=earth_tiles()))]
    pw, ph = panels[0][1].size
    pad, head = 16, 30
    W = pad + 2 * (pw + pad)
    H = 70 + 3 * (ph + head + pad) + 40
    out = Image.new("RGB", (W, H), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, r["title"], pad, 14, W - 2 * pad, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(panels):
        x = pad + (i % 2) * (pw + pad)
        y = 70 + (i // 2) * (ph + head + pad)
        d.text((x, y), label, font=font(18), fill=(225, 215, 185))
        out.paste(im.convert("RGB"), (x, y + head - 4))
    x, y = pad + pw + pad, 70 + 2 * (ph + head + pad)
    y = wrap(d, "A: " + r["a"]["note"], x, y, pw, font(16))
    y = wrap(d, "B: " + r["b"]["note"], x, y + 8, pw, font(16))
    wrap(d, r["light"], x, y + 8, pw, font(16))
    path = os.path.join(zm.OUT, "review_" + key + ".png")
    out.save(path)
    return path


if __name__ == "__main__":
    for k in sys.argv[1:] or REVIEWS:
        print(sheet(k))
