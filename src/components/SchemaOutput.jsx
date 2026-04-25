import React from 'react'
import './SchemaOutput.css'

export default function SchemaOutput({ answers, points, achievements, onReset }) {
  const generateSchema = () => {
    const schema = {
      nodes: {
        core: ['Self', 'Mindset'],
        dimensions: [],
        contexts: []
      },
      relationships: [],
      properties: {}
    }

    // Add dimensions
    if (answers.entities) {
      schema.nodes.dimensions.push(...answers.entities)
    }

    // Add contexts
    if (answers.learning_styles) {
      schema.nodes.contexts.push(`Learning: ${answers.learning_styles.join(', ')}`)
    }
    if (answers.work_preferences) {
      schema.nodes.contexts.push(`Work: ${answers.work_preferences.join(', ')}`)
    }
    if (answers.relationships) {
      schema.nodes.contexts.push(`Relationships: ${answers.relationships.join(', ')}`)
    }
    if (answers.alone_time) {
      schema.nodes.contexts.push(`Alone Time: ${answers.alone_time.join(', ')}`)
    }

    // Add relationships
    if (answers.connections) {
      schema.relationships = answers.connections
    }

    return schema
  }

  const schema = generateSchema()

  const downloadSchema = () => {
    const data = JSON.stringify(schema, null, 2)
    const element = document.createElement('a')
    element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(data))
    element.setAttribute('download', 'personal-profile-schema.json')
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  const copyToClipboard = () => {
    const text = JSON.stringify(schema, null, 2)
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="schema-output-container">
      <div className="success-header">
        <h1>🎉 Profile Complete!</h1>
        <p>Your personal cognitive architecture schema is ready</p>
      </div>

      <div className="summary-box">
        <div className="summary-stat">
          <div className="stat-value">{points}</div>
          <div className="stat-label">Total XP Earned</div>
        </div>
        <div className="summary-stat">
          <div className="stat-value">{Object.keys(schema.nodes).reduce((sum, key) => sum + schema.nodes[key].length, 0)}</div>
          <div className="stat-label">Nodes Defined</div>
        </div>
        <div className="summary-stat">
          <div className="stat-value">{schema.relationships.length}</div>
          <div className="stat-label">Relationships</div>
        </div>
      </div>

      <div className="schema-display">
        <h2>📊 Your Schema</h2>
        <pre className="schema-json">{JSON.stringify(schema, null, 2)}</pre>
      </div>

      <div className="answer-details">
        <h2>📝 Your Answers</h2>
        <div className="answers-grid">
          {Object.entries(answers).map(([key, value]) => (
            <div key={key} className="answer-item">
              <h3>{key.replace(/_/g, ' ').toUpperCase()}</h3>
              <ul>
                {(Array.isArray(value) ? value : [value]).map((v, i) => (
                  <li key={i}>{v}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="action-buttons">
        <button className="btn-download" onClick={downloadSchema}>
          📥 Download Schema
        </button>
        <button className="btn-copy" onClick={copyToClipboard}>
          📋 Copy as JSON
        </button>
        <button className="btn-reset" onClick={onReset}>
          🔄 Start Over
        </button>
      </div>
    </div>
  )
}
