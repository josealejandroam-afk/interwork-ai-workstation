# Secret Scan Report

Generated: 2026-06-28 12:38
Scope: D:\ai-workstation (excludes .venv, stores/, .git/)

## Result: CLEAN

The 1 "possible secret value" hit was a **false positive**. Reviewed manually:

| File | Line | Pattern Type | Actual Content | Verdict |
|------|------|-------------|----------------|---------|
| \commands\ask-openai-review.md | 135 | OPENAI_API_KEY\s*=\s... | `$env:OPENAI_API_KEY = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY","User")` | FALSE POSITIVE — PowerShell reads from env var, no literal key value |

No actual secret values found anywhere in the repo.

## Keyword Reference Hits (name-only, no values)

These files reference secret *names* (env var names, config keys, policy docs).
No actual secret values present.

| File | Line | Keyword |
|------|------|---------|
| \commands\ask-openai-review.md | 1 | OPENAI |
| \commands\ask-openai-review.md | 3 | OPENAI |
| \commands\ask-openai-review.md | 4 | SUPABASE |
| \commands\ask-openai-review.md | 14 | OPENAI |
| \commands\ask-openai-review.md | 15 | SUPABASE |
| \commands\ask-openai-review.md | 17 | OPENAI |
| \commands\ask-openai-review.md | 31 | secret |
| \commands\ask-openai-review.md | 33 | OPENAI |
| \commands\ask-openai-review.md | 34 | SUPABASE |
| \commands\ask-openai-review.md | 42 | OPENAI |
| \commands\ask-openai-review.md | 46 | SUPABASE |
| \commands\ask-openai-review.md | 55 | OPENAI |
| \commands\ask-openai-review.md | 87 | SUPABASE |
| \commands\ask-openai-review.md | 135 | api_key |
| \commands\ask-openai-review.md | 136 | OPENAI |
| \commands\ask-openai-review.md | 141 | OPENAI |
| \commands\ask-openai-review.md | 156 | OPENAI |
| \commands\ask-openai-review.md | 168 | SUPABASE |
| \commands\ask-openai-review.md | 198 | api_key |
| \commands\ask-openai-review.md | 199 | secret |
| \commands\completion-backlog.md | 70 | SUPABASE |
| \commands\completion-backlog.md | 132 | SUPABASE |
| \commands\completion-backlog.md | 143 | SUPABASE |
| \commands\completion-intake.md | 3 | SUPABASE |
| \commands\completion-intake.md | 63 | SUPABASE |
| \commands\completion-intake.md | 144 | SUPABASE |
| \commands\completion-intake.md | 177 | SUPABASE |
| \commands\completion-intake.md | 208 | SUPABASE |
| \commands\completion-intake.md | 211 | SUPABASE |
| \commands\completion-intake.md | 213 | SUPABASE |
| \commands\dashboard-status.md | 3 | SUPABASE |
| \commands\dashboard-status.md | 12 | SUPABASE |
| \commands\dashboard-status.md | 74 | SUPABASE |
| \commands\fastfield-assignment-watch.md | 21 | SUPABASE |
| \commands\fastfield-assignment-watch.md | 24 | webhook |
| \commands\fastfield-assignment-watch.md | 65 | webhook |
| \commands\fastfield-assignment-watch.md | 68 | webhook |
| \commands\fastfield-assignment-watch.md | 96 | SUPABASE |
| \commands\fastfield-assignment-watch.md | 98 | webhook |
| \commands\fastfield-assignment-watch.md | 103 | webhook |
| \commands\fastfield-assignment-watch.md | 115 | SUPABASE |
| \commands\fastfield-intake.md | 3 | webhook |
| \commands\fastfield-intake.md | 10 | webhook |
| \commands\fastfield-intake.md | 12 | SUPABASE |
| \commands\fastfield-intake.md | 16 | SUPABASE |
| \commands\fastfield-intake.md | 35 | webhook |
| \commands\fastfield-intake.md | 44 | webhook |
| \commands\fastfield-intake.md | 69 | SUPABASE |
| \commands\fastfield-intake.md | 122 | webhook |
| \commands\fastfield-intake.md | 132 | SUPABASE |
| \commands\fastfield-intake.md | 152 | webhook |
| \commands\fastfield-intake.md | 163 | webhook |
| \commands\feedback-status.md | 23 | OPENAI |
| \commands\feedback-status.md | 56 | OPENAI |
| \commands\feedback-status.md | 63 | OPENAI |
| \commands\feedback-status.md | 71 | OPENAI |
| \commands\ff-sent.md | 21 | SUPABASE |
| \commands\ff-sent.md | 23 | webhook |
| \commands\ff-sent.md | 31 | SUPABASE |
| \commands\ff-sent.md | 36 | SUPABASE |
| ... | ... | (+405 more keyword refs) |

## Patterns Checked

Secret value patterns (actual values, not just names):
- Assignment patterns: api_key='...', token='...', secret='...', password='...'
- Bearer tokens: bearer <20+ char token>
- JWT tokens: eyJ... (30+ chars)
- OpenAI keys: sk-<20+ chars>
- Supabase/OpenAI key assignments with values

## What Was NOT Checked

- .env files (none found in repo)
- Windows registry (not in scope)
- .venv virtual environment (excluded)
- D:\ai-cache (HuggingFace model weights, not secrets)
