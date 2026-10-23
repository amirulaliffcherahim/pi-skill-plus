# Tooling

Run every scan against something you own or are authorised to test. Scanning a third party is not a security check, it is an unauthorised one. Default to `localhost`/staging; production only for read-only checks you would be comfortable seeing in a log.

**Status of these commands (checked 2026-10-22):** the flags below match each tool's documented interface, but only `nmap`, `curl`, `node`, and `git` exist on this machine — `gitleaks`, `trufflehog`, `semgrep`, `trivy`, and `docker` are not installed, so none of those invocations have been executed here. Install, then confirm the flags with `--help` before trusting a clean result. A scanner that failed to run looks exactly like a scanner that found nothing.

Windows notes: prefix Python invocations with `PYTHONUTF8=1` and set `PY` to your interpreter (`where python` prints it); Git Bash is the shell for the commands below.

## Secrets — code and git history

```bash
# gitleaks: full history, then exit non-zero on any finding
gitleaks detect --source . --log-opts="--all" --redact -v

# trufflehog: verified findings only, so the report is actionable
trufflehog git file://. --only-verified --no-update

# client bundle: run before trusting any prefix
grep -rnoE "(sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]+)" dist/ build/ .next/ 2>/dev/null
```

Add gitleaks as a pre-commit hook so the next leak dies locally. A finding is a **rotation** task, not a deletion task.

## Dependencies and containers

```bash
npm audit --audit-level=high          # or: pnpm audit / yarn npm audit
pip-audit -r requirements.txt         # Python
cargo audit                           # Rust
go list -m -u all && govulncheck ./... # Go
trivy fs --severity HIGH,CRITICAL .    # lockfiles + misconfig in one pass
trivy image --severity HIGH,CRITICAL <image>:<tag>
```

`npm audit` reports what the advisory database knows about your tree; it cannot see a package that does not exist upstream. Check every direct dependency name against the registry when the code was generated.

## Static analysis

```bash
semgrep --config=p/owasp-top-ten --config=p/secrets --error .
```

Semgrep catches structural patterns you would grep for badly: string-built SQL, unsafe deserialisation, missing authz middleware, tainted HTML sinks. Triage, do not just count.

## Live application — external, read-only

```bash
# vibe-check: ~70 GET/HEAD/OPTIONS probes for .env/.git exposure, source maps,
# security headers, CORS, cookie flags, debug endpoints. Python 3.8+, no deps.
PYTHONUTF8=1 python3 check.py https://yourapp.com --api https://api.yourapp.com/health
PYTHONUTF8=1 python3 check.py https://yourapp.com --json > vibe-check.json
```

```bash
# OWASP ZAP baseline: passive + a few safe active rules, no exploitation
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://staging.yourapp.com -r zap-report.html
```

```bash
# headers, cookies, HSTS
curl -sSI https://yourapp.com | tee headers.txt
curl -sS -o /dev/null -w '%{http_code}\n' https://yourapp.com/.env        # expect 404
curl -sS -o /dev/null -w '%{http_code}\n' https://yourapp.com/.git/config # expect 404
```

```bash
# TLS and header grades
curl -sS "https://api.ssllabs.com/api/v3/analyze?host=yourapp.com&publish=off" | head -40
# Mozilla Observatory: open https://developer.mozilla.org/observatory for a graded header report
```

```bash
# port exposure from outside the host — run from your laptop, not the server
nmap -Pn -sV -p 22,80,443,3000,3306,5432,6379,9200,27017 yourapp.com
```

## Tests no scanner replaces

Automated tools cannot see missing authorization, business-logic abuse, or multi-tenant bleed. These are manual, with two accounts and the payment provider's test mode — the matrix in the skill's "Evidence, not assertion" table.

## What each tool misses

| Tool | Blind to |
|---|---|
| gitleaks / trufflehog | secrets already rotated away from the code, secrets in a vendor dashboard, secrets in a screenshot |
| `npm audit`, Trivy | hallucinated packages, malware in a brand-new package with no advisory, license risk |
| semgrep | logic bugs, missing ownership predicates, anything pattern-shaped but semantically fine |
| ZAP baseline | authenticated surfaces (it is anonymous by default), business logic, race conditions, IDOR |
| vibe-check | anything behind a login, anything in your code at all — it is a black-box surface check |
| SSL Labs / Observatory | application behaviour entirely |
| Every tool above | client-side trust, entitlement checks, webhook replay, tenant isolation |

## Legal and policy artefacts

No scanner produces these. They are written documents: the data inventory, the notice, the DSR runbook, the breach plan, the vendor list, the consent record schema, and the Article 50 disclosure. Keep them in the repository beside the code so the gate can check them and a new hire can find them.
