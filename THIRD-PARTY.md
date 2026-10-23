# Third-party attribution

This repository is a curated set. Some skills are original, some are derived from permissively licensed work, and some condense publicly documented rule sets without reproducing their text. Per-skill notices live in `skills/<name>/LICENSE`; this file is the index.

## Derived skills

| Upstream | Licence | Used in | What came across |
|---|---|---|---|
| [HoangNguyen0403/agent-skills-standard](https://github.com/HoangNguyen0403/agent-skills-standard) | MIT, © 2026 Hoang Nguyen | `code-quality`, `system-design`, `zeroday-compliance` | the base best-practices, TDD, API-design, database-design, and security-audit material; merged, rewritten and extended |
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | Apache-2.0, © Mahipal Jangra and contributors | `zeroday-compliance/references/audit-standards.md`, `audit-procedures.md` | SOC 2 / GDPR / HIPAA / PCI control catalogs and assessment procedures, retained largely verbatim |
| [patrikherak/llm-privacy](https://github.com/patrikherak/llm-privacy) | MIT, © 2026 Patrik Herák | `zeroday-compliance/scripts/llm_privacy.py`, `references/pii-masking.md`, `pii-locales.md` | the reversible PII mask/restore pipeline; the script is unmodified |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | `docs-write/references/writing-for-agents.md` | guidance for documents an agent reads |
| [Cathryn Lavery](https://github.com/cathrynlavery) — `diagram-design` | MIT, © 2025 | `diagram-design` | the skill in full; see its own `LICENSE` and `THIRD_PARTY_LICENSES.md` |

Each of these licences requires the copyright notice to travel with substantial portions of the work, which is why the per-skill `LICENSE` files are kept rather than collapsed into one.

## Referenced, not reproduced

These informed the content of `system-design` and `zeroday-compliance`. No text is copied verbatim; rules were restated and tables rebuilt.

- [ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) — component explainers and diagrams
- [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) — latency and powers-of-two tables, availability arithmetic, worked designs
- [binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) — symptom-to-pattern taxonomy
- [microsoft/api-guidelines](https://github.com/microsoft/api-guidelines) — Azure REST conventions
- [zalando/restful-api-guidelines](https://github.com/zalando/restful-api-guidelines) — rule-numbered REST catalog; rule numbers are cited where used
- [public-apis/public-apis](https://github.com/public-apis/public-apis) — API catalogue only, no rules taken
- [benavlabs/vibe-check](https://github.com/benavlabs/vibe-check) — MIT; vulnerability category ordering, and the scanner referenced in `zeroday-compliance/references/tooling.md`
- Web write-ups on launch readiness: vibeaudits.com, blog.vibecoder.me, securitywall.co, launchreadycode.com — paraphrased obligations only

Icons and fonts inside `diagram-design` are attributed in `skills/diagram-design/THIRD_PARTY_LICENSES.md` (Tabler Icons, Simple Icons, Devicon, log-z/logos, Instrument Serif under the SIL Open Font License).

Legal sources cited in `zeroday-compliance/references/legal.md` are public statutes and regulator guidance (Malaysia PDPA Act 709 and Act A1727; GDPR; EU AI Act 2024/1689). Quoted figures are dated in that file — verify before relying on them.
