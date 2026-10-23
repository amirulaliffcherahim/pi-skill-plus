# Sources and Provenance

## How this skill was assembled

- **The eight-section gate** is the user's own pre-launch outline. It was kept as the spine, with items added, tagged BLOCK/HOLD/ADVICE, and given a verification method for each.
- **The adversarial test matrix** and the authentication checks (session expiry, JWT secret strength, single-use reset tokens, enforced email verification, OAuth `state`, RLS testing as two users) come from the vibeaudits checklist.
- **The category ordering** — database access control first, committed secrets third, IDOR fourth — and the "items 1–5 are what actually took apps down" framing come from the vibe-check repository, along with the scanner referenced in [tooling.md](tooling.md).
- **Legal obligations** (consent records, sub-processors named in the notice, 30-day DSR clock, cookie audit) follow the vibecoder GDPR guide; the **EU AI Act Article 50** obligation and the SOC 2 readiness minimums follow the launchreadycode checklist.
- **Vendor repositories** (Stripe legacy processes, hosted fields, gateway callbacks, PCI position) follow the payment-provider documentation of each gateway named.
- The securitywall checklist contributed the tool pipeline shape (SAST → DAST → secret scan → dependency scan); its vendor framing was not used.

## Sources

| Source | What it is good for | Caveat |
|---|---|---|
| [vibeaudits.com/blog/vibe-coded-app-security-checklist](https://vibeaudits.com/blog/vibe-coded-app-security-checklist) | 25 concrete pre-launch checks, and a table of adversarial tests with expected results — the closest thing to an acceptance test suite for a launch | vendor blog for an audit firm; the checks are sound, the calls to action are sales |
| [github.com/benavlabs/vibe-check](https://github.com/benavlabs/vibe-check) (MIT) | 17 vulnerability categories ranked by real incidents, a zero-dependency external scanner (`check.py`), `AGENTS.md` security rules, a manual checklist | scanner is black-box surface only — no auth, no code review, no business logic |
| [blog.vibecoder.me/gdpr-compliance-vibe-coded-apps](https://blog.vibecoder.me/gdpr-compliance-vibe-coded-apps) | practical GDPR for a small app: consent records, notice contents, DSR deadlines, cookie auditing | GDPR-centric; PDPA-specific obligations are separate |
| [securitywall.co/blog/vibe-coding-security-checklist](https://securitywall.co/blog/vibe-coding-security-checklist) | a structured 44-check layout and the automated-tooling pipeline | mostly service marketing; check list itself is not published in the fetched text |
| [launchreadycode.com/blog/vibe-coding-compliance-checklist](https://launchreadycode.com/blog/vibe-coding-compliance-checklist) | EU AI Act Article 50 disclosure duty, SOC 2 day-zero minimums, RLS failure mode (`USING (true)` = off) | sells a paid compliance scan; stats are their own scan data |
| Malaysian PDPA (Act 709, as amended 2024) | the actual obligations for a Malaysian app | verify commencement dates and DPO thresholds with the Commissioner's guidance |

Vendor statistics quoted in those sources (for example "61% of AI-generated code is functional, 10.5% secure") are cited by the vendors themselves. Treat them as directional, not as measurements to rely on.

## Inherited skills merged into this one

| Old skill | What survived | Licence |
|---|---|---|
| `common-security-audit` | the vulnerability-scanning discipline and severity weighting, now in [appsec.md](appsec.md) and [tooling.md](tooling.md) | MIT, © 2026 Hoang Nguyen — `LICENSE` (agent-skills-standard) |
| `common-compliance` | the five-stage assessment loop, evidence discipline, Type I/II distinction, framework routing, output format — now [frameworks.md](frameworks.md), plus the catalogs and procedures retained verbatim as [audit-standards.md](audit-standards.md) and [audit-procedures.md](audit-procedures.md) | Apache-2.0, © Mahipal Jangra and contributors (Anthropic Cybersecurity Skills) — `LICENSE-compliance` |
| `common-privacy-pii` | the mask/restore pipeline, now [pii-masking.md](pii-masking.md) + `scripts/llm_privacy.py`, unchanged | MIT, © 2026 Patrik Herák (llm-privacy) — `LICENSE-llm-privacy` |

The three licence notices are retained because each licence requires it: MIT and Apache-2.0 both travel with substantial portions of the work. `scripts/llm_privacy.py` is unmodified; if you change it, the upstream licence still governs the original.

## Limits of this skill

- Not legal advice. Anything with IC/passport numbers, health, financial, biometric, or children's data needs a review by someone qualified in the applicable regime.
- Not a penetration test. The gate catches the classes that consistently break generated apps; a determined attacker with business-logic creativity needs a human who does that for a living.
- The compliance frameworks material answers questionnaires and prepares audits; it does not attest anything. Only an independent auditor issues a SOC 2 report.
