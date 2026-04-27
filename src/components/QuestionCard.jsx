import React, { useState } from 'react'
import './QuestionCard.css'

export default function QuestionCard({ question, questionNumber, totalQuestions, onAnswer }) {
  const [selected, setSelected] = useState([])

  const toggleOption = (option) => {
    if (selected.includes(option)) {
      setSelected(selected.filter(o => o !== option))
    } else {
      setSelected([...selected, option])
    }
  }

  const handleSubmit = () => {
    if (selected.length > 0) {
      onAnswer(selected)
    }
  }

  return (
    <div className="question-card">
      <div className="question-header">
        <h2>{question.question}</h2>
        <span className="question-number">{questionNumber}/{totalQuestions}</span>
      </div>

      <div className="options-grid">
        {question.options.map((option, idx) => (
          <button
            key={idx}
            className={`option-button ${selected.includes(option) ? 'selected' : ''}`}
            onClick={() => toggleOption(option)}
          >
            <span className="option-text">{option}</span>
            {selected.includes(option) && <span className="checkmark">✓</span>}
          </button>
        ))}
      </div>

      <div className="button-group">
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={selected.length === 0}
        >
          Next {selected.length > 0 && `(${selected.length} selected)`}
        </button>
      </div>
    </div>
  )
}
