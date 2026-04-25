# State Tracker Dashboard Guide

Your interactive Markov Chain state tracking dashboard is ready to use.

## 🚀 Quick Start

```bash
npm run dev
```

Then navigate to the **State Tracker** from the home menu.

## 📊 Dashboard Features

### 1. **Current State Display**
Shows your active cognitive state with:
- Large emoji/visual indicator
- Elapsed time in current state
- State description

### 2. **Suggested Next States**
Displays probabilistically optimal next states based on:
- Your current state
- Markov transition probabilities
- Feedback loop guards

**Example:**
- In Deep Focus? → Suggested: Recharge (recovery needed)
- In Recharge? → Suggested: Collaboration, Admin, or Learning

### 3. **Active Warnings**
Real-time detection of feedback loops with:
- **Severity levels** (HIGH, MEDIUM, LOW)
- **Icon indicators** for quick scanning
- **Specific warnings** (reflection paralysis, isolation, etc.)
- **Actionable recommendations**

Example warnings:
```
⚠️ REFLECTION_LOOP (HIGH SEVERITY)
   Planning paralysis detected: >45min in Reflection
   💡 Force transition to Deep Focus or Recharge
```

### 4. **Daily Time Allocation**
Live metrics showing:
- Total minutes per state
- Number of sessions
- Average session duration
- Sorted by time spent

### 5. **Today's Timeline**
Chronological view of all state transitions:
- Time of transition
- State entered
- Duration in state

### 6. **Daily Summary** (After tracking)
Overall statistics:
- Total time tracked
- Number of states visited
- Feedback loops detected
- Most common state

## 🎯 How to Use

### Starting Your Tracking

1. Click **State Tracker** from the home menu
2. Select your initial state (e.g., "🤔 Reflection" for morning planning)
3. Dashboard begins tracking elapsed time

### Making State Transitions

1. Complete work in current state
2. Dashboard suggests optimal next states (based on Markov model)
3. Click the suggested state to transition
4. Elapsed time resets, new state tracking begins

### Interpreting Warnings

**Reflection Loop** (>45 min planning)
- ⚠️ You're in analysis paralysis
- 💡 Action: Move to Deep Focus or Recharge immediately
- Why: Plans are ready; execution is next

**Recharge Loop** (>120 min alone)
- 🔋 Isolation risk detected
- 💡 Action: Transition to Collaboration or Learning
- Why: Extended isolation creates "dull stable state"

**Collaboration Avoidance** (>3 days without it)
- 👥 Missing energizing peer interaction
- 💡 Action: Schedule or initiate collaboration
- Why: Mentoring and peer work energizes you

### Exporting Logs

Click **📥 Export Daily Log** to download:
```json
{
  "date": "2026-04-25",
  "states": [
    {"state": "reflection", "duration_minutes": 15, "timestamp": "..."},
    {"state": "deep_focus", "duration_minutes": 90, "timestamp": "..."}
  ],
  "warnings": [
    {"type": "REFLECTION_LOOP", "severity": "HIGH", "message": "..."}
  ]
}
```

Use for:
- Weekly analysis
- Pattern recognition
- Optimization feedback
- Historical tracking

## 📈 Your State Transition Probabilities

```
Starting State    →  Next State         Probability
─────────────────────────────────────────────────
deep_focus       →  recharge           95%
deep_focus       →  transition         100% (always)

recharge         →  collaboration      50%
recharge         →  admin              30%
recharge         →  learning           20%

reflection       →  deep_focus         90%
reflection       →  recharge           85%

collaboration    →  recharge           80%

learning_input   →  reflection         60%
learning_input   →  deep_focus         40%
```

## 🛡️ Feedback Loop Guards in Action

### Guard 1: Reflection Paralysis
```
6:00 AM - Start Reflection (planning)
6:15 AM - Still in Reflection... OK
6:30 AM - Still in Reflection... OK
6:45 AM - ⚠️ WARNING: >45 min in Reflection
         Recommendation: Move to Deep Focus now
```

### Guard 2: Recharge Isolation
```
8:00 AM - Start Recharge
8:45 AM - Still recharging... OK
9:30 AM - Still recharging... OK
10:15 AM - ⚠️ WARNING: >2 hours in Recharge
          Recommendation: Transition to Collaboration or Learning
```

### Guard 3: Collaboration Avoidance
```
Monday - Have collaboration
Tuesday - No collaboration
Wednesday - No collaboration
Thursday - No collaboration
Friday - ⚠️ WARNING: No collaboration for >3 days
        Recommendation: Schedule peer interaction
```

## 💡 Real-World Examples

### Morning Optimal Flow
```
6:00-6:15   Reflection (morning planning)
6:15-8:00   Deep Focus (peak work block) - 105 min
8:00-9:00   Recharge (solo recovery)
9:00-10:00  Collaboration (scheduled meeting)
```
✅ No warnings | Maximum productivity

### Feedback Loop Triggered
```
6:00-6:15   Reflection ✓
6:15-6:45   Still Reflection (checking plan)
6:45-7:15   Still Reflection (analyzing more)
7:15        ⚠️ REFLECTION_LOOP WARNING
            Transition to Deep Focus needed
```
❌ Planning paralysis detected | Take action now

## 🔄 Daily Rhythm Alignment

Your ideal daily rhythm (from Markov model):

| Time | States | Goal | Feedback |
|------|--------|------|----------|
| 6:00-9:00 | Reflection → Deep Focus → Recharge | Prime focus block | Track: Are you in deep work? |
| 9:00-10:30 | Collaboration OR Admin | Meetings/logistics | Track: Scheduled? Unplanned? |
| 10:30-12:00 | Recharge + Learning | Recovery + growth | Track: Recharge duration |
| Afternoon | Flexible | Deep work or admin | Track: Avoiding isolation? |
| Evening | Reflection → Admin → Learning | Review & plan | Track: Reflection time <45min? |

## 📊 Weekly Analysis Checklist

Every Friday, review your logs:

- [ ] Total deep focus time: ___ hours (goal: 15-20/week)
- [ ] Reflection time average: ___ min (warning if >45 consecutive)
- [ ] Recharge sessions: ___ (goal: 1-2 per day)
- [ ] Collaboration days: ___ (goal: ≥3 days/week)
- [ ] Feedback loop incidents: ___ (goal: <2/week)
- [ ] Did you follow the ideal rhythm? ___% compliance
- [ ] What worked? What didn't?

## 🚨 Common Pitfalls

### ❌ "I'll Just Plan a Bit More"
- **Problem**: Reflection → Reflection loop
- **Guard**: Max 45 minutes
- **Solution**: When timer hits 45 min, forced transition to Deep Focus

### ❌ "I Need More Recovery Time"
- **Problem**: Recharge → Recharge loop
- **Guard**: Max 120 minutes
- **Solution**: After 2 hours, transition to Collaboration or Learning

### ❌ "I'm Too Busy for Meetings"
- **Problem**: Avoid Collaboration for >3 days
- **Guard**: Collaboration avoidance detection
- **Solution**: Schedule or initiate peer interaction

### ❌ "I Can't Track Everything"
- **Solution**: Start with just 3 states: Deep Focus, Recharge, Reflection
- **Grow**: Add Collaboration once the basic rhythm is solid

## 🔗 Integrating with Neo4j (Optional)

When you have Docker/Neo4j available:

```bash
# Start Neo4j locally
./scripts/setup-neo4j.sh

# Populate with your Markov model
npm run populate-markov

# Populate with your personal profile
npm run populate-graph
```

Then query your graph:
```cypher
MATCH (cs:CognitiveState)-[t:TRANSITIONS_TO]->(next:CognitiveState)
RETURN cs.label, t.probability, next.label
```

## 📱 Mobile Usage

The dashboard is mobile-responsive:
- Full functionality on phones
- Touch-friendly buttons
- Optimized view for small screens
- One-tap state transitions

## ⚡ Keyboard Shortcuts (Coming Soon)

Future enhancements:
- `R` → Transition to Recharge
- `D` → Transition to Deep Focus
- `C` → Transition to Collaboration
- `L` → Export log
- `ESC` → Back to menu

## 🎯 Success Metrics

You're using the tracker successfully if:

✅ Tracking daily state transitions  
✅ Responding to warnings before 45-min reflection limit  
✅ Getting 90+ minutes of uninterrupted deep focus  
✅ Taking 60-90 min recharge breaks  
✅ Collaboration happening 3+ days/week  
✅ Following ideal rhythm 70%+ of the time  

## 📚 Next Steps

1. **Start tracking today** - Use for 1-2 weeks
2. **Export weekly logs** - Analyze patterns
3. **Adjust thresholds** - Personalize the guards
4. **Build on it** - Integrate with calendar, tasks, goals
5. **Connect to Neo4j** - Persistent graph storage & queries

---

Questions? Review:
- [MARKOV_COGNITIVE_MODEL.md](./MARKOV_COGNITIVE_MODEL.md) - Core concepts
- [NEO4J_SETUP.md](./NEO4J_SETUP.md) - Database integration
- [personal-profile.json](../data/personal-profile.json) - Your profile data
