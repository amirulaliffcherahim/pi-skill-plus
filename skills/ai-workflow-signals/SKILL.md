---
name: ai-workflow-signals
description: Research recent community patterns in AI workflows, looping loops, autonomous setups, and agentic habits. Use only on explicit command or request.
metadata:
  version: "1.0.0"
  type: "on-demand"
---

# AI Workflow Signals

Track how developers, engineers, and AI practitioners are currently designing and running autonomous agent loops, prompt patterns, and coding workflows (past 30 days).

## Trigger & Scope
- Trigger on command `/ai-workflow-signals` or when asked: *"How are people using AI workflows lately?", "What agent loops or patterns are trending?"*
- Focus on real-world engineering practitioner discussions: GitHub discussions, X/Twitter developer threads, Hacker News, Reddit (r/LocalLLaMA, r/MachineLearning), tech blogs.
- Never auto-trigger during standard coding turns.

## Research Protocol

1. **Targeted Search (Last 30 Days)**:
   - Use `web_search` with recency set to `month`:
     - `"agent loop" OR "agentic workflow" architecture developer patterns`
     - `coding agent harness "loop" OR "cascade" best practices 2026`
     - `site:news.ycombinator.com "coding agent" OR "LLM workflow" OR "subagent"`
     - `site:reddit.com/r/LocalLLaMA "agent workflow" OR "routing" OR "decision model"`

2. **Synthesis Themes**:
   Extract practical trends across:
   - **Looping & Feedback Patterns**: How people structure observe -> act -> test -> reflect loops.
   - **Cost & Latency Hacks**: How practitioners avoid runaway API bills (SLM cascades, prompt caching, spec decoding).
   - **Common Pitfalls**: What breaks when people let agents run autonomously.

3. **Output Format (Caveman / Terse & Token-Bounded)**:
   - `Trend / Pattern`: Short title.
   - `How people do it`: Concrete workflow diagram or pseudocode logic.
   - `Why it matters`: What failure it solves or performance it unlocks.
   - `Relevance to Pi`: How we can adapt it in Pi extensions or subagent workflows.
