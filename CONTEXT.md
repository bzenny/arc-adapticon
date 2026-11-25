# Project context

This file states the repository as it will be once the PR that last changed it merges (see [governance](GOVERNANCE.md)). GitHub is authoritative for actual repository state; the [event ledger](lineage/EVENTS.jsonl) records evidence of it. A gate counts as met only when the ledger records it. If a merge has no ledger receipt, verify it on GitHub and record the missing receipt.

**Current state:** M0 foundation documentation is complete: PR #3 merged as `bd7e488` (ARC-EVO-0043). The M0 closeout PR (#4) records acceptance evidence and the J-01A and J-05 corrections. M0 is **not closed**: the independent Codex cold walk (I-06) has not been run. No Scout runtime or product code exists.
**Next permitted action:** Run the independent Codex cold walk (six questions in [FR-003](research/reviews/FR-003-push-002-review.md)) against the current main head and record it in the ledger. When every M1 entry gate in [governance](GOVERNANCE.md) is recorded as met, record M0 closure; then PUSH 004, M1 step 1 (local inventory and JSON manifest, per the [Scout protocol](research/scout-protocol.md)), may start under the founder's conditional authorization (ARC-EVO-0040).
**May I implement Scout now?** No, not until all M1 entry gates are recorded as met. Research and decisions are not execution authority.
**History:** [lineage](lineage/CONTEXT.md). **Authority:** [governance](GOVERNANCE.md), [decisions](decisions/CONTEXT.md). **Reviews and open findings:** [research](research/CONTEXT.md).

| Milestone | Scope | Gate notes |
|---|---|---|
| M0 | Contextual foundation and review | PUSH 003 merged; closes when the M1 entry gates are recorded (Codex walk open) |
| M1 | Scout local read-only discovery and im-ICM | Early step: vet ScanCode and Syft adapters (D-005) |
| M2 | Capability contracts | No weighted utility ranking until the F-02 utility P1 is resolved |
| M3 | Governed execution | Blocked by sandbox-sequencing P1 (F-03) |
| M4 | Optional local model intelligence | |
| M5 | Adaptation experiments | Blocked by logging (F-01) and utility-function (F-02) P1s |
| M6 | GitHub event responses | |
| M7 | Workbench and specialist lanes | |
| M8 | Reproducible public release | |

Check: a fresh agent answers the six cold-walk questions in [FR-003](research/reviews/FR-003-push-002-review.md) within AGENTS.md plus at most two further files per question.
