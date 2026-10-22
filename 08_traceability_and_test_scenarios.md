# 08 – Requirements Traceability and Draft Test Scenarios

The scenarios below are **test designs** for a hypothetical HIS integration, not executed end-to-end tests or user acceptance evidence. The only executable component is the **fixture consistency check** described in README; it does not validate a real adapter or clinical use.

## Requirements-to-Design Traceability

| Requirements | Design reference | Draft test IDs |
|---|---|---|
| BR-001, FR-001, FR-002, FR-003 | `02_source_systems_and_contracts`, `04_canonical_data_model_and_mapping` | IT-01, IT-02, IT-09 |
| BR-002, FR-009, FR-014 | `04_canonical_data_model_and_mapping`, `06_validation_and_error_handling` | IT-10 |
| BR-003, FR-004, FR-008 | `04_canonical_data_model_and_mapping` | IT-04, IT-05 |
| FR-005, FR-006 | `02_source_systems_and_contracts`, `04_canonical_data_model_and_mapping` | IT-03, IT-06 |
| FR-007, FR-012 | `06_validation_and_error_handling` | IT-06, IT-07 |
| FR-010, FR-011 | `05_data_flow_and_synchronization` | IT-08, IT-09 |
| FR-013, NFR-004 | `05_data_flow_and_synchronization`, `06_validation_and_error_handling` | IT-11 |
| FR-015 | `07_risks_and_architecture_decisions` | IT-12 |
| NFR-001, NFR-002, NFR-003 | `06_validation_and_error_handling` | IT-10, IT-12 |
| NFR-005, NFR-006 | `07_risks_and_architecture_decisions` | IT-08, IT-11 |

## Draft Integration Tests (not executed on an HIS)

| Test | Input / precondition | Proposed expected result | Requirement |
|---|---|---|---|
| IT-01 – Valid registration snapshot | Fictional REG release contains four valid packages | Four stable package references with provenance are staged; no patient data | FR-001, FR-003 |
| IT-02 – Leading-zero identifier | GTIN `05901234567893` supplied as a string | Value retains 14 digits and leading zero | FR-002 |
| IT-03 – Exact package match | Coverage `COV-001` points to GTIN of `PAK-001` | One and only one package match | FR-005, FR-006 |
| IT-04 – Expired coverage | `COV-002` expires before the fixture date | Rule retained historically, not currently displayed | FR-008, BR-003 |
| IT-05 – Withdrawn registry pack | `COV-003` points to withdrawn `PAK-003` | Package and rule traceable, no current coverage | FR-004, FR-008 |
| IT-06 – Unmatched GTIN | `COV-004` points to no registry package | Exception `E-NO-MATCH`; row quarantined | FR-006, FR-007 |
| IT-07 – Overlapping intervals | `COV-005` and `COV-006` overlap for `PAK-004` | Both quarantined as `E-OVERLAP`; no auto-winner | FR-007 |
| IT-08 – Identical replay | Same release ID and identical digest processed again | No duplicate package/rule IDs | FR-010, NFR-006 |
| IT-09 – Mutated replay | Same release ID with changed payload digest | Reject with release conflict; published revision unchanged | FR-011, NFR-004 |
| IT-10 – Audit/security review | Inspect mock import record and role permissions | Source lineage present; unauthorized publication denied; no sensitive payload logging | FR-009, FR-014, NFR-001/002/003 |
| IT-11 – Transient failure | Interrupt acquisition or publication | Bounded retry/rollback; last accepted catalogue remains | FR-013, NFR-004/005 |
| IT-12 – License gate | Optional ENR source has no verified entitlement | Adapter remains blocked; no vendor content imported | FR-015 |

## Example Fixture Reconciliation Oracle

At evaluation date `2026-10-22`, the invented test dataset contains:

- **4** registry packages; **3** active, **1** withdrawn.
- **6** coverage rows; **3** matched without interval conflict, **1** unmatched, **2** overlapping.
- Among the 3 nonconflicting rows, **1** currently publishable, **1** expired and **1** suppressed because its package is withdrawn.
- Therefore, **3** coverage rows in quarantine; only **COV-001** eligible for current display **if partial publication is authorized** (`DEC-03` remains OPEN).

See [`expected_reconciliation.json`](sample_data/expected_reconciliation.json). Run `python scripts/validate_fixtures.py` to check fixture consistency. **This is not a production or HIS integration-test suite.**

## Acceptance and Evidence Gaps

- No real source/API connectivity has been established.
- No clinician/pharmacist/business stakeholder has approved this model.
- No production performance, security or recovery tests have been conducted.
- Publication with row-level exceptions requires an unresolved policy decision.
- No clinical decision-support or prescribing safety conclusion can be drawn from the fixtures.
