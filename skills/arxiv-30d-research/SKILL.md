---
name: arxiv-30d-research
description: Discover high-impact AI research papers published in the last 30 days (arXiv, OpenReview). Use only on explicit command or request.
metadata:
  version: "1.0.0"
  type: "on-demand"
---

# ArXiv 30-Day Research Scout

Search and analyze newly published research papers from the last 30 days focusing on agentic workflows, SLM routing, reasoning, context scaling, and code intelligence.

## Trigger & Scope
- Trigger on command `/arxiv-30d-research` or when asked: *"Find recent AI research papers", "What papers published in the last 30 days?"*
- Papers only: Focus on arXiv, OpenReview, PapersWithCode, and conference preprints.
- Never auto-trigger during standard coding turns.

## Research Protocol

1. **Targeted Search**:
   - Use `web_search` with recency filter set to `month`:
     - `site:arxiv.org "coding agents" OR "agentic workflows" 2026`
     - `site:arxiv.org "model routing" OR "SLM delegation" OR "test-time compute"`
     - `site:openreview.net agentic reasoning or context compression`
   - Use `fetch_content` to read abstracts and key methodology sections.

2. **Curation Filters**:
   - Must be published within the last 30 days.
   - Must present concrete architectural insights or empirical benchmarks, not speculative editorial pieces.

3. **Output Format (Caveman / Terse & Token-Bounded)**:
   For each paper (curate top 3–5 max):
   - `[Title] (arXiv link)`: Authors & publication date.
   - `Core Insight`: What new mechanism or benchmark is proven.
   - `Practical Takeaway for Pi`: How this applies to our local SLMs, decision models, prompt caches, or subagents.
   - `Limitations`: Bounded risks or caveats noted in the paper.
