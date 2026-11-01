"""Instagram profil resmi (1080x1080) - Tarih Hoca maskotu."""
import math, cairo
from engine import draw as D

S = 1080

def burst(ctx):
    ctx.rectangle(0, 0, S, S); ctx.set_source_rgb(1.0, 0.93, 0.62); ctx.fill()
    cx, cy = S / 2, S * 0.42
    for i in range(20):
        a1 = 0.1 + i * 2 * math.pi / 20; a2 = a1 + math.pi / 20
        ctx.move_to(cx, cy)
        ctx.line_to(cx + math.cos(a1) * 1200, cy + math.sin(a1) * 1200)
        ctx.line_to(cx + math.cos(a2) * 1200, cy + math.sin(a2) * 1200)
        ctx.close_path(); ctx.set_source_rgb(1.0, 0.84, 0.30); ctx.fill()

def ribbon(ctx, text, y):
    D.set_font(ctx, D.TITLE_FONT, 92)
    t = D.tr_upper(text); tw = D.text_width(ctx, t)
    w, h = tw + 90, 120; x0 = S / 2 - w / 2
    for side in (-1, 1):  # katlanmış uçlar
        ex = x0 - 40 if side < 0 else x0 + w + 40
        bx = x0 + 20 if side < 0 else x0 + w - 20
        ctx.move_to(bx, y + 25); ctx.line_to(ex, y + 25); ctx.line_to(ex + side * -30 * -1 * 0 + (25 if side < 0 else -25), y + 25 + h / 2)
        ctx.line_to(ex, y + 25 + h); ctx.line_to(bx, y + 25 + h); ctx.close_path()
        D.stroke_fill(ctx, (0.62, 0.18, 0.13), D.INK_DAY, 8)
    ctx.rectangle(x0, y, w, h)
    D.stroke_fill(ctx, D.RED, D.INK_DAY, 9)
    D.outlined_text(ctx, text, S / 2, y + h / 2 + 2, D.TITLE_FONT, 92, (1, 1, 1), D.INK_DAY, outline=12)

def make(path, with_text):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
    ctx = cairo.Context(surf)
    burst(ctx)
    pose = D.NARRATOR_POSES["wave"]
    scale = 3.2 if with_text else 3.5
    head_y = 400 if with_text else 450
    y = head_y + (D.N_ULEG + D.N_LLEG + D.N_TORSO + D.N_HEAD - 6) * D.GLOBAL_SCALE * scale
    j = D.draw_narrator(ctx, S / 2 - 30, y, scale, pose, "wink", 0.5, False, "none", 1.0, 1.0)
    ex, ey = j["eye_l"]
    D.draw_sparkle(ctx, ex - j["head_r"] * 0.95, ey - j["head_r"] * 0.55, 85, 0.15)
    if with_text:
        ribbon(ctx, "Çöp Adamla Tarih", 790)
    surf.write_to_png(path)

make("output/profil_resmi_A.png", False)
make("output/profil_resmi_B_yazili.png", True)
