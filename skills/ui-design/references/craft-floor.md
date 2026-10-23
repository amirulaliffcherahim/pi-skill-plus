# Craft floor

Condensed from impeccable's craft floor (see NOTICE.md). Run once the direction is settled, as checks on the **built, rendered result** in one batched look. A pinned brief overrides anything here.

## Verify
- **Contrast:** body and placeholder text >= 4.5:1, large text >= 3:1. On coloured surfaces tint secondary text from that hue, never plain grey.
- **Depth:** shadows have offset and soft blur. A zero-offset coloured halo is decoration. Declare elevation once, border or shadow; a 1px border under a wide soft shadow is a ghost card.
- **Spacing:** tight groups, generous separation, more space above a heading than below. Read computed values.
- **Type:** body measure 65-75ch, display max ~6rem, tracking floor -0.04em (-0.02 to -0.03em usually reads better), balanced headings, obvious scale and weight steps. Run real copy at every breakpoint and fix overflow.
- **Motion:** one authored moment, not scattered effects or one identical entrance per section. Ease-out from an already-visible default. Respect `prefers-reduced-motion`.
- **States:** hover, focus, disabled, loading, error, empty. Plus real content, working controls, responsive composition, keyboard focus.
- **Browser surfaces:** theme what you did not draw: text selection, caret, scrollbars, focus rings, underline offset, tabular numerals. Cheapest sign a page was built, not assembled.
- **Copy:** controls name their action; errors name the problem and the recovery.
- **Coverage:** every brief requirement present and findable within seconds.

## Refuse by default
Defaults of the category, not hard bans: the brief's own words can earn any of them. Reaching for one when the axis is free means you were not deciding.

Scaffolds
- Same-size cards of icon + heading + text as the page structure; nested cards.
- The hero-metric template (big number, small label, supporting stats, accent).
- An eyebrow/kicker above a heading, and section numbers (01/02/03) unless the sequence carries information.
- A modal for a task that needs neither interruption nor protected focus.

Surface
- Gradient text (use weight or size for emphasis).
- Glass/blur as decoration rather than a specific effect.
- Coloured `border-left`/`border-right` over 1px on cards, list items, callouts or alerts.
- Hard offset shadows (`4px 4px 0`) outside a genuinely neobrutalist world.
- Sparklines, progress rings and soft rounded rectangles standing in for content.
- Monospace as a costume for "technical" instead of for code, data or measurement.
- Unicode glyphs or emoji as an icon system. Use one real icon set or authored SVG at one stroke weight.
- Geometric masks faking organic contours; derive a real matte or omit.
- Sketch-style SVG scenes and `feTurbulence` grain pretending to be illustration. SVG doing geometry (diagrams, shapes, linework) is fine.
- Stripe or grid-overlay backgrounds with nothing under them that justifies them.
- Light/dark chosen by category instead of use scene.
- A system display face as the display voice of a Persuade/Experience page. Operate and Read surfaces may use reliable system or neutral sans fonts.
- Inventing claims or configuration; label illustrative values.

When every check is green, spend the page on the committed direction. When torn between refined and committed in Persuade/Experience, commit.
