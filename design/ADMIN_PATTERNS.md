# NICHE Platform — Admin Portal UI Pattern Playbook

> **Companion to:** [PLATFORM_DESIGN.md](./PLATFORM_DESIGN.md) · [DATA_MODEL.md](./DATA_MODEL.md)
> **Audience:** dev team building the Admin / Student Portal (the "management portal" from `requirements/ref.md`)
> **Sources:** Linear · Notion · GitHub Org · Maven Admin · Stripe Dashboard · Vercel · Beehiiv · Cal.com · shadcn/ui · OneTrust PDPA
> **Status:** v1.0 — concrete patterns ready for shadcn/ui implementation

The original ref.md included a SchoolHub Admin Figma file as the management-portal reference. That file is paywall-blocked (Figma MCP Starter quota) and provides zero leverage on NICHE-critical features anyway (cohort concept, multi-role RBAC, invite-based enrollment). This playbook delivers the patterns from production SaaS exemplars instead.

---

## 1. Sidebar IA for NICHE Admin

**Comparative baseline:**

- **Linear (Dec 2024 redesign):** Account / Features / Administration (admin-only) / Your Teams. Settings sub-section is data-rich tables for users and teams; sidebar items are right-click-customizable and draggable.
- **Notion:** Workspace nav (Home / Inbox / Teamspaces) + user-created pages; settings split Workspace + Account.
- **GitHub Org settings:** Settings-first IA — Members / Teams / Repositories / Billing / Security / Integrations — separated from product sidebar.
- **Maven Admin:** Students tab (status-segmented) + cohort selector in top bar. Flat, enrollment-centric.
- **Stripe Dashboard:** Primary nav (Balances / Transactions / Customers / Products) + Shortcuts + Settings. Pinned shortcuts for frequently-visited pages.

**Recommended NICHE Admin Sidebar IA:**

```
OVERVIEW
  ├─ Dashboard           (KPI strip + at-risk + quick-links)

PROGRAMS
  ├─ Programs            (catalog list)
  ├─ Cohorts             (active cohorts list)
  ├─ Courses             (course content library)
  ├─ Schedule            (cross-cohort calendar)

PEOPLE
  ├─ Learners            (user list filtered to learner role)
  ├─ Instructors         (user list filtered to instructor role)
  ├─ All Users           (full roster + role matrix)
  ├─ Enrollments         (enrollment records table)

COMMUNICATIONS
  ├─ Announcements       (composer + sent history)

FINANCE
  ├─ Payments            (transaction table + summary tiles)

SETTINGS  (admin-only, Linear-style separated section)
  ├─ Roles & Permissions
  ├─ Invite Links
  ├─ PDPA & Consent
  ├─ Audit Log
  ├─ Integrations
  ├─ Workspace
```

**Principles applied:** Design for the most restricted view first (single-cohort instructor sees only their cohort's subset); admin sees everything. Groups mirror mental models: content (Programs/Cohorts/Courses), people (Learners/Instructors), money (Finance), compliance (Settings/PDPA). Settings is visually separated like Linear's Administration section — same sidebar, distinct divider.

---

## 2. List + Detail + Form Trio per Entity

**Reference:** Linear issue tables (dense, sortable, bulk-actionable), Notion database views (filter pills above table), Stripe payments list (status badges, date/amount columns, click-to-detail).

**Universal list view structure:**

- **Header row:** `[Entity name] (count)` left + `[Search box]` + `[Filter pills: status, date range, program/cohort]` + `[+ Create]` button right
- **Column defaults per entity:**
  - **Users:** Avatar+Name · Email · Role(s) · Cohort(s) · Status · Last Active · Actions menu
  - **Programs:** Name · Pillar · Cohort count · Status (draft/active/archived) · Created
  - **Cohorts:** Name · Program · Start–End dates · Capacity meter (enrolled/max) · Status · Actions
  - **Courses:** Name · Program · Module count · Published toggle · Last updated
  - **Enrollments:** Learner · Cohort · Enrolled date · Status (enrolled/waitlisted/dropped/completed) · Payment status
  - **Payments:** Learner · Cohort · Amount · Date · Status pill · Invoice #
- **Bulk actions toolbar** appears on row-checkbox select — contextual ("Move to cohort", "Export selected", "Send announcement", "Mark paid")
- **Density toggle:** compact / default / spacious (Notion-style)
- **Pagination:** 25/50/100 rows + total count

**Detail view structure (right-panel drawer for quick-view; full page for deep edit):**

- **Hero:** entity name (editable inline), status badge, key metadata row (dates, counts), action buttons (Edit, Archive, Duplicate)
- **Tabs:** for Cohort — Roster / Analytics / Schedule / Communications; for User — Profile / Roles & Access / Enrollments / Activity / PDPA
- **Sub-resources** within tabs use mini-tables with their own search/filter

**Form layout:**

- Single-column for short forms (< 6 fields): Create Enrollment, Invite User
- Two-column grid for medium forms (6–15 fields): Create Cohort, Create Program
- Wizard (stepped) for complex flows (> 15 fields or conditional branching): CSV import, complex role assignment
- All forms: React Hook Form + Zod schema validation. Inline field-level errors. Auto-save draft on blur for long forms. Primary CTA "Save" pinned to bottom; secondary "Cancel" beside it. Destructive actions behind confirmation dialog with type-to-confirm text.

**shadcn/ui components:**
- List view: `DataTable` (TanStack Table v8) + `Input` (search) + `Badge` (status pills) + `DropdownMenu` (actions menu) + `Checkbox` (bulk select)
- Detail: `Tabs` + `TabsContent` + `Card` + `Separator`
- Form: `Form` + `FormField` + `Input` + `Select` + `Combobox` + `DatePicker` + `Switch` + `Button`

---

## 3. Cohort Dashboard — The Differentiator

This is the most NICHE-specific screen. Maven's six enrollment states (waitlisted, dropped-off, enrolled, application-incomplete, applied, accepted) inform the status model; EducateMe's Kanban-based assignment tracker informs progress visualization.

**Cohort header / hero:**
```
[Cohort Name] [Program name chip] [Status pill: Upcoming / Active / Completed]
Start: Jan 12 2026  →  End: Apr 12 2026   |   Enrolled: 18 / 24  [capacity bar]
[Edit Cohort] [Send Announcement] [View Schedule] [Archive]
```
Capacity bar: `Progress` component, red when > 90% full, amber 70–90%.

**Roster tab:**

Columns: Avatar | Full Name | Email | Progress % | Attendance % | Last Active | Assignments (X/Y done) | At-Risk flag | Actions

- At-Risk flag: auto-set when progress < 40% AND last active > 14 days. Renders as red `AlertCircle` icon with tooltip explaining criteria.
- Filters: Status (enrolled/waitlisted/dropped/completed) | At-Risk only | Program module | Date range (last active)
- Bulk actions: Send announcement to selection | Export roster | Move to different cohort | Mark at-risk manually | Download certificates

**Analytics tab:**
- Completion curve: line chart (x = week of cohort, y = % learners completed that week's content). Recharts via shadcn `ChartContainer`.
- At-risk list: table of learners meeting at-risk criteria, sortable by progress asc
- NPS score tile (collected via post-session surveys)
- Attendance heatmap: week × session grid, color intensity = % attendance. Custom CSS grid component.

**Communications tab:** Announcement composer (see §7).

**Schedule tab:** Week-view calendar filtered to this cohort's sessions (see §6), with attendance overlay: `[session title] [date/time] [X/18 attended]`.

---

## 4. Multi-Role / Scope Assignment UI

**Reference:** Slack decomposes admin into discrete assignable permissions scoped per workspace. Notion uses "inheritance with override". Linear proves minimal global roles work when delegating at team/cohort layer.

**Role assignment modal (4 steps):**

1. **Search user:** `Combobox` with avatar + name + current roles shown.
2. **Pick role:** `RadioGroup` with role descriptions inline (Learner / Instructor / Admin).
3. **Pick scope:** `Select` for scope type (Platform-wide / Program / Cohort / Course), then a second `Combobox` for the specific resource.
4. **Confirm:** summary row "Grant [User] role [Instructor] on [Cohort: BKK-Design-01]" + Grant button.

This maps to OpenFGA tuple: `(user: X, relation: instructor, object: cohort:BKK-Design-01)`.

**User detail — role/scope matrix (User detail "Roles & Access" tab):**

| Scope Type | Resource | Role | Granted by | Granted at | Revoke |
|---|---|---|---|---|---|
| Cohort | BKK-Design-01 | Instructor | admin@niche.ac | 2025-12-01 | × |
| Course | Typography-101 | Learner | system | 2025-12-05 | × |

**Bulk role assignment** (e.g., 5 instructors to a cohort):

List view in "All Users" → select 5 rows → bulk action "Assign Role" → same modal but scope is pre-filled from context (if initiated from Cohort detail) and role assignment applies to all selected. Confirmation shows preview list of all affected users before committing.

**shadcn/ui:** `Dialog` + `Command` (Combobox search) + `RadioGroup` + `Select` + `Table` + `Button`

---

## 5. Enrollment Flow

**Reference:** Vercel team invites (role-at-invite-time, 7-day expiry, invite link gives lowest permission to joiners).

### 5.1 Manual single-add form

Fields: Email (required) | Full Name | Cohort (Combobox) | Role (Select: Learner/Instructor) | Payment status (Paid / Scholarship / Pending) | Send invite email toggle (on by default).

Submit: if toggle on → Resend invite email sent; if off → direct enrollment without email notification.

### 5.2 Bulk CSV import — 5-step wizard

1. **Download template** — pre-formatted CSV with columns: email, full_name, cohort_id, role, payment_status
2. **Upload** — drag-and-drop file input + DropZone. Show file name + row count preview.
3. **Map columns** — if headers mismatch, show mapping table: CSV column → NICHE field, with auto-suggest + manual override `Select`.
4. **Validate** — show summary "48 valid / 2 errors". Errors table: Row # | Column | Issue | Suggested fix. Inline correction in cells before proceeding.
5. **Confirm** — "Import 48 learners to Cohort BKK-Design-01?" → confirm. Post-import: success toast + downloadable error report for failed rows.

### 5.3 Invite link generator

Form: Cohort (pre-filled from context) | Role (Learner default) | Expiry (7 days / 30 days / No expiry) | Usage limit (Single-use / N uses / Unlimited) | [Generate link].

Output: copy-to-clipboard field showing `https://niche.ac/join/abc123xyz` + QR code (for onsite display).

Link analytics row: Created | Expires | Uses (3/10) | Status (active/expired) | Deactivate button.

**shadcn/ui:** `Dialog` + `Form` + `Input` + `Select` + `Switch` + `Stepper` (custom: `ol` with `Step` components) + `Table` + `CopyButton` (custom)

---

## 6. Schedule — Combined Onsite + Online

**Reference:** Cal.com supports daily/weekly/monthly views, drag-to-schedule, conflict detection across calendars, and recurring event support.

**Calendar layout:** Default view = week. Toggle: Day | Week | Month | Agenda. For cohort-scoped schedule, Agenda is most useful (flat list of upcoming sessions with metadata).

**Event card (in week grid):**
```
[●] Typography Workshop           ← color dot = cohort color
    Mon Feb 3, 09:00–12:00
    [🏢 Onsite: NICHE Studio B]  or  [📹 Live Online: Zoom link →]
    Attendance: 12/18 ✓ (if past)
```

**Event creation/edit form:** Title | Cohort (Combobox) | Date + Time | Duration | Location type (toggle: Onsite / Live Online / Async) → conditional field (address or Zoom URL) | Recurrence (None / Weekly / Bi-weekly / Custom) | Description | Instructor (Combobox).

**Conflict detection:** On date/time change, run client-side check against existing events for the same room or instructor. Surface as inline warning banner: "Conflict: Instructor Achara has Typography Workshop at this time."

**Attendance recording UI:** On past/current session event detail: Roster tab shows the cohort roster as a checklist. Bulk mark "Mark all present"; individual `Checkbox` per learner. Auto-save on each toggle.

**shadcn/ui:** `Calendar` (date picker) + `ToggleGroup` (Day/Week/Month) + `Popover` + `Select` + `Switch` (location type) + `Input` + custom week-grid layout via CSS grid.

---

## 7. Announcement Composer

**Reference:** Beehiiv's composer with dynamic segment builder. Slack channel + @mention targeting. Discord role-targeted announcements.

**Editor:** Block-based WYSIWYG (Tiptap, integrates cleanly with shadcn-style components) — admin staff are non-technical. Toolbar: Bold / Italic / Link / Bullet list / Heading / Image upload (Cloudflare R2).

**Audience scoping pills** rendered as `TagInput`-style component above the composer:
- `Cohort: BKK-Design-01 ×`
- `Status: at-risk ×`
- `Individual: Somchai Rakpong ×`

Multiple pills are unioned (OR within a cohort, AND across cohort + status). A "Preview audience" link shows count + matched-learner list before sending.

**Channel row:** `[☑ In-app]  [☑ Email]  [☐ Line OA (coming soon)]` — each toggleable `Checkbox`.

**Scheduling:** `RadioGroup`: Send now / Schedule. If Schedule, show `DateTimePicker`. Display timezone: Asia/Bangkok (hardcoded for MVP).

**Preview:** Opens a `Dialog` with rendered announcement as it will appear in-app + email preview side-by-side.

**shadcn/ui:** `Card` (composer container) + `Tabs` (In-App / Email preview) + `Dialog` (preview) + `RadioGroup` (send mode) + `DatePicker` + `Badge` (audience pills) + `Button`

---

## 8. Analytics Dashboard

**Reference:** Plausible (PDPA-friendly, no PII in events). Mixpanel/Amplitude (cohort retention curves). Stripe Dashboard (revenue tiles).

**Top KPI tile strip (5 tiles):**

| Tile | Metric | Trend indicator |
|---|---|---|
| Active Cohorts | 4 | — |
| Enrolled Learners | 87 | +12 this month |
| Cohort Fill Rate | 76% | ↑ vs last cohort |
| Avg Completion | 61% | ↓ needs attention |
| MRR | ฿248,000 | +8% MoM |

Rendered as `Card` grid (5-column at lg, 2+3 at md, 1-column at sm).

**Cohort completion curve:** Line chart (Recharts `LineChart`) x = Week 1–12, y = % learners completed that week's required content. One line per cohort. Overlaying multiple cohorts enables benchmarking.

**At-risk learners list:** Name | Cohort | Progress % | Last Active | Days Since Active | At-Risk Reason. Sortable by Days Since Active desc. Row click → user detail.

**Filter strip (sticky above content):** Date range `DateRangePicker` | Cohort multi-select | Program multi-select | Pillar `Select`.

**Drill-down:** KPI tiles are links — click "Active Cohorts → 4" navigates to Cohorts list pre-filtered to active. Completion curve data points open tooltip with learner names.

**shadcn/ui:** `Card` + `ChartContainer` (Recharts wrapper) + `Table` + `DateRangePicker` (custom: `Calendar` + `Popover`) + `MultiSelect` (custom Combobox variant)

---

## 9. Payment Dashboard

**Reference:** Stripe Dashboard transaction table with status filtering, date filtering, click-through to detail. Shopify Orders for bulk status actions.

**Summary tiles (4):** Revenue This Month | Outstanding (pending/unpaid) | Refunded | Failed Payments

**Transaction table columns:** Invoice # | Learner | Cohort | Amount | Date | Status pill | Actions

Status pills: `paid` (green) | `pending` (yellow) | `failed` (red) | `refunded` (grey). `Badge` with semantic `variant`.

**Filters:** Date range | Cohort | Program | Status (multi-select) | Amount range.

**Detail drawer (`Sheet` from right):**
- Invoice metadata (learner, cohort, program, amount, currency THB, date, payment method, notes)
- Action buttons: Mark Paid Manually (offline/bank transfer) | Send Payment Reminder (Resend email) | Issue Refund (confirmation dialog with refund amount field).

**shadcn/ui:** `Card` (tiles) + `DataTable` + `Badge` + `Sheet` (detail drawer) + `Dialog` (confirm refund) + `Button` + `Select` (filter dropdowns)

---

## 10. Mobile / Tablet Considerations

Admin work is desktop-first. Instructors use tablet for roster + grading; mobile for announcements.

**Sidebar breakpoints:**

- `≥ 1024px` (lg): Full sidebar, collapsible to icon-only (`collapsible="icon"` mode). State persisted in cookie via `useSidebar`.
- `768–1023px` (md/tablet): Sidebar collapses to icon-only by default. `SidebarTrigger` hamburger in top bar opens full sidebar as overlay (`collapsible="offcanvas"`).
- `< 768px` (mobile): Sidebar hidden entirely. Bottom navigation bar (`fixed bottom-0`) with 5 tabs: Dashboard / Cohorts / People / Comms / More. "More" opens a `Sheet` with full nav.

**Table behavior at narrow breakpoints:**
- `< 768px`: Data tables transform to card list layout. Each row becomes a `Card` with primary fields visible and a `Collapsible` for secondary columns.
- Bulk actions toolbar collapses to a `DropdownMenu` "Actions (3 selected)" button.

**Forms at mobile:** Single-column enforced regardless of viewport. `DatePicker` uses native `input type=date` on mobile for better UX.

---

## 11. PDPA-Aware UI Elements

**Thai PDPA requirements:** explicit logged consent; right to data portability (export); right to erasure with anonymization; processing records.

### 11.1 Consent log viewer (User detail → PDPA tab)

Table: Date | Consent type (Marketing emails / Course data processing / Third-party share) | Action (Granted / Revoked) | Channel (web-signup / admin-override) | IP address (masked: `203.xxx.xxx.12`).

Rendered as timeline (`ol` with `Separator`), not flat table, to match the sequential nature of consent history.

### 11.2 Data export (Right to Access)

Button: "Export Personal Data (PDPA)". On click: triggers a background job (tRPC mutation), shows `Toast` "Export preparing, you'll receive an email." Email (Resend) delivers a JSON or PDF of all stored personal data. Do not expose raw DB dump; sanitize to user-readable fields.

### 11.3 Soft-delete + anonymize (Right to Erasure)

Two-step:
1. **Deactivate account** → user can no longer log in, data retained for 30-day undo window.
2. **Anonymize** → irreversible: name → "Learner [ID]", email → `deleted_[hash]@niche.ac`, phone → null. Triggered via `AlertDialog` with type-to-confirm: user must type "ANONYMIZE" before button activates. Post-anonymize: record retained (enrollment history preserved for financial records) but all PII replaced. A 30-second `Toast` with "Undo" is shown during the cancel window before the job commits.

### 11.4 Audit log viewer (Settings → Audit Log)

Table: Timestamp | Actor (admin email) | Action | Resource type | Resource ID | IP address.

Actions logged: role-grant, role-revoke, enrollment-create, enrollment-delete, anonymize, data-export-requested, announcement-sent, payment-marked-paid.

Filterable by actor, action type, date range. Read-only — no edit or delete on audit log rows.

**shadcn/ui:** `Table` + `Accordion` (consent timeline) + `AlertDialog` (confirm anonymize) + `Toast` + `Button` + `Badge` (action type pills)

---

## 12. shadcn/ui Component Mapping (consolidated)

| Feature | Base shadcn components | Custom additions |
|---|---|---|
| Sidebar | `Sidebar`, `SidebarProvider`, `SidebarMenu`, `SidebarMenuBadge`, `SidebarGroup` | Active-group highlight; NICHE brand colors |
| Cohort header/hero | `Card` + `Badge` + `Progress` + `Tabs` | Capacity meter via `Progress` with color thresholds; status pill color map |
| Roster table | `DataTable` (TanStack Table) + `Checkbox` + `Avatar` + `Badge` + `DropdownMenu` | At-risk flag (`AlertCircle` + `Tooltip`); inline progress percentage bar |
| Analytics KPI tiles | `Card` + `CardHeader` + `CardContent` | Trend indicator with `TrendingUp`/`TrendingDown` icons (lucide-react) |
| Completion curve | `ChartContainer` + Recharts `LineChart` | Multi-cohort color legend |
| Attendance heatmap | Custom CSS grid | Opacity-scaled `bg-` cells; no shadcn equivalent |
| Role assignment modal | `Dialog` + `Command` + `RadioGroup` + `Select` + `Table` | Multi-step `Stepper` (custom `ol`-based) |
| CSV import wizard | `Dialog` + `Stepper` + `Table` (validation errors) + `Input` (file) | Inline-editable error cells; step progress indicator |
| Invite link | `Input` (read-only) + `Button` (copy) + `Select` + `Switch` | QR code (`qrcode.react`) |
| Schedule calendar | `Calendar` + `ToggleGroup` + `Popover` | Week-grid CSS grid; event cards with location-type icon |
| Announcement composer | `Card` + `Badge` (audience pills) + `RadioGroup` + `DatePicker` + `Dialog` (preview) | Tiptap WYSIWYG block editor; audience TagInput |
| Payment detail | `Sheet` + `Card` + `Badge` + `Button` + `Dialog` | Manual-pay confirmation with notes field |
| PDPA viewer | `Table` + `Accordion` + `Button` + `AlertDialog` | Consent timeline component; anonymize countdown toast |

---

## 13. Recommended Build Order

1. **Cohort dashboard** is the highest-differentiating screen — build it first as a Storybook story against real Drizzle schema types so the at-risk flag logic and capacity meter thresholds are validated against actual data shapes before broader implementation.
2. **Role assignment modal** needs an OpenFGA tuple write function behind it — spec the tRPC `grantRole` mutation input/output type before building the UI so the `Command` search component is wired to real user data from Supabase.
3. **PDPA anonymize job** should be a Railway background worker (not a synchronous tRPC call) with a 30-day soft-delete window stored in a `pending_anonymization` Drizzle table — design the DB schema before building the UI cancel-window toast.

---

## Sources

- [Maven Student Management — Admin Dashboard](https://help.maven.com/en/articles/6069488-student-management-in-the-maven-admin-dashboard)
- [Linear Sidebar Changelog Dec 2024](https://linear.app/changelog/2024-12-18-personalized-sidebar)
- [WorkOS: Multi-tenant Permissions — Slack, Notion, Linear](https://workos.com/blog/multi-tenant-permissions-slack-notion-linear)
- [shadcn/ui Sidebar Docs](https://ui.shadcn.com/docs/components/radix/sidebar)
- [Vercel Team Members & Roles](https://vercel.com/docs/rbac/managing-team-members)
- [Bulk Import UX Patterns — Smart Interface Design Patterns](https://smart-interface-design-patterns.com/articles/bulk-ux/)
- [Beehiiv Audience Segmentation Redesign](https://product.beehiiv.com/p/audience-segmentation-reimagined)
- [Stripe Dashboard Basics](https://docs.stripe.com/dashboard/basics)
- [Cal.com Open Source Scheduling](https://cal.com/)
- [EducateMe Cohort Platforms Comparison](https://www.educate-me.co/blog/best-cohort-based-learning-platforms)
- [OneTrust Thai PDPA Guide](https://www.onetrust.com/blog/the-ultimate-guide-to-thai-pdpa-compliance/)

### Version notes
- shadcn/ui Sidebar: stable late 2024. 768px mobile breakpoint hardcoded in current release; feature request [github.com/shadcn-ui/ui/issues/5747](https://github.com/shadcn-ui/ui/issues/5747) open. Override with CSS custom property or fork `useSidebar` hook.
- TanStack Table v8: stable, underlying engine for shadcn `DataTable` examples.
- Recharts 2.x: default in shadcn `ChartContainer`; tree-shakable.
- OpenFGA 1.x: compatible with Next.js 15 server actions.
