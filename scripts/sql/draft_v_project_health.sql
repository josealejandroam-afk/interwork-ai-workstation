-- ============================================================
-- DRAFT — v_project_health view for interwork-command-center
-- STATUS: APPLIED 2026-06-26 via apply_migration (create_v_project_health_view)
-- BUG FIX: original used `b.*` in scored CTE but `FROM base` without alias.
--           Applied version uses `FROM base AS b` with columns explicitly qualified.
-- PURPOSE: Deterministic, phase-aware health scoring for all
--          active/scheduled projects. SQL handles hard rules;
--          Claude handles judgment/context risks.
-- ============================================================

CREATE OR REPLACE VIEW public.v_project_health AS
WITH base AS (
    SELECT
        p.id,
        p.project_number,
        p.name,
        p.type,
        p.status,
        p.scheduled_date,
        p.scheduled_end_date,
        p.pm_assigned,
        p.vendor_required,
        p.vendor_confirmed,
        p.client_confirmed,
        p.access_confirmed,
        p.client_informed,
        p.fastfield_submitted,
        p.completion_report_sent,
        p.invoiced,

        -- Proximity
        (p.scheduled_date - CURRENT_DATE)::int  AS days_until,
        (CURRENT_DATE - p.scheduled_date)::int  AS days_past,

        -- Missing critical confirmations (weighted by proximity)
        (
            CASE WHEN p.vendor_required AND NOT p.vendor_confirmed  THEN 1 ELSE 0 END +
            CASE WHEN NOT p.client_confirmed                        THEN 1 ELSE 0 END +
            CASE WHEN NOT p.access_confirmed                        THEN 1 ELSE 0 END +
            CASE WHEN NOT p.pm_assigned                             THEN 1 ELSE 0 END +
            CASE WHEN NOT p.client_informed                         THEN 1 ELSE 0 END
        )::int AS missing_count

    FROM public.projects p
    WHERE p.status NOT IN ('completed', 'closed', 'cancelled')
),
scored AS (
    SELECT
        b.*,

        -- ── Health color ─────────────────────────────────────────
        CASE
            -- Overdue: past scheduled date, still in_progress
            WHEN status = 'in_progress' AND days_past > 0
                THEN 'red'

            -- Imminent (≤3 days): any critical item missing
            WHEN days_until <= 3
             AND (    (vendor_required AND NOT vendor_confirmed)
                   OR NOT access_confirmed
                   OR NOT pm_assigned)
                THEN 'red'

            -- Near-term (≤7 days): vendor or access missing
            WHEN days_until <= 7
             AND (    (vendor_required AND NOT vendor_confirmed)
                   OR NOT access_confirmed)
                THEN 'red'

            -- Two-week window: vendor unconfirmed
            WHEN days_until <= 14
             AND vendor_required AND NOT vendor_confirmed
                THEN 'yellow'

            -- No PM assigned at any horizon
            WHEN NOT pm_assigned
                THEN 'yellow'

            -- Client not informed for upcoming work
            WHEN days_until <= 14 AND NOT client_informed
                THEN 'yellow'

            -- Missing items but comfortably in future
            WHEN missing_count > 0
                THEN 'yellow'

            ELSE 'green'
        END AS health_color,

        -- ── Top risk factor (first match wins) ───────────────────
        CASE
            WHEN status = 'in_progress' AND days_past > 0
                THEN 'overdue_in_progress'
            WHEN days_until <= 3 AND vendor_required AND NOT vendor_confirmed
                THEN 'vendor_unconfirmed_imminent'
            WHEN days_until <= 3 AND NOT access_confirmed
                THEN 'access_unconfirmed_imminent'
            WHEN NOT pm_assigned
                THEN 'no_pm_assigned'
            WHEN vendor_required AND NOT vendor_confirmed
                THEN 'vendor_unconfirmed'
            WHEN NOT access_confirmed
                THEN 'access_unconfirmed'
            WHEN NOT client_confirmed
                THEN 'client_unconfirmed'
            WHEN NOT client_informed
                THEN 'client_not_informed'
            ELSE NULL
        END AS top_risk,

        -- ── Numeric score (100 = perfect, lower = worse) ─────────
        GREATEST(0,
            100
            - CASE WHEN status = 'in_progress' AND days_past > 0 THEN 40 ELSE 0 END
            - CASE WHEN vendor_required AND NOT vendor_confirmed
                   THEN LEAST(30, GREATEST(5, 30 - days_until))   -- proximity-weighted
                   ELSE 0 END
            - CASE WHEN NOT access_confirmed
                   THEN LEAST(20, GREATEST(3, 20 - days_until))
                   ELSE 0 END
            - CASE WHEN NOT client_confirmed  THEN 10 ELSE 0 END
            - CASE WHEN NOT pm_assigned       THEN 15 ELSE 0 END
            - CASE WHEN NOT client_informed   THEN  5 ELSE 0 END
        )::int AS health_score

    FROM base
)
SELECT
    id,
    project_number,
    name,
    type,
    status,
    scheduled_date,
    days_until,
    days_past,
    health_color,
    health_score,
    top_risk,
    missing_count,
    pm_assigned,
    vendor_required,
    vendor_confirmed,
    client_confirmed,
    access_confirmed,
    client_informed,
    fastfield_submitted,
    completion_report_sent,
    invoiced
FROM scored
ORDER BY
    -- Reds first, then yellows, then greens; within color sort by proximity
    CASE health_color WHEN 'red' THEN 0 WHEN 'yellow' THEN 1 ELSE 2 END,
    CASE WHEN days_until < 0 THEN days_until ELSE 0 END,   -- most overdue first
    days_until ASC NULLS LAST;

-- ============================================================
-- NOTES
-- ============================================================
-- * health_score is deterministic — SQL only. Claude adds judgment
--   context on top (e.g. "vendor email received but not yet marked
--   confirmed in Supabase").
-- * Proximity weighting: vendor_confirmed penalty scales from 5 pts
--   (far out) to 30 pts (imminent) using LEAST/GREATEST.
-- * top_risk is the single most actionable item to surface per project.
-- * /project-health queries this view. /dashboard-status queries
--   the raw projects table (lightweight).
-- * Extend with additional checks as the workflow matures:
--   e.g. fastfield_submitted, completion_report_sent for in_progress.
-- * RLS: apply same policy as open_loops once RLS project is complete.
-- ============================================================
