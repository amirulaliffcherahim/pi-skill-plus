---
name: code-quality
description: Write and change code with tests - match the repo's conventions, keep structure readable, and run a bounded test-first loop. Use when implementing a feature, writing or changing a function, refactoring, or fixing a bug.
---

# Code Quality

Applies to any request that creates or changes code: features, fixes, refactors. Read it before opening the editor, not after the diff exists.

## 0. Decide the mode

| Change | Mode |
|---|---|
| New behaviour, new or changed contract, changed output | test-first: RED → GREEN → REFACTOR |
| Bug with a plausible regression path | failing test first, then the fix |
| Mechanical: rename, formatting, comment, config value, dependency bump that changes nothing observable | no new test; run the existing suite |
| Throwaway spike to learn something | say it is a spike, delete it after — never promote it silently |

Ceremony on a mechanical change is waste. Shipping a behaviour change with no expected RED is gambling. Either way, name the mode and the reason before writing.

**The gate has one escape rule: if any observable output, contract, or side effect changes, it is not mechanical.** A "config value" that changes behaviour is a behaviour change; a rename that alters a public name is a contract change. Unsure which side you are on counts as behaviour. The two costs are not symmetric — a needless test costs minutes, an untested behaviour change costs a production incident.

**Criterion:** the mode is stated, and it matches what actually changed.

## 1. Read the neighbourhood first

Before editing: the file being changed, one or two of its neighbours, how the repo already names things, handles errors, logs, and tests, and the exact command that runs the suite. Match existing convention over generic preference — a new abstraction in a plain file is a cost, not a gift.

**Criterion:** you know the command that proves the change, and you know whether an existing test already covers this path.

## 2. Design the change

- **Smallest change** that satisfies the requirement. Nothing "while I'm here".
- **Names reveal intent** (`isUserAuthenticated`, not `checkUser`); match the repo's casing and vocabulary.
- **Guard clauses over nesting**; functions short enough to read in one screen.
- **Duplication is cheaper than the wrong abstraction**: duplicate twice, abstract on the third.
- **YAGNI** for "we might need it later"; no unused parameters, flags, or config.
- **Validate at the boundary once** — external input at the edge, trusted values inside.
- **Pass dependencies in**, not globals or module-level mutable state.
- **Comments explain why**, not what; if the what needs explaining, rename it.

**Criterion:** every new abstraction, parameter, or config value is explainable in one sentence — otherwise it was deleted.

## 3. Write the intent before the test

One intent record per behaviour or risk: the observable contract, the distinct fault the test catches, the smallest honest layer, the minimal distinct cases, and the focused command.

**Criterion:** the fault line names a bug this test would actually catch. "It calls the function" is not a fault, and a test that duplicates one three files away is not coverage.

Full record, admission checks, RED taxonomy and escalation ladder: [testing.md](references/testing.md).

## 4. Bounded loop

1. **RED** — add one intent group, run it focused and in the foreground. Classify the result: `expected_red`, `invalid_red`, `unexpected_green`, or `verification_infra_failed`.
2. `unexpected_green` means the test does not exercise the change. Fix the test before writing production code; do not implement around it.
3. **GREEN** — implement only enough to satisfy the expected RED. Rerun the same command.
4. **REFACTOR** — improve structure without changing behaviour. Rerun the same command after each step.
5. **Escalate** to broader suites only when evidence requires it: related unit target, then integration/contract, then the full suite.

**Criterion:** you have seen the test fail for the expected reason, then pass, on the same command.

## 5. Bug-fix path

1. **Reproduce** as a failing test, or as the smallest command that shows the wrong output.
2. **Find the root cause** — the first place the wrong value appears, not the last place it surfaces.
3. **Fix it there.** No unrelated reformatting, renames, or drive-by refactors in the same diff; they hide the fix and the reviewer cannot see it.
4. **Keep the test.** It is the regression proof, and it is the only thing that stops the bug coming back.
5. **Check the siblings** — other call sites of the changed function, other handlers of the same event, the mirror endpoint.

**Criterion:** the new test fails on the old code and passes on the new, and the neighbouring tests are still green.

## Non-negotiables

1. Tests assert **observable outcomes and outward effects**, never mock choreography or call order.
2. A test that passed before the change is **not** evidence, and does not count as coverage.
3. No coverage padding, no invented thresholds, no four-pillar scores without measurement.
4. **Every external input validated at the boundary**; **every caught error handled, logged, or rethrown** — never an empty catch.
5. No hardcoded environment values; named constants or config.
6. No debug prints, skipped tests, `TODO` markers, or commented-out code left in the diff.
7. **Report what you did not run.** Unverified is stated plainly, never implied green.

## Finish

Run the real command — the one from step 1 — not a mental check, and not a subset chosen after seeing a failure. Report:

```text
Changed: <files> — <what and why>
Mode: <test-first | regression-first | mechanical>
Verified: <exact command> → <pass/fail counts>
Not verified: <what was not run, and why>
Risk / follow-up: <anything left, or none>
```

## References

| File | Read it for |
|---|---|
| [design-rules.md](references/design-rules.md) | file and function organisation, SOLID where it pays, readability checks |
| [testing.md](references/testing.md) | the intent record, admission checks, RED taxonomy, protocols, F.I.R.S.T. and the three laws |
| [test-anti-patterns.md](references/test-anti-patterns.md) | the eight ways a suite lies to you, and the verification checklist |
| [aaa.md](references/aaa.md) | Arrange-Act-Assert structure, with an example |
| [test-runners.md](references/test-runners.md) | focused test command per language and runner |
| [sources.md](references/sources.md) | provenance and licence |
