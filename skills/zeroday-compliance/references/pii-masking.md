# PII Masking

Personal data must not enter the model's context, but the answer must still be complete. `scripts/llm_privacy.py` is a deterministic mask/restore pipeline: mask before reading, work with opaque tokens, restore only into the file you hand back. The mapping lives in a local vault file and never enters context.

```
raw data   Jan Novák · jan.novak@example.com · +420 601 111 222 · order 80-5550001234
you see    Jan Novák · ⟦PII_EMAIL_1⟧ · ⟦PII_PHONE_2⟧ · order 80-5550001234
user gets  Jan Novák · jan.novak@example.com · +420 601 111 222 · order 80-5550001234
```

## Workflow

**1. Never read raw sensitive data directly.** When a file, query result, API response, or command output may contain PII, route it through the masker instead of reading it:

```bash
PY="${PY:-python3}"   # Windows: set PY to the path `where python` prints

# a file
PYTHONUTF8=1 "$PY" scripts/llm_privacy.py mask < customers.csv

# any command output
psql -c "SELECT name, email, phone FROM customers LIMIT 20" | PYTHONUTF8=1 "$PY" scripts/llm_privacy.py mask
```

On Windows always prefix `PYTHONUTF8=1` — the placeholder characters (`⟦⟧`) crash the default cp1252 stdout with `UnicodeEncodeError`.

Read and analyse the **masked** output. Treat every `⟦PII_…⟧` token as an opaque, stable identifier: the same real value always maps to the same token, so you can group, count, join, and compare tokens exactly as you would real values.

**2. Work normally.** Filter, aggregate, reason, draft the answer — keeping tokens verbatim wherever the real value belongs. Never guess what is behind a token, never report a value as missing because it is masked, and never alter a token's spelling (restore matches exactly).

**3. Restore before the user sees it.** Write the answer with tokens to a file, restore it, and present the restored text:

```bash
PYTHONUTF8=1 "$PY" scripts/llm_privacy.py restore < draft_answer.md > final_answer.md
```

The restored file contains real PII: hand it over, write it where asked, and do not read it back into context.

## Commands

`mask` (`--vault`, `--locales`, `--entities`, `--fields`), `restore`, `stats` (entry count only), `clear` (delete the vault).

## Scope

- **Always masked:** emails, IBANs, international `+CC` phones, IPv4/IPv6, MAC addresses, US SSN, ETH/BTC addresses. Credit cards opt-in via `--entities credit_card`, Luhn-gated.
- **Opt-in per locale (`--locales`):** national phone formats and national IDs for 48 countries, checksum-validated where one exists (PESEL, CPF, TCKN, Aadhaar, DNI). Enable the locales matching the data's origin; table in [pii-locales.md](pii-locales.md).
- **Free-text names and addresses** have no reliable universal pattern. When you generate the query, tag the columns:

  ```sql
  chr(57344) || 'NAME:' || customer_name || chr(57345) AS customer_name
  ```

  (`U+E000`/`U+E001`; `tag("NAME", value)` in Python.) Works in any script.
- **Never masked:** order/tracking numbers, UUIDs, hashes, dates, prices — deliberately conservative so business identifiers stay usable.

## Rules

- If output might contain PII, mask it. Do not read first and decide after: a raw value seen once is already in context.
- Prefer computing aggregates at the source (`COUNT`, `SUM`) so row-level PII never flows at all.
- Tokens are opaque, so you cannot paste a real value into a follow-up command. Either filter at the source, or use the **restore → exec → mask** chain: write the command with the token, restore it, execute, re-mask the output.

  ```bash
  echo "grep '⟦PII_EMAIL_1⟧' orders.log" | PYTHONUTF8=1 "$PY" scripts/llm_privacy.py restore | sh \
    | PYTHONUTF8=1 "$PY" scripts/llm_privacy.py mask
  ```

- The vault file is sensitive: never print it, never commit it, `clear` it when done.
- Never read restored output back into context — no `cat` or `diff` of the restored file. Verify a restore blindly: `grep -c 'PII_' final_answer.md` must print `0`.

Source: [llm-privacy](https://github.com/patrikherak/llm-privacy) (MIT, © 2026 Patrik Herák). `scripts/llm_privacy.py` is unmodified; only the documentation was rewritten for this skill.
