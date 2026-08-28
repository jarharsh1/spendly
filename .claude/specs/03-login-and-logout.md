# Spec: Login and Logout

## Overview
Implements session-based authentication for Spendly. `GET /login` already renders `login.html`, whose form POSTs `email` and `password` to `/login`, but there is no `POST /login` handler yet, and no session mechanism exists anywhere in the app. This step adds the `POST /login` handler (verify credentials against `users`, start a session), implements `GET /logout` (clear the session, redirect to landing), and makes the shared nav in `base.html` session-aware so a signed-in user sees a way to sign out instead of "Sign in" / "Get started". This is the step that turns "an account exists" (Registration) into "a user is recognized across requests," and unblocks Profile (Step 4) and the expense routes (Steps 7–9), which all require knowing who is logged in.

## Depends on
- Step 1 — Database Setup (`database/db.py`: `get_db()`, `init_db()`, `users` table). Complete.
- Step 2 — Registration (`POST /register`, `create_user`, `get_user_by_email`). Complete.

## Routes
- `POST /login` — verify email/password against `users` and start a session — public
  - On validation error (missing field, no matching email, or wrong password) — re-render `login.html` with a generic `error` (do not reveal whether the email exists), preserve submitted `email` in the form, HTTP 400
  - On success — store the user's id in `session`, redirect to `GET /profile` (updated in Step 4 once the profile route existed; originally redirected to landing since there was no dashboard route yet)
- `GET /logout` — clear the session and redirect to the login page — logged-in
  - Replaces the current stub (`"Logout — coming in Step 3"`)
  - If called while not logged in, just redirect to `/login` (no error)

`GET /login` is unchanged (already implemented).

## Database changes
None. `users` table already has `password_hash` — see `database/db.py`. No new tables or columns required for session auth (Flask's signed cookie session holds `user_id`; no server-side session table).

## Templates
- **Create:** none
- **Modify:**
  - `templates/base.html` — nav must reflect session state: if logged in, show a link to `{{ url_for('logout') }}` (and, since `/profile` is still a stub, do not link it yet — keep the nav minimal, just add "Sign out") instead of the "Sign in" / "Get started" links; if not logged in, nav is unchanged
  - `templates/login.html` — none expected (already has `action="/login"`, `error` block, `email`/`password` field names); modify only if implementation finds the markup insufficient (e.g. add `value="{{ email or '' }}"` to repopulate the email field on error, matching the pattern used in `register.html`)

## Files to change
- `app.py` — add `app.secret_key` (required for Flask sessions), replace the existing `GET`-only `/login` route with one that accepts `GET` and `POST` and contains the login logic, replace the `/logout` stub with a real handler
- `database/db.py` — add a `verify_user(email, password)` helper (looks up the user by email, checks the password hash with `check_password_hash`, returns the user row or `None`) — no raw SQL in `app.py`
- `templates/base.html` — session-aware nav (see Templates above)

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` (already used for `generate_password_hash`) also provides `check_password_hash`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` against the stored `password_hash` — never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- All DB access goes through `database/db.py` — no raw SQL in `app.py`
- Use Flask's built-in `session` (signed cookie) for login state — no server-side session table, no new dependencies
- `app.secret_key` must be set for sessions to work — read from an environment variable if present, otherwise fall back to a hardcoded dev-only value, but do not skip setting it
- Login error message must be generic ("Invalid email or password") for both "no such user" and "wrong password" cases — do not leak which one failed
- Keep routes in `app.py` — no blueprints

## Definition of done
- [ ] Submitting the login form with the seeded demo account (`demo@spendly.com` / `demo123`) logs in and redirects to `/`
- [ ] Submitting the login form with a correct email but wrong password re-renders `login.html` with a generic error and does not log in
- [ ] Submitting the login form with an email that doesn't exist re-renders `login.html` with the same generic error (indistinguishable from wrong-password case)
- [ ] Submitting with a missing email or password re-renders `login.html` with an error message
- [ ] After logging in, visiting any page shows "Sign out" in the nav instead of "Sign in" / "Get started"
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/login`, and the nav reverts to "Sign in" / "Get started" on the next page load
- [ ] Visiting `/logout` while not logged in just redirects to `/login` without error
- [ ] `GET /login` still renders the empty form as before
- [ ] App starts without errors and existing routes (landing, register, terms, privacy) are unaffected
