# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly — a Flask expense-tracker web app being built incrementally as a guided learning project. Code comments like `# Students will write this file in Step 1` and placeholder routes (`"Logout — coming in Step 3"`) mark work that hasn't been implemented yet; don't "fix" these unless asked to implement that step.

## Architecture

```
spendly/
├── app.py              # All routes — single file, no blueprints
├── database/
│   └── db.py           # SQLite helpers: get_db(), init_db(), seed_db()
├── templates/
│   ├── base.html       # Shared layout — all templates must extend this
│   └── *.html          # One template per page
├── static/
│   ├── css/
│   │   └── style.css       # Global styles — no per-page CSS files
│   └── js/
│       └── main.js         # Vanilla JS only
└── requirements.txt
```

- `app.py` — single Flask app with all routes defined directly on it (no blueprints). Routes render Jinja templates via `render_template`; several routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) are still stub placeholders returning plain strings.
- `database/db.py` — intended to hold `get_db()` (SQLite connection, row_factory + foreign keys on), `init_db()` (CREATE TABLE IF NOT EXISTS), and `seed_db()` (sample data). Not yet implemented — currently just a comment describing the expected shape. There's no ORM; raw SQLite is the intended approach.
- `templates/base.html` — the shared layout (nav, footer, `{% block content %}` / `{% block scripts %}` / `{% block head %}`). All pages `{% extends "base.html" %}`; footer links use `url_for('terms')` / `url_for('privacy')`, not hardcoded paths.
- `templates/*.html` — one template per route (`landing.html`, `login.html`, `register.html`, `terms.html`, `privacy.html`). Auth forms (`register.html`, `login.html`) POST directly to the route path (e.g. `action="/register"`) and expect an optional `error` template variable to render a `.auth-error` box.
- `static/css/style.css` — single global stylesheet (no per-page CSS files) covering nav, hero, features, auth forms, footer, and modal styles.
- `static/js/main.js` — currently empty/placeholder; page-specific JS (e.g. the "how it works" video modal on `landing.html`) is inlined in that template's `{% block scripts %}` rather than added here. Follow that pattern (inline per-template `<script>` blocks) unless a script is genuinely shared across pages.
- Currency/locale: amounts are formatted in rupees (₹), matching the target audience.

---

## Tech constraints 

- **Flask only** - no FastAPI, no Django, no other web frameworks
- **SQLite only** - no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** - no React, no npm packages
- **No new pip packages** - Work within `requirements.txt` as-is unless explicitly told otherwise
- Python 3.14 (see `venv/pyvenv.cfg`) - f-strings and `match` statements are fine
- SQLite database file is `spendly.db` (see `.gitignore`), created at the project root by `init_db()`

---

## Commands
```bash
# Setup
python -m venv venv
venv\Scripts\Activate.ps1         # Windows PowerShell (this project's environment)
pip install -r requirements.txt

# Run dev server (port 5001)
python app.py

# Run all tests
pytest

# Run a specific test file
pytest tests/test_foo.py

# Run a specific test by name
pytest -k "test_name"

# Run tests with output visible
pytest -s
```

---

## Implemented vs stub routes

| Route | Status |
|---|---|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` |
| `GET /login` | Implemented — renders `login.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<id>/edit` | Stub — Step 8 |
| `GET /expenses/<id>/delete` | Stub — Step 9 |

**Do not implement a stub route unless the active task explicitly targets that step.**

---

## Warnings and things to avoid

- **Never use raw string returns for stub routes** once a step is implemented — always render a template
- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** mid-feature without flagging it — keep `requirements.txt` in sync
- **Never use JS frameworks** — the frontend is intentionally vanilla
- **`database/db.py` is currently empty** — do not assume helpers exist until the step that implements them
- **FK enforcement is manual** — SQLite foreign keys are off by default; `get_db()` must run `PRAGMA foreign_keys = ON` on every connection
- The app runs on **port 5001**, not the Flask default 5000 — don't change this
- **Commit message convention**: `<area>: <lowercase description>` (e.g. `landing: add privacy policy page and route`) — every commit so far follows this style, match it