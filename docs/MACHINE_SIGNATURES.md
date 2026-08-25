# InterWork Machine Signatures

Every workstation or automated agent that changes Git or Supabase must identify itself with a stable audit signature.

## Identity format

Use `Agent@Machine`, for example:

- `Codex@FrankWork`
- `ClaudeCode@OperationsLaptop`
- `Human@AlejandroDesktop`

This is audit metadata, not authentication. Do not put passwords, tokens, email addresses, or other secrets in a signature.

## One-time setup on each machine

From the repository root, run:

```powershell
.\scripts\setup_machine_signature.ps1 -MachineId "FrankWork" -AgentId "Codex"
```

Choose a short, unique machine name and identify the system making commits. The setup is repository-local and does not replace the normal Git author name or email.

## Git behavior

New commits automatically receive these trailers:

```text
InterWork-Actor: Codex@FrankWork
InterWork-Machine: FrankWork
```

GitHub still records the authenticated account that pushes the commit. These trailers identify where and by which system the commit was created.

## Supabase behavior

Every approved material Supabase write must continue to insert an `activity_log` record. Set:

- `actor` to the same `Agent@Machine` signature used by Git.
- `source` to `manual` until the database enum is intentionally extended.
- `before_state` and `after_state` where practical.

Example actor for this workstation: `Codex@FrankWork`.

No historical commits or database entries are backfilled. This convention applies moving forward.

