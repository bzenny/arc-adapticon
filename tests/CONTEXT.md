# Tests

Run from the repository root: `python -m unittest discover -s tests -v` (POSIX, Python 3.12+, installed Git, no network).

- [fixtures.py](fixtures.py): builds synthetic bare repositories from raw objects under a fixed Git environment, including hostile trees Git porcelain would refuse; canaries that leave marker files if executed.
- [test_inventory.py](test_inventory.py): P004 acceptance tests T01 to T15 and the PUSH 004.1 regression classes T06b, T08b, T12b and T15b, as listed in the [P004 inventory spec](../research/p004-inventory-spec.md).

Run once as an unprivileged user too: `T15b.test_unwritable_directory_reports_exit_3` skips as root.

Fixture code may run any Git command; the allowlist applies only to Scout. These are slice-level tests of metadata inventory, not Scout S-1 to S-8 or ARC-EXP-001.
