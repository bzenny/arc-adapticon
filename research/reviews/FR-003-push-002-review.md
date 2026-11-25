# FR-003 — PUSH 002 independent review

Nov 25, 2026 · Reviewer: Claude (independent review) · Commissioned by: Thomas Hogan (founder)

## Disposition

**Merge of PUSH 002: APPROVE WITH NON-BLOCKING FINDINGS. Readiness for M1: NOT YET.** No P0 or P1 findings. The candidate resolves H-02, H-04 and H-06, resolves H-03 and H-08 in substance, and improves routing from 2/6 to 3/6 questions answered within the read budget (4/6 under the FR-002 scoring). Nothing executes; no Scout runtime or dependency was added.

**One amendment is recommended before merge (founder's choice, not a blocker).** `GOVERNANCE.md` states that ruleset 28052575 targets all branches and tells agents to stop if feature-branch writes are blocked. The founder reports the ruleset now targets only the default branch. If merged as is, `main` carries a known-false statement in its authority file until PUSH 003. A two-line edit plus one appended lineage event fixes it; the new head then needs only a diff review.

**M1 cannot start yet** because three gates that GOVERNANCE.md itself sets are open: the Claude cold walk is 3/6, not 6/6; no Codex cold walk has been run; and the full review exports (H-05) are not yet committed. The exports are supplied with this review, so PUSH 003 can close all three.

## Exact SHA, files and tests

**Reviewed `574a9063a080d69d715c735d05065556ff3a5bad` (head of `push-002-context-optimization`, PR #2), base `d52afe68d5ecc59c887fa5d8353f33bfef293d45` (`main`, the merge of PR #1).** The PR #1 merge tree is identical to the FR-002-reviewed commit `a35fb1b` (empty diff). Fetched read-only; nothing was written to the repository.

**Files examined:** all 17 changed paths: `AGENTS.md`, `CONTEXT.md`, `GOVERNANCE.md`, `README.md`, `_templates/decision.md`, `decisions/CONTEXT.md`, `decisions/D-002-authority.md`, `lineage/CONTEXT.md`, `lineage/EVENTS.jsonl`, `lineage/ORIGIN.md`, `research/CONTEXT.md`, `research/FR-001.md`, `research/FR-002.md`, `research/reviews/FR-001.md`, `research/reviews/FR-002.md`, `research/scout-protocol.md`, `research/scout-toolchain.md`. Diff: 163 insertions, 58 deletions.

| # | Test | Method | Result |
| --- | --- | --- | --- |
| T1 | Link check | `python3 -I _tools/links.py` (Python 3.13.18) | `21 files, 52 links and inputs checked, 0 broken`; exit 0 |
| T2 | Ledger parse and schema | Python: parse every line; check sequential IDs, required fields, allowed statuses, `supersedes` is a list of earlier IDs | 24 events, IDs 0001–0024 sequential; all six fields present; all statuses in the defined vocabulary; one supersession (0016 → 0013), backward-pointing; no unresolved `pending` |
| T3 | D-002 Rev. 1 completeness | Each of the 18 sentences of the founder's issued amendment searched verbatim in `decisions/D-002-authority.md` | 18/18 present verbatim: decision (2), interim controls (8), migration triggers (6), accepted limitation (2) |
| T4 | No runtime code or mandatory dependency | Diff and tree scan for code, manifests, workflows | Only `_tools/links.py` (vendored, unchanged); no `requirements*`, `pyproject.toml`, `package.json` or workflows |
| T5 | Cold walk, Claude (ARC-EXP-000) | Fresh agent, no project context, same six questions as FR-002 | Below |

**Not executed:** Codex cold walk (no Codex session available to this reviewer); ruleset verification (GitHub API unavailable here; the ruleset state is founder-reported).

## ARC-EXP-000 — Cold-walk retest

**Strict result 3/6 within AGENTS.md plus two reads (Q2, Q4, Q5); 4/6 under the FR-002 scoring, which counted Q1 on status alone. Baseline 2/6.** All six answers were correct in the end. The agent read 10 files (about 182 lines in total) and modified nothing; its whole session consumed about 89,300 tokens, against about 86,600 for the FR-002 baseline run (tool overhead included in both).

**Exact questions** (identical to FR-002):

- Q1. What is this project, and what is its current status (is there working software)?
- Q2. Who may authorize and merge changes, and is that technically enforced on GitHub or only procedural?
- Q3. Where do I record a new decision, and in what format?
- Q4. What is the next permitted action / next piece of work, and what must happen before it can start?
- Q5. If I were asked to start implementing the "Scout" tool right now, am I permitted to? Cite the file that says so.
- Q6. Where is the history of how the project originated, and how is a proposal distinguished from something implemented?

**Read order:** `AGENTS.md` (16 lines), `CONTEXT.md` (22), `GOVERNANCE.md` (10), `decisions/CONTEXT.md` (12), `_templates/decision.md` (4), `lineage/ORIGIN.md` (4), `lineage/EVENTS.jsonl` (25), `research/CONTEXT.md` (11), `research/scout-protocol.md` (32), `decisions/D-002-authority.md` (46).

| Q | Correct? | Reads (FR-002 → FR-003) | Within 3? | Why not, if not |
| --- | --- | --- | --- | --- |
| Q1 | Yes | Status 2 → 2; what it is 7 → 6 | Status yes; description no | No one-line description of the project in AGENTS.md or CONTEXT.md, and no route to README |
| Q2 | Yes | 3 → 3 | Yes | Now correctly reports the ruleset and that approvals are procedural |
| Q3 | Yes | Place 4, format not found → place 4, format 5 | No | AGENTS.md routes to `decisions/CONTEXT.md`, not to the template |
| Q4 | Yes | 10 → 2 | Yes | — |
| Q5 | Yes | 7 → 2 | Yes | — |
| Q6 | Yes | 9 → 6 | No | AGENTS.md links ORIGIN and EVENTS directly, skipping `lineage/CONTEXT.md`, which holds the status definitions |

**Ambiguities the agent reported:** two status vocabularies (events vs decision template) and D-002's status "Founder-authorized amendment" in neither; D-002 does not follow the new template; "D-4" still in event 0014; CONTEXT.md says "this P002 candidate" without naming a SHA or PR; the M0→M1 gate restated in CONTEXT, GOVERNANCE and the Scout protocol; the ruleset scope flagged as unresolved.

**Three one-line routing changes would likely reach 6/6:** a one-sentence project description at the top of AGENTS.md; a "Record a decision" row pointing to the template; and the history row pointing to `lineage/CONTEXT.md` first.

## Reconciliation of FR-002 findings

| Finding | Status in candidate | Verdict |
| --- | --- | --- |
| H-01 routing | Route table, current state, next action, milestone table | **Partly resolved**: 3/6 strict (from 2/6); see I-03 |
| H-02 decision template | `_templates/decision.md` with required fields | **Resolved**; it is a field list rather than a copyable skeleton, and D-002 does not yet follow it (P3) |
| H-03 lineage schema | Vocabulary defined; `supersedes` field; 0013 superseded by 0016; ORIGIN narrative only; 0011 normalized | **Resolved in substance**; 0014 still "D-4"; in-place migration of 0001–0017 has no event (I-05) |
| H-04 P1 gates | CONTEXT.md: sandbox P1 at M3; logging and utility P1s at M5; repeated in FR-001.md and research/CONTEXT.md | **Resolved**. The FR-002 note "no weighted utility in M1–M2 ranking until defined" is not recorded (P3) |
| H-05 full review exports | Partial records only; marked open | **Open**; exports supplied with this review |
| H-06 D-002 verbatim | Full Rev. 1 text | **Resolved** (T3, 18/18) |
| H-07 toolchain | `research/scout-toolchain.md`: ScanCode and Syft adopt as optional adapters with installation deferred; OSV-Scanner deferred | **Resolved as a proposal**; needs founder ratification and an M1 vetting step (I-07) |
| H-08 main protection | Ruleset 28052575 active; documented | **Resolved by founder action**; documentation stale (I-01) |

| P3 | Status | Verdict |
| --- | --- | --- |
| H-09 duplicated rules | GOVERNANCE.md made canonical and links D-002; AGENTS no longer restates authority | Improved; M0→M1 gate and "untrusted content" still restated in three files |
| H-10 CODEOWNERS inert | Unchanged | Acceptable; still inert with zero required approvals |
| H-11 Scout tests and annotation | Not addressed (details were unavailable) | Open |
| H-12 register | `REFERENCES.md` unchanged | Open |
| H-13 copyright line | Not added | Open |
| H-14 push, PR and merge events | Events 0018–0024 appended | Resolved |

## Toolchain decisions (objective 8)

**The three decisions are sound.** ScanCode and Syft as optional, pinned adapters, not installed until vetted, follow the integration doctrine without adding a mandatory dependency. Deferring OSV-Scanner to a bounded vulnerability stage is reasonable, because its offline mode needs a separately obtained database.

**One gap:** the protocol says that without a vetted adapter, licence and dependency assessment is reported as unknown. Licence assessment is a large part of what makes Scout useful, so adapter vetting for ScanCode and Syft should be an explicit, early M1 step with its own acceptance tests: pinned release and digest, hostile-input canaries, offline operation, and normalized output with source references. The file correctly calls these proposals; they need a founder decision record before installation.

## Findings

**No P0; no P1; 7 P2; 4 P3.**

| ID | Sev | Location | Finding and consequence | Correction | Acceptance test |
| --- | --- | --- | --- | --- | --- |
| I-01 | P2 | GOVERNANCE.md; EVENTS 0023 | States the ruleset targets all branches and tells agents to stop if feature-branch writes fail; the founder reports it now targets the default branch only. The authority file would be false on `main` | Replace the sentence with the current configuration and its verification date; append an event recording the retarget that supersedes 0023 | Text matches the live ruleset; ledger check passes |
| I-02 | P2 | CONTEXT.md | Current state describes the candidate ("P002 is a documentation-only candidate"; next action "review and test this P002 candidate"). After merge, both lines are wrong, and the candidate is not named by PR or SHA | Write CONTEXT.md as it will be true after merge, naming the PR; add a governance rule that every PR updates CONTEXT.md to its post-merge state | Cold walk on `main` after merge reports the correct next action |
| I-03 | P2 | AGENTS.md | 3 of 6 routing questions answered within budget (Q1 description, Q3, Q6 fail) | Add a one-line project description; a "Record a decision" row to the template; route history through `lineage/CONTEXT.md` | Fresh Claude and Codex walks: 6/6 within AGENTS.md plus two reads |
| I-04 | P2 | Template, EVENTS, D-002 | Two status vocabularies (events vs decisions) not declared as separate; D-002 status in neither | State which vocabulary applies to which record type; set D-002 status to `ratified` (Rev. 1) | Every decision and event status is in its declared vocabulary |
| I-05 | P2 | `lineage/EVENTS.jsonl` | Events 0001–0017 rewritten in place (field added, 0011 text changed) on a ledger declared append-only; the migration is described in `lineage/CONTEXT.md` but not recorded as an event; 0014 still reads "D-4" | Append one event recording the schema migration and spelling normalization, with the commit; leave history unchanged from then on | Ledger check flags any change to a line already on `main` |
| I-06 | P2 | M1 gate | Codex cold walk not run; GOVERNANCE.md requires it before M1 | Run an independent Codex session with the exact six questions, or record a founder deferral | Logged result attached to the PUSH 003 PR |
| I-07 | P2 | `research/scout-toolchain.md` | Adapter decisions are proposals; without vetted adapters, Scout's first output reports licences as unknown | Founder decision record ratifying the toolchain plan; make ScanCode and Syft vetting an explicit early M1 step | Decision record exists; M1 plan lists the vetting step and its tests |
| I-08 | P3 | D-002 | The Rev. 1 text is labelled "not a verbatim founder quotation", but it matches the amendment the founder issued for review, sentence for sentence | Founder confirms and relabels it as the issued text | Label updated |
| I-09 | P3 | Scout protocol | FR-002 H-11 tests not yet added (licence accuracy against hand-verified fixtures; every inference cites an observation; two annotators; preregistration frozen by SHA) | Add, now that the details are available | Tests listed in the protocol |
| I-10 | P3 | REFERENCES.md, README | H-12 register import and H-13 copyright line still open | Import the FR-001 register; add a copyright line | Present |
| I-11 | P3 | FR-001.md, CONTEXT.md | "No weighted utility in M1–M2 ranking until F-02 is defined" not recorded | Add one line to the M2 row | Present |

## PUSH 003 scope

**PUSH 003 is the last documentation-only push before M1. It closes I-01 to I-07 and H-05, then reruns both cold walks.** No Scout code.

| Path | Change | Closes |
| --- | --- | --- |
| `GOVERNANCE.md` | Current ruleset configuration (default branch only) with verification date; rule that every PR updates CONTEXT.md to its post-merge state | I-01, I-02 |
| `CONTEXT.md` | Post-merge state naming PR #2's merge; next action "PUSH 003 review, then M1 step 1"; M2 row notes no weighted utility before F-02 | I-02, I-11 |
| `AGENTS.md` | One-line project description; "Record a decision" row to the template; history row via `lineage/CONTEXT.md` | I-03 |
| `_templates/decision.md`, `decisions/D-002-authority.md` | Declare decision vocabulary; D-002 status `ratified`; relabel the issued text after founder confirmation | I-04, I-08 |
| `decisions/D-005-scout-toolchain.md` | Founder ratification (or amendment) of the toolchain plan | I-07 |
| `lineage/CONTEXT.md` | Declare which vocabulary applies to events vs decisions | I-04 |
| `lineage/EVENTS.jsonl` | Append only: schema migration record; ruleset retarget verified (supersedes 0023); PR #2 opened; FR-003 received; PR #2 merged; FR-001/002/003 exports committed | I-01, I-05, H-05 |
| `research/reviews/` | Add `FR-001-genesis-review.md`, `FR-001-supplement-bundle-v0.2.0-review.md`, `FR-002-push-001-review.md`, `FR-003-push-002-review.md` exactly as supplied; mark the partial records superseded | H-05 |
| `research/scout-protocol.md` | H-11 tests; ScanCode and Syft vetting as an explicit early M1 step | I-07, I-09 |
| `research/REFERENCES.md`, `README.md` | Import the FR-001 register; add a copyright line | I-10 |

**PUSH 003 acceptance:** link check exits 0; ledger check passes with no changed historical lines; independent fresh Claude and Codex cold walks each answer all six questions within AGENTS.md plus two reads, with logs in the PR; Claude reviews the exact head SHA; founder authorizes merge. **M1 begins after that merge**, with Scout step 1 (local fixture scanner and JSON manifest) under its own authorization.

## Addendum — PUSH 002.1 bounded diff review

**APPROVE FOR MERGE at `4b913401c3438d14c327a9b6c8cea990ce60c8b2`. I-01 is resolved. Readiness for M1 is unchanged: not yet.** All other FR-003 findings (I-02 to I-11, H-05) remain assigned to PUSH 003.

| Check | Result |
| --- | --- |
| Parentage | `4b91340` has the single parent `574a906` (the previously approved head); PR #2 head and branch point at `4b91340`; `main` still at `d52afe6` |
| Scope | Diff touches exactly the two authorized paths: `GOVERNANCE.md` (1 line replaced) and `lineage/EVENTS.jsonl` (1 line appended); 2 insertions, 1 deletion |
| I-01 | The obsolete "~ALL and ~DEFAULT_BRANCH" sentence and its stop instruction are replaced by "only ~DEFAULT_BRANCH (main)", with the other ruleset settings unchanged. Resolved |
| Append-only | The first 24 lines are byte-identical to `574a906`; one line added |
| Event 0025 | Sequential ID; all six fields; status `verified`; `supersedes: ["ARC-EVO-0023"]`, which is earlier and exists |
| `python3 -I _tools/links.py` | `21 files, 52 links and inputs checked, 0 broken`; exit 0 |
| Ledger check (25 events) | IDs 0001–0025 sequential; statuses in the defined vocabulary; all supersession references point backward |

**Evidence limits:** I cannot read ruleset settings from here; the configuration is implementer-reported. One observation supports it: the feature branch was updated to `4b91340` while `main` did not move.

**Two P3 notes, for PUSH 003:** GOVERNANCE.md and event 0025 say "independently reverified", but the reverification was done by the implementing session, not an independent party; "reverified by the implementer" is accurate. Event 0025's `commit` field holds `574a906`, the head at verification time, not the commit that records the event; `lineage/CONTEXT.md` should say which meaning the field carries.
