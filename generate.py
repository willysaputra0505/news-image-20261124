#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news poster (1024x1024 PNG).

Deterministic: PIL primitives only, no randomness, no timestamps, no
network. Running this file twice writes byte-identical entry.png.

Layout: newspaper masthead on top, six story panels in a 2x3 grid,
a four-item "Also today" strip, and a small footer line.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- data ---

DATE_LINE = "TUESDAY \u00b7 24 NOVEMBER 2026"
STANDFIRST = "Six stories that defined the day \u2014 from Kyiv to Copenhagen, Wall Street to Java."

# Each panel: kicker, kicker colour, headline, deck, icon kind.
PANELS = [
    {
        "kicker": "WAR \u00b7 UKRAINE",
        "colour": (155, 28, 28),
        "headline": "Russian strikes kill at least 12 in Kyiv region",
        "deck": "A drone flattens a block of flats in Dymer; rescuers still search the rubble for the missing.",
        "icon": "burst",
    },
    {
        "kicker": "MARKETS",
        "colour": (22, 101, 52),
        "headline": "Huang's return lifts tech: Nvidia adds nearly $1tn",
        "deck": "Nvidia jumps 31% as its founder is reinstated; SK hynix ADRs surge 20% and Asian markets rally.",
        "icon": "chart",
    },
    {
        "kicker": "EUROPE",
        "colour": (30, 58, 95),
        "headline": "Denmark's top court backs \u2018ghetto law\u2019 evictions",
        "deck": "The Supreme Court rules the housing law is not ethnic discrimination, backing the hard line on immigration.",
        "icon": "court",
    },
    {
        "kicker": "AMERICA",
        "colour": (91, 33, 182),
        "headline": "Trump gets path to erase hush-money conviction",
        "deck": "Appeals judges revive his bid to move the case to federal court, where he can argue immunity.",
        "icon": "scales",
    },
    {
        "kicker": "DISASTER",
        "colour": (194, 65, 12),
        "headline": "Java factory fire: 24 dead, about 30 still missing",
        "deck": "Rescuers pick through the ruined candy plant in Cikande as DNA tests are needed to name the dead.",
        "icon": "flame",
    },
    {
        "kicker": "SPORT",
        "colour": (15, 118, 110),
        "headline": "FIFA picks 2031 and 2035 Women's Cup hosts",
        "deck": "USA, Mexico, Costa Rica and Jamaica take 2031 \u2014 the first 48-team edition; the UK hosts 2035.",
        "icon": "ball",
    },
]

# Each strip item: bold lead-in, then the short text.
STRIP = [
    ("UKRAINE STRIKES BACK", "Drones hit oil sites in Tatarstan, Perm and Rostov."),
    ("NATO MEETS", "Allies meet in Brussels over missiles in Poland."),
    ("GROK SUED", "Virginia and Oregon sue SpaceX over Grok images."),
    ("UNDER-16 BAN", "Bangladesh court orders social-media limits."),
]

FOOTER = "Compiled from wire reports: Reuters \u00b7 AP \u00b7 FIFA \u00b7 Korea Exchange \u2014 morning edition"

# -------------------------------------------------------------- constants ---

SIZE = 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 244)
INK = (25, 25, 25)
GREY = (90, 86, 76)
RULE = (25, 25, 25)
STRIP_BG = (238, 231, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- helpers ---

def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top-down; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ------------------------------------------------------------------ icons ---

def icon_burst(draw, x, y, s):
    """Explosion burst over dark rooftops."""
    cx, cy = x + s // 2, y + s // 2 - 6
    pts = []
    import math

    for i in range(16):
        ang = math.pi * 2 * i / 16
        r = s * 0.42 if i % 2 == 0 else s * 0.20
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=(245, 158, 11), outline=(180, 83, 9))
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(254, 243, 199))
    base = y + s - 4
    draw.rectangle([x + 2, base - 16, x + 24, base], fill=INK)
    draw.rectangle([x + 28, base - 24, x + 48, base], fill=INK)
    draw.rectangle([x + 52, base - 12, x + 72, base], fill=INK)


def icon_chart(draw, x, y, s):
    """Rising market line over bars."""
    bar_w = 10
    heights = [18, 30, 24, 42]
    for i, h in enumerate(heights):
        bx = x + 6 + i * 16
        draw.rectangle([bx, y + s - 8 - h, bx + bar_w, y + s - 8], fill=(187, 247, 208))
    pts = [(x + 6, y + s - 26), (x + 22, y + s - 40), (x + 38, y + s - 32),
           (x + 54, y + s - 52), (x + 70, y + s - 60)]
    draw.line(pts, fill=(22, 101, 52), width=5, joint="curve")
    draw.polygon([(x + 70, y + s - 60), (x + 58, y + s - 58), (x + 68, y + s - 46)],
                 fill=(22, 101, 52))


def icon_court(draw, x, y, s):
    """Courthouse: pediment, columns, steps."""
    draw.polygon([(x + 4, y + 22), (x + s // 2, y + 4), (x + s - 4, y + 22)],
                 fill=(30, 58, 95))
    draw.rectangle([x + 6, y + 22, x + s - 6, y + 26], fill=(30, 58, 95))
    for i in range(3):
        cx = x + 16 + i * 22
        draw.rectangle([cx - 4, y + 28, cx + 4, y + s - 22], fill=(30, 58, 95))
    draw.rectangle([x + 6, y + s - 22, x + s - 6, y + s - 18], fill=(30, 58, 95))
    draw.rectangle([x + 2, y + s - 16, x + s - 2, y + s - 10], fill=(30, 58, 95))


def icon_scales(draw, x, y, s):
    """Scales of justice."""
    cx = x + s // 2
    draw.rectangle([cx - 2, y + 8, cx + 2, y + s - 16], fill=(91, 33, 182))
    draw.line([(x + 8, y + 16), (x + s - 8, y + 16)], fill=(91, 33, 182), width=4)
    for sx in (x + 8, x + s - 8):
        draw.line([(sx, y + 16), (sx - 12, y + 38)], fill=(91, 33, 182), width=3)
        draw.line([(sx, y + 16), (sx + 12, y + 38)], fill=(91, 33, 182), width=3)
        draw.arc([sx - 13, y + 30, sx + 13, y + 56], 0, 180, fill=(91, 33, 182), width=3)
    draw.rectangle([x + s // 2 - 14, y + s - 16, x + s // 2 + 14, y + s - 10],
                   fill=(91, 33, 182))


def icon_flame(draw, x, y, s):
    """Flame in three layered teardrops."""
    cx = x + s // 2
    outer = [(cx, y + 4), (cx + 26, y + 34), (cx + 20, y + s - 8),
             (cx - 20, y + s - 8), (cx - 26, y + 34)]
    draw.polygon(outer, fill=(234, 88, 12))
    mid = [(cx, y + 20), (cx + 16, y + 42), (cx + 12, y + s - 10),
           (cx - 12, y + s - 10), (cx - 16, y + 42)]
    draw.polygon(mid, fill=(249, 115, 22))
    core = [(cx, y + 38), (cx + 9, y + 54), (cx + 7, y + s - 12),
            (cx - 7, y + s - 12), (cx - 9, y + 54)]
    draw.polygon(core, fill=(253, 224, 71))


def icon_ball(draw, x, y, s):
    """Soccer ball: white circle, dark pentagon, seams."""
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 3
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=INK, width=3)
    import math

    pent = []
    for i in range(5):
        ang = -math.pi / 2 + 2 * math.pi * i / 5
        pent.append((cx + 13 * math.cos(ang), cy + 13 * math.sin(ang)))
    draw.polygon(pent, fill=INK)
    for i in range(5):
        ang = -math.pi / 2 + 2 * math.pi * i / 5
        px, py = pent[i]
        ex = cx + r * math.cos(ang) * 0.92
        ey = cy + r * math.sin(ang) * 0.92
        draw.line([(px, py), (ex, ey)], fill=INK, width=2)


ICONS = {
    "burst": icon_burst,
    "chart": icon_chart,
    "court": icon_court,
    "scales": icon_scales,
    "flame": icon_flame,
    "ball": icon_ball,
}

# ------------------------------------------------------------------ poster ---

def draw_panel(draw, x, y, w, h, panel):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    pad = 16
    # Kicker tag, top left.
    kf = font(SANS_BOLD, 15)
    kw = draw.textlength(panel["kicker"], font=kf)
    tag_w = kw + 16
    draw.rectangle([x + pad, y + 12, x + pad + tag_w, y + 38], fill=panel["colour"])
    draw.text((x + pad + 8, y + 16), panel["kicker"], font=kf, fill=(255, 255, 255))
    # Icon, top right.
    ICONS[panel["icon"]](draw, x + w - 88, y + 10, 76)
    # Headline, wrapped to the width left of the icon.
    hf = font(SANS_BOLD, 26)
    head_lines = wrap(draw, panel["headline"], hf, w - pad * 2 - 92)
    hy = text_block(draw, x + pad, y + 46, head_lines, hf, INK, 30)
    # Thin rule under the headline.
    draw.line([(x + pad, hy + 4), (x + w - pad, hy + 4)], fill=(200, 192, 172), width=1)
    # Deck, full width, trimmed to fit the panel.
    df = font(SANS, 17)
    deck_lines = wrap(draw, panel["deck"], df, w - pad * 2)
    room = (y + h - 12) - (hy + 12)
    max_deck = max(1, room // 22)
    deck_lines = deck_lines[:max_deck]
    text_block(draw, x + pad, hy + 12, deck_lines, df, (58, 54, 46), 22)


def draw_poster():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    # Double outer frame.
    draw.rectangle([12, 12, SIZE - 12, SIZE - 12], outline=INK, width=3)
    draw.rectangle([20, 20, SIZE - 20, SIZE - 20], outline=INK, width=1)

    # Masthead.
    mast = font(SERIF_BOLD, 58)
    centred(draw, SIZE // 2, 32, "THE WORLD IN ONE DAY", mast, INK)
    draw.line([(48, 112), (SIZE - 48, 112)], fill=RULE, width=2)
    date_f = font(SANS_BOLD, 25)
    centred(draw, SIZE // 2, 124, DATE_LINE, date_f, (155, 28, 28))
    stand_f = font(SERIF, 19)
    centred(draw, SIZE // 2, 156, STANDFIRST, stand_f, GREY)
    draw.line([(48, 186), (SIZE - 48, 186)], fill=RULE, width=2)

    # Six panels, 2 columns x 3 rows.
    margin = 36
    gap = 12
    pw = (SIZE - margin * 2 - gap) // 2
    ph = 208
    top = 196
    for i, panel in enumerate(PANELS):
        px = margin + (i % 2) * (pw + gap)
        py = top + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, panel)

    # "Also today" strip: two rows of two items, lead line then text line.
    strip_y = top + 3 * ph + 2 * gap + 14
    strip_h = 118
    draw.rectangle([margin, strip_y, SIZE - margin, strip_y + strip_h],
                   fill=STRIP_BG, outline=INK, width=2)
    label_f = font(SANS_BOLD, 16)
    draw.text((margin + 14, strip_y + 8), "ALSO TODAY", font=label_f,
              fill=(155, 28, 28))
    item_f = font(SANS, 16)
    bold_f = font(SANS_BOLD, 16)
    cell_w = (SIZE - margin * 2 - 28) // 2
    for i, (lead, text) in enumerate(STRIP):
        cx = margin + 14 + (i % 2) * cell_w
        cy = strip_y + 30 + (i // 2) * 46
        draw.text((cx, cy), lead, font=bold_f, fill=INK)
        draw.text((cx, cy + 20), text, font=item_f, fill=(58, 54, 46))

    # Footer.
    foot_f = font(SANS, 14)
    centred(draw, SIZE // 2, strip_y + strip_h + 8, FOOTER, foot_f, GREY)

    return img


def main():
    poster = draw_poster()
    poster.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
