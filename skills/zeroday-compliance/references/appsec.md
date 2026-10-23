# Application Security

Ordered by what actually takes vibe-coded apps down, not by theoretical severity. Items 1–5 account for most documented incidents: none of them needed a sophisticated attacker.

| # | Category | Severity | Why it lands here |
|---|---|---|---|
| 1 | Database/storage reachable without access control (RLS off, `USING (true)`, open bucket) | critical | one signed-in stranger reads every row |
| 2 | API routes with no auth check | critical | the route exists, nothing verifies the caller |
| 3 | Committed or web-served secrets | critical | full account takeover with no exploit |
| 4 | Broken object-level authorization (IDOR/BOLA) | critical | change the id in the URL |
| 5 | Secrets or source maps in the frontend bundle | critical | the key is published |
| 6 | Unverified payment webhooks, non-idempotent fulfilment | high | free subscriptions, duplicate orders |
| 7 | SQL injection | high | parameterisation missing |
| 8 | XSS via raw HTML sinks | high | user content rendered unescaped |
| 9 | SSRF | high | server fetches an attacker-chosen URL |
| 10 | Wildcard CORS with credentials | high | any site can call the API as the user |
| 11 | Hallucinated or slopsquatted dependencies | high | you installed an attacker's package |
| 12 | Weak password hashing / weak JWT secret | medium–high | offline crack or token forgery |
| 13 | No rate limiting on login, reset, or paid model calls | medium | brute force and bill shock |
| 14 | Insecure file uploads | medium | stored XSS, RCE, disk exhaustion |
| 15 | Missing security headers / partial CSP | medium | defence-in-depth gone |
| 16 | Verbose errors, debug endpoints, exposed API docs | low | reconnaissance |
| 17 | Client-side trust (price, plan, role in the browser) | high | see #6 and mass assignment |
| 18 | Insecure deserialisation, path traversal | high | pickle/YAML/native deserialise on untrusted input; a joined path with no containment check |

## 1. Object and tenant authorization

The most common real vulnerability, and the one AI tools write most often: `findById(id)` with no ownership predicate.

```js
// vulnerable — any authenticated user reads any record
const invoice = await db.invoice.findUnique({ where: { id } });

// fixed — scope the query itself
const invoice = await db.invoice.findFirst({
  where: { id, orgId: session.orgId },
});
if (!invoice) return res.status(404).end();
```

Rules:

- Authorize **in the query**, not after the fetch. A fetch-then-check leaks through timing, through error messages, and through the next developer who forgets the check.
- Take the tenant/owner id from verified server context (session, token claim), never from the request body, query, or a client header.
- Return `404` for other users' resources where the existence itself is sensitive; `403` is fine when the resource is acknowledged as shared.
- Grep for the pattern: every `findById`, `findUnique({ where: { id } })`, `get_object_or_404`, `.filter(id=...)`, or raw `WHERE id = ?` must be paired with an owner predicate.
- Supabase/PostgREST: the table is the API. RLS on for every table, a policy per operation, `USING (true)` is equivalent to off. Test signed-out and as two different users; the anon key is public.

## 2. Route coverage

- Enumerate routes, then mark each one `public` or `authenticated` explicitly. A route that is neither is a finding.
- Apply auth middleware at the router level, not per handler, so a new endpoint is protected by default.
- Server actions, cron endpoints, internal admin triggers, and webhook receivers all need explicit handling — they are the ones usually forgotten.
- Test each protected route signed-out. `401`, no data.

## 3. Secrets

- Scan the workspace **and the git history**; a deleted secret is still in history, forks, CI logs, and the bundle you shipped.
- Anything that ever touched a remote is rotated. Deleting the line does not un-leak it.
- Frontend prefixes (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `PUBLIC_`) mean "compiled into the browser bundle". Only publishable keys (gateway publishable key, analytics site id) belong there. Grep the built assets, not the source.
- Server-side env vars must not be readable through a static route, and `.env` must not be in the web root.

## 4. Authentication

| Control | Requirement |
|---|---|
| Password storage | bcrypt (cost ≥ 12), argon2id, or scrypt at OWASP parameters. Never MD5/SHA-1/SHA-256 alone |
| Session | Expiry and idle timeout; `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict` on cookies |
| JWT | HS256 secret ≥ 32 random bytes from env, or asymmetric keys; `exp` and `iss`/`aud` validated; no `alg: none`, no key confusion |
| Refresh | Rotation with reuse detection; revocation path exists |
| Reset tokens | Random, single-use, 30–60 minute expiry, invalidated on password change |
| Email verification | Unverified accounts are actually blocked from sensitive features |
| OAuth | `state` generated server-side, stored in session, validated on callback; PKCE for public clients; redirect URI allowlisted exactly |
| Login throttling | Per account **and** per source, shared store across instances, no permanent lockout that lets others deny access |
| MFA | On for admin, cloud, GitHub, and DB consoles; available to users for high-value actions |

## 5. Input, output, and injection

- **SQL**: parameterized queries or the ORM only. Grep for template literals inside query strings, string concatenation, and `raw()` with interpolation. Identifiers (table/column names) cannot be parameters — allowlist them.
- **NoSQL**: operator injection via `{"$ne": null}` on a body passed straight into a filter. Validate shape and types; reject keys starting with `$`.
- **XSS**: escape on output for the context. `dangerouslySetInnerHTML`, `innerHTML`, `v-html`, `|safe`, and `eval` are sinks — if user content must be rich, sanitize with a maintained library (DOMPurify) and keep a strict CSP.
- **CSRF**: cookie-authenticated state changes need a token or `SameSite` plus origin check. Bearer-token APIs are largely immune; cookie-session ones are not.
- **SSRF**: any server-side fetch of a user-supplied URL. Allowlist hosts and schemes, block link-local and cloud metadata addresses (`169.254.169.254`), and disable redirect following.
- **Path traversal**: normalize and confine any user-influenced path to a base directory.
- **Mass assignment**: never spread a request body into a model (`...req.body`). Allowlist writable fields; `role`, `isAdmin`, `orgId`, `price`, and `balance` are the usual incidents.
- **Validation**: schema-validate body, path, and query server-side with an allowlist. Client validation is UX.

## 6. Payments and entitlements

- Verify webhook signatures against the **raw** body (parsing first breaks the signature): `stripe.webhooks.constructEvent(rawBody, sig, secret)`.
- Store the event id and skip duplicates; fulfilment must be idempotent because retries are normal.
- Grant entitlements from server-verified state only. A price, plan, or discount supplied by the browser is attacker-controlled input.
- Check entitlement server-side on every gated request, not once at page load.
- Handle the lifecycle: failed payment, cancellation at period end, refund, chargeback. "Subscription status" is a server-side state machine, not a boolean in local storage.
- FPX/bank transfer: reconcile against the gateway's records; a lost callback is an unpaid order.

## 7. Rate limiting and cost control

- Login, registration, password reset, OTP send, contact forms, and any endpoint that sends email or SMS.
- Any endpoint that calls a paid model: per-user and per-session token/spend caps, plus a global circuit breaker. An unbounded LLM endpoint is a financial DoS against you.
- Public read APIs: a limit generous enough for real clients and tight enough to stop scraping.
- Distributed limits need a shared store; a per-instance counter multiplies your limit by the instance count. Return `429` with `Retry-After`.

## 8. Frontend and mobile

- Source maps off in production, or restricted; `.map` URLs must not be publicly fetchable.
- No secrets, internal hostnames, admin URLs, or debug flags in the bundle.
- Mobile: tokens in the Keychain/Keystore, not `SharedPreferences`/`localStorage`; certificate pinning for high-value apps; `debuggable=false`; deep links validated with allowlisted hosts; no logging of tokens.
- Client-side route guards are UX. The server check is the control.

## 9. Dependencies and supply chain

- Every package name in the lockfile verified to exist and be the intended one. AI assistants invent plausible names; attackers register them (slopsquatting).
- Lockfile committed; CI installs from it; no `latest` in production.
- CVE scan at high/critical before each release (commands in [tooling.md](tooling.md)).
- Post-install scripts reviewed for anything that fetched and executed code you did not intend.
- Pin the base images, and rebuild rather than patch running containers.

## 10. Errors, headers, and information exposure

- Client gets a generic message plus a correlation id; the stack, SQL, and paths stay in the server log.
- Security headers: `Content-Security-Policy` (start from `default-src 'self'` and widen deliberately), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` or CSP `frame-ancestors`, `Referrer-Policy: strict-origin-when-cross-origin`, `Strict-Transport-Security` once HTTPS is stable.
- CORS: explicit origins, and never reflect the request's `Origin` on an authenticated endpoint. (A literal `*` combined with credentials is rejected by browsers — the real bug is handler code that echoes whatever `Origin` it receives, or allows `null`, which lets any site read the logged-in user's data.)
- Disable framework debug pages, `/actuator`, `/docs`, `/graphql` introspection, and admin scaffolds in production, or put them behind auth.

## AI-specific failure modes

These are not in classic checklists because they are properties of generated code:

- **Over-permissive defaults** — service role keys used where a scoped key belongs; `AllowAll` policies; `GRANT ALL` to the client role.
- **Authz skipped because the UI hides it** — the button is hidden, the endpoint is open.
- **The happy path only** — no ownership predicate because the demo had one user.
- **Plausible-but-wrong vendor API** — a webhook verified the way a blog post did in 2019; a payment intent confirmed client-side.
- **Config drift between environments** — the security header exists in the dev proxy and not in the deployed edge.
- **Copy-pasted snippets with the demo key left in**.
