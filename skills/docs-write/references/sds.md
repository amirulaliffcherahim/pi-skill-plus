# SDS / SDD: software design (technical design) document

Condensed from spec-forge's tech-design skill (see NOTICE.md). Relates to IEEE 1016 (Software Design Descriptions), which is the authority for the formal standard. An SDS says **how** the system satisfies the SRS. Every design element traces to a requirement ID; every FR and NFR is addressed somewhere or explicitly deferred.

## Workflow
1. **Scan the codebase and docs**: languages, frameworks, DB, auth, existing architecture, existing design docs. Read the upstream SRS and PRD.
2. **Extend, do not duplicate.** If a design doc exists, edit it in place. Keep requirement IDs intact.
3. **Infer, then ask**: only what changes the design and cannot be read from the repo (scale, SLAs, compliance, deployment target).
4. **Write**, filling only sections the project actually needs. A CLI or library has no database section and no rollback plan: write "not applicable, <one-line reason>" and keep the heading. Never invent filler.
5. **Trace** each SRS FR to the component that implements it and each NFR to the decision that satisfies it. List what is deliberately deferred, with a reason. A grep over requirement IDs shows uncovered and dangling ones.
6. **Check** against the list at the end.

## Structure
1. Document information, revision history
2. Overview: background, goals, **non-goals**, scope, user scenarios (human and agent consumers), acceptance criteria, success metrics
3. System context (C4 level 1)
4. **Solution design**: alternatives, comparison matrix, decision and rationale
5. Architecture (C4 level 2 container, level 3 component where it helps)
6. Technology stack, naming conventions, validation, limits and edge cases, business rules, error handling
7. Detailed design: components, interactions, core workflow, data flow
8. API design
9. Database design
10. Security design
11. Performance design
12. Observability
13. Deployment and operations (environments, CI/CD, rollback)
14. Risks, open questions, traceability matrix

## Rules that make a design reviewable
- **Genuine alternatives only.** Compare real options on the same criteria (complexity, performance, scalability ceiling, cost, team skill, delivery time, risk). Where one approach is viable, write "no meaningful alternative, rationale: ..." instead of a strawman. Give the strongest argument for each rejected option and say what the chosen option does **not** solve.
- **Technology stack table**: every layer, a version, and a project-specific reason. "It is popular" is not a reason; "team has 3 years of Go and the concurrency model fits event processing" is.
- **Naming conventions** at three levels, consistent across them: code (files, types, functions), API (paths, params, body fields, error codes), database (tables, columns, `idx_<table>_<cols>`, `fk_<table>_<ref>`).
- **Validation matrix** for every input crossing a trust boundary: name, type, required, min, max, pattern, default, sanitisation, exact error returned. Also: coercion rules, injection and traversal defences, null vs missing vs empty.
- **Limits and edge cases**: for every limit (body size, field length, array size, rate limit, upload size, nesting depth, page cap, batch size) state the exact number, the behaviour when exceeded, and why. Edge-case table covers at least empty input, unicode, duplicate requests, concurrent updates, delete with references, timezones, overflow, null vs zero, long-running timeouts.
- **Business rules precise enough to implement**: state machines (every transition with from, to, trigger, guard, side effects, plus illegal transitions); computations with ID, formula, inputs, precision, rounding and a **worked example with real numbers**; conditional logic with both branches.
- **Error taxonomy**: category, HTTP status, code pattern, retry or not, user message. Per external dependency: retries, backoff, circuit-breaker threshold, timeout, fallback.
- **API spec** (any protocol): operation, auth, request schema with validation, response schema with example payloads, full error table. REST: plural-noun resources, correct verbs, URL versioning, one error shape with a request ID.
- **Database**: every table with columns, types, constraints and purpose; ER diagram; indexes with the query each supports; migration plan (expand-contract, backfill, backward compatibility).
- **Security as a first-class section**: authentication and token lifecycle, authorisation model and where it is enforced, encryption at rest and in transit and key rotation, audit events, retention and tamper protection.
- **Performance**: numeric targets (p50/p95/p99, throughput, error rate), what is cached, where, and how it is invalidated, and the optimisation plan. A target needs a rationale.
- **Diagrams**: Mermaid in fenced `mermaid` blocks, source-controlled, each with a title and human-readable labels. C4 levels 1 and 2 at minimum. Delete stale renders; everything legible in an image is a claim.

## Check before delivery
- [ ] Every FR and NFR maps to a component or decision, or is deferred with a reason
- [ ] Alternatives are real, compared on shared criteria, with a recorded decision
- [ ] Validation matrix covers every external input; limits state exact numbers and behaviour
- [ ] State machines list illegal transitions; computations have worked examples
- [ ] Error taxonomy and dependency fallbacks defined; security section complete
- [ ] Performance targets are numeric with rationale; observability planned
- [ ] Not-applicable sections say why; no placeholder text remains
- [ ] Diagrams render and match the text
