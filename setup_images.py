"""
setup_images.py
===============
Generates branded placeholder images for the Saeed English Language & Computer
Academy website using Pillow (PIL).

These are REAL, valid JPEG/PNG files (correct binary format and headers) so
browsers render them properly in <img> tags and as CSS backgrounds — unlike
plain SVG text written into a .jpg file, which most browsers refuse to show.

They are *placeholders*: each image is a tastefully branded plate (academy
colours + label) indicating which real photo belongs there. Replace the files
with the actual photos when ready; the filenames and code stay the same.

    python setup_images.py

Outputs:
    static/images/logo.png            round academy logo (transparent PNG)
    static/images/academy/gallery1.jpg  Certificate Distribution Ceremony
    static/images/academy/gallery2.jpg  Certificate Presentation
    static/images/academy/gallery3.jpg  New Batch Starting (Saeed Wazir)
    static/images/academy/gallery4.jpg  World Peace Summit
    static/images/academy/gallery5.jpg  Our Students in Class
    static/images/academy/gallery6.jpg  Welcome to the Academy
    static/images/academy/classroom.jpg  Classroom Learning
    static/images/academy/ceo.jpg       Saeed Wazir — Founder & CEO
"""

import os
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
BASE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE, "static", "images")
ACADEMY_DIR = os.path.join(IMAGES_DIR, "academy")
os.makedirs(ACADEMY_DIR, exist_ok=True)

# --------------------------------------------------------------------------- #
# Brand palette
# --------------------------------------------------------------------------- #
MAROON      = (139, 0, 0)      # #8B0000
GOLD        = (201, 168, 76)   # #C9A84C
NAVY        = (13, 27, 42)     # #0d1b2a
DEEP_GREEN  = (15, 61, 46)     # #0f3d2e
ROYAL_BLUE  = (24, 49, 110)    # #18316e
NEAR_BLACK  = (40, 0, 0)      # deep maroon-black
SLATE       = (62, 66, 77)     # grey-blue
WHITE       = (255, 255, 255)
OFFWHITE    = (245, 241, 230)
PAPER       = (238, 236, 228)  # near-white for portrait
DARK_TEXT   = (38, 34, 28)

ACADEMY_NAME = "Saeed English Language & Computer Academy"


# --------------------------------------------------------------------------- #
# Font helpers
# --------------------------------------------------------------------------- #
def load_font(size, bold=False, italic=False):
    """Load a system TrueType font, falling back through sensible choices."""
    order = []
    if bold and italic:
        order += [
            "C:/Windows/Fonts/georgiai.ttf",
            "C:/Windows/Fonts/arialbi.ttf",
            "C:/Windows/Fonts/segoeuiz.ttf",
        ]
    if bold:
        order += [
            "C:/Windows/Fonts/ariblk.ttf",
            "C:/Windows/Fonts/georgiab.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/seguisb.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
        ]
    if italic:
        order += [
            "C:/Windows/Fonts/georgiai.ttf",
            "C:/Windows/Fonts/ariali.ttf",
            "C:/Windows/Fonts/segoeuii.ttf",
        ]
    order += [
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/seguisym.ttf",
    ]
    for path in order:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


# --------------------------------------------------------------------------- #
# Background helpers
# --------------------------------------------------------------------------- #
def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size, top, bottom):
    """Smooth top->bottom gradient, drawn as horizontal lines (fast)."""
    w, h = size
    img = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1) if h > 1 else 0
        draw.line([(0, y), (w - 1, y)], fill=_lerp(top, bottom, t))
    return img


# --------------------------------------------------------------------------- #
# Emblems drawn inside the inner frame to signal "image goes here"
# --------------------------------------------------------------------------- #
def draw_landscape_emblem(overlay, box, color):
    """Classic photo-placeholder: a sun and two mountains."""
    x0, y0, x1, y1 = box
    sun_r = max(40, (x1 - x0) // 9)
    sx, sy = x1 - 90, y0 + 90
    overlay.ellipse(
        [sx - sun_r, sy - sun_r, sx + sun_r, sy + sun_r],
        fill=color + (90,),
    )
    base_y = y1 - 26
    cx = (x0 + x1) // 2
    overlay.polygon(
        [(x0 + 70, base_y), (cx - 130, base_y - 180), (cx - 30, base_y)],
        fill=color + (70,),
    )
    overlay.polygon(
        [(x1 - 70, base_y), (cx + 130, base_y - 195), (cx + 30, base_y)],
        fill=color + (85,),
    )
    overlay.line([(x0 + 36, base_y), (x1 - 36, base_y)], fill=color + (120,), width=2)


def draw_portrait_emblem(overlay, box, color):
    """A simple head-and-shoulders silhouette for portrait placeholders."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    head_r = max(50, (y1 - y0) // 6)
    head_cy = y0 + (y1 - y0) * 0.38
    overlay.ellipse(
        [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
        fill=color + (85,),
    )
    sw = head_r * 2.4
    sh = (y1 - y0) * 0.45
    overlay.pieslice(
        [cx - sw / 2, y1 - sh, cx + sw / 2, y1 + sw / 2],
        start=180, end=360, fill=color + (80,),
    )


# --------------------------------------------------------------------------- #
# Main placeholder builder (landscape / event style)
# --------------------------------------------------------------------------- #
def make_placeholder(
    path,
    title,
    subtitle,
    c1,
    c2,
    accent=GOLD,
    emblem="landscape",
    size=(1200, 800),
    body_color=OFFWHITE,
    note_color=(230, 225, 210),
    light_bg=False,
):
    w, h = size
    base = vertical_gradient(size, c1, c2).convert("RGBA")
    draw = ImageDraw.Draw(base, "RGBA")

    # Translucent elements go on a separate layer and are alpha-composited
    # so the blending is correct regardless of Pillow's draw behaviour.
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    lod = ImageDraw.Draw(layer)

    # --- decorative double frame ------------------------------------------- #
    m = 30
    draw.rectangle([m, m, w - m, h - m], outline=accent + (255,), width=4)
    draw.rectangle([m + 11, m + 11, w - m - 11, h - m - 11],
                   outline=accent + (160,), width=1)

    # --- inner "photo" panel ----------------------------------------------- #
    fx0, fy0 = m + 64, m + 74
    fx1, fy1 = w - m - 64, int(h * 0.64)
    panel_fill = (0, 0, 0, 40) if not light_bg else (255, 255, 255, 120)
    lod.rectangle([fx0, fy0, fx1, fy1], fill=panel_fill, outline=accent + (180,), width=2)

    # dashed tick marks along the top edge of the panel
    dash_len = 18
    x = fx0 + 14
    while x < fx1 - 14:
        lod.line([(x, fy0 - 7), (x, fy0 - 1)], fill=accent + (200,), width=2)
        x += dash_len * 2

    # emblem inside the panel
    if emblem == "landscape":
        draw_landscape_emblem(lod, (fx0, fy0, fx1, fy1), accent)
    elif emblem == "portrait":
        draw_portrait_emblem(lod, (fx0, fy0, fx1, fy1), accent)

    base = Image.alpha_composite(base, layer)
    draw = ImageDraw.Draw(base, "RGBA")

    # --- text block below the panel ---------------------------------------- #
    title_font = load_font(54, bold=True)
    sub_font = load_font(32, italic=True)
    tag_font = load_font(24)
    note_font = load_font(21)

    ty = int(h * 0.70)
    draw.text(((w - text_width(draw, title, title_font)) / 2, ty),
              title, font=title_font, fill=accent, anchor="lm")
    draw.text(((w - text_width(draw, subtitle, sub_font)) / 2, ty + 68),
              subtitle, font=sub_font, fill=body_color, anchor="lm")
    draw.text(((w - text_width(draw, ACADEMY_NAME, tag_font)) / 2, ty + 112),
              ACADEMY_NAME, font=tag_font, fill=body_color, anchor="lm")

    note = "Placeholder \u2014 replace with the actual photo"
    draw.text(((w - text_width(draw, note, note_font)) / 2, h - m - 40),
              note, font=note_font, fill=note_color, anchor="lm")

    tag = "PHOTO PLACEHOLDER"
    draw.text(((w - text_width(draw, tag, note_font)) / 2, m + 20),
              tag, font=note_font, fill=accent, anchor="lm")

    base.convert("RGB").save(path, "JPEG", quality=90, optimize=True)
    print("Created:", os.path.relpath(path, BASE))


# --------------------------------------------------------------------------- #
# Round logo (transparent PNG)
# --------------------------------------------------------------------------- #
def make_logo(path, size=500):
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    cx = s / 2

    outer = 18
    draw.ellipse([outer, outer, s - outer, s - outer],
                 fill=NAVY + (255,), outline=GOLD + (255,), width=10)
    inner_pad = outer + 26
    draw.ellipse([inner_pad, inner_pad, s - inner_pad, s - inner_pad],
                 outline=GOLD + (170,), width=2)

    # top accent arc
    draw.arc([outer + 4, outer + 4, s - outer - 4, s - outer - 4],
             start=-60, end=60, fill=GOLD + (255,), width=4)

    name_font = load_font(74, bold=True)
    line_font = load_font(26, bold=True)
    tag_font = load_font(24, italic=True)

    draw.text((cx, s * 0.40), "SAEED", font=name_font, fill=GOLD, anchor="mm")
    draw.line([(s * 0.30, s * 0.50), (s * 0.70, s * 0.50)],
              fill=GOLD + (180,), width=2)
    draw.text((cx, s * 0.58), "ENGLISH LANGUAGE", font=line_font, fill=WHITE, anchor="mm")
    draw.text((cx, s * 0.635), "& COMPUTER ACADEMY", font=line_font, fill=WHITE, anchor="mm")
    draw.text((cx, s * 0.72), "Learn \u2022 Practice \u2022 Excel",
              font=tag_font, fill=GOLD, anchor="mm")

    img.save(path, "PNG")
    print("Created:", os.path.relpath(path, BASE))


# --------------------------------------------------------------------------- #
# Build everything
# --------------------------------------------------------------------------- #
def main():
    make_logo(os.path.join(IMAGES_DIR, "logo.png"))

    # (filename, title, subtitle, c1, c2, accent, emblem)
    items = [
        ("gallery1.jpg", "Certificate Distribution Ceremony",
         "Annual awards celebration", DEEP_GREEN, (60, 80, 50), GOLD, "landscape"),
        ("gallery2.jpg", "Certificate Presentation",
         "Honouring our graduates", (176, 132, 48), MAROON, (255, 235, 170), "landscape"),
        ("gallery3.jpg", "New Batch Starting",
         "Enrol now with Saeed Wazir", MAROON, NEAR_BLACK, GOLD, "landscape"),
        ("gallery4.jpg", "World Peace Summit",
         "Saeed Wazir at the podium", NAVY, ROYAL_BLUE, GOLD, "landscape"),
        ("gallery5.jpg", "Our Students in Class",
         "Learning together every day", NAVY, (30, 50, 40), GOLD, "landscape"),
        ("gallery6.jpg", "Welcome to the Academy",
         "A new student's first day", SLATE, NAVY, GOLD, "landscape"),
        ("classroom.jpg", "Classroom Learning",
         "On the red carpet, engaged and curious", MAROON, (108, 0, 0), GOLD, "landscape"),
    ]
    for fname, title, sub, c1, c2, accent, emblem in items:
        make_placeholder(os.path.join(ACADEMY_DIR, fname), title, sub, c1, c2,
                         accent=accent, emblem=emblem)

    # CEO portrait — lighter background, green accents, portrait silhouette
    make_placeholder(
        os.path.join(ACADEMY_DIR, "ceo.jpg"),
        "Saeed Wazir",
        "Founder & CEO",
        PAPER, (216, 220, 208),
        accent=DEEP_GREEN, emblem="portrait", size=(800, 1000),
        body_color=DARK_TEXT, note_color=(90, 90, 80), light_bg=True,
    )

    print("\nAll placeholder images generated.")


if __name__ == "__main__":
    main()
