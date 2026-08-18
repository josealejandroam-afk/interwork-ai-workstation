import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const baseDir = String.raw`C:\Users\AlejandroAcosta\Documents\ai-workstation\work\monitor_inventory_2026-07-27`;
const outputDir = String.raw`C:\Users\AlejandroAcosta\Documents\ai-workstation\outputs\monitor_inventory_2026-07-27`;
const records = JSON.parse(await fs.readFile(path.join(baseDir, "reconciled_inventory.json"), "utf8"));

const manualModelResolutions = {
  "IMG_6306.JPG": ["ThinkVision T22i-10", "A16215FT0"],
  "IMG_6326.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6375.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6376.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6383.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6387.JPG": ["ThinkVision T22i-10", "A16215FT0"],
  "IMG_6393.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6397.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6401.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6403.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6404.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6408.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6410.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6411.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6416.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6424.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6442.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6445.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6448.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6459.JPG": ["ThinkVision T22i-10", "A16215FT0"],
  "IMG_6463.JPG": ["ThinkVision T2254pC", "T2254pC"],
};

const manualSerialResolutions = {
  "IMG_6326.JPG": {
    serial: "VNA1H63AK",
    confidence: "High",
    note: "Serial confirmed by user-assisted visual review; atypical 9-character value retained exactly as confirmed.",
  },
  "IMG_6383.JPG": {
    serial: "VNA21P7P",
    confidence: "Low",
    note: "LOW-CONFIDENCE SERIAL",
  },
  "IMG_6393.JPG": {
    serial: "VNA21POY",
    confidence: "High",
    note: "Serial confirmed by direct visual review of the source-photo label.",
  },
  "IMG_6404.JPG": {
    serial: "VNA21N77",
    confidence: "High",
    note: "Serial confirmed from the supplied high-legibility review.",
  },
  "IMG_6408.JPG": {
    serial: "VNA2PHF",
    confidence: "Low",
    note: "LOW-CONFIDENCE SERIAL",
  },
  "IMG_6448.JPG": {
    serial: "VNA21PD4",
    confidence: "High",
    note: "Serial and label fields confirmed from the supplied high-legibility review.",
  },
};

for (const row of records) {
  row.original_model_reconciliation_status = row.model_reconciliation_status;
  const modelResolution = manualModelResolutions[row.photo_file];
  if (modelResolution) {
    row.manufacturer = "Lenovo";
    row.series_name = modelResolution[0];
    row.type_model_code = modelResolution[1];
    row.canonical_model_key = `${modelResolution[0]} | ${modelResolution[1]}`;
    row.model_reconciliation_status = "Confirmed by visual review";
    row.model_identification_basis = "Printed Type/Model line confirmed by direct source-photo review";
  }
  const serialResolution = manualSerialResolutions[row.photo_file];
  if (serialResolution) {
    row.serial_number = serialResolution.serial;
    row.serial_source = "Manual visual review";
    row.confidence = serialResolution.confidence;
    row.review_notes = serialResolution.note;
    row.review_status = serialResolution.confidence === "Low" ? "Needs Review" : "Ready";
  }
}

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Summary");
const inventory = workbook.worksheets.add("Reconciled Inventory");
const reconciliation = workbook.worksheets.add("Reconciliation Detail");
const needsReview = workbook.worksheets.add("Needs Review");
const d202Check = workbook.worksheets.add("D202 Visual Check");
workbook.comments.setSelf({ displayName: "Alejandro Acosta" });

const headers = [
  "Photo File",
  "Manufacturer",
  "Series Name",
  "Type/Model Code",
  "Canonical Model Key",
  "Original Model Field",
  "MTM",
  "Serial Number",
  "FRU Number",
  "Manufacture Date",
  "Model Reconciliation Status",
  "Model Identification Basis",
  "Record Review Status",
  "Record Review Notes",
  "Reconciliation Scope",
  "Source Photo Path",
];

const toRow = (row) => [
  row.photo_file,
  row.manufacturer,
  row.series_name,
  row.type_model_code,
  row.canonical_model_key,
  row.original_model_field,
  row.mtm,
  row.serial_number,
  row.fru_number,
  row.manufacture_date ? new Date(`${row.manufacture_date}T00:00:00`) : null,
  row.model_reconciliation_status,
  row.model_identification_basis,
  row.review_status,
  row.review_notes,
  row.reconciliation_scope,
  row.source_path,
];

function styleDetailSheet(sheet, rows, tableName, headerColor) {
  sheet.getRange("A1:P1").values = [headers];
  if (rows.length) sheet.getRange(`A2:P${rows.length + 1}`).values = rows.map(toRow);
  sheet.tables.add(`A1:P${rows.length + 1}`, true, tableName);
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);
  sheet.showGridLines = false;
  sheet.getRange("A1:P1").format = {
    fill: headerColor,
    font: { bold: true, color: "#FFFFFF" },
    rowHeight: 30,
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:P${rows.length + 1}`).format.borders = {
    insideHorizontal: { style: "thin", color: "#E5E7EB" },
    bottom: { style: "thin", color: "#CBD5E1" },
  };
  sheet.getRange(`J2:J${rows.length + 1}`).format.numberFormat = "yyyy-mm-dd";
  sheet.getRange(`K2:O${rows.length + 1}`).format.wrapText = true;
  const widths = [16, 13, 23, 18, 42, 18, 18, 17, 16, 16, 24, 40, 18, 34, 34, 62];
  widths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, rows.length + 1, 1).format.columnWidth = width;
  });
  sheet.getRange(`K2:K${rows.length + 1}`).conditionalFormats.add("containsText", {
    text: "Inferred",
    format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } },
  });
  sheet.getRange(`K2:K${rows.length + 1}`).conditionalFormats.add("containsText", {
    text: "Unresolved",
    format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
  });
  sheet.getRange(`M2:M${rows.length + 1}`).conditionalFormats.add("containsText", {
    text: "Needs Review",
    format: { fill: "#FFF7ED", font: { color: "#9A3412", bold: true } },
  });
}

styleDetailSheet(inventory, records, "ReconciledMonitorInventory", "#17324D");

const reconciliationRows = records.filter((row) => row.reconciliation_scope);
styleDetailSheet(reconciliation, reconciliationRows, "ReconciliationDetail", "#7C2D12");

const reviewRows = records.filter((row) => row.review_status === "Needs Review");
styleDetailSheet(needsReview, reviewRows, "NeedsReviewDetail", "#92400E");

const d202Rows = records.filter((row) => row.original_model_field === "D20215FT0");
styleDetailSheet(d202Check, d202Rows, "D202VisualCheck", "#155E75");

summary.showGridLines = false;
summary.getRange("A1:G1").merge();
summary.getRange("A1").values = [["Monitor Inventory — Model Reconciliation"]];
summary.getRange("A1:G1").format = {
  fill: "#17324D",
  font: { bold: true, color: "#FFFFFF", size: 18 },
  rowHeight: 38,
};

summary.getRange("A3:B10").values = [
  ["Coverage Metric", "Count"],
  ["Photos processed", null],
  ["High-confidence serials", null],
  ["Low-confidence serials", null],
  ["Total serial values", null],
  ["Serials missing", null],
  ["Record-level Needs Review", null],
  ["Model key unresolved", null],
];
summary.getRange("B4").formulas = [[`=COUNTA('Reconciled Inventory'!$A$2:$A$191)`]];
summary.getRange("B5").formulas = [[`=B7-B6`]];
summary.getRange("B6").formulas = [[`=COUNTIF('Reconciled Inventory'!$N$2:$N$191,"LOW-CONFIDENCE SERIAL")`]];
summary.getRange("B7").formulas = [[`=B4-COUNTBLANK('Reconciled Inventory'!$H$2:$H$191)`]];
summary.getRange("B8").formulas = [[`=COUNTBLANK('Reconciled Inventory'!$H$2:$H$191)`]];
summary.getRange("B9").formulas = [[`=COUNTIF('Reconciled Inventory'!$M$2:$M$191,"Needs Review")`]];
summary.getRange("B10").formulas = [[`=COUNTIF('Reconciled Inventory'!$K$2:$K$191,"Unresolved")`]];

summary.getRange("D3:G8").values = [
  ["Series Name", "Type/Model Code", "All Rows", "Confirmed/Extracted"],
  ["ThinkVision T2254pC", "T2254pC", null, null],
  ["ThinkVision T22i-10", "A16215FT0", null, null],
  ["ThinkVision T22i-20", "D20215FT0", null, null],
  ["ThinkVision P24h-30", "D22238QP0", null, null],
  ["Unresolved", "", null, null],
];
for (let row = 4; row <= 7; row += 1) {
  summary.getRange(`F${row}`).formulas = [[`=COUNTIF('Reconciled Inventory'!$E$2:$E$191,D${row}&" | "&E${row})`]];
  summary.getRange(`G${row}`).formulas = [[`=COUNTIFS('Reconciled Inventory'!$E$2:$E$191,D${row}&" | "&E${row},'Reconciled Inventory'!$K$2:$K$191,"<>Inferred - review")`]];
}
summary.getRange("F8").formulas = [[`=COUNTBLANK('Reconciled Inventory'!$E$2:$E$191)`]];
summary.getRange("G8").values = [[0]];

summary.getRange("A3:B3").format = { fill: "#DCE6F1", font: { bold: true, color: "#17324D" } };
summary.getRange("D3:G3").format = { fill: "#DCE6F1", font: { bold: true, color: "#17324D" } };
summary.getRange("A3:B10").format.borders = { preset: "outside", style: "thin", color: "#94A3B8" };
summary.getRange("D3:G8").format.borders = { preset: "outside", style: "thin", color: "#94A3B8" };
summary.getRange("B4:B10").format = { font: { bold: true, size: 14, color: "#17324D" }, numberFormat: "#,##0" };
summary.getRange("F4:G8").format.numberFormat = "#,##0";

summary.getRange("A12:G14").merge();
summary.getRange("A12").values = [[
  "Final model reconciliation: all 190 photos have assigned models. Quantities are ThinkVision T2254pC 151, ThinkVision T22i-10 25, ThinkVision T22i-20 5, and ThinkVision P24h-30 9."
]];
summary.getRange("A12:G14").format = {
  fill: "#ECFDF5",
  font: { color: "#065F46" },
  wrapText: true,
  verticalAlignment: "top",
  borders: { preset: "outside", style: "thin", color: "#6EE7B7" },
};
summary.getRange("A16:G18").merge();
summary.getRange("A16").values = [[
  "Serial status: 190 rows contain a serial value. IMG_6383.JPG and IMG_6408.JPG are explicitly flagged as low-confidence best guesses and should not be represented as equivalent to the 188 high-confidence serials in a customs annex."
]];
summary.getRange("A16:G18").format = {
  fill: "#FFF7ED",
  font: { color: "#9A3412" },
  wrapText: true,
  verticalAlignment: "top",
  borders: { preset: "outside", style: "thin", color: "#FDBA74" },
};

const summaryWidths = [25, 15, 3, 25, 19, 13, 20];
summaryWidths.forEach((width, index) => summary.getRangeByIndexes(0, index, 18, 1).format.columnWidth = width);

const previews = [
  ["summary_reconciled_preview.png", "Summary", "A1:G18", 1.4],
  ["reconciled_inventory_preview.png", "Reconciled Inventory", "A1:P12", 1.0],
  ["reconciliation_detail_preview.png", "Reconciliation Detail", "A1:P12", 1.0],
  ["needs_review_preview.png", "Needs Review", "A1:P12", 1.0],
  ["d202_visual_check_preview.png", "D202 Visual Check", "A1:P6", 1.0],
];
for (const [fileName, sheetName, range, scale] of previews) {
  const preview = await workbook.render({ sheetName, range, scale, format: "png" });
  await fs.writeFile(path.join(baseDir, fileName), new Uint8Array(await preview.arrayBuffer()));
}

console.log((await workbook.inspect({
  kind: "table",
  range: "Summary!A1:G18",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 10,
})).ndjson);
console.log((await workbook.inspect({
  kind: "table",
  range: "D202 Visual Check!A1:P6",
  include: "values,formulas",
  tableMaxRows: 8,
  tableMaxCols: 16,
})).ndjson);
console.log((await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 200 },
  summary: "final formula error scan",
})).ndjson);

await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "monitor_inventory_reconciled.xlsx"));
console.log(path.join(outputDir, "monitor_inventory_reconciled.xlsx"));

// Dedicated 21-row handoff for resolving model assignments before Sunset quantities are finalized.
const assignmentRows = records.filter((row) =>
  row.original_model_reconciliation_status === "Inferred - review" ||
  row.original_model_reconciliation_status === "Unresolved"
);
const reviewWorkbook = Workbook.create();
const reviewSummary = reviewWorkbook.worksheets.add("Review Summary");
const assignments = reviewWorkbook.worksheets.add("21 Model Assignments");
reviewWorkbook.comments.setSelf({ displayName: "Alejandro Acosta" });

const assignmentHeaders = [
  "Review Bucket",
  "Photo File",
  "Proposed Series",
  "Proposed Type/Model",
  "MTM",
  "Serial Number",
  "FRU Number",
  "Manufacture Date",
  "Identification Basis",
  "Original Model Field",
  "Record Review Notes",
  "Source Photo Path",
  "Resolution Status",
  "Final Series",
  "Final Type/Model",
  "Reviewer Notes",
];
const visualModelResolutions = {
  "IMG_6306.JPG": ["ThinkVision T22i-10", "A16215FT0"],
  "IMG_6326.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6375.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6376.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6383.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6387.JPG": ["ThinkVision T22i-10", "A16215FT0"],
  "IMG_6393.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6397.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6401.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6403.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6404.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6408.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6410.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6411.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6416.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6424.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6442.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6445.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6448.JPG": ["ThinkVision T2254pC", "T2254pC"],
  "IMG_6459.JPG": ["ThinkVision T22i-10", "A16215FT0"],
  "IMG_6463.JPG": ["ThinkVision T2254pC", "T2254pC"],
};
const assignmentData = assignmentRows.map((row) => [
  row.original_model_reconciliation_status === "Unresolved" ? "Fully Unresolved" : "Identifier-Based Inference",
  row.photo_file,
  row.series_name,
  row.type_model_code,
  row.mtm,
  row.serial_number,
  row.fru_number,
  row.manufacture_date ? new Date(`${row.manufacture_date}T00:00:00`) : null,
  row.model_identification_basis,
  row.original_model_field,
  row.review_notes,
  row.source_path,
  visualModelResolutions[row.photo_file] ? "Confirmed" : "Unresolved",
  visualModelResolutions[row.photo_file]?.[0] ?? "",
  visualModelResolutions[row.photo_file]?.[1] ?? "",
  visualModelResolutions[row.photo_file]
    ? "Confirmed by direct visual review of the printed source-photo label on 2026-07-27."
    : "Printed model identifiers remain unreadable.",
]);

assignments.getRange("A1:P1").values = [assignmentHeaders];
assignments.getRange(`A2:P${assignmentRows.length + 1}`).values = assignmentData;
assignments.tables.add(`A1:P${assignmentRows.length + 1}`, true, "ModelAssignmentReview");
assignments.freezePanes.freezeRows(1);
assignments.freezePanes.freezeColumns(2);
assignments.showGridLines = false;
assignments.getRange("A1:P1").format = {
  fill: "#7C2D12",
  font: { bold: true, color: "#FFFFFF" },
  rowHeight: 30,
};
assignments.getRange(`H2:H${assignmentRows.length + 1}`).format.numberFormat = "yyyy-mm-dd";
assignments.getRange(`I2:P${assignmentRows.length + 1}`).format.wrapText = true;
const assignmentWidths = [25, 16, 24, 20, 18, 18, 16, 16, 38, 20, 36, 62, 18, 24, 20, 36];
assignmentWidths.forEach((width, index) => {
  assignments.getRangeByIndexes(0, index, assignmentRows.length + 1, 1).format.columnWidth = width;
});
assignments.getRange(`M2:M${assignmentRows.length + 1}`).dataValidation = {
  rule: { type: "list", values: ["Pending", "Confirmed", "Corrected", "Unresolved"] },
};
assignments.getRange(`A2:A${assignmentRows.length + 1}`).conditionalFormats.add("containsText", {
  text: "Fully Unresolved",
  format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
});
assignments.getRange(`A2:A${assignmentRows.length + 1}`).conditionalFormats.add("containsText", {
  text: "Identifier-Based Inference",
  format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } },
});

reviewSummary.showGridLines = false;
reviewSummary.getRange("A1:F1").merge();
reviewSummary.getRange("A1").values = [["Model Assignment Review — 21 Units"]];
reviewSummary.getRange("A1:F1").format = {
  fill: "#17324D",
  font: { bold: true, color: "#FFFFFF", size: 18 },
  rowHeight: 38,
};
reviewSummary.getRange("A3:B11").values = [
  ["Review Bucket", "Count"],
  ["Identifier-Based Inference", null],
  ["Fully Unresolved", null],
  ["Total", null],
  ["", ""],
  ["Resolution Outcome", "Count"],
  ["Confirmed by Visual Review", null],
  ["Still Unresolved", null],
  ["Final Assigned Total", null],
];
reviewSummary.getRange("B4").formulas = [[`=COUNTIF('21 Model Assignments'!$A$2:$A$22,A4)`]];
reviewSummary.getRange("B5").formulas = [[`=COUNTIF('21 Model Assignments'!$A$2:$A$22,A5)`]];
reviewSummary.getRange("B6").formulas = [["=SUM(B4:B5)"]];
reviewSummary.getRange("B9").formulas = [[`=COUNTIF('21 Model Assignments'!$M$2:$M$22,"Confirmed")`]];
reviewSummary.getRange("B10").formulas = [[`=COUNTIF('21 Model Assignments'!$M$2:$M$22,"Unresolved")`]];
reviewSummary.getRange("B11").formulas = [["=B9"]];
reviewSummary.getRange("A3:B3").format = { fill: "#DCE6F1", font: { bold: true, color: "#17324D" } };
reviewSummary.getRange("A8:B8").format = { fill: "#DCE6F1", font: { bold: true, color: "#17324D" } };
reviewSummary.getRange("A3:B6").format.borders = { preset: "outside", style: "thin", color: "#94A3B8" };
reviewSummary.getRange("A8:B11").format.borders = { preset: "outside", style: "thin", color: "#94A3B8" };
reviewSummary.getRange("B4:B6").format = { font: { bold: true, size: 14 }, numberFormat: "#,##0" };
reviewSummary.getRange("B9:B11").format = { font: { bold: true, size: 14 }, numberFormat: "#,##0" };
reviewSummary.getRange("A13:F16").merge();
reviewSummary.getRange("A13").values = [[
  "Completed 2026-07-27: all 21 model assignments were confirmed by direct visual review of the printed source-photo labels. Final quantities across all 190 photos: ThinkVision T2254pC 151; ThinkVision T22i-10 25; ThinkVision T22i-20 5; ThinkVision P24h-30 9."
]];
reviewSummary.getRange("A13:F16").format = {
  fill: "#ECFDF5",
  font: { color: "#065F46" },
  wrapText: true,
  verticalAlignment: "top",
  borders: { preset: "outside", style: "thin", color: "#6EE7B7" },
};
reviewSummary.getRange("A1:F16").format.columnWidth = 20;
reviewSummary.getRange("A:A").format.columnWidth = 30;

const reviewSummaryPreview = await reviewWorkbook.render({
  sheetName: "Review Summary",
  range: "A1:F16",
  scale: 1.5,
  format: "png",
});
await fs.writeFile(path.join(baseDir, "model_assignment_review_summary_preview.png"), new Uint8Array(await reviewSummaryPreview.arrayBuffer()));
const assignmentPreview = await reviewWorkbook.render({
  sheetName: "21 Model Assignments",
  range: "A1:P22",
  scale: 1,
  format: "png",
});
await fs.writeFile(path.join(baseDir, "model_assignment_review_detail_preview.png"), new Uint8Array(await assignmentPreview.arrayBuffer()));

console.log((await reviewWorkbook.inspect({
  kind: "table",
  range: "Review Summary!A1:F16",
  include: "values,formulas",
  tableMaxRows: 15,
  tableMaxCols: 8,
})).ndjson);
console.log((await reviewWorkbook.inspect({
  kind: "table",
  range: "21 Model Assignments!A1:P22",
  include: "values,formulas",
  tableMaxRows: 25,
  tableMaxCols: 16,
  maxChars: 9000,
})).ndjson);
console.log((await reviewWorkbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "review workbook formula error scan",
})).ndjson);

const reviewOutput = await SpreadsheetFile.exportXlsx(reviewWorkbook);
await reviewOutput.save(path.join(outputDir, "monitor_model_assignment_review_21.xlsx"));
console.log(path.join(outputDir, "monitor_model_assignment_review_21.xlsx"));
