# SRS: software requirements specification

Condensed from spec-forge's SRS skill (see NOTICE.md). Based on IEEE 830 and ISO/IEC/IEEE 29148, which are the authority; read them for exact clause wording. An SRS says **what** the system shall do and under what constraints, never **how**.

## Workflow
1. **Scan context.** Read the repo, any existing SRS, and the upstream PRD. List existing requirement IDs.
2. **Reuse, extend, or new** for each requirement. Default to extending the existing SRS in place. Never create `srs-v2.md` or append `## Update` blocks. IDs are contracts: never renumber, never reuse a retired ID; split a requirement by keeping the old ID on one part.
3. **Infer, then ask.** State assumptions you can infer from the PRD and code. Ask only what changes the requirements and cannot be inferred: NFR thresholds, regulatory duties, integration contracts.
4. **Write** to the structure below.
5. **Trace.** Build the RTM mapping each PRD item to SRS IDs with coverage (Full / Partial / None). Find uncovered PRD items and dangling references (a grep over IDs does this).
6. **Check** against the list at the end. Fix before delivery.

## Structure
1. Document information (ID, version, status, owner, related PRD) and revision history
2. Introduction: purpose, **scope boundaries**, definitions, references, overview
3. Overall description: product perspective, functions, user classes, constraints, assumptions and dependencies
4. **Functional requirements**, grouped by module, plus cross-cutting sections: CRUD matrix, state machines, permission matrix, error catalogue
5. **Non-functional requirements** by category
6. Data requirements: data model, data dictionary
7. External interfaces: user, hardware, software, communication
8. **Requirements traceability matrix**
9. Acceptance and change control
10. Appendix: diagrams, open questions, glossary

**Scope boundaries must have an out-of-scope table**: each row names the exclusion, why, and who owns it instead. If nothing is excluded, say so with a reason. Also state precedence when documents disagree (SRS, then PRD, then SDS, then chat; chat agreements are not binding until recorded here).

## Requirement IDs
- Functional: `FR-<MODULE>-<NNN>` (FR-AUTH-001). Non-functional: `NFR-<CAT>-<NNN>` with CAT in PERF, SEC, REL, AVL, MNT, PRT, USB.
- Zero-padded, sequential, unique across the document. The next free number is computed from the existing file, not guessed.

## Language
- **shall** = mandatory, **should** = recommended, **may** = optional (RFC 2119). One requirement, one `shall`, one interpretation.
- No "fast", "user-friendly", "efficient", "robust", "appropriate" without a number. "Within 200 ms at p95", not "fast".
- Describe behaviour, not implementation. A technology appears only when it is a real constraint.

## A functional requirement carries
ID and title | description (system behaviour) | actors (human and API/agent consumers, with interaction pattern) | preconditions | numbered main flow | alternative and error flows | postconditions | **input field rules** | **acceptance criteria** | priority | **priority rationale** | source (PRD item).

- **Input field rules**: a table per requirement that accepts input: type, required, exact constraints, default, rejection behaviour naming a catalogue error code. "Max 254 characters", not "reasonable length"; "1 <= n <= 999", not "a positive number". Say explicitly when a requirement takes no input.
- **Acceptance criteria**: Given / When / Then, objectively settleable. A criterion nobody can decide is a defect in the spec. Cover the boundary, the error, and the negative case, not only the happy path. For agent-facing requirements use exact contracts ("POST /v1/users with {name, email} returns 201 and a body containing id, email, created_at").
- **Priority**: P0 must-have, P1 should-have, P2 nice-to-have, each with a **rationale** tied to a consequence ("P0: no launch without it, sole entry point for all actions").

## Cross-cutting sections
- **CRUD matrix**: entities by Create/Read/Update/Delete, each cell the governing FR. A blank cell is either deliberate (say why) or a gap.
- **State machines**: per entity with a lifecycle: diagram, legal-transition table (trigger, actor, guard, FR), and an **illegal-transition table** (idempotent-ignore or hard-reject, error code, side effects). Half a state machine is only the legal half.
- **Permission matrix**: role x operation x data scope, each scope a concrete predicate (`records where owner_id = authenticated principal`). Decide denial behaviour on purpose: 403 reveals the record exists, 404 hides it.
- **Error catalogue**: every anticipated failure as its own code with trigger, visible message, recovery path and source FR. No `INTERNAL_ERROR` standing in for an anticipated cause. For each external dependency, define behaviour when it is down: fail closed, fail open, serve stale (how stale), or queue and retry (how long).

## Non-functional requirements
Each NFR carries: a **metric**, a **target value**, a **measurement method**, a **verification** method (Test / Demonstration / Inspection / Analysis, naming environment and load), and a **threshold rationale** citing a source (SLA, production baseline, benchmark, regulation, cost trade-off). A target with no rationale is a guess; a target with no verification cannot be accepted or disputed.
Categories: performance (p50/p95/p99, throughput, capacity), security, reliability (MTBF, MTTR, integrity), availability (uptime, RPO/RTO), maintainability, portability, usability (accessibility level, task time).

## Quality attributes (IEEE 830)
Every requirement is **unambiguous, testable, traceable (back to source, forward to design and test), complete**. Also correct, consistent, ranked, modifiable.

## Check before delivery
- [ ] Out-of-scope table populated; precedence stated
- [ ] Every PRD item covered or its exclusion justified; RTM complete
- [ ] Every FR has input rules (or says none), Given/When/Then criteria, priority with rationale
- [ ] No vague adjectives; correct shall/should/may; no implementation detail
- [ ] State machines include illegal transitions; permission matrix defines scopes and denial behaviour
- [ ] Error catalogue has no catch-all; dependency degradation stated
- [ ] Every NFR has metric, target, verification and rationale
- [ ] IDs unique, none reused; no template placeholders left
- [ ] Data dictionary covers every field, type and constraint
