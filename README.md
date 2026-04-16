# 🛡️ Watchdog AI – Live Defense Dashboard

A real-time AI agent monitoring simulation built with Flask. Watchdog continuously generates synthetic agent actions, evaluates each one for risk, and displays the results on a live web dashboard — colour-coded by threat level.

---

## Overview

Watchdog simulates an environment where an AI agent produces actions (emails, code, deployments, etc.) and a dedicated **Watchdog** safety layer evaluates every action in real time. The dashboard auto-refreshes every 3 seconds, giving a live feed of agent behaviour and risk scores.

This project can serve as a learning tool, a prototype for AI oversight systems, or a demo for AI safety concepts.

---

## Project Structure

```
watchdog/
├── app.py                  # Flask app & background simulation loop
├── watchdog.py             # Agent and Watchdog logic
├── templates/
│   └── dashboard.html      # Live dashboard UI
└── static/
    └── style.css           # Custom dark-theme styles
```

---

## How It Works

### Agent (`watchdog.py → Agent`)
The `Agent` class simulates an AI producing actions at regular intervals. Each action has:
- **Type** – one of `email`, `code`, `deploy`, `reply`, `image`, `patch`, `research`
- **Content** – a description of the action
- **Intent** – randomly assigned as `benign` (70%), `risky` (20%), or `malicious` (10%)

Malicious actions use hardcoded high-risk templates (e.g., data exfiltration, ransomware generation).

### Watchdog (`watchdog.py → Watchdog`)
The `Watchdog` class scores each action and decides how to respond:

| Decision | Risk Score | Meaning |
|---|---|---|
| ✅ OK | < 60 | Safe to proceed |
| ⚠️ ALERT | 60–84 | Flagged for review |
| 🚨 ESCALATE | ≥ 85 | Blocked / escalated |

Scoring uses:
- **Keyword matching** — high-risk terms (e.g., *exfiltrate*, *ransomware*, *backdoor*) add 50 points; medium-risk terms add 20
- **Action-type sensitivity weights** — e.g., `deploy` and `code` are more scrutinised than `patch` or `research`
- **Recency spike detection** — if a score is 25+ points above the recent rolling average, a further penalty is applied

### Flask App (`app.py`)
- Runs the simulation in a **background daemon thread**, generating one action every 3 seconds
- Keeps a rolling log of the last 100 actions in memory
- Exposes two routes:
  - `GET /` — renders the dashboard
  - `GET /data` — returns the action log as JSON (polled by the frontend)

---

## Installation

**Requirements:** Python 3.8+

```bash
# 1. Unzip the project
unzip watchdog.zip
cd watchdog

# 2. Install dependencies
pip install flask

# 3. Run the app
python app.py
```

Then open your browser at [http://localhost:5000](http://localhost:5000).

---

## Dashboard

The dashboard renders a live table of agent actions, colour-coded by decision:

- 🟢 **Green** — OK (benign / low-risk)
- 🟡 **Yellow** — ALERT (moderate risk)
- 🔴 **Red** — ESCALATE (high risk, blocked)

The table shows: Action ID, Timestamp, Action Type, Content, Risk Score, and Decision Status.

---

## Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web server and routing |
| `bootstrap 5.3` (CDN) | Dashboard styling |

No database or external API is required — all data is held in memory.

---

## Notes & Limitations

- The simulation is **randomised with a fixed seed** (`seed=42`), so action sequences are reproducible on first run.
- The action log is **in-memory only** — restarting the server clears all history.
- This is a **simulation/prototype** and not intended for production AI safety use.
