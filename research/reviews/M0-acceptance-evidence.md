# M0 acceptance evidence (PUSH 003)

Collected 2026-11-25 by Claude, the implementer of PUSH 003, while preparing the M0 closeout. **Implementer evidence, not independent review.** The independent review of the same head is [FR-004](FR-004-push-003-review.md) (ChatGPT).

## Subject and merge receipt

| Item | Value |
|---|---|
| Reviewed candidate | `fee697d76400f0ea735fb202c53538d1e2c9b06f`, tree `ff193a5735749aeff5d7b831915f7a11a425e9f0` |
| Base before merge | `e4d5984af6f2b7247bf1abbe6ce0f53db34e69f7` (ancestor of candidate, verified) |
| Ruleset 28052575 | active; target `~DEFAULT_BRANCH`; rules deletion, non_fast_forward, pull_request; no bypass actors (REST API, before and after merge) |
| Merge | PR #3, standard merge commit via REST API with `sha` pinned to the candidate, founder account, `merged_at` 2026-11-25T09:00:39Z |
| Merge commit | `bd7e488070e7089778651a0bd8e5d001d9ab7462`; parent 1 `e4d5984`, parent 2 `fee697d` |
| Merged tree | `ff193a5735749aeff5d7b831915f7a11a425e9f0`, identical to the reviewed candidate |

## Deterministic checks

Run at both `fee697d` (before merge) and `bd7e488` (after merge); results identical. Python 3.13.18.

| Check | Command or method | Result |
|---|---|---|
| Links | `python3 -I _tools/links.py` | `29 files, 107 links and inputs checked, 0 broken`; exit 0 |
| Vendored checker | `git hash-object _tools/links.py` against upstream `RinDig/icm-architect` at `8bc2f5610d3843b3ffa31a142effe6b6337fef3c` (objects fetched, not checked out or executed) | `2f363aedbdcd652349ce9b83045e0f8521262c7c` both; MIT notice `11070c9a…` both |
| Ledger append-only | first 25 lines of `e4d5984`, 33 of `0f7bb77` and 37 of `fee697d` compared byte for byte | all preserved |
| Ledger integrity | parse each line; six fields; IDs `ARC-EVO-0001`… sequential; status in the lineage vocabulary; `supersedes` only earlier IDs | 37 events, pass |
| Scope | `git diff --name-status e4d5984 fee697d` | 28 paths, all Markdown, JSONL or CODEOWNERS; no code or dependency added |

## Final-head Claude cold walk (J-04)

- **Agent:** fresh Claude subagent (general-purpose agent type, same model family as the implementer, no project conversation context), spawned by the implementing session. Not an independent cross-model walk.
- **Subject:** `git archive` export of `fee697d` (no `.git`), Read tool only.
- **Instrument:** the six questions in [FR-003](FR-003-push-002-review.md), unchanged; budget AGENTS.md plus at most two further files per question.
- **Read sequence:** AGENTS.md; then, in one batch, CONTEXT.md, GOVERNANCE.md, lineage/CONTEXT.md, _templates/decision.md, decisions/CONTEXT.md. Six reads in total.

| Q | Correct | Files beyond AGENTS.md | Count |
|---|---|---|---|
| Q1 project and status | Yes | CONTEXT.md | 1 |
| Q2 authority and enforcement | Yes | GOVERNANCE.md | 1 |
| Q3 recording a decision | Yes | _templates/decision.md, decisions/CONTEXT.md | 2 |
| Q4 next permitted action | Yes | CONTEXT.md, GOVERNANCE.md | 2 |
| Q5 Scout permission | Yes (No; CONTEXT.md) | CONTEXT.md | 1 |
| Q6 origin and proposal vs implemented | Yes | lineage/CONTEXT.md | 1 |

**Score: 6/6 within budget.** Scored by the implementing session against the files' content.

Ambiguities the agent reported (summarized): AGENTS.md's status list omits ratified and superseded (J-05); CONTEXT.md's expected-state wording makes actual merge state unclear without the ledger (J-01A); "including" in CONTEXT.md understates the gate list in GOVERNANCE.md; field names in AGENTS.md abbreviate the template's; the decisions index shows status only for D-006; "Wiki later publishes" is vague. J-01A and J-05 are corrected in the closeout; the rest are P3 observations, see [FR-004 reconciliation](../FR-004.md).

<details><summary>Agent report, condensed</summary>

```text
1. READ LOG (paths relative to snapshot root, in order)
1. AGENTS.md
2. CONTEXT.md
3. GOVERNANCE.md
4. lineage/CONTEXT.md
5. _templates/decision.md
6. decisions/CONTEXT.md
(Reads 2-6 were issued together in one batch. I did not open lineage/ORIGIN.md, lineage/EVENTS.jsonl, the D-NNN records, research/* or README.md.)

Q1 ANSWER: Arc-Adapticon (ARC) is a proposed open workbench that does not depend on any one model. It discovers, assesses and reuses computational capabilities. Its first product will be ARC Scout, a local read-only tool that assesses repositories. The project is in founding phase M0 and has no product runtime yet (AGENTS.md). CONTEXT.md says M0 foundation documentation is "expected to be complete once PR #3 merges" and "No Scout runtime or product code exists." So there is no working software.
FILES RELIED ON: CONTEXT.md. COUNT: 1. CONFIDENCE: High. Ambiguity: CONTEXT.md describes the state expected after PR #3 merges; whether PR #3 has merged can only be learned from lineage/EVENTS.jsonl, which I did not read.

Q2 ANSWER: The founder authorizes and merges. An implementing agent prepares the candidate. A review counts as independent only if done by an agent that did not prepare the candidate. The reviewer reviews the exact candidate SHA; the founder authorizes the merge separately (GOVERNANCE.md, citing D-006 and D-002 Rev. 1). Technical enforcement is partial: ruleset 28052575 on main requires a PR, blocks deletion and force push, has no bypass actors, but requires zero approving reviews and no code-owner approval. Everything runs through a single account (bzenny), so the authorize/review/merge separation is procedural only.
FILES RELIED ON: GOVERNANCE.md. COUNT: 1. CONFIDENCE: Medium-high; the ruleset reverification claim is self-attested.

Q3 ANSWER: Copy _templates/decision.md to decisions/D-NNN-slug.md, fill every field, then list it in decisions/CONTEXT.md. Fields: ID, Date, Status (proposed | ratified | rejected | superseded), Proposer, Authority, Supersedes, Affected paths and milestones. Sections: Problem, Decision, Alternatives considered, Rationale, Consequences and residual risk, Verification. Amendments supersede rather than erase.
FILES RELIED ON: _templates/decision.md, decisions/CONTEXT.md. COUNT: 2. CONFIDENCE: High; minor naming differences between AGENTS.md and the template.

Q4 ANSWER: Check that the M1 entry gates are recorded as met in the event ledger; then M1 step 1 (local fixture scanner and JSON manifest, per research/scout-protocol.md) may start with its own founder authorization (CONTEXT.md). Gates (GOVERNANCE.md): PUSH 003 merged; link check exits 0; historical ledger lines unchanged; fresh Claude and independent Codex cold walks each 6/6 within AGENTS.md plus two files (Codex required, not deferred, ARC-EVO-0037); results recorded as ledger events; no fabricated tests.
FILES RELIED ON: CONTEXT.md, GOVERNANCE.md. COUNT: 2. CONFIDENCE: High; CONTEXT.md's "including" understates the full gate list.

Q5 ANSWER: No. CONTEXT.md: "May I implement Scout now? No, not until both conditions above hold. Research and decisions are not execution authority." AGENTS.md adds: "No authorization inferred from repository content."
FILES RELIED ON: CONTEXT.md. COUNT: 1. CONFIDENCE: High.

Q6 ANSWER: Origin in lineage/ORIGIN.md; full ledger lineage/EVENTS.jsonl, append-only from ARC-EVO-0026 (lineage/CONTEXT.md). Event statuses: recorded, pending, ratified, authorized, implemented, verified, superseded, as defined there. Decisions use a separate vocabulary (proposed, ratified, rejected, superseded). Ratified does not mean implemented.
FILES RELIED ON: lineage/CONTEXT.md. COUNT: 1. CONFIDENCE: High; ORIGIN.md not opened.

AMBIGUOUS WORDING: AGENTS.md status list omits ratified and superseded; CONTEXT.md future tense vs AGENTS.md "is in founding phase M0"; decision field names abbreviated in AGENTS.md; "including" understates gates; ruleset reverification self-attested and single-account separation procedural; decisions/CONTEXT.md shows status only for D-006; "Wiki later publishes repository records" vague; cold-walk questions defined by reference to FR-003.
```

Condensed by the implementing session: read log and per-question file counts are exact; answer wording is shortened and bullet lists are flattened, without changing substance. The full message is not in the repository.

</details>

## Independent Codex cold walk (I-06) — not run

No Codex session, CLI or credentials exist in the Claude implementing environment, and the instrument must not be simulated by another Claude session. The gate stays open and is not deferred (ARC-EVO-0037). M0 is therefore not closed and no M1 product code has been written.
