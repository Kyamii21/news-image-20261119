"""Renderer v3 untuk entry news-image-20261119.

Menggambar satu halaman depan 1024x1024: masthead navy, panel lead
KTT trilateral Shenzhen, enam kartu cerita dengan blok ikon warna
penuh, dan strip ticker tiga kabar tambahan hari yang sama.
Semua bentuk digambar tebal supaya tetap terbaca di lebar 300px.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (251, 247, 238)
NAVY = (15, 42, 82)
RED = (196, 30, 42)
INK = (18, 18, 18)
CHAR = (45, 45, 45)
WHITE = (255, 255, 255)
GOLD = (232, 168, 32)

BLACK = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Black.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, text, f):
    box = d.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def draw_star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=3)
    stripe = h / 7
    for i in range(0, 7, 2):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=RED)
    d.rectangle([x, y, x + w * 0.42, y + stripe * 4], fill=NAVY)
    for r in range(3):
        for c in range(4):
            cx = x + 8 + c * (w * 0.42 - 12) / 3
            cy = y + 8 + r * (stripe * 4 - 14) / 2
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=WHITE)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=3)
    draw_star(d, x + w * 0.22, y + h * 0.30, 11, GOLD)
    for dx, dy in [(0.42, 0.12), (0.48, 0.30), (0.48, 0.50), (0.42, 0.66)]:
        draw_star(d, x + w * dx, y + h * dy, 5, GOLD)


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=3)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))


def skyline(d, x, y_base, w):
    heights = [70, 120, 90, 150, 100, 135, 80, 115, 95]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        d.rectangle([x + i * bw + 2, y_base - hh, x + (i + 1) * bw - 2, y_base],
                    fill=(70, 95, 140))


def icon_scales(d, x, y, s):
    cx = x + s / 2
    d.line([cx, y + 18, cx, y + s - 26], fill=WHITE, width=9)
    d.line([x + 16, y + 30, x + s - 16, y + 30], fill=WHITE, width=9)
    d.ellipse([cx - 9, y + 8, cx + 9, y + 26], fill=GOLD)
    for px in (x + 16, x + s - 16):
        d.line([px, y + 30, px - 14, y + 62], fill=WHITE, width=6)
        d.line([px, y + 30, px + 14, y + 62], fill=WHITE, width=6)
        d.pieslice([px - 20, y + 50, px + 20, y + 84], 0, 180, fill=GOLD)
    d.rectangle([cx - 26, y + s - 26, cx + 26, y + s - 16], fill=WHITE)


def icon_bridge(d, x, y, s):
    deck_y = y + s - 36
    for tx in (x + 28, x + s - 28):
        d.line([tx, y + 16, tx, deck_y], fill=WHITE, width=11)
    d.arc([x + 28, y + 16, x + s - 28, y + 96], 0, 180, fill=WHITE, width=7)
    for fx in (0.30, 0.42, 0.58, 0.70):
        px = x + s * fx
        d.line([px, y + 40, px, deck_y], fill=WHITE, width=5)
    d.line([x + 10, deck_y, x + s - 10, deck_y], fill=WHITE, width=11)
    draw_star(d, x + s / 2, deck_y - 14, 23, (255, 140, 0))
    draw_star(d, x + s / 2, deck_y - 14, 12, (255, 220, 60))
    d.line([x + 10, y + s - 14, x + s - 10, y + s - 14], fill=(120, 200, 255), width=7)


def icon_rocket(d, x, y, s):
    cx = x + s / 2 - 8
    d.polygon([(cx, y + 12), (cx + 26, y + 58), (cx + 16, y + 88),
               (cx - 16, y + 88), (cx - 26, y + 58)], fill=WHITE)
    d.ellipse([cx - 9, y + 44, cx + 9, y + 62], fill=RED)
    d.polygon([(cx - 16, y + 88), (cx + 16, y + 88), (cx, y + 112)], fill=GOLD)
    d.line([x + 14, y + s - 16, x + s - 22, y + 26], fill=(90, 230, 140), width=9)
    d.polygon([(x + s - 22, y + 18), (x + s - 40, y + 22), (x + s - 26, y + 40)],
              fill=(90, 230, 140))


def icon_globe(d, x, y, s):
    cx, cy, r = x + s / 2 - 10, y + s / 2, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 150, 235), outline=WHITE, width=5)
    for bx, by, br in [(-18, -14, 14), (12, -22, 11), (-6, 12, 16), (20, 14, 10)]:
        d.ellipse([cx + bx - br, cy + by - br, cx + bx + br, cy + by + br],
                  fill=(70, 200, 110))
    tx = x + s - 26
    d.rounded_rectangle([tx, y + 24, tx + 16, y + s - 30], 8, fill=WHITE)
    d.rectangle([tx + 4, y + 52, tx + 12, y + s - 34], fill=RED)
    d.ellipse([tx - 3, y + s - 36, tx + 19, y + s - 14], fill=RED, outline=WHITE, width=3)


def icon_pad(d, x, y, s):
    d.rounded_rectangle([x + 8, y + 30, x + s - 8, y + s - 26], 26, fill=WHITE)
    d.rectangle([x + 30, y + 56, x + 40, y + 88], fill=INK)
    d.rectangle([x + 20, y + 66, x + 50, y + 78], fill=INK)
    for dx, dy, col in [(82, 56, RED), (98, 70, GOLD), (82, 84, (50, 140, 230)),
                        (66, 70, (60, 190, 100))]:
        d.ellipse([x + dx - 8, y + dy - 8, x + dx + 8, y + dy + 8], fill=col)
    d.arc([x + 30, y + 2, x + 62, y + 34], 200, 340, fill=WHITE, width=7)
    d.arc([x + 62, y + 2, x + 94, y + 34], 200, 340, fill=WHITE, width=7)


def icon_probe(d, x, y, s):
    cx, cy = x + 52, y + 44
    d.pieslice([cx - 34, cy - 34, cx + 34, cy + 34], 200, 340, fill=WHITE)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    d.line([cx, cy, cx + 26, cy + 30], fill=WHITE, width=8)
    d.rectangle([cx + 18, cy + 26, cx + 50, cy + 50], fill=GOLD)
    d.line([cx + 50, cy + 50, cx + 78, cy + 76], fill=WHITE, width=8)
    for px, py in [(x + 14, y + 16), (x + s - 18, y + 20), (x + 16, y + s - 18)]:
        d.line([px - 7, py, px + 7, py], fill=GOLD, width=5)
        d.line([px, py - 7, px, py + 7], fill=GOLD, width=5)


CARDS = [
    ((27, 58, 110), icon_scales, "ICJ: MYANMAR", "GENOCIDE RULING", "First verdict of its kind"),
    ((170, 30, 45), icon_bridge, "UKRAINE HITS", "CRIMEA BRIDGE", "Third strike this week"),
    ((0, 120, 110), icon_rocket, "ANTHROPIC IPO", "$81.3 BILLION", "Biggest ever · $83/share"),
    ((20, 130, 60), icon_globe, "COP31 CLIMATE", "TALKS STALL", "No phaseout deal yet"),
    ((110, 40, 160), icon_pad, "GTA VI LAUNCH", "GOES GLOBAL", "Rollout starts in NZ"),
    ((20, 40, 90), icon_probe, "VOYAGER 1", "1 LIGHT-DAY AWAY", "16 billion miles out"),
]


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # Masthead band
    d.rectangle([0, 0, W, 118], fill=NAVY)
    f_mast = font(BLACK, 58)
    d.text((36, 26), "THE WORLD TODAY", font=f_mast, fill=WHITE)
    f_badge = font(BOLD, 34)
    bw = tw(d, "19 NOV 2026", f_badge) + 44
    d.rounded_rectangle([W - 36 - bw, 28, W - 36, 90], 14, fill=RED)
    d.text((W - 36 - bw + 22, 40), "19 NOV 2026", font=f_badge, fill=WHITE)

    # Date line
    f_date = font(BLACK, 56)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - tw(d, date, f_date)) / 2, 134), date, font=f_date, fill=NAVY)
    f_sub = font(REG, 30)
    sub = "The day in ten stories"
    d.text(((W - tw(d, sub, f_sub)) / 2, 202), sub, font=f_sub, fill=CHAR)
    d.rectangle([36, 246, W - 36, 252], fill=RED)
    d.rectangle([36, 258, W - 36, 262], fill=NAVY)

    # Lead panel
    d.rounded_rectangle([36, 282, W - 36, 558], 22, fill=WHITE, outline=INK, width=4)
    fx, fy, fw, fh = 66, 308, 118, 74
    for i, fn in enumerate((flag_us, flag_cn, flag_ru)):
        x = fx + i * (fw + 16)
        d.line([x, fy - 8, x, fy + 146], fill=INK, width=6)
        fn(d, x + 4, fy, fw, fh)
    skyline(d, 60, 500, 400)
    f_cap = font(BOLD, 29)
    d.text((66, 508), "SHENZHEN · APEC", font=f_cap, fill=NAVY)
    tx = 500
    d.text((tx, 302), "LEAD STORY", font=font(BOLD, 29), fill=RED)
    f_lead = font(BLACK, 42)
    d.text((tx, 336), "TRUMP · XI · PUTIN", font=f_lead, fill=INK)
    d.text((tx, 384), "FIRST 3-WAY SUMMIT", font=f_lead, fill=INK)
    f_leadsub = font(REG, 29)
    d.text((tx, 440), "Joint call: cut nuclear risk,", font=f_leadsub, fill=CHAR)
    d.text((tx, 474), "keep energy flowing", font=f_leadsub, fill=CHAR)
    d.ellipse([tx, 514, tx + 22, 536], fill=NAVY)
    d.ellipse([tx + 16, 514, tx + 38, 536], fill=RED)
    d.text((tx + 48, 512), "First-ever trilateral", font=font(BOLD, 25), fill=NAVY)

    # Story grid
    gx, gy = 36, 576
    cw, ch, gap = 464, 112, 13
    f_head = font(BLACK, 32)
    f_line = font(REG, 25)
    for i, (color, icon, l1, l2, line) in enumerate(CARDS):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], 16, fill=WHITE,
                            outline=INK, width=3)
        d.rounded_rectangle([cx + 9, cy + 9, cx + 121, cy + ch - 9], 12, fill=color)
        icon(d, cx + 9, cy + 9, 112)
        d.text((cx + 136, cy + 8), l1, font=f_head, fill=INK)
        d.text((cx + 136, cy + 43), l2, font=f_head, fill=INK)
        d.text((cx + 136, cy + 78), line, font=f_line, fill=CHAR)

    # Ticker strip
    ty = gy + 3 * (ch + gap) + 2
    d.rounded_rectangle([36, ty, W - 36, ty + 58], 14, fill=NAVY)
    f_tick = font(BOLD, 25)
    tick = "ALSO: HORMUZ THREAT · VAN GOGH $190M · S&P DOWN 5TH DAY"
    d.text(((W - tw(d, tick, f_tick)) / 2, ty + 15), tick, font=f_tick, fill=WHITE)

    img.save("entry.png", optimize=True)
    img.resize((300, 300), Image.LANCZOS).save("preview-300.png")


if __name__ == "__main__":
    build()
