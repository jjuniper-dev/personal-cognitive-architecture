[![Header](https://capsule-render.vercel.app/api?type=waving&color=0:0d1f2d,50:1a3a4a,100:0d1f2d&height=280&section=header&text=Personal%20Cognitive%20Architecture&fontSize=42&fontColor=e0f2f1&animation=fadeIn&fontAlignY=38&desc=Capture%20%E2%80%A2%20Reconcile%20%E2%80%A2%20Activate%20%E2%80%A2%20Local-first%20AI%20infrastructure&descSize=18&descAlignY=58)](https://github.com/jjuniper-dev/personal-cognitive-architecture)

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=1000&color=4DB6AC&center=true&vCenter=true&multiline=false&repeat=true&width=650&lines=Orchestrator-worker+agent+patterns;Neo4j+knowledge+graph+%2B+Obsidian+vault;n8n+workflow+automation+%7C+local-first;34+use+cases+across+8+clusters;Sprint+5+dual-agent+validation+layer" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active%20Build-4DB6AC?style=flat&logoColor=white" />
  <img src="https://img.shields.io/badge/Sprint-5-1a3a4a?style=flat" />
  <img src="https://img.shields.io/badge/UCs-34%20mapped-4DB6AC?style=flat" />
  <img src="https://img.shields.io/badge/License-Private-555?style=flat" />
</p>

---

## 🧠 What this is

A cognitive operating system — not a note-taking app, not a chatbot wrapper. A designed system that captures knowledge from multiple modalities, evaluates it, reconciles it against existing understanding, and activates it through AI agents and automated workflows.

Built local-first, self-hosted, privacy-by-design. Ayla is the user-facing assistant within the PCA system.

---

## 🏗️ Five-Layer Architecture

| Layer | Purpose | Stack |
|-------|---------|-------|
| **L1** Knowledge & Control | Persistent memory, vault, graph | ![Neo4j](https://skillicons.dev/icons?i=neo4j) ![Obsidian](https://skillicons.dev/icons?i=obsidian) |
| **L2** Agent Runtime | Orchestrator-worker pattern | ![Claude](https://img.shields.io/badge/Claude-Sonnet%20%2F%20Haiku-4DB6AC?style=flat) |
| **L3** Workflow & Integration | Automation, webhooks, pipelines | ![n8n](https://skillicons.dev/icons?i=n8n) |
| **L4** Infrastructure | Mesh networking, containers | ![Docker](https://skillicons.dev/icons?i=docker) ![Linux](https://skillicons.dev/icons?i=linux) |
| **L5** AI Models | Cloud + local inference | ![Python](https://skillicons.dev/icons?i=python) |

---

## 🛠️ Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=neo4j,docker,python,fastapi,git,github,obsidian,n8n,linux" />
</p>

| Component | Role | Status |
|-----------|------|--------|
| **n8n** (Docker) | Workflow orchestration — L3 | ✅ Live |
| **Neo4j** (Docker) | Knowledge graph — L1 | ✅ Live |
| **Obsidian** (`050926_vault`) | Canonical vault — L1 | ✅ Live |
| **Tailscale** | Mesh network — L4 | ✅ Live |
| **Claude Sonnet** `T=0.3` | Orchestrator agent — L2 | ✅ Active |
| **Claude Haiku** `T=0.8` | Critical review agent — L2 | ✅ Active |
| **OpenClaw** | L2 gateway (provisional) | 🟡 NanoClaw under eval |
| **Whisper** | Transcription — L5 | 🟡 API interim / RTX 3090 planned |
| **iOS capture pipeline** | Vault ingest — L3 | 🔴 Gating dependency |

---

## 📦 Repository Structure

```
personal-cognitive-architecture/
├── src/
│   └── capture-api/        # FastAPI capture layer (iOS → Neo4j → n8n)
├── docs/
│   ├── uc-profiles/        # 34 UC full profiles (trigger, flow, tools, deps)
│   └── *.md                # Architecture, sprint docs, decision logs
├── agents/                 # Agent definitions
├── workflows/              # n8n workflow exports
├── schemas/                # Neo4j and data schemas
└── scripts/                # Utility scripts
```

---

## 🗂️ Use Case Clusters

<details>
<summary>34 UCs across 8 clusters — click to expand</summary>

| Cluster | UCs | Status |
|---------|-----|--------|
| 🧠 Personal Knowledge | UC 01–05 | 🟡 UC-01 in progress |
| ⚙️ Automation | UC 06–10 | 🟡 UC-07 migrating Zapier→n8n |
| 🎯 Lifestyle | UC 11–14 | 🔴 Not started |
| 💰 Finance | UC 15–18 | 🔴 Blocked on UC-16 bank connectivity |
| 🌐 Open Source | UC 19–22 | 🔴 Not started |
| 🏛️ Enterprise Architecture | UC 23–28 | 🟡 UC-25 active |
| 📊 Data & Platform Strategy | UC 29–31 | 🔴 Not started |
| 📢 Knowledge Publishing | UC 32–34 | 🔴 Not started |

Full profiles: [`docs/uc-profiles/`](./docs/uc-profiles/)

</details>

---

## 🤖 Agent Pattern

```
[Ayla Orchestrator — Sonnet T=0.3]
        │
        ├──▶ [Worker: Knowledge Query — Haiku]
        ├──▶ [Worker: Memory Recall — Haiku]
        ├──▶ [Worker: Web Search — Haiku]
        ├──▶ [Worker: Workflow Trigger]
        └──▶ [Critical Review — Haiku T=0.8]
```

Workers are n8n sub-workflows exposed as tools — not autonomous agents.

---

## 🔴 Critical Path

1. **iOS capture pipeline** → unblocks UC-01, 02, 03
2. **UC-07 Zapier → n8n migration** → quick win
3. **UC-16 bank connectivity decision** (SimpleFIN / Flinks / CSV) → unblocks Finance cluster
4. **UC-01 stable** → unblocks UC-03, 04, 05
5. **UC-06 Ayla routing layer** → unblocks Lifestyle + Automation clusters

---

## 📁 Related Repos

| Repo | Purpose |
|------|--------|
| [`jjuniper-dev/pca`](https://github.com/jjuniper-dev/pca) | Live operational workspace — active scripts, n8n workflows, BACKLOG, and task queue |
| [`jjuniper-dev/Obsidian`](https://github.com/jjuniper-dev/Obsidian) | Vault reference — structure and templates only |
| [`jjuniper-dev/status-site`](https://github.com/jjuniper-dev/status-site) | HC/PHAC AI Project Dashboard (PATH/HAIL tracking) |

---

[![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:0d1f2d,50:1a3a4a,100:0d1f2d&height=120&section=footer)](https://github.com/jjuniper-dev/personal-cognitive-architecture)
