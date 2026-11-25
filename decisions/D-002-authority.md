# D-002 — Progressive implementation authority (Rev. 1)

Original decision ratified 2026-11-25: distinct implementation identity, protected main and founder-specific review. Founder amendment: "i understand the concerns of claude, but in this initial stage we are only going to implement the core account. If we get to a stoppage or problem, we will convert to a new bifurcated account structure."

The following is the complete implementation-policy wording recorded in the conversation, not a verbatim founder quotation:

# D-002 Rev. 1 — Progressive Implementation Authority

**Date:** November 25, 2026  
**Status:** Founder-authorized amendment  
**Supersedes:** Original D-002 identity separation requirement

## Decision

During the initial development of Arc-Adapticon, the existing founder-controlled GitHub account shall serve as the primary implementation identity.

Separate implementation and administrative identities are deferred until operational complexity, security requirements, external contributions or governance limitations justify their introduction.

## Interim controls

1. Every proposed push requires prior disclosure of its scope and intended consequences.
2. Substantive development occurs through feature branches and pull requests.
3. Claude independently reviews the exact candidate commit.
4. Review findings and corrective actions are recorded.
5. Automated verification is introduced alongside executable functionality.
6. Human authorization is required before consequential repository changes and merges.
7. Direct changes to main are avoided except for explicitly authorized administrative or recovery operations.
8. Intellectual, architectural and implementation lineage is preserved.

## Migration triggers

Separate implementation identities shall be reconsidered when:

- External contributors become active.
- Identity restrictions obstruct development or verification.
- Automated agents require independent repository permissions.
- Security or credential exposure increases materially.
- Public deployment introduces consequential operational responsibilities.
- Procedural authorization proves insufficient.

## Accepted limitation

During the initial phase, independent human authorization is procedurally enforced rather than fully enforced through separate GitHub reviewer identities.

This limitation is acknowledged and shall not be represented as technically enforced identity separation.
