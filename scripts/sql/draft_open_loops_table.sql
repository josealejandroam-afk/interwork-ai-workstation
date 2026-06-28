-- ============================================================
-- DRAFT — open_loops table for interwork-command-center
-- STATUS: NOT APPLIED — pending Alejandro approval
-- PURPOSE: Canonical open-loop queue in Supabase so the
--          dashboard can display them. Memory/open_loops/
--          mirrors this for RAG context.
-- ============================================================

CREATE TABLE IF NOT EXISTS public.open_loops (
    id              UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),

    -- Link to project (nullable — some loops are not project-specific)
    project_id      UUID REFERENCES public.projects(id) ON DELETE SET NULL,

    -- Content
    title           TEXT NOT NULL,
    detail          TEXT,

    -- Workflow state
    status          TEXT NOT NULL DEFAULT 'open'
                        CHECK (status IN ('open', 'resolved', 'snoozed')),
    priority        TEXT NOT NULL DEFAULT 'medium'
                        CHECK (priority IN ('high', 'medium', 'low')),

    -- Origin
    source          TEXT NOT NULL DEFAULT 'manual'
                        CHECK (source IN ('teams', 'gmail', 'smartsheet', 'fastfield', 'manual', 'ai', 'dashboard')),
    ai_generated    BOOLEAN NOT NULL DEFAULT false,

    -- External reference for dedup (e.g. Gmail thread_id, Teams message_id)
    external_ref    TEXT,

    -- Timestamps
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at     TIMESTAMPTZ
);

-- Index for dashboard queries
CREATE INDEX IF NOT EXISTS open_loops_project_id_idx    ON public.open_loops (project_id);
CREATE INDEX IF NOT EXISTS open_loops_status_idx        ON public.open_loops (status);
CREATE INDEX IF NOT EXISTS open_loops_source_idx        ON public.open_loops (source);
CREATE INDEX IF NOT EXISTS open_loops_priority_idx      ON public.open_loops (priority);

-- Auto-update updated_at on change
CREATE OR REPLACE FUNCTION update_open_loops_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER open_loops_updated_at
    BEFORE UPDATE ON public.open_loops
    FOR EACH ROW EXECUTE FUNCTION update_open_loops_updated_at();

-- ============================================================
-- NOTES
-- ============================================================
-- * project_id is nullable (account-level or cross-project loops)
-- * Memory/open_loops/*.md files mirror these for RAG — sync manually
--   or via a future automation.
-- * external_ref ties back to Gmail message_id or Teams message_id
--   to prevent duplicate loop creation on re-scan.
-- * RLS: apply policies before enabling RLS on this table.
--   Suggested policy: service role has full access; anon has none.
-- ============================================================
