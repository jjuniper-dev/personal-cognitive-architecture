#!/usr/bin/env node

import neo4j from 'neo4j-driver'
import dotenv from 'dotenv'

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

async function createSelfNode() {
  const query = `
    MERGE (self:Self {name: 'Self'})
    SET self.role = 'Learner, Builder, Mentor, Strategic Thinker',
        self.created_date = datetime(),
        self.core_values = ['Contribution', 'Growth', 'Autonomy', 'Authenticity'],
        self.mindset = ['Systems thinking', 'Self-aware', 'Growth-oriented', 'Intentional']
    RETURN self
  `
  return executeQuery(query)
}

async function createValues() {
  const values = [
    { name: 'Contribution', description: 'Making a real difference in work and life' },
    { name: 'Growth', description: "Personal and others' continuous development" },
    { name: 'Autonomy', description: 'Freedom to make own choices and decisions' },
    { name: 'Authenticity', description: 'Being genuine, no masks or performance' }
  ]

  for (const value of values) {
    const query = `
      MERGE (v:Value {name: $name})
      SET v.description = $description
      RETURN v
    `
    await executeQuery(query, value)

    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (v:Value {name: $name})
      MERGE (self)-[:VALUES]->(v)
    `
    await executeQuery(linkQuery, { name: value.name })
  }
}

async function createLearningStyles() {
  const styles = [
    { modality: 'Visual', description: 'Diagrams, charts, videos' },
    { modality: 'Auditory', description: 'Discussion, podcasts, talking it out' },
    { modality: 'Trial and Error', description: 'Hands-on experimentation and learning' },
    { modality: 'Teaching Others', description: 'Learning by explaining and mentoring' }
  ]

  for (const style of styles) {
    const query = `
      MERGE (ls:LearningStyle {modality: $modality})
      SET ls.description = $description
      RETURN ls
    `
    await executeQuery(query, style)

    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (ls:LearningStyle {modality: $modality})
      MERGE (self)-[:HAS_LEARNING_STYLE]->(ls)
    `
    await executeQuery(linkQuery, { modality: style.modality })
  }
}

async function createWorkContext() {
  const contexts = [
    { aspect: 'Environment: Flex Remote', description: 'Mix of remote and office work' },
    { aspect: 'Environment: Solo Deep Work', description: 'Dedicated space for focused work' },
    { aspect: 'Pace: Deep Focus', description: 'Long stretches on meaningful work' },
    { aspect: 'Pace: Balanced Collaboration', description: 'Collaboration balanced with focus' },
    { aspect: 'Value: Learning', description: 'Constantly growing and new challenges' },
    { aspect: 'Value: Impact', description: 'Seeing work make real difference' },
    { aspect: 'Value: Mastery', description: 'Getting excellent at what matters' },
    { aspect: 'Value: Autonomy', description: 'Owning work and decisions' },
    { aspect: 'Time: Deep Work Priority', description: 'Most time on core work, minimal meetings' },
    { aspect: 'Time: Reflection', description: 'Intentional thinking and planning time' }
  ]

  for (const context of contexts) {
    const query = `
      MERGE (wc:WorkContext {aspect: $aspect})
      SET wc.description = $description
      RETURN wc
    `
    await executeQuery(query, context)

    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (wc:WorkContext {aspect: $aspect})
      MERGE (self)-[:WORKS_IN]->(wc)
    `
    await executeQuery(linkQuery, { aspect: context.aspect })
  }
}

async function createRelationships() {
  const relTypes = [
    { type: 'Deep 1-on-1', preference: 'Preferred' },
    { type: 'Small Groups (3-5)', preference: 'Preferred' },
    { type: 'Async Communication', preference: 'Preferred' },
    { type: 'Mentoring', preference: 'Energizing' },
    { type: 'Peer Collaboration', preference: 'Energizing' },
    { type: 'Surface Talk', preference: 'Draining' },
    { type: 'Competitive Dynamics', preference: 'Draining' }
  ]

  for (const rel of relTypes) {
    const query = `
      MERGE (r:Relationship {type: $type})
      SET r.preference = $preference
      RETURN r
    `
    await executeQuery(query, rel)

    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (r:Relationship {type: $type})
      MERGE (self)-[:HAS_RELATIONSHIP_STYLE]->(r)
    `
    await executeQuery(linkQuery, { type: rel.type })

    if (rel.preference === 'Energizing') {
      const valuesQuery = `
        MATCH (r:Relationship {type: $type}), (v:Value)
        WHERE v.name IN ['Contribution', 'Growth']
        MERGE (r)-[:ROOTED_IN]->(v)
      `
      await executeQuery(valuesQuery, { type: rel.type })
    }
  }
}

async function createEnergy() {
  const energyAspects = [
    { aspect: 'Chronotype: Early Morning', description: 'Peak thinking time before others awake' },
    { aspect: 'Recharge Need: Solo Time', description: 'Essential for recharging as introvert' },
    { aspect: 'Creative Necessity: Deep Work', description: 'Best thinking happens in solitude' },
    { aspect: 'Rhythm: Protected Focus Blocks', description: 'Deep work time blocked off' }
  ]

  for (const energy of energyAspects) {
    const query = `
      MERGE (e:Energy {aspect: $aspect})
      SET e.description = $description
      RETURN e
    `
    await executeQuery(query, energy)

    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (e:Energy {aspect: $aspect})
      MERGE (self)-[:OPERATES_WITH_ENERGY]->(e)
    `
    await executeQuery(linkQuery, { aspect: energy.aspect })
  }
}

async function createChallenges() {
  const challenges = [
    { name: 'Networking & Visibility', impact: 'Ideas need visibility to have impact' },
    { name: 'Turning Ideas into Action', impact: 'Execution gap between thinking and doing' }
  ]

  for (const challenge of challenges) {
    const query = `
      MERGE (c:Challenge {name: $name})
      SET c.impact = $impact
      RETURN c
    `
    await executeQuery(query, challenge)

    const linkQuery = `
      MATCH (self:Self {name: 'Self'}), (c:Challenge {name: $name})
      MERGE (self)-[:FACES_CHALLENGE]->(c)
    `
    await executeQuery(linkQuery, { name: challenge.name })
  }
}

async function createCrossRelationships() {
  const query1 = `
    MATCH (ls:LearningStyle {modality: 'Visual'}), (wc:WorkContext {aspect: 'Environment: Solo Deep Work'})
    MERGE (ls)-[:SHAPES]->(wc)
  `
  await executeQuery(query1)

  const query2 = `
    MATCH (ls:LearningStyle {modality: 'Teaching Others'}), (r:Relationship {type: 'Mentoring'})
    MERGE (ls)-[:ENERGIZED_BY]->(r)
  `
  await executeQuery(query2)
}

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
