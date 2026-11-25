# Project context

This file states the repository as it is after its most recent merge. Every PR updates it to its own post-merge state (see [governance](GOVERNANCE.md)).

**Current state:** M0 foundation complete in documentation. PUSH 003 (PR #3, branch `push-003-final-contextual-foundation`) is the final documentation-only push; its merge commit is recorded in the [event ledger](lineage/EVENTS.jsonl). No Scout runtime or product code exists.
**Next permitted action:** Check that the M1 entry gates in [governance](GOVERNANCE.md) are recorded as met in the event ledger (fresh Claude and Codex cold walks 6/6, or a recorded founder deferral). Then M1 step 1 (local fixture scanner and JSON manifest, per the [Scout protocol](research/scout-protocol.md)) may start, but only with its own founder authorization.
**May I implement Scout now?** No, not until both conditions above hold. Research and decisions are not execution authority.
**History:** [lineage](lineage/CONTEXT.md). **Authority:** [governance](GOVERNANCE.md), [decisions](decisions/CONTEXT.md). **Reviews and open findings:** [research](research/CONTEXT.md).

| Milestone | Scope | Gate notes |
|---|---|---|
| M0 | Contextual foundation and review | Closes with PUSH 003 and the M1 entry gates |
| M1 | Scout local read-only discovery and im-ICM | Early step: vet ScanCode and Syft adapters (D-005) |
| M2 | Capability contracts | No weighted utility ranking until the F-02 utility P1 is resolved |
| M3 | Governed execution | Blocked by sandbox-sequencing P1 (F-03) |
| M4 | Optional local model intelligence | |
| M5 | Adaptation experiments | Blocked by logging (F-01) and utility-function (F-02) P1s |
| M6 | GitHub event responses | |
| M7 | Workbench and specialist lanes | |
| M8 | Reproducible public release | |

Check: a fresh agent answers the six cold-walk questions in [FR-003](research/reviews/FR-003-push-002-review.md) within AGENTS.md plus at most two further files per question.
