#!/usr/bin/env python3
"""Favicon set + Open Graph card for nickjwolf.com.

The site had NO favicon and NO og:image: a generic globe in tabs and search results, and a bare
URL whenever the link was shared — including on LinkedIn, which is where a recruiter meets it.

Mark and colours are taken from the wolf SVG already inline in index.html (ink #111827, accent
#059669), so nothing new is invented. Drawn with PIL rather than rasterised: no rasteriser is
installed and the mark is four flat shapes. 8x supersample + LANCZOS keeps 16px clean.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
INK, ACCENT, PAPER = "#111827", "#059669", "#ffffff"
SS = 8
WOLF = [(6, 5), (18, 14), (30, 14), (42, 5), (44, 22), (24, 45), (4, 22)]
EYE_L = [(16, 21), (23, 24.2), (16, 27.4)]
EYE_R = [(32, 21), (25, 24.2), (32, 27.4)]


def _font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mark(px):
    s = px * SS
    k = s / 48.0
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(10 * k), fill=PAPER)
    for shape, colour in ((WOLF, INK), (EYE_L, ACCENT), (EYE_R, ACCENT)):
        d.polygon([(x * k, y * k) for x, y in shape], fill=colour)
    return img.resize((px, px), Image.LANCZOS)


def og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 12, W, H], fill=ACCENT)
    # the mark, scaled up
    m = mark(112).convert("RGBA")
    img.paste(m, (80, 78), m)
    d.text((80, 226), "Nick Wolf", font=_font(72), fill=INK)
    d.text((80, 318), "Senior Software Engineer", font=_font(38), fill="#374151")
    small = _font(25)
    d.text((80, 400), "Healthcare SaaS · Cloud platforms · Real-time systems", font=small, fill="#6b7280")
    d.text((80, 442), "10+ years · Louisville, KY · Remote", font=small, fill="#9ca3af")
    d.text((80, 508), "scratchwolf.com  ·  wolfdigitable.com", font=small, fill=ACCENT)
    return img


def main():
    (HERE / "assets").mkdir(exist_ok=True)
    for name, px in [("favicon-48.png", 48), ("favicon-96.png", 96),
                     ("favicon-192.png", 192), ("apple-touch-icon.png", 180)]:
        mark(px).save(HERE / name, "PNG", optimize=True)
        print(f"  {name}")
    mark(48).save(HERE / "favicon.ico", "ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico (16/32/48)")
    og().save(HERE / "assets" / "og-image.png", "PNG", optimize=True)
    print("  assets/og-image.png (1200x630)")


if __name__ == "__main__":
    main()
