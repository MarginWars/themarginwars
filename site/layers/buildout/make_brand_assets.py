"""Brand assets for the site, rendered from the approved logo C generator (linkedin_page_1110/gen.py).
Writes into site_calm: favicon.ico (16/32/48), icon.svg, apple-touch-icon.png, assets/brand/og-default.png (1200x630).
Idempotent: same inputs give the same files."""
import sys, shutil, pathlib
sys.path.insert(0, "@MW_ROOT@/linkedin_page_1110")
import gen
from PIL import Image, ImageDraw
SITE = pathlib.Path("@MW_ROOT@/site_calm")
L = pathlib.Path("@MW_ROOT@/linkedin_page_1110")
mark = gen.render_mark(scale=8).convert("RGBA")  # 400x400, ink square, six-colour stacked rule, paper M
mark.resize((48, 48), Image.Resampling.LANCZOS).save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
mark.resize((180, 180), Image.Resampling.LANCZOS).convert("RGB").save(SITE / "apple-touch-icon.png", optimize=True)
mark.resize((512, 512), Image.Resampling.LANCZOS).convert("RGB").save(SITE / "assets/brand/icon-512.png", optimize=True)
shutil.copyfile(L / "mark400.svg", SITE / "icon.svg")
# Approved C files replace the old option_C drafts (the swappable logo component reads these).
oc = SITE / "assets/logo/option_C"
shutil.copyfile(L / "lockup_light.svg", oc / "lockup_light.svg"); shutil.copyfile(L / "mark32.svg", oc / "mark32_dark.svg")
# OG / social default: ink ground, six-colour band, logo C, pink-rule wordmark, tagline.
S = 2; W, H = 1200 * S, 630 * S
og = Image.new("RGBA", (W, H), gen.hx(gen.INK) + (255,)); d = ImageDraw.Draw(og)
bw = W / 6
for i, c in enumerate(gen.BAND): d.rectangle([round(i * bw), 0, round((i + 1) * bw) - 1, 10 * S - 1], fill=gen.hx(c))
m = mark.resize((200 * S, 200 * S), Image.Resampling.LANCZOS); og.paste(m, (88 * S, 170 * S), m)
lock, _ = gen.render_lockup(word_px=76, scale=S, bg=None, fg=gen.PAPER, bp_fill="#8A949A", rule_fill=gen.PINK)
og.paste(lock, (340 * S, 175 * S), lock)
d.text((340 * S + 4 * S, 175 * S + lock.height + 34 * S), "Payments tactics from the front lines.", font=gen.font(gen.mm_path(), 24 * S), fill=gen.hx("#C9D0D4"))
d.text((88 * S, H - 70 * S), "themarginwars.com", font=gen.font(gen.mm_path(), 20 * S), fill=gen.hx("#8A949A"))
og.resize((1200, 630), Image.Resampling.LANCZOS).convert("RGB").save(SITE / "assets/brand/og-default.png", optimize=True)
print("brand assets ok")
