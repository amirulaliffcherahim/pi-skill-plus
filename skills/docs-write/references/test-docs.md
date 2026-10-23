# Test plan and test cases

Condensed from spec-forge's test-plan and test-cases skills (see NOTICE.md). Based on IEEE 829/29119 practice. Written after the SRS and SDS exist: every test case traces to a requirement ID.

## Test plan structure
1. Document information, revision history
2. Introduction: purpose, scope, references, definitions
3. **Test strategy**: levels, types, methods, rationale; database policy; what may be mocked (exceptions)
4. Test scope: in scope, out of scope (with reasons)
5. Test environment: hardware, software, network, test data
6. **Entry and exit criteria**
7. Test case specifications: happy path, error/negative, boundary, data integrity, performance
8. Test data: sets and management
9. Defect management: severity, lifecycle, report template
10. Risk assessment
11. Traceability matrix (requirement ID to test case IDs)

## Strategy
- **Test pyramid**: many fast unit tests, fewer integration tests against real dependencies, few end-to-end tests. State the ratio and why.
- **Real database over mocks** for anything that touches persistence: mocks hide schema, constraint and transaction bugs. List the narrow cases where a mock is acceptable (third-party network, clock, payment, email) and say why.
- **Risk-based priority**: rank by impact x likelihood and test the top first.

## Test case structure
Each case has: unique ID (`TC-<MODULE>-<NNN>`), title, linked requirement ID(s), priority, preconditions, test data, numbered steps, **expected result** (exact values), actual result and status (left blank in a plan), notes.

## Design principles
- **Positive and negative**: every P0 requirement gets a happy path, a boundary/error case, and a negative case. A happy-path-only set is rejected.
- **Boundary value analysis**: min, min-1, min+1, max, max-1, max+1 for every numeric, length and size constraint in the SRS input rules.
- **Edge cases**: empty input, unicode, duplicates, concurrency, null vs zero, timezones, overflow, timeout.
- **Data integrity**: referential integrity, transactions and rollback, idempotency, migration behaviour.
- **Security**: authentication, authorisation (the 403 vs 404 decision), injection and traversal, token expiry.
- **Performance**: tied to the NFR targets, naming load profile, environment and percentile.
- **Combination tests** for interacting units and cross-module flows; a coverage matrix of unit x depth shows gaps.
- Expected results come from the SRS acceptance criteria, never from observing current behaviour.

## Entry and exit criteria
- **Entry**: SRS and SDS approved, build deployed to the test environment, test data loaded, smoke test green.
- **Exit**: all P0 cases run and passed, no open critical or high defects, requirement coverage at the stated threshold, performance targets met or deviations signed off.

## Defects
Severity: Critical (data loss, security, no workaround), High (major feature broken), Medium (workaround exists), Low (cosmetic). Lifecycle: New, Triaged, In progress, Fixed, Verified, Closed (or Rejected, Reopened). A report carries ID, title, severity, steps, expected vs actual, environment, evidence, linked requirement and test case.

## Check before delivery
- [ ] Every FR and NFR has at least one test case; no orphan test cases
- [ ] Every P0 requirement has positive, boundary/error and negative cases
- [ ] Expected results are exact and traceable to acceptance criteria
- [ ] Mocking exceptions listed with reasons; environment and data defined
- [ ] Entry and exit criteria are objectively checkable
