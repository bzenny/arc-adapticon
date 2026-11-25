# Review records

Independent reviews, one file per review. Records are evidence, not authority; decisions live in [decisions](../../decisions/CONTEXT.md).

| Review | Subject | Disposition | Record | Provenance |
|---|---|---|---|---|
| FR-001 | Genesis brief | APPROVE WITH REQUIRED CORRECTIONS | [genesis](FR-001-genesis-review.md) | Direct export of the reviewer's Claude Docs document |
| FR-001 supplement | Draft bundle v0.2.0 | See record | [supplement](FR-001-supplement-bundle-v0.2.0-review.md) | Reconstructed by the reviewing agent from the text it wrote into the document; not a byte export |
| FR-002 | PUSH 001 at a35fb1b | APPROVE FOR MERGE | [FR-002](FR-002-push-001-review.md) | Reconstructed by the reviewing agent from the text it wrote into the document; not a byte export |
| FR-003 | PUSH 002 at 574a906, addendum PUSH 002.1 at 4b91340 | APPROVE WITH NON-BLOCKING FINDINGS; addendum APPROVE FOR MERGE; M1 not yet | [FR-003](FR-003-push-002-review.md) | Authored in Markdown by the reviewing agent, addendum included |
| FR-004 | PUSH 003/003.1 at fee697d | APPROVE WITH NON-BLOCKING FINDINGS; addendum: exact-head checks pass; gates open | [FR-004](FR-004-push-003-review.md) | Verbatim PR #3 comment bodies fetched by REST API |

Implementer evidence (not review): [M0 acceptance evidence](M0-acceptance-evidence.md): merge receipt, deterministic checks, final-head Claude cold walk, Codex blocker.

Earlier partial summaries: [FR-001](FR-001.md), [FR-002](FR-002.md), both superseded. Reconciliations: [FR-001](../FR-001.md), [FR-002](../FR-002.md), [FR-003](../FR-003.md), [FR-004](../FR-004.md).

Reviewer for FR-001 to FR-003: Claude. PUSH 003 was prepared by Claude, so under [D-006](../../decisions/D-006-implementer-reviewer-separation.md) FR-004 came from ChatGPT. The M0 closeout is also prepared by Claude and needs review by another agent.
