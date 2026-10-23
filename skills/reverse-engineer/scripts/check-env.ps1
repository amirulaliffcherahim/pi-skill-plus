# Read-only environment check for reverse-engineer. Installs nothing, changes nothing.
$ErrorActionPreference = 'Continue'
$fix = New-Object System.Collections.Generic.List[string]
function Row($n, $ok, $d) { "{0,-8} {1,-4} {2}" -f $n, $(if ($ok) { 'ok' } else { 'FAIL' }), $d }

# --- Ghidra
$gd = $env:GHIDRA_INSTALL_DIR; if (-not $gd) { $gd = [Environment]::GetEnvironmentVariable('GHIDRA_INSTALL_DIR','User') }
if (-not $gd) {
  $c = Get-Command ghidraRun, ghidraRun.bat -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($c) { $gd = Split-Path (Split-Path (Resolve-Path $c.Source)) }
}
$gver = $null; $gok = $false
if ($gd -and (Test-Path "$gd\Ghidra\application.properties")) {
  $gver = (Select-String "$gd\Ghidra\application.properties" -Pattern '^application\.version=(.+)$').Matches.Groups[1].Value
  $gok = ($gver -like '12.1*') -and (Test-Path "$gd\support\analyzeHeadless.bat")
  Row 'ghidra' $gok "$gd (version $gver)$(if(-not $gok){' - REA needs 12.1.x'})"
} else {
  Row 'ghidra' $false 'not found (GHIDRA_INSTALL_DIR unset, no ghidraRun on PATH)'
}
if (-not $gok) { $fix.Add('Download Ghidra 12.1.x from https://github.com/NationalSecurityAgency/ghidra/releases, extract it, then: setx GHIDRA_INSTALL_DIR <extracted dir>') }

# --- JDK (needs full JDK 21+, 64-bit)
$jh = $env:JAVA_HOME; if (-not $jh -or (Get-Item $jh -ErrorAction SilentlyContinue) -and ((& "$jh\bin\java.exe" -version 2>&1 | Select-Object -First 1) -notmatch '"(2[1-9]|[3-9]\d)')) { $u = [Environment]::GetEnvironmentVariable('JAVA_HOME','User'); if ($u) { $jh = $u } }
$java = if ($jh -and (Test-Path "$jh\bin\java.exe")) { Join-Path $jh "bin\java.exe" } else { (Get-Command java -ErrorAction SilentlyContinue).Source }
$jmajor = 0; $hasJavac = $false
if ($java) {
  $v = (& $java -version 2>&1 | Select-Object -First 1) -as [string]
  if ($v -match '"(\d+)') { $jmajor = [int]$Matches[1] }
  $jdir = (Split-Path (Split-Path $java)).TrimEnd("\")
  $hasJavac = Test-Path "$jdir\bin\javac.exe"
  Row 'jdk' ($jmajor -ge 21 -and $hasJavac) "$java (major $jmajor, javac $(if($hasJavac){'yes'}else{'no'}))"
} else { Row 'jdk' $false 'java not found' }
if (-not ($jmajor -ge 21 -and $hasJavac)) { $fix.Add('Install a full 64-bit JDK 21+ (for example Temurin 21), then set JAVA_HOME to it. JDK 17 is too old for Ghidra 12.1.') }

# --- Node (REA)
$tn = Get-ChildItem "$env:USERPROFILE\tools" -Directory -Filter "node-v*" -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
$node = if ($tn) { Join-Path $tn.FullName "node.exe" } else { "node" }
$nv = (& $node --version 2>$null) -as [string]
$nok = $false
if ($nv -match '^v(\d+)\.(\d+)') {
  $maj = [int]$Matches[1]; $min = [int]$Matches[2]
  $nok = ($maj -eq 22 -and $min -ge 19) -or ($maj -eq 24 -and $min -ge 11) -or ($maj -ge 26)
}
Row 'node' $nok "$nv (REA needs 22.19+, 24.11+, or 26+)"
if (-not $nok) { $fix.Add('Use Node 24.11+ or 26+ for REA (Node 25 is unsupported). Headless Ghidra works without Node.') }

# --- REA
$rea = (Get-Command rea -ErrorAction SilentlyContinue).Source; if (-not $rea -and (Test-Path "$env:USERPROFILE\tools\rea\rea.cmd")) { $rea = "$env:USERPROFILE\tools\rea\rea.cmd" }
Row 'rea' ($null -ne $rea) $(if ($rea) { $rea } else { 'no global rea; npx -y rea-agents@latest works if Node is ok' })

# --- verdict
""
if ($gok -and $jmajor -ge 21 -and $hasJavac) {
  if ($nok) { 'READY: REA + Ghidra. Use REA with provider ghidra.' }
  else { 'READY (headless only): Ghidra works; REA blocked by Node version.' }
} else {
  'NOT READY. Next fix:'
  $fix | ForEach-Object { "  - $_" }
}
