# Testing

The intent record, the bounded loop, test shape, and the runner commands. Read before writing any test.

## Quality Contract

### Test Intent Record

Record one row before each behavior/risk group:

| Field | Required evidence |
| --- | --- |
| `contract` | Observable result or side effect owned by the application |
| `fault` | Plausible regression that would make the test fail |
| `layer` | Smallest honest layer and why broader behavior is not needed |
| `cases` | Minimal distinct equivalence classes; merge equivalent inputs |
| `command` | Exact focused, single-run command |

The record is an agent handoff artifact, not a comment requirement inside test code.

### Admission checks

- Before proposing a new test, compare against the existing suite; discard if the behavior and fault are already covered by nearby or upstream tests.
- For existing tests: never auto-delete on apparent static duplication alone. Recommending deletion requires proof of no unique behavioral contribution plus measured full-suite dynamic coverage/mutation impact; otherwise suggest review or refactoring.
- Keep a case only when it detects a distinct fault, boundary, or contract rule.
- Prefer public behavior and state transitions over private methods, call counts, or mock existence.
- Verify one logical contract per test; multiple assertions are allowed when verifying related aspects or outward side effects of that single contract.
- Distinguish outward side effects from internal mock choreography: verify what the system produces or changes externally, not how collaborators are invoked internally.
- Coverage percentages are diagnostic rather than admission gates; never write padding tests to hit an arbitrary target.
- The Four Pillars (Protection against Regressions, Resistance to Refactoring, Fast Feedback, Maintainability) provide a qualitative reasoning framework, not a static numeric score (avoid inventing formulas like $P \times R \times F \times M$ per test without rigorous empirical measurement across all four dimensions).
- Route cross-component behavior to integration/contract tests. Do not label a mock-heavy orchestration test as a unit test.
- Use deterministic fixtures, explicit cleanup, and stable clocks/data. A test that passes only in one order is not evidence.

### RED taxonomy

| Status | Meaning | Next action |
| --- | --- | --- |
| `expected_red` | Owned behavior is missing or wrong | Implement the smallest fix |
| `invalid_red` | Import, syntax, fixture, mock, or environment defect | Repair test setup; do not change production |
| `unexpected_green` | Behavior already exists or test is redundant | Inspect existing coverage and revise/remove case |
| `verification_infra_failed` | Runner missing, timeout, or orphaned process | Stop, clean owned processes, report exact command/error |

### Escalation ladder

1. Lint/type preflight when configured.
2. One focused test target, foreground and sequential.
3. Related unit file/package after the slice is green.
4. Integration/contract target only when the changed boundary requires it.
5. Full suite only for an explicit repository or release gate.

Use the repository timeout when present; otherwise use 120 seconds for a focused command. Never retry without a changed hypothesis. Never use a broad `pkill`; terminate only the process group created for the command and verify it is gone.

## Protocols

### Protocol: Bug Fix Discovery

When a bug is reported:

1. **REPRODUCE**: Write a minimal failing test that triggers the bug.
2. **VERIFY RED**: Watch the test fail with the expected error.
3. **FIX**: Write minimal code to pass.
4. **VERIFY GREEN**: Test passes + prevents regressions forever.

For legacy code, characterization can document current behavior first. The intended change still needs its own RED evidence; unrelated existing implementation is not deleted.

### Protocol: Scaffolding (When Stuck)

- **API First**: Write the test you _wish_ you could run. Use the ideal interface.
- **Assertion First**: Work backwards from `expect(...)`.
- **Simplification**: If the test is too hard to write, the design is too coupled. Refactor design _before_ finishing the test.

### Protocol: Bounded Verification

1. Run lint/type checks when configured.
2. Run one focused target in foreground, single-run, sequential mode.
3. Classify `expected_red`, `invalid_red`, `unexpected_green`, or `verification_infra_failed`.
4. Escalate to related or full suites only when the changed boundary requires it.
5. Use the project timeout or 120 seconds for a focused command; clean only its process group and never retry unchanged failures.

## TDD Best Practices

Extracted from industry standards (Graphite, dev.to, et al.).

### 1. F.I.R.S.T. Principles

- **F**ast: Tests should run quickly. Slow tests discourage frequent running.
- **I**solated/Independent: Tests should not depend on each other or external state (DB, Network).
- **R**epeatable: Run it 1,000 times, get the same result.
- **S**elf-Validating: The test output is boolean (Pass/Fail). No manual inspection needed.
- **T**horough: Test distinct contract rules, boundaries, and plausible faults; do not enumerate low-signal combinations.

### 2. The "Three Laws" of TDD

1.  You are not allowed to write any production code unless it is to make a failing unit test pass.
2.  You are not allowed to write any more of a unit test than is sufficient to fail; and compilation failures are failures.
3.  You are not allowed to write any more production code than is sufficient to pass the one failing unit test.

### 3. Testing Philosophy

- **Test Behavior, Not Implementation**: Refactoring should not break tests.
- **Positive & Negative**: Test success and failure contracts when each represents a distinct risk.
- **One Logical Behavior**: Keep one behavior per test; multiple assertions may prove that behavior and its required side effect.
- **Project-Owned Coverage**: Use repository-configured thresholds when present. Never pad tests to reach a universal percentage.

### 4. When NOT to TDD

- UI Tweaks (CSS modifications, color changes).
- Exploratory prototyping (throwaway code).

### 5. TDD vs BDD (Behavior-Driven Development)

- **TDD**: Starts at the smallest honest layer: use a unit for pure owned behavior, and a broader contract/integration layer when the behavior crosses components.
- **BDD**: Focuses on system behavior from a user's perspective. "Given I am logged in, When I check out, Then my order is placed."
- _Tip_: Use TDD for internal logic and BDD (often with tools like Cucumber or Gherkin syntax) for high-level user flows.
