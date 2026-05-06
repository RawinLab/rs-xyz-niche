# NICHE Platform — Data Model & Authorization

> **Companion to:** [PLATFORM_DESIGN.md](./PLATFORM_DESIGN.md)
> **Audience:** dev team — schema reference + permission matrix + migration path
> **Stack assumption:** Postgres + Drizzle (or Prisma) + OpenFGA for authorization
> **Status:** v1.0 — pre-implementation reference; verify with dev team before coding

This document is the schema and authorization reference. It uses TypeScript-flavored pseudo-schema for clarity. Production code will be Drizzle/Prisma syntax — semantics are identical.

---

## 1. Design principles

1. **Separate identity from authorization.** Clerk knows *who you are*. OpenFGA knows *what you can do*. The application code never asks Clerk "is this user an admin?" — it asks OpenFGA "can this user do action X on resource Y?"

2. **Never hardcode roles in app logic.** No `if (user.role === 'admin')`. All checks route through `can(userId, permissionKey, scopeType, scopeId)`. Adding roles is data, not code.

3. **Separate role from permission.** A role is a label (Instructor). A permission is a verb-on-noun (`course:content:edit`). Roles map to bundles of permissions; permissions are checked.

4. **Scope-aware from day one.** Every permission check has a scope (Course / Program / Platform). The same role at different scopes does different things.

5. **Multi-role per user is the norm, not the exception.** Plan for it from day one. Learner-alumni who becomes Creator must work without redesign.

6. **Soft delete with anonymization for PDPA.** Right-to-erasure = anonymize PII, retain aggregate stats. No hard deletes for production data — only for failed signups before email verification.

7. **Auditable.** Every role grant, every permission change, every data access on PII-flagged records logs to `audit_events`.

8. **Domain-event-driven.** Mutations emit events (`course.published`, `enrollment.completed`, `submission.graded`). Notifications, analytics rollups, and future marketplace services are subscribers — not direct callers. This is the architectural seam for adding capabilities without touching core code.

---

## 2. Core entities (relational schema)

### 2.1 Identity

```typescript
// Synced from Clerk; Clerk is source of truth for auth fields
table users {
  id            uuid          primary key             // synced from Clerk user_id
  clerk_id      text          unique not null
  email         text          unique not null
  name          text          not null
  username      text          unique                  // for /u/{username}
  avatar_url    text
  locale        enum('th', 'en')  default 'th'
  created_at    timestamptz   default now()
  updated_at    timestamptz   default now()
  deleted_at    timestamptz                           // null = active; non-null = soft-deleted
}
```

Notes:
- `username` is generated at signup (slug from name + numeric suffix on collision). Reserved.
- `deleted_at` triggers PII anonymization on a 7-day delay (cancel-window for accidental deletion).

### 2.2 Programs, Cohorts, Courses

```typescript
table programs {
  id              uuid          primary key
  name            text          not null
  slug            text          unique not null
  pillar          enum('creativity', 'humanity', 'entrepreneurship') not null
  level           enum('bootcamp', 'studio', 'degree') not null
  duration_months int           not null  // 3, 6, 12
  description     text
  hero_image_url  text
  status          enum('draft', 'open_for_application', 'archived') default 'draft'
  created_at      timestamptz   default now()
  updated_at      timestamptz   default now()
}

table cohorts {
  id              uuid          primary key
  program_id      uuid          references programs(id) on delete restrict
  name            text          not null    // e.g. "Cohort 1 — Nov 2026"
  start_date      date          not null
  end_date        date          not null
  capacity        int           not null    // typical 25–40
  application_deadline  date
  status          enum('planning', 'open', 'running', 'completed', 'archived') default 'planning'
  created_at      timestamptz   default now()
  updated_at      timestamptz   default now()
}
create index cohorts_program_idx on cohorts(program_id);
create index cohorts_status_idx on cohorts(status) where status in ('open', 'running');

table courses {
  id              uuid          primary key
  program_id      uuid          references programs(id) on delete cascade
  name            text          not null
  slug            text          not null
  order_index     int           not null
  description     text
  unique (program_id, slug)
}

table modules {
  id              uuid          primary key
  course_id       uuid          references courses(id) on delete cascade
  name            text          not null
  order_index     int           not null
  description     text
}

table sessions {
  id              uuid          primary key
  module_id       uuid          references modules(id) on delete cascade
  cohort_id       uuid          references cohorts(id) on delete cascade  // sessions are cohort-specific
  type            enum('onsite', 'live_online', 'async_video', 'async_reading') not null
  title           text          not null
  starts_at       timestamptz                        // null for async
  duration_minutes int
  location        text                                // physical address for onsite
  video_url       text                                // YouTube/Vimeo unlisted, or Cloudflare Stream
  resource_urls   jsonb                               // additional materials
  order_index     int           not null
}
create index sessions_cohort_idx on sessions(cohort_id);
create index sessions_starts_at_idx on sessions(starts_at);
```

**Key decisions:**
- Cohort and Module are siblings under Course (not nested). A session belongs to BOTH a module (curriculum context) AND a cohort (when it happens). Same module's sessions across different cohorts are different rows.
- `sessions.cohort_id` is the index that drives "what's on my schedule this week?"

### 2.3 Enrollment + Progress

```typescript
table enrollments {
  id              uuid          primary key
  user_id         uuid          references users(id) on delete restrict
  cohort_id       uuid          references cohorts(id) on delete restrict
  status          enum('applied', 'accepted', 'waitlisted', 'enrolled', 'withdrawn', 'completed') not null default 'applied'
  applied_at      timestamptz   default now()
  enrolled_at     timestamptz                          // set when status -> enrolled
  completed_at    timestamptz                          // set when status -> completed
  unique (user_id, cohort_id)
}
create index enrollments_user_idx on enrollments(user_id);
create index enrollments_cohort_idx on enrollments(cohort_id);
create index enrollments_status_idx on enrollments(status);

table session_attendances {
  id              uuid          primary key
  user_id         uuid          references users(id)
  session_id      uuid          references sessions(id) on delete cascade
  status          enum('present', 'absent', 'late', 'excused') not null
  recorded_at     timestamptz   default now()
  recorded_by     uuid          references users(id)   // who marked it
  unique (user_id, session_id)
}
```

### 2.4 Assignments + Submissions

```typescript
table assignments {
  id              uuid          primary key
  session_id      uuid          references sessions(id) on delete cascade
  title           text          not null
  brief           text                                  // markdown
  rubric          jsonb                                 // { criteria: [{name, weight, max_score}, ...] }
  max_score       int           default 100
  deadline        timestamptz   not null
  allow_late      boolean       default true
}

table submissions {
  id              uuid          primary key
  assignment_id   uuid          references assignments(id) on delete cascade
  user_id         uuid          references users(id) on delete restrict
  cohort_id       uuid          references cohorts(id)
  text_content    text                                  // optional
  file_urls       jsonb                                 // [{name, r2_key, size_bytes}, ...]
  submitted_at    timestamptz   default now()
  status          enum('draft', 'submitted', 'graded', 'returned_for_revision', 'needs_1on1') default 'draft'
  // grading
  score           int
  rubric_scores   jsonb                                 // { criterion_id: score }
  feedback_text   text
  graded_at       timestamptz
  graded_by       uuid          references users(id)
  // versioning — each new submission becomes a new row
  version         int           default 1
  prior_submission_id uuid      references submissions(id)
}
create index submissions_assignment_idx on submissions(assignment_id);
create index submissions_user_idx on submissions(user_id);
create index submissions_status_idx on submissions(status);
```

The `needs_1on1` status is NICHE-specific — exploits the onsite-first model and signals to instructor "discuss in next class, not via async feedback."

### 2.5 Career System

```typescript
table portfolio_items {
  id              uuid          primary key
  user_id         uuid          references users(id) on delete restrict
  // either auto-aggregated from a submission, OR manual entry
  source_submission_id uuid     references submissions(id)   // nullable
  program_id      uuid          references programs(id)
  title           text          not null
  description     text                                       // learner-edited
  artifact_urls   jsonb                                       // [{type, url, caption}]
  skill_tags      text[]                                      // pre-populated from curriculum + learner-extended
  visibility      enum('private', 'employer', 'public') default 'private'
  featured        boolean       default false                 // max 3 featured per user
  created_at      timestamptz   default now()
  updated_at      timestamptz   default now()
}
create index portfolio_user_idx on portfolio_items(user_id);
create index portfolio_visibility_idx on portfolio_items(visibility) where visibility in ('employer', 'public');

table resumes {
  id              uuid          primary key
  user_id         uuid          references users(id) on delete restrict
  json_data       jsonb         not null                      // JSON Resume schema
  template_id     enum('clean', 'creative') not null
  last_pdf_url    text                                         // R2 URL of last generated PDF
  last_generated_at timestamptz
  created_at      timestamptz   default now()
  updated_at      timestamptz   default now()
}

table certificates {
  id              uuid          primary key                   // = credential_id, used in /verify/{id}
  user_id         uuid          references users(id) on delete restrict
  cohort_id       uuid          references cohorts(id)
  program_id      uuid          references programs(id)
  issued_at       timestamptz   default now()
  // Open Badges 2.0 assertion JSON, served at /credentials/{id}
  ob_assertion_json jsonb       not null
  pdf_url         text                                         // styled PDF + QR code
  revoked         boolean       default false
  revoked_reason  text
}
create index certificates_user_idx on certificates(user_id);
```

### 2.6 Communications

```typescript
table announcements {
  id              uuid          primary key
  scope           enum('platform', 'program', 'cohort') not null
  scope_id        uuid                                          // null for platform; program_id or cohort_id otherwise
  author_id       uuid          references users(id)
  title           text          not null
  body            text          not null                        // markdown
  audience_filter jsonb                                         // optional: filter by enrollment status, etc.
  scheduled_at    timestamptz                                    // null = send immediately
  sent_at         timestamptz
  created_at      timestamptz   default now()
}
create index announcements_scope_idx on announcements(scope, scope_id);

table notifications {
  id              uuid          primary key
  user_id         uuid          references users(id) on delete cascade
  type            enum('deadline', 'announcement', 'feedback', 'enrollment_status', 'system') not null
  title           text          not null
  body            text
  link_url        text
  read_at         timestamptz
  created_at      timestamptz   default now()
}
create index notifications_user_unread_idx on notifications(user_id, read_at) where read_at is null;
```

### 2.7 Payments

```typescript
table payments {
  id              uuid          primary key
  user_id         uuid          references users(id)
  cohort_id       uuid          references cohorts(id)
  amount          decimal(10,2) not null
  currency        char(3)       default 'THB'
  status          enum('pending', 'succeeded', 'failed', 'refunded') not null
  gateway         text          default 'stripe'
  gateway_payment_id text       unique                            // Stripe payment_intent_id
  gateway_metadata jsonb
  paid_at         timestamptz
  created_at      timestamptz   default now()
}
create index payments_user_idx on payments(user_id);
create index payments_cohort_idx on payments(cohort_id);
```

### 2.8 PDPA / consent / audit

```typescript
table consent_events {
  id              uuid          primary key
  user_id         uuid          references users(id) on delete cascade
  consent_type    enum('account_creation', 'cohort_progress_tracking', 'cohort_aggregated_analytics', 'career_employer_visibility', 'cross_border_transfer_disco') not null
  action          enum('grant', 'withdraw') not null
  policy_version  text          not null                          // e.g. "2026-09-01"
  ip_hash         text                                             // sha256 of IP, for forensic only
  user_agent_short text                                            // browser/OS class only, no fingerprint
  occurred_at     timestamptz   default now()
}
create index consent_events_user_idx on consent_events(user_id, consent_type);

table audit_events {
  id              uuid          primary key
  actor_user_id   uuid          references users(id)
  action          text          not null                          // e.g. "user.role_granted", "submission.graded", "data.exported"
  target_type     text                                             // e.g. "user", "cohort", "submission"
  target_id       uuid
  metadata        jsonb
  occurred_at     timestamptz   default now()
}
create index audit_events_actor_idx on audit_events(actor_user_id);
create index audit_events_target_idx on audit_events(target_type, target_id);
```

### 2.9 Authorization (synced to OpenFGA)

The relational schema mirrors the OpenFGA tuple store for backup/queryability. OpenFGA is the source of truth at runtime; the table is a read-replica for "list all users with role X in scope Y" admin queries that OpenFGA's check API doesn't optimize for.

```typescript
table roles {
  id              uuid          primary key
  name            text          unique not null         // 'learner', 'instructor', 'admin', 'ta', 'creator', 'employer_partner'
  description     text
  is_built_in     boolean       default false           // built-in roles cannot be deleted
}

table permissions {
  id              uuid          primary key
  key             text          unique not null         // e.g. 'course:content:edit'
  description     text
}

table role_permissions {
  role_id         uuid          references roles(id) on delete cascade
  permission_id   uuid          references permissions(id) on delete cascade
  scope_type      enum('platform', 'program', 'course', 'cohort') not null
  primary key (role_id, permission_id, scope_type)
}

table user_role_memberships {
  id              uuid          primary key
  user_id         uuid          references users(id) on delete cascade
  role_id         uuid          references roles(id) on delete restrict
  scope_type      enum('platform', 'program', 'course', 'cohort') not null
  scope_id        uuid                                                 // null for platform-wide
  granted_at      timestamptz   default now()
  granted_by      uuid          references users(id)
  expires_at      timestamptz                                          // null = never expires
}
create index user_role_memberships_user_idx on user_role_memberships(user_id);
create index user_role_memberships_scope_idx on user_role_memberships(scope_type, scope_id);
```

---

## 3. OpenFGA model

```
model
  schema 1.1

type user

type platform
  relations
    define admin: [user]

type program
  relations
    define parent: [platform]
    define admin: [user] or admin from parent
    // future: define creator: [user]
    // future: define employer_partner: [user]

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
    define ta: [user]
    define learner: [user]

type submission
  relations
    define owner: [user]
    define cohort: [cohort]
    define grader: instructor from cohort or ta from cohort
    define viewer: owner or grader

type portfolio_item
  relations
    define owner: [user]
    // visibility checks done in app code against portfolio_items.visibility column

type announcement
  relations
    define platform_scope: [platform]
    define program_scope: [program]
    define cohort_scope: [cohort]
    define author: [user]
```

**Key tuples to write at signup time:**

```
// When a learner enrolls in a cohort:
write cohort:{cohort_id}#learner@user:{user_id}

// When an instructor is assigned to a cohort:
write cohort:{cohort_id}#instructor@user:{user_id}

// When NICHE platform admin is granted:
write platform:niche#admin@user:{user_id}
```

**Override pattern — instructor of A but learner of B:**

```
write cohort:cohort_A#instructor@user:user_X      // user is instructor in A
write cohort:cohort_B#learner@user:user_X         // user is learner in B
// no tuple at program level for user_X — so no over-inheritance
```

Permission check from app:

```typescript
// Can user_X edit content in course_A?
const allowed = await fga.check({
  user: 'user:user_X',
  relation: 'instructor',
  object: 'course:course_A',
})
// Returns true if user_X has instructor relation on course_A,
// OR admin relation on course_A's program (via from parent),
// OR admin relation on platform (via from parent of program).
```

---

## 4. Permission catalog (MVP)

| Permission key | Description | MVP holder (role × scope) |
|---|---|---|
| `course:content:view` | View course content (videos, readings, assignments brief) | Learner @ course (via enrollment), Instructor @ course, Admin @ platform |
| `course:content:edit` | Create/edit modules, sessions, assignments | Instructor @ course, Admin @ program, Admin @ platform |
| `course:content:publish` | Make content visible to learners | Instructor @ course (own course), Admin @ program |
| `course:roster:view` | View enrolled learner list with progress | Instructor @ course, Admin @ program, Admin @ platform |
| `course:assignment:submit` | Submit work to an assignment | Learner @ course (via enrollment) |
| `course:assignment:grade` | Grade a submission | Instructor @ course, TA @ course (subset) |
| `cohort:create` | Create a new cohort within a program | Admin @ program, Admin @ platform |
| `cohort:edit` | Edit cohort details, dates, capacity | Admin @ program, Admin @ platform |
| `cohort:roster:view` | View cohort roster | Instructor @ cohort, Admin @ program |
| `cohort:roster:manage` | Add/remove learners, change enrollment status | Admin @ program, Admin @ platform |
| `cohort:announcement:send` | Broadcast announcement to cohort | Instructor @ cohort, Admin @ program, Admin @ platform |
| `cohort:analytics:view` | View cohort analytics dashboard | Instructor @ cohort, Admin @ program, Admin @ platform |
| `program:create` | Create a new program | Admin @ platform |
| `program:edit` | Edit program details | Admin @ program, Admin @ platform |
| `program:announcement:send` | Send program-wide announcement | Admin @ program, Admin @ platform |
| `platform:user:manage` | Invite, deactivate, change roles | Admin @ platform |
| `platform:user:role:assign` | Grant or revoke roles | Admin @ platform |
| `platform:user:export` | Export user data (PDPA Right to Access) | Admin @ platform (logged) |
| `platform:user:delete` | Soft-delete user (PDPA Right to Erasure) | Admin @ platform (logged) |
| `platform:announcement:send` | Platform-wide announcement | Admin @ platform |
| `platform:analytics:view` | Platform-level analytics | Admin @ platform |
| `platform:settings:edit` | Edit org settings, integrations, brand | Admin @ platform |
| `portfolio:own:edit` | Edit own portfolio item | Learner (always, on items where owner = user) |
| `portfolio:own:visibility:set` | Set visibility (private/employer/public) | Learner (always, on own items) |
| `resume:own:generate` | Generate own resume PDF | Learner (always) |
| `certificate:own:download` | Download own certificate | Learner (always) |
| `certificate:verify:public` | Public verification page (no auth) | Anyone (public route) |

---

## 5. Migration phases

### Phase 1 — MVP (September 2026)

Roles seeded:
- `learner` (assigned via cohort enrollment)
- `instructor` (assigned via course/cohort assignment by Admin)
- `admin` (NICHE staff; platform scope)

OpenFGA model: as defined in §3. ~25 permissions in catalog.

### Phase 2 — Q1 2027 — TA + Creator (internal pilot)

Add roles:
- `ta` — subset of Instructor permissions (grade, view roster) but NOT content edit
- `creator` — `content:listing:publish` at platform scope (for vetted external content partners)

Migration:
1. Insert rows in `roles` table
2. Insert rows in `role_permissions` joining ta/creator to relevant permissions
3. Update OpenFGA model to add `creator` relation on `program` type
4. Issue role memberships to pilot users via `user_role_memberships` + OpenFGA tuples

Zero application code changes (assuming all checks already go through `can()`).

### Phase 3 — Q2 2027 — Employer Portal

Add role:
- `employer_partner` — `program:roster:view` (aggregate only, PDPA-gated), `program:certificate:verify`

New entities:
```
table employer_partners {
  id            uuid          primary key
  name          text          not null
  contact_email text          not null
  approved_at   timestamptz
  approved_by   uuid          references users(id)
}

table employer_inquiries {
  id            uuid          primary key
  employer_partner_id uuid    references employer_partners(id)
  to_user_id    uuid          references users(id)
  subject       text          not null
  body          text          not null
  status        enum('sent', 'accepted', 'declined', 'expired') default 'sent'
  created_at    timestamptz   default now()
}
```

Migration: schema additions only; no changes to existing tables.

### Phase 4 — 2027-2028 — Marketplace

Add type to OpenFGA:
```
type marketplace_listing
  relations
    define creator: [user]
    define reviewer: [user]
    define approved_by: [user]
```

Add `content.source = 'creator'` enum value to existing content tables (already nullable from day one; make explicit in MVP).

A new marketplace service subscribes to existing domain events (`content.submitted_for_review`, `content.approved`). No changes to course or enrollment code.

---

## 6. Domain events

Mutations emit events to a queue (BullMQ on Railway, Postgres-backed). Subscribers handle: notifications, analytics rollups, future marketplace features.

### Catalog (MVP)

```
user.created                 // Clerk webhook
user.role_granted            // user × role × scope
user.role_revoked
user.deleted                 // soft-delete

cohort.created
cohort.status_changed        // planning → open → running → completed
cohort.enrollment_opened
cohort.enrollment_closed

enrollment.applied
enrollment.accepted
enrollment.enrolled          // payment confirmed
enrollment.withdrawn
enrollment.completed

session.scheduled
session.attendance_recorded

assignment.created
submission.created
submission.graded
submission.returned

announcement.published

certificate.issued
certificate.revoked

payment.succeeded
payment.failed
payment.refunded

consent.granted
consent.withdrawn
data.exported               // PDPA Right to Access
data.deleted                // PDPA Right to Erasure
```

Subscribers:
- **Notifications** — listens to: deadline approaching, submission graded, announcement published, enrollment status changed
- **Analytics** — listens to: all session_attendance, submission, completion events
- **Email** — listens to: enrollment.accepted, payment.succeeded, certificate.issued, announcement.published (cohort scope)
- **Audit** — listens to: all events tagged sensitive (PII access, consent, role grants)
- **Future Marketplace** — will listen to: content.submitted_for_review, content.approved (no NICHE-side coupling needed)

---

## 7. Indexes + performance notes

- `submissions(cohort_id, status)` — instructor grading queue
- `sessions(cohort_id, starts_at)` — learner schedule (next 7 days)
- `enrollments(user_id, status)` — "my cohorts" view
- `notifications(user_id, read_at)` partial index where unread — bell badge count
- `portfolio_items(user_id, visibility, featured desc)` — public profile page
- `audit_events(actor_user_id, occurred_at desc)` — admin user-history view
- Materialized view `cohort_progress_summary` refreshed nightly — for analytics dashboard quick-load

---

## 8. Backup + retention

- Supabase daily backups + PITR (point-in-time recovery) → 7-day retention on Pro tier
- Manual backup before every schema migration (Drizzle migration tool runs in transaction)
- Audit events retention: 3 years (PDPA compliance baseline)
- Anonymized soft-deleted users retained 1 year (regulator/dispute window) then hard-deleted

---

## 9. Implementation checklist for dev team

Before Phase 1 dev kickoff:

- [ ] Validate this schema against PDF §4 features end-to-end
- [ ] Stand up OpenFGA in Docker locally
- [ ] Model the 4 critical permission scenarios in OpenFGA Playground:
  1. Learner accessing own course content
  2. Instructor grading a submission for cohort A but blocked from cohort B
  3. Admin overriding (platform admin → access any course)
  4. Employer partner viewing aggregated program data only (Phase 3 scenario, validate today)
- [ ] Decide ORM (Drizzle preferred, Prisma if team is junior to SQL)
- [ ] Decide auth provider (Clerk recommended; Better Auth as future-proof alternative)
- [ ] Write the `can()` abstraction first — single function all permission checks route through
- [ ] Generate Drizzle migrations; review with team; commit
- [ ] Seed minimal data: one platform admin, one program (one of NICHE's 12), one cohort, three test users
