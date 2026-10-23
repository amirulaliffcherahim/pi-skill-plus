# Ghidra headless fallback

Use when REA is not available. All commands are static analysis; the target is imported as bytes and never executed.

## Basic import + analysis
```powershell
$g = $env:GHIDRA_INSTALL_DIR
$w = Join-Path $env:TEMP "re-work\sample1"; New-Item -ItemType Directory $w -Force | Out-Null
& "$g\support\analyzeHeadless.bat" $w proj `
  -import "C:\path\to\target.exe" `
  -analysisTimeoutPerFile 900 `
  -scriptPath "$env:USERPROFILE\.pi\agent\skills\reverse-engineer\scripts" `
  -postScript RE_Decompile.java main `
  -deleteProject -log "$w\ghidra.log" 2>&1 | Select-String "RE_|ERROR|Exception"
```
- `<project_dir> <project_name>` come first, then options.
- `-deleteProject` removes the project after the run (leave it out to keep it for follow-up passes, then use `-process <name> -noanalysis` against the saved project).
- `-readOnly` stops changes being saved when you only want output.
- Language is auto-detected from the header. Override only for raw blobs: `-processor x86:LE:64:default -cspec windows`.
- `-postScript` runs after analysis; pass arguments after the script name. `-preScript` runs before.
- Windows launcher is `analyzeHeadless.bat`; Linux/macOS is `analyzeHeadless`.

## Bundled scripts (`scripts/`)
| Script | Does |
|---|---|
| `RE_Overview.java` | Prints image base, function count, imports (external symbols), defined strings (first 200) |
| `RE_Decompile.java <name\|0xaddr>` | Decompiles matching function(s), prints C. No arg means the first 20 functions |
| `RE_Xrefs.java <name\|0xaddr>` | Lists callers/references to a function or address |

Output lines are prefixed `RE_` so you can filter the noisy Ghidra log.

These are plain Java `GhidraScript`s (no Python needed). Tested headless on Ghidra 12.1.4 + JDK 21 against a real PE: all three compile and produce correct output.

## Typical pass
1. `RE_Overview.java`: size up the binary.
2. Pick strings/imports tied to the question, then `RE_Xrefs.java <symbol or addr>` for who uses them.
3. `RE_Decompile.java <function>` on only those functions.
4. Report with addresses; list unknowns.

## Gotchas
- JDK must be full 21+; set `JAVA_HOME` if `java -version` shows 17. Ghidra picks the JDK from `JAVA_HOME` or `PATH`.
- Large files: raise analysis time with `-analysisTimeoutPerFile`, or use `-noanalysis` plus targeted scripts for a quick look.
- A project name cannot be reused with `-import` unless you add `-overwrite`.
- Log noise is normal; the answer is in `RE_` lines. A non-zero exit with no `RE_` lines means the script failed to compile or the import failed: read the log tail.
