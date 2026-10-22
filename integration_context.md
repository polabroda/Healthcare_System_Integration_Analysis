# System Context – Fictional Medication Reference Data

```mermaid
flowchart LR
    REG["Cedar Registry<br/>(fictional registration snapshot)"] --> ING["HIS reference-data import<br/>(design proposal)"]
    COV["Willow Coverage Bulletin<br/>(fictional effective-dated CSV)"] --> ING
    ENR["Pine Partner Catalogue<br/>(BLOCKED: licensing and contract)"] -.-> ING
    ING --> STG["Staging and validation"]
    STG --> CAN["Canonical product / package model"]
    CAN --> VIEW["Reference catalogue view<br/>(not clinical prescribing)"]
    STG --> EX["Exception queue and run audit"]
    OPS["Integration operator"] -.-> EX
```

**Legend:** Solid arrows are **proposed** data flows. Dotted arrows indicate **unimplemented/unverified** dependencies or human review. No service shown is a real vendor API.

See [integration context](../01_integration_context.md) and [source contracts](../02_source_systems_and_contracts.md).
