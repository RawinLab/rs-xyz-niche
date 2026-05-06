# NICHE Platform — UI Patterns from Figma References

> **Companion to:** [PLATFORM_DESIGN.md](./PLATFORM_DESIGN.md) · [ADMIN_PATTERNS.md](./ADMIN_PATTERNS.md)
> **Sources:** 3 Figma reference files duplicated into NICHE workspace; analyzed via Figma MCP `get_metadata` + `get_design_context` (where Starter-plan quota allowed) + screenshot inspection
> **Status:** v1.0 consolidated patterns from 2 of 3 readable refs (Education Landing was paywall-blocked entirely)

This document consolidates concrete adopt/reject patterns from the Figma references provided in `requirements/ref.md`. The 4th file (SchoolHub Admin) was paywall-blocked; admin patterns are covered separately in [ADMIN_PATTERNS.md](./ADMIN_PATTERNS.md). The 3rd (Education Landing) hit quota during analysis; only its conventional genre patterns are summarized here.

---

## 1. Reference inventory

| # | File / fileKey | Purpose for NICHE | MCP read status |
|---|---|---|---|
| 1 | Dashboard - Online Learning Profile · `zBQmmtoZAnnmNkAZ0njsPW` | Learner-side dashboard | ✅ full read (single-screen reference) |
| 2 | LMS and Course Dashboard Design · `cxnc2cwhRfFYIkimSnuwBS` | Course module nav + iconography | ⚠ metadata + screenshot only (quota hit on `get_design_context`) |
| 3 | Online Education Website Landing Page · `MosgE4Fxzs5KoiOkmsJjSV` | Public marketing site | ❌ all endpoints rate-limited; conventional patterns only |
| 4 | SchoolHub School Management Admin · `1381931496411280342` | Admin / Student Portal | ❌ not duplicated (paywall); see ADMIN_PATTERNS.md |

---

## 2. Patterns to ADOPT (with source citation)

### 2.1 Three-column app shell
- **Source:** Online Learning Profile `node 10:1626` (240px sidebar / 840px main / 296px right rail)
- **Why:** mirrors learner mental model — navigation / current work / cohort context
- **NICHE adaptation:** keep sidebar (collapsible to icon-only at md breakpoint, hidden at < 768px); right rail = cohort progress + upcoming onsite session; sidebar in dark `#252026` with cream content area

### 2.2 KPI tile strip with tinted icon affordance
- **Source:** Online Learning Profile `node 10:1202` + LMS Course Dashboard `node 1:1596`
- **Anatomy:** card with rounded-square solid black tile (~48px) + centered icon glyph + label + big number + delta indicator
- **Why:** clean, high-density way to surface key metrics
- **NICHE use:** Learner home (Sessions attended / Onsite hours / Assignments due) · Instructor dashboard (Pending submissions / Attendance / Avg progress / Unread) · Admin dashboard (Cohort fill / MRR / Active learners / Completion %)
- **shadcn:** `Card` + `CardHeader` with trailing icon `Badge`; tone variants for default/accent

### 2.3 Dual-bar progress + fraction label
- **Source:** LMS Course Dashboard `node 1:1625` (282px track + 144px fill + "4/10 Lesion" label)
- **Why:** cohort-paced learning reads better as fraction than percentage
- **NICHE adoption:** "4/10 sessions attended", "3/12 modules complete" — replaces absolute % progress bars
- **shadcn:** `Progress` component + custom trailing `<span>` for fraction

### 2.4 Tagged course card with progress + instructor footer
- **Source:** Online Learning Profile `node 10:1206`
- **Anatomy:** cover image (113h) + tag pill (uppercase 8px primary-tinted) + title (14px Medium, 2-line max) + progress bar + circular avatar + instructor name/role footer
- **Why:** compact info density — cover, category, title, progress, mentor in one card
- **NICHE adaptation:** replace heart-favorite with status badge ("In progress" / "Behind by 2" / "Complete"); tag color = pillar (Creativity / Humanity / Entrepreneurship)
- **shadcn:** `Card` + `Progress` + `Badge` + `Avatar`

### 2.5 Sidebar with grouped sections
- **Source:** Online Learning Profile `node 10:1168` (OVERVIEW / FRIENDS / SETTINGS sections)
- **Why:** visually tames a long nav with tiny-caps gray section labels
- **NICHE groups (Admin):** OVERVIEW / PROGRAMS / PEOPLE / COMMUNICATIONS / FINANCE / SETTINGS (see [ADMIN_PATTERNS.md §1](./ADMIN_PATTERNS.md#1-sidebar-ia-for-niche-admin))
- **shadcn:** `SidebarGroup` + `SidebarGroupLabel` (Bai Jamjuree uppercase, tracked)

### 2.6 Section header with paginated arrow controls
- **Source:** Online Learning Profile `node 10:1549` + `10:1608`
- **Why:** horizontal carousel pattern useful for "Resume your module" / "Upcoming sessions" rows on Learner home
- **shadcn:** `Carousel` (embla via shadcn) + `Button ghost` icons for prev/next; Fraunces 20px header

### 2.7 Pinned upsell card in sidebar bottom
- **Source:** Online Learning Profile `node 10:1568`
- **Anatomy:** large central icon + title + CTA pill, pinned via `SidebarFooter`
- **NICHE use:** "Apply for next cohort" (when learner is in completing cohort) or "Upgrade to Studio Program" cross-sell
- **shadcn:** `Card` in `SidebarFooter`

### 2.8 Stat strip 3-up + right-rail mini-list
- **Source:** Online Learning Profile `node 10:1640-1652` (right-rail "Daily progress")
- **Why:** vertical icon-prefixed stack — perfect for "Today's focus" panel showing onsite/online session items
- **NICHE use:** right-rail on Learner home — agenda for the day with location-type chip per item

### 2.9 Stacked-segment weekly bar chart in CSS
- **Source:** Online Learning Profile `node 10:1125` (4-step purple ramp, no chart library)
- **Why:** lightweight, on-brand
- **NICHE use:** weekly study minutes / weekly assignments submitted, colored in moss-green ramp
- **NB:** respect `prefers-reduced-motion`

### 2.10 Hero split layout + dual CTA (marketing only)
- **Source:** Education Landing (genre convention; specific frame not readable)
- **Why:** standard high-conversion landing pattern
- **NICHE adaptation:** voice inversion — "Find your niche" (primary) + "See the 12 programs" (ghost CTA); replace floating "12k+ students" chip with provocation card "Are you learning the wrong way?"; replace stock photo collage with single high-contrast portrait + cream type
- **shadcn:** `NavigationMenu` + `Card` + `Button` (primary + ghost variants)

### 2.11 FAQ accordion + closing CTA banner
- **Source:** Education Landing (genre convention)
- **NICHE use:** provocative-FAQ block ("Why November only?" / "What if I'm self-taught already?") + closing CTA banner inverting cream/dark
- **shadcn:** `Accordion` + `Card` for CTA banner

### 2.12 Stat counter row (lean into scarcity)
- **Source:** Education Landing (genre convention — usually "100k+ students")
- **NICHE inversion:** "3 pillars · 12 programs · 1 cohort/year" — leans into scarcity rather than fake-large numbers; supports "anti-marketplace" institute positioning

---

## 3. Patterns to REJECT (with reasoning)

### 3.1 Outer rounded card framing the entire app
- **Source:** Online Learning Profile `node 10:1626` (`rounded-[20px]`)
- **Why reject:** breaks at narrow viewports; wastes 40+px on every edge
- **NICHE rule:** fill viewport edge-to-edge

### 3.2 Translucent primary at 20% opacity
- **Source:** Online Learning Profile (e.g. `rgba(112,45,255,0.2)` on icon tiles + tags)
- **Why reject:** unstable contrast over white; on NICHE cream `#f2f1f0` + red `#fe1d25` produces muddy pink
- **NICHE rule:** use solid token from a designed red ramp (`red/50`, `red/100`) instead of opacity-modulated brand color

### 3.3 Heart "favorite" on every course/cohort card
- **Source:** Online Learning Profile `node I10:1206;5:430`
- **Why reject:** favoriting is irrelevant to a cohort-based assigned curriculum
- **NICHE replacement:** status badge ("In progress" / "Submitted" / "Needs revision" / "Complete")

### 3.4 8px and 10px text in production UI
- **Source:** Online Learning Profile (avatar role labels, tag labels)
- **Why reject:** fails WCAG comfort sizing; breaks on Bai Jamjuree Thai script
- **NICHE rule:** floor at 11px; eyebrow + caption tokens already defined in `brand-book/css/tokens.css` start at 12px

### 3.5 Single-bar progress with no states
- **Source:** LMS Course Dashboard `node 1:1625`
- **Why reject:** NICHE needs at minimum 6 states (locked / current / complete / needs-revision / live-session / onsite-only)
- **NICHE replacement:** per-lesson status chips in vertical timeline; keep single-bar only for course-card summary

### 3.6 Monochrome-only palette
- **Source:** LMS Course Dashboard (entire file is black/white/grey)
- **Why reject:** erases NICHE identity (cream + red + moss + ink)
- **NICHE rule:** semantic color use — red = action/urgent · moss = success/on-track · neutral = current · gray = decorative-only (NO text)

### 3.7 Marketing top-nav inside authenticated dashboard
- **Source:** LMS Course Dashboard `node 1:1576` (Courses / Blog / Music / Contest)
- **Why reject:** mixes app shell with marketing
- **NICHE rule:** marketing layout (no sidebar) ≠ app layout (sidebar + topbar). Two separate Next.js route groups.

### 3.8 Stale "Sign In" button on authenticated dashboard
- **Source:** LMS Course Dashboard `node 1:1586`
- **Why reject:** dead state; design drift
- **NICHE rule:** topbar shows logged-in user identity (avatar + name + role chip); no Sign In button when authenticated

### 3.9 Decorative SVG starbursts behind hero title
- **Source:** Online Learning Profile `nodes 10:1101-1105`
- **Why reject:** Web 2.0 sparkle aesthetic
- **NICHE rule:** brand is editorial/serif-led; hero composition uses Fraunces display + photography (per brand book §5)

### 3.10 `capitalize` CSS on body content
- **Source:** Online Learning Profile ("good Morning Prashant" / "continue your journey")
- **Why reject:** CSS title-casing breaks Thai text and creates content/UX coupling
- **NICHE rule:** author content with proper casing in DB; no `text-transform: capitalize` in CSS for content

### 3.11 Sidebar of 8 unrelated nouns (flat IA)
- **Source:** LMS Course Dashboard `nodes 1:1539-1561`
- **Why reject:** NICHE has 3 roles (Learner/Instructor/Admin) and cohort-scoped content
- **NICHE rule:** role-switched sidebar (different items per role) + cohort-contextual; never flat product menu

### 3.12 Single all-powerful Admin role
- **Source:** SchoolHub admin (inferred — single-role implicit; no permission UI)
- **Why reject:** NICHE needs RBAC from day one
- **NICHE replacement:** OpenFGA-backed multi-role + scope (see [DATA_MODEL.md §3](./DATA_MODEL.md#3-openfga-model))

### 3.13 K-12 vocabulary
- **Source:** SchoolHub admin (Subjects, Class periods, Parent fields, Grade book, GPA)
- **Why reject:** NICHE = adult learners, non-credit creative ed, continuous cohorts
- **NICHE rule:** Programs (the 12) + Courses + Cohorts + Sessions; portfolio-based assessment only

### 3.14 Generic edtech copy ("Unlock your potential")
- **Source:** Education Landing (genre convention)
- **Why reject:** brand book §7 voice principles forbid; flattens NICHE's declarative/provocative voice
- **NICHE replacement:** "Find your niche" / "Are you learning the wrong way?" / "All Eyes on Independents" / "The photography program that teaches you to sell"

### 3.15 Mint-green + purple gradient CTA buttons
- **Source:** Education Landing (genre convention)
- **Why reject:** violates NICHE 5-color palette
- **NICHE rule:** buttons use red `#fe1d25` (primary) or near-black `#252026` (secondary) on cream

### 3.16 Star ratings + "4.9 from 12k reviews" badges
- **Source:** Education Landing (genre convention)
- **Why reject:** marketplace pattern; NICHE is admissions-gated institute
- **NICHE rule:** outcomes (employment %, alumni quotes by name) > anonymous ratings

### 3.17 Counters of fake-large numbers
- **Source:** Education Landing (genre convention)
- **Why reject:** NICHE is small, intentional, cohort-based — leans into scarcity
- **NICHE replacement:** "11 seats remaining in November cohort" / "3 pillars · 12 programs · 1 cohort/year"

---

## 4. Critical extensions NOT covered by any reference (NICHE original)

The references give NICHE roughly 30% of its UI surface as adopt-and-adapt patterns. The following 70% must be designed from scratch — there is no Figma file in the references that covers these:

1. **Cohort awareness strip** — "Cohort 02 · Module 4 of 12" indicator in topbar; cohort-color-coded affordances throughout
2. **Onsite session card variant** — distinct from online; map pin + location address + RSVP/checked-in/missed status
3. **Relative-progress signals** — `PaceIndicator` component (red = behind / cream = on-track / moss = ahead) replacing absolute %
4. **Assignment upload affordance** — drop-zone card + deadline countdown + status (draft/submitted/reviewed/revisions-requested) + inline grade/feedback
5. **Notification center** — dedicated panel (not stat-card co-opting); types: instructor announcements / cohort reminders / schedule changes / feedback
6. **Office-hours / mentor booking** — slot-booking UI + async questions queue
7. **Cohort peers feed** — cohort-scoped activity (who submitted, who attended) with privacy controls
8. **Program structure tree** — left-rail outline (Program → Phase → Module → Session) with state per node
9. **Bilingual readiness** — Thai/Latin line-height tokens; Bai Jamjuree alongside Fraunces; no `capitalize` CSS
10. **Role-aware shell** — Learner / Instructor / Admin role-guards baked into layout; sidebar items swap by role
11. **Cohort dashboard with at-risk detection** — see [ADMIN_PATTERNS.md §3](./ADMIN_PATTERNS.md#3-cohort-dashboard--the-differentiator)
12. **Multi-role assignment + scope matrix** — see [ADMIN_PATTERNS.md §4](./ADMIN_PATTERNS.md#4-multi-role--scope-assignment-ui)
13. **Bulk CSV enrollment wizard** — see ADMIN_PATTERNS.md §5
14. **Schedule with onsite + online combined** — see ADMIN_PATTERNS.md §6
15. **Announcement composer with audience targeting** — see ADMIN_PATTERNS.md §7
16. **PDPA-compliant UI elements** (consent log viewer, data export, anonymize confirmation) — see ADMIN_PATTERNS.md §11

---

## 5. Recommendation: shift from Figma-source-of-truth to Code-source-of-truth

The 4 Figma community references in `ref.md` provide concept-grade inspiration but:

- **Single-screen showcases** (refs 1, 2) — not multi-screen UI kits; ~70% of NICHE surface is missing
- **Rate-limited** on Starter plan — full-canvas extraction would require Figma plan upgrade
- **Generic genre patterns** — no NICHE-specific differentiators (cohort-first, multi-role, hybrid onsite/online)

Given (a) the brand book is already implemented as HTML+CSS (`brand-book/css/tokens.css`), (b) the platform stack is React/Next.js + shadcn/ui, (c) Claude has `frontend-design` skill installed for code-first design generation:

**Recommended workflow:**

1. **Tokens in code** = source of truth (already done — `brand-book/css/tokens.css`)
2. **shadcn/ui** = component primitives, themed by tokens
3. **Claude `frontend-design` skill** = screen-level designer; generate React components from natural language + brand context
4. **Storybook (optional)** = visual review surface for stakeholders
5. **Figma MCP (consume mode only)** = activate when external designers send Figma files; use `figma-implement-design` skill to translate

This frees NICHE from Figma quota constraints and avoids the "design-to-code lossy translation" step entirely.

---

## 6. Sources

- [Dashboard Online Learning Profile (Community)](https://www.figma.com/community/file/1313209648458042020/dashboard-online-learning-profile) — `zBQmmtoZAnnmNkAZ0njsPW`
- [LMS and Course Dashboard Design (Community)](https://www.figma.com/community/file/1319524540637048768/lms-and-course-dashboard-design) — `cxnc2cwhRfFYIkimSnuwBS`
- [Online Education Website Landing Page (Community)](https://www.figma.com/community/file/1428384686040444933/online-education-website-landing-page-ui-design) — `MosgE4Fxzs5KoiOkmsJjSV`
- [SchoolHub School Management Admin (Community)](https://www.figma.com/community/file/1381931496411280342/schoolhub-school-management-admin-dashboard-template) — paywall-blocked

### Recommended additional Figma references (if Figma quota refreshes)
- [CourseFlow UI Kit](https://www.figma.com/community/file/1505496020038538472/courseflow-ui-kit-elearning-web-app-ui-kit-for-figma-preview) — 35+ desktop screens incl. instructor pages
- [Dreams LMS](https://www.figma.com/community/file/1542911527930004020/dreams-lms-free-figma-ui-kit-for-learning-management-systems) — instructor modules + cohort screens
- [Designo Streamlined LMS Dashboards](https://www.figma.com/community/file/1395793003651190548/designo-streamlined-lms-dashboards)
