# PRD / feature spec from the conversation

Adapted from Matt Pocock's `to-spec` skill (MIT, see NOTICE.md). Synthesize what has already been discussed; **do not interview** the user. If a formal SRS is wanted, write this first, then use [srs.md](srs.md) and trace to it.

## Process
1. Explore the repo if you have not: current state, the domain glossary (use its vocabulary throughout), and any ADRs in the area.
2. Sketch the **seams** where the feature will be tested. Prefer existing seams, use the highest seam possible, and propose new ones at the highest point. The fewer seams the better; one is ideal. Confirm them with the user.
3. Write the spec below and publish it where the project keeps specs or issues.

## Template

**Problem statement**: the problem from the user's point of view.

**Solution**: the solution from the user's point of view.

**User stories**: a long, numbered list covering every aspect of the feature, each as `As a <actor>, I want <feature>, so that <benefit>`. Example: "As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending."

**Implementation decisions**: modules built or changed, their interfaces, technical clarifications from the developer, architecture and schema decisions, API contracts, specific interactions. No file paths or code snippets, which go stale fast. Exception: a snippet from a prototype that encodes a decision more precisely than prose (state machine, reducer, schema, type shape); trim it to the decision-rich part and say it came from a prototype.

**Testing decisions**: what makes a good test (external behaviour, not implementation), which modules are tested, and prior art in the codebase.

**Out of scope**: what this spec does not cover.

**Further notes**: anything else.
