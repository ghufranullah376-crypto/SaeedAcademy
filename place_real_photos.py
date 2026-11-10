"""
place_real_photos.py
====================
Maps the uploaded photos to their correct destination filenames.
Run once to install the real photos into the project.

The uploaded images (already on disk from Kiro's session) are read from
their source paths and copied to the correct static/ locations.

Usage:
    python place_real_photos.py  [source_folder]

If source_folder is omitted the script looks in common download/desktop
locations automatically.
"""

import os, sys, shutil, glob

BASE = os.path.dirname(os.path.abspath(__file__))

DEST = {
    "logo":        os.path.join(BASE, "static", "images", "logo.png"),
    "ceo":         os.path.join(BASE, "static", "images", "academy", "ceo.jpg"),
    "gallery1":    os.path.join(BASE, "static", "images", "academy", "gallery1.jpg"),
    "gallery2":    os.path.join(BASE, "static", "images", "academy", "gallery2.jpg"),
    "gallery3":    os.path.join(BASE, "static", "images", "academy", "gallery3.jpg"),
    "gallery4":    os.path.join(BASE, "static", "images", "academy", "gallery4.jpg"),
    "gallery5":    os.path.join(BASE, "static", "images", "academy", "gallery5.jpg"),
    "gallery6":    os.path.join(BASE, "static", "images", "academy", "gallery6.jpg"),
    "classroom":   os.path.join(BASE, "static", "images", "academy", "classroom.jpg"),
}

# ── MANUAL OVERRIDE ────────────────────────────────────────────────────────
# Fill in the full paths to your photos here, then run this script.
# Leave a value as "" to skip that photo.
MANUAL = {
    # Example: "logo": r"C:\Users\khan\Downloads\logo.png",
    "logo":      "",
    "ceo":       "",    # Saeed Wazir portrait (green shalwar kameez)
    "gallery1":  "",    # Certificate distribution group photo
    "gallery2":  "",    # Certificate presentation (two people)
    "gallery3":  "",    # New batch starting poster
    "gallery4":  "",    # World Peace Summit photo
    "gallery5":  "",    # Students sitting in classroom
    "gallery6":  "",    # Welcome/portrait shot
    "classroom": "",    # Students on red carpet learning
}
# ──────────────────────────────────────────────────────────────────────────


def find_images_in(folder):
    """Return list of image paths in folder sorted by size desc."""
    found = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        found.extend(glob.glob(os.path.join(folder, "**", ext), recursive=True))
    return sorted(found, key=os.path.getsize, reverse=True)


def copy_photo(src, dest, label):
    if not src or not os.path.exists(src):
        print(f"  SKIP  {label} — source not found: {src}")
        return False
    shutil.copy2(src, dest)
    kb = os.path.getsize(dest) // 1024
    print(f"  OK    {label} → {os.path.relpath(dest, BASE)}  ({kb} KB)")
    return True


def main():
    search_folder = sys.argv[1] if len(sys.argv) > 1 else None
    copied = 0

    print("Installing real photos...\n")

    for key, dest in DEST.items():
        src = MANUAL.get(key, "")
        if src:
            if copy_photo(src, dest, key):
                copied += 1
        else:
            print(f"  SKIP  {key} — no source path set in MANUAL dict")

    if search_folder:
        print(f"\nAuto-scan of '{search_folder}':")
        imgs = find_images_in(search_folder)
        print(f"  Found {len(imgs)} images — listing largest 20:")
        for p in imgs[:20]:
            print(f"    {os.path.basename(p):40s}  {os.path.getsize(p)//1024} KB  →  {p}")
        print("\nEdit MANUAL dict in this script with the correct source paths, then re-run.")

    print(f"\nDone. {copied}/{len(DEST)} photos installed.")
    if copied < len(DEST):
        print(
            "\nTo install your real photos:\n"
            "  1. Open place_real_photos.py\n"
            "  2. Fill in the MANUAL dict with full paths to each photo\n"
            "  3. Run:  python place_real_photos.py\n"
            "\nPhoto guide:\n"
            "  logo      → Your round academy logo (PNG preferred)\n"
            "  ceo       → Saeed Wazir (green shalwar kameez, white background)\n"
            "  gallery1  → Certificate distribution ceremony (large group)\n"
            "  gallery2  → Certificate presentation (two people at whiteboard)\n"
            "  gallery3  → New batch poster / Saeed Wazir speaking\n"
            "  gallery4  → World Peace Summit podium photo\n"
            "  gallery5  → Students sitting in classroom\n"
            "  gallery6  → Welcome backdrop portrait\n"
            "  classroom → Students on red carpet, learning session\n"
        )


if __name__ == "__main__":
    main()
