---
name: ui-design
description: Design, build, redesign, review or polish user interfaces - web pages, landing pages, dashboards, app screens, components, forms, docs sites, CSS/layout/typography/color/motion, accessibility and responsive behavior. Includes Apple Human Interface Guidelines for iOS/macOS/visionOS UI or an Apple-like feel. Use before writing or judging any UI code or styling. Not for backend or non-visual work.
---
# UI Design

Applies to anything that changes how an interface **looks, feels, moves or is used**. Skip for pure logic.

## 1. Settle the brief (before any code)

- **The brief wins.** Fonts, palette, era, brand or style the user named beat every default below. Never steer a clear brief toward your own taste.
- **Refine vs redesign.** Refine = keep identity, copy, behavior and everything outside scope; change only what was asked. Redesign = keep product truth, content and function, treat the old look as evidence, pick a replacement direction and commit. Never split the difference.
- Resolve who uses it, for what job, and on what device from the conversation and repo before asking. Ask only when the answer would change the design.
- Existing design system, tokens, components or `DESIGN.md`/`PRODUCT.md` in the repo outrank this skill. Read them first.
- **Apple platform targets** (iOS, iPadOS, macOS, watchOS, visionOS, or a brief asking for an Apple feel): follow [apple-hig.md](references/apple-hig.md). The platform conventions outrank any expressive direction here.

## 2. Pick the mode (from the surface, not the product)

| Mode | Visitor's success | Surfaces | Rule |
|---|---|---|---|
| **Operate** | finishes a task | app UI, dashboards, editors, admin, settings | Scanability, standard controls, consistency. Expression only via type, palette, density, one signature detail |
| **Read** | understands something | docs, articles, guides, changelogs | Calm column, 60-75ch, real contrast. World lives in the frame, not behind the text |
| **Persuade** | decides and acts | landing, marketing, pricing | Commit to a distinct direction. Offer and primary action clear in the first view |
| **Experience** | is inside the work | portfolio, gallery, showcase | The artifact leads; the interface recedes |

A tool's landing page is Persuade; a fashion house's docs are Read. Details: [references/modes.md](references/modes.md).

## 3. Direction

- **Persuade/Experience:** commit to one tone (see [tones.md](references/tones.md)) and one memorable thing. A distinctive display face, a dominant color with a sharp accent, one orchestrated entrance. Intentional, not intense: refined minimal and bold maximal both work.
- **Operate/Read:** restraint is the ambition. A clean grid, real type scale, standard controls and states beat decoration. A reliable sans (including Inter or system fonts) is fine here. A grey screen with one accent is still a choice: give the shell a committed palette.
- Never pick light or dark by category; pick from who uses it and under what light.
- On Apple platforms, the platform's own patterns, controls, type styles and materials come first; brand lives in content and accent.
- Do not repeat one aesthetic across projects: vary tone, type and theme.

## 4. Priority order when rules conflict

1 Accessibility (contrast 4.5:1, keyboard, labels, focus, reduced motion) > 2 Touch/interaction (44px targets, feedback) > 3 Performance (reserve space, lazy-load, CLS) > 4 Style fit > 5 Layout/responsive (mobile-first, no horizontal scroll) > 6 Type/color tokens > 7 Motion > 8 Forms (visible labels, errors by the field) > 9 Navigation > 10 Charts (never color alone).

Never remove focus rings, ship icon-only buttons without labels, disable zoom, or use emoji as icons.

## 5. Build

- Tokens first: CSS custom properties for color, type, space, radius, motion. No raw hex inside components.
- Type: body 16px+, line-height ~1.5, measure 65-75ch, balanced headings. Self-host fonts (`@font-face`, `next/font`), no CDN `<link>` in production.
- Motion: one authored moment beats ten effects. Ease-out, 200-600ms, honor `prefers-reduced-motion`. See [motion.md](references/motion.md).
- Real content in real states: hover, focus, disabled, loading, error, empty. No lorem or placeholder tiles.
- Follow [craft-floor.md](references/craft-floor.md) before calling any UI done, including small edits.

## 6. Verify by looking

Render at the sizes it ships at (mobile + desktop) and fix everything one look shows before looking again. Use the `playwright` skill/tool when a browser is available. If you cannot render, say so and list what is unchecked. Never claim a UI works from reading CSS.

## 7. Look things up (do not preload)

- Specific rule to check (a11y, performance, HTML, CSS, images): [checklist-index.md](references/checklist-index.md), one line per rule with its upstream page.
- Studying how a known brand structures a design system: [brands.md](references/brands.md). Learn structure and token organization; never copy a brand's identity, logo or trademarks.

## References

[apple-hig.md](references/apple-hig.md) - Apple HIG foundations (native targets) | [modes.md](references/modes.md) - mode playbooks | [craft-floor.md](references/craft-floor.md) - done-checks and defaults to refuse | [tones.md](references/tones.md) - tone + fonts (Persuade/Experience) | [motion.md](references/motion.md) | [checklist-index.md](references/checklist-index.md) | [brands.md](references/brands.md)

Sources and licences: [NOTICE.md](NOTICE.md).
