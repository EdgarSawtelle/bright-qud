"""Shape-based sprite drawing for 16x24 tiles: draw with lines/polygons/ellipses in tile-pixel
coordinates (floats OK), supersampled 4x, then reduced to the text grid. Think in gesture and mass,
not in single pixels; touch up single pixels with px() afterwards.

    from vkit import Canvas
    c = Canvas()
    c.line([(3, 8), (6, 12), (9, 12)], "2", w=1.2)    # polyline, width in tile pixels
    c.poly([(5, 10), (11, 9), (12, 14), (6, 14)], "2")  # filled polygon
    c.ellipse(8, 12, 3.5, 2, "2")                       # centre x, y, radius x, y
    c.erase_line([(7, 14), (7, 20)], w=1)               # cut negative space back out
    c.px(4, 9, "5")                                      # single final pixel (after shapes)
    grid = c.grid()                                      # 24 strings of 16 chars

Shapes are painted in call order (later on top). threshold = share of a 4x4 block that must be
covered for the pixel to be on (default 0.35; lower keeps thin lines, higher cleans blobs).
"""
from PIL import Image, ImageDraw

S = 4
_ERASE = "."


class Canvas:
    def __init__(self, w=16, h=24):
        self.w, self.h = w, h
        self.chars = ["."]
        self.img = Image.new("L", (w * S, h * S), 0)
        self.d = ImageDraw.Draw(self.img)
        self.over = {}

    def _v(self, ch):
        if ch == _ERASE:
            return 0
        if ch not in self.chars:
            self.chars.append(ch)
        return self.chars.index(ch)

    @staticmethod
    def _p(pts):
        return [(x * S + S / 2, y * S + S / 2) for x, y in pts]

    def line(self, pts, ch, w=1.0):
        v, P = self._v(ch), self._p(pts)
        width = max(1, round(w * S))
        self.d.line(P, fill=v, width=width, joint="curve")
        r = width / 2
        for x, y in P:  # round caps so joints don't gap
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=v)

    def poly(self, pts, ch):
        self.d.polygon(self._p(pts), fill=self._v(ch))

    def ellipse(self, cx, cy, rx, ry, ch):
        x, y = cx * S + S / 2, cy * S + S / 2
        self.d.ellipse([x - rx * S, y - ry * S, x + rx * S, y + ry * S], fill=self._v(ch))

    def erase_line(self, pts, w=1.0):
        self.line(pts, _ERASE, w)

    def erase_poly(self, pts):
        self.poly(pts, _ERASE)

    def px(self, x, y, ch):
        self.over[(x, y)] = ch

    def grid(self, threshold=0.35):
        p = self.img.load()
        rows = []
        for gy in range(self.h):
            row = ""
            for gx in range(self.w):
                counts = {}
                for yy in range(gy * S, gy * S + S):
                    for xx in range(gx * S, gx * S + S):
                        v = p[xx, yy]
                        if v:
                            counts[v] = counts.get(v, 0) + 1
                tot = sum(counts.values())
                ch = "."
                if tot >= threshold * S * S:
                    ch = self.chars[max(counts, key=counts.get)]
                row += self.over.get((gx, gy), ch)
            rows.append(row)
        return rows
