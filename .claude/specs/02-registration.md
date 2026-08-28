# Spec: Registration

## Overview
Implements user account creation for Spendly. `GET /register` already renders `register.html`, whose form POSTs `name`, `email`, and `password` to `/register`. This step adds the `POST /register` handler: validate the submitted fields, hash the password, insert a new row into `users`, and redirect the new user to `/login` to sign in. This is the first step that writes to the database from a live route, and it unblocks Login (next step), which depends on real user rows existing.

## Depends on
- Step 1 — Database Setup (`database/db.py`: `get_db()`, `init_db()`, `users` table). Complete.

## Routes
- `POST /register` — create a new user account from the registration form — public
  - On validation error (missing field, malformed email, password too short, or email already registered) — re-render `register.html` with `error` set and the submitted `name`/`email` preserved in the form, HTTP 400
  - On success — insert the user, then redirect to `GET /login`

`GET /register` is unchanged (already implemented).

## Database changes
None. `users` table already has the required columns (`id`, `name`, `email` UNIQUE, `password_hash`, `created_at`) — see `database/db.py`. The `UNIQUE` constraint on `email` is the backstop for the duplicate-email check.

## Templates
- **Create:** none
- **Modify:** none — `templates/register.html` already has the correct `action="/register"`, field names (`name`, `email`, `password`), and `{% if error %}` block. No template changes needed unless implementation finds the existing markup insufficient (e.g. re-populating `name`/`email` on error requires `value="{{ name or '' }}"` attributes — add these only if missing).

## Files to change
- `app.py` — replace the existing `GET`-only `/register` route with one that accepts `GET` and `POST`, add the registration/validation/insert logic

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- All DB access goes through `database/db.py` — no raw SQL in `app.py`
- Never trust the `UNIQUE` constraint alone for the user-facing duplicate-email message — check first so a friendly error can be shown instead of an unhandled `IntegrityError`
- Keep the route in `app.py` — no blueprints

## Definition of done
- [ ] Submitting the register form with valid, unique data creates a row in `users` with a bcrypt/werkzeug password hash (not plaintext) and redirects to `/login`
- [ ] Submitting with an email that already exists in `users` re-renders `register.html` with an error message and does not create a duplicate row
- [ ] Submitting with a missing name, email, or password re-renders `register.html` with an error message
- [ ] Submitting with an invalid email format re-renders `register.html` with an error message
- [ ] `GET /register` still renders the empty form as before
- [ ] App starts without errors and existing routes (landing, login, terms, privacy) are unaffected
