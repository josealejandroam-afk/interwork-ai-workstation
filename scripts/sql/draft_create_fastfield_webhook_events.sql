-- fastfield_webhook_events: raw intake buffer for FastField HTTP webhook payloads
-- Purpose: store every incoming webhook before any project matching or field updates
-- This is purely additive — no changes to existing tables
-- Constraint: fastfield_forms.project_id is NOT NULL, so it cannot store unmatched events
-- Created: 2026-06-26 | Awaiting Alejandro approval before applying
--
-- Change ROLLBACK to COMMIT to apply.

BEGIN;

CREATE TABLE IF NOT EXISTS public.fastfield_webhook_events (
    id                         uuid        PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),
    received_at                timestamptz NOT NULL DEFAULT now(),
    source                     text        NOT NULL DEFAULT 'fastfield',
    form_name                  text,
    submission_id              text,
    project_number_detected    text,
    submitter_name             text,
    submitted_at               timestamptz,
    raw_payload                jsonb       NOT NULL DEFAULT '{}',
    processed                  boolean     NOT NULL DEFAULT false,
    processing_status          text        NOT NULL DEFAULT 'pending'
                                           CHECK (processing_status IN ('pending', 'matched', 'unmatched', 'error', 'skipped')),
    matched_project_id         uuid        REFERENCES public.projects(id),
    matched_project_confidence text        CHECK (matched_project_confidence IN ('high', 'medium', 'low', NULL)),
    error_message              text,
    created_at                 timestamptz NOT NULL DEFAULT now(),
    updated_at                 timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE public.fastfield_webhook_events IS
    'Raw FastField webhook intake buffer. Every inbound submission is stored here first. '
    'No project fields are updated from this table automatically. '
    'Alejandro approves all downstream project updates via /completion-intake.';

ROLLBACK; -- Change to COMMIT to apply
