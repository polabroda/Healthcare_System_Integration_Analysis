# 02 – Source Systems and Example Contracts

**Evidence status:** All sources, contracts and file names in this document are **fictional mock examples**. They are **not** real external API specifications, confirmed feeds or verified contractual capabilities.

## Source Overview

| Code | Fictional source | Purpose | Mock transport | Authority in proposal | Status |
|---|---|---|---|---|---|
| `REG` | Cedar Registry | Product/package identification and registration status | JSON snapshot file | Product name, status, package identifier, GTIN | DESIGN CANDIDATE |
| `COV` | Willow Coverage Bulletin | Effective-dated coverage reference attributes | CSV release file | Coverage tier and validity interval | DESIGN CANDIDATE |
| `ENR` | Pine Partner Catalogue | Optional supplementary descriptions | Unspecified | None until contract reviewed | BLOCKED |

**Separation of responsibility:** Coverage attributes cannot rewrite product identity. A licensed feed cannot be assumed available merely because a supplier might provide it.

## 1. Registry Snapshot (`REG`)

**Mock input:** [`sample_data/registry_snapshot.json`](sample_data/registry_snapshot.json)

Illustrative object:

```json
{
  "release_id": "REG-2026-10-20-A",
  "exported_at": "2026-10-20T06:00:00Z",
  "source_name": "Cedar Registry (fictional)",
  "records": [
    {
      "source_product_id": "PRD-001",
      "source_pack_id": "PAK-001",
      "gtin": "05901234567893",
      "name": "Demo Product Alpha",
      "strength": "10 mg",
      "form": "tablet",
      "status": "ACTIVE"
    }
  ]
}
```

This snippet is a subset, not the full file. Values and identifiers are invented. GTIN is **text**, because numeric conversion loses leading zeros.

### Contract Expectations (unverified proposal)

| Item | Rule | Status |
|---|---|---|
| Release metadata | `release_id`, `exported_at` required | PROPOSED |
| Identifiers | `source_product_id`, `source_pack_id` are required strings | PROPOSED |
| Package identity | One `source_pack_id` maps to one GTIN within a release | PROPOSED |
| GTIN | Exactly 14 digits, preserve leading zero, valid check digit | PROPOSED |
| Product state | `ACTIVE` or `WITHDRAWN` in the mock contract | PROPOSED |
| Repeated release | Same release ID with different payload checksum -> reject and investigate | PROPOSED |
| Authentication / availability | No real endpoint exists for this example | N/A |

The mock's status vocabulary is intentionally simplified and **must not be interpreted as a real registry's status model**.

## 2. Coverage Release (`COV`)

**Mock input:** [`sample_data/coverage_release.csv`](sample_data/coverage_release.csv)

Fields: `coverage_row_id`, `release_id`, `gtin`, `effective_from`, `effective_to`, `coverage_status`, `coverage_tier`.

| Field | Mock meaning | Constraint |
|---|---|---|
| `coverage_row_id` | Stable row identifier within a published release | Required and unique |
| `release_id` | Source release/version | Required |
| `gtin` | Package candidate matching key | 14-digit text with valid check digit |
| `effective_from` | Coverage start (inclusive) | ISO date |
| `effective_to` | Coverage end (inclusive) | ISO date; >= start |
| `coverage_status` | `ACTIVE` or `SUSPENDED` | Enumerated for demo only |
| `coverage_tier` | `FULL`, `PARTIAL` or `NONE` | Enumerated for demo only |

**Mock release semantics:** A row is currently applicable for a package only if the package exists, is `ACTIVE`, its row is `ACTIVE`, the evaluation date is in its validity window, and no overlapping competing coverage entries exist for that GTIN. Historical rows remain accessible for audit but are not presented as current coverage.

An unrecognized GTIN or **overlap for the same GTIN** enters quarantine until a domain owner resolves it. This is a conservative portfolio rule, **not a documented payer policy**.

## 3. Optional Enrichment (`ENR`)

- Licensing, rights to redistribute data, schema, identifiers, auth, frequency and support requirements: **NOT AVAILABLE**.
- Proposed adapter and import: **BLOCKED** until signed entitlement and genuine contract are obtained.
- No mock records are supplied or published as verified enriched clinical content.

## Contract Gaps Requiring Real Discovery

- Is the registry feed a full snapshot or a delta stream?
- What are the actual identifiers, versioning strategy, transport authentication and rate limits?
- How do coverage amendments and retroactive corrections work?
- Are GTIN collisions, missing identifiers or overlapping entitlements expected?
- How is an urgent correction promoted and how are stale snapshots rejected?
- What is the licensing boundary between downloaded vendor content and HIS displays?

## Source Provenance Principle

For each resulting canonical attribute, retain at least the **source code**, **source release**, **source record identifier**, **import run**, and **last published time**. The exact storage and retention model requires architecture and compliance approval.
