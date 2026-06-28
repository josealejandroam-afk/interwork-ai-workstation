-- DRAFT ONLY — NOT APPLIED
-- Review this before approving.
--
-- Project 7447: MMA Tech Install Move Clearwater Tampa FL
-- Problem: actual_end_at = 2026-04-15 which is BEFORE scheduled_date = 2026-06-16
-- This is a data entry error (actual_end set ~2 months before the job even started).
-- Fix: NULL out the invalid actual_end_at.
-- Status stays as 'scheduled' — do not change status until project is actually completed.
--
-- To apply: change ROLLBACK to COMMIT and run.

BEGIN;

-- Step 1: NULL out the invalid actual_end_at
UPDATE public.projects
SET
    actual_end_at = NULL,
    updated_at    = NOW()
WHERE project_number = '7447'
  AND actual_end_at = '2026-04-15 12:00:00+00';  -- safety guard: only if value is the known-bad one

-- Step 2: Log to activity_log
INSERT INTO public.activity_log (
    project_id,
    actor,
    action,
    detail,
    source,
    before_state,
    after_state,
    occurred_at
)
SELECT
    p.id,
    'alejandro',
    'field_correction',
    'Cleared invalid actual_end_at (2026-04-15) that predated scheduled_start (2026-06-16). Data entry error.',
    'manual',
    jsonb_build_object('actual_end_at', '2026-04-15T12:00:00+00:00'),
    jsonb_build_object('actual_end_at', NULL),
    NOW()
FROM public.projects p
WHERE p.project_number = '7447';

-- Verify
SELECT
    project_number,
    name,
    scheduled_date,
    scheduled_end_date,
    actual_end_at,
    status
FROM public.projects
WHERE project_number = '7447';

ROLLBACK;  -- Change to COMMIT to apply
