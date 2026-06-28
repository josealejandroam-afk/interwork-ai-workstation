---
name: interwork-project-lifecycle
description: "How an InterWork project moves from request to closeout — 14 stages with required info, Claude's role, and approval gates"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  review_after: 2026-12-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork Project Lifecycle
_Last updated: 2026-06-26_

---

## Overview

A project moves through 14 stages from initial request to administrative close.
Claude's role at each stage is noted. Approval gates are marked.

---

## Stage 1 — Request / Inquiry

**What happens:** Client, internal team, or vendor sends a request via Teams, email, Smartsheet, Read AI meeting, or call notes.

**Claude's role:**
- Detect project-relevant signals in incoming communications
- Log to `open_loops` or memory as a pending item
- Surface to Alejandro for initial review

**Never:** Create a project record or assign a project number at this stage.

---

## Stage 2 — Quote / Project Number

**What happens:** A project number is assigned and a quote is prepared.

**Claude's role:**
- Help draft quote fields when asked
- QuickQuo-style entry fields to prioritize:
  - Sold To
  - Ship To
  - Bill To
  - Project Location
  - Project Destination
  - Scope
- Never invent project numbers
- Project number must be confirmed by Alejandro or sourced from Smartsheet/existing records before creating a Supabase record

**Gate:** Project number confirmed before creating Supabase record.

---

## Stage 3 — Smartsheet Calendar Entry

**What happens:** The project is added to the Smartsheet schedule.

**Claude's role:**
- Treat Smartsheet as read-only
- If a calendar insert is requested, prepare the entry fields and surface for Alejandro/Hunter/Stephanie to apply
- Never write directly to Smartsheet

**Gate:** Smartsheet insert requires human action (Claude prepares, does not send).

---

## Stage 4 — Supabase / Dashboard Record

**What happens:** An official project record is created or updated in Supabase.

**Claude's role:**
- Propose the INSERT or UPDATE with all known fields
- Flag any missing required fields
- Wait for Alejandro approval before applying

**Gate:** All Supabase writes require Alejandro approval.

---

## Stage 5 — Planning

**What happens:** Scope, logistics, and requirements are confirmed.

**Claude's role:**
- Run `/project-brief` to surface current state of project fields
- Flag missing fields from this checklist:
  - Scope confirmed
  - Start date / end date
  - Site address, floor, suite
  - PM assigned
  - Client POC name and phone
  - Building access / loading dock / freight elevator / after-hours
  - Vendor required (yes/no)
  - Equipment / truck / materials
  - Special requirements (COI, e-waste, anchoring, masonite, speedpacks, etc.)
- Surface open questions as open loops

---

## Stage 6 — Vendor Coordination

**What happens:** If a vendor is required, they are contacted and confirmed.

**Claude's role:**
- Draft vendor email or Teams message (do not send without approval)
- Track confirmation status in `vendor_confirmed`
- Checklist:
  - Vendor name confirmed
  - Lead contact and phone confirmed
  - Crew size confirmed
  - Truck / equipment plan confirmed
  - Rate confirmed
  - Date and arrival time confirmed

**Gate:** `vendor_confirmed = true` requires Alejandro approval. Vendor messages require approval before sending.

---

## Stage 7 — Client Confirmation

**What happens:** Client is confirmed on schedule, PM, access, and expectations.

**Claude's role:**
- Draft client confirmation email or Teams message (do not send without approval)
- Include PM full name and phone number when known
- Do not expose vendor names, rates, or internal details
- Checklist:
  - Date and time confirmed
  - PM name and phone included
  - Site access confirmed
  - Client POC confirmed
  - Expectations set

**Gate:** `client_confirmed = true` requires Alejandro approval. Client messages require approval before sending.

---

## Stage 8 — FastField

**What happens:** FastField scope is prepared for the field PM.

**Claude's role:**
- Draft FF scope if asked
- Include: scope, site address, floor/suite, client POC and phone, arrival time, truck/equipment plan, special instructions, photos/docs if needed
- FastField forms are submitted by the field PM, not by Claude

**Gate:** `fastfield_submitted = true` is only updated from confirmed submission evidence (email, export, or Alejandro approval).

---

## Stage 9 — Teams PM Instructions

**What happens:** A concise Teams message is sent to the assigned field PM.

**Claude's role:**
- Draft the Teams message
- Include: scope summary, full address, client POC and phone, arrival time, truck/equipment plan, parking, special instructions
- Keep it field-ready and practical — no unnecessary detail
- Do not send without Alejandro approval

**Gate:** Teams sends require Alejandro approval.

---

## Stage 10 — Execution

**What happens:** Crew performs the work on-site.

**Claude's role:**
- Monitor incoming signals from Teams, FastField, calls, photos, email
- Log updates to project memory file
- Surface unexpected issues as open loops
- Do not change any Supabase fields based on field updates alone — propose and wait for approval

---

## Stage 11 — Verification

**What happens:** Work completion is verified before calling the project done.

**Claude's role (via `/completion-intake`):**
- Check FastField submission
- Check WC report
- Check photos if available
- Check client satisfaction signal
- Check for remaining punch items
- Flag if any signals are missing or contradictory
- Produce a verification summary — do not update fields without approval

**Never call a project done** if:
- FastField not submitted AND no WC report
- Open punch items remain
- Client has flagged issues
- Scope says multi-phase and later phases are incomplete

---

## Stage 12 — Completion Report

**What happens:** A Work Completion (WC) report is sent or filed.

**Claude's role:**
- Detect WC report evidence via `/completion-intake` (email, PDF, pasted note)
- Propose `completion_report_sent = true` if strong evidence exists
- Draft WC report if asked

**Gate:** `completion_report_sent = true` requires Alejandro approval or confirmed documentary evidence.

---

## Stage 13 — Administrative Closeout

**What happens:** Invoice, final client follow-up, accounting reconciliation, remaining open loops cleared.

**Claude's role:**
- Surface open loops related to this project
- Flag unpaid invoices or missing PO numbers
- Flag unanswered client emails
- Do not mark project closed without confirmation

**Gate:** `status = 'closed'` requires verified administrative completion and Alejandro approval.

---

## Stage 14 — Closed

**What happens:** Project is administratively complete.

**Claude's role:**
- Archive project memory file
- Close remaining open loops
- Log final status to activity_log

**Gate:** `status = 'closed'` requires Alejandro approval.

---

## Quick Reference — Approval Gates

| Stage | Field / Action | Requires Approval |
|-------|---------------|-------------------|
| 4 | Any Supabase write | Yes |
| 6 | vendor_confirmed = true | Yes |
| 6 | Vendor message send | Yes |
| 7 | client_confirmed = true | Yes |
| 7 | Client message send | Yes |
| 8 | fastfield_submitted = true | Yes (or confirmed evidence) |
| 9 | Teams PM message send | Yes |
| 12 | completion_report_sent = true | Yes (or confirmed evidence) |
| 13–14 | status = completed / closed | Yes |
