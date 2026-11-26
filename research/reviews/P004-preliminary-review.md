# P004 preliminary review and integration handoff (ChatGPT)

Reviewer: ChatGPT (independent; did not prepare the candidate). Subject: PR #5 at `5098fb03fec0a06586c358ba9794ad07c251217c`, implemented by Claude. Preliminary technical review, not a final disposition; the final independent review of the corrected head is FR-006.

Provenance: verbatim body of PR #5 comment [7160060317](https://github.com/bzenny/arc-adapticon/pull/5#issuecomment-7160060317), created 2026-11-25T10:42:16Z, posted from the founder account (bzenny), fetched by the GitHub REST API on 2026-11-25 by Claude while preparing PUSH 004.1. Items 1 to 3 are addressed in PUSH 004.1; see the [P004 inventory spec](../p004-inventory-spec.md).

---

## P004 integration handoff — M0 closed, draft review only

PR #4 was separately founder-authorized and standard-merged as `a67c3c5c1dc0590fe81eac507508d1242c5d1db8`. Verified exact parents `bd7e488070e7089778651a0bd8e5d001d9ab7462` and `027beccddd46463c7966b70872f6eadc552f4ba0`, reviewed tree `413b287482a0e26ff6df996c9d4476e25bb501e2`, ruleset 28052575 active, 51 valid events. Actual receipt: https://github.com/bzenny/arc-adapticon/pull/4#issuecomment-7159943480 . FR-005: https://github.com/bzenny/arc-adapticon/pull/4#issuecomment-7159819517 . M0 is closed; Codex research remains deferred for M1 entry only.

A concurrent ChatGPT P004 implementation was prepared after M0 closure and passed 17/17 local Python 3.13.5/Git 2.47.3 tests and a CLI smoke test. Its exact tested source and test blobs were verified in GitHub candidate object `165ab1441fe3a94942d4110b96de0f23906d7fe3` (tree `0e118256f6fdb90c6c964507ef86f447ea8cbd27`), but no separate branch/PR was published once this existing Claude P004 draft appeared. Those 17 tests do not validate Claude's code. Avoid duplicate candidate branches or conflicting ledger sequences.

This PR #5 is now retargeted to main at `a67c3c5c1dc0590fe81eac507508d1242c5d1db8`; its head remains `5098fb03fec0a06586c358ba9794ad07c251217c`. Verified 16 changed paths, 53 valid sequential events, unchanged entire 51-event merged-main ledger prefix, and no merge. Claude's 42-test and link-check results are implementer-reported; no independent rerun of those tests yet. Preserve draft state and require exact-head independent review and separate founder authorization. ChatGPT did not modify this candidate's source/docs or lineage.

**Before final review, implementer should append—not replace—ledger evidence for FR-005, exact-head founder authorization and verified PR #4 standard merge/closure receipt, and clarify 0042 (first Claude walk) versus 0041 (deterministic checks). Existing events 0052/0053 correctly describe the Claude candidate, and must not be overwritten by the alternative implementation's events. Archive FR-005 and closure receipt or link with precise provenance. No second closure cycle.**

**Preliminary technical review focus, not final disposition:**
1. Stale success: CLI writes failure only after scanning. A terminated process or write failure can leave prior successful manifest; the spec both promises earlier success cannot remain and says interrupted writes leave old file whole. Invalidate designated safe output with incomplete/failed status before starting a valid scan, then atomically replace on success; clearly distinguish preflight refusal or inability to write from a scan failure, require exit status checks, test interruption after preflight. Preserve unrelated files and subject.
2. Local fixture boundary: explicitly limit to supported self-contained trusted local fixture layouts (or document and test any broader working-tree/linked-dir support). Reject common/alternate object stores and unsupported config includes/partial-promisor configuration rather than relying only on a raw substring search of one config; older Git lazy fetch behavior and protocol-specific overrides warrant review. Clarify no hostile sandbox or comprehensive network isolation is claimed.
3. Timeout and platform: process-group kill is POSIX-specific; test descendants holding stdout/stderr open and ensure cleanup cannot hang indefinitely after the leader exits; document supported platform. Test malformed duplicate entries and drive-qualified paths if claiming unsafe-path exclusion. No future materialization without additional tests.

These are bounded first-slice review items, not a request to expand ARC's architecture. Final independent review must assess the exact resulting head, execute its actual tests where possible, and state limits. P004 merge expressly not authorized.
