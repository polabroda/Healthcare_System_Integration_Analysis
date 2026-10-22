# 03 – Requirements Catalogue

All requirements below are **hypothetical proposals**, not a customer-approved baseline. `PROPOSED` means stated for this case study; `TO VERIFY` means external or internal confirmation is needed; `BLOCKED` means a missing dependency prevents design finalization. Priorities are **illustrative MoSCoW proposals**.

## Business Requirements

| ID | Requirement | Rationale | Priority | Status |
|---|---|---|---|---|
| BR-001 | The HIS shall maintain one traceable medication product/package reference built from multiple external sources. | Avoid disconnected duplicate catalogues. | Must | PROPOSED |
| BR-002 | Each imported attribute shall retain its source and release provenance; registry identity shall not be replaced by coverage or enrichment fields. | Preserve accountability and authoritative ownership. | Must | PROPOSED |
| BR-003 | The HIS shall not present unmatched, ambiguous, expired or withdrawn-package coverage as currently applicable. | Prevent misleading reference information. | Must | PROPOSED |

## Functional Requirements

| ID | Proposed requirement | Verification evidence (planned) | Priority | Status |
|---|---|---|---|---|
| FR-001 | Import a versioned registration snapshot with its source release metadata and checksum. | Sample release parsed; metadata stored. | Must | PROPOSED |
| FR-002 | Validate registry source identifiers, record statuses and package GTINs before canonical mapping. | Invalid-row negative tests. | Must | PROPOSED |
| FR-003 | Create/update a canonical product and package with stable internal identifiers, without merging distinct source packages silently. | Deterministic import/reimport comparison. | Must | PROPOSED |
| FR-004 | Preserve withdrawn registry packages for historical reference while excluding them from active-package display. | Withdrawal-state test. | Must | PROPOSED |
| FR-005 | Import a versioned coverage release with effective-date fields and source row identifiers. | Sample CSV parsed and staged. | Must | PROPOSED |
| FR-006 | Match a coverage row to exactly one registry package only when its normalized GTIN is valid and unique. | Known/unmatched/duplicate match tests. | Must | PROPOSED |
| FR-007 | Quarantine unmatched or overlapping coverage rows without automatically choosing a winner. | Exception counts and reasons. | Must | PROPOSED |
| FR-008 | Show coverage as currently applicable only when the package and row are active and the evaluation date is within an unambiguous validity period. | Reference-date eligibility tests. | Must | PROPOSED |
| FR-009 | Retain imported source-release, source-row and import-run provenance on published mappings. | Field lineage review. | Must | PROPOSED |
| FR-010 | Detect duplicate release processing; identical replays produce no duplicate canonical package or coverage-rule records. | Same-release replay test. | Must | PROPOSED |
| FR-011 | Reject a reused release identifier if its payload checksum differs from the previously accepted content. | Tampered-release test. | Must | PROPOSED |
| FR-012 | Provide a quarantined-item report with reason, source identifier and safe reprocessing status. | Exception-report inspection. | Should | PROPOSED |
| FR-013 | Support controlled retry for transient ingestion failures without replaying already committed results. | Simulated transient-failure test. | Should | TO VERIFY |
| FR-014 | Record start/end, totals, state transitions and correlation IDs for each import run. | Mock audit/reconciliation review. | Must | PROPOSED |
| FR-015 | Permit optional commercial enrichment only after the interface contract and licensing are approved. | Gate prevents premature import. | Won't (MVP) | BLOCKED |

## Non-functional Requirements

| ID | Proposed requirement | Verification proposal | Priority | Status |
|---|---|---|---|---|
| NFR-001 | Import fixtures and operational logs in this scope shall contain no patient identifiers or personal health information. | Schema/log review. | Must | PROPOSED |
| NFR-002 | Access to import administration, quarantine review and publication shall be role restricted and audited. | Positive/negative authorization tests. | Must | TO VERIFY |
| NFR-003 | Import processing shall expose run counts, duration, errors and correlation identifiers without sensitive payload logging. | Observability design review. | Must | PROPOSED |
| NFR-004 | Invalid inputs shall not partially overwrite the last accepted canonical catalogue. | Publication-atomicity tests. | Must | PROPOSED |
| NFR-005 | Availability, throughput, backup, RPO/RTO and retention targets shall be agreed before production implementation. | Approved operational requirements. | Must | TO VERIFY |
| NFR-006 | Adapter mappings and source schema versions shall be controlled and reproducible between runs. | Version/change-control review. | Should | PROPOSED |

**Count: 3 business + 15 functional + 6 non-functional = 24 proposed requirements.**

## Dependency Map

- `FR-006` depends on `FR-002`, `FR-003` and `FR-005`.
- `FR-007`, `FR-008` and `BR-003` depend on `FR-006` and the coverage effective-date policy.
- `FR-009`, `FR-010`, `FR-011` and `NFR-004` depend on a stable release identity and publication transaction model.
- `FR-015` is blocked on source ownership, license and contract review (`DEC-06`).

## Open Questions for Baseline Approval

1. Does the actual HIS already define canonical product/package keys and source priorities?
2. Is GTIN alone sufficient to associate the feeds, or is a validated crosswalk necessary?
3. Who is authorized to resolve ambiguous coverage rows and how are retroactive corrections represented?
4. What audit retention, import recovery and access-control standards apply?
5. Is the coverage bulletin intended for information display only, or does a separate business process consume it?

None has been answered by a real client or implementation team.
