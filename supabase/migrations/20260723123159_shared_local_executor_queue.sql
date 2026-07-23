create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

create table private.local_executor_queue_tokens (
    token_hash bytea primary key,
    token_role text not null check (token_role in ('submitter', 'worker')),
    label text not null check (length(label) between 1 and 100),
    created_at timestamptz not null default now(),
    revoked_at timestamptz
);

alter table private.local_executor_queue_tokens enable row level security;

create table private.local_executor_queue (
    id uuid primary key default gen_random_uuid(),
    task_id text not null unique
        check (task_id ~ '^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$'),
    payload jsonb not null
        check (jsonb_typeof(payload) = 'object')
        check (octet_length(payload::text) <= 262144),
    status text not null default 'pending'
        check (status in ('pending', 'claimed', 'submitted', 'rejected')),
    submitted_token_hash bytea not null references private.local_executor_queue_tokens(token_hash),
    submitted_at timestamptz not null default now(),
    claimed_at timestamptz,
    claim_token uuid,
    worker_id text,
    claim_attempts integer not null default 0 check (claim_attempts >= 0),
    completed_at timestamptz,
    result jsonb,
    error text,
    check ((payload ->> 'task_id') = task_id),
    check (
        (status = 'pending' and claimed_at is null and claim_token is null and completed_at is null)
        or (status = 'claimed' and claimed_at is not null and claim_token is not null and completed_at is null)
        or (status in ('submitted', 'rejected') and completed_at is not null)
    )
);

alter table private.local_executor_queue enable row level security;

create index local_executor_queue_pending_idx
    on private.local_executor_queue (submitted_at)
    where status = 'pending';

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

    if v_role not in ('submitter', 'worker') then
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

create or replace function public.claim_local_executor_task(
    p_token text,
    p_worker_id text,
    p_lease_seconds integer default 900
)
returns table (queue_id uuid, claim_token uuid, task jsonb)
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_hash bytea := extensions.digest(p_token, 'sha256');
    v_id uuid;
begin
    if not exists (
        select 1 from private.local_executor_queue_tokens t
        where t.token_hash = v_hash
          and t.token_role = 'worker'
          and t.revoked_at is null
    ) then
        raise exception 'invalid worker credential' using errcode = '28000';
    end if;
    if p_worker_id !~ '^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$' then
        raise exception 'invalid worker_id' using errcode = '22023';
    end if;
    if p_lease_seconds < 60 or p_lease_seconds > 3600 then
        raise exception 'lease must be between 60 and 3600 seconds' using errcode = '22023';
    end if;

    update private.local_executor_queue q
    set status = 'pending',
        claimed_at = null,
        claim_token = null,
        worker_id = null
    where q.status = 'claimed'
      and q.claimed_at < now() - make_interval(secs => p_lease_seconds);

    select q.id into v_id
    from private.local_executor_queue q
    where q.status = 'pending'
    order by q.submitted_at, q.id
    for update skip locked
    limit 1;

    if v_id is null then
        return;
    end if;

    return query
    update private.local_executor_queue q
    set status = 'claimed',
        claimed_at = now(),
        claim_token = gen_random_uuid(),
        worker_id = p_worker_id,
        claim_attempts = q.claim_attempts + 1
    where q.id = v_id
    returning q.id, q.claim_token, q.payload;
end;
$$;

create or replace function public.complete_local_executor_task(
    p_token text,
    p_queue_id uuid,
    p_claim_token uuid,
    p_status text,
    p_result jsonb default null,
    p_error text default null
)
returns table (queue_id uuid, task_id text, status text)
language plpgsql
security definer
set search_path = ''
as $$
declare
    v_hash bytea := extensions.digest(p_token, 'sha256');
begin
    if not exists (
        select 1 from private.local_executor_queue_tokens t
        where t.token_hash = v_hash
          and t.token_role = 'worker'
          and t.revoked_at is null
    ) then
        raise exception 'invalid worker credential' using errcode = '28000';
    end if;
    if p_status not in ('submitted', 'rejected') then
        raise exception 'invalid completion status' using errcode = '22023';
    end if;

    return query
    update private.local_executor_queue q
    set status = p_status,
        completed_at = now(),
        result = p_result,
        error = case when p_status = 'rejected' then left(p_error, 4000) else null end
    where q.id = p_queue_id
      and q.status = 'claimed'
      and q.claim_token = p_claim_token
    returning q.id, q.task_id, q.status;

    if not found then
        raise exception 'queue claim is missing or expired' using errcode = 'P0002';
    end if;
end;
$$;

create or replace function public.get_local_executor_task_status(
    p_token text,
    p_queue_id uuid
)
returns table (
    queue_id uuid,
    task_id text,
    status text,
    submitted_at timestamptz,
    completed_at timestamptz,
    result jsonb,
    error text
)
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

    if v_role is null then
        raise exception 'invalid queue credential' using errcode = '28000';
    end if;

    return query
    select q.id, q.task_id, q.status, q.submitted_at, q.completed_at, q.result, q.error
    from private.local_executor_queue q
    where q.id = p_queue_id
      and (v_role = 'worker' or q.submitted_token_hash = v_hash);
end;
$$;

revoke all on function public.enqueue_local_executor_task(text, jsonb) from public, anon, authenticated;
revoke all on function public.claim_local_executor_task(text, text, integer) from public, anon, authenticated;
revoke all on function public.complete_local_executor_task(text, uuid, uuid, text, jsonb, text) from public, anon, authenticated;
revoke all on function public.get_local_executor_task_status(text, uuid) from public, anon, authenticated;

grant execute on function public.enqueue_local_executor_task(text, jsonb) to anon, authenticated;
grant execute on function public.claim_local_executor_task(text, text, integer) to anon, authenticated;
grant execute on function public.complete_local_executor_task(text, uuid, uuid, text, jsonb, text) to anon, authenticated;
grant execute on function public.get_local_executor_task_status(text, uuid) to anon, authenticated;
