# Module 2 — Project Lifecycle and Practical Examples
Still no AI tools, dashboard, or repository navigation in this module — that's Module 4. This module is the process itself, and four real projects that show it in action.

_Sources used: `memory/company_knowledge/OPERATING_WORKFLOW.md` (lifecycle sequence and pre-execution checklist), `memory/company_knowledge/COMMUNICATION_RULES.md` (client vs. internal standards), and four project cards, sanitized for training — see "Where these examples came from" at the bottom for exact paths._

## The full lifecycle

```
1. Quote issued
   Account manager sends a quote. Project number is assigned here — this is where
   a project starts existing as a trackable thing.

2. Project created / scheduled
   Scheduling entry added (Smartsheet). A record is created in the operational
   database (Supabase) — often synced from the schedule.

3. PM and vendor assigned
   Office PM identified. Field PM identified if execution needs an on-site lead.
   Vendor or crew confirmed if the work needs one.

4. Pre-execution confirmation — the checklist that protects everyone
   - Client has confirmed the date
   - Building access is confirmed (COI submitted if the building requires one)
   - Vendor/crew has confirmed availability
   - Field PM has what they need (scope, contacts, schedule) to run the day
   - Client has received a confirmation notice

5. Execution
   Field PM runs the crew, then submits FastField on or after the execution day.
   FastField is a mobile form — there's no other way to submit it.

6. Closeout
   A Work Completion (WC) report is generated from the FastField content.
   A completion email goes to the client with the WC report attached.
   The project's status is set to completed once everything above is actually done —
   not before.
```

Pre-execution confirmation checklist, in full (not every item applies to every job — use judgment):
loading dock / liftgate needed, freight elevator reserved, COI submitted, union restrictions, building hours, on-site POC name and phone, crew check-in location, parking/loading instructions, floor protection, broom-clean requirement, sustainability/donation coordination for decommissions, e-waste disposal responsibility, cabling scope (IDF/MDF only unless risers explicitly included).

## Where information normally originates

| Lifecycle stage | Typical source |
|---|---|
| Quote / project number | Account manager, via QuickQuo |
| Schedule | Smartsheet entry |
| Scope detail | Site walk notes, FastField inventory form, or the client's original request email |
| Confirmations (client/vendor/access) | Direct email, phone call, or Teams — not inferred |
| Execution detail | The Field PM's FastField submission |
| Closeout | WC report generated from FastField, then the completion email |

Notice the pattern: **the person or document closest to the actual event is the source**, not a summary of a summary. If a fact came from a relayed handoff rather than the original email or form, that's worth noting — it changes how much you'd trust it if something later doesn't add up.

## Client-facing vs. internal communication — the short version

Full rules: `memory/company_knowledge/COMMUNICATION_RULES.md`. The parts that matter most on day one:

- **Client emails**: concise, professional, no filler. State dates/location/PM name and phone/open items. Never name the vendor, never mention the warehouse address, never reference internal pricing or margins.
- **Internal messages (Teams, PM dispatch)**: full address, POC name and phone, scope bullets, schedule, restrictions — the detail a client email deliberately leaves out.
- Keep vendor problems and vendor substitutions **out of client-facing messages** unless the client specifically needs to know.
- Mark anything unconfirmed as "needs confirmation" in both — never guess a name, number, or date to fill a gap.

## Four real projects, walked through

Each shows the lifecycle, the roles from Module 1, where the information came from, and at least one real judgment/escalation moment. Client-side individuals are referred to by role only; project numbers, InterWork staff, and vendor names are real since that's exactly what you need to learn to recognize.

### Example 1 — Decommission (Project 7492)

A two-floor office decommission in Denver, plus outbound deliveries to two other client locations once the Denver items reached InterWork's warehouse.

- **Roles in play**: an account manager set up the original quote; a vendor (a Denver-based installation company) handled the on-site decommission labor; a separate transportation vendor moved the removed assets to InterWork's warehouse; a Field PM was then assigned for the outbound delivery leg; the client had **two different facilities contacts** — one for each delivery site.
- **Scope**: disposal of monitor arms, TVs, whiteboards, and full security-system removal (cameras, badge readers, access panels) on one floor; cabling traced back to the nearest IDF/MDF only (risers excluded, per the standard rule).
- **A building contact appears**: one of the two delivery sites required a Certificate of Insurance from that building's own property management before delivery — a separate approval from anything the client's facilities contact had already confirmed.
- **The judgment moment**: during the decommission, some items were inadvertently removed that weren't supposed to be. That problem and the separately-planned warehouse pickup are two unrelated issues — the project card explicitly flags that they must **never be merged in client communications**, and that the removal mistake isn't mentioned to the client unless it actually needs to be. This is the vendor-problems-stay-internal rule from Communication Rules, in practice.
- **Where the facts came from**: a mix of a knowledge export, a direct client email thread, and a Smartsheet screenshot for the PM assignment — multiple source types feeding one project card, which is normal.

### Example 2 — Furniture Relocation (Project 7350)

A two-day office relocation, Philadelphia to a nearby PA location — pack and load day one, offload and install day two. This was the **final phase** of a longer relationship with this client; earlier phases were already complete.

- **Roles in play**: an Office PM (administrative owner) and a Field PM (on-site lead) are two different named people on this project — a clean example of that split from Module 1. The account manager provided a confirmed inventory list.
- **Scope**: disassembling and reinstalling height-adjustable desks and hoteling stations, monitor arms, and — notably — physically relocating IT equipment (a network switch, a firewall, wireless access points). InterWork moves the hardware; it does not configure it.
- **The judgment moment**: the project card carries an explicit warning not to merge inventory or scope from the earlier phases into this one, and to use only the account manager's latest confirmed inventory list — a real example of why "the newest confirmed source wins" matters when a client relationship spans multiple projects over time.
- **Open items even this late**: onsite contact phone numbers for both locations were still missing shortly before execution — a reminder that "scheduled" doesn't mean "fully confirmed."
- **Where the facts came from**: the account manager's inventory list, and coordinator-approved corrections made directly to the operational database.

### Example 3 — E-Waste / Furniture Disposal (Project 7594)

An e-waste and furniture disposal job that started as one request and grew: it was later combined into a single multi-stop route with an unrelated chair relocation for the same client, and a reception-desk-replacement request stayed attached to the same thread without becoming part of the execution scope.

- **Roles in play**: the request originated with a client facilities/real-estate contact; a different site contact was present for the initial walkthrough but explicitly would **not** be present on the actual disposal day — someone else, not yet identified at the time, would need to be there instead. The Field PM named at the walkthrough and the Field PM named on the execution dispatch were two different people, and the project card flags that reconciliation as unresolved rather than assuming it's fine.
- **A vendor that isn't a crew**: the vendor used on this job supplied a rental truck only — no labor. "Vendor" doesn't always mean the people doing the work.
- **The judgment moment**: the added reception-desk-replacement request stayed explicitly "on hold" and was called out as **excluded** on both the quote and the execution dispatch — twice. That's what keeping excluded scope visibly excluded looks like, so a crew never does unapproved work because a request happened to arrive on the same thread.
- **Where the facts came from, at three different stages**: a FastField inventory form from the site walk (the scope), a quote document (the price and combined route), and a separate execution FastField (the actual dispatch) — three different documents, three different lifecycle stages, one project number tying them together.

### Example 4 — Delivery / Installation (Project 7547)

An electrical/desk-power-beam installation at a client headquarters — a single-day install, not a full relocation.

- **Roles in play**: a Field PM confirmed the crew and start time directly with the vendor; the account manager relayed a scope concern from the client side before the account manager had even seen the resolution; the client had one general contact and a separate contact who specifically handled electrical drawings.
- **The judgment moment, twice**: (1) the account manager flagged a discrepancy in the number of electrical connections needed, based on the client's own drawing — that got resolved with an updated drawing from the client, not by guessing a number and proceeding; (2) a general-contractor permit had to "piggyback" for the electrical work to be allowed at all — an access precondition, similar in spirit to a COI, that had to be confirmed before the crew showed up, not discovered on-site.
- **Where the facts came from**: internal email threads, a client-provided revised drawing, and a direct vendor confirmation of the crew and start time.

## Knowledge Check 2

1. Walk through the six lifecycle stages, in order, for any project type of your choice.
2. In Example 3, why didn't the reception-desk request just get folded into the execution scope once it came up on the same thread?
3. In Example 1, why must the "items inadvertently removed" issue and the warehouse pickup never appear together in a client-facing message?
4. In Example 2, why is the account manager's latest confirmed inventory list the one to trust, over data from an earlier phase of the same client relationship?
5. Give an example, from any of the four projects, of a building contact or access precondition that was separate from the main client contact.
6. What's one thing a client-facing email should never include that an internal Teams message to a field PM should?
7. In Example 4, what did the account manager do when a scope discrepancy came up — pick a number and move on, or something else?

Talk through your answers with Alejandro before Module 3.

## Where these examples came from

For your own reference later — not required reading for Scott/Matt, but here so the source is traceable:
- Example 1: `memory/clients/radian/projects/7492_radian_denver_decom/PROJECT_CARD.md`
- Example 2: `memory/clients/bentley_systems/projects/7350_cesium_to_exton/PROJECT_CARD.md`
- Example 3: `memory/clients/amtrust/projects/7594_nashua_ewaste_disposal/PROJECT_CARD.md`
- Example 4: `memory/clients/dropbox/projects/7547_power_beam_install/PROJECT_CARD.md`

Client-side individuals' names, emails, and direct phone numbers were removed and replaced with role labels for this training document. InterWork staff, vendor company names, and project numbers were kept as-is since recognizing those is part of the point. These are point-in-time snapshots — the real projects have moved on since these cards were written; don't treat this file as current project status.
