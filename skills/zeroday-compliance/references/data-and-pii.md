# Data and PII

## Inventory template

One row per field. This table is the artefact phase 1 produces; everything legal refers back to it.

| Field | Category | Sensitive | Where stored | Where logged | Sent to | Retention | Protection |
|---|---|---|---|---|---|---|---|
| `users.email` | identifier | no | primary DB `users` | no | Resend (email) | account life + 30d | at-rest encryption |
| `users.ic_number` | national id | **yes** | `users` (encrypted column) | no | — | 7 years after end of relationship | field-level encryption + masking |
| `orders.card_last4` | financial | **yes** | `orders` | no | Stripe | 7 years | tokenized, provided by gateway |

Categories worth naming explicitly: identity (name, IC/passport, DOB), contact (email, phone, address), digital identifiers (IP, device id, cookie id, user agent), financial (card, bank, transaction), health, biometrics, location, children's data, employment, and free-text that may contain any of the above.

**Children's data** — if the product can be used by under-18s, age assurance and parental consent become a requirement, not a nicety. This is the one category where a legal review is not optional.

## Sensitive categories and what to do

| Category | Extra measure |
|---|---|
| National id (IC/passport), financial account | field-level encryption or tokenization; mask in every UI, export, and log; restrict who can read plaintext |
| Payment card | never stored by you; hosted fields or redirect to a PCI-compliant provider |
| Health, biometric | encryption at rest plus access audit log; DPIA; legal review |
| Children's data | age gate, parental consent, DPIA, legal review |
| Location, device id | purpose limitation — collect only what a named feature uses |

## Retention

For each data type, answer three questions in writing: **how long**, **why that long**, and **what deletes it**.

- Retention needs a trigger: account close + N days, order date + statutory period (Malaysia: 7 years for tax records), consent withdrawal.
- The delete must cascade: database rows, files, search index, analytics events, email/marketing list, third-party processors notified, caches invalidated, and a decision recorded about backups (kept until rotation, not restored into production).
- A retention job that logs failures and never alerts is the same as no job. Alert on it.
- Deletion request handling: verify the requester, delete, record what was deleted and when, and notify processors where required. GDPR allows one month; answer every request even if you must extend.

## No PII in logs, errors, analytics, or URLs

This is the most common leak, and the cheapest to fix.

Search the codebase for the sinks, not the data:

```bash
# logging whole request/response objects (the usual culprit)
grep -rnE "(console\.(log|info|debug|error)|logger\.(info|debug|warn|error)|print\(|fmt\.Print|log\.(Info|Error))\(.*(req\.|request\.|ctx\.|body|payload|user|session|customer)" --include=*.{js,ts,py,go,java,dart,cs,php} .

# logging fields by name
grep -rniE "(log|print|debug|capture|track|identify)[^\n]{0,80}(email|phone|ic_?no|passport|address|password|token|ssn|nric)" --include=*.{js,ts,py,go,java,dart,cs,php} .

# PII in URLs / query strings
grep -rnE "\?[^\"' ]*(email|phone|token|password)=" --include=*.{js,ts,py,go,java,dart,cs,php} .
```

Then fix the sink, not the instance: a logger that redacts known fields on serialisation prevents the next developer from reintroducing the leak.

Also check:

- **Error reporting** (Sentry and friends): `sendDefaultPii` off, request bodies scrubbed, cookies and auth headers stripped before the event leaves the process.
- **Analytics** `identify`/`track` calls: use an internal id, not email, phone, or name.
- **Access logs and proxies**: query strings and paths land in CDN, WAF, and load-balancer logs you do not control. Length and identifier in the path is fine; PII in the query string is not.
- **Frontend bundle and support tools**: an error message shown to the user must be generic; details go to the server log with a correlation id.

## Data outside production

No real customer data in dev, test, staging, demos, or screenshots.

- Seed with generated data. Faker-style generators for names, emails, phones, addresses, and ids — with a fixed seed so tests are reproducible.
- When a real sample is unavoidable (a production bug that only reproduces on real data), mask it before it enters your context or a lower environment:

```bash
PY="${PY:-python3}"   # Windows: set PY to the path `where python` prints

# mask, then read the masked output
PYTHONUTF8=1 "$PY" scripts/llm_privacy.py mask < export.json > export.masked.json

# restore only into the file you hand back, never read it back
PYTHONUTF8=1 "$PY" scripts/llm_privacy.py restore < answer.md > answer.final.md
```

Full mechanics, vault handling, and locale-specific ids: [pii-masking.md](pii-masking.md). National id and phone formats per country: [pii-locales.md](pii-locales.md).

- Add the masked/real file patterns to `.gitignore` so a masked or restored dump never gets committed.
- Production data copied to staging is a breach waiting for a misconfigured port. If a business insists, the copy needs the same encryption, the same access control, and a deletion date.

## Payments

- Card data never touches your servers: hosted fields (Stripe Elements), or a redirect flow. If you find a card number column in your schema, delete it and re-plan the flow.
- Malaysian providers (Billplz, iPay88, toyyibPay, Stripe MY) each have their own redirect and callback verification; verify the signature or the callback secret before granting anything.
- Store the minimum: gateway customer id, last4, brand, expiry month/year, and the transaction reference. Never CVV, never full PAN.
- Entitlement is server-side state. A client telling you the user is on the pro plan is a client telling you what to do with your money.
- FPX/bank-transfer flows need a reconciliation job — callbacks get lost, and the user's bank statement is not your source of truth unless you reconcile.

## Cookies and trackers

- Enumerate every cookie and storage key actually set: DevTools → Application → Cookies and Local Storage, plus a network pass on first load.
- Classify: strictly necessary (session, CSRF) versus analytics/advertising. Necessary ones may be set without consent; the others may not, where EU/UK users exist.
- Rejecting must prevent the scripts from loading, not merely hide the banner. Test by rejecting, reloading, and watching the network tab.
- AI-generated apps often ship a tracking script nobody chose. If you cannot name the owner of a cookie, remove it.
