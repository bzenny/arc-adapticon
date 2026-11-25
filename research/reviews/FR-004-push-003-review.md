# FR-004 — PUSH 003 independent review (ChatGPT)

Reviewer: ChatGPT (independent; did not prepare the candidate). Implementer of PUSH 003/003.1: Claude. Subject: `fee697d76400f0ea735fb202c53538d1e2c9b06f`, tree `ff193a5735749aeff5d7b831915f7a11a425e9f0`.

Provenance: verbatim bodies of two PR #3 comments posted from the founder account (bzenny), fetched by the GitHub REST API on 2026-11-25 by Claude while preparing the M0 closeout. Comment text is unchanged below each heading.

- Review: [7157214096](https://github.com/bzenny/arc-adapticon/pull/3#issuecomment-7157214096), created 2026-11-25T08:34:52Z
- Addendum: [7157417601](https://github.com/bzenny/arc-adapticon/pull/3#issuecomment-7157417601), created 2026-11-25T08:44:46Z

This record is evidence, not authority, and not a GitHub approval by a separate identity.

---

## FR-004 — independent engineering transition review (ChatGPT)
Reviewed head `fee697d76400f0ea735fb202c53538d1e2c9b06f`, base `e4d5984af6f2b7247bf1abbe6ce0f53db34e69f7`, original Claude implementation `0f7bb771bbc825431696183f29542782f313d17e`. 28 changed paths, 7 in the bounded amendment; 36 files in candidate tree. Claude prepared P003/P003.1. ChatGPT reviewed the changes, without contributing to this candidate. Founder has directed ChatGPT back to implementation and Claude back to independent review for subsequent pushes, under D-006. This comment is a review/evidence record, not a GitHub approval by a separate identity, a merge authorization, or authorization to begin M1.

**Disposition: APPROVE WITH NON-BLOCKING FINDINGS for the inspected documentation changes; final acceptance gates remain open.** No P0/P1 identified in inspected changes. J-01 through J-03 substantively addressed; D-006 recorded as ratified. H-05: four full records present with provenance; Git blob hashes match the corresponding new files in the supplied P003 patch. Text comparison to the supplied reviews agrees after Markdown table/whitespace normalization, including a single Markdown escape difference in the supplement; not byte-identical to all source exports. Latest FR-003 addendum included. D-005 optional adapter policy and S-1..S-8/H-11 acceptance additions are present. I-05: independently checked candidate ledger preserves the complete 25-event main prefix and 33-event original candidate prefix exactly; all 37 IDs sequential, six fields, valid event statuses, backward supersession references. Vendored link script retains upstream blob `2f363aedbdcd652349ce9b83045e0f8521262c7c`. Active ruleset 28052575 targets default branch only; main remains protected and unchanged. Candidate contains documentation changes only. Implementer reports link check 29 files/107 checks/0 broken; not independently rerun here (local network unavailable). Do not treat this comment as a fresh Codex cold walk.

**Carry-forward observations**
- J-01A (P3): GitHub proves actual merge state; absence of a ledger receipt proves missing documentation, not an unmerged PR. CONTEXT.md's “if the ledger has no such event, PR #3 is not merged” should read “verify actual PR status on GitHub; record missing merge evidence.” Ledger evidence remains an entry gate.
- J-04 (P2 M1 gate): the reported Claude 6/6 run was before the final Q3 field-list edit. Repeat the fixed six-question instrument against the exact final head. No independent Codex session was available; I-06 remains open and not deferred.
- Record final review, actual merge receipt, exact-head link/ledger checks and both cold-walk logs with accurate attribution in the next authorized append-only lineage update. Do not fabricate a merge event or test result. No historical lines changed.

## P004 — prepared execution scope, not yet authorized
M1 step 1, deterministic local fixture inventory. Proposed branch `push-004-scout-inventory` from the verified post-P003 acceptance baseline. Before runtime changes: separate founder merge authorization for PR #3, verify actual merge tree/protection, complete the fresh Claude and real Codex walks (strict 6/6 per question within AGENTS + 2 reads), independently execute link and lineage checks, record gate receipts, close M0, obtain founder authorization for P004. A short evidence-only closeout may be necessary to record actual merge/test events; no new conceptual architecture needed.

Deliverable: Python 3.12+ standard library + installed Git; local trusted synthetic fixture only. No remote acquisition, checkout, blob-content execution, inference, LLM or paid API. Explicit full SHA-1 commit ID, verify exact commit (no tag/branch resolution, replace refs or lazy fetching). Use read-only Git plumbing with subprocess argument arrays, sanitized environment, bounded output/time/entries/path length, no shell, network or credential prompts; do not claim hostile-repo sandboxing. Enumerate tracked tree entries and metadata deterministically; never follow symlinks or gitlinks; reject unsafe names; report omissions and bounded failures explicitly. No content reading needed for metadata inventory. JSON v0.1 manifest records schema version, subject commit and object format, ordered path/mode/type/object ID/size/disposition, coverage and limitations, license/dependency/runtime assessment unknown. Stable serialization and no timestamps/absolute paths in canonical manifest; separate run evidence. Write only designated output outside fixture, atomically; fail closed with nonzero exit and incomplete status, never stale success.

Proposed implementation files (subject to final exact manifest disclosure): `arc_scout/CONTEXT.md`, `arc_scout/__init__.py`, `arc_scout/__main__.py`, `arc_scout/inventory.py`, `tests/CONTEXT.md`, `tests/__init__.py`, `tests/fixtures.py`, `tests/test_inventory.py`, `research/p004-inventory-spec.md`, `research/FR-004.md`; update root AGENTS/CONTEXT/README, research/CONTEXT, and append lineage/EVENTS.jsonl as applicable. No new runtime dependencies. Read-only hosted CI requires separately disclosed reviewed full-SHA action pins; local tests first. Do not install ScanCode/Syft/OSV-Scanner. Early M1 adapter vetting after local inventory is a separately authorized step.

Tests: deterministic synthetic Git object fixtures, exact expected manifest, pinned older commit, repeated byte-identical output, wrong/non-commit SHA, missing Git, malformed/unsafe paths, symlink/gitlink omissions, limits/timeouts, malicious README and executable canary non-execution, source tree unchanged, offline no paid service. Run `python -m unittest discover -s tests -v` and `python3 -I _tools/links.py`; append-only ledger check. These are slice-level checks, not claims of completing full Scout S-1..S-8 or ARC-EXP-001. Rollback by closing draft PR (main unchanged) or reviewed revert; supersede history rather than deleting events.

Next pushes: safe remote acquisition after P004; early optional ScanCode/Syft vetting per D-005; System Map/im-ICM projection; evidence matrix/export; comparative research and reproducible Scout release. No weighted utility ranking in M1/M2; F-03 blocks M3 execution and F-01/F-02 block M5.

No code, branch, merge or settings change made by this review comment. Claude returns to reviewer role for the first ChatGPT-implemented engineering push; founder authorization is still required.

---

## FR-004 addendum — independently executed exact-head checks and M0 closeout

Subject: `fee697d76400f0ea735fb202c53538d1e2c9b06f`. ChatGPT reviewer; Claude implemented P003/P003.1. All 36/36 file Git blob IDs in a locally reconstructed snapshot matched the pinned GitHub candidate tree `ff193a5735749aeff5d7b831915f7a11a425e9f0`. Reconstruction used supplied patches and pinned connector file reads; no remote checkout or discovered code execution.

**Actual independently executed results**
- Byte-identical vendored checker `_tools/links.py`, blob `2f363aedbdcd652349ce9b83045e0f8521262c7c`: Python 3.13.5, `python3 -I _tools/links.py`, 29 files, 107 links and inputs checked, 0 broken, exit 0.
- Ledger: 37 sequential events; exactly six fields each; valid statuses; every supersession points backward. Connector comparison confirms 25-event main prefix and 33-event original P003 prefix unchanged exactly.
- Live PR still draft/open/unmerged at exact head; main protected and unchanged at `e4d5984af6f2b7247bf1abbe6ce0f53db34e69f7`.
- Technical inspection disposition remains APPROVE WITH NON-BLOCKING FINDINGS. These deterministic checks pass. They do not complete the cold-walk gates.

**Outstanding**
- J-04: qualifying fresh final-head Claude walk, with six-question scoring/read log, not evidenced here. Founder supplied feedback from a walk identifying J-05; no complete final-head scored transcript supplied.
- I-06: actual fresh Codex cold walk not available in this session. No deferral.
- J-05 (minor, founder-supplied reviewer feedback): AGENTS.md's “implemented means done and verified means checked” is ambiguous. Closeout: use semicolon-separated definitions (“implemented = completed action; verified = completed check”), preserving all status distinctions.
- J-01A: actual GitHub PR status is authoritative; missing ledger entry is missing evidence, not proof of unmerged status.
- Founder directed completion of gates, P003 merge, closeout and P004 execution. Treat authorization as conditional on recorded acceptance evidence; do not waive gates. Merge receipt and postmerge checks must be recorded only after merge. Append actual FR-004, cold-walk, check and closeout events; preserve all 37 existing ledger lines. If a cold walk fails due to ambiguous wording, correct within a reviewed candidate and rerun against that head.

**P004 scope refinements (accepted design direction, no runtime changes yet)**
- First slice explicitly supports SHA-1 Git object storage only. Determine storage format with `git rev-parse --show-object-format=storage`; reject SHA-256 repositories as unsupported, not as malformed SHA-1. Require exactly 40 hexadecimal characters and verify object type `commit` with `git cat-file -t <sha>`; no branch/tag/revision expression resolution.
- Allowlisted subject inspection commands: `rev-parse --show-object-format=storage`, `cat-file -t <sha>`, `ls-tree -r -z -l --full-tree <sha>`. Use fixed argv, explicit local git-dir, no shell, replacement objects disabled, lazy fetch disabled, sanitized config/environment, bounded time/output/entry count, no credential prompts, no checkout/fetch/install/execute. `ls-tree -l` returns blob sizes without returning file contents to Scout. Git may internally access objects to obtain sizes; do not claim zero object access.
- SHA-256 rejection fixture; explicit command-allowlist assertion; metadata-only test with hostile README, executable canaries, symlink and gitlink handling. Canary results establish that this inventory slice never reads source content into its application logic or executes repository code; not proof of safe future content parsing or prompt-injection resistance. Later content extraction requires its own tests.
- Preserve prior P004 scope and D-005 constraints. P004 may start only after M0 gate evidence is present. No new architecture cycle. No PR head, main branch, ruleset, merge or product-code changes made by this audit.
