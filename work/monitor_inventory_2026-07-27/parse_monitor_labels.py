import json
import re
from pathlib import Path

BASE = Path(r"C:\Users\AlejandroAcosta\Documents\ai-workstation\work\monitor_inventory_2026-07-27")
SOURCE = BASE / "ocr_results.json"
RETRY_SOURCE = BASE / "ocr_retry_results.json"
OUTPUT = BASE / "parsed_inventory.json"

MANUAL_SERIALS = {
    "IMG_6283.JPG": "VNA21PCL",
    "IMG_6291.JPG": "VNA21PGV",
    "IMG_6298.JPG": "VNA21PGW",
    "IMG_6304.JPG": "VNA21PCR",
    "IMG_6312.JPG": "VNA21PCX",
    "IMG_6314.JPG": "VNA21P7V",
    "IMG_6315.JPG": "VNA21PHV",
    "IMG_6317.JPG": "VNA21PCW",
    "IMG_6327.JPG": "VNA21PF6",
    "IMG_6345.JPG": "VNA21PGN",
    "IMG_6347.JPG": "V9-06ZV2Y",
    "IMG_6348.JPG": "V9-070Z51",
    "IMG_6353.JPG": "V5Z21014",
    "IMG_6358.JPG": "VNA21PHL",
    "IMG_6365.JPG": "V9-06ZV2V",
    "IMG_6367.JPG": "VNA21PGY",
    "IMG_6374.JPG": "V9-06ZV35",
    "IMG_6375.JPG": "VNA20MYX",
    "IMG_6376.JPG": "VNA21PQ1",
    "IMG_6386.JPG": "VNA21P79",
    "IMG_6387.JPG": "V5LA0027",
    "IMG_6389.JPG": "VNA21PQV",
    "IMG_6397.JPG": "VNA20MRL",
    "IMG_6401.JPG": "VNA21PN1",
    "IMG_6403.JPG": "VNA20MKP",
    "IMG_6410.JPG": "VNA21PA9",
    "IMG_6420.JPG": "VNA20HBH",
    "IMG_6424.JPG": "VNA21PCK",
    "IMG_6425.JPG": "VNA21PGP",
    "IMG_6442.JPG": "VNA21PHD",
    "IMG_6445.JPG": "VNA20MK6",
    "IMG_6463.JPG": "VNA21PQ2",
    "IMG_6464.JPG": "VNA21PGT",
}


def clean_token(value: str) -> str:
    return re.sub(r"[^A-Z0-9-]", "", value.upper())


def first_match(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1)
    return ""


def parse_record(record, retry_text=""):
    original_text = record.get("ocr_text") or ""
    text = f"{original_text} {retry_text}".strip()
    compact = re.sub(r"[^A-Z0-9]", "", text.upper())

    if "61FEMAR6" in compact or "D20215FT0" in compact or "D20215FTO" in compact:
        model = "D20215FT0"
        mtm = "61FE-MAR6-WW"
        fru = "5D10Y48252"
    elif "63B3GAR6" in compact or "D22238QP" in compact:
        model = "D22238QP0"
        mtm = "63B3-GAR6-WW"
        fru = "5D11J31074"
    elif "61A9MAR1" in compact or "T22I10" in compact:
        model = "T22i-10"
        mtm = "61A9-MAR1-WW"
        fru = "00PC160"
    elif "60E1MAR2" in compact or "T2254PC" in compact or "RA22WLCABNS" in compact:
        model = "T2254pC"
        mtm = "60E1-MAR2-WW"
        fru = "00PC018"
    else:
        model = first_match(
            [
                r"\b(T\d{2}[A-Z0-9-]{2,8})\b",
                r"\b(D\d{7}[A-Z0-9])\b",
            ],
            text,
        )
        mtm = first_match([r"\b(\d{2}[A-Z0-9]{2}[-. ][A-Z0-9]{4}[-. ][A-Z0-9]{2})\b"], text)
        fru = first_match([r"FR[UI]\s+(?:NUMBER)?\s*[:.-]?\s*([A-Z0-9]{7,12})"], text)

    serial = ""
    serial_source = ""
    serial_patterns = [
        (r"\b(VNA[0-9A-Z]{5})\b", "pattern"),
        (r"\b(V5[0-9A-Z]{6})\b", "pattern"),
        (r"\b(V9[- ]?[0O][A-Z0-9]{5})\b", "pattern"),
        (r"63B3GAR6(?:WW|VM|VV)(V9[0O][A-Z0-9]{5})\b", "barcode"),
    ]
    for pattern, source in serial_patterns:
        match = re.search(pattern, text.upper())
        if match:
            serial = clean_token(match.group(1))
            serial_source = source
            break

    if serial.startswith("V90"):
        serial = "V9-" + serial[2:]
    elif serial.startswith("V9O"):
        serial = "V9-0" + serial[3:]

    if record["file_name"] in MANUAL_SERIALS:
        serial = MANUAL_SERIALS[record["file_name"]]
        serial_source = "visual review"

    raw_date = first_match(
        [
            r"\b(20\d{2})[.\-/, ](0?\d{1,2})[.\-/, ](0?\d{1,2})\b",
        ],
        text,
    )
    # first_match only returns group 1, so use a full date match separately.
    date_match = re.search(r"\b(20\d{2})[.\-/, ](0?\d{1,2})[.\-/, ](0?\d{1,2})\b", text)
    manufacture_date = ""
    if date_match:
        year, month, day = date_match.groups()
        month_num, day_num = int(month), int(day)
        if 1 <= month_num <= 12 and 1 <= day_num <= 31:
            manufacture_date = f"{year}-{month_num:02d}-{day_num:02d}"

    fields_found = sum(bool(value) for value in [model, mtm, fru, serial, manufacture_date])
    if serial and fields_found >= 4:
        confidence = "High"
    elif serial or fields_found >= 3:
        confidence = "Medium"
    else:
        confidence = "Low"

    review_reasons = []
    if not serial:
        review_reasons.append("Serial not confidently extracted")
    if not model:
        review_reasons.append("Model not confidently extracted")
    if not manufacture_date:
        review_reasons.append("Manufacture date not extracted")
    if not text:
        review_reasons.append("No OCR text")

    return {
        "photo_file": record["file_name"],
        "manufacturer": "Lenovo" if text or model or mtm else "",
        "model": model,
        "mtm": mtm,
        "serial_number": serial,
        "fru_number": fru,
        "manufacture_date": manufacture_date,
        "confidence": confidence,
        "review_status": "Needs Review" if review_reasons else "Ready",
        "review_notes": "; ".join(review_reasons),
        "source_path": record["full_path"],
        "ocr_text": original_text,
        "retry_ocr_text": retry_text,
        "ocr_error": record.get("error") or "",
        "serial_source": serial_source,
    }


records = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
retry_by_source = {}
if RETRY_SOURCE.exists():
    retry_records = json.loads(RETRY_SOURCE.read_text(encoding="utf-8-sig"))
    for retry in retry_records:
        source_stem = retry["file_name"].split("__r", 1)[0]
        retry_by_source.setdefault(source_stem, []).append(retry.get("ocr_text") or "")

parsed = [
    parse_record(record, " ".join(retry_by_source.get(Path(record["file_name"]).stem, [])))
    for record in records
]
OUTPUT.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Parsed: {len(parsed)}")
print(f"Ready: {sum(row['review_status'] == 'Ready' for row in parsed)}")
print(f"Needs review: {sum(row['review_status'] == 'Needs Review' for row in parsed)}")
print(f"Serials found: {sum(bool(row['serial_number']) for row in parsed)}")
print(f"Models found: {sum(bool(row['model']) for row in parsed)}")
print("Unresolved files:")
print(", ".join(row["photo_file"] for row in parsed if row["review_status"] == "Needs Review"))
