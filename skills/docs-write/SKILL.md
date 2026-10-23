---
name: docs-write
description: Write and edit technical documents and prose - SRS (software requirements), SDS/SDD (software design), PRD and specs, test plans, ADRs, READMEs, API docs, code comments, handoff notes, articles and blog drafts, and documents an agent reads (skills, AGENTS.md, CLAUDE.md). Use when asked to document, specify, draft, or tighten text. Not for code changes or UI copy.
---
# Docs and writing

Pick the document type, load its guide, write. Load only the guide the task needs.

| Writing... | Load |
|---|---|
| **SRS**: software requirements specification (IEEE 830 / ISO 29148) | [srs.md](references/srs.md) |
| **SDS / SDD**: software design or technical design document (IEEE 1016) | [sds.md](references/sds.md) |
| Test plan or test cases from an SRS/SDS | [test-docs.md](references/test-docs.md) |
| PRD / feature spec from the current conversation | [spec-template.md](references/spec-template.md) |
| ADR, README, code comments, docstrings, API docs, runbook, changelog | [code-docs.md](references/code-docs.md) |
| A skill, `AGENTS.md`, `CLAUDE.md`, or any doc an agent will read | [writing-for-agents.md](references/writing-for-agents.md) |
| An article, essay or post from raw notes | [articles.md](references/articles.md) |
| A handoff so a fresh agent can continue | [handoff.md](references/handoff.md) |
| Any prose: truth rules, style, banned phrases, final pass | [style-and-truth.md](references/style-and-truth.md) |

Document chain: PRD (why, for whom) -> SRS (what, testable) -> SDS (how) -> test plan (proof). Each links back by requirement ID. Do not write a downstream document before the upstream one exists; ask for it or write it first.

## Rules for every document

1. **Name the reader and their next action.** A new hire running setup, an implementer building FR-AUTH-003, a tester writing cases, an agent choosing a tool. Write for that action.
2. **Read first, then write.** Open up to two comparable documents in the same folder and follow their structure and tone. Check whether the topic already has an owner document; extend it in place instead of starting a rival file. Add the new document to any index README.
3. **Classify before editing.** Normative (contracts, specs): do not weaken them to match code, record the violation. Descriptive (flows, component docs): match the code exactly. Historical (changelogs, accepted ADRs): never rewrite, supersede with a new entry. Runbook: every step must have been run. Reference: exhaustive.
4. **Why before what.** Code, config and `--help` already show what. Record intent, constraints, the gotcha, the rejected alternative.
5. **One source of truth.** State each fact once; link to it elsewhere. Never restate what a command or config file already reports.
6. **Lead with the answer** at every level: document, chapter, paragraph.
7. **State the target behaviour.** Write "return early on empty input", not "never process empty input". A banned behaviour named in the text becomes more present; keep a prohibition only as a hard guardrail, paired with the positive target.
8. **Concrete over general.** Exact values, commands, paths, copy-pasteable examples. A number beats an adjective. Expand an abbreviation at first use; one term per concept all the way through.
9. **Trace every claim.** Never state as fact what you cannot point to (code path, test, document, primary source). Unsourced input: use it and mark `**[source wanted: ...]**`. Unfinished parts: `**[DRAFT - input wanted]**`. Never invent a citation, a metric or a requirement.
10. **Ship docs with the change.** Update the document in the same change as the thing it describes.

## Finish

Re-read as the reader. Follow every link, run every command, check every path and ID. Remove placeholders unless a template was requested. Report what was written, where, and what is unverified.

Sources and licences: [NOTICE.md](NOTICE.md).
