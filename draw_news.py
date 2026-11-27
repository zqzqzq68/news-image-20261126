#!/usr/bin/env python3
"""Draw the front page that sums up Thursday 26 November 2026 in one image.

The program renders a 1024x1024 newspaper-style infographic with PIL and
writes it to entry.png next to this file. All news text is baked in as
constants below; there is no network access, no randomness and no clock
input, so repeated runs write byte-identical files.

News picked for the day (all first reported on 26 November 2026):
  1. A huge storm hits the US East Coast; New York postpones the Macy's
     Thanksgiving Day Parade for the first time in a century.
  2. A fuel tanker crashes on a busy Cairo highway and bursts into
     flames; 31 people are killed and 21 injured.
  3. A huge explosion rocks an oil depot in Bangkok; several people are
     hurt and residents are told to evacuate.
  4. President Trump calls the GDP figures "fake" and demands a probe of
     his own Commerce Department.
  5. UK net migration falls to 77,000, its lowest annual level in
     nearly 30 years.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
NAVY_LIGHT = (43, 58, 92)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
CARD = (255, 255, 255)
MUTED = (96, 94, 84)
RULE = (196, 190, 172)
ORANGE = (232, 89, 12)
YELLOW = (244, 180, 0)
TEAL = (11, 114, 133)
BLUE = (43, 108, 196)
SKY = (52, 74, 116)
RAIN = (150, 185, 225)
CLOUD = (128, 146, 176)
CLOUD_DARK = (96, 114, 144)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split(" ")
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top to bottom; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, x, y, w, h, accent):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD, outline=RULE, width=1)
    draw.rectangle([x, y, x + w - 1, y + 5], fill=accent)


def draw_flame(draw, cx, cy, s):
    """A stylised flame made of three nested polygons."""
    outer = [
        (cx, cy - 46 * s),
        (cx + 26 * s, cy - 8 * s),
        (cx + 34 * s, cy + 18 * s),
        (cx + 14 * s, cy + 38 * s),
        (cx - 14 * s, cy + 38 * s),
        (cx - 34 * s, cy + 18 * s),
        (cx - 26 * s, cy - 8 * s),
    ]
    draw.polygon(outer, fill=ORANGE)
    mid = [
        (cx, cy - 22 * s),
        (cx + 16 * s, cy + 2 * s),
        (cx + 20 * s, cy + 22 * s),
        (cx - 20 * s, cy + 22 * s),
        (cx - 16 * s, cy + 2 * s),
    ]
    draw.polygon(mid, fill=YELLOW)
    draw.ellipse(
        [cx - 9 * s, cy + 8 * s, cx + 9 * s, cy + 30 * s], fill=RED
    )


def draw_burst(draw, cx, cy, r):
    """A starburst explosion with smoke puffs."""
    pts = []
    spikes = 12
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rad = r if i % 2 == 0 else r * 0.45
        x = cx + rad * math.cos(ang)
        y = cy + rad * math.sin(ang)
        pts.append((x, y))
    draw.polygon(pts, fill=ORANGE)
    pts2 = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r * 0.55 if i % 2 == 0 else r * 0.28
        x = cx + rad * math.cos(ang)
        y = cy + rad * math.sin(ang)
        pts2.append((x, y))
    draw.polygon(pts2, fill=YELLOW)
    draw.ellipse([cx - 22, cy - 30, cx - 4, cy - 14], fill=CLOUD)
    draw.ellipse([cx + 4, cy - 34, cx + 22, cy - 16], fill=CLOUD_DARK)


def draw_bars(draw, x, y, w, h):
    """Three bars, the tallest one red, for the GDP story."""
    bw = w // 4
    heights = [h * 0.45, h * 0.7, h * 1.0]
    colors = [BLUE, TEAL, RED]
    for i in range(3):
        bx = x + i * (bw + 6)
        bh = heights[i]
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=colors[i])
    draw.line([x, y + h + 2, x + w, y + h + 2], fill=INK, width=2)


def draw_arrow_down(draw, cx, cy, w, h):
    """A bold downward arrow for falling migration."""
    shaft_w = w * 0.34
    head_h = h * 0.45
    pts = [
        (cx - shaft_w / 2, cy - h / 2),
        (cx + shaft_w / 2, cy - h / 2),
        (cx + shaft_w / 2, cy + h / 2 - head_h),
        (cx + w / 2, cy + h / 2 - head_h),
        (cx, cy + h / 2),
        (cx - w / 2, cy + h / 2 - head_h),
        (cx - shaft_w / 2, cy + h / 2 - head_h),
    ]
    draw.polygon(pts, fill=TEAL)


def draw_storm_panel(draw, x, y, w, h):
    """Storm sky with clouds, rain and a parade balloon."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=SKY)
    draw.ellipse([x + 8, y + 18, x + 118, y + 78], fill=CLOUD_DARK)
    draw.ellipse([x + 80, y + 4, x + 210, y + 62], fill=CLOUD)
    draw.ellipse([x + 180, y + 26, x + 292, y + 84], fill=CLOUD_DARK)
    draw.ellipse([x + 30, y + 52, x + 140, y + 100], fill=CLOUD)
    for i in range(9):
        rx = x + 18 + i * 30
        draw.line([rx, y + 118, rx - 14, y + 168], fill=RAIN, width=3)
    for i in range(8):
        rx = x + 34 + i * 30
        draw.line([rx, y + 186, rx - 14, y + 232], fill=RAIN, width=3)
    bx, by = x + w - 108, y + 96
    draw.ellipse([bx, by, bx + 84, by + 104], fill=RED)
    draw.rectangle([bx, by + 44, bx + 84, by + 60], fill=CARD)
    draw.line([bx + 8, by + 100, bx + 30, by + 132], fill=INK, width=2)
    draw.line([bx + 76, by + 100, bx + 54, by + 132], fill=INK, width=2)
    draw.rectangle([bx + 28, by + 130, bx + 56, by + 148], fill=(120, 72, 20))
    draw.line([x + 8, y + h - 34, x + w - 8, y + h - 34], fill=GOLD, width=2)
    draw.text(
        (x + 12, y + h - 28),
        "The parade waits out the storm.",
        font=font(SANS, 17),
        fill=(235, 235, 225),
    )


def story_card(draw, x, y, w, h, kicker, headline, deck, accent, icon,
               hsize=28, dsize=19, icon_h=52):
    card(draw, x, y, w, h, accent)
    ix, iy = x + 20, y + 14
    if icon == "flame":
        draw_flame(draw, ix + 28, iy + icon_h / 2 + 4, icon_h / 90.0)
    elif icon == "burst":
        draw_burst(draw, ix + 30, iy + icon_h / 2, icon_h * 0.5)
    elif icon == "bars":
        draw_bars(draw, ix + 2, iy + 8, 56, icon_h - 14)
    elif icon == "arrow":
        draw_arrow_down(draw, ix + 28, iy + icon_h / 2, 50, icon_h - 4)
    draw.text((x + 88, y + 20), kicker, font=font(SANS_B, 18), fill=accent)
    rule_y = y + icon_h + 8
    draw.line([x + 20, rule_y, x + w - 20, rule_y], fill=RULE, width=1)
    head_lines = wrap(draw, headline, font(SERIF_B, hsize), w - 40)
    ty = draw_lines(
        draw, x + 20, rule_y + 10, head_lines, font(SERIF_B, hsize),
        INK, hsize + 5,
    )
    deck_lines = wrap(draw, deck, font(SANS, dsize), w - 40)
    draw_lines(draw, x + 20, ty + 6, deck_lines, font(SANS, dsize),
               MUTED, dsize + 5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, W - 1, 149], fill=NAVY)
    draw.rectangle([0, 150, W - 1, 153], fill=GOLD)
    title = "THE WORLD IN ONE IMAGE"
    tf = font(SERIF_B, 54)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 26), title, font=tf, fill=(250, 247, 238))
    date = "THURSDAY  •  26 NOVEMBER 2026"
    df = font(SANS, 24)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 96), date, font=df, fill=GOLD)

    # Lead story: the postponed parade.
    lx, ly, lw, lh = 36, 170, 952, 316
    card(draw, lx, ly, lw, lh, RED)
    draw.text(
        (lx + 24, ly + 22),
        "NEW YORK  •  UNITED STATES",
        font=font(SANS_B, 20),
        fill=RED,
    )
    head = wrap(
        draw, "STORM POSTPONES\nTHE PARADE", font(SERIF_B, 48), 580
    )
    ty = draw_lines(
        draw, lx + 24, ly + 56, head, font(SERIF_B, 48), INK, 56
    )
    deck = wrap(
        draw,
        "A huge storm hits the US East Coast, forcing the first "
        "postponement in a century of New York's Macy's Thanksgiving "
        "Day Parade.",
        font(SANS, 23),
        580,
    )
    draw_lines(draw, lx + 24, ty + 14, deck, font(SANS, 23), MUTED, 30)
    draw_storm_panel(draw, lx + 632, ly + 22, 296, 272)

    # Second row: Cairo and Bangkok.
    story_card(
        draw, 36, 506, 466, 240,
        "CAIRO  •  EGYPT",
        "31 KILLED IN CAIRO TANKER FIRE",
        "A fuel tanker crashes on a busy Cairo highway and bursts "
        "into flames; 21 more are injured, Egypt's health ministry says.",
        ORANGE, "flame",
    )
    story_card(
        draw, 522, 506, 466, 240,
        "BANGKOK  •  THAILAND",
        "BLAST ROCKS BANGKOK OIL DEPOT",
        "A huge explosion at an oil depot sends black smoke over "
        "Bangkok; several people are hurt and residents are told to "
        "evacuate.",
        RED, "burst",
    )

    # Third row: Washington and London.
    story_card(
        draw, 36, 766, 466, 194,
        "WASHINGTON  •  UNITED STATES",
        "TRUMP CALLS GDP FIGURES \u201cFAKE\u201d",
        "The president demands a probe of his own Commerce Department.",
        BLUE, "bars", hsize=26, icon_h=44,
    )
    story_card(
        draw, 522, 766, 466, 194,
        "LONDON  •  UNITED KINGDOM",
        "UK MIGRATION FALLS TO 77,000",
        "Net migration drops to its lowest annual level in nearly "
        "30 years.",
        TEAL, "arrow", hsize=26, icon_h=44,
    )

    # Footer: more of the day, then sources.
    foot = ("ALSO:  SpaceX cleared for a million satellites  •  "
            "New ECB chief named  •  Nvidia halts AI server shipments")
    ff = font(SANS, 15)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 972), foot, font=ff, fill=INK)
    src = "Sources: South China Morning Post  •  NDTV  •  BBC  •  Al Jazeera  —  26 November 2026"
    sf = font(SANS, 15)
    sw = draw.textlength(src, font=sf)
    draw.text(((W - sw) / 2, 996), src, font=sf, fill=MUTED)

    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
