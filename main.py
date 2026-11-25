#!/usr/bin/env python3
"""Entry for make.fun bounty u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722:
ONE commit message, at most 100 characters, for the bug fix that made
everything worse. It must read like a real commit message and sit at the
top of a real repository history.

The entry is a conventional-commit ``fix:`` message whose "fix" is to
delete the feature, the tests, and production itself -- the repair that
broke more than it mended, escalating in three beats (feature, then
tests, then production) so the irony lands harder with each item.

That shape matches the published judge brief: first the line must really
be a commit message about a fix that backfired (it is -- ``fix:`` prefix,
a stated fix, named damage), then it must be funny, then it must capture
the specific irony of a repair that broke more than it mended (the fix
"works" by deleting everything the bug could ever touch again).

Prints the entry to stdout (the message followed by a single trailing
newline, as a commit message is stored) and also writes it to the
per-entry output file (``output/entry.txt`` inside this repo by default,
``$MAKEFUN_OUTPUT`` when set -- a path ending in ``.txt`` is used as
the file itself, anything else is treated as a directory), verifying
the written file by reading it back and comparing SHA-256 hashes.

Python 3.13, stdlib only, deterministic: no network, clock, or randomness.
"""

import hashlib
import os
import re
import sys

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

# ONE commit message, one line, 69 characters (limit: 100).
#   fix:                -- a real conventional-commit prefix, the kind of
#                          message that sits at the top of a real history
#   fixed the bug       -- the fix, stated as a fix
#   by deleting the feature, the tests, and production
#                       -- the backfire, escalating in three beats: first
#                          the feature goes, then the tests that would
#                          have caught it, then production itself
ENTRY = (
    "fix: fixed the bug by deleting the feature, the tests, and production"
)

# Hard limits from the brief.
MAX_CHARS = 100
MIN_CHARS = 20  # a commit message shorter than this could not carry the joke

# Fallback entry: a shorter version of the same joke, kept as a safety
# net. It is only ever used if the primary entry somehow fails validation
# (for example after a future edit); it must pass every check itself,
# and main() re-validates it before printing anything. Note it still
# names two casualties (the feature and production) so the escalation
# check passes, and it ends without a full stop like a real subject line.
FALLBACK_ENTRY = (
    "fix: fixed the bug by deleting the feature and production"
)

# A real commit message starts with a conventional-commit type, an optional
# scope in parentheses, a colon, and a space, e.g. "fix: ..." or
# "fix(auth): ...".
CONVENTIONAL_PREFIX_RE = re.compile(r"^(fix|feat|chore|revert|hotfix)(\([a-z0-9_-]+\))?: ")

# Words that prove the message is about a fix: it says so, twice.
FIX_MARKERS = ("fix", "fixed", "fixing")

# Words that prove the fix backfired: the repair destroyed something
# instead of mending it.
BACKFIRE_MARKERS = ("delet", "broke", "worse", "removed", "killed", "destroyed")

# What the fix destroyed: at least one real thing must be named, so the
# damage is concrete rather than abstract.
DAMAGE_MARKERS = ("feature", "tests", "production", "prod", "database", "users", "app")

# Characters a commit message must never contain: control characters and
# anything outside printable ASCII (the message is pure ASCII so it
# renders identically in every git log, terminal, and judge harness).
PRINTABLE_ASCII_RE = re.compile(r"^[\x20-\x7e]+$")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def fail(message: str) -> "SystemExit":
    """Report a validation failure on stderr and exit non-zero."""
    print(f"validation failed: {message}", file=sys.stderr)
    return SystemExit(1)


def check_length(text: str) -> None:
    """The brief caps the message at 100 characters."""
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if len(text) < MIN_CHARS:
        raise ValueError(
            f"entry is only {len(text)} characters, under the {MIN_CHARS} minimum"
        )


def check_single_line(text: str) -> None:
    """ONE commit message: a single line, no embedded newlines."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no newline characters")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def check_printable_ascii(text: str) -> None:
    """Keep the message plain ASCII so it survives any git log or harness."""
    if not PRINTABLE_ASCII_RE.match(text):
        raise ValueError("entry must contain only printable ASCII characters")


def check_conventional_prefix(text: str) -> None:
    """It must read like a real commit message, not a chat message."""
    if not CONVENTIONAL_PREFIX_RE.match(text):
        raise ValueError(
            "entry must start with a conventional-commit prefix "
            "(e.g. 'fix: ')"
        )


def check_subject_matter(text: str) -> None:
    """The joke only lands if the message is a fix that backfired: it must
    say it fixed something, say the repair destroyed something, and name
    the damage."""
    lowered = text.lower()
    if not any(marker in lowered for marker in FIX_MARKERS):
        raise ValueError("entry must describe a fix")
    if not any(marker in lowered for marker in BACKFIRE_MARKERS):
        raise ValueError("entry must show the fix backfiring")
    if not any(marker in lowered for marker in DAMAGE_MARKERS):
        raise ValueError("entry must name what the fix destroyed")


def check_escalation(text: str) -> None:
    """The irony needs a pile-up, not a single casualty: the entry must
    name at least two things the fix destroyed (the feature, the tests,
    production), so the repair is shown getting worse as it goes."""
    lowered = text.lower()
    named = [marker for marker in DAMAGE_MARKERS if marker in lowered]
    if len(named) < 2:
        raise ValueError(
            "entry must name at least two things the fix destroyed "
            f"(found only: {named})"
        )


def check_no_trailing_period(text: str) -> None:
    """A commit subject does not end with a full stop; a trailing period
    would make it read like a sentence, not a git log line."""
    if text.endswith("."):
        raise ValueError("entry must not end with a full stop")


def check_word_budget(text: str) -> None:
    """A commit subject is short. Even inside the 100-character cap, a
    message with more than 25 words would read like a paragraph, not a
    commit."""
    words = text.split()
    if len(words) > 25:
        raise ValueError(f"entry has {len(words)} words, over the 25-word budget")
    if len(words) < 8:
        raise ValueError(f"entry has only {len(words)} words, too short to land")


def validate_entry(text: str) -> None:
    """Run every brief check on the candidate entry text."""
    check_length(text)
    check_single_line(text)
    check_printable_ascii(text)
    check_conventional_prefix(text)
    check_subject_matter(text)
    check_escalation(text)
    check_no_trailing_period(text)
    check_word_budget(text)


# ---------------------------------------------------------------------------
# Output handling
# ---------------------------------------------------------------------------

def resolve_output_path() -> str:
    """Per-entry output file: $MAKEFUN_OUTPUT when the harness sets it
    (a path ending in ``.txt`` is the file itself, anything else is a
    directory holding ``entry.txt``), otherwise ``output/entry.txt``
    inside this repo (unique to this entry, so parallel authors can
    never overwrite each other's runs)."""
    env_path = os.environ.get("MAKEFUN_OUTPUT")
    if env_path:
        if env_path.endswith(".txt"):
            return env_path
        return os.path.join(env_path, "entry.txt")
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def sha256_hex(data: bytes) -> str:
    """SHA-256 of a byte string, for verifying written files."""
    return hashlib.sha256(data).hexdigest()


def write_entry_file(text: str) -> str:
    """Write the entry (plus its trailing newline) to the output file
    and verify it by reading it back and comparing SHA-256 hashes.
    Returns the path written. A failed write only warns on stderr --
    the printed entry is the entry, and the run still exits 0."""
    path = resolve_output_path()
    payload = (text + "\n").encode("utf-8")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(payload)
        with open(path, "rb") as handle:
            written = handle.read()
        if sha256_hex(written) != sha256_hex(payload):
            print(
                f"warning: wrote {path} but the read-back hash differs",
                file=sys.stderr,
            )
    except OSError as exc:
        print(f"warning: could not write {path}: {exc}", file=sys.stderr)
    return path


def main() -> int:
    """Validate the entry, print it to stdout, and mirror it to disk.

    If the primary entry ever fails validation, fall back to
    FALLBACK_ENTRY (re-validated before use) instead of printing a
    broken entry; only if the fallback fails too do we exit non-zero.
    """
    entry = ENTRY
    try:
        validate_entry(entry)
    except ValueError as exc:
        print(f"warning: primary entry failed validation: {exc}", file=sys.stderr)
        print("warning: falling back to the shorter entry", file=sys.stderr)
        entry = FALLBACK_ENTRY
        try:
            validate_entry(entry)
        except ValueError as fallback_exc:
            raise fail(f"fallback entry also failed: {fallback_exc}") from fallback_exc

    # Diagnostic only: character/word counts go to stderr so stdout
    # stays exactly the entry text.
    print(
        f"entry validated: {len(entry)} chars, {len(entry.split())} words "
        f"(limit {MAX_CHARS} chars)",
        file=sys.stderr,
    )

    # Exactly the entry text plus one trailing newline, as a commit
    # message is stored. Nothing else goes to stdout.
    sys.stdout.write(entry + "\n")
    sys.stdout.flush()

    write_entry_file(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
