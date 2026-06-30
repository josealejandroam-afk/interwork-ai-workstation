# Claude → ChatGPT Inbox
_Claude leaves compact updates here for ChatGPT to read._
_Format: date, summary, open questions. Newest at top._
_Last updated: 2026-06-29_

---

## How to Use This File

ChatGPT: Start here when Alejandro brings you into a session. Read the latest entry, then read:
- `memory/shared/AI_SHARED_CONTEXT.md` — system overview
- `memory/shared/OPEN_LOOPS.md` — what needs action
- `memory/shared/PROJECT_INDEX.md` — active project table
- `memory/shared/DAILY_HANDOFF.md` — what happened today

---

## 2026-06-29 — Claude Update

**System state:** Operational. Supabase connected read-only. M365/Teams OAuth pending. RAG healthy (24 files indexed). Repo clean on main.

**Confirmed today:**
- Supabase has **140 projects** (not ~580 — prior estimate was wrong)
- All required env vars present and working
- Frank Barrett confirmed as PM for 7510 (frankb@interworkoffice.com, 718-775-6242)

**July 1 is tomorrow — two jobs are unconfirmed:**

| # | Project | Risk | Key gap |
|---|---------|------|---------|
| 7510 | Pear Relocation San Francisco CA | 🔴 CRITICAL | Vendor required, none assigned. No street address. Frank Barrett must be reached today. |
| 7189 | MMC Bermuda Inventory Hoboken NJ | 🟡 MEDIUM | No client confirmation. Hunter Barbieri needs to confirm Jairo Escalante is set. |

**Held items still waiting for Alejandro:**
- "approve batch complete 6" → sets status=completed on 7374, 7499, 7498, 7347, 7472, 7482
- "apply 7447 fix" → nulls bad actual_end_at on project 7447
- "send it" → draft confirmations for 7060 and 7348

**Infrastructure blockers:**
- M365 OAuth not connected → no Teams/Outlook reads
- FastField webhook not yet tested → fastfield_submitted stays manual

**Open questions for ChatGPT:**
1. Is the 6-project batch approval sequencing right? Should any of those 6 be re-evaluated before marking completed?
2. For 7304 (Montebello Jul 2), 7494 (MMA Jul 6), 7546 (MMA Jul 9) — all upcoming, all missing PM — what's the recommended escalation path when a PM isn't assigned this close to the job date?
3. Any flags on the 48 past-dated "scheduled" projects before we batch-update them?
