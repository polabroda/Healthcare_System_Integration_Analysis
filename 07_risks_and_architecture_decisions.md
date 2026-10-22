# 07 – Risks, Dependencies and Architecture Decisions

This register is **illustrative** and is not the output of a real security, vendor or architecture review.

## Risk Register

| ID | Risk | Impact | Proposed mitigation | Status |
|---|---|---|---|---|
| R-01 | Incorrect package match across sources | High: wrong reference attribution | Validate GTIN and uniqueness; quarantine ambiguity | OPEN |
| R-02 | Coverage validity misinterpreted | High: outdated coverage displayed | Explicit inclusive date policy and tests | OPEN |
| R-03 | Source changes schema or status vocabulary | High: failed/misleading imports | Schema-version pinning and contract regression tests | OPEN |
| R-04 | Import replay duplicates packages or coverage rules | High: inconsistent catalogue | Stable IDs, digest-based idempotency and transaction control | OPEN |
| R-05 | Partial failure overwrites accepted reference data | High: availability and integrity loss | Stage, validate and publish atomically | OPEN |
| R-06 | Commercial enrichment imported without license | High: contractual/legal exposure | Gate optional feed, require vendor agreement | BLOCKED |
| R-07 | Operational logs capture sensitive content | High: privacy/security exposure | Minimal run metadata, log review, restricted access | OPEN |
| R-08 | Stale source releases go unnoticed | Medium/High: outdated reference | Source freshness metrics and escalation thresholds | TO VERIFY |

## Open Architecture / Business Decisions

| ID | Question | Required owner | Impact if unresolved | Status |
|---|---|---|---|---|
| DEC-01 | Which system owns stable product and package IDs in a real HIS? | HIS architect + domain expert | Canonical model cannot be signed off | OPEN |
| DEC-02 | Is GTIN sufficient for coverage association, or is a validated crosswalk mandatory? | Domain owner + data architect | Matching algorithm may be unsafe | OPEN |
| DEC-03 | Can a release with quarantined rows be partially published? Under what threshold and approval? | Business owner + operations + security | Publication policy not final | OPEN |
| DEC-04 | How are coverage amendments, cancellations and retroactive intervals resolved? | Coverage domain expert | Temporal consistency undefined | OPEN |
| DEC-05 | What are authentication, access roles, retention and recovery objectives? | Security + operations | NFR acceptance blocked | OPEN |
| DEC-06 | Is optional enrichment licensed and what exact vendor contract exists? | Procurement/legal + vendor | Vendor adapter cannot be implemented | BLOCKED |
| DEC-07 | Which real source release identifiers, delivery channels and schedules exist? | Integration owner | Live adapter design unavailable | OPEN |
| DEC-08 | Are any outputs allowed to inform clinical decisions or prescribing workflows? | Clinical safety + product owner | Separate validation and controls required | OUT OF SCOPE |

## Dependencies

```text
Source contract + licensing → validated adapter and entitlement
        ↓
Release identity + schema validation → staging and reproducibility
        ↓
Approved identity/matching policy → canonical mapping
        ↓
Approved temporal/exception rules → coverage reconciliation
        ↓
Publication/operations policy → controlled rollout and monitoring
```

## Proposed Delivery Boundary

- **Phase A — analysis & contract discovery:** source ownership, identity, security and schema decisions; no production import.
- **Phase B — mock prototype:** local synthetic fixtures and integration tests; no live data.
- **Phase C — real integration candidate:** only after verified provider access, approved architecture, legal/licensing review and clinical/domain sign-off if applicable.

The repository contains **Phase A analytical documents** plus a tiny **local fixture check**; it does not claim completion of Phase B or C as an operational project.
