# PreLandfall

Local prototype for anticipatory action during Bay of Bengal cyclones, scoped to **Puri, Odisha** and a replay of **Cyclone Fani (2019)**. It shows a screening-level surge scenario, exposed assets, likely isolated wards, and numeric-validated advisory drafts.

> **Safety:** surge results are screening-level and **not a hydrodynamic simulation**. This demo must not be used as an operational evacuation or asset-control system. Any insurance payout figure would be illustrative only.

## One-command demo

```powershell
.\run.ps1 -Demo
```

Open `http://127.0.0.1:8000`. The demo uses only `data/fani_demo.json`; bulletin extraction and dispatch are deliberately mocked. It remains useful if Earth Engine, Gemini, or Telegram are unavailable. The command requires Python 3.11+.

## Architecture

```text
IMD PDF/image or manual entry
          │ (Gemini structured extraction in live deployment)
          ▼
  scenario engine ──► cached DEM/OSM/EE adapters ──► risk & isolation
          │                                               │
          └────────────► FastAPI ◄─────────────────────────┘
                            │
                  Leaflet dashboard / advisory validator
                            │
                 approved Telegram + email dispatch
```

## Project layout

- `app.py` — local server entrypoint.
- `backend/engine.py` — deterministic screening scenario and risk ranking.
- `backend/api.py` — bulletin, scenario, advisory, and safe dispatch endpoints.
- `frontend/` — plain HTML + Leaflet dashboard.
- `data/` — cached Fani replay and a sample IMD bulletin.
- `scripts/backtest.py` — cached Sentinel-1 comparison fixture.

## Live integration configuration

Copy `.env.example` to `.env` and set `GEMINI_API_KEY`, `EE_PROJECT`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and SMTP settings. No secret is hardcoded. When a Gemini key is present outside demo mode, the app uses `gemini-3.7-flash` to extract structured bulletin data and produce engine-grounded advisories; a failed API call falls back to cached/template results. Telegram/email remain deliberately safe-disabled in this prototype until production dispatch adapters and recipient controls are reviewed.

## Backtest

```powershell
python scripts/backtest.py
```

The fixture prints precision/recall for flooded critical assets. Its limitations are printed alongside the result: Sentinel-1 can miss peak flood due to timing, radar geometry, vegetation, and storm conditions. A production implementation must query Earth Engine using only imagery available after landfall and only forecast/bulletin data available before landfall.

## API quick check

`GET /api/scenario/low|mid|high` returns the map layers and Top-20-compatible asset list. `POST /api/advisories` generates a constrained draft, and `POST /api/dispatch` validates all numbers before recording a demo dispatch.
