# NICHE Platform — Code-First Design Mockups

> **Status:** Proof-of-concept demonstrating Claude as a Figma alternative
> **Approach:** Static HTML+CSS mockups using the brand-book token system as source of truth
> **Date:** 2026-05-06

This directory is a **clickable HTML mockup** of the NICHE Platform across all 3 portals (Learning System / Student Portal / Career System) and the public marketing site. It's the proof-of-concept for the workflow proposed in [`design/UI_PATTERNS.md` §5](../design/UI_PATTERNS.md): tokens-in-code as source of truth, no Figma source-of-truth file required.

## Structure

```
platform/
├── shared/              ← imported on every page
│   ├── tokens.css       (design tokens — copied from brand-book/css/tokens.css)
│   ├── base.css         (reset + typography)
│   ├── platform.css     (app shell, sidebar, topbar, cards, tables, forms, badges)
│   └── logos/           (logo PNGs from brand book)
│
├── public/              ← Public marketing site (anonymous visitors)
│   ├── index.html       — landing + hero "Find your niche" + 12 programs
│   ├── programs.html    — 3-pillar segmented control + program grid
│   ├── program-detail.html
│   ├── about.html
│   ├── faculty.html
│   ├── faq.html
│   └── apply.html       — multi-step application flow
│
├── auth/                ← Authentication (Clerk-backed in production)
│   ├── login.html
│   ├── signup.html
│   ├── verify-email.html
│   └── consent.html     — PDPA consent (4 toggles)
│
├── learner/             ← Learning System + Student dashboard + Career stub
│   ├── dashboard.html   — 3-column home: nav / focus / cohort context
│   ├── curriculum.html  — Program → Phase → Module → Session tree
│   ├── session.html     — content view (video / reading / live / async)
│   ├── assignment-submit.html
│   ├── schedule.html    — week + month calendar (onsite + online)
│   ├── portfolio.html   — auto-aggregated work + curate
│   ├── resume.html      — JSON Resume + 2 templates
│   └── profile.html     — settings + consent + payment history
│
├── instructor/          ← Cohort + grading
│   ├── dashboard.html
│   ├── cohort-detail.html      — roster / analytics / schedule / communications
│   ├── grading-queue.html
│   ├── content-authoring.html
│   └── announcement-composer.html
│
└── admin/               ← Student Portal (NICHE staff)
    ├── dashboard.html
    ├── programs.html
    ├── cohorts.html
    ├── cohort-detail.html      — admin view of a cohort
    ├── users.html
    ├── user-detail.html        — role/scope matrix + PDPA tab
    ├── enrollments.html
    ├── invite-link.html
    ├── schedule.html           — cross-cohort calendar
    ├── payments.html
    ├── analytics.html
    ├── role-assignment.html    — multi-role + scope modal
    ├── audit-log.html
    └── pdpa.html
```

## How to view

Open any HTML file in a browser. No build step. No dev server needed.

```bash
# macOS
open platform/public/index.html
open platform/admin/cohort-detail.html
open platform/learner/dashboard.html
```

## Design system

Every page imports the same 3 stylesheets in order:

```html
<link rel="stylesheet" href="../shared/tokens.css">
<link rel="stylesheet" href="../shared/base.css">
<link rel="stylesheet" href="../shared/platform.css">
```

- **`tokens.css`** — color, typography, spacing, motion. Single source of truth. Identical to brand-book.
- **`base.css`** — CSS reset + semantic typography classes (`t-h1`, `t-eyebrow`, etc.).
- **`platform.css`** — app shell, sidebar, topbar, KPI tile, data table, status chips, etc.

To change brand-wide design (e.g., new pillar color), edit `tokens.css` only — propagates to every screen.

## Conventions

### Status taxonomy (NICHE-specific)

The platform uses 6 lesson/session states beyond the typical "in-progress / done":

- `locked` — gated by prerequisite or schedule
- `current` — active right now
- `complete` — finished
- `needs-revision` — instructor returned for resubmit
- `live-now` — live session in progress (pulse animation)
- `onsite-only` — must be physically present; no remote join

Use the `.status-chip` component with the appropriate modifier class.

### Pace indicator (cohort-relative)

Replaces absolute % progress bars. A learner is:

- `ahead` (moss-green) — beyond cohort median
- `on-track` (neutral) — within cohort median ± 1 session
- `behind` (red) — > 2 sessions behind

Use the `.pace` component.

### Pillar tags

Three pillars get distinct tinted-pill colors:

- Creativity → red tint
- Humanity → moss-green tint
- Entrepreneurship → ink-grey

Use `.pillar-tag.pillar-tag--{pillar-name}`.

## Translating to production code

These are HTML mockups. The Next.js + shadcn/ui platform will translate:

- `<aside class="sidebar">` → shadcn `<Sidebar>` component
- `<table class="data-table">` → shadcn `<DataTable>` (TanStack Table)
- `<button class="btn btn--primary">` → shadcn `<Button variant="default">`
- `<span class="status-chip status-chip--complete">` → shadcn `<Badge variant="success">`

The class names in `platform.css` are the contract between mockup and production. shadcn components will be themed via the same `tokens.css` variables.

## What's not in the mockups (intentionally)

Mockups are static. They don't exercise:

- Live data fetching (tRPC / Supabase queries)
- Authorization (OpenFGA permission checks)
- Real-time updates (WebSocket / Pusher)
- Form submission to a backend
- File upload to Cloudflare R2
- Video playback (Cloudflare Stream)

These are validated separately in the dev environment per [`design/MVP_ROADMAP.md`](../design/MVP_ROADMAP.md).

## Reference

- Strategic context: [`design/PLATFORM_DESIGN.md`](../design/PLATFORM_DESIGN.md)
- Schema + RBAC: [`design/DATA_MODEL.md`](../design/DATA_MODEL.md)
- Admin UI patterns this implements: [`design/ADMIN_PATTERNS.md`](../design/ADMIN_PATTERNS.md)
- Pattern source decisions: [`design/UI_PATTERNS.md`](../design/UI_PATTERNS.md)
- Brand foundations: [`brand-book/`](../brand-book/)
