import json
import re
from pathlib import Path

BASE = Path(r"C:\Users\AlejandroAcosta\Documents\ai-workstation\work\monitor_inventory_2026-07-27")
SOURCE = BASE / "parsed_inventory.json"
OUTPUT = BASE / "reconciled_inventory.json"

MODEL_MAP = {
    "T2254pC": ("ThinkVision T2254pC", "T2254pC"),
    "T22S4pC": ("ThinkVision T2254pC", "T2254pC"),
    "T22i-10": ("ThinkVision T22i-10", "A16215FT0"),
    "T221-10": ("ThinkVision T22i-10", "A16215FT0"),
    "D20215FT0": ("ThinkVision T22i-20", "D20215FT0"),
    "D22238QP0": ("ThinkVision P24h-30", "D22238QP0"),
}

DIRECT_VARIANTS = {"T22S4pC", "T221-10"}
D202_FILES = {"IMG_6347.JPG", "IMG_6348.JPG", "IMG_6365.JPG", "IMG_6374.JPG", "IMG_6421.JPG"}


def compact(value):
    return re.sub(r"[^A-Z0-9]", "", (value or "").upper())


def infer_from_identifiers(row):
    mtm = compact(row.get("mtm"))
    serial = (row.get("serial_number") or "").upper()
    fru = compact(row.get("fru_number"))

    if "60E1MAR2" in mtm or fru == "00PC018" or serial.startswith("VNA"):
        return "ThinkVision T2254pC", "T2254pC", "Inferred - review", "Identifier family: MTM/FRU/serial"
    if "61A9MAR1" in mtm or fru == "00PC160" or serial.startswith("V5"):
        return "ThinkVision T22i-10", "A16215FT0", "Inferred - review", "Identifier family: MTM/FRU/serial"
    if "61FEMAR6" in mtm or fru == "5D10Y48252" or serial.startswith(("V9-06", "V9-07")):
        return "ThinkVision T22i-20", "D20215FT0", "Inferred - review", "Identifier family: MTM/FRU/serial"
    if "63B3GAR6" in mtm or fru == "5D11J31074" or serial.startswith("V9-0E"):
        return "ThinkVision P24h-30", "D22238QP0", "Inferred - review", "Identifier family: MTM/FRU/serial"
    return "", "", "Unresolved", "No reliable series/code evidence"


rows = json.loads(SOURCE.read_text(encoding="utf-8"))
reconciled = []

for row in rows:
    raw_model = row.get("model") or ""
    if raw_model in MODEL_MAP:
        series, type_code = MODEL_MAP[raw_model]
        if row["photo_file"] in D202_FILES:
            model_status = "Confirmed by visual review"
            basis = "Label explicitly shows ThinkVision T22i-20 and D20215FT0"
        elif raw_model in DIRECT_VARIANTS:
            model_status = "Normalized OCR variant"
            basis = f"Normalized OCR value {raw_model}"
        else:
            model_status = "Extracted from label"
            basis = "Series or Type/Model text extracted from label"
    else:
        series, type_code, model_status, basis = infer_from_identifiers(row)

    canonical_key = f"{series} | {type_code}" if series and type_code else ""
    reconciliation_flags = []
    if row.get("review_status") == "Needs Review":
        reconciliation_flags.append("Needs Review")
    if not raw_model:
        reconciliation_flags.append("Original Unresolved")
    if raw_model in DIRECT_VARIANTS:
        reconciliation_flags.append("Original Other Extracted")
    if row["photo_file"] in D202_FILES:
        reconciliation_flags.append("D20215FT0 manual check")
    if model_status in {"Inferred - review", "Unresolved"}:
        reconciliation_flags.append(model_status)

    reconciled.append(
        {
            **row,
            "original_model_field": raw_model,
            "series_name": series,
            "type_model_code": type_code,
            "canonical_model_key": canonical_key,
            "model_reconciliation_status": model_status,
            "model_identification_basis": basis,
            "reconciliation_scope": "; ".join(reconciliation_flags),
        }
    )

OUTPUT.write_text(json.dumps(reconciled, indent=2, ensure_ascii=False), encoding="utf-8")

from collections import Counter

print("Canonical tally:")
for key, count in Counter(row["canonical_model_key"] or "<unresolved>" for row in reconciled).most_common():
    print(count, key)
print("Status tally:")
for status, count in Counter(row["model_reconciliation_status"] for row in reconciled).most_common():
    print(count, status)
print("Reconciliation scope:", sum(bool(row["reconciliation_scope"]) for row in reconciled))
