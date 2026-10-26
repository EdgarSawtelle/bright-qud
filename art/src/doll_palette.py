"""Paper doll colours and stacking order, shared by tools/doll_preview.py and tools/build_mod.py
(-> mod/BrightQud/DollTable.cs)."""

# bottom -> top (docs/PAPERDOLL_BRIEF.md); the C# runtime uses the same order
ORDER = ["back", "mutback", "body/base", "feet", "body", "hands", "mutfront", "face", "head", "muthead",
         "left", "right", "two", "offhand"]

# material -> (main, detail) colours; None keeps the item's own game colours
MATERIALS = {
    "steel": ("a8b0b8", "5c6470"), "iron": ("8e8a84", "4e4a46"), "bronze": ("c08a48", "7a5428"),
    "carbide": ("2a62d6", "8fb4ff"), "fullerite": ("3c3a4c", "9a96c0"), "crysteel": ("8fe4f0", "e0fcff"),
    "zetachrome": ("d060e0", "ffd0ff"), "plastifer": ("e0d8c0", "8a8270"), "elastyne": ("44444e", "7a7a96"),
    "leather": ("a06a3a", "5a3a1e"), "fur": ("b08a5a", "6a5030"), "wood": ("8a5a32", "53321c"),
    "linen": ("d8c8a0", "9a8a68"),
}


# Chitin palettes (shell, legs/stinger): one per character, picked from its ID (seed) at runtime.
CHITIN = [("blue/red", "4a52b8", "c8402e"), ("red/blue", "b83a2e", "3a5ed0"), ("gold/purple", "d0a020", "8a3ab8"),
          ("purple/gold", "7a3ab0", "d8a828"), ("teal/orange", "1e8a86", "e0782a")]
CHITIN_LAYERS = ("mutback/carapace", "mutfront/legs", "mutback/stinger")
CHITIN_ROLES = {"p": "1", "P": "2", "d": "3", "r": "4", "R": "5", "e": "6"}
