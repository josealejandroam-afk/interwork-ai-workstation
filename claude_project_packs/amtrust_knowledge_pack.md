# AmTrust Financial Services — Claude Chat Knowledge Pack
_Generated: 2026-06-30_

## Client Overview

AmTrust Financial Services is a specialty insurance company. InterWork has multiple projects for AmTrust across multiple US locations.

---

## Active / Pending Actions

**"send it 7348"** — Teams notification to Pedro Martinez for AmTrust Cleveland is held, waiting for Alejandro's approval. Trigger: Alejandro says "send it" for project 7348.

---

## Known Projects

### 7348 — AmTrust Cleveland
- **Location:** Princeton, NJ (**NOTE: labeled "Cleveland" but Supabase location says Princeton NJ — confirm correct city before any dispatch**)
- **Scheduled:** 2026-04-15
- **PM:** Pedro Martinez
- **Vendor:** Yes
- **FastField:** true (submitted)
- **Status:** In-progress / overdue — FastField submitted but status not updated in Supabase
- **Pending:** Teams notification to Pedro Martinez ("send it 7348") — awaiting Alejandro approval

### 7502 — Small Office Move Garden Grove CA
- **Location:** Garden Grove, CA
- **Scheduled:** 2026-05-11
- **PM:** External PM
- **Vendor:** Yes
- **FastField:** false
- **Status:** Past-dated — no signals

### 7513 — Move Office Furniture Southington CT
- **Location:** Southington, CT
- **Scheduled:** 2026-05-21
- **PM:** Pedro Martinez
- **Vendor:** Yes
- **FastField:** false
- **Status:** Past-dated — no signals

### 7515 — Storage Disposal New York NY
- **Location:** New York, NY
- **Scheduled:** 2026-05-27
- **PM:** Manny Gonzalez
- **Vendor:** Yes
- **FastField:** false
- **Status:** Past-dated — no signals

### 7536 — AmTrust Project (NYC / Melville)
- **Location:** Needs confirmation — may be New York City or Melville, NY
- **Status:** Needs confirmation
- **Source:** CLIENT_CONTEXT.md (no project card yet)

### 7568 — Site Walk Irvine CA
- **Location:** Irvine, CA
- **Scheduled:** 2026-06-26
- **PM:** External PM
- **Vendor:** Yes
- **FastField:** false
- **Status:** Past-dated — no signals

---

## Data Quality Flags

- **7348 location mismatch:** Named "Cleveland" but Supabase location field says Princeton NJ. Do not use "Cleveland" in any client communication until confirmed.
- **7572 conflict:** PROJECT_INDEX shows a 7572 as "AmTrust Move 40-50 Boxes New York NY" — but project folder 7572 already exists under `rothman_orthopaedics/`. Do NOT create a duplicate folder. Alejandro must confirm which client this project belongs to.

---

## Open Loops

| # | Item |
|---|---|
| 1 | Confirm location for 7348 — "Cleveland" vs Princeton NJ |
| 2 | Approve Teams send for 7348 |
| 3 | Confirm completion of 7502, 7513, 7515, 7568 — no FastField on any |
| 4 | Confirm details for 7536 (NYC/Melville) |
| 5 | Resolve 7572 conflict — AmTrust vs Rothman Orthopaedics |

---

## PM Key (InterWork)

AJ = Alejandro Acosta | FV = Francisco Vinueza | HB = Hunter Barbieri | JuM = Juan Martinez | PeM = Pedro Martinez | FB = Frank Barrett | JE = Jairo Escalante | MG = Manny Gonzalez | MH = Melvin Hernandez | EXT = External PM

---

## How to Read This Pack

This pack was generated from `memory/clients/amtrust/` in the InterWork AI workstation repo. Do not invent details not listed here. If a field says "Needs confirmation," it is unknown — do not guess.
