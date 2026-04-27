import React, { useState } from 'react'
import Quiz from './components/Quiz'
import SchemaOutput from './components/SchemaOutput'
import StateTrackerDashboard from './components/StateTrackerDashboard'
import ADHDTrackerDashboard from './components/ADHDTrackerDashboard'
import './App.css'

export default function App() {
  const [view, setView] = useState('menu')
  const [answers, setAnswers] = useState(null)
  const [points, setPoints] = useState(0)
  const [achievements, setAchievements] = useState([])

  const handleQuizComplete = (quizAnswers, finalPoints, finalAchievements) => {
    setAnswers(quizAnswers)
    setPoints(finalPoints)
    setAchievements(finalAchievements)
    setView('schema')
  }

  const handleReset = () => {
    setAnswers(null)
    setPoints(0)
    setAchievements([])
    setView('menu')
  }

  const handleStartQuiz = () => {
    setView('quiz')
  }

  const handleStartTracker = () => {
    setView('tracker')
  }

  const handleStartADHDTracker = () => {
    setView('adhd-tracker')
  }

  return (
    <div className="app">
      {view === 'menu' && (
        <div className="menu-view">
          <div className="menu-container">
            <h1>🧠 Personal Cognitive Architecture</h1>
            <p>Build and track your cognitive profile</p>

            <div className="menu-buttons">
              <button
                className="menu-btn quiz-btn"
                onClick={handleStartQuiz}
              >
                <span className="menu-emoji">📋</span>
                <span className="menu-title">Profile Discovery</span>
                <span className="menu-desc">Take the gamified quiz to define your cognitive profile</span>
              </button>

              <button
                className="menu-btn tracker-btn"
                onClick={handleStartTracker}
              >
                <span className="menu-emoji">📊</span>
                <span className="menu-title">State Tracker</span>
                <span className="menu-desc">Real-time Markov Chain state management & tracking</span>
              </button>

              <button
                className="menu-btn adhd-btn"
                onClick={handleStartADHDTracker}
              >
                <span className="menu-emoji">🧠</span>
                <span className="menu-title">ADHD State Tracker</span>
                <span className="menu-desc">Hyperfocus-preserving, rumination-preventing, dopamine-optimized</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {view === 'quiz' && !answers && (
        <Quiz onComplete={handleQuizComplete} />
      )}

      {view === 'schema' && answers && (
        <SchemaOutput
          answers={answers}
          points={points}
          achievements={achievements}
          onReset={handleReset}
        />
      )}

      {view === 'tracker' && (
        <div className="tracker-view">
          <button className="back-btn" onClick={() => setView('menu')}>
            ← Back to Menu
          </button>
          <StateTrackerDashboard />
        </div>
      )}

      {view === 'adhd-tracker' && (
        <div className="tracker-view">
          <button className="back-btn" onClick={() => setView('menu')}>
            ← Back to Menu
          </button>
          <ADHDTrackerDashboard />
        </div>
      )}
    </div>
  )
}
