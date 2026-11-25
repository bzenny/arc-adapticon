# FR-001 supplement — Review of draft bundle v0.2.0

Nov 25, 2026 · Reviewer: Claude (independent review) · Commissioned by: Thomas Hogan (founder)

Scope note: this review covers the pre-repository draft bundle ARC-001 to ARC-014 (v0.2.0). Its P1 findings F-01 to F-03 are the "later P1s" carried into the repository. Gate assignment as corrected in FR-002 (H-04): F-01 → M5; F-02 → M5 (and no weighted utility in M1–M2 ranking until defined); F-03 → before any execution of generated code (M3).

## Disposition

**Approve with revisions. Ratification of the full bundle is blocked by three P1 findings; there are no P0 findings.** All three P1s sit in the evolution and evaluation layer (ARC-006, ARC-007, ARC-010, ARC-012). The kernel, packaging, registry, security, product and decision documents are sound enough to govern M1–M3.

The bundle is a large improvement on the one-page brief. It already fixes most of what the brief-only review raised: policy checks now come before execution, "AI Synaptic Dynamism" is defined as a research construct, a capability manifest exists, a license is proposed and the cost rule is precise.

The three blocking findings:

1. **F-01: the logs cannot answer the research question.** ARC-012 logs selections from a deterministic policy without selection probabilities. Unbiased offline comparison of selection policies needs randomized or probability-logged choices.
2. **F-02: the utility function is not yet a measurement.** Q, R, F, C and L, their normalization and their weights are undefined. As written, the weights could be tuned after results are seen.
3. **F-03: the plan builds candidate generation before the sandbox it needs.** M6 generates candidates that must be executed to be evaluated, but the native sandbox arrives only at M8 and is marked optional. ARC-008 would then correctly disable execution, so M6 cannot pass its exit test.

**Recommended path:** ratify ARC-001, 003, 004, 005, 008, 009, 011, 013 and 014 for M1–M3 now, after the P2 corrections the founder accepts. Hold ARC-002, 006, 007, 010 and 012 until F-01 to F-03 are corrected and re-reviewed.

## What was reviewed

**This review covers the exact draft bundle supplied on 25 November 2026: README, ARC-001 to ARC-014 (all version 0.2.0, status draft), RESEARCH-REGISTER.md and the commission CLAUDE-REVIEW.md.** No commit exists for this draft, and the GitHub repository was still empty at review time.

| Evidence type | What it covers |
| --- | --- |
| Executed tests | None. No code exists to execute |
| Inspected evidence | All 17 files, read in full; the ARC-012 formulas checked by hand |
| Primary sources opened this session | 11 of the 14 register entries, plus 6 sources the register lacks (listed in Sources) |
| Not opened this session | W3C PROV, Microsoft human-AI guidelines, the Pyodide documentation (see Unverified evidence) |

Every finding below is a judgment about documents, not a test result. Where a finding relies on a source, the source is linked in the row.

## Findings

**3 P1 (block ratification), 10 P2 (resolve or explicitly defer), 6 P3 (minor). No P0.** Severity follows ARC-014.

### P1 — blocking

| ID | Location | Finding and consequence | Correction | Acceptance test |
| --- | --- | --- | --- | --- |
| F-01 | ARC-012 (LinUCB logging); ARC-007; ARC-002 | Logs hold context, candidates, selection and reward from a deterministic policy, with no selection probability. Replay evaluation of another policy is unbiased only when logged arms were chosen at random ([Li et al. 2011](https://arxiv.org/pdf/1003.5956)). Static-vs-adaptive conclusions drawn from these logs would be biased toward the policy that collected them | Benchmark tasks: run every policy on every sealed task as a paired, full-information comparison; no bandit is needed there. Live use: log each choice's selection probability and explore only through an explicitly randomized rule within authorized budgets | Every selection record carries a probability in (0, 1]. On a synthetic fixture with known rewards, the off-policy estimate of a second policy falls inside its interval around the true value |
| F-02 | ARC-012 (utility); ARC-002 | Q, R, F, C and L are never defined; normalization is unspecified; weights are "task-defined". Min-max scaling within the candidate set would make a capability's score depend on which rivals happen to be eligible. Weights set after results are seen would let the hypothesis be confirmed by tuning | Define each term: name, unit, source field, range. Normalize against fixed reference scales. Freeze weights per task family in the preregistration, and report results across a fixed sensitivity grid | Adding or removing an unrelated candidate never changes the order of the others. The preregistration digest includes the weights. A sensitivity table is produced automatically |
| F-03 | ARC-010 (M6 vs M8); ARC-006; ARC-008 | M6 generates candidates, which must run to be evaluated. ARC-008 allows generated code only in an isolated native runtime, else execution is disabled. That runtime arrives at M8 and is optional, so M6 cannot meet its exit test. Browser-side Python import restrictions are not a substitute: one research team found sandbox escapes in seven products that relied on them ([Cyera](https://www.cyera.com/research/sandcastles-not-sandboxes-how-one-architectural-flaw-exposed-seven-products)) | Make a named, per-OS native isolation mechanism an entry criterion of M6. State that the browser baseline runs approved capabilities only and never evaluates candidates | M6 cannot start until an escape suite passes: no reads outside the work directory, no network, CPU, memory and time limits enforced, no host secrets in the environment. The browser build contains no code path that executes candidate code |

### P2 and P3

| ID | Sev | Location | Finding and consequence | Correction | Acceptance test |
| --- | --- | --- | --- | --- | --- |
| F-04 | P2 | ARC-002; ARC-012; register | The cited regret bound is proved for SupLinUCB, a variant built for analysis, not for the LinUCB rule ARC-012 specifies ([Chu et al.](https://www.schapire.net/papers/bandit-lin.pdf); [survey](https://arxiv.org/pdf/1508.03326)). "After sufficient data" is undefined | Cite the exact algorithm and its assumptions; describe LinUCB here as a heuristic; define the data threshold numerically | Register entry names algorithm, setting and assumptions; threshold appears in config and is tested |
| F-05 | P2 | ARC-012 (Beta posterior) | Conjugate update is correct for exchangeable binary outcomes, but pooling across task families breaks that assumption. "Conservative defaults" and the ranking rule are unspecified | Keep posteriors per capability and task family; name the prior; rank on a stated lower posterior quantile | Fixtures with known expected order pass; prior and quantile appear in config |
| F-06 | P2 | ARC-007 | Six arms and several metrics, but no primary contrast, sample size, multiplicity control or budget unit that applies to non-LLM arms | One primary contrast; task count from a stated minimum effect; paired tests; Holm correction for secondaries; budget in wall-clock, memory and tokens | Analysis script recovers a planted effect on synthetic data; preregistration contains all four items |
| F-07 | P2 | ARC-006 | Evaluator freezing is stated, not enforced. The Darwin Gödel Machine authors observed objective hacking, and it was more frequent when detection functions were visible to the agent ([DGM](https://arxiv.org/pdf/2505.22954)) | Keep evaluator and holdout outside the candidate sandbox; pin the evaluator digest in each decision record | A candidate that tries to read holdout data or alter the evaluator is blocked and logged |
| F-08 | P2 | ARC-004 | Agent Skills requires only `name` and `description`; its `metadata` field is a string-to-string map, so ACP's nested schemas cannot live there ([spec](https://agentskills.io/specification)) | Put the ACP manifest in its own file beside SKILL.md; map ACP `id` to the spec's `name` rules | Every package passes both `skills-ref validate` and ACP schema validation |
| F-09 | P2 | ARC-004 exit | "Identical digest" needs a canonical form: file order, path normalization, exclusions, algorithm | Specify it, e.g. SHA-256 over sorted (path, bytes) pairs | Same package exported on two operating systems yields the same digest |
| F-10 | P2 | ARC-003 | Two runtimes double the selection logic and create parity work | Write registry and selection logic once in Python; run it in the browser through Pyodide in a worker; keep TypeScript for UI | One fixture gives byte-identical JSON in browser and native |
| F-11 | P2 | ARC-002; ARC-007 | "Static ICM" is used as a baseline, but the ICM preprint's abstract page reports no benchmarks or quantitative results; it describes a methodology ([ICM](https://arxiv.org/abs/2603.16021)) | Define every baseline operationally, as a runnable configuration | Each named baseline exists as a config and runs on the reference task |
| F-12 | P2 | ARC-002 | Closest prior art is missing from the comparison: ADAS, AFlow, DSPy and the DGM (see Prior art). DSPy and AFlow are in the register but not in ARC-002 | Add them to the originality analysis; use a DSPy-style optimizer as a comparator when a local LLM is present | Prior-art note reviewed before preregistration |
| F-13 | P2 | ARC-013 | "Bounded low-risk operations" may run under standing authorization, but low-risk is undefined | Enumerate allowed operation classes; everything else needs explicit approval | An unlisted operation is refused without explicit approval |
| F-14 | P3 | ARC-007 | Local GPU inference can differ across hardware and drivers, so "fixed model versions" alone may not reproduce runs | Record hardware, browser and runtime versions in the run manifest; state tolerances | Manifest schema includes these fields |
| F-15 | P3 | ARC-003 | Browser storage is best-effort and can be evicted ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)) | Request persistent storage; prompt for export | Restore test after simulated eviction |
| F-16 | P3 | ARC-009 | "Scheduled web discovery" brings untrusted content into candidate generation | Discovery output enters only as quarantined candidates | Injection fixture in discovered content cannot trigger any action |
| F-17 | P3 | ARC-001; ARC-005 | Many open-weight models carry non-OSI licenses; Apache-2.0 compatibility of dependencies is unaudited | License audit before ratifying Apache-2.0; registry blocks bundling incompatible weights | Audit file committed; bundling test refuses a restricted license |
| F-18 | P3 | ARC-011 | Stage names ("AI Synaptic Dynamism", "AI Directed") remain metaphorical | Add a glossary mapping each stage to its state-machine states | Glossary reviewed |
| F-19 | P3 | ARC-003; ARC-009 | Free third-party hosts (model weights, Python packages) become runtime dependencies | Allow self-hosted or cached copies for offline use | Reference task completes offline after first load |

## Mathematical review of ARC-012

**The formulas are stated correctly; the problems are in what they are applied to and how their outputs are judged.** Checked by hand, not executed.

| Element | Verdict | Notes |
| --- | --- | --- |
| Hard eligibility filter, then ranking | Sound | Keeps policy, license and budget out of the score, so a high score can never buy past a hard limit |
| Utility = wQ·Q + wR·R + wF·F − wC·C − wL·L | Form acceptable; inputs undefined | A linear score lets quality fully offset cost or latency within the eligible set; acceptable if intended. Terms, scales and weights must be defined and frozen (F-02) |
| Beta(a, b) → Beta(a + s, b + f) | Correct | Holds for exchangeable success/failure outcomes with a common rate. Pool only within a task family; name the prior and the ranking quantile (F-05). Exact quantiles come from the inverse regularized incomplete beta function |
| LinUCB: A = λI + Σxxᵀ, b = Σrx, θ = solve(A, b), score = xᵀθ + γ√(xᵀ solve(A, x)) | Matches the standard ridge-regression UCB form | Unspecified: one shared θ or one per capability; reward scale and bounds; feature scaling; how γ is chosen; λ > 0 required. Using solve() rather than an explicit inverse is the right numerical choice. Guarantees: see F-04 |
| Logging for later comparison | Insufficient | Deterministic selection without probabilities cannot support unbiased offline comparison (F-01) |
| Workflow credit not spread to every edge | Sound | Avoids the common error of crediting all components for a joint success |
| Bounded DAGs, cycle rejection, cumulative budget | Sound | Add a test that budget is checked before each node, not only at the end |

One structural point matters more than any formula. In the benchmark setting, every candidate can be run on every task, so feedback is full-information, not bandit feedback. Bandit machinery earns its place only where trying every option is too costly, such as live user tasks. ARC-007's comparisons should not depend on it.

## Claims-to-evidence matrix

**Of 14 checkable claims, 9 are supported, 3 are supported only with a correction, 1 is not established and 1 is unverified.** The bundle is notably honest: it already marks its own hypotheses as unverified and its originality as unestablished.

| Claim | Doc | Evidence checked | Status |
| --- | --- | --- | --- |
| Voyager's demonstration is domain-limited | ARC-002 | Skill library of executable code, demonstrated in Minecraft with GPT-4 ([Voyager](https://arxiv.org/abs/2305.16291)) | Supported |
| ICM is a preprint | ARC-002 | arXiv only; abstract page reports no benchmarks ([ICM](https://arxiv.org/abs/2603.16021)) | Supported; also see F-11 |
| Contextual-bandit guarantees are conditional | ARC-002 | True, but the cited bound is for SupLinUCB ([Chu et al.](https://www.schapire.net/papers/bandit-lin.pdf)) | Supported with correction (F-04) |
| LinUCB update and score formulas | ARC-012 | Hand check against standard form | Supported |
| Beta posterior update | ARC-012 | Standard conjugacy | Supported with correction (F-05) |
| Logged data supports static-vs-adaptive comparison | ARC-012 exit | Replay needs random logging ([Li et al.](https://arxiv.org/pdf/1003.5956)) | Not established (F-01) |
| Browser workers alone are not a security boundary for hostile code | ARC-008 | Pyodide escapes across seven products ([Cyera](https://www.cyera.com/research/sandcastles-not-sandboxes-how-one-architectural-flaw-exposed-seven-products)) | Supported |
| Browser cannot guarantee persistent storage | ARC-003 | Best-effort storage may be evicted ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)) | Supported |
| Optional in-browser LLM via WebLLM | ARC-003 | Open-source engine, up to 80% of native speed ([WebLLM](https://arxiv.org/abs/2412.15803)) | Supported |
| Standard public CI is free | ARC-008 | Free on standard GitHub-hosted runners in public repositories ([GitHub](https://docs.github.com/en/actions/concepts/billing-and-usage)) | Supported for public repos only |
| Static distribution must satisfy host terms | ARC-003 | GitHub Pages excludes commercial SaaS ([limits](https://docs.github.com/pages/getting-started-with-github-pages/github-pages-limits)); Cloudflare Pages Free caps builds and file sizes ([limits](https://developers.cloudflare.com/pages/platform/limits/)) | Supported |
| ACP extends Agent Skills conventions | ARC-004 | Compatible in spirit; manifest placement conflicts with the `metadata` type ([spec](https://agentskills.io/specification)) | Supported with correction (F-08) |
| Originality is not established | ARC-002 | ADAS, AFlow, DSPy and DGM cover adjacent ground | Supported; the gap is real |
| Provenance model follows W3C PROV | Register | Not opened this session | Unverified |

## Prior-art comparison

**No single system combines Arc-Adapticon's elements, but each element has a strong precedent.** The defensible novelty is the combination: typed, evidence-weighted selection on consumer hardware, with human authorization bound to exact plan digests. That is an empirical claim to test, not to assert.

| Work | What it does | Overlap with Arc-Adapticon | Use |
| --- | --- | --- | --- |
| [Voyager](https://arxiv.org/abs/2305.16291) (NeurIPS 2023) | Growing library of executable code skills, retrieved by description embedding | Retained skills, retrieval | Baseline: "fixed skill library" arm |
| [ADAS](https://arxiv.org/abs/2408.08435) (ICLR 2025) | A meta agent programs new agents in code from a growing archive; inventions transferred across domains and models | Candidate generation, archive, transfer | Cite; closest precedent for ARC-006 |
| [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) (ICLR 2026) | Self-modifying coding agents, each change validated on benchmarks; SWE-bench 20.0% to 50.0% | Evolution protocol, empirical validation | Cite; adopt its objective-hacking lesson (F-07) |
| [AFlow](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5492ecbce4439401798dcd2c90be94cd-Abstract-Conference.html) (ICLR 2025) | Monte Carlo Tree Search over code-represented workflows; 5.7% average gain over baselines on six benchmarks | Workflow composition as search | Cite; possible comparator for DAG composition |
| [DSPy](https://arxiv.org/abs/2310.03714) | Compiles declarative LM modules into optimized pipelines against a user metric | Metric-driven improvement of LLM steps | Comparator when a local LLM is present (F-12) |
| [ICM](https://arxiv.org/abs/2603.16021) (preprint) | Folder structure and markdown files replace framework orchestration for sequential, human-reviewed work | Structured context | Baseline only once defined operationally (F-11) |
| [Agent Skills](https://agentskills.io/specification) | Skill directory with SKILL.md frontmatter, optional scripts and references | Packaging | Integrate as the outer format (F-08) |

## Zero incremental service cost

**Feasible as ARC-001 defines it.** The definition is now precise: no new paid service, with existing hardware, electricity, internet and subscriptions excluded. Every layer has a no-cost path; the risks are availability and quality, not price.

| Layer | Bundle policy | Verified constraint | Verdict |
| --- | --- | --- | --- |
| Inference | Deterministic default; optional WebLLM, Ollama or llama.cpp; never fall back to paid | WebLLM is open source and reaches up to 80% of native speed ([WebLLM](https://arxiv.org/abs/2412.15803)) | Feasible; local model quality limits what the LLM arms can show |
| Static hosting | Optional; must satisfy host terms | GitHub Pages is not for commercial SaaS ([limits](https://docs.github.com/pages/getting-started-with-github-pages/github-pages-limits)); Cloudflare Pages Free allows 500 builds a month and 25 MiB per asset ([limits](https://developers.cloudflare.com/pages/platform/limits/)) | Feasible for a free tool; never host model weights there |
| CI | Standard public CI for bounded tests | Free on standard runners for public repositories ([GitHub](https://docs.github.com/en/actions/concepts/billing-and-usage)) | Feasible only while the repository stays public |
| Storage | IndexedDB/OPFS, SQLite, export/import; no database server | Browser storage is best-effort ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)) | Feasible; export is the durability guarantee (F-15) |
| Review | Existing Claude session | Covered by ARC-001's subscription exclusion | Feasible |
| Third-party downloads | Not addressed | Model weights and Python packages fetched from free hosts | Feasible; add offline caching (F-19) |

## Simpler alternatives and existing solutions

**Five substitutions would remove work and risk without weakening the research question.**

1. **Evaluate on full information.** On sealed benchmark tasks, run every policy on every task and compare paired results. This answers ARC-002 directly and removes the logging problem in F-01.
2. **Use Thompson sampling on the Beta posteriors as the first adaptive arm, before LinUCB.** ARC-012 already maintains those posteriors. Sampling is randomized, so selection probabilities can be estimated by simulation and logged, which serves F-01 for live use.
3. **One implementation of the selection logic.** Python, run natively and in the browser through Pyodide in a worker (F-10). Treat that worker as a convenience boundary, never a security one.
4. **Agent Skills as the outer package, ACP as a separate manifest file** (F-08). Contributors then get existing validators and tooling for free.
5. **Adopt existing OS-level isolation rather than building one.** Containers, microVMs, gVisor and seccomp are the established layers ([Cyera](https://www.cyera.com/research/sandcastles-not-sandboxes-how-one-architectural-flaw-exposed-seven-products)); choose per operating system and record the choice in ARC-008 (F-03).

## Unverified evidence

**These items were not confirmed in this review and should not be treated as established.**

- W3C PROV, the Microsoft human-AI interaction guidelines and the Pyodide documentation were in the register but not opened this session.
- Licenses of Pyodide, WebLLM, llama.cpp, Ollama and candidate model weights were not audited (F-17).
- Whether GitHub accepts this specific free tool on Pages is an interpretation of its published terms, not a confirmation from GitHub.
- Results quoted for ADAS, AFlow and DSPy come from their abstracts, not full papers. DSPy's arXiv page lists no peer-reviewed venue.
- None of ARC-002's four hypotheses has any supporting evidence yet. The bundle says so itself; this review agrees.

## Reconciliation checklist

**Per ARC-014, the founder reconciles each finding, then ratifies.** P1s must be corrected; P2s corrected or explicitly deferred with a reason.

- [ ] F-01: add selection probabilities and a full-information benchmark design to ARC-012 and ARC-007
- [ ] F-02: define Q, R, F, C, L, their scales and frozen weights in ARC-012
- [ ] F-03: move native isolation into M6 entry criteria in ARC-010; name the mechanism per OS in ARC-008
- [ ] F-04 to F-13: correct or defer each, with a recorded reason
- [ ] Re-review ARC-002, 006, 007, 010 and 012 after correction
- [ ] Ratify scope, license and cost policy (ARC-001 exit)

## Sources

- [ICM: Interpretable Context Methodology](https://arxiv.org/abs/2603.16021)
- [Voyager](https://arxiv.org/abs/2305.16291)
- [DSPy](https://arxiv.org/abs/2310.03714)
- [AFlow](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5492ecbce4439401798dcd2c90be94cd-Abstract-Conference.html)
- [ADAS: Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435)
- [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954)
- [Chu et al. 2011, Contextual Bandits with Linear Payoff Functions](https://www.schapire.net/papers/bandit-lin.pdf)
- [A Survey on Contextual Multi-armed Bandits](https://arxiv.org/pdf/1508.03326)
- [Li et al. 2011, Unbiased Offline Evaluation of Contextual-bandit Algorithms](https://arxiv.org/pdf/1003.5956)
- [WebLLM](https://arxiv.org/abs/2412.15803)
- [Agent Skills specification](https://agentskills.io/specification)
- [Cyera: Sandcastles, Not Sandboxes](https://www.cyera.com/research/sandcastles-not-sandboxes-how-one-architectural-flaw-exposed-seven-products)
- [GitHub Actions billing](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [GitHub Pages limits](https://docs.github.com/pages/getting-started-with-github-pages/github-pages-limits)
- [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/)
- [MDN: Storage quotas and eviction criteria](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)
