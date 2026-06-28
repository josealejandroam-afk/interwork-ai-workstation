# Desktop PC Inventory
**Generated:** 2026-06-28  
**Purpose:** Technical reference for AI workstation setup — safe read-only data only.

---

## 1. Operating System

| Field | Value |
|-------|-------|
| OS Name | Windows 11 Pro |
| Reported Caption | Microsoft Windows 11 Pro |
| Version | 10.0.26200 |
| Build Number | 26200 |
| Architecture | 64-bit |

> Note: `Get-ComputerInfo` reports "Windows 10 Pro" — this is a known quirk on Windows 11 insider/preview builds. `Win32_OperatingSystem` correctly identifies it as **Windows 11 Pro**.

---

## 2. Computer Name

| Field | Value |
|-------|-------|
| Hostname | DESKTOP-1R6HS6S |

---

## 3. CPU

| Field | Value |
|-------|-------|
| Model | 12th Gen Intel Core i5-12500T |
| Generation | Alder Lake (12th Gen) |

---

## 4. RAM

### Summary

| Field | Value |
|-------|-------|
| Total Physical Memory | 64 GB (68,474,781,696 bytes reported by OS) |
| Sticks | 4 × 16 GB |
| Type | DDR4 |
| Manufacturer | Crucial Technology |
| Rated Speed | 2667 MHz |
| Configured Speed | 2666 MHz (1 MHz BIOS rounding — normal) |
| Slots populated | All 4 (A1, A2, B1, B2) |
| Upgrade path | None — all slots full; would require replacing sticks |

### Module Detail

| Slot | Part Number | Capacity | Speed | Running At |
|------|------------|----------|-------|------------|
| DDR4-A1 | CT16G4DFD8266.C16FP | 16 GB | 2667 MHz | 2666 MHz |
| DDR4-A2 | CT16G4DFD8266.C16FP | 16 GB | 2667 MHz | 2666 MHz |
| DDR4-B1 | CT16G4DFD8266.M16FD | 16 GB | 2667 MHz | 2666 MHz |
| DDR4-B2 | CT16G4DFD8266.C16FP | 16 GB | 2667 MHz | 2666 MHz |

> B1 has a slightly different part number suffix (M16FD vs C16FP) — minor revision difference, compatible in practice. 3 of 4 sticks are a matched set.

### Conclusion

64 GB DDR4 is **sufficient for the AI workstation**. RAM is not a bottleneck. The main constraint is C: drive free space (3.7 GB), not memory.

---

## 5. GPU

| GPU | VRAM (reported) |
|-----|----------------|
| NVIDIA GeForce RTX 5060 Ti | ~4 GB (reported; actual VRAM is higher — Windows reports shared memory floor) |
| Intel UHD Graphics 770 | ~2 GB (integrated, iGPU) |

> The RTX 5060 Ti is a discrete GPU. The 4 GB figure from Win32 is an artifact of how Windows reports VRAM; actual VRAM should be confirmed via NVIDIA Control Panel or `nvidia-smi`.

---

## 6. Disk Drives

### Physical Disks

| Drive | Type | Total Size |
|-------|------|-----------|
| Samsung SSD 850 EVO 500GB | SSD | 500 GB |
| TOSHIBA MQ01ABD100 | HDD | 1,000 GB (1 TB) |
| PC601 NVMe SK hynix 512GB | SSD (NVMe) | 512 GB |

### Logical Volumes

| Drive | Total (GB) | Used (GB) | Free (GB) |
|-------|-----------|----------|----------|
| C: | 464.8 | 461.1 | **3.7** |
| D: | 476.9 | 107.1 | 369.9 |
| E: | 931.5 | 7.8 | 923.7 |

> **C: drive has only 3.7 GB free.** This is a critical issue — package installs, virtual environments, and model weights will fail or degrade. Immediate cleanup or redirection to D: or E: is recommended before proceeding with AI workstation setup.

---

## 7. PowerShell Version

| Field | Value |
|-------|-------|
| Version | 5.1.26100.8655 (Windows PowerShell) |
| Note | PowerShell 7 (pwsh) not detected in PATH |

---

## 8. Git

| Field | Value |
|-------|-------|
| Status | Installed |
| Version | 2.54.0.windows.1 |

---

## 9. Python

| Field | Value |
|-------|-------|
| Status | Installed (this session) |
| Version | 3.12.10 |
| Launcher | `py` (Windows launcher — use this, not `python`) |
| Note | `python` command routes to Windows Store stub. Disable via Settings > Apps > Advanced app settings > App execution aliases if needed. |

---

## 10. uv

| Field | Value |
|-------|-------|
| Status | Installed (this session) |
| Version | 0.11.25 |
| Note | PATH update requires a new shell session to take effect |

---

## 11. winget

| Field | Value |
|-------|-------|
| Status | Installed |
| Version | v1.28.240 |

---

## 12. Node / npm

| Field | Value |
|-------|-------|
| Status | Not installed |
| node | Not found |
| npm | Not found |

---

## 13. Docker

| Field | Value |
|-------|-------|
| Status | Not installed |
| Note | Docker Desktop not found in PATH |

---

## 14. WSL (Windows Subsystem for Linux)

| Field | Value |
|-------|-------|
| Status | Not installed |
| Note | `wsl --install` required to enable |

---

## 15. OneDrive

| Field | Value |
|-------|-------|
| Status | Present |
| Path | `C:\Users\Owner\OneDrive` |
| Top-level folders visible | Documentos, Escritorio, Imágenes, Microsoft File Share |

> Folder names in Spanish suggest the account locale is Spanish. OneDrive is synced and active.

---

## 16. Important Folders

| Folder | Status | Notes |
|--------|--------|-------|
| `C:\Users\Owner\.claude` | Exists (9 items) | Fresh Claude Code install — credentials, sessions, plugins, projects |
| `C:\Users\Owner\scripts` | **Missing** | Needs to be created |
| `C:\Users\Owner\Documents\ai-workstation` | Exists (12 items) | Git repo initialized this session |

### ai-workstation contents

```
ai-workstation/
├── .claude/          (session settings, not committed)
├── .git/             (initialized this session)
├── .gitignore
├── README.md
├── commands/
├── config/
├── docs/
├── logs/
├── memory/
├── rag/
├── scripts/
└── sql/
```

---

## 17. Network Adapters (active only, no IPs)

| Name | Interface Description |
|------|-----------------------|
| Ethernet | Realtek Gaming 2.5GbE Family Controller |

> Only one active adapter found. No Wi-Fi adapter active (could be disabled or absent).

---

## 18. Installed Browsers

| Browser | Status |
|---------|--------|
| Microsoft Edge | Installed (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`) |
| Google Chrome | Not detected (no Win32 install found) |
| Mozilla Firefox | Installed — Windows Store package v151.0.4.0 |
| Brave | Not detected |
| Microsoft Teams | Installed — Windows Store package v26032.208.4399.5 |
| ChatGPT Desktop | Installed — Windows Store package v1.2026.133.0 |
| Claude Desktop | Installed — Windows Store package v1.15962.1.0 |
| Microsoft Office Hub | Installed — Windows Store package v19.2606.39121.0 (web/hub app, not full Office) |

> Firefox, Teams, ChatGPT, and Claude are installed as packaged Windows Store apps — they don't appear in the standard `App Paths` registry keys, which is why the earlier check missed them. All confirmed via `Get-AppxPackage`.

---

## 19. Setup Gaps for AI Workstation (original)

| Gap | Severity | Notes |
|-----|----------|-------|
| **C: drive nearly full (3.7 GB free)** | Critical | Do not install more packages until uv cache, pip cache, and the ai-workstation folder are moved or configured on D:. D: has 370 GB free, E: has 924 GB free. |
| Python `python` command broken | Medium | Use `py` launcher or `uv run`. Disable Store stub in App Execution Aliases settings. |
| WSL not installed | Medium | Required if any Linux-native tools or Docker (Linux containers) are needed |
| Docker not installed | Low-Medium | Needed for containerized services (e.g., Supabase local dev, Qdrant, etc.) |
| Node/npm not installed | Low | Needed if any JS tooling or Claude Code extensions require it |
| PowerShell 7 not installed | Low | PS 5.1 works but PS 7 is faster and cross-platform compatible |
| `C:\Users\Owner\scripts` missing | Low | Placeholder folder for utility scripts — create when ready |
| No uv/Python PATH without shell refresh | Low | Solved by opening a new terminal session after install |
| No GPU drivers verified | Low | RTX 5060 Ti detected but `nvidia-smi` not confirmed — verify CUDA availability if needed for local models |

---

## 20. GPU Readiness

**nvidia-smi ran successfully.**

| Field | Value |
|-------|-------|
| GPU Name | NVIDIA GeForce RTX 5060 Ti |
| VRAM Total | 16,311 MiB (~16 GB) |
| VRAM In Use (at query time) | 2,744 MiB (~2.7 GB, desktop idle) |
| Driver Version | 595.79 |
| CUDA Version | 13.2 |
| Temperature | 46°C (idle) |
| Power Draw | 23W / 180W cap |
| GPU Utilization | 1% (idle) |
| Display Active | Yes |

### Active GPU Processes (at query time)

Notable processes using the GPU:
- `ChatGPT.exe` — ChatGPT desktop app
- `claude.exe` — Claude desktop app (two instances)
- `firefox.exe` — Firefox (two instances)
- `EADesktop.exe` + `EACefSubProcess.exe` — EA Desktop (game launcher)
- `RazerCentral.exe`, `RazerAppEngine.exe` — Razer peripherals software
- `NVIDIA Overlay.exe` — NVIDIA overlay (two instances)

### GPU Conclusion

The RTX 5060 Ti with **16 GB VRAM** is well-suited for local AI workloads:
- Can run 7B–13B parameter models locally (e.g., Mistral 7B, Llama 3 8B) via Ollama or llama.cpp
- 16 GB VRAM supports quantized 30B+ models depending on format
- CUDA 13.2 is current — compatible with PyTorch, llama-cpp-python, etc.
- Driver is up to date (595.79)

---

## 21. Drive Health and Speed

| Drive | Type | Bus | Health | Status | Size (GB) |
|-------|------|-----|--------|--------|-----------|
| Samsung SSD 850 EVO 500GB | SSD | SATA | Healthy | OK | 465.8 |
| TOSHIBA MQ01ABD100 | HDD | SATA | Healthy | OK | 931.5 |
| PC601 NVMe SK hynix 512GB | SSD | NVMe | Healthy | OK | 476.9 |

### Drive Mapping

| Volume | Physical Drive | Type | Total (GB) | Used (GB) | Free (GB) |
|--------|---------------|------|-----------|----------|----------|
| C: | PC601 NVMe SK hynix 512GB | NVMe SSD | 464.8 | 461.1 | **3.7** |
| D: | Samsung SSD 850 EVO 500GB | SATA SSD | 476.9 | 107.1 | 369.9 |
| E: | TOSHIBA MQ01ABD100 | SATA HDD | 931.5 | 7.8 | 923.7 |

All three drives report **Healthy / OK**. No SMART failures or degraded status detected.

### Speed Notes

| Drive | Expected Sequential Read | Best Use |
|-------|------------------------|----------|
| C: (NVMe) | ~2,000–3,500 MB/s | OS, active tools |
| D: (SATA SSD) | ~500–550 MB/s | Project files, virtual envs, caches |
| E: (SATA HDD) | ~100–130 MB/s | Archives, datasets, model weights (cold) |

---

## 22. C: Drive Usage Breakdown

**Goal:** understand why C: has only 3.7 GB free on a 465 GB NVMe drive.

| Folder | Size (GB) |
|--------|----------|
| `C:\Program Files (x86)` | **371.0** |
| `C:\Windows` | 31.4 |
| `C:\Users\Owner` | 14.1 |
| `C:\ProgramData` | 7.0 |
| `C:\Program Files` | 4.4 |
| **Total accounted** | ~427.9 GB |

### Root Cause: Steam

| Subfolder of `C:\Program Files (x86)` | Size (GB) |
|---------------------------------------|----------|
| **Steam** | **363.1** |
| Microsoft | 5.5 |
| Razer | 1.3 |
| Interhaptics | 0.3 |
| NVIDIA Corporation | 0.2 |
| LG Electronics | 0.2 |
| GIGABYTE | 0.1 |
| All others | < 0.1 each |

**Steam and its installed games occupy 363 GB on C: — this is the sole reason C: is nearly full.**

The AI workstation has no disk space problem once Steam is either moved to D: or E:, or games are uninstalled/moved. This is a configuration issue, not a hardware limitation.

---

## 23. Power Settings

| Setting | Value |
|---------|-------|
| Active Power Plan | **Balanced** (GUID: 381b4222-f694-41f0-9685-ff5bb260df2e) |
| Sleep after (AC) | **900 seconds (15 minutes)** |
| Sleep after (DC/battery) | 600 seconds (10 min — likely N/A, desktop) |
| Display off after (AC) | **300 seconds (5 minutes)** |
| Display off after (DC) | 180 seconds (3 min — likely N/A, desktop) |

### Notes

- **Balanced** plan may throttle CPU during long AI tasks. For sustained workloads (RAG indexing, model inference), consider switching to **High Performance** or a custom plan.
- 15-minute sleep timeout will interrupt long-running Python jobs unless sleep is disabled for AI workstation tasks.
- No UPS or power conditioning noted.

---

## 24. OneDrive Status

| Field | Value |
|-------|-------|
| Installed | Yes |
| Version | 26.098.0524.0004 |
| Folder path | `C:\Users\Owner\OneDrive` |
| Folder exists | Yes |
| Sync status | Active (registry key present, no error state) |
| Top-level folders | Documentos, Escritorio, Imágenes, Microsoft File Share |

OneDrive is running and synced. Account locale appears to be Spanish (folder names in Spanish).

---

## 25. Browser and App Readiness

| App | Status | Install Type | Version |
|-----|--------|-------------|---------|
| Microsoft Edge | Installed | Win32 | Current |
| Mozilla Firefox | Installed | Windows Store | 151.0.4.0 |
| Google Chrome | **Not installed** | — | — |
| Brave | **Not installed** | — | — |
| Microsoft Teams | Installed | Windows Store | 26032.208.4399.5 |
| ChatGPT Desktop | Installed | Windows Store | 1.2026.133.0 |
| Claude Desktop | Installed | Windows Store | 1.15962.1.0 |
| Microsoft Office Hub | Installed (web hub only) | Windows Store | 19.2606.39121.0 |
| Full Microsoft 365 / Office | **Not detected** | — | — |

> Office Hub is a launcher/web wrapper — it is not the full desktop Office suite. If Word, Excel, or Outlook are needed for integrations, full Microsoft 365 would need to be installed separately.

---

## 26. AI Workstation Recommendations

### Drive Assignment

| Purpose | Recommended Drive | Reason |
|---------|------------------|--------|
| OS and tools | C: (NVMe) | Already there, fast |
| **Project files** (`ai-workstation`) | **D: (SATA SSD)** | Fast enough, 370 GB free |
| **uv cache / pip cache** | **D:** | Redirect `UV_CACHE_DIR` and `PIP_CACHE_DIR` to `D:\cache\` |
| **Python virtual envs** | **D:** | Keep off C: entirely |
| **Model weights** (Ollama, GGUF, etc.) | **D: or E:** | D: for active models (faster), E: for cold storage |
| **Datasets / RAG corpus** | **E: (HDD)** | Large, rarely accessed at speed |
| Steam / games | Move to E: | Frees ~363 GB on C: — most impactful single action |

### What Should Be Fixed Before Installing RAG Dependencies

| Priority | Action | Why |
|----------|--------|-----|
| **1 — Critical** | Move Steam library to E: or D:, OR move `ai-workstation` to D: | C: has 3.7 GB free — pip/uv installs will fail |
| **2 — Critical** | Set `UV_CACHE_DIR=D:\cache\uv` and `PIP_CACHE_DIR=D:\cache\pip` in system environment | Prevents cache from filling C: |
| **3 — High** | Move `ai-workstation` repo to `D:\ai-workstation` | Keeps project and venvs off the full NVMe |
| **4 — Medium** | Disable sleep / display timeout for AI workload sessions | Prevents interrupting long RAG indexing jobs |
| **5 — Medium** | Verify `nvidia-smi` accessible in all shells after PATH refresh | CUDA installs depend on this |
| **6 — Low** | Install WSL if any Linux-native tools are needed | Optional but useful for Docker |
| **7 — Low** | Disable Windows `python` App Execution Alias | Prevents confusion between Store stub and real Python |

---

## 27. Game Launchers Detected

| Launcher | Status | Location |
|----------|--------|----------|
| **Steam** | Installed | `C:\Program Files (x86)\Steam` |
| Epic Games | Not found | — |
| Xbox / Game Pass | Partial — `C:\XboxGames` exists (GameSave folder only, no games) | — |
| Battle.net / Blizzard | Not found | — |
| EA Desktop | Installed (launcher only, ~1 GB) | `C:\Program Files\Electronic Arts` + `C:\Program Files\EA` |

Steam is the only launcher with active game installs. EA Desktop is present as a launcher but holds no large game data on C:.

---

## 28. Steam Library Layout

Steam has **two configured library locations:**

| Library Path | Drive | Type | Notes |
|-------------|-------|------|-------|
| `C:\Program Files (x86)\Steam\steamapps\common` | C: (NVMe) | Primary | All 6 large games installed here |
| `E:\SteamLibrary\steamapps\common` | E: (HDD) | Secondary | 1 game installed here |

---

## 29. Installed Games — Full Inventory

### On C: (primary Steam library) — 361.5 GB total

| Game | Steam App ID | Size (GB) | Safe to Move via Steam |
|------|-------------|----------|----------------------|
| STAR WARS Jedi: Survivor | 1774580 | **130.0** | Yes — Steam Move Install Folder |
| Resident Evil Requiem | 3764200 | **76.2** | Yes |
| Counter-Strike 2 | 730 | **63.8** | Yes |
| STAR WARS Jedi: Fallen Order | 1172380 | **56.2** | Yes |
| Age of Mythology: Retold | 1934680 | **34.1** | Yes |
| Buckshot Roulette | 2835570 | 1.2 | Yes |
| Steamworks Common Redistributables | 228980 | 0.16 | N/A (Steam system files) |
| Steam Controller Configs | — | ~0 | N/A |
| **Total on C:** | | **~361.7 GB** | |

### On E: (secondary Steam library)

| Game | Steam App ID | Size (GB) | Notes |
|------|-------------|----------|-------|
| Hollow Knight: Silksong | 1030300 | 7.6 | Already on E: — no action needed |

---

## 30. C: Drive Space Recovery Plan (Updated 2026-06-28)

### Decision

Jedi: Survivor and Jedi: Fallen Order will be **uninstalled** (no longer played).
The remaining games will be **moved** via Steam to D: or E:.

| Game | Action | Destination | Space Freed on C: |
|------|--------|------------|------------------|
| Jedi: Survivor | **Uninstall via Steam** | — | 130.0 GB |
| Jedi: Fallen Order | **Uninstall via Steam** | — | 56.2 GB |
| Counter-Strike 2 | **Move via Steam** | `D:\Games\SteamLibrary` | 63.8 GB |
| Resident Evil Requiem | **Move via Steam** | `E:\Games\SteamLibrary` | 76.2 GB |
| Age of Mythology: Retold | **Move via Steam** | `E:\Games\SteamLibrary` | 34.1 GB |
| Buckshot Roulette | **Move via Steam** | `E:\Games\SteamLibrary` | 1.2 GB |
| **Total recoverable** | | | **~361.5 GB** |

### Rules
- Use Steam only — never manually move or delete game folders in Explorer
- Do not touch save files
- Do not uninstall anything outside these 2 games
- Do not move or change the AI workstation yet

### Expected result after cleanup

| Drive | Before | After (approx) |
|-------|--------|---------------|
| C: | 3.7 GB free | ~365 GB free |
| D: | 369.9 GB free | ~306 GB free (CS2 moved here) |
| E: | 923.7 GB free | ~812 GB free (RE Requiem + AoM + Buckshot moved here) |

### Other recoverable space on C: (optional, secondary)

| Source | Size | Action |
|--------|------|--------|
| `AppData\Local\NVIDIA` | 4.5 GB | NVIDIA shader cache — safe to clear, rebuilds automatically on next game launch |
| `AppData\Local\Packages` | 3.5 GB | Windows Store app data — leave |
| `AppData\Local\Microsoft` | 1.4 GB | System/Edge cache — leave |
| `AppData\Local\Razer` | 1.1 GB | Razer Synapse cache — can be cleared carefully |

> Steam game moves and uninstalls alone recover ~361 GB. The optional items above are not needed and can be skipped.

---

## 31. AppData Large Folders (non-game)

| Path | Size (GB) | Notes |
|------|----------|-------|
| `C:\Users\Owner\AppData\Local` | 11.9 | Breakdown below |
| `C:\Users\Owner\AppData\Roaming` | 0.7 | App config/profiles |
| `C:\Users\Owner\AppData\LocalLow` | ~0 | — |
| `C:\Users\Owner\Downloads` | 1.1 | May have old installers worth clearing |

### AppData\Local breakdown

| Subfolder | Size (GB) | Safe to clear? |
|-----------|----------|---------------|
| NVIDIA | 4.5 | Yes — shader cache, rebuilds on first game launch |
| Packages | 3.5 | No — Store app data |
| Microsoft | 1.4 | No — system/Edge cache |
| Razer | 1.1 | Carefully — Razer config, back up first |
| CrashDumps | 0.4 | Yes — safe to clear |
| Steam | 0.3 | No — Steam client cache |
| Electronic Arts | 0.2 | Possibly — EA launcher cache |

### Summary: additional recoverable space (optional, low-risk)

| Action | Recoverable |
|--------|-------------|
| Clear NVIDIA shader cache | ~4.5 GB |
| Clear CrashDumps | ~0.4 GB |
| Clear Downloads folder (manually review first) | ~1.1 GB (review before deleting) |
| **Total optional** | **~6 GB** |

These are secondary — the Steam move alone recovers 361 GB, which solves everything.

---

## 32. Steam Cleanup Status (2026-06-28)

### Completed

| Action | Result |
|--------|--------|
| Uninstall Jedi: Survivor | ✅ Done — ~130 GB freed on C: |
| Uninstall Jedi: Fallen Order | ✅ Done — ~56 GB freed on C: |
| Move Counter-Strike 2 → D:\SteamLibrary | ✅ Done — 63.75 GB moved |

### In Progress

| Action | Status |
|--------|--------|
| Move Resident Evil Requiem → E:\SteamLibrary (76.13 GB) | 🔄 In progress |
| Move Age of Mythology: Retold → E:\SteamLibrary (34.11 GB) | ⏳ Queued |
| Move Buckshot Roulette → E:\SteamLibrary (1.24 GB) | ⏳ Queued |

### C: Drive Status
- **Before cleanup:** 3.7 GB free (critical)
- **After Batch 1 (uninstalls):** ~190 GB free
- **After Batch 2 (CS2 move):** ~190 GB free on C:, D: reduced by ~64 GB
- **After Batch 3 (expected):** ~300+ GB free on C:

C: is **no longer critical**. AI workstation setup can proceed safely.

---

## 33. AI Cache Configuration (2026-06-28)

All AI/ML tool caches are pointed to D: to avoid filling C:.

### Folders Created

| Path | Purpose |
|------|---------|
| `D:\ai-cache\uv` | uv package manager cache |
| `D:\ai-cache\pip` | pip download cache |
| `D:\ai-cache\huggingface` | HuggingFace model hub cache |
| `D:\ai-cache\torch` | PyTorch hub cache |
| `D:\ai-cache\models` | Manual model downloads |

### User Environment Variables Set

| Variable | Value |
|----------|-------|
| `UV_CACHE_DIR` | `D:\ai-cache\uv` |
| `PIP_CACHE_DIR` | `D:\ai-cache\pip` |
| `HF_HOME` | `D:\ai-cache\huggingface` |
| `TRANSFORMERS_CACHE` | `D:\ai-cache\huggingface` |
| `TORCH_HOME` | `D:\ai-cache\torch` |

These are user-scoped environment variables (persistent, no reboot required for new processes).
New terminal sessions will automatically pick them up.

### Heavy Installs Deferred

The following are **not yet installed** and should wait until Steam moves finish:
- Docker Desktop
- WSL2 / Ubuntu
- Node.js / npm
- Ollama or any local model runner
- Python ML packages (torch, transformers, etc.)

---

## 34. Next Steps (as of 2026-06-28)

| Priority | Task | Blocker |
|----------|------|---------|
| 1 | Verify Batch 3 Steam moves complete (RE Requiem, AoM, Buckshot) | Steam in progress |
| 2 | Move ai-workstation repo from C: to D: | Wait for Steam moves to finish |
| 3 | Laptop → Desktop file migration | See migration checklist doc |
| 4 | Set up .env with API keys | Manual, per-machine |
| 5 | Install Python ML packages (torch, transformers) | After repo move |
| 6 | Connect integrations (Supabase, Make, Gmail) | After env setup |
| 7 | Initialize RAG pipeline | After integrations |

See `docs/laptop_to_desktop_migration_checklist.md` for transfer rules.
