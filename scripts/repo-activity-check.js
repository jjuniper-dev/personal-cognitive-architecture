#!/usr/bin/env node

import { Octokit } from '@octokit/rest'
import dotenv from 'dotenv'

dotenv.config()

const REPOS = [
  { owner: 'jjuniper-dev', repo: 'pca', defaultBranch: 'master' },
  { owner: 'jjuniper-dev', repo: 'personal-cognitive-architecture', defaultBranch: 'main' },
  { owner: 'jjuniper-dev', repo: 'Obsidian', defaultBranch: 'main' },
]

const STALE_DAYS = parseInt(process.env.STALE_DAYS || '14', 10)
const RECENT_DAYS = parseInt(process.env.RECENT_DAYS || '30', 10)

function daysSince(dateString) {
  return Math.floor((Date.now() - new Date(dateString).getTime()) / 86400000)
}

function fmtDate(dateString) {
  return dateString.slice(0, 10)
}

async function getRepoActivity(octokit, owner, repo, defaultBranch) {
  const [branches, prs] = await Promise.all([
    octokit.paginate(octokit.repos.listBranches, { owner, repo, per_page: 100 }),
    octokit.paginate(octokit.pulls.list, { owner, repo, state: 'open', per_page: 100 }),
  ])

  const openPRBranches = new Set(prs.map(pr => pr.head.ref))

  const since = new Date(Date.now() - RECENT_DAYS * 86400000).toISOString()
  const recentCommitsRes = await octokit.repos.listCommits({
    owner, repo, sha: defaultBranch, since, per_page: 10,
  }).catch(() => ({ data: [] }))

  const branchDetails = await Promise.all(
    branches.map(async b => {
      const commitRes = await octokit.repos.getCommit({ owner, repo, ref: b.commit.sha })
      const lastDate = commitRes.data.commit.author.date
      return {
        name: b.name,
        lastDate,
        age: daysSince(lastDate),
        hasOpenPR: openPRBranches.has(b.name),
        isDefault: b.name === defaultBranch,
        sha: b.commit.sha.slice(0, 7),
      }
    })
  )

  return {
    repo,
    branches: branchDetails,
    openPRs: prs.map(pr => ({
      number: pr.number,
      title: pr.title,
      branch: pr.head.ref,
      updatedAt: pr.updated_at,
      draft: pr.draft,
    })),
    recentCommits: recentCommitsRes.data.map(c => ({
      sha: c.sha.slice(0, 7),
      message: c.commit.message.split('\n')[0].slice(0, 70),
      date: c.commit.author.date,
    })),
  }
}

function categorise(branches) {
  return {
    claude: branches.filter(b => b.name.startsWith('claude/')),
    codex: branches.filter(b => b.name.startsWith('codex/')),
    feat: branches.filter(b => /^(feat|fix|chore)\//.test(b.name)),
    other: branches.filter(b => !b.isDefault && !/^(claude|codex|feat|fix|chore)\//.test(b.name)),
    main: branches.filter(b => b.isDefault),
  }
}

function branchLine(b) {
  const tag = b.hasOpenPR ? 'PR open' : b.age > STALE_DAYS ? 'STALE  ' : 'active '
  return `  ${b.name.padEnd(55)} ${String(b.age).padStart(4)}d  ${fmtDate(b.lastDate)}  ${tag}`
}

function renderRepo(data) {
  const { repo, branches, openPRs, recentCommits } = data
  const cats = categorise(branches)
  const stale = [...cats.claude, ...cats.codex].filter(b => !b.hasOpenPR && b.age > STALE_DAYS)
  const lines = []

  lines.push(`## ${repo}`)
  lines.push(`Branches: ${branches.length}  Open PRs: ${openPRs.length}  Stale (no PR, >${STALE_DAYS}d): ${stale.length}`)
  lines.push('')

  for (const [label, list] of [
    ['claude', cats.claude],
    ['codex', cats.codex],
    ['feat/fix/chore', cats.feat],
    ['other', cats.other],
    ['default', cats.main],
  ]) {
    if (!list.length) continue
    lines.push(`### ${label}`)
    list.sort((a, b) => a.age - b.age).forEach(b => lines.push(branchLine(b)))
    lines.push('')
  }

  if (openPRs.length) {
    lines.push('### Open PRs')
    openPRs.forEach(pr => {
      const age = daysSince(pr.updatedAt)
      lines.push(`  #${pr.number} ${pr.draft ? '[draft] ' : ''}${pr.title.slice(0, 65).padEnd(65)}  updated ${age}d ago`)
    })
    lines.push('')
  }

  if (recentCommits.length) {
    lines.push(`### Recent commits to default branch (last ${RECENT_DAYS}d)`)
    recentCommits.forEach(c => lines.push(`  ${c.sha}  ${fmtDate(c.date)}  ${c.message}`))
    lines.push('')
  }

  if (stale.length) {
    lines.push('### Stale branches flagged for cleanup')
    stale.sort((a, b) => b.age - a.age).forEach(b =>
      lines.push(`  ${b.name}  (${b.age}d, last commit ${fmtDate(b.lastDate)})`)
    )
    lines.push('')
  }

  return lines.join('\n')
}

async function main() {
  if (!process.env.GITHUB_TOKEN) {
    console.error('GITHUB_TOKEN is required. Add it to .env or set it in the environment.')
    process.exit(1)
  }

  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN })
  const now = new Date().toISOString().replace('T', ' ').slice(0, 19)

  console.log('# PCA Repo Activity Report')
  console.log(`Generated: ${now} UTC  |  Stale threshold: ${STALE_DAYS}d  |  Recent window: ${RECENT_DAYS}d`)
  console.log('')

  for (const { owner, repo, defaultBranch } of REPOS) {
    try {
      process.stderr.write(`Fetching ${owner}/${repo}...\n`)
      const data = await getRepoActivity(octokit, owner, repo, defaultBranch)
      console.log(renderRepo(data))
    } catch (err) {
      console.error(`\nError fetching ${owner}/${repo}: ${err.message}\n`)
    }
  }
}

main()
