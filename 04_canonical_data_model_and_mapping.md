# 04 – Canonical Data Model and Mapping

The following is an **illustrative logical model**, not a database schema approved by a real HIS architect. Field names are placeholders and deliberately differ from real vendor contracts.

## Proposed Logical Entities

| Entity | Suggested key | Selected fields | Purpose |
|---|---|---|---|
| `source_release` | `source_code + release_id` | checksum, published_at, received_at, schema_version | Reproducible input identity |
| `import_run` | `run_id` | source_release, started_at, ended_at, state, row_counts | Execution/audit trail |
| `source_record` | `source_code + release_id + source_row_id` | original_payload_ref, validation_status | Raw/staged lineage |
| `drug_product` | `product_id` | registry_product_id, name, form, strength | Basic registration identity |
| `drug_package` | `package_id` | source_package_id, product_id, gtin, registry_status | Identifiable sellable pack |
| `coverage_rule` | `coverage_rule_id` | source_row_id, package_id, tier, valid_from, valid_to, status | Time-dependent rule |
| `integration_exception` | `exception_id` | run_id, source_row_id, reason_code, resolution_status | Remediation workflow |

A **source record** and a **canonical record** are not the same object. Raw source releases and reconciliation evidence must remain distinguishable from current published state.

## Identity and Matching Policy

1. The registration source is the proposed authority for `drug_product` and `drug_package` identity.
2. Use the original registry `source_pack_id` as the stable source reference. The HIS creates its **own** immutable canonical `package_id`.
3. Match a coverage row to an active/withdrawn package only if its GTIN is a valid 14-digit string with a correct check digit **and resolves to exactly one registry package**.
4. A missing/multiple matching package is **not** resolved by fuzzy product-name matching.
5. Keep leading zeros; treat GTIN as **text**, never a numeric measurement.
6. Overlapping coverage rows for one GTIN are **quarantined** in this demonstration rather than combined or selected by last-write-wins.
7. Coverage status is a **time- and package-dependent view**. No coverage field may overwrite a registration status.

This policy is a conservative **DESIGN CANDIDATE**, not a mandated real-world regulatory rule.

## Field-Level Source-to-Canonical Mapping

| Source field | Canonical field | Transformation | Validation / fallback |
|---|---|---|---|
| `REG.release_id` | `source_release.release_id` | Preserve exact string | Missing -> reject release |
| `REG.records[].source_product_id` | `drug_product.registry_product_id` | Preserve exact string | Missing -> quarantine row |
| `REG.records[].source_pack_id` | `drug_package.source_package_id` | Preserve exact string | Duplicated ID with conflicting GTIN -> quarantine |
| `REG.records[].gtin` | `drug_package.gtin` | Preserve text; do not coerce number | Invalid check digit -> quarantine row |
| `REG.records[].name` | `drug_product.name` | Trim outer whitespace | Empty -> quarantine row |
| `REG.records[].strength` | `drug_product.strength` | Preserve display text | Missing -> domain decision |
| `REG.records[].status` | `drug_package.registry_status` | Enumerated `ACTIVE/WITHDRAWN` | Unknown -> quarantine row |
| `COV.coverage_row_id` | `coverage_rule.source_row_id` | Stable per release | Duplicate -> quarantine |
| `COV.gtin` | `coverage_rule.package_id` | Find unique package by GTIN | No/ambiguous match -> quarantine |
| `COV.effective_from` | `coverage_rule.valid_from` | Parse ISO date | Invalid -> quarantine row |
| `COV.effective_to` | `coverage_rule.valid_to` | Parse ISO date | End before start -> quarantine row |
| `COV.coverage_status` | `coverage_rule.status` | Preserve supported enum | Unknown -> quarantine row |
| `COV.coverage_tier` | `coverage_rule.tier` | Preserve `FULL/PARTIAL/NONE` | Unknown -> quarantine row |

## Publication Rules: Fictional Evaluation Date

Let `T = 2026-10-22` for the supplied sample data only. A coverage row is **publishable as current** if:

```text
registry_package_exists_and_unique
AND registry_status == ACTIVE
AND coverage_status == ACTIVE
AND effective_from <= T <= effective_to
AND no_overlapping_conflicting_coverage_rows_for_same_gtin
```

A registry package marked `WITHDRAWN` is retained as a historical item. A coverage row associated with it can be kept in audited data but **is not currently displayed**. An expired row can likewise be retained without being currently published.

## Concrete Example

| Source pack | GTIN | Registry state | Example coverage | Outcome on `2026-10-22` |
|---|---|---|---|---|
| `PAK-001` | `05901234567893` | ACTIVE | `COV-001`, valid through 2026-12-31 | **Current** |
| `PAK-002` | `05901234567909` | ACTIVE | `COV-002`, ended 2026-10-20 | Suppressed: expired |
| `PAK-003` | `05901234567916` | WITHDRAWN | `COV-003`, unexpired | Suppressed: withdrawn |
| `PAK-004` | `05901234567923` | ACTIVE | `COV-005` and `COV-006`, overlapping | Both quarantined |
| — | `05901234567930` | No matching pack | `COV-004` | Quarantined: unmatched |

## Source Ownership and Provenance

Persist source code, source release ID, source row ID, transform version and import-run ID. **Every proposed field mapping and authority rule remains subject to real domain/architecture review**.

See [mock inputs](sample_data/registry_snapshot.json) and [coverage CSV](sample_data/coverage_release.csv).
