# D-005 — Scout toolchain policy

- **ID:** D-005
- **Date:** 2026-11-25
- **Status:** ratified
- **Proposer:** implementing agent (ChatGPT), from the FR-002 H-07 recommendation
- **Authority:** founder authorization of PUSH 003 scope, 2026-11-25 (ledger event ARC-EVO-0031)
- **Supersedes:** none
- **Affected paths and milestones:** [research/scout-toolchain.md](../research/scout-toolchain.md), [research/scout-protocol.md](../research/scout-protocol.md); M1

## Problem

Scout needs licence and dependency evidence. Re-implementing mature analyzers conflicts with the integration doctrine; installing them unvetted adds supply-chain and execution risk.

## Decision

| Upstream | Decision |
|---|---|
| ICM Architect | Adopted (D-004), pinned at `8bc2f5610d3843b3ffa31a142effe6b6337fef3c` |
| ScanCode Toolkit | Optional adapter, subject to vetting |
| Syft | Optional adapter, subject to vetting |
| OSV-Scanner | Deferred until a bounded vulnerability stage |

This decision does not authorize installing or executing any adapter. Vetting ScanCode and Syft is an early, separately authorized M1 step.

## Alternatives considered

Write stdlib licence and dependency parsers (rejected: rebuilds mature tools, likely less accurate); install all three tools now (rejected: unvetted dependencies); report licences as unknown indefinitely (rejected: removes much of Scout's value).

## Rationale

Follows the integration hierarchy while keeping the baseline free of mandatory dependencies.

## Consequences and residual risk

Until vetting completes, Scout reports licence and dependency assessment as unknown. Adapters add third-party code to the trust boundary once adopted.

## Verification

Before adoption of each adapter: pinned release and digest; licence and data-notice review; hostile-input and canary tests; offline operation; normalized output with source references; no execution or installation of scanned code. Implementation: pending.
