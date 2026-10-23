# pi-skill-plus

Twelve skills for the [Pi coding agent](https://github.com/earendil-works/pi), written and maintained here. Each one is a directory with a `SKILL.md` (frontmatter + routing description) and, where the topic needs depth, a `references/` set that is only loaded when the skill fires.

## What's inside

| Skill | Fires when |
|---|---|
| `code-quality` | implementing a feature, writing/changing a function, refactoring, fixing a bug |
| `system-design` | choosing components/storage, designing or versioning endpoints, modelling tables and indexes, migrating, reviewing a design |
| `zeroday-compliance` | before a first production deploy or public launch, masking PII, security/pentest review, SOC 2 / GDPR / PDPA prep |
| `surgical-patch` | minimal-diff fix in legacy or high-risk code, regression proof |
| `verify-and-stop` | proving existing work meets acceptance, no scope creep |
| `docs-write` | SRS, SDS, PRD, ADR, test plan, README, API docs, prose, docs an agent reads |
| `ui-design` | building, redesigning or reviewing a UI; layout, type, colour, motion, a11y, Apple HIG |
| `diagram-design` | any diagram as HTML/SVG/PNG, plus drawio / Mermaid / Excalidraw import |
| `reverse-engineer` | Ghidra + REA on native, .NET, Electron, Android, firmware, packaged, browser targets |
| `ai-workflow-signals` | explicit request only — community agent-workflow patterns |
| `arxiv-30d-research` | explicit request only — last 30 days of AI papers |
| `github-trends-scout` | explicit request only — trending repos |

Three skills were each built by merging narrower predecessors; every one of them carries the merged material rather than a stub:

- `code-quality` ← best-practices + TDD
- `system-design` ← API design + database design
- `zeroday-compliance` ← compliance + privacy/PII + security audit

## Install

Portable skills (shared by any agent that reads `~/.agents/skills`):

```bash
cp -r skills/* ~/.agents/skills/
```

Or keep this checkout as the source of truth and symlink:

```bash
ln -s "$PWD/skills/code-quality" ~/.agents/skills/code-quality
```

Pi-local skills (only Pi, at `~/.pi/agent/skills`) work the same way with that path instead. Pi discovers any directory containing a `SKILL.md`, recursively, so pointing it at a subdirectory works too.

Then `/reload` in a running session, or start a new one. Each skill is advertised by its `description` only — the body and references stay out of context until the task matches.

## Layout

```text
skills/
  <name>/SKILL.md              frontmatter (name, description) + the instructions
  <name>/references/*.md       depth, loaded on demand
  <name>/scripts/              deterministic helpers, where a script beats prose
  <name>/LICENSE               upstream notice, where the skill derived from one
reference.txt                  inventory: every skill, extension and upstream repo
THIRD-PARTY.md                 attribution for derived material
```

## Notes on the skills themselves

- `zeroday-compliance` is a gate, not a checklist to skim: items are tagged BLOCK / HOLD / ADVICE, and a single BLOCK fails the launch regardless of how many passes surround it. Legal figures there are dated and change — re-check the ones that decide money or a launch date.
- `code-quality` gates test-first work — new behaviour and regression risk get a failing test first; a mechanical edit (rename, format, config value) gets the existing suite and no new test. The gate has an escape rule: any observable behaviour change is not mechanical.
- `system-design` presents the two strict API rule sets (Zalando-style, Azure-style) as coherent bundles and requires picking one, because mixing them is what produces an unpredictable API.
- `diagram-design` carries its own assets (icons, example HTML) and its own `THIRD_PARTY_LICENSES.md`.

## Licence

Our original content is MIT — see `LICENSE`. Derived skills keep their upstream notices in the relevant `LICENSE` file and are attributed in [THIRD-PARTY.md](THIRD-PARTY.md). Some Apache-2.0 material is redistributed inside `zeroday-compliance`; that notice travels with it.

Not legal advice, not a penetration test, not an audit. The skills say so themselves.
