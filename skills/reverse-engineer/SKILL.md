---
name: reverse-engineer
description: Reverse engineer native, managed (.NET), Electron/JavaScript, Android, packaged, firmware and browser targets with Ghidra and REA (MCP/CLI), with Ghidra headless as fallback. Use to decompile, list functions/strings/xrefs, explain how a shipped binary or app works, compare versions, or guide a reconstruction. Skip for ordinary source repositories.
---

# Reverse engineer (REA + Ghidra)

**REA** (`morluto/rea`) is an evidence-first MCP/CLI layer over many analysers. **Ghidra** (`NationalSecurityAgency/ghidra`) is its native-code engine, and `analyzeHeadless` also works on its own. Prefer REA; fall back to headless Ghidra for native binaries.

Use this when a claim depends on a shipped binary or package, decompilation, runtime evidence, or behaviour source code cannot show. For a complete source repository use normal repo tools and do **not** run REA readiness commands.

## Scope and safety (read first)
- Only analyse files the user owns or is authorised to inspect. If ownership is unclear, ask once.
- **Static by default.** Never run, load or detonate the target on your own. Runtime observation (browser/Electron scenarios, process capture, Frida) executes the declared target: do it only when the user explicitly asks, and never widen the target or action beyond what was declared. Frida is **not installed** on this machine (EDR risk).
- Analysis, explanation, interoperability and compatibility work are in scope. Do not write exploits, payloads, PoCs or bypasses for third-party software; say so and offer the analysis instead.
- Keep samples and Ghidra projects out of Downloads and out of the user's repo. Work in `%TEMP%\re-work\<name>`.
- Every conclusion separates **observed**, **inferred** and **unknown**. Cite Evidence IDs and addresses; keep limitations and incomplete coverage; never imply static analysis observed execution. Decompiler output is an observation, not original source.

## Step 0: environment (once, only if needed)
```powershell
powershell -File "$env:USERPROFILE\.pi\agent\skills\reverse-engineer\scripts\check-env.ps1"
```
Reports Ghidra, JDK, Node, REA and the next fix. Install nothing without the user's approval. Run it (or `rea doctor`) only when REA tools are absent, a call fails, or the user asks for a diagnosis, never before every task.

Verified here (2026-10-22): Ghidra 12.1.4, JDK 21 and a private Node 24 live in `~/tools`; `GHIDRA_INSTALL_DIR`/`JAVA_HOME` are user-level env vars; REA is registered in `~/.pi/agent/mcp.json` with its own Node. Requirements: Ghidra 12.1.x, full 64-bit JDK 21+ (17 fails), REA on Node 22.19+/24.11+/26+ (system Node 25 is unsupported, so do not use `npx rea-agents` from it). Cold Ghidra analysis of a small PE ~75s; minutes for large ones.

REA never installs Node, Java, Ghidra, IDA, JADX, Kuna, Binwalk or Unblob; do not install them to repair MCP registration.

## Connect only when needed
If REA tools are present and registration is not known stale, go straight to the target. In pi they are `mcp__rea__*`, reached through the `codemode` tool. Use the connected server's actual tool list and input schemas (a newer skill can describe tools an older REA lacks).

If tools are absent or a call is blocked, read [connection-and-recovery.md](references/connection-and-recovery.md). Short version:
1. Diagnose without changing config: `rea doctor --json` (add `--client pi`).
2. Tell the cause apart: missing/stale registration needs a scoped repair; an aligned registration with no tools needs a pi `/reload` or restart; a missing provider only affects tasks needing it (static JavaScript needs neither Hopper nor Ghidra; Android needs separate JADX/Java).
3. For a repair, show the read-only plan first (`rea setup --client pi --dry-run --format json`), get approval, then apply with `--yes`. Setup writes agent config and replaces installed skills, so never run it unasked.
4. Reload, confirm the tools appear, resume the original task. If they still do not, read the client's MCP launch error instead of repeating setup.

If a host call times out with no REA result, do not repeat it unchanged or assume the work stopped.

## Route the target first
Pick the first tool from the target the user gave. `open_binary` is for active-target native/archive work; target-free tools take their own explicit path.

| Target | Use |
|---|---|
| Native exe/DLL/library/analysis DB | `open_binary` (provider `ghidra`), then focused tools: `binary_overview`, `list_procedures`, `procedure_pseudo_code`, `analyze_function`, `xrefs`, `search_strings`; `close_binary` when done |
| ASAR / extracted JS or Electron tree | `analyze_javascript_application` (use `detail: "summary"` for large ones) |
| ZIP/APK/IPA/MSIX/AppX/DMG archive | `open_binary` with the path; `inspect_artifact` for graph and findings; `extract_artifact` only when files are needed |
| Android APK code/classes/methods | `inspect_android_package`, then focused Android tools |
| Managed PE/CLI (.NET) | `inspect_managed_artifact` (execution-free; never claim it loaded or ran the assembly) |
| NativeAOT PE/ELF | native Ghidra analysis (workflow in [native-and-artifacts.md](references/native-and-artifacts.md)) |
| Firmware image | `inspect_firmware_regions`; `extract_firmware` only on request, into a new absolute output dir (needs Binwalk/Unblob, Linux) |
| Open browser page (user-owned) | `list_browser_targets`; acting on it: `capture_browser_scenario` with declared actions |
| Open Electron runtime (user-owned) | `list_electron_targets`; check `inspect_electron_fuses` before an Inspector attempt |
| HAR/SAZ/mitmproxy/qlog capture | `inspect_web_network_capture` (summary first; no URL fetching, no live attribution claims) |
| Packet capture / pcap | `inspect_packet_fields` to choose fields, `inspect_packet_capture`, `inspect_pcap_capture`. Needs tshark; reads recordings only |
| Logic/signal recording | `inspect_signal_decoders`, `decode_signal_recording` (needs sigrok-cli; reads files only) |
| WebAssembly | `inspect_wasm_artifact` (needs WABT; WAT is not original source) |
| EVM bytecode | `inspect_evm_interface` (selectors/mutability are inferred, no chain lookup) |
| Go / Rust binary metadata | `inspect_go_binary` / `inspect_rust_binary` (absent metadata proves nothing) |
| SQLite snapshot | `inspect_sqlite_database` (schema first; use a quiescent copy) |
| Linux ELF layout/mitigations, core dump | `inspect_binary_layout` / `inspect_recorded_crash` |
| PE resources | `inspect_pe_resources` |
| Apple bundle plist/IB/assets | `inspect_plist`, `decode_interface_builder`, `inspect_asset_catalog`, `inspect_keyed_archive` (Mach-O: `inspect_macho`) |
| Version comparison, feature tracing | `compare_application_versions`, `compare_artifacts`, `compare_functions`, `trace_feature`, `trace_application_feature`, `find_changed_behavior` |
| Static vs runtime | `reconcile_javascript_runtime`, `correlate_static_and_runtime` (only when runtime evidence was requested) |

Other providers (not configured here): IDA (`provider_id: "ida"`, open the original binary, not an `.idb`), Kuna (`REA_KUNA_COMMAND`), Hopper. If the user says only "my app", ask which one before searching; resolve a named app to one installed artifact, ask when ambiguous, never pick an example app for them. Do not call a tool `binary_session` does not advertise (`binary_session` with `{}` shows availability and remediation).

Read only the guide the task needs (all in `references/`):
- Native binaries, .NET assemblies, archives/packages, extraction, NativeAOT: [native-and-artifacts.md](references/native-and-artifacts.md)
- ASAR / extracted JavaScript, feature tracing, version comparison, large-graph recipes: [javascript-applications.md](references/javascript-applications.md)
- Android APK declarations, classes, methods, references: [android-applications.md](references/android-applications.md)
- Browser/Electron observation (passive and scenario), static vs runtime reconciliation: [runtime-observation.md](references/runtime-observation.md)
- Evidence paging, comparisons, residual unknowns, verification: [evidence-workflows.md](references/evidence-workflows.md)
- REA tools missing, stale registration, blocked calls, timeouts: [connection-and-recovery.md](references/connection-and-recovery.md)
- Native via Ghidra headless without REA: [headless.md](references/headless.md)

## Native workflow (Ghidra)
1. **Identify**: path, format (PE/ELF/Mach-O), arch, size, `Get-FileHash`.
2. **Overview first**: imports, exports, sections, function count, notable strings. Do not decompile everything.
3. **Hypothesis** tied to the question (for example "where is the licence file validated").
4. **Follow it**: strings/imports to xrefs to the calling function, then decompile only those. Rename nothing permanently.
5. **Corroborate**: a claim needs two independent observations (a string xref and the decompiled branch using it). One snippet is a lead, not a fact.
6. **Report** with addresses and function names plus unknowns: stripped symbols, packing, indirect calls, unloaded PDB. Empty search results do not prove absence.
7. **Clean up**: close the REA session; delete the scratch project unless asked to keep it.

REA CLI fallback (no MCP): `rea analyze <path> --provider ghidra --json`. No REA, Ghidra present: [references/headless.md](references/headless.md).

## Work summary-first
- Start with the default result and its inline Evidence and graph; make a focused follow-up only when it leaves a specific question open. Never repeat an identical call without a changed input or a resolved blocker.
- Large JavaScript apps or ELF layouts: call with `detail: "summary"`, then `inspect_analysis_view` on the retained `parent_evidence_id`; page module identities and pick the returned `node_id` before requesting an item. A broad bidirectional trace pulls in unrelated containment.
- On `resource_constraint` with `details.resource: "transport"`, use `inspect_analysis_view` with the reported Evidence reference, `trace_application_feature` once a seed is known, or `export_evidence_bundle`. The analysis is complete in the ledger; do not re-run it to get the same oversized reply. A client-truncated preview is incomplete: do not parse it as canonical JSON.
- Lost the parent ID: `get_evidence_bundle` with `detail: "summary"` and exact filters (operation, target SHA-256, profile digest, procedure address).
- Within the user's requested investigation, call available tools directly; REA needs no per-call approval flags, but the client may. Use the observed rejection, not guesses.

## Broad investigations
1. Turn the request into a checklist of questions and the evidence each needs. Resolve target identity from the conversation and workspace before asking.
2. Reuse the current REA session, saved analysis and prior evidence; do not open duplicate sessions.
3. Smallest useful overview first, then follow each question from entry point to result. Batch operations around one hypothesis.
4. Read packaged resources and configuration alongside code when they affect the answer; use format-aware parsers, not filenames or strings alone.
5. Use runtime observation only if static evidence cannot answer and the user asked for it.
6. Independent questions can go to parallel workers if available (distinct scopes, point them at existing evidence); otherwise work sequentially.
7. Keep a short finding ledger: conclusion, Evidence IDs, confidence, search boundary, remaining unknowns.

Before finishing, revisit the checklist and mark each item answered, partial or unresolved. Keep negative searches bounded; do not call a broad investigation complete while required questions are open.

## Known limits
- Ghidra only sees *defined* string data; packed or undefined literals (including Rust strings) can be missing.
- PE names may be absent without a loaded PDB: say "recovered name" vs "original name".
- On Windows REA's Ghidra provider is read-only and admits native PE only (x86, x86-64, ARMNT, ARM64).
- Large binaries can take many minutes: set a per-file timeout, report it, do not retry blindly.

## Finish
Explain in plain language, tied to returned evidence, with unknowns listed. If asked to build something, use normal coding tools and mark what is observed behaviour and what is your design.
