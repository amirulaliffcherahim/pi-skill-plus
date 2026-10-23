# Design Walkthrough

For when the deliverable is a document, a review, or an interview answer rather than code.

## Document section order

Write these in order; each section is short and ends in a decision.

1. **Problem and scope** — what is being built, for whom, and explicitly what is out of scope.
2. **Requirements** — functional flows; non-functional numbers (QPS, data size, p95 latency, availability, consistency, retention, RPO/RTO).
3. **Capacity estimate** — the arithmetic from those numbers, one line per quantity.
4. **API contract** — resources, operations, error shape, versioning, pagination, auth. Link or embed the OpenAPI.
5. **Data model** — tables/collections, keys, indexes, retention. One diagram, then the DDL or schema.
6. **Components and data flow** — the boxes, what each owns, and the synchronous vs asynchronous edges between them.
7. **Consistency and failure** — what is strongly consistent vs eventual, and the failure table (dependency down, partial write, hot partition, region loss).
8. **Capacity and cost** — where it breaks at 10×, and the first thing you would change.
9. **Operability** — metrics, SLOs, alerts, runbook skeleton, rollout and rollback.
10. **Decisions and alternatives** — ADR-style: decision, context, alternatives rejected and why.
11. **Open questions** — each with an owner and the date it must be answered.

Sections 1–3 are the ones skipped under time pressure and the ones that determine whether 4–8 are right.

## Estimation worksheet

Fill this in before drawing anything:

```text
DAU                        = ____________
actions per user per day   = ____________        (split read / write)
read QPS   = DAU × reads  / 86400 = ____________
write QPS  = DAU × writes / 86400 = ____________
peak factor (2–3×)         = ____________  → peak read/write QPS
record size                = ____________  → bytes/day, bytes/year
replicas + index overhead  = ____________  → total storage/year
payload × QPS              = ____________  → egress bandwidth
p95 budget                 = ____________ ms
  hops allowed = budget ÷ (network RTT + dependency time)
working set (80/20)        = ____________  → cache size
first bottleneck           = ____________  at ____________ (number)
```

Then compute the one number that decides the architecture: writes/s against a single primary, or data size against one node's disk, or request rate against one cache node.

## Worked example — short link service

**Requirements.** Create a short link from a long URL; redirect; optional expiry; click count. 10 M new links/month, 100:1 read:write, p95 redirect < 50 ms global, 99.99% redirect availability, counts may lag by minutes.

**Numbers.** 10 M/month ≈ 3.9 writes/s average, ~12/s peak — trivial for one primary. Reads ≈ 390/s average, ~1 200/s peak. 120 M links/year × ~500 B ≈ 60 GB/year plus indexes — fits one node for years. **The bottleneck is redirect latency and availability, not storage or write throughput.** That single sentence removes Kafka, sharding, and a graph database from the design.

**Contract.**

```text
POST /v1/links            → 201, Location: /v1/links/{code}
GET  /v1/links/{code}     → 200 link metadata | 404
GET  /v1/links            → cursor-paginated list for the caller
DELETE /v1/links/{code}   → 204
GET  /{code}              → 302 to target (the hot path, no auth)
```

`POST` takes an `Idempotency-Key`; the short code is generated server-side (base62 of a sequence, or a random 7-char space with a uniqueness constraint and retry).

**Data.** `links(code PK, target_url, owner_id, created_at, expires_at, deleted_at)`, index on `(owner_id, created_at DESC)` for the list, partial index `WHERE deleted_at IS NULL`. `link_clicks` as an append-only counter table or a Redis counter flushed in batches — never an update per redirect on the primary.

**Flow.** Redirect resolves from cache-aside Redis (`link:{code}`, TTL 24 h + jitter); miss reads the primary and populates. Negative-cache 404s for 60 s. Click counting is fire-and-forget into a queue, aggregated asynchronously — the redirect path does no writes.

**Failure behaviour.** Redis down → fall through to the primary with a circuit breaker and a lower connection-pool ceiling; the primary is sized for the fallback. Primary read replica lag → redirects may serve a just-created link as 404 for a second; the create response returns the code so the creator's own client does not depend on the replica. Expiry is enforced on read, not by a deletion job, so a failed cron does not serve dead links.

**At 10×.** Redirects go to the edge (CDN/edge KV with a short TTL), link creation shards by `owner_id`, click aggregation becomes a stream with a pre-aggregated rollup.

**Rejected.** Kafka for click counts (a queue suffices at 400/s). Sharding (single node holds five years of data). A NoSQL store for links (the access pattern is a key lookup, but the list-by-owner query and the transactional create are free in a relational store).

That paragraph structure — requirements, numbers, contract, data, flow, failure, 10×, rejected — is the shape to reuse.

## Reviewing an existing design

Ask these in order; each has a specific failure it is looking for.

| Question | Failure it exposes |
|---|---|
| What is the p95 budget, and how many network hops fit inside it? | a design that cannot meet its own latency target |
| What breaks first at 10×, and what is the number? | no capacity model, only a diagram |
| Which writes are not idempotent, and what happens on a client retry? | duplicate orders, double charges |
| Where do two systems get written to outside a transaction? | silently lost events, drifting replicas |
| Which queries have a verified plan? | unindexed FK, hidden N+1, unbounded scan |
| What does a client see when each dependency is down? | retry storms, cascading failure |
| How is a breaking change shipped? | in-place field rename with no version |
| Which copies of personal data exist, and how is one deleted? | PII sprawl with no deletion path |
| What is the restore time from backup, measured? | untested backups |
| What is the rollback for this deploy? | forward-only migration with no plan |

A design that answers all ten in one line each is reviewable. A design that answers none in a hundred slides is a diagram with prose attached.

## Interview framing

If the ask is an interview rather than a build: clarify scale in 2–3 minutes and state assumptions aloud, compute the numbers visibly so they can be corrected early, draw the high-level flow with one named storage choice and its reason, deep-dive the single component where the trade-off lives, say explicitly what breaks at 10× and what you would change, then close on trade-offs and next steps rather than a summary of the drawing.

Scoring traps: an unstated assumption carrying the whole design, a cache with no invalidation, a shard key that concentrates writes, an async step with a non-idempotent consumer, and numbers that never connect to a component choice.
