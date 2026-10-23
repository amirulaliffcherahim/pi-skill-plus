---
name: zeroday-compliance
description: Day-zero launch gate for compliance, PII, and security - data inventory, PDPA/GDPR/EU AI Act duties, PII masking before inspection, application-security and infrastructure checks, ending in a pass or block verdict. Use before a first production deploy or public launch, when customer records, logs, or exports with personal data must be masked before use, when reviewing an app for security or pentest readiness, or when preparing a SOC 2 / GDPR / PDPA assessment.
---

# Day-Zero Compliance Gate

Runs **once before the first production deploy**, and again whenever a change adds a data category, a third-party vendor, a payment path, or an AI feature.

The failure this gate exists for: the code works, so the launch happens, and the privacy layer was never built. Working code is not lawful code, and a demo that handles real user data is a live obligation.

## Verdict model

Judge every item as one of three, and put the verdict in the report:

| Verdict | Meaning | Examples |
|---|---|---|
| **BLOCK** (P0) | Do not ship. Fix or the launch is cancelled. | committed secret, unguarded object route, PII in logs, no delete path, publicly readable storage, unverified payment webhook, no privacy notice |
| **HOLD** (P1) | Ship only with a written waiver: item, owner, reason, fix-by date. | missing rate limit on a low-traffic endpoint, cookie banner missing for an EU-optional feature, backup restore untested |
| **PASS** | Checked, correct, evidence recorded. | — |

A single BLOCK item fails the gate regardless of how many PASS items surround it. Do not average, do not score out of 100, do not let a launch date reinterpret a P0.

## The eight phases

Work in this order — later phases assume the data inventory from phase 1.

| # | Phase | Produce | Done when |
|---|---|---|---|
| 1 | Know your data | Data inventory table: field → category → where stored/processed/logged/sent → retention | Every field of personal data is listed, marked sensitive or not, and has a retention period |
| 2 | Legal and policy | Privacy notice, lawful basis per purpose, consent record, DSR runbook, breach plan, vendor list | Each processing purpose has a lawful basis and a notice clause; a user request can be fulfilled without a code change |
| 3 | PII in the system | Field-level protection list, log-scrubbing evidence, fake-data policy, payment boundary | No PII in logs/errors/analytics/URLs, no real data outside production, card data never touches your servers |
| 4 | Access control | Role matrix, MFA evidence, prod-access list, audit-log plan | Every route's authorization is checked server-side, and a regular user provably cannot reach another's record |
| 5 | Secrets and config | Clean scan output, rotation log, env-var inventory per environment | Secret scanners are clean on code *and* git history; nothing sensitive is client-bundled; debug off in prod |
| 6 | Application security | Findings list per category with severity, fixes applied | Every category in [appsec.md](references/appsec.md) is either fixed or waived with a reason |
| 7 | Infrastructure | Exposure check, backup + restore log, monitoring/alerts list | No public DB/storage/.env, backup restore has been performed once, alerts reach a human |
| 8 | Launch readiness | Rollback procedure, incident contacts, sign-off | Rollback tested, contacts named, and a named person owns security and privacy sign-off |

Full item-by-item checklist: [checklist.md](references/checklist.md). That file is the working document — read it, tick items, attach evidence.

## Evidence, not assertion

A working screen is not evidence. For each of these, record the request and the response (or a screenshot of the denial), because these are the exact failures that have taken real apps down:

| Test | Expected |
|---|---|
| Account B requests account A's record by id | `403`/`404`, no fields from A returned |
| Signed-out browser hits a protected API route | `401`, no private data in the body |
| Regular user calls an admin route directly | Denied server-side, not hidden in the UI |
| Webhook arrives without a valid signature | Rejected before any order or entitlement changes |
| The same verified payment event arrives twice | One fulfilment, no duplicate order |
| Browser request changes a price or discount | Server uses its own validated pricing |
| User exceeds the login or AI-request limit | Limited, with no bypass by changing an identifier |
| `GET /users/<other-id>` with a token from another tenant | Denied at the query, not after fetching |

Use a staging environment, two accounts you control, and the payment provider's test mode. Production smoke tests are allowed only for reads you would be comfortable seeing logged.

## Rules that override the rest

1. **No real customer data outside production.** Dev, test, staging, and demos use generated or masked data. A copy of production data in a dev database is a breach waiting for a misconfigured port.
2. **Mask before reading.** When inspecting records, exports, or query output that may hold personal data, run it through `scripts/llm_privacy.py mask` first and restore only in the file you hand back. See [pii-masking.md](references/pii-masking.md).
3. **A secret that ever touched git is rotated, not deleted.** Removing it from the working tree leaves it in history, in forks, in CI logs, and in the bundle you shipped.
4. **Deletion must actually delete.** A hidden row, a soft-delete flag, or a removed UI element is not erasure; the record and its copies in analytics, email lists, and backups need a defined path.
5. **Waivers are written**, with item, owner, reason, and an expiry date. An undocumented "we'll fix it after launch" is a finding.
6. **This is not legal advice.** Anything involving IC/passport numbers, health, financial, biometric, or children's data needs a review by someone qualified in the applicable regime — Malaysian PDPA and/or GDPR.

## Output

```text
LAUNCH READINESS - <app> - <environment> - <date>
Assessor: <name> | Commit: <sha> | Data categories in scope: <list>

VERDICT: BLOCK | HOLD(n) | PASS

BLOCKERS (P0)
1. <item> - <evidence or its absence> - <fix>

HOLDS (P1, waived)
1. <item> - owner - fix-by <date> - <reason>

PHASE STATUS
[pass]    Data inventory: <n> fields, <n> sensitive, retention defined
[block]   Access control: 3 of 41 routes lack an ownership check
...

FIX ORDER
P0 (before deploy) : <action>
P1 (before launch) : <action>
P2 (first month)   : <action>

SIGN-OFF
Security: <name> | Privacy: <name> | Date: <date>
```

## References

| File | Read it when |
|---|---|
| [checklist.md](references/checklist.md) | always — the item-by-item gate, tagged BLOCK / HOLD / ADVICE |
| [scan-patterns.md](references/scan-patterns.md) | phases 5 and 6 — breadth greps and per-language scan commands |
| [remediation.md](references/remediation.md) | after a finding — fix protocols, not just the fix |
| [mobile.md](references/mobile.md) | only when a mobile client ships with the app |
| [data-and-pii.md](references/data-and-pii.md) | phase 1 and 3 — inventory template, sensitive categories, retention, log leakage, payments |
| [legal.md](references/legal.md) | phase 2 — Malaysian PDPA, GDPR, cookie rules, breach notification, EU AI Act disclosure |
| [appsec.md](references/appsec.md) | phase 6 — the vulnerability categories ranked by what actually breaks vibe-coded apps |
| [infra.md](references/infra.md) | phases 5 and 7 — secrets, exposure, backups, monitoring, rollback |
| [tooling.md](references/tooling.md) | phase 5, 6, 7 — exact commands for the scanners, and what each one misses |
| [pii-masking.md](references/pii-masking.md) + `scripts/llm_privacy.py` | any time real personal data must be inspected |
| [pii-locales.md](references/pii-locales.md) | masking national IDs and phone formats for a specific country |
| [frameworks.md](references/frameworks.md) | when a customer, investor, or auditor asks about SOC 2 / ISO / HIPAA / PCI |
| [audit-standards.md](references/audit-standards.md), [audit-procedures.md](references/audit-procedures.md) | only during real audit preparation — control catalogs and step-by-step procedures |
| [sources.md](references/sources.md) | provenance and licensing |
