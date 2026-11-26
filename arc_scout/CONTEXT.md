# ARC Scout package

M1 step 1 (PUSH 004): deterministic, metadata-only inventory of one commit in a trusted local Git directory. Contract and limits: [P004 inventory spec](../research/p004-inventory-spec.md). Tests: [tests](../tests/CONTEXT.md).

| File | Role |
|---|---|
| [inventory.py](inventory.py) | Engine: layout and config checks, deadline-bound allowlisted Git runner, path policy, manifest, atomic write |
| [\_\_main\_\_.py](__main__.py) | CLI: `python -m arc_scout inventory --git-dir D --commit SHA --output F`; invalidates the output before scanning; exit 0/1/2/3 |
| [\_\_init\_\_.py](__init__.py) | Version and Python 3.12+ guard |

POSIX only; Python standard library and installed Git only. P004.2 rejects unsafe output directory entries and ambiguous layouts before writes, validates finite bounded limits before spawn, and cleans up after collection errors. Both output destinations must pass preflight. Accepts only self-contained bare or non-linked `.git` directories and refuses includes, alternates, partial-clone and protocol configuration. Never checks out, reads file contents into Scout, follows symlinks or gitlinks, or runs repository code. Not a sandbox for hostile repositories. Changes to the Git allowlist (`ALLOWED_COMMANDS`, `GIT_GLOBAL_OPTIONS`) need independent review and a matching T14 test change.
