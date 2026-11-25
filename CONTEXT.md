# Project context

This file states the repository as it will be once the PR that last changed it merges (see [governance](GOVERNANCE.md)). GitHub is authoritative for actual repository state; the [event ledger](lineage/EVENTS.jsonl) records evidence of it. A gate counts as met only when the ledger records it. If a merge has no ledger receipt, verify it on GitHub and record the missing receipt.

**Current state:** **M0 is closed**: PR #3 merged as `bd7e488` (ARC-EVO-0043) and the closeout PR #4 as `a67c3c5` (ARC-EVO-0056, 0057), after FR-004 and FR-005 independent review. M1 entry evidence: two fresh Claude cold walks at 6/6 (ARC-EVO-0042, 0047; 0041 is the deterministic check) and the founder's deferral of the Codex cold walk (ARC-EVO-0048). PUSH 004 with its 004.1 corrections (PR #5, M1 step 1) adds the first Scout code: a deterministic, metadata-only inventory of one commit in a trusted local Git directory ([package](arc_scout/CONTEXT.md), [spec](research/p004-inventory-spec.md), [tests](tests/CONTEXT.md)). It is not a sandbox for hostile repositories and makes no licence, dependency or runtime assessment.
**Next permitted action:** M1 step 2, PUSH 005 (safe pinned remote acquisition, [Scout protocol](research/scout-protocol.md) stage 1), only with its own founder authorization. Each PR merges only after independent review by an agent that did not prepare it and separate founder merge authorization. The deferred Codex cold walk is run when an independent Codex environment is operational.
**May I implement Scout now?** Only a step the founder has separately authorized; PUSH 005 is not yet authorized. Research and decisions are not execution authority.
**History:** [lineage](lineage/CONTEXT.md). **Authority:** [governance](GOVERNANCE.md), [decisions](decisions/CONTEXT.md). **Reviews and open findings:** [research](research/CONTEXT.md).

| Milestone | Scope | Gate notes |
|---|---|---|
| M0 | Contextual foundation and review | Closed with the closeout PR (ARC-EVO-0050); Codex walk deferred (ARC-EVO-0048) |
| M1 | Scout local read-only discovery and im-ICM | Step 1 local inventory (PUSH 004); early step: vet ScanCode and Syft adapters (D-005) |
| M2 | Capability contracts | No weighted utility ranking until the F-02 utility P1 is resolved |
| M3 | Governed execution | Blocked by sandbox-sequencing P1 (F-03) |
| M4 | Optional local model intelligence | |
| M5 | Adaptation experiments | Blocked by logging (F-01) and utility-function (F-02) P1s |
| M6 | GitHub event responses | |
| M7 | Workbench and specialist lanes | |
| M8 | Reproducible public release | |

Check: a fresh agent answers the six cold-walk questions in [FR-003](research/reviews/FR-003-push-002-review.md) within AGENTS.md plus at most two further files per question.
