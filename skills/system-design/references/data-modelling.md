# Data Modelling

## Choosing the store

| Store | Shape it fits | Weak at |
|---|---|---|
| Relational (Postgres, MySQL) | entities with relationships, ad-hoc queries, transactions, reporting | single-node write ceiling, wide horizontal sharding |
| Document (MongoDB, DynamoDB) | whole aggregates fetched and written together, per-document schema drift | joins, cross-document transactions, ad-hoc aggregation |
| Key-value (Redis, DynamoDB KV) | lookups by known key, sessions, counters, caches | querying by anything but the key |
| Wide-column (Cassandra, Bigtable, HBase) | very high write volume, time-series access, known query patterns | flexible queries, aggregation, anything not in the partition key |
| Search (Elasticsearch, OpenSearch) | ranked full-text, facets, fuzzy matching | source of truth, transactions, exact accounting |
| Time-series (Timescale, InfluxDB, Prometheus) | metrics with retention and downsampling | transactional entities |
| Object store (S3) | blobs, files, backups, static assets | query, update-in-place, low-latency small reads |
| Graph (Neo4j) | variable-depth traversal, relationship-first queries | bulk aggregation, whole-dataset scans |

Default to the relational store. Add a second store only when a **named access pattern** fails on the first, and accept the real cost: dual writes, eventual consistency between them, and a reconciliation job. If you add search or an analytical store, feed it from the primary via CDC or an outbox — never by writing both sides in application code.

## Schema modelling

- **Normalize to 3NF first, denormalize only with a measured reason.** Name the read pattern and the query cost avoided. "For performance" without a number is a guess that will be paid for at write time and in consistency bugs.
- **Primary keys**: surrogate (`bigint` identity or UUIDv7) for identity; the natural/business key becomes a separate `UNIQUE` constraint. Never reuse a business value as the PK — business values change, and cascading a change through FKs is a data-loss event waiting for a bad day. Prefer UUIDv7/ULID over UUIDv4 when the key is exposed or generated client-side: they index sequentially instead of scattering b-tree inserts.
- **Foreign keys with explicit `ON DELETE`**: `RESTRICT` (default, safest), `CASCADE` (true ownership only — the child cannot exist alone), `SET NULL` (optional relation), `NO ACTION` when you need deferred checks. An unstated `ON DELETE` is an accident.
- **`NOT NULL` by default.** Nullable is a decision — if "unknown" is a real state, say so in the comment and handle it in queries; if not, reject it.
- **Money**: `NUMERIC(19,4)`/`DECIMAL`, or integer minor units with an explicit currency column. Never `float`/`double`, never a string. Rounding rules belong in the domain layer and must be documented (banker's vs half-up).
- **Time**: `timestamptz` in Postgres, UTC everywhere. Localize at presentation only. Store the timezone separately when the user's zone is meaningful data (recurring schedules, calendar events).
- **Enums**: a lookup table with an FK when values may grow, be renamed, or need metadata; a native `enum` or `CHECK` constraint when the set is truly fixed. Native enums require a migration to extend and cannot be reordered or removed.
- **Booleans**: name assertions (`is_active`, `has_shipped`). A boolean that will grow a third state should be an enum now.
- **JSONB**: only for genuinely variable shape (provider payloads, user-defined metadata). Document the expected schema, validate on write, and index (GIN) only the paths you query. A JSONB column used for core fields is a schema you refused to design.
- **Arrays**: prefer a child table when you need to query, join, or constrain the members.
- **Naming**: one convention, project-wide — `snake_case` tables and columns in SQL, singular or plural tables chosen once, `_at` suffix for timestamps, `_id` for FKs, `is_`/`has_` for booleans.
- **Constraints over conventions**: `CHECK` for ranges and formats, `UNIQUE` (including partial unique indexes) for business invariants, `NOT NULL` for required. Application validation is a UX layer, not a guarantee — the database is the last line that cannot be bypassed by a script, a migration, or a second service.

## Indexing

- **Index every FK** queried by parent. Unindexed FKs turn joins, `CASCADE` deletes, and existence checks into full scans.
- **Composite order matters**: equality columns first, then range/sort columns. `(tenant_id, created_at)` serves `WHERE tenant_id = ? ORDER BY created_at`; the reverse order serves neither well. A composite index also serves a prefix (`tenant_id` alone), so a separate index on the prefix is usually redundant.
- **Covering indexes** (`INCLUDE` columns) for hot read paths to skip the heap fetch.
- **Partial indexes** for skewed predicates — `WHERE deleted_at IS NULL` on a soft-deleted table is usually the single highest-value index you can add.
- **Index type by predicate**: B-tree (default: equality, ranges, sorting), hash (equality only, rarely worth it over B-tree), GIN (JSONB, arrays, full-text), GiST (geometric, ranges, nearest-neighbour), BRIN (huge append-only tables, clustered by the column, very small).
- **Don't index**: low-cardinality columns alone, write-heavy columns with no read pattern, or every column "just in case". Each index costs write throughput and must be maintained.
- **`EXPLAIN (ANALYZE, BUFFERS)` is the arbiter**, not intuition. An index the planner ignores is dead weight; a plan that changes with data volume is a plan you do not yet know.

## Queries

- **No N+1.** Count queries per request, don't read the ORM call. Fix with a join, a batched `IN`, or a dataloader.
- **Select explicit columns** in production paths. `SELECT *` breaks on schema change and moves data you never read.
- **Paginate everything unbounded**; keyset (`WHERE (created_at, id) < (:cursor_ts, :cursor_id) ORDER BY created_at DESC, id DESC LIMIT :n`) beats `OFFSET` — offset degrades linearly and skips or duplicates rows under concurrent writes.
- **Set a statement timeout** on request-path queries. An unbounded query is an outage waiting for a bad plan.
- **Never concatenate SQL.** Parameterized statements only, including migrations and admin scripts. Identifiers (table/column) cannot be parameters — allowlist them.
- **Aggregate in the database** when the result set is large; aggregate in the app only when the data is already there or the expression is not expressible.
- **`UNION ALL` over `UNION`** unless you need dedupe; `EXISTS` over `IN` for large subqueries; avoid functions on indexed columns in `WHERE` (`WHERE date(created_at) = …` cannot use the index — use a range).
- **`COUNT(*)` on filtered large sets is expensive** and gets worse with growth. Cache it, approximate it, or drop it from the contract.

## Transactions

- **Keep transactions short.** Never hold one open across a network call, a file read, or user think-time. Long transactions hold locks and bloat the vacuum.
- **Isolation**: know your engine's default before you rely on it — Postgres is `READ COMMITTED`, MySQL/InnoDB is `REPEATABLE READ`. `READ COMMITTED` plus explicit locking is the sane general default; `REPEATABLE READ` (snapshot isolation in Postgres) when a multi-statement read must see one consistent snapshot; `SERIALIZABLE` only for genuinely concurrent invariants, and then you must handle serialization failures with a retry. Postgres prevents dirty reads at every level; the anomalies left to cause are non-repeatable reads, phantoms, and write skew.
- **Lock ordering**: acquire locks in a consistent order (by id, ascending) to avoid deadlocks; keep the retry-on-deadlock path tested.
- **`SELECT … FOR UPDATE`** for read-modify-write on a contended row; `SKIP LOCKED` for queue-style workers.
- **Advisory locks** for cross-transaction mutual exclusion on a named resource (per-tenant migration, singleton job).

## Migrations

- **Expand → migrate → contract, across separate deploys**:
  1. Add the new nullable column/table (nothing reads it yet).
  2. Deploy code that writes both, reads old.
  3. Backfill in bounded batches, throttled, restartable.
  4. Switch reads to new and verify.
  5. Drop the old in a later release.
- **Locking**: adding a column with a non-constant default, changing a type, or adding a constraint with validation takes a full rewrite and a lock. Prefer nullable-add + backfill + `SET NOT NULL` via a validated `CHECK` (Postgres) or `NOT VALID` then `VALIDATE CONSTRAINT`.
- **Create indexes concurrently** (`CREATE INDEX CONCURRENTLY`) on live tables, outside a transaction block. Expect a failed concurrent build to leave an invalid index that must be dropped.
- **Every migration is reversible, or the risk is written down.** `down` must exist and be tested, or the migration is explicitly one-way with a stated recovery plan.
- **Never edit a migration that has run anywhere.** Add a new one.
- **Test against production-sized data**, not an empty schema, and always exercise the rollback path.
- **Set `lock_timeout` and `statement_timeout`** in migration sessions so a blocked migration fails instead of queueing every query behind itself.

## Partitioning and sharding

- **Partition by time** (range) for append-heavy tables: retention becomes `DROP PARTITION`, writes stay in the hot partition, and indexes stay small.
- **Partition by tenant hash** for multi-tenant scale, keeping each tenant's data on one partition.
- **Shard only when one primary cannot absorb the writes.** It costs cross-shard joins, distributed transactions, and a resharding project. Choose the shard key by write distribution and dominant query; both must agree.
- **Hot partitions** come from skewed keys (one whale tenant, one counter row). Counter rows can be split and summed; whale tenants can be isolated to their own shard.

## Integrity, audit, and lifecycle

- **Enforce invariants in the database** where it can: `CHECK`, `UNIQUE`, `NOT NULL`, FK, exclusion constraints.
- **Soft delete only when audit or recovery is a real requirement.** Otherwise hard delete and let backups serve recovery. Soft delete adds a predicate to every query, a partial index to every table, and a class of bug where a forgotten `WHERE deleted_at IS NULL` resurrects deleted data.
- **Audit columns**: `created_at`, `updated_at` (maintained by trigger or ORM, not by hope), and actor identity on anything a regulator or customer may ask about. Append-only audit tables for money, permissions, and state transitions.
- **Retention**: define it per table at design time. Unbounded growth is a latency and cost bug that surfaces a year later.
- **PII**: encrypt in transit and at rest; column-level encryption or tokenization for identifiers; never in logs or analytics exports; support deletion by subject, which means a delete path through every derived store — plan it before the first copy exists.
- **Destructive operations** (`DROP`, `TRUNCATE`, unqualified `DELETE`/`UPDATE`) need a confirmation path, a row-count preview first, and a transaction where the engine supports it. `DELETE FROM t` without `WHERE` is never a fix.

## Verification checklist

1. `EXPLAIN (ANALYZE, BUFFERS)` every hot query — index usage, no sequential scan on a large table, no nested loop over a big set, row estimate close to actual.
2. Every FK has an index that serves its join, and every `CASCADE` path is indexed.
3. Every request-path list query is paginated, ordered deterministically, and covered by a statement timeout.
4. Every business invariant is enforced by a constraint, not only by application code.
5. Migrations dry-run against production-sized data, with the rollback exercised.
6. Every new table has an owner, a retention rule, and an audit story if it holds money, permissions, or personal data.
