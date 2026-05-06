# NICHE — Brand Book + Platform Design + Demo

> **NICHE** = New Institute of Creativity, Humanity & Entrepreneurship
> Bangkok-based creative education institute · Cohort-based, hands-on · Soft Launch September 2026
> Tagline: **Find your niche.**

This repository holds the complete brand and platform foundation for NICHE — from the brand book deliverable through the platform system design, to a clickable HTML demo of all 38 platform screens.

**🟢 Live demo:** https://rawinlab.github.io/rs-xyz-niche/

---

## What's in this repo

```
rs-xyz-niche/
├── brand-book/             ← Brand book v1.0 deliverable (HTML+CSS site, 20 sections)
│   ├── index.html          ←   open this for the brand book site
│   ├── sections/           ←   20 section files
│   ├── css/{tokens,base,book}.css
│   ├── js/nav.js
│   ├── build-print.py      ←   Python script bundling all sections into print.html
│   └── assets/
│
├── design/                 ← Platform system design (5 strategy docs)
│   ├── PLATFORM_DESIGN.md  ←   start here · build vs buy · tech stack · architecture
│   ├── DATA_MODEL.md       ←   schema · OpenFGA · permission catalog · migration phases
│   ├── ADMIN_PATTERNS.md   ←   Admin Portal UI playbook (sidebar IA, cohort dashboard)
│   ├── UI_PATTERNS.md      ←   adopt/reject patterns from Figma references
│   └── MVP_ROADMAP.md      ←   5-month week-by-week plan to Sept 2026
│
├── platform/               ← Code-first design demo (38 HTML screens)
│   ├── index.html          ←   demo entry point — links to all 38 screens
│   ├── shared/             ←   tokens.css + base.css + platform.css + logos
│   ├── public/  (7)        ←   landing · programs · about · faculty · faq · apply · etc.
│   ├── auth/    (4)        ←   login · signup · verify-email · PDPA consent
│   ├── learner/ (8)        ←   dashboard · curriculum · session · portfolio · resume · etc.
│   ├── instructor/ (5)     ←   dashboard · cohort-detail · grading-queue · authoring · etc.
│   ├── admin/   (14)       ←   dashboard · cohorts · users · payments · PDPA · etc.
│   ├── README.md           ←   convention + how to translate to Next.js/shadcn
│   └── robots.txt
│
├── requirements/           ← Source-of-truth requirements from NICHE
│   ├── NICHE_Platform_Requirements_v0.4_TH.pdf  ←   the platform spec (Thai, v0.4 DRAFT)
│   └── ref.md              ←   Figma reference URLs
│
├── raws/                   ← Original PDFs from designer
│   └── NICHE_BRAND (1).pdf ←   18-page brand exploration (3 logo options + mockups)
│
├── BRAND_UNDERSTANDING.md  ← Factual inventory of raws/ (no opinion)
├── BRAND_BOOK_RESEARCH.md  ← Opinionated research synthesis (12 sections + sources)
├── NICHE_BRAND_BOOK.md     ← Single-file markdown brand book
├── NICHE_BRAND_BOOK.pdf    ← Production print edition (30 MB)
└── CLAUDE.md               ← Project context for Claude Code
```

---

## Live URLs

| Resource | URL |
|---|---|
| **Platform demo (38 screens)** | https://rawinlab.github.io/rs-xyz-niche/ |
| Demo · Admin · Cohort detail | https://rawinlab.github.io/rs-xyz-niche/admin/cohort-detail.html |
| Demo · Admin · Role assignment (RBAC) | https://rawinlab.github.io/rs-xyz-niche/admin/role-assignment.html |
| Demo · Learner dashboard | https://rawinlab.github.io/rs-xyz-niche/learner/dashboard.html |
| Demo · Public landing | https://rawinlab.github.io/rs-xyz-niche/public/index.html |

The demo is `noindex` so it won't appear in search engines.

---

## Quick start

### View the platform demo locally

No build step. Open any HTML file:

```bash
open platform/index.html              # demo entry point
open platform/admin/cohort-detail.html # the differentiator screen
open platform/learner/dashboard.html   # 3-column cohort-aware home
```

### View the brand book

```bash
open brand-book/index.html
```

### Generate the brand-book PDF

```bash
cd brand-book
python3 build-print.py    # bundles all sections into print.html
# Then print → save as PDF in browser
```

### Read the platform design

Start with `design/PLATFORM_DESIGN.md`. It's the executive synthesis with build-vs-buy recommendation, tech stack, IA, and 5-month roadmap. The other design docs are companions for specific topics.

---

## Headline decisions (from `design/PLATFORM_DESIGN.md`)

| Decision | Recommendation |
|---|---|
| **Build vs Buy** | **Hybrid for Year 1** — Disco (Learning System + community) + custom Next.js (Student Portal + Career stub). Year 2 = exit ramp to fully custom. |
| **Custom tech stack** | Next.js 15 + tRPC + Drizzle + Supabase Postgres SG + Clerk + OpenFGA + Cloudflare R2/Stream + Resend + Railway SG. ~$40-55/mo infra. |
| **Authorization** | OpenFGA (Apache 2.0, CNCF Incubating) — handles "instructor of A, learner of B" natively. Migrates additively to Creator/Employer/Marketplace. |
| **Career System MVP** | Auto-aggregate portfolio + JSON Resume builder + in-house Open Badges 2.0. Defer OB 3.0, employer login, AI features. |
| **Soft Launch** | September 2026 (~5 months from May 2026 design freeze) |
| **Cohort 1** | 11–30 November 2026 |

---

## Brand foundations

The 5 brand colors and complete WCAG audit are in `brand-book/css/tokens.css` (also copied to `platform/shared/tokens.css` — single source of truth):

| Hex | Role |
|---|---|
| `#252026` | Near-black (primary surface dark · primary text) |
| `#f2f1f0` | Cream (primary surface light · page background) |
| `#cccecd` | Warm gray (decorative only — never text) |
| `#fe1d25` | Vivid red (accent · CTAs · large display only) |
| `#779152` | Moss green (program signage · body on ink only) |

**Typography:** Fraunces (display, free) + Bai Jamjuree (Thai+Latin body, free SIL OFL).
**Voice:** Declarative · provocative · short. *"Find your niche"* · *"Are you learning the wrong way?"* · *"All Eyes on Independents"*. Never *"unlock your potential"* or *"transformative journey"*.

---

## How design works in this project

This repo is a **code-first design** workflow — the design tokens live in `tokens.css`, the design system lives in `platform.css`, and screens live as HTML files. There's no Figma source-of-truth file.

To change brand-wide design (e.g., new pillar color), edit `tokens.css` once — propagates to every screen across both the brand-book site and the platform demo.

When the dev team builds the production Next.js + shadcn/ui platform, the same `tokens.css` variables drive the React components. The class contract in `platform.css` (e.g., `.btn--primary`, `.kpi-tile`, `.status-chip--complete`) maps 1:1 to shadcn primitives — see [`platform/README.md`](./platform/README.md) for the translation table.

---

## Tech & infrastructure

- **Hosting:** GitHub Pages (Actions-based deploy of `platform/` subfolder)
- **CI/CD:** `.github/workflows/pages.yml` — auto-deploy on `push` to `main`
- **Source:** Public repo · MIT-style internal use (NICHE-owned brand IP)

---

## Status & current phase

- ✅ Brand book v1.0 complete (`brand-book/`)
- ✅ Platform system design complete (`design/`)
- ✅ Code-first demo of 38 screens (`platform/`)
- ✅ GitHub Pages deployed
- ⏳ Awaiting NICHE leadership decisions:
  1. Build vs Buy (recommended: Hybrid)
  2. Pedagogical model freeze (program structure, assessment, cohort ops)
  3. Disco contract + dev team retainer
  4. Trademark search (Thailand DIP / USPTO / EUIPO)
- ⏳ Pre-kickoff actions per [`design/MVP_ROADMAP.md`](./design/MVP_ROADMAP.md) Phase 0
- 🟡 Phase 1 dev kickoff target: June 2026

---

## Documentation map (reading order)

For NICHE leadership:
1. [`design/PLATFORM_DESIGN.md`](./design/PLATFORM_DESIGN.md) — strategic synthesis
2. [`design/MVP_ROADMAP.md`](./design/MVP_ROADMAP.md) — week-by-week plan
3. View the live demo: https://rawinlab.github.io/rs-xyz-niche/
4. [`BRAND_BOOK_RESEARCH.md`](./BRAND_BOOK_RESEARCH.md) — brand decisions

For incoming dev team:
1. [`design/PLATFORM_DESIGN.md`](./design/PLATFORM_DESIGN.md) §3 (tech stack) and §11 (open questions answered)
2. [`design/DATA_MODEL.md`](./design/DATA_MODEL.md) — schema + RBAC
3. [`design/ADMIN_PATTERNS.md`](./design/ADMIN_PATTERNS.md) — UI playbook
4. [`platform/README.md`](./platform/README.md) — convention + shadcn mapping
5. [`design/MVP_ROADMAP.md`](./design/MVP_ROADMAP.md) — 5-month plan

For Claude Code working in this repo:
1. [`CLAUDE.md`](./CLAUDE.md)

---

## License & ownership

- **Brand IP** (logos, name, programs, copy) — © NICHE
- **Code in `platform/` and `brand-book/`** — internal use; not for redistribution
- **Documentation** — internal working docs; share with consultants/partners under NDA where applicable

The repository is public for transparent collaboration with consultants and prospective dev teams. Sensitive operational details (specific budget figures, vendor contracts, learner data) are not stored in this repo.

---

*Last updated: 2026-05-06*
