# Lineage shelf

[Origin](ORIGIN.md) explains intellectual origins; [EVENTS.jsonl](EVENTS.jsonl) is the sole full event ledger. Wiki later publishes repository records.

Events and decisions use separate status vocabularies. The vocabulary below applies only to ledger events; decision records use proposed, ratified, rejected or superseded ([template](../_templates/decision.md)).

Required fields: id, date, event, status, commit (the commit the event observes or refers to, which may precede the commit that records the event; null if none), supersedes (array of prior event IDs). Status: recorded = documented observation or proposal; pending = unresolved proposal; ratified = policy authorized; authorized = action approved but not necessarily performed; implemented = observed completed action; verified = observed check; superseded = closed by later event. Compute effective status from later supersession records; historical status remains unchanged. P002 migrated 0001–0017 in place (supersedes field added, 0011 spelling normalized); ARC-EVO-0026 records that migration. From ARC-EVO-0026 onward the ledger is append-only: no line already on main is edited, reordered or deleted; corrections are new events that supersede. Check that every line already on main is byte-identical, sequential unique IDs, valid JSON and backward references.
