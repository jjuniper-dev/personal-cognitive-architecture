import React, { useState, useEffect } from 'react'
import ADHDStateTracker from '../markov/ADHDStateTracker'
import './ADHDTrackerDashboard.css'

const STATES = [
  { id: 'deep_focus', label: '🎯 Deep Focus', color: '#667eea', emoji: '🎯' },
  { id: 'recharge', label: '🔋 Recharge', color: '#48bb78', emoji: '🔋' },
  { id: 'reflection', label: '🤔 Reflection', color: '#f6ad55', emoji: '🤔' },
  { id: 'collaboration', label: '👥 Collaboration', color: '#ed64a6', emoji: '👥' },
  { id: 'learning_input', label: '📚 Learning', color: '#4299e1', emoji: '📚' },
  { id: 'execution_admin', label: '✅ Admin', color: '#9f7aea', emoji: '✅' },
  { id: 'transition', label: '🔄 Transition', color: '#38b2ac', emoji: '🔄' }
]

const TRANSITIONS = {
  deep_focus: ['recharge', 'transition'],
  recharge: ['collaboration', 'execution_admin', 'learning_input', 'reflection'],
  reflection: ['deep_focus', 'recharge'],
  collaboration: ['recharge', 'reflection'],
  learning_input: ['reflection', 'deep_focus', 'execution_admin'],
  execution_admin: ['deep_focus', 'learning_input', 'reflection'],
  transition: ['recharge', 'deep_focus']
}

export default function ADHDTrackerDashboard() {
  const [tracker] = useState(new ADHDStateTracker())
  const [currentState, setCurrentState] = useState(null)
  const [energyLevel, setEnergyLevel] = useState('medium')
  const [isHyperfocused, setIsHyperfocused] = useState(false)
  const [stateHistory, setStateHistory] = useState([])
  const [metrics, setMetrics] = useState({})
  const [warnings, setWarnings] = useState([])
  const [dopamineHits, setDopamineHits] = useState(0)
  const [elapsedTime, setElapsedTime] = useState(0)
  const [recoveryRating, setRecoveryRating] = useState(0)
  const [recommendations, setRecommendations] = useState([])

  const stateConfig = STATES.find(s => s.id === currentState) || {}
  const availableTransitions = TRANSITIONS[currentState] || []
  const availableStates = availableTransitions
    .map(id => STATES.find(s => s.id === id))
    .filter(Boolean)

  // Update elapsed time
  useEffect(() => {
    const interval = setInterval(() => {
      setElapsedTime(prev => prev + 1)

      // Time blindness alert every 30 minutes after 1 hour
      const alert = tracker.getTimeBlindnessAlert()
      if (alert) {
        console.log('⏰ TIME BLINDNESS ALERT:', alert)
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [tracker])

  const handleStateTransition = (newStateId) => {
    // Check energy-aware advice
    tracker.transitionToWithEnergy(newStateId, energyLevel)
    setCurrentState(newStateId)
    setStateHistory(tracker.stateHistory)
    setMetrics(tracker.getStateMetrics())
    setWarnings(tracker.getDailyLog().warnings)
    setRecommendations(tracker.getADHDRecommendations())
    setElapsedTime(0)
    setRecoveryRating(0)

    // Time blindness check
    const timeAlert = tracker.getTimeBlindnessAlert()
    if (timeAlert) {
      console.log('Time check:', timeAlert)
    }
  }

  const handleEnergeLevelChange = (level) => {
    tracker.setEnergyLevel(level)
    setEnergyLevel(level)
  }

  const toggleHyperfocus = () => {
    if (isHyperfocused) {
      const result = tracker.disableHyperfocus()
      setIsHyperfocused(false)
      setDopamineHits(tracker.dopamineHits)
      alert(`🔥 ${result.message}\n${result.nextAction}`)
    } else {
      tracker.enableHyperfocus()
      setIsHyperfocused(true)
    }
  }

  const addDopamineHit = (type) => {
    const hit = tracker.addDopamineHit(type, `Completed ${type}!`)
    setDopamineHits(tracker.dopamineHits)
    return hit
  }

  const submitRecoveryRating = () => {
    if (recoveryRating === 0) return

    const result = tracker.rateRecoveryQuality(recoveryRating)
    alert(`${result.message}\n${result.recommendation}`)
    setRecoveryRating(0)
  }

  const getTaskInitiationHelp = () => {
    if (!currentState) return null
    return tracker.getTaskInitiationSupport(currentState)
  }

  const hyperfocusInfo = tracker.getHyperfocusPreservationRule()

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60

    if (hours > 0) {
      return `${hours}h ${minutes}m`
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`
    } else {
      return `${secs}s`
    }
  }

  const exportLog = () => {
    tracker.exportADHDLog()
  }

  const getEnergyColor = () => {
    switch (energyLevel) {
      case 'high':
        return '#48bb78'
      case 'medium':
        return '#f6ad55'
      case 'low':
        return '#f56565'
      default:
        return '#999'
    }
  }

  return (
    <div className="adhd-tracker-dashboard">
      <div className="dashboard-header">
        <h1>🧠 ADHD-Aware Cognitive State Tracker</h1>
        <p>Hyperfocus-preserving, rumination-preventing, dopamine-optimized</p>
      </div>

      <div className="dashboard-grid">
        {/* Current State */}
        <div className="card current-state-card">
          <div className="card-header">Current State</div>
          {currentState ? (
            <>
              <div
                className="current-state-display"
                style={{ borderColor: stateConfig.color }}
              >
                <div className="state-emoji">{stateConfig.emoji}</div>
                <div className="state-info">
                  <h2>{stateConfig.label}</h2>
                  <p className="elapsed-time">{formatTime(elapsedTime)}</p>
                  {isHyperfocused && (
                    <p className="hyperfocus-indicator">🔥 HYPERFOCUSED</p>
                  )}
                </div>
              </div>

              {/* Task Initiation Help */}
              {getTaskInitiationHelp() && (
                <div className="task-initiation">
                  <p className="initiation-trick">
                    💡 {getTaskInitiationHelp().initiationTrick}
                  </p>
                </div>
              )}

              {/* Hyperfocus Control */}
              {currentState === 'deep_focus' && (
                <button
                  className={`hyperfocus-btn ${isHyperfocused ? 'active' : ''}`}
                  onClick={toggleHyperfocus}
                >
                  {isHyperfocused ? '🔥 Stop Hyperfocus' : '🔥 Enable Hyperfocus Mode'}
                </button>
              )}

              {hyperfocusInfo && (
                <div className="hyperfocus-protection">
                  <p>⚠️ {hyperfocusInfo.message}</p>
                </div>
              )}
            </>
          ) : (
            <div className="no-state">
              <p>Select a state to begin tracking</p>
            </div>
          )}
        </div>

        {/* Energy Level */}
        <div className="card energy-card">
          <div className="card-header">⚡ Energy Level</div>
          <div
            className="energy-gauge"
            style={{ backgroundColor: getEnergyColor() }}
          >
            <p className="energy-level">{energyLevel.toUpperCase()}</p>
          </div>
          <div className="energy-buttons">
            {['high', 'medium', 'low'].map(level => (
              <button
                key={level}
                className={`energy-btn ${energyLevel === level ? 'active' : ''}`}
                onClick={() => handleEnergeLevelChange(level)}
              >
                {level === 'high' && '⚡⚡⚡'}
                {level === 'medium' && '⚡⚡'}
                {level === 'low' && '⚡'}
              </button>
            ))}
          </div>
          <p className="energy-note">
            {energyLevel === 'low' && '⚠️ Recharge soon to avoid paralysis'}
            {energyLevel === 'medium' && 'Balanced. Good for most tasks.'}
            {energyLevel === 'high' && '🔥 Perfect for Deep Focus or challenging work'}
          </p>
        </div>

        {/* Dopamine Hits */}
        <div className="card dopamine-card">
          <div className="card-header">🎉 Dopamine Hits</div>
          <div className="dopamine-counter">
            <div className="hit-count">{dopamineHits}</div>
            <p>wins today</p>
          </div>
          <div className="dopamine-buttons">
            <button
              className="dopamine-btn"
              onClick={() => addDopamineHit('task_completed')}
            >
              ✅ Task Done
            </button>
            <button
              className="dopamine-btn"
              onClick={() => addDopamineHit('breakthrough')}
            >
              💡 Breakthrough
            </button>
          </div>
        </div>

        {/* State Transitions */}
        <div className="card transitions-card">
          <div className="card-header">Suggested Next States</div>
          <div className="transition-buttons">
            {currentState ? (
              availableStates.length > 0 ? (
                availableStates.map(state => (
                  <button
                    key={state.id}
                    className="transition-btn"
                    style={{ borderColor: state.color }}
                    onClick={() => handleStateTransition(state.id)}
                  >
                    <span className="btn-emoji">{state.emoji}</span>
                    <span className="btn-label">{state.label.split(' ')[1]}</span>
                  </button>
                ))
              ) : (
                <p className="no-transitions">No transitions available</p>
              )
            ) : (
              <div className="start-states">
                {STATES.slice(0, 4).map(state => (
                  <button
                    key={state.id}
                    className="transition-btn start-btn"
                    style={{ borderColor: state.color }}
                    onClick={() => handleStateTransition(state.id)}
                  >
                    <span className="btn-emoji">{state.emoji}</span>
                    <span className="btn-label">{state.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Recovery Quality Rating */}
        {currentState === 'recharge' && (
          <div className="card recovery-card">
            <div className="card-header">🔋 Recovery Quality</div>
            <p className="recovery-prompt">How good is this recharge?</p>
            <div className="rating-buttons">
              {[1, 2, 3, 4, 5].map(rating => (
                <button
                  key={rating}
                  className={`rating-btn ${recoveryRating === rating ? 'selected' : ''}`}
                  onClick={() => setRecoveryRating(rating)}
                >
                  {rating}
                </button>
              ))}
            </div>
            {recoveryRating > 0 && (
              <button className="submit-rating-btn" onClick={submitRecoveryRating}>
                Submit Rating
              </button>
            )}
          </div>
        )}

        {/* ADHD Warnings */}
        {warnings.length > 0 && (
          <div className="card warnings-card">
            <div className="card-header">⚠️ ADHD Alerts</div>
            <div className="warnings-list">
              {warnings
                .filter(w =>
                  ['RUMINATION_LOOP', 'REJECTION_SENSITIVITY', 'ENERGY_MISMATCH'].includes(
                    w.type
                  )
                )
                .map((warning, idx) => (
                  <div key={idx} className={`warning warning-${warning.severity.toLowerCase()}`}>
                    <div className="warning-header">
                      <span className="warning-type">{warning.type}</span>
                    </div>
                    <p className="warning-message">{warning.message}</p>
                    <p className="warning-recommendation">💡 {warning.recommendation}</p>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* ADHD Metrics */}
        <div className="card metrics-card">
          <div className="card-header">📊 ADHD Metrics</div>
          {Object.keys(metrics).length > 0 ? (
            <div className="metrics-display">
              <div className="metric">
                <span className="metric-label">Focus Time</span>
                <span className="metric-value">
                  {Object.entries(metrics).find(([key]) => key === 'deep_focus')?.[1]
                    ?.total_minutes || 0}
                  m
                </span>
              </div>
              <div className="metric">
                <span className="metric-label">Recharge</span>
                <span className="metric-value">
                  {Object.entries(metrics).find(([key]) => key === 'recharge')?.[1]
                    ?.total_minutes || 0}
                  m
                </span>
              </div>
              <div className="metric">
                <span className="metric-label">Warnings</span>
                <span className="metric-value">{warnings.length}</span>
              </div>
            </div>
          ) : (
            <p className="no-metrics">Start tracking to see metrics</p>
          )}
        </div>

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div className="card recommendations-card">
            <div className="card-header">💡 ADHD Recommendations</div>
            <div className="recommendations-list">
              {recommendations.map((rec, idx) => (
                <div key={idx} className={`recommendation rec-${rec.priority.toLowerCase()}`}>
                  <span className="rec-icon">{rec.icon}</span>
                  <p className="rec-message">{rec.message}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="card actions-card">
          <div className="card-header">Actions</div>
          <button className="action-btn export-btn" onClick={exportLog}>
            📥 Export ADHD Log
          </button>
          <button
            className="action-btn reset-btn"
            onClick={() => {
              setCurrentState(null)
              setStateHistory([])
              setMetrics({})
              setWarnings([])
              setElapsedTime(0)
              setDopamineHits(0)
              setEnergyLevel('medium')
              setIsHyperfocused(false)
            }}
          >
            🔄 Reset Tracker
          </button>
        </div>
      </div>

      {/* Daily Summary */}
      {stateHistory.length > 0 && (
        <div className="daily-summary">
          <h3>📊 Daily ADHD Summary</h3>
          <div className="summary-stats">
            <div className="stat">
              <span className="stat-label">Dopamine Hits</span>
              <span className="stat-value">{dopamineHits}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Focus Sessions</span>
              <span className="stat-value">
                {stateHistory.filter(s => s.state === 'deep_focus').length}
              </span>
            </div>
            <div className="stat">
              <span className="stat-label">Warnings</span>
              <span className="stat-value">{warnings.length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Energy Level</span>
              <span className="stat-value">{energyLevel}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
