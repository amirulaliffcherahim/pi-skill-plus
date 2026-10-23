# Sources

How this material was assembled, and what each upstream is worth opening for.

## Assembly

- **API rules** were read directly from the upstream rule sets and paraphrased: `zalando/restful-api-guidelines` chapters for URLs/naming and pagination (rule numbers cited below are theirs), and `microsoft/api-guidelines` for `api-version`, repeatability, `Operation-Location`, and conditional requests. The two disagree on surface conventions, so `api-design.md` presents them as two coherent bundles and requires choosing one.
- **Latency, availability, and capacity arithmetic** were checked against `donnemartin/system-design-primer`'s appendix tables (latency numbers, powers of two) rather than recalled.
- **Scaling, caching, replication, and resilience patterns** are a curated synthesis of the three system-design repositories, with the symptom-to-pattern organisation taken from `awesome-scalability`.
- **`public-apis` informed no rule here.** It is a catalogue, not a design reference.
- Nothing here is a verbatim copy: rules are restated in the imperative, tables are rebuilt, and prose is original.

## System design and scaling

| Repository | Open it for | Worth knowing |
|---|---|---|
| [ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101) | diagrams for REST vs GraphQL vs gRPC, CAP, caching strategies, sharding, consistent hashing, message queues, API gateway, 12-factor | visual explainers — the fastest way to get a component's trade-offs into a design-doc figure |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | the worked designs (URL shortener, pastebin, crawler, social feed, Mint), the latency and powers-of-two appendices, availability math, the interview process | `design-walkthrough.md` follows its shape, and its worked URL-shortener design is the model for the short-link example |
| [binhnguyennus/awesome-scalability](https://github.com/binhnguyennus/awesome-scalability) | a pattern-to-production reading list organised by symptom: slow means scalability/performance, down means availability/stability | the organisation is the useful part: symptom → pattern family → real systems that ran it at scale, with engineering write-ups for each |

## API conventions and public API catalogues

| Repository | Open it for | Worth knowing |
|---|---|---|
| [zalando/restful-api-guidelines](https://github.com/zalando/restful-api-guidelines) | RFC-2119 rule catalogue with stable rule numbers and `MUST`/`SHOULD`/`MAY` severity, machine-checkable via Zally | cite a rule number in a review and the argument about taste ends. Numbers used here: `#129` kebab-case segments, `#130` snake_case query params, `#134` pluralize, `#135` no `/api` base path, `#136` normalized paths, `#137` conventional query params, `#138`/`#141` no verbs, `#143` path segments, `#146` limit resource types, `#147` limit nesting, `#159` paginate, `#160` prefer cursors, `#161`/`#248` page object and links, `#228` URL-safe ids, `#254` avoid total counts |
| [microsoft/api-guidelines](https://github.com/microsoft/api-guidelines) | required `api-version` query parameter and date-based versioning, `nextLink` paging with continuation tokens, `Repeatability-Request-ID` idempotency, `Operation-Location` long-running operations, `ETag`/`If-Match`, the `{error:{code,message,target,details,innererror}}` envelope, `Retry-After` | the strictest widely-used REST rule set, and Azure-specific in its conventions — adopt it whole or not at all, not as a spice rack |
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | a catalogue of free public APIs by category, with auth and HTTPS flags | not a design reference. Use it to find a real API to inspect for contract patterns, or an integration target while prototyping |

## Attribution and licensing

The API and database material descends from [agent-skills-standard](https://github.com/HoangNguyen0403/agent-skills-standard) (MIT, © 2026 Hoang Nguyen), which shipped here previously as `common-api-design` and `common-database-design`. Its text has been merged, rewritten, and extended; its MIT notice is retained in `LICENSE` beside this file because the licence requires the notice to travel with substantial portions of the work.

Licensing of the upstream repositories above is set by each repository's own `LICENSE`; consult it before copying text or figures into a deliverable.
