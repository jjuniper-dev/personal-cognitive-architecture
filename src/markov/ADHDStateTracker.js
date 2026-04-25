import StateTracker from './StateTracker'

// ADHD-specific enhancements to StateTracker

class ADHDStateTracker extends StateTracker {
  constructor() {
    super()

    // ADHD-specific tracking
    this.energyLevel = 'medium' // high, medium, low
    this.isHyperfocused = false
    this.hyperfocusStartTime = null
    this.ruminationDetected = false
    this.dopamineHits = 0
    this.contextSwitches = 0
    this.recoveryQuality = []
    this.rejectionSensitivityAlert = false

    // ADHD guard thresholds (adaptive)
    this.reflectionMaxTime = 45 // base threshold, will vary
    this.focusMaxTime = 90 // base, extends if hyperfocused
    this.rechargeMaxTime = 120

    // ADHD patterns (learned over time)
    this.hyperfocusTriggers = []
    this.energyVariance = {}
    this.ruminationPatterns = []
    this.recoveryNeeds = {}
  }

  setEnergyLevel(level) {
    if (!['high', 'medium', 'low'].includes(level)) {
      throw new Error('Energy level must be: high, medium, or low')
    }
    this.energyLevel = level
    return this.energyLevel
  }

  enableHyperfocus() {
    this.isHyperfocused = true
    this.hyperfocusStartTime = new Date()
    this.focusMaxTime = 150 // extend limit when hyperfocused

    console.log('🔥 Hyperfocus Mode ENABLED - do NOT interrupt!')
    return {
      status: 'hyperfocus_enabled',
      message: 'You are in hyperfocus. Flow state protected.',
      maxDuration: '150 minutes',
      exitMethod: 'User-triggered only'
    }
  }

  disableHyperfocus() {
    if (!this.isHyperfocused) return

    const hyperfocusDuration = Math.round(
      (new Date() - this.hyperfocusStartTime) / 60000
    )

    this.isHyperfocused = false
    this.hyperfocusStartTime = null
    this.focusMaxTime = 90 // reset to normal

    // Record hyperfocus for learning
    this.hyperfocusTriggers.push({
      duration: hyperfocusDuration,
      timestamp: new Date(),
      context: this.currentState
    })

    this.addDopamineHit('hyperfocus_completion', `Completed ${hyperfocusDuration}min hyperfocus session!`)

    return {
      status: 'hyperfocus_ended',
      duration: hyperfocusDuration,
      message: `Amazing! You hyperfocused for ${hyperfocusDuration} minutes!`,
      nextAction: 'Transition to Recharge for recovery'
    }
  }

  addDopamineHit(type, message) {
    this.dopamineHits += 1

    const hit = {
      type,
      message,
      timestamp: new Date(),
      currentState: this.currentState
    }

    if (!this.dailyLog.dopamine_hits) {
      this.dailyLog.dopamine_hits = []
    }
    this.dailyLog.dopamine_hits.push(hit)

    return {
      emoji: '🎉',
      points: 1,
      total: this.dopamineHits,
      message
    }
  }

  transitionToWithEnergy(newStateId, energyLevel) {
    // Transition with energy context
    this.setEnergyLevel(energyLevel)

    // Check if transition is energy-appropriate
    const transitionAdvice = this.getEnergyAwareTransitionAdvice(
      this.currentState,
      newStateId,
      energyLevel
    )

    if (transitionAdvice.warning) {
      this.dailyLog.warnings.push({
        type: 'ENERGY_MISMATCH',
        severity: 'MEDIUM',
        message: transitionAdvice.warning,
        recommendation: transitionAdvice.recommendation,
        timestamp: new Date().toISOString()
      })
    }

    return this.transitionTo(newStateId)
  }

  getEnergyAwareTransitionAdvice(fromState, toState, energyLevel) {
    // ADHD-specific: Energy requirements vary by state and level
    const energyRequirements = {
      deep_focus: { high: 'optimal', medium: 'possible', low: 'risky' },
      collaboration: { high: 'optimal', medium: 'optimal', low: 'risky' },
      reflection: { high: 'optimal', medium: 'optimal', low: 'paralysis_risk' },
      learning_input: { high: 'optimal', medium: 'optimal', low: 'possible' },
      recharge: { high: 'good', medium: 'needed', low: 'critical' },
      execution_admin: { high: 'good', medium: 'optimal', low: 'possible' },
      transition: { high: 'ok', medium: 'ok', low: 'ok' }
    }

    const suitability = energyRequirements[toState]?.[energyLevel]

    let warning = null
    let recommendation = null

    if (suitability === 'risky') {
      warning = `Energy level (${energyLevel}) risky for ${toState}`
      recommendation = `Try Recharge first, then retry ${toState}`
    } else if (suitability === 'paralysis_risk' && toState === 'reflection') {
      warning = 'Low energy + Reflection = rumination risk'
      recommendation = 'Do Recharge first, reflection later with fresh mind'
    } else if (suitability === 'critical' && toState === 'recharge') {
      recommendation = 'Critical: Take extended recharge (90+ min)'
    }

    return { warning, recommendation, suitability }
  }

  detectRumination(timeInReflection) {
    // ADHD rumination detection
    const ruminationThreshold = this.getAdaptiveReflectionLimit()

    if (timeInReflection > ruminationThreshold) {
      this.ruminationDetected = true

      const warning = {
        type: 'RUMINATION_LOOP',
        severity: 'HIGH',
        message: `Rumination detected: ${timeInReflection}min in Reflection`,
        recommendation: 'STOP. Transition to movement or recharge NOW.',
        timestamp: new Date().toISOString()
      }

      this.dailyLog.warnings.push(warning)

      // Record for learning
      this.ruminationPatterns.push({
        duration: timeInReflection,
        dayOfWeek: new Date().getDay(),
        time: new Date().getHours(),
        energyLevel: this.energyLevel,
        timestamp: new Date()
      })

      return warning
    }

    this.ruminationDetected = false
    return null
  }

  getAdaptiveReflectionLimit() {
    // ADHD: Reflection time varies by context
    const dayOfWeek = new Date().getDay()
    const hour = new Date().getHours()

    let baseLimit = 45

    // Friday fatigue: shorter limit
    if (dayOfWeek === 5) {
      baseLimit = 35
    }
    // Morning: longer limit (fresh mind)
    else if (hour < 10) {
      baseLimit = 50
    }
    // Late afternoon: shorter (ADHD fatigue)
    else if (hour > 16) {
      baseLimit = 35
    }

    // Energy-aware adjustment
    if (this.energyLevel === 'low') {
      baseLimit -= 10
    } else if (this.energyLevel === 'high') {
      baseLimit += 5
    }

    this.reflectionMaxTime = Math.max(25, baseLimit) // never below 25 min

    return this.reflectionMaxTime
  }

  rateRecoveryQuality(rating) {
    // 1-5 scale: how good was that recharge?
    if (rating < 1 || rating > 5) {
      throw new Error('Recovery quality must be 1-5')
    }

    const recovery = {
      rating,
      timestamp: new Date(),
      state: this.currentState,
      energyBefore: this.energyLevel
    }

    this.recoveryQuality.push(recovery)

    // Learn: what recovery duration works best?
    if (!this.recoveryNeeds[this.energyLevel]) {
      this.recoveryNeeds[this.energyLevel] = []
    }
    this.recoveryNeeds[this.energyLevel].push(rating)

    const avgRating = (
      this.recoveryNeeds[this.energyLevel].reduce((a, b) => a + b, 0) /
      this.recoveryNeeds[this.energyLevel].length
    ).toFixed(1)

    return {
      recorded: true,
      message: `Recovery quality: ${rating}/5`,
      averageQuality: `${avgRating}/5 for ${this.energyLevel} energy`,
      recommendation:
        rating < 3 ? 'Try longer recharge next time' : 'Great recovery!'
    }
  }

  checkRejectionSensitivity(triggerEvent) {
    // ADHD trait: Rejection sensitivity
    // Detect when in Reflection after critical feedback
    if (this.currentState === 'reflection' && triggerEvent === 'criticism') {
      this.rejectionSensitivityAlert = true

      const warning = {
        type: 'REJECTION_SENSITIVITY',
        severity: 'HIGH',
        message: 'Reflection + criticism = rumination risk (ADHD pattern)',
        recommendation:
          'Take 5-min movement break now. Revisit this after recharge.',
        timestamp: new Date().toISOString()
      }

      this.dailyLog.warnings.push(warning)
      return warning
    }

    this.rejectionSensitivityAlert = false
    return null
  }

  getTaskInitiationSupport(taskType) {
    // ADHD: Task initiation difficulty
    // Provide dopamine-boosting support

    const initiationTricks = {
      deep_focus: '2-minute rule: Just start for 2 min, then decide',
      collaboration: 'Join call 2 min early, ease in',
      learning_input: 'Pick ONE resource only',
      reflection: 'Set timer for 30 min max upfront',
      recharge: 'Pick activity NOW before deciding',
      execution_admin: 'Chunk into 15-min blocks, reward after each'
    }

    const advice = initiationTricks[taskType]

    return {
      taskType,
      initiationTrick: advice,
      message: '💪 You can do this. Just start.',
      reward: 'One dopamine point when you start!'
    }
  }

  getTimeBlindnessAlert() {
    // ADHD: Time blindness
    // Alert when time has passed unexpectedly

    const timeInState = this.stateHistory.length > 0
      ? this.stateHistory[this.stateHistory.length - 1].duration_minutes
      : 0

    if (timeInState > 60 && timeInState % 30 === 0) {
      // Every 30 minutes after 1 hour
      return {
        alert: 'Time check!',
        elapsed: `${timeInState} minutes have passed`,
        currentState: this.currentState,
        message: 'Does your body agree with the timer?'
      }
    }

    return null
  }

  getHyperfocusPreservationRule() {
    // ADHD: Hyperfocus is RARE and valuable
    // Protect it at all costs

    if (!this.isHyperfocused) {
      return null
    }

    return {
      status: 'HYPERFOCUS_ACTIVE',
      rule: '🔥 DO NOT INTERRUPT. All guards suspended.',
      duration: Math.round(
        (new Date() - this.hyperfocusStartTime) / 60000
      ),
      exitOnly: 'User-triggered (your choice to stop)',
      message: 'This is magic. Protect it. Exit only when you choose.'
    }
  }

  getADHDDailyMetrics() {
    // ADHD-specific metrics that matter
    const totalFocusTime = this.stateHistory
      .filter(s => s.state === 'deep_focus')
      .reduce((sum, s) => sum + s.duration_minutes, 0)

    const totalRechargeTime = this.stateHistory
      .filter(s => s.state === 'recharge')
      .reduce((sum, s) => sum + s.duration_minutes, 0)

    const avgRecoveryQuality =
      this.recoveryQuality.length > 0
        ? (
            this.recoveryQuality.reduce((sum, r) => sum + r.rating, 0) /
            this.recoveryQuality.length
          ).toFixed(1)
        : 'N/A'

    const ruminationIncidents = this.dailyLog.warnings.filter(
      w => w.type === 'RUMINATION_LOOP'
    ).length

    return {
      dopamineHits: this.dopamineHits,
      contextSwitches: this.contextSwitches,
      focusTime: totalFocusTime,
      rechargeTime: totalRechargeTime,
      recoveryQuality: avgRecoveryQuality,
      ruminationIncidents,
      hyperfocusSessions: this.hyperfocusTriggers.length,
      totalWarnings: this.dailyLog.warnings.length,
      goals: {
        focusTime: '90+ minutes',
        dopamineHits: '3+ hits',
        contextSwitches: '<5 per day',
        ruminationIncidents: '0',
        recoveryQuality: '4+/5'
      }
    }
  }

  getADHDRecommendations() {
    // Smart recommendations based on ADHD patterns

    const metrics = this.getADHDDailyMetrics()
    const recommendations = []

    if (metrics.focusTime < 60) {
      recommendations.push({
        icon: '🎯',
        message: 'Deep focus time is low. Try hyperfocus mode next session.',
        priority: 'HIGH'
      })
    }

    if (metrics.ruminationIncidents > 0) {
      recommendations.push({
        icon: '⚠️',
        message: 'Rumination detected multiple times. Shorter reflection limits needed.',
        priority: 'HIGH'
      })
    }

    if (metrics.recoveryQuality < 3) {
      recommendations.push({
        icon: '🔋',
        message: 'Recharge quality is low. Try different recovery activities.',
        priority: 'MEDIUM'
      })
    }

    if (metrics.contextSwitches > 6) {
      recommendations.push({
        icon: '🔄',
        message: 'Too many context switches. Block out focus time without interruptions.',
        priority: 'MEDIUM'
      })
    }

    if (metrics.dopamineHits < 2) {
      recommendations.push({
        icon: '🎉',
        message: 'Need more dopamine hits. Celebrate small wins!',
        priority: 'LOW'
      })
    }

    return recommendations
  }

  exportADHDLog(filename = null) {
    const filename_default = `adhd-cognitive-log-${this.dailyLog.date}.json`

    const adhd_log = {
      ...this.dailyLog,
      adhd_metrics: this.getADHDDailyMetrics(),
      adhd_warnings: this.dailyLog.warnings.filter(w =>
        ['RUMINATION_LOOP', 'REJECTION_SENSITIVITY', 'ENERGY_MISMATCH'].includes(
          w.type
        )
      ),
      recommendations: this.getADHDRecommendations(),
      hyperfocus_sessions: this.hyperfocusTriggers,
      recovery_quality: this.recoveryQuality,
      rumination_patterns: this.ruminationPatterns,
      dopamine_hits: this.dailyLog.dopamine_hits || []
    }

    const data = JSON.stringify(adhd_log, null, 2)

    if (typeof window === 'undefined') {
      // Node.js
      const fs = require('fs')
      fs.writeFileSync(filename || filename_default, data)
      console.log(`📊 ADHD log saved: ${filename || filename_default}`)
    } else {
      // Browser
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

export default ADHDStateTracker
