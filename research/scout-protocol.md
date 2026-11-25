# ARC Scout v0.1 — proposed M1 specification

Objective: source-grounded integration assessment of a bounded public Git repository at a pinned commit, without running its code or requiring paid inference. First user: developer assessing upstream dependencies. Local Python standard library + Git; optional model enrichment later. No browser acquisition, remote execution, arbitrary URLs, credentials or installed dependencies from scanned sources.

## Checked stages

1. Acquire: explicit HTTPS GitHub owner/repo and full SHA; isolated temporary bare repository with hooks, filters, submodules, credential helpers and external protocols disabled; bounded time/disk/process/memory; verify actual commit. No checkout. Reject unsupported input and redirects outside allowlist. Prove hardening before enabling network acquisition.
2. Inventory: git ls-tree and bounded cat-file reads; reject symlinks, submodules and unsafe names; no source execution. Manifest path, blob SHA, size and omissions. Begin with trusted synthetic local Git fixtures.
3. Extract: prefer vetted optional upstream adapters per [toolchain assessment](scout-toolchain.md); do not rebuild mature license/dependency analyzers. Inventory manifest paths as observations only; unsupported or unavailable analysis remains unknown. No legal conclusions or runtime claims.
4. Project: upstream System Map checked slices (inventory, catalog, nouns, actual processes, impact, reverify). Small tree: context and index only. Larger tree: evidenced cards. Keep live/leftover/ghost/undetermined independent of observed/inferred/unknown/contradicted. Observed declaration is not runtime proof. Claims cite commit, path, blob, line span; inference gives rationale and supporting IDs. Never mutate subject.
5. Assess: capability, evidence, constraints, license, compatibility, risk, integration option. Hard exclusions before ranking. Missing evidence unknown; no unsupported scores. Human chooses adopt/adapt/reference/reject/revisit.
6. Export: Markdown and JSON manifest, coverage, omissions, evidence and limitations; deterministic ordering; no secrets. HTML later with escaped text and no remote executable content. Failed checks stop advancement.

## Acceptance tests

FR-001 criteria S-1 to S-8 ([genesis review, section I](reviews/FR-001-genesis-review.md)), with FR-002 H-11 additions:

1. S-1 complete workspace for a pinned public repo with no API token and no paid service.
2. S-2 byte-identical regeneration from the same SHA and tool versions; timestamps only in a separate run record.
3. S-3 never executes repository code: malicious `setup.py`, npm `postinstall` and `Makefile` canaries never appear.
4. S-4 repository text is data: an instruction-bearing README is quoted, never acted on or cited as instruction.
5. S-5 every report claim resolves to path, lines and blob SHA (validator, 100%).
6. S-6 every inference cites at least one observation (schema rule, H-11).
7. S-7 fails loudly: unreachable, oversized, missing-tool, rate-limit, wrong-SHA and timeout fixtures each give an explicit error and an incomplete workspace, never a successful report.
8. S-8 declared licence matches hand-verified ground truth on every fixture (H-11).
9. Symlinks, submodules, oversized files and malformed manifests are handled explicitly; an unwired feature is never reported as runtime-verified.

Reference answers for ARC-EXP-001 come from at least two independent annotators, with agreement reported. The preregistration is a committed file whose commit SHA is recorded before any held-out data is collected (H-11).

## Early M1 step: adapter vetting (D-005)

Before any adapter output is used, vet ScanCode and Syft against the criteria in [D-005](../decisions/D-005-scout-toolchain.md): pinned release and digest, licence and data notices, offline and resource policy, hostile-input and canary fixtures, normalized output with source references. Each vetting run needs its own founder authorization; D-005 does not authorize installation or execution. Until an adapter passes, Scout reports licence and dependency assessment as unknown.

## ARC-EXP-001 (draft; preregister before data collection)

H1: im-ICM improves evidence-supported architecture and integration answer accuracy versus static inspection and native System Map; H0 no improvement. A raw pinned files; B deterministic inventory; C inventory plus native System Map; D same plus ARC evidence/integration matrix. Primary comparison C vs D. Same tasks, source versions, model/version if applicable, token/time budgets; count projection construction cost. Pilot 12 synthetic repos then at least 20 held-out public snapshots with independent reference answers; confirmatory sample size from pilot variance, not claimed powered. Randomize order, fresh sessions, blinded rubric, paired repo-level differences. Freeze rubric and minimally meaningful effect before held-out evaluation. Primary: correct supported answers / prespecified questions, missing answers incorrect. Secondary precision, coverage, unsupported claims, time, tokens, cost, reproducibility. Report paired bootstrap confidence intervals by repo, all failures, omissions, negative results. Security canary failure blocks release. If no incremental benefit, prefer native map. No measured results yet.

## First implementation order

Local fixture scanner and JSON manifest; safe pinned acquisition; deterministic extraction and compact map; evidence matrix/export; comparative experiment. Each step separately authorized and checked. No product code until PUSH 003 is merged, the M1 entry gates in [governance](../GOVERNANCE.md) are recorded as met, and the step is separately authorized. M3 needs the F-03 sandbox; M5 needs F-01 logging and F-02 utility.
