import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

BASE = Path(r"C:\Users\AlejandroAcosta\Documents\ai-workstation\work\monitor_inventory_2026-07-27")
SOURCE_DIR = BASE / "monitors"
RETRY_DIR = BASE / "retry_images"
PARSED = BASE / "parsed_inventory.json"

RETRY_DIR.mkdir(exist_ok=True)
records = json.loads(PARSED.read_text(encoding="utf-8"))
targets = [row for row in records if not row["serial_number"]]

for row in targets:
    source = SOURCE_DIR / row["photo_file"]
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("L")
        image = ImageOps.autocontrast(image, cutoff=1)
        image = ImageEnhance.Contrast(image).enhance(1.5)
        max_dimension = max(image.size)
        if max_dimension > 2200:
            scale = 2200 / max_dimension
            image = image.resize((round(image.width * scale), round(image.height * scale)))

        stem = source.stem
        for degrees in (0, 90, 180, 270):
            variant = image.rotate(degrees, expand=True, fillcolor=255)
            variant.save(RETRY_DIR / f"{stem}__r{degrees}.jpg", quality=94)

print(f"Prepared {len(targets)} source photos and {len(targets) * 4} retry images")
