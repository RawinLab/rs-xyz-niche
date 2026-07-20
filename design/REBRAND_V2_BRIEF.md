# NICHE Brand V2 — Rebrand & UX Alignment Brief

> Source of truth handed down 2026-07-20 (RSX-523 comment). **Brand V2 supersedes the
> in-repo brand book v1 palette, typography, and several platform UI decisions.**
>
> References (fetch these directly — all content is public and annotated):
> - Brand ID V2: https://carmochest.github.io/niche/brand/
> - Homepage mock built from Brand ID: https://niche-public-facing-site.vercel.app/
> - LMS mock (features decided internally by CEO เชษฐ์ — implement as shown): https://carmochest.github.io/niche/

## 1. Brand V2 core system

### Color (replaces the old 5-color ink/cream/red/moss palette)

| Token | Hex | Role |
|---|---|---|
| Black | `#0A0A0A` | Identity base — the brand is black on white |
| White | `#FFFFFF` | Base surface |
| Gray | `#757575` | Only neutral support |
| Creativity | `#FF4000` | Pillar color — blob mark |
| Humanity | `#E50695` | Pillar color — circle mark |
| Entrepreneurship | `#0533F3` | Pillar color — triangle mark |

**The rule:** identity is black on white. A pillar color appears only as a **full flood**
(entire poster/banner/section) or **inside the mark itself** — never as an accent, tint,
or decoration. One color per piece.

### Typography (replaces Fraunces + Bai Jamjuree)

One family: **Libre Franklin**, all nine weights. Hierarchy is built with weight and
scale, never a second typeface.

| Level | Weight | Tracking |
|---|---|---|
| Display | Black 900 | −4.5% |
| H1 | ExtraBold 800 | −3% |
| H2 | Bold 700 | −2% |
| Body | Regular 400 | 0 |
| Caption | SemiBold 600 | +14%, all caps |

### Wordmark & mark

- Wordmark: `NICHE` in Libre Franklin Black 900, tracked −4.5%, followed by **the mark**
  on the baseline — 0.165× type size, 0.07em gap (mark enlarges to 0.42em below ~32px).
- The mark is punctuation, not a logo: **blob** = Creativity, **circle** = Humanity,
  **triangle** = Entrepreneurship. It ends the name (`NICHE ●`) or stands alone
  (favicon/avatar) — never both at once.
- Sub-brands/programs: institute name in Black, program name in Thin, mark takes the
  program's shape. No extra symbols.
- Motion on screens (mark morphs between states); frozen in print.

### Voice

- "Find your niche." remains the signature line. New supporting line: "Learn by building".
- Old repo voice rules (declarative, short, "you") still consistent with V2 samples.

## 2. Public site IA (per homepage mock)

Three-level structure: **School → Program → Pathway**.

**Schools & programs (12):**
- School of Business & Entrepreneurship: Sales & Dealmaking · Online Store & E-Commerce · Running a Business with AI · Start & Build Your Business
- School of Creativity: Content Creator Studio · Branding & Design · Digital Marketing for Growth · Craft & Product Making
- School of Hospitality & Humanities: Coffee: From Bean to Café · Wellness & Spa · Pet Care & Business · Hospitality & Service Excellence

**Pathways (every program starts as a Bootcamp; extend by adding modules):**

| Pathway | Duration | Modules | Tuition |
|---|---|---|---|
| Bootcamp / Lab | 3 months | 4 | ฿15,000 |
| Studio | 6 months | 8 | ฿30,000 |
| Professional | 12 months | 16 | ฿65,000 |

2026 soft launch: 6 programs across two waves, Sep 2026 intake, 0% installments.
(All dates/pricing marked "draft prototype — indicative" on the mock.)

## 3. LMS / Student Portal feature set (per LMS mock — decided, implement as shown)

Left sidebar nav: **Dashboard · Chat · Learn · Progress** (+ program switcher:
General / per-program / Career services).

- **Dashboard:** greeting, programs-in-progress cards (module N of M, next/live class,
  join/open CTA), enroll-in-another-program, updates/announcements feed.
- **Chat:** "NICHE Tutor" AI grounded in course materials, aware of the learner's current
  module/lesson; recents list scoped per program.
- **Learn:** Today's classes (Live online / In-person / Async-self-paced), upcoming +
  previous classes with attendance ✓ and replays, **Submissions** (due/open/submitted/
  reviewed states), **Course materials** library (videos/slides/readings/datasets,
  filterable, per program/module).
- **Progress (per program):** % program progress + module N of M, **Standing**
  (e.g. "Meeting/Exceeding" across modules), attendance %, module journey with
  instructor notes per completed module, locked capstone, **portfolio pieces
  auto-created from module work** (+ "Generate a portfolio piece" AI action), link to
  job portal.
- Multi-program enrollment is first-class (learner shown in 2 programs simultaneously).

### Conflicts with existing repo patterns — V2 mock wins

| Repo pattern (old) | LMS mock (new) |
|---|---|
| Pace chip (ahead/on-track/behind), no absolute % | Program progress **%** + Standing label |
| 6 session states incl. `onsite-only` | Class formats: Live online / In-person / Async |
| Fraunces/Bai Jamjuree, ink-on-cream | Libre Franklin, black-on-white |
| Moss/red accent usage | Pillar-color floods only; UI chrome is black/white/gray |

`needs_1on1`-style instructor feedback survives as "K. Anan's note" per module — keep
the concept, restyle the surface.

## 4. Impact map

1. `brand-book/css/tokens.css` + `platform/shared/tokens.css` — full token replacement.
2. `platform/shared/{base,platform}.css` — restyle component contract to V2 (keep class
   names; add variants, don't rename).
3. `platform/**` 38 screens — restyle + IA realignment to LMS mock (learner portal
   especially); public screens realign to homepage mock IA (Schools/Programs/Pathways).
4. `brand-book/` v1 — **superseded** by the external Brand ID V2. Do not iterate on v1
   content until leadership decides whether to rebuild the brand book to document V2.
5. `CLAUDE.md`, `BRAND_BOOK_RESEARCH.md`, `design/UI_PATTERNS.md` — update palette/type
   guardrails to V2 as part of the rebrand work.
