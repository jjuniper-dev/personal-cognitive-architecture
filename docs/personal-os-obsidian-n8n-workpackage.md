# Personal OS Implementation — Obsidian & n8n Work Package

## Overview

Implement your Personal OS operationally using Obsidian (knowledge management) and n8n (workflow automation).

This work package transforms your Personal OS from specification to daily practice.

---

## Part 1: Obsidian Work Package

### What Obsidian Does in Your PCA

```
Capture (raw input)
  ↓
[Obsidian Inbox] — Raw, unprocessed notes
  ↓
Design (mental models)
  ↓
[Obsidian Design Vault] — Systems, architectures, designs
  ↓
Reconciliation (contradictions)
  ↓
[Obsidian Models] — Updated beliefs, reconciled contradictions
  ↓
Execution (action)
  ↓
[Obsidian Projects] — What's being built, status, blockers
```

### Folder Structure

```
Personal OS Vault/
├── 00 Inbox/
│   ├── Capture (unprocessed items)
│   ├── Metadata:
│   │   - timestamp: when captured
│   │   - source: where from (Slack, email, voice, etc.)
│   │   - cognitive_state: current state (fresh, fatigued, anxious)
│   │   - urgency: signal, routine, or noise
│   └── Example: "2025-04-25 0915 [Slack] Question about auth system.md"
│
├── 01 Design/
│   ├── Active Projects/
│   │   ├── System Architecture (current focus)
│   │   ├── Authentication Redesign
│   │   └── Data Pipeline v2
│   ├── Design Templates/
│   │   ├── System Design Template
│   │   ├── Decision Log Template
│   │   └── Assumption Tracker
│   └── Metadata:
│       - status: active, paused, completed
│       - os_fit: native (your strongest work)
│       - layers: 1-4 (how many abstraction layers)
│       - cognitive_load: low/medium/high
│
├── 02 Models/
│   ├── System Architectures/
│   │   ├── Authentication (v3.2, trusted)
│   │   ├── Data Pipeline (v2, in execution)
│   │   └── API Standards (v1, trusted)
│   ├── Decision Framework/
│   │   ├── Technology Choices
│   │   └── Architectural Decisions
│   ├── Contradictions (being reconciled)/
│   │   ├── API standards vs. legacy system
│   │   └── Performance assumptions vs. real data
│   └── Metadata:
│       - status: trusted, under review, needs reconciliation
│       - last_updated: date
│       - version: model version
│
├── 03 Execution/
│   ├── Current Sprint/
│   │   ├── Sprint Backlog (items in progress)
│   │   ├── Blockers (items needing resolution)
│   │   └── Completed (shipped items)
│   ├── Sprint Retrospectives/
│   │   └── What we learned (feeds reconciliation)
│   └── Metadata:
│       - status: in_progress, blocked, completed
│       - os_fit: native/adapted/emulated
│       - blocker_escalation: if blocked, why?
│
├── 04 Personal OS/
│   ├── Profile Summary (your current OS)
│   ├── Daily Schedule (meeting days vs. no-meeting days)
│   ├── Hygiene Rules (constraints you enforce)
│   ├── Mode State (current mode: design/capture/execution/reconciliation)
│   ├── System Health (pending, trusted, needs reconciliation counts)
│   ├── Weekly Reviews (Friday reflections)
│   └── Quarterly Rebases (profile updates)
│
├── 05 Knowledge/
│   ├── Patterns (recurring insights)
│   ├── Tools & Frameworks
│   ├── Team Standards
│   └── Best Practices
│
└── 99 Archive/
    ├── Completed Projects
    ├── Old Designs (v1, v2)
    └── Deprecated Models
```

### Daily Workflows in Obsidian

#### Morning (6am): Enter Design Mode

**Action**:
1. Open `04 Personal OS/Mode State.md`
2. Set: `Current Mode: Design`
3. Open `04 Personal OS/Daily Schedule.md`
4. Check: Is today a meeting day or no-meeting day?
5. If no-meeting day: Go to `01 Design/Active Projects/` → Open today's focus
6. If meeting day: Note meeting time and recovery block in schedule

**File created**: Today's design session note
- Title: `2025-04-25 Design Session - [Topic]`
- Location: `01 Design/Active Projects/[Project Name]/`
- Metadata: Start time, expected duration, abstraction layers needed

#### 10am: Design → Capture Transition

**Action**:
1. Save design state (document what you designed, assumptions, flags)
2. Update `01 Design/[Project]/Decision Log` with today's design decisions
3. Open `04 Personal OS/Mode State.md` → Set: `Current Mode: Capture`
4. Move to `00 Inbox/` — inbox items are waiting

**Governance applied** (at transition):
- What did I design today?
- What assumptions did I make?
- What needs reconciliation?
- What's the next step?

#### 10am-12pm: Capture Mode

**Action**:
1. Process inbox items one by one
2. For each item:
   - Read it (no judgment)
   - Tag: `#signal`, `#routine`, `#noise`, `#urgent`
   - Add: source, timestamp, cognitive_state
   - Move to temporary holding folder

**No analysis yet. Just triage.**

#### 12pm: Triage

**Action**:
1. Open `04 Personal OS/System Health.md`
2. Sort inbox by urgency:
   - `#urgent` → Needs design review (flag for next design session)
   - `#signal` → Feeds models (flag for reconciliation)
   - `#routine` → Can be batched (schedule for specific time)
   - `#noise` → Archive

**Update counts**: Pending signals, routine items, urgent items

#### 1pm: Enter Execution Mode

**Action**:
1. Open `03 Execution/Current Sprint/`
2. Check: What did I design this morning or yesterday?
3. Open the design document
4. Follow the design; execute
5. If blocker: Flag it (don't try to re-design)

**Metadata**: Record what was completed, what was blocked, why

#### 3pm-5pm: Recovery / Light Work

**Action**:
1. If fatigued: Read `04 Personal OS/System Health.md` (visible state)
2. If recovered: Continue light execution or process routine items
3. Update `04 Personal OS/Mode State.md` → Set: `Current Mode: Off`

#### Friday 2pm: Weekly Review

**Action**:
1. Open `04 Personal OS/Weekly Review - Week of [Date].md`
2. Answer:
   - Did I protect 6-10am every day? (If no, why?)
   - Did I exceed 1 context switch/hour? (When?)
   - Did I hit 2-3 meetings max? (Yes/No)
   - How many items moved from inbox → design?
   - How many designs → execution?
   - What contradictions emerged?
3. Note: What's working? What needs adjustment?

**File created**: Weekly review (guides monthly reflection)

#### Monthly: System Health Dashboard

**Create**: `04 Personal OS/Monthly Review - April 2025.md`

**Contents**:
```
## Capture Health
- Inbox start: 23 items
- Inbox end: 3 items
- Items processed: 20
- Status: Good (staying current)

## Design Health
- Active projects: 3
- Completed designs: 2
- Blocked designs: 1 (why?)
- Status: Good pace

## Execution Health
- Sprint 1: 8 completed, 3 blocked
- Sprint 2: 5 in progress
- Status: On track

## Reconciliation Health
- Contradictions flagged: 3
- Contradictions resolved: 1
- Models updated: 2
- Status: Need to address 2 remaining

## OS Health
- Protected 6-10am: 18/20 days ✓
- Meeting days: 2 (target: 2-3) ✓
- Anxiety level: Moderate (improved)
- Phone usage spikes: Only 2 days
- Status: System is working

## Next month adjustments
- Continue current approach
- Add: Monthly model audit
```

### Essential Templates

#### Design Session Template

```markdown
---
title: Design Session - [Topic]
date: YYYY-MM-DD
mode: design
os_fit: native
layers: 4
status: in_progress
---

## Goal
What's the one design question?

## Current State
- Existing model/system: ...
- Known constraints: ...
- Assumptions: ...

## Design Thinking
### Layer 4: Strategic Intent
Why are we doing this? What's the goal?

### Layer 3: Architecture
How do major components fit?

### Layer 2: Design Patterns
What patterns help us achieve this?

### Layer 1: Implementation
What are API contracts, data structures?

## Decisions Made
- Decision 1: ...
- Decision 2: ...

## Assumptions Flagged
- Assumption A: (needs validation)
- Assumption B: (needs validation)

## Next Steps
- What's the next design session?
- What's ready for execution?

## Reconciliation Items
- Any contradictions found?
- Any models that need updating?
```

#### Weekly Review Template

```markdown
---
title: Weekly Review - Week of YYYY-MM-DD
---

## Personal OS Health
### Constraints Met
- Protected 6-10am: X/5 days ✓
- Meetings: X per week ✓
- Context switches: Average X/hour
- Meeting anxiety: (low/moderate/high)

### Violations
- Broke 6-10am on Monday (why?)
- Had X context switches Thursday (why?)

## Workload Routing
- Items captured: X
- Items designed: X
- Items executed: X
- Items blocked: X (why?)

## Signals & Contradictions
- New signals: (list)
- Contradictions emerged: (list)
- Models affected: (list)

## Adjustments for Next Week
- Continue: (what's working)
- Start: (new approach)
- Stop: (what's not working)

## Trend
(Is the system getting easier or harder?)
```

### Implementation Steps

**Week 1: Vault Setup**
- [ ] Create folder structure above
- [ ] Create Personal OS profile note in `04 Personal OS/`
- [ ] Create daily schedule template (meeting vs. no-meeting days)
- [ ] Create mode state tracker
- [ ] Create system health dashboard template

**Week 2: Daily Workflows**
- [ ] Create `01 Design/Active Projects/[Your First Project]`
- [ ] Start using design session template
- [ ] Start processing inbox items (tag them)
- [ ] Document first daily cycle (capture → triage → execute)

**Week 3: Tracking**
- [ ] Create weekly review template
- [ ] First weekly review (Friday)
- [ ] Monthly review template

---

## Part 2: n8n Work Package

### What n8n Does in Your PCA

```
Personal OS Profile (Obsidian)
  ↓
[n8n Reads Profile]
  ↓
[Task Arrives]
  ↓
[n8n Classifies Workload Type]
  ↓
[n8n Checks OS-Fit]
  ↓
[Routing Decision]
  ├─ High Priority (native fit)
  ├─ Medium Priority (adapted fit)
  ├─ AI Augmentation (emulated fit)
  └─ Deferred (budget exceeded)
  ↓
[Notification to User]
  ↓
[Update System Health in Obsidian]
```

### 5 Core n8n Workflows

#### Workflow 1: Task Classification & Routing

**Trigger**: New task arrives (via Slack, email, or manual input)

**Steps**:
1. **Read input**: 
   - Task description
   - Urgency
   - Context
   
2. **Load Personal OS profile** from Obsidian data/personal-os-profile.json
   - Attention model: sequential
   - Meeting limit: 2-3/week
   - Context switch tolerance: 1/hour
   - Current date/time
   
3. **Classify workload type**:
   - Is this deep_work? → design
   - Is this routine_execution? → execution
   - Is this meeting/collaborative? → meeting (check meeting count)
   - Is this interrupt_driven? → flag for batching
   
4. **Check OS-fit**:
   - Look up workload type in workload-compatibility.schema.json
   - Get required OS dimensions
   - Compare to user's actual OS
   - Calculate fit: native/adapted/emulated
   
5. **Check constraints**:
   - Is it a meeting? Check: meetings this week < 3? (If yes, allow; if no, defer)
   - Is it async work? Check: cognitive budget available?
   - Is it urgent? Override budget check
   
6. **Make routing decision**:
   ```
   IF fit == "native" THEN route = "high_priority"
   IF fit == "adapted" AND budget_available THEN route = "medium_priority"
   IF fit == "emulated" THEN offer = "AI_augmentation"
   IF budget_exceeded THEN route = "deferred"
   ```
   
7. **Send notification**:
   ```
   Slack message:
   "[Task]: Classification Complete
   
   Workload Type: deep_work
   OS-Fit: NATIVE ✓ (energizing work)
   Route: High Priority
   Action: Schedule for 6-10am tomorrow
   Cost: 60 min/hr (within budget)"
   ```
   
8. **Update Obsidian**:
   - Add task to appropriate backlog
   - Update system health counts
   - Log classification decision

**Frequency**: Every task (real-time)

---

#### Workflow 2: Meeting Load Monitoring

**Trigger**: Daily at 8am (check weekly meeting count)

**Steps**:
1. **Query calendar** (Google Calendar, Outlook, or ICS file):
   - Get all meetings for current week
   - Filter out optional meetings
   - Count: meetings so far + meetings scheduled
   
2. **Check against limit**:
   - Target: 2-3 meetings/week
   - If count >= 3: WARN
   - If count >= 4: ESCALATE
   
3. **Check meeting density today**:
   - Any back-to-back meetings?
   - Consecutive hours > 2?
   - If yes: FLAG recovery block
   
4. **Send notification**:
   ```
   IF meetings_this_week >= 3:
     "⚠️ Meeting Load: You're at 3 meetings this week.
      New meeting requests should be declined or moved to async.
      Last meeting today: 2pm → 4pm recovery blocked."
   ```
   
5. **Update Obsidian**:
   - Add to `04 Personal OS/System Health.md`
   - Meeting count: X/3
   - Recovery blocks scheduled: Y

**Frequency**: Daily at 8am, or whenever meeting is added to calendar

---

#### Workflow 3: Cognitive Hygiene Enforcement

**Trigger**: Every 30 minutes during work hours (6am-5pm)

**Steps**:
1. **Sample cognitive state**:
   - How many Slack switches in last 30 min?
   - How many calendar events overlapped work blocks?
   - Current time vs. design window (6-10am)?
   - User self-reported stress level (optional prompt)
   
2. **Check constraints**:
   ```
   IF time == 3pm-5pm AND mode == "deep_work":
     ALERT: "Your overstimulation boundary (3pm) is approaching.
             Consider wrapping up or switching to light work."
   
   IF context_switches > 3 in last hour:
     ALERT: "High context switching detected (X switches/hour).
             Complete current task, then take a break."
   
   IF meeting_hours_consecutive > meeting_density_tolerance:
     ALERT: "Recovery time needed. 30-min solo work blocked on calendar."
   
   IF daily_compute_used > 75% of budget:
     ALERT: "Approaching daily cognitive budget. Save complex tasks for tomorrow."
   ```
   
3. **Take action**:
   - Block calendar if recovery needed
   - Send alerts to Slack
   - Log violations to Obsidian
   
4. **Update Obsidian**:
   - Add to daily log: violations, triggers, actions taken
   - Update cognitive state tracker

**Frequency**: Every 30 minutes (background, non-intrusive)

---

#### Workflow 4: Daily Schedule Generator

**Trigger**: 5:30am each morning

**Steps**:
1. **Check calendar**:
   - How many meetings scheduled today?
   - What time are they?
   
2. **Determine schedule type**:
   - 0 meetings → "No-Meeting Day" schedule
   - 1 meeting → "Single Meeting Day" schedule
   - 2+ meetings → "Multi-Meeting Day" schedule
   
3. **Generate daily schedule**:
   ```
   NO-MEETING DAY:
   6:00am  - Design Mode starts (6-10am protected)
   10:00am - Capture Mode (triage inbox)
   12:00pm - Lunch (break)
   1:00pm  - Execution Mode (implement design)
   3:00pm  - Recovery/Light Work (or stop)
   5:00pm  - OFF
   
   SINGLE MEETING DAY (meeting at 11am):
   6:00am  - Design Mode (pre-meeting focus)
   10:45am - Pre-meeting ritual (grounding)
   11:00am - MEETING
   12:00pm - POST-MEETING RECOVERY (walk, light admin)
   1:00pm  - Continue recovery or light execution
   4:00pm  - Review recovery status
   5:00pm  - OFF
   ```
   
4. **Push to calendar**:
   - Add time blocks to Google Calendar
   - Color-coded by mode (design = blue, recovery = yellow, etc.)
   - Block all calendar for focus time
   
5. **Send notification**:
   ```
   "Today's Schedule:
    No-meeting day ✓
    6-10am: Design window protected
    10am-12pm: Triage 8 inbox items
    1-3pm: Execute design from yesterday"
   ```

**Frequency**: Every morning at 5:30am

---

#### Workflow 5: System Health Dashboard Update

**Trigger**: Friday 2pm (weekly review time)

**Steps**:
1. **Collect data**:
   - Meetings this week: X (target: 2-3)
   - 6-10am protected: X/5 days
   - Context switch violations: X (target: 0)
   - Cognitive budget overages: X days
   - Anxiety level: Low/Moderate/High
   - Tasks processed: X
   
2. **Calculate health scores**:
   ```
   Constraints Met: (X/10) * 100%
   Meeting Load: (meetings / 3) * 100%
   Focus Protection: (protected_days / 5) * 100%
   Budget Adherence: (within_budget_days / 5) * 100%
   ```
   
3. **Update Obsidian dashboard**:
   - `04 Personal OS/System Health.md`
   - Add weekly snapshot
   - Track trends (improving/declining)
   
4. **Generate summary report**:
   ```
   "Week of 2025-04-21:
    
    Constraints: 85% ✓
    - Meetings: 2/3 ✓
    - 6-10am protected: 4/5 ✓ (broken Mon, why?)
    - Context switches: Good (avg 1.2/hr)
    
    Cognitive Health: Good
    - Anxiety: Moderate (improved from last week)
    - Budget adherence: 4/5 days ✓
    - Fatigue at 3pm: As expected
    
    Work Completed:
    - 12 items captured
    - 3 designs completed
    - 8 items executed
    - 1 blocked (why?)
    
    Adjustments for Next Week:
    - Protect Monday 6-10am (recurring meeting)
    - Consider batching routine tasks on Wednesday"
   ```

**Frequency**: Weekly, every Friday at 2pm

---

### n8n Setup Checklist

#### Phase 1: Foundation (Week 1)

- [ ] Install n8n locally or connect to cloud instance
- [ ] Create Obsidian integration (read/write access to vault)
- [ ] Load `personal-os-profile.json` as reference data
- [ ] Test: Can n8n read your Personal OS profile?

#### Phase 2: Core Workflows (Week 2-3)

- [ ] **Workflow 1**: Task Classification & Routing
  - [ ] Create webhook for new tasks (Slack, email, or manual)
  - [ ] Implement workload classification (LLM-based or rules-based)
  - [ ] Test with 5 sample tasks
  - [ ] Connect to Obsidian (log classifications)

- [ ] **Workflow 4**: Daily Schedule Generator
  - [ ] Read Google Calendar
  - [ ] Generate morning schedule based on meeting count
  - [ ] Push schedule back to calendar (color-coded blocks)
  - [ ] Send daily 5:30am notification

#### Phase 3: Monitoring (Week 4)

- [ ] **Workflow 2**: Meeting Load Monitoring
  - [ ] Daily 8am check of meeting count
  - [ ] Alerts if >= 3 meetings scheduled
  - [ ] Recovery block calendar insertion

- [ ] **Workflow 3**: Cognitive Hygiene (sampling)
  - [ ] 30-min sampling of context switches
  - [ ] Alerts for violations
  - [ ] Logging to Obsidian

#### Phase 4: Analytics (Week 5)

- [ ] **Workflow 5**: System Health Dashboard
  - [ ] Weekly data collection
  - [ ] Health score calculation
  - [ ] Summary report generation
  - [ ] Update `04 Personal OS/System Health.md`

---

### Implementation Templates

#### n8n Workflow: Task Classification (Simplified)

```javascript
// Pseudocode for n8n workflow

// Input: Task description
const task = {
  description: "Design authentication system",
  urgency: "medium",
  context: "Q2 security improvement"
};

// Load Personal OS
const os = loadFromObsidian("data/personal-os-profile.json");

// Classify
const workloadType = classifyTask(task.description); // deep_work

// Check fit
const fit = checkOSFit(workloadType, os.personal_os);
// fit = "native" (sequential attention + design-strong = good fit)

// Check constraints
const meetsConstraints = {
  meetingCount: getCurrentWeekMeetings() <= 3,
  budgetAvailable: getRemainingBudget() > 60,
  contextSwitches: getLastHourSwitches() < 1
};

// Route
if (fit === "native" && meetsConstraints.budgetAvailable) {
  route = "HIGH_PRIORITY";
  message = "Schedule for 6-10am peak focus window";
} else if (fit === "adapted" && meetsConstraints.budgetAvailable) {
  route = "MEDIUM_PRIORITY";
  message = "Can handle, but not ideal. Consider batching.";
} else {
  route = "DEFERRED or AI_AUGMENTATION";
  message = "OS-fit is poor. Defer or get AI support.";
}

// Notify
sendSlack(`Task: ${task.description}\nRoute: ${route}\nReason: ${message}`);

// Log
appendToObsidian("00 Inbox/", {
  task: task.description,
  workload_type: workloadType,
  os_fit: fit,
  routing: route,
  timestamp: now()
});
```

---

## Part 3: Integration Points (Obsidian ↔ n8n)

### Data Flow

```
Personal OS Profile (JSON)
  ↓ (n8n reads daily)
Task Classification Engine
  ↓
Routing Decision
  ↓
Obsidian Update (via n8n)
  ├─ Backlog updated
  ├─ System health updated
  └─ Daily log updated
  ↓
Weekly Review (Obsidian manual)
  ↓
Monthly Rebase (Obsidian manual)
  ↓
Profile Updated (JSON)
  ↓ (cycle repeats)
```

### Obsidian Files That n8n Reads

- `data/personal-os-profile.json` — Your current OS and constraints
- `04 Personal OS/Daily Schedule.md` — Meeting count for the week
- `04 Personal OS/Mode State.md` — What mode you're currently in

### Obsidian Files That n8n Writes

- `00 Inbox/[Task].md` — New tasks get logged here
- `04 Personal OS/System Health.md` — Daily/weekly updates
- `04 Personal OS/Daily Log.md` — Hourly constraint checks

---

## Part 4: Getting Started (This Week)

### Day 1-2: Obsidian Setup

```
1. Create vault folder structure (copy from above)
2. Create: 04 Personal OS/Profile Summary.md
   - Paste your personal-os-profile.json content as markdown table
3. Create: 04 Personal OS/Daily Schedule.md
   - No-meeting day template
   - Meeting day template
4. Create: 04 Personal OS/Mode State.md
   - Current mode: OFF
5. Test: Can you find all key files easily?
```

### Day 3: First Design Session

```
1. Monday 6am: Open Obsidian
2. Check: Is today a meeting day? (Check calendar)
3. Open: 01 Design/Active Projects/[Your First Project]/
4. Create: Design Session note (use template above)
5. Start designing (6-10am uninterrupted)
6. At 10am: Save and document decisions
7. Move to: 00 Inbox/ for triage
```

### Day 4-5: n8n Basics

```
1. Install/access n8n
2. Create simple test workflow:
   - Trigger: Manual test
   - Action: Read obsidian/personal-os-profile.json
   - Output: Confirm profile loaded
3. Next: Build Task Classification workflow
```

### Week 2: Full System Running

```
- Obsidian: Daily use (design → capture → execute → review)
- n8n: 2-3 core workflows (classification, schedule, monitoring)
- Integration: n8n updating Obsidian automatically
```

---

## Key Files to Create This Week

```
✓ Obsidian:
  - 04 Personal OS/Profile Summary.md
  - 04 Personal OS/Daily Schedule.md
  - 04 Personal OS/System Health.md
  - 01 Design/Active Projects/[Your Project]/
  - Weekly Review Template
  
✓ n8n:
  - Task Classification workflow (test)
  - Daily Schedule workflow (test)
  
✓ Automation:
  - n8n → Obsidian integration tested
```

This gives you operational Personal OS (Obsidian) + automated constraint enforcement (n8n) in 2 weeks.

Start with Obsidian workflows. Once you have the daily practice, add n8n automation.
