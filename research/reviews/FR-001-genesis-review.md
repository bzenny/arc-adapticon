# FR-001 — Genesis and contextual architecture review

Nov 25, 2026 · @Thomas Hogan

## N. Final disposition

**APPROVE WITH REQUIRED CORRECTIONS.** Arc-Adapticon should proceed to PUSH 001 and then to ARC Scout. Two P1 corrections must land with or before PUSH 001; neither needs code.

1. **G-01: narrow what ICM governs.** ICM's own documentation says it is for sequential, human-checked work and that automated mid-pipeline branching moves it toward being a framework. Synaptic Dynamism and GitHub event responses are both automated branching. ICM should govern structure, context and checked stages; adaptive selection and event handling should be code that a stage contract names as a command.
2. **G-02: make the human decision gate enforceable on GitHub.** GitHub does not let a pull request's author approve it. If the implementing agent pushes under the founder's account, required review cannot record the founder's authorization. The implementing agent needs its own identity, and `main` needs a rule requiring the founder's approval.

The three P1s from the v0.2.0 bundle review (logging, utility definition, sandbox sequencing) still stand. They block M3 and M5, not this phase.

**One integration recommendation outweighs the rest:** im-ICM largely re-describes the "System map" form that ICM Architect already ships, plus existing SBOM and licence scanners. Adopt them and keep im-ICM as a thin, testable profile on top (section E).

The recommended next engineering action closes this tab.

### Reconciliation log

| Date | Finding | Founder action | Reviewer disposition |
| --- | --- | --- | --- |
| 2026-11-25 | G-02 (P1) | D-002 Rev. 1: single founder-controlled identity during initial development; eight interim controls; six migration triggers; limitation explicitly accepted | **Deferred by founder authority, accepted risk.** No longer blocks PUSH 001. The risk is unchanged and must not be described as enforced separation. Four no-cost strengthenings recommended below |

**Recommended strengthenings to D-002 Rev. 1** (all work with one account):

1. Turn on a ruleset for `main` that requires a pull request before merging, with zero required approvals. This makes interim control 7 technical rather than procedural for ordinary pushes.
2. If the implementing agent uses the founder's credentials, give it a fine-grained token limited to this repository, with only contents and pull-request permissions and an expiry date.
3. Record each authorization as a PR comment that names the exact commit SHA being approved; a new push needs a new authorization.
4. Add a seventh migration trigger: any automation that can push or merge without a human acting in that moment.

G-01 is now the only open P1 for PUSH 001.

## A. Repository verification

**The repository holds exactly one file, `README.md`, at commit `605ee8902a0984d7589c1a81c081f8c87930102a`, which is the tip of `main` and the only ref.** Verified by shallow clone on 25 November 2026.

| Item | Observed |
| --- | --- |
| Commit | `605ee8902a0984d7589c1a81c081f8c87930102a`, author bzenny, 2026-11-25 12:56 +0800, "docs: establish Arc-Adapticon founding genesis" |
| Refs | `refs/heads/main` only; HEAD = the commit above |
| Tree | `README.md`, 7,479 bytes, blob `826e84c8` |
| Not present | LICENSE, AGENTS.md, workflows, code, tests, specifications, issues templates |

The README matches the commission's description: it declares a founding phase, "not a functioning product", and states that no performance or novelty claims are verified. Everything else in this review is **proposed architecture**, not implementation.

**Verification limits:**

- The GitHub API was not available to this session, so repository settings, branch protection, Actions settings, issues and wiki state could not be checked.
- The 14 ARC drafts reviewed earlier (Bundle v0.2.0 tab) are not committed; findings about them are carried forward but not re-verified against the repository.
- No tests were executed; none exist.

## B. Executive assessment

**The foundational proposition is viable as a research programme, and its testable core is small: does organizing, validating and reusing capabilities improve results at fixed model scale?** That is a legitimate hypothesis. The genesis README already labels it untested, which is the right starting posture.

**Principal strengths**

- Honest status discipline: the README separates proposal from implementation and makes no performance claims.
- Integration-first doctrine, local-first operation and portable workspaces.
- Human authorization and independent evidence named as governing principles.
- A sensible first product: read-only repository assessment (ARC Scout) produces value before any adaptive machinery exists.

**Principal deficiencies**

1. **ICM is asked to govern more than it claims to.** Its documented scope excludes automated branching and concurrency (G-01).
2. **The human gate is described, not yet enforced** in the GitHub workflow (G-02).
3. **im-ICM and much of ARC Scout re-describe existing tools**: ICM Architect's System map form, SPDX/CycloneDX SBOM generators, licence and vulnerability scanners (G-06).
4. **ICM vocabulary is attributed to the wrong source.** Sequences, shelves and catalogs come from ICM Architect, not the ICM paper (G-04).
5. **The proposed PUSH 001 tree duplicates catalogs** and uses underscore folders for the work itself, against ICM's own naming rule (G-05).
6. **Independence is partial.** Implementer and reviewer are both language models; only executed tests and the founder are independent of model error (G-13).

**Should it proceed? Yes**, with the corrections above. The next phase is documentation and read-only analysis, which carries low risk and produces evidence the later phases need.

## C. ICM fidelity matrix

**Today Arc-Adapticon is neither genuine ICM nor Markdown-fronted orchestration: nothing is structured yet.** The proposed tree leans toward the second risk in two places: duplicated catalogs, and automated components described in prose rather than named as commands in stage contracts.

Sources compared: the ICM paper ([arXiv 2603.16021](https://arxiv.org/abs/2603.16021)), the reference repository ([RinDig/Interpretable-Context-Methodology](https://github.com/RinDig/Interpretable-Context-Methodology) at `02ba5d8`) and [ICM Architect](https://github.com/RinDig/icm-architect) at `8bc2f56`. Both repositories are MIT-licensed.

| Principle | What the ICM sources say | Arc-Adapticon proposal | Verdict | Correction |
| --- | --- | --- | --- | --- |
| Sequences | Numbered folders; each step's `output/` is the next step's input (Architect) | Seven-stage stream; no numbered stage folders for development work | Missing | Model the development flow as a short sequence (propose, review, authorize, implement, verify) only where it repeats |
| Shelves | A folder of same-shaped files, each copied from one template (Architect) | `_research/`, `_evolution/`, `_integrations/` with no templates | Not yet shelves | Shelves for decisions, sources and lineage events, each with a template in `_templates/` |
| Catalogs | Small routing files that store no content; generated indexes are never hand-edited (Architect) | README, AGENTS.md, CLAUDE.md, CONTEXT.md, CATALOG.md, GOVERNANCE.md | Duplicated | AGENTS.md is the catalog; CLAUDE.md is a one-line pointer; drop a hand-written CATALOG.md |
| Scoped instructions | Each working folder has a CONTEXT.md with Inputs, Process, Outputs and one Check (reference repo; Architect) | None yet | Missing | Contract per working folder, exact input paths |
| Progressive disclosure | Five layers; entry file under about 60 lines; a step's context under about 8,000 tokens | README is the only entry (7,479 bytes) | Partial | Entry routing in AGENTS.md; README stays human-facing |
| Persistent file state | Status lives on disk; state is the files | Lineage in README; event records proposed | Consistent in intent | Lineage as an append-only file, not README prose |
| Explicit handoffs | Output folders; a non-human check writes `check.md` with `pass` or `fail: <why>`; a fail stops the run | Human Decision Point | Strong match | Encode the decision point as a check with a recorded decision |
| Deterministic scripts | "A step that is code names its command" (Architect) | "Deterministic enforcement remains code" (README) | Consistent | Every automated component appears as a named command in a contract |
| Human-interpretable | Plain text, every output an edit surface | Plain Markdown, JSON, YAML | Consistent | None |
| Underscore folders | About the workspace, not the work: `_shared/`, `_templates/`, `_tools/`, `_meta/`, `_archive/` (Architect) | `_core/`, `_research/`, `_evolution/`, `_integrations/`, `_development/` | Contradicts | Underscore only for factory, templates, tools; the work gets plain names |
| Entry naming | AGENTS.md is the entry; CLAUDE.md holds `@AGENTS.md` (Architect, Oct 2026). The older reference repo uses CLAUDE.md | Both, content unclear | Ambiguous | Follow Architect: AGENTS.md is read natively by Codex and many other agents ([agents.md](https://agents.md/)) |
| Method vs instance | Blank reusable template lives apart from any filled deployment (Architect) | Not addressed | Missing | Keep Arc's development workspace separate from the workspace templates it ships (e.g. ARC Scout) |
| Where ICM loses | Real-time multi-agent work, high concurrency, automated branching (reference repo) | Synaptic Dynamism; GitHub event responses | Conflict (G-01) | These run as code behind a contract; ICM structures their inputs, outputs and checks |

### Could a cold agent enter today?

**No.** With only the README, an unfamiliar agent can learn the purpose but not where to go for a task, which fails the first step of ICM Architect's walk test. After PUSH 001 (section J), the acceptance test is that a fresh agent answers three routing questions within the entry file plus two more reads.

### Documented findings versus Arc extrapolations

The ICM paper's evidence is descriptive. It reports token counts from one workspace, practitioner reports from a 52-member community, use of a single model family, and says no controlled comparison against monolithic prompting has been run ([arXiv 2603.16021](https://arxiv.org/html/2603.16021)). The terms "shelf" and "catalog" do not appear in the paper; they come from ICM Architect.

Arc-Adapticon extrapolates ICM to three settings no ICM source tests: a governing method for a computational platform, adaptive capability selection, and projections over external resources. Each is a proposal, not an ICM finding.

## D. Prior-art and integration matrix

**Almost every component Arc-Adapticon needs before M5 already exists as a maintained open project.** Justified original work is narrow: the capability contract, the evidence ledger linking claims to sources, and the experiment that tests the central hypothesis.

### Research prior art

| Work | Established result | Duplication risk for Arc | Use |
| --- | --- | --- | --- |
| ICM paper and ICM Architect | Folder structure as agent architecture; descriptive evidence only | Arc's development structure | Adopt conventions; do not cite as validated |
| [Voyager](https://arxiv.org/abs/2305.16291), [ADAS](https://arxiv.org/abs/2408.08435), [DGM](https://arxiv.org/abs/2505.22954), [AFlow](https://arxiv.org/abs/2410.10762), [DSPy](https://arxiv.org/abs/2310.03714) | Skill libraries, generated agents and workflow search improve benchmark scores with frontier models | Synaptic Dynamism and evolution | Baselines and comparators (Bundle tab) |
| [Garcia et al., ASE 2013](https://doi.org/10.1109/ASE.2013.6693106) | Against verified ground-truth architectures, even the best of six recovery techniques had surprisingly low accuracy | im-ICM architecture maps | Treat any recovered architecture as inference |
| [RepoAgent](https://arxiv.org/abs/2402.16667) (EMNLP 2024 demo) | LLM-generated repository-level documentation that is kept in sync with Git | im-ICM LLM layer | Comparator for the interpretive layer |
| [SPDX](https://www.iso.org/standard/81870.html) (ISO/IEC 5962:2021), CycloneDX | Standard formats for component, licence and dependency data | `dependencies.md`, `licensing.md` | Emit SPDX JSON instead of inventing a format |
| [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) (Recommendation, 2013) | Entity, Activity, Agent; generation, use, derivation, attribution; invalidation | Lineage records | Map lineage fields to PROV terms |
| [Parasuraman, Sheridan and Wickens 2000](https://doi.org/10.1109/3468.844354) | Automation applies at different levels to acquisition, analysis, decision and action | The seven-stage stream | Assign an automation level per stage (section H) |

### Dependency candidates

Licences below were read from each project's LICENSE file at its default branch on 25 November 2026; every repository except ICM Architect (last commit 23 October 2026) had commits within the last month.

| Project | Licence | Role | When | Integration method | Security and maintenance notes |
| --- | --- | --- | --- | --- | --- |
| [ICM Architect](https://github.com/RinDig/icm-architect) | MIT | Conventions; `links.py` and `index.py` (standard-library Python) | PUSH 001 | Vendor scripts into `_tools/`, pinned to `8bc2f56`, with attribution | Single maintainer; pin and review on update |
| [Agent Skills](https://github.com/agentskills/agentskills) | Apache-2.0 | Outer format for capability packages | M2 | Follow spec; ACP manifest in a separate file | SKILL.md is untrusted descriptive text |
| [Model Context Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | Apache-2.0 for new contributions; older parts remain MIT during a licensing transition | Optional adapter exposing Scout as a tool | After M3 | Adapter only; never in the core | Tool calls widen the attack surface |
| [Pyodide](https://github.com/pyodide/pyodide) | MPL-2.0 | Browser Python | M7 | Web worker; load from pinned version | Threads, multiprocessing and sockets are not functional ([constraints](https://pyodide.org/en/stable/usage/wasm-constraints.html)); not a security boundary |
| [JupyterLite](https://github.com/jupyterlite/jupyterlite) | BSD-3-Clause | Browser workbench | M7 | Integrate instead of building a workbench | Static hosting; inherits Pyodide limits |
| [WebLLM](https://github.com/mlc-ai/web-llm) | Apache-2.0 | Optional browser inference | M4 | Optional plug-in | Model weights carry their own licences |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) / [Ollama](https://github.com/ollama/ollama) | MIT / MIT | Optional native inference | M4 | Local HTTP or CLI adapter | Hardware-dependent; weights licensed separately |
| [NetworkX](https://github.com/networkx/networkx) | BSD-3-Clause | Typed capability graph | M2 | In-process library; no graph database | Pure Python; fine at early scale |
| [SciPy](https://github.com/scipy/scipy), [scikit-learn](https://github.com/scikit-learn/scikit-learn) | BSD-3-Clause | Beta quantiles; non-LLM baselines | M5 | Library | Widely maintained |
| [DSPy](https://github.com/stanfordnlp/dspy) | MIT | Comparator for LLM pipelines | M5, only with a local model | Experiment arm | Not in the core path |
| [Optuna](https://github.com/optuna/optuna) | MIT | Tuning comparator configurations | Defer | Experiment tooling | Not needed before M5 |
| [MLflow](https://github.com/mlflow/mlflow) | Apache-2.0 | Experiment tracking | Defer | Only if plain JSON run manifests prove insufficient | Heavier; plain files first is more ICM-native |
| [Syft](https://github.com/anchore/syft) | Apache-2.0 | SBOM in SPDX or CycloneDX | M1 Scout | Native CLI on a checked-out tree | Reads files only; no build |
| [ScanCode Toolkit](https://github.com/aboutcode-org/scancode-toolkit) | Apache-2.0 (code), CC-BY-4.0 (data) | Licence detection | M1 Scout | Native CLI | Slower on large trees; set size caps |
| [OSV-Scanner](https://github.com/google/osv-scanner) | Apache-2.0 | Known vulnerabilities | M1 Scout | Native CLI | Queries the public OSV database |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Apache-2.0 | Project health checks | M1 Scout, optional | CLI with a token | Requires authentication for the GitHub API |
| [scc](https://github.com/boyter/scc) | MIT | Languages and size | M1 Scout | Native CLI | Read-only |
| [tree-sitter](https://github.com/tree-sitter/tree-sitter) | MIT | Parsing for entry points and symbols | M1+ | Python bindings | Grammars licensed separately |

**Workflow and agent runtimes** (LangGraph, CrewAI, AutoGen and similar) are not recommended for the core: ICM's premise is that sequential, checked work does not need them. Revisit only if a measured need appears.

## E. im-ICM assessment

**im-ICM is a sound idea that is not novel: it is software architecture recovery plus SBOM generation plus an ICM workspace, with an evidence ledger.** ICM Architect's "System map" form already covers "map this repo": it sorts parts into live, leftover and ghost, marks a card `verified` only with a date, a commit and citations, and has a later agent re-verify load-bearing claims ([system-map.md](https://github.com/RinDig/icm-architect/blob/main/references/system-map.md)). Arc's contribution should be a thin profile: a strict split between observation and inference, and a measured comparison.

### What already exists

- **Architecture recovery** is a mature field with a sobering result: against verified ground truth, even the best of six techniques had surprisingly low accuracy ([Garcia et al. 2013](https://doi.org/10.1109/ASE.2013.6693106)). Any `architecture-map` is therefore inference.
- **Dependency and licence facts** have standard formats and tools: SPDX and CycloneDX via Syft, licences via ScanCode, vulnerabilities via OSV-Scanner.
- **LLM repository documentation** exists (RepoAgent).
- **Provenance** has a W3C model (PROV-DM).

### Deterministic versus LLM work

| Deterministic (reproducible, counted as observations) | LLM-assisted (always inferences) |
| --- | --- |
| File tree, sizes, languages | Purpose summary |
| Package manifests, dependency graph, SBOM | Capability names and grouping |
| Declared and detected licences | Architecture grouping into components |
| Known vulnerabilities | Fit to an Arc integration need |
| Entry points, test and CI presence | Risk narrative |
| Commit, release and contributor activity | Questions worth asking upstream |

### Minimum specification (im-ICM profile v0.1)

```
im-icm/<owner>__<repo>@<sha7>/
  AGENTS.md              catalog: source, commit, generated date, status, expiry rule
  source-manifest.json   URI, full commit SHA, retrieved_at, tool names and versions, file hashes
  sbom.spdx.json         Syft output
  licenses.json          ScanCode output
  vulns.json             OSV-Scanner output
  observations.jsonl     one fact per line, each with evidence
  inferences.jsonl       one inference per line, each citing observation IDs
  unknowns.md            questions with no evidence yet
  map/                   ICM Architect System-map cards, citing observations
  integration-review.md  assessment citing observation and inference IDs
  check.md               pass or fail: <why>
```

The proposed `CONTEXT.md` and `CATALOG.md` merge into `AGENTS.md`; `dependencies.md` and `licensing.md` become the standard files above plus a short summary; `evidence/` becomes `observations.jsonl`; `capability-matrix.json` stays, but every cell must cite IDs.

**Record rules**

- **Observation:** `id`, `statement`, `evidence` (path, line range, blob SHA), `method` (tool and version, or `human`).
- **Inference:** `id`, `statement`, `supports` (one or more observation IDs, required), `method` (`llm:<model>@<version>` or `human`), `status` (`proposed`, `checked`, `rejected`).
- **Uncertainty:** categorical, not invented percentages: `observed`, `inferred-checked`, `inferred-unchecked`, `unknown`.
- **Coverage:** share of files, manifests and declared dependencies actually examined, recorded in the manifest.
- **Contradictions:** both records kept and linked with `conflicts_with`; never silently resolved.
- **Freshness:** a projection is stale when the upstream ref no longer equals its SHA; Scout reports staleness rather than editing in place.
- **Lifecycle:** regenerate from SHA and tool versions; export as the folder; retire by moving to `_archive/` with a lineage event. The source is never modified, and projection grants no execution or redistribution rights (as the README already says).

### Evaluation methodology

The smallest experiment that can falsify "im-ICM improves review quality":

1. **Sample:** 10 public repositories of varied size and language, pinned by SHA.
2. **Ground truth:** two people independently record licence, direct dependencies, entry points and three integration questions per repository; disagreements are reconciled.
3. **Conditions:** (a) reviewer with the repository only; (b) reviewer with deterministic tool output only; (c) reviewer with the im-ICM projection.
4. **Metrics:** factual accuracy against ground truth; share of report claims whose citation resolves; reviewer minutes; agreement between reviewers on the integrate/reject decision; byte-identical regeneration of deterministic files.
5. **Result rule:** im-ICM earns its extra structure only if (c) beats (b) on accuracy or time without losing citation validity. If (b) is as good, keep the tools and drop the projection layer.

## F. Mathematical assessment of Synaptic Dynamism

**The five-step progression is correct, and advanced adaptation is not justified until stage 3 has produced repeated evidence that stages 1 and 2 cannot use.** Each mechanism is standard; the risks lie in the data it will see. The formula-level review is in the Bundle v0.2.0 tab (sections on ARC-012) and still applies.

| Issue | Risk in Arc's setting | Recommended handling | Stage |
| --- | --- | --- | --- |
| Cold start | No evidence for new capabilities | Deterministic eligibility and ranking; every new capability must pass its own tests before it is eligible | 1 |
| Statistical uncertainty | Few runs per capability | Beta posteriors per capability, version and task family; rank on a stated lower quantile, not the mean | 3 |
| Sparse and correlated evidence | Tasks from one family share causes, so successes are not independent | Pool only within a family; count a repeated task once; report intervals | 3 |
| Context drift | Upstream libraries, models and tasks change | Evidence keyed to capability version and dependency SHAs; stale evidence expires on change | 3–4 |
| Selection bias | A deterministic selector only gathers evidence on what it already picks | Benchmarks run every eligible candidate on every task; live exploration logs selection probabilities | 3–4 |
| Reward hacking | A candidate optimizes the evaluator, not the task; DGM's authors observed this, more often when detection functions were visible | Evaluator and holdout outside the candidate's reach; evaluator digest pinned | 5 |
| Credit assignment | A workflow success credited to every component | Record workflow evidence separately; credit a component only through its own tests or ablation | 2–3 |
| Version-specific performance | Evidence carried across versions unjustifiably | New version starts with its own evidence; transfer only by explicit, recorded decision | 3 |
| Computational overhead | Negligible: small matrices and counts | Not a constraint at this scale | All |
| Security and authorization | A high score could route around policy | Eligibility filter (policy, licence, budget) runs before any scoring; scores never grant permission | 1 |

### Gates between stages

1. **Deterministic eligibility and ranking.** Ships with ARC Scout's capability matrix. Gate to stage 2: typed inputs and outputs exist for at least the capabilities Scout itself uses.
2. **Typed composition.** Gate: composed workflows beat hand-run steps on time or errors on the fixture set.
3. **Empirical reliability.** Gate: multiple eligible candidates exist for the same task family, and their posterior intervals separate on held-out tasks.
4. **Contextual adaptive selection.** Gate: a paired comparison on sealed tasks shows adaptive beats static ranking by a preregistered margin.
5. **Governed evolution.** Gate: a native sandbox passes its escape suite, and the evaluator-isolation test passes.

**Simpler alternatives:** a ranked list with Beta lower bounds may deliver much of the value of stages 3 and 4; it should be the static arm that adaptive selection has to beat. Thompson sampling on those posteriors is a simpler first adaptive arm than LinUCB, and it produces selection probabilities that later evaluation needs.

## G. Zero-cost feasibility

**A zero-incremental-cost baseline is feasible, but ARC Scout's deterministic toolchain is native-only; the browser can display Scout results, not produce them.** Hosted compute is used only for bounded verification.

| Profile | What runs | Requires | Unavoidable limits |
| --- | --- | --- | --- |
| P0 Read-only | Documentation and ICM workspaces in any Git host or folder | Git or a file browser | None beyond reading |
| P1 Local native (supported baseline) | ARC Scout: clone, Syft, ScanCode, OSV-Scanner, scc, report generation | Python, Git, the CLIs above, internet to fetch public repos | Unauthenticated GitHub API: 60 requests an hour per IP; with a user's own token, 5,000 ([rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)). Scout should clone with Git rather than walk the API |
| P2 Browser static | Viewing Scout workspaces; Pyodide or JupyterLite for compatible Python | A browser; free static hosting | Threads, multiprocessing and sockets do not function in Pyodide; HTTP goes through the browser and CORS can block requests ([Pyodide](https://pyodide.org/en/stable/usage/wasm-constraints.html)); storage is best-effort |
| P3 Optional local models | WebLLM, Ollama, llama.cpp | User hardware | Quality and speed depend on the device |
| P4 Public CI | Tests, link checks, Scout fixture runs | Public repository, standard runners | Free only for public repos on standard runners; jobs end at 6 hours ([limits](https://docs.github.com/en/actions/reference/limits)); `GITHUB_TOKEN` allows 1,000 API requests an hour per repository; scheduled workflows in public repos are disabled after 60 days without repository activity ([events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)) |

**Infrastructure dependencies that remain** even at zero cost: GitHub (or another host) for public source; PyPI, npm and the tools' release downloads; the OSV database; model-weight hosts for P3. Each is free today and none is guaranteed, so Scout must run offline against already-cloned sources, and P1 must never require P4.

## H. GitHub spine assessment

**GitHub's built-in mechanisms cover every proposed spine function; no custom infrastructure is needed before M6.** Two rules keep it safe: event workflows only propose (issues or pull requests), and only the founder's approval merges.

| Function | GitHub mechanism | Portable equivalent | Notes |
| --- | --- | --- | --- |
| Source and architecture history | Commits, tags | Any Git remote | Canonical lineage lives in the repository, not issues |
| Requirements | Issues with forms | `proposals/` shelf | Issues are not in Git; copy decisions into the repo |
| Independent review | Pull requests, CODEOWNERS, rulesets requiring approval | Patch review by email | See G-02 on identities |
| Deterministic verification | Actions on `pull_request` | Local `make check` or script | Default `GITHUB_TOKEN` to read-only contents ([secure use](https://docs.github.com/en/actions/reference/security/secure-use)) |
| Upstream release and dependency signals | Dependabot version updates; scheduled Scout re-runs | Local scheduled run | Dependabot opens pull requests for dependencies and Actions references ([Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates)) |
| Security responses | Dependabot security updates; OSV-Scanner; Scorecard | Same CLIs locally | Scorecard needs a token |
| External triggers | `repository_dispatch` | Manual run | Payload limited to 10 top-level properties and 65,535 characters |
| Capability distribution | Releases with checksums | Tagged archives | Reproducible build required before M8 |
| Public docs and wiki | Wiki | Generated Markdown | The wiki is cloned from its own `.wiki.git` URL ([wiki](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages)); publish one way from the main repo |

### Required safeguards

- **Never use `pull_request_target`** with checkout of contributed code. GitHub states such workflows "must not explicitly check out untrusted code, including from pull request forks".
- **Pin third-party actions to full commit SHAs**, and pass untrusted values such as titles through environment variables, not inline script.
- **No self-hosted runners** on the public repository; GitHub advises any user can open pull requests and compromise them.
- **Scanned repositories are data.** Scout never builds, installs or runs them, in CI or locally.
- **Human gate (G-02).** "Pull request authors cannot approve their own pull requests" ([GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews)). The implementing agent needs its own GitHub identity; a ruleset on `main` requires one approving review and blocks direct pushes. Admins can still bypass, so the founder should leave bypass off for routine work and record any use as a lineage event.

### The stream as an enforceable state machine

The seven stages map to states, with automation levels assigned per Parasuraman, Sheridan and Wickens. The **Human Decision Point** becomes a decision record bound to the exact commit or plan digest; **AI Directed** may run only actions named in that record, within its scope, budget and expiry. Rejection, revision, cancellation and expiry return to formation. Standing authorizations cover only a listed set of read-only operations (for example, re-running Scout on a pinned repo). The founder's PR approval is the enforcement point on GitHub; the decision record is the portable equivalent.

## I. ARC Scout assessment

**ARC Scout is the right first vertical slice.** It is read-only, deterministic, useful to developers immediately, and it exercises the pieces later phases depend on: ICM workspaces, im-ICM, provenance, licence policy and the human gate. It also serves the integration doctrine directly: Scout's first job is to assess Arc's own candidate dependencies.

**Two corrections to the proposed pipeline:**

- v0.1 takes an explicit list of repository URLs and SHAs. Search-based discovery waits until assessment works, because search spends API quota and adds ranking questions.
- Scout retrieves code with `git clone --depth 1` at a pinned SHA rather than the API, so it works without a token.

### v0.1 pipeline

1. **Input:** repository URL and commit SHA.
2. **Fetch:** shallow clone into a fresh directory; record SHA and time.
3. **Inspect (deterministic):** Syft, ScanCode, OSV-Scanner, scc; write `observations.jsonl`.
4. **Project:** build the im-ICM folder (section E).
5. **Assess:** fill `integration-review.md` from a template; optional local model writes only to `inferences.jsonl`.
6. **Check:** citation validator plus a human read; `check.md` records the verdict.
7. **Export:** the folder, as is.

### Acceptance criteria

| ID | Criterion | Test |
| --- | --- | --- |
| S-1 | Produces a complete workspace for a pinned public repo with no API token and no paid service | Run on fixture set with networking limited to Git and tool downloads |
| S-2 | Deterministic outputs regenerate byte-identically from the same SHA and tool versions | Run twice; compare hashes; timestamps live only in a separate run record |
| S-3 | Never executes repository code | Fixture repos with a malicious `setup.py`, an npm `postinstall` and a `Makefile` that each write a canary file; the canary must not appear |
| S-4 | Treats repository text as data | Fixture README containing instructions to the agent; the report quotes it, no action follows, and no inference cites it as an instruction |
| S-5 | Every report claim cites a resolvable observation or inference | Validator script: 100% of IDs resolve to path, lines and blob SHA |
| S-6 | Every inference cites at least one observation | Schema validation |
| S-7 | Fails loudly | Unreachable repo, oversized repo, missing tool and rate-limit fixtures each produce an explicit error and a workspace marked incomplete |
| S-8 | Licence facts match ground truth | Top-level licence correct on every fixture whose licence was verified by hand (for example, the 20 projects whose LICENSE files were read for section D) |

### Measurable evaluation

The section E experiment, plus: minutes per assessment against a manual baseline; share of claims marked `unknown`; reviewer agreement on integrate or reject. Scout is "genuinely useful" when a reviewer reaches the same integrate/reject decision as a careful manual review in less time, with every claim traceable.

### Fixtures

- Synthetic, committed under `tests/fixtures/`: no-licence repo, dual-licence repo, monorepo, malicious build scripts, prompt-injection README, binary-heavy repo.
- Real, pinned by SHA: ICM Architect, the ICM reference repository, NetworkX and two or three others from section D.

## J. PUSH 001 recommendation

**PUSH 001 should be documentation only: an ICM-native entry, one contract, one factory file, three shelves and one vendored check script.** No code, no CI, no empty folders.

### Resulting tree

```
arc-adapticon/
  README.md                  modify: human overview only
  AGENTS.md                  create: L0 catalog, routing only
  CLAUDE.md                  create: one line, @AGENTS.md
  CONTEXT.md                 create: L1, how work moves through the repo
  _shared/governance.md      create: authority, push disclosure, review rules
  _templates/decision.md     create: decision record template
  _tools/links.py            create: vendored from ICM Architect @8bc2f56
  decisions/0001-adopt-icm-architect-conventions.md
  decisions/0002-source-code-license.md
  lineage/events.jsonl       create: append-only lineage
  research/register.md       create: verified sources (section K)
  specs/ARC-001 … ARC-014    create, optional: drafts, status draft
```

### Manifest

| Path | Action | Required | Purpose |
| --- | --- | --- | --- |
| `README.md` | Modify | Yes | Keep purpose, status and principles; point agents to AGENTS.md; move chronology to `lineage/`, authority rules to `_shared/governance.md`; attribute sequences, shelves and catalogs to ICM Architect |
| `AGENTS.md` | Create | Yes | Under about 60 lines: what this is, where things live, route by task, the one rule (nothing merges without founder approval) |
| `CLAUDE.md` | Create | Yes | `@AGENTS.md`, nothing else; Codex and other agents read AGENTS.md directly |
| `CONTEXT.md` | Create | Yes | The development sequence (propose, review, authorize, implement, verify) and where each step's artifacts go |
| `_shared/governance.md` | Create | Yes | Single home for roles, push disclosure, review protocol, standing authorizations |
| `_templates/decision.md` | Create | Yes | ADR-style record (context, decision, consequences, status, supersedes) with PROV-mappable fields |
| `_tools/links.py` | Create | Yes | Checks every link and contract input resolves; MIT attribution and source commit in the header |
| `decisions/0001-…` | Create | Yes | Adopt ICM Architect conventions; record G-01 scope wording |
| `decisions/0002-…` | Create | Yes | Licence decision; status `proposed` until the founder decides |
| `lineage/events.jsonl` | Create | Yes | ARC-EVO-0001 to 0009 moved from README; fields `id`, `type` (origin, proposal, authorization, implementation, verification, supersession), `date`, `actor`, `summary`, `refs`, `supersedes` |
| `research/register.md` | Create | Yes | Section K, with classification per source |
| `specs/ARC-*.md` | Create | Optional | The v0.2.0 drafts, unchanged, marked draft with open findings linked |

**Not created, and why:** `CATALOG.md` (AGENTS.md is the catalog; generated indexes come later), `GOVERNANCE.md` at root (lives in `_shared/`), `_core/`, `_research/`, `_evolution/`, `_integrations/`, `_development/` (speculative, and they use underscore names for the work itself). **Removed:** nothing.

### Acceptance criteria

- `python -I _tools/links.py` exits 0.
- AGENTS.md is under 60 lines and holds no content beyond routing.
- Cold walk test: a fresh Claude session and a fresh Codex session each answer "where do I record a decision?", "what is the current status?" and "who may merge?" within AGENTS.md plus two reads.
- No rule appears in two files (spot-check governance and README).
- Every lineage event has a type, and no proposal is typed as implementation.
- The README still says the project is not a functioning product.

### Risks and rollback

- **Risk:** churn in names before the first code lands. **Mitigation:** decision 0001 fixes conventions.
- **Risk:** vendored script drifts from upstream. **Mitigation:** pinned commit in its header.
- **Rollback:** single documentation commit on a feature branch; revert the merge commit. Nothing executes.

## L. Review findings

**No P0; 2 new P1; 9 P2; 4 P3.** The three P1s from the Bundle v0.2.0 review are carried forward and block M3 and M5 only.

| ID | Sev | Location | Finding, rationale and consequence | Correction | Acceptance test |
| --- | --- | --- | --- | --- | --- |
| G-01 | P1 | Commission req. 1; README "Foundational commitments" | ICM is named the governing methodology for everything, but its own README lists automated mid-pipeline branching and high concurrency as where it does not work. Synaptic Dynamism and event responses are exactly that. Consequence: either hidden orchestration behind Markdown, or ICM bent past its design | Founder rewords req. 1: ICM governs structure, context and checked stages; automated selection and event handling are code named as commands in stage contracts, writing files and checks | Every automated component appears in a CONTEXT.md with command, inputs, outputs and check; walk test passes |
| G-02 | P1 | README "Development authority"; GitHub settings | The founder's decision is not yet an enforceable boundary. PR authors cannot approve their own PRs, so if the implementing agent pushes as the founder, required review cannot record authorization | Separate identity for the implementing agent (machine account or GitHub App) with PR-only rights; ruleset on `main` requiring one approval and no direct pushes | A bot PR cannot merge without founder approval; a direct push to `main` is rejected |
| F-01–F-03 | P1 (carried) | ARC-007, 010, 012 drafts | Logging without selection probabilities; undefined utility terms; candidate generation before sandbox | As in the Bundle tab | As in the Bundle tab; block M3/M5 only |
| G-04 | P2 | README "ICM and im-ICM" | Sequences, shelves and catalogs are attributed to ICM; they come from ICM Architect, and the paper never uses "shelf" or "catalog" | Cite ICM Architect for the primitives | Register entry and README wording match sources |
| G-05 | P2 | Commission §12 tree | Duplicate catalogs (CATALOG.md, CONTEXT.md, AGENTS.md, README); GOVERNANCE.md separate from authority text in README; underscore folders for work; empty folders | PUSH 001 manifest (J) | Section J acceptance criteria |
| G-06 | P2 | im-ICM | Duplicates ICM Architect's System map and standard SBOM, licence and vulnerability tooling; novelty not established | Adopt them; keep im-ICM as a thin profile (E) | Section E experiment run before claiming benefit |
| G-07 | P2 | im-ICM spec | Separation of observation and inference is stated, not enforced | Two files with a schema; inferences must cite observations | Schema validation in Scout tests (S-6) |
| G-08 | P2 | ARC Scout | Discovery through the API and any build step would add quota use and code-execution risk | Clone at pinned SHA; never build or install | S-1, S-3, S-4 |
| G-09 | P2 | GitHub spine, M6 | Scheduled workflows in public repos are disabled after 60 days without activity and may be delayed or dropped under load | Treat schedules as convenience; every event response also runs locally on demand | Local re-run reproduces the scheduled result |
| G-10 | P2 | Lineage, wiki | The wiki is a separate Git repository and is not reviewed through pull requests | Generate wiki pages one way from the main repo; restrict wiki editing to collaborators | Wiki content equals generated output |
| G-11 | P2 | Roadmap M0–M8 | M7 plans a new web workbench while JupyterLite exists; zero-cost audit appears only at M8; Scout dogfooding not scheduled | M7: integrate JupyterLite; add a zero-cost and licence check to every milestone exit; M1 includes Scout on Arc's own dependencies | Each milestone exit record includes cost and licence check |
| G-13 | P2 | Development authority | Implementer and reviewer are both language models and can share errors; only executed tests and the founder are independent of that | Verification claims count only with executed tests and their logs | Each PR links test output, not just a description |
| G-14 | P3 | README | Mixes chronology, governance and roadmap in one file | Split per J | J criteria |
| G-15 | P3 | README research list | AFlow and contextual-bandit links differ from the draft register (ICLR page versus arXiv; Li et al. 2010 versus Chu et al. 2011) | Use one register as the single home | Register and README agree |
| G-16 | P3 | ICM citations | ICM paper evidence is descriptive and from one model family | Cite it as method, not validation | Register classification |
| G-17 | P3 | README status | Brand clearance pending | Founder decision | Decision record exists |

### Roadmap assessment

The sequence is sound in order, with three adjustments already listed: integrate JupyterLite at M7 (G-11); run the zero-cost and licence audit at every gate, not only M8; and move the native sandbox ahead of any execution of generated code (carried F-03). M1 can deliver useful output early because Scout needs none of M2–M5.

## M. Founder decision register

**Nine decisions need explicit founder authorization; the first three block PUSH 001 or the code that follows it.**

| # | Decision | Options | Reviewer recommendation | Blocks |
| --- | --- | --- | --- | --- |
| D-1 | Reword non-negotiable requirement 1 (G-01) | Keep as is; narrow to structure, context and checked stages | Narrow | PUSH 001 (decision 0001) |
| D-2 | Implementing agent identity and `main` ruleset (G-02) | Founder account; machine account; GitHub App | Separate identity, PR-only rights, required founder approval | Any PR after PUSH 001 |
| D-3 | Source-code licence | Apache-2.0 (proposed); MIT; other | Founder's call; record in decision 0002 before any code | First code commit |
| D-4 | Commit the v0.2.0 drafts in PUSH 001 | Yes, as drafts; later, after reconciliation | Yes, as drafts with findings linked | Lineage completeness |
| D-5 | ARC Scout fixture list and pass thresholds | As in section I; custom | Section I list | M1 acceptance |
| D-6 | Optional GitHub token for Scout | None; user-supplied token | None by default; optional user token | Nothing |
| D-7 | Wiki enabled and who edits | Off; collaborators only; public | Off until generated docs exist | M8 docs |
| D-8 | Standing authorizations list | None; read-only re-runs | Read-only Scout re-runs on pinned repos only | M6 |
| D-9 | Brand clearance for "Arc-Adapticon" | Proceed; check first | Check before public release | M8 |

## K. Research register

**Every entry below was checked on 25 November 2026, either by opening the source or, for Garcia et al., Parasuraman et al., SPDX and Nygard, through publisher or index records found by search.** Classification uses the commission's six categories and describes what the source supports for Arc, not the source's quality.

| Source | What it supports | Classification for Arc | Applicability |
| --- | --- | --- | --- |
| [ICM paper](https://arxiv.org/abs/2603.16021) (preprint) | Folder-structured context for sequential, human-reviewed work; descriptive evidence only | Research-supported extrapolation when applied to Arc | Method for structure |
| [ICM reference repo](https://github.com/RinDig/Interpretable-Context-Methodology) (MIT) | Working workspaces, five-layer routing, 15 conventions | Demonstrated existing capability | Conventions |
| [ICM Architect](https://github.com/RinDig/icm-architect) (MIT) | Sequences, shelves, catalogs; System map form; walk test; scripts | Demonstrated existing capability | PUSH 001, im-ICM |
| [AGENTS.md](https://agents.md/) | Open entry-file format, nearest-file precedence, Linux Foundation stewardship | Demonstrated existing capability | Entry file |
| [Agent Skills spec](https://agentskills.io/specification) | Skill package format | Demonstrated existing capability | M2 packages |
| [Voyager](https://arxiv.org/abs/2305.16291) | Reusable code-skill library in Minecraft | Established research (domain-limited) | Baseline |
| [ADAS](https://arxiv.org/abs/2408.08435) | Meta-agent search over an archive of coded agents | Established research | Prior art for evolution |
| [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) | Empirically validated self-modification; objective hacking observed | Established research | Evaluator isolation |
| [AFlow](https://arxiv.org/abs/2410.10762) | MCTS over code-represented workflows | Established research | Composition comparator |
| [DSPy](https://arxiv.org/abs/2310.03714) | Metric-driven compilation of LM pipelines | Established research | M5 comparator |
| [Li et al. 2010](https://arxiv.org/abs/1003.0146), [Chu et al. 2011](https://proceedings.mlr.press/v15/chu11a.html) | LinUCB; SupLinUCB regret bound | Established research | Stage 4, with stated assumptions |
| [Li et al. 2011 replay](https://arxiv.org/abs/1003.5956) | Unbiased offline evaluation needs randomized logging | Established research | Logging design |
| [Garcia et al. 2013](https://doi.org/10.1109/ASE.2013.6693106) | Low accuracy of automated architecture recovery vs ground truth | Established research | im-ICM labels architecture as inference |
| [RepoAgent](https://arxiv.org/abs/2402.16667) | LLM repository documentation kept in sync with Git | Demonstrated existing capability | im-ICM comparator |
| [SPDX, ISO/IEC 5962:2021](https://www.iso.org/standard/81870.html) | Standard software package metadata | Established standard | Scout outputs |
| [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | Provenance model (Recommendation, 2013) | Established standard | Lineage fields |
| [Parasuraman et al. 2000](https://doi.org/10.1109/3468.844354) | Types and levels of automation | Established research | Stream automation levels |
| [Nygard 2011 via Fowler](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html) | Architecture decision records | Established practice | `decisions/` shelf |
| [Pyodide constraints](https://pyodide.org/en/stable/usage/wasm-constraints.html) | No functional threads, multiprocessing or sockets | Demonstrated limitation | Browser profile |
| [Cyera Pyodide research](https://www.cyera.com/research/sandcastles-not-sandboxes-how-one-architectural-flaw-exposed-seven-products) | Import restrictions are not isolation | Demonstrated limitation | Sandbox policy |
| [GitHub REST rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), [Actions limits](https://docs.github.com/en/actions/reference/limits), [secure use](https://docs.github.com/en/actions/reference/security/secure-use), [events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [billing](https://docs.github.com/en/actions/concepts/billing-and-usage), [PR approval](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews), [wiki](https://docs.github.com/en/communities/documenting-your-project-with-wikis/adding-or-editing-wiki-pages), [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates) | Platform terms and limits | Official specification | Sections G and H |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Automated project health checks | Demonstrated existing capability | Scout, optional |

### Arc-Adapticon's own claims, classified

| Claim | Classification |
| --- | --- |
| Capability organization and reuse improve utility independent of model scale | Untested hypothesis |
| ICM can govern the whole project | Research-supported extrapolation, limited by G-01 |
| im-ICM improves review quality | Untested hypothesis (section E experiment) |
| Zero-incremental-cost baseline | Proposed engineering decision, feasible per section G |
| Synaptic Dynamism improves selection | Untested hypothesis |
| GitHub can serve as spine | Proposed engineering decision, supported by platform features |

**Not verified this session:** the graphify tool that ICM Architect mentions; licences of individual tree-sitter grammars and model weights; repository settings not visible without API access.

## Next engineering action

**Founder records decisions D-1 to D-3; then the implementing agent, under its own GitHub identity, opens one documentation-only pull request on branch `push-001-icm-foundation` containing exactly the section J manifest.** The PR description lists files created and modified, runs `python -I _tools/links.py` and includes its output, and reports the cold walk test from a fresh Claude session and a fresh Codex session. Claude reviews that exact commit; the founder approves and merges. ARC Scout v0.1 work starts only after that merge.
