# NICHE Platform — System Design & MVP Plan

> **Project:** NICHE Platform = Learning System + Student Portal + Career System (3 ระบบในประสบการณ์เดียว)
> **Date:** 2026-05-06
> **Status:** v1.0 design synthesis (research crystallized for dev team review)
> **Soft Launch:** September 2026 (~5 months from authoring date)
> **Audience:** NICHE leadership · incoming developer team · future Tech Manager
> **Companions:**
> - **[DATA_MODEL.md](./DATA_MODEL.md)** — schemas + RBAC + OpenFGA model + permission catalog + migration phases
> - **[MVP_ROADMAP.md](./MVP_ROADMAP.md)** — 5-month week-by-week plan to Sept 2026 launch
> - **[ADMIN_PATTERNS.md](./ADMIN_PATTERNS.md)** — Admin / Student Portal UI playbook (sidebar IA, cohort dashboard, RBAC modal, CSV import, schedule, announcements, payments, PDPA)
> - **[UI_PATTERNS.md](./UI_PATTERNS.md)** — Adopt/reject patterns from Figma references + recommendation to shift to code-source-of-truth design
> - **[../BRAND_BOOK_RESEARCH.md](../BRAND_BOOK_RESEARCH.md)** — Brand foundations (typography, color, motion, voice)

This document consolidates research from 8 parallel streams (4 Figma references + 4 deep-research streams on cohort LMS architecture, Career System patterns, RBAC/multi-role/PDPA, and Admin UI patterns) into a single decision-ready brief. Every recommendation is opinionated. Treat it as the working spec for the dev team to evaluate, push back on, and execute against — not as neutral background.

---

## 0. Executive Summary (TL;DR)

| Decision | Recommendation |
|---|---|
| **Build vs Buy** | **Hybrid for Year 1** — adopt Disco for Learning System + community; build a thin custom Student Portal + Career System stub in Next.js. Exit ramp to fully custom in Year 2 once Tech Manager is hired and revenue proven. |
| **Custom tech stack (when build)** | Next.js 15 (App Router) + tRPC + Supabase Postgres (ap-southeast-1 Singapore) + Drizzle + Clerk + Cloudflare R2 + Cloudflare Stream + Resend + Railway SG. Total infra ~$40-55/month at MVP scale. |
| **Authorization** | **OpenFGA** (Apache 2.0, CNCF Incubating) for ReBAC — handles "instructor of A, learner of B" natively and migrates additively to Creator/Employer/Marketplace without redesign. Auth0 FGA managed for early days; self-host at scale. |
| **Identity** | **Clerk** for MVP — production auth in 10 min, MFA + magic link + Google + Thai SMS OTP, free tier covers <100 users. Migration path to Better Auth (self-hosted) post-launch if data ownership becomes a Tech Manager priority. |
| **Career System architecture** | Auto-aggregate (every assignment becomes a portfolio record) + manual curate (learner publishes) + JSON-Resume-backed resume builder + in-house Open Badges 2.0 issuer. Defer OB 3.0/W3C VC, employer login, AI features. |
| **PDPA strategy** | Supabase Singapore region (practical residency) + explicit cross-border consent on signup + granular per-purpose consent toggles + 72h breach response runbook + soft-delete anonymization for right-to-erasure. |
| **MVP scope cut** | **Cut from MVP**: Career System full features (ship as Notion/Airtable stub), Employer Portal, AI features, native mobile app, peer review, in-platform DMs (use Discord/Line), payment installments, full Thai language UI (i18n strings ready, switcher post-launch). |
| **Critical gaps in references** | All 4 Figma refs are gated community files; SchoolHub admin has **zero cohort concept** and **single-role admin only** — NICHE's cohort-first + multi-role architecture must be designed from scratch. |
| **Timeline** | 5 months tight but feasible with hybrid path + 1 senior + 2 mid devs + frozen pedagogical model by June 2026. Full custom build in 5 months requires 3-4 devs and is high-risk. |

---

## 1. Requirements DNA Confirmed (from PDF v0.4)

- **Brand positioning** — *NICHE เป็นสถาบัน, ไม่ใช่ marketplace.* "เน้นการเชื่อมต่อผู้เรียนเข้าสู่ตลาดแรงงานอย่างตรงจุด" — every product decision must reinforce this anti-marketplace stance.
- **Pedagogical model** — cohort-based, hands-on, **onsite เป็นหลัก + online module เสริม** (ไม่ใช่ self-paced).
- **Three program tiers** — Bootcamp 3m / Studio 6m / Degree 12m, all cohort-based.
- **Path metaphor** — เรียน → ลงมือทำ → สร้างผลงาน → เข้าสู่อาชีพ. Career System is the strategic differentiator.
- **Three systems mapped to "portals" the user named:**
  - "learning portal" = **Learning System** (LMS-like — content delivery, assignment, feedback)
  - "management portal" = **Student Portal** (dashboard, schedule, cohort, enrollment, payment, announcement, analytics)
  - "job-link portal" = **Career System** (Portfolio + Resume + Certificate + future Employer view)
- **Three core MVP roles** — Learner, Instructor/Facilitator, Admin (NICHE).
- **Three future roles** — Creator/Content Partner, Employer/Partner, Teaching Assistant. Architecture must accommodate from day one without redesign.
- **Scope** — RBAC must support Course / Program / Platform levels; one user can hold multiple roles.
- **Out-of-MVP scope (explicit)** — Marketplace, self-paced LMS, full university stack (grading scales, multi-semester, transcripts), platform that builds its own video hosting (use YouTube/Vimeo embed for MVP).
- **Constraints** — <100 users at launch · 99%+ uptime during class · PDPA · Thai+English (English first acceptable for MVP) · Mobile-responsive · Tech Manager not yet hired.

---

## 2. The Build vs Buy Decision

### 2.1 The honest framing

The PDF's §7.1 question — *"custom build, or open-source LMS adapted?"* — is a false binary. The 2026 mature answer is **hybrid**: buy what's commodity, build what differentiates.

Commodity (shouldn't build): video hosting, email delivery, auth/identity, file storage, calendar embedding, community/forums.

Differentiator (must build to own): the cohort experience, the Career System, the brand voice, the Thai-localized journey, the data NICHE collects on its learners.

### 2.2 Buy candidates evaluated

| Platform | Verdict | Why |
|---|---|---|
| **Disco** ($399/mo Org tier) | ✅ Best buy option | Best-in-class cohort + community + multi-cohort mgmt + AI tools; Thai THB Stripe payments; SSO available |
| **Maven** | ❌ Disqualifying | 10% revenue share + Maven owns the student relationship — fatal for an institute brand |
| **Open edX** | ❌ Wrong scale | 3-5 months just to deploy cleanly; UI is dated; appropriate at 10,000+ students, not 100 |
| **Moodle** | ❌ Wrong fit | University-shaped; cohort is plugin-dependent; theming work to meet brand premium positioning is significant |
| **Canvas** | ❌ Disproportionate | $10k+/yr enterprise minimum for <100 users |
| **Circle / Mighty Networks** | ❌ Wrong category | Community tools, not LMS — would require LMS layer on top |

### 2.3 Custom build path

If NICHE goes fully custom (rejecting Disco), the realistic stack and team:

- **Stack:** Next.js 15 (App Router) + tRPC + Drizzle + Postgres (Supabase SG) + Clerk + Cloudflare R2 + Stream + Resend + Railway SG.
- **Team:** 1 senior full-stack (the technical decision-maker) + 2 mid-level + 1 part-time designer (or shadcn/ui to compress design work).
- **Risk:** 5 months to deliver Learning + Student Portal + Career stub is tight; cohort orchestration features alone (multi-cohort mgmt, peer visibility, live session scheduling) eat 3-4 months → leaves no runway for Career System.

### 2.4 The recommended path: Hybrid with 12-month exit ramp

**Year 1 (now → Sept 2026 launch + 12 months):**
- Disco = Learning System (content delivery, assignments, cohort dashboards, community, live sessions). Whitelabel as much as $399 tier allows; accept "Powered by Disco" footer.
- Custom Next.js Student Portal = NICHE-branded landing, learner dashboard wrapper, application flow, payment, announcements, schedule overlay (onsite + online).
- Custom Career System stub = portfolio links page (Notion or Airtable-backed) + manually issued PDF certificates with QR verification page on niche.com.

**Year 2 (post-launch + 12-18 months):**
- Tech Manager hired, revenue proven, requirements stabilized.
- Custom Learning System replaces Disco, migrating cohort data through Disco's CSV exports + API.
- Career System upgrades to full architecture (auto-aggregate portfolios, JSON-Resume builder, Open Badges 2.0 issuer, employer inquiry portal).

**Why this is the correct call:**
- Disco at $399/mo = ~THB 14,400/mo, less than 1 dev-month per year.
- 5-month timeline becomes humanly achievable.
- PDPA risk is documented and managed (Disco is US-hosted; explicit cross-border consent at signup; <100 users keeps risk surface small).
- Brand-critical surfaces (landing, application, dashboard wrapper, Career System) are 100% NICHE-controlled from day one.
- Exit path is defined upfront — not "we got locked in and now can't leave."

### 2.5 The decision NICHE leadership must make

Before dev team estimation, NICHE must commit to **one** of:

- **(A) Hybrid path (recommended)** — sign Disco contract, build Next.js Student Portal + Career stub.
- **(B) Full custom build** — must extend timeline to ~7 months OR accept narrower MVP than PDF §4 lists. Requires 3-4 devs.
- **(C) Pure Disco** — fastest, cheapest, lowest brand control. Disco hosts every learner touchpoint. Career System requires manual curation.

A → C in increasing risk for the 5-month timeline; A → C in decreasing brand differentiation. **Recommendation = A.**

---

## 3. Tech Stack Recommendation (Custom Components)

For the parts NICHE will build (Student Portal + Career System stub in Hybrid path; or the entire platform in Custom path):

| Layer | Choice | Reasoning |
|---|---|---|
| **Frontend / Backend** | Next.js 15 (App Router) + tRPC | 2026 industry standard SaaS; largest Thai dev talent pool; Vercel/Railway deploy trivial; tRPC eliminates separate API for MVP, end-to-end type safety |
| **Database** | Supabase Postgres, ap-southeast-1 (Singapore) | Singapore region = practical PDPA residency; Pro tier $25/mo includes auth, storage, point-in-time recovery; future TM can grok |
| **ORM** | Drizzle (preferred) or Prisma 7 | Drizzle = smaller bundle, SQL-close, serverless-friendly; Prisma if dev team is junior (Studio UI is forgiving) |
| **Auth (Identity)** | Clerk | 10-min production auth; MFA + magic link + Google + Thai SMS OTP; free tier covers MVP; Better Auth as future-proof open-source migration |
| **Authorization** | OpenFGA (or Auth0 FGA managed) | ReBAC for "instructor of A, learner of B"; Apache 2.0; CNCF Incubating; migrates additively to marketplace |
| **File storage** | Cloudflare R2 | Zero egress fees vs S3 (egress is cost dominator for assignment/resource downloads); S3-compatible for migration optionality |
| **Video** | Cloudflare Stream → Mux at scale | $5/1k min stored + $1/1k min delivered = ~$3/mo at MVP scale; Mux when per-learner watchtime data and engagement heatmaps are needed |
| **Email** | Resend (MVP) → Postmark (growth) | Resend free 3k emails/mo + native React Email components; Postmark switch at ~500 learners for deliverability premium on cohort notifications |
| **Hosting** | Railway (Singapore region) | Container-based; same private network as Postgres = low DB latency; cost-predictable vs Vercel's per-seat $40/mo + usage |
| **Background jobs** | BullMQ on Railway | Cohort notifications, certificate generation, analytics rollups |
| **PDF generation** | `@react-pdf/renderer` (MVP) → Puppeteer (scale) | Client-side avoids server infra at MVP scale; embed Sarabun (SIL OFL) for Thai resume text |
| **Avoid** | Vimeo (post-2025 Bending Spoons acquisition introduced 2TB caps + forced enterprise tiers); Open edX (DevOps overhead); Maven (revenue share + brand surrender) |

**Total infra cost (MVP, ~100 users):** $40–55/month. Disco adds $399/month = ~$440–455/month all-in for hybrid path.

**Skill profile of future Tech Manager:** TypeScript + SQL basics + Git + Railway dashboard. ~60-70% of working web devs in 2026 fit this profile. Stack avoids: Kubernetes, AWS IAM, Ruby/Python, PHP/Moodle plugins.

---

## 4. Three Systems, One Experience — Architecture

PDF §1 is explicit: *"Platform นี้ประกอบด้วย 3 ระบบหลักที่รวมอยู่ในประสบการณ์เดียว."* The user must feel one product, not three.

```
                    ┌─────────────────────────────────┐
                    │   NICHE Platform (one shell)    │
                    │   Sidebar + topbar + content    │
                    └─────────────────────────────────┘
                              │  (role + scope)
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
  Learning System        Student Portal        Career System
  (LMS-like)             (admin + learner      (Portfolio + Resume
                          overlap)              + Cert + Employer)
       │                      │                      │
       │  shared identity, RBAC, design tokens, auth │
       └──────────────────────┴──────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Public website    │  (Find your niche, 12 programs,
                    │  (marketing)       │   admissions journey, FAQ)
                    └────────────────────┘
```

### 4.1 The shared shell

Single sidebar + topbar layout across all 3 systems and all 6 roles. Sidebar items swap by role; shell stays stable. This is the single biggest UX leverage point: learners, instructors, and admins experience the same navigation grammar.

**Why:** SchoolHub (ref 4) and the LMS dashboard (ref 1) both use sidebar-first IA. Topbar-only nav fails at NICHE's matrix of 3 roles × 3 program levels × 12 programs.

**Mobile collapse:** sidebar → bottom tab bar (5 items max). Right rail (calendar/notifications) → swipe-up sheet.

### 4.2 Learning System — features (PDF §4.1, §4.2)

**Learner side (MVP):**
- Login (email or Google SSO via Clerk)
- Dashboard: hero "continue where you left off" card + cohort schedule strip + announcements + progress
- Course/module navigation (Program → Phase → Module → Session 4-level tree)
- Content access (video embed YouTube/Vimeo unlisted, PDF, text, link)
- Assignment upload (file or text submission to R2)
- Progress tracking (relative to cohort schedule, NOT absolute % — learner sees "On track / Behind by 2 sessions")
- Notifications (deadline, announcement, feedback) — email + in-app
- Mobile-responsive

**Learner side (post-MVP):** Peer forum per course

**Instructor side (MVP):**
- Content authoring (split-pane: tree left, editor right)
- Cohort management (roster table with attendance, progress %, last-active, status)
- Grade assignments + leave feedback
- Broadcast announcements to cohort (with cohort-targeting chips)
- Monitor cohort progress (4-up stat tiles: pending submissions / attendance / avg progress / unread announcements)

**Instructor side (post-MVP):** Calendar live session booking integration, rubric/grading scale UI

**Anti-patterns (research-driven, in NICHE's voice):**
- Star ratings on courses → marketplace, not institute
- "Browse 1000 courses" grids → NICHE has 36 programs across 3 pillars; curate, don't catalog
- Self-paced % progress bars → cohort = relative to schedule, not absolute
- Achievement badge gamification → infantilizing for serious institute brand
- AI tutor chatbot foregrounded → undermines "human instructor" value prop
- Recommended-for-you feeds → enrolled learners don't need recommendations, they need clarity about *this* program

### 4.3 Student Portal — features (PDF §4.3)

**MVP:**
- User management (Admin)
- Program / course creation (Admin)
- Enrollment (manual + invite link) — *invite is net-new pattern; SchoolHub provides only single-form add*
- Schedule (onsite + online sessions) — calendar with location-type toggle
- Cohort visibility — *largest design gap; SchoolHub has no cohort concept; design from scratch*
- Announcement (Admin → cohort)
- Basic analytics — KPI tile strip + cohort completion + at-risk learners
- Course catalog (admissions-facing)
- Payment (Stripe, Thai THB; one-time + future installment)

**Post-MVP:** Content version control, advanced reporting

**Cohort dashboard structure (NICHE-original):**
1. **Header** — cohort name, program, dates, enrollment vs capacity
2. **Roster tab** — table: learner / progress % / last active / assignment status / quick actions
3. **Analytics tab** — completion curve, at-risk list (bottom quartile of engagement signals: days-since-login + overdue submissions + lesson completion vs cohort median)
4. **Communications tab** — bulk announcement, segmented by status
5. **Bulk actions** — move dates, mass-enroll/unenroll, export roster CSV

### 4.4 Career System — features (PDF §4.4)

**MVP:**
- **Portfolio (basic)** — every assignment auto-logs to learner's private portfolio record; learner curates description, sets visibility (private/employer/public), picks max 3 featured pieces
- **Public portfolio URL** — `/u/{username}` shows published artifacts
- **Resume builder (template)** — 2 templates (clean + creative); pre-populates from program + portfolio; JSON Resume schema-backed; PDF export via @react-pdf/renderer with Sarabun font embedded
- **Certificate / credential download** — styled PDF with QR + Open Badges 2.0 assertion JSON hosted at `/credentials/{id}` + public verification page at `/verify/{id}` (no login required)

**Post-MVP:**
- **Skill tracking** — populate `rubric_scores` on portfolio items; aggregate skill progress dashboard
- **Public profile** (employer view)
- **Employer inquiry portal** — search/filter by program/skill/cohort + inquiry form (no direct cold contact); learner accepts/declines before contact info shared

**MVP cuts (defer to post-launch):**
- Peer review (too complex)
- Employer login (curated public listings + contact form is enough at MVP)
- Open Badges 3.0 / W3C VC wallet (OB 2.0 sufficient through 2026)
- LinkedIn sync, AI resume suggestions

**Why this works for NICHE:** Le Wagon's 86% employment rate is built on (a) project-based curriculum where every deliverable is a portfolio artifact, (b) Career Services-mediated employer access, (c) alumni network reactivation. NICHE inherits (a) by auto-logging assignments, builds the foundation for (b) with the credential + verification system, defers (c) to post-MVP.

---

## 5. Information Architecture

### 5.1 Sidebar items per role (MVP)

**Learner:**
1. Dashboard (home)
2. My Cohort (current cohort + schedule + classmates)
3. Curriculum (program → phase → module tree)
4. Assignments (submit + history + feedback)
5. Portfolio (my work, draft + published)
6. Resume
7. Certificates
8. Schedule (calendar view of all sessions)
9. Profile + Settings

**Instructor:**
1. Dashboard (4-up stat tiles)
2. My Cohorts (list + detail)
3. Content (authoring split-pane)
4. Grading (queue: pending / late / graded)
5. Announcements
6. Calendar
7. Profile + Settings

**Admin:**
1. Dashboard (KPI strip: cohort fill, active learners, MRR, completion %)
2. Cohorts (list + create + lifecycle: planning → open → running → completed)
3. Programs (the 12, organized under 3 pillars)
4. Users (with role assignment UI)
5. Enrollments (incl. invite generation)
6. Payments (Finance: tiles + tx table)
7. Announcements (platform + per-cohort)
8. Analytics (cohort + program + platform views)
9. Settings (organization, integrations, brand)

### 5.2 Public marketing site (separate from logged-in app)

Single Next.js app, separate route group `/(marketing)/`:
- `/` — Hero ("Find your niche") + 3-pillar segmented control + 12-program grid + cohort countdown chip + provocative FAQ + CTA banner
- `/programs` — full grid filtered by pillar / level (Bootcamp/Studio/Degree)
- `/programs/[slug]` — program detail + cohort dates + mentor cards + outcomes + apply CTA
- `/about` — institute story
- `/faculty` — instructor profiles
- `/journal` — editorial content (NICHE Journal masthead from brand book §2.3)
- `/apply` — admissions journey
- `/verify/[credentialId]` — public credential verification (no login)
- `/u/[username]` — public learner portfolio page

The marketing pages use the same NICHE design tokens but a different shell (no sidebar). This is the primary site for SEO + acquisition; the app shell starts after login.

### 5.3 Role context switcher (post-MVP, but architect today)

For multi-role users (e.g., Learner-alumni who becomes Creator), provide a context indicator in topbar showing active role + scope. Click to switch. Pattern: Slack workspace switcher.

Implementation: persist active context in session state (NOT JWT claim — JWT would require re-issue on switch). Clear UI state on switch to prevent data bleed.

---

## 6. Data Model + RBAC (overview — see DATA_MODEL.md for schema)

### 6.1 Core entities

- **User** — id, email, name, locale
- **Role** — id, name (enum), description (extensible — never hardcoded in app logic)
- **UserRoleMembership** — user × role × scope_type × scope_id × granted_at × expires_at — *the join table that does real work*
- **Permission** — key (e.g. `course:content:edit`), description
- **RolePermission** — role × permission × scope_type
- **Program** (the 12, under 3 pillars) — id, name, pillar, level (bootcamp/studio/degree), duration_months
- **Cohort** — id, program_id, name, start_date, end_date, capacity, status (planning/open/running/completed)
- **Enrollment** — user_id × cohort_id × status × enrolled_at
- **Course** (within a program) — id, program_id, name, order
- **Module** — id, course_id, name, order
- **Session** — id, module_id, type (live/onsite/online-async), starts_at, location_type, location, video_url
- **Assignment** — id, session_id, title, brief, deadline, max_score
- **Submission** — id, assignment_id, user_id, file_url, text, submitted_at, feedback, score, rubric_scores, status
- **PortfolioItem** — derived view over Submission + manual additions; visibility flag (private/employer/public)
- **Certificate** — id, user_id, program_id, issued_at, credential_url, pdf_url
- **Resume** — id, user_id, json_data (JSON Resume schema), template_id
- **Announcement** — id, scope (platform/program/cohort), author_id, title, body, audience_filter, scheduled_at
- **Payment** — id, user_id, cohort_id, amount, currency (THB), status, gateway_id
- **ConsentEvent** — user_id, consent_type, action, timestamp, ip_hash, policy_version (PDPA audit)
- **Notification** — user_id, type, payload, read_at

### 6.2 OpenFGA model (sketch)

```
type platform
  relations
    define admin: [user]

type program
  relations
    define parent: [platform]
    define admin: [user] or admin from parent

type course
  relations
    define parent: [program]
    define instructor: [user] or admin from parent
    define ta: [user]
    define learner: [user]

type cohort
  relations
    define program: [program]
    define instructor: [user] or instructor from program
    define learner: [user]
```

The `from` keyword inherits up the hierarchy. `instructor of a course` AND `learner of a different course` is a natural fit — just don't write the inheritance tuple at program level.

### 6.3 Migration phases (additive, no redesign)

| Phase | Roles added | Permissions added | Schema change? |
|---|---|---|---|
| **MVP (Sep 2026)** | Learner, Instructor, Admin | ~15 base perms (course content, roster, grading, announce, analytics) | Initial schema |
| **Phase 2 (Q1 2027)** | TA, Creator (internal pilot) | TA = subset of Instructor; Creator = `content:listing:publish` (platform scope) | New rows in Role + RolePermission tables |
| **Phase 3 (Q2 2027)** | Employer/Partner | `program:roster:view` (aggregate, PDPA-gated), `program:certificate:verify` | None (scope_type=program already exists) |
| **Phase 4 (2027-2028)** | Marketplace launch — public Creators | Creator self-service, content listing review workflow | New `marketplace_listing` type in OpenFGA; subscribe new service to existing domain events |

Every phase = new tuples + new event subscribers. Zero application code changes because all checks go through `can(user, permission, scope_type, scope_id)`.

---

## 7. Cohort Management UX (the differentiator)

SchoolHub admin (ref 4) provides **zero leverage** here — it has no cohort concept, treating students as individuals attached to a single classroom. NICHE's cohort-first model requires net-new design. Reference points for adoption: Maven admin dashboard (six enrollment states) + EducateMe Kanban assignment tracker + Reforge cohort dashboard.

**Cohort lifecycle states:**

```
planning → open (accepting applications) → running → completed → archived
```

**Cohort detail page structure (already specified in §4.3):**

1. Header card (name, program, dates, enrollment, capacity, status)
2. Roster (table + filters + bulk actions)
3. Analytics (completion curve, at-risk learners, NPS if collected)
4. Communications (bulk announce + segmented broadcasts)
5. Schedule (sessions, attendance overlay)
6. Bulk actions (move dates, export, etc.)

**At-risk detection logic (NICHE-specific, not in any reference):**

A learner is at-risk if any 2 of:
- > 7 days since last login during active cohort weeks
- Has 2+ overdue assignment submissions
- Lesson completion < 60% of cohort median for current week

Surface at-risk learners on instructor dashboard with quick-action: "schedule 1-on-1" button.

---

## 8. PDPA Compliance Strategy

Thai PDPA (effective June 2022; punitive enforcement August 2025 — first THB 21.5M fine issued) is non-optional.

### 8.1 Architectural decisions for PDPA

| Requirement | Implementation |
|---|---|
| Data residency | Supabase Singapore region for all PII; Cloudflare R2 with `auto` region (which uses APAC PoPs); avoid US-only services for PII storage |
| Cross-border transfer (PDPA §28-29) | If using Disco (US-hosted): explicit consent at signup with cross-border transfer disclosure; document lawful basis (contractual necessity); appoint DPO contact |
| Granular opt-in consent | 4+ separate consent toggles at signup: (1) account creation, (2) cohort progress tracking & instructor visibility, (3) cohort-aggregated analytics, (4) Career System data → employer access (deferred to post-MVP) |
| Auditable consent log | `ConsentEvent` table — every grant/withdrawal with timestamp, ip_hash, policy_version |
| Right to access | One-click "Export my data" → JSON dump of all user records |
| Right to erasure | Soft-delete: anonymize PII fields (name → "Former Learner", email → null, avatar removed); retain aggregate stats with anonymous token |
| Right to portability | Structured JSON (JSON Resume + portfolio + completion records + certificates) |
| 72h breach notification | Incident response runbook (in `design/runbooks/breach-response.md` post-MVP); log all data access events |
| Children's data | Not collected (NICHE adult learners only) — confirm at signup |

### 8.2 Analytics gate

- **Public dashboards** (Admin views) — aggregate-only; no PII in the analytics layer; join only on anonymized `learner_token`
- **Personal data** stays in primary DB (Supabase Postgres SG)
- **Third-party pixels** — DO NOT use without explicit consent + signed Data Processing Agreement
- **Mixpanel / Amplitude / GA** — defer entirely if possible; if needed, route through Plausible (EU, no cookies, no PII) or self-host PostHog

### 8.3 Disco-specific PDPA handling (Hybrid path)

If using Disco for Year 1:
- Consent flow at signup explicitly states: "Your learning data (progress, assignments, discussion posts) will be processed by Disco Inc. (United States) to deliver the Learning System. By continuing, you consent to this cross-border transfer." [Reject] / [Accept and continue].
- Annual privacy notice review and update.
- Plan for Disco data extraction at exit ramp time (Disco supports CSV export + API).

---

## 9. UI Design — Mapping to NICHE Brand

The NICHE brand book is in production (`brand-book/index.html` and 20 sections). The platform UI uses the same design tokens directly.

### 9.1 Token reuse (already defined in `brand-book/css/tokens.css`)

- **Color** — same 5 brand colors + green tints + WCAG-audited usage rules. Dark-mode tokens to be defined in brand book §5.5; platform should default to dark-mode (matches PDF mockups)
- **Type** — Fraunces (display) + Bai Jamjuree (body, Thai+Latin) — same files, same scale
- **Motion** — same 5 IBM Carbon-style tokens
- **Spacing** — base-8 scale already in tokens.css

### 9.2 Component library

For dev velocity, build on **shadcn/ui** (copy-paste components, owned by your repo, customizable). Adapt to NICHE tokens via the existing `tokens.css` patterns.

For Figma → code workflow: once Figma design system is built (post-launch task), use the newly installed Figma plugin's `figma-implement-design` skill to translate frames into shadcn/ui-themed components. Avoid premature lock-in to any UI library NICHE doesn't control.

### 9.3 Voice in UX copy

Per brand book §7 (4 voice principles):

| Do | Don't |
|---|---|
| "Submit your week 3 work" | "Please submit your assignment for week 3" |
| "You're 2 sessions behind. Your mentor will reach out." | "Warning: insufficient progress detected" |
| "Find your niche" (header on application page) | "Apply now to unlock your potential" |
| Empty state: "No work submitted yet. Start with the brief." | Empty state: "It looks like you haven't submitted anything yet" |

The platform copy should sound the same as the brand book — declarative, short, sides with the learner.

### 9.4 Patterns adopted from Figma references (sourced even when files were gated)

| Pattern | Source ref | Apply to |
|---|---|---|
| Three-column dashboard (sidebar + content + activity) | Ref 1 (Online Learning Profile) | Learner home |
| "Continue where you left off" hero card | Ref 1 | Learner home |
| 4-up KPI tile strip | Ref 2 (LMS Course Dashboard) + Ref 4 (SchoolHub) | Instructor + Admin dashboards |
| Sidebar IA with grouped primary nouns | Ref 4 (SchoolHub) | All 3 portals |
| List + detail + add trio per entity | Ref 4 | Admin user/program/cohort |
| Hero split layout + dual CTA | Ref 3 (Education Landing) | Public marketing site |
| FAQ accordion + closing CTA banner | Ref 3 | Public marketing site |
| Stat counter row | Ref 3 | Public marketing ("3 pillars · 12 programs · 1 cohort/year") |
| Calendar/event detail page | Ref 4 | Schedule (onsite + online sessions) |

### 9.5 Patterns rejected from references

| Anti-pattern | Source | Why reject |
|---|---|---|
| "Subjects" K-12 vocabulary | Ref 4 | NICHE has Programs + Courses |
| Parent/guardian fields on learner record | Ref 4 | Adult learners only |
| Multi-semester / academic-year switcher | Ref 4 | Continuous cohorts, not semesters |
| Letter grades / GPA | Ref 4 | Non-credit creative ed; portfolio-based assessment |
| Marketplace browse 1000 courses grid | Refs 1, 2, 3 | NICHE is curated institute |
| Self-paced absolute % progress bar | Refs 1, 2 | Cohort = relative to schedule |
| Star ratings on courses | Ref 3 | Marketplace pattern |
| "Unlock your potential" / generic edtech copy | Ref 3 | Brand book §7 voice principles forbid |
| Mint-green + purple gradient buttons | Ref 3 | Brand palette is dark + cream + red + moss green |
| Counters of fake-large numbers | Ref 3 | NICHE leans into scarcity ("11 seats remaining") |
| Stocky multi-ethnic student photo collages | Ref 3 | Photography direction (brand book §5) is hands working, candid |

---

## 10. Five-Month MVP Roadmap (overview — see MVP_ROADMAP.md for week-by-week)

### Phase 0 (May 2026 — current month, before dev kickoff)

- Build vs Buy decision committed by NICHE leadership
- Disco contract signed (if Hybrid path)
- Tech consultant team selected; retainer Model B vs C decided
- Pedagogical model frozen (program structure, assessment criteria, cohort ops)

### Phase 1 (June 2026 — foundation)

- Repo + infra setup (Next.js + Supabase + Clerk + Railway)
- OpenFGA model for the 3 MVP roles
- Brand design tokens imported from `brand-book/css/tokens.css`
- shadcn/ui themed to NICHE tokens
- Auth flow (signup, login, MFA, role-based redirect)
- User + Program + Cohort + Course schemas + admin CRUD
- Disco workspace provisioned and configured (if Hybrid)

### Phase 2 (July 2026 — Student Portal)

- Public marketing site (landing, programs grid, program detail, FAQ, apply)
- Application flow + payment (Stripe Thai THB)
- Admin: enrollment management (manual + invite link)
- Admin: cohort dashboard (roster + bulk actions)
- Learner: dashboard wrapper + profile

### Phase 3 (August 2026 — Learning System integration + Career stub)

- If Hybrid: Disco SSO with Clerk; Disco cohort provisioning automation; embedded learner experience
- If Custom: course/module/session content authoring; assignment submission; instructor grading queue
- Career System stub: portfolio links page + manual PDF certificates + verification page
- Schedule (onsite + online overlay)
- Announcements (Admin → cohort)

### Phase 4 (September 2026 — polish + soft launch)

- Notifications (email + in-app)
- Mobile-responsive QA across all critical flows
- PDPA: consent flows + audit logging + privacy notice page
- Analytics dashboard (basic — Admin only)
- Soft Launch with cohort 1 (target: ~30 learners)

### Phase 5 (post-launch, Q4 2026 → Q1 2027)

- Tech Manager hired
- Career System full features (auto-aggregate portfolio, JSON Resume builder, OB 2.0 issuer)
- Disco exit ramp planning (if Hybrid path proves Disco doesn't fit Year 2 needs)
- TA + Creator roles (internal pilot)

---

## 11. Open Questions Answered (PDF §7)

The PDF asks the dev team 9 questions across §7.1–7.3. Direct answers:

### §7.1 Platform direction

> *จาก requirements นี้ ทางทีมแนะนำไปทาง custom build หรือใช้ open-source LMS แล้วปรับต่อ?*

**Hybrid.** Disco for Learning System + community + cohort orchestration; custom Next.js for Student Portal + Career System stub. Reasoning in §2.4. Open-source LMS (Moodle, Open edX) is wrong fit — too universities-shaped, too DevOps-heavy for 5-month timeline at <100-user scale.

> *MVP ที่วางไว้สามารถทำได้มั้ย หรือมีอะไรที่ควรเลื่อนไปทำทีหลัง?*

**Yes, with hybrid path. No, with full custom in 5 months without scope cut.** §2.5 lists the cuts. Most consequential cut: full Career System → ship as Notion stub, build properly in Year 2.

> *ทางทีมแนะนำ tech stack / infrastructure แบบไหน?*

§3 stack table. Stack chosen specifically for: (a) future Tech Manager hireability, (b) Thai dev market familiarity, (c) cost predictability at <500 users, (d) PDPA-friendly residency.

### §7.2 Capability + collaboration model

> *ตอนนี้ทีมมี bandwidth พอจะรับโปรเจกต์นี้ควบคู่กับงานอื่นไหม?*

Cannot answer — depends on the specific dev team. The minimum viable team is **1 senior + 2 mid-level developers** dedicated. Anything less = scope further reduced or timeline pushed.

> *prefer แบบดูแลต่อหลัง launch (retainer) หรือทำเป็นโปรเจกต์จบแล้วส่งมอบ?*

Strongly recommend **retainer (Model B or C from PDF §6.1)**. Edtech platform requires continuous tuning — first cohort feedback cascades into UI changes, instructor workflow improvements, edge cases. Project-handover (Model A) at this risk level + this small a team = handover failure within 6 months.

> *ถ้าเป็น Model B (TM + retainer): ปกติ retainer ของทีม cover อะไรบ้าง?*

Standard retainer for a Next.js platform of this scope: bug fixes (P1 within 24h, P2 within 5d), small feature additions (≤1 week of work each), monthly stack updates (Next.js patch versions, dependency security), monthly performance review. SLA: 99% uptime during class hours (8am-10pm Bangkok). Cost: typical Thai dev retainer for this scope = THB 80,000–150,000/month at 20 hours/month minimum. Larger features = T&M outside retainer.

> *ถ้าเป็น Model C (long-term partner): ทีมมองว่าแบ่ง role ระหว่าง TM กับทีมยังไงถึงจะ work ดีสุด?*

TM owns: product decisions, content/curriculum updates, learner support, Disco/admin operations, requirements definition. Dev team owns: code, infrastructure, deployments, security, third-party integrations. **Don't split roles by codebase area — split by decision authority.**

### §7.3 Handover and continuity

> *ถ้ามี TM เข้ามาทีหลัง ทีมจะเตรียม documentation และ onboarding ยังไงบ้าง?*

Recommended deliverables:
- `README.md` — quick start (clone, env, run)
- `docs/architecture.md` — high-level diagram + data flow
- `docs/runbooks/` — deployment, breach response, restoring from backup, adding a cohort, issuing a certificate
- `docs/data-model.md` — schema reference + permission matrix
- `docs/onboarding-tm.md` — the 5-day onboarding plan for incoming TM
- All inline JSDoc + tRPC procedure docs

> *จากสิ่งที่จะ build + model ที่เลือก ทีมคิดว่า TM ควรมี skill ด้าน tech ระดับไหนถึงจะดูแลต่อได้?*

For the recommended stack: TM = TypeScript intermediate + SQL basics + Git + Railway dashboard. Does NOT need: DevOps, Kubernetes, AWS IAM, Ruby/Python, PHP. Most "PM with light coding" candidates from the Thai market will fit.

> *หลัง launch แล้ว ถ้ามี feature ใหม่ / bug / improvement ปกติ workflow ของทีมเป็นยังไง?*

GitHub Issues for bugs (TM creates → dev triages → P1/P2/P3 → SLA tracked). Linear or Notion for feature requests (TM curates roadmap → dev estimates → quarterly planning). Direct dev access only for critical incidents. Weekly 30-min sync.

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Pedagogical model changes during build** | High | Critical | Freeze pedagogical model by June 2026 before dev kickoff. Lock the program structure, cohort ops, assessment criteria. Any changes = explicit scope decision with timeline impact. |
| **Disco PDPA cross-border issue** | Medium | Medium | Explicit consent flow at signup; legal review of Standard Contractual Clauses with Disco; <100-user surface area limits exposure |
| **5-month timeline too tight** | High | Critical | Hybrid path is the primary mitigation. If chosen, scope is achievable. If full custom, must add 1-2 months OR reduce MVP to "Learning System only, ship Student Portal + Career in Q4 2026." |
| **Tech Manager hire delayed past launch** | Medium | High | Dev team retainer (Model B or C) ensures continuity even without TM in place. TM hire becomes Q4 priority not Q3. |
| **Cohort 1 has < 30 learners** | Medium | Low | Architecture is over-built for <100 anyway; smaller cohort means less stress on infra and more attention per learner. Treat as feature. |
| **Brand book changes after platform shipped** | Low | Medium | Token-based design system means brand changes propagate via single token file update. Components reference tokens, not hex values. |
| **Disco shuts down or pivots** | Low | High | Exit ramp documented (CSV + API export); custom path is the documented Year 2 plan anyway. |
| **PDPA enforcement raid / fine** | Low | Critical | Compliance baked in (consent log, residency, audit trail); maintain DPO contact; annual privacy review |
| **Career System stub feels low-effort to learners** | Medium | Medium | Frame the stub as "Career Portal v1 — full launch Q4 2026"; commit roadmap publicly. Manual cert issuance for Cohort 1 = high-touch, high-quality (a feature, not a bug). |
| **Multi-role complexity confuses learners** | Low | Low | MVP only exposes single roles per user (Learner OR Instructor OR Admin); multi-role activated post-MVP for Creator/TA/Alumni cases. |

---

## 13. What Next — Suggested Actions

For NICHE leadership (sequenced):

1. **Read this doc + DATA_MODEL.md + MVP_ROADMAP.md** with NICHE leadership team. (Allow 2-3 days for review.)
2. **Decision meeting on Build vs Buy** (§2.5 — A/B/C). Commit in writing.
3. **If Hybrid (recommended):**
   - Sign Disco Org tier contract
   - Brief Tech consultant team that Hybrid is the path
4. **Freeze pedagogical model** — program structure, assessment, cohort ops, instructor workflow. Document in a separate `pedagogy.md`.
5. **Run trademark search** (Thailand DIP + USPTO TESS + EUIPO) on NICHE wordmark + N. submark before launch (per brand book §12).
6. **Sign Tech retainer agreement** (Model B or C from PDF §6.1).
7. **Duplicate the 4 Figma reference files** into a NICHE Figma workspace so the dev team can run Figma MCP `get_design_context` directly when they need component-level extraction. (Currently MCP can't read community files anonymously.)
8. **Commission Figma source of truth** — design system file + key screens for the 6 priority sidebar sections per role. Run `figma-generate-library` skill against `brand-book/css/tokens.css`.
9. **Start dev kickoff Phase 1** (June 2026) per MVP_ROADMAP.md.

---

## 14. Sources

### Cohort-based learning + Build vs Buy
- [6 Best Cohort-Based Learning Platforms 2026 — Educate-Me](https://www.educate-me.co/blog/best-cohort-based-learning-platforms)
- [L&D Trends 2026: AI Integration, Capability Building, Cohort Learning — CLO100](https://clo100.com/2025/12/23/ld-trends-2026-ai-integration-capability-building-and-cohort-learning/)
- [What Is Cohort-Based Learning — Disco](https://www.disco.co/cohort-based-learning)
- [6 Best Cohort-Based Learning Platforms for 2026 — Disco](https://www.disco.co/blog/best-cohort-based-learning-platforms-2026)
- [Disco Pricing](https://www.disco.co/pricing)
- [Maven Reviews 2026 — SourceForge](https://sourceforge.net/software/product/Maven/)
- [Custom LMS Development: Build vs Buy Decision Framework 2026](https://www.ofashandfire.com/blog/custom-lms-development-build-vs-buy)
- [Open Source LMS Comparison 2026 — Selleo](https://selleo.com/blog/open-source-lms-comparison)

### Tech stack
- [Drizzle vs Prisma ORM in 2026 — MakerKit](https://makerkit.dev/blog/tutorials/drizzle-vs-prisma)
- [Better Auth vs Clerk vs NextAuth 2026 SaaS Showdown — StarterPick](https://starterpick.com/blog/better-auth-clerk-nextauth-saas-showdown-2026)
- [Video Streaming Pricing Comparison April 2026 — BuildMVPFast](https://www.buildmvpfast.com/api-costs/video)
- [Cloudflare Stream Pricing](https://developers.cloudflare.com/stream/pricing/)
- [Mux vs Cloudflare Stream](https://www.mux.com/compare/cloudflare-stream)
- [Resend vs Postmark 2026 — Nuntly](https://nuntly.com/versus/resend-vs-postmark)
- [Railway vs Vercel — LazyAdmin](https://lazyadmin.nl/it/railway-vs-vercel-choosing-the-right-hosting-for-your-app/)
- [Supabase vs Railway 2026 — BuildMVPFast](https://www.buildmvpfast.com/compare/supabase-vs-railway)
- [Vercel vs Supabase 2026 — UI Bakery](https://uibakery.io/blog/vercel-vs-supabase)
- [Next.js + Prisma + Postgres guide — Vercel KB](https://vercel.com/kb/guide/nextjs-prisma-postgres)

### RBAC + multi-role
- [RBAC vs ABAC and ReBAC — Permit.io](https://www.permit.io/blog/rbac-vs-abac-and-rebac-choosing-the-right-authorization-model)
- [OpenFGA](https://openfga.dev/)
- [OpenFGA Modeling Roles and Permissions](https://openfga.dev/docs/modeling/roles-and-permissions)
- [OpenFGA Organization Context Authorization](https://openfga.dev/docs/modeling/organization-context-authorization)
- [OpenFGA Sample Stores](https://github.com/openfga/sample-stores)
- [Permify vs OpenFGA](https://permify.co/permify-openfga/)
- [Multi-Role UX: The 2026 Guide — CreateBytes](https://createbytes.com/insights/designing-ux-for-multi-role-platforms)
- [Top RBAC Providers for Multi-Tenant SaaS 2025 — WorkOS](https://workos.com/blog/top-rbac-providers-for-multi-tenant-saas-2025)

### Career System + portfolios
- [Le Wagon Career Services](https://www.lewagon.com/career-services)
- [Le Wagon Hiring Portal](https://www.lewagon.com/hirings)
- [Le Wagon Jobs Report (Dec 2024)](https://www.lewagon.com/jobs-report)
- [Holberton School Checker](https://blog.holbertonschool.com/introducing-holberton-1-checker-you/)
- [BloomTech Outcomes](https://www.bloomtech.com/outcomes)
- [JSON Resume](https://jsonresume.org/)
- [Reactive Resume](https://rxresu.me/) · [GitHub](https://github.com/amruthpillai/reactive-resume)
- [Open Badges 3.0 Status in 2026 — VirtualBadge](https://www.virtualbadge.io/blog-articles/open-badges-3-0-what-is-the-status-in-2026)
- [1EdTech Open Badges 3.0 announcement](https://www.1edtech.org/1edtech-article/new-open-badges-30-standard-provides-enhanced-security-and-mobility/411060)
- [Accredible OB3 launch (Jan 2026)](https://www.accredible.com/blog/now-supporting-open-badge-3-0-and-w3c-verifiable-credentials)
- [Codebasics Learner Portfolios](https://codebasics.io/portfolio)

### PDPA + privacy
- [Thailand PDPA 2026 Guide — Cookie Information](https://cookieinformation.com/blog/what-is-the-thailand-pdpa/)
- [Thai PDPA Ultimate Guide — OneTrust](https://www.onetrust.com/blog/the-ultimate-guide-to-thai-pdpa-compliance/)
- [Thailand PDPA — Securiti](https://securiti.ai/thailand-personal-data-protection-act-pdpa/)
- [Thailand PDPA Compliance — BigID](https://bigid.com/blog/thailand-pdpa-compliance/)
- [Thailand PDPA Data Privacy Law 2025 — Themis Partner](https://thailand.themispartner.com/guides/thailand-pdpa-data-privacy-law-2025-guide/)
- [EdTech SaaS GDPR + student privacy](https://complydog.com/blog/edtech-saas-compliance-student-privacy-gdpr-implementation)

### Cohort UX + admin
- [Student Management — Maven Admin Dashboard](https://help.maven.com/en/articles/6069488-student-management-in-the-maven-admin-dashboard)
- [7 Best Cohort Program Software 2026 — Disco](https://www.disco.co/blog/best-cohort-program-software-2026)
- [Maven Alternatives 2026 — Disco](https://www.disco.co/blog/maven-alternatives-elevate-learning-programs-2026)

### Figma references (from `requirements/ref.md` — community files; require workspace duplication for direct MCP read)
- [Dashboard - Online Learning Profile (file 1313209648458042020)](https://www.figma.com/community/file/1313209648458042020/dashboard-online-learning-profile)
- [LMS and Course Dashboard Design (file 1319524540637048768)](https://www.figma.com/community/file/1319524540637048768/lms-and-course-dashboard-design)
- [Online Education Website Landing Page (file 1428384686040444933)](https://www.figma.com/community/file/1428384686040444933/online-education-website-landing-page-ui-design)
- [SchoolHub School Management Admin (file 1381931496411280342)](https://www.figma.com/community/file/1381931496411280342/schoolhub-school-management-admin-dashboard-template)

### Recommended additional Figma references (not in original ref.md)
- [CourseFlow UI Kit](https://www.figma.com/community/file/1505496020038538472/courseflow-ui-kit-elearning-web-app-ui-kit-for-figma-preview) — 35+ desktop screens incl. instructor pages
- [Dreams LMS](https://www.figma.com/community/file/1542911527930004020/dreams-lms-free-figma-ui-kit-for-learning-management-systems) — instructor modules + cohort screens
- [Designo Streamlined LMS Dashboards](https://www.figma.com/community/file/1395793003651190548/designo-streamlined-lms-dashboards)
