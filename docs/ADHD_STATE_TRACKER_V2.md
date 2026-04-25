# ADHD StateTracker v2.0 Documentation

StateTracker v2.0 is designed by and for ADHD brains. It recognizes ADHD as a neurodevelopmental difference that requires different tools, not willpower.

## 🧠 ADHD-Specific Design Principles

### 1. **Hyperfocus is Sacred**
- Can't be interrupted by arbitrary time limits
- Toggle manually when you feel it
- Protected state: no guards applied
- Celebrated when you exit (dopamine hit!)

### 2. **Energy is Variable**
- Not all hours are equal
- Energy level drives task suitability
- Guards adjust based on energy
- Recovery needs are tracked

### 3. **Rumination ≠ Reflection**
- Reflection is planning (good)
- Rumination is looping (dangerous)
- ADHD executive dysfunction trap
- Adaptive guards prevent it

### 4. **Dopamine Matters**
- Motivation comes from visible wins
- Celebrate small completions
- Track "hits" not just metrics
- Gamification is functional, not frivolous

### 5. **Time Blindness is Real**
- Alarms at regular intervals
- Not to shame, to inform
- "Has it really been 45 minutes?"
- Checks without judgment

## 🎯 Core Features

### 1. **Energy Level Tracking**

Not about mood, about task capacity.

```
HIGH ENERGY ⚡⚡⚡
- Perfect for: Deep Focus, Collaboration, Challenging Work
- Safe for: Admin, Learning
- Risky for: Nothing (use this time!)

MEDIUM ENERGY ⚡⚡
- Perfect for: Most tasks
- Safe for: Any work except high-risk
- Risky for: Extended Reflection (paralysis risk)

LOW ENERGY ⚡
- Safe for: Recharge, Admin, Light Input
- Risky for: Deep Focus, Collaboration, Reflection
- Guard: Reflection limit drops to 35 min
- Recommendation: Recharge first
```

**How to use:**
```javascript
tracker.setEnergyLevel('low')
tracker.transitionToWithEnergy('reflection', 'low')
// Returns advice: "Low energy + Reflection = rumination risk"
```

### 2. **Hyperfocus Mode** 🔥

The superpower. Protect it.

```javascript
// In Deep Focus, feeling immersed?
tracker.enableHyperfocus()

// System now:
// ✓ Removes time limits (150 min instead of 90 min)
// ✓ Ignores reflection guards
// ✓ Protects the flow state
// ✗ Only exits when YOU choose

// When you're done:
tracker.disableHyperfocus()
// Returns: "Amazing! You hyperfocused for 127 minutes!"
// + Automatic dopamine hit
```

**Why this matters:**
- ADHD hyperfocus is rare and valuable
- Interrupting it costs hours of recovery time
- Most productivity systems destroy hyperfocus
- This one protects it

### 3. **Adaptive Reflection Guards**

Prevents planning paralysis and analysis loops.

**Base threshold: 45 minutes**
**Adjusts based on:**
- Day of week (Friday: 35 min - end-of-week fatigue)
- Time of day (Morning: 50 min - fresh mind; Afternoon: 35 min)
- Energy level (Low: -10 min; High: +5 min)
- Never below 25 minutes

```javascript
// Friday afternoon, low energy
const limit = tracker.getAdaptiveReflectionLimit()
// Returns: 25 minutes (conservative)

// Monday morning, high energy
const limit = tracker.getAdaptiveReflectionLimit()
// Returns: 55 minutes (generous)
```

**Detects rumination:**
```javascript
tracker.detectRumination(50) // 50 minutes in reflection
// Returns: RUMINATION_LOOP warning
// Message: "Stop. Transition to movement or recharge NOW."
```

### 4. **Rejection Sensitivity Detection**

Catches the ADHD trap: criticism → rumination → paralysis

```javascript
tracker.checkRejectionSensitivity('criticism')
// Detects: In Reflection + just received criticism
// Warning: "Reflection + criticism = rumination risk"
// Recommendation: "5-min movement break now. Revisit after recharge."
```

### 5. **Task Initiation Support**

ADHD struggle: starting tasks, not completing them.

```javascript
const help = tracker.getTaskInitiationSupport('deep_focus')
// Returns: "2-minute rule: Just start for 2 min, then decide"

const help = tracker.getTaskInitiationSupport('execution_admin')
// Returns: "Chunk into 15-min blocks, reward after each"
```

**Supports:**
- 2-minute rule (just start)
- Chunking (break into micro-tasks)
- Pre-easing (join call early)
- Resource limiting (one thing only)

### 6. **Recovery Quality Tracking**

Not all rest is equal. Track what actually helps.

```javascript
// After Recharge state:
tracker.rateRecoveryQuality(4) // 1-5 scale
// System learns:
// "Medium energy + 75 min recharge = 4/5 quality"
// "Low energy + 60 min recharge = 2/5 quality"
// 
// Recommends: "Try longer recharge next time for low energy"
```

### 7. **Dopamine Hits** 🎉

Track wins, not just time.

```javascript
// Task completed
tracker.addDopamineHit('task_completed', 'Finished that email!')
// Count: 1

// Had a breakthrough
tracker.addDopamineHit('breakthrough', 'Figured out the algorithm!')
// Count: 2

// Hyperfocus session ended
// (auto-added)
// Count: 3
```

**Goal: 3+ hits per day**
- Sustains motivation
- Makes progress visible
- Combats ADHD motivation deficit

### 8. **Time Blindness Alerts**

No shaming, just checking in.

```javascript
// After 60 minutes in any state:
// Every 30 minutes, get an alert:
// "⏰ Time check! 90 minutes have passed."
// "Does your body agree with the timer?"
```

**Purpose:**
- Inform without interrupting
- Reality-check against internal sense of time
- Prepare for transitions

## 📊 ADHD-Specific Metrics

Standard StateTracker metrics + ADHD insights:

```javascript
const metrics = tracker.getADHDDailyMetrics()
// Returns:
{
  dopamineHits: 5,           // Wins today
  contextSwitches: 4,        // Lower is better
  focusTime: 165,            // Minutes
  rechargeTime: 120,         // Minutes
  recoveryQuality: 4.2,      // Average rating
  ruminationIncidents: 1,    // Should be 0
  hyperfocusSessions: 2,     // Rare and precious
  totalWarnings: 2,          // ADHD-specific alerts
  
  goals: {
    focusTime: '90+ minutes',
    dopamineHits: '3+ hits',
    contextSwitches: '<5 per day',
    ruminationIncidents: '0',
    recoveryQuality: '4+/5'
  }
}
```

## 🚨 ADHD-Specific Warnings

### High Severity
- **RUMINATION_LOOP**: >45 min (or adaptive limit) in Reflection
  - Action: Stop. Transition to Recharge or movement.
  - Why: Planning paralysis, executive dysfunction

- **REJECTION_SENSITIVITY**: Reflection after criticism
  - Action: 5-min break. Revisit with fresh mind.
  - Why: ADHD trait + rumination = hours lost

### Medium Severity
- **ENERGY_MISMATCH**: Low energy trying high-demand task
  - Action: Do Recharge first, then retry
  - Why: Will drain faster, increase crash risk

- **RECHARGE_ISOLATION**: >120 min in Recharge
  - Action: Transition to Collaboration or Learning
  - Why: Extended isolation becomes "dull stable state"

## 🤖 Smart Recommendations

Automatic coaching based on patterns:

```javascript
const recommendations = tracker.getADHDRecommendations()
// Examples:
[
  {
    icon: '🎯',
    message: 'Deep focus time is low. Try hyperfocus mode next session.',
    priority: 'HIGH'
  },
  {
    icon: '⚠️',
    message: 'Rumination detected multiple times. Shorter reflection limits needed.',
    priority: 'HIGH'
  },
  {
    icon: '🔋',
    message: 'Recharge quality is low. Try different recovery activities.',
    priority: 'MEDIUM'
  },
  {
    icon: '🔄',
    message: 'Too many context switches. Block out focus time without interruptions.',
    priority: 'MEDIUM'
  },
  {
    icon: '🎉',
    message: 'Need more dopamine hits. Celebrate small wins!',
    priority: 'LOW'
  }
]
```

## 💾 ADHD Log Export

Everything saved for analysis:

```json
{
  "date": "2026-04-25",
  "adhd_metrics": {
    "dopamineHits": 5,
    "focusTime": 165,
    "ruminationIncidents": 0,
    "hyperfocusSessions": 2,
    "recoveryQuality": 4.2
  },
  "adhd_warnings": [
    {"type": "RUMINATION_LOOP", "severity": "HIGH", ...},
    {"type": "ENERGY_MISMATCH", "severity": "MEDIUM", ...}
  ],
  "recommendations": [...],
  "hyperfocus_sessions": [
    {"duration": 127, "timestamp": "..."},
    {"duration": 95, "timestamp": "..."}
  ],
  "recovery_quality": [
    {"rating": 4, "energyBefore": "low", ...},
    {"rating": 2, "energyBefore": "low", ...}
  ],
  "dopamine_hits": [
    {"type": "task_completed", "message": "Email done", ...},
    {"type": "hyperfocus_completion", "message": "127min session!", ...}
  ]
}
```

## 🎯 Daily Usage Pattern

### Morning
```
1. Set energy level
2. Transition to Reflection (planning)
3. If ready: enable Hyperfocus → Deep Focus
4. Guard: 45 min max reflection
```

### After Focus Block
```
1. Rate energy level
2. Transition to Recharge
3. Rate recovery quality
4. Prepare for next block
```

### Midday
```
1. Check energy
2. Collaboration or Admin (if energy allows)
3. Short recharge
4. Optional: second focus block
```

### Evening
```
1. Light Reflection (review day)
2. Admin (emails, logistics)
3. Learning (skill building)
4. Dopamine count: did you hit 3+ wins?
```

## 📈 Weekly Review Checklist

Every Friday:
- [ ] Hyperfocus sessions: ___ (goal: 2+)
- [ ] Rumination incidents: ___ (goal: 0)
- [ ] Dopamine hits: ___ (goal: 15+)
- [ ] Recovery quality average: ___ (goal: 4+/5)
- [ ] Context switches per day: ___ (goal: <5)
- [ ] Energy crashes: ___ (goal: <2)
- [ ] What worked? (pattern recognition)
- [ ] What didn't? (adjust next week)

## 🔄 Compared to Standard StateTracker

| Feature | Standard | ADHD v2.0 |
|---------|----------|-----------|
| Time limits | Fixed | Adaptive + respects hyperfocus |
| Energy tracking | No | Yes, with task recommendations |
| Rumination detection | Basic | Advanced + rejection sensitivity |
| Recovery tracking | No | Quality ratings + learning |
| Dopamine gamification | Minimal | Central (dopamine hits tracked) |
| Task initiation help | No | Yes, with specific tactics |
| Time blindness alerts | No | Yes, informative not shaming |
| Hyperfocus support | Generic | Protected, celebrated, extended |
| Rejection sensitivity | No | Detected and handled |

## 🚀 Implementation Notes

### State Preservation
- Hyperfocus state persists across state transitions
- Energy level context applies to all states
- Guards adapt in real-time

### Recommendations Engine
- Learns from your actual patterns over time
- Adapts to individual ADHD expression
- Acknowledges: "No two ADHD brains are the same"

### Recovery Quality Learning
- Tracks: Duration + Energy level before → Quality rating
- Example: "45 min recharge after high focus = 2/5"
- "75 min recharge after high focus = 4/5"
- Learns YOUR optimal recovery formula

## ⚠️ Important Notes

### This is NOT
- A replacement for professional ADHD support
- A replacement for medication if you take it
- A cure or "fix" for ADHD
- A way to force productivity

### This IS
- A system designed WITH ADHD in mind
- Honoring how ADHD brains actually work
- Protecting your rare superpowers (hyperfocus)
- Preventing common ADHD traps (rumination, paralysis)
- Making progress visible (dopamine support)

### When to Seek Help
- If rumination incidents consistently >3/week
- If you can't access hyperfocus
- If dopamine hits drop below 2/day
- If recovery quality stays <2/5
- If rejection sensitivity is preventing work

---

**Remember:** Your ADHD brain isn't broken. Standard tools are designed for neurotypical brains. This tool is designed for you.

🎯 **Goal: Stop fighting your brain and start working with it.**
