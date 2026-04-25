import React from 'react'
import './GamificationBar.css'

const ACHIEVEMENT_DETAILS = {
  started: { icon: '🚀', label: 'First Step', description: 'Started your profile journey' },
  completed: { icon: '🎉', label: 'Finisher', description: 'Completed all questions' },
  allAnswered: { icon: '✨', label: 'Thorough', description: 'Answered every question' }
}

export default function GamificationBar({ points, progress, achievements }) {
  return (
    <div className="gamification-bar">
      <div className="points-box">
        <div className="points-value">{points}</div>
        <div className="points-label">XP</div>
      </div>

      <div className="progress-section">
        <div className="progress-bar-container">
          <div className="progress-bar-fill" style={{ width: `${progress}%` }}></div>
        </div>
        <span className="progress-text">{Math.round(progress)}% Complete</span>
      </div>

      <div className="achievements-box">
        <div className="achievements-title">Achievements</div>
        <div className="achievements-list">
          {achievements.map(ach => (
            <div key={ach} className="achievement" title={ACHIEVEMENT_DETAILS[ach]?.description}>
              <span className="achievement-icon">{ACHIEVEMENT_DETAILS[ach]?.icon}</span>
            </div>
          ))}
          {achievements.length === 0 && <span className="no-achievements">Keep going...</span>}
        </div>
      </div>
    </div>
  )
}
