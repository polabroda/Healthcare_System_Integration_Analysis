# 01 – Integration Context and Business Need

## Scenario and Problem

Northbridge Clinics (**fictional**) is planning a reference-data component within its HIS. The current conceptual problem is that a registry-like file describes products and packages, while a payer-like file describes **time-bound coverage rules**. These datasets have different refresh cycles and can disagree.

A catalogue assembled without identity checks, provenance or effective dates could display stale or incorrectly matched information. This **case study does not validate clinical use** and deliberately excludes patient-level eligibility and prescribing decisions.

## Business Objectives (proposals)

| ID | Objective | Intended outcome | Evidence for future acceptance |
|---|---|---|---|
| OBJ-01 | Establish one auditable package reference | Each package has a stable internal key and source trace | Import review and duplicate checks |
| OBJ-02 | Preserve source authority | Registration attributes never silently overwritten by coverage data | Mapping review and provenance audit |
| OBJ-03 | Prevent ambiguous coverage display | Unmatched, conflicting, expired or inactive entries do not appear as valid current coverage | Synthetic reconciliation tests |
| OBJ-04 | Make imports recoverable | Failed batches can be investigated and safely replayed | Retry/idempotency demonstration |

All objectives are **unapproved analytical proposals**.

## Stakeholders and Information Needed

| Role (fictional) | Concern | Discovery question | Status |
|---|---|---|---|
| Clinical operations lead | Searchable product/package reference | Which package attributes are mandatory to search? | TO VERIFY |
| Pharmacy domain expert | Accurate product identity | What constitutes a distinct package? | TO VERIFY |
| Finance / coverage analyst | Applicable coverage data | Who approves source priority and effective-date semantics? | TO VERIFY |
| HIS development lead | Mapping and ingestion contract | Which canonical tables and adapter conventions already exist? | OPEN |
| Security/data protection lead | Access controls and logs | What data classes and retention policies apply? | OPEN |
| Integration operator | Monitoring and recovery | Who accepts a quarantined batch and who may replay it? | OPEN |

No interviews or stakeholder approval have occurred; these are roles and questions for a hypothetical discovery phase.

## System Boundary

**Included:** two fictional file feeds (JSON registration snapshot and CSV coverage release), validation, staging, mapping, reconciliation, controlled publication and operational audit. An optional licensed enrichment feed remains a future possibility only.

**Excluded:** live APIs, patient data, medication orders, prescriptions, interaction alerts, dosing, clinical decisions, insurance eligibility and user-facing clinical workflows.

See [system context](diagrams/integration_context.md).

## Working Assumptions

| ID | Assumption | Consequence if false | Status |
|---|---|---|---|
| ASM-01 | Registry package GTIN can serve as a match candidate | Additional product/pack crosswalk required | TO VERIFY |
| ASM-02 | Coverage rows have explicit start/end dates | Business rules needed to infer or reject validity | TO VERIFY |
| ASM-03 | Source payloads are versioned releases | Must introduce a reliable release identifier | TO VERIFY |
| ASM-04 | Reference-data import runs separately from clinical transactions | Publication/caching design would change | TO VERIFY |
| ASM-05 | No patient-level information is required in this scope | Privacy and security model would materially expand | PROPOSED |

## Proposed Nonbinding Success Measures

- A run records received, accepted, quarantined and publishable row counts, with no unexplained loss of rows.
- Publishing the same release twice yields the **same package and rule identifiers**.
- An expired or withdrawn package's coverage is **not presented as currently applicable**.
- Every published attribute has an identifiable source release and import run.

Numerical performance, availability, RPO/RTO, data retention and legal requirements **must be agreed by a real team**; none is claimed here.
