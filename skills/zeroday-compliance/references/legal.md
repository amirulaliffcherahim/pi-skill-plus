# Legal and Policy

Not legal advice. This file exists so the engineering work matches what the notice promises, and so the questions sent to a lawyer are the right ones. Legal facts below were checked on 2026-10-22 against primary sources (Act A1727, the Commissioner's DBN and DPO guidelines, the AI Act service desk) — they change; re-check before relying on them.

## Which regime applies

| Regime | Applies when | Core obligation for a small app |
|---|---|---|
| **Malaysia PDPA** (Act 709, as amended 2024) | Processing personal data in a commercial context in Malaysia | Notice in Malay **and** English, one lawful basis per purpose, security, retention limit, access and correction |
| **GDPR** (EU 2016/679) | You offer goods/services to people in the EU/UK, or monitor their behaviour — regardless of where you are | Lawful basis, full rights set, records, 72-hour breach notification, transfer safeguards |
| **EU AI Act** (2024/1689), Article 50 | Any AI feature a user interacts with or sees output from | Tell the user AI is involved, at the point of use; applies from 2 August 2026 |
| **PDPA (Singapore), LGPD (Brazil), DPDP (India), APP (Australia), US state laws** | Serving those users | Broadly GDPR-shaped; check retention, notice, and breach duties per regime |
| **PCI DSS** | You touch card data | Do not touch card data — delegate to a compliant gateway |

When two apply, satisfy the stricter one and tag each measure with the regimes it covers. Do not run parallel programmes.

## Malaysian PDPA in practice

The seven principles are the structure: General, Notice and Choice, Disclosure, Security, Retention, Data Integrity, Access.

What that means for the code:

- **Notice** — a written notice at or before collection, in **both Malay and English**, stating the data collected, purposes, whether provision is obligatory, third parties it is disclosed to, your contact route, and the access/correction route. Put it at the point of collection (signup form), not only in the footer.
- **Choice** — consent for direct marketing must be explicit and withdrawable. Withdrawal must be as easy as giving it, and must stop the processing, not just hide the checkbox.
- **Disclosure** — no use or disclosure beyond the stated purpose. Adding a new purpose later means a new notice, not a silent update.
- **Security** — practical steps against unauthorised access, use, disclosure, alteration, or loss. That is the technical gate in this skill.
- **Retention** — keep only as long as needed for the purpose, then destroy. There is no general "keep it in case" allowance, and no statutory erasure right, so retention design is how you honour deletion expectations.
- **Data integrity** — take reasonable steps so data is accurate and current.
- **Access and correction** — a route for a data subject to see their data and correct it. Under the 2024 amendments a portability right also applies.

The **2024 amendments (Act A1727)** — Royal Assent 9 October 2024, gazetted 17 October 2024 — commenced in stages on **1 January, 1 April, and 1 June 2025**. They are what make a day-zero gate necessary:

| Provision | Obligation |
|---|---|
| **s.12A** | **Data protection officer** — required of data controllers *and* of data processors, accountable for compliance with the Act |
| **s.12B** | **Breach notification** — notify the Commissioner **and** the affected data subjects where a breach causes or is likely to cause **significant harm**. The Commissioner's guideline sets **72 hours** to notify, counted from when the controller is informed of, or detects, the incident |
| **s.43A** | **Data portability** — on request, transmit personal data to another controller, subject to technical feasibility and format compatibility |
| **s.129** | **Cross-border transfer** — moved from a whitelist to an assessment of adequate protection |

"Significant harm" in the guideline covers risk of physical harm, financial loss, damage to credit records, loss or damage to property, misuse of the data for illegal purposes, and compromise of sensitive personal data. Notification to the Commissioner and to the affected individuals are separate duties under the same test.

Two things people get wrong. **The notice must be bilingual** (Malay and English). And **PDPA has no GDPR-style right to erasure** — the rights are access and correction, plus portability since s.43A, with deletion enforced through the retention principle. A delete feature is still the right product behaviour; the legal framing is retention limitation plus correction, not a right to be forgotten.

## GDPR in practice

- **Applicability (Article 3)** — established in the EU, or targeting/monitoring EU data subjects. One EU signup with an EU-facing price list or language is usually enough to be in scope. Decide this first; everything else follows.
- **Lawful basis (Article 6)** per purpose: consent, contract, legal obligation, vital interest, public task, legitimate interest. Bundled consent for several purposes is invalid. Legitimate interest needs the documented three-part test: purpose, necessity, balancing.
- **Special categories (Article 9)** — health, biometrics, ethnicity, religion, sexual orientation, trade-union membership — need an Article 9 condition on top of a basis.
- **Rights** — access (15), rectification (16), erasure (17), restriction (18), portability (20), objection (21). Default deadline one month, extendable by two with notice. Automated decision-making (22) needs its own analysis.
- **Records of processing (Article 30)** — the backbone of every audit. Missing retention periods is the single most common gap.
- **Transfers (Chapter V)** — SCCs (2021 modules) plus a transfer impact assessment, an adequacy decision, or the EU-US Data Privacy Framework. A US-hosted database without one of these is a blocker, not a warning.
- **Breach (Articles 33–34)** — notify the supervisory authority within **72 hours** of becoming aware unless unlikely to result in risk; notify individuals when risk is high. "Becoming aware" is when your monitoring should have told you — an undetected breach does not stop the clock in the regulator's view.
- **DPIA (Article 35)** — mandatory for profiling with significant effects, special-category or large-scale monitoring.
- **EU representative (Article 27)** — required if you are outside the EU, in scope, and not established there.
- **Cookies** — ePrivacy consent for non-essential cookies: opt-in, granular, reject as easy as accept, no pre-ticked boxes, no consent walls for non-essential purposes.

## EU AI Act Article 50 disclosure

If any feature chats, generates content, or makes an automated choice a user sees:

- Say an AI is involved **where the user meets it** — the chat widget, the generated output, the automated decision. A clause in the terms is not the disclosure.
- Mark AI-generated content in a machine-readable way where the regulation requires it (synthetic media, deepfakes).
- Keep a one-page internal note: what the AI does, what data feeds it, and where a human reviews its output, if anywhere.
- Track this as its own obligation line, separate from GDPR consent — the duties and the fines differ.

Status as of 2026-10-22: Article 50 applies, and Commission enforcement begins, on **2 August 2026**. Breaching the transparency obligations falls under Article 99(4) — up to **€15M or 3% of worldwide annual turnover**, whichever is higher. The Digital Omnibus on AI moved the *high-risk* timeline (to December 2027) but left the Article 50 transparency date in place. Re-check before quoting a date at a customer.

## Privacy notice contents

One document, plain language, covering: who you are and how to contact you (and the DPO if appointed); what you collect and why, per purpose, with the lawful basis; whether providing it is required and what happens if not; who you share it with, naming every sub-processor; whether data leaves the country and under what safeguards; how long you keep each type; the rights available and how to exercise them; the complaint route to the regulator; the cookie and analytics position; and whether automated decision-making or AI is used.

Rules learned from real launch failures: the notice must name the actual services (the database host, the email provider, the payment gateway, the model provider), not "trusted third parties"; it must be linked from every collection point, not only the footer; and it must be updated in the same change that adds a vendor, because an out-of-date notice is nearly as bad as none.

## Consent records

Store per user, per purpose: whether consent was given, the timestamp, the exact notice/consent text version, the source (form, API, import), and the withdrawal timestamp. A checkbox that disappears on submit is not a record. A pre-filled box is not consent. Withdrawal must be one action and must propagate to the systems that relied on it — which means the marketing list, not only the app database.

## Data subject requests

A runbook with a named owner, and a flow the team can run without a developer:

1. **Intake** — a form or an address, logged with a ticket id and a received date.
2. **Verify identity** — proportional to the risk; do not ask for an IC scan to answer an email preference request.
3. **Locate** — every store in the inventory: primary DB, secondary stores, search index, analytics, email platform, support desk, backups (state the backup limitation in the response).
4. **Fulfil** — export as JSON/CSV for portability; delete or correct; record what was done.
5. **Close** — respond within one month (GDPR) or the PDPA equivalent, and tell the subject what was retained and why.
6. **Log** — every request, its outcome, and its timing. An audit asks for this.

## Breach response

One page, four questions answered in advance:

| Question | Answer format |
|---|---|
| Who decides whether it is notifiable? | Named role, plus a deputy |
| Whom do we notify, and how fast? | Supervisory authority within 72 h (both GDPR and amended PDPA), affected individuals when risk is high, payment provider, insurer |
| What do we say? | Template: what happened, what data, what we did, what the user should do, contact route |
| How do we find out? | The alerting and log review that actually runs, with an owner |

Breach detection is an engineering deliverable: unusual access patterns, bulk exports, auth failures, and sudden permission changes need alerts, otherwise the 72-hour clock starts whenever a third party tells you.

## Vendors

- A DPA or the vendor's standard data-processing terms on file for every processor, with the security schedule attached.
- A list of sub-processors, and a habit of re-reading the vendor's notice when it changes — a vendor adding a sub-processor silently is a change in your processing.
- Record the storage region per vendor. "The cloud" is not a jurisdiction.
- Offboarding: when a vendor is dropped, the data is deleted there too, in writing.
