#!/usr/bin/env node

import neo4j from 'neo4j-driver'
import dotenv from 'dotenv'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

dotenv.config()

// Safety guard for database writes
if (process.env.CONFIRM_NEO4J_WRITE !== 'true') {
  console.error('❌ CONFIRM_NEO4J_WRITE must be set to "true" to run database write scripts')
  process.exit(1)
}

if (!process.env.NEO4J_PASSWORD || process.env.NEO4J_PASSWORD === 'password') {
  console.error('❌ NEO4J_PASSWORD is missing or set to default "password". Set a secure password in .env')
  process.exit(1)
}

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const uri = process.env.NEO4J_URI || 'bolt://localhost:7687'
const user = process.env.NEO4J_USER || 'neo4j'
const password = process.env.NEO4J_PASSWORD || 'password'

const driver = neo4j.driver(uri, neo4j.auth.basic(user, password))

async function executeQuery(query, parameters = {}) {
  const session = driver.session()
  try {
    const result = await session.run(query, parameters)
    return result
  } finally {
    await session.close()
  }
}

async function createCognitiveStates() {
  const statesData = JSON.parse(
    fs.readFileSync(path.join(__dirname, '../data/markov-cognitive-states.json'), 'utf8')
  )

  console.log('📍 Creating Cognitive State nodes...')

  for (const [stateKey, stateData] of Object.entries(statesData.cognitive_states)) {
    const query = `
      MERGE (cs:CognitiveState {id: $id})
      SET cs.label = $label,
          cs.description = $description,
          cs.energy_requirement = $energy_requirement,
          cs.typical_duration_minutes = $typical_duration_minutes,
          cs.risk_level = $risk_level,
          cs.feedback_loop_risk = $feedback_loop_risk
      RETURN cs
    `

    const params = {
      id: stateKey,
      label: stateData.label,
      description: stateData.description,
      energy_requirement: stateData.energy_requirement,
      typical_duration_minutes: stateData.typical_duration_minutes,
      risk_level: stateData.risk_level,
      feedback_loop_risk: stateData.feedback_loop_risk
    }

    await executeQuery(query, params)

    // Link to Self
    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (cs:CognitiveState {id: $id})
      MERGE (self)-[:HAS_COGNITIVE_STATE]->(cs)
    `
    await executeQuery(linkQuery, { id: stateKey })

    console.log(`  ✓ Created state: ${stateData.label}`)
  }
}

async function createStateTransitions() {
  const statesData = JSON.parse(
    fs.readFileSync(path.join(__dirname, '../data/markov-cognitive-states.json'), 'utf8')
  )

  console.log('\n🔗 Creating State Transitions...')

  for (const [transitionKey, transitionData] of Object.entries(statesData.state_transitions)) {
    const query = `
      MATCH (from:CognitiveState {id: $from_state})
      MATCH (to:CognitiveState {id: $to_state})
      MERGE (from)-[t:TRANSITIONS_TO {id: $id}]-(to)
      SET t.probability = $probability,
          t.typical_duration_minutes = $typical_duration_minutes,
          t.description = $description,
          t.risk_level = $risk_level
      RETURN t
    `

    const params = {
      id: transitionKey,
      from_state: transitionData.from,
      to_state: transitionData.to,
      probability: transitionData.probability,
      typical_duration_minutes: transitionData.typical_duration_time || 0,
      description: transitionData.description,
      risk_level: transitionData.risk_level || 'Low'
    }

    try {
      await executeQuery(query, params)
      console.log(`  ✓ ${transitionData.from} → ${transitionData.to} (p=${transitionData.probability})`)
    } catch (err) {
      console.log(`  ⚠️  Skipping ${transitionKey}: ${err.message}`)
    }
  }
}

async function createFeedbackLoopGuards() {
  const statesData = JSON.parse(
    fs.readFileSync(path.join(__dirname, '../data/markov-cognitive-states.json'), 'utf8')
  )

  console.log('\n⚠️  Creating Feedback Loop Guards...')

  for (const [guardKey, guardData] of Object.entries(statesData.feedback_loop_safeguards)) {
    const query = `
      CREATE (guard:FeedbackLoopGuard {id: $id})
      SET guard.trigger = $trigger,
          guard.warning = $warning,
          guard.action = $action,
          guard.rationale = $rationale
      RETURN guard
    `

    const params = {
      id: guardKey,
      trigger: guardData.trigger,
      warning: guardData.warning,
      action: guardData.action,
      rationale: guardData.rationale
    }

    await executeQuery(query, params)
    console.log(`  ✓ Guard: ${guardKey}`)
  }
}

async function createDailyRhythm() {
  const statesData = JSON.parse(
    fs.readFileSync(path.join(__dirname, '../data/markov-cognitive-states.json'), 'utf8')
  )

  console.log('\n⏰ Creating Ideal Daily Rhythm...')

  const rhythm = statesData.daily_ideal_rhythm

  for (const [timeSlot, slotData] of Object.entries(rhythm)) {
    const query = `
      CREATE (slot:DailyRhythmSlot {id: $id})
      SET slot.time = $time,
          slot.sequence = $sequence,
          slot.duration_minutes = $duration_minutes,
          slot.goal = $goal
      RETURN slot
    `

    const params = {
      id: timeSlot,
      time: slotData.time,
      sequence: JSON.stringify(slotData.sequence),
      duration_minutes: slotData.duration_minutes,
      goal: slotData.goal
    }

    await executeQuery(query, params)
    console.log(`  ✓ ${timeSlot}: ${slotData.time}`)
  }
}

async function main() {
  try {
    console.log('🧠 Populating Markov Chain Cognitive States...\n')

    await createCognitiveStates()
    await createStateTransitions()
    await createFeedbackLoopGuards()
    await createDailyRhythm()

    console.log('\n✅ Markov cognitive state model complete!')
    console.log('\n📊 Query suggestions:')
    console.log('  - MATCH (cs:CognitiveState) RETURN cs')
    console.log('  - MATCH (cs1:CognitiveState)-[t:TRANSITIONS_TO]->(cs2:CognitiveState) RETURN cs1, t, cs2')
    console.log('  - MATCH (guard:FeedbackLoopGuard) RETURN guard')
  } catch (error) {
    console.error('❌ Error populating Markov states:', error)
    process.exit(1)
  } finally {
    await driver.close()
  }
}

main()
