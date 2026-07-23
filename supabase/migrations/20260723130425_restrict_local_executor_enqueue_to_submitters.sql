-- Human-run production hardening.
-- This migration has not been executed by Codex.

create or replace function public.enqueue_local_executor_task(
    p_token text,
    p_task jsonb
)
returns table (queue_id uuid, task_id text, status text)
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_hash bytea := extensions.digest(p_token, 'sha256');
    v_role text;
begin
    select t.token_role into v_role
    from private.local_executor_queue_tokens t
    where t.token_hash = v_hash and t.revoked_at is null;

    if v_role is distinct from 'submitter' then
        raise exception 'invalid queue credential' using errcode = '28000';
    end if;
    if jsonb_typeof(p_task) is distinct from 'object' then
        raise exception 'task must be a JSON object' using errcode = '22023';
    end if;
    if coalesce(p_task ->> 'task_id', '') !~ '^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$' then
        raise exception 'invalid task_id' using errcode = '22023';
    end if;
    if octet_length(p_task::text) > 262144 then
        raise exception 'task exceeds queue size limit' using errcode = '22023';
    end if;

    return query
    insert into private.local_executor_queue (task_id, payload, submitted_token_hash)
    values (p_task ->> 'task_id', p_task, v_hash)
    returning local_executor_queue.id, local_executor_queue.task_id, local_executor_queue.status;
end;
$$;

revoke all on function public.enqueue_local_executor_task(text, jsonb)
    from public, anon, authenticated;
grant execute on function public.enqueue_local_executor_task(text, jsonb)
    to anon, authenticated;
