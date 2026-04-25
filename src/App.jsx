import React, { useState } from 'react'
import Quiz from './components/Quiz'
import SchemaOutput from './components/SchemaOutput'
import './App.css'

export default function App() {
  const [answers, setAnswers] = useState(null)
  const [points, setPoints] = useState(0)
  const [achievements, setAchievements] = useState([])

  const handleQuizComplete = (quizAnswers, finalPoints, finalAchievements) => {
    setAnswers(quizAnswers)
    setPoints(finalPoints)
    setAchievements(finalAchievements)
  }

  const handleReset = () => {
    setAnswers(null)
    setPoints(0)
    setAchievements([])
  }

  return (
    <div className="app">
      {!answers ? (
        <Quiz onComplete={handleQuizComplete} />
      ) : (
        <SchemaOutput
          answers={answers}
          points={points}
          achievements={achievements}
          onReset={handleReset}
        />
      )}
    </div>
  )
}
