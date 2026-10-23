# Style and truth rules

Condensed from riekelt/technical-writer's `technical-writing`, `truth.md`, `style.md` (MIT, see NOTICE.md). These bind running prose in technical documents, not quoted material, code blocks, schemas, or an example that discusses a banned phrase.

## Truth and sourcing
- Every load-bearing claim traces to a source stated in the document: a `file:line`, a pinned commit, a test, a query, a primary source. If a claim is unbacked, say so. "I read this from empty files" beats a confident guess.
- Facts given without sources: use them and mark `**[source wanted: <what, from whom>]**`. Never invent a citation, never block.
- **One section owns each number**; others cite it. Print the command behind a count and run it on committed state (HEAD), not the working tree. Say when it was checked.
- Third-party behaviour is perishable (versions, prices, limits, model behaviour): date it once, next to the claim.
- Distinguish **written** (in the repo), **shipped** (live), **externally verified**. "Verified" always names what was checked, never a bare checkmark.
- Keep hypotheses labelled as hypotheses. Label an estimate and what it depends on. Carry known weaknesses forward. Name the role or the process failure, never a person.
- Where a document mixes evidence grades, define tiers: **Measured** (reproduced from a named script), **Sourced** (named primary source), **Estimated** (judgement, with its dependencies).
- A document that requires approval keeps an append-only dated sign-off log (`YYYY-MM-DD <reviewer>: approved <scope>`); content newer than the last sign-off counts as unreviewed.

## Keeping documents true
Update in the same change as the code. Sweep every surface that states a changed fact. Correct visibly. Superseded documents get a banner, not deletion. Indexes are derived: rebuild them from the files and verify counts. A descriptive document names the code it describes (a path) so drift has an anchor. Diagrams are source-controlled text; delete stale renders. Tense matches status: a dormant system cannot take the present tense. When auditing, count documented items against total public items instead of judging by impression.

## Sentences and words
- One claim per sentence; about 20 words on average, 35 at most. Procedures: one action per sentence, imperative, visible actor.
- Active voice, named actor. Give agency only to what acted: a diagram does not "prove", an architecture does not "decide".
- Vary length; merge runs of three short sentences. Do not start three sentences in a row with the same subject. Keep articles. No noun stacks over three words.
- A number instead of an adjective ("140 keys", not "many keys"). One term per concept all the way through; more than five defined terms means a glossary.
- Plain verbs: "is" and "has", not "serves as" or "boasts"; "test", not "exercise".
- Concrete over abstract: a version number beats "recent releases", a named failure mode beats "issues". Metaphor only where it explains what the literal cannot.
- **Read-aloud rule**: rewrite whatever you would not say to a colleague. **Remove-the-name test**: delete the product name; if the text is still equally true of any product, it carries no information.

## Headings
Sentence case. Name the content: a noun phrase by default, an imperative above a procedure, a verbatim symptom for troubleshooting, a question only in a real FAQ. A heading states the finding and never promises a reveal; the first sentence under it does not repeat it.

## Banned constructions (and the repair)
| Pattern | Repair |
|---|---|
| Antithesis: "not X, but Y"; "less X than Y" | State the positive claim |
| Meaning sentence closing a section ("That distinction matters") | Delete; end on the last fact |
| Manufactured insight ("what nobody tells you", "the part most people miss") | State the point without announcing it |
| Importance announcement ("it is important to note", "the key takeaway") | State the consequence |
| Recap ("Overall", "In conclusion") and restatement for emphasis | End on the last fact; keep the better sentence |
| Rhetorical triad ("faster, safer, more predictable") | The one measured claim, or a different count |
| Throat-clearing ("this document will explore", "in order to") | Start with the subject |
| Filler ("essentially", "basically", "in practice", "note that") | Delete |
| Inflated or promotional words (robust, seamless, comprehensive, cutting-edge, game-changing) | A number, a named property, or nothing |
| AI vocabulary (delve, tapestry, pivotal, underscore, foster, leverage, unlock, realm, nuanced, holistic) | The plain word |
| Trailing participle ("..., highlighting the need for") | Delete the tail |
| Stacked hedging, vague attribution ("experts say") | One qualifier, or name the source |
| Bold-lead bullets repeated down a list; emoji as bullets | Subsections, or parallel plain items |
| Assistant or production residue ("here is an overview", "as requested", "unlike the previous version", leaked reasoning) | Delete; documents end on content |

Formatting reveals structure already present; it never supplies importance. Use a table only when items carry two or more properties and a reader compares across them. No heading above every paragraph. Specifications and required review formats keep their structural Markdown; these rules never flatten a document whose schema carries evidence.

## Hard rules
- **No em or en dashes and no ` -- `** in running prose; use commas, colons, parentheses, or a spaced hyphen. A plain hyphen serves ranges.
- **No changelog section and no "last updated" field inside a document**; version history belongs to Git, or to the changelog document type.
- **No delivery-history narrative** (phases, task IDs, ticket keys, SHAs) in prose or code comments. A pinned commit may appear solely as claim evidence.
- **One fact, one home.** An index may route but never decide; when an index and its source disagree, the source wins.
- **Accepted decisions and applied migrations are immutable.** Corrections are new dated entries.

An author's stated style choice outranks the style preferences here (not the truth, safety and history rules). When the author says to leave their voice alone, the style pass stops.

## Final pass (reviewing any document)
Follow every reference, run every command, check every ID and path. Confirm there is no unmarked placeholder, no unverified claim stated as fact, and no section that restates another. Edits to someone else's document are surgical: preserve their voice, structure, numbering and IDs.
