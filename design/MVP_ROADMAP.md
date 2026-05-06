# NICHE Platform — 5-Month MVP Roadmap

> **Companion to:** [PLATFORM_DESIGN.md](./PLATFORM_DESIGN.md) · [DATA_MODEL.md](./DATA_MODEL.md)
> **Audience:** dev team + NICHE leadership for sprint planning + risk tracking
> **Soft Launch target:** September 2026
> **Path assumed:** Hybrid (Disco + custom Next.js Student Portal + Career stub)
> **Status:** v1.0 — pre-kickoff plan; needs dev team estimation + commitment

This document breaks the 5-month build into 5 monthly phases × ~4 weeks each. Each week has explicit deliverables, owner, and acceptance criteria. The plan assumes a team of **1 senior full-stack lead + 2 mid-level developers + 1 part-time designer** (or shadcn/ui replacing dedicated design work for non-marketing surfaces).

If team is smaller or hybrid path isn't chosen, scope must be cut further (see PLATFORM_DESIGN.md §2.5 + §12).

---

## Pre-flight (May 2026 — current month)

These must complete before June 1, 2026 dev kickoff. **Without them, the timeline does not work.**

| Action | Owner | Deadline |
|---|---|---|
| Build vs Buy committed (Hybrid / Custom / Pure-Disco) | NICHE leadership | May 15 |
| Pedagogical model frozen — program structure, assessment criteria, cohort ops, instructor workflow, application flow | NICHE leadership + lead instructor | May 20 |
| Disco Org-tier contract signed (if Hybrid) | NICHE ops | May 25 |
| Dev team retainer signed (Model B or C from PDF §6.1) | NICHE ops | May 25 |
| Brand book v1 frozen (typography licensed, logo OPT 02 approved, color rules locked) | NICHE designer | May 30 |
| Figma source-of-truth file scaffolded (variables, type styles, basic logo components) | NICHE designer | May 30 |
| Trademark preliminary search filed (USPTO TESS + EUIPO eSearch + Thailand DIP) on NICHE wordmark + N. submark | NICHE legal | May 30 |
| PDPA legal review of Disco cross-border transfer | NICHE legal | May 30 |
| Repository created on GitHub Org (or GitLab); CI minimum (lint + typecheck + test) configured | Senior dev | May 30 |
| Supabase project provisioned in `ap-southeast-1` Singapore region | Senior dev | May 30 |
| Clerk production app provisioned + Google OAuth + Thai SMS OTP enabled | Senior dev | May 30 |
| OpenFGA local Docker setup; model from DATA_MODEL.md §3 deployed | Senior dev | May 30 |

---

## Phase 1 — June 2026 — Foundation

**Goal:** Working app shell with auth, role-based routing, and admin CRUD for the core entities. Disco workspace configured (if Hybrid).

### Week 1 (Jun 1-7)

- Repo bootstrapped: Next.js 15 App Router, TypeScript strict, ESLint + Prettier + Husky pre-commit
- shadcn/ui installed; tokens.css from `brand-book/css/tokens.css` ported into `app/globals.css`
- Drizzle setup; first migration (users, programs, cohorts, courses tables)
- tRPC scaffolded with first 3 procedures (`auth.me`, `program.list`, `cohort.list`)
- Clerk integrated — signup + login + email verification + Google OAuth
- OpenFGA local instance + first tuples (platform admin role granted to NICHE staff seed users)
- Deploy to Railway Singapore — public URL working

**Deliverable:** sign in, see "Hello {your name}" page. Admin can sign in and see empty admin dashboard placeholder.

### Week 2 (Jun 8-14)

- Layout shells: marketing layout (no sidebar) + app layout (sidebar + topbar + content)
- Sidebar with role-aware items via `auth.me` (different items for Learner / Instructor / Admin)
- Admin: User list view + detail page + role assignment UI (modal: pick user → pick role → pick scope)
- `can()` abstraction implemented; one example permission check wired (`platform:user:manage`)
- Brand fonts loaded (Fraunces + Bai Jamjuree from Google Fonts)
- Reading progress component, dark/light mode toggle (default: dark, matching PDF mockups)

**Deliverable:** Admin can grant/revoke roles. Permission checks gating admin pages.

### Week 3 (Jun 15-21)

- Admin: Program list / detail / create form (12 programs seeded)
- Admin: Cohort list / detail / create form with status lifecycle (planning → open → running → completed)
- Admin: Course list within program / detail / create form
- Admin: Module list within course / detail / create form
- Domain event scaffolding (BullMQ on Railway, first event subscriber: audit log writer)

**Deliverable:** All MVP entities have admin CRUD. Audit log captures every mutation.

### Week 4 (Jun 22-28)

- Disco workspace branded with NICHE logo + colors (if Hybrid path); single test cohort created in Disco
- Disco SSO with Clerk (custom OIDC provider config)
- Webhook from Disco → NICHE Postgres for cohort events (enrollment, submission, completion)
- Marketing layout: hero shell + 12-program grid + program detail page (static, copy from PDF later)
- PDPA: privacy policy page + cookie banner + initial 4 consent toggles

**Deliverable:** Disco-NICHE bridge functional. Marketing layout can render any program. Consent capture works.

**Phase 1 milestone:** Admin can configure platform end-to-end. Empty cohort, empty roster, but the structure is real.

---

## Phase 2 — July 2026 — Student Portal + Application

**Goal:** Learners can apply to a cohort, pay, and see their dashboard. Public marketing site complete.

### Week 5 (Jun 29-Jul 5)

- Public marketing site full build:
  - Hero with NICHE voice ("Find your niche", provocative inversion of generic edtech)
  - 3-pillar segmented control filtering 12-program grid
  - Program detail with cohort dates + apply CTA + outcomes
  - About / Faculty / FAQ pages
- SEO: sitemap, robots, OG images, structured data
- Mobile-responsive across all marketing pages

**Deliverable:** Marketing site live on niche.com. Apply CTA links to application flow.

### Week 6 (Jul 6-12)

- Application flow (multi-step): personal info → program selection → cohort selection → essay/portfolio link → payment
- Enrollment status lifecycle: applied → accepted (admin action) → enrolled (payment confirmed)
- Stripe integration in Thai THB; webhooks for payment status
- Admin: Enrollment management — applications queue, accept/decline, send invite
- Email templates (Resend + React Email): application received, accepted, payment confirmation, welcome

**Deliverable:** Full application + payment flow. Admin can move applicants through pipeline.

### Week 7 (Jul 13-19)

- Learner dashboard: hero "what's next" card + cohort schedule strip + announcements + progress
- Cohort detail page (learner view): roster (avatars only — privacy-respectful), schedule, announcements
- Profile + Settings: edit name/avatar/locale, manage consent toggles, view payment history
- Public credential verification page (`/verify/{id}`) — empty state until certificates issued

**Deliverable:** Onboarded learners can sign in and see their cohort. Profile editable.

### Week 8 (Jul 20-26)

- Invite link generator (cohort-scoped, expiry, single-use vs reusable, link analytics)
- Bulk CSV enrollment import: upload → preview → validate → confirm
- Admin Cohort dashboard: roster table with progress %, attendance, last active, at-risk flag, bulk actions toolbar
- At-risk detection logic: > 7 days no login + 2 overdue submissions + < 60% lesson completion
- Notifications system v1 (in-app bell + email) for: enrollment status change, payment success, announcement

**Deliverable:** Admin can manage a cohort end-to-end. Learners receive notifications. At-risk surfaces.

**Phase 2 milestone:** End-to-end happy path from "see ad → apply → enroll → see dashboard" works. Admin can run a cohort.

---

## Phase 3 — August 2026 — Learning System Integration + Career stub

**Goal:** Curriculum content delivery + assignments + grading + announcements. Career System stub functional.

### Week 9 (Jul 27-Aug 2)

- **If Hybrid:** Embed Disco learner experience inside NICHE shell (via iframe or deep link). NICHE handles application + payment + Career; Disco handles curriculum, live sessions, community.
- **If Custom:** Course / Module / Session content authoring (instructor-side). Rich text editor + video URL + resource attachments.
- Schedule view (learner): week + month calendar showing onsite + online sessions + assignment deadlines
- Schedule overlay: cohort sessions auto-injected from Disco webhook (Hybrid) or session schema (Custom)

**Deliverable:** Learners see their schedule. Instructors can create content (Custom) or use Disco (Hybrid).

### Week 10 (Aug 3-9)

- Assignments: brief, deadline, max score, optional rubric (Custom only — Hybrid uses Disco assignments)
- Submissions: file upload to R2 + text content; status flow (draft → submitted → graded → returned/needs_1on1)
- Instructor grading queue: filterable list (pending / late / graded), grade with rubric + feedback text
- Submission versioning (resubmissions create new version, not overwrite)

**Deliverable:** Full assignment loop. Or in Hybrid, this lives in Disco; NICHE displays summary.

### Week 11 (Aug 10-16)

- Announcement composer: markdown editor + audience targeting (whole cohort / segment / individual) + scheduled send
- Announcements feed: per-cohort + per-program + platform; unread badge
- Notifications: new feedback on submission, assignment due in 24h, announcement published, schedule change
- Analytics dashboard v1: KPI tiles (cohort fill, MRR, active learners, completion %), cohort completion curve, at-risk list

**Deliverable:** Communication channel between admin/instructor and cohort. Live KPIs.

### Week 12 (Aug 17-23)

- Career System stub:
  - Portfolio links page: learner adds external links manually (Notion, Behance, GitHub, etc.) + thumbnails + descriptions
  - Resume builder template: 2 templates (clean + creative); JSON Resume schema; PDF via @react-pdf/renderer + Sarabun font
  - Public portfolio URL `/u/{username}` showing curated links
  - Certificate generator (manual trigger by Admin): styled PDF with QR + Open Badges 2.0 assertion JSON; verification page at `/verify/{id}`
- Schedule onsite check-in: instructors mark attendance via session detail page (mobile-friendly)

**Deliverable:** Learners have a portfolio + resume + certificate path. Manual cert issuance for cohort 1 is acceptable.

**Phase 3 milestone:** All MVP features functional end-to-end. Cohort 1 could theoretically launch.

---

## Phase 4 — September 2026 — Polish + Soft Launch

**Goal:** Bugs squashed, performance acceptable, mobile-responsive complete, PDPA compliance audited, soft launch with cohort 1.

### Week 13 (Aug 24-30)

- Mobile responsive QA across all critical flows (landing, application, dashboard, cohort, schedule, profile)
- Sidebar collapses to bottom tab bar at < 768px (5 items max)
- Right rail (calendar/notifications) collapses to swipe-up sheet
- Loading states + skeleton screens
- Error boundaries + 404 + 500 pages with NICHE voice

**Deliverable:** Phone-friendly experience. No catastrophic mobile bugs.

### Week 14 (Aug 31-Sep 6)

- PDPA audit: consent flow review, audit log review, data export endpoint test, soft-delete + anonymize end-to-end test
- Privacy policy page + cookie banner final copy reviewed by legal
- Security audit: OWASP Top 10 checks, OpenFGA model review against principle of least privilege, secrets rotation
- Backup verification: trigger restore-from-backup drill on staging
- Performance: Lighthouse > 90 on dashboard + landing; Core Web Vitals green

**Deliverable:** PDPA-compliant. Production-secure. Performant.

### Week 15 (Sep 7-13)

- Admin training: walkthrough sessions for NICHE staff (cohort management, enrollment, announcements, payments, analytics)
- Instructor onboarding: video walkthrough + cheat sheet (grading queue, content authoring or Disco walkthrough, announcement composer)
- Beta cohort: 5-10 friendly users dry-run the full flow (apply → enroll → first week sessions)
- Bug triage based on dry-run feedback; prioritized fixes

**Deliverable:** NICHE staff can operate the platform without dev hand-holding.

### Week 16 (Sep 14-20) — Soft Launch Window

- Cohort 1 enrollment opens publicly
- 24/7 monitoring for first week (Uptime Robot + Sentry + on-call rotation)
- Daily standups dev-NICHE for first 2 weeks
- Hot-fix lane: fix-deploy in < 4 hours for any P1 issue
- Announcement to NICHE community / IG / partners

**Deliverable:** First real cohort enrolled. Platform stable in production.

---

## Phase 5 — Q4 2026 → Q1 2027 — Stabilization + Career System Full Build

After soft launch, the focus shifts from net-new features to:

### Q4 2026 (Oct-Dec)

- **Career System full build:**
  - Auto-aggregate portfolio (every assignment becomes a portfolio record with curriculum-driven skill tags)
  - Skill tracking dashboard
  - Public profile employer-view (with explicit consent gate)
  - Open Badges 2.0 issuer in-house (replace manual cert issuance)
- **Cohort 2 onboarding** (likely Jan-Feb 2027 cohort)
- **Tech Manager hiring + onboarding** (5-day onboarding plan from PLATFORM_DESIGN.md §11)
- **Disco exit ramp planning** (if Hybrid path is being abandoned)
- **Bug + UX iteration** based on cohort 1 feedback
- **Analytics expansion** based on what NICHE leadership actually asks about

### Q1 2027 (Jan-Mar)

- **TA + Creator roles enabled** (internal pilot; 1-2 trusted external content partners as Creators)
- **Multi-role context switcher UI** (for Learner-alumni who become Creator)
- **Peer review workflow** (post-MVP, for upper-level Studio + Degree programs)
- **Native mobile app evaluation** (React Native? Capacitor? PWA-only?)
- **Thai localization full UI** (i18n strings already present from MVP; build language switcher)
- **Payment installments** (Thai market expectation for higher-priced Degree programs)

### Q2-Q3 2027

- **Employer Portal MVP** (curated directory + inquiry form, no employer login yet)
- **Employer login + talent search** (Phase 3 roles enabled; PDPA-gated)
- **Marketplace evaluation** (only after positioning vs anti-marketplace stance is reconciled with leadership)

---

## Risks tracked weekly

A standing weekly risk review (15 min) tracks:

| Risk | Trigger | Owner |
|---|---|---|
| Pedagogical model creep | Any change to program structure post-Jun-1 | NICHE leadership decision required |
| Velocity below plan | A weekly milestone slips by > 2 days | Dev team flag in weekly demo |
| Disco PDPA legal escalation | Any complaint from learner re: cross-border | Legal review |
| Payment gateway issue | Stripe webhook failures > 2/day | Senior dev + ops |
| Performance regression | Lighthouse < 80 or DB query > 1s p95 | Senior dev |
| Hire delay (TM) | Past Sep-30 with no candidate in pipeline | NICHE leadership |
| Brand inconsistency | UI deviating from brand book tokens | Designer audit + tokens.css enforcement |

---

## Acceptance criteria for "MVP done"

The platform is "MVP done" when **every item below is true**:

- [ ] Public marketing site live on niche.com with all 12 programs detailed
- [ ] Learner can: apply → pay → enroll → access curriculum → submit assignment → view feedback → receive certificate
- [ ] Instructor can: create content (or use Disco) → manage cohort roster → grade submissions → broadcast announcement → view cohort progress
- [ ] Admin can: manage users → manage programs/cohorts → process applications → manually issue certificates → view analytics
- [ ] PDPA: consent captured, audit log functional, data export endpoint tested, soft-delete + anonymize tested
- [ ] Mobile-responsive across all critical flows
- [ ] All emails (transactional + announcements) send and deliver
- [ ] Lighthouse > 90 on landing + dashboard
- [ ] Sentry + Uptime monitoring live with on-call rotation
- [ ] Backup + restore drill completed within last 30 days
- [ ] At-risk learner detection running daily; surfaces on instructor dashboard
- [ ] Career System stub: portfolio links + resume PDF + certificate + public verification page

If any item is incomplete by Sep 14, 2026, the soft launch slips by 1 week (max 2 weeks) — do not launch with broken core flows.

---

## What this plan deliberately does NOT include

The following were considered and DEFERRED. None are MVP. All are sketched in PLATFORM_DESIGN.md for future phases:

- Native iOS/Android apps (mobile-responsive web only at MVP)
- In-platform DMs / chat (use Discord/Line for cohort 1)
- Peer review workflows (defer to Q1 2027)
- AI features (resume suggestions, content recommendations, auto-tagging)
- Employer login / talent portal (defer to Q2-Q3 2027)
- Marketplace / Creator self-service publishing
- Open Badges 3.0 / W3C VC (OB 2.0 sufficient through 2026)
- LinkedIn sync
- Advanced reporting / data warehouse
- Multi-language full UI switcher (i18n strings ready, switcher post-launch)
- Payment installments (post-launch)
- Content version control (post-launch)
- Live session video hosting (use Zoom/Meet embed)
- Forum / peer discussion (use Discord for cohort 1; build later if needed)
- A/B testing / experiments framework
- Public API for third-party integrations
- Affiliate / referral program

Each of these adds 2-6 weeks of work. None is needed to launch cohort 1.
