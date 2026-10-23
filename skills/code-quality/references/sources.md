# Sources

## Provenance

Both merged skills descend from [agent-skills-standard](https://github.com/HoangNguyen0403/agent-skills-standard) (MIT, © 2026 Hoang Nguyen), previously shipped here as `common-best-practices` and `common-tdd`. The MIT notice is retained in `LICENSE` because both licences require it to travel with substantial portions of the work.

- **Design rules** came from `common-best-practices` (`references/CODE_STRUCTURE.md`, `references/EFFECTIVENESS.md`), concatenated into [design-rules.md](design-rules.md) with the text unchanged and only heading levels adjusted to fit under one title.
- **Testing** came from `common-tdd` (`quality-contract.md`, `tdd_patterns.md`, `best-practices.md`), merged into [testing.md](testing.md). Headings were adjusted; wording was not.
- **Anti-patterns** came from `common-tdd` (`testing_anti_patterns.md`, plus two unique items from `anti-patterns.md`), merged into [test-anti-patterns.md](test-anti-patterns.md).
- [aaa.md](aaa.md) and [test-runners.md](test-runners.md) are carried from `common-tdd` unchanged.

## What was deduplicated in the merge

The two `common-tdd` references overlapped substantially, so the merge dropped rather than concatenated:

- Two near-identical anti-pattern lists became one; the surviving file keeps the seven shared pitfalls, adds *Integration tests as an afterthought* and *Layer mismatch*, and keeps the original verification checklist.
- F.I.R.S.T. appeared in both `tdd_patterns.md` and `best-practices.md`; the fuller version in `best-practices.md` survives.
- Arrange-Act-Assert appeared in three places; it now lives only in [aaa.md](aaa.md), with the other two mentions removed.

Nothing else was changed; the surviving text is the upstream text.

## Upstream claims worth knowing

`best-practices.md` credits "Graphite, dev.to, et al." for its content rather than a specific source. Treat its rules as conventional practice rather than as citations of a study — the claims that matter here (F.I.R.S.T., three laws of TDD, AAA) are long-standing and uncontroversial, and none of them are stated as measured results.
