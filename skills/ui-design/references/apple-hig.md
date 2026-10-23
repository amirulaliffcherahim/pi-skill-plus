# Apple Human Interface Guidelines - foundations summary

Reference for building or reviewing **Apple-platform UI** (iOS, iPadOS, macOS, watchOS, visionOS) and for any interface where the brief asks for an Apple-like feel.

Source: Apple Human Interface Guidelines, <https://developer.apple.com/design/human-interface-guidelines/foundations>. This is a condensed summary in this skill's own words, not a reproduction of Apple's text. Apple's pages are the authority, and they change; read the linked page when exact wording or a new platform matters. Apple's own docs, SF Symbols, system colours and typefaces are Apple property; do not copy Apple artwork, icons or marketing.

## The 8 design principles

Apple frames these as tools for weighing competing priorities, not a checklist.

| Principle | Meaning for the build |
|---|---|
| **Purpose** | Design starts with intention. Name what the product is for and whether each screen serves it. Cut features that don't. |
| **Agency** | Let people act their own way: no dead-end flows, escape hatches from guided flows, undo rather than confirmations everywhere. |
| **Responsibility** | Act in the user's interest: say why a permission is needed, collect only what is required, protect the data. |
| **Familiarity** | Build on what people know. Use platform patterns and conventions consistently; consistent behaviour teaches faster than novelty. |
| **Flexibility** | Adapt to devices, input methods (touch, keyboard, pointer, voice), text sizes and perspectives. Accessibility is a requirement from the start, not a pass at the end. |
| **Simplicity** | Simplicity is not minimalism: keep what matters close, let the rest fall away, and write the fewest words that say the thing. |
| **Craft** | Every detail is a decision. Prefer polish over volume, iterate, and test on the real device. |
| **Delight** | Design for a feeling (calm, energising, playful), add character in small moments, and never let delight obstruct the task. |

## Foundations that change the code

**Layout**
- Respect safe areas: do not put primary content under the notch, Dynamic Island, home indicator, toolbars or tab bars.
- Align consistently and use indentation for hierarchy. Inconsistent spacing stops reading as a grid.
- Layout must adapt across rotations, window resizes, split view and external displays, not just "fit at one size".
- Interactive targets: about **44x44 pt** minimum for touch.

**Typography**
- Meet the platform's legibility minimums rather than shrinking text to fit; test at real viewing distance.
- Avoid very light weights (Ultralight/Thin/Light) for body text: use Regular/Medium/Semibold/Bold.
- Use text styles and support **Dynamic Type**: text must grow with the user's size setting without clipping or overlap. Prefer wrapping and reflow over truncation, and test the largest accessibility sizes.
- Custom fonts must stay legible, support Dynamic Type and honour Bold Text.

**Colour**
- Prefer semantic/dynamic system colours: they adapt to light, dark and Increased Contrast automatically, and keep their meaning.
- Check every colour pair in light, dark and increased-contrast appearances, and in real ambient light (sunlight, dim rooms).
- **Never use colour as the only signal** for state, interactivity or meaning; add shape, text, icon or position.
- Contrast minimum (HIG): **4.5:1** for text up to 17 pt, **3:1** for 18 pt+ or bold text.

**Dark Mode**
- Provide both appearances unless there is a product reason not to. Don't just invert: test images, materials, elevation and shadows in each.

**Motion**
- Motion should explain a change (where something came from, where it went), not decorate.
- Honour **Reduce Motion** by substituting a cross-fade or an instant state change for large movement.
- Be cautious with fast, repeating or blinking animation: it distracts and can trigger vestibular symptoms or photosensitivity.

**Accessibility (baseline)**
- Every control needs an accessible label and a sensible reading order; icon-only buttons need names.
- Support VoiceOver, Voice Control, Full Keyboard Access and Switch Control: focus order, visible focus, and no interaction that requires precision gestures alone.
- Support larger text, Increased Contrast and bold text without breaking layout.

**Materials, icons, branding**
- Prefer system materials (blur/translucency) for chrome so content stays legible behind it; every text layer on glass needs its own contrast.
- Use SF Symbols or one authored icon set at consistent weight and optical size. Don't mix symbol families, and don't use emoji as an icon system.
- Branding belongs in content and accent, not in restyling controls the user already knows.

## Applying this on the web
These rules transfer well even when the target is a browser: safe-area insets (`env(safe-area-inset-*)`), 44px touch targets, Dynamic-Type-style fluid type with a user-adjustable base size, semantic colours with light/dark variants, `prefers-reduced-motion`, `prefers-contrast`, visible focus, and colour never used alone. Where HTML and HIG disagree (e.g. raw `pt` sizes), follow the platform.

## Related pages
- Foundations index: <https://developer.apple.com/design/human-interface-guidelines/foundations>
- Design principles: <https://developer.apple.com/design/human-interface-guidelines/design-principles>
- Accessibility: <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- Colour / Typography / Layout / Motion / Dark Mode / Materials: append the page name to the foundations URL.
- Platform specifics: `/design/human-interface-guidelines/designing-for-ios`, `-ipados`, `-macos`, `-watchos`, `-visionos`.
