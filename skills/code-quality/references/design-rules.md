# Design Rules

Structure and readability rules for production code. Read when shaping a change or reviewing one.

## Naming & Structure Reference

Example of expressive, modular code following the high-density standards.

### 🏷 Variable & Method Naming

```typescript
// BAD: Generic or cryptic
const data = await get();
let flag = false;

// GOOD: Expressive and context-aware
const userData = await fetchUserAccount();
let isUserAuthenticated = false;
```

### 💂 Guard Clauses (Expressive Logic)

```typescript
// BAD: Nested indentation (Pyramid of Doom)
function processOrder(order) {
  if (order != null) {
    if (order.isValid) {
      if (order.total > 0) {
        // ... logic
      }
    }
  }
}

// GOOD: Early returns (High Density)
function processOrder(order) {
  if (!order || !order.isValid) return;
  if (order.total <= 0) return;

  // Clear path for core business logic
}
```

### 📦 Modular Design (SOLID)

```typescript
// Single Responsibility Principle
class UserProfile {
  // Handles only user data
}

class UserRepository {
  // Handles only persistence
}

class AuthService {
  // Handles only authentication
}
```

## Skill Effectiveness & Token Economy Verification

This document outlines the rationale and verified impact of the "High-Density" standard applied to these skills.

### 📈 Token Density Comparison

| Format                        | Avg. Tokens per Rule | Context Efficiency                |
| :---------------------------- | :------------------- | :-------------------------------- |
| **Traditional Documentation** | 150 - 300            | Low (conversational / redundant)  |
| **High-Density (SKILL.md)**   | 10 - 25              | **Critical (4-10x optimization)** |

### ✅ Verified Benefits

1. **Reduced Latency**: By stripping articles ("a", "the") and conversational fluff, the LLM processes context faster.
2. **Lower Cost**: Fewer tokens consumed per query result in significant cost savings for long-running agent sessions.
3. **Instruction Following**: LLMs are more likely to follow imperative, bulleted instructions than long-form prose.
4. **Context Window Safety**: Allows loading multiple specialized skills (Flutter, Dart, Security, Git) simultaneously without hitting token limits.

### 🛠 Strategic Separation

- **Core (SKILL.md)**: 100% actionable rules. Loaded into active memory.
- **References (references/)**: Heavy examples. Only read by the agent when deep exploration is required.

### 🧬 Digital DNA Principles

- **Delete > Comment**: Minimizes noise.
- **Imperative Mood**: Direct mapping to LLM instruction-tuning.
- **Structural Triggers**: Automated activation ensures only relevant skills consume tokens.
