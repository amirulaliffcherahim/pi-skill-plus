---
name: system-design
description: System design guidance for architecture, API contracts, and the data layer, with review checklists. Use when choosing components, storage or caching; designing or versioning endpoints; modelling tables and indexes; fixing a slow query with EXPLAIN; planning a zero-downtime migration; or reviewing a design for bottlenecks and failure modes.
---

# System Design

Run the five steps in order. Each ends on a criterion; the step is not done until the criterion is met. Jumping to components because that is the visible part produces a diagram that cannot answer "what happens at 10x".

## 1. Requirements

Collect three lists:

- **Functional** — the 3–5 flows that matter, one sentence each, with the actor and the outcome.
- **Non-functional, as numbers** — reads/s and writes/s now and at 10x, data volume and growth per year, p95 latency budget, availability target, consistency requirement, retention, recovery targets (RPO/RTO).
- **Constraints** — existing stack, team size, budget, compliance regime, deadline, and what you are not allowed to change.

**Criterion:** every non-functional line has a number, or reads `assumed <value> — confirm`. An unqualified "should be scalable" is an unresolved requirement, not a requirement.

## 2. Numbers

Convert requirements into load before choosing anything:

- `QPS = DAU × actions/user/day ÷ 86_400`; peak ≈ 2–3× average.
- Storage/year = `rows/year × bytes/row × replication factor`.
- Read:write ratio decides caching and replication strategy, not storage choice alone.
- Compare against the latency table in [scaling-and-reliability.md](references/scaling-and-reliability.md) — network and disk round trips dominate the arithmetic.

**Criterion:** you can name the resource that runs out first (single-leader write throughput, network egress, hot partition, storage, connection pool) and the number at which it happens.

## 3. Components

Pick per concern, then justify against the simpler alternative.

| Concern | Default | Switch when |
|---|---|---|
| Storage | relational, single node | write throughput or data size exceeds one node; shape is genuinely schemaless; the access pattern is a lookup by key; full-text/ranked search is a product feature |
| Cache | cache-aside in the app, TTL + jitter | read-heavy and the source tolerates staleness; needs multi-writer consistency (then cache less) |
| Consistency | strong on writes you own, eventual on derived/read models | user must see their own write (read-your-writes), money/stock (strong), feeds/counters (eventual) |
| Sync vs async | synchronous until the response time budget breaks | work is slower than the budget, is retryable later, or must fan out to N consumers — then queue it |
| Deployable shape | modular monolith | a component needs an independent scaling curve, release cadence, or team ownership |
| API style | REST over HTTP/JSON | internal service-to-service at high throughput (gRPC); many clients wanting different shapes (GraphQL); decoupled consumers (events) |

**Criterion:** for every component, one line of form "chosen for X load; the simpler alternative Y was rejected because Z". Components you cannot justify with a number or a concrete failure belong in a "not yet" list.

## 4. Contract

Write the contract before the implementation: resources, methods, payloads, error shape, and the schema it persists to.

- **API** — full rules in [api-design.md](references/api-design.md): nouns from the domain, plural collections, kebab-case paths, cursor pagination, one error shape, one convention bundle for casing/versioning/idempotency chosen once rather than mixed, deprecation headers.
- **Data** — full rules in [data-modelling.md](references/data-modelling.md): 3NF first, explicit `ON DELETE`, integer money, UTC time, indexed FKs, verified query plans, expand→migrate→contract migrations.

**Criterion:** the API exists as OpenAPI 3.1 (or proto/schema) with request, response, error, and auth for every operation, and each endpoint maps to a table and index that serves it. A payload with no schema behind it is not a contract.

## 5. Failure modes

Walk the design through each, and write the behaviour, not the intention:

| Failure | Answer it with |
|---|---|
| Dependency slow (not down) | deadline propagated from the entry point, timeout < caller's remaining budget |
| Dependency down | circuit breaker, fallback (stale cache, degraded field, queued write), never an unbounded retry |
| Retry storm | exponential backoff + jitter, capped attempts, retry only idempotent work |
| Traffic spike | bounded queues (shed, don't grow), rate limit with `429`/`503` + `Retry-After`, per-tenant fairness |
| Partial write across two systems | outbox or saga with compensating action; document which side wins |
| Hot partition | shard by a key with even write distribution, or split the counter/hot row |
| Region/AZ loss | what serves during failover, and the RPO you accept |
| Operator error | tested restore, `DROP`/`DELETE` guard rails |

**Criterion:** each row has an owner behaviour. "It should be resilient" and "we'll monitor it" do not answer a row.

## Non-negotiables

These hold in every design regardless of scale; they are cheap now and unfixable later.

1. **Idempotency on any mutating call that can be retried** — idempotency key with stored response, or a natural uniqueness constraint.
2. **Every collection bounded** — pagination plus a maximum page size on every list endpoint.
3. **Money as integer minor units or `NUMERIC`**, never floating point; **time stored UTC**, localized at the edge.
4. **Every foreign key indexed**, and every hot query checked with `EXPLAIN ANALYZE` rather than intuition.
5. **One error shape with a machine-readable code** — never a `200` carrying `{"success": false}`.
6. **Break nothing silently** — additive change ships now, breaking change ships behind a new version with a deprecation window.
7. **Every remote call has a timeout**, and every retry loop has a bound and jitter.

## Anti-patterns

- **Premature distribution.** Splitting services before the monolith's wall is measured buys network partitions and distributed transactions for nothing.
- **Two sources of truth.** Dual writes to database and queue/warehouse without an outbox or CDC.
- **Cache without invalidation.** A cache with no eviction story is a bug with a TTL.
- **N+1 behind an ORM**, `SELECT *` in production paths, unbounded query on a request path.
- **Enum as an unconstrained string**, `float` money, local-time storage.
- **Design by resume.** Adding Kafka, a service mesh, or a graph database because it is in the diagram you copied, with no requirement that names it.

## Deliverable

When the ask is a document rather than code — design doc, SRS/SDS section, interview answer — use [design-walkthrough.md](references/design-walkthrough.md) for the section order, the estimation worksheet, and a worked example.

## References

- [scaling-and-reliability.md](references/scaling-and-reliability.md) — latency/availability numbers, replication, sharding, caching, queues, resilience patterns, rate limiting, observability. Read for steps 2 and 5.
- [api-design.md](references/api-design.md) — resource and URL rules, methods, status codes, versioning, pagination, errors, idempotency, long-running operations, conditional requests, security, OpenAPI. Read for step 4.
- [data-modelling.md](references/data-modelling.md) — keys, types, constraints, index selection, query and transaction rules, partitioning, migrations, integrity, PII. Read for step 4.
- [design-walkthrough.md](references/design-walkthrough.md) — section order, estimation worksheet, worked short-link example, review checklist. Read when producing the document.
- [sources.md](references/sources.md) — the upstream references this knowledge is drawn from, and what each is worth opening for.
