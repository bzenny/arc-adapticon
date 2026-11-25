# Lineage shelf

[Origin](ORIGIN.md) explains intellectual origins; [EVENTS.jsonl](EVENTS.jsonl) is the sole full event ledger. Wiki later publishes repository records.

Required fields: id, date, event, status, commit (null if not applicable), supersedes (array of prior event IDs). Status: recorded = documented observation or proposal; pending = unresolved proposal; ratified = policy authorized; authorized = action approved but not necessarily performed; implemented = observed completed action; verified = observed check; superseded = closed by later event. Compute effective status from later supersession records; historical status remains unchanged. Historical spelling correction and schema migration in P002 are explicit, not a rewrite of event meaning. Check sequential unique IDs, valid JSON and backward references.
