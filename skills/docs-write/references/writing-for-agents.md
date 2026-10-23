# Writing documents an agent reads

Condensed from Matt Pocock's `writing-for-agents` skill (MIT, see NOTICE.md). For skills, `AGENTS.md`, `CLAUDE.md`, or any doc reached by a pointer. The packaging differs; the writing does not: the same levers make each one predictable.

## Context pointers
A **context pointer** is a reference held in the agent's context that names out-of-context material and the condition for reaching it. A skill description is one; a line in `AGENTS.md` naming a doc is the same thing. The pointer's wording, not its target, decides when the agent reaches the material. A must-have target behind a weak pointer is a variance bug: sharpen the wording first, inline the material only if that fails.
- State what the material is, then list the distinct **branches** that should trigger reaching it.
- **Front-load the leading word.** One trigger per branch; synonyms that rename one branch are one branch written twice.
- Cut identity the body already carries. An always-loaded pointer costs on every turn, so it earns harder pruning than the body.

## Two loads
- **Context load**: always-loaded text (an `AGENTS.md` line, a skill description) spends tokens and attention every turn whether it fires or not.
- **Cognitive load**: the human is the index; every extra document is one more thing to remember. Spend it where human judgement matters.
Material reached only through a pointer escapes context load at the price of the pointer's line.

## Information hierarchy
1. **In-file step**: what the agent does, in order.
2. **In-file reference**: rules and facts consulted on demand (a flat peer-set is fine).
3. **Disclosed reference**: a separate file behind a pointer, loaded only when the pointer fires.
Inline what every branch needs; push behind a pointer what only some branches reach. Reference buried among steps makes attending to the steps a coin flip. **Co-locate**: keep one concept's definition, rules and caveats under one heading. **Sprawl** is a document too long even when every line is live; cure it by disclosure and by splitting per branch or sequence.

## Steps and completion criteria
Every step ends on a **completion criterion**: the condition that tells the agent it is done.
- **Clarity**: a vague bound ("understanding reached") invites premature completion, because visible later steps pull attention toward being done. Sharpen the bound first; hide later steps by splitting across a real context boundary (a handoff or subagent) only if the criterion is irreducibly fuzzy and you observe the rush.
- **Demand**: "every modified model accounted for" forces more legwork than "produce a change list". The strongest criteria are both checkable and exhaustive.

## When to split
By sequence: when post-completion steps tempt the agent to rush the current one. By invocation: see below. Merging sequences exposes each step to what follows.

## Leading words
A **leading word** is a compact concept already in the model's pretraining that the agent thinks with (_lesson_, _fog of war_, _tracer bullets_, _tight loop_). Used as a token, never a sentence, it anchors a region of behaviour cheaply. Reach for an existing word before coining one; a made-up word recruits no priors. Hunt for triads spelled out at several sites or a pointer spending a sentence on one idea; each collapses into a single word. A word too weak to beat the default (_be thorough_) is a no-op; use a stronger one.

## State the positive
Steering by prohibition drags the forbidden behaviour into context. Write the target ("write one-line comments"), so the banned behaviour is never spoken. Keep a prohibition only as a hard guardrail you cannot phrase positively, and pair it with the positive target.

## Pruning
- **Single source of truth** for every meaning. Duplication costs tokens and inflates prominence.
- The environment (`package.json` scripts, config, directory layout, `--help`) is a source of truth; restating it makes a cache that goes stale. Document what the agent cannot find by looking: the unwritten convention, the reason behind a choice, the gotcha no config confesses.
- Check **relevance** of every line; without pruning discipline the default fate is sediment.
- **No-ops**: an instruction the model already obeys pays load to say nothing. Test whether it changes behaviour versus the default, by running the document. Delete the whole sentence rather than trimming it.

## Invocation (skills)
- **Model-invoked**: keeps a `description` so the agent can fire it itself and other skills can reach it. Permanent context load for discoverability. The description carries the trigger branches.
- **User-invoked** (`disable-model-invocation: true`): only a human typing the name fires it. Zero context load, but you are the index. The description becomes a one-line human summary.
Use model-invocation only when the agent, or another skill, must reach it unprompted. Shared reference two user-invoked skills both need lives in a plain file outside the skill system.
- **Router skill**: when user-invoked skills multiply, one user-invoked skill names the others and when to reach for each, so the human remembers one.
