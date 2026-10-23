"""llm-privacy — deterministic, reversible, multilingual PII tokenization for any LLM agent.

Sealed against leaks: real personal data is swapped for stable tokens BEFORE it reaches the
model, and reclaimed on the way out — so the answer is complete but the model never sees a name,
address, phone, e-mail, card, or national id. Pure deterministic code; no ML, no network, no LLM.

Detection is three tiers (enable what you need):
  1. Source tags  — data tools wrap known-PII fields in U+E000..U+E001 markers via ``tag()``.
                    Language-agnostic and exact — every script, every language, identically.
  2. Regex packs  — universal structured formats (email, IBAN, card, IP, MAC, crypto, intl phone)
                    plus opt-in per-locale packs for national phone + national id formats. IDs
                    that are bare digit runs are gated on their real checksum, so only a *valid*
                    id ever masks — a random number of the same length does not.
  3. NER backend  — optional, opt-in (Presidio / GLiNER) for untagged free-text names/places.

Dependency-free (Python stdlib only) and framework-agnostic. Used as a CLI: pipe text through
``mask`` before it reaches the model and through ``restore`` before the user sees the answer; a
persistent vault file keeps tokens stable across calls. Locale coverage is in SPECS.md.
"""
from __future__ import annotations

import os
import re
from collections import OrderedDict
from typing import Callable, Iterable, List, Optional, Tuple

__all__ = ["PrivacyVault", "tag", "luhn_ok", "main", "D1", "D2", "UNIVERSAL", "LOCALES"]

# ── Tier 1: source-tag markers (language-agnostic) ─────────────────────────────
D1, D2 = chr(0xE000), chr(0xE001)
_TAG_RE = re.compile(re.escape(D1) + r"([A-Z_]+):(.*?)" + re.escape(D2), re.DOTALL)


def tag(kind: str, value) -> str:
    """Wrap a value your tool KNOWS is PII so PrivacyVault tokenizes it. Any language, any script."""
    value = "" if value is None else str(value)
    return f"{D1}{kind}:{value}{D2}" if value.strip() else value


# ── Checksums — only a VALID id masks (kills false positives on bare digit runs) ──
def _digits(s: str) -> List[int]:
    return [int(c) for c in s if c.isdigit()]


def _luhn(d: List[int]) -> bool:
    total, alt = 0, False
    for x in reversed(d):
        if alt:
            x *= 2
            if x > 9:
                x -= 9
        total += x
        alt = not alt
    return total % 10 == 0


def luhn_ok(candidate: str) -> bool:
    """Luhn mod-10 over 13–19 digits (payment cards)."""
    d = _digits(candidate)
    return 13 <= len(d) <= 19 and _luhn(d)


def _all_same(d: List[int]) -> bool:
    return len(set(d)) <= 1


def _v_luhn(n):  # CA SIN (9), ZA ID (13), IL Teudat Zehut (9), AU TFN (9) — generic Luhn
    d = _digits(n)
    return bool(d) and not _all_same(d) and _luhn(d)


def _v_tfn(n):  # Australia TFN — 9 digits, weighted mod-11 (NOT Luhn)
    d = _digits(n)
    if len(d) != 9:
        return False
    w = [1, 4, 3, 7, 5, 8, 6, 9, 10]
    return sum(x * y for x, y in zip(d, w)) % 11 == 0


def _v_cpf(n):  # Brazil CPF — 11 digits, two mod-11 check digits
    d = _digits(n)
    if len(d) != 11 or _all_same(d):
        return False
    for k in (9, 10):
        s = sum(d[i] * ((k + 1) - i) for i in range(k))
        c = (s * 10) % 11
        if c == 10:
            c = 0
        if c != d[k]:
            return False
    return True


def _v_cnpj(n):  # Brazil CNPJ — 14 digits
    d = _digits(n)
    if len(d) != 14 or _all_same(d):
        return False
    for w in ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]):
        s = sum(x * y for x, y in zip(d, w))
        c = s % 11
        c = 0 if c < 2 else 11 - c
        if c != d[len(w)]:
            return False
    return True


def _v_pesel(n):  # Poland PESEL — 11 digits
    d = _digits(n)
    if len(d) != 11:
        return False
    w = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    c = (10 - sum(x * y for x, y in zip(d, w)) % 10) % 10
    return c == d[10]


def _v_tckn(n):  # Turkey T.C. Kimlik No — 11 digits
    d = _digits(n)
    if len(d) != 11 or d[0] == 0:
        return False
    d10 = ((sum(d[0:9:2]) * 7) - sum(d[1:8:2])) % 10
    d11 = sum(d[0:10]) % 10
    return d10 == d[9] and d11 == d[10]


_DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


def _v_dni_es(n):  # Spain DNI/NIE — 8 digits + control letter
    m = re.match(r"^([XYZ]?)(\d{7,8})-?([A-Z])$", n.strip().upper())
    if not m:
        return False
    prefix, num, letter = m.groups()
    base = {"": "", "X": "0", "Y": "1", "Z": "2"}[prefix] + num
    return _DNI_LETTERS[int(base) % 23] == letter


def _v_cnp_ro(n):  # Romania CNP — 13 digits
    d = _digits(n)
    if len(d) != 13:
        return False
    w = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    c = sum(x * y for x, y in zip(d, w)) % 11
    c = 1 if c == 10 else c
    return c == d[12]


def _v_egn_bg(n):  # Bulgaria EGN — 10 digits
    d = _digits(n)
    if len(d) != 10:
        return False
    w = [2, 4, 8, 5, 10, 9, 7, 3, 6]
    c = sum(x * y for x, y in zip(d, w)) % 11 % 10
    return c == d[9]


def _v_nir_fr(n):  # France NIR/INSEE — 13 digits + 2-digit key
    d = re.sub(r"\s", "", n)
    if not re.fullmatch(r"\d{15}", d):
        return False
    return int(d[13:]) == 97 - (int(d[:13]) % 97)


def _v_nhs_uk(n):  # UK NHS number — 10 digits, mod-11
    d = _digits(n)
    if len(d) != 10:
        return False
    s = sum(d[i] * (10 - i) for i in range(9))
    c = 11 - (s % 11)
    c = 0 if c == 11 else c
    return c != 10 and c == d[9]


def _v_bsn_nl(n):  # Netherlands BSN — 9 digits, 11-test
    d = _digits(n)
    if len(d) != 9:
        return False
    return (sum(d[i] * (9 - i) for i in range(8)) - d[8]) % 11 == 0


def _v_rrn_kr(n):  # South Korea RRN — 13 digits
    d = _digits(n)
    if len(d) != 13:
        return False
    w = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    c = (11 - sum(x * y for x, y in zip(d, w)) % 11) % 10
    return c == d[12]


# Verhoeff (India Aadhaar)
_VF_D = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
         [2, 3, 4, 0, 1, 7, 8, 9, 5, 6], [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
         [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
         [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
         [8, 7, 6, 5, 9, 3, 2, 1, 0, 4], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
_VF_P = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
         [5, 8, 0, 3, 7, 9, 6, 1, 4, 2], [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
         [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
         [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]


def _v_aadhaar(n):  # India Aadhaar — 12 digits, Verhoeff (first digit not 0/1)
    d = _digits(n)
    if len(d) != 12 or d[0] in (0, 1):
        return False
    c = 0
    for i, x in enumerate(reversed(d)):
        c = _VF_D[c][_VF_P[i % 8][x]]
    return c == 0


# ── Tier 2: universal entity patterns  (kind, regex, validator|None) ──────────
_SP = r"[  .\-]"  # space / nbsp / dot / dash — NOT newline

UNIVERSAL: Tuple = (
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,24}\b"), None),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){2,7}(?:[ ]?[A-Z0-9]{1,3})?\b"), None),
    ("MAC", re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b"), None),
    ("IPV6", re.compile(r"\b(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}\b"), None),
    ("IPV4", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"), None),
    ("ETH", re.compile(r"\b0x[a-fA-F0-9]{40}\b"), None),
    ("BTC", re.compile(r"\b(?:bc1[ac-hj-np-z02-9]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b"), None),
    ("SSN_US", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), None),
    ("PHONE", re.compile(r"\+\d(?:" + _SP + r"?\(?\d\)?){6,16}"), None),  # international +CC (all countries)
    ("CREDIT_CARD", re.compile(r"\b(?:\d[ \-]?){13,19}\b"), luhn_ok),     # opt-in; Luhn-gated
)


def _rx(p):
    return re.compile(p)


# ── Per-locale packs (opt-in via config.locales). Bare-digit ids are checksum-gated. ──
LOCALES: dict = {
    # ── Europe ──
    "cz": [("PHONE", _rx(r"\b(?:(?:00420|\+?420)[ ]?)?[67]\d{2}[ ]\d{3}[ ]\d{3}\b"), None),
           ("NID", _rx(r"\b\d{6}/\d{3,4}\b"), None)],  # rodné číslo (slash = distinctive)
    "sk": [("PHONE", _rx(r"\b(?:(?:00421|\+?421)[ ]?)?9\d{2}[ ]\d{3}[ ]\d{3}\b"), None),
           ("NID", _rx(r"\b\d{6}/\d{3,4}\b"), None)],
    "de": [("PHONE", _rx(r"\b0\d{2,4}[ /]\d{5,9}\b"), None)],
    "at": [("PHONE", _rx(r"\b0\d{3}[ /]\d{4,10}\b"), None)],
    "ch": [("PHONE", _rx(r"\b0\d{2}[ ]\d{3}[ ]\d{2}[ ]\d{2}\b"), None),
           ("AHV", _rx(r"\b756\.\d{4}\.\d{4}\.\d{2}\b"), None)],
    "fr": [("PHONE", _rx(r"\b0[1-9](?:[ .]\d{2}){4}\b"), None),
           ("NIR", _rx(r"\b[12][ ]?\d{2}[ ]?\d{2}[ ]?\d{2}[ ]?\d{3}[ ]?\d{3}[ ]?\d{2}\b"), _v_nir_fr)],
    "es": [("PHONE", _rx(r"\b[6789]\d{2}[ ]\d{2}[ ]\d{2}[ ]\d{2}\b"), None),
           ("DNI", _rx(r"\b[XYZ]?\d{7,8}-?[A-Z]\b"), _v_dni_es)],
    "it": [("PHONE", _rx(r"\b3\d{2}[ ]\d{6,7}\b"), None),
           ("CF", _rx(r"\b[A-Z]{6}\d{2}[A-EHLMPR-T]\d{2}[A-Z]\d{3}[A-Z]\b"), None)],
    "pl": [("PHONE", _rx(r"\b(?:\+?48[ ]?)?\d{3}[ ]\d{3}[ ]\d{3}\b"), None),
           ("PESEL", _rx(r"\b\d{11}\b"), _v_pesel)],
    "nl": [("PHONE", _rx(r"\b0[6][ -]?\d{8}\b"), None),
           ("BSN", _rx(r"\b\d{9}\b"), _v_bsn_nl)],
    "be": [("PHONE", _rx(r"\b04\d{2}[ /]\d{2}[ ]\d{2}[ ]\d{2}\b"), None)],
    "pt": [("PHONE", _rx(r"\b9[1236]\d[ ]\d{3}[ ]\d{3}\b"), None)],
    "uk": [("PHONE", _rx(r"\b07\d{3}[ ]?\d{6}\b"), None),
           ("NINO", _rx(r"\b[ABCEGHJ-PRSTW-Z]{2}[ ]?\d{2}[ ]?\d{2}[ ]?\d{2}[ ]?[A-D]\b"), None),
           ("NHS", _rx(r"\b\d{3}[ ]\d{3}[ ]\d{4}\b"), _v_nhs_uk)],
    "ie": [("PHONE", _rx(r"\b08[35679][ ]?\d{3}[ ]?\d{4}\b"), None)],
    "se": [("PHONE", _rx(r"\b07[0-9][ -]?\d{3}[ ]?\d{2}[ ]?\d{2}\b"), None),
           ("PNR", _rx(r"\b\d{6}[-+]\d{4}\b"), None)],
    "no": [("PHONE", _rx(r"\b[49]\d{2}[ ]\d{2}[ ]\d{3}\b"), None)],
    "dk": [("PHONE", _rx(r"\b\d{2}[ ]\d{2}[ ]\d{2}[ ]\d{2}\b"), None),
           ("CPR", _rx(r"\b\d{6}-\d{4}\b"), None)],
    "fi": [("PHONE", _rx(r"\b0[45]\d[ ]?\d{3,4}[ ]?\d{3,4}\b"), None),
           ("HETU", _rx(r"\b\d{6}[-+A]\d{3}[0-9A-Z]\b"), None)],
    "gr": [("PHONE", _rx(r"\b6\d{2}[ ]\d{3}[ ]\d{4}\b"), None)],
    "ro": [("PHONE", _rx(r"\b07\d{2}[ ]\d{3}[ ]\d{3}\b"), None),
           ("CNP", _rx(r"\b[1-8]\d{12}\b"), _v_cnp_ro)],
    "bg": [("PHONE", _rx(r"\b08[789][ ]?\d{3}[ ]?\d{3}\b"), None),
           ("EGN", _rx(r"\b\d{10}\b"), _v_egn_bg)],
    "hu": [("PHONE", _rx(r"\b06[ ]?[237]0[ ]?\d{3}[ ]?\d{4}\b"), None)],
    "ru": [("PHONE", _rx(r"\b8[ ]?\(?9\d{2}\)?[ ]?\d{3}[ -]?\d{2}[ -]?\d{2}\b"), None)],
    "ua": [("PHONE", _rx(r"\b0\d{2}[ ]\d{3}[ ]\d{2}[ ]\d{2}\b"), None)],
    "tr": [("PHONE", _rx(r"\b05\d{2}[ ]\d{3}[ ]\d{2}[ ]\d{2}\b"), None),
           ("TCKN", _rx(r"\b[1-9]\d{10}\b"), _v_tckn)],
    # ── Americas ──
    "us": [("PHONE", _rx(r"\(\d{3}\)[ ]?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b"), None),
           ("EIN", _rx(r"\b\d{2}-\d{7}\b"), None)],
    "ca": [("PHONE", _rx(r"\(\d{3}\)[ ]?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b"), None),
           ("SIN", _rx(r"\b\d{3}[ -]\d{3}[ -]\d{3}\b"), _v_luhn)],
    "br": [("PHONE", _rx(r"\(\d{2}\)[ ]?9?\d{4}-\d{4}"), None),
           ("CPF", _rx(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"), _v_cpf),
           ("CNPJ", _rx(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"), _v_cnpj)],
    "mx": [("PHONE", _rx(r"\b\d{2}[ ]\d{4}[ ]\d{4}\b"), None),
           ("CURP", _rx(r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b"), None)],
    "ar": [("PHONE", _rx(r"\b11[ ]\d{4}[ ]\d{4}\b"), None)],
    # ── Asia / Pacific ──
    "cn": [("PHONE", _rx(r"\b1[3-9]\d[ ]?\d{4}[ ]?\d{4}\b"), None),
           ("RIC", _rx(r"\b\d{17}[0-9Xx]\b"), None)],
    "jp": [("PHONE", _rx(r"\b0[789]0-\d{4}-\d{4}\b"), None)],
    "kr": [("PHONE", _rx(r"\b01[016789]-\d{3,4}-\d{4}\b"), None),
           ("RRN", _rx(r"\b\d{6}-\d{7}\b"), _v_rrn_kr)],
    "in": [("PHONE", _rx(r"\b[6-9]\d{4}[ ]?\d{5}\b"), None),
           ("AADHAAR", _rx(r"\b\d{4}[ ]\d{4}[ ]\d{4}\b"), _v_aadhaar),
           ("PAN", _rx(r"\b[A-Z]{5}\d{4}[A-Z]\b"), None)],
    "id": [("PHONE", _rx(r"\b08\d{2}[ -]?\d{4}[ -]?\d{3,4}\b"), None)],
    "th": [("PHONE", _rx(r"\b0[689]\d[ -]?\d{3}[ -]?\d{4}\b"), None)],
    "vn": [("PHONE", _rx(r"\b0[35789]\d[ ]?\d{3}[ ]?\d{4}\b"), None)],
    "ph": [("PHONE", _rx(r"\b09\d{2}[ ]?\d{3}[ ]?\d{4}\b"), None)],
    "sg": [("PHONE", _rx(r"\b[89]\d{3}[ ]?\d{4}\b"), None),
           ("NRIC", _rx(r"\b[STFGM]\d{7}[A-Z]\b"), None)],
    "my": [("PHONE", _rx(r"\b01\d[ -]?\d{3,4}[ -]?\d{4}\b"), None),
           ("MYKAD", _rx(r"\b\d{6}-\d{2}-\d{4}\b"), None)],
    "au": [("PHONE", _rx(r"\b04\d{2}[ ]\d{3}[ ]\d{3}\b"), None),
           ("TFN", _rx(r"\b\d{3}[ ]\d{3}[ ]\d{3}\b"), _v_tfn)],
    "nz": [("PHONE", _rx(r"\b02\d[ ]?\d{3}[ ]?\d{3,4}\b"), None)],
    # ── Middle East / Africa ──
    "il": [("PHONE", _rx(r"\b05\d-\d{3}-\d{4}\b"), None),
           ("TZ", _rx(r"\b\d{9}\b"), _v_luhn)],
    "ae": [("PHONE", _rx(r"\b05[024568][ ]?\d{3}[ ]?\d{4}\b"), None),
           ("EID", _rx(r"\b784-?\d{4}-?\d{7}-?\d\b"), None)],
    "sa": [("PHONE", _rx(r"\b05\d[ ]?\d{3}[ ]?\d{4}\b"), None)],
    "za": [("PHONE", _rx(r"\b0\d{2}[ ]\d{3}[ ]\d{4}\b"), None),
           ("SAID", _rx(r"\b\d{13}\b"), _v_luhn)],
    "ng": [("PHONE", _rx(r"\b0[789]\d{2}[ ]?\d{3}[ ]?\d{4}\b"), None)],
    "eg": [("PHONE", _rx(r"\b01[0125]\d{8}\b"), None)],
}


class PrivacyVault:
    """A per-process vault + mask/restore. One instance per gateway (each is its own process)."""

    def __init__(
        self,
        entities: Optional[Iterable[str]] = None,
        locales: Optional[Iterable[str]] = None,
        source_tags: bool = True,
        token_format: str = "⟦PII_{kind}_{n}⟧",
        max_values: int = 5000,
        terms: Optional[Iterable[str]] = None,
        terms_file: Optional[str] = None,
        terms_kind: str = "TERM",
        terms_ignore_case: bool = True,
    ):
        # Default: all universal patterns EXCEPT credit cards (opt-in — the only universal entity
        # whose length overlaps tracking/order numbers; a Luhn gate still guards it when enabled).
        wanted = set(e.upper() for e in entities) if entities else {k for k, _, _ in UNIVERSAL} - {"CREDIT_CARD"}
        self._patterns: List[Tuple[str, "re.Pattern", Optional[Callable]]] = [
            (k, rx, v) for k, rx, v in UNIVERSAL if k in wanted
        ]
        for loc in (locales or []):
            self._patterns += LOCALES.get(loc.lower(), [])
        self._source_tags = source_tags
        self._fmt = token_format
        self._max = max_values
        self._t2v: "OrderedDict[str, str]" = OrderedDict()
        self._v2t: dict = {}
        self._n = 0
        # Custom terms (Tier 1.5): a caller-supplied list of literal strings to always mask —
        # personal names, internal codenames, account handles, anything a regex can't recognise.
        # Terms may be inline and/or in a file that some external job regenerates; the file is
        # hot-reloaded on mtime change so a periodic refresh lands without restarting.
        self._inline_terms: List[str] = [t for t in (terms or []) if t and t.strip()]
        self._terms_file = terms_file or None
        self._terms_kind = _sanitize_kind(terms_kind)
        self._terms_ic = terms_ignore_case
        self._term_patterns: List[Tuple[str, "re.Pattern"]] = []
        self._terms_mtime = None
        self._load_terms()

    def _read_terms_file(self) -> List[Tuple[str, str]]:
        """Parse the terms file: one term per line, optional ``term<TAB>KIND`` to set a custom token
        kind; blank lines and ``#`` comments are ignored. A missing/unreadable file yields nothing."""
        entries: List[Tuple[str, str]] = []
        if not self._terms_file:
            return entries
        try:
            with open(self._terms_file, "r", encoding="utf-8") as fh:
                for raw in fh:
                    line = raw.rstrip("\n")
                    if not line.strip() or line.lstrip().startswith("#"):
                        continue
                    if "\t" in line:
                        term, kind = line.split("\t", 1)
                        kind = _sanitize_kind(kind) or self._terms_kind
                    else:
                        term, kind = line, self._terms_kind
                    if term.strip():
                        entries.append((term.strip(), kind))
        except OSError:
            pass
        return entries

    def _load_terms(self) -> None:
        entries = [(t, self._terms_kind) for t in self._inline_terms] + self._read_terms_file()
        by_kind: "OrderedDict[str, list]" = OrderedDict()
        for term, kind in entries:
            by_kind.setdefault(kind, []).append(term)
        flags = re.IGNORECASE if self._terms_ic else 0
        patterns: List[Tuple[str, "re.Pattern"]] = []
        for kind, terms in by_kind.items():
            # Longest-first: a regex alternation is leftmost-FIRST, so a longer/multi-word term must
            # precede its own substrings to win. Boundaries stop matches inside a larger word/number.
            ordered = sorted(set(terms), key=len, reverse=True)
            alt = "|".join(re.escape(t) for t in ordered)
            patterns.append((kind, re.compile(r"(?<!\w)(?:" + alt + r")(?!\w)", flags)))
        mtime = None
        if self._terms_file:
            try:
                mtime = os.stat(self._terms_file).st_mtime
            except OSError:
                mtime = None
        self._term_patterns = patterns
        self._terms_mtime = mtime

    def _maybe_reload_terms(self) -> None:
        if not self._terms_file:
            return
        try:
            mtime = os.stat(self._terms_file).st_mtime
        except OSError:
            return
        if mtime != self._terms_mtime:
            self._load_terms()

    def _token(self, value: str, kind: str) -> str:
        if not value or not value.strip():  # keep the EXACT matched text (whitespace incl.) for lossless restore
            return value
        tok = self._v2t.get(value)
        if tok is not None:
            self._t2v.move_to_end(tok)
            return tok
        if len(self._t2v) >= self._max:
            old_tok, old_val = self._t2v.popitem(last=False)
            self._v2t.pop(old_val, None)
        self._n += 1
        tok = self._fmt.format(kind=kind, n=self._n)
        self._t2v[tok] = value
        self._v2t[value] = tok
        return tok

    def mask(self, text: str) -> str:
        """Replace PII with tokens (call on the way IN — tool / terminal output)."""
        if not isinstance(text, str) or not text:
            return text
        if self._source_tags:
            text = _TAG_RE.sub(lambda m: self._token(m.group(2), m.group(1)), text)
        if self._terms_file:
            self._maybe_reload_terms()
        for kind, rx in self._term_patterns:  # Tier 1.5: caller-supplied literal terms
            text = rx.sub(lambda m, k=kind: self._token(m.group(0), k), text)
        for kind, rx, validator in self._patterns:
            if validator is None:
                text = rx.sub(lambda m, k=kind: self._token(m.group(0), k), text)
            else:
                text = rx.sub(
                    lambda m, k=kind, v=validator: self._token(m.group(0), k) if v(m.group(0)) else m.group(0),
                    text,
                )
        return text

    def restore(self, text: str) -> str:
        """Swap tokens back to the real values (call on the way OUT — final model message)."""
        if not isinstance(text, str) or not text or not self._t2v:
            return text
        for tok, val in list(self._t2v.items()):
            if tok in text:
                text = text.replace(tok, val)
        return text

    @property
    def size(self) -> int:
        return len(self._t2v)


# ── CLI with a persistent, lock-protected vault file (any agent can pipe text through) ─────────
def _split(value: Optional[str]) -> Optional[list]:
    parts = [x.strip() for x in (value or "").split(",") if x.strip()]
    return parts or None


def _sanitize_kind(kind: Optional[str]) -> str:
    """A token kind must be a bare identifier — it goes into ``token_format`` and the restore path."""
    k = re.sub(r"[^A-Za-z0-9_]", "", (kind or "").strip()).upper()
    return k or "TERM"


def _vault_path(arg: Optional[str]) -> str:
    return arg or os.getenv("LLM_PRIVACY_VAULT") or os.path.join(
        os.path.expanduser("~"), ".llm-privacy", "vault.json"
    )


class _VaultLock:
    """Advisory file lock so concurrent mask calls can't clobber each other's mappings.
    (fcntl — POSIX; on platforms without it the lock degrades to a no-op.)"""

    def __init__(self, path: str):
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, mode=0o700, exist_ok=True)
        self._fh = open(path + ".lock", "a")

    def __enter__(self):
        try:
            import fcntl

            fcntl.flock(self._fh, fcntl.LOCK_EX)
        except ImportError:
            pass
        return self

    def __exit__(self, *exc):
        try:
            import fcntl

            fcntl.flock(self._fh, fcntl.LOCK_UN)
        except ImportError:
            pass
        self._fh.close()
        return False


def _load(pv: "PrivacyVault", path: str) -> None:
    import json

    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pv._n = int(data.get("n", 0))
    for tok, val in data.get("map", []):
        pv._t2v[tok] = val
        pv._v2t[val] = tok


def _save(pv: "PrivacyVault", path: str) -> None:
    import json

    d = os.path.dirname(path)
    if d:
        os.makedirs(d, mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump({"n": pv._n, "map": list(pv._t2v.items())}, f, ensure_ascii=False)


# ── Structured mode: mask whole CSV columns / JSON keys by field name (exact, no guessing) ──
def _norm_kind(name: str) -> str:
    return re.sub(r"\W+", "_", name).strip("_").upper() or "FIELD"


def _mask_csv_fields(pv: "PrivacyVault", text: str, fields) -> Optional[str]:
    """If the text is CSV/TSV whose header row names ≥1 requested field, tokenize those columns
    whole. Returns the re-serialized CSV, or None if the text doesn't look like matching CSV."""
    import csv as _csv
    import io as _io

    want = {f.lower() for f in fields}
    first = text.split("\n", 1)[0]
    best = None
    for delim in (",", ";", "\t"):
        header = next(_csv.reader([first], delimiter=delim), [])
        hitidx = {i for i, h in enumerate(header) if h.strip().lower() in want}
        if hitidx and (best is None or len(hitidx) > len(best[1])):
            best = (delim, hitidx, [h.strip() for h in header])
    if best is None:
        return None
    delim, hitidx, header = best
    out = _io.StringIO()
    writer = _csv.writer(out, delimiter=delim, lineterminator="\n")
    rows = _csv.reader(_io.StringIO(text), delimiter=delim)
    writer.writerow(next(rows))
    for row in rows:
        writer.writerow([
            pv._token(cell, _norm_kind(header[i])) if i in hitidx and cell.strip() else cell
            for i, cell in enumerate(row)
        ])
    return out.getvalue()


def _mask_json_fields(pv: "PrivacyVault", text: str, fields) -> Optional[str]:
    """If the text is JSON, tokenize string values of the requested keys (recursively).
    Returns re-serialized JSON, or None if the text isn't JSON."""
    import json

    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    want = {f.lower() for f in fields}

    def walk(node):
        if isinstance(node, dict):
            return {
                k: (pv._token(v, _norm_kind(k)) if k.lower() in want and isinstance(v, str) and v.strip()
                    else walk(v))
                for k, v in node.items()
            }
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    return json.dumps(walk(data), ensure_ascii=False, indent=2)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse
    import sys

    ap = argparse.ArgumentParser(
        prog="llm_privacy.py",
        description="Reversible PII tokenization: `mask` stdin before an LLM sees it, "
        "`restore` stdin before the user sees it. The vault file maps tokens back to real values.",
    )
    ap.add_argument("command", choices=["mask", "restore", "stats", "clear"])
    ap.add_argument("--vault", help="vault file (default: $LLM_PRIVACY_VAULT or ~/.llm-privacy/vault.json)")
    ap.add_argument("--locales", help="comma-list of locale packs, e.g. cz,sk,de,us (default: $LLM_PRIVACY_LOCALES)")
    ap.add_argument("--entities", help="comma-list of universal entities (default: all except CREDIT_CARD)")
    ap.add_argument("--fields", help="mask these CSV columns / JSON keys whole, e.g. name,customer,street "
                                     "(default: $LLM_PRIVACY_FIELDS) — exact structured masking, catches "
                                     "free-text names no regex can")
    ap.add_argument("--terms", help="comma-list of literal terms to always mask, e.g. 'Jane Roe,Project Orion' "
                                    "(default: $LLM_PRIVACY_TERMS)")
    ap.add_argument("--terms-file", help="path to a wordlist (one term per line, optional 'term<TAB>KIND'), "
                                         "hot-reloaded on change (default: $LLM_PRIVACY_TERMS_FILE)")
    args = ap.parse_args(argv)

    path = _vault_path(args.vault)
    pv = PrivacyVault(
        entities=_split(args.entities) or _split(os.getenv("LLM_PRIVACY_ENTITIES")),
        locales=_split(args.locales) or _split(os.getenv("LLM_PRIVACY_LOCALES")),
        source_tags=os.getenv("LLM_PRIVACY_SOURCE_TAGS", "true").lower() not in ("0", "false", "no"),
        token_format=os.getenv("LLM_PRIVACY_TOKEN_FORMAT", "⟦PII_{kind}_{n}⟧"),
        max_values=int(os.getenv("LLM_PRIVACY_MAX_VALUES", "5000")),
        terms=_split(args.terms) or _split(os.getenv("LLM_PRIVACY_TERMS")),
        terms_file=args.terms_file or os.getenv("LLM_PRIVACY_TERMS_FILE") or None,
        terms_kind=os.getenv("LLM_PRIVACY_TERMS_KIND", "TERM"),
        terms_ignore_case=os.getenv("LLM_PRIVACY_TERMS_IGNORE_CASE", "true").lower() not in ("0", "false", "no"),
    )

    if args.command == "clear":
        with _VaultLock(path):
            if os.path.exists(path):
                os.remove(path)
        print(f"vault cleared: {path}")
        return 0

    if args.command == "stats":
        with _VaultLock(path):
            _load(pv, path)
        print(f"vault: {path}\nentries: {pv.size}")
        return 0

    text = sys.stdin.read()
    if args.command == "mask":
        fields = _split(args.fields) or _split(os.getenv("LLM_PRIVACY_FIELDS"))
        with _VaultLock(path):
            _load(pv, path)
            if fields:
                structured = _mask_json_fields(pv, text, fields)
                if structured is None:
                    structured = _mask_csv_fields(pv, text, fields)
                if structured is not None:
                    text = structured
            sys.stdout.write(pv.mask(text))
            _save(pv, path)
    else:
        with _VaultLock(path):
            _load(pv, path)
        sys.stdout.write(pv.restore(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
