# Personal Cognitive Architecture (PCA)

## React Profile App (New)

This repository now includes a lightweight React app for building and tracking a personal cognitive profile.

### Setup

```
npm install
```

### Run (dev)

```
npm run dev
```

### Build (production)

```
npm run build
npm run preview
```

### ⚠️ Neo4j Scripts Warning

The following scripts perform write operations against a Neo4j database:

- `npm run populate-graph`
- `npm run populate-markov`

These scripts are **guarded** and require explicit confirmation:

```
CONFIRM_NEO4J_WRITE=true
```

You must also set:

- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`

They will refuse to run with default or missing credentials.

---

(Original README content continues below)

## One-Line Definition

A cognitive operating system that captures, evaluates, integrates, and activates knowledge to continuously improve human thinking and decision-making.

... (rest unchanged)
