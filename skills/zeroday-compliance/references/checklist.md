# The Gate Checklist

Work top to bottom. Tag legend: **[B]** block the deploy · **[H]** ship only with a written waiver (owner + fix-by) · **[A]** advice for the first month.

Mark the verdict, date, and evidence link for every row. An untagged row you skipped is an unassessed row, not a pass.

## If you only do five

These are what actually took down real vibe-coded apps, in order:

1. Database or storage reachable without access control (Supabase with RLS off, or a policy of `USING (true)`).
2. API routes with no auth check.
3. A committed or web-served secret (`.env` in the repo, or served from the web root).
4. Object access with no ownership check — change the id in the URL, get someone else's record.
5. Secret keys or source maps shipped in the frontend bundle.

## 1. Know your data

| Tag | Item | How to verify |
|---|---|---|
| B | Every personal-data field listed: name, email, phone, IC/passport, address, location, IP, device id, payment info | Inventory table, one row per field |
| B | Sensitive fields marked — IC/passport, health, financial, biometrics, children's data | Column in the same table |
| B | Each field mapped: stored where, processed where, logged where, sent to whom | Column per field; "nowhere" is a valid entry |
| B | Sub-processor list: every third-party that touches user data (database host, email, analytics, payments, AI model) | Named in the privacy notice and in one internal list |
| H | Data you do not need is removed | Deletion, not "we'll ignore it" |
| B | Retention period per data type, and a mechanism that actually deletes at the end | A job, a policy, or a documented manual runbook |

Data you never collected cannot leak. The cheapest privacy control is a smaller inventory.

## 2. Legal and policy

| Tag | Item | How to verify |
|---|---|---|
| B | Privacy notice: what is collected, why, who it is shared with, how long it is kept, how to contact you | Linked from every page, the signup form, and each data-collection point |
| B | Notice in **both Malay and English** if Malaysian PDPA applies | Two versions published |
| B | A lawful basis per processing purpose — consent, contract, legal obligation, or legitimate interest | Written per purpose; bundled consent for several purposes is invalid |
| B | Consent is unchecked by default, per purpose, recorded with timestamp and notice version, and as easy to withdraw as to give | Consent table row per user; a one-click withdrawal path |
| B | Terms of service; cookie notice with real opt-in for non-essential cookies where EU/UK users exist, and rejecting must actually block the scripts | DevTools → Application → Cookies; reject, reload, confirm no analytics call |
| B | A user-request process: access, correction, deletion, portability | Runbook with owner, timeline (GDPR: one month), and a tested delete path |
| B | Breach response plan: who decides, whom to notify, how fast (Malaysian PDPA 2024 amendments; GDPR 72 hours) | One page, named people, contact details |
| B | Vendor agreements in place for anyone processing data on your behalf | Signed DPA or the vendor's standard terms on file |
| H | Cross-border transfer check if data leaves Malaysia (or the EU) | Storage region of every vendor written down |
| H | DPO appointed if the size and data types require it | Named, with contact route |
| H | EU representative (Article 27) if you serve EU users with no EU establishment | Named |
| B | **EU AI Act Article 50 disclosure** if any feature uses a chatbot, generates content, or makes visible automated decisions | Disclosure at the point of use, not buried in terms; applies from 2 Aug 2026, fines up to €15M or 3% of turnover |
| A | DPIA if profiling, special-category data, or large-scale monitoring | Written assessment |

## 3. PII protection in the system

| Tag | Item | How to verify |
|---|---|---|
| B | Encryption in transit everywhere, HSTS on | `curl -I https://…`; SSL Labs grade |
| B | Encryption at rest for database, backups, and file storage | Provider settings, checked not assumed |
| H | Extra protection for the most sensitive fields — field-level encryption, tokenization, or masking for IC/passport and payment identifiers | Schema or code reference |
| B | **No PII in logs, error messages, analytics events, URLs, or query strings** | `grep` patterns in [data-and-pii.md](data-and-pii.md); check the actual log output and the error handler |
| B | No real customer data in dev, test, staging, or demos | Seeded fake data; masking tool when a real sample is needed |
| B | Card data handled entirely by a PCI-compliant provider (Stripe, Billplz, iPay88); never stored, never proxied through your server | No card fields in your schema; hosted fields or redirect flow |
| B | Row-level security (or equivalent) on every table reachable from a client SDK | RLS enabled, owner-scoped policy per table, `USING (true)` counts as off; test signed-out and as two different users |
| H | Analytics choice documented; tracking scripts you did not add are removed | Script inventory |

## 4. Access control

| Tag | Item | How to verify |
|---|---|---|
| B | Every route and server action checks the caller on the server; intentionally public routes are listed explicitly | Route-by-route walkthrough |
| B | Object-level authorization: any fetch-by-id verifies the record belongs to the caller or their tenant | Adversarial test with two accounts |
| B | Admin routes and admin APIs restricted server-side, not by hiding the UI | Direct request as a regular user must be denied |
| B | Multi-tenant boundary enforced in the query, using a tenant id from verified server context — never a client-supplied tenant | Query inspection, not UI testing |
| B | Password hashing with bcrypt, argon2, or scrypt at OWASP-recommended parameters; never MD5/SHA1/plaintext | Code reference |
| B | Sessions expire; JWT signing secret is 32+ random characters from an env var, never `"secret"` | Token TTL and secret length |
| B | Password reset tokens expire (30–60 min) and are single-use | Replay a used link |
| B | Email verification actually blocks sensitive features | Register, do not verify, try to act |
| B | OAuth `state` generated server-side, stored in session, validated on callback | Callback code path |
| B | Login and reset endpoints rate-limited on both account and source signals, using a shared store if there is more than one instance | Attempt script |
| B | Least privilege for staff and service accounts; production access limited to those who need it; separate production credentials; no shared admin logins | Role matrix + access list |
| B | MFA on admin, cloud, GitHub, and database accounts | Enabled and enforced |
| H | Audit log of who accessed or changed sensitive data, retained and protected | Log exists and is queryable |
| H | Offboarding removes access | Written process |

## 5. Secrets and configuration

| Tag | Item | How to verify |
|---|---|---|
| B | No secrets in code **or git history** | `gitleaks` / `trufflehog` over the full history, output attached |
| B | No secrets in the client bundle — `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` prefixed values ship to the browser | Grep the built assets for `sk-`, `pk_`, key patterns |
| B | `.env`, `.env.local`, `.env.production` ignored and not tracked | `git ls-files \| grep env` |
| B | Secrets in a manager or environment variables, distinct per environment, present in all environments | Deploy config review |
| B | Every key that was ever committed, shared, or used in testing is **rotated** | Rotation log with dates |
| B | Debug mode, verbose errors, and test endpoints off in production | `NODE_ENV`, `DEBUG=false`, framework debug page off |
| B | Every dependency actually exists and is the package you meant (hallucinated or slopsquatted packages) | Lockfile review; registry check for the exact names |
| H | Secret rotation schedule; a manager with its own access control | Written |

## 6. Application security

Full category detail, with the failure modes that are specific to AI-generated code, in [appsec.md](appsec.md).

| Tag | Item | How to verify |
|---|---|---|
| B | Server-side input validation (allowlist schema) on body, path, and query | Code path |
| B | Parameterized queries everywhere; no string-built SQL | Grep for interpolation into query strings |
| B | User content escaped on output; no raw `dangerouslySetInnerHTML` / `innerHTML` with user data | Sink review |
| B | CSRF protection on cookie-authenticated state changes | Token or SameSite verification |
| B | File uploads restricted by MIME type and size **server-side** | Upload a `.php`/oversized file |
| B | Security headers: CSP, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`; CORS allows explicit origins, never `*` with credentials | `curl -I`, Mozilla Observatory |
| B | Payment and entitlement checks server-side; a browser-supplied price or plan is ignored | Tamper test |
| B | Webhook signatures verified against the raw body before any state change | Send an unsigned request |
| B | Webhook handlers idempotent — event id stored, duplicates skipped | Send the same event twice |
| B | Error responses return a generic message; stack traces, SQL, and paths stay in server logs | Trigger a 500 |
| H | Rate limiting on public APIs; spend caps on any endpoint that calls a paid model | Configured limits |
| H | SSRF surface closed — outbound fetch restricted to allowlisted hosts, cloud metadata IPs blocked | Code review |
| H | Source maps not served in production | Request a `.map` URL |
| H | Dependency CVE scan clean at high/critical | `npm audit`, `pip-audit`, `Trivy` output |
| H | OWASP ZAP baseline scan against staging with no unfixed high findings | Report attached |
| A | OWASP Top 10 and API Security Top 10 walkthrough | Checklist artefact |
| A | Mobile: no tokens in plaintext storage, cert pinning, debug flags off, deep links validated | Only when a mobile client exists |

## 7. Infrastructure

| Tag | Item | How to verify |
|---|---|---|
| B | Database and storage not publicly accessible — no open bucket, no exposed `5432`/`3306`/`6379`/`27017` | External port scan from outside the network |
| B | `.env`, `.git`, and backup files not served from the web root | `https://app/.env`, `/.git/config`, `/backup.sql` |
| B | Firewall and security groups allow only required ports | Rule review |
| B | Backups running, encrypted, and **restore-tested at least once** with the time recorded | Restore log |
| B | Logs centralised, access-controlled, and free of PII | Sample log dump |
| H | Monitoring and alerts for errors, downtime, and unusual activity, routed to a human | Trigger a test alert |
| H | TLS configuration sane — modern protocols and ciphers, no known-broken settings | SSL Labs B or better |

## 8. Launch readiness

| Tag | Item | How to verify |
|---|---|---|
| B | Rollback plan tested; the previous version can be restored | Deploy the old build once |
| B | Incident contacts: who to call, in what order, and how | One page, current numbers |
| B | Final sign-off from whoever owns security and privacy | Named, dated |
| H | A way to tell users about problems (status page or mailing channel) | Live before launch |
| H | Alert routing and someone watching for the first week | On-call named |
| A | Post-launch review scheduled — the gate rerun after the first real traffic | Date set |
