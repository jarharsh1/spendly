# Spendly Design System Reference

Everything here reflects what's actually in `static/css/style.css` today, plus the small,
consistent extensions worth adding when a task needs them. The rule is simple: **reuse what
exists, extend it by adding tokens/classes in the same spirit, and never scatter one-off
hardcoded values.**

## Contents
1. Existing tokens (source of truth)
2. Gaps worth extending
3. Component vocabulary that already exists
4. Patterns to build (components Spendly needs but doesn't have yet)
5. Responsive
6. Accessibility

---

## 1. Existing tokens (source of truth)

These live in `:root` in `style.css`. Use them by name. Don't paste their hex values inline.

**Ink (text) scale**
- `--ink: #0f0f0f` — primary text, key numbers
- `--ink-soft: #2d2d2d` — strong secondary text
- `--ink-muted: #6b6b6b` — labels, captions, secondary info
- `--ink-faint: #a0a0a0` — placeholders and decoration only; **not** for meaningful text (fails contrast)

**Paper (surface) scale**
- `--paper: #f7f6f3` — app/page background
- `--paper-warm: #f0ede6` — subtle raised/hover surface, zebra rows
- `--paper-card: #ffffff` — cards, panels, inputs

**Accents**
- `--accent: #1a472a` (forest green) — primary/brand, links-on-hover, positive-brand moments
- `--accent-light: #e8f0eb` — green tint background (badges, subtle fills)
- `--accent-2: #c17f24` (gold) — secondary highlight, "Food" category, special emphasis
- `--accent-2-light: #fdf3e3` — gold tint background

**Feedback**
- `--danger: #c0392b` — negative amounts, destructive actions, errors
- `--danger-light: #fdecea` — error background (see `.auth-error`)

**Borders**
- `--border: #e4e1da` — standard hairline
- `--border-soft: #eeebe4` — even lighter divider

**Type**
- `--font-display: 'DM Serif Display', Georgia, serif` — hero/section/page titles, big statement numbers
- `--font-body: 'DM Sans', system-ui, sans-serif` — everything else, including data and labels

**Layout & shape**
- `--max-width: 1200px` — main content column
- `--auth-width: 440px` — narrow auth column
- `--radius-sm: 6px` — buttons, inputs, small chips
- `--radius-md: 12px` — cards, panels
- `--radius-lg: 20px` — large feature/hero surfaces

---

## 2. Gaps worth extending

The system has no spacing, shadow, transition, or positive/category tokens yet — those values
are currently hardcoded (e.g. the hero uses `#4caf7d` for a positive delta and `#4a7fd6` /
`#7b6fd6` for category bars). When a task makes you reach for one of these, **add it as a
token** in `:root` using the names below and switch the hardcoded usages you touch over to it.
Don't rewrite the whole sheet to adopt them in one go — extend as you work.

```css
/* Positive / success — promote the hero's inline green */
--positive: #2f8f5f;
--positive-light: #e6f2ec;

/* Warning reuses the gold accent family; no new hue needed:
   use --accent-2 / --accent-2-light for warnings. */

/* Spacing — soft 4px base; use for padding/gaps/margins */
--space-1: 0.25rem;  /* 4  */
--space-2: 0.5rem;   /* 8  */
--space-3: 0.75rem;  /* 12 */
--space-4: 1rem;     /* 16 */
--space-5: 1.5rem;   /* 24 */
--space-6: 2rem;     /* 32 */
--space-8: 3rem;     /* 48 */
--space-10: 4rem;    /* 64 */

/* Shadows — keep them barely-there; this is a calm, flat-ish product */
--shadow-sm: 0 1px 2px rgba(15, 15, 15, 0.04);
--shadow-md: 0 2px 8px rgba(15, 15, 15, 0.06);
--shadow-lg: 0 8px 24px rgba(15, 15, 15, 0.08);

/* Transitions — the repo already leans on ~0.2s; name it */
--transition-fast: 120ms ease;
--transition: 200ms ease;
--transition-slow: 320ms ease;

/* Category palette — ONE set, reused for every category everywhere.
   Promotes the hero's existing bar colors. */
--cat-food: #c17f24;      /* == --accent-2 */
--cat-travel: #4a7fd6;
--cat-bills: #7b6fd6;
--cat-shopping: #2f8f5f;
--cat-health: #c0392b;    /* == danger hue, fine as a category too */
--cat-other: #6b6b6b;     /* == --ink-muted */
```

Keep shadows and radii restrained — heavy elevation and giant rounding are on the "avoid"
list because they read as generic-SaaS rather than premium-editorial.

---

## 3. Component vocabulary that already exists

Reuse these class names. If you're building something similar, extend the existing family
rather than inventing a parallel one.

**Shell** — `.navbar`, `.nav-inner`, `.nav-brand`, `.brand-icon`, `.brand-name`, `.nav-links`,
`.nav-cta`; `.main-content`; `.footer`, `.footer-inner`, `.footer-name`, `.footer-copy`, `.footer-links`.

**Buttons**
- `.btn-primary` — solid ink background that shifts to `--accent` on hover; the main call to action.
- `.btn-ghost` — bordered/transparent secondary button.
- `.btn-submit` — full-width form submit (ink → accent on hover). Reuse for any full-width primary form action.

**Auth / forms** — `.auth-section`, `.auth-container`, `.auth-header`, `.auth-title`,
`.auth-subtitle`, `.auth-card`, `.auth-error` (danger-tinted box), `.form-group`, `label`,
`.form-input` (border turns `--accent` on focus), `.auth-switch`. This is the canonical form
styling — extend it for any new form.

**Landing** — `.hero`, `.hero-badge`, `.hero-title`, `.hero-title-accent`, `.hero-subtitle`,
`.hero-actions`; the dashboard preview: `.dash-window`, `.dash-dots`, `.dash-stats`,
`.dash-stat`, `.dash-stat-label`, `.dash-stat-value`, `.dash-stat-delta` (+`-pos` / `-neg` /
`-muted`), `.dash-bars`, `.dash-bar-row`, `.dash-bar-label`, `.dash-bar-track`,
`.dash-bar-fill` (+`-food` / `-travel` / `-bills`); `.features`, `.feature-card`,
`.feature-icon`, `.feature-title`, `.feature-body`; `.cta-section`.

**Legal** — `.legal-page`, `.legal-inner`, `.legal-title`, `.legal-updated`, `.legal-section`, `.legal-back`.

**Modal** — `.modal-overlay` (toggled via the `hidden` attribute), `.modal-box`,
`.modal-close`, `.modal-video-wrap`, `.modal-video`.

> The dashboard-preview classes are the single most reusable thing in the repo for real
> financial UI. When Spendly gets an actual dashboard, promote `.dash-stat*` and `.dash-bar*`
> into first-class `.stat-card` / `.budget-bar` components rather than starting fresh.

---

## 4. Patterns to build (components Spendly needs but doesn't have yet)

Ready-made, in Spendly's language. Build these as real classes in `style.css`.

**Page header** (context row at the top of an app page)
- Title in `--font-display`; optional one-line subtitle in `--ink-muted`; optional primary action right-aligned.
- Establishes "where am I" before any data.

**KPI / summary card** (promote `.dash-stat`)
- Small uppercase-ish label in `--ink-muted`; the primary number large in `--ink` with `font-variant-numeric: tabular-nums`; an optional delta line using `--positive` (with a `+`) or `--danger` (with a `−`) so meaning survives without color.
- Card = `--paper-card`, `--radius-md`, `1px solid var(--border)`, `--shadow-sm`. Lay KPIs out in a responsive row/grid.

**Transaction list / table**
- Toolbar row: search/filter on the left, primary "Add expense" action on the right.
- Each row: a category dot (from the `--cat-*` palette) + description (`--ink`), date (`--ink-muted`), amount right-aligned with `tabular-nums` (negative → `--danger` and a `−`).
- Row hover → `--paper-warm`; contextual edit/delete actions appear on hover or in a trailing cell. Use a real `<table>` with `<th scope="col">`, or a semantic list.

**Budget progress bar** (promote `.dash-bar*`)
- `.budget-bar-track` in `--paper-warm`/`--border-soft`; `.budget-bar-fill` in the category color or `--accent`; over-budget → `--danger` fill. Pair with a label and a `spent / limit` figure.

**Empty state**
- Centered, generous but not cavernous. A muted glyph (line-style, no emoji), a short heading in `--font-display`, a one-line explanation in `--ink-muted`, and one primary action (e.g. "Add your first expense"). This is where a finance app earns trust — make it inviting, not blank.

**Alerts / toasts** (extend `.auth-error`)
- `.alert` base + variants: `.alert-danger` (`--danger-light` / `--danger`), `.alert-success`
  (`--positive-light` / `--positive`), `.alert-warning` (`--accent-2-light` / `--accent-2`).
  Keep them quiet — a tinted background, a hairline, readable text; no loud full-bleed banners.

**Form extras** (beyond auth)
- Reuse `.form-group` / `.form-input`. Add `.form-help` (`--ink-faint`, small) for hints and
  `.form-error` (`--danger`, small) for inline field errors. Group related fields; give every
  form exactly one obvious primary action.

**Category icons (inline SVG — no icon library)**
- Spendly is vanilla, so category icons are **inline SVG**, never an icon font, npm package,
  or emoji. Draw simple line icons on a `0 0 24 24` viewBox with
  `fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"`.
- Wrap each in a `.cat-badge` — a small rounded-square chip whose tint derives from the
  category color via `currentColor`, so one rule covers every category:
  ```css
  .cat-badge { width: 32px; height: 32px; border-radius: 9px; display: inline-flex;
    align-items: center; justify-content: center; flex-shrink: 0;
    background: color-mix(in srgb, currentColor 12%, var(--paper-card)); }
  .cat-badge svg { width: 17px; height: 17px; }
  .cat-food { color: var(--cat-food); }      /* icon + tint follow the palette */
  .cat-travel { color: var(--cat-travel); }  /* ...one class per category */
  ```
- Keep the icon set small, consistent (same weight and style), and mapped 1:1 to the
  `--cat-*` palette so a category reads the same everywhere: badge in a transaction row, dot-
  sized badge (`.cat-badge.sm`, ~24px) in a budget row. Reuse the exact same SVGs across pages.

**Progressive disclosure / drill-down (CSS-first, no JS)**
- For "summary now, detail on demand" — e.g. a monthly overview that expands to daily detail —
  use native **`<details>` / `<summary>`**. It's keyboard-accessible and needs zero JavaScript,
  which is exactly the repo's "prefer CSS over JS for visual behavior" rule. Style the summary
  as the collapsed row and rotate a chevron on open:
  ```css
  summary { cursor: pointer; list-style: none; }
  summary::-webkit-details-marker { display: none; }
  .chev { transition: transform var(--transition); }
  details[open] .chev { transform: rotate(90deg); }
  ```
- **Product rule for Spendly's month→day drill:** show day-level detail **only for the current
  month**. Past months are summary rows with no expander; make the current month the sole
  `<details>` and add a short caption ("Daily breakdown is available for the current month").
  Keep the collapsed month rows uniform so the one expandable row reads as intentional, not odd.
- **When the drill goes one level deeper** — e.g. clicking a day in the month chart to see that
  day's transactions — you've crossed from disclosure into *selecting a record and rendering its
  detail*. That's genuine behavior, so a small, page-specific `<script>` in the template's
  `{% block scripts %}` is the right tool, not a CSS hack with 28 hidden radios. Keep it minimal
  and accessible: make each selectable item a real `<button>` (keyboard-operable for free),
  reflect the current choice with `aria-pressed`, and render the detail into a container marked
  `aria-live="polite"` so a screen reader announces the change. Derive the chart bars and the
  per-day detail from the **same** data structure so they can never disagree, and always handle
  the empty case (a day with no spend gets a small, friendly "nothing here" state, not a blank).

---

## 5. Responsive

Existing breakpoints in `style.css`: **`@media (max-width: 900px)`** (tablet — e.g. features
collapse to one column) and **`@media (max-width: 600px)`** (mobile — hero actions go
full-width). Extend these two rather than scattering new breakpoints. Targets:
- **Desktop:** multi-column KPI rows, table with all columns.
- **Tablet (≤900px):** KPIs wrap to 2-up; keep tables scannable, hide non-essential columns if needed.
- **Mobile (≤600px):** single-column KPIs; consider turning dense tables into stacked cards; full-width primary buttons; touch targets ≥ 40px.

---

## 6. Accessibility

- **Contrast:** `--ink` / `--ink-soft` on paper are strong. `--ink-muted` is fine for
  secondary text but use `--ink-soft`/`--ink` for anything critical. `--ink-faint` is
  decoration/placeholder only — never body text.
- **Focus:** the repo currently only changes an input's border color on focus. Add a visible
  keyboard focus ring for interactive elements:
  ```css
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  ```
- **Semantic HTML:** real `<button>` for actions (not styled `<div>`s), `<table>`/`<th scope>`
  for tabular data, `<nav>`/`<main>`/`<header>`/`<footer>`, and `<label for>` tied to every input (auth already does this).
- **Don't rely on color alone:** positive/negative amounts also carry a `+` / `−` sign; status also carries a word or icon. The hero's deltas already model this — follow it.
- **Text size:** body ≥ `0.9rem` (≈14.4px); prefer `1rem`. No tiny print for real content.