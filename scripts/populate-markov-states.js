#!/usr/bin/env node

import neo4j from 'neo4j-driver'
import dotenv from 'dotenv'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

dotenv.config()

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const uri = process.env.NEO4J_URI || 'bolt://localhost:7687'
const user = process.env.NEO4J_USER || 'neo4j'
const password = process.env.NEO4J_PASSWORD || 'password'

if (process.env.CONFIRM_NEO4J_WRITE !== 'true') {
  console.error('❌ This script writes to Neo4j. Set CONFIRM_NEO4J_WRITE=true to proceed.')
  process.exit(1)
}

if (!process.env.NEO4J_PASSWORD || password === 'password') {
  console.error('❌ Refusing to run with default or missing Neo4j password.')
  process.exit(1)
}

const driver = neo4j.driver(uri, neo4j.auth.basic(user, password))

// rest unchanged

async function main() {
  try {
    console.log('🧠 Populating Markov Chain Cognitive States...\n')

    await createCognitiveStates()
    await createStateTransitions()
    await createFeedbackLoopGuards()
    await createDailyRhythm()

    console.log('\n✅ Markov cognitive state model complete!')
  } catch (error) {
    console.error('❌ Error populating Markov states:', error)
    process.exit(1)
  } finally {
    await driver.close()
  }
}

main()
