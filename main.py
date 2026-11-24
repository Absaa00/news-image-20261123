#!/usr/bin/env python3
"""THE DAILY WORLD - one-page newspaper image summing up world news,
Monday 23 November 2026. Writes /output/entry.png (1024x1024, PNG).

Deterministic: no network, no clock, no randomness. Pure Pillow drawing.
Revision r3-a: double rule under the masthead for the classic front-page
look, and the lead chip now carries its own green price tag.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (247, 242, 231)
INK = (18, 18, 18)
RULE = (18, 18, 18)
GREY = (90, 86, 78)
ACCENT = (176, 32, 28)
GREEN = (34, 128, 74)
NAVY = (28, 52, 92)
GOLD = (184, 134, 11)
SKY = (70, 130, 180)
PANEL = (255, 253, 247)


def font(size, bold=False):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading=6, fill=INK):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading=2):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=INK)
        y += fnt.size + leading
    return y


def rule(draw, x0, y, x1, wdt=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=wdt)


def kicker(draw, x, y, text, color=ACCENT):
    f = font(17)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 22


def draw_chip(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=GREEN, outline=INK, width=3)
    for i in range(4):
        px = x + 12 + i * (s - 24) // 3
        draw.line([(px, y - 10), (px, y)], fill=INK, width=3)
        draw.line([(px, y + s), (px, y + s + 10)], fill=INK, width=3)
        py = y + 12 + i * (s - 24) // 3
        draw.line([(x - 10, py), (x, py)], fill=INK, width=3)
        draw.line([(x + s, py), (x + s + 10, py)], fill=INK, width=3)
    draw.rectangle([x + s // 4, y + s // 4, x + 3 * s // 4, y + 3 * s // 4],
                   outline=(255, 255, 255), width=3)
    draw.text((x + s // 4 + 8, y + s // 4 + 8), "NVDA", font=font(20),
              fill=(255, 255, 255))


def draw_ship(draw, x, y, w, h):
    draw.rectangle([x, y + h - 26, x + w, y + h - 8], fill=NAVY)
    draw.polygon([(x + 8, y + h - 26), (x + w - 8, y + h - 26),
                  (x + w - 22, y + h - 44), (x + 22, y + h - 44)], fill=NAVY)
    draw.rectangle([x + w // 2 - 4, y + 6, x + w // 2 + 4, y + h - 44],
                   fill=NAVY)
    draw.line([(x + w // 2, y + 6), (x + w // 2 + 26, y + 16)],
              fill=ACCENT, width=3)
    for cx, cy, r in [(x + w - 14, y + 2, 7), (x + w - 26, y + 10, 5),
                      (x + w - 4, y + 14, 4)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 165, 0))


def draw_globe(draw, x, y, r):
    draw.ellipse([x - r, y - r, x + r, y + r], outline=NAVY, width=3)
    draw.ellipse([x - r // 2, y - r, x + r // 2, y + r], outline=NAVY, width=2)
    draw.line([(x - r, y), (x + r, y)], fill=NAVY, width=2)
    draw.arc([x - r, y - r // 2, x + r, y + r // 2], 200, 340, fill=NAVY,
             width=2)
    draw.line([(x - r - 14, y - r - 6), (x + r + 14, y - r - 6)],
              fill=ACCENT, width=4)


def draw_city(draw, x, y, w, h):
    for i, bh in enumerate([52, 78, 44, 66, 58]):
        bx = x + i * (w // 5)
        draw.rectangle([bx, y + h - bh, bx + w // 5 - 6, y + h], fill=GREY)
    for cx, cy in [(x + 20, y + 8), (x + w - 30, y + 2)]:
        for r, col in [(16, (200, 200, 200)), (10, (160, 160, 160))]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def draw_mercury(draw, x, y, r):
    draw.ellipse([x - r - 26, y - r - 20, x + r + 26, y + r + 20],
                 outline=GREY, width=2)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(196, 164, 132),
                 outline=INK, width=2)
    for cx, cy, cr in [(x - 12, y - 8, 7), (x + 14, y + 10, 5),
                       (x + 4, y - 18, 4), (x - 20, y + 14, 4)]:
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                     outline=(120, 96, 74), width=2)


def draw_ball(draw, x, y, r):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255),
                 outline=INK, width=3)
    draw.polygon([(x, y - 14), (x + 13, y - 4), (x + 8, y + 12),
                  (x - 8, y + 12), (x - 13, y - 4)], fill=INK)
    for ang in (90, 210, 330):
        import math
        ex = x + int(r * 0.92 * math.cos(math.radians(ang)))
        ey = y - int(r * 0.92 * math.sin(math.radians(ang)))
        draw.line([(x, y - 14), (ex, ey)], fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # Masthead
    d.text((W // 2, 34), "THE DAILY WORLD", font=font(66), fill=INK,
           anchor="ma")
    rule(d, 40, 112, W - 40, 3)
    d.text((40, 122), "MONDAY, 23 NOVEMBER 2026", font=font(20), fill=INK)
    d.text((W - 40, 122), "THE WORLD IN ONE PAGE", font=font(20), fill=INK,
           anchor="ra")
    rule(d, 40, 150, W - 40, 1)
    rule(d, 40, 154, W - 40, 1)

    # Lead story: Nvidia
    lx, ly, lw, lh = 40, 164, W - 80, 236
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL, outline=INK, width=2)
    kicker(d, lx + 16, ly + 12, "Lead story  |  Technology & markets")
    y = headline(d, lx + 16, ly + 38, "HUANG IS BACK",
                 font(44), 560)
    y = headline(d, lx + 16, y + 2, "SHARES SOAR 31%",
                 font(44), 560)
    y = para(d, lx + 16, y + 10,
             "Jensen Huang is reinstated as chief executive and returns to "
             "Nvidia's Santa Clara headquarters. Wall Street cheers: the "
             "chipmaker's shares jump 31% in a single day.",
             font(19), 560, leading=5)
    draw_chip(d, lx + lw - 190, ly + 52, 120)
    d.text((lx + lw - 190, ly + 190), "NVDA  +31.5%", font=font(24),
           fill=GREEN)
    d.text((lx + lw - 190, ly + 218), "Best day of the year", font=font(15),
           fill=GREY)

    # Grid: 2 columns x 2 rows
    gx, gy = 40, 420
    cw, ch, gap = 462, 196, 20
    panels = [
        ("War  |  Mediterranean", "DRONES SINK WARSHIP IN LIBYA",
         "Ukraine confirms its sea drones sank a Russian warship at "
         "Benghazi, widening the war to a new sea. A second Russian "
         "cargo ship is hit in the Baltic.", "ship"),
        ("Climate  |  Turkey", "COP31 ENDS WITH NO DEAL",
         "The longest UN climate summit closes without agreement after "
         "record-long talks split over fossil-fuel phase-out and "
         "adaptation finance.", "globe"),
        ("War  |  Ukraine", "KYIV STRIKES KILL AT LEAST 15",
         "Russian bombardment of the Kyiv region kills at least 15 "
         "people. A boy is pulled alive from the rubble as homes and "
         "streets burn.", "city"),
        ("Space  |  Mercury", "ARRIVAL AT MERCURY",
         "After an eight-year journey, the BepiColombo spacecraft enter "
         "orbit around Mercury - a first for the joint European-Japanese "
         "mission.", "mercury"),
    ]
    for i, (kick, head, body, art) in enumerate(panels):
        px = gx + (i % 2) * (cw + gap)
        py = gy + (i // 2) * (ch + gap)
        d.rectangle([px, py, px + cw, py + ch], fill=PANEL, outline=INK,
                    width=2)
        kicker(d, px + 14, py + 10, kick)
        headline(d, px + 14, py + 34, head, font(24), cw - 150)
        para(d, px + 14, py + 96, body, font(15), cw - 150, leading=3)
        ax, ay = px + cw - 128, py + 52
        if art == "ship":
            draw_ship(d, ax, ay, 112, 96)
        elif art == "globe":
            draw_globe(d, ax + 56, ay + 48, 42)
        elif art == "city":
            draw_city(d, ax, ay, 112, 96)
        elif art == "mercury":
            draw_mercury(d, ax + 56, ay + 48, 40)

    # Bottom strip: World Cup + also today
    bx, by, bw, bh = 40, 852, W - 80, 132
    d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY, outline=INK, width=2)
    draw_ball(d, bx + 66, by + 66, 40)
    d.text((bx + 126, by + 16), "UK TO HOST 2035 WOMEN'S WORLD CUP",
           font=font(26), fill=(255, 255, 255))
    d.text((bx + 126, by + 52),
           "FIFA confirms England, Scotland, Wales and Northern Ireland",
           font=font(17), fill=(220, 225, 235))
    d.text((bx + 126, by + 74),
           "as joint hosts. Also today: NHS trials AI breast screening  |  "
           "Eurozone inflation 4.0%  |  Indonesia factory fire kills 24",
           font=font(15), fill=(200, 208, 220))
    d.text((bx + 126, by + 102), "THE DAILY WORLD  -  23 NOVEMBER 2026",
           font=font(14), fill=(180, 188, 200))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes sha256",
          hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
