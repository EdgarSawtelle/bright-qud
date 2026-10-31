"""Phase 3 batch 1: terrain & walls. Generators return 16x24 grids (see tiles.py for the legend).

Walls are 3/4 view like the brinestalk wall: a lit top surface, and a front face with a dark base
when nothing of the same wall is to the south (the "blocks you" tier). Materials use role colors,
so one design serves every rock type the seed picks (shale, mudroot, sandstone, ...).
"""
import math
import random
import zlib

from tiles import _bits, _grid, _rows


# ---------- painted walls (8-digit masks: N NE E SE S SW W NW) ----------

def _rock_texture(g, y0, y1, rnd, light, mid, dark):
    """Irregular stones: mid fill, dark cracks, light top-left rims."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
    for _ in range(6):
        cx, cy = rnd.randrange(0, 16), rnd.randrange(y0, max(y0 + 1, y1))
        rx, ry = rnd.randrange(3, 6), rnd.randrange(2, 4)
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if not (y0 <= y < y1 and 0 <= x < 16):
                    continue
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if 0.75 < d <= 1.05:
                    g[y][x] = dark
                elif d <= 0.75 and (x - cx) + (y - cy) < -rx // 2:
                    g[y][x] = light


def _salt_texture(g, y0, y1, rnd, light, mid, dark):
    """Salt/halite crystals: blocky facets with bright diagonal glints."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid if ((x // 4) + (y // 3)) % 2 else light
            if x % 4 == 3 or y % 3 == 2:
                g[y][x] = dark
    for _ in range(4):
        x, y = rnd.randrange(0, 15), rnd.randrange(y0, max(y0 + 1, y1 - 1))
        g[y][x] = "w"


def _metal_texture(g, y0, y1, rnd, light, mid, dark):
    """Riveted plates with rust streaks (detail color)."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
            if (y - y0) % 6 == 0 or x % 8 == 0:
                g[y][x] = dark
            elif (y - y0) % 6 == 1 or x % 8 == 1:
                g[y][x] = light
    for y in range(y0 + 3, y1, 6):
        for x in (3, 12):
            g[y][x] = "l"
    for _ in range(3):
        x = rnd.randrange(1, 15)
        for y in range(rnd.randrange(y0, max(y0 + 1, y1 - 2)), y1):
            if rnd.random() < 0.7 and g[y][x] == mid:
                g[y][x] = "5"


def _slab_texture(g, y0, y1, rnd, light, mid, dark):
    """Smooth poured slabs (fulcrete/concrete) with a few hairline cracks."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
            if (y - y0) % 8 == 7:
                g[y][x] = dark
    x = rnd.randrange(3, 13)
    for y in range(y0, y1):
        if rnd.random() < 0.5:
            x = max(1, min(14, x + rnd.choice((-1, 1))))
        if rnd.random() < 0.6:
            g[y][x] = dark


def _canvas_texture(g, y0, y1, rnd, light, mid, dark):
    """Canvas stretched over poles: vertical folds, stripes in the detail color."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = light if x % 5 == 1 else (dark if x % 5 == 4 else mid)
            if (y - y0) % 7 in (2, 3):
                g[y][x] = "5"
    for y in range(y0, y1):
        g[y][0] = "N"


def _wood_texture(g, y0, y1, rnd, light, mid, dark):
    """Horizontal planks: lit top edge, dark seams, staggered joints and a few knots."""
    for y in range(y0, y1):
        r = (y - y0) % 4
        for x in range(16):
            g[y][x] = dark if r == 3 else (light if r == 0 else mid)
        joint = (5 + 7 * ((y - y0) // 4)) % 16
        if r != 3:
            g[y][joint] = dark
    for _ in range(2):
        y = rnd.randrange(y0, max(y0 + 1, y1))
        if (y - y0) % 4 in (1, 2):
            g[y][rnd.randrange(1, 15)] = dark


def _brick_texture(g, y0, y1, rnd, light, mid, dark):
    """Staggered bricks, 3 rows tall, mortar in the dark shade."""
    for y in range(y0, y1):
        r = (y - y0) % 3
        off = 0 if ((y - y0) // 3) % 2 == 0 else 3
        for x in range(16):
            if r == 2 or (x + off) % 6 == 5:
                g[y][x] = dark
            else:
                g[y][x] = light if r == 0 and (x + off) % 6 == 0 else mid


def _stone_texture(g, y0, y1, rnd, light, mid, dark):
    """Big cut blocks (8x6, staggered): smooth faces, light top rims."""
    for y in range(y0, y1):
        r = (y - y0) % 6
        off = 0 if ((y - y0) // 6) % 2 == 0 else 4
        for x in range(16):
            if r == 5 or (x + off) % 8 == 7:
                g[y][x] = dark
            else:
                g[y][x] = light if r == 0 else mid


def _plant_texture(g, y0, y1, rnd, light, mid, dark):
    """Thick vegetation: dark tangle with leaf clusters in the detail color."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = dark if (x + y) % 5 == 0 else mid
    for _ in range(9):
        cx, cy = rnd.randrange(0, 16), rnd.randrange(y0, max(y0 + 1, y1))
        for dx, dy, c in ((0, 0, "5"), (1, 0, "4"), (-1, 0, "5"), (0, -1, "4"), (0, 1, "6")):
            x, y = cx + dx, cy + dy
            if 0 <= x < 16 and y0 <= y < y1:
                g[y][x] = c
        if 0 <= cx < 16 and y0 <= cy - 1 < y1:
            g[cy - 1][cx] = light if light != "2" else "4"


def _shroom_texture(g, y0, y1, rnd, light, mid, dark):
    """Spongy fungus flesh with round spots in the detail color."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = light if (x * 3 + y * 5) % 11 == 0 else mid
    for _ in range(5):
        cx, cy = rnd.randrange(1, 15), rnd.randrange(y0, max(y0 + 1, y1))
        for y in range(cy - 1, cy + 2):
            for x in range(cx - 1, cx + 2):
                if 0 <= x < 16 and y0 <= y < y1 and abs(x - cx) + abs(y - cy) <= 1:
                    g[y][x] = "4" if (x, y) == (cx - 1, cy) or (x, y) == (cx, cy - 1) else "5"
        if 0 <= cx + 1 < 16 and y0 <= cy + 1 < y1:
            g[cy + 1][cx + 1] = dark


def _crystal_texture(g, y0, y1, rnd, light, mid, dark):
    """Faceted crystal: diagonal facets in three shades with bright glints."""
    for y in range(y0, y1):
        for x in range(16):
            a, b = (x + y) % 8, (x - y) % 8
            g[y][x] = dark if a == 0 or b == 0 else (light if a < b else mid)
    for _ in range(3):
        g[rnd.randrange(y0, max(y0 + 1, y1))][rnd.randrange(0, 16)] = "w"


def _bone_texture(g, y0, y1, rnd, light, mid, dark):
    """Stacked bones (light, knobbed ends) packed in dark matter."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = dark
    y = y0 + 1
    while y < y1 - 1:
        x0 = rnd.randrange(-3, 4)
        for x in range(x0, x0 + 11):
            if 0 <= x < 16:
                g[y][x] = light
        for x in (x0, x0 + 10):
            for yy in (y - 1, y + 1):
                if 0 <= x < 16 and y0 <= yy < y1:
                    g[yy][x] = mid
        y += 3


def _tech_texture(g, y0, y1, rnd, light, mid, dark):
    """Machine panels: dark grid, lit edges, glowing conduits in the detail color."""
    for y in range(y0, y1):
        for x in range(16):
            r = (y - y0) % 8
            g[y][x] = dark if r == 7 or x % 8 == 7 else (light if r == 0 or x % 8 == 0 else mid)
    for _ in range(2):
        y = rnd.randrange(y0 + 2, max(y0 + 3, y1 - 1))
        if (y - y0) % 8 in (2, 3, 4, 5):
            for x in range(1, 15):
                if x % 8 != 7:
                    g[y][x] = "4"
    for _ in range(2):
        g[rnd.randrange(y0, max(y0 + 1, y1))][rnd.choice((2, 5, 10, 13))] = "w"


def _scale_texture(g, y0, y1, rnd, light, mid, dark):
    """Overlapping scales (rows of half-discs, staggered)."""
    for y in range(y0, y1):
        r = (y - y0) % 4
        off = 0 if ((y - y0) // 4) % 2 == 0 else 2
        for x in range(16):
            u = (x + off) % 4
            g[y][x] = dark if r == 3 and u in (0, 3) else (light if r == 0 and u in (1, 2) else mid)


# Ornate walls (ruins, tombs, crypts): a smooth slab with a motif in the detail color.
MOTIFS = {
    "diamonds": [".4..", "4.4.", ".4..", "...."],
    "runes": ["4.44", "4..4", "44.4", "...."],
    "columns": ["14.3", "14.3", "14.3", "14.3"],
    "arches": [".44.", "4..4", "4..4", "...."],
    "shields": ["444.", "454.", ".4..", "...."],
    "valence": ["4...", ".4.4", "..4.", "...."],
    "zigzag": ["4...", ".4.4", "..4.", "...."],
    "chevron": ["4..4", ".44.", "....", "...."],
    "filigree": [".4..", "4.5.", ".4..", "..5."],
    "fluted": ["1.3.", "1.3.", "1.3.", "1.3."],
    "backslash": ["4...", ".4..", "..4.", "...4"],
}


def _ornate(motif):
    pat = MOTIFS[motif]

    full = motif in ("columns", "fluted")  # vertical motifs run the whole height

    def texture(g, y0, y1, rnd, light, mid, dark):
        for y in range(y0, y1):
            r = (y - y0) % 8
            for x in range(16):
                c = mid if r != 0 else light
                if full or r in (2, 3, 4):
                    p = pat[(r - (0 if full else 2)) % 4][x % 4]
                    c = {"1": light, "3": dark}.get(p, p) if p != "." else c
                g[y][x] = c
            if r == 7:
                g[y] = [dark] * 16
    return texture


def _cage_texture(g, y0, y1, rnd, light, mid, dark):
    """Kyakukya's mushroom flesh: "spore-rich slime glistens on the cage-like fruiting body, trimmed like a
    hedge". A lattice of glossy fungus with round dark holes (red cage fungus), a few wet glints."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
    for row, cy in enumerate(range(y0 + 2, y1, 5)):
        for cx in range(1 + (row % 2) * 3, 16, 6):
            for y in range(cy - 1, cy + 2):
                for x in range(cx - 1, cx + 3):
                    if 0 <= x < 16 and y0 <= y < y1 and not (y != cy and x in (cx - 1, cx + 2)):
                        g[y][x] = dark                         # a hole in the lattice
            if 0 <= cx - 1 < 16 and y0 <= cy - 2 < y1:
                g[cy - 2][cx] = light                          # the rim above each hole catches light
                g[cy - 2][cx + 1] = light
    for _ in range(3):                                         # glistening slime
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(16)
        if g[y][x] != dark:
            g[y][x] = "w" if light == "1" else light


def _petal_texture(g, y0, y1, rnd, light, mid, dark):
    """Bey Lah's huts: "stripped trunks of sallow brinestalk bonded with mud and strewn with flower petals".
    Upright pale trunks with mud between them, a few pressed petals (fixed pink/gold/violet) stuck on."""
    for y in range(y0, y1):
        for x in range(16):
            col = x % 4
            g[y][x] = dark if col == 3 else (light if col == 0 else mid)   # trunk, its lit edge, mud seam
    for _ in range(2):                                         # a mud band across the trunks
        y = rnd.randrange(y0, max(y0 + 1, y1))
        for x in range(16):
            if g[y][x] != dark:
                g[y][x] = dark if x % 2 else mid
    for _ in range(4):                                         # pressed petals
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(16)
        g[y][x] = rnd.choice("MyM")
        if x + 1 < 16 and rnd.random() < 0.5:
            g[y][x + 1] = "m"


def _marl_texture(g, y0, y1, rnd, light, mid, dark):
    """Hills: "lacustrine ecosystems, cast in lime-rich mud ... in chalk-white shine" - wavy chalk strata."""
    phase = rnd.randrange(16)
    for y in range(y0, y1):
        for x in range(16):
            band = (y - y0 + (1 if (x + phase) % 8 < 4 else 0)) % 5    # gently waving bands
            g[y][x] = dark if band == 4 else (light if band in (0, 1) else mid)
    for _ in range(3):                                         # ripple marks of the old lake bed
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(1, 14)
        if g[y][x] == mid:
            g[y][x] = light
            g[y][x + 1] = light


def _limestone_texture(g, y0, y1, rnd, light, mid, dark):
    """Mountains: "the glaucous rock is a necropolis" - bedded stone with small fossil shells."""
    for y in range(y0, y1):
        r = (y - y0) % 6
        for x in range(16):
            g[y][x] = dark if r == 5 else (light if r == 0 else mid)
        if r != 5 and ((y - y0) // 6) % 2 == 0:
            g[y][(3 + 9 * ((y - y0) // 6)) % 16] = dark           # sparse vertical joints between beds
    for _ in range(3):                                         # fossil pocks: a dark dot with a lit rim
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(1, 15)
        if g[y][x] == mid:
            g[y][x] = dark
            g[y][x - 1] = light


def _concrete_texture(g, y0, y1, rnd, light, mid, dark):
    """Stilt: "smooth grey stone hides its bonded pebbly innards ... streaked with dirt" - poured lifts, few pebbles."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = dark if (y - y0) % 8 == 7 else mid
    for _ in range(3):                                         # a dirt streak running down from a lift line
        x, y = rnd.randrange(16), rnd.randrange(y0, max(y0 + 1, y1))
        for i in range(rnd.randrange(2, 5)):
            if y + i < y1:
                g[y + i][x] = dark
    for _ in range(3):                                         # a pebble showing through
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(0, 15)
        if g[y][x] == mid:
            g[y][x] = light


def _stiltmarble_texture(g, y0, y1, rnd, light, mid, dark):
    """Stilt: "ribbons of impurity ... polished along the ideal plane" - big white blocks, thin veins, wide joints."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = dark if (y - y0) % 12 == 11 else light
    for _ in range(3):
        x, y = rnd.randrange(0, 8), rnd.randrange(y0, max(y0 + 1, y1))
        for i in range(rnd.randrange(5, 9)):
            if 0 <= y < y1 and g[y][min(15, x + i)] == light:
                g[y][min(15, x + i)] = mid
            y += rnd.choice((0, 1, 1, -1))


def _stiltpillar_texture(g, y0, y1, rnd, light, mid, dark):
    """Stilt: "fluted marble column" - vertical flutes under a gold band."""
    for y in range(y0, y1):
        for x in range(16):
            f = x % 4
            g[y][x] = dark if f == 3 else (light if f in (0, 1) else mid)
    for y in range(y0, min(y0 + 2, y1)):
        for x in range(16):
            g[y][x] = "y"


def _ironbars_texture(g, y0, y1, rnd, light, mid, dark):
    """Stilt: the iron fence - upright bars between two rails."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = light if x % 4 == 1 else (mid if x % 4 == 2 else dark)
        if (y - y0) % 12 in (2, 3):
            for x in range(16):
                g[y][x] = mid


def _fulcrete_texture(g, y0, y1, rnd, light, mid, dark):
    """Ruins: "carbon gravel ... an ocean of bitumen ... hair-line trenches along the basin" - dark mass, sparse gravel,
    one hairline crack wandering across."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
    for _ in range(9):
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(0, 16)
        g[y][x] = light
    y = rnd.randrange(y0, max(y0 + 1, y1))
    for x in range(16):
        g[y][x] = dark
        y = min(y1 - 1, max(y0, y + rnd.choice((0, 0, 1, -1))))


def _vinefulcrete_texture(g, y0, y1, rnd, light, mid, dark):
    """Surface ruins: the same fulcrete, "vine-swathed" - leafy strands hanging down it (fixed leaf greens)."""
    _fulcrete_texture(g, y0, y1, rnd, light, mid, dark)
    for _ in range(rnd.randrange(1, 3)):
        x = rnd.randrange(16)
        for y in range(y0, min(y1, y0 + rnd.randrange(6, 15))):
            g[y][x % 16] = "h"
            if y % 3 == 0:
                g[y][(x + 1) % 16] = "g"
            x += rnd.choice((0, 0, 1, -1))


def _mudroot_texture(g, y0, y1, rnd, light, mid, dark):
    """Ruins: "braids of fibrous plant veins enmesh compacted mud" - two or three thick root braids over mud."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
    for _ in range(3):
        x = rnd.randrange(16)
        for y in range(y0, y1):
            g[y][x % 16] = light
            g[y][(x + 1) % 16] = dark
            x += rnd.choice((0, 1, -1))
    for _ in range(4):
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(16)
        g[y][x] = "6"                                          # brackish weep


def _crysteel_texture(g, y0, y1, rnd, light, mid, dark):
    """Baroque: "longwise infill plates of burnished crysteel are girdered by fulcrete beams"."""
    for y in range(y0, y1):
        r = (y - y0) % 8
        for x in range(16):
            g[y][x] = "6" if r == 7 or x in (0, 15) else (light if r == 0 else mid)
    for y in range(y0, y1, 3):                                 # burnish lines along the plate
        x = rnd.randrange(2, 9)
        for i in range(rnd.randrange(3, 6)):
            if g[y][x + i] == mid:
                g[y][x + i] = dark


def _starorchid_texture(g, y0, y1, rnd, light, mid, dark):
    """Baroque: "outworld hard-shelled beings ... crushed together" - pale stone with fossil shells and magenta ribbons."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = "4"
    for _ in range(2):                                         # magenta ribbons of the shell
        x, y = 0, rnd.randrange(y0, max(y0 + 1, y1))
        for i in range(16):
            g[y][x + i] = mid
            if i % 3 == 0 and y + 1 < y1:
                g[y + 1][x + i] = dark
            y = min(y1 - 1, max(y0, y + rnd.choice((0, 1, -1))))
    for _ in range(3):
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(0, 15)
        g[y][x] = light
        g[y][x + 1] = light


def _tubing_texture(g, y0, y1, rnd, light, mid, dark):
    """Baroque: "vacuum tubes slice through circuit topography" - brass tubes over dark board, glowing in the detail colour."""
    for y in range(y0, y1):
        for x in range(16):
            f = x % 5
            g[y][x] = dark if f == 4 else (mid if f == 3 else (light if f == 0 else "4"))
    for y in range(y0 + 3, y1, 7):                             # junctions
        for x in range(16):
            g[y][x] = mid
    for _ in range(3):
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(16)
        if g[y][x] == dark:
            g[y][x] = "5"


def _verdigris_texture(g, y0, y1, rnd, light, mid, dark):
    """Golgotha: "chrome's graveyard" - riveted chrome plates gone green, rust bleeding down from the seams (detail)."""
    for y in range(y0, y1):
        r = (y - y0) % 10
        for x in range(16):
            g[y][x] = dark if r == 9 else (light if r == 0 and x % 7 else mid)
        if r == 1:
            g[y][2] = dark
            g[y][12] = dark                                    # rivets
    for _ in range(4):                                         # rust running down from a seam
        x = rnd.randrange(16)
        y = y0 + 10 * rnd.randrange(0, max(1, (y1 - y0) // 10 + 1))
        for i in range(rnd.randrange(3, 8)):
            if y0 <= y + i < y1:
                g[y + i][x] = "5" if i < 3 else "6"
    for _ in range(4):                                         # flakes
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(0, 15)
        g[y][x] = "4"


def _verdigris2_texture(g, y0, y1, rnd, light, mid, dark):
    """The same plates with other streaks, so a long Golgotha wall doesn't repeat."""
    rnd.random()
    rnd.random()
    _verdigris_texture(g, y0, y1, rnd, light, mid, dark)


def _oolite_texture(g, y0, y1, rnd, light, mid, dark):
    """Grove: "stony eggs are incubated in pearly planar sheets" - packed round grains in thin sheets."""
    for y in range(y0, y1):
        sheet = (y - y0) % 8
        for x in range(16):
            g[y][x] = dark if sheet == 7 else mid
    for y in range(y0, y1 - 1, 2):
        for x in range((y // 2) % 2, 15, 3):                   # the eggs
            if g[y][x] == mid:
                g[y][x] = light
                g[y][x + 1] = light
                if g[y + 1][x] == mid:
                    g[y + 1][x] = dark


def _gypsum_texture(g, y0, y1, rnd, light, mid, dark):
    """Rivers: "burnt crystal gold tosses its geometric shadows" - angular blades of crystal, each lit on one side."""
    for y in range(y0, y1):
        for x in range(16):
            g[y][x] = mid
    for _ in range(7):
        x, y = rnd.randrange(0, 15), rnd.randrange(y0, max(y0 + 1, y1))
        for i in range(rnd.randrange(3, 7)):
            if y + i < y1:
                xx = min(15, x + i // 2)
                g[y + i][xx] = light
                if xx + 1 < 16:
                    g[y + i][xx + 1] = dark


def _shale_texture(g, y0, y1, rnd, light, mid, dark):
    """Canyons: "clay and quartz were dried and smashed into the red rock" - thin flaking plates, unevenly stacked."""
    y = y0
    while y < y1:
        h = rnd.choice((2, 2, 3))
        off = rnd.randrange(16)
        for x in range(16):
            for r in range(h):
                if y + r < y1:
                    g[y + r][x] = dark if r == h - 1 else (light if r == 0 and (x + off) % 7 < 3 else mid)
        y += h
    for _ in range(4):                                         # flakes that broke off: a nick in the plate edge
        y, x = rnd.randrange(y0, max(y0 + 1, y1)), rnd.randrange(0, 15)
        g[y][x] = dark
        g[y][x + 1] = dark


def _sandstone_texture(g, y0, y1, rnd, light, mid, dark):
    """Canyons: "rock is eroded to sand, sand is blown into lakes" - broad cross-bedded bands that slant."""
    phase = rnd.randrange(12)
    for y in range(y0, y1):
        for x in range(16):
            band = (y - y0 + (x + phase) // 3) % 7                 # slanted dune bedding
            g[y][x] = dark if band == 6 else (light if band in (0, 1) else mid)
    for y in range(y0 + 7, y1, 8):                             # a level bedding plane cuts the slanted bands
        for x in range(16):
            g[y][x] = dark


MATERIALS = {"canvas": _canvas_texture, "rock": _rock_texture, "salt": _salt_texture, "metal": _metal_texture,
             "slab": _slab_texture, "wood": _wood_texture, "brick": _brick_texture, "stone": _stone_texture,
             "plant": _plant_texture, "shroom": _shroom_texture, "crystal": _crystal_texture, "bone": _bone_texture,
             "tech": _tech_texture, "scale": _scale_texture,
             "cage": _cage_texture, "petal": _petal_texture, "marl": _marl_texture, "limestone": _limestone_texture,
             "shale": _shale_texture, "sandstone": _sandstone_texture, "concrete": _concrete_texture,
             "stiltmarble": _stiltmarble_texture, "stiltpillar": _stiltpillar_texture, "ironbars": _ironbars_texture,
             "fulcrete": _fulcrete_texture, "vinefulcrete": _vinefulcrete_texture, "mudroot": _mudroot_texture, "crysteel": _crysteel_texture,
             "starorchid": _starorchid_texture, "tubing": _tubing_texture, "verdigris": _verdigris_texture, "verdigris2": _verdigris2_texture, "oolite": _oolite_texture, "gypsum": _gypsum_texture}
# Materials drawn as 16 N/E/S/W wall variants but reached by a runtime swap (BrightQud.cs WallSwaps), not an alias.
EXTRA_WALL_MATERIALS = ["cage", "petal", "marl", "limestone", "shale", "sandstone", "concrete", "stiltmarble", "stiltpillar", "ironbars",
                        "fulcrete", "vinefulcrete", "mudroot", "crysteel", "starorchid", "tubing", "verdigris", "verdigris2", "gypsum"]
MATERIALS.update({"ornate_" + m: _ornate(m) for m in MOTIFS})

# Wall families drawn through a runtime alias (Generated.WallAliases): the game's 256 mask variants
# of each family map onto our 16 N/E/S/W variants of one material ("brightqudwall/<material>-nesw").
ALIAS_FAMILIES = {
    "tiles/wall/wood-": "wood", "walls/wall/wood/worn-": "wood",
    "tiles/wall/stone-": "stone", "tiles/wall/granite-": "stone", "tiles/wall/oolite-": "oolite",
    "walls/wall/brick-": "brick", "tiles/wall/plant-": "plant", "tiles/wall/flower-": "plant",
    "walls/wall/mushroom-": "shroom", "tiles/wall/crystal1-": "crystal", "tiles/wall/bone-": "bone",
    "walls/wall/skull/1-": "bone", "walls/wall/skull/2-": "bone",
    "tiles/wall/circuit-": "tech", "tiles/wall/cyber-": "tech", "tiles/wall/secure-": "tech",
    "walls/wall/coolant-": "tech", "walls/wall/coolant/b-": "tech", "walls/wall/golem/interior-": "tech",
    "tiles/wall/scale-": "scale", "tiles/wall/fluted-": "ornate_fluted",
    "walls/wall/zigzag-": "ornate_zigzag", "walls/wall/filigree-": "ornate_filigree",
    "walls/sw/chevron1-": "ornate_chevron", "walls/sw/chevron2-": "ornate_chevron",
    "walls/wall/backslash-": "ornate_backslash",
    "walls/wall/nephilim/1-": "ornate_runes", "walls/wall/nephilim/2-": "ornate_runes",
}
for _m in ("diamonds", "runes", "columns", "arches", "shields", "valence"):
    ALIAS_FAMILIES[f"walls/wall/sultan/{_m}-"] = "ornate_" + _m
    ALIAS_FAMILIES[f"walls/wall/sultan/{_m}/b-"] = "ornate_" + _m


def alias_variants():
    """(nesw suffix, 8-char game mask) for the 16 variants shipped per aliased material."""
    out = []
    for i in range(16):
        n, e, s_, w = (i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1
        out.append((f"{n}{e}{s_}{w}", f"{n}0{e}0{s_}0{w}0"))
    return out


def painted_wall(material, mask="00000000", seed=1):
    """3/4 wall in a role-colored material. Top = foreground light/mid, face = mid/dark."""
    # (crc32, not hash(): string hashes change every run, so every build redrew the walls.)
    rnd = random.Random(zlib.crc32(f"{material}|{mask}|{seed}".encode()) & 0xFFFF)
    m = _bits(mask)
    face = not m["s"]
    g = _grid("2")
    top = 9 if face else 24
    MATERIALS[material](g, 0, top, rnd, "1", "2", "3")
    if not m["n"]:
        g[0] = list("1" * 16)
    if face:
        MATERIALS[material](g, top, 24, rnd, "2", "3", "O")
        g[top - 1] = list("O" * 16)       # ledge shadow
        g[top] = list("2" * 16)           # face lip catching light
        g[23] = list("O" * 16)            # dark base: "this blocks you"
    for y in range(24):
        if not m["w"]:
            g[y][0] = "3"
        if not m["e"]:
            g[y][15] = "O"
    return _rows(g)


# ---------- fences and tent edges (n/s/e/w suffix families, 16 variants) ----------

def _dirs(suffix):
    return {d: d in suffix for d in "nsew"}


def fence(suffix=""):
    """Brinestalk fence: a post with rails toward connected sides. Solid: outline + shadow."""
    d = _dirs(suffix)
    g = _grid(".")
    top = 0 if d["n"] else 9
    bottom = 24 if d["s"] else 21
    for y in range(top, bottom):
        g[y][7], g[y][8] = "1", "3"
    for y in (9, 10):
        g[y][7] = g[y][8] = "1"           # post cap
    for rail in (12, 17):
        x0 = 0 if d["w"] else 6
        x1 = 16 if d["e"] else 10
        for x in range(x0, x1):
            g[rail][x] = "1"
            g[rail + 1][x] = "3"
        if d["w"] or d["e"]:
            for x in range(x0, x1):
                if x % 5 == 2:
                    g[rail][x] = "5"      # bindings (detail color)
    return _rows(g)


def tent(suffix=""):
    """Canvas tent edge: a draped canvas strip toward connected sides, stripes in the detail color."""
    d = _dirs(suffix)
    g = _grid(".")
    x0 = 0 if d["w"] else 4
    x1 = 16 if d["e"] else 12
    y0 = 0 if d["n"] else 6
    y1 = 24 if d["s"] else 20
    for y in range(y0, y1):
        for x in range(x0, x1):
            horizontal = d["w"] or d["e"] or not (d["n"] or d["s"])
            if horizontal and not (8 <= y < 20):
                continue
            if not horizontal and not (5 <= x < 11):
                continue
            stripe = (x // 3) % 2 if horizontal else (y // 3) % 2
            g[y][x] = "5" if stripe else "2"
            if (horizontal and y == 19) or (not horizontal and x == 10):
                g[y][x] = "3"
    return _rows(g)


# ---------- doors ----------

def door_closed():
    """Wooden door: frame, plank leaf, iron bands and handle. Fills the cell like a wall face."""
    g = _grid(".")
    for y in range(2, 24):
        for x in range(1, 15):
            g[y][x] = "N"
    for y in range(4, 23):
        for x in range(3, 13):
            g[y][x] = "n" if (x - 3) % 3 else "N"
    for x in range(3, 13):
        g[4][x] = "t"
    for y in (8, 18):
        for x in range(3, 13):
            g[y][x] = "L"
    g[13][10] = g[13][11] = "y"
    g[23] = list("O" * 16)
    return _rows(g)


def door_open():
    """Open doorway: the frame only, the floor shows through (walkable)."""
    g = _grid(".")
    for y in range(2, 24):
        for x in (1, 2, 13, 14):
            g[y][x] = "N" if x in (1, 14) else "n"
    for x in range(1, 15):
        g[2][x] = "N"
        g[3][x] = "n"
    for y in range(4, 23):
        g[y][3] = "x"                      # shade inside the frame
    return _rows(g)


# ---------- plants, liquids, ground ----------

def brinestalk(seed=1):
    """Reed clump: walk-through but blocks sight (tall tier). Thin, light stalks so it stays airy;
    stalks fg, seed tips detail."""
    rnd = random.Random(seed)
    g = _grid(".")
    for x in (3, 8, 12):
        h = rnd.randrange(12, 18)
        sway = rnd.choice((-1, 1))
        for k in range(h):
            xx = x + (sway if k > h * 0.6 else 0)
            g[21 - k][xx] = "1" if k % 5 else "2"
            if k == h - 1:
                g[21 - k][xx] = "4"
    for x in (5, 10):  # a couple of short leaves near the base
        g[19][x] = g[18][x + 1] = "1"
    return _rows(g)


def puddle(seed=1):
    """Small puddle: one or two blobs, foreground ramp (the liquid's color), flat."""
    rnd = random.Random(seed)
    g = _grid(".")
    blobs = [(7.5, 13, 6, 4)] if seed % 2 else [(5.5, 9, 4, 3), (10, 16, 4.5, 3)]
    for cx, cy, rx, ry in blobs:
        cx, cy = cx + rnd.choice((-1, 0, 1)), cy + rnd.choice((-1, 0, 1))
        for y in range(24):
            for x in range(16):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1:
                    g[y][x] = "3" if d > 0.7 else ("1" if (x - cx) + (y - cy) < -1 else "2")
    return _rows(g)


def trickle(mask):
    """A few drams of liquid: a thin trickle, not a cell full of water. mask = N*8 + E*4 + S*2 + W*1, the wet
    neighbours it runs to (the game's shallow-liquid paint mask). Each arm meets the cell edge at a fixed
    point (N/S x 7-8, E/W y 12-13) so trickles in neighbouring cells join up; 0 = a small lone puddle.
    Foreground ramp (the liquid's colour), flat, mostly transparent so the ground shows."""
    rnd = random.Random(mask * 7 + 3)
    g = _grid(".")

    def dab(x, y, c="2"):
        if 0 <= x < 16 and 0 <= y < 24 and g[y][x] != "1":
            g[y][x] = c

    cx, cy = 7, 12
    arms = [(d, b) for d, b in (("N", 8), ("E", 4), ("S", 2), ("W", 1)) if mask & b]
    for d, _ in arms:
        # 3 px wide where it meets the edge, 2-4 px in between: a lit edge, the liquid, a darker edge
        if d in ("N", "S"):
            ys = range(0, cy + 1) if d == "N" else range(cy, 24)
            for y in ys:
                mid = 2 < y < 21
                wob = round(math.sin((y + mask) / 3.1) * 1.0) if mid else 0
                wide = 1 if mid and rnd.random() < 0.35 else 0
                dab(cx - 1 + wob, y, "1" if y % 4 == 1 else "2")
                dab(cx + wob, y)
                dab(cx + 1 + wob, y, "3")
                if wide:
                    dab(cx + 2 + wob, y, "3")
        else:
            xs = range(0, cx + 2) if d == "W" else range(cx, 16)
            for x in xs:
                mid = 1 < x < 14
                wob = round(math.sin((x + mask) / 2.7) * 1.0) if mid else 0
                dab(x, cy - 1 + wob, "1" if x % 5 == 2 else "2")
                dab(x, cy + wob)
                dab(x, cy + 1 + wob, "3")
                if mid and rnd.random() < 0.35:
                    dab(x, cy + 2 + wob, "3")
    # little pool where the arms meet (a lone puddle when there are none)
    # (none on a straight run: a pool in every cell read as a bead chain)
    rx, ry = (0, 0) if mask in (10, 5) else (3.2, 2.4) if arms else (3.8, 2.6)
    for y in range(24 if rx else 0):
        for x in range(16):
            d = ((x - cx - 0.5) / rx) ** 2 + ((y - cy - 0.5) / ry) ** 2
            if d <= 1:
                dab(x, y, "3" if d > 0.6 and y > cy else "1" if d > 0.6 and y < cy else "2")
    if rx:
        g[cy - 1][cx] = "1"
    # flecks in the liquid's detail colour (the lava-lit specks of primordial soup)
    for y in range(24):
        for x in range(16):
            if g[y][x] == "2" and rnd.random() < 0.18:
                g[y][x] = "5"
    if not arms:                                  # a couple of drops beside the lone puddle
        for _ in range(2):
            dab(rnd.choice((2, 3, 12, 13)), rnd.randrange(8, 17))
    return _rows(g)


def dune(seed=1):
    """Salt-dune ground: sparse specks and a short wind ripple."""
    rnd = random.Random(seed)
    g = _grid(".")
    for y in range(24):
        for x in range(16):
            if rnd.random() < 0.04:
                g[y][x] = "3"
    y = rnd.randrange(6, 18)
    for x in range(rnd.randrange(1, 5), rnd.randrange(10, 15)):
        g[y + (1 if (x // 3) % 2 else 0)][x] = "2"
    return _rows(g)


def _canopy(g, cx, cy, rx, ry, rnd):
    for y in range(24):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + rnd.random() * 0.15
            if d <= 1:
                g[y][x] = "1" if (x - cx) + (y - cy) < -rx * 0.5 else ("3" if d > 0.75 else "2")


def starapple_tree(seed=3):
    """Starapple: round canopy with star-shaped fruit (detail color), short trunk. Tall tier."""
    rnd = random.Random(seed)
    g = _grid(".")
    _canopy(g, 7.5, 7, 7, 6, rnd)
    for (x, y) in ((4, 5), (10, 4), (7, 9), (12, 9), (3, 10)):
        g[y][x] = "4"
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if g[y + dy][x + dx] != ".":
                g[y + dy][x + dx] = "5"
    for y in range(13, 21):
        g[y][7], g[y][8] = "n", "N"
    g[20][6] = g[20][9] = "n"
    for x in range(3, 13):
        g[21][x] = "x"
    return _rows(g)


def witchwood_tree(seed=5):
    """Witchwood: twisted trunk with sparse, drooping leaf clusters. Tall tier."""
    rnd = random.Random(seed)
    g = _grid(".")
    x = 8
    for y in range(21, 6, -1):
        if rnd.random() < 0.35:
            x = max(5, min(10, x + rnd.choice((-1, 1))))
        g[y][x], g[y][x + 1] = "N", "n"
    for cx, cy in ((4, 6), (11, 4), (8, 2), (12, 10), (3, 11)):
        for y in range(cy - 2, cy + 3):
            for xx in range(cx - 3, cx + 4):
                if 0 <= y < 24 and 0 <= xx < 16 and abs(xx - cx) + abs(y - cy) * 1.3 <= 3.2:
                    g[y][xx] = "1" if y < cy else ("2" if y == cy else "3")
        if 0 <= cy + 3 < 24:
            g[cy + 3][cx] = "4"            # hanging pod (detail)
    for xx in range(4, 12):
        g[22][xx] = "x"
    return _rows(g)


def boulder(seed=2):
    """Small boulder: round rock with a highlight. Object tier (it's an item you can pick up)."""
    g = _grid(".")
    cx, cy, rx, ry = 7.5, 16, 5, 4
    for y in range(24):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1:
                g[y][x] = "3" if (x - cx) + (y - cy) > 2 else "2"
    g[13][5] = g[13][6] = g[14][5] = "1"
    return _rows(g)


def crack(seed=4):
    """Stone crack / opening in the ground: dark jagged hole with lit rims. Flat."""
    rnd = random.Random(seed)
    g = _grid(".")
    x = 3
    for y in range(4, 21):
        x = max(2, min(11, x + rnd.choice((0, 1, 1, -1))))
        w = 2 + (1 if 7 < y < 17 else 0) + rnd.choice((0, 0, 1))
        for xx in range(x, min(15, x + w)):
            g[y][xx] = "O"
        if x - 1 >= 0:
            g[y][x - 1] = "3"
        if x + w < 16:
            g[y][x + w] = "1"
    return _rows(g)
