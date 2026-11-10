import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
targets = [
    "static/images/logo.png",
    "static/images/academy/gallery1.jpg",
    "static/images/academy/gallery2.jpg",
    "static/images/academy/gallery3.jpg",
    "static/images/academy/gallery4.jpg",
    "static/images/academy/gallery5.jpg",
    "static/images/academy/gallery6.jpg",
    "static/images/academy/classroom.jpg",
    "static/images/academy/ceo.jpg",
]

lines = []
ok = 0
for rel in targets:
    p = os.path.join(BASE, rel)
    if not os.path.exists(p):
        lines.append(f"MISSING: {rel}")
        continue
    size = os.path.getsize(p)
    with open(p, "rb") as f:
        head = f.read(8)
    try:
        with Image.open(p) as im:
            fmt = im.format
            dim = f"{im.size[0]}x{im.size[1]}"
            mode = im.mode
        lines.append(f"OK  {rel:42s} fmt={fmt:5s} {dim:10s} mode={mode:5s} bytes={size}")
        ok += 1
    except Exception as e:
        lines.append(f"BAD {rel}: {type(e).__name__}: {e}  (head={head!r})")

lines.append(f"\n{ok}/{len(targets)} valid image files")
# also show magic-byte check
lines.append("--- magic bytes ---")
for rel in targets:
    p = os.path.join(BASE, rel)
    if not os.path.exists(p):
        continue
    with open(p, "rb") as f:
        head = f.read(4)
    # JPEG starts FF D8 FF, PNG starts 89 50 4E 47
    kind = "JPEG" if head[:3] == b"\xff\xd8\xff" else ("PNG" if head[:4] == b"\x89PNG" else "?")
    lines.append(f"{rel:42s} {kind}  {head.hex()}")

out = os.path.join(BASE, "__verify_out.txt")
with open(out, "w") as f:
    f.write("\n".join(lines))
print("WROTE", out)
