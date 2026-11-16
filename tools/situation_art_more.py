"""Second batch of situation-game illustrations (15 more situations).

Imported by tools/situation_art.py; uses the same drawing helpers so the style matches.
"""
from situation_art import P, C, E, R, G, W, OL, kid, frame, tiles, dust

# ------------------------------------------------------------------ objects (200x200)
def o_book():
    s = P("M100,60 Q70,46 26,52 L26,150 Q70,144 100,158 Z", "#ffffff") + P("M100,60 Q130,46 174,52 L174,150 Q130,144 100,158 Z", "#ffffff")
    s += P("M20,56 L20,156 Q66,150 100,164 Q134,150 180,156 L180,56", sw=W) + P("M100,60 L100,158", sw=2)
    s += "".join(P(f"M{x1},{y} Q{(x1 + x2) / 2},{y - 6} {x2},{y}", sw=2, stroke="#b8c4dd") for y in (78, 96, 114, 132) for x1, x2 in ((38, 88), (112, 162)))
    s += P("M14,60 L14,162 Q66,156 100,170 Q134,156 186,162 L186,60", "none", sw=6, stroke="#7fa6e6")
    return s

def o_pencil():
    body = R(-14, -70, 28, 120, "#ffd66b", rx=3) + P("M-14,50 L14,50 L0,86 Z", "#f6deb7") + P("M-5,74 L5,74 L0,86 Z", OL, sw=1)
    body += R(-14, -90, 28, 22, "#ff9fb4", rx=5) + R(-16, -72, 32, 10, "#c9cdd8", rx=2) + P("M-4,-60 L-4,48", sw=1.5, stroke="#e6b94a")
    return G(body, 100, 100, rot=40)

def o_eraser():
    return (P("M40,96 L132,60 L164,84 L72,122 Z", "#ffffff") + P("M40,96 L72,122 L72,150 L40,124 Z", "#f3f3f3")
            + P("M72,122 L164,84 L164,112 L72,150 Z", "#f3f3f3")
            + P("M88,78 L132,60 L164,84 L120,102 Z", "#8fc0f0") + P("M120,102 L164,84 L164,112 L120,130 Z", "#7fb0e6"))

def o_mat():
    s = P("M20,150 L60,60 L180,60 L156,150 Z", "#9fc3f0")
    for i in range(1, 4):
        t = i / 4
        s += P(f"M{20 + 40 * t},{150 - 90 * t} L{156 + 24 * t},{150 - 90 * t}", sw=5, stroke="#ffffff", extra='opacity="0.8"')
        s += P(f"M{20 + 136 * t},150 L{60 + 120 * t},60", sw=5, stroke="#ffffff", extra='opacity="0.8"')
    s += P("M20,150 L60,60 L180,60 L156,150 Z")
    return s

def o_lunchbox():
    s = R(26, 64, 148, 96, "#ffe3a3", rx=14) + R(36, 74, 128, 76, "#ffffff", rx=8) + P("M100,74 L100,150", sw=2.5)
    s += "".join(C(x, y, 9, "#ffffff", sw=2) for x, y in ((52, 96), (70, 92), (60, 112), (78, 112), (54, 130), (74, 132)))
    s += E(130, 98, 18, 12, "#fff6c8") + C(130, 98, 7, "#ffcd4d", sw=0)
    s += C(120, 130, 9, "#8fcf7d") + C(134, 126, 9, "#8fcf7d") + C(146, 132, 8, "#8fcf7d") + R(148, 112, 10, 10, "#ff8fa3", rx=3, sw=1.5)
    return s

def o_water_bottle():
    s = R(70, 54, 60, 116, "#9fd8f0", rx=16) + R(70, 104, 60, 40, "#c9ecfa", rx=0, sw=0)
    s += R(78, 30, 44, 28, "#6fb6e6", rx=8) + P("M122,40 Q156,40 150,100", sw=4) + P("M70,104 L130,104", sw=2)
    return s

def o_soap():
    s = R(40, 92, 120, 62, "#ffd0e0", rx=26) + R(52, 98, 96, 40, "#ffe4ee", rx=18, sw=0)
    s += C(66, 72, 12, "#eaf6ff", sw=2) + C(92, 58, 16, "#eaf6ff", sw=2) + C(124, 70, 10, "#eaf6ff", sw=2) + C(146, 54, 7, "#eaf6ff", sw=2)
    return s

def o_shampoo():
    s = R(60, 70, 80, 110, "#b9a6f2", rx=20) + R(76, 102, 48, 46, "#ffffff", rx=8, sw=2)
    s += R(88, 52, 24, 22, "#ffffff") + R(94, 30, 12, 24, "#ffffff", rx=2) + P("M94,30 L66,30 L66,40", sw=6) + P("M94,30 L66,30 L66,40", sw=2.5, stroke="#ffffff")
    s += P("M88,116 Q100,108 112,116 Q100,130 88,116 Z", "#9fd8f0", sw=2)
    return s

def o_towel():
    s = R(30, 40, 140, 10, "#c9cdd8", rx=5)
    s += P("M46,46 L154,46 L154,150 Q100,160 46,150 Z", "#9fe0c4") + R(46, 124, 108, 14, "#ffffff", rx=0, sw=2)
    s += P("M100,46 L100,150", sw=1.5, stroke="#7cc9a8")
    return s

def o_umbrella():
    s = P("M20,110 Q100,10 180,110 Q160,96 140,110 Q120,96 100,110 Q80,96 60,110 Q40,96 20,110 Z", "#ff8c8c")
    s += P("M100,30 L100,110", sw=2) + P("M60,110 Q74,62 100,30 Q126,62 140,110", sw=2)
    s += P("M100,110 L100,168 Q100,184 86,184 Q74,184 74,170", sw=7) + P("M100,110 L100,168 Q100,184 86,184 Q74,184 74,170", sw=3, stroke="#d9d9e3")
    return s

def boot(x, col):
    return G(P("M-22,-60 L14,-60 L14,20 L46,28 Q54,30 54,44 L54,50 L-22,50 Z", col) + R(-26, -68, 44, 14, col, rx=5) + P("M-22,50 L54,50", sw=6), x, 112)

def o_rain_boots():
    return boot(54, "#ffd25e") + boot(112, "#ffd25e")

def o_raincoat():
    s = P("M64,48 Q100,18 136,48 L170,150 Q100,166 30,150 Z", "#ffd25e")
    s += P("M76,56 Q100,32 124,56 Q118,80 100,82 Q82,80 76,56 Z", "#ffe8a3") + P("M100,82 L100,156", sw=2.5)
    s += P("M64,72 L34,130 L52,138 L74,96", "#ffd25e") + P("M136,72 L166,130 L148,138 L126,96", "#ffd25e")
    s += "".join(C(108, y, 3.5, "#ffffff", sw=1.5) for y in (100, 120, 140))
    return s

def o_pot():
    s = R(40, 84, 120, 76, "#c9d3e6", rx=16) + R(32, 76, 136, 16, "#dfe6f2", rx=8) + R(86, 62, 28, 16, "#4b4a5c", rx=6)
    s += R(16, 98, 26, 12, "#4b4a5c", rx=6) + R(158, 98, 26, 12, "#4b4a5c", rx=6)
    return s

def o_frying_pan():
    return E(84, 110, 64, 40, "#4b4a5c", sw=W) + E(84, 106, 54, 31, "#6b6a80", sw=0) + P("M140,100 L188,72", sw=16) + P("M140,100 L188,72", sw=10, stroke="#d79a63")

def o_spatula():
    head = R(-28, -86, 56, 66, "#e46f6f", rx=10) + "".join(R(x, -76, 8, 40, "#ffffff", rx=3, sw=2) for x in (-18, -4, 10))
    return G(head + R(-6, -22, 12, 108, "#d79a63", rx=5), 100, 96, rot=-20)

def o_crayons():
    s = ""
    for i, col in enumerate(("#ff7f7f", "#ffcd4d", "#7fd39f", "#7fb3ea", "#b9a6f2")):
        x = 52 + i * 22
        s += R(x, 54, 18, 90, col, rx=3, sw=2) + P(f"M{x},{54} L{x + 9},{34} L{x + 18},{54} Z", col, sw=2)
    s += R(40, 100, 122, 66, "#ffe08a", rx=6) + R(56, 116, 90, 24, "#ffffff", rx=12, sw=2)
    return s

def o_sketchbook():
    s = R(36, 44, 128, 130, "#ffffff", rx=6) + R(36, 30, 128, 18, "#7fa6e6", rx=4)
    s += "".join(C(x, 39, 4, "#ffffff", sw=2) for x in range(52, 160, 16))
    s += C(130, 82, 14, "#ffe08a", sw=0) + P("M48,150 Q80,110 112,150", "#bfe3b4", sw=0) + P("M90,150 Q120,120 152,150", "#a7d79a", sw=0)
    return s

def o_paint():
    s = P("M40,120 C20,70 70,36 120,46 C170,56 182,110 150,130 C130,142 120,120 104,130 C86,142 104,170 76,170 C56,170 48,146 40,120 Z", "#fff1d8")
    s += C(74, 84, 11, "#ff7f7f", sw=2) + C(108, 70, 11, "#ffcd4d", sw=2) + C(142, 86, 11, "#7fb3ea", sw=2) + C(70, 120, 11, "#7fd39f", sw=2)
    s += G(R(-5, -60, 10, 90, "#d79a63", rx=4) + R(-6, 26, 12, 12, "#c9cdd8", rx=2, sw=2) + P("M-7,38 Q0,64 7,38 Z", "#7fb3ea", sw=2), 150, 120, rot=-35)
    return s

def o_winter_hat():
    s = P("M44,140 Q44,56 100,56 Q156,56 156,140 Z", "#ff8c8c") + R(36, 130, 128, 30, "#ffffff", rx=12)
    s += C(100, 46, 18, "#ffffff") + "".join(P(f"M{x},68 L{x},128", sw=2, stroke="#e46f6f") for x in (76, 100, 124))
    return s

def mitten_shape():
    return (P("M-26,40 L-26,-20 Q-26,-56 4,-56 Q30,-56 30,-20 L30,40 Z", "#7fb3ea")
            + P("M-26,6 Q-52,0 -48,-26 Q-42,-40 -26,-28 Z", "#7fb3ea") + R(-30, 34, 64, 20, "#ffffff", rx=6))

def o_mittens():
    return (f'<g transform="translate(66 104) rotate(-8)">{mitten_shape()}</g>'
            + f'<g transform="translate(134 104) rotate(8) scale(-1 1)">{mitten_shape()}</g>')

def o_scarf():
    s = P("M40,58 Q100,90 160,58 L160,86 Q100,118 40,86 Z", "#ffd25e")          # loop around the neck
    s += P("M120,96 L150,96 L160,172 L130,176 Z", "#ffd25e") + P("M92,98 L120,96 L118,168 L90,170 Z", "#ffd25e")   # two hanging ends
    s += "".join(P(f"M{a},{y} L{b},{y + 1}", sw=5, stroke="#ff8c8c") for a, b, y in ((122, 154, 130), (92, 119, 130)))
    s += "".join(P(f"M{x},{170} L{x},{186}", sw=3) for x in (96, 106, 116, 134, 144, 154))
    s += "".join(P(f"M{x},{64 + 0.0},L{x},0", sw=0) for x in ())
    return s

def o_padded_jacket():
    s = P("M64,40 L30,64 L14,150 L40,156 L54,96 L54,170 L146,170 L146,96 L160,156 L186,150 L170,64 L136,40 Z", "#8fb8ef")
    s += "".join(P(f"M54,{y} Q100,{y + 8} 146,{y}", sw=2.5) for y in (78, 106, 134))
    s += P("M22,110 L48,116 M178,110 L152,116", sw=2.5)
    s += P("M100,44 L100,170", sw=2.5) + P("M76,40 Q100,62 124,40", "#ffffff")
    return s

def o_swim_ring():
    s = C(100, 100, 74, "#ffffff") + C(100, 100, 30, "#e9f6ff")
    for a in range(0, 360, 90):
        s += f'<path d="M100,26 A74,74 0 0 1 152.3,47.7 L121.2,78.8 A30,30 0 0 0 100,70 Z" fill="#ff8c8c" stroke="{OL}" stroke-width="2" transform="rotate({a} 100 100)"/>'
    s += C(100, 100, 74, "none") + C(100, 100, 30, "none")
    return s

def o_sand_bucket():
    s = P("M44,74 L132,74 L122,170 L54,170 Z", "#ff9fb4") + E(88, 74, 44, 10, "#ffd0dc")
    s += P("M46,80 Q88,20 130,80", sw=4)
    s += G(R(-6, -60, 12, 80, "#7fd39f", rx=5) + P("M-20,18 L20,18 L14,60 Q0,72 -14,60 Z", "#7fd39f"), 160, 104, rot=18)
    return s

def o_swimsuit():
    s = P("M70,36 L84,36 Q100,64 116,36 L130,36 L134,94 Q150,140 134,170 L112,170 Q100,148 88,170 L66,170 Q50,140 66,94 Z", "#7fd3e6")
    s += "".join(C(x, y, 5, "#ffffff", sw=0) for x, y in ((84, 110), (114, 104), (100, 132), (80, 150), (120, 150)))
    return s

def o_cart():
    s = P("M20,46 L44,46 L64,128 L160,128", sw=6) + P("M48,60 L176,60 L162,112 L60,112 Z", "#ffe08a")
    s += "".join(P(f"M{x},62 L{x - 3},110", sw=2) for x in (80, 104, 128, 152)) + P("M54,86 L170,86", sw=2)
    s += C(76, 152, 13, "#7fb3ea") + C(150, 152, 13, "#7fb3ea")
    return s

def o_shopping_bag():
    s = P("M32,82 L168,82 L154,170 L46,170 Z", "#9fe0c4") + P("M66,82 Q66,30 100,30 Q134,30 134,82", sw=7)
    s += "".join(P(f"M{x},90 L{x - 2},164", sw=2, stroke="#6fbf9c") for x in (70, 100, 130))
    return s

def o_wallet():
    s = R(30, 60, 140, 92, "#e2a274", rx=14) + R(110, 86, 64, 40, "#d18c5e", rx=10) + C(146, 106, 8, "#ffe08a")
    s += C(54, 156, 14, "#ffd25e") + C(84, 162, 14, "#ffd25e")
    return s

def o_backpack():
    s = R(48, 46, 104, 128, "#ff9f7f", rx=30) + R(66, 112, 68, 50, "#ffc3ad", rx=12) + P("M74,46 Q100,14 126,46", sw=7)
    s += P("M66,126 L134,126", sw=2.5)
    return s

def o_sneakers():
    s = P("M24,140 L24,96 Q24,78 44,78 L78,78 Q96,100 130,104 L166,112 Q184,118 182,140 Z", "#ffffff")
    s += P("M20,140 L186,140 L182,156 L24,156 Z", "#7fb3ea") + P("M78,78 L64,112 M92,92 L80,118 M106,100 L96,122", sw=3, stroke="#ff8c8c")
    return s

def o_comb():
    s = R(30, 72, 140, 30, "#b9a6f2", rx=8)
    s += "".join(R(x, 98, 7, 50, "#b9a6f2", rx=3, sw=2) for x in range(36, 162, 12))
    return s

def o_mirror():
    return (E(100, 74, 54, 60, "#ffd6e4") + E(100, 74, 42, 48, "#e8f4ff") + P("M80,50 L92,40 M76,64 L102,40", sw=4, stroke="#ffffff")
            + R(90, 130, 20, 54, "#ffd6e4", rx=8))

def o_hair_dryer():
    s = R(30, 50, 104, 64, "#9fd8f0", rx=32) + E(132, 82, 22, 32, "#7fc4e6") + E(138, 82, 10, 18, "#4b4a5c", sw=0)
    s += P("M54,108 L76,108 L90,178 L66,178 Z", "#9fd8f0") + R(68, 132, 14, 10, "#ffffff", rx=3, sw=2)
    s += "".join(P(f"M{168},{y} Q178,{y - 6} 190,{y}", sw=3, stroke="#b9c3d6") for y in (68, 82, 96))
    return s

def o_scissors():
    s = P("M100,104 L176,40", sw=10) + P("M100,104 L176,40", sw=6, stroke="#dfe6f2")
    s += P("M100,104 L182,72", sw=10) + P("M100,104 L182,72", sw=6, stroke="#dfe6f2")
    s += C(70, 120, 24, "none", sw=14) + C(70, 120, 24, "none", sw=8, stroke="#ff8c8c")
    s += C(104, 150, 24, "none", sw=14) + C(104, 150, 24, "none", sw=8, stroke="#ff8c8c") + C(100, 104, 4, OL, sw=0)
    return s

def o_watering_can():
    s = P("M46,80 L130,80 L124,166 L52,166 Z", "#7fd39f") + P("M128,104 L178,62", sw=12) + P("M128,104 L178,62", sw=7, stroke="#7fd39f")
    s += R(166, 50, 22, 18, "#5fbf86", rx=4, extra='transform="rotate(-40 177 59)"') + P("M60,80 Q88,30 116,80", sw=6)
    return s

def o_trowel():
    return G(P("M-26,-80 Q0,-100 26,-80 L18,-10 Q0,6 -18,-10 Z", "#c9d3e6") + R(-5, -6, 10, 26, "#9aa3b5", sw=2)
             + R(-12, 18, 24, 66, "#7fd39f", rx=10), 100, 100, rot=30)

def o_flower_pot():
    s = P("M46,70 L154,70 L136,170 L64,170 Z", "#e2a274") + R(38, 56, 124, 24, "#d18c5e", rx=6)
    s += E(100, 66, 56, 8, "#8a6248", sw=0)
    return s

def o_washing_machine():
    s = R(40, 30, 120, 146, "#ffffff", rx=12) + P("M40,62 L160,62", sw=2.5) + C(62, 46, 6, "#ff8c8c", sw=2) + R(116, 40, 32, 12, "#c9d3e6", rx=4, sw=2)
    s += C(100, 118, 42, "#dfe6f2") + C(100, 118, 30, "#9fd8f0") + P("M78,112 Q100,98 122,112", sw=2.5, stroke="#ffffff")
    return s

def o_detergent():
    s = R(48, 62, 104, 112, "#9fc3f0", rx=16) + R(60, 38, 40, 28, "#ffffff", rx=6) + P("M112,66 L112,92 Q112,100 120,100 L140,100", sw=8)
    s += R(68, 104, 64, 46, "#ffffff", rx=10, sw=2) + C(88, 124, 8, "#c9ecfa", sw=1.5) + C(110, 120, 11, "#c9ecfa", sw=1.5)
    return s

def o_drying_rack():
    s = P("M44,176 L74,60 M156,176 L126,60 M74,60 L126,60", sw=6)                 # A-frame legs and top bar
    s += P("M30,96 L170,96", sw=5) + P("M22,126 L178,126", sw=5)                 # hanging bars
    s += P("M46,96 L46,120 Q46,124 50,124 L76,124 Q80,124 80,120 L80,96", "#ffb3c7", sw=2.5)   # towel
    s += P("M92,96 L86,118 L96,118 L100,106 L104,118 L114,118 L108,96 Z", "#ffe08a", sw=2.5)   # shirt-ish
    s += P("M124,126 L120,160 L134,160 L138,140 L142,160 L156,160 L152,126 Z", "#9fd8f0", sw=2.5)   # shorts
    s += P("M40,126 L40,150 Q52,158 64,150 L64,126", "#c7b8f0", sw=2.5)        # sock
    return s

def o_tent():
    s = P("M20,160 L100,40 L180,160 Z", "#ffb36b") + P("M100,40 L76,160 L124,160 Z", "#ff8c4d") + P("M100,40 L100,160", sw=2)
    s += P("M100,40 L100,24", sw=4) + P("M10,162 L190,162", sw=4)
    return s

def o_flashlight():
    return G(R(-18, -10, 36, 110, "#7fb3ea", rx=8) + P("M-28,-48 L28,-48 L18,-10 L-18,-10 Z", "#5f97d6") + E(0, -48, 28, 8, "#fff3b0")
             + R(-8, 24, 16, 22, "#ffffff", rx=4, sw=2)
             + P("M-20,-60 L-34,-86 M0,-62 L0,-92 M20,-60 L34,-86", sw=4, stroke="#ffcd4d"), 100, 104, rot=-30)

def o_sleeping_bag():
    s = R(30, 60, 140, 100, "#9fd38a", rx=40) + R(30, 60, 50, 100, "#7fc06a", rx=40) + P("M80,64 L80,156", sw=2.5)
    s += P("M100,60 L100,160", sw=2, stroke="#7fc06a") + P("M130,60 L130,160", sw=2, stroke="#7fc06a")
    return s

def o_baby_bottle():
    s = R(70, 70, 60, 104, "#ffffff", rx=16) + "".join(P(f"M70,{y} L86,{y}", sw=2) for y in (96, 120, 144))
    s += R(64, 56, 72, 20, "#9fd8f0", rx=6) + P("M84,56 Q84,22 100,20 Q116,22 116,56 Z", "#ffe0b8")
    s += R(76, 120, 48, 50, "#fff6e6", rx=0, sw=0) + R(70, 70, 60, 104, "none", rx=16)
    return s

def o_diaper():
    s = P("M30,64 L170,64 Q164,110 128,132 Q118,160 100,162 Q82,160 72,132 Q36,110 30,64 Z", "#ffffff")
    s += R(26, 58, 30, 22, "#9fd8f0", rx=6) + R(144, 58, 30, 22, "#9fd8f0", rx=6)
    s += "".join(C(x, y, 5, "#ffd6e4", sw=0) for x, y in ((80, 90), (120, 90), (100, 116)))
    return s

def o_pacifier():
    s = P("M100,128 L100,160", sw=0) + E(100, 104, 62, 30, "#ffb3c7") + C(100, 104, 14, "#ff8fa3")
    s += C(100, 160, 22, "none", sw=8) + C(100, 160, 22, "none", sw=4, stroke="#ffb3c7")
    s += P("M90,72 Q100,30 110,72 Z", "#ffe0b8")
    return s

OBJECTS = {
    "book": o_book, "pencil": o_pencil, "eraser": o_eraser,
    "mat": o_mat, "lunchbox": o_lunchbox, "water_bottle": o_water_bottle,
    "soap": o_soap, "shampoo": o_shampoo, "towel": o_towel,
    "umbrella": o_umbrella, "rain_boots": o_rain_boots, "raincoat": o_raincoat,
    "pot": o_pot, "frying_pan": o_frying_pan, "spatula": o_spatula,
    "crayons": o_crayons, "sketchbook": o_sketchbook, "paint": o_paint,
    "winter_hat": o_winter_hat, "mittens": o_mittens, "scarf": o_scarf, "padded_jacket": o_padded_jacket,
    "swim_ring": o_swim_ring, "sand_bucket": o_sand_bucket, "swimsuit": o_swimsuit,
    "cart": o_cart, "shopping_bag": o_shopping_bag, "wallet": o_wallet,
    "backpack": o_backpack, "sneakers": o_sneakers,
    "comb": o_comb, "mirror": o_mirror, "hair_dryer": o_hair_dryer, "scissors": o_scissors,
    "watering_can": o_watering_can, "trowel": o_trowel, "flower_pot": o_flower_pot,
    "washing_machine": o_washing_machine, "detergent": o_detergent, "drying_rack": o_drying_rack,
    "tent": o_tent, "flashlight": o_flashlight, "sleeping_bag": o_sleeping_bag,
    "baby_bottle": o_baby_bottle, "diaper": o_diaper, "pacifier": o_pacifier,
}

# ------------------------------------------------------------------ scenes (400x440) — never draw the answer objects
KIDS2 = [("minu", "sora"), ("hana", "jun")]

def floor(col, y=330):
    return R(0, y, 400, 440 - y, col, rx=0) + P(f"M0,{y} L400,{y}", sw=W)

def window(x, y, w, h, sky, extra=""):
    return R(x, y, w, h, sky, rx=10) + extra + P(f"M{x + w / 2},{y} L{x + w / 2},{y + h} M{x},{y + h / 2} L{x + w},{y + h / 2}", sw=3) + R(x, y, w, h, "none", rx=10)

def sun(x, y, r=26):
    return C(x, y, r, "#ffe08a", sw=2) + "".join(f'<path d="M{x},{y - r - 8} L{x},{y - r - 20}" stroke="#ffcd4d" stroke-width="4" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 45))

def tree(x, y, s=1):
    return G(R(-10, 0, 20, 70, "#c98f56", rx=4) + C(0, -20, 44, "#a7d79a") + C(-30, 6, 28, "#a7d79a") + C(30, 6, 28, "#a7d79a"), x, y, s)

def sc_study(v):
    k, wall = [("minu", "#f2f6ff"), ("sora", "#fff6ea")][v]
    s = frame(wall) + window(250, 40, 110, 90, "#d6ecff") + R(40, 60, 70, 50, "#ffffff", rx=4) + P("M50,98 L68,76 L84,92 L100,72", sw=2.5, stroke="#9fd38a")
    s += kid(k, 200, 190, 1.1, eye="open", mth="smile", arms=(("to", -56, 98, (-74, 70)), ("to", 56, 98, (74, 70))))
    s += R(30, 290, 340, 24, "#e7b989", rx=6) + R(50, 312, 22, 110, "#d7a36f", rx=5) + R(328, 312, 22, 110, "#d7a36f", rx=5)
    s += R(300, 230, 10, 62, "#c9cdd8", rx=4) + P("M280,232 L330,232 L318,206 L292,206 Z", "#ffe08a")   # desk lamp
    return s

def family(names, xs, y, s=0.85, adult=None):
    out = ""
    if adult:
        out += kid("mom", adult, y - 40, 1.05, eye="happy", mth="smile", arms=(("down",), ("down",)))
    for n, x in zip(names, xs):
        out += kid(n, x, y, s, eye="happy", mth="grin", arms=(("to", -50, 30, (-70, 70)), ("down",)))
    return out

def sc_picnic(v):
    k = KIDS2[v]
    s = frame("#e6f6ff") + sun(70, 70) + tree(330, 200, 1.0) + tree(60, 230, 0.8)
    s += R(0, 300, 400, 140, "#bfe3a6", rx=0) + P("M0,300 L400,300", sw=W)
    s += "".join(P(f"M{x},{y} l4,-10 l4,10", sw=2, stroke="#7fb36a") for x, y in ((40, 360), (120, 400), (300, 380), (360, 420), (220, 350)))
    s += family(k, (150, 250), 250, 0.85, adult=None)
    return s

def sc_bath(v):
    k, wall, tile = [("jun", "#e9f6ff", "#d3e9f7"), ("hana", "#f3f0ff", "#e2dcf5")][v]
    s = frame(wall) + tiles(tile, 0, 330)
    s += kid(k, 120, 200, 1.0, eye="happy", mth="smile", shirt="#ffffff", arms=(("down",), ("to", 74, 40, (80, 90))))
    s += P("M180,250 L390,250 L380,350 Q376,370 356,370 L214,370 Q194,370 190,350 Z", "#ffffff") + R(176, 240, 218, 16, "#ffffff", rx=8)
    s += P("M190,262 Q290,276 384,262", "#a9dcf5", sw=2.5)
    s += G(E(0, 0, 18, 12, "#ffd25e") + C(-12, -14, 10, "#ffd25e") + P("M-24,-14 L-30,-12 L-24,-10 Z", "#ff9f5e", sw=2) + C(-14, -16, 2, OL, sw=0), 300, 262)   # duck
    s += R(360, 170, 14, 72, "#c9d3e6", rx=6) + P("M367,170 L367,150 L340,150", sw=8)
    s += floor("#dbe7f2", 370)
    return s

def rain(x0, y0, w, h):
    return "".join(P(f"M{x},{y} l-6,14", sw=3, stroke="#7fb3ea") for x in range(x0 + 10, x0 + w, 22) for y in range(y0 + 10, y0 + h - 10, 30))

def sc_rain(v):
    k, wall = [("sora", "#f4f1ea"), ("minu", "#eef3f7")][v]
    sky = R(220, 40, 150, 170, "#b9c6d6", rx=10) + rain(220, 70, 150, 140) + E(260, 70, 30, 16, "#ffffff", sw=0) + E(320, 64, 36, 18, "#ffffff", sw=0)
    s = frame(wall) + sky + P("M295,40 L295,210 M220,125 L370,125", sw=3) + R(220, 40, 150, 170, "none", rx=10)
    s += R(30, 60, 120, 270, "#d7a36f", rx=6) + C(132, 200, 6, "#ffe08a")   # front door
    s += kid(k, 200, 210, 1.0, eye="open", mth="hmm", arms=(("to", -60, 40, (-76, 90)), ("down",)))
    s += floor("#d9c7ae", 330) + E(300, 390, 50, 12, "#b9d8f0", sw=2)
    return s

def sc_cooking(v):
    wall = ["#fff4e6", "#eef7f1"][v]
    s = frame(wall) + R(250, 40, 120, 90, "#ffffff", rx=10) + "".join(R(262 + i * 36, 54, 26, 14, c, rx=4, sw=2) for i, c in enumerate(("#ffe08a", "#ffb3c7", "#9fe0c4")))
    s += kid("mom", 140, 160, 1.15, eye="happy", mth="smile", shirt=["#c9b6ef", "#9fcbf2"][v], arms=(("to", -40, 110, (-80, 80)), ("to", 40, 110, (80, 80))),
             extra=P("M-34,60 L34,60 L40,150 L-40,150 Z", "#ffffff", sw=2.5))   # apron
    s += R(0, 300, 400, 140, "#e7c9a7", rx=0) + P("M0,300 L400,300", sw=W)   # counter
    s += R(210, 270, 170, 34, "#dfe6f2", rx=6) + C(250, 286, 14, "#4b4a5c") + C(340, 286, 14, "#4b4a5c") + C(250, 286, 7, "#9aa3b5", sw=0) + C(340, 286, 7, "#9aa3b5", sw=0)   # empty stove
    s += E(60, 296, 16, 20, "#fff6e6") + E(90, 298, 15, 19, "#fff6e6") + P("M120,300 L150,268 L156,300 Z", "#ff9f5e", sw=2) + C(176, 290, 14, "#ff6f6f")   # eggs, carrot, tomato
    return s

def sc_drawing(v):
    k, wall = [("hana", "#fff7ef"), ("jun", "#f2f6ff")][v]
    s = frame(wall)
    s += R(250, 50, 110, 84, "#ffffff", rx=4) + C(280, 84, 12, "#ffe08a", sw=0) + P("M262,124 Q300,92 346,124", "#bfe3b4", sw=0) + R(250, 50, 110, 84, "none", rx=4)  # child's drawing on wall
    s += kid(k, 170, 190, 1.1, eye="happy", mth="grin", arms=(("to", -40, -20, (-80, 40)), ("to", 56, 98, (74, 70))))
    s += P("M118,138 Q100,120 112,104", sw=0)
    s += R(30, 290, 340, 24, "#e7b989", rx=6) + R(50, 312, 22, 110, "#d7a36f", rx=5) + R(328, 312, 22, 110, "#d7a36f", rx=5)
    s += P("M226,120 Q232,104 248,108", sw=3, stroke="#ffcd4d") + C(250, 100, 6, "#ffcd4d", sw=0)   # idea sparkle
    return s

def snow(x0, y0, w, h):
    return "".join(C(x, y, 4, "#ffffff", sw=1) for x in range(x0 + 12, x0 + w, 26) for y in range(y0 + 14, y0 + h - 8, 28))

def sc_cold(v):
    k, wall = [("minu", "#eef3fb"), ("sora", "#f6f0f7")][v]
    sky = R(220, 40, 150, 170, "#9fb6d6", rx=10) + snow(220, 40, 150, 170) + C(300, 186, 18, "#ffffff", sw=2) + C(300, 160, 12, "#ffffff", sw=2)
    s = frame(wall) + sky + P("M295,40 L295,210 M220,125 L370,125", sw=3) + R(220, 40, 150, 170, "none", rx=10)
    s += R(30, 60, 120, 270, "#d7a36f", rx=6) + C(132, 200, 6, "#ffe08a")
    s += kid(k, 200, 210, 1.0, eye="closed", mth="flat", arms=(("to", 30, 100, (-60, 90)), ("to", -30, 100, (60, 90))))
    s += P("M168,180 l-12,-6 M232,180 l12,-6 M164,200 l-14,0 M236,200 l14,0", sw=3, stroke="#7fb3ea")   # shiver lines
    s += floor("#d9c7ae", 330)
    return s

def sc_beach(v):
    k = KIDS2[v]
    s = frame("#dff3ff") + sun(330, 64)
    s += P("M0,200 Q50,190 100,200 Q150,210 200,200 Q250,190 300,200 Q350,210 400,200 L400,290 L0,290 Z", "#8fd0f0")
    s += P("M0,230 Q50,222 100,230 Q150,238 200,230 Q250,222 300,230 Q350,238 400,230", sw=3, stroke="#ffffff")
    s += P("M0,280 Q200,262 400,280 L400,440 L0,440 Z", "#ffe6b0")
    s += family(k, (150, 260), 260, 0.85)
    s += P("M60,380 l10,-6 l6,10 l-12,4 Z", "#ffb3c7", sw=2) + P("M330,400 q8,-14 16,0 q-8,10 -16,0 Z", "#fff6e6", sw=2)   # shells
    return s

def sc_shopping(v):
    k = ["jun", "hana"][v]
    s = frame("#fff8ee")
    for row, y in enumerate((60, 140)):
        s += R(20, y + 50, 360, 12, "#d7a36f", rx=3)
        for i in range(8):
            x = 40 + i * 44
            col = ["#ff8c8c", "#ffcd4d", "#9fd38a", "#ffb36b"][(i + row) % 4]
            s += C(x, y + 36, 14, col, sw=2)
    s += kid("mom", 260, 250, 1.0, eye="happy", mth="smile", arms=(("down",), ("down",)))
    s += kid(k, 140, 290, 0.85, eye="happy", mth="grin", arms=(("to", -50, -30, (-70, 30)), ("down",)))
    s += floor("#eee3d3", 380)
    return s

def sc_daycare(v):
    k, wall = [("sora", "#fff6e6"), ("jun", "#eef7ff")][v]
    s = frame(wall) + window(240, 40, 130, 100, "#cfeaff", sun(306, 90, 16)) + R(40, 60, 110, 270, "#9fcbf2", rx=6) + C(132, 200, 6, "#ffe08a")
    s += kid(k, 220, 210, 1.0, eye="happy", mth="grin", arms=(("to", -60, -30, (-80, 40)), ("down",)))
    s += floor("#e9d8c4", 330) + "".join(R(x, 300, 10, 30, "#ffffff", rx=4, sw=2) for x in (196, 236))   # socks on feet
    return s

def sc_haircut(v):
    k = ["minu", "sora"][v]
    s = frame("#f3f0ff" if v == 0 else "#fff3ee")
    s += R(250, 60, 120, 120, "#ffffff", rx=8) + "".join(C(280 + (i % 2) * 60, 92 + (i // 2) * 56, 18, "#ffd6e4" if i % 2 else "#d6e6ff", sw=2) for i in range(4))   # hairstyle poster
    s += R(110, 300, 180, 30, "#9aa3b5", rx=10) + R(186, 330, 28, 70, "#c9cdd8", rx=4) + R(130, 396, 140, 14, "#c9cdd8", rx=6)
    hairy = dict(minu="#5b3a2c", sora="#2f2a2e")[k]
    # long, messy hair grown down to the shoulders (drawn behind the head)
    s += P("M126,250 Q112,200 130,150 Q138,110 170,100 Q200,86 232,100 Q262,110 270,150 Q288,200 274,250 Q262,236 256,252 Q246,232 236,246 L164,246 Q154,232 144,252 Q138,236 126,250 Z", hairy)
    s += kid(k, 200, 190, 1.05, eye="open", mth="flat", arms=(("down",), ("down",)))
    s += P("M150,176 Q150,128 176,116 Q200,104 226,116 Q252,128 250,176 Q240,150 226,160 Q214,140 200,158 Q186,140 174,160 Q160,150 150,176 Z", hairy)   # fringe over the forehead
    s += P("M140,250 L260,250 L290,320 L110,320 Z", "#ffffff", sw=2.5)   # hair-cut cape
    return s

def sc_planting(v):
    k = ["hana", "minu"][v]
    s = frame("#e6f6ff") + sun(60, 60) + R(0, 280, 400, 160, "#bfe3a6", rx=0) + P("M0,280 L400,280", sw=W)
    s += R(200, 320, 180, 70, "#a8744f", rx=20) + "".join(P(f"M{x},{y} l6,-4", sw=2, stroke="#7a5236") for x, y in ((230, 350), (280, 340), (330, 360), (260, 372)))
    s += kid(k, 120, 230, 0.95, eye="happy", mth="grin", arms=(("to", 44, 70, (60, 110)), ("down",)))
    s += G(R(-14, -20, 28, 36, "#ffffff", rx=3) + C(0, -4, 8, "#ffcd4d", sw=0) + P("M0,4 L0,12", sw=2, stroke="#7fb36a"), 170, 290)   # seed packet
    return s

def clothes_pile(x, y):
    return (G(P("M-60,30 Q-70,-10 -30,-20 Q0,-40 30,-20 Q70,-10 60,30 Z", "#ffb3c7") + P("M-50,0 L-10,-20 L10,10 Z", "#9fd8f0", sw=2)
              + P("M10,-10 L50,-6 L40,22 L4,20 Z", "#ffe08a", sw=2) + C(-20, 10, 6, "#a58a6a", sw=0) + C(30, 4, 5, "#a58a6a", sw=0), x, y))

def sc_laundry(v):
    k, wall = [("jun", "#f3f7ff"), ("sora", "#fff7ef")][v]
    s = frame(wall) + window(250, 40, 110, 90, "#d6ecff")
    s += kid(k, 140, 200, 1.0, eye="closed", mth="hmm", arms=(("to", -6, 26, (-60, 70)), ("down",)))
    s += floor("#e9d8c4", 330) + clothes_pile(280, 330)
    s += P("M250,282 q-6,-12 2,-20 M280,276 q-6,-12 2,-20 M310,282 q-6,-12 2,-20", sw=3, stroke="#b5a17f")   # smell lines
    return s

def sc_camping(v):
    k = KIDS2[v]
    sky = ["#3e4a7a", "#4a3e6e"][v]
    s = frame(sky) + C(330, 70, 22, "#fff3b0", sw=2) + "".join(P(f"M{x},{y - 5} L{x},{y + 5} M{x - 5},{y} L{x + 5},{y}", sw=2.5, stroke="#fff3b0") for x, y in ((60, 50), (140, 90), (240, 40), (380, 130)))
    s += P("M0,240 L80,150 L160,240 Z", "#5d7a6a") + P("M120,240 L220,130 L320,240 Z", "#6f8f7c") + P("M260,240 L340,170 L420,240 Z", "#5d7a6a")
    s += R(0, 240, 400, 200, "#7da36a", rx=0) + P("M0,240 L400,240", sw=W)
    s += family(k, (140, 260), 300, 0.85)
    return s

def sc_baby(v):
    wall, adult_shirt = [("#fff4f7", "#c9b6ef"), ("#f2f8ff", "#9fe0c4")][v]
    s = frame(wall) + window(260, 40, 110, 90, "#d6ecff")
    s += kid("mom", 110, 190, 1.0, eye="open", mth="o", shirt=adult_shirt, arms=(("down",), ("to", 70, 90, (80, 50))))
    s += floor("#e9d8c4", 360)
    # crib with a crying baby
    s += R(170, 250, 210, 80, "#fdf6e9", rx=10)
    s += G(C(0, 0, 30, "#ffe1cc") + C(-30, 4, 7, "#ffe1cc") + C(30, 4, 7, "#ffe1cc") + P("M-10,-28 Q0,-38 6,-28", sw=2.5)
           + P("M-17,-2 Q-11,4 -5,-2") + P("M5,-2 Q11,4 17,-2") + E(0, 14, 8, 7, "#d9535f")
           + P("M-18,4 Q-22,16 -16,22 Q-12,16 -18,4 Z", "#9fd8f0", sw=1.5) + P("M18,4 Q22,16 16,22 Q12,16 18,4 Z", "#9fd8f0", sw=1.5), 230, 262)
    s += P("M250,276 Q300,262 360,276 L360,320 L250,320 Z", "#ffd6e4")     # baby blanket
    s += R(160, 200, 230, 14, "#d8a877", rx=6) + "".join(R(x, 210, 10, 120, "#d8a877", rx=4, sw=2) for x in range(170, 384, 34))
    s += R(160, 326, 230, 14, "#d8a877", rx=6) + R(160, 200, 14, 160, "#d8a877", rx=5) + R(376, 200, 14, 160, "#d8a877", rx=5)
    s += P("M200,170 l-10,-12 M230,164 l0,-16 M260,170 l10,-12", sw=3, stroke="#ff8c8c")   # crying lines
    return s

SCENES = {
    "study": sc_study, "picnic": sc_picnic, "bath": sc_bath, "rain": sc_rain, "cooking": sc_cooking,
    "drawing": sc_drawing, "cold": sc_cold, "beach": sc_beach, "shopping": sc_shopping, "daycare": sc_daycare,
    "haircut": sc_haircut, "planting": sc_planting, "laundry": sc_laundry, "camping": sc_camping, "baby": sc_baby,
}

def register(objects, scenes, usage):
    objects.update(OBJECTS)
    scenes.update(SCENES)
