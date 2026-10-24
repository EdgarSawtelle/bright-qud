"""Read-only helpers for the game's ObjectBlueprints (resolves inheritance)."""
import glob, os, re
import xml.etree.ElementTree as ET

BASE = os.path.expanduser("~/.local/share/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base")


def _parse(path):
    txt = open(path, encoding="utf-8-sig").read()
    return ET.fromstring(re.sub(r"&#x?[0-9a-fA-F]+;", "?", txt))


class Blueprints:
    def __init__(self):
        self.objs = {}
        for f in glob.glob(BASE + "/ObjectBlueprints/*.xml"):
            for o in _parse(f).iter("object"):
                d = {"inh": o.get("Inherits"), "parts": {}, "tags": {}, "builders": {}}
                for p in o.findall("part"):
                    d["parts"].setdefault(p.get("Name"), {}).update(p.attrib)
                for b in o.findall("builder"):
                    d["builders"].setdefault(b.get("Name"), {}).update(b.attrib)
                for t in o.findall("tag"):
                    d["tags"][t.get("Name")] = t.get("Value")
                self.objs[o.get("Name")] = d

    def _walk(self, name):
        seen = 0
        while name in self.objs and seen < 50:
            yield self.objs[name]
            name = self.objs[name]["inh"]
            seen += 1

    def part(self, name, part, attr):
        for o in self._walk(name):
            v = o["parts"].get(part, {}).get(attr)
            if v is not None:
                return v

    def builder(self, name, builder, attr):
        for o in self._walk(name):
            v = o.get("builders", {}).get(builder, {}).get(attr)
            if v is not None:
                return v

    def tag(self, name, tag):
        for o in self._walk(name):
            if tag in o["tags"]:
                return o["tags"][tag]

    def render(self, name):
        keys = ("Tile", "ColorString", "TileColor", "DetailColor", "RenderString", "RenderLayer", "DisplayName")
        return {k: self.part(name, "Render", k) for k in keys}
