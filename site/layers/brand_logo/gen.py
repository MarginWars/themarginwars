#!/usr/bin/env python3
"""LinkedIn company-page assets for The Margin Wars (soft launch, assets only).

Adapts logo option C, 'Ledger margin' (logo_1104).

The logo mark (v1) keeps the six-colour stacked rule on a dark ink field.
The pink ledger rule (#B5237F) is used on the cover wordmark and the
Substack wordmark, not on the logo. Does not post or touch LinkedIn.

Band order (approved cycle): sky, violet, mint, grey, gold, coral.
C structure: ledger-rule + M mark (the rule + M reads as 'IM' at small size),
stacked 'The Margin / Wars' wordmark, mono 'bp' tag.
"""
from __future__ import annotations

import math
import os
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = Path(__file__).resolve().parent
BAND = ["#8FB0E0", "#A08FE6", "#3FBF85", "#B7C1C9", "#D2A63A", "#EA6259"]
INK = "#111417"
PAPER = "#F4F6F7"
WHITE = "#FFFFFF"
PINK = "#B5237F"  # ledger rule on the cover and Substack wordmark; not on the logo
MUTED = "#5B656B"  # original lockup sub colour (light)
RULE = "#C2CBD0"
LI_GREY = "#F3F2EF"  # LinkedIn page chrome, for mocks only
SG_BOLD = "@MW_FONTS@/SchibstedGrotesk-Bold.ttf"
SG_REG = "@MW_FONTS@/SchibstedGrotesk-Regular.ttf"
MM_VAR = "@MW_FONTS@/MartianMono-VariableFont_wdth,wght.ttf"

# Instantiate Martian Mono SemiBold (wght 600, wdth 100) once, as in logo_1104/gen.py.
_MM_PATH = None


def mm_path() -> str:
    global _MM_PATH
    if _MM_PATH is None:
        inst = instantiateVariableFont(TTFont(MM_VAR), {"wght": 600, "wdth": 100})
        fd, _MM_PATH = tempfile.mkstemp(suffix=".ttf")
        os.close(fd)
        inst.save(_MM_PATH)
    return _MM_PATH


def font(path: str, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def hx(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def new(w: int, h: int, color: str) -> Image.Image:
    return Image.new("RGB", (w, h), hx(color))


def down(im: Image.Image, w: int, h: int) -> Image.Image:
    return im.resize((w, h), Image.Resampling.LANCZOS)


def down_logo(im: Image.Image, w: int, h: int) -> Image.Image:
    """Box-filter downsample, then clamp any remaining light overshoot to paper.

    Lanczos ringing on the dark field produced a faint white fringe around the M.
    The mark itself is unchanged: six-colour rule, paper M, ink field.
    """
    import numpy as np
    out = im.resize((w, h), Image.Resampling.BOX)
    arr = np.array(out)
    paper = np.array([0xF4, 0xF6, 0xF7], dtype=np.int16)
    sat = arr.max(axis=2) - arr.min(axis=2)
    lum = arr.astype(np.int16).sum(axis=2) // 3
    mask = (lum >= 200) & (sat <= 40)
    for i in range(3):
        ch = arr[:, :, i]
        over = mask & (ch > int(paper[i]))
        ch = ch.copy()
        ch[over] = int(paper[i])
        arr[:, :, i] = ch
    return Image.fromarray(arr)


def draw_band_h(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float) -> None:
    """Horizontal six-colour strip, left-to-right in cycle order."""
    seg = w / 6.0
    for i, col in enumerate(BAND):
        x0 = x + i * seg
        x1 = x + w if i == 5 else x + (i + 1) * seg
        draw.rectangle([round(x0), round(y), round(x1) - (0 if i == 5 else 1), round(y + h) - 1], fill=hx(col))
    # Use inclusive fill without 1px gaps: redraw with floor/ceil adjacency
    x0 = x
    for i, col in enumerate(BAND):
        x1 = x + w if i == 5 else x + (i + 1) * seg
        draw.rectangle([int(round(x0)), int(round(y)), int(round(x1)) - 1, int(round(y + h)) - 1], fill=hx(col))
        x0 = x1


def draw_band_v(draw: ImageDraw.ImageDraw, x: float, y: float, w: float, h: float) -> None:
    """Vertical six-colour ledger rule, top-to-bottom in cycle order."""
    y0 = y
    seg = h / 6.0
    for i, col in enumerate(BAND):
        y1 = y + h if i == 5 else y + (i + 1) * seg
        draw.rectangle([int(round(x)), int(round(y0)), int(round(x + w)) - 1, int(round(y1)) - 1], fill=hx(col))
        y0 = y1


def circle_crop(im: Image.Image, size: int | None = None) -> Image.Image:
    if size is None:
        size = im.width
    im = down(im, size, size) if im.size != (size, size) else im
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im.convert("RGBA"), mask=mask)
    return out


# ---------------------------------------------------------------------------
# 400x400 mark: ink field, banded ledger rule, paper M. Built for circle crop.
# ---------------------------------------------------------------------------
def render_mark(scale: int = 8) -> Image.Image:
    S = 400 * scale
    im = new(S, S, INK)
    d = ImageDraw.Draw(im)
    cx = cy = S / 2
    # Safe area inside the circle: keep content within ~78% of the radius
    # so a 60px circle crop still has padding and nothing clips.
    r = S * 0.50
    safe = r * 0.78
    # Rule + M as a unit, optically centered in the circle.
    # Rule thickness ~10% of the square (reads at 60px); height ~58% of square.
    rule_w = S * 0.095
    rule_h = S * 0.58
    gap = S * 0.035
    m_size = S * 0.46
    mfont = font(SG_BOLD, m_size)
    mb = mfont.getbbox("M")
    m_w = mb[2] - mb[0]
    m_h = mb[3] - mb[1]
    # Total content width and height
    total_w = rule_w + gap + m_w
    # Vertical: align the M cap-height block with the rule, slight optical sink
    rule_x = cx - total_w / 2
    # M visual centre slightly above geometric centre (heavy baseline)
    block_cy = cy - S * 0.01
    rule_y = block_cy - rule_h / 2
    draw_band_v(d, rule_x, rule_y, rule_w, rule_h)
    # Place M: left after the rule, baseline so glyph bbox is vertically centred on the rule
    mx = rule_x + rule_w + gap - mb[0]
    my = block_cy - (mb[1] + mb[3]) / 2
    d.text((mx, my), "M", font=mfont, fill=hx(PAPER))
    return down_logo(im, 400, 400)


# ---------------------------------------------------------------------------
# C lockup (light): stacked wordmark, banded ledger rule, muted mono 'bp'
# Returns (image, width, height) at the requested typographic size.
# ---------------------------------------------------------------------------
def render_lockup(word_px: float, scale: int = 4, bg: str | None = PAPER, fg: str = INK, bp_fill: str = MUTED, rule_fill: str = PINK):
    """Draw the C lockup into a tight RGB (or RGBA if bg is None) image.

    Returns (image, text_x) where text_x is the left edge of the wordmark, in image pixels.
    Construction follows logo_1104 option C: stacked 'The Margin' / 'Wars' against a
    ledger rule, with a mono 'bp' tag on the Wars baseline. The rule is solid pink
    (#B5237F) by default (cover and Substack wordmark). Pass rule_fill="band" only
    if a six-colour rule is required; the logo mark does not use this lockup.
    """
    s = scale
    f_word = font(SG_BOLD, word_px * s)
    f_bp = font(mm_path(), word_px * 0.50 * s)
    # Ink boxes relative to a left-baseline origin.
    t_box = f_word.getbbox("The Margin", anchor="ls")
    w_box = f_word.getbbox("Wars", anchor="ls")
    bp_box = f_bp.getbbox("bp", anchor="ls")
    # Original C lockup (logo_1104): 24px type, baselines at 26 and 54, so 28/24 = 1.1667 em.
    pad_y = word_px * (4 / 24) * s
    base1 = pad_y + word_px * (22 / 24) * s   # 26/24 em from the top of the 62-unit frame, scaled
    base2 = base1 + word_px * (28 / 24) * s
    # Rule spans a little above first cap to a little below second baseline
    content_top = base1 + t_box[1]
    content_bot = base2 + max(w_box[3], bp_box[3])
    rule_w = max(3 * s, word_px * 0.18 * s)
    rule_h = (content_bot - content_top) + pad_y * 0.2
    rule_y = content_top - pad_y * 0.1
    gap = word_px * 0.42 * s
    text_x = rule_w + gap
    wars_w = w_box[2] - w_box[0]
    bp_gap = word_px * 0.38 * s
    bp_x = text_x + wars_w + bp_gap
    margin_right = text_x + (t_box[2] - t_box[0])
    bp_right = bp_x + (bp_box[2] - bp_box[0])
    width = int(math.ceil(max(margin_right, bp_right) + pad_y))
    height = int(math.ceil(content_bot + pad_y))
    if bg is None:
        im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    else:
        im = new(width, height, bg)
    d = ImageDraw.Draw(im)
    if rule_fill == "band":
        draw_band_v(d, 0, rule_y, rule_w, rule_h)
    else:
        d.rectangle(
            [0, int(round(rule_y)), int(round(rule_w)) - 1, int(round(rule_y + rule_h)) - 1],
            fill=hx(rule_fill),
        )
    d.text((text_x, base1), "The Margin", font=f_word, fill=hx(fg), anchor="ls")
    d.text((text_x, base2), "Wars", font=f_word, fill=hx(fg), anchor="ls")
    d.text((bp_x, base2), "bp", font=f_bp, fill=hx(bp_fill), anchor="ls")
    return im, int(round(text_x))



def render_cover() -> Image.Image:
    W, H = 1128, 191
    scale = 4
    im = new(W * scale, H * scale, PAPER)
    d = ImageDraw.Draw(im)
    # Signature band along the top, slightly stronger than the site's 6px so it
    # holds on this short ribbon (8px at target).
    band_h = 8 * scale
    draw_band_h(d, 0, 0, W * scale, band_h)
    # Wordmark + tagline in the clear zone to the right of the logo overlap.
    # Logo overlap (desktop): ~160px circle, left ~24px, half on the cover.
    # Keep x < 280 and the bottom-left quadrant free of type.
    lock, text_x = render_lockup(word_px=52, scale=scale, bg=None, fg=INK, bp_fill=MUTED)
    # Tagline
    tag = "Payments tactics from the front lines."
    f_tag = font(mm_path(), 15 * scale)
    tb = f_tag.getbbox(tag)
    tag_w = tb[2] - tb[0]
    tag_h = tb[3] - tb[1]
    gap = 12 * scale
    block_h = lock.height + gap + tag_h
    # Vertical centre in the area below the band, with a hair more weight above
    avail_top = band_h
    avail_h = H * scale - band_h
    block_y = avail_top + (avail_h - block_h) / 2 - 2 * scale
    # Horizontal: start well clear of the logo, but not so far right that a
    # centre-weighted mobile crop loses the wordmark. 1128*0.28 = 316.
    lock_x = int(312 * scale)
    lock_y = int(block_y)
    im.paste(lock, (lock_x, lock_y), lock)
    # Tagline under the wordmark, flush with the left edge of 'The Margin'.
    tag_x = lock_x + text_x
    tag_y = lock_y + lock.height + gap - tb[1]
    d.text((tag_x, tag_y), tag, font=f_tag, fill=hx("#4A555B"))
    return down(im, W, H)


def render_cover_with_guides(cover: Image.Image) -> Image.Image:
    """QA overlay: logo overlap (desktop + mobile) and side crops."""
    im = cover.convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # Desktop logo: 160px circle, left 24, half-overlapping the cover bottom.
    logo_s, logo_l, overlap = 160, 24, 80
    # Occupied rect on the cover
    d.rectangle([0, 191 - overlap, logo_l + logo_s + 16, 191], fill=(234, 98, 89, 70))
    # Circle where the logo will sit (partly below the cover)
    # only the part on the cover
    cx, cy = logo_l + logo_s / 2, 191 - overlap + logo_s / 2
    # cy = 191 - 80 + 80 = 191, i.e. centre on the bottom edge
    d.ellipse([logo_l, 191 - overlap, logo_l + logo_s, 191 - overlap + logo_s], outline=(234, 98, 89, 220), width=2)
    # Mobile: cover scaled to ~390 wide (scale 390/1128), logo ~72, left ~12 in that frame.
    # Map back to 1128 space: left = 12 * 1128/390 ≈ 35, size = 72*1128/390 ≈ 208? Wait.
    # Better: show the mobile *visible* crop of the cover (full width scaled, no side crop)
    # and a tighter left overlap of ~72 * (1128/390) ≈ 208 px wide in source? That's wrong
    # for a "keep clear" zone: on mobile the whole cover is shown (same aspect), just smaller.
    # So the mobile logo occupies left 24*(390/390) ... actually both see the full 1128x191
    # image, just at different CSS sizes. The reserved zone is still the bottom-left
    # of the image. Desktop is the stricter pixel reservation (160/1128).
    # Some clients centre-crop height or sides. Mark a 5% side inset.
    d.rectangle([0, 0, int(1128 * 0.04), 191], fill=(17, 20, 23, 30))
    d.rectangle([int(1128 * 0.96), 0, 1128, 191], fill=(17, 20, 23, 30))
    out = Image.alpha_composite(im, ov)
    return out.convert("RGB")


def render_desktop_mock(cover: Image.Image, logo: Image.Image) -> Image.Image:
    """Cover + circular logo overlapping bottom-left, plus a name row."""
    pad_x, top = 36, 24
    name_row = 120
    W = 1128 + pad_x * 2
    H = top + 191 + name_row + 24
    im = new(W, H, LI_GREY)
    # White card
    card = Image.new("RGB", (1128, 191 + name_row), hx(WHITE))
    im.paste(card, (pad_x, top))
    im.paste(cover, (pad_x, top))
    # Hairline under cover
    d = ImageDraw.Draw(im)
    # Logo
    logo_s, logo_l, overlap = 160, 24, 80
    badge = circle_crop(logo, logo_s)
    lx = pad_x + logo_l
    ly = top + 191 - overlap
    im.paste(badge, (lx, ly), badge)
    # Name and tagline to the right of the logo, in the white row
    f_name = font(SG_BOLD, 28)
    f_sub = font(mm_path(), 13)
    name = "The Margin Wars"
    sub = "Payments tactics from the front lines."
    nx = lx + logo_s + 20
    ny = top + 191 + 22
    d.text((nx, ny), name, font=f_name, fill=hx(INK))
    nb = f_name.getbbox(name)
    d.text((nx, ny + (nb[3] - nb[1]) + 10), sub, font=f_sub, fill=hx(MUTED))
    return im


def render_mobile_mock(cover: Image.Image, logo: Image.Image) -> Image.Image:
    """Phone-width LinkedIn-style crop: full cover scaled to 390, short ribbon, logo overlap."""
    mw = 390
    ch = round(191 * mw / 1128)  # ~66
    pad = 16
    name_row = 88
    W = mw + pad * 2
    H = 20 + ch + name_row + 20
    im = new(W, H, LI_GREY)
    card_h = ch + name_row
    card = Image.new("RGB", (mw, card_h), hx(WHITE))
    im.paste(card, (pad, 20))
    cov = down(cover, mw, ch)
    im.paste(cov, (pad, 20))
    logo_s, logo_l, overlap = 72, 12, 36
    badge = circle_crop(logo, logo_s)
    lx = pad + logo_l
    ly = 20 + ch - overlap
    im.paste(badge, (lx, ly), badge)
    d = ImageDraw.Draw(im)
    f_name = font(SG_BOLD, 18)
    f_sub = font(mm_path(), 9)
    nx = lx + logo_s + 12
    ny = 20 + ch + 14
    d.text((nx, ny), "The Margin Wars", font=f_name, fill=hx(INK))
    nb = f_name.getbbox("The Margin Wars")
    d.text((nx, ny + (nb[3] - nb[1]) + 6), "Payments tactics from the front lines.", font=f_sub, fill=hx(MUTED))
    return im


def render_qa_sheet(logo, logo60, cover, guides, desk, mobile) -> Image.Image:
    """Contact sheet for visual QA."""
    W, H = 1400, 1500
    im = new(W, H, "#E7EAEC")
    d = ImageDraw.Draw(im)
    f_h = font(SG_BOLD, 28)
    f_l = font(SG_REG, 15)
    f_m = font(mm_path(), 11)
    y = 36
    d.text((40, y), "The Margin Wars — LinkedIn assets QA", font=f_h, fill=hx(INK))
    y = 76
    d.text((40, y), "Logo C Ledger margin  ·  band sky / violet / mint / grey / gold / coral  ·  10 Nov 2026", font=f_m, fill=hx(MUTED))
    y = 110

    def label(x, y, text):
        d.text((x, y), text, font=f_l, fill=hx(MUTED))

    # Logo 400 on paper and on grey
    label(40, y, "logo_400.png on paper")
    label(480, y, "logo_400 circle-cropped (as LinkedIn)")
    label(900, y, "logo_60.png  and  60px circle")
    y += 26
    im.paste(logo, (40, y))
    # paper mat
    # already paper? logo is ink square. Put a paper plate behind circle.
    plate = new(400, 400, PAPER)
    im.paste(plate, (40, y))
    im.paste(logo, (40, y))
    plate2 = new(400, 400, WHITE)
    im.paste(plate2, (480, y))
    c400 = circle_crop(logo, 400)
    im.paste(c400, (480, y), c400)
    # 60px on a checker / paper / cover sliver
    plate3 = new(200, 400, PAPER)
    im.paste(plate3, (900, y))
    # 60 square
    im.paste(logo60, (920, y + 40))
    c60 = circle_crop(logo, 60)
    im.paste(c60, (1000, y + 40), c60)
    # also 60 on a dark and on the cover colour, and a 160 (desktop size)
    d.text((920, y + 40 + 70), "60 sq", font=f_m, fill=hx(MUTED))
    d.text((1000, y + 40 + 70), "60 circle", font=f_m, fill=hx(MUTED))
    c160 = circle_crop(logo, 160)
    im.paste(c160, (920, y + 140), c160)
    d.text((920, y + 140 + 168), "160 circle (desktop size)", font=f_m, fill=hx(MUTED))
    y += 420

    label(40, y, "cover_1128x191.png")
    label(40 + 1128 + 20, y, "cover with logo-overlap guide")
    y += 24
    # scale covers if needed - they are 1128, sheet is 1400, so stack
    im.paste(cover, (40, y))
    y += 191 + 16
    label(40, y, "cover + reserved bottom-left (coral tint) and 4% side insets")
    y += 22
    im.paste(guides, (40, y))
    y += 191 + 28

    # Desktop and mobile mocks side by side — may need shrink
    label(40, y, "Desktop mock: logo over cover, bottom-left")
    # desktop mock is 1128+72 wide; shrink to fit remaining height
    desk_w = 900
    ratio = desk_w / desk.width
    desk_r = down(desk, desk_w, int(desk.height * ratio))
    im.paste(desk_r, (40, y + 22))
    mob_r_w = 320
    ratio_m = mob_r_w / mobile.width
    mob_r = down(mobile, mob_r_w, int(mobile.height * ratio_m))
    mx = 40 + desk_w + 40
    label(mx, y, "Mobile mock (390-wide crop)")
    im.paste(mob_r, (mx, y + 22))
    return im


def write_svgs():
    """Vector sources for the adapted mark and lockup (light)."""
    # Reuse the logo_1104 text-path approach for a faithful lockup SVG.
    SG = TTFont(SG_BOLD)
    MM = TTFont(mm_path())

    def text_paths(font, s, x, y, size, track=0):
        gs = font.getGlyphSet()
        cmap = font.getBestCmap()
        upm = font["head"].unitsPerEm
        sc = size / upm
        pen = SVGPathPen(gs)
        cx = x
        for ch in s:
            g = cmap.get(ord(ch))
            if g is None:
                continue
            tp = TransformPen(pen, (sc, 0, 0, -sc, cx, y))
            gs[g].draw(tp)
            cx += gs[g].width * sc + track
        return pen.getCommands(), cx - track

    def band_v(x, y, w, h):
        parts = []
        y0 = y
        seg = h / 6.0
        for i, col in enumerate(BAND):
            y1 = y + h if i == 5 else y + (i + 1) * seg
            parts.append(f'<rect x="{x:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{y1-y0:.2f}" fill="{col}"/>')
            y0 = y1
        return "".join(parts)

    # Lockup — same metrics as original C (type 24 / 12, rule 4x54, view ~152x62)
    a, ax = text_paths(SG, "The Margin", 18, 26, 24, -0.4)
    b, bx = text_paths(SG, "Wars", 18, 54, 24, -0.4)
    n, nx = text_paths(MM, "bp", bx + 10, 54, 12, 0.5)
    body = (
        f'<rect x="0" y="4" width="4" height="54" fill="{PINK}"/>'
        + f'<path d="{a+b}" fill="{INK}"/>'
        + f'<path d="{n}" fill="{MUTED}"/>'
    )
    w = int(max(ax, nx) + 4)
    lock = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 62" width="{w}" height="62" '
        f'role="img" aria-label="The Margin Wars">{body}</svg>'
    )
    (OUT / "lockup_light.svg").write_text(lock)

    # Mark 32-equivalent construction, plus a 400-viewBox version
    m, mx = text_paths(SG, "M", 13, 24, 17, 0)
    mark32 = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" '
        f'role="img" aria-label="The Margin Wars">'
        f'<rect width="32" height="32" rx="16" fill="{INK}"/>'
        + band_v(8, 7, 3, 18)
        + f'<path d="{m}" fill="{PAPER}"/>'
        + "</svg>"
    )
    (OUT / "mark32.svg").write_text(mark32)

    # 400 viewBox mark matching the raster construction more closely
    # We'll keep a simple centred version.
    # Rule at x=122, y=84, w=38, h=232; M sized ~184 at a fitted origin.
    m400, _ = text_paths(SG, "M", 172, 268, 184, 0)
    mark400 = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400" '
        f'role="img" aria-label="The Margin Wars">'
        f'<rect width="400" height="400" fill="{INK}"/>'
        + band_v(122, 84, 38, 232)
        + f'<path d="{m400}" fill="{PAPER}"/>'
        + "</svg>"
    )
    (OUT / "mark400.svg").write_text(mark400)


def render_substack_wordmark(width: int = 1100, height: int = 220, bg: str = PAPER, scale: int = 4) -> Image.Image:
    """Wide Substack header wordmark: C lockup with a pink vertical ledger rule."""
    im = new(width * scale, height * scale, bg)
    # Type size so the stacked lockup sits comfortably in 220px with padding.
    # Original C is 62 tall in a 24px word; target ~ 140px of the 220 canvas.
    word_px = 64
    lock, _ = render_lockup(word_px=word_px, scale=scale, bg=None, fg=INK, bp_fill=MUTED, rule_fill=PINK)
    # Left-aligned with even padding, vertically centred.
    pad_x = int(round(height * 0.22 * scale))
    pad_y = (height * scale - lock.height) // 2
    im.paste(lock, (pad_x, pad_y), lock)
    return down(im, width, height)


def render_substack_wordmark_tight(scale: int = 4) -> Image.Image:
    """Tight transparent lockup (pink rule) for placing on a Substack header."""
    lock, _ = render_lockup(word_px=72, scale=scale, bg=None, fg=INK, bp_fill=MUTED, rule_fill=PINK)
    # Add a little transparent padding so the rule and descenders are not clipped.
    pad = int(8 * scale)
    im = Image.new("RGBA", (lock.width + pad * 2, lock.height + pad * 2), (0, 0, 0, 0))
    im.paste(lock, (pad, pad), lock)
    out_scale = 2  # export at 2x so it stays crisp on retina headers
    w, h = max(1, (lock.width // scale + 16) * out_scale), max(1, (lock.height // scale + 16) * out_scale)
    # Resize premultiplied (no dark halo), then clamp resampling ringing so empty pixels are exactly 0 alpha.
    small = im.convert("RGBa").resize((w, h), Image.Resampling.LANCZOS).convert("RGBA")
    r, g, b, a = small.split()
    a = a.point(lambda v: 0 if v < 8 else v)
    small = Image.merge("RGBA", (r, g, b, a))
    px = small.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                px[x, y] = (0, 0, 0, 0)
    return small


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    logo = render_mark(scale=8)
    logo.save(OUT / "logo_400.png", "PNG", optimize=True)
    logo60 = logo.resize((60, 60), Image.Resampling.BOX)
    logo60.save(OUT / "logo_60.png", "PNG", optimize=True)
    # Explicit circle preview at 60 (on paper, so the crop is visible)
    prev = new(60, 60, PAPER)
    c60 = circle_crop(logo, 60)
    # For a 60x60 preview of the circle, the circle fills the frame (LinkedIn thumbnail).
    # Also save a padded preview so the circular silhouette is obvious on a page.
    c60.save(OUT / "logo_60_circle.png", "PNG", optimize=True)
    pad = new(92, 92, PAPER)
    pad.paste(c60, (16, 16), c60)
    pad.save(OUT / "logo_60_circle_on_paper.png", "PNG", optimize=True)

    cover = render_cover()
    cover.save(OUT / "cover_1128x191.png", "PNG", optimize=True)
    guides = render_cover_with_guides(cover)
    guides.save(OUT / "qa_cover_guides.png", "PNG", optimize=True)
    desk = render_desktop_mock(cover, logo)
    desk.save(OUT / "mock_logo_on_cover.png", "PNG", optimize=True)
    mobile = render_mobile_mock(cover, logo)
    mobile.save(OUT / "mock_mobile.png", "PNG", optimize=True)
    sheet = render_qa_sheet(logo, logo60, cover, guides, desk, mobile)
    sheet.save(OUT / "qa_sheet.png", "PNG", optimize=True)
    word = render_substack_wordmark(1100, 220, bg=PAPER, scale=4)
    word.save(OUT / "substack_wordmark.png", "PNG", optimize=True)
    word2 = render_substack_wordmark(2200, 440, bg=PAPER, scale=4)
    word2.save(OUT / "substack_wordmark@2x.png", "PNG", optimize=True)
    tight = render_substack_wordmark_tight(scale=4)
    tight.save(OUT / "substack_wordmark_transparent.png", "PNG", optimize=True)
    write_svgs()
    print("wrote", OUT)
    for p in sorted(OUT.iterdir()):
        if p.is_file():
            print(f"  {p.name:28s} {p.stat().st_size:8d}")


if __name__ == "__main__":
    main()
