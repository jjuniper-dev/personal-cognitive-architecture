import React, { useState, useEffect } from 'react'
import StateTracker from '../markov/StateTracker'
import './StateTrackerDashboard.css'

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

export default function StateTrackerDashboard() {
  const [tracker] = useState(new StateTracker())
  const [currentState, setCurrentState] = useState(null)
  const [stateHistory, setStateHistory] = useState([])
  const [metrics, setMetrics] = useState({})
  const [warnings, setWarnings] = useState([])
  const [elapsedTime, setElapsedTime] = useState(0)

  const stateConfig = STATES.find(s => s.id === currentState) || {}
  const availableTransitions = TRANSITIONS[currentState] || []
  const availableStates = availableTransitions
    .map(id => STATES.find(s => s.id === id))
    .filter(Boolean)

  // Update elapsed time every second
  useEffect(() => {
    const interval = setInterval(() => {
      setElapsedTime(prev => prev + 1)
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  const handleStateTransition = (newStateId) => {
    const result = tracker.transitionTo(newStateId)
    setCurrentState(newStateId)
    setStateHistory(tracker.stateHistory)
    setMetrics(tracker.getStateMetrics())
    setWarnings(tracker.getDailyLog().warnings)
    setElapsedTime(0)
  }

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

  const getWarningIcon = (type) => {
    switch (type) {
      case 'REFLECTION_LOOP':
        return '⚠️'
      case 'REFLECTION_LEARNING_LOOP':
        return '⚡'
      case 'RECHARGE_LOOP':
        return '🔋'
      case 'COLLABORATION_AVOIDANCE':
        return '👥'
      default:
        return '⚠️'
    }
  }

  const exportLog = () => {
    tracker.exportDailyLog()
  }

  return (
    <div className="state-tracker-dashboard">
      <div className="dashboard-header">
        <h1>🧠 Cognitive State Tracker</h1>
        <p>Real-time Markov Chain state management</p>
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
                </div>
              </div>
              <div className="state-description">
                {STATES.find(s => s.id === currentState)?.label}
              </div>
            </>
          ) : (
            <div className="no-state">
              <p>Select a state to begin tracking</p>
            </div>
          )}
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

        {/* Warnings */}
        {warnings.length > 0 && (
          <div className="card warnings-card">
            <div className="card-header">⚠️ Active Warnings</div>
            <div className="warnings-list">
              {warnings.map((warning, idx) => (
                <div key={idx} className={`warning warning-${warning.severity.toLowerCase()}`}>
                  <div className="warning-header">
                    <span className="warning-icon">
                      {getWarningIcon(warning.type)}
                    </span>
                    <span className="warning-type">{warning.type}</span>
                    <span className="warning-severity">{warning.severity}</span>
                  </div>
                  <p className="warning-message">{warning.message}</p>
                  <p className="warning-recommendation">
                    💡 {warning.recommendation}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Daily Metrics */}
        <div className="card metrics-card">
          <div className="card-header">Daily Time Allocation</div>
          <div className="metrics-grid">
            {Object.entries(metrics)
              .sort((a, b) => b[1].total_minutes - a[1].total_minutes)
              .map(([state, data]) => (
                <div key={state} className="metric-item">
                  <div className="metric-label">
                    {STATES.find(s => s.id === state)?.emoji} {state}
                  </div>
                  <div className="metric-value">{data.total_minutes}m</div>
                  <div className="metric-detail">
                    {data.count} sessions, avg {data.average_duration}m
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* State History */}
        <div className="card history-card">
          <div className="card-header">Today's Timeline</div>
          <div className="history-timeline">
            {stateHistory.length > 0 ? (
              stateHistory.slice(-8).map((entry, idx) => (
                <div key={idx} className="timeline-item">
                  <div className="timeline-time">
                    {entry.startTime.toLocaleTimeString()}
                  </div>
                  <div className="timeline-state">
                    {STATES.find(s => s.id === entry.state)?.emoji}{' '}
                    {entry.state}
                  </div>
                  <div className="timeline-duration">{entry.duration_minutes}m</div>
                </div>
              ))
            ) : (
              <p className="no-history">No history yet</p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="card actions-card">
          <div className="card-header">Actions</div>
          <button className="action-btn export-btn" onClick={exportLog}>
            📥 Export Daily Log
          </button>
          <button
            className="action-btn reset-btn"
            onClick={() => {
              setCurrentState(null)
              setStateHistory([])
              setMetrics({})
              setWarnings([])
              setElapsedTime(0)
            }}
          >
            🔄 Reset Tracker
          </button>
        </div>
      </div>

      {/* Daily Summary */}
      {stateHistory.length > 0 && (
        <div className="daily-summary">
          <h3>📊 Daily Summary</h3>
          <div className="summary-stats">
            <div className="stat">
              <span className="stat-label">Total Time Tracked</span>
              <span className="stat-value">
                {Math.round(
                  Object.values(metrics).reduce((sum, m) => sum + m.total_minutes, 0)
                )}m
              </span>
            </div>
            <div className="stat">
              <span className="stat-label">States Visited</span>
              <span className="stat-value">{Object.keys(metrics).length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Feedback Loops Detected</span>
              <span className="stat-value">{warnings.length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Most Common State</span>
              <span className="stat-value">
                {Object.entries(metrics).sort((a, b) => b[1].count - a[1].count)[0]?.[0] ||
                  'N/A'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
