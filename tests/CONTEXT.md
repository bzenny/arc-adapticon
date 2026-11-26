# Tests

Run from the repository root: `python -m unittest discover -s tests -v` (POSIX, Python 3.12+, installed Git, no network).

- [fixtures.py](fixtures.py): builds synthetic bare repositories from raw objects under a fixed Git environment, including hostile trees Git porcelain would refuse; canaries that leave marker files if executed.
- [test_inventory.py](test_inventory.py): original 66 P004 and P004.1 acceptance tests, unchanged, as listed in the [P004 inventory spec](../research/p004-inventory-spec.md).
- [test_fr006.py](test_fr006.py): 13 P004.2 regression tests for K-01 and K-02; preflight no-write/no-spawn assertions, real child cleanup and normal success/failure compatibility. Total 79 tests.

Run once as an unprivileged user too: `T15b.test_unwritable_directory_reports_exit_3` skips as root.

Fixture code may run any Git command; the allowlist applies only to Scout. These are slice-level tests of metadata inventory, not Scout S-1 to S-8 or ARC-EXP-001.
