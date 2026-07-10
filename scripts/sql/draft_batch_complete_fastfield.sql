-- ============================================================
-- DRAFT — Batch status → completed for fastfield-submitted projects
-- STATUS: REVIEW ONLY — DO NOT RUN without Alejandro approval
-- SCOPE:  11 past-dated scheduled projects with fastfield_submitted = true
-- SAFE:   Wrapped in BEGIN / ROLLBACK. Change ROLLBACK → COMMIT to apply.
-- ============================================================

-- ── Projects covered ──────────────────────────────────────────────────────────
--
-- STRONG SIGNAL (fastfield + actual_end_at):
--   7364  MMC Allentown Move & Workstation Setup Support     (actual_end_at: 2026-04-20)
--   7447  MMA Tech Install Move Clearwater Tampa FL          (actual_end_at: 2026-04-15)
--
-- FASTFIELD ONLY:
--   7053  Strategic Education Washington DC
--   7374  Ingersoll Rand Internal Move Buffalo NY
--   7499  MMC Hoboken to Huddle Room King of Prussia PA
--   7498  MMC Furniture from 1166 Hoboken NJ
--   7482  Amtrust Furniture Delivery & Installation Jersey City NJ
--   7472  MMA Walkthrough Addison TX + Colleague Relocation Dallas TX
--
-- ⚠️  VERIFY SCOPE BEFORE INCLUDING in batch (multi-phase — are all phases done?):
--   7391  Premier Orthopedics Multi-Phase Newtown Square PA
--   7352  Goldberg Segalla Phase 1 Decom White Plains NY
--
-- REMOVED 2026-07-10 (Claude Code): 7347 MMA Colleague Relocation McLean VA.
-- A Claude Chat handoff found the Zoom Room AV system from this project was
-- never fully shipped to Wilmington — real, active recovery work is still
-- open (see memory/clients/marsh_mclennan/projects/7347_mma_mclean_consolidation/).
-- fastfield_submitted=true only reflects the original move, not this. Do not
-- re-add 7347 here until that recovery closes out.
--
-- ── What this does ────────────────────────────────────────────────────────────
-- Sets status = 'completed' on the 8 confirmed projects.
-- 7391 and 7352 are excluded by default — remove the exclusion once scope confirmed.
-- Logs each change to activity_log with actor = 'alejandro', source = 'manual_review'.
-- ──────────────────────────────────────────────────────────────────────────────

BEGIN;

-- ── Step 1: Preview what will change ─────────────────────────────────────────
SELECT project_number, name, status, scheduled_date, fastfield_submitted, actual_end_at
FROM public.projects
WHERE project_number IN (
    '7364','7053','7374','7499','7498','7482','7472','7447'
    -- Add '7391','7352' here once multi-phase scope is confirmed
)
ORDER BY scheduled_date;

-- ── Step 2: Apply status change ───────────────────────────────────────────────
UPDATE public.projects
SET
    status     = 'completed',
    updated_at = now()
WHERE project_number IN (
    '7364','7053','7374','7499','7498','7482','7472','7447'
    -- Add '7391','7352' here once multi-phase scope is confirmed
)
  AND status = 'scheduled';   -- Safety: only touch scheduled, never overwrite other statuses

-- ── Step 3: Log to activity_log ───────────────────────────────────────────────
INSERT INTO public.activity_log (project_id, action, actor, source, detail, created_at)
SELECT
    p.id,
    'status_update',
    'alejandro',
    'manual_review',
    'Batch status → completed. Signal: fastfield_submitted = true (past-dated scheduled backfill 2026-06-26)',
    now()
FROM public.projects p
WHERE p.project_number IN (
    '7364','7053','7374','7499','7498','7482','7472','7447'
);

-- ── Step 4: Verify — confirm only targeted projects changed ──────────────────
SELECT project_number, name, status, updated_at
FROM public.projects
WHERE project_number IN (
    '7364','7053','7374','7499','7498','7482','7472','7447','7391','7352'
)
ORDER BY project_number;

-- ── Step 5: Confirm no other projects were touched ───────────────────────────
SELECT COUNT(*) AS in_progress_count   FROM public.projects WHERE status = 'in_progress';
SELECT COUNT(*) AS scheduled_count     FROM public.projects WHERE status = 'scheduled';
SELECT COUNT(*) AS completed_count     FROM public.projects WHERE status = 'completed';

-- ─────────────────────────────────────────────────────────────────────────────
-- DEFAULT: ROLLBACK (safe — nothing is written until you change this to COMMIT)
-- Once you've reviewed the Step 4/5 output and approve, change to COMMIT.
-- ─────────────────────────────────────────────────────────────────────────────
ROLLBACK;
-- COMMIT;
