import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = "C:/Users/AlejandroAcosta/Documents/ai-workstation";
const TMP = `${ROOT}/tmp/presentations/scott_matt_onboarding`;
const ASSETS = `${TMP}/assets`;
const OUT = `${ROOT}/outputs/onboarding`;
const FINAL = `${OUT}/InterWork_Operations_Onboarding_Scott_Matt_READABLE.pptx`;

const W = 1280;
const H = 720;
const RED = "#C4474A";
const RED_DARK = "#9F3035";
const RED_LIGHT = "#D96567";
const WHITE = "#FFFFFF";
const INK = "#191919";
const MUTED = "#F2DCDD";
const NAVY = "#172634";
const BLUE = "#2D6CDF";
const GREEN = "#2CA56B";
const ORANGE = "#F39A3E";
const GRID = "#D56669";

async function bytes(file) {
  const b = await fs.readFile(file);
  return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
}

function addRect(slide, x, y, w, h, fill, radius = 0, line = "none") {
  return slide.shapes.add({
    geometry: radius ? "roundRect" : "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
    ...(radius ? { borderRadius: radius } : {}),
  });
}

function addText(slide, text, x, y, w, h, size, color = WHITE, bold = false, align = "left") {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: size,
    fontFamily: "Aptos",
    color,
    bold,
    alignment: align,
  };
  return shape;
}

function addGrid(slide, fill = RED) {
  slide.background.fill = fill;
  for (let x = -20; x < W + 100; x += 105) {
    const line = addRect(slide, x, 0, 2, H, GRID);
    line.rotation = 5;
  }
  for (let y = -30; y < H + 60; y += 82) {
    const line = addRect(slide, 0, y, W, 2, GRID);
    line.rotation = 5;
  }
}

function addFooter(slide, section, number) {
  addText(slide, "» INTERWORK  OFFICE SOLUTIONS", 44, 674, 360, 22, 13, WHITE, true);
  addText(slide, section.toUpperCase(), 936, 674, 250, 22, 12, MUTED, true, "right");
  addText(slide, String(number).padStart(2, "0"), 1190, 674, 44, 22, 12, WHITE, true, "right");
}

function addTitle(slide, title, subtitle = "") {
  addText(slide, title, 54, 42, 900, 58, 36, WHITE, true);
  if (subtitle) addText(slide, subtitle, 56, 100, 980, 38, 18, WHITE, true);
}

async function addImage(slide, file, x, y, w, h, opts = {}) {
  const ext = path.extname(file).toLowerCase();
  const contentType =
    ext === ".jpg" || ext === ".jpeg"
      ? "image/jpeg"
      : ext === ".svg"
        ? "image/svg+xml"
        : "image/png";
  return slide.images.add({
    blob: await bytes(file),
    contentType,
    alt: opts.alt || path.basename(file),
    fit: opts.fit || "cover",
    position: { left: x, top: y, width: w, height: h },
    ...(opts.crop ? { crop: opts.crop } : {}),
    ...(opts.geometry ? { geometry: opts.geometry } : {}),
    ...(opts.borderRadius ? { borderRadius: opts.borderRadius } : {}),
  });
}

function addNotes(slide, lines, sources) {
  const sourceBlock = sources.length ? `\n\n[Sources]\n${sources.map((s) => `- ${s}`).join("\n")}` : "";
  slide.speakerNotes.textFrame.setText(`${lines.join("\n")}${sourceBlock}`);
  slide.speakerNotes.setVisible(true);
}

function addRole(slide, x, y, size, initials, title, detail, fill) {
  slide.shapes.add({
    geometry: "ellipse",
    position: { left: x, top: y, width: size, height: size },
    fill,
    line: { style: "solid", fill: WHITE, width: 3 },
  });
  addText(slide, initials, x, y + 24, size, 38, 26, WHITE, true, "center");
  addText(slide, title, x - 42, y + size + 12, size + 84, 30, 18, WHITE, true, "center");
  addText(slide, detail, x - 68, y + size + 43, size + 136, 44, 16, WHITE, true, "center");
}

async function addLogoTile(slide, cfg) {
  const { x, y, label, color, file, initials, sublabel } = cfg;
  slide.shapes.add({
    geometry: "ellipse",
    position: { left: x, top: y, width: 82, height: 82 },
    fill: WHITE,
    line: { style: "solid", fill: "#E8E8E8", width: 1 },
  });
  if (file) {
    await addImage(slide, file, x + 20, y + 20, 42, 42, { fit: "contain", alt: `${label} logo` });
  } else {
    slide.shapes.add({
      geometry: "ellipse",
      position: { left: x + 16, top: y + 16, width: 50, height: 50 },
      fill: color,
      line: { style: "solid", fill: "none", width: 0 },
    });
    addText(slide, initials, x + 16, y + 28, 50, 26, 20, WHITE, true, "center");
  }
  addText(slide, label, x - 38, y + 91, 158, 26, 16, WHITE, true, "center");
  if (sublabel) addText(slide, sublabel, x - 58, y + 117, 198, 36, 15, WHITE, true, "center");
}

async function main() {
  await fs.mkdir(OUT, { recursive: true });
  await fs.mkdir(`${TMP}/rendered`, { recursive: true });

  const deck = Presentation.create({ slideSize: { width: W, height: H } });

  // 1 — Welcome
  {
    const slide = deck.slides.add();
    await addImage(slide, `${TMP}/atlanta-01.png`, 0, 0, W, H, {
      alt: "InterWork Office Solutions visual reference cover",
    });
    addRect(slide, 0, 530, W, 190, "#8F2A2FCC");
    addText(slide, "WELCOME, SCOTT + MATT", 58, 548, 810, 62, 38, WHITE, true);
    addText(slide, "Operations Coordinator Onboarding", 60, 610, 670, 36, 22, WHITE, false);
    addText(slide, "Learn the business. Master the workflow. Own the outcome.", 60, 653, 720, 30, 17, MUTED, false);
    addText(slide, "AUGUST 2026", 1010, 615, 208, 30, 15, WHITE, true, "right");
    addNotes(
      slide,
      [
        "Welcome Scott and Matt and explain that this is a practical introduction to how InterWork operates.",
        "Set the expectation: business and workflow come before systems and AI.",
      ],
      [
        "User-provided visual reference: AtlantaProject_Presentation (4).pdf, slide 1.",
        `${ROOT}/docs/onboarding/operations_coordinator/README.md`,
      ],
    );
  }

  // 2 — Company purpose
  {
    const slide = deck.slides.add();
    await addImage(slide, `${ASSETS}/company_workflow.png`, 0, 0, W, H, {
      alt: "InterWork project coordination and field execution",
    });
    addRect(slide, 0, 0, 520, H, "#8F2A2FDC");
    addText(slide, "WE MAKE WORKPLACE\nCHANGE HAPPEN", 56, 74, 430, 126, 39, WHITE, true);
    addText(slide, "From planning to closeout, InterWork coordinates the people, places and details that keep projects moving.", 58, 221, 405, 94, 20, WHITE, false);
    const services = [
      ["MOVE", "Relocations + restacks"],
      ["REMOVE", "Decommissions + disposal"],
      ["INSTALL", "Furniture + service calls"],
      ["REPORT", "Field evidence + closeout"],
    ];
    services.forEach((item, i) => {
      addText(slide, item[0], 60, 350 + i * 65, 140, 28, 17, WHITE, true);
      addText(slide, item[1], 206, 350 + i * 65, 250, 30, 17, WHITE, true);
    });
    addFooter(slide, "The company", 2);
    addNotes(
      slide,
      [
        "Describe InterWork as a commercial furniture moving, installation and project-coordination company.",
        "Explain that clients are usually facilities and real-estate teams managing workplace change.",
        "Use one personal example of a project that went well because coordination was strong.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/01_MODULE1_INTERWORK_FUNDAMENTALS.md`,
        "AI-generated visual created for this deck; no external visual source.",
      ],
    );
  }

  // 3 — People map
  {
    const slide = deck.slides.add();
    addGrid(slide);
    addTitle(slide, "EVERY PROJECT IS A TEAM SPORT", "Clear ownership keeps information, commitments and field execution aligned.");

    // Connector band sits behind roles.
    addRect(slide, 118, 331, 1044, 8, "#E79899");
    [232, 432, 632, 832, 1032].forEach((x) => addRect(slide, x, 225, 3, 110, "#E79899"));

    slide.shapes.add({
      geometry: "ellipse",
      position: { left: 546, top: 270, width: 188, height: 188 },
      fill: NAVY,
      line: { style: "solid", fill: WHITE, width: 4 },
    });
    addText(slide, "PROJECT", 560, 307, 160, 32, 20, WHITE, true, "center");
    addText(slide, "#", 560, 344, 160, 52, 40, WHITE, true, "center");
    addText(slide, "one shared identifier", 548, 400, 184, 28, 16, WHITE, true, "center");

    addRole(slide, 172, 168, 120, "AM", "Account Manager", "Quote + client relationship", ORANGE);
    addRole(slide, 372, 168, 120, "OP", "Office PM", "Schedule + coordination", BLUE);
    addRole(slide, 772, 168, 120, "FP", "Field PM", "On-site execution", GREEN);
    addRole(slide, 972, 168, 120, "POC", "Client / Building", "Access + decisions", "#7654C4");
    addRole(slide, 572, 486, 120, "TEAM", "Crew / Partner", "Physical work + evidence", RED_DARK);

    addText(slide, "SCOTT + MATT: OPERATIONS", 286, 574, 326, 28, 16, WHITE, true, "center");
    addText(slide, "FRANCISCO: FIELD ESCALATION", 685, 574, 328, 28, 16, WHITE, true, "center");
    addFooter(slide, "Who is who", 3);
    addNotes(
      slide,
      [
        "Explain each role using a current project example.",
        "Account Manager owns the quote and client relationship. Office PM owns administrative coordination. Field PM leads execution.",
        "Client and building contacts may be different people. Crew or vendor details remain internal in client-facing communication.",
        "The project number connects every role and every source.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/01_MODULE1_INTERWORK_FUNDAMENTALS.md`,
        `${ROOT}/memory/references/interwork_people_map.md`,
      ],
    );
  }

  // 4 — Lifecycle
  {
    const slide = deck.slides.add();
    addGrid(slide);
    addTitle(slide, "ONE PROJECT NUMBER. SIX CONTROL POINTS.", "The workflow protects the client experience before, during and after execution.");

    const stages = [
      ["01", "QUOTE", "Scope + project number", ORANGE],
      ["02", "SCHEDULE", "Calendar + record", "#5D8CE6"],
      ["03", "ASSIGN", "Office PM + field team", "#7654C4"],
      ["04", "CONFIRM", "Client + access + crew", "#E5B53F"],
      ["05", "EXECUTE", "Field PM + FastField", GREEN],
      ["06", "CLOSE", "WC report + completion", NAVY],
    ];
    const xs = [50, 255, 460, 665, 870, 1075];
    // Arrows first so they remain behind the nodes.
    for (let i = 0; i < xs.length - 1; i++) {
      slide.shapes.add({
        geometry: "chevron",
        position: { left: xs[i] + 148, top: 324, width: 56, height: 48 },
        fill: "#F0B4B5",
        line: { style: "solid", fill: "none", width: 0 },
      });
    }
    stages.forEach((s, i) => {
      slide.shapes.add({
        geometry: "ellipse",
        position: { left: xs[i], top: 246, width: 156, height: 156 },
        fill: s[3],
        line: { style: "solid", fill: WHITE, width: 3 },
      });
      addText(slide, s[0], xs[i], 267, 156, 36, 25, WHITE, true, "center");
      addText(slide, s[1], xs[i], 315, 156, 34, 19, WHITE, true, "center");
      addText(slide, s[2], xs[i] - 20, 414, 196, 54, 16, WHITE, true, "center");
    });
    addText(slide, "CONFIRMED FACTS MOVE FORWARD. OPEN QUESTIONS STAY VISIBLE.", 178, 529, 924, 42, 21, WHITE, true, "center");
    addFooter(slide, "The workflow", 4);
    addNotes(
      slide,
      [
        "Walk through the six stages in order.",
        "Emphasize that scheduled does not mean fully confirmed.",
        "FastField is submitted by the field PM after execution. Closeout includes the work-completion report and completion communication.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/02_MODULE2_PROJECT_LIFECYCLE_AND_EXAMPLES.md`,
        `${ROOT}/memory/company_knowledge/OPERATING_WORKFLOW.md`,
      ],
    );
  }

  // 5 — Project examples
  {
    const slide = deck.slides.add();
    addGrid(slide);
    addTitle(slide, "THE WORK CHANGES. THE COORDINATION DISCIPLINE DOESN'T.", "Four project types show the range Scott and Matt will learn to manage.");
    const image = `${ASSETS}/project_collage.png`;
    const panels = [
      { x: 46, crop: { left: 0, top: 0, right: 0.73, bottom: 0 }, label: "DECOMMISSION", sub: "Remove + recycle", project: "#7492" },
      { x: 348, crop: { left: 0.25, top: 0, right: 0.48, bottom: 0 }, label: "RELOCATION", sub: "Move + reinstall", project: "#7350" },
      { x: 650, crop: { left: 0.50, top: 0, right: 0.23, bottom: 0 }, label: "E-WASTE", sub: "Sort + dispose", project: "#7594" },
      { x: 952, crop: { left: 0.73, top: 0, right: 0, bottom: 0 }, label: "INSTALLATION", sub: "Deliver + complete", project: "#7547" },
    ];
    for (const p of panels) {
      await addImage(slide, image, p.x, 165, 282, 370, {
        crop: p.crop,
        geometry: "roundRect",
        borderRadius: 18,
        alt: p.label,
      });
      addRect(slide, p.x, 447, 282, 88, "#8F2A2FE8", 18);
      addText(slide, p.label, p.x + 18, 465, 214, 26, 17, WHITE, true);
      addText(slide, p.sub, p.x + 18, 494, 210, 28, 16, WHITE, true);
      addText(slide, p.project, p.x + 214, 480, 54, 26, 14, WHITE, true, "right");
    }
    addText(slide, "Different scope. Same habits: verify • confirm • communicate • document", 117, 576, 1046, 38, 20, WHITE, true, "center");
    addFooter(slide, "Project examples", 5);
    addNotes(
      slide,
      [
        "Use the four examples as short stories, not detailed case studies.",
        "Call out one coordination judgment from each: separate internal issues from client communication; use the latest confirmed scope; keep excluded scope excluded; resolve drawing/access discrepancies before field work.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/02_MODULE2_PROJECT_LIFECYCLE_AND_EXAMPLES.md`,
        "AI-generated project collage created for this deck; no external visual source.",
      ],
    );
  }

  // 6 — Systems
  {
    const slide = deck.slides.add();
    addGrid(slide);
    addTitle(slide, "EACH SYSTEM HAS ONE CLEAR JOB", "Scott and Matt will learn what to trust, where to work and when to escalate.");

    // Flow arrows first.
    [228, 450, 672, 894].forEach((x) => {
      slide.shapes.add({
        geometry: "chevron",
        position: { left: x, top: 286, width: 54, height: 48 },
        fill: "#F0B4B5",
        line: { style: "solid", fill: "none", width: 0 },
      });
    });
    await addLogoTile(slide, { x: 90, y: 230, label: "QuickQuo", initials: "Q", color: ORANGE, sublabel: "Quote + project #" });
    await addLogoTile(slide, { x: 310, y: 230, label: "Smartsheet", initials: "✓", color: BLUE, sublabel: "Schedule" });
    await addLogoTile(slide, { x: 530, y: 230, label: "Command Center", initials: "CC", color: RED_DARK, sublabel: "Operational view" });
    await addLogoTile(slide, { x: 750, y: 230, label: "Supabase", file: `${ASSETS}/supabase_512.png`, sublabel: "Operational truth" });
    await addLogoTile(slide, { x: 970, y: 230, label: "FastField", initials: "FF", color: GREEN, sublabel: "Field evidence" });

    await addLogoTile(slide, { x: 250, y: 460, label: "Outlook", file: `${ASSETS}/outlook_512.png`, sublabel: "Client communication" });
    await addLogoTile(slide, { x: 468, y: 460, label: "Teams", file: `${ASSETS}/microsoftteams_512.png`, sublabel: "Internal coordination" });
    await addLogoTile(slide, { x: 686, y: 460, label: "GitHub", file: `${ASSETS}/github_512.png`, sublabel: "Shared memory" });
    await addLogoTile(slide, { x: 904, y: 460, label: "Claude", file: `${ASSETS}/anthropic_512.png`, sublabel: "Research + drafting" });

    addFooter(slide, "Systems", 6);
    addNotes(
      slide,
      [
        "QuickQuo creates the quote and project number. Smartsheet is the schedule. Command Center displays Supabase. Supabase is operational truth. FastField captures field evidence.",
        "Outlook and Teams are human communication tools. GitHub stores durable project memory. Claude helps research and draft, but does not replace operational judgment.",
        "Do not teach passwords or administrative access on this slide; access is staged separately.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/03_MODULE3_SYSTEMS_AND_SOURCES_OF_TRUTH.md`,
        `${ROOT}/docs/onboarding/operations_coordinator/04_MODULE4_AI_AND_SHARED_KNOWLEDGE.md`,
        "Supabase, GitHub and Anthropic marks: Simple Icons (cdn.jsdelivr.net/npm/simple-icons@v15).",
        "Teams and Outlook marks: Iconify icon catalog.",
      ],
    );
  }

  // 7 — AI and shared knowledge
  {
    const slide = deck.slides.add();
    addGrid(slide, NAVY);
    addText(slide, "AI COMES AFTER THE FUNDAMENTALS", 54, 45, 840, 58, 36, WHITE, true);
    addText(slide, "It helps Scott and Matt find, prepare and preserve the work—not guess or bypass the workflow.", 56, 105, 1000, 40, 18, "#C7D5E3", true);

    const items = [
      ["FIND", "Project number first", BLUE],
      ["UNDERSTAND", "Live state + project context", "#7654C4"],
      ["DRAFT", "Briefs, emails and dispatches", ORANGE],
      ["REVIEW", "Human judgment before action", RED_LIGHT],
      ["PRESERVE", "Update shared project memory", GREEN],
    ];
    items.forEach((item, i) => {
      const x = 62 + i * 238;
      addRect(slide, x, 230, 205, 252, "#FFFFFF10", 18, "#FFFFFF36");
      slide.shapes.add({
        geometry: "ellipse",
        position: { left: x + 62, top: 254, width: 82, height: 82 },
        fill: item[2],
        line: { style: "solid", fill: WHITE, width: 2 },
      });
      addText(slide, String(i + 1), x + 62, 278, 82, 32, 24, WHITE, true, "center");
      addText(slide, item[0], x + 12, 357, 181, 32, 19, WHITE, true, "center");
      addText(slide, item[1], x + 12, 400, 181, 64, 18, WHITE, true, "center");
    });
    addText(slide, "DRAFT FREELY", 185, 544, 270, 32, 21, WHITE, true, "center");
    addText(slide, "SEND / WRITE ONLY AFTER APPROVAL", 512, 544, 586, 32, 21, "#F3C16C", true, "center");
    addText(slide, "No invented facts • No secrets in chat • No silent conflict resolution", 156, 594, 970, 38, 18, WHITE, true, "center");
    addFooter(slide, "Shared knowledge", 7);
    addNotes(
      slide,
      [
        "This is the first AI-focused slide. Reinforce that the company and workflow were intentionally taught first.",
        "Show the safe progression: find, understand, draft, review, preserve.",
        "During onboarding, all sends and live writes remain routed through Alejandro. Week 2 determines any future authority individually.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/04_MODULE4_AI_AND_SHARED_KNOWLEDGE.md`,
        `${ROOT}/memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md`,
      ],
    );
  }

  // 8 — Two-week plan
  {
    const slide = deck.slides.add();
    addGrid(slide);
    addText(slide, "TWO WEEKS: FROM CONTEXT TO CONTROLLED OWNERSHIP", 54, 42, 1160, 52, 34, WHITE, true);
    addText(slide, "Scott and Matt train together, practice independently and earn trust individually.", 56, 101, 1040, 34, 18, MUTED, true);

    const phases = [
      ["DAY 1", "COMPANY", "What we do + who is who", 75, ORANGE],
      ["DAY 2", "WORKFLOW", "Lifecycle + real examples", 295, "#7654C4"],
      ["DAY 3", "SYSTEMS", "Sources of truth + AI", 515, BLUE],
      ["DAYS 4–7", "PRACTICE", "Watch → do → reverse shadow", 735, GREEN],
      ["DAYS 8–10", "OWNERSHIP", "Small portfolio + review", 955, NAVY],
    ];
    addRect(slide, 110, 334, 1035, 12, "#F0B4B5");
    phases.forEach((p, i) => {
      slide.shapes.add({
        geometry: "ellipse",
        position: { left: p[3], top: 292, width: 96, height: 96 },
        fill: p[4],
        line: { style: "solid", fill: WHITE, width: 3 },
      });
      addText(slide, String(i + 1), p[3], 319, 96, 34, 25, WHITE, true, "center");
      addText(slide, p[0], p[3] - 32, 207, 160, 27, 15, MUTED, true, "center");
      addText(slide, p[1], p[3] - 52, 412, 200, 30, 18, WHITE, true, "center");
      addText(slide, p[2], p[3] - 64, 448, 224, 62, 18, WHITE, true, "center");
    });
    addRect(slide, 258, 548, 764, 66, "#8F2A2F", 18, WHITE);
    addText(slide, "DAY 10: INDIVIDUAL COMPETENCY + AUTHORITY DECISION", 279, 568, 722, 28, 19, WHITE, true, "center");
    addFooter(slide, "Training plan", 8);
    addNotes(
      slide,
      [
        "Explain that the plan deliberately moves from context to systems to controlled work.",
        "Scott and Matt will be evaluated separately even when working on the same scenario.",
        "All external communications and live updates remain reviewed during onboarding.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/05_MODULE5_TRAINING_AGENDA.md`,
        `${ROOT}/docs/onboarding/operations_coordinator/08_COMPETENCY_SIGNOFF_SCOTT.md`,
        `${ROOT}/docs/onboarding/operations_coordinator/08_COMPETENCY_SIGNOFF_MATT.md`,
      ],
    );
  }

  // 9 — Close / success
  {
    const slide = deck.slides.add();
    addGrid(slide);
    addText(slide, "SUCCESS LOOKS LIKE...", 70, 70, 780, 62, 39, WHITE, true);
    const words = [
      ["FIND THE TRUTH", 82, 190, ORANGE],
      ["CONFIRM THE DETAILS", 430, 190, BLUE],
      ["COMMUNICATE CLEARLY", 778, 190, "#7654C4"],
      ["PROTECT THE CLIENT", 82, 345, RED_DARK],
      ["ESCALATE EARLY", 430, 345, GREEN],
      ["LEAVE A CLEAN HANDOFF", 778, 345, NAVY],
    ];
    words.forEach((w) => {
      addRect(slide, w[1], w[2], 310, 112, "#FFFFFF10", 18, "#FFFFFF44");
      addRect(slide, w[1], w[2], 12, 112, w[3], 8);
      addText(slide, w[0], w[1] + 28, w[2] + 36, 260, 42, 19, WHITE, true);
    });
    addText(slide, "Learn the business first. The systems will help you execute it.", 126, 533, 1028, 48, 26, WHITE, true, "center");
    addText(slide, "WELCOME TO INTERWORK", 350, 608, 580, 38, 23, MUTED, true, "center");
    addFooter(slide, "Ready to begin", 9);
    addNotes(
      slide,
      [
        "Close by making success behavioral, not technical.",
        "Invite questions and transition Scott and Matt to Module 1 and the detailed onboarding materials.",
      ],
      [
        `${ROOT}/docs/onboarding/operations_coordinator/01_MODULE1_INTERWORK_FUNDAMENTALS.md`,
        `${ROOT}/docs/onboarding/operations_coordinator/05_MODULE5_TRAINING_AGENDA.md`,
      ],
    );
  }

  for (const [index, slide] of deck.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await deck.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(`${TMP}/rendered/${stem}.png`, new Uint8Array(await png.arrayBuffer()));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(`${TMP}/rendered/${stem}.layout.json`, await layout.text());
  }

  const montage = await deck.export({ format: "webp", montage: true, scale: 1 });
  await fs.writeFile(`${TMP}/rendered/deck-montage.webp`, new Uint8Array(await montage.arrayBuffer()));

  const pptx = await PresentationFile.exportPptx(deck);
  await pptx.save(FINAL);
  console.log(FINAL);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
