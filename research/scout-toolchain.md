# Scout toolchain — adopt-or-defer assessment

Source inspection 2026-11-25, official upstream documentation; no binaries installed, no tests run, no versions approved. Ratified as [D-005](../decisions/D-005-scout-toolchain.md): ScanCode and Syft are optional adapters subject to vetting, OSV-Scanner deferred. This does not authorize installation or execution of the proposed adapters.

| Tool | Decision | Rationale |
|---|---|---|
| [ScanCode Toolkit](https://github.com/aboutcode-org/scancode-toolkit) | Adopt as optional adapter candidate, defer installation | License/copyright evidence and package metadata; preserve mixed data/third-party notices; [NOTICE](https://github.com/aboutcode-org/scancode-toolkit/blob/develop/NOTICE). |
| [Syft](https://github.com/anchore/syft) | Adopt as optional adapter candidate, defer installation | Local directory SBOM, SPDX/CycloneDX/JSON; Apache-2.0 per upstream. Do not build images or resolve remote artifacts. |
| [OSV-Scanner](https://github.com/google/osv-scanner) | Defer until bounded vulnerability stage | Lockfile vulnerability assessment; offline mode requires previously obtained database, see [offline docs](https://github.com/google/osv-scanner/blob/main/docs/offline-mode.md). No silent network calls or remediation. |

M1 inventory requires only Git + Python standard library, not replacement SCA parsers. If no vetted adapter exists, report license/dependency assessment unknown rather than claim completeness. Before adoption pin release and digest, inspect licenses/data notices, confirm resource and offline policy, test hostile inputs and canaries, normalize outputs with source references; no execution or installation of scanned code. Record database age and coverage, not a safety guarantee. Isolated sanitized read-only materialization only if adapter needs filesystem; no unsafe paths, links or checkout hooks. No mandatory paid services.
