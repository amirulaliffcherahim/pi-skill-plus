# Code-adjacent documents

Covers comments, docstrings, README, ADRs, decision logs, runbooks, changelogs and API/contract docs. ADR, runbook, changelog and contract rules are condensed from riekelt/technical-writer (MIT, see NOTICE.md). For SRS or SDS use their own guides.

## Comments and docstrings
- Explain **why** the logic exists; the code already says what. Example: for a retry delay, say that jitter prevents a thundering herd, instead of restating the arithmetic.
- Public members get the language's doc-comment form (JSDoc, docstring, `///`) with arguments, returns and a usage example.
- Delete commented-out code; Git keeps history.
- `TODO(owner): description`, linked to a ticket. No orphan TODOs.
- Describe current behaviour only. "Now uses", "replaces the old" and "was refactored to" describe an edit, not the system.

## README
Mission in one sentence; prerequisites and exact install and run commands (copy-pasteable, each with a check command); usage; configuration; known quirks and fixes; where deeper docs live. Run the **remove-the-name test**: delete the product name and reread; if a stranger could not tell what it is about, rewrite from its specifics. Ship the README with the feature.

## ADR (one decision per record, append-only)
```markdown
# ADR-<n>: <short title>
Status: Proposed / Accepted / Superseded by ADR-<m>   Date: YYYY-MM-DD   Deciders: <names>
## Context        forces at play, factual, without giving the decision away
## Decision       "We release on tags", active voice
## Consequences   Positive / Negative / Neutral
## Alternatives considered   each with its strongest argument for, and why it lost
## References
```
- **Negative consequences may not be empty.** A rejection without the alternative's strongest argument is a strawman.
- An accepted ADR is immutable. Its only permitted edit is the Status line gaining "Superseded by ADR-m"; a wrong entry gets a new dated entry.
- Record a decision before citing it; a chat is not a durable source. Offer to record when you hear "we decided X instead of Y".
- A lighter **decision log** entry: date, the rule as one imperative sentence, `Why:` bullets, `Instead of:` the rejected option.

## Runbook, setup guide, procedure
The reader is in a hurry. Write from a **real run**: every step one actually taken. A procedure never run is a draft; label it so, or run it first.
- State what the document is and is not, up front. A **risk legend** when steps differ: safe anytime / operator-only (writes to production) / manual outside the terminal.
- TL;DR happy path first, then numbered steps, one action each, imperative, copy-pasteable with real example values.
- Version-pinned prerequisites each with a check command. Steps state the cost of wrong ordering inline.
- Every state-changing procedure names its **rollback**, or says plainly there is none.
- End with "verify it worked": the observable end state and the command that proves it.
- **Troubleshooting entries are symptom-first**: Symptom (verbatim error string, searchable), Cause, Fix (exact commands); cheapest diagnostic first.
- **Migration or deprecation guide**: a before/after mapping table is the core, rollback per step, dates for what stops working ("a future release" is banned), and a stated completion condition after which it becomes historical.

## Changelog and release notes
- Append-only, newest first, ISO dates. Categories: Added / Changed / Deprecated / Fixed / Removed / Security. A deprecation carries a removal date and the replacement.
- **Breaking changes lead**, each with the required migration action.
- Entry shape: a bold lead stating the user impact, then root cause, then the fix. "Fixed" explains the failure mode, not the diff.
- Honesty: list **known issues**, **deferred items** and **deliberate omissions**. Never mark something implemented, deployed or verified unless that exact action was done and checked.
- Release notes are the user-facing cut of the same facts and must never contradict the changelog.

## API and contract documentation
Written for a stranger who cannot see the code. Document the wire, exhaustively, every endpoint, field and error.
- If a generated OpenAPI/AsyncAPI spec exists it owns the field tables; the prose adds only semantics and links the spec. Never hand-maintain field tables beside a generated one.
- Levels, each with one home: **index** (what exists), **semantics** (what invoking it does: side effects, events, idempotency), **shape** (one field table per DTO), **example** (at most one per DTO, never containing a field the table lacks).
- Use **wire types** (`string (date, ISO 8601)`), not language types. One `Source:` line per DTO. Required is `yes`, `no`, or `if <condition>`. State omitted vs null wherever it matters. Enums get their own table.
- Verify against the **serializer configuration**, not the class: a global null-omitter or date format changes the contract.
- Catalogue errors once (envelope plus status table); an endpoint lists only which apply.
