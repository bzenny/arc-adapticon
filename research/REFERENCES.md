# Research register

- [ICM paper](https://arxiv.org/abs/2603.16021): descriptive methodology, not controlled evidence of ARC benefit.
- [ICM Architect pinned](https://github.com/RinDig/icm-architect/tree/8bc2f5610d3843b3ffa31a142effe6b6337fef3c): practical conventions, System Map, sequences/shelves/catalogs.
- [W3C PROV](https://www.w3.org/TR/prov-dm/): provenance model.
- [Voyager](https://arxiv.org/abs/2305.16291): skill reuse in a specific environment.
- [DSPy](https://arxiv.org/abs/2310.03714), [AFlow](https://arxiv.org/abs/2410.10762): candidate program/workflow optimization.
- [Contextual bandits](https://arxiv.org/abs/1003.0146): candidate adaptive selection.

ARC improvement, transfer and novelty remain untested; zero mandatory service cost is a design target. Starting register, not systematic review.

## Imported register (FR-001 section K)

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

Source: [FR-001 genesis review](reviews/FR-001-genesis-review.md), section K, imported unchanged in PUSH 003 (H-12, I-10). Bandit roles: Li et al. 2010 is LinUCB; the regret bound is Chu et al. 2011.
