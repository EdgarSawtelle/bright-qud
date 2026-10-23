"""Batch 3b creatures (30 tile keys)."""
from kit import E, compose, human, TURBAN, STAFF
from kit2 import body


def _fx(d):
    return {k: (v + "." * (16 - len(v)) if len(v) < 16 else v) for k, v in d.items()}

# ---------------- humanoid parts ----------------
# disciple: red hood-wrap blindfold
BLINDFOLD = {7: "...5555555555...", 8: "...5666666665...", 9: "....srssssrs...."}
SW_ROBE = {14: "...2222222222...", 15: "..s2122222222s..", 16: "..s2222222222s..",
           17: "...3222222223...", 18: "...2222222222...", 19: "...3333333333...",
           20: "....xNNxxNNx....", 13: "....44444444....", 12: "...s22222222s..."}
SW_SASH = {14: "....44444444....", 15: "...s24422222s...", 16: "...s22244222s..."}
STRAW_HAT = {2: "......tttt......", 3: "....tttttttt....", 4: "..tttttttttttt..",
             5: "...tttNNNNttt...", 6: "...ssssssssss...", 7: "...ssssssssss..."}
OVERALLS = {14: "....55555555....", 15: "...s25555552s...", 16: "...s25555552s...",
            17: "....55555555....", 18: "....55....55...."}
BANANAS = {14: "..............yy", 15: ".............yyy", 16: "............yyy.", 17: "...........yy..."}
BANDANA = {5: "....rrrrrrrr....", 6: "...rRRRRRRRRr..."}
CANNIB_MOHAWK = {2: ".......55.......", 3: "......5555......", 4: "......5555......",
                 5: "......6666......", 6: "...ssssssssss..."}
SYRINGE = {11: "..............ww", 12: ".............wL.", 13: "............wL..", 14: "...........rr...",
           15: "...........rs...", 16: "...........s...."}
BANDOLIER = {14: "....33rrrrrr....", 15: "...s2rr2222rs...", 16: "...s2r2rr222s..."}
MISSILE = {10: ".............rr.", 11: "............wrr.", 12: "...........wLr..", 13: "..........wL....",
           14: "...........s...."}
CROWN_HELM = {1: ".......44.......", 2: "......4554......", 3: "....44llll44....",
              4: "....llllllll....", 5: "...lwlllllllL...", 6: "...llllllllllL..",
              7: "...LLLLLLLLLLL..", 8: "...L........L..."}
KNIGHT_ARMOR = {13: "...444444444....", 14: "..2lllllllllll2.",
                15: "..2lL44444LLl2s.", 16: "...lLllllllLl...", 17: "...3222222223..."}
BROADSWORD = {y: ".............l.." for y in range(3, 14)} | {2: ".............w..", 14: "...........yyyy.",
              15: "............ns.."}
DERVISH_HOOD = {3: "......1111......", 4: "....11111111....", 5: "...1122222211...",
                6: "..112222222211..", 7: "..122222222221..", 8: "..12........21..",
                9: "..12........21.."}
DERVISH_SKIRT = {13: "....22222222....", 14: "...1222222221...", 15: "..112222222211..",
                 16: ".11222222222211.", 17: ".11222222222211.",
                 18: "1122222222222211", 19: "3333333333333333", 20: "...xxxxxxxxxx..."}
SPIN_ARMS = {12: "5..s........s..5", 13: "55s..........s55", 14: ".5..............",
             15: "...............5"}
DER_CLEAN = {16: "..1222222222211.", 17: ".11222222222211.", 18: "1122222222222211"}
ABBOT_HAT = {1: ".....666666.....", 2: "....66666666....", 3: "...6666666666...", 4: "...6555555556...",
             5: "...5555555555...", 6: "...5ssssssss5...", 7: "...ssssssssss..."}
TRASH_ARMOR = {13: "...5522222255...", 14: "..552lll22225...", 15: "..s52L4L222L5s..",
               16: "..s5222222L25s..", 17: "...5LLLLLLL5....", 18: "...5522222255...",
               19: "...3333333333...", 20: "....xNNxxNNx...."}
ABBOT_BEARD = {10: "....ww....ww....", 11: "....wwwwwwww....", 12: "....wwwwwwww....", 13: ".....wwwwww....."}


# ---------------- creature bodies ----------------
def sym(*halves):
    return [h + h[::-1] for h in halves]


def put(rows, y, x, text):
    r = rows[y].ljust(16, ".")
    rows[y] = r[:x] + text + r[x + len(text):]
    return rows


WORM = body(sym(
    "..44...", ".5444..", "...5444", "...1111", "..11111", ".111111", ".11wO11", ".111111",
    ".1122OO", "..22111", "..22211", ".222221", "..33222", "...3333"))

CRAB = body(sym(
    "w2......", "2112....", "21122...", ".2112222", "..221111", ".2211111", ".2111w11",
    ".2111111", ".2211OOO", "..222222", "..3.33.3", ".3.3...."))

FISH = body(sym(
    ".....44.", "....4455", "..222222", ".2211111", ".211wO11", ".2111111", ".21OOOOO",
    ".22w2w2w", "..222222", "4.552222", ".44.3333", "...4.44."))

FLY = body(sym(
    "ww..5..", "www.4..", "wwww.11", "www.222", "ww.2111", "w.21wO1", "..21111", "...2OO1",
    "..22222", ".222555", ".222222", "..33333", "...3.3."))

RANCHER = human(STRAW_HAT, OVERALLS, BANANAS)
CYCLOPS = body(sym(
    "......22", "....2222", "..222222", "..222222", "..224444", "..244www", "..244wOO",
    "..244www", "..224444", "..2244OO", ".2222222", "22.22111", "22.22111", "22.22211",
    "2..22222", "2..33.33"))
CANNIBAL = human(CANNIB_MOHAWK, BANDOLIER, SYRINGE)
BASILISK = body(sym(
    "...3..33", "..322222", ".3222222", ".2211111", ".21yO111", ".2111111", ".2211111",
    "..2OOOOO", "..222222", ".2222222", "22225522", "2.222222", "33.33333", "3...3.33"))
DACCA = body(sym(
    "4...44..", "54.4545.", ".5445555", "..222222", ".2211111", ".21wO111", ".2111111",
    ".2OOOOOO", ".2wOwOwO", "..2OOOOO", "..222222", "...3222.", "..3.3.3."))

FLAMINGO = body([
    "....1111....",
    "...122222...",
    "...12wO2555.",
    "...122225...",
    "....2222....",
    "....122.....",
    "...1222.....",
    "..111222222.",
    ".1111222222.",
    ".1144552222.",
    ".1155552222.",
    "..155552233.",
    "..22222333..",
    "...333333...",
    "....5..5....",
    "....5..5....",
    "....5..5....",
    "...55.55....",
])

KNIGHT = human(CROWN_HELM, KNIGHT_ARMOR, BROADSWORD)

CATAPULT = body([
    ".1111...........",
    ".1221...........",
    "..55............",
    "...55...........",
    "....55..........",
    ".....55.........",
    ".....55.........",
    "....1111111111..",
    "...122222222223.",
    "...2222LL222223.",
    "..12222222222233",
    "..NNN......NNN..",
    ".NNONN....NNONN.",
    ".NNNNN....NNNNN.",
], bottom=20)

CUPOLA = body(sym(
    ".....111", "...11111", "..11w111", ".11w1111", ".1111111", "11111445", "11111555",
    "22111155", "22222222", "33222222", "3.33.33."))

DERVISH = human(TURBAN, {
    12: "s..s22222222s..s", 13: ".s.1222222221.s.", 14: "..112222222211..",
    15: ".11222222222211.", 16: "1122444444442211", 17: "3333333333333333",
    18: "..xxxxxxxxxxxx..", 19: "................", 20: "................"})

SLYNTH = body(sym(
    "....5544", "...22222", "..222222", "..2wO111", "..211111", "...22111", "....2222",
    "...22111", "..221111", "..221444", "..222222", "...3333.", "..33..33"))
put(SLYNTH, 18, 14, "55")
put(SLYNTH, 19, 15, "5")

ABBOT = human(ABBOT_HAT, TRASH_ARMOR, ABBOT_BEARD, STAFF)

SITTER = body(sym(
    "....1111", "..111111", ".1111111", ".1w11111", "11144www", "1114wOOO", "11144www",
    "11222222", "..222222", "...33333", "..5.5...", ".5.5...."))

WREN = body(sym(
    ".....55", "...1111", "..11111", "..1wO11", "..1111y", ".112222", "1122444",
    "1122545", ".222554", "..22222", "...3333", "....5.."))

SNAIL = body([
    "..........1.....",
    ".........11.....",
    "........1221....",
    "........5555....",
    ".......122221...",
    ".O..O..555555...",
    ".s..s.12222221..",
    ".s..s.55555555..",
    ".sssss12222223..",
    ".ssssssssss3333.",
    "ssOwsssssssSSS..",
    ".SSSSSSSSSSSS...",
])

EATER = body(sym(
    "....4455", "..445544", ".4554554", ".5445545", "..222222", ".2211111", ".2111www",
    ".2111wOO", ".2211www", "..222222", ".2.22.22", "2..2.2.2", "5..3..3."))

EEL = body([
    ".4..1111........",
    "...111111..4....",
    "..11wO2111......",
    "..11OOO2211.....",
    "...12222221.....",
    ".4..222222221...",
    "......2222222211",
    ".4......22222221",
    ".........3222222",
    "........332222..",
    ".......3322222..",
    "......3322222...",
    ".....3322222....",
    "....3322221.....",
    "....332211......",
    "...33321........",
])

JELLY = body(sym(
    ".....111", "...11111", "..11w111", ".11w1111", ".1OO1444", "11111444", "22222222",
    "4.5.4.5.", ".4.5.4.5", "4.5.4.5.", ".5.4..4."), bottom=20)

HERMIT = body([
    ".......1111.....",
    "......122221....",
    ".....12255221...",
    ".44..122552221..",
    "4554.1222222221.",
    "4554.1222222223.",
    ".O.O.122222223..",
    ".4444.1222233...",
    "45555.3333333...",
    "4554555555......",
    "5.5.5.5.5.5.....",
])

ANEMONE = body(sym(
    "4..5..4.", ".45.45.4", "..224455", ".2211111", ".21wO111", ".2111111", ".21OOOOO",
    ".21OOO44", "..221455", "..222455", "...3.45.", "..333333"))

LAMPREY = body(sym(
    "...2222", "..22www", ".22wOOO", ".22wOOO", ".222www", "..22222", "..1wO22", "...2222",
    "..22444", "...2222", "..22444", "...2222", "....333"))

PYRAMID = body(sym(
    ".......1", "......11", ".....111", "....1111", "...11111", "..111111", ".1114www",
    ".114wOOO", ".1114www", "11222222", "22222233", "33333333"), bottom=18)

APE = body(sym(
    "4...5...", "....1111", "...11111", "...1wO11", "...14444", "..222222", ".2211111",
    "2211?444".replace("?", "1"), "22112222", "2.112222", "2.332222", "2..3.33."))

CRUNGLE = body(sym(
    "......11", "....1111", "..111111", ".1114111", ".11wO111", "11111111", "1112B111",
    "11114111", "22222222", "22BB2222", ".3333333", "..3.3.3."))

def shade(g):
    """Darken 1->2, 2->3 and add a light rim (1) on top/left edges for volume."""
    t = [list(r.replace("2", "3").replace("1", "2")) for r in g]
    o = [r[:] for r in t]
    for y in range(24):
        for x in range(16):
            if t[y][x] == "2" and (y == 0 or t[y - 1][x] == "." or x == 0 or t[y][x - 1] == "."):
                o[y][x] = "1"
    return ["".join(r) for r in o]


BASILISK, PYRAMID, CYCLOPS, FISH = (
    shade(g) for g in (BASILISK, PYRAMID, CYCLOPS, FISH))


def grad(g, a, b):
    """Replace S by 1/2/3 according to x+y (light top-left, dark bottom-right)."""
    return ["".join(("1" if x + y <= a else "2" if x + y <= b else "3") if c == "S" else c
                    for x, c in enumerate(r)) for y, r in enumerate(g)]


WORM = body([
    "..11111.....g...",
    ".1222221...gGg..",
    ".2wOOOw2....G...",
    ".2OOOOO2.....g..",
    ".2wOOOw2....gG..",
    "..2222221111g...",
    "..12222222222...",
    "..33333333323...",
    "....12222222221.",
    "....22222222223.",
    "....3333333333..",
    "...1222222221...",
    "..122222222223..",
    "..333333333333..",
    ".EEEEeEEEEEEEE..",
    "EEeEEEEEEEEeEEEE",
], bottom=20, shadow=False)
CRAB = body([
    "11.11......22.33",
    "12.12......22.33",
    "122222....222233",
    ".1222......2233.",
    "..122......233..",
    "...1111111222...",
    "..1w11111122223.",
    ".11111112222233.",
    ".11111122222233.",
    ".12222222222233.",
    ".2222222OO23333.",
    "..222222333333..",
    ".3.3.3....3.3.3.",
    "3.3.3......3.3.3",
], bottom=20)
APE = grad(body(sym(
    "...44555", "....SSSS", "...SSSSS", "...33333", "...SwOSS", "...S4444", "....4OOO",
    ".SSSSSSS", "SSSSSSSS", "SSSS44SS", "SS.SSSSS", "SS.SSSSS", "SS.SSSSS", "SS..SSSS",
    "3S..SSSS", "33..33SS"), bottom=20), 15, 22)
FLY = grad(body(sym(
    "..w....", "...w...", "..rrSSS", ".rwrrSS", ".rrrrSS", ".RrrrSS", "..RRSSS", "..SSSSS",
    ".SS5555", ".SSSSSS", ".SS5555", "..SSSSS", "..3.3.3"), bottom=20), 20, 26)

HUMANOID3B = {"rancher", "cannibal", "knight", "dervish", "abbot"}

CREATURES3B = {
    "worm3b": WORM, "crab3b": CRAB, "fish3b": FISH, "fly3b": FLY, "rancher": RANCHER,
    "cyclops3b": CYCLOPS, "cannibal": CANNIBAL, "basilisk3b": BASILISK, "dacca3b": DACCA,
    "flamingo3b": FLAMINGO, "knight": KNIGHT, "catapult3b": CATAPULT, "cupola3b": CUPOLA,
    "dervish": DERVISH, "slynth3b": SLYNTH, "abbot": ABBOT, "sitter3b": SITTER,
    "wren3b": WREN, "snail3b": SNAIL, "eater3b": EATER, "eel3b": EEL, "jelly3b": JELLY,
    "hermit3b": HERMIT, "anemone3b": ANEMONE, "lamprey3b": LAMPREY, "pyramid3b": PYRAMID,
    "ape3b": APE, "crungle3b": CRUNGLE,
}

DISCIPLE = human(BLINDFOLD, SW_ROBE, STAFF)
CHROMELING = body(sym(
    "....1111", "..111111", ".11w1111", ".11yO111", ".1111111", ".2211222", "2.221111",
    "22111w11", "2211?1?1".replace("?", "4"), "22112222", "2.222222", "2.333333", "..3.3.3."))
CREATURES3B["disciple"] = DISCIPLE
CREATURES3B["chromeling3b"] = CHROMELING
HUMANOID3B.add("disciple")

KEYS3B = {k: (v, "object") for k, v in {
    "creatures/sw/sprouting/worm": "worm3b",
    "creatures/sw/sightless/disciple": "disciple",
    "creatures/sw/plated/chromeling": "chromeling3b",
    "creatures/sw/kingcrab": "crab3b",
    "creatures/sw/weird/fish": "fish3b",
    "creatures/sw/fruitfly": "fly3b",
    "creatures/sw/rancher": "rancher",
    "creatures/sw/cyclops": "cyclops3b",
    "creatures/juicing-cannibal": "cannibal",
    "creatures/sw/basilisk": "basilisk3b",
    "creatures/sw/dacca": "dacca3b",
    "creatures/sw/flamingo/2": "flamingo3b",
    "creatures/sw/templar/leader": "knight",
    "creatures/sw/catapult": "catapult3b",
    "creatures/sw/cupola": "cupola3b",
    "creatures/sw/dervish2": "dervish",
    "creatures/sw/slynth": "slynth3b",
    "creatures/sw/elder/trash/monk": "abbot",
    "creatures/sw/orb/legged": "sitter3b",
    "creatures/sw/chavvah/bird": "wren3b",
    "creatures/sw/cone/snail": "snail3b",
    "creatures/sw/memory/eater": "eater3b",
    "creatures/sw/eel/2": "eel3b",
    "creatures/sw/jelly": "jelly3b",
    "creatures/sw/reef/hermit": "hermit3b",
    "creatures/sw/anemone/1": "anemone3b",
    "creatures/sw/trining/lamprey": "lamprey3b",
    "creatures/sw/pyramid4": "pyramid3b",
    "creatures/sw/dawning/ape": "ape3b",
    "creatures/sw/dreamcrungle": "crungle3b",
}.items()}


# Redrawn by the orchestrator after review (worm and ape read poorly).
CREATURES3B["worm3b"] = body([
    "...22222.......",
    "..2OOOOO2......",
    "..2OwwwO2......",
    "..2OOOOO2..g...",
    "..1222223.gGg..",
    "...33333...g...",
    "...1222223.....",
    "....3333333....",
    "....122222223..",
    ".....333333333.",
    "......1222222223",
    "...eEeE333333333",
    "..eEEeeEEeeEEeE.",
])
CREATURES3B["ape3b"] = body([
    "......44......",
    ".....4554.....",
    "....222222....",
    "...23333332...",
    "...2O2222O2...",
    "...2w2112w2...",
    "....211112....",
    "..2222222222..",
    ".222222222222.",
    "22.21155112.22",
    "22.21111112.22",
    "2..22222222..2",
    "3..222..222..3",
    "33.33....33.33",
])
