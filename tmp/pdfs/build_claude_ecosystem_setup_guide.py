from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing


ROOT = Path(r"C:\Users\AlejandroAcosta\Documents\ai-workstation")
OUT = ROOT / "outputs" / "onboarding" / "Scott_Matt_Claude_Bootstrap_and_Project_Setup_Guide.pdf"

RED = colors.HexColor("#C4474A")
RED_DARK = colors.HexColor("#922D32")
RED_SOFT = colors.HexColor("#F7E7E8")
NAVY = colors.HexColor("#172634")
BLUE = colors.HexColor("#2D6CDF")
GREEN = colors.HexColor("#2CA56B")
ORANGE = colors.HexColor("#F39A3E")
INK = colors.HexColor("#202124")
MUTED = colors.HexColor("#5E646B")
LINE = colors.HexColor("#E6D3D4")

REPO = "https://github.com/josealejandroam-afk/interwork-ai-workstation"
RAW = "https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/"
CLAUDE_DOWNLOAD = "https://claude.ai/download"
CLAUDE_PROJECTS_HELP = "https://support.anthropic.com/en/articles/9517075-what-are-projects"
DASHBOARD = "https://interwork-command-center.vercel.app/"


def link(label, url, color="#2D6CDF"):
    return f'<link href="{url}" color="{color}"><u>{label}</u></link>'


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=colors.white, alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverSub", fontName="Helvetica-Bold", fontSize=14, leading=19, textColor=colors.HexColor("#FBECEE"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1x", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=RED_DARK, spaceAfter=10))
styles.add(ParagraphStyle(name="H2x", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name="Bodyx", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyBold", fontName="Helvetica-Bold", fontSize=10.5, leading=15, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="Smallx", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED))
styles.add(ParagraphStyle(name="CardTitle", fontName="Helvetica-Bold", fontSize=12, leading=14, textColor=colors.white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CardBody", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=INK, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CodexCode", fontName="Courier-Bold", fontSize=8.5, leading=12, textColor=NAVY, backColor=colors.HexColor("#F3F5F7"), borderColor=colors.HexColor("#D7DCE1"), borderWidth=0.6, borderPadding=7, spaceAfter=6))
styles.add(ParagraphStyle(name="PasteCode", fontName="Courier", fontSize=7.7, leading=10.4, textColor=NAVY, backColor=colors.HexColor("#F3F5F7"), borderColor=BLUE, borderWidth=0.8, borderPadding=8, spaceAfter=6))
styles.add(ParagraphStyle(name="Prompt", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK, backColor=colors.HexColor("#FFF7E8"), borderColor=ORANGE, borderWidth=1, borderPadding=9, spaceAfter=8))
styles.add(ParagraphStyle(name="Warn", fontName="Helvetica-Bold", fontSize=9.5, leading=14, textColor=RED_DARK, backColor=RED_SOFT, borderColor=RED, borderWidth=1, borderPadding=9, spaceAfter=8))
styles.add(ParagraphStyle(name="Good", fontName="Helvetica-Bold", fontSize=9.5, leading=14, textColor=colors.HexColor("#146B47"), backColor=colors.HexColor("#EAF7F1"), borderColor=GREEN, borderWidth=1, borderPadding=9, spaceAfter=8))


class StepBadge(Flowable):
    def __init__(self, number, color=RED, size=26):
        super().__init__()
        self.number = str(number)
        self.color = color
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.circle(self.size / 2, self.size / 2, self.size / 2, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(self.size / 2, self.size / 2 - 4, self.number)


def step(number, title, body, color=RED):
    table = Table(
        [[StepBadge(number, color), Paragraph(f"<b>{title}</b><br/>{body}", styles["Bodyx"])]],
        colWidths=[0.42 * inch, 6.45 * inch],
        hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def colored_card(title, body, color, width=2.18 * inch):
    data = [[Paragraph(title, styles["CardTitle"])], [Paragraph(body, styles["CardBody"])]]
    t = Table(data, colWidths=[width], rowHeights=[0.45 * inch, 0.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (0, 1), (0, 1), colors.white),
        ("BOX", (0, 0), (-1, -1), 1, color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def qr(url, size=1.0 * inch):
    widget = QrCodeWidget(url)
    b = widget.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    drawing = Drawing(size, size, transform=[size / w, 0, 0, size / h, 0, 0])
    drawing.add(widget)
    return drawing


def page_chrome(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setFillColor(RED)
    canvas.rect(0, height - 0.54 * inch, width, 0.54 * inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(0.45 * inch, height - 0.34 * inch, ">> INTERWORK  OFFICE SOLUTIONS")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.45 * inch, 0.32 * inch, "Claude Bootstrap & Project Setup Guide - Scott and Matt")
    canvas.drawRightString(width - 0.45 * inch, 0.32 * inch, f"Page {doc.page}")
    canvas.restoreState()


def cover_chrome(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setFillColor(RED)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#D9686B"))
    canvas.setLineWidth(0.6)
    for x in range(-60, int(width) + 80, 54):
        canvas.line(x, 0, x + 58, height)
    for y in range(-20, int(height) + 40, 52):
        canvas.line(0, y, width, y + 26)
    canvas.restoreState()


def bullet(text):
    return Paragraph(f"<b>&bull;</b>&nbsp;&nbsp;{text}", styles["Bodyx"])


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUT), pagesize=letter,
        leftMargin=0.52 * inch, rightMargin=0.52 * inch,
        topMargin=0.78 * inch, bottomMargin=0.55 * inch,
        title="Scott & Matt - Claude Bootstrap and Project Setup Guide",
        author="InterWork Office Solutions",
    )
    normal_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    cover_frame = Frame(0.62 * inch, 0.8 * inch, 6.76 * inch, 9.3 * inch, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_chrome),
        PageTemplate(id="normal", frames=[normal_frame], onPage=page_chrome),
    ])

    story = []

    # Cover
    story += [
        Spacer(1, 1.25 * inch),
        Paragraph(">> INTERWORK<br/>OFFICE SOLUTIONS", styles["CoverTitle"]),
        Spacer(1, 0.45 * inch),
        Paragraph("CLAUDE BOOTSTRAP<br/>& PROJECT SETUP GUIDE", styles["CoverTitle"]),
        Paragraph("How Scott and Matt inherit InterWork's rules, client knowledge, project structure and drafting workflows", styles["CoverSub"]),
        Spacer(1, 0.55 * inch),
        Table([[colored_card("COMPANY BRAIN", "Rules, people, procedures and source priorities", NAVY, 1.95 * inch), colored_card("CLIENT BRAIN", "Stable bootstrap plus current repo files", BLUE, 1.95 * inch), colored_card("PROJECT BRAIN", "Four standard files tied to one project number", GREEN, 1.95 * inch)]], colWidths=[2.12 * inch] * 3, style=[("VALIGN", (0,0), (-1,-1), "TOP")]),
        Spacer(1, 0.7 * inch),
        Paragraph("Prepared for Scott & Matt | Operations Coordinators<br/>Direct manager: Francisco Vinueza<br/>Setup owner: Alejandro Acosta", styles["CoverSub"]),
        Spacer(1, 0.55 * inch),
        Paragraph("Version 2 - August 4, 2026", styles["CoverSub"]),
        PageBreak(),
    ]
    doc.handle_nextPageTemplate("normal")

    # Page 2 architecture
    story += [
        Paragraph("The goal: give Claude a map to current knowledge", styles["H1x"]),
        Paragraph("Claude accounts do not permanently absorb everything they see. We reproduce the InterWork operating context by combining stable Project instructions with current files fetched from the shared repository.", styles["Bodyx"]),
        Spacer(1, 0.08 * inch),
        Table([[colored_card("1. BOOTSTRAP", "Uploaded once. Teaches routing, rules and what to fetch.", RED_DARK), Paragraph("<b>&rarr;</b>", styles["H1x"]), colored_card("2. LIVE REPO", "Changing facts: clients, project cards, open loops and notes.", BLUE), Paragraph("<b>&rarr;</b>", styles["H1x"]), colored_card("3. CLAUDE", "Finds current context, drafts work and flags conflicts.", GREEN)]], colWidths=[2.0*inch, .28*inch, 2.0*inch, .28*inch, 2.0*inch], style=[("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("ALIGN",(1,0),(1,0),"CENTER"), ("ALIGN",(3,0),(3,0),"CENTER")]),
        Spacer(1, 0.25 * inch),
        Paragraph("Source priority", styles["H2x"]),
        step(1, "Live dashboard / safe APIs", "Use current operational data for status, dates and confirmation fields.", GREEN),
        step(2, "Client and project files", "Use the repo for scope, contacts, open loops, decisions and history.", BLUE),
        step(3, "Uploaded knowledge pack", "Fallback only when live URL fetching is unavailable. Treat dated facts as potentially stale.", ORANGE),
        Paragraph("Important: the uploaded bootstrap is a map, not the territory. The repo is the durable shared memory; Supabase and the dashboard are the current operational state.", styles["Warn"]),
        Paragraph("What Scott and Matt can safely ask from day one", styles["H2x"]),
        Table([[colored_card("LOOK UP", "Client, project, contact and procedure context", BLUE), colored_card("DRAFT", "FastField notes, calendar entries, emails and Teams messages", ORANGE), colored_card("CHECK", "Missing facts, conflicts, risks and open loops", GREEN)]], colWidths=[2.23*inch]*3, style=[("VALIGN",(0,0),(-1,-1),"TOP")]),
        PageBreak(),
    ]

    # Page 3 company project
    story += [
        Paragraph("Part 1 - Create the company Claude Project", styles["H1x"]),
        Paragraph("Do this once in Scott's account and once in Matt's account. Each person uses an individual company identity - never Alejandro's login.", styles["BodyBold"]),
        step(1, "Install and sign in", f"Install Claude Desktop from {link('claude.ai/download', CLAUDE_DOWNLOAD)}. Sign in with the employee's own company-managed Claude account."),
        step(2, "Create a Project", "In Claude, create a new Project named <b>InterWork Office Solutions Knowledge Base</b>. This is the company-level workspace, not a client project."),
        step(3, "Upload the stable company bootstrap", "Add this file to Project Knowledge:<br/><font name='Courier-Bold'>claude_project_bootstraps/interwork_company_bootstrap.md</font>"),
        step(4, "Add the Project instructions", "Use the bootstrap's operating rules as the Project instructions. The instructions must require current repo lookups, preserve uncertainty and prohibit invented facts."),
        step(5, "Test the company brain", "Start a new chat and run the test prompts below. Do not move to client Projects until the tests pass."),
        Paragraph("Test prompt 1", styles["H2x"]),
        Paragraph("Before answering, follow the uploaded InterWork bootstrap. Tell me who our direct manager is, what the project number is used for, and what you must do when two sources disagree.", styles["Prompt"]),
        Paragraph("Expected result", styles["Good"]),
        bullet("Francisco Vinueza is the direct manager and operational escalation point."),
        bullet("The project number is the operational identifier across the workflow."),
        bullet("Conflicts are stated and escalated; Claude does not silently choose or guess."),
        Paragraph("Test prompt 2", styles["H2x"]),
        Paragraph("What can you draft freely, and what requires approval before it is sent or written to a live system?", styles["Prompt"]),
        Paragraph("Correct answer: drafting and analysis are allowed. External sends and live writes remain approval-gated during onboarding.", styles["Good"]),
        PageBreak(),
    ]

    # Page 4 client project
    story += [
        Paragraph("Part 2 - Create one Claude Project per client", styles["H1x"]),
        Paragraph("A Claude Project is created for a client, not for every individual job. Multiple project numbers for the same client live inside that client's shared repo folder.", styles["Warn"]),
        step(1, "Choose the canonical client", "Check <font name='Courier-Bold'>memory/clients/CLIENT_INDEX.md</font>. Do not create a duplicate client name or slug."),
        step(2, "Create the Claude Project", "Name it <b>InterWork - [Client Name]</b>. Examples: InterWork - Radian; InterWork - Marsh McLennan; InterWork - Bentley Systems."),
        step(3, "Upload the client bootstrap", "Select the matching file under:<br/><font name='Courier-Bold'>claude_project_bootstraps/&lt;client_slug&gt;_bootstrap.md</font>"),
        step(4, "Use a knowledge pack only as fallback", "If raw GitHub fetching fails, upload the matching file from <font name='Courier-Bold'>claude_project_packs/</font>. Check its generated date and do not treat changing project facts as current."),
        step(5, "Run a routing test", "Ask Claude to identify the client slug, fetch the client context, and wait for a project number before opening any project folder."),
        Paragraph("Client Project test prompt", styles["H2x"]),
        Paragraph("Follow this Project's bootstrap. Identify the canonical client folder, fetch CLIENT_CONTEXT.md, summarize the client's normal project types and communication expectations, then stop. Do not scan unrelated clients.", styles["Prompt"]),
        Table([[qr(REPO, 1.0*inch), Paragraph(f"<b>Shared repository</b><br/>{link('Open interwork-ai-workstation on GitHub', REPO)}<br/><br/>The repo must be synced before Scott or Matt relies on newly created onboarding or client files.", styles["Bodyx"]), qr(CLAUDE_PROJECTS_HELP, 1.0*inch), Paragraph(f"<b>Claude Projects help</b><br/>{link('Open Anthropic Projects guidance', CLAUDE_PROJECTS_HELP)}", styles["Bodyx"])]], colWidths=[1.05*inch, 2.3*inch, 1.05*inch, 2.3*inch], style=[("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("BOX",(0,0),(-1,-1),.7,LINE), ("INNERGRID",(0,0),(-1,-1),.4,LINE), ("BACKGROUND",(0,0),(-1,-1),colors.white), ("LEFTPADDING",(0,0),(-1,-1),7), ("RIGHTPADDING",(0,0),(-1,-1),7), ("TOPPADDING",(0,0),(-1,-1),7), ("BOTTOMPADDING",(0,0),(-1,-1),7)]),
        PageBreak(),
    ]

    # Page 5 project folder
    story += [
        Paragraph("Part 3 - Give Claude read-only access to the repo", styles["H1x"]),
        Paragraph("Scott and Matt do not need permission to change the repository. Their Claude Projects only need instructions that point to the public raw files and enforce a read-only boundary.", styles["BodyBold"]),
        step(1, "Open the client Claude Project", "Choose <b>InterWork - [Client Name]</b>, open Project settings, and find the Project instructions field."),
        step(2, "Paste the instruction block", "Use the two-page copy block that follows. Replace <font name='Courier-Bold'>&lt;client_slug&gt;</font> with the canonical folder from <font name='Courier-Bold'>memory/clients/CLIENT_INDEX.md</font>."),
        step(3, "Upload the matching bootstrap", "Add <font name='Courier-Bold'>claude_project_bootstraps/&lt;client_slug&gt;_bootstrap.md</font> to Project Knowledge. It is the routing map; the live repo remains the source for changing facts."),
        step(4, "Start a new chat and test access", "Ask Claude to fetch the AI index, client context and one known project card. It must name the files it used and must not claim it changed anything."),
        Paragraph("Raw GitHub starting points", styles["H2x"]),
        Table([
            [Paragraph("<b>AI routing index</b>", styles["Bodyx"]), Paragraph(link("Open START_HERE_FOR_AI.md", RAW + "memory/ai_index/START_HERE_FOR_AI.md"), styles["Bodyx"])],
            [Paragraph("<b>Client index</b>", styles["Bodyx"]), Paragraph(link("Open CLIENT_INDEX.md", RAW + "memory/clients/CLIENT_INDEX.md"), styles["Bodyx"])],
            [Paragraph("<b>Company rules</b>", styles["Bodyx"]), Paragraph(link("Open START_HERE.md", RAW + "memory/company_knowledge/START_HERE.md"), styles["Bodyx"])],
            [Paragraph("<b>Safety rules</b>", styles["Bodyx"]), Paragraph(link("Open ACCESS_AND_SAFETY_RULES.md", RAW + "memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md"), styles["Bodyx"])],
        ], colWidths=[1.65*inch, 5.05*inch], style=[("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("BOX",(0,0),(-1,-1),.8,LINE), ("INNERGRID",(0,0),(-1,-1),.5,LINE), ("BACKGROUND",(0,0),(0,-1),RED_SOFT), ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8), ("TOPPADDING",(0,0),(-1,-1),7), ("BOTTOMPADDING",(0,0),(-1,-1),7)]),
        Spacer(1, .12*inch),
        Paragraph("Read-only means Claude may fetch, summarize and draft from repository files. It may not commit, push, upload, edit, delete, open a pull request or ask for credentials. Any durable update becomes a proposed handoff for Alejandro.", styles["Warn"]),
        Paragraph("Access test prompt", styles["H2x"]),
        Paragraph("Read the InterWork AI routing index from the raw GitHub URL. Then locate the canonical client folder for [CLIENT] and fetch only its CLIENT_CONTEXT.md. Tell me the exact URLs you used, summarize the context, and stop. Do not modify the repository.", styles["Prompt"]),
        PageBreak(),
    ]

    # Copy block 1
    story += [
        Paragraph("Copy into Claude Project instructions - 1 of 2", styles["H1x"]),
        Paragraph("Paste this into each client Claude Project. Replace only the client slug. Keep the safety language intact.", styles["BodyBold"]),
        Paragraph(
            "You are the read-only InterWork operations assistant for this client.<br/><br/>"
            "CLIENT FOLDER: memory/clients/&lt;client_slug&gt;/<br/>"
            "RAW BASE: https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/<br/><br/>"
            "At the start of operational work:<br/>"
            "1. Fetch memory/ai_index/START_HERE_FOR_AI.md.<br/>"
            "2. Fetch memory/company_knowledge/START_HERE.md.<br/>"
            "3. Fetch memory/company_knowledge/COMMUNICATION_RULES.md.<br/>"
            "4. Fetch memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md.<br/>"
            "5. Fetch this client's CLIENT_CONTEXT.md.<br/>"
            "6. Wait for a confirmed project number before opening a project folder.<br/><br/>"
            "When a project number is provided, use the AI index or search only inside this client's projects folder. If the matching folder exists, read only PROJECT_CARD.md, OPEN_LOOPS.md, DRAFTS.md and NOTES.md. Do not scan unrelated clients or projects.<br/><br/>"
            "Use the project number as the primary operational identifier. Do not invent project numbers, dates, statuses, contacts, phone numbers, assignments or approvals. Separate confirmed facts, conflicts, missing information and proposed details.",
            styles["PasteCode"]),
        Paragraph("Tip: after pasting, save the Project instructions and begin a completely new chat for the validation test. Existing chats may retain older context.", styles["Good"]),
        PageBreak(),
    ]

    # Copy block 2
    story += [
        Paragraph("Copy into Claude Project instructions - 2 of 2", styles["H1x"]),
        Paragraph(
            "REPOSITORY BOUNDARY<br/>"
            "Repository access is read-only. You may fetch and cite files, summarize facts, identify conflicts and prepare drafts. Never commit, push, upload, edit, delete, create a branch, create a pull request or request credentials. If a durable fact should be saved, prepare a Claude Code handoff for Alejandro.<br/><br/>"
            "ACTION BOUNDARY<br/>"
            "Drafting and analysis are allowed. Do not send emails or Teams messages. Do not submit FastField. Do not create calendar events. Do not write to Supabase or Smartsheet. Do not claim an action happened when you only drafted it. External sends and live-system writes require Alejandro's approval during onboarding.<br/><br/>"
            "SOURCE RULES<br/>"
            "Use live dashboard or safe API data for current operational state when available. Use current repo files for client context, scope, contacts, history and open loops. Uploaded knowledge packs are fallback only and may be stale. When sources disagree, state the conflict and ask for confirmation; never silently choose.<br/><br/>"
            "IF ACCESS FAILS<br/>"
            "Say: I cannot access the repository directly in this chat. Ask the user to paste the specific file or request a Claude Code handoff. Do not guess from chat memory.<br/><br/>"
            "HANDOFF FORMAT<br/>"
            "Claude Code Handoff - [Client / Project]<br/>New confirmed facts: [facts]<br/>Sources: [where each fact came from]<br/>Open questions: [unresolved items]<br/>Suggested files: [exact repository paths]<br/>No repository changes have been made.",
            styles["PasteCode"]),
        Paragraph("Success test", styles["H2x"]),
        Paragraph("For Project #[NUMBER], fetch only the correct client's context and the four standard project files. Prepare a short status summary, a FastField draft and a calendar-entry draft. List missing information separately. Do not send, submit, create or modify anything.", styles["Prompt"]),
        Paragraph("Claude passes when it identifies its sources, uses the project number, preserves uncertainty, produces drafts only and confirms that no repository or live-system changes were made.", styles["Good"]),
        PageBreak(),
    ]

    # Essential rules embedded
    story += [
        Paragraph("Embedded essentials - the rules they must always have", styles["H1x"]),
        Paragraph("This page is the compact fallback when a linked file is unavailable. The live repository remains authoritative and may contain newer detail.", styles["Warn"]),
        Table([
            [colored_card("IDENTITY", "Project number first. Confirm the canonical client and existing folder before routing.", BLUE, 3.25*inch), colored_card("TRUTH", "Current sources beat old chat memory. Show conflicts, missing facts and stale data.", GREEN, 3.25*inch)],
            [colored_card("DRAFT ONLY", "FastField, calendar, email and Teams content may be drafted - never represented as sent.", ORANGE, 3.25*inch), colored_card("READ ONLY", "No repo edits, commits, branches, pull requests, deletes or credential requests.", RED_DARK, 3.25*inch)],
        ], colWidths=[3.38*inch,3.38*inch], style=[("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5)]),
        Paragraph("Never invent", styles["H2x"]),
        bullet("Project numbers, dates, status, contact names, phone numbers, PM assignments or approvals"),
        bullet("A completed send, FastField submission, calendar creation or live-system update"),
        Paragraph("Never expose or request", styles["H2x"]),
        bullet("Passwords, tokens, API keys, service-role keys, connection strings or .env contents"),
        bullet("Vendor rates, internal margins or vendor details in client-facing material"),
        Paragraph("Always preserve", styles["H2x"]),
        bullet("The difference between confirmed facts, proposed details and unresolved questions"),
        bullet("The source trail for material facts and the exact file paths used"),
        bullet("A narrow client/project lookup instead of loading the whole repository"),
        bullet("A durable handoff when new facts should be added by an authorized person"),
        Paragraph("Manager and escalation: Francisco Vinueza is the direct manager and field escalation point. During onboarding, Alejandro remains the approval route for external sends and live-system writes until the competency decision is made.", styles["Good"]),
        PageBreak(),
    ]

    # Page 5 project folder
    story += [
        Paragraph("Part 3 - Make every job project-ready", styles["H1x"]),
        Paragraph("Do not create a new Claude Project for every job. Create or update the job inside the canonical client folder, using the confirmed project number as the key.", styles["BodyBold"]),
        Paragraph("Required folder shape", styles["H2x"]),
        Paragraph("memory/clients/&lt;client_slug&gt;/projects/<br/>&nbsp;&nbsp;&nbsp;&nbsp;&lt;project_number&gt;_&lt;short_description&gt;/<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PROJECT_CARD.md<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;OPEN_LOOPS.md<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DRAFTS.md<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NOTES.md", styles["CodexCode"]),
        Table([
            [colored_card("PROJECT_CARD.md", "Identity, people, locations, dates, scope, status and confirmed facts", RED_DARK, 3.25*inch), colored_card("OPEN_LOOPS.md", "Unresolved items, owner, priority, next action and blocking questions", ORANGE, 3.25*inch)],
            [colored_card("DRAFTS.md", "Client emails, Teams messages, FastField notes and calendar-entry drafts", BLUE, 3.25*inch), colored_card("NOTES.md", "Source notes, history, decisions, evidence and context that should persist", GREEN, 3.25*inch)],
        ], colWidths=[3.38*inch, 3.38*inch], style=[("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5)]),
        Spacer(1, 0.12*inch),
        Paragraph("Project-ready checklist", styles["H2x"]),
        bullet("Confirmed project number and canonical client slug"),
        bullet("Project type and approved scope"),
        bullet("Origin/destination or site address, including floor/suite"),
        bullet("Dates and start time clearly labeled confirmed or needs confirmation"),
        bullet("Office PM, field PM, client POC and building/access contacts"),
        bullet("Access restrictions, COI, dock/elevator, parking and exclusions"),
        bullet("Open loops separated from confirmed facts"),
        bullet("Source trail showing where each important fact came from"),
        Paragraph("If a matching folder already exists, update it. Do not create a duplicate folder under a different client name or informal abbreviation.", styles["Warn"]),
        PageBreak(),
    ]

    # Page 6 FF
    story += [
        Paragraph("Part 4 - Ask Claude for a FastField draft", styles["H1x"]),
        Paragraph("Claude can prepare the field-ready FastField content. It does not submit the mobile form. The field assignment and the post-FF Teams message are separate artifacts.", styles["Warn"]),
        Paragraph("Minimum information Claude must confirm", styles["H2x"]),
        Table([
            [Paragraph("<b>Identity</b><br/>Project number<br/>Client<br/>Project type", styles["Bodyx"]), Paragraph("<b>Execution</b><br/>Date and start time<br/>Field PM<br/>Full address / route", styles["Bodyx"]), Paragraph("<b>Field detail</b><br/>Scope bullets<br/>POC + phone<br/>Restrictions / exclusions", styles["Bodyx"])],
        ], colWidths=[2.25*inch]*3, style=[("VALIGN",(0,0),(-1,-1),"TOP"), ("BOX",(0,0),(-1,-1),1,RED), ("INNERGRID",(0,0),(-1,-1),.6,LINE), ("BACKGROUND",(0,0),(-1,-1),colors.white), ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10), ("TOPPADDING",(0,0),(-1,-1),10), ("BOTTOMPADDING",(0,0),(-1,-1),10)]),
        Spacer(1, 0.18*inch),
        Paragraph("FastField request prompt", styles["H2x"]),
        Paragraph("Prepare the FastField assignment draft for Project #[NUMBER]. Follow the client bootstrap and current project files. Verify the project number, execution date, field PM, site address, client POC, access restrictions, scope and exclusions. Separate confirmed facts from missing information. Do not invent anything and do not submit the form.", styles["Prompt"]),
        Paragraph("Expected output", styles["H2x"]),
        bullet("Project number, client, date and assigned field PM"),
        bullet("Full origin/destination or site address"),
        bullet("Concise field-ready scope bullets"),
        bullet("POC name and confirmed phone number"),
        bullet("Special access notes, restrictions and exclusions"),
        bullet("A separate 'Needs confirmation' list"),
        Paragraph("After the FastField is manually submitted, ask Claude to draft the separate Teams notification using <font name='Courier-Bold'>memory/procedures/post_fastfield_teams_notification_standard.md</font>.", styles["Good"]),
        PageBreak(),
    ]

    # Page 7 calendar
    story += [
        Paragraph("Part 5 - Ask Claude for a calendar-entry draft", styles["H1x"]),
        Paragraph("Claude can structure a complete calendar entry for manual review and entry. The M365/Teams AI connector is currently blocked by company tenant policy, so the AI must not claim it created the event.", styles["Warn"]),
        Paragraph("Calendar request prompt", styles["H2x"]),
        Paragraph("Draft a calendar entry for Project #[NUMBER]. Fetch the current project record and project card. Include the project number, client, project type, confirmed date(s), start/end time or duration, full address, office PM, field PM, POC, scope, access instructions and open items. Mark anything unconfirmed. Do not create or send the event.", styles["Prompt"]),
        Paragraph("Recommended calendar format", styles["H2x"]),
        Table([
            [Paragraph("<b>Title</b>", styles["Bodyx"]), Paragraph("Project #[NUMBER] - Client - Location - Work Type", styles["Bodyx"])],
            [Paragraph("<b>When</b>", styles["Bodyx"]), Paragraph("Confirmed date, start time, end time or expected duration", styles["Bodyx"])],
            [Paragraph("<b>Where</b>", styles["Bodyx"]), Paragraph("Full address, floor/suite, loading/check-in information", styles["Bodyx"])],
            [Paragraph("<b>Description</b>", styles["Bodyx"]), Paragraph("PMs, POC, concise scope, restrictions, exclusions and open items", styles["Bodyx"])],
        ], colWidths=[1.25*inch, 5.5*inch], style=[("VALIGN",(0,0),(-1,-1),"TOP"), ("BOX",(0,0),(-1,-1),1,BLUE), ("INNERGRID",(0,0),(-1,-1),.5,LINE), ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#EEF3FD")), ("LEFTPADDING",(0,0),(-1,-1),9), ("RIGHTPADDING",(0,0),(-1,-1),9), ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8)]),
        Spacer(1, 0.2*inch),
        Paragraph("Self-check before manual calendar entry", styles["H2x"]),
        bullet("Project number matches the live operational record"),
        bullet("No proposed date is presented as confirmed"),
        bullet("Time zone and multi-day schedule are explicit"),
        bullet("Client-facing description excludes vendor names, rates and internal issues"),
        bullet("Access requirements and onsite contact are visible"),
        bullet("Open questions remain visible instead of being silently filled"),
        PageBreak(),
    ]

    # Page 8 safety and links
    story += [
        Paragraph("Part 6 - Final rules, validation and quick links", styles["H1x"]),
        Table([[colored_card("ALWAYS", "Fetch current sources, use project numbers, preserve uncertainty and draft clearly", GREEN, 3.25*inch), colored_card("NEVER", "Share credentials, invent facts, expose vendor details, send or write without authority", RED_DARK, 3.25*inch)]], colWidths=[3.38*inch, 3.38*inch], style=[("VALIGN",(0,0),(-1,-1),"TOP")]),
        Spacer(1, 0.18*inch),
        Paragraph("Account setup validation", styles["H2x"]),
        bullet("Company Claude Project exists and contains the company bootstrap"),
        bullet("Client Project uses the correct canonical client bootstrap"),
        bullet("Claude can fetch START_HERE_FOR_AI.md and the appropriate client context"),
        bullet("Claude refuses to invent a missing date, project number, contact or phone"),
        bullet("Claude describes FastField and calendar work as drafts, not completed actions"),
        bullet("Scott and Matt know how to request a Claude Code handoff for durable repo updates"),
        Paragraph("Quick links", styles["H2x"]),
        Table([
            [Paragraph(f"<b>Claude Desktop</b><br/>{link('Download', CLAUDE_DOWNLOAD)}", styles["Bodyx"]), Paragraph(f"<b>Shared repo</b><br/>{link('Open GitHub', REPO)}", styles["Bodyx"]), Paragraph(f"<b>Command Center</b><br/>{link('Open dashboard', DASHBOARD)}", styles["Bodyx"])],
            [Paragraph(f"<b>AI index</b><br/>{link('START_HERE_FOR_AI.md', RAW + 'memory/ai_index/START_HERE_FOR_AI.md')}", styles["Bodyx"]), Paragraph(f"<b>Company rules</b><br/>{link('START_HERE.md', RAW + 'memory/company_knowledge/START_HERE.md')}", styles["Bodyx"]), Paragraph(f"<b>Client index</b><br/>{link('CLIENT_INDEX.md', RAW + 'memory/clients/CLIENT_INDEX.md')}", styles["Bodyx"])],
        ], colWidths=[2.25*inch]*3, style=[("VALIGN",(0,0),(-1,-1),"TOP"), ("BOX",(0,0),(-1,-1),1,LINE), ("INNERGRID",(0,0),(-1,-1),.5,LINE), ("BACKGROUND",(0,0),(-1,-1),colors.white), ("LEFTPADDING",(0,0),(-1,-1),9), ("RIGHTPADDING",(0,0),(-1,-1),9), ("TOPPADDING",(0,0),(-1,-1),9), ("BOTTOMPADDING",(0,0),(-1,-1),9)]),
        Spacer(1, 0.2*inch),
        Paragraph("Manager note", styles["H2x"]),
        Paragraph("Before relying on newly created client files, bootstraps or onboarding materials, Alejandro must confirm the local repository changes have been reviewed and synced to GitHub. Local-only files are not visible to Scott or Matt's Claude accounts.", styles["Warn"]),
        Paragraph("The desired behavior is not 'Claude memorizes everything.' It is: Claude knows where the current truth lives, reads only the relevant context, follows the same rules every time and leaves a durable handoff when new facts appear.", styles["Good"]),
    ]

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    build()
