# Personal OS Profiler Guide

## Overview

This guide walks you through diagnosing your Personal OS profile and integrating it into your PCA's control plane for task routing, AI augmentation, and cognitive hygiene enforcement.

---

## Part 1: Self-Diagnosis (1-2 hours)

### Step 1: Prepare
1. **Block 90 minutes** of uninterrupted time
2. **Quiet environment** — minimize distractions
3. **Pen and paper** or digital notes (you'll record observations)
4. **Review the last 2-3 weeks** of work — examples will help

### Step 2: Work Through Each Dimension

Use the diagnostic questions in `personal-os-system-spec.md` Section 7.

For each dimension (Attention Model, Processing Mode, Decision Style, Energy Profile, Structure Tolerance, Social Bandwidth):

1. Read the three diagnostic questions
2. **Record your answer** (A, B, or C) for each question
3. **Add a real-world example** from your recent work that illustrates your answer
4. **Note any uncertainty** — some people have hybrid patterns

### Step 3: Score

For each dimension:
- Count which answer (A, B, or C) appears most
- That's your **default OS** for that dimension
- If it's split, note that you have a **hybrid pattern** (e.g., "parallel-leaning-sequential")

**Example result**:
```
Attention Model: Sequential (A, A, A)
Processing Mode: Internal (A, B, A) ← hybrid, but internal-leaning
Decision Style: Deliberative (B, B, C)
Energy Profile: Burst (B, B, A) ← mostly burst
Structure Tolerance: Medium (B, B, B)
Social Bandwidth: Low (A, A, A)
```

### Step 4: Validate Against Recent Patterns

Look back at the last 2 weeks. Do these results match your real behavior?

- **If yes**: Proceed to Step 5
- **If no**: Revisit the diagnostic questions. You might have misunderstood or have a hybrid pattern.

### Step 5: Collect Observational Data

Track these signals for 3-5 working days:

| Signal | How to Measure | Goal |
|--------|----------------|------|
| **Context switches** | How many times do you switch tasks per hour? | Validate attention model |
| **Meeting fatigue** | Hours of meetings before you feel drained? | Validate social bandwidth |
| **Decision time** | How long do you typically spend before deciding on a significant question? | Validate decision style |
| **Energy curve** | Plot your energy 1-10 across the day; is it steady, spiky, or volatile? | Validate energy profile |
| **Processing preference** | When stuck, do you talk it out, write it, or think alone? | Validate processing mode |

**Simple tracking method**: Create a notes file and record observations as they happen.

```
Monday 9am: Started deep work on X. Got interrupted 4 times in 2 hours (need sequential).
Tuesday 2pm: Back-to-back meetings 1-5pm. Drained afterward (low social bandwidth).
Wednesday 3pm: Asked for feedback. Took 2 hours to think, then decided (deliberative).
```

### Step 6: Refine

Based on the 3-5 day observational data, does your profile need adjustment?

- **No change**: Profile is solid. Proceed to Part 2.
- **Minor adjustment**: Update one or two dimensions. Document why.
- **Major shift**: You may need to re-profile. This is normal; some patterns take weeks to surface.

---

## Part 2: Structured Profile (30-45 minutes)

### Create Your Profile JSON

Use `schemas/personal-os-profile.schema.json` as a template.

```json
{
  "name": "Your Name",
  "date_profiled": "2025-04-25",
  "personal_os": {
    "attention_model": "sequential",
    "processing_mode": "internal",
    "decision_style": "deliberative",
    "energy_profile": "burst",
    "structure_tolerance": "medium",
    "social_bandwidth": "low"
  },
  "firmware_notes": {
    "baseline_energy_level": "high",
    "sensory_sensitivity": "high",
    "introversion_extroversion": "introverted"
  },
  "native_workloads": [
    "deep_work",
    "meta_work"
  ],
  "adapted_workloads": [
    "routine_execution",
    "creative_exploration"
  ],
  "emulated_workloads": [
    "interrupt_driven",
    "collaborative_work"
  ],
  "daily_compute_budget": 480,
  "context_switch_tolerance": 3,
  "meeting_density_tolerance": 3,
  "recovery_time_ratio": 1.5,
  "notes": "Protect focus time for deep work. Batch meetings into 2-hour blocks with recovery after."
}
```

**Key fields to complete**:

1. **native_workloads**: Types of work where your OS is naturally aligned (low cost)
2. **adapted_workloads**: Types of work with medium cost (manageable mismatch)
3. **emulated_workloads**: Types of work with high cost (unsustainable long-term)
4. **daily_compute_budget**: Total cognitive minutes available (default 480 for 8-hour day)
5. **context_switch_tolerance**: How many context switches per hour before degradation?
6. **meeting_density_tolerance**: How many consecutive meeting hours before recovery needed?
7. **recovery_time_ratio**: Hours of recovery per hour of emulated work (e.g., 1.5 = 90 min recovery per hour worked)

---

## Part 3: Build Your Workload Map (30-45 minutes)

### Map Your Current Roles/Responsibilities

For each major workload type you regularly face:

1. **Identify the workload type** (deep_work, collaborative_work, interrupt_driven, etc.)
2. **Check OS compatibility** using `schemas/workload-compatibility.schema.json`
3. **Assess cost** using `schemas/cognitive-cost-model.schema.json`
4. **Document current allocation** (e.g., "40% of my time is interrupt-driven")

**Example**:

| Workload | Compatibility | Current Time | Cost | Sustainable? |
|----------|---|---|---|---|
| Deep work (systems design) | Native | 20% | Low | Yes |
| Team meetings | Adapted | 30% | Medium | Yes (if batched) |
| Interrupt support (Slack, on-call) | Emulated | 25% | High | No—unsustainable |
| Routine tasks | Adapted | 25% | Medium | Yes |

**Insight from this analysis**:
- You're spending 25% of time on unsustainable work
- This explains end-of-week fatigue and decision degradation
- **Recommendation**: Reduce interrupt-driven work to <10%, or add AI augmentation

### Calculate Your Cognitive Budget

Use the cost breakdown from your workload map:

```
Daily Budget = 480 compute-minutes

Deep work (20% = 1.6 hours): 60 min/hr × 1.6 = 96 minutes
Team meetings (30% = 2.4 hours): 80 min/hr × 2.4 = 192 minutes  
Interrupt support (25% = 2 hours): 120 min/hr × 2 = 240 minutes
Routine tasks (25% = 2 hours): 70 min/hr × 2 = 140 minutes

Total = 96 + 192 + 240 + 140 = 668 minutes

OVER BUDGET by 188 minutes / day (39% overspend)
```

**What this means**: You're spending 39% more cognitive energy than you have. This manifests as:
- End-of-day fatigue
- Decision paralysis
- Reduced work quality
- Need for extended recovery (weekends, time off)

---

## Part 4: Design Workload Adjustments (1-2 hours)

Based on your cognitive budget analysis, adjust your workload mix.

### Option A: Reduce Emulated Work

Move interrupt-driven work to someone else or change how it's handled.

```
Reduction: 25% → 10% (1.5 hours/day instead of 2 hours)
Cost savings: 120 × 0.5 = 60 compute-minutes/day
New budget total: 668 - 60 = 608 minutes (within 480 budget by consolidation)
```

**Implementation**: 
- Batch interrupt handling into two 45-minute windows (10-10:45am, 3-3:45pm)
- Outside those windows, async-only (email, docs)
- Critical only: reach out directly

### Option B: Add AI Augmentation

Use AI to reduce the cost of emulated workloads.

**Deep work + AI**:
- AI handles research synthesis while you focus on core problem
- Cost reduction: 15-20%

**Interrupt-driven + AI**:
- AI triages and batches interrupts; you review decisions
- Cost reduction: 40-50%

**Example**: With AI augmenting interrupt-driven work:
```
Interrupt-driven: 25% at full cost = 240 minutes
Interrupt-driven: 25% with 50% AI reduction = 120 minutes  
Savings: 120 compute-minutes/day
New total: 668 - 120 = 548 minutes
```

### Option C: Shift OS Temporarily

For unavoidable mismatched work, consciously shift your OS for the duration.

**Example**: For a 3-day intense collaborative event:
- **Normal mode** (sequential, internal): Meeting days would cost 80 × 3 × 8 = 1,920 minutes for the week
- **Temporary shift** (parallel, external): Reduce context switch cost, increase social energy temporarily
- **Cost with shift**: 60 × 3 × 8 = 1,440 minutes (25% savings)
- **Trade-off**: Requires 2-3 days recovery after; plan for it

---

## Part 5: Enable Cognitive Hygiene Agent (30 minutes)

Once your profile is defined, configure the Cognitive Hygiene Agent in your PCA control plane.

### Create Hygiene Rules

For your unique OS, define enforcement rules:

```json
{
  "hygiene_rules": [
    {
      "monitor": "context_switches",
      "threshold": ">3 per hour",
      "your_os": "sequential",
      "action": "block_new_tasks",
      "notification": "Context switching detected. Protect your focus?"
    },
    {
      "monitor": "meeting_density",
      "threshold": ">3 hours consecutive",
      "your_social_bandwidth": "low",
      "action": "suggest_break",
      "duration": "30 minutes alone"
    },
    {
      "monitor": "interrupt_rate",
      "threshold": ">10 per hour",
      "your_os_fit": "emulated",
      "action": "activate_ai_triage",
      "effect": "AI batches interrupts; you review async"
    },
    {
      "monitor": "daily_overbudget",
      "threshold": ">50% of budget spent",
      "action": "suggest_workload_reduction",
      "options": [
        "Defer non-urgent tasks",
        "Add AI augmentation",
        "Extend deadline"
      ]
    }
  ]
}
```

### Integrate into PCA Control Plane

The Cognitive Hygiene Agent becomes a filter in your PCA's task routing:

```
[Incoming Task]
  ↓
[Hygiene Agent Checks]
  - Is current workload within OS-fit?
  - Would adding this exceed budget?
  - Are there active constraints (recovery time, meeting density)?
  ↓
[Three Outcomes]
  1. ACCEPT → Route to executor
  2. CONDITION → Accept if: add AI support, defer lower priority, etc.
  3. DEFER → Recommend reschedule or delegation
```

**Implementation in n8n/control plane**:

Use your Personal OS profile as a data source for routing decisions:

```
IF task.type = "collaborative" AND 
   daily_meeting_hours > meeting_density_tolerance AND
   not task.critical
THEN
  route = "defer_queue"
  message = "You've hit your meeting capacity for today. Schedule for tomorrow?"
```

---

## Part 6: Monitoring and Iteration (Ongoing)

### Weekly Reflection (15 minutes)

Every Friday, review:
- Did you stay within your daily compute budget?
- Which workloads felt most aligned with your OS?
- Which felt misaligned or exhausting?
- Did the Cognitive Hygiene Agent's recommendations help?

**Track in a note**:
```
Week of Apr 21:
- Mon-Wed: Mostly deep work + meetings. Energy good.
- Thu-Fri: Interrupt-driven support kicked in. Hit thermal stress >8.
- Insight: Interrupt-driven work still costs too much. Need more batching or AI support.
```

### Quarterly Rebase (1-2 hours)

Every 3 months, re-run the profiler:

1. **Re-answer diagnostic questions** (Section 7 of spec)
2. **Compare to last quarter** — has your OS shifted?
3. **Validate against monitoring data** — does the data align?
4. **Update your profile** if needed
5. **Adjust workload map and hygiene rules**

**Why quarterly?**
- OS can shift due to life changes, role changes, or sustained workload patterns
- Recovery patterns improve with practice
- New tools or workflows might change cost structure

### Annual Review (2-3 hours)

Once a year:

1. **Reflect on the full year** — major patterns, shifts, insights
2. **Assess which workloads improved** — which got worse?
3. **Document firmware observations** (Section 1.2) — have baseline characteristics shifted?
4. **Update your profiler guide** based on what you learned
5. **Share your Personal OS** with your team/manager for collaborative design

**Example output**:
```
Annual Review 2025:

Attention Model: Still sequential, but more comfortable with short bursts of parallel work
Processing Mode: More external; discovered I think better when writing in real-time
Decision Style: Still deliberative, but can batch-decide faster with clear criteria
Energy Profile: Volatile → more balanced; systematic recovery improved stability
Structure Tolerance: Medium → high; I adapt better than I used to

Implication: Role design should shift toward:
- More writing/externalization
- Clearer decision frameworks (reduces deliberation time)
- Fewer recovery days needed

New risks:
- Parallel work increasing; may need more batching
```

---

## Part 7: Integration Examples

### Example 1: Task Routing in n8n

**Trigger**: New task arrives

```javascript
// Get user's Personal OS profile
const userOS = await getPersonalOSProfile(userId);

// Determine workload type and cost
const taskCost = calculateCost(task.type, userOS);

// Check budget
const dailyUsed = await getDailyComputeUsed(userId, today);
const remainingBudget = userOS.daily_compute_budget - dailyUsed;

// Route based on fit
if (taskCost.native) {
  // Native fit: highest priority
  route = "high_priority";
} else if (taskCost.adapted && taskCost.compute < remainingBudget) {
  // Adapted fit: medium priority, check budget
  route = "medium_priority";
} else if (taskCost.emulated) {
  // Emulated fit: offer AI augmentation
  route = "ai_augmentation";
  message = "This task doesn't fit your OS well. AI augmentation available?";
} else {
  // Over budget
  route = "deferred";
  message = "You're at budget limit. Suggest deferring or adding AI support.";
}
```

### Example 2: Meeting Scheduler Constraint

**Rule**: Respect social bandwidth

```
IF person.social_bandwidth = "low" THEN
  - Max consecutive meeting hours = person.meeting_density_tolerance
  - Block recovery time after meetings
  - Async-first default for <8 people
  
Example:
User has 3-hour meeting 1-4pm.
System auto-blocks 4-5pm for recovery.
New meeting request for 4:30pm → suggest 5pm or next day instead.
```

### Example 3: AI Augmentation Trigger

**Rule**: When OS-workload fit is poor, suggest AI

```
Scenario: User assigned to interrupt-driven on-call duty (emulated fit)
Current status: Already used 400 of 480 budget for the day

Action:
1. Alert: "On-call duty usually costs 120 min/hr. You have 80 min left."
2. Offer: "AI can triage incoming requests, reducing cost by ~50%."
3. Implementation: "AI reviews all Slack messages, drafts response, you approve."
4. Result: On-call cost drops from 120 to 60 min/hr; now sustainable.
```

---

## Troubleshooting

### "My profile changed mid-way through"

This is normal. Work stress, life changes, or new tools can shift your OS temporarily.

**Action**: 
- Note what changed and when
- Continue with the current profile for the quarter
- Re-profile next quarter; look for the shift

### "I have a hybrid pattern (e.g., sequential-leaning-parallel)"

This is also normal. Many people are hybrid.

**Action**:
- List both modes: "sequential (70%), parallel (30%)"
- Workload design: 70% of tasks should be sequential, 30% can be parallel
- Monitor which mode feels sustainable longer

### "My workload doesn't fit any native mode"

If all your current work is adapted or emulated:

**Options**:
1. Discuss with manager about role redesign
2. Add AI augmentation to reduce costs
3. Delegate or outsource emulated work
4. Accept the energy cost, plan recovery

**This is a red flag** — unsustainable long-term. Address in the next 1-2 quarters.

### "The Cognitive Hygiene Agent's rules are too restrictive"

Adjust thresholds based on your experience.

**Example**: 
- Rule said: "Defer if >4 meetings"
- In practice: You handle 5-6 meetings fine, but crash on day 6
- New rule: "Warn at >5, defer at >6, auto-block at 7"

Rules should be **guardrails**, not handcuffs. Calibrate to your reality.

---

## Checklist

- [ ] Part 1: Self-diagnosis complete; profile identified
- [ ] Part 2: JSON profile created and validated
- [ ] Part 3: Current workload map documented
- [ ] Part 4: Workload adjustments planned
- [ ] Part 5: Cognitive Hygiene Agent rules configured
- [ ] Part 6: Monitoring process established (weekly review template created)
- [ ] Part 7: Integration with PCA control plane tested
- [ ] Profile shared with team/manager for collaborative design

---

## Next Steps

1. **This quarter**: Run through Parts 1-5. Enable cognitive hygiene monitoring.
2. **Ongoing**: Weekly reflections; track what's working and what's not.
3. **Next quarter**: Rebase your profile. Iterate on workload adjustments.
4. **Year 1**: Build organizational muscle around Personal OS-aware task design.

Your Personal OS is now part of your PCA's operational DNA. Use it.
