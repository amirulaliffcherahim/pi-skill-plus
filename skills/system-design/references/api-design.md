# API Design

The API is the contract: other teams' code, mobile clients you cannot force-update, and public integrations depend on it. Everything below is chosen so that the contract can survive change.

## Style choice

| Style | Strengths | Costs | Choose when |
|---|---|---|---|
| REST/JSON | cacheable, universal tooling, inspectable | over/under-fetching, chatty | default for anything browser or third-party facing |
| GraphQL | client-specified shape, one endpoint, strong schema | caching is hard, server-side complexity analysis required, N+1 risk | many clients with genuinely different data needs over one graph |
| gRPC | typed, fast, streaming, codegen | poor browser support, harder to debug by hand | internal service-to-service, high throughput, streaming |
| Events (async) | decoupling, buffering, fan-out | eventual consistency, consumer idempotency, ordering limits | work with no immediate response, multiple consumers |

Don't mix styles on one surface without a reason you can state in one sentence.

## Pick one convention set

The two strict rule sets this reference draws on disagree on surface details. Both are internally coherent; mixing them is what produces an API nobody can predict. Choose one bundle, apply it everywhere, and match the existing codebase when there is one.

| | Zalando-style | Azure-style |
|---|---|---|
| Path segments | `kebab-case` | `camelCase` |
| Query parameters | `snake_case` | `camelCase`, OData `$top`/`$skip` |
| JSON properties | `snake_case` | `camelCase` |
| Versioning | major in path (`/v1/…`) | required `api-version` query parameter, `YYYY-MM-DD` |
| Idempotent `POST` | `Idempotency-Key` | `Repeatability-Request-ID` + `Repeatability-First-Sent` |
| Async operation | operation resource returned in the body | `Operation-Location` header |
| Errors | problem+json (RFC 9457) | `{ "error": { "code", "message", "target", "details", "innererror" } }` |

Everything below states both where they differ, and marks the Azure-only items. A new internal API on a kebab/snake codebase should take the left column; a new API on a camelCase codebase, or one that has to sit beside a cloud provider's SDKs, should take the right.

## Resources and URLs

Model the domain, not the database and not the UI screen.

- **Nouns for resources, plural for collections**: `/sales-orders`, `/invoices`, `/invoice-lines`. Domain-specific beats generic (`sales-order-items` over `items`).
- **No verbs in paths.** The method is the verb. Turn actions into resources instead of endpoints: `PUT /article-locks/{article-id}` rather than `POST /articles/{id}/lock`.
- **kebab-case path segments**, lowercase ASCII, pattern `^[a-z][a-z\-0-9]*$`. **snake_case query parameters**, never camelCase.
- **Path parameters**: `{invoice-id}`, kebab-case in the template, opaque in value. Keep identifiers URL-safe (`[A-Za-z0-9:._\-]`), never empty.
- **Normalized paths**: no trailing slash, no duplicate slash. `/invoices/42` and `/invoices/42/` are one resource; accept the canonical form and reject or normalize the rest explicitly.
- **Nesting ≤ 3 levels.** Nest a sub-resource only when it cannot exist without the parent; otherwise expose it top-level with its own id.
- **Keep the API small.** 4–8 resource types per API is the healthy range; more means split by subdomain.
- **No `/api` prefix.** The base path is deployment config, not API design.
- **Singleton sub-resources** (`/customers/{id}/preferences`) are collections of cardinality 1 — model them as an object and state the cardinality, don't invent an id.
- **`self`** as a pseudo-identifier when the identity comes from the token: `/employees/self`, `/employees/self/personal-details`.

## Methods

| Method | Safe | Idempotent | Body | Meaning |
|---|---|---|---|---|
| `GET` | yes | yes | no | read; never mutates |
| `POST` | no | no (make it so when retryable) | yes | create or non-idempotent action |
| `PUT` | no | yes | yes | full replace / upsert at a known URL |
| `PATCH` | no | no by default | yes | partial update (JSON Merge Patch or an explicit patch format) |
| `DELETE` | no | yes | rarely | remove; second call is `204`/`404`, not an error |

`GET` must never mutate — browsers, CDNs, proxies, and prefetchers will replay it. Anything with a side effect that must not be replayed belongs behind `POST` with an idempotency key.

## Status codes

| Code | Use |
|---|---|
| `200` | success with a body |
| `201` | created, with `Location` of the new resource |
| `202` | accepted, work continues asynchronously (see long-running operations) |
| `204` | success, no body (typical for `DELETE`, `PUT` with nothing to return) |
| `304` | not modified (conditional `GET`) |
| `400` | malformed request, unparseable body, invalid parameter format |
| `401` | missing or invalid credentials |
| `403` | authenticated but not permitted |
| `404` | resource does not exist (or is hidden from this caller — prefer `404` over leaking `403` for others' resources) |
| `405` | method not allowed on this resource; include `Allow` |
| `409` | conflict with current state (duplicate, version mismatch, illegal transition) |
| `412` | precondition failed (`If-Match` version mismatch) |
| `415` | unsupported media type |
| `422` | syntactically valid, semantically invalid (business rule) |
| `429` | rate limited, with `Retry-After` |
| `500` | unhandled server fault |
| `502`/`504` | upstream failure / upstream timeout |
| `503` | temporarily unavailable, with `Retry-After` |

Rule of thumb: `4xx` means the client must change the request; `5xx` means retrying the same request may work. Getting this backwards breaks every client's retry policy.

## Versioning

- **Pick one mechanism and keep it.** Major version in the path (`/v1/…`) is the default because it is visible, routable, and cacheable. **Azure-style:** a required query parameter (`api-version=2026-10-01`, date-based) is a valid alternative, particularly in cloud APIs where many resource providers share a hostname; a required header is acceptable internally. Do not support two mechanisms, and do not let one surface mix them.
- **Version on breaking changes only.** These are non-breaking: adding an optional request field, adding a response field, adding a new endpoint, adding an enum value the client must tolerate, adding an optional header. These are breaking: removing or renaming a field, changing a type or format, changing the meaning of an existing value, tightening validation, changing default behaviour, changing a status code, changing pagination or auth semantics.
- **Clients must tolerate unknown fields** and unknown enum values; state that in the contract so servability is not a per-client negotiation.
- **One version per route module.** Branch in a shared layer if you must, never inside a handler with `if version == 2` scattered through it.
- **Overlap window** quantified in the policy (e.g. previous major supported ≥ 6 months after the new one ships, ≥ 12 months for public APIs with SDKs).

## Deprecation

Ship deprecation as machine-readable signal, not a changelog entry:

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Link: </v2/invoices>; rel="successor-version"
```

`Sunset` follows RFC 8594. Also: emit a `Warning` or custom header naming the replacement, count callers on the deprecated path (telemetry is how you know the window is real), and never sunset a route with active traffic and no migration path.

## Pagination

- **Every collection is paginated**, and every list operation has a server-enforced maximum page size. A collection endpoint without a limit is a denial-of-service you wrote yourself.
- **Cursor pagination is the default** — stable under concurrent writes and cheap on large or sharded data. Offset pagination is acceptable for small, static, and human-paged datasets, and for "jump to page 50".
- **The cursor is opaque.** Clients never construct or inspect it. It encodes position (last seen sort key + id) and, ideally, a hash of the applied filters.
- **Stable total ordering** is required — sort by `(created_at, id)`, never by a non-unique column alone, or rows repeat and vanish between pages.
- Page object shape:

```json
{
  "items": [ { "id": "inv_123" } ],
  "self": "/v1/invoices?cursor=eyJpZCI6MTIzfQ&limit=50",
  "next": "/v1/invoices?cursor=eyJpZCI6MTczfQ&limit=50",
  "prev": null,
  "query": { "status": "open" }
}
```

- **Avoid total counts** in pagination responses: `COUNT(*)` over a filtered set is a full scan that gets more expensive as the data grows, and once a client depends on it you cannot remove it. Offer it behind an opt-in (`Prefer: return=total-count`) if someone genuinely needs it.
- **Conventional query parameters** — `q` (search), `sort` (comma-separated, `-` for descending), `fields` (sparse fieldsets), `embed` (expand references), `limit`, `cursor`, `offset`. Deviating per endpoint makes every client a special case.

## Errors

One shape, everywhere. Pick either RFC 9457 (`application/problem+json`) or the cloud-provider style, but never both:

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Request validation failed",
  "status": 422,
  "code": "VALIDATION_ERROR",
  "detail": "3 fields failed validation",
  "instance": "/v1/invoices",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "errors": [
    { "field": "customer_id", "code": "required", "message": "customer_id is required" },
    { "field": "due_date", "code": "format", "message": "must be an RFC 3339 date" }
  ]
}
```

Required properties of any error contract: a **stable machine-readable code** the client can branch on (never branch on the message text), a **human message**, **field-level detail** for validation, a **correlation id**, and the HTTP status mirrored in the body. Errors are `4xx`/`5xx`; a `200` with `{"success": false}` breaks every proxy, monitor, and SDK in the chain. Never include stack traces, SQL, internal hostnames, or upstream error bodies verbatim.

## Idempotency

Any mutating operation a client may retry needs a dedupe mechanism:

- **Client-supplied key**, one header chosen per API: `Idempotency-Key: <uuid>` (widely used) or `Repeatability-Request-ID` + `Repeatability-First-Sent` (Azure convention for `POST`). Scope the key to the authenticated principal and the operation.
- **Store the outcome, not just the lock**: key → status code + response body, retained ~24 h (longer than any retry window, shorter than your storage budget).
- **Same key, different body** → `422`; do not silently replay a different request.
- **Concurrent duplicate** → return `409` (or hold and replay once complete) rather than executing twice.
- **Natural idempotency is better when available**: a client-generated id used as the primary key, or a unique constraint on the business key.

`POST` that creates at a client-chosen URL is `PUT` and is idempotent by definition — prefer that when the client can name the resource.

## Long-running operations

When work outlasts an HTTP request:

1. Respond `202 Accepted` with the operation URL — Azure-style in the `Operation-Location` header, elsewhere in the body (`{ "operationId": "op_123" }`) plus a `Location` header.
2. Return an operation resource with a status enum (`notStarted`/`running`/`succeeded`/`failed`/`canceled`), timestamps, and the result or error when terminal.
3. Tell the client how to poll: `Retry-After` on the operation response.
4. Support `DELETE`/cancel on the operation resource when the work is cancellable.
5. Expire terminal operations after a documented retention window.

Never hold a request open for minutes and hope the client wait loop is patient — proxies time out first, and the client retries a job that is already running.

## Conditional requests and concurrency

- `GET` returns `ETag`; the client sends `If-None-Match` to get `304` and skip the body. Cheap bandwidth wins on polling clients.
- Optimistic concurrency control: `PUT`/`PATCH` with `If-Match: "etag"`, mismatch → `412`. This is the correct answer to lost updates; last-write-wins without a version check silently discards a user's edit.
- `If-Modified-Since`/`Last-Modified` where a clock is good enough; prefer `ETag` where it is not.

## Caching headers

| Header | Set it to |
|---|---|
| `Cache-Control` | `no-store` for per-user and secrets; `private, max-age=N` for user data; `public, max-age=N, s-maxage=M, stale-while-revalidate=K` for shared |
| `Vary` | exactly the request headers that change the response (`Accept-Encoding`, `Authorization` if it does) |
| `ETag` | on anything pollable or re-fetched |
| `Age` | surfaced by caches; useful when debugging stale reads |

Only `GET`/`HEAD` are cacheable. If the answer depends on the token, it is `private` — a shared cache that ignores this leaks one user's data to another.

## Security

- **Authn**: OAuth 2.0 / OIDC bearer tokens over TLS. No basic auth, no credentials in query strings (they land in logs and history).
- **Authz**: deny by default; every operation declares its required scope, and **every object access re-checks ownership** — broken object-level authorization is the most common API vulnerability by a wide margin. A valid token is not permission for this record.
- **Scopes** named by resource and action (`invoices.read`, `invoices.write`), assigned per client, not per user role guesswork.
- **Input validation**: schema-based allowlist validation of body, path, and query; reject unknown fields on write; bound array lengths and page sizes; validate content type and reject the unexpected with `415`.
- **Output**: never echo secrets; no internal ids, stack traces, or version banners in errors; `X-Content-Type-Options: nosniff`.
- **Transport and CORS**: TLS only, HSTS, explicit origin allowlist, no `*` with credentials.
- **Abuse**: rate limit per identity and per tenant, body size limits, query complexity limits (GraphQL depth/complexity), and a documented `429` contract with `Retry-After`.

## Contract and tooling

- **OpenAPI 3.1 is the contract** (or `.proto` for gRPC). Every operation has request, response, error, auth, and examples. Generate it from code or generate code from it — one direction, never hand-maintained in parallel.
- **Validate in CI**: schema lint, breaking-change detection against the last released spec (`oasdiff`, `buf breaking`), and response-shape tests against the spec.
- **Trace context**: propagate W3C `traceparent` and echo a request id (`x-request-id`) so a client error report maps to a server log line.
- **gRPC specifics**: field numbers are forever — never reuse or renumber; reserve removed tags; set deadlines on every call; keep `proto` in a versioned package.
- **GraphQL specifics**: persisted queries in production, depth and complexity limits, cursor-based connections, and a dataloader per relation to avoid N+1.

## Naming and formats inside payloads

- JSON properties in the bundle's casing — `snake_case` (Zalando) or `camelCase` (Azure). Never both in one payload; identifiers as opaque strings; never encode meaning in an id.
- Timestamps as RFC 3339 / ISO 8601 with UTC offset, always. Durations in a documented unit, and put the unit in the field name (`timeout_seconds`).
- Money: integer minor units plus an ISO 4217 currency code, or a decimal string. Never a float.
- Booleans: `is_`/`has_` prefix, always present rather than nullable.
- Distinguish absent from `null` deliberately, and document what `null` means where you allow it.
- Enums are open for read (clients tolerate unknown values), closed for write (validate on input).
