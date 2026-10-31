"""Paper doll mutation layers (mutback/*, mutfront/*, muthead/*). Fixed natural colours
(chitin n/N + t highlight, bone w/t, skin s/S), wings use roles 4-6. See docs/PAPERDOLL_BRIEF.md."""
from b3kit import C


def _poly(c, pts, ch):
    n = len(pts)
    for y in range(24):
        for x in range(16):
            inside = False
            for i in range(n):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    inside = not inside
            if inside:
                c.m(x, y, ch)


def carapace():
    """domed shell BEHIND the back: bright rim above the shoulders, dark banded plates at both sides."""
    c = C()
    c.ell(7.5, 12.8, 7.7, 7.2, "d")
    c.ell(7.5, 12.8, 6.7, 6.2, "P")
    for y in range(24):
        for x in range(16):
            if c.g[y][x] == "P" and y <= 10 and ((x - 7.5) / 7.7) ** 2 + ((y - 12.8) / 7.2) ** 2 > 0.6:
                c.g[y][x] = "p"
    for y in (11, 14, 17):          # dark seams between plates
        for x in range(0, 16):
            if c.g[y][x] in "Pp":
                c.g[y][x] = "d"
    for y in (12, 13, 15, 16, 18):  # lit face of each plate at the sides
        for x in (0, 1, 2, 3, 12, 13, 14, 15):
            if c.g[y][x] == "P" and (y in (12, 15, 18) or x in (1, 2, 13, 14)):
                c.g[y][x] = "p"
    return c.out()


def _mir(half):
    """16-col grid from 8-col left halves (mirrored)."""
    rows = []
    for h in half:
        assert len(h) == 8, h
        rows.append(h + h[::-1])
    return rows


def wings():
    """FOLDED wings (walking): two feathered arches above the shoulders and a narrow feathered edge
    down both sides of the body to the hips, ending in short feather tips. Roles 4/5/6."""
    half = [
        "........",  # 0
        "........",  # 1
        "........",  # 2
        "........",  # 3
        "........",  # 4
        "...4....",  # 5
        "..44....",  # 6
        "..455...",  # 7
        ".4455...",  # 8
        ".4455666",  # 9
        ".445666.",  # 10
        "..45....",  # 11
        ".44.....",  # 12
        "..45....",  # 13
        ".44.....",  # 14
        "..46....",  # 15
        ".45.....",  # 16
        "..6.....",  # 17
        "........", "........", "........", "........", "........", "........",
    ]
    g = _mir(half)
    return g




def wingsopen():
    """SPREAD wings (flying): a broad pennant on each side, bone leading edge, filled feather
    membrane (roles 4/5/6) with a scalloped lower edge."""
    half = [
        "ww4.....",  # 0
        "wt44....",  # 1
        "w4455...",  # 2
        "w44555..",  # 3
        "w44555..",  # 4
        "w45555..",  # 5
        "w45556..",  # 6
        "w45566..",  # 7
        "w4556...",  # 8
        "w4556...",  # 9
        "w4566...",  # 10
        "w456....",  # 11
        "w456....",  # 12
        "5455....",  # 13
        "5.56....",  # 14
        "5.5.....",  # 15
        "6.5.....",  # 16
        "..6.....",  # 17
        "........", "........", "........", "........", "........", "........",
    ]
    return _mir(half[:24])


def quills():
    """four slim bone quills fanning from each shoulder blade, calm and symmetric."""
    c = C()
    for (x1, y1) in ((1, 2), (0, 6), (0, 10), (1, 14)):
        c.line(4, 10, x1, y1, "w", mirror=True)
    for (x, y) in ((1, 2), (0, 6), (0, 10), (1, 14)):
        c.m(x, y, "t")
    c.line(6, 9, 5, 1, "w", mirror=True); c.m(5, 1, "t")
    return c.out()


def stinger():
    """segmented tail: 3-wide chitin bulbs up the left side, slimmer arch over the head, barb on the right."""
    c = C()
    for i, (x, y) in enumerate([(1, 20), (1, 17), (1, 14), (1, 11), (1, 8)]):
        c.r(x - 1, y - 1, x + 1, y + 1, "r" if i % 2 == 0 else "R")
        c.p(x - 1, y + 1, "e"); c.p(x, y + 1, "e") if i % 2 == 0 else None
    for i, (x, y) in enumerate([(1, 5), (3, 3), (5, 1), (7, 0), (9, 0), (11, 1)]):
        c.r(x, y, x + 1, y + 1, "r" if i % 2 == 0 else "R")
    c.r(12, 2, 13, 3, "R"); c.p(12, 3, "e")          # barb base
    c.r(13, 4, 13, 5, "w"); c.p(13, 6, "y")          # bone barb dropping
    c.p(14, 3, "w")
    return c.out()


def arms():
    """second raised pair: sleeve stubs (roles) up to bare skin forearms and hands."""
    c = C()
    for (sx, d, a, b) in ((2, 1, "s", "S"), (13, -1, "S", "s")):
        l = d == 1
        sl = ("1", "2") if l else ("3", "2")
        c.r(sx - 1, 9, sx + 1, 10, sl[1]) if False else None
    # left
    c.r(2, 9, 3, 10, "2"); c.p(2, 9, "1"); c.p(3, 9, "1")
    c.r(2, 7, 3, 8, "2"); c.p(2, 7, "1"); c.p(2, 8, "1")
    c.r(1, 5, 3, 6, "s"); c.p(0, 5, "s"); c.p(1, 4, "s"); c.p(3, 4, "s"); c.p(1, 6, "S")
    c.p(2, 5, "S") if False else None
    # right
    c.r(12, 9, 13, 10, "3"); c.p(13, 9, "2"); c.p(13, 10, "2")
    c.r(12, 7, 13, 8, "3"); c.p(13, 7, "2")
    c.r(12, 5, 14, 6, "S"); c.p(15, 5, "S"); c.p(14, 4, "S"); c.p(12, 4, "S"); c.p(14, 6, "S")
    c.p(12, 5, "s")
    return c.out()


def legs():
    """a jointed chitin leg stepping out in front on each side of the hem (thigh, knee, shin, claw)."""
    c = C()
    for d in (1, -1):
        X = (lambda x: x) if d == 1 else (lambda x: 15 - x)
        for (x, y, ch) in ((1, 15, "r"), (2, 16, "r"), (0, 16, "r"),            # knee peak
                           (3, 17, "R"), (2, 17, "R"), (1, 17, "e"), (0, 17, "R"),  # thigh + joint
                           (1, 18, "R"), (0, 18, "R"),
                           (1, 19, "R"), (0, 19, "r"), (1, 20, "R"), (0, 20, "r"),  # shin
                           (1, 21, "R"), (0, 21, "R"),
                           (0, 22, "e"), (1, 22, "e"), (2, 22, "e")):           # claw foot
            c.p(X(x), y, ch)
    return c.out()


def twoheads():
    """second head on the right shoulder with a visible neck rising out of the shoulder line."""
    c = C()
    c.r(12, 3, 14, 3, "N")
    c.r(11, 4, 15, 4, "N"); c.p(14, 4, "s"); c.p(15, 4, "S")
    c.r(11, 5, 15, 5, "s"); c.p(15, 5, "S"); c.p(12, 5, "O"); c.p(14, 5, "O")
    c.r(11, 6, 15, 6, "s"); c.p(15, 6, "S"); c.p(13, 6, "S")
    c.r(12, 7, 14, 7, "s"); c.p(14, 7, "S"); c.p(13, 7, "R")
    c.r(12, 8, 13, 8, "s"); c.p(13, 8, "S")
    c.r(11, 9, 14, 9, "s"); c.p(14, 9, "S")
    c.r(10, 10, 13, 10, "s"); c.p(13, 10, "S")
    return c.out()


def beak():
    c = C()
    c.r(7, 5, 8, 5, "y")
    c.r(6, 6, 9, 7, "y")
    c.r(7, 8, 8, 8, "y")
    c.r(6, 7, 9, 7, "t")
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.p(6, 6, "w"); c.p(7, 5, "w")
    c.p(8, 8, "t")
    return c.out()


def claws():
    c = C()
    c.mr(3, 14, 4, 16, "s")
    c.mr(3, 16, 4, 16, "S")
    c.line(3, 17, 1, 21, "w", mirror=True)
    c.line(4, 17, 3, 22, "w", mirror=True)
    c.line(2, 17, 0, 19, "w", mirror=True)
    c.m(1, 21, "t"); c.m(3, 22, "t"); c.m(0, 19, "t")
    return c.out()


def fur():
    c = C()
    c.mr(2, 8, 5, 9, "n")
    c.mr(1, 10, 3, 13, "n")
    c.mr(2, 8, 4, 8, "t")
    for y in range(9, 14, 2):
        c.m(1, y, "N"); c.m(2, y + 1, "N")
    c.m(0, 12, "n"); c.m(0, 14, "N"); c.m(1, 15, "n")
    for x in range(3, 13):
        c.p(x, 21, "n" if x % 2 else "N")
    c.m(2, 20, "n"); c.m(3, 20, "N")
    return c.out()


def horns():
    c = C()
    for d in (0, 1):
        f = (lambda x: x) if d == 0 else (lambda x: 15 - x)
        for (x, y, ch) in ((5, 4, "t"), (4, 4, "w"), (4, 3, "w"), (3, 3, "w"), (3, 2, "w"), (2, 2, "t"),
                           (2, 1, "w"), (2, 0, "w"), (3, 0, "t"), (5, 3, "t")):
            c.p(f(x), y, ch)
    return c.out()


LAYERS = {
    "mutback/carapace": carapace(), "mutback/wings": wings(), "mutback/wingsopen": wingsopen(), "mutback/quills": quills(),
    "mutback/stinger": stinger(), "mutfront/arms": arms(), "mutfront/legs": legs(),
    "mutfront/twoheads": twoheads(), "mutfront/beak": beak(), "mutfront/claws": claws(),
    "mutfront/fur": fur(), "muthead/horns": horns(),
}
