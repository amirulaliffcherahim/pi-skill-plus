# Scaling & Reliability

## Numbers worth memorising

Approximate latencies, cache to network. Treat as orders of magnitude; measure your own stack.

| Operation | Time |
|---|---|
| L1 cache reference | 0.5 ns |
| Branch mispredict | 5 ns |
| L2 cache reference | 7 ns |
| Mutex lock/unlock | 25 ns |
| Main memory reference | 100 ns |
| Compress 1 KB (zlib) | 3 µs |
| Send 1 KB over 1 Gbps | 10 µs |
| Read 4 KB random from SSD | 20–150 µs |
| Read 1 MB sequentially from memory | 250 µs |
| Round trip within one datacenter | 0.5 ms |
| Read 1 MB sequentially from SSD | 1 ms |
| Read 1 MB sequentially from disk | 20 ms |
| Disk seek (spinning) | 10 ms |
| Round trip CA ↔ Netherlands | 150 ms |

Two consequences to design around: **network round trips are the unit of cost** in a distributed design, and **sequential access beats random access by orders of magnitude** — which is why append-only logs, LSM stores, and batched reads win at volume.

Availability, per year of downtime:

| Target | Downtime/year | Downtime/month |
|---|---|---|
| 99% | 3.65 days | 7.2 h |
| 99.9% | 8.77 h | 43.8 min |
| 99.95% | 4.38 h | 21.9 min |
| 99.99% | 52.6 min | 4.4 min |
| 99.999% | 5.26 min | 26 s |

Availability composes badly in series and well in parallel:

- Serial dependency chain: `A_total = A1 × A2 × … × An`. Ten 99.9% services in a chain give ~99.0%.
- Redundant replicas: `A_total = 1 − (1 − A)^n`. Two 99.9% replicas without a shared failure domain give ~99.9999%; with a shared failure domain (same AZ, same config, same deploy) you get 99.9% and a correlated outage.

Use the numbers to reject impossible targets early: a 50 ms p95 budget cannot afford three serial cross-region calls.

## Back-of-envelope

Do this before the diagram, in this order:

1. **Users** — DAU, concurrent sessions (`DAU × 5–20%`), growth/year.
2. **Traffic** — `QPS = actions/day ÷ 86_400`, peak = 2–3× average. Split read and write QPS.
3. **Data** — bytes/record × records/day × 365, times replica count, plus index overhead (~20–40%).
4. **Bandwidth** — payload size × QPS at the edge.
5. **Cache size** — working set from the 80/20 rule, not total data.
6. **Bottleneck** — which of the above hits a single-node limit first.

Single-node planning limits worth knowing: a well-tuned relational primary handles low thousands of simple writes/s and tens of thousands of reads/s; a single Redis node hundreds of thousands of ops/s; one TCP connection's throughput is bounded by bandwidth-delay product long before CPU.

## Scaling up vs out

Order of escalation, each cheaper than the next until it isn't:

1. Fix the query, add the index, remove the N+1.
2. Add a cache for the read path.
3. Vertical scale — simplest, and often all a business needs. Ceiling is cost and single point of failure.
4. Read replicas for read-heavy traffic.
5. Stateless app tier behind a load balancer (sessions in a store, not in process memory).
6. Partition/shard the write path — the last resort, because it costs joins, transactions, and operational simplicity.

App tier scales horizontally only if it is stateless: session, uploaded file, and in-memory cache state move to shared stores. Sticky sessions are a workaround that turns a lost node into lost users.

## Replication

| Model | Use when | Cost |
|---|---|---|
| Single-leader | Default. One writer, N read replicas | write throughput capped by one node; replica lag |
| Multi-leader | Multi-region writes with local latency needs | write conflicts need resolution (LWW, CRDT, app merge) |
| Leaderless (quorum) | Very high write availability, tunable consistency | read repair, quorum sizing, no ordering |

Async replication lag breaks read-your-writes: a user writes, is routed to a lagging replica, and does not see their own change. Fix by routing that user's reads to the leader for a window, by session stickiness, or by passing a write watermark the replica waits for.

Synchronous replication buys zero data loss at the price of write latency and a write path that fails when a replica is unreachable. Quorum (`W + R > N`) is the middle ground.

## Partitioning and sharding

Partition when one node can no longer hold the data or absorb the writes — not before.

- **Key choice dominates everything.** It must have high cardinality, spread writes evenly, and match the dominant query. A tenant key concentrates a whale tenant; a timestamp key concentrates today's writes.
- **Avoid cross-shard joins and transactions.** If the query needs them, the shard key is wrong.
- **Hot partition** is the common failure: one key (celebrity user, single counter, current day) absorbs the load. Remedies: split the key, add a random suffix and aggregate, or pre-shard.
- **Resharding is the expensive operation.** Consistent hashing with virtual nodes moves `1/n` of the keys instead of everything; directory-based mapping is easier to reason about but adds a lookup.
- **Partition by time** (range) makes retention trivial (drop old partitions) and writes append-only.

## Caching

Default pattern: **cache-aside** — read cache, miss, read source, populate with TTL.

| Pattern | Writes | Read latency | Consistency | Use |
|---|---|---|---|---|
| Cache-aside | app writes source, then invalidates | miss = source | eventual | default |
| Read-through | cache loads on miss | same | eventual | cache owns loading |
| Write-through | cache writes source synchronously | consistent-ish | stronger | small hot working set |
| Write-behind | cache buffers, flushes async | fastest | loss window | write-heavy, loss-tolerant |
| Refresh-ahead | pre-refresh before expiry | no miss spike | eventual | predictable hot keys |

Rules that prevent the classic outages:

- **TTL with jitter** (`ttl × (0.8 + rand × 0.4)`) so keys do not expire together.
- **Single-flight** (per-key mutex or request coalescing) so a hot key's expiry does not send 10k requests to the database.
- **Negative caching** for not-found lookups, with a shorter TTL.
- **Key namespacing and versioning** (`v2:user:123`) so a schema change is a cache flush, not a migration.
- **Never cache an authorization decision** without a short TTL and explicit invalidation on permission change.
- **Measure hit ratio.** A cache under ~80% hit rate on the hot path is paying complexity for nothing.

Invalidation is the hard half. Prefer short TTLs plus write-time invalidate over elaborate dependency graphs. Two sources of truth with no invalidation path is a permanent inconsistency.

## CDN and edge

- Immutable assets: hash in the filename, `Cache-Control: public, max-age=31536000, immutable`.
- HTML and API responses: short `max-age` + `stale-while-revalidate`, or `private, no-store` when per-user.
- `Vary` on what actually varies (encoding, auth-relevant headers) — never on nothing, and never wildcarding by accident.
- Have a purge story before you set a long TTL, and remember a purge is eventually consistent at the edge.

## Async, queues, and streams

Move work off the request path when it is slower than the response budget, retryable, or needs fan-out.

- **At-least-once is the default reality.** Consumers must be idempotent (dedupe key, upsert, or processed-message table). "Exactly-once" is exactly-once within one broker+consumer pair, and costs ordering and throughput.
- **Ordering exists only within a partition.** Choose the partition key as the ordering key; global ordering means one partition and no scale.
- **Dead-letter queue with an inspection path**, plus a bounded retry count and an alert on DLQ depth.
- **Backpressure over buffering.** A queue that grows without bound converts a slow consumer into a memory outage. Bound it, then shed or throttle.
- **Outbox pattern** for database + queue: write the event row in the same transaction as the state change, publish from the outbox, mark sent. Prevents the dual-write lost-message hole.
- **Stream vs queue**: a queue deletes on ack (task distribution); a log retains and replays (event sourcing, multiple consumers, reprocessing). Replay is the reason to choose a log.

## Resilience patterns

| Pattern | Problem it solves | Detail that matters |
|---|---|---|
| Timeout + deadline propagation | slow dependency consumes all workers | each hop gets the caller's remaining budget, not a fresh constant |
| Retry with backoff + jitter | transient failure | only idempotent ops, capped attempts, full jitter to break synchronised retries |
| Circuit breaker | failing dependency amplifies load | closed → open on error threshold → half-open probe → closed; fail fast, keep the fallback cheap |
| Bulkhead | one dependency exhausts a shared pool | separate connection pools/threads per dependency |
| Load shedding | overload | reject the cheapest-to-drop requests first, with `503` + `Retry-After` |
| Graceful degradation | partial outage | named fallbacks: stale cache, omit a section, serve read-only |
| Health checks | routing and restarts | liveness = process alive; readiness = can serve traffic; keep dependency checks out of liveness |
| Graceful shutdown | dropped requests on deploy | stop accepting, drain in-flight, then exit |

Timeouts and retries multiply: three hops × three retries × two seconds is a 54-second tail. Set the entry-point budget and derive downward.

## Rate limiting

| Algorithm | Behaviour | Use |
|---|---|---|
| Token bucket | allows bursts up to bucket size, then steady rate | default for APIs |
| Leaky bucket | smooths to constant output | protecting a downstream |
| Fixed window | simple, but allows 2× at the boundary | internal, low stakes |
| Sliding window (counter or log) | accurate, more state | strict quotas, billing |

Limit on the identity that matters (API key, user, tenant, IP), and make the limit dimensions additive rather than one global counter. Return `429` with `Retry-After` and the current `RateLimit-*` state. Distributed limiting needs a shared store (Redis) with an atomic script — a per-node counter silently multiplies the limit by node count.

## Observability

- **Metrics**: RED for services (rate, errors, duration), USE for resources (utilisation, saturation, errors). Percentiles, never averages — an average hides the tail that users feel.
- **Logs**: structured, with request/trace id, sampled at volume, never carrying secrets or full PII payloads.
- **Traces**: W3C `traceparent` propagated on every hop; spans on outbound calls, queue publish/consume, and the DB.
- **SLO + error budget** rather than raw thresholds: define the measurable objective, alert when the burn rate threatens it.
- **Alert on symptoms** (error rate, latency, saturation) and page a human only for things a human must act on now.

## Data protection

- **Backups are unverified until restored.** Run the restore drill on a schedule and time it against RTO.
- **RPO/RTO belong in the requirements**, because they decide sync vs async replication and cross-region spend.
- **Point-in-time recovery** for anything a human can delete by accident; logical dumps alone lose the last hours.
- **Multi-AZ** for node/AZ failure, **multi-region** for region failure and latency — and multi-region means deciding which side wins on split brain before you need it.
