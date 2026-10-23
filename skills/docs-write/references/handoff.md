# Handoff document

Adapted from Matt Pocock's `handoff` skill (MIT, see NOTICE.md). Compact the current conversation so a fresh agent can continue.

- Save to the OS temp directory (`%TEMP%` on Windows, `$TMPDIR` or `/tmp` elsewhere), **not** the current workspace.
- If the user passed a focus ("what will the next session be used for?"), tailor the document to it.
- Include a **suggested skills** section naming the skills the next agent should load.
- Do not duplicate what other artefacts already hold (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL.
- Cover: the goal, current state, decisions made and why, what is done, what is next, open questions, and what is **unverified**.
- **Redact** secrets and personal data: API keys, passwords, tokens, personal identifiers.
