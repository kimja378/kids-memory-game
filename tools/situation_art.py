#!/usr/bin/env python3
"""Generate the illustrations for situation-game/ as plain SVG files.

All pictures (situation scenes, object cards, "how it is used" scenes) are drawn here
from shared parts so the style stays consistent: soft pastel fills, round dark outlines,
simple 2D shapes. Nothing is downloaded; the output is committed to the repository.

Usage: python3 tools/situation_art.py      (writes situation-game/assets/**.svg)

Add a new picture by writing a function that returns SVG body markup and registering
it in OBJECTS / SCENES / USAGE at the bottom.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "situation-game", "assets")
OL = "#4b4a5c"          # outline colour
W = 3                   # outline width

def svg(w, h, body, extra_style=""):
    style = f"<style>{extra_style}</style>" if extra_style else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'stroke-linejoin="round" stroke-linecap="round">{style}{body}</svg>\n')

def P(d, fill="none", sw=W, stroke=OL, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def C(x, y, r, fill, sw=W, stroke=OL, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def E(x, y, rx, ry, fill, sw=W, stroke=OL, extra=""):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def R(x, y, w, h, fill, rx=8, sw=W, stroke=OL, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def G(body, x=0, y=0, s=1, rot=0, extra=""):
    t = f"translate({x} {y})"
    if rot: t += f" rotate({rot})"
    if s != 1: t += f" scale({s})"
    return f'<g transform="{t}" {extra}>{body}</g>'

# ------------------------------------------------------------------ characters
KIDS = {
    "minu": dict(skin="#ffdcc4", hair="#5b3a2c", shirt="#9fcbf2", style="boy"),
    "sora": dict(skin="#f7cfae", hair="#2f2a2e", shirt="#f7b9cb", style="girl"),
    "hana": dict(skin="#ffe1cc", hair="#7a4a2a", shirt="#bfe3b4", style="bob"),
    "jun":  dict(skin="#efc39f", hair="#262326", shirt="#ffd98a", style="boy"),
    "mom":  dict(skin="#ffdcc4", hair="#3d2b28", shirt="#c9b6ef", style="bun"),
}

def hair(style, color, front=True):
    if not front:
        if style == "girl":
            return C(-50, 14, 15, color) + C(50, 14, 15, color)
        if style == "bun":
            return C(0, -54, 17, color)
        if style == "bob":
            return P("M-50,-4 C-56,30 -50,46 -38,48 L38,48 C50,46 56,30 50,-4 Z", color)
        return ""
    if style in ("boy",):
        return P("M-46,6 C-52,-42 -18,-60 2,-57 C28,-58 54,-38 46,6 C40,-12 30,-22 16,-20 C8,-30 -10,-28 -20,-20 C-32,-24 -42,-12 -46,6 Z", color)
    # girl / bob / bun: rounder fringe
    return P("M-47,8 C-54,-44 -16,-60 2,-58 C30,-58 56,-40 47,8 C44,-6 36,-18 22,-24 C10,-14 -12,-14 -24,-24 C-38,-18 -44,-6 -47,8 Z", color)

def eyes(kind):
    if kind == "open":
        return (E(-16, 2, 4.5, 6, OL, sw=0) + E(16, 2, 4.5, 6, OL, sw=0)
                + C(-14.5, 0, 1.6, "#fff", sw=0) + C(17.5, 0, 1.6, "#fff", sw=0))
    if kind == "happy":
        return P("M-23,5 Q-16,-4 -9,5") + P("M9,5 Q16,-4 23,5")
    if kind == "closed":
        return P("M-23,2 Q-16,9 -9,2") + P("M9,2 Q16,9 23,2")
    if kind == "sleepy":
        return P("M-23,4 L-9,4") + P("M9,4 L23,4") + P("M-23,0 Q-16,-4 -9,0", sw=2) + P("M9,0 Q16,-4 23,0", sw=2)
    if kind == "look":   # looking down/side
        return (E(-14, 6, 4.5, 5.5, OL, sw=0) + E(18, 6, 4.5, 5.5, OL, sw=0))
    return ""

def mouth(kind):
    if kind == "smile":
        return P("M-10,20 Q0,30 10,20")
    if kind == "grin":
        return P("M-12,18 Q0,34 12,18 Z", "#e66a72")
    if kind == "aah":   # wide open, teeth visible (ready to brush)
        return (P("M-14,16 Q0,44 14,16 Z", "#d9535f")
                + P("M-12,17 L12,17 L11,22 L-11,22 Z", "#ffffff", sw=1.5))
    if kind == "yawn":
        return E(0, 24, 9, 13, "#c74b57") + E(0, 30, 5, 4, "#f08a93", sw=0)
    if kind == "o":
        return E(0, 23, 6, 7, "#d9535f")
    if kind == "hmm":
        return P("M-9,24 Q0,18 9,24")
    if kind == "flat":
        return P("M-8,22 L8,22")
    return ""

def head(pal, eye="open", mth="smile", blush=True):
    s = hair(pal["style"], pal["hair"], front=False)
    s += C(-44, 8, 9, pal["skin"]) + C(44, 8, 9, pal["skin"])
    s += C(0, 0, 44, pal["skin"])
    s += hair(pal["style"], pal["hair"])
    s += eyes(eye) + mouth(mth)
    if blush:
        s += E(-27, 15, 7, 4.5, "#ffb3b8", sw=0, extra='opacity="0.8"') + E(27, 15, 7, 4.5, "#ffb3b8", sw=0, extra='opacity="0.8"')
    return s

def arm(x1, y1, x2, y2, pal, cx=None, cy=None):
    if cx is None:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 + 10
    d = f"M{x1},{y1} Q{cx},{cy} {x2},{y2}"
    return (P(d, sw=22) + P(d, sw=16, stroke=pal["shirt"]) + C(x2, y2, 10, pal["skin"]))

def body(pal, collar=True, w=48):
    s = P(f"M-{w},150 C-{w},80 -40,46 0,46 C40,46 {w},80 {w},150 Z", pal["shirt"])
    if collar:
        s += P("M-14,48 Q0,62 14,48", sw=2.5)
    return s

def kid(name, x, y, s=1, eye="open", mth="smile", arms=(("down",), ("down",)), back_arms=False, shirt=None, extra=""):
    """A child bust: head at (0,0), shoulders at y~56. arms = (left, right) as ('down',) or ('to', hx, hy)."""
    pal = dict(KIDS[name])
    if shirt:
        pal["shirt"] = shirt
    out = ""
    def one(spec, side):
        sx = -36 * side
        if spec[0] == "down":
            return arm(sx, 64, sx - 14 * side, 132, pal, sx - 18 * side, 98)
        _, hx, hy = spec[:3]
        c = spec[3] if len(spec) > 3 else None
        return arm(sx, 64, hx, hy, pal, *(c or (None, None)))
    a = one(arms[0], 1) + one(arms[1], -1)
    out += body(pal)
    if back_arms:
        out = a + out
    else:
        out += a
    out += head(pal, eye, mth) + extra
    return G(out, x, y, s)

# ------------------------------------------------------------------ objects (200x200 cards)
def o_toothbrush():
    return G(R(-9, -10, 18, 150, "#7fb3ea", rx=9) + R(-14, -62, 28, 56, "#ffffff", rx=6)
             + "".join(P(f"M{x},-60 L{x},-10", sw=2, stroke="#9fc4ec") for x in (-7, 0, 7))
             + R(-12, -12, 24, 10, "#7fb3ea", rx=4), 100, 62, rot=35)

def toothpaste_tube():
    tube = P("M-30,-60 L30,-60 L36,70 L-36,70 Z", "#e9f4ff") + R(-36, 66, 72, 14, "#9fc4ec", rx=3)
    tube += R(-12, -86, 24, 28, "#7fb3ea", rx=5)
    tube += R(-22, -30, 44, 50, "#9fc4ec", rx=10, sw=0)
    tooth = P("M-10,-18 C-16,-18 -16,-6 -12,4 C-10,12 -6,12 -4,4 C-2,0 2,0 4,4 C6,12 10,12 12,4 C16,-6 16,-18 10,-18 C6,-18 4,-15 0,-15 C-4,-15 -6,-18 -10,-18 Z", "#ffffff", sw=2)
    return tube + tooth

def o_toothpaste():
    return G(toothpaste_tube(), 100, 104, rot=-12)

def o_cup():
    return G(P("M-40,-50 L40,-50 L32,52 Q30,62 20,62 L-20,62 Q-30,62 -32,52 Z", "#ffe08a")
             + P("M38,-26 C70,-26 70,30 34,30", sw=10) + P("M38,-26 C70,-26 70,30 34,30", sw=5, stroke="#ffe08a")
             + E(0, -50, 40, 9, "#fff3c4"), 92, 104)

def o_spoon():
    return G(E(0, -50, 26, 36, "#e3e7ef") + E(-6, -56, 9, 16, "#ffffff", sw=0)
             + P("M-6,-15 L-8,88 Q0,98 8,88 L6,-15 Z", "#d7dce6"), 100, 92, rot=-35)

def o_chopsticks():
    return (G(P("M-6,-80 L-3,80 L3,80 L6,-80 Z", "#e7c08e") + R(-7, -80, 14, 34, "#c98f56", rx=3, sw=2), 84, 100, rot=-12)
            + G(P("M-6,-80 L-3,80 L3,80 L6,-80 Z", "#e7c08e") + R(-7, -80, 14, 34, "#c98f56", rx=3, sw=2), 116, 100, rot=12))

def o_plate():
    return E(100, 108, 84, 46, "#ffffff") + E(100, 104, 54, 27, "#f2f5fb") + P("M24,118 Q100,170 176,118", sw=2, stroke="#c9d3e6")

def o_bowl():
    return P("M28,86 L172,86 Q168,150 100,158 Q32,150 28,86 Z", "#e8f1fb") + E(100, 86, 72, 14, "#ffffff") + R(76, 154, 48, 12, "#e8f1fb", rx=4)

def o_bed():
    s = R(22, 54, 18, 112, "#d8a877", rx=6) + R(160, 98, 18, 68, "#d8a877", rx=6)
    s += R(30, 108, 142, 34, "#f6e7d6", rx=8)
    s += E(64, 98, 26, 14, "#ffffff")
    s += P("M70,104 L170,104 Q176,104 176,112 L176,132 L70,132 Z", "#a9c8f0")
    return s

def o_blanket():
    s = ""
    for i, col in enumerate(("#9fc3f0", "#b7d3f5", "#9fc3f0")):
        y = 62 + i * 30
        s += R(26, y, 148, 34, col, rx=16)
    s += "".join(C(x, y, 3.5, "#ffffff", sw=0) for x in (50, 80, 110, 140) for y in (78, 108, 138))
    return s

def o_pillow():
    return (P("M34,70 Q100,52 166,70 Q182,100 166,130 Q100,148 34,130 Q18,100 34,70 Z", "#fdf6e9")
            + P("M60,92 Q100,84 140,92", sw=2, stroke="#e6d7bd") + P("M60,108 Q100,116 140,108", sw=2, stroke="#e6d7bd"))

def o_pajamas():
    top = P("M60,40 L84,32 Q100,44 116,32 L140,40 L170,72 L152,88 L140,78 L140,128 L60,128 L60,78 L48,88 L30,72 Z", "#c7b8f0")
    top += P("M100,44 L100,128", sw=2) + "".join(C(106, y, 3, "#ffffff", sw=1.5) for y in (62, 84, 106))
    pants = P("M66,132 L134,132 L138,182 L106,182 L100,148 L94,182 L62,182 Z", "#c7b8f0")
    dots = "".join(C(x, y, 3.5, "#fff6a8", sw=0) for x, y in ((76, 60), (126, 70), (82, 110), (122, 112), (80, 160), (120, 162)))
    return top + pants + dots

def o_broom():
    s = R(94, 14, 12, 120, "#d79a63", rx=6)
    s += P("M66,132 L134,132 L150,186 L50,186 Z", "#f1d27a")
    s += "".join(P(f"M{x},140 L{x + (x - 100) // 4},184", sw=2, stroke="#c9a24a") for x in (74, 86, 100, 114, 126))
    s += R(62, 124, 76, 14, "#e46f6f", rx=5)
    return s

def o_dustpan():
    return (P("M30,150 L130,150 L150,70 L60,70 Z", "#8ccfb7") + P("M60,70 L150,70 L130,150", sw=W)
            + P("M28,152 L132,152", sw=7) + R(144, 92, 46, 18, "#6cb79b", rx=9, extra='transform="rotate(-25 167 101)"'))

def o_vacuum():
    s = R(92, 18, 14, 120, "#b9c3d6", rx=7) + R(80, 14, 38, 20, "#6f8fd6", rx=10)
    s += R(84, 70, 34, 56, "#7fa0e6", rx=12)
    s += P("M62,140 L142,140 Q152,140 152,152 L152,166 L52,166 L52,152 Q52,140 62,140 Z", "#6f8fd6")
    s += C(66, 170, 7, "#4b4a5c", sw=0) + C(138, 170, 7, "#4b4a5c", sw=0)
    return s

def o_mop():
    s = R(94, 14, 12, 140, "#e39a5e", rx=6)
    s += R(46, 150, 108, 22, "#8ec5f0", rx=8) + R(56, 140, 88, 14, "#5f97d6", rx=4)
    return s

def o_cake():
    s = R(40, 100, 120, 66, "#ffd6e4", rx=10) + P("M40,118 Q55,132 70,118 Q85,132 100,118 Q115,132 130,118 Q145,132 160,118", sw=2.5, stroke="#ffffff")
    s += R(30, 162, 140, 12, "#ffffff", rx=6)
    s += R(54, 70, 92, 34, "#fff1f6", rx=8)
    s += "".join(C(x, 82, 5, "#ff6f8b", sw=1.5) for x in (70, 100, 130))
    for x in (78, 100, 122):
        s += R(x - 4, 42, 8, 28, ["#8fd3ff", "#ffd36b", "#b49af0"][(x // 22) % 3], rx=3, sw=2)
        s += P(f"M{x},40 Q{x - 7},30 {x},18 Q{x + 7},30 {x},40 Z", "#ffb347", sw=2)
    return s

def o_party_hat():
    s = P("M100,22 L150,160 Q100,178 50,160 Z", "#b9a6f2")
    s += P("M84,66 L118,66", sw=0) + P("M66,112 L134,112", sw=4, stroke="#ffe08a") + P("M80,72 L120,72", sw=4, stroke="#9fe0c4")
    s += C(100, 22, 12, "#ffb3c7") + P("M54,160 Q100,174 146,160", sw=3)
    return s

def o_gift():
    s = R(40, 84, 120, 86, "#9fe0c4", rx=6) + R(32, 64, 136, 28, "#7fcfb0", rx=6)
    s += R(92, 64, 16, 106, "#ff8fa3", rx=0) + P("M100,64 C76,30 52,44 70,62 Z", "#ff8fa3") + P("M100,64 C124,30 148,44 130,62 Z", "#ff8fa3")
    return s

OBJECTS = {
    "toothbrush": o_toothbrush, "toothpaste": o_toothpaste, "cup": o_cup,
    "spoon": o_spoon, "chopsticks": o_chopsticks, "plate": o_plate,
    "bed": o_bed, "blanket": o_blanket, "pillow": o_pillow, "pajamas": o_pajamas,
    "broom": o_broom, "dustpan": o_dustpan, "vacuum": o_vacuum, "mop": o_mop,
    "cake": o_cake, "party_hat": o_party_hat, "gift": o_gift,
}

# ------------------------------------------------------------------ situation scenes (400x440)
def frame(bg):
    return f'<rect x="0" y="0" width="400" height="440" fill="{bg}"/>'

def tiles(color, y0=0, y1=300):
    s = ""
    for x in range(0, 401, 50):
        s += P(f"M{x},{y0} L{x},{y1}", sw=1.5, stroke=color)
    for y in range(y0, y1 + 1, 50):
        s += P(f"M0,{y} L400,{y}", sw=1.5, stroke=color)
    return s

def sc_brushing(v):
    kidname, bg, tile = [("minu", "#e3f1ff", "#cfe3f7"), ("sora", "#e4f7ef", "#cbeadc")][v]
    s = frame(bg) + tiles(tile, 0, 300)
    s += R(110, 24, 180, 120, "#f4fbff", rx=14) + P("M136,46 L170,46 M136,60 L156,60", sw=4, stroke="#ffffff")   # mirror
    s += kid(kidname, 200, 168, 1.15, eye="happy", mth="aah",
             arms=(("to", -58, 112, (-74, 84)), ("to", 58, 112, (74, 84))))
    s += R(0, 296, 400, 144, "#ffffff", rx=0) + P("M0,296 L400,296", sw=W)
    s += P("M70,300 L330,300 Q326,372 200,378 Q74,372 70,300 Z", "#eef6ff")   # basin
    s += R(300, 270, 26, 30, "#cfd7e3", rx=6) + P("M313,272 L313,252 L286,252", sw=10) + P("M313,272 L313,252 L286,252", sw=5, stroke="#cfd7e3")
    s += P("M52,404 Q200,426 348,404", sw=2, stroke="#dfe7f2")
    return s

def sc_eating(v):
    kidname, bg = [("jun", "#fff4e3"), ("hana", "#f6f0ff")][v]
    s = frame(bg) + R(40, 40, 100, 80, "#ffffff", rx=10) + P("M90,40 L90,120 M40,80 L140,80", sw=2.5)  # window
    s += kid(kidname, 200, 170, 1.15, eye="happy", mth="grin",
             arms=(("to", -62, 96, (-78, 70)), ("to", 62, 96, (78, 70))),
             extra=P("M-30,50 Q0,78 30,50 L30,96 Q0,106 -30,96 Z", "#ffffff", sw=2.5))   # bib
    s += R(20, 280, 360, 30, "#e7b989", rx=8) + R(40, 306, 24, 120, "#d7a36f", rx=6) + R(336, 306, 24, 120, "#d7a36f", rx=6)
    # steaming soup pot on the table (food is ready, no eating tools shown)
    s += R(280, 236, 84, 48, "#f2a4a4", rx=14) + R(270, 228, 104, 16, "#f6bcbc", rx=8) + R(308, 216, 28, 14, "#e48989", rx=6)
    s += "".join(P(f"M{x},206 C{x - 10},190 {x + 10},182 {x},158", sw=3, stroke="#b9bccb") for x in (298, 322, 346))
    s += R(270, 40, 100, 80, "#ffffff", rx=10, sw=0, extra='opacity="0"')
    return s

def sc_sleeping(v):
    kidname, bg, wall = [("minu", "#3e4a7a", "#e8e4f7"), ("sora", "#3a5470", "#f3ece2")][v]
    s = frame(wall)
    s += R(40, 36, 150, 130, bg, rx=12) + P("M115,36 L115,166 M40,100 L190,100", sw=3)
    s += P("M150,62 A18,18 0 1 0 168,86 A14,14 0 1 1 150,62 Z", "#fff3b0", sw=2)
    s += "".join(P(f"M{x},{y - 5} L{x},{y + 5} M{x - 5},{y} L{x + 5},{y}", sw=2.5, stroke="#fff3b0") for x, y in ((66, 60), (86, 130), (160, 140), (70, 116)))
    s += R(250, 52, 90, 90, "#ffffff", rx=45) + P("M295,97 L295,70 M295,97 L314,106", sw=4)   # clock ~9
    s += R(0, 340, 400, 100, "#d9c7ae", rx=0) + P("M0,340 L400,340", sw=W)
    s += kid(kidname, 210, 214, 1.1, eye="closed", mth="yawn",
             arms=(("to", -20, 10, (-74, 40)), ("down",)))
    s += P("M300,200 L322,200 L300,222 L322,222", sw=3, stroke="#8a85b8") + P("M332,170 L346,170 L332,184 L346,184", sw=2.5, stroke="#8a85b8")
    return s

def dust(x, y, s=1):
    return G(P("M-20,6 Q-24,-8 -10,-8 Q-8,-20 6,-14 Q18,-18 20,-4 Q30,2 20,10 Z", "#cbbfae", sw=2), x, y, s)

def sc_cleaning(v):
    kidname, wall, floor = [("hana", "#fff7e8", "#f0dcc0"), ("jun", "#eef7ff", "#e9d8c4")][v]
    s = frame(wall) + R(0, 260, 400, 180, floor, rx=0) + P("M0,260 L400,260", sw=W)
    s += R(250, 60, 110, 80, "#ffffff", rx=6) + P("M262,120 L290,92 L314,112 L336,86 L350,120 Z", "#bfe3b4", sw=2)   # picture frame
    s += kid(kidname, 130, 120, 1.0, eye="look", mth="hmm",
             arms=(("to", -40, 116, (-82, 86)), ("to", 40, 116, (82, 86))))
    s += R(82, 260, 96, 0.1, floor, sw=0)
    for x, y, k in ((60, 330, 1.2), (150, 372, 1.0), (250, 316, 1.3), (330, 390, 1.1), (300, 280, 0.8), (90, 410, 0.9)):
        s += dust(x, y, k)
    s += "".join(C(x, y, 4, "#e2b06a", sw=1.5) for x, y in ((200, 330), (214, 340), (190, 350), (360, 340), (120, 300), (40, 380)))
    s += P("M226,400 L262,392 L258,418 Z", "#ffffff", sw=2) + P("M330,300 L352,306 L344,324 L324,316 Z", "#ffffff", sw=2)   # paper scraps
    return s

def flag_row(y):
    cols = ["#ffb3c7", "#ffe08a", "#9fe0c4", "#b9a6f2", "#9fcbf2"]
    s = P(f"M10,{y} Q200,{y + 36} 390,{y}", sw=2.5)
    for i in range(8):
        x = 30 + i * 46
        yy = y + 10 + 14 * (1 - ((x - 200) / 190) ** 2)
        s += P(f"M{x - 14},{yy - 6} L{x + 14},{yy - 6} L{x},{yy + 22} Z", cols[i % 5], sw=2)
    return s

def balloon(x, y, col):
    return P(f"M{x},{y + 36} Q{x + 10},{y + 70} {x - 4},{y + 110}", sw=2) + E(x, y, 26, 32, col) + P(f"M{x - 5},{y + 32} L{x + 5},{y + 32} L{x},{y + 40} Z", col, sw=2)

def sc_birthday(v):
    a, b, c, wall = [("sora", "minu", "jun", "#fff2f6"), ("jun", "hana", "minu", "#f3f7ff")][v]
    s = frame(wall) + flag_row(20)
    s += balloon(46, 110, "#ff9fb4") + balloon(354, 120, "#9fcbf2") + balloon(318, 90, "#ffe08a")
    s += kid(b, 96, 196, 0.85, eye="happy", mth="grin", arms=(("to", -8, 78, (-46, 96)), ("to", 8, 70, (46, 96))))
    s += kid(c, 304, 196, 0.85, eye="happy", mth="grin", arms=(("to", -8, 70, (-46, 96)), ("to", 8, 78, (46, 96))))
    s += kid(a, 200, 176, 1.0, eye="happy", mth="grin", arms=(("to", -66, -36, (-84, 28)), ("to", 66, -36, (84, 28))))
    s += R(40, 292, 320, 26, "#ffffff", rx=8) + P("M40,318 L60,350 L80,318 L100,350 L120,318 L140,350 L160,318 L180,350 L200,318 L220,350 L240,318 L260,350 L280,318 L300,350 L320,318 L340,350 L360,318", "#ffd6e4", sw=2.5)
    s += "".join(R(x, y, 8, 8, col, rx=1, sw=0, extra=f'transform="rotate(30 {x} {y})"') for x, y, col in ((150, 60, "#ffb3c7"), (250, 80, "#9fe0c4"), (190, 100, "#ffe08a"), (110, 90, "#b9a6f2"), (300, 52, "#9fcbf2")))
    return s

SCENES = {"brushing": sc_brushing, "eating": sc_eating, "sleeping": sc_sleeping,
          "cleaning": sc_cleaning, "birthday": sc_birthday}

# ------------------------------------------------------------------ usage scenes (300x240), lightly animated
ANIM = """
.wig{animation:wig 0.6s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
@keyframes wig{from{transform:translateX(-8px)}to{transform:translateX(8px)}}
.bob{animation:bob 1.2s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(10px)}to{transform:translateY(-6px)}}
.sweep{animation:sweep 0.9s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:50% 0%}
@keyframes sweep{from{transform:rotate(14deg)}to{transform:rotate(-14deg)}}
.slide{animation:slide 1.6s ease-in-out infinite alternate}
@keyframes slide{from{transform:translateX(-50px)}to{transform:translateX(50px)}}
.fade{animation:fade 1.6s ease-in-out infinite alternate}
@keyframes fade{from{opacity:1}to{opacity:0.1}}
.flick{animation:flick 0.4s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:50% 100%}
@keyframes flick{from{transform:scaleY(1)}to{transform:scaleY(0.75)}}
.zz{animation:zz 2s ease-in-out infinite}
@keyframes zz{0%{opacity:0;transform:translate(0,10px)}40%{opacity:1}100%{opacity:0;transform:translate(16px,-24px)}}
.pop{animation:pop 1.4s ease-in-out infinite alternate}
@keyframes pop{from{transform:translateY(0)}to{transform:translateY(-26px)}}
"""

def ubg(col="#f7fbff"):
    return f'<rect x="0" y="0" width="300" height="240" fill="{col}"/>'

def u_toothbrush():
    s = ubg("#e9f4ff") + kid("minu", 150, 96, 1.0, eye="happy", mth="aah", arms=(("to", -24, 26, (-70, 60)), ("down",)))
    brush = G(R(-70, -5, 70, 10, "#7fb3ea", rx=5) + R(0, -9, 26, 18, "#ffffff", rx=4), 132, 122)
    s += f'<g class="wig">{brush}</g>'
    s += "".join(C(x, y, 5, "#ffffff", sw=1.5) for x, y in ((168, 118), (176, 128), (160, 132)))
    return s

def u_toothpaste():
    s = ubg("#e9f4ff")
    s += G(R(-90, -6, 120, 12, "#7fb3ea", rx=6) + R(30, -10, 40, 20, "#ffffff", rx=5), 140, 170)
    s += f'<g class="fade">{P("M176,156 Q190,146 204,156 Q190,162 176,156 Z", "#9fd4ff", sw=2)}</g>'
    s += G(toothpaste_tube(), 170, 105, 0.6, rot=150)
    return s

def u_cup():
    s = ubg("#fff8e3") + kid("sora", 150, 96, 1.0, eye="closed", mth="o", arms=(("to", -20, 30, (-66, 64)), ("down",)))
    s += f'<g class="bob">{G(o_cup(), 136, 92, 0.45)}</g>'
    return s

def u_spoon():
    s = ubg("#fff4e3") + kid("jun", 150, 90, 1.0, eye="happy", mth="o", arms=(("to", 36, 46, (70, 80)), ("down",)))
    spoon = G(E(0, -30, 16, 22, "#e3e7ef") + E(0, -36, 11, 8, "#ffffff", sw=1.5) + P("M-4,-8 L-5,50 L5,50 L4,-8 Z", "#d7dce6"), 180, 150, rot=-30)
    s += f'<g class="bob">{spoon}</g>'
    s += R(30, 206, 240, 40, "#e7b989", rx=6)
    return s

def u_chopsticks():
    s = ubg("#fff4e3") + R(20, 196, 260, 50, "#e7b989", rx=6) + G(o_plate(), 60, 120, 0.9)
    s += C(150, 210, 0, "#fff")
    piece = C(150, 150, 14, "#9fd38a")
    sticks = G(o_chopsticks(), 112, 30, 0.6)
    s += f'<g class="pop">{sticks}{piece}</g>'
    s += C(118, 214, 10, "#f2a65a") + C(182, 212, 11, "#9fd38a") + C(150, 222, 10, "#ffffff")
    return s

def u_plate():
    s = ubg("#fff4e3") + R(10, 170, 280, 76, "#e7b989", rx=8)
    food = E(150, 150, 44, 22, "#ffffff", sw=2) + C(128, 140, 14, "#ffffff") + C(170, 142, 12, "#9fd38a") + C(150, 132, 10, "#f2a65a")
    s += f'<g class="bob">{G(o_plate(), 40, 70, 1.1)}{food}</g>'
    return s

def u_sleep():
    s = ubg("#3e4a7a") + P("M236,30 A18,18 0 1 0 254,54 A14,14 0 1 1 236,30 Z", "#fff3b0", sw=2)
    s += R(20, 120, 260, 70, "#d8a877", rx=8) + R(20, 90, 22, 120, "#d8a877", rx=6)
    s += E(80, 128, 40, 18, "#fdf6e9")
    s += G(head(KIDS["minu"], eye="closed", mth="smile"), 84, 112, 0.7)
    s += P("M104,130 L278,130 Q286,130 286,140 L286,172 L104,172 Q92,152 104,130 Z", "#a9c8f0")
    s += P("M100,130 Q90,124 112,122", sw=8, stroke="#c7b8f0")   # pajama collar
    s += f'<g class="zz">{P("M150,70 L170,70 L150,90 L170,90", sw=4, stroke="#fff3b0")}</g>'
    return s

def u_broom():
    s = ubg("#fff7e8") + R(0, 190, 300, 50, "#f0dcc0", rx=0)
    s += f'<g class="fade">{dust(110, 205, 1.1)}{dust(190, 212, 0.9)}</g>'
    s += f'<g class="sweep">{G(o_broom(), 100, 20, 1.0)}</g>'
    return s

def u_dustpan():
    s = ubg("#fff7e8") + R(0, 190, 300, 50, "#f0dcc0", rx=0)
    s += G(o_dustpan(), 150, 70, 0.8)
    s += f'<g class="slide">{dust(140, 200, 0.8)}</g>'
    s += f'<g class="sweep">{G(o_broom(), 0, 40, 0.75, rot=-18)}</g>'
    return s

def u_vacuum():
    s = ubg("#eef7ff") + R(0, 190, 300, 50, "#e9d8c4", rx=0)
    s += f'<g class="fade">{dust(80, 214, 0.8)}{dust(230, 214, 0.8)}</g>'
    s += f'<g class="slide">{G(o_vacuum(), 60, 40, 0.85)}</g>'
    return s

def u_mop():
    s = ubg("#eef7ff") + R(0, 190, 300, 50, "#cfe6fb", rx=0)
    s += "".join(f'<g class="fade">{P(f"M{x},{y - 8} L{x},{y + 8} M{x - 8},{y} L{x + 8},{y}", sw=3, stroke="#ffffff")}</g>' for x, y in ((50, 214), (250, 220), (180, 230)))
    s += f'<g class="slide">{G(o_mop(), 60, 30, 0.85)}</g>'
    return s

def u_cake():
    s = ubg("#fff2f6") + G(o_cake(), 50, 40, 1.0)
    s += "".join(R(x, y, 8, 8, c, rx=1, sw=0) for x, y, c in ((40, 40, "#ffb3c7"), (250, 60, "#9fe0c4"), (60, 120, "#ffe08a"), (230, 150, "#b9a6f2")))
    return s.replace('<path d="M78,40', '<path class="flick" d="M78,40').replace('<path d="M100,40', '<path class="flick" d="M100,40').replace('<path d="M122,40', '<path class="flick" d="M122,40')

def u_party_hat():
    s = ubg("#fff2f6") + kid("hana", 150, 120, 1.0, eye="happy", mth="grin", arms=(("to", -60, -30, (-80, 30)), ("to", 60, -30, (80, 30))))
    s += G(o_party_hat(), 150, 4, 0.5, rot=0, extra='transform-origin="0 0"').replace('translate(150 4) scale(0.5)', 'translate(108 -8) scale(0.42)')
    s += "".join(R(x, y, 8, 8, c, rx=1, sw=0) for x, y, c in ((40, 40, "#ffb3c7"), (250, 50, "#9fe0c4"), (60, 200, "#ffe08a"), (240, 190, "#b9a6f2")))
    return s

def u_gift():
    s = ubg("#f0fbf6")
    box = R(90, 120, 120, 86, "#9fe0c4", rx=6) + R(142, 120, 16, 86, "#ff8fa3", rx=0)
    lid = G(R(-68, -14, 136, 28, "#7fcfb0", rx=6) + R(-8, -14, 16, 28, "#ff8fa3", rx=0), 150, 106)
    s += box + f'<g class="pop">{lid}</g>'
    s += f'<g class="fade">{P("M150,70 L156,86 L172,86 L160,96 L164,112 L150,102 L136,112 L140,96 L128,86 L144,86 Z", "#ffe08a", sw=2)}</g>'
    return s

USAGE = {
    "toothbrush": u_toothbrush, "toothpaste": u_toothpaste, "cup": u_cup,
    "spoon": u_spoon, "chopsticks": u_chopsticks, "plate": u_plate,
    "sleep": u_sleep, "broom": u_broom, "dustpan": u_dustpan, "vacuum": u_vacuum, "mop": u_mop,
    "cake": u_cake, "party_hat": u_party_hat, "gift": u_gift,
}

def main():
    for sub in ("objects", "scenes", "usage"):
        os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    for k, f in OBJECTS.items():
        open(os.path.join(ROOT, "objects", f"{k}.svg"), "w").write(svg(200, 200, f()))
    for k, f in SCENES.items():
        for v in (0, 1):
            open(os.path.join(ROOT, "scenes", f"{k}-{v + 1}.svg"), "w").write(svg(400, 440, f(v)))
    for k, f in USAGE.items():
        open(os.path.join(ROOT, "usage", f"{k}.svg"), "w").write(svg(300, 240, f(), ANIM))
    print("objects", len(OBJECTS), "scenes", len(SCENES) * 2, "usage", len(USAGE))

if __name__ == "__main__":
    main()
