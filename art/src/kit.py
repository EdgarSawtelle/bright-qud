"""Character kit: shared caricature bases + overlay parts, so related characters stay consistent.

compose(base, *overlays): overlays are dicts {row: string}; '.' in an overlay keeps what's below,
'_' erases to transparent. All rows are 16 wide (checked).
Roles: 1-3 foreground light/mid/dark, 4-6 detail light/mid/dark (the game's colors at runtime).
"""

E = "................"


def compose(base, *overlays):
    g = [list(r) for r in base]
    assert len(g) == 24 and all(len(r) == 16 for r in g), "base must be 16x24"
    for ov in overlays:
        for y, row in ov.items():
            assert len(row) == 16, (y, row, len(row))
            for x, ch in enumerate(row):
                if ch == "_":
                    g[y][x] = "."
                elif ch != ".":
                    g[y][x] = ch
    return ["".join(r) for r in g]


# ---------------- humanoid (big head, short body, seen slightly from above) ----------------

HUMAN = [
    E, E, E, E,
    ".....ssssss.....",
    "....ssssssss....",
    "...ssssssssss...",
    "...ssssssssss...",
    "...ssssssssss...",
    "...ssssssssss...",
    "...ssOOssOOss...",
    "...ssOwssOwss...",
    "....srssssrs....",
    ".....SSSSSS.....",
    "....22222222....",
    "...s21222222s...",
    "...s22222222s...",
    "....33nnnn33....",
    "....55555555....",
    ".....55..55.....",
    "....xNNxxNNx....",
    "...xxxxxxxxxx...",
    "....xxxxxxxx....",
    E,
]

HAIR_SHORT = {4: ".....NNNNNN.....", 5: "....NNNnNNNN....", 6: "...NNnnNNNNNN...",
              7: "...NNNNNNNNNN...", 8: "...N........N..."}
HAIR_LONG = {**HAIR_SHORT, 9: "...N........N...", 10: "..NN........NN..", 11: "..NN........NN..",
             12: "..NN........NN.."}
HAIR_WILD_GREY = {3: "..l..l.ll..l....", 4: ".llllllllllll...", 5: "lllwllllllllll..",
                  6: ".ll.........ll..", 7: ".l...........l.."}
BALD = {4: ".....swwsss.....", 5: "....swssssss...."}
HOOD = {3: "......3333......", 4: "....33333333....", 5: "...3322222233...", 6: "..332222222233..",
        7: "..322222222223..", 8: "..32........23..", 9: "..32........23..", 10: "..32........23..",
        11: "..32........23..", 12: "..33........33..", 13: "...3........3..."}
TURBAN = {3: ".....444444.....", 4: "....45555554....", 5: "...4555445554...", 6: "...5554555555...",
          7: "...6666666666..."}
GOGGLES = {7: "...LLLLLLLLLL...", 8: "...L44LLLL44L...", 9: "...L45LLLL45L..."}
HELMET = {3: "......lllll.....", 4: "....llllllll....", 5: "...lwlllllllL...", 6: "...llllllllllL..",
          7: "...LLLLLLLLLLL..", 8: "...L........L..."}
BEARD = {12: "....lslllsl.....", 13: "....llllllll....", 14: "....lllllll.....", 15: ".....lllll......"}
ROBE = {14: "...2222222222...", 15: "..s2122222222s..", 16: "..s2222222222s..", 17: "...3222222223...",
        18: "...2222222222...", 19: "...3333333333...", 20: "....xNNxxNNx...."}
APRON = {16: "....45555554....", 17: "....5555555.....", 18: "....5555555....."}
ARMOR = {14: "....llllllll....", 15: "...sLlllllllLs..", 16: "...sLLllllLL.s.."}

# Things held in the right hand (screen right, cols 12-14) or left hand.
STAFF = {y: "..............n." for y in range(6, 22)} | {5: ".............yyy", 4: "..............y."}
SPEAR = {y: ".............n.." for y in range(5, 22)} | {2: ".............l..", 3: "............lll.",
                                                      4: ".............l.."}
BOW = {9: ".............n..", 10: "..............n.", 11: "..............n.", 12: "..............n.",
       13: ".............ln.", 14: "............sln.", 15: ".............ln.", 16: "..............n.",
       17: "..............n.", 18: "..............n.", 19: ".............n.."}
SWORD = {y: ".............l.." for y in range(6, 14)} | {14: "............yyy.", 15: ".............s.."}
GUN = {15: "............LLLL", 16: "............sL..", 17: ".............L.."}
CLUB = {10: ".............NN.", 11: "............NNN.", 12: "............NnN.", 13: ".............n..",
        14: ".............n..", 15: "............sn..", 16: ".............n.."}
AXE = {9: "............ll..", 10: "...........llln.", 11: "............lln.", 12: ".............n..",
       13: ".............n..", 14: ".............n..", 15: "............sn..", 16: ".............n.."}
NET = {12: ".l.l............", 13: "l.l.l...........", 14: ".l.l............", 15: "l.l.s...........",
       16: ".l.l............", 17: "l.l.l...........", 18: ".l.l............"}
WRENCH = {12: "............l.l.", 13: "............lll.", 14: ".............l..", 15: "............sl.."}
BOOK = {15: ".44s............", 16: ".54.............", 17: ".55............."}
GEAR = {14: "..l.l...........", 15: ".lll............", 16: "..ls............"}
HOE = {y: ".............n.." for y in range(11, 21)} | {20: "............lll."}


def human(*parts):
    return compose(HUMAN, *parts)


# ---------------- snapjaw (hyena-folk) ----------------

SNAPJAW = [
    E, E,
    "...2........2...",
    "...22......22...",
    "...252....252...",
    "...2222222222...",
    "..222222222222..",
    "..212222222212..",
    "..22rO2222rO22..",
    "..2222tttt2222..",
    "...22ttttttt22..",
    "....ttOttOtt....",
    "....wOwOwOwO....",
    ".....tttttt.....",
    "...2255555522...",
    "..t2252222522t..",
    "..t.22222222.t..",
    "....22222222....",
    ".....33..33.....",
    ".....33..33.....",
    "....xttxxttx....",
    "...xxxxxxxxxx...",
    "....xxxxxxxxx...",
    E,
]
SJ_HEADBAND = {6: "..555555555555.."}
SJ_FEATHERS = {0: "....4..4..4.....", 1: "....5..5..5.....", 2: "...25.25.252...."}
SJ_WARPAINT = {7: "..2r222222r212..", 9: "..22r2tttt2r22.."}
SJ_HOWL = {11: "....ttOOOOtt....", 12: "....wOOOOOOw....", 13: ".....tOOOOt....."}
SJ_BULK = {14: "..222555555222..", 15: ".t22252222522 2t".replace(" ", "2"), 16: ".t2222222222222t",
           17: "...2222222222...", 18: "....33....33....", 19: "....33....33....", 20: "...xttxxxxttx..."}
SJ_BELLY = {16: "..t22211112222t.", 17: "...2211111122...", 18: "....22111122...."}
SJ_CAPE = {14: "..6255555526....", 15: ".66225222252266.", 16: ".66.22222222.66.", 17: ".66.22222222.66."}
SJ_BONE = {15: "..........wwww..", 16: "...........ww..."}


def snapjaw(*parts):
    return compose(SNAPJAW, *parts)


# ---------------- creatures ----------------

CREATURES = {
    "convert": human(HOOD, ROBE, GEAR),
    "mehmet": human(HAIR_SHORT, BEARD, APRON, HOE),
    "argyve": human(HAIR_WILD_GREY, GOGGLES, APRON, WRENCH),
    "irudad": human(BALD, BEARD, ROBE, STAFF),
    "yrame": human(HELMET, ARMOR, SPEAR),
    "nima": human(HAIR_LONG, ROBE, BOOK),
    "snapjaw_hunter": snapjaw(SJ_HEADBAND, BOW),
    "snapjaw_brute": snapjaw(SJ_BULK, CLUB),
    "snapjaw_warrior": snapjaw(SJ_WARPAINT, AXE),
    "snapjaw_warlord": snapjaw(SJ_FEATHERS, SJ_CAPE, SWORD),
    "snapjaw_spearthrower": snapjaw(SJ_HEADBAND, SPEAR),
    "snapjaw_netter": snapjaw(NET),
    "snapjaw_howler": snapjaw(SJ_HOWL, SJ_WARPAINT),
    "snapjaw_feeder": snapjaw(SJ_BELLY, SJ_BONE),
    "snapjaw_gunner": snapjaw(SJ_HEADBAND, GUN),
    # Dromad trader: camel-folk with a long snout and a pack.
    "dromad": [
        E, E,
        "....2......2....",
        "....22....22....",
        "...2222222222...",
        "...2222222222...",
        "..2O22222222O2..",
        "..2w22222222w2..",
        "...2211111122...",
        "....21111112....",
        "....11O11O11....",
        ".....111111.....",
        "......3333......",
        "..55.555555.55..",
        ".5545444444545..",
        ".55s44444444s5..",
        ".555.444444.55..",
        ".....444444.....",
        ".....33..33.....",
        ".....33..33.....",
        "....x33xx33x....",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E,
    ],
    "cat": [
        E, E, E, E, E, E,
        "...2.......2....",
        "...22.....22....",
        "...2222222222...",
        "..222222222222..",
        "..22cO2222Oc22..",
        "..222222222222..",
        "..w22221122 2w..".replace(" ", "2"),
        "...22211112 2...".replace(" ", "2"),
        "....22222222....",
        "....21111112...2",
        "...2211111122.2.",
        "...2222222222.2.",
        "...2222222222.2.",
        "...33.3333.33...",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E, E,
    ],
    "dog": [
        E, E, E, E, E,
        "...22......22...",
        "..2222....2222..",
        "..322222222223..",
        "..222222222222..",
        "..22Ow2222Ow22..",
        "..222111111222..",
        "...2211OO1122...",
        "....21111112....",
        ".....555555.....",
        "....22222222....",
        "...2222222222.2.",
        "...2122222222.2.",
        "...2222222222.2.",
        "...22.2222.22...",
        "...33.3333.33...",
        "..xxxxxxxxxxxx..",
        "...xxxxxxxxxx...",
        E, E,
    ],
    "goat": [
        E, E,
        "..ll........ll..",
        "...ll......ll...",
        "....l2222222l...",
        "..22222222222 2.".replace(" ", "2"),
        "...2O222222O2...",
        "...2w222222w2...",
        "....22222222....",
        ".....211112.....",
        ".....11OO11.....",
        "......1ll1......",
        ".......ll.......",
        "....22222222....",
        "...2222222222...",
        "...2122222222...",
        "...2222222222...",
        "...33.3333.33...",
        "...33.3333.33...",
        "...NN.NNNN.NN...",
        "..xxxxxxxxxxxx..",
        "...xxxxxxxxxx...",
        E, E,
    ],
    # Glowpad: a lily-pad creature that glows (detail).
    "glowpad": [
        E, E, E, E, E, E, E, E, E, E, E,
        "......4444......",
        "....44555544....",
        "...4552222554...",
        "..452211112254..",
        "..522O1111O225..",
        "..522211112225..",
        "..352222222253..",
        "...3322222233...",
        ".....333333.....",
        "...xxxxxxxxxx...",
        E, E, E,
    ],
    "dragonfly": [
        E, E, E, E, E, E,
        ".44...........44",
        ".454.........454",
        "..454..22...454.",
        "...454O22O454...",
        "....45522554....",
        "......2112......",
        "......2222......",
        "......2332......",
        ".......22.......",
        ".......32.......",
        ".......22.......",
        ".......32.......",
        ".......3........",
        E, E,
        "......xxxx......",
        E, E,
    ],
    # Qudzu: creeping vine mass with red buds (detail).
    "qudzu": [
        E, E, E, E, E, E, E, E,
        "...1.....1......",
        "..121...121..1..",
        ".12221.12221121.",
        ".2232212232212 2".replace(" ", "2"),
        "..2322422232242.",
        ".122223222332221",
        "1222421222242221",
        ".2333223332232 3".replace(" ", "3"),
        "..23.32..23.32..",
        "...3..3...3..3..",
        E, E, E, E, E, E,
    ],
    # Dreadroot: gnarled root creature with a gaping knot mouth.
    "dreadroot": [
        E, E, E, E,
        "......1.........",
        ".....121...1....",
        "...12222112 1...".replace(" ", "2"),
        "..122222222221..",
        "..2224O22O42 2..".replace(" ", "2"),
        "..222222222222..",
        "..2222OOOO2222..",
        "..2222OwwO2222..",
        "...22222222 2...".replace(" ", "2"),
        "...3222222223...",
        "..33.322223.33..",
        ".33..32..23..33.",
        "33..33....33..33",
        "3..3........3..3",
        "...xxxxxxxxxx...",
        E, E, E, E, E,
    ],
    "bat": [
        E, E, E, E, E, E, E,
        "......2..2......",
        "......2222......",
        "2....2O22O2....2",
        "22..22222222..22",
        "222222w22w222222",
        "2322222222222232",
        "3.32322222232 3.".replace(" ", "3"),
        "...3..3223..3...",
        "........3.......",
        E, E, E,
        "......xxxx......",
        E, E, E, E,
    ],
    # Seed-spitting vine: a bulb with a spout mouth on a stalk.
    "seed_vine": [
        E, E, E, E, E,
        ".....2222.......",
        "....221122......",
        "...2211112O55...",
        "...221111225 5..".replace(" ", "4"),
        "...2221122 2....".replace(" ", "2"),
        "....222222......",
        "......33........",
        "......33..1.....",
        ".....33..121....",
        "..1..3...33.....",
        ".121.3..33......",
        "..33.33.3.......",
        "....3.333.......",
        "...33333333.....",
        "..xxxxxxxxxxx...",
        E, E, E, E,
    ],
    # Young ivory: a pale sapling-creature with a single bright eye (detail).
    "young_ivory": [
        E, E, E, E, E, E,
        "......1111......",
        ".....111111.....",
        "....11222211....",
        "....12O44O21....",
        "....12244221....",
        ".....122221.....",
        "......2222......",
        "......2332......",
        "...1..2332..1...",
        "..12..2332..21..",
        "...2222332222...",
        "......2332......",
        ".....223322.....",
        "....33.33.33....",
        "...xxxxxxxxxx...",
        E, E, E,
    ],
    # Plant creature (jilted lover): a flower head on leafy arms.
    "plant": [
        E, E, E,
        ".....4..4.......",
        "....454454......",
        "...45544554.....",
        "...54O55O45.....",
        "....455554......",
        ".....4444.......",
        "......22........",
        "..11..22..11....",
        ".1221.22.1221...",
        "..1222222221....",
        "......22........",
        "......22........",
        ".....2222.......",
        "....3....3......",
        "...3......3.....",
        "..xxxxxxxxxx....",
        E, E, E, E, E,
    ],
    "croc": [
        E, E, E, E, E, E, E, E, E,
        "..2O2...........",
        ".22222222.......",
        "2222222222211...",
        "wOwOwOw12222221.",
        "2222222222222221",
        ".333333222222222",
        "......2222222223",
        ".....22.22..22.3",
        ".....33.33..33..",
        "....xxxxxxxxxxxx",
        E, E, E, E, E,
    ],
    "salthopper": [
        E, E, E, E, E, E, E, E,
        "......4..4......",
        ".......44.......",
        ".....222222.....",
        "....2O1111O2....",
        "....21111112....",
        "...2.222222.2...",
        "..2.22222222.2..",
        ".2..23333332..2.",
        ".3...333333...3.",
        "3...3.3..3.3...3",
        "...3..3..3..3...",
        "..xxxxxxxxxxxx..",
        E, E, E, E,
    ],
    # Girshling: a sandy solifuge, big jaws.
    "girshling": [
        E, E, E, E, E, E, E,
        "....5......5....",
        "...55O2222O55...",
        "....5222222 5...".replace(" ", "5"),
        ".....211112.....",
        "..2.21111112.2..",
        ".2.2222222222.2.",
        "2.2.22222222.2.2",
        "2.2.23333332.2.2",
        "...2.333333.2...",
        "..2...3333...2..",
        ".2............2.",
        "..xxxxxxxxxxxx..",
        E, E, E, E,
        E,
    ],
    "spider": [
        E, E, E, E, E, E, E, E,
        "2.2..........2.2",
        ".2.2...22...2.2.",
        "..2.2.2112.2.2..",
        "...22211112222..",
        "....2rOrrOr2....",
        "...22211112222..",
        "..2.2.2332.2.2..",
        ".2.2..2332..2.2.",
        "2..2...33...2..2",
        "...3........3...",
        "..xxxxxxxxxxxx..",
        E, E, E, E, E,
    ],
    "beetle": [
        E, E, E, E, E, E, E,
        ".....3....3.....",
        "......3..3......",
        ".....222222.....",
        "....2O2222O2....",
        "...3222222223...",
        "..3.11155111.3..",
        "...1112552111...",
        "..3122255222 13.".replace(" ", "2"),
        "...2222552222...",
        "..3222255222 23.".replace(" ", "2"),
        "...3322552233...",
        "....33333333....",
        "...3...33...3...",
        "..xxxxxxxxxxxx..",
        E, E, E,
    ],
    "centipede": [
        E, E, E, E, E, E,
        ".....3....3.....",
        "......2222......",
        ".....2O22O2.....",
        "....3221122 3...".replace(" ", "2"),
        "......2552......",
        "....3.2222.3....",
        "......2552......",
        "....3.2222.3....",
        "......2552......",
        "....3.2222.3....",
        "......2552......",
        "....3.2222.3....",
        "......2552......",
        ".......33.......",
        ".....xxxxxx.....",
        E, E, E,
    ],
    # Jel / goo: a wobbly blob with a shine and two eyes.
    "jel": [
        E, E, E, E, E, E, E, E, E, E,
        "......2222......",
        "....22111122....",
        "...2211w11122...",
        "..221111111122..",
        "..2211O11O1122..",
        "..222111111222..",
        ".22222222222222.",
        ".23222222222232.",
        "..333333333333..",
        "..xxxxxxxxxxxx..",
        E, E, E, E,
    ],
    "leech": [
        E, E, E, E, E, E, E, E, E, E, E, E,
        "...........22...",
        ".........221122.",
        ".......2221O112.",
        "....2222222222r.",
        "..2221122222....",
        ".22332222333....",
        "..33.....33.....",
        "..xxxxxxxxxx....",
        E, E, E, E,
    ],
    "scorpiock": [
        E, E, E,
        ".........44.....",
        "..........54....",
        "...........2....",
        "...........2....",
        "..........22....",
        ".55......22.....",
        "5..5...222...55.",
        "5..52222222.5..5",
        ".552O1111O2 5..5".replace(" ", "2"),
        "...221111122.55.",
        "..2.2222222.2...",
        ".2.2.22222.2.2..",
        "2.2..23332..2.2.",
        "....2.333.2.....",
        "...2.......2....",
        "..xxxxxxxxxxxx..",
        E, E, E, E, E,
    ],
    "baboon": [
        E, E, E, E,
        "....22222222....",
        "...2222222222...",
        "..222rrrrrr222..",
        "..22rrrrrrrr22..",
        "..2rrOrrrrOrr2..",
        "..2rrrrrrrrrr2..",
        "...rrrOOOOrrr...",
        "...2rrwwwwrr2...",
        "....22rrrr22....",
        "...2222222222...",
        "..22211111122 2.".replace(" ", "2"),
        "..2.21111112..2.",
        "..2.22222222..2.",
        "..s.22222222...2",
        ".....33..33....2",
        "....333..333....",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E, E,
    ],
    "bear": [
        E, E, E,
        "...22......22...",
        "..2112....2112..",
        "..2222222222 2..".replace(" ", "2"),
        ".22222222222222.",
        ".222O222222O222.",
        ".222w222222w222.",
        ".22222111122222.",
        "..222211OO122 2.".replace(" ", "2"),
        "...2221111222...",
        "...22221122222..",
        "..222222222222..",
        ".2w2222222222w2.",
        ".22.21111112.22.",
        "....22222222....",
        "...2222222222...",
        "...333....333...",
        "..3333....3333..",
        "..xxxxxxxxxxxx..",
        "...xxxxxxxxxx...",
        E, E,
    ],
    "boar": [
        E, E, E, E, E, E,
        "...2........2...",
        "...22222222 2...".replace(" ", "2"),
        "..222222222222..",
        "..22O222222O22..",
        "..222111111222..",
        ".w22111OO11122w.",
        ".w.2111111112.w.",
        "...2222222222...",
        "..225555555522..",
        "..222222222222..",
        "..2222222222 2..".replace(" ", "2"),
        "...33.3333.33...",
        "...33.3333.33...",
        "..xxxxxxxxxxxx..",
        "...xxxxxxxxxx...",
        E, E, E,
    ],
    "crab": [
        E, E, E, E, E, E, E, E, E,
        ".44..........44.",
        "4554........4554",
        ".44.2......2.44.",
        "....22222222....",
        "...2111111112...",
        "..221111111122..",
        "..222222222222..",
        ".2.2333333332.2.",
        "2.2..2....2..2.2",
        "..2..........2..",
        "..xxxxxxxxxxxx..",
        E, E, E, E,
    ],
    "sparktick": [
        E, E, E, E, E, E, E, E, E,
        "......4..4......",
        ".......44.......",
        ".....222222.....",
        "....24O22O42....",
        "...2221111222...",
        "..2.22144122.2..",
        ".2..22222222..2.",
        "....23333332....",
        "...3.3....3.3...",
        "..3..........3..",
        "...xxxxxxxxxx...",
        E, E, E, E,
    ],
}

# ---------------- batch 5: common across the whole world (factions) ----------------

CANNIBAL_EXTRA = {12: "....srsOOsrs....", 14: "....2w2w2w22....",  # snarl, bone necklace
                  10: "...ssrOssrOss..."}
BONE_CLUB = {10: ".............ww.", 11: "............wwww", 12: ".............ww.", 13: ".............n..",
             14: ".............n..", 15: "............sn..", 16: ".............n.."}
BASKET_BACK = {13: ".55..........55.", 14: "5445........5445", 15: "5555........5555"}
TEMPLAR_HELM = {3: ".....lllll......", 4: "....lllllll.....", 5: "...lwllllllll...", 6: "...llllllllll...",
                7: "...lllllllllL...", 8: "...lLLLLLLLLL...", 9: "...lL......Ll...", 10: "...lLOOOOOOLl...",
                11: "...llllllllll...", 12: "....llllllll....", 13: ".....LLLLLL....."}
TABARD = {14: "....55545555....", 15: "...s54444445s...", 16: "...s55545555s...", 17: "....55545555....",
          18: "....LLLLLLLL...."}
BEAR_HEAD = {3: "...22......22...", 4: "..2112222221122.", 5: "..222222222222..", 6: "..222222222222..",
             7: "..222222222222..", 8: "..22O222222O22..", 9: "..22w222222w22..", 10: "...2221111222...",
             11: "...2211OO1122...", 12: "....21111112....", 13: ".....222222....."}

CREATURES.update({
    "cannibal": human(HAIR_WILD_GREY, CANNIBAL_EXTRA, BONE_CLUB),
    "naphtaali": human(HOOD, BASKET_BACK),
    "templar": human(TEMPLAR_HELM, TABARD, SWORD),
    "templar_gunner": human(TEMPLAR_HELM, TABARD, GUN),
    "templar_squire": human(HAIR_SHORT, TABARD, SPEAR),
    "barathrumite": human(BEAR_HEAD, ROBE, WRENCH),
    "mushroom": [
        E, E, E, E, E, E,
        "......1111......",
        "....11411411....",
        "...1111111141...",
        "..141111411111..",
        "..222222222222..",
        "....33333333....",
        ".....wwwwww.....",
        ".....wOwwOw.....",
        ".....wwwwww.....",
        ".....wwOOww.....",
        "......wwww......",
        ".....wwwwww.....",
        "....xxxxxxxx....",
        E, E, E, E, E,
    ],
    "prickler": [
        E, E, E, E, E, E, E, E,
        "....4..4..4.....",
        ".4..2..2..2..4..",
        "..42222222224...",
        "...2111111112...",
        ".422O1111O12 24.".replace(" ", "2"),
        "...2111111112...",
        "..42222222224...",
        ".4..32.2.23..4..",
        "....3..3..3.....",
        "...xxxxxxxxxx...",
        E, E, E, E, E, E,
    ],
    "urchin": [
        E, E, E, E, E, E, E, E,
        ".....4.4.4......",
        "...4.2.2.2.4....",
        "....2222222.....",
        ".4.221111122.4..",
        "..2211O1O1122...",
        ".4222111112224..",
        "..222222222 2...".replace(" ", "2"),
        ".4.233333332.4..",
        "...3.3.3.3.3....",
        "..xxxxxxxxxxx...",
        E, E, E, E, E, E,
    ],
    "fish_school": [
        E, E, E, E, E, E,
        "..222.5.........",
        ".2O1225.........",
        "..222.5...222.5.",
        "..........2O1225",
        "....222.5..222.5",
        "...2O1225.......",
        "....222.5.......",
        ".........222.5..",
        "........2O1225..",
        ".........222.5..",
        E, E, E, E, E, E, E, E,
    ],
    "palm": [
        E, E,
        "...1..1..1......",
        "..121.121.121...",
        ".12.212221.212..",
        "1.2..12221..2.1.",
        "....1.222.1.....",
        "......2O2O......",
        "......2222......",
        "......3223......",
        ".......nN.......",
        ".......nN.......",
        "......nN........",
        "......nN........",
        ".......nN.......",
        ".......nN.......",
        "......nnNn......",
        ".....nnNNnn.....",
        "....xxxxxxxx....",
        E, E, E, E, E,
    ],
    "aloe": [
        E, E, E, E, E, E, E, E,
        "......1...1.....",
        "..1...21.12..1..",
        "..21..221221.12.",
        "...21.2222212 2.".replace(" ", "1"),
        "...2212O22O2 2..".replace(" ", "1"),
        "....22222222....",
        "....43222234....",
        "....33333333....",
        ".....333333.....",
        "...xxxxxxxxxx...",
        E, E, E, E, E, E,
    ],
    "yonderbrush": [
        E, E, E, E, E, E, E, E, E,
        "....1..1.1......",
        "..1121211121....",
        ".122222222221...",
        ".12242222422 1..".replace(" ", "2"),
        "1222222222222 1.".replace(" ", "2"),
        ".233222222333...",
        "..3333333333....",
        "...3.3..3.3.....",
        "..xxxxxxxxxxx...",
        E, E, E, E, E, E,
    ],
    "waydroid": [
        E, E, E, E, E, E,
        "......4.........",
        "......5.........",
        "....llllllll....",
        "...lwlllllllL...",
        "...l44llll44L...",
        "...l45llll45L...",
        "...lllllllllL...",
        "....LLLLLLLL....",
        ".....llllll.....",
        "...LLlll2llLL...",
        "...L.ll222l.L...",
        ".....LLLLLL.....",
        "....OO....OO....",
        "....OO....OO....",
        "...xxxxxxxxxx...",
        E, E, E,
    ],
    "albino_ape": [
        E, E, E,
        "....wwwwwwww....",
        "...wwwwwwwwww...",
        "..wwwsssssswww..",
        "..wwsssssssssw..",
        "..wwsrOssrOssw..",
        "..wwssssssssww..",
        "...wssOOOOssw...",
        "...wwswwwwsww...",
        "..wwwwwwwwwwwww.",
        ".wwwwwwwwwwwwwww",
        ".ww.wwwwwwww.ww.",
        ".ss.wwwwwwww.ss.",
        "....wwwwwwww....",
        "....ww....ww....",
        "...sss....sss...",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E, E, E, E,
    ],
    "asphodelyte": [
        E, E,
        "......4.4.......",
        ".....454454.....",
        "....45555554....",
        "....5O5445O5....",
        ".....455554.....",
        "......4444......",
        ".......22.......",
        "...11..22.......",
        "..1221.22..11...",
        "...12222..1221..",
        ".......2222 1...".replace(" ", "2"),
        ".......22.......",
        ".......22.......",
        ".......22.......",
        "......2222......",
        ".....3....3.....",
        "....xxxxxxxx....",
        E, E, E, E, E,
    ],
    "cragmensch": [
        E, E, E,
        "...2.2....2.2...",
        "..2222222222 2..".replace(" ", "2"),
        ".22222222222222.",
        ".222rO2222rO222.",
        ".22222222222222.",
        ".222wOwOwOwO222.",
        "..222222222222..",
        ".22222222222222.",
        "2222211111122222",
        "22.2211111122.22",
        "ss.2222222222.ss",
        "...2222222222...",
        "...333....333...",
        "..3333....3333..",
        "..xxxxxxxxxxxx..",
        "...xxxxxxxxxx...",
        E, E, E, E, E,
    ],
    "voider": [
        E, E, E, E, E, E, E, E, E,
        "......2222......",
        ".....2OOOO2.....",
        "....2OO44OO2....",
        "....2OO44OO2....",
        ".....2OOOO2.....",
        "......2222......",
        ".....22..22.....",
        "....22....22....",
        "...33......33...",
        "...xxxxxxxxxx...",
        E, E, E, E, E,
    ],
    "ant": [
        E, E, E, E, E, E, E, E, E,
        ".....3....3.....",
        "......3..3......",
        "......2222......",
        ".....2O22O2.....",
        "......2112......",
        "...3...22...3...",
        "....3.2222.3....",
        "......2222......",
        "....3.2332.3....",
        "...3..2222..3...",
        "......3333......",
        "...xxxxxxxxxx...",
        E, E, E,
    ],
    "knollworm": [
        E, E, E, E, E, E, E,
        ".....222222.....",
        "....21111112....",
        "...2111OO1112...",
        "...21OwwwwO12...",
        "...2111OO1112...",
        "....22222222....",
        "....25555552....",
        "....22222222....",
        "....25555552....",
        "...3222222223...",
        "..333333333333..",
        ".n33333333333 3n".replace(" ", "3"),
        "..nnnnnnnnnnnn..",
        E, E, E, E,
    ],
    "flybot": [
        E, E, E, E, E, E,
        "..ll........ll..",
        ".l44l......l44l.",
        "..ll..llll..ll..",
        "....lllllllll...",
        "...lL44ll44lL...",
        "...lLlllllllL...",
        "....LLLLLLLL....",
        "......L..L......",
        E, E, E,
        ".....xxxxxx.....",
        E, E, E, E, E, E,
    ],
    "tombbot": [
        E, E, E,
        ".....llllll.....",
        "....lwllllllL...",
        "....l44ll44lL...",
        "....l45ll45lL...",
        "....llllllllL...",
        ".....LLLLLL.....",
        "...LLllllllLL...",
        "..LllL2222LllL..",
        "..Ll.L2112L.lL..",
        "..Ll.L2222L.lL..",
        "..LL.LLLLLL.LL..",
        ".....ll..ll.....",
        ".....LL..LL.....",
        "....LLL..LLL....",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E, E, E, E,
        E,
    ],
})


# ---------------- mutation overlays (anchored to the HUMAN layout) ----------------
# The game doesn't change sprites for mutations; BrightQud.cs composites these at runtime onto
# humanoid-kit tiles of creatures that have the mutation (part name = key). "back" layers are drawn
# behind the body, "front" over it. Digits use the creature's own colors.

MUTATIONS = {
    "Horns": ("front", {1: "..w..........w..", 2: "..tw........wt..", 3: "...tw......wt...",
                        4: "....t......t...."}),
    "MultipleArms": ("front", {16: "s..............s", 17: "ss............ss", 18: ".s............s."}),
    "Wings": ("back", {8: ".4............4.", 9: "454..........454", 10: "4554........4554",
                       11: "45554......45554", 12: "455554....455554", 13: "45555......55554",
                       14: "4565........5654", 15: "466..........664", 16: "46............64",
                       17: ".6............6."}),
    "Carapace": ("back", {11: "..3333333333 3..".replace(" ", "3"), 12: ".32222222222223.",
                          13: "3221222222221223", 14: "3222222222222223", 15: "3212222222222123",
                          16: "3222222222222223", 17: "3222222222222223", 18: ".32222222222223.",
                          19: "..333333333333.."}),
    "Quills": ("back", {2: "....w..w..w.....", 3: "..w.t..t..t.w...", 4: ".wt.........tw..",
                        6: "wt............tw", 9: "wt............tw", 12: ".wt..........tw.",
                        15: "..t..........t.."}),
    "Stinger": ("back", {9: ".4w.............", 10: ".55.............", 11: "..55............",
                         12: "...5............", 13: "...5............", 14: "..55............",
                         15: ".55.............", 16: "55..............", 17: "5...............",
                         18: "55..............", 19: ".55............."}),
    "TwoHeaded": ("front", {8: "ss..............", 9: "sss.............", 10: "OsO.............",
                            11: "sss.............", 12: ".s.............."}),
    "Beak": ("front", {11: "......yyyy......", 12: ".......yy......."}),
    "BurrowingClaws": ("front", {15: "..w..........w..", 16: ".w.w........w.w.", 17: "..w..........w.."}),
    "ThickFur": ("front", {6: "..n..........n..", 7: ".nn..........nn.", 8: "..n..........n..",
                           9: ".nn..........nn.", 10: "..n..........n..", 11: ".nn..........nn.",
                           13: "...nn......nn...", 14: "..nnn......nnn.."}),
    "MultipleLegs": ("front", {18: "..5..........5..", 19: "..55........55..", 20: ".NN..........NN.",
                               21: ".NN..........NN."}),
}

# Skin-tint mutations: replace the skin colors (s, S) with these palette letters.
SKIN_TINTS = {"PhotosyntheticSkin": ("g", "h"), "Albino": ("w", "l")}


# ---------------- idle animation: hand-drawn second frames ----------------
# Shipped as "brightqudframe/<key>"; the runtime alternates frame 0/1 on a shared beat.
# Creatures without a second frame get an automatic 1px bob instead.

def move_pixels(grid, chars, dy):
    """Second frame by moving the pixels of `chars` (e.g. the wing colors) dy rows (negative = up)."""
    out = [list(r.translate({ord(c): "." for c in chars})) for r in grid]
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in chars and 0 <= y + dy < 24:
                out[y + dy][x] = ch
    return ["".join(r) for r in out]


def frames(sprites):
    """{key-name: second frame}. `sprites` = tiles.SPRITES (for the player's gunwing)."""
    return {
        "gunwing": move_pixels(sprites["gunwing"], "456", -2),          # wings up
        "bat": move_pixels(CREATURES["bat"], "23", -2)[:7] + CREATURES["bat"][7:9]
               + move_pixels(CREATURES["bat"], "23", -2)[9:],           # wings up, head stays
        "dragonfly": move_pixels(CREATURES["dragonfly"], "45", 2),      # wings down
        "flybot": move_pixels(CREATURES["flybot"], "l4", -1),           # rotors bob
    }


# ---------------- player looks (Options → Mods → "Bright Qud: player look") ----------------
# Name -> sprite. All on the HUMAN layout, so mutation overlays line up. Colors come from the
# player's own game colors at runtime.

def player_looks(sprites):
    return {
        "Gunslinger": sprites["gunwing"],
        "Adventurer": sprites["adventurer"],
        "Mystic": human(HOOD, ROBE, STAFF),
        "Tinker": human(HAIR_SHORT, GOGGLES, APRON, WRENCH),
        "Scavenger": human(HAIR_WILD_GREY, ARMOR, CLUB),
        "Warden": human(HELMET, ARMOR, SPEAR),
        "Pilgrim": human(TURBAN, ROBE, BOOK),
        "Hunter": human(HAIR_LONG, BOW),
    }


# ---------------- calling / caste / pregen sprites (Phase 4, option A) ----------------
# The player's sprite in the base game comes from the chosen calling/caste or preset. Each gets a
# caricature on the HUMAN layout (so mutations line up); body color = the game's foreground.

SUN_HALO = {1: ".....4.44.4.....", 2: "....4.5555.4....", 3: "...4.555555.4...", 4: "..4.5........5.4"}
MOON_CROWN = {2: "......l..l......", 3: ".....lwllwl.....", 4: "....l......l...."}
CROWN = {2: "....y.y..y.y....", 3: "....yyyyyyyy....", 4: "....y5yy5yyy...."}
CAPE = {14: ".6..........6...", 15: "66............66", 16: "66............66", 17: "66............66",
        18: ".6............6."}
PACK = {12: "..NN............", 13: ".NnnN...........", 14: ".NnnN...........", 15: ".NNNN..........."}
WIDE_HAT = {2: "......NNNN......", 3: ".....NnnnnN.....", 4: "...NNNNNNNNNN...", 5: "..NNNNNNNNNNNN.."}
SHIELD = {14: "5555............", 15: "5445............", 16: "5445............", 17: ".55............."}
VEIL = {11: "...4444444444...", 12: "....44444444....", 13: ".....444444....."}
FISHSCALES = {6: "...c.c.c.c.c....", 12: "..c..........c..", 13: ".c............c."}
FLAME_HAIR = {1: "....r..y..r.....", 2: "...ryr.r.ryr....", 3: "...rrryrryrr....", 4: "....rrrrrrrr....",
              5: "...r........r..."}
STAR_EYE = {7: "...ssssssssss...", 8: "....s..44..s....", 9: "...ss.4wO4.ss...", 10: "...sss.44.sss...",
            11: "...ssssssssss..."}
LEAF_HAIR = {2: "...g..G..g......", 3: "..gGg.gGg.gG....", 4: ".gGGGgGGGgGGg...", 5: "..gggggggggg...."}
TURTLE_SHELL = {13: "..4444444444....", 14: ".455555555554...", 15: "45565555565554..", 16: "45555555555554..",
                17: "45565555565554..", 18: ".455555555554...", 19: "..4444444444...."}
ROBOT_HEAD = {4: ".....llllll.....", 5: "....lwlllllL....", 6: "...llllllllll...", 7: "...lLLLLLLLLl...",
              8: "...lL44LL44Ll...", 9: "...lL45LL45Ll...", 10: "...lLLLLLLLLl...", 11: "...llllllllll...",
              12: "....lLOOOOLl....", 13: ".....LLLLLL....."}
TAUR_LEGS = {17: "....33nnnn3333..", 18: "....5555555555..", 19: "...55.55..55.55.", 20: "...xNNxxNNxxNNx."}

CASTES = {
    "creatures/caste/1": human(HAIR_SHORT, LEAF_HAIR, APRON, HOE),           # Horticulturist
    "creatures/caste/2": human(BALD, SUN_HALO, ROBE, STAFF),                  # Priest of All Suns
    "creatures/caste/3": human(HAIR_LONG, MOON_CROWN, ROBE, BOOK),            # Priest of All Moons
    "creatures/caste/4": human(HELMET, ARMOR, CAPE, SWORD),                   # Syzygyrior
    "creatures/caste/5": human(HAIR_SHORT, GOGGLES, APRON, GEAR),             # Artifex
    "creatures/caste/6": human(HAIR_SHORT, CROWN, ROBE, BOOK),                # Consul
    "creatures/caste/7": human(HELMET, ARMOR, SHIELD, SPEAR),                 # Praetorian
    "creatures/caste/8": human(BALD, VEIL, ROBE),                             # Eunuch
    "creatures/caste/9": human(HAIR_LONG, FLAME_HAIR, ROBE),                  # Child of the Hearth
    "creatures/caste/10": human(HAIR_SHORT, GOGGLES, ARMOR, WRENCH),          # Child of the Wheel
    "creatures/caste/11": human(HOOD, FISHSCALES, SPEAR),                     # Child of the Deep
    "creatures/caste/12": human(FLAME_HAIR, CAPE),                            # Fuming God-Child
    "creatures/caste/13": human(HOOD, ROBE, STAFF),                           # Apostle
    "creatures/caste/14": human(HAIR_SHORT, GOGGLES, PACK, AXE),              # Arconaut
    "creatures/caste/15": human(BALD, BEARD, ROBE, BOOK),                     # Greybeard
    "creatures/caste/16": human(WIDE_HAT, GUN),                               # Gunslinger
    "creatures/caste/17": human(HAIR_WILD_GREY, ARMOR, AXE),                  # Marauder
    "creatures/caste-pilgrim": human(TURBAN, ROBE, STAFF),                    # Pilgrim
    "creatures/caste/19": human(WIDE_HAT, PACK, SPEAR),                       # Nomad
    "creatures/caste/20": human(HAIR_SHORT, GOGGLES, ROBE, BOOK),             # Scholar
    "creatures/caste/21": human(HAIR_WILD_GREY, GOGGLES, APRON, WRENCH),      # Tinker
    "creatures/caste/22": human(HELMET, ARMOR, BOW),                          # Warden
    "creatures/caste/23": human(TURBAN, PACK, BOOK),                          # Water Merchant
    "creatures/caste/24": human(WIDE_HAT, APRON, HOE),                        # Watervine Farmer
    "creatures/sw/praetorian/prime": human(CROWN, ARMOR, SHIELD, SPEAR),
    "creatures/sw/first/horticulturalist": human(LEAF_HAIR, ROBE, HOE),
    "creatures/sw/first/child/of/the/hearth": human(FLAME_HAIR, ROBE, STAFF),
    "creatures/sw/marsh/taur": human(HAIR_LONG, TAUR_LEGS, SPEAR),
    "creatures/sw/dream/tortoise": human(BALD, TURTLE_SHELL, STAFF),
    "creatures/sw/stareye/esper": human(HOOD, STAR_EYE, ROBE),
    "creatures/sw/firefrond": human(LEAF_HAIR, FLAME_HAIR, ROBE),
    "creatures/sw/bzzzt": human(ROBOT_HEAD, ARMOR, GUN),
}
