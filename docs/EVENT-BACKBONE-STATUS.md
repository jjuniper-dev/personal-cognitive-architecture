# Event Backbone — Current State vs Design Target

**Status:** Design aspiration ahead of current implementation  
**Last revised:** 2026-05-30

---

## What the Design Specifies

`AGENTS.md` in this repository defines the event backbone aspiration:

> Events should be:
> - explicit
> - schema-validatable
> - timestamped
> - source-linked
> - traceable to the producing component
> - safe to replay or ignore where practical

This is the **target**. The current running system does not yet meet all of these properties.

---

## What Is Actually Running

The current event integration model in `jjuniper-dev/pca` is **HTTP webhook request/response**:

| Property | Current State |
|---|---|
| Transport | HTTP POST to n8n webhook endpoints (`/webhook/pca/*`) |
| Pattern | Synchronous request/response — caller blocks until workflow completes |
| Schema validation | Partial — WF10 validates `type` + `source`; other endpoints unvalidated |
| Timestamps | Auto-filled by WF10 on capture |
| Traceability | n8n execution logs in PostgreSQL; no distributed trace IDs |
| Replayability | Not supported — re-posting a webhook creates a new execution |
| Message broker | None — no Kafka, Redis Streams, NATS, or similar |
| Queue | None — WF13 failure alerting polls on a 15-min schedule, not triggered by failure events |

**WF13 is polling, not event-driven:** Failure alerting runs on a schedule (daily digest at 08:00). A true event backbone would emit on failure occurrence and trigger alerting immediately.

---

## Why This Is Acceptable at Current Scale

The system has one operator, one machine, and ~14 workflows. HTTP webhooks are:

- Simpler to operate and debug
- Fully observable via n8n execution logs
- Already working reliably

Adding a message broker (Kafka, Redis Streams, NATS) introduces operational overhead not yet justified. The upgrade trigger is: multiple producers, consumers needing replay, or throughput exceeding what synchronous webhooks can handle.

---

## The Terminology Gap

`AGENTS.md` says: *"Do not create a new workflow path that bypasses the event model."*

The current HTTP webhook paths **are** the effective event model — they just aren't async or replayable. Any new integration should use the existing `/webhook/pca/*` pattern rather than direct service-to-service calls.

---

## Near-Term Hardening (Before Adding Infrastructure)

These steps move the system toward the AGENTS.md event backbone properties without requiring a broker:

1. **Add `trace_id` to all WF10 payloads** — enables correlation across captures; WF-Learn and WF-Ayla should include this field
2. **Log all incoming webhook payloads to Qdrant** — creates a queryable event log that approximates replay capability
3. **WF13: Add triggered mode** — call WF13 from the health check script on detected failure, in addition to the polling schedule
4. **Document `/webhook/pca/*` as the event API surface** — treat these endpoints as the event bus and enforce schema validation on all of them

---

## Path to True Event Backbone (If Scale Justifies It)

**Option A — Redis Streams via n8n (no new infrastructure)**  
n8n has a Redis node. Producers POST to a Redis Stream; consumers subscribe. Events become async and replayable. Redis is already in the pca stack (unconfirmed per `pca-architecture.md`).

**Option B — n8n Queue Mode**  
n8n supports queue mode with a Redis backend. Turns workflow executions into queued jobs with backpressure and retries. Higher operational overhead.

**Option C — Accept HTTP hybrid as sufficient**  
Harden existing webhooks: add `X-Event-ID` headers, log all payloads to a dedicated Qdrant collection, replay by re-POSTing from log. Event-like behavior without a broker.

**Upgrade trigger:** Any of these:
- A capture workflow misses events because the caller doesn't wait for the response
- A downstream consumer needs to process the same event more than once
- Sustained throughput exceeds ~100 events/minute
