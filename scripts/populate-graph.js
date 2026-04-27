#!/usr/bin/env node

import neo4j from 'neo4j-driver'
import dotenv from 'dotenv'

dotenv.config()

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

async function executeQuery(query, parameters = {}) {
  const session = driver.session()
  try {
    const result = await session.run(query, parameters)
    return result
  } finally {
    await session.close()
  }
}

// (rest unchanged)

async function main() {
  try {
    console.log('🚀 Populating Personal Cognitive Architecture Graph...\n')

    console.log('📌 Creating Self node...')
    await createSelfNode()

    console.log('📌 Creating Values...')
    await createValues()

    console.log('🧠 Creating Learning Styles...')
    await createLearningStyles()

    console.log('💼 Creating Work Context...')
    await createWorkContext()

    console.log('👥 Creating Relationships...')
    await createRelationships()

    console.log('⚡ Creating Energy patterns...')
    await createEnergy()

    console.log('⚠️  Creating Challenges...')
    await createChallenges()

    console.log('🔗 Creating cross-relationships...')
    await createCrossRelationships()

    console.log('\n✅ Database population complete!')
    console.log('\n📍 View your graph at: http://localhost:7474')
  } catch (error) {
    console.error('❌ Error populating database:', error)
    process.exit(1)
  } finally {
    await driver.close()
  }
}

main()
