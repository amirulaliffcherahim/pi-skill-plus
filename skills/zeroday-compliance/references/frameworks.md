# Certification Frameworks

The gate in this skill gets you to a lawful launch. This file is for the question that comes later: a customer sends a security questionnaire, an enterprise deal needs SOC 2, or a payment processor asks about PCI. Day-zero readiness and an actual attestation are different jobs — do not let a launch date imply you have the second.

## Framework routing

| Framework | Applies when | Control catalog | Detail |
|---|---|---|---|
| **SOC 2** | B2B SaaS, customer security questionnaires, enterprise procurement | AICPA Trust Services Criteria CC1–CC9; categories Security / Availability / Processing Integrity / Confidentiality / Privacy | [audit-standards.md](audit-standards.md) |
| **GDPR** | Processing EU/UK residents' personal data | Regulation 2016/679: Articles 3, 6, 28, 30, 32, 33–34, 35; Chapter V | [legal.md](legal.md) |
| **HIPAA** | US protected health information | Administrative / Physical / Technical Safeguards; Breach Notification Rule | [audit-standards.md](audit-standards.md) |
| **PCI DSS** | Storing, processing, or transmitting cardholder data | 12 requirement groups; SAQ type depends on integration method | delegate to the gateway — see [data-and-pii.md](data-and-pii.md) |
| **ISO 27001** | Enterprise procurement outside the US | Annex A control set, ISMS process | [audit-standards.md](audit-standards.md) |

Overlap is the norm. Build **one** control matrix and tag each control with every framework it satisfies; running parallel assessments doubles the work and produces contradictions.

## The five-stage loop

Every framework runs the same loop. Only the control catalog changes.

1. **Scope** — applicability, in-scope systems, entities, audit period.
2. **Map** — control matrix: criterion → control → evidence → owner.
3. **Gap-assess** — mark each control `implemented` / `partial` / `missing`, record the gap.
4. **Collect and test** — evidence that the control *operated*, not that it exists.
5. **Report and remediate** — rank by risk, roadmap, schedule the re-test.

## Evidence discipline

The most common audit failure is claiming a control exists because documentation says so.

- Evidence is **timestamped inside the audit period**.
- Evidence is **machine-generated or a system export** — not a hand-written summary of one.
- A single exception (one PR merged without review) is not automatically a finding; the criterion is whether the control operated consistently enough to be effective. Document exceptions explicitly and let the assessor judge.
- Never fabricate, round, or extrapolate an evidence number. If a metric does not exist, record it as unavailable — that is a gap you can fix, and a fabricated one is a fraud.

The same rule applies at day zero: "we have rate limiting" without a test recording is a claim, not a control.

## Type I versus Type II

| | Type I | Type II |
|---|---|---|
| Question | Is the control designed correctly today? | Did it operate effectively over the period? |
| Period | A single date | 3–12 months |
| Evidence | Design documents, screenshots | Continuous system exports across the period |
| Cost of being late | rework | the period must restart |

Type II readiness typically needs **8–12 weeks** of lead time before the audit period starts. Starting readiness on period day one guarantees a finding, because there is no history to test. This is the practical reason the day-zero gate matters: the logs and alerts you switch on at launch become the evidence you will need a year later.

## Day-zero minimum for each framework

Do this now, so the later attestation is bookkeeping rather than archaeology:

| Framework | Minimum that must exist from day one |
|---|---|
| SOC 2 | Access logs with actor and timestamp, least-privilege roles, change history with approver, incident plan, vendor list |
| GDPR | Article 30-style records: purpose, categories, recipients, retention, security measures, per processing activity |
| HIPAA | Access control to PHI, audit logs, encryption, a signed BAA with every vendor that touches PHI |
| PCI DSS | No card data in your systems; gateway-hosted fields; documented SAQ position |
| ISO 27001 | Asset inventory, risk register, documented policies, management review cadence |

## Reporting an assessment

```text
COMPLIANCE ASSESSMENT - <Framework> - <Organisation>
Assessment date: <date> | Period: <start> to <end> | Assessor: <name>

OVERALL: <compliant | partial | non-compliant>  (<n> open findings)

CRITICAL FINDINGS
1. <criterion> - <gap> - <evidence gap> - <remediation estimate>

CRITERION-BY-CRITERION STATUS
[ok]      <criterion>: <one-line status>
[partial] <criterion>: <what is missing>
[fail]    <criterion>: <what is missing>

REMEDIATION ROADMAP
P1 (0–30d)  : <action>  <cost>
P2 (1–3mo)  : <action>  <cost>
P3 (3–6mo)  : <action>  <cost>
```

Before delivering one:

- Applicability and scope are written down, not assumed.
- Every criterion is addressed, including the ones that pass.
- Each finding cites the specific criterion id (CC6.1, Article 32, PCI 3.4).
- Each finding names the evidence that was missing or deficient.
- Exceptions are separated from systemic gaps.
- Evidence dates fall inside the stated period.
- Remediation items have an owner, an estimate, and a priority.

## Procedures

Step-by-step assessment procedures — scoping, control mapping, evidence collection, readiness, audit support, and the GDPR phase templates (Articles 30, lawful basis, DSR timelines, DPIA, breach decision tree, transfer mechanisms) — are in [audit-procedures.md](audit-procedures.md). Read that only when an assessment is actually underway; it is long and specific to that job.
