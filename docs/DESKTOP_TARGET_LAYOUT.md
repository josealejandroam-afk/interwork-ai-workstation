# Desktop Drive Layout (Target)

This document defines the intended drive layout for the AI workstation once setup is complete.

---

## Drive Assignment

| Drive | Label | Type | Purpose |
|-------|-------|------|---------|
| **C:** | Local Drive | NVMe SSD (465 GB) | Windows OS, system apps, Steam client only |
| **D:** | Games Drive | SATA SSD (477 GB) | AI workstation repo, caches, active AI work, Python environments, active games |
| **E:** | Extra Storage | HDD (932 GB) | Backups, archives, bulk storage, rarely played games |

---

## C: — OS and System Only

- Windows 11 Pro system files
- Installed applications (non-AI)
- Steam client (the launcher, not game files)
- Do **not** store AI projects, model caches, or virtual environments here

---

## D: — Active AI Work

| Path | Purpose |
|------|---------|
| `D:\ai-workstation` | Main project repo (final target — move from C: after Steam cleanup) |
| `D:\ai-cache\uv` | uv package manager cache |
| `D:\ai-cache\pip` | pip download cache |
| `D:\ai-cache\huggingface` | HuggingFace model hub downloads |
| `D:\ai-cache\torch` | PyTorch hub cache |
| `D:\ai-cache\models` | Manually downloaded models |
| `D:\SteamLibrary` | Active Steam games (CS2 currently here) |

### Environment Variables (already set)

```
UV_CACHE_DIR        = D:\ai-cache\uv
PIP_CACHE_DIR       = D:\ai-cache\pip
HF_HOME             = D:\ai-cache\huggingface
TRANSFORMERS_CACHE  = D:\ai-cache\huggingface
TORCH_HOME          = D:\ai-cache\torch
```

---

## E: — Archive and Bulk Storage

| Path | Purpose |
|------|---------|
| `E:\SteamLibrary` | Rarely played games (RE Requiem, AoM, Buckshot moving here) |
| `E:\ai-backups` | Backup root for AI workstation snapshots |
| `E:\archives` | Long-term document and project archives |

---

## Current vs Target State

| Item | Current Location | Target Location | Status |
|------|-----------------|-----------------|--------|
| ai-workstation repo | `C:\Users\Owner\Documents\ai-workstation` | `D:\ai-workstation` | Pending — move after Steam finishes |
| AI caches | (none — newly configured) | `D:\ai-cache\*` | ✅ Configured |
| CS2 | C: → D: ✅ | `D:\SteamLibrary` | ✅ Done |
| RE Requiem | C: | `E:\SteamLibrary` | 🔄 Moving |
| Age of Mythology | C: | `E:\SteamLibrary` | ⏳ Queued |
| Buckshot Roulette | C: | `E:\SteamLibrary` | ⏳ Queued |
| Jedi: Survivor | ✅ Uninstalled | — | ✅ Done |
| Jedi: Fallen Order | ✅ Uninstalled | — | ✅ Done |

---

## Repo Move Plan (after Steam finishes)

1. Verify all 3 games have moved to E: and manifests are present
2. Confirm C: free space is stable
3. Copy `C:\Users\Owner\Documents\ai-workstation` → `D:\ai-workstation`
4. Reinitialize git remote (if any) pointing to new path
5. Update any shell shortcuts or Claude Code project paths
6. Archive the C: copy (do not delete immediately — verify D: copy first)

---

*Last updated: 2026-06-28*
