# Spec: Profile Page

## Overview
This feature replaces the `/profile` stub with a fully designed profile page. The user info card (name, email, member-since) shows the real logged-in user's data, fetched from the database — this was needed because showing a hardcoded "Demo User" for every account was misleading. The transaction history table, summary stats, and category breakdown remain static, clearly-labeled sample data, since real expense queries are Step 5's job. Building the rest of the UI first lets the team validate the design in isolation and ensures the templates are ready for the backend-connection step.

## Depends on
- Step 1: Database setup (schema must exist)
- Step 2: Registration (user accounts must be creatable)
- Step 3: Login + Logout (session must be set; `/profile` must be a protected route)

## Routes
- GET /profile — render the profile page — logged-in only (redirect to /login if not authenticated)
- POST /login (existing, Step 3) — on success, now redirects to `GET /profile` instead of the landing page, since a real destination exists after sign-in

## Database changes
No schema changes. Adds one new read helper: `get_user_by_id(user_id)` in `database/db.py`, returning `id`, `name`, `email`, `created_at` for the logged-in user.

## Templates
- Create: `templates/profile.html` — full profile page extending `base.html`; contains four sections:
  1. **User info card** — avatar initials, name, email, member-since date (real data, from `get_user_by_id`)
  2. **Summary stats row** — total spent, number of transactions, top category (hardcoded)
  3. **Transaction history table** — list of recent expenses with date, description, category badge, amount (hardcoded rows)
  4. **Category breakdown** — per-category totals displayed as a simple list or progress-bar rows (hardcoded)

## Files to change
- `app.py` — replace the `/profile` stub with a real view function that:
  - Redirects unauthenticated users to `/login`
  - Fetches the real user via `get_user_by_id(session["user_id"])`; redirects to `/login` if the id no longer resolves
  - Passes the real user plus hardcoded stats/transactions/categories context variables to `profile.html`
- `database/db.py` — add `get_user_by_id(user_id)`

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3 via `get_db()` if any DB call is ever needed
- Parameterised queries only — never string-format SQL
- Passwords hashed with werkzeug (no changes to auth in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No inline styles except data-driven layout values (e.g. a progress-bar's `width: {{ percent }}%`) — never inline colour
- Authentication guard: check `session.get("user_id")`; if absent, `redirect(url_for("login"))`
- User identity (name, email, member-since) comes from the database via `database/db.py`; transactions, category breakdown, and summary stats stay hardcoded in `app.py` until Step 5, and must be visibly labeled as sample data in the template
- Category badges and bars must use CSS classes backed by the shared `--cat-*` tokens (one palette, reused everywhere) — not inline colour styles, and not one-off hex per component

## Definition of done
- [ ] Submitting the login form successfully redirects straight to `/profile`, not the landing page
- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] Visiting `/profile` while logged in returns HTTP 200
- [ ] The page displays a user info card with the logged-in user's real name and email (verified with two different accounts showing different data)
- [ ] The page displays at least three summary stat values (e.g. total spent, transaction count, top category)
- [ ] The page displays a transaction history table with at least three hardcoded rows
- [ ] The page displays a category breakdown section with at least three categories
- [ ] The navbar shows the logged-in state (username + logout link)
- [ ] No hex colour values appear in `profile.html` — only CSS variables