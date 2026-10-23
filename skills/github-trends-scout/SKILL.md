---
name: github-trends-scout
description: Research trending GitHub repos relevant to Pi workflows, agent engineering, and tools to explore. Use only on explicit command or request.
metadata:
  version: "1.0.0"
  type: "on-demand"
---

# GitHub Trends Scout

Run research across trending and breakout GitHub repositories. Filter for high-impact tools, libraries, and frameworks.

## Trigger & Scope
- Trigger on command `/github-trends-scout` or when explicitly asked: *"What's trending on GitHub?", "Search top repos for Pi."*
- Never auto-trigger during ordinary coding tasks.

## Research Protocol

1. **Query Top & Trending Repos**:
   - Use `web_search` with targeted queries:
     - `site:github.com trending "agent" OR "coding agent" 2026`
     - `site:github.com "pi" OR "tool" OR "workflow" top stars this month`
     - `trending developer tools github this week`
   - Filter out promotional spam, empty forks, or basic prompt lists.

2. **Categorize Findings**:
   Divide output into two clear sections:
   - **Section A: Useful for Pi Ecosystem**:
     - Extensions, MCP servers, prompt compressors, context management, or subagent orchestrators directly integrable into Pi.
   - **Section B: Interesting Beyond Pi**:
     - Standalone developer utilities, desktop tools, local inference runners, or innovative hardware/software projects.

3. **Output Format (Caveman / Terse & Token-Bounded)**:
   For each repository:
   - `[Repo Name] (URL)`: 1-line summary of what it does.
   - `Why useful`: Concrete technical capability.
   - `Actionable note`: How to integrate into Pi or install locally.
   - Cap output to top 5–7 curated items to avoid context bloat.
