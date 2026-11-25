# FR-002 — PUSH 001 independent review

Nov 25, 2026 · Reviewer: Claude (independent review) · Commissioned by: Thomas Hogan (founder)

## Merge disposition

**APPROVE FOR MERGE. No P0 or P1 findings; no correction is required before merging `a35fb1b`.** The candidate is documentation plus one byte-identical vendored script; nothing executes, and every defect found is a record or routing correction that the project's own append-and-supersede rule can fix in PUSH 002 without rewriting history.

The candidate resolves FR-001's G-01 (D-001), represents D-002 Rev. 1 honestly, adopts Apache-2.0 correctly, and fixes the G-04 and G-05 structure findings. Its link check passes and demonstrably catches failures.

**What it does not yet achieve:** the cold walk answered only 2 of 6 routing questions within the entry file plus two reads (H-01); a Codex cold walk has not been run; and one carried P1 is assigned to the wrong milestone gate (H-04). These are PUSH 002 work and should be done before M1 starts, as GOVERNANCE.md already requires.

**Residual risk under D-002 Rev. 1 (not reopened):** `main` is unprotected and authorization is procedural, as the candidate itself states. A ruleset requiring a pull request before merging, with zero required approvals, is compatible with the single-account decision and would make interim control 7 technical (H-08).

## Exact SHA, files and tests

**Reviewed commit `a35fb1b2209f945fc65023b69f93e9817ef2d2bd`, parent `605ee8902a0984d7589c1a81c081f8c87930102a`, head of `push-001-icm-foundation` and of PR #1 (open, draft, no reviews, no checks).** `main` still points at the genesis commit. Fetched read-only by SHA; nothing was written to the repository.

**Files examined:** all 23 changed paths, read in full: `.github/CODEOWNERS`, `.github/pull_request_template.md`, `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `GOVERNANCE.md`, `LICENSE`, `README.md`, `_tools/LICENSE-icm-architect`, `_tools/links.py`, `decisions/` (5 files), `lineage/` (3 files), `research/` (5 files). Diff against the base: 554 insertions, 69 deletions, no deletions of files.

### Tests actually executed

| # | Test | Command or method | Result |
| --- | --- | --- | --- |
| T1 | Link and input check | `python3 -I _tools/links.py` (Python 3.13.18), repo root | `17 files, 33 links and inputs checked, 0 broken`; exit 0 |
| T2 | Negative control for T1 | Same script on a scratch copy with one broken link added to `CONTEXT.md` | `1 broken`, named `does-not-exist.md`; exit 1. The checker does detect failures |
| T3 | Vendored script identity | `cmp` against ICM Architect at `8bc2f5610d3843b3ffa31a142effe6b6337fef3c` | Byte-identical; blob `2f363aed` matches upstream `scripts/links.py` |
| T4 | Vendored licence identity | `cmp` against upstream `LICENSE` at the same commit | Byte-identical; blob `11070c9a` |
| T5 | Apache-2.0 text | Token diff against the LICENSE files of two Apache-2.0 projects | Identical except `https` vs `http` in the appendix URL; canonical terms |
| T6 | Lineage file parses | `json.loads` per line of `lineage/EVENTS.jsonl` | 17 events, IDs sequential 0001–0017; keys `id`, `date`, `event`, `status`, `commit` |
| T7 | Cold walk, Claude | Fresh agent with no conversation context, read-only, entry from `AGENTS.md` | Section below |

**Not executed:** a Codex cold walk (no Codex session available here); any repository-settings check (GitHub API unavailable to this session). `links.py` skips `.github/` and does not check `.jsonl` files or external URLs, so T1 says nothing about those.

## Cold-walk results

**Claude cold walk: 2 of 6 questions answered within AGENTS.md plus two reads; the FR-001 acceptance criterion is not yet met.** A separate agent with no access to this conversation entered at `AGENTS.md`, read one file at a time, and stopped at its 12-read limit. It modified nothing.

Read order: `AGENTS.md`, `CONTEXT.md`, `GOVERNANCE.md`, `decisions/CONTEXT.md`, `decisions/D-002-authority.md`, `research/CONTEXT.md`, `research/scout-protocol.md`, `lineage/CONTEXT.md`, `lineage/ORIGIN.md`, `research/FR-001.md`, `lineage/EVENTS.jsonl`, `decisions/D-001-icm-scope.md`.

| Question | Answered at read | Within 3? | Notes |
| --- | --- | --- | --- |
| Q1 What is it; is there working software? | 2 | Yes | Status clear; what the project *is* only clear at read 7, because the entry files never route to README |
| Q2 Who authorizes and merges; enforced? | 1, confirmed at 3 | Yes | Correctly understood as procedural, `main` unprotected |
| Q3 Where and how to record a decision? | 4 (place only) | Partly | No template or required fields; format had to be inferred |
| Q4 Next permitted action and prerequisites? | 10 | No | Had to combine four files; noted the Section J gate cannot be met from the repo |
| Q5 May I start Scout now? | 7 | No | Correct answer (no), but only found in the Scout spec |
| Q6 Origin history; proposal vs implemented? | 9 | No | Found, with status per event |

The agent also reported, independently of this review: decision IDs written "D-1 to D-3" in lineage but `D-001` in `decisions/`; ARC-EVO-0013 left `pending` after D-002 Rev. 1 replaced it; undefined status vocabulary; milestones M0–M8 used without definition in any routed file; governance text repeated across AGENTS.md, GOVERNANCE.md and D-002; ORIGIN.md and EVENTS.jsonl holding the same 17 items.

**Codex cold walk:** not run; no Codex session was available to this review.

### Exact cold-walk questions (ARC-EXP-000 instrument)

The fresh agent received these questions verbatim, with instructions to start at `AGENTS.md`, read one file at a time, log every read, stop after at most 12 reads, modify nothing and not use the web:

- Q1. What is this project, and what is its current status (is there working software)?
- Q2. Who may authorize and merge changes, and is that technically enforced on GitHub or only procedural?
- Q3. Where do I record a new decision, and in what format?
- Q4. What is the next permitted action / next piece of work, and what must happen before it can start?
- Q5. If I were asked to start implementing the "Scout" tool right now, am I permitted to? Cite the file that says so.
- Q6. Where is the history of how the project originated, and how is a proposal distinguished from something implemented?

Pass criterion: each question answered correctly within AGENTS.md plus two further reads (read count ≤ 3).

## Reconciliation against FR-001 and the review objectives

### Section J manifest

| Section J item | Candidate | Verdict |
| --- | --- | --- |
| README modified, human-facing | Done; chronology and authority moved out; ICM Architect credited for the primitives | Met |
| AGENTS.md, routing only, under 60 lines | 3 lines; delegates all routing to CONTEXT.md | Met on size; routing weak (H-01) |
| CLAUDE.md = `@AGENTS.md` | Exactly | Met |
| CONTEXT.md, the development sequence | Routes to four shelves; sequence lives in GOVERNANCE.md | Partly met |
| `_shared/governance.md` | `GOVERNANCE.md` at root | Acceptable deviation; single home intended |
| `_templates/decision.md` | Absent | Not met (H-02) |
| `_tools/links.py` with attribution | Byte-identical file plus a separate upstream MIT notice | Met, better than specified |
| Decision records | D-001 to D-004 | Met; D-002 summarized rather than recorded verbatim (H-06) |
| `lineage/events.jsonl` with type, actor, refs, supersedes | `EVENTS.jsonl` with id, date, event, status, commit | Partly met (H-03) |
| `research/register.md` | `REFERENCES.md`, 6 entries | Partly met (H-12) |
| Not created: CATALOG.md, `_core/` and other underscore work folders | None created | Met |
| Additions not in Section J | `.github/CODEOWNERS`, PR template, `research/scout-protocol.md`, `research/icm-architect.md`, `lineage/ORIGIN.md` | Acceptable; ORIGIN.md duplicates EVENTS (H-03) |

### Objectives

| # | Objective | Result |
| --- | --- | --- |
| 1 | Reconcile 23 files against Section J | Above. The implementer did not have Section J (stated in `research/FR-001.md`); H-05 fixes that gap |
| 2 | ICM fidelity and simplicity | Good: one catalog per shelf, pointer CLAUDE.md, no speculative folders. Gaps: entry file does not route by task; shelves have no templates |
| 3 | Fresh cold walk | Done for Claude: 2 of 6 within criterion. Codex not run |
| 4 | D-002 representation | Accurate in substance: procedural only, `main` unprotected, no claim of enforced review, triggers listed. Not the founder's verbatim text (H-06) |
| 5 | Vendored utility and MIT notice | Verified byte-identical to upstream `8bc2f56` (T3, T4) |
| 6 | `links.py` output | `17 files, 33 links and inputs checked, 0 broken`, exit 0 (T1); negative control fails correctly (T2) |
| 7 | Scout implementation and protocol | Strong safety design: bare repository, no checkout, hooks and submodules disabled, data-only parsing. Concerns: licence and dependency detection re-implemented rather than integrated (H-07); two acceptance tests missing (H-11) |
| 8 | Later P1s recorded and gated | Recorded, but the logging P1 is assigned to M3 when it belongs to M5 (H-04) |
| 9 | Lineage distinguishes proposal, ratification, implementation | Yes per event; only the genesis commit is marked implemented. Vocabulary undefined and one stale pending event (H-03) |
| 10 | Corrections before merge | None required; see PUSH 002 |

## Findings

**No P0; no P1; 8 P2; 6 P3.** None blocks merge. The P2s should be resolved, or explicitly deferred with a reason, before M1 starts.

| ID | Sev | Location | Finding and consequence | Correction | Acceptance test |
| --- | --- | --- | --- | --- | --- |
| H-01 | P2 | AGENTS.md, CONTEXT.md | Entry routes only to CONTEXT.md and GOVERNANCE.md; no route by task, no current-state line, milestones undefined in routed files. Cold walk: Q4 took 10 reads, Q5 7, Q6 9 | AGENTS.md gets a short "if you need X, go to Y" table; CONTEXT.md gets a current-state and next-permitted-action line and the milestone list with gates | Fresh Claude and Codex walks answer all six questions within AGENTS.md plus two reads |
| H-02 | P2 | `decisions/` | No decision template or required fields; format had to be inferred | `_templates/decision.md`: id, title, status (proposed, ratified, superseded), dates, decider, context, decision, consequences, supersedes, effective-in commit | Every decision record validates against the template's fields |
| H-03 | P2 | `lineage/` | Status vocabulary undefined (`recorded` covers proposals and receipts); no actor, refs or supersedes fields; ARC-EVO-0013 left `pending`; "D-1 to D-3" vs `D-001`; ORIGIN.md and EVENTS.jsonl both hold the full list | Define vocabulary in `lineage/CONTEXT.md`; add fields to new events; append a supersession event for 0013 and a correction event for the ID naming; make ORIGIN.md narrative only, or generated from EVENTS | Schema check passes; no event lacks a defined status; one home for the event list |
| H-04 | P2 | `research/FR-001.md` | States that the logging P1 blocks M3. Logging concerns comparing selection policies, which is M5. My FR-001 wording ("block M3 and M5") did not map each P1 to a gate; that ambiguity is mine | Record each carried P1 separately: F-01 logging → M5; F-02 utility definition → M5, and no weighted utility in M1–M2 ranking until defined; F-03 sandbox → before any execution of generated code (M3) | Each P1 appears once with its text, gate and source |
| H-05 | P2 | GOVERNANCE.md, `research/FR-001.md` | The governing reviews live outside the repo; the implementer did not have Section J, so a GOVERNANCE gate ("reconcile Section J") cannot be met from repository records | Commit FR-001 and FR-002 as exported Markdown under `research/reviews/` | Every gate in GOVERNANCE.md points to a file in the repo |
| H-06 | P2 | `decisions/D-002-authority.md` | Summarizes D-002 Rev. 1 rather than recording it: the eight interim controls, six triggers and accepted-limitation sentence are condensed, and "bifurcate upon stoppage" is not the founder's wording | Record the founder's ratified text verbatim, with the summary below it | Text matches the founder's issued amendment |
| H-07 | P2 | `research/scout-protocol.md` | Licence and dependency extraction are planned as new stdlib parsers, re-implementing what ScanCode, Syft and OSV-Scanner do; this tests the integration doctrine and is likely less accurate | Keep stdlib acquisition and inventory (the safety design is sound). For licence and SBOM, record an adopt or defer decision per tool; if deferred, include the tool as a comparison arm in ARC-EXP-001 | Upstream decision records exist for each tool |
| H-08 | P2 (residual) | GitHub settings | `main` unprotected, as declared. Not reopening D-002 | Ruleset on `main`: require a pull request, zero required approvals; scope any agent token to this repo with contents and pull-request permissions and an expiry | A direct push to `main` is rejected |
| H-09 | P3 | AGENTS.md, README, GOVERNANCE.md, D-002, FR-001.md, PR template | The single-account limitation and authority rules are restated in up to six places with slightly different wording | GOVERNANCE.md holds the rules; others link | Spot check finds one statement per rule |
| H-10 | P3 | `.github/CODEOWNERS` | `* @bzenny` has no effect without protection; the PR template already says so | Keep, but note it is inert until H-08 | None |
| H-11 | P3 | Scout tests, ARC-EXP-001 | Missing: declared-licence accuracy against hand-verified fixtures; a schema rule that every inference cites an observation. Reference answers need at least two independent annotators with agreement reported; preregistration location unstated | Add both tests; name the annotation procedure and freeze the preregistration by commit SHA | Tests listed; prereg file and SHA recorded before held-out data |
| H-12 | P3 | `research/REFERENCES.md` | 6 entries against FR-001's verified register; the contextual-bandit link is Li et al. 2010, while the regret bound is Chu et al. 2011 | Import the FR-001 register | Register lists both bandit papers with roles |
| H-13 | P3 | LICENSE, README | No copyright line for ARC-owned material | Add one line to README or a NOTICE file | Present |
| H-14 | P3 | `lineage/EVENTS.jsonl` | ARC-EVO-0015 ("no remote write") is overtaken by the branch push and PR #1; neither is recorded | Append events for the push, PR #1, FR-002 and the merge | Events present with commit refs |

## PUSH 002 scope

**PUSH 002 should be one documentation-only pull request that closes H-01 to H-07 and the chosen P3s, records FR-002, and runs both cold walks. No Scout code.** M1 starts after it merges.

| Path | Action | Closes |
| --- | --- | --- |
| `AGENTS.md` | Add a route-by-task table (status, next action, decisions, reviews, lineage, Scout spec, milestones); stay under 60 lines | H-01 |
| `CONTEXT.md` | Add current state, next permitted action, milestone list with gates and blockers | H-01, H-04 |
| `_templates/decision.md` | Create | H-02 |
| `decisions/D-002-authority.md` | Founder's Rev. 1 text verbatim, summary below | H-06 |
| `decisions/D-005-…` (optional) | Adopt or defer ScanCode, Syft, OSV-Scanner for Scout | H-07 |
| `lineage/CONTEXT.md` | Status vocabulary and event fields | H-03 |
| `lineage/EVENTS.jsonl` | Append only: push and PR #1, FR-002 received, PUSH 001 merge with SHA, supersession of 0013, ID-naming correction | H-03, H-14 |
| `lineage/ORIGIN.md` | Narrative only, or generated from EVENTS | H-03 |
| `research/reviews/FR-001.md`, `FR-002.md` | Founder exports from this doc | H-05 |
| `research/FR-001.md` | Per-P1 table with gates (F-01 → M5, F-02 → M5 and no weighted ranking before, F-03 → before generated-code execution) | H-04 |
| `research/scout-protocol.md` | Two added tests; annotation and preregistration procedure; tool decision reference | H-07, H-11 |
| `research/REFERENCES.md` | Import FR-001 register | H-12 |
| `.github/workflows/links.yml` (optional) | Run `links.py` on `pull_request`; `permissions: contents: read`; actions pinned by full SHA | Interim control 5 |

**Not a file change, but recommended now:** the `main` ruleset and scoped token in H-08.

**PUSH 002 acceptance:** `python -I _tools/links.py` exits 0; fresh Claude and Codex cold walks each answer all six questions within AGENTS.md plus two reads, with logs attached to the PR; every EVENTS line parses and uses defined statuses; each governance rule appears in one file; Claude reviews the exact head SHA before founder merge.
