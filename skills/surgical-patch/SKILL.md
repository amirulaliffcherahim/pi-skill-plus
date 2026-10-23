---
name: surgical-patch
description: Fix bugs and small behavior changes at the narrowest responsible layer, for legacy or high-risk code where scope must stay minimal. Use when regression proof, preserved surrounding behavior, and task-relevant tests matter.
---

# Surgical patch

Reproduce failure first when economical; otherwise capture strongest available evidence.

- Trace symptom to responsible mechanism.
- Change narrowest layer that owns incorrect behavior.
- Preserve unrelated behavior and user changes.
- Avoid cleanup, renaming, and abstraction outside fix.
- Add only regression proof relevant to task.

Run focused proof plus nearest affected gate. Stop when failure is fixed and regression proof passes.
