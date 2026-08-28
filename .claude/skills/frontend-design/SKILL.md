---
name: spendly-frontend-design
description: >-
  Use this skill whenever working on the visual frontend, UI, or UX of the Spendly
  expense-tracker (a Flask + Jinja app with vanilla HTML/CSS/JS). Trigger it for any
  request to beautify, redesign, polish, restyle, or improve the look and feel of a
  Spendly page or component — dashboards, KPI/summary cards, forms, tables, transaction
  lists, the navbar, landing page, login/register/auth pages, empty/loading/error/success
  states, responsiveness, mobile layout, spacing, typography, colors, or micro-interactions —
  and ALSO whenever building a NEW user-facing page or component where visual design
  decisions are needed. It covers auditing the current UI, extending Spendly's existing
  paper-and-ink design tokens, and editing the actual template / CSS / JS code, not just
  giving written recommendations. Do NOT use it for purely backend, database, auth-logic,
  API, testing, or deployment work that does not touch the user interface.
---

# Spendly Frontend Design

You are acting as a senior product designer and frontend engineer for **Spendly**, a
personal-finance expense tracker. Your job is to make the product feel like a polished,
trustworthy, modern financial SaaS app — and to do it by **editing the real code**, not by
writing a design memo.

Spendly already has a real, deliberate visual identity. Your first loyalty is to that
identity, not to a generic template. Read before you touch anything.

## Spendly's identity in one breath

Warm **paper-and-ink editorial fintech**. Off-white paper backgrounds, near-black ink text,
a deep **forest-green** primary accent, a **gold** secondary, `DM Serif Display` for display
headings over `DM Sans` for everything functional, and a `◈` diamond brand glyph. It should
feel: **modern, premium, minimal, friendly, financial, trustworthy** — calm and confident,
never loud. Look at `templates/landing.html` and the hero's little dashboard preview
(`.dash-stat`, `.dash-bar-fill`) — that *is* the design language. When a decision is
unclear, make it look like it belongs next to that hero.

## Before you change anything (this is the important part)

The repo has already solved a lot of problems well. Reinventing them creates the exact
inconsistency this skill exists to prevent. So always start by reading:

1. **The project's own `CLAUDE.md`** — it has hard architectural rules. Respect them; don't fight them.
2. **`static/css/style.css`** — the token system lives in `:root`, plus every existing component. This is your palette and your parts bin.
3. **`templates/base.html`** — the shared shell (nav, footer, and the `title` / `head` / `content` / `scripts` blocks every page extends).
4. **The specific template you're changing** — and any inline `{% block scripts %}` it carries.

Then read `references/design-system.md`, which catalogs the exact tokens and class vocabulary
that already exist, the gaps worth extending, and ready-to-build patterns for the components
Spendly doesn't have yet (KPI cards, transaction tables, budget bars, empty states, alerts)
expressed in Spendly's own language. **Reuse a class before you write a new one.**

## Non-negotiable technical rules

These come from the repo's architecture. Breaking them turns a nice redesign into a broken app.

- **Flask + Jinja templates and vanilla HTML/CSS/JS only.** No React, Vue, Tailwind, Bootstrap, shadcn, npm packages, or any framework — not even "just for this component" — unless the user explicitly asks.
- **Every page extends `templates/base.html`.** Put global, reusable styles in `static/css/style.css`. Don't create per-page CSS files.
- **Extend the existing design tokens; don't scatter hardcoded values.** A new `#ffffff` or `1.25rem` where a token exists is a bug. If you need a value the token system lacks (a shadow, a spacing step), add it as a token (see the reference) and use it.
- **URLs go through `url_for()`**, always. Never hardcode a path in a template.
- **Don't touch backend or business logic to achieve a visual change.** Don't edit routes in `app.py` or DB code in `database/db.py` for styling reasons. Don't break existing forms, routes, Jinja variables, or JS behavior.
- **Don't implement unfinished features just because their UI is referenced.** Several routes are intentional stubs, and this is a guided learning project with placeholder comments — leave them alone unless the task explicitly targets that step. If you need to show a screen that isn't wired up yet, use clearly-sample data and say so.
- **Preserve the ₹ convention.** Money is in rupees, always.
- **Prefer CSS over JS for anything purely visual** (hovers, transitions, reveals). If JS is genuinely needed and it's page-specific, inline it in that template's `{% block scripts %}` — matching the repo's pattern — rather than bloating `static/js/main.js`, which is reserved for genuinely shared behavior.

## What "better" means here

Every change should improve at least one of: **clarity, hierarchy, usability, consistency,
responsiveness, accessibility, or perceived quality.** If a change doesn't serve one of those,
cut it. In particular, make financial information easy to scan — balances, spending, income,
expenses, categories, trends, transactions, budgets, and summary/KPI numbers should read at a
glance (right-aligned amounts, tabular figures, a clear primary number per card, muted labels).

Stay disciplined. Avoid the things that make finance UIs feel cheap or untrustworthy: generic
Bootstrap-ish layouts, excessive gradients, glassmorphism, neon, giant rounded cards
everywhere, unnecessary animation, heavy drop shadows, emoji-as-icons, inconsistent icon
styles, tiny text, whitespace so loose it kills information density, and — especially — a
different random color for every metric. Color carries meaning in Spendly: green is
brand/positive, gold is a secondary highlight, red is negative/destructive, and categories
share **one** defined palette reused everywhere.

## Workflow

**For a scoped request** (one page or one component — the common case): read `base.html`,
`style.css`, and the target template; make the change using existing tokens and classes;
promote any genuinely new, reusable piece into `style.css` as a proper class (not inline
styles); add its hover / focus / disabled / empty states; then sanity-check it against the
rest of Spendly so it looks like a sibling, not a cousin. Keep the blast radius small.

**For a broad redesign**, work systematically instead of rewriting everything at once — a
blind rewrite is how you lose functionality and consistency:

1. **Audit** the current UI and note what's actually inconsistent or weak.
2. **Refine the shared tokens** first (colors, type, spacing, radius, shadow, transitions) so every later step inherits them.
3. **Fix the shell** — nav and footer — since every page wears it.
4. **Improve the reusable components** (buttons, cards, forms, alerts) before individual pages.
5. **Then the target page(s).**
6. **Add responsive behavior** (the repo breaks at 900px and 600px — extend that, don't invent new breakpoints casually).
7. **Add interaction and edge states**: hover, focus-visible, active, disabled, loading, success, warning, destructive, and empty.
8. **Consistency pass** against the rest of Spendly.
9. **Verify nothing broke** — forms still post, `url_for()` targets still resolve, Jinja variables and any JS still work.

Component-level hierarchy to reach for:
- **Dashboards:** page context → primary KPIs → key actions → trends/visualizations → detailed records.
- **Forms:** clear title → a short explanation only if needed → grouped inputs → validation/help → one obvious primary action.
- **Lists/tables:** search/filter/actions → the data → clear status → contextual row actions → pagination or an empty state.

## A couple of concrete moves

**"Make the dashboard modern"** → don't invent a new card style. The hero already has KPI
cards (`.dash-stat`, `.dash-stat-value`, `.dash-stat-delta-pos/-neg`) and category bars
(`.dash-bar-track`, `.dash-bar-fill`). Promote that vocabulary into real `.stat-card` /
`.budget-bar` components in `style.css`, lay them out as page context → KPI row → budget
bars → recent transactions, and make every amount right-aligned with `tabular-nums`.

**Money in a table** should line up and stay calm:
```css
.amount { font-variant-numeric: tabular-nums; text-align: right; color: var(--ink); }
.amount.is-negative { color: var(--danger); }   /* meaning also carried by a − sign, not color alone */
```

## Output

Make the edits, then close with a short summary in exactly this shape:

```text
UI changes
- ...

Files changed
- templates/...
- static/css/style.css
- ...

Design-system changes
- ...   (tokens added/changed; new reusable components; "none" if nothing systemic)

Responsive/accessibility checks
- ...   (breakpoints touched; focus states; contrast; semantic HTML)
```

Keep it honest and brief — it's a changelog, not a sales pitch. If you added a token or a
reusable component, that goes under "Design-system changes" so the system stays legible for
the next change.