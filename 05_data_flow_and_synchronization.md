# 05 – Data Flow and Synchronization

**Status: DESIGN CANDIDATE.** No real endpoint, worker, staging database or production pipeline has been implemented or exercised for this case study.

## Proposed Pipeline

1. **Acquire** a release from a source-specific, authenticated mechanism to be defined in a real project. In this demonstration, files are **local fixtures**, not downloaded data.
2. **Identify** source, release ID, schema version and payload digest. A reused ID with a different digest must stop the run (`FR-011`).
3. **Validate transport/structure** before writing canonical state (`FR-001`, `FR-005`).
4. **Stage** rows unchanged, retaining source-row identifiers and row-level outcomes.
5. **Validate domain rules** and map registry products/packages to canonical records (`FR-002`, `FR-003`).
6. **Reconcile coverage** against unique, valid package GTINs; hold unmatched/overlap cases (`FR-006`, `FR-007`).
7. **Calculate current applicability** at a documented evaluation timestamp (`FR-008`).
8. **Review run totals and critical errors**; block publication when release-level consistency fails (`NFR-004`).
9. **Publish atomically** as a new catalogue revision or maintain the previously published revision (`NFR-004`).
10. **Audit** the run, its input versions and its exceptions (`FR-009`, `FR-014`).

See the [proposed pipeline diagram](diagrams/import_and_reconciliation.md).

## Proposed Run States

`RECEIVED → VALIDATING → STAGED → RECONCILING → READY_TO_PUBLISH → PUBLISHED`

Alternative states: `QUARANTINED_ROWS`, `FAILED`, `REJECTED_RELEASE`, `BLOCKED_FOR_REVIEW`. Row-level quarantine need not imply wholesale run failure; the exact partial-publication policy is **OPEN** (`DEC-03`).

## Refresh, Release and Replay Semantics

| Situation | Proposed behavior | Status |
|---|---|---|
| New release ID + new digest | Run validation and controlled publication | PROPOSED |
| Same release ID + same digest | No-op or safely replay without duplicate canonical records | PROPOSED |
| Same release ID + different digest | Reject; record contract integrity exception | PROPOSED |
| Source temporarily unavailable | Keep last accepted catalogue, alert operator, retry according to policy | TO VERIFY |
| Coverage release arrives before matching registry version | Hold coverage pending validated dependency | TO VERIFY |
| Retroactive corrections | Preserve release history, recompute relevant effective-date view | OPEN |
| Optional vendor feed | Do not ingest until license and contract are confirmed | BLOCKED |

**Idempotency scope:** `source_code + release_id + payload_digest`, together with stable canonical source identifiers. Exactly-once processing across external networks is **not** claimed.

## Safe Retry Policy (design proposal)

- Retry only for transient network or storage failures; apply capped exponential backoff and a defined retry budget in a real design.
- Do **not** automatically retry malformed source rows, invalid GTINs, duplicate identities or an inconsistent checksum.
- Replaying an already published release must not create duplicate coverage rules or new canonical package IDs.
- Every manual replay requires an actor, reason and correlation identifier.

## Atomic Publication Boundary

Validate a proposed revision before making it visible. A fatal release error must not partially overwrite the previous accepted state. Whether quarantined **row-level** exceptions can coexist with a published revision requires explicit decision `DEC-03`.

## Worked Synthetic Reconciliation

From the supplied fixtures, with an invented reference date of **2026-10-22**:

| Measure | Count | Explanation |
|---|---:|---|
| Registry package records | 4 | 3 ACTIVE, 1 WITHDRAWN |
| Coverage rows | 6 | COV-001 to COV-006 |
| Matched without overlap conflict | 3 | COV-001, COV-002, COV-003 |
| Quarantined: unmatched GTIN | 1 | COV-004 |
| Quarantined: overlapping GTIN rules | 2 | COV-005, COV-006 |
| Current publishable coverage rows | 1 | COV-001 |
| Suppressed: expired | 1 | COV-002 |
| Suppressed: withdrawn package | 1 | COV-003 |

The numbers are **fixture expectations**, not observed integration performance. The companion Python script only checks these local invented inputs.
