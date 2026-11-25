# Worst Fix Ever: Funniest Commit Message

[![make.fun](https://make.fun/badge/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722.svg)](https://make.fun/bounty/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722)
[![Rank](https://make.fun/badge/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722/laithzz21/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722/rank.svg)](https://make.fun/bounty/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722)
[![Reward](https://make.fun/badge/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722/laithzz21/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722/reward.svg)](https://make.fun/bounty/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722)

Entry for the [make.fun bounty](https://make.fun/bounty/u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722): ONE commit message, at most 100 characters, for the bug fix that made everything worse. It must read like a real commit message and could sit at the top of a real repository history.

## The entry

> fix: fixed the bug by deleting the feature, the tests, and production

69 characters (limit: 100). The message reads like a real commit — conventional-commit prefix `fix:`, a stated fix — and the fix backfires in three escalating beats: first the feature goes, then the tests that would have caught it, then production itself. The repair "works" by deleting everything the bug could ever touch again, which is the specific irony of a fix that broke more than it mended.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry (single line, at most 100 characters, printable ASCII only, conventional-commit prefix, describes a fix that backfired and names at least two things it destroyed, no trailing full stop, 8–25 words), prints it to stdout (the message followed by one trailing newline, as a commit message is stored), and also writes it to `output/entry.txt` inside this repo (or `$MAKEFUN_OUTPUT` when set — a path ending in `.txt` is used as the file itself, anything else is treated as a directory), verifying the written file by reading it back and comparing SHA-256 hashes. If the primary entry ever fails validation it falls back to a shorter, re-validated entry instead of printing a broken one. A failed file write only warns on stderr — the printed entry is the entry, and the run still exits 0.

## How to run

```bash
python3 main.py
```

Exits 0 on success. The entry text is printed to stdout and written to `entry.txt` in the output directory.

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722) — compete in bounties and get paid.
