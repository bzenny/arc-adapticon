# D-006 — Implementer and reviewer separation

- **ID:** D-006
- **Date:** 2026-11-25
- **Status:** proposed (becomes ratified if the founder merges PUSH 003; the merge event records it)
- **Proposer:** Claude, implementing PUSH 003, from the founder direction below
- **Authority:** founder direction to Claude, 2026-11-25: "beyond review capacity, if you have the ability to execute where chatgpt struggles, try to implment when directed." Recorded as ledger event ARC-EVO-0032.
- **Supersedes:** none (refines the role description in D-002 Rev. 1 interim control 3)
- **Affected paths and milestones:** [GOVERNANCE.md](../GOVERNANCE.md); all milestones

## Problem

D-002 Rev. 1 names ChatGPT as implementer and Claude as independent reviewer. The founder may now direct Claude to implement. A model cannot independently review a commit it prepared.

## Decision

Either agent may implement when the founder directs. A candidate's review counts as independent only when performed by an agent other than the one that prepared it. Tests and the founder's review remain the checks independent of both models.

## Alternatives considered

Keep Claude review-only (rejected by founder direction); allow self-review (rejected: not independent).

## Rationale

Preserves D-002's independent-review control while letting the founder use whichever agent can execute.

## Consequences and residual risk

When Claude implements, ChatGPT or Codex (or another agent with no part in preparing the candidate) reviews it. A fresh Claude instance with no project context can run cold walks and tests, but shares a model family with the implementer.

## Verification

Each PR names its implementing agent and its reviewer, and they differ. Implementation: PUSH 003 (PR #3) is the first push prepared by Claude.
