# Front-end checklist index

One line per rule: `priority` name - what to do. Full rule text and examples at the URL (fetch only the rule you need). Covers accessibility, HTML, CSS, images, performance and JavaScript rules rated critical or high. Source: thedaviddias/Front-End-Checklist (MIT), see NOTICE.md.

## accessibility (34)

- `critical` **aria-hidden-body** - Do not use aria-hidden on the document body <https://frontendchecklist.io/rules/accessibility/aria-hidden-body>
- `critical` **aria-input-field-name** - Ensure all input fields have accessible names <https://frontendchecklist.io/rules/accessibility/aria-input-field-name>
- `critical` **button-name** - Provide accessible names for buttons <https://frontendchecklist.io/rules/accessibility/button-name>
- `critical` **flashing-content** - Prevent seizure-triggering flashing content <https://frontendchecklist.io/rules/accessibility/flashing-content>
- `critical` **form-labels** - Associate labels with form controls <https://frontendchecklist.io/rules/accessibility/form-labels>
- `critical` **heading-hierarchy** - Use logical heading hierarchy <https://frontendchecklist.io/rules/accessibility/heading-hierarchy>
- `critical` **input-image-alt** - Provide alt text for image buttons <https://frontendchecklist.io/rules/accessibility/input-image-alt>
- `critical` **keyboard-navigation** - Enable keyboard navigation for all elements <https://frontendchecklist.io/rules/accessibility/keyboard-navigation>
- `critical` **zoom-reflow** - Support content reflow at 400% zoom <https://frontendchecklist.io/rules/accessibility/zoom-reflow>
- `high` **accessible-authentication** - Provide accessible authentication methods <https://frontendchecklist.io/rules/accessibility/accessible-authentication>
- `high` **aria-labels** - Provide accessible names for all interactive elements <https://frontendchecklist.io/rules/accessibility/aria-labels>
- `high` **aria-live-regions** - Announce dynamic content with ARIA live regions <https://frontendchecklist.io/rules/accessibility/aria-live-regions>
- `high` **aria-required-children** - Ensure ARIA roles contain required child roles <https://frontendchecklist.io/rules/accessibility/aria-required-children>
- `high` **aria-valid-attr** - Ensure ARIA attributes are valid <https://frontendchecklist.io/rules/accessibility/aria-valid-attr>
- `high` **autoplay-media** - Avoid autoplaying media <https://frontendchecklist.io/rules/accessibility/autoplay-media>
- `high` **color-contrast** - Meet minimum color contrast ratios <https://frontendchecklist.io/rules/accessibility/color-contrast>
- `high` **content-without-css** - Ensure content remains usable without CSS <https://frontendchecklist.io/rules/accessibility/content-without-css>
- `high` **duplicate-id-active** - Use unique IDs for active elements <https://frontendchecklist.io/rules/accessibility/duplicate-id-active>
- `high` **duplicate-id-aria** - Use unique IDs for ARIA references <https://frontendchecklist.io/rules/accessibility/duplicate-id-aria>
- `high` **focus-management** - Manage focus during dynamic interactions <https://frontendchecklist.io/rules/accessibility/focus-management>
- `high` **focus-not-obscured** - Keep focused elements unobscured <https://frontendchecklist.io/rules/accessibility/focus-not-obscured>
- `high` **focus-order** - Ensure logical focus order <https://frontendchecklist.io/rules/accessibility/focus-order>
- `high` **link-text** - Use descriptive link text <https://frontendchecklist.io/rules/accessibility/link-text>
- `high` **modal-accessibility** - Make modal dialogs keyboard accessible <https://frontendchecklist.io/rules/accessibility/modal-accessibility>
- `high` **orientation** - Support both portrait and landscape orientation <https://frontendchecklist.io/rules/accessibility/orientation>
- `high` **reduced-motion** - Respect reduced motion preferences <https://frontendchecklist.io/rules/accessibility/reduced-motion>
- `high` **redundant-entry** - Avoid redundant entry in the same process <https://frontendchecklist.io/rules/accessibility/redundant-entry>
- `high` **screen-reader-testing** - Test with screen readers <https://frontendchecklist.io/rules/accessibility/screen-reader-testing>
- `high` **sensory-instructions** - Avoid sensory-only instructions <https://frontendchecklist.io/rules/accessibility/sensory-instructions>
- `high` **session-timeout-recovery** - Prevent data loss from session timeouts <https://frontendchecklist.io/rules/accessibility/session-timeout-recovery>
- `high` **skip-navigation** - Include a skip navigation link <https://frontendchecklist.io/rules/accessibility/skip-navigation>
- `high` **text-resizing** - Support text resizing to 200% <https://frontendchecklist.io/rules/accessibility/text-resizing>
- `high` **video-captions** - Provide captions for video content <https://frontendchecklist.io/rules/accessibility/video-captions>
- `high` **viewport-zoom** - Do not disable pinch zoom <https://frontendchecklist.io/rules/accessibility/viewport-zoom>

## css (10)

- `high` **animation-performance** - Use transform and opacity for animations <https://frontendchecklist.io/rules/css/animation-performance>
- `high` **css-critical** - Inline critical CSS for faster rendering <https://frontendchecklist.io/rules/css/css-critical>
- `high` **css-custom-properties** - Use CSS custom properties for design tokens <https://frontendchecklist.io/rules/css/css-custom-properties>
- `high` **css-minification** - Minify all CSS files <https://frontendchecklist.io/rules/css/css-minification>
- `high` **css-non-blocking** - Load CSS without blocking render <https://frontendchecklist.io/rules/css/css-non-blocking>
- `high` **embedded-or-inline-css** - Avoid embedded and inline CSS <https://frontendchecklist.io/rules/css/embedded-or-inline-css>
- `high` **focus-styles** - Provide visible custom focus indicators <https://frontendchecklist.io/rules/css/focus-styles>
- `high` **responsive-units** - Use relative units for responsive layouts <https://frontendchecklist.io/rules/css/responsive-units>
- `high` **specificity-management** - Keep CSS specificity low and flat <https://frontendchecklist.io/rules/css/specificity-management>
- `high` **unused-css** - Remove unused CSS rules <https://frontendchecklist.io/rules/css/unused-css>

## html (16)

- `critical` **charset** - Declare UTF-8 character encoding <https://frontendchecklist.io/rules/html/charset>
- `critical` **doctype** - Use the HTML5 doctype <https://frontendchecklist.io/rules/html/doctype>
- `critical` **viewport** - Set the responsive viewport meta tag <https://frontendchecklist.io/rules/html/viewport>
- `high` **accessible-notifications** - Make notifications accessible <https://frontendchecklist.io/rules/html/accessible-notifications>
- `high` **defer-async** - Load scripts with defer, async, or type=module <https://frontendchecklist.io/rules/html/defer-async>
- `high` **form-validation** - Validate forms accessibly <https://frontendchecklist.io/rules/html/form-validation>
- `high` **html5-semantic-elements** - Use semantic HTML elements <https://frontendchecklist.io/rules/html/html5-semantic-elements>
- `high` **html-resource-hints** - Add resource hints (preload, prefetch, dns-prefetch) <https://frontendchecklist.io/en/rules/html/html-resource-hints>
- `high` **input-types** - Use semantic input type attributes <https://frontendchecklist.io/rules/html/input-types>
- `high` **lang-attribute** - Set the page lang attribute <https://frontendchecklist.io/rules/html/lang-attribute>
- `high` **navigation-landmark** - Use navigation landmark regions <https://frontendchecklist.io/rules/html/navigation-landmark>
- `high` **subresource-integrity** - Add Subresource Integrity to external scripts <https://frontendchecklist.io/rules/html/subresource-integrity>
- `high` **unique-id** - Ensure all IDs are unique <https://frontendchecklist.io/rules/html/unique-id>
- `high` **video-accessibility** - Make videos accessible with captions <https://frontendchecklist.io/rules/html/video-accessibility>
- `high` **w3c-compliant** - Validate HTML against W3C standards <https://frontendchecklist.io/rules/html/w3c-compliant>
- `high` **webpagetest** - Analyze performance with WebPageTest <https://frontendchecklist.io/rules/html/webpagetest>

## images (16)

- `critical` **alt-text** - Provide meaningful alt text for images <https://frontendchecklist.io/rules/images/alt-text>
- `high` **broken-images** - Fix broken images <https://frontendchecklist.io/rules/images/broken-images>
- `high` **critical-images** - Prioritize loading critical images <https://frontendchecklist.io/rules/images/critical-images>
- `high` **dimensions** - Set explicit width and height on images <https://frontendchecklist.io/rules/images/dimensions>
- `high` **image-cdn** - Serve images from a CDN <https://frontendchecklist.io/rules/images/image-cdn>
- `high` **image-compression** - Compress images without quality loss <https://frontendchecklist.io/rules/images/image-compression>
- `high` **image-file-size** - Keep image file sizes within recommended limits <https://frontendchecklist.io/rules/images/image-file-size>
- `high` **image-optimization** - Optimize all images for web <https://frontendchecklist.io/rules/images/image-optimization>
- `high` **modern-format** - Use modern image formats (WebP, AVIF) <https://frontendchecklist.io/rules/images/modern-format>
- `high` **offscreen-lazy** - Lazy load offscreen images <https://frontendchecklist.io/rules/images/offscreen-lazy>
- `high` **optimized** - Optimise images for faster loading <https://frontendchecklist.io/rules/images/optimized>
- `high` **picture-element** - Use <picture> with an <img> fallback <https://frontendchecklist.io/rules/images/picture-element>
- `high` **responsive-images** - Implement responsive images with srcset <https://frontendchecklist.io/rules/images/responsive-images>
- `high` **responsive-size** - Serve images at the correct display size <https://frontendchecklist.io/rules/images/responsive-size>
- `high` **srcset** - Use srcset for responsive images <https://frontendchecklist.io/rules/images/srcset>
- `high` **webp-format** - Use WebP format with fallbacks <https://frontendchecklist.io/rules/images/webp-format>

## javascript (13)

- `critical` **avoid-eval** - Never use eval() or unsafe dynamic code execution <https://frontendchecklist.io/rules/javascript/avoid-eval>
- `high` **code-splitting** - Split large JavaScript bundles <https://frontendchecklist.io/rules/javascript/code-splitting>
- `high` **const-let** - Prefer const and let over var <https://frontendchecklist.io/rules/javascript/const-let>
- `high` **cross-origin-security** - Handle cross-origin requests securely <https://frontendchecklist.io/rules/javascript/cross-origin-security>
- `high` **debounce-throttle** - Debounce and throttle event handlers <https://frontendchecklist.io/rules/javascript/debounce-throttle>
- `high` **dom-performance** - Minimize costly DOM read/write operations <https://frontendchecklist.io/rules/javascript/dom-performance>
- `high` **error-handling** - Implement proper error handling <https://frontendchecklist.io/rules/javascript/error-handling>
- `high` **es-modules** - Use ES modules (import/export) <https://frontendchecklist.io/rules/javascript/es-modules>
- `high` **javascript-inline** - Avoid inline JavaScript <https://frontendchecklist.io/rules/javascript/javascript-inline>
- `high` **javascript-minification** - Minify all JavaScript files <https://frontendchecklist.io/rules/javascript/javascript-minification>
- `high` **memory-leaks** - Prevent common memory leak patterns <https://frontendchecklist.io/rules/javascript/memory-leaks>
- `high` **runtime-validation** - Validate external data at runtime with a schema library <https://frontendchecklist.io/rules/javascript/runtime-validation>
- `high` **typescript-strict-mode** - Enable TypeScript strict mode in tsconfig.json <https://frontendchecklist.io/rules/javascript/typescript-strict-mode>

## performance (24)

- `critical` **largest-contentful-paint** - Optimize largest contentful paint <https://frontendchecklist.io/rules/performance/largest-contentful-paint>
- `high` **back-forward-cache** - Optimize pages for back/forward cache <https://frontendchecklist.io/rules/performance/back-forward-cache>
- `high` **browser-caching** - Enable browser caching <https://frontendchecklist.io/rules/performance/browser-caching>
- `high` **cdn** - Use a content delivery network <https://frontendchecklist.io/rules/performance/cdn>
- `high` **compression** - Enable text-based compression <https://frontendchecklist.io/rules/performance/compression>
- `high` **consent-mode** - Implement Google Consent Mode v2 <https://frontendchecklist.io/rules/performance/consent-mode>
- `high` **critical-request-chains** - Minimize critical request chains <https://frontendchecklist.io/rules/performance/critical-request-chains>
- `high` **cumulative-layout-shift** - Minimize cumulative layout shift <https://frontendchecklist.io/rules/performance/cumulative-layout-shift>
- `high` **first-contentful-paint** - Optimize first contentful paint <https://frontendchecklist.io/rules/performance/first-contentful-paint>
- `high` **font-loading** - Optimize web font loading <https://frontendchecklist.io/rules/performance/font-loading>
- `high` **http2** - Enable HTTP/2 or HTTP/3 <https://frontendchecklist.io/rules/performance/http2>
- `high` **http-requests** - Minimize HTTP requests <https://frontendchecklist.io/rules/performance/http-requests>
- `high` **import-on-interaction** - Load non-critical code on user interaction <https://frontendchecklist.io/rules/performance/import-on-interaction>
- `high` **import-on-visibility** - Load non-critical code when content approaches the viewport <https://frontendchecklist.io/rules/performance/import-on-visibility>
- `high` **interaction-to-next-paint** - Optimize interaction to next paint <https://frontendchecklist.io/rules/performance/interaction-to-next-paint>
- `high` **lazy-loading** - Implement lazy loading for offscreen content <https://frontendchecklist.io/rules/performance/lazy-loading>
- `high` **list-virtualization** - Virtualize long lists and tables <https://frontendchecklist.io/rules/performance/list-virtualization>
- `high` **loading-indicators** - Show loading indicators <https://frontendchecklist.io/rules/performance/loading-indicators>
- `high` **page-load-time** - Keep page load time under 3 seconds <https://frontendchecklist.io/rules/performance/page-load-time>
- `high` **page-weight** - Keep page weight under 1500KB <https://frontendchecklist.io/rules/performance/page-weight>
- `high` **performance-resource-hints** - Use resource hints for faster loading <https://frontendchecklist.io/en/rules/performance/performance-resource-hints>
- `high` **resource-hints** - Use resource hints for faster loading <https://frontendchecklist.io/rules/performance/resource-hints>
- `high` **third-party-scripts** - Optimize third-party script loading <https://frontendchecklist.io/rules/performance/third-party-scripts>
- `high` **video-optimization** - Optimize and compress web videos <https://frontendchecklist.io/rules/performance/video-optimization>

