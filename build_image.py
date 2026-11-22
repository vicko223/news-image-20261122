#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up Sunday 22 November 2026.

Only the four verified stories of that day are shown:
  1. COP31 climate summit in Antalya reaches a final deal text.
  2. Formula 1 races under the Las Vegas lights.
  3. A magnitude 4.1 earthquake strikes Myanmar before dawn.
  4. South Africa lowers its flags for Phumzile Mlambo-Ngcuka.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
TEAL = (15, 94, 92)
BRICK = (168, 50, 38)
NAVY = (18, 24, 52)
OCEAN = (46, 109, 164)
LAND = (94, 156, 92)
GOLD = (214, 164, 32)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def centered(draw, cx, y, s, f, fill=INK):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Stylised Earth with meridians, simple land blobs, sun and coast waves."""
    # sun with rays, top right of the globe
    sx, sy, sr = cx + r + 38, cy - r + 6, 26
    for i in range(12):
        a = math.radians(i * 30)
        draw.line(
            [(sx + (sr + 6) * math.cos(a), sy + (sr + 6) * math.sin(a)),
             (sx + (sr + 20) * math.cos(a), sy + (sr + 20) * math.sin(a))],
            fill=GOLD, width=5)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD)
    # ocean
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN, outline=INK, width=3)
    # land blobs (abstract continents)
    blobs = [
        [(cx - 0.72 * r, cy - 0.45 * r), (cx - 0.30 * r, cy - 0.62 * r),
         (cx - 0.18 * r, cy - 0.30 * r), (cx - 0.42 * r, cy - 0.08 * r),
         (cx - 0.68 * r, cy - 0.18 * r)],
        [(cx - 0.40 * r, cy + 0.12 * r), (cx - 0.12 * r, cy + 0.05 * r),
         (cx - 0.16 * r, cy + 0.55 * r), (cx - 0.34 * r, cy + 0.72 * r),
         (cx - 0.48 * r, cy + 0.38 * r)],
        [(cx + 0.05 * r, cy - 0.55 * r), (cx + 0.55 * r, cy - 0.45 * r),
         (cx + 0.62 * r, cy - 0.05 * r), (cx + 0.30 * r, cy + 0.18 * r),
         (cx + 0.10 * r, cy - 0.15 * r)],
        [(cx + 0.22 * r, cy + 0.38 * r), (cx + 0.55 * r, cy + 0.32 * r),
         (cx + 0.58 * r, cy + 0.58 * r), (cx + 0.30 * r, cy + 0.62 * r)],
    ]
    for b in blobs:
        draw.polygon(b, fill=LAND)
    # meridians and parallels, clipped by redrawing the rim
    for k in (-0.66, -0.33, 0.0, 0.33, 0.66):
        ew = r * math.sqrt(max(0.0, 1 - k * k))
        draw.ellipse([cx - ew, cy - r, cx + ew, cy + r], outline=(255, 255, 255), width=2)
    for k in (-0.6, -0.3, 0.0, 0.3, 0.6):
        yy = cy + k * r
        half = r * math.sqrt(max(0.0, 1 - k * k))
        draw.line([(cx - half, yy), (cx + half, yy)], fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    # Antalya coast waves under the globe
    for row in range(2):
        wy = cy + r + 22 + row * 18
        pts = []
        for x in range(cx - r, cx + r + 1, 8):
            pts.append((x, wy + 6 * math.sin((x - cx) / 26.0 + row)))
        draw.line(pts, fill=OCEAN, width=4)


def draw_f1_visual(draw, x, y, w, h):
    """Night skyline, neon strip and a chequered flag bar."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline silhouettes
    buildings = [(0.04, 0.55), (0.16, 0.75), (0.30, 0.45), (0.44, 0.68),
                 (0.58, 0.52), (0.70, 0.80), (0.84, 0.60)]
    for fx, fh in buildings:
        bx, bw = x + fx * w, 0.11 * w
        by = y + h - 40 - fh * (h - 54)
        draw.rectangle([bx, by, bx + bw, y + h - 40], fill=(8, 10, 26))
        for wy in range(int(by) + 8, int(y + h - 48), 14):
            draw.rectangle([bx + 5, wy, bx + 11, wy + 6], fill=GOLD)
    # neon strip
    draw.line([(x + 8, y + h - 34), (x + w - 8, y + h - 34)], fill=(255, 64, 160), width=4)
    # chequered bar, two rows
    sq, cols = 13, int(w // 13)
    for j in range(2):
        for i in range(cols):
            c = (245, 245, 245) if (i + j) % 2 == 0 else (20, 20, 20)
            draw.rectangle([x + i * sq, y + h - 26 + j * 13, x + (i + 1) * sq, y + h - 13 + j * 13], fill=c)


def draw_quake_visual(draw, x, y, w, h):
    """Seismograph trace with a spike, and the magnitude."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 233, 219), outline=MUTED, width=2)
    mid = y + h * 0.62
    pts, n = [], 60
    for i in range(n + 1):
        t = i / n
        amp = 3
        if 0.38 < t < 0.62:
            amp = 3 + 34 * math.sin((t - 0.38) / 0.24 * math.pi)
        pts.append((x + 10 + t * (w - 20), mid + amp * math.sin(t * 90)))
    draw.line(pts, fill=BRICK, width=3)
    f = font(SERIF_B, 44)
    draw.text((x + 14, y + 10), "M4.1", font=f, fill=INK)


def draw_flag_visual(draw, x, y, w, h):
    """A flagpole with the flag flown at half-mast."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 233, 219), outline=MUTED, width=2)
    px = x + w * 0.32
    draw.line([(px, y + 12), (px, y + h - 14)], fill=INK, width=5)
    draw.ellipse([px - 6, y + 4, px + 6, y + 16], fill=GOLD, outline=INK, width=2)
    # flag at half-mast: green, gold, black bands with a red accent
    fy = y + h * 0.34
    fw, fh = w * 0.44, h * 0.30
    draw.rectangle([px, fy, px + fw, fy + fh / 3], fill=(0, 122, 61))
    draw.rectangle([px, fy + fh / 3, px + fw, fy + 2 * fh / 3], fill=GOLD)
    draw.rectangle([px, fy + 2 * fh / 3, px + fw, fy + fh], fill=(20, 20, 20))
    draw.polygon([(px, fy), (px + fw * 0.4, fy + fh / 2), (px, fy + fh)], fill=BRICK)
    draw.line([(px - 26, y + h - 14), (px + 26, y + h - 14)], fill=INK, width=5)


def tile(draw, x, y, w, h, header, header_fill, visual, label, sub):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 38], fill=header_fill)
    hf = font(SANS_B, 21)
    centered(draw, x + w / 2, y + 8, header, hf, fill=(255, 255, 255))
    visual(draw, x + 12, y + 50, w - 24, 104)
    lf = font(SERIF_B, 23)
    ly = y + 164
    for line in wrap(draw, label, lf, w - 24):
        centered(draw, x + w / 2, ly, line, lf)
        ly += 28
    sf = font(SANS, 18)
    for line in wrap(draw, sub, sf, w - 28):
        centered(draw, x + w / 2, ly + 3, line, sf, fill=MUTED)
        ly += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 48  # margin
    cx = W / 2

    # --- masthead -----------------------------------------------------------
    d.line([(M, 36), (W - M, 36)], fill=INK, width=2)
    small = font(SANS_B, 19)
    d.text((M, 46), "SUNDAY EDITION", font=small, fill=MUTED)
    right = "WORLD NEWS IN ONE PAGE"
    d.text((W - M - text_w(d, right, small), 46), right, font=small, fill=MUTED)
    centered(d, cx, 72, "THE WORLD TODAY", font(SERIF_B, 76))
    centered(d, cx, 162, "Sunday, 22 November 2026", font(SERIF_B, 36), fill=BRICK)
    d.line([(M, 216), (W - M, 216)], fill=INK, width=4)
    d.line([(M, 224), (W - M, 224)], fill=INK, width=1)

    # --- lead story: COP31 ---------------------------------------------------
    kicker = font(SANS_B, 24)
    d.text((M, 244), "CLIMATE SUMMIT  ·  ANTALYA, TÜRKIYE", font=kicker, fill=TEAL)
    head = font(SERIF_B, 43)
    hy = 280
    for line in ["COP31 climate talks reach", "final deal text in Antalya"]:
        d.text((M, hy), line, font=head, fill=INK)
        hy += 52
    deck = font(SANS, 24)
    deck_text = ("Negotiators ran past Friday's deadline through Saturday into "
                 "early Sunday. Delegations had until 0300 GMT to object; an "
                 "approval session was set for 0600 GMT.")
    dy = hy + 10
    for line in wrap(d, deck_text, deck, 520):
        d.text((M, dy), line, font=deck, fill=(50, 46, 38))
        dy += 32
    note = font(SANS, 20)
    d.text((M, dy + 8), "The climate summit's closing text, as reported early Sunday.",
           font=note, fill=MUTED)
    draw_globe(d, 822, 468, 92)
    cap = font(SANS, 19)
    centered(d, 822, 610, "COP31 · Antalya coast", cap, fill=MUTED)

    d.line([(M, 638), (W - M, 638)], fill=INK, width=2)

    # --- three tiles ---------------------------------------------------------
    tw, th, ty = 296, 326, 648
    gap = (W - 2 * M - 3 * tw) / 2
    tile(d, M, ty, tw, th, "FORMULA 1 · LAS VEGAS", NAVY, draw_f1_visual,
         "Formula 1 races under the Las Vegas lights",
         "Sunday night race on the Strip circuit")
    tile(d, M + tw + gap, ty, tw, th, "MYANMAR", BRICK, draw_quake_visual,
         "M4.1 quake strikes Myanmar before dawn",
         "02:35 IST · 95 km deep · no casualties reported")
    tile(d, M + 2 * (tw + gap), ty, tw, th, "SOUTH AFRICA", TEAL, draw_flag_visual,
         "South Africa lowers flags for Phumzile Mlambo-Ngcuka",
         "First woman deputy president · died 20 Nov, aged 71 · state funeral 28 Nov")

    # --- footer --------------------------------------------------------------
    d.line([(M, 984), (W - M, 984)], fill=INK, width=2)
    centered(d, cx, 990, "The world on Sunday, 22 November 2026", font(SERIF, 20), fill=MUTED)

    img.save("entry.png", "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
