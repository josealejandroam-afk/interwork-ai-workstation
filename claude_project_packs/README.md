# Claude Project Packs — Fallback Only
_Last updated: 2026-06-30_

---

## Status: Fallback

These files are **no longer the primary source of truth** for Claude Chat projects.

The preferred architecture is:

```
Bootstrap file (uploaded once)  →  tells Claude Chat how to reach the repo
GitHub repo                     →  holds all changing project facts
Dashboard snapshot (in repo)    →  live operational status
```

See `docs/CLAUDE_PROJECT_BOOTSTRAP_MODEL.md` for the full explanation.

---

## When to Use a Pack

Use a pack only when:
- The Claude Chat session cannot fetch raw GitHub URLs
- Alejandro explicitly asks to use the pack as a reference

When using a pack, always check the `Generated:` date at the top.
- If the pack is more than a few days old, treat project-specific facts (dates, status, open loops) as potentially stale.
- Use the pack for contacts and routing patterns.
- Prefer the repo for current facts.

---

## Preferred Alternative

Upload `claude_project_bootstraps/<client_slug>_bootstrap.md` to each Claude Project instead.
The bootstrap is stable and does not need to be re-uploaded when project facts change.

---

## Files in This Directory

| Pack | Client | Notes |
|---|---|---|
| marsh_mclennan_knowledge_pack.md | Marsh McLennan | Fallback only — use bootstrap |
| bentley_systems_knowledge_pack.md | Bentley Systems | Fallback only — use bootstrap |
| radian_knowledge_pack.md | Radian | Fallback only — use bootstrap |
| rothman_orthopaedics_knowledge_pack.md | Rothman Orthopaedics | Fallback only — use bootstrap |
| pear_vc_knowledge_pack.md | Pear VC | Fallback only |
| claritev_multiplan_knowledge_pack.md | Claritev / MultiPlan | Fallback only |
| strategic_education_knowledge_pack.md | Strategic Education | Fallback only — use bootstrap |
| premier_orthopaedics_knowledge_pack.md | Premier Orthopaedics | Fallback only |
| percheron_capital_knowledge_pack.md | Percheron Capital | Fallback only |
| ss_c_technologies_knowledge_pack.md | SS&C Technologies | Fallback only |
| bevin_palidar_knowledge_pack.md | Bevin Palidar | Fallback only |
| guardian_knowledge_pack.md | Guardian | Fallback only — use bootstrap |
| uipath_knowledge_pack.md | UiPath | Fallback only — use bootstrap |
| tegna_knowledge_pack.md | Tegna / Premion | Fallback only — use bootstrap |
| goldberg_segalla_knowledge_pack.md | Goldberg Segalla | Fallback only — use bootstrap |
| dropbox_knowledge_pack.md | Dropbox | Fallback only — use bootstrap |
| amtrust_knowledge_pack.md | AmTrust | Fallback only — use bootstrap |
