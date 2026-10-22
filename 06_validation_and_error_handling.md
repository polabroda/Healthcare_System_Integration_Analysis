# 06 – Validation, Error Handling and Observability

## Validation Layers (Proposed)

| Layer | Example check | Invalid outcome | Requirement |
|---|---|---|---|
| Release identity | Required `release_id`, distinct digest for distinct accepted content | Reject or block whole release | FR-001, FR-011 |
| Structural contract | JSON object/CSV columns, required fields and types | Reject malformed release / quarantine row | FR-002, FR-005 |
| Product/package identity | Stable source IDs, unique pack, supported source status | Quarantine affected registry row | FR-002, FR-003 |
| GTIN | String of 14 digits with valid check digit | Quarantine affected row | FR-002, FR-006 |
| Coverage dates | Parseable ISO date, end >= start | Quarantine coverage row | FR-005 |
| Referential integrity | Coverage GTIN maps to exactly one source package | Quarantine coverage row | FR-006, FR-007 |
| Cross-row conflict | Overlapping time intervals for same GTIN | Quarantine all conflicting rows | FR-007 |
| Temporal display | Package ACTIVE, row ACTIVE, `from <= date <= to` | Keep history; suppress current display | FR-004, FR-008 |
| Publication | Mandatory checks and totals completed | Keep prior published revision | NFR-004 |

## Exception Taxonomy

| Code | Meaning | Proposed action | Retry? |
|---|---|---|---|
| `E-REL-ID` | Release ID reused with changed payload | Reject/review source | No |
| `E-STRUCT` | Invalid structural contract | Reject release or row according to scope | No |
| `E-PACK-ID` | Conflicting registry package identifier | Quarantine | No |
| `E-GTIN` | GTIN invalid or not unique | Quarantine | No |
| `E-NO-MATCH` | Coverage package missing in registry | Quarantine; await source review | Not automatically |
| `E-OVERLAP` | Conflicting coverage windows for same GTIN | Quarantine affected rows | No |
| `E-DATE` | Invalid validity dates | Quarantine | No |
| `E-SOURCE-TEMP` | Transient source/transport outage | Hold state; bounded retry | Yes |
| `E-PUBLISH` | Publication transaction failed | Roll back; retry under run lock | Conditional |

Example exception evidence for this toy dataset: `COV-004` -> `E-NO-MATCH`; `COV-005` and `COV-006` -> `E-OVERLAP`.

## Publication vs Quarantine

Row-level errors should never be silently rewritten. Preserve source row, reason and review state. **Whether partial publication is permissible** is unresolved (`DEC-03`), even though the supplied fixture shows what a *conditional* publishable subset would look like.

This distinction matters: a local test that counts 1 `publishable` rule does **not** confirm that a real policy allows publication of a release with 3 quarantined rows.

## Observability and Safe Audit

Suggested run-event fields: `run_id`, `source_code`, `release_id`, `source_checksum`, `schema_version`, `state`, `received_count`, `validated_count`, `quarantined_count`, `published_count`, `error_code`, `started_at`, `finished_at`.

Suggested monitoring: elapsed processing time, failed/retried releases, row mismatch rates, stale snapshots, source availability and reconciliation backlogs. Thresholds, retention and escalation contacts require approval.

**No personal health information** is needed for this portfolio's reference-data problem. Do not include patient data, access tokens, credentials or full sensitive records in logs. A real system requires a security/privacy review appropriate to its actual data and use.

## Representative Recovery Scenarios

- **Malformed coverage CSV**: identify invalid columns or dates; quarantine or reject according to severity; do not auto-correct without business policy.
- **Unmatched package**: keep row with `E-NO-MATCH`, do not infer a product from a similar name.
- **Reused source version with different content**: stop and investigate, rather than treating it as an ordinary re-import.
- **Source unavailable**: retain previous accepted view, flag data freshness, apply a reviewed retry policy.
- **Deployment rollback**: restore prior published revision and preserve incident/provenance records.

No recovery procedure has been tested against a real HIS.
