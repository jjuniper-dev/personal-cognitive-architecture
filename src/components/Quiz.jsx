import React, { useState } from 'react'
import QuestionCard from './QuestionCard'
import GamificationBar from './GamificationBar'
import './Quiz.css'

const QUESTIONS = [
  {
    id: 'entities',
    question: 'Beyond Learning Styles, Work Contexts, Relationships, and Time Blocks—what other dimensions matter to you?',
    options: [
      'Values & Principles',
      'Goals & Ambitions',
      'Energy Levels',
      'Skills & Expertise',
      'Interests & Hobbies',
      'Mental Health & Wellbeing'
    ],
    type: 'multi'
  },
  {
    id: 'learning_styles',
    question: 'How would you describe your learning style?',
    options: [
      'Visual (diagrams, charts)',
      'Auditory (discussion, listening)',
      'Kinesthetic (hands-on, experimenting)',
      'Reading/Writing (books, articles)',
      'Learn through teaching others',
      'Learn in structured curricula'
    ],
    type: 'multi'
  },
  {
    id: 'work_preferences',
    question: 'What matters most in your work context?',
    options: [
      'Task type (creative vs analytical)',
      'Environment (quiet, social, remote)',
      'Collaboration style (independent vs team)',
      'Autonomy level (self-directed vs guided)',
      'Pace (fast-paced vs deep focus)',
      'Impact visibility'
    ],
    type: 'multi'
  },
  {
    id: 'relationships',
    question: 'How do you think about relationships?',
    options: [
      'By role (mentors, peers, mentees)',
      'By type (intimate, professional, casual)',
      'By interaction style (deep 1-on-1 vs group)',
      'By shared interests/values',
      'By frequency & intensity',
      'By mutual support & growth'
    ],
    type: 'multi'
  },
  {
    id: 'alone_time',
    question: 'What describes your alone time best?',
    options: [
      'How much time you need (hours/week)',
      'When you prefer it (morning, evening, weekends)',
      'What activities (reflection, hobbies, rest)',
      'Recovery from social interaction',
      'Creative/solo work time',
      'All of the above matter equally'
    ],
    type: 'multi'
  },
  {
    id: 'connections',
    question: 'Which connections are most important to you?',
    options: [
      'Learning style ↔ Work context',
      'Values ↔ Relationship types',
      'Energy level ↔ Social availability',
      'Goals ↔ Work preferences',
      'Alone time needs ↔ Relationship intensity',
      'All of them equally'
    ],
    type: 'multi'
  }
]

export default function Quiz({ onComplete }) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState({})
  const [points, setPoints] = useState(0)
  const [achievements, setAchievements] = useState([])

  const handleAnswer = (selectedOptions) => {
    const newAnswers = {
      ...answers,
      [QUESTIONS[currentQuestion].id]: selectedOptions
    }
    setAnswers(newAnswers)

    const newPoints = points + (selectedOptions.length * 10)
    setPoints(newPoints)

    // Award achievements
    const newAchievements = [...achievements]
    if (currentQuestion === 0 && !achievements.includes('started')) {
      newAchievements.push('started')
    }
    if (currentQuestion === QUESTIONS.length - 1) {
      newAchievements.push('completed')
    }
    if (Object.keys(newAnswers).length === QUESTIONS.length) {
      newAchievements.push('allAnswered')
    }
    setAchievements(newAchievements)

    if (currentQuestion < QUESTIONS.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      onComplete(newAnswers, newPoints, newAchievements)
    }
  }

  const progress = ((currentQuestion) / QUESTIONS.length) * 100
  const currentQ = QUESTIONS[currentQuestion]

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h1>🧠 Personal Profile Graph</h1>
        <p>Build your cognitive architecture schema</p>
      </div>

      <GamificationBar
        points={points}
        progress={progress}
        achievements={achievements}
      />

      <div className="quiz-content">
        <QuestionCard
          question={currentQ}
          questionNumber={currentQuestion + 1}
          totalQuestions={QUESTIONS.length}
          onAnswer={handleAnswer}
        />
      </div>

      <div className="quiz-footer">
        <small>Question {currentQuestion + 1} of {QUESTIONS.length}</small>
      </div>
    </div>
  )
}
