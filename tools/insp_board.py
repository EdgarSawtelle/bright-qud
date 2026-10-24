"""Inspiration board for a zone review: what people wrote about the place + pictures (fan art first,
then real-world references), each with its source. Pictures stay local (scratchpad / mockups/local).

Library use: board(path, title, quotes=[(text, source)], pics=[(image path, caption, source)])
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402


def _wrap(d, text, x, y, width, f, fill):
    line = ""
    for w in text.split():
        if d.textlength(line + " " + w, font=f) > width:
            d.text((x, y), line, font=f, fill=fill)
            y += f.size + 5
            line = w
        else:
            line = (line + " " + w).strip()
    d.text((x, y), line, font=f, fill=fill)
    return y + f.size + 5


def board(path, title, quotes, pics, cols=3, cw=420, ch=280):
    W = 20 + cols * (cw + 20)
    tmp = Image.new("RGB", (W, 4000), (24, 24, 28))
    d = ImageDraw.Draw(tmp)
    y = _wrap(d, title, 20, 14, W - 40, font(24), (240, 236, 220)) + 6
    for text, src in quotes:
        y = _wrap(d, "“" + text + "”", 30, y, W - 60, font(17), (230, 222, 196))
        y = _wrap(d, "— " + src, 50, y - 2, W - 80, font(13), (150, 150, 140)) + 6
    y += 6
    for i, (p, cap, src) in enumerate(pics):
        x = 20 + (i % cols) * (cw + 20)
        yy = y + (i // cols) * (ch + 70)
        im = Image.open(p).convert("RGB")
        im.thumbnail((cw, ch))
        tmp.paste(im, (x, yy))
        e = _wrap(d, cap, x, yy + im.height + 6, cw, font(15), (220, 215, 195))
        _wrap(d, src, x, e - 4, cw, font(12), (140, 140, 130))
    rows = (len(pics) + cols - 1) // cols
    tmp.crop((0, 0, W, y + rows * (ch + 70) + 10)).save(path)
    return path
