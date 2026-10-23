# Infrastructure, Config, and Launch

## Secrets and configuration

- **Inventory:** list every secret (API keys, DB URL, signing keys, webhook secrets, SMTP, model keys) with where it lives and who can read it. A secret nobody can locate is a secret nobody can rotate.
- **Per environment:** dev, staging, and production have distinct values. Sharing a production key with staging means a staging bug spends production money and can read production data.
- **Storage:** a secret manager (or the platform's encrypted env store) — not a committed file, not a `.env` inside the web root, not a value pasted into a build arg, and never in a container image layer.
- **Rotation:** scheduled for long-lived credentials, and immediately for anything ever committed, shared in chat, logged in CI, or used in a test. Record the rotation date; an unrotated leaked key is still a live key.
- **Least privilege:** the app's database user is not the schema owner and not an admin; the service key is not a superuser; CI has no production write access it does not need.
- **Build and CI:** secrets not echoed in build logs; fork PRs get no secrets; CI tokens scoped per repository.
- **Prevention:** a pre-commit secret scanner so the next leak does not reach a remote (commands in [tooling.md](tooling.md)).

Production config sanity: debug off, verbose error pages off, test/dev routes removed, `NODE_ENV=production`, framework admin and API docs disabled or authenticated, CORS origins explicit, log level not `debug`.

## Exposure

Check from **outside** the network, because that is the attacker's view:

| Check | Expected |
|---|---|
| Open ports on the deployed host | Only `80`/`443` (plus your bastion/SSH if required) — never `3306`, `5432`, `6379`, `27017`, `9200`, `11211` |
| Storage buckets | Private by default; no public-read ACL; no listing; no predictable URL that serves other people's files |
| `.env`, `.git/config`, `.DS_Store`, `backup.sql`, `dump.tar.gz` | `404` |
| Database "public access" toggle at the provider | Off, with an allowlisted network if remote access is genuinely needed |
| Firewall / security group | Only required ports, sourced from the load balancer, not `0.0.0.0/0` |
| Admin panels, dashboards, queue consoles | Behind auth and ideally not on the public hostname |
| SSH | Keys only, no root login, no shared account, fail2ban or equivalent |
| Directory listing | Off |

Add a WAF or CDN in front only if you will actually tune it; an untuned WAF is a false sense of security.

## Backups

- **On, encrypted, and off the primary failure domain** — a backup on the same volume or the same account is a restore plan for a bug, not for an account compromise.
- **Restore tested at least once**, with the time it took written down. Until a restore has run, you have a backup *claim*.
- **State the targets:** RPO (how much data you can lose) and RTO (how long to recover). Neither is a number you discover during an incident.
- **Back up before a destructive migration**, and know where that specific dump is.
- **Deleted-user tension:** backups will still contain data you deleted. Document it — retain backups for a defined window, and exclude them from "we deleted everything" claims in the notice.
- **Access control on backups** matters as much as on the database: a public bucket full of encrypted dumps is still a copy of every customer.

## Deploy and rollback

- Immutable, versioned artefacts; the deploy is a promotion of something already tested, not a rebuild on the production host.
- Migrations: additive first (see the data rules for expand → migrate → contract), run before the app that needs them, with a lock timeout so a blocked migration fails instead of queueing every query behind it.
- One deploy can be rolled back: keep the previous artefact, know the command, and have run it once.
- Feature flags to decouple deploy from release for anything risky.
- Staging close enough to production that "works on staging" means something — same platform, same headers, same proxy. Many security-header and CORS failures exist only in the deployed edge.

## Monitoring and alerts

Alerts that reach a human, for:

| Signal | Why |
|---|---|
| 5xx rate and p95 latency | the user-visible failure |
| Uptime of the app and the database | availability baseline |
| Auth failure spikes, login from new geography for admins | credential stuffing, takeover |
| Bulk export / unusual row counts read | the breach pattern that matters most |
| Permission or role changes | privilege escalation |
| Error tracker volume spike | a deploy broke something |
| Disk, queue depth, connection pool saturation | the failure before the failure |
| Paid-model spend per hour | bill shock |
| Backup job failures | silent loss of the restore plan |

- Error tracking configured with PII scrubbing on (`sendDefaultPii` off, request bodies stripped) — an error tracker that captures cookies and tokens is a breach database.
- Logs centralised, access-controlled, retained for a defined period, and free of PII.
- Every alert has a runbook line: what it means and what to do. An alert nobody knows how to action is noise, and noise gets muted.

## Incident readiness

- Contacts: who to call, in what order, day and night, with a deputy for each role.
- Severity ladder: what counts as an incident, who declares it, who communicates.
- Comms: a user-facing template (what happened, what data, what we did, what to do), a status page or mailing channel that exists before it is needed, and the regulator notification path in [legal.md](legal.md).
- The first hour is: contain, preserve evidence, assess data and people affected, notify per the breach plan, then fix. Do not rebuild before capturing the log.
- A short postmortem after any incident, including the near-misses.

## Sign-off

Name one person who owns security and one who owns privacy, and record the dated sign-off in the readiness report. Shared ownership at launch means nobody is accountable when a BLOCK item is argued into a PASS.
