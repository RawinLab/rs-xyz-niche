# NICHE Project — Context for Claude Code

> Quick orientation for any Claude Code instance working in this repo.

## Mission

This repo holds three deliverables for **NICHE** — *New Institute of Creativity, Humanity & Entrepreneurship*, a Bangkok-based creative education institute launching September 2026:

1. **Brand book** (`brand-book/`) — v1.0 ready for stakeholder review · HTML+CSS site, 20 sections, generated print PDF
2. **Platform system design** (`design/`) — strategy + architecture + roadmap for the Learning + Student + Career portals
3. **Code-first design demo** (`platform/`) — 38 HTML screens proving the design system end-to-end · live at https://rawinlab.github.io/rs-xyz-niche/

Phase: **Design synthesis complete · pre-implementation**. Dev kickoff target June 2026.

## Project conventions

### Tokens-in-code is the source of truth

There is **no Figma source-of-truth file**. Design tokens live in `brand-book/css/tokens.css` (also copied to `platform/shared/tokens.css`). Editing tokens.css propagates across the brand book, the platform demo, and the future Next.js production build. See `design/UI_PATTERNS.md` §5 for the rationale.

When asked for design changes, prefer editing tokens or component classes in `*.css` over editing many HTML files.

### The 5-color palette is locked. Don't add new colors.

`#252026` ink · `#f2f1f0` cream · `#cccecd` warm gray · `#fe1d25` red · `#779152` moss green (+ shade and tint scales for green). Any color outside this set is a brand violation. The WCAG 2.2 AA audit + usage rules are in `BRAND_BOOK_RESEARCH.md` §4 — red is display-only (never body text), gray is decorative-only (never text).

### Voice rules (from `BRAND_BOOK_RESEARCH.md` §7)

- Declarative · provocative · short
- Side with the independent learner — use "you", not "students/learners"
- *"Find your niche"* · *"Are you learning the wrong way?"* · *"All Eyes on Independents"* are signature lines
- **Never** write "unlock your potential" / "transformative journey" / "empower the next generation" / "discover a better approach". This is a hard rule.

### Class contract in `platform/shared/platform.css`

The 38 HTML demo files share these class names: `.app-shell`, `.sidebar`, `.kpi-tile`, `.data-table`, `.status-chip` (with 6 NICHE states), `.pace`, `.pillar-tag`, `.btn--primary/--secondary/--ghost/--text/--destructive/--lg/--moss-soft`, etc. Renaming any of these breaks all 38 files. **Add new variants; don't rename existing ones.**

### NICHE-specific patterns to preserve

- **6 status states for sessions:** `locked` · `current` · `complete` · `needs-revision` · `live-now` · `onsite-only` (the last is unique to NICHE's onsite-first model — keep it)
- **Pace indicator** (`ahead/on-track/behind`) replaces absolute % progress — cohort-paced, not self-paced
- **`needs_1on1` submission status** — the unique exploit of onsite-first model for instructor feedback (see `design/DATA_MODEL.md` §2.4)
- **Cohort-first IA** — never structure UIs around individual learners alone; cohort context goes in topbar + sidebar consistently

## Headline decisions (committed)

Per `design/PLATFORM_DESIGN.md` §0:

- **Build vs Buy:** Hybrid Year 1 (Disco LMS + custom Next.js Student Portal + Career stub) → fully custom Year 2 exit ramp
- **Stack:** Next.js 15 + tRPC + Drizzle + Supabase Postgres SG + Clerk + OpenFGA + Cloudflare R2/Stream + Resend + Railway SG
- **Authorization:** OpenFGA (ReBAC) — supports "instructor of A, learner of B" natively, migrates additively to Creator/Employer/Marketplace
- **Career System MVP:** auto-aggregate portfolio + JSON Resume + in-house Open Badges 2.0 issuer. Defer OB 3.0, employer login, AI features.

When in doubt about scope, refer to `design/PLATFORM_DESIGN.md` §0 (TL;DR table) before suggesting alternatives.

## Common tasks

### Run the brand-book PDF build

```bash
cd brand-book && python3 build-print.py
# bundles 20 sections into print.html · print to PDF in browser
```

### Modify a platform screen

Edit the HTML file in `platform/{public,auth,learner,instructor,admin}/`. Use existing component classes from `platform/shared/platform.css`. Add new utility classes inline only when truly page-specific.

### Add a new screen

1. Choose role directory (`learner/`, `admin/`, etc.)
2. Copy the closest existing file as a template
3. Use the same `<head>` block (3 stylesheets + Google Fonts + viewport + robots noindex meta)
4. Add the demo banner: `<div class="demo-banner"><span class="demo-banner__dot"></span>NICHE Demo · {Track}</div>`
5. Update `platform/index.html` to link the new screen

### Deploy the demo

Push to `main`. The `.github/workflows/pages.yml` workflow auto-deploys `platform/` to GitHub Pages within ~30 seconds. Verify via `gh run watch`.

### Verify before committing

- Open the changed file in a browser (no build step needed)
- Check that `<meta name="robots" content="noindex, nofollow">` is present (required for all platform/* pages)
- Check that the demo banner is present
- Check that all 3 stylesheet imports resolve (`../shared/{tokens,base,platform}.css`)

## What NOT to do

- ❌ Add new colors outside the 5-color palette + green tints
- ❌ Use generic edtech voice ("unlock your potential", "transformative")
- ❌ Rename existing CSS classes used across the 38 HTML files
- ❌ Introduce a Figma source-of-truth file (we explicitly chose code-first; see `design/UI_PATTERNS.md` §5)
- ❌ Add a build step to `platform/` (it's intentionally static)
- ❌ Use star ratings, "courses sold" counters, or marketplace patterns — NICHE is an institute, not a marketplace
- ❌ Write code that hardcodes role names (`if (role === 'admin')`) — always use the OpenFGA permission abstraction `can(user, permission, scope)` per `design/DATA_MODEL.md` §1
- ❌ Push the repo private (`gh repo edit ... --visibility private`) — repo is intentionally public; sensitive ops details are kept out of git

## What's reversible vs not

- **Reversible:** edits to HTML/CSS/Markdown, local commits, branch operations
- **Hard to reverse:** pushing to `main` (Pages auto-deploys; cached/forked content remains in others' clones), changing repo visibility
- **Irreversible:** repo is already public; any sensitive data committed has already been distributed

When making non-obvious changes, prefer a feature branch and PR over direct push to `main`.

## Where to find what

| Need | File |
|---|---|
| Strategic decisions (build vs buy, stack, roadmap) | `design/PLATFORM_DESIGN.md` |
| DB schema + RBAC + permissions | `design/DATA_MODEL.md` |
| Admin/Student Portal UI patterns | `design/ADMIN_PATTERNS.md` |
| 5-month sprint plan | `design/MVP_ROADMAP.md` |
| Brand voice + color rules + WCAG | `BRAND_BOOK_RESEARCH.md` |
| Brand book site (rendered) | `brand-book/index.html` |
| Platform demo (rendered) | `platform/index.html` |
| Platform requirements from NICHE | `requirements/NICHE_Platform_Requirements_v0.4_TH.pdf` |
| Original brand designer PDF | `raws/NICHE_BRAND (1).pdf` |
| Platform CSS contract | `platform/shared/platform.css` |
| Conventions + shadcn mapping | `platform/README.md` |

## Live URLs

- **Platform demo:** https://rawinlab.github.io/rs-xyz-niche/
- **Repo:** https://github.com/RawinLab/rs-xyz-niche

## Open questions waiting on NICHE leadership

Per `design/MVP_ROADMAP.md` Pre-flight checklist (must close by end of May 2026):

1. Build vs Buy decision (Hybrid recommended)
2. Pedagogical model freeze (program structure, assessment, cohort ops)
3. Disco contract signed
4. Dev retainer signed (Model B or C from PDF §6.1)
5. Trademark search filed (Thailand DIP / USPTO / EUIPO)
6. PDPA legal review of Disco cross-border transfer
7. Brand book v1 frozen and approved by leadership

If any task involves these, flag the dependency rather than picking unilaterally.
