"""Extract original Qud tiles (reference only, local) from the game's Kobold atlases.

Usage: .venv/bin/python -I tools/extract_ref.py [--probe]
Reads the game install read-only; writes PNGs to reference/tiles/<lowercased tile path>.png
"""
import UnityPy, sys, struct, os, re, collections
from PIL import ImageChops

GAME = os.path.expanduser("~/.local/share/Steam/steamapps/common/Caves of Qud/CoQ_Data")
OUT = os.path.join(os.path.dirname(__file__), "..", "reference", "tiles")


def read_str(raw, p):
    n = struct.unpack_from("<i", raw, p)[0]
    s = raw[p + 4 : p + 4 + n].decode("utf-8", "replace")
    return s, (p + 4 + n + 3) & ~3


def parse_entry(raw):
    """Per-tile entry: name, asset guid, atlas guid, ..., rect (x, y, w, h)."""
    if len(raw) < 100 or len(raw) > 600:
        return None
    try:
        name, p = read_str(raw, 28)
        guid, p = read_str(raw, p)
        atlas, p = read_str(raw, p)
    except Exception:
        return None
    if len(guid) != 32 or len(atlas) != 32:
        return None
    ints = struct.unpack_from("<16i", raw, p)
    w, h, x, y = ints[8], ints[9], ints[10], ints[11]
    return name, atlas, (x, y, w, h)


def load():
    env = UnityPy.load(os.path.join(GAME, "resources.assets"))
    entries, atlases, singles = [], {}, {}
    for obj in env.objects:
        t = obj.type.name
        if t == "MonoBehaviour":
            e = parse_entry(obj.get_raw_data())
            if e:
                entries.append(e)
        elif t == "Texture2D":
            d = obj.read()
            if d.m_Name.startswith("Kobold_DynamicAtlas"):
                atlases[d.m_Name] = d.image.convert("RGBA")
            elif d.m_Width == 16 and d.m_Height == 24:
                singles[d.m_Name] = d.image.convert("RGBA")
    return entries, atlases, singles


def stem_of(name):
    """'Assets_Content_Textures_Creatures_sw_farmer.bmp' -> 'sw_farmer'."""
    base = os.path.splitext(name)[0]
    m = re.match(r"(?i)assets_content_textures_[^_]+_(.*)", base)
    return m.group(1) if m else base


def coverage(img, es):
    """Fraction of rects that land on non-empty pixels."""
    hits = 0
    for _, _, r in es[:200]:
        if r[0] + r[2] <= img.width and r[1] + r[3] <= img.height and crop(img, r).getbbox():
            hits += 1
    return hits / min(len(es), 200)


def crop(img, rect):
    x, y, w, h = rect
    # Unity rects are bottom-up; PIL images from UnityPy are already flipped top-down.
    top = img.height - y - h
    return img.crop((x, top, x + w, top + h))


def match_atlases(entries, atlases, singles):
    """Map each atlas guid to an atlas texture by comparing crops against standalone sprites."""
    by_guid = collections.defaultdict(list)
    for e in entries:
        by_guid[e[1]].append(e)
    mapping = {}
    for guid, es in by_guid.items():
        best = None
        for aname, img in atlases.items():
            score = 0
            for name, _, rect in es:
                ref = singles.get(stem_of(name))
                if ref is None or rect[0] + rect[2] > img.width or rect[1] + rect[3] > img.height:
                    continue
                if ImageChops.difference(crop(img, rect), ref).getbbox() is None:
                    score += 1
            cov = coverage(img, es)
            key = (score, cov)
            if cov > 0.9 and (best is None or key > best[1]):
                best = (aname, key)
        # Fallback: the only atlas big enough for every rect, if unique.
        if best is None:
            fits = [a for a, img in atlases.items()
                    if all(r[0] + r[2] <= img.width and r[1] + r[3] <= img.height for _, _, r in es)]
            if len(fits) == 1:
                best = (fits[0], 0)
        # Prefer the atlas named after the group's dominant texture folder, if its rects land on content.
        folders = collections.Counter(
            m.group(1).lower() for m in (re.match(r"(?i)assets_content_textures_([^_]+)_", n) for n, _, _ in es) if m)
        if folders:
            want = folders.most_common(1)[0][0]
            for aname, img in atlases.items():
                if aname.lower().replace("abilitites", "abilities") == f"kobold_dynamicatlas_{want}_1" and coverage(img, es) > 0.8:
                    best = (aname, "folder")
        mapping[guid] = best
    return by_guid, mapping


if __name__ == "__main__":
    entries, atlases, singles = load()
    by_guid, mapping = match_atlases(entries, atlases, singles)
    for g, es in sorted(by_guid.items(), key=lambda kv: -len(kv[1])):
        print(g[:8], len(es), mapping[g], es[0][0])
    if "--probe" in sys.argv:
        sys.exit()
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for name, guid, rect in entries:
        m = mapping.get(guid)
        if not m:
            continue
        path = os.path.join(OUT, name.lower() + ".png")
        crop(atlases[m[0]], rect).save(path)
        n += 1
    print("extracted", n, "of", len(entries))
