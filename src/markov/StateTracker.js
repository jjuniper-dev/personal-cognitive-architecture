// Markov Chain State Tracker for Personal Cognitive Architecture

class StateTracker {
  constructor() {
    this.currentState = null
    this.stateHistory = []
    this.stateStartTime = null
    this.dailyLog = {
      date: new Date().toISOString().split('T')[0],
      states: [],
      warnings: []
    }
  }

  transitionTo(newState) {
    const now = new Date()

    // Log current state if exists
    if (this.currentState) {
      const duration = Math.round((now - this.stateStartTime) / 60000) // minutes
      this.stateHistory.push({
        state: this.currentState,
        startTime: this.stateStartTime,
        endTime: now,
        duration_minutes: duration
      })

      this.dailyLog.states.push({
        state: this.currentState,
        duration_minutes: duration,
        timestamp: this.stateStartTime.toISOString()
      })
    }

    // Check for feedback loop risks
    this.checkFeedbackLoops(this.currentState, newState)

    // Transition to new state
    this.currentState = newState
    this.stateStartTime = now

    return {
      previous_state: this.stateHistory[this.stateHistory.length - 1]?.state || null,
      current_state: newState,
      timestamp: now.toISOString()
    }
  }

  checkFeedbackLoops(fromState, toState) {
    const now = new Date()
    const recentStates = this.stateHistory.slice(-10)

    // REFLECTION LOOP CHECK
    if (fromState === 'reflection' && toState === 'reflection') {
      const reflectionTime = this.stateHistory
        .filter(s => s.state === 'reflection')
        .slice(-1)
        .reduce((sum, s) => sum + s.duration_minutes, 0)

      if (reflectionTime > 45) {
        this.dailyLog.warnings.push({
          type: 'REFLECTION_LOOP',
          severity: 'HIGH',
          message: 'Planning paralysis detected: >45min in Reflection',
          recommendation: 'Force transition to Deep Focus or Recharge',
          timestamp: now.toISOString()
        })
        return 'REFLECTION_LOOP_WARNING'
      }
    }

    // REFLECTION → LEARNING LOOP (consumes planning time)
    if (fromState === 'reflection' && toState === 'learning_input') {
      const reflectionDuration = this.stateHistory[this.stateHistory.length - 1]?.duration_minutes || 0
      if (reflectionDuration > 30) {
        this.dailyLog.warnings.push({
          type: 'REFLECTION_LEARNING_LOOP',
          severity: 'MEDIUM',
          message: 'Reflection time consumed by learning input',
          recommendation: 'Skip to Deep Focus - you have a plan',
          timestamp: now.toISOString()
        })
      }
    }

    // RECHARGE ISOLATION CHECK
    if (fromState === 'recharge' && toState === 'recharge') {
      const rechargeTime = this.stateHistory
        .filter(s => s.state === 'recharge')
        .slice(-1)
        .reduce((sum, s) => sum + s.duration_minutes, 0)

      if (rechargeTime > 120) {
        this.dailyLog.warnings.push({
          type: 'RECHARGE_LOOP',
          severity: 'MEDIUM',
          message: 'Extended isolation: >120min in Recharge',
          recommendation: 'Transition to Collaboration or Learning',
          timestamp: now.toISOString()
        })
      }
    }

    // COLLABORATION AVOIDANCE CHECK
    if (!recentStates.some(s => s.state === 'collaboration')) {
      if (this.getDaysSinceState('collaboration') > 3) {
        this.dailyLog.warnings.push({
          type: 'COLLABORATION_AVOIDANCE',
          severity: 'LOW',
          message: 'No collaboration for >3 days',
          recommendation: 'Schedule or initiate peer interaction',
          timestamp: now.toISOString()
        })
      }
    }
  }

  getDaysSinceState(state) {
    const lastOccurrence = this.stateHistory
      .reverse()
      .find(s => s.state === state)

    if (!lastOccurrence) return Infinity

    const daysSince = Math.floor(
      (new Date() - lastOccurrence.endTime) / (1000 * 60 * 60 * 24)
    )
    return daysSince
  }

  getStateMetrics() {
    const metrics = {}

    for (const entry of this.stateHistory) {
      if (!metrics[entry.state]) {
        metrics[entry.state] = {
          count: 0,
          total_minutes: 0,
          average_duration: 0
        }
      }
      metrics[entry.state].count += 1
      metrics[entry.state].total_minutes += entry.duration_minutes
    }

    // Calculate averages
    for (const state in metrics) {
      metrics[state].average_duration = Math.round(
        metrics[state].total_minutes / metrics[state].count
      )
    }

    return metrics
  }

  getDailyLog() {
    return this.dailyLog
  }

  getRecommendedNextState(currentState) {
    const transitions = {
      'deep_focus': ['recharge', 'transition'],
      'recharge': ['collaboration', 'execution_admin', 'learning_input'],
      'reflection': ['deep_focus', 'recharge'],
      'collaboration': ['recharge'],
      'learning_input': ['reflection', 'deep_focus'],
      'execution_admin': ['deep_focus', 'learning_input'],
      'transition': ['recharge', 'deep_focus']
    }

    return transitions[currentState] || []
  }

  exportDailyLog(filename = null) {
    const filename_default = `cognitive-log-${this.dailyLog.date}.json`
    const data = JSON.stringify(this.dailyLog, null, 2)

    if (typeof window === 'undefined') {
      // Node.js environment
      const fs = require('fs')
      fs.writeFileSync(filename || filename_default, data)
      console.log(`📊 Daily log saved: ${filename || filename_default}`)
    } else {
      // Browser environment - download as file
      const blob = new Blob([data], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename || filename_default
      link.click()
      URL.revokeObjectURL(url)
    }

    return data
  }
}

export default StateTracker
