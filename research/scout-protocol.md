# ARC Scout v0.1 — proposed M1 specification

Objective: source-grounded integration assessment of a bounded public Git repository at a pinned commit, without running its code or requiring paid inference. First user: developer assessing upstream dependencies. Local Python standard library + Git; optional model enrichment later. No browser acquisition, remote execution, arbitrary URLs, credentials or installed dependencies from scanned sources.

## Checked stages

1. Acquire: explicit HTTPS GitHub owner/repo and full SHA; isolated temporary bare repository with hooks, filters, submodules, credential helpers and external protocols disabled; bounded time/disk/process/memory; verify actual commit. No checkout. Reject unsupported input and redirects outside allowlist. Prove hardening before enabling network acquisition.
2. Inventory: git ls-tree and bounded cat-file reads; reject symlinks, submodules and unsafe names; no source execution. Manifest path, blob SHA, size and omissions. Begin with trusted synthetic local Git fixtures.
3. Extract: prefer vetted optional upstream adapters per [toolchain assessment](scout-toolchain.md); do not rebuild mature license/dependency analyzers. Inventory manifest paths as observations only; unsupported or unavailable analysis remains unknown. No legal conclusions or runtime claims.
4. Project: upstream System Map checked slices (inventory, catalog, nouns, actual processes, impact, reverify). Small tree: context and index only. Larger tree: evidenced cards. Keep live/leftover/ghost/undetermined independent of observed/inferred/unknown/contradicted. Observed declaration is not runtime proof. Claims cite commit, path, blob, line span; inference gives rationale and supporting IDs. Never mutate subject.
5. Assess: capability, evidence, constraints, license, compatibility, risk, integration option. Hard exclusions before ranking. Missing evidence unknown; no unsupported scores. Human chooses adopt/adapt/reference/reject/revisit.
6. Export: Markdown and JSON manifest, coverage, omissions, evidence and limitations; deterministic ordering; no secrets. HTML later with escaped text and no remote executable content. Failed checks stop advancement.

## Proposed acceptance tests (not Claude's unavailable exact eight)

1. Known synthetic fixture: exact inventory and commit.
2. Repeat: byte-stable normalized output excluding timestamps.
3. Unwired feature never runtime verified.
4. Observed claims resolve to pinned source; inference labeled.
5. Malicious README and executable canaries never executed.
6. Symlink, submodule, oversized file, malformed manifest explicitly handled.
7. Wrong SHA, timeout and quota failure never yield successful report.
8. Offline fixture run without paid APIs; independent reproduction.

## ARC-EXP-001 (draft; preregister before data collection)

H1: im-ICM improves evidence-supported architecture and integration answer accuracy versus static inspection and native System Map; H0 no improvement. A raw pinned files; B deterministic inventory; C inventory plus native System Map; D same plus ARC evidence/integration matrix. Primary comparison C vs D. Same tasks, source versions, model/version if applicable, token/time budgets; count projection construction cost. Pilot 12 synthetic repos then at least 20 held-out public snapshots with independent reference answers; confirmatory sample size from pilot variance, not claimed powered. Randomize order, fresh sessions, blinded rubric, paired repo-level differences. Freeze rubric and minimally meaningful effect before held-out evaluation. Primary: correct supported answers / prespecified questions, missing answers incorrect. Secondary precision, coverage, unsupported claims, time, tokens, cost, reproducibility. Report paired bootstrap confidence intervals by repo, all failures, omissions, negative results. Security canary failure blocks release. If no incremental benefit, prefer native map. No measured results yet.

## First implementation order

Local fixture scanner and JSON manifest; safe pinned acquisition; deterministic extraction and compact map; evidence matrix/export; comparative experiment. Each step separately authorized and checked. No product code until P002 is merged and M0 acceptance gates in [governance](../GOVERNANCE.md) are satisfied.
