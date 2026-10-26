# Proposed Import and Reconciliation Flow

```mermaid
flowchart TD
    A["Receive fictional REG/COV file release"] --> B["Identify release ID and checksum"]
    B --> C{"Known release?"}
    C -- "Same checksum" --> D["Idempotent no-op or safe replay"]
    C -- "Different checksum" --> E["Reject release and raise integrity exception"]
    C -- "New release" --> F["Validate structure and source fields"]
    F --> G{"Fatal release error?"}
    G -- "Yes" --> H["Reject; retain last published revision"]
    G -- "No" --> I["Stage source rows with provenance"]
    I --> J["Map REG products/packages and reconcile COV"]
    J --> K["Quarantine invalid, unmatched or overlapping rows"]
    J --> L["Evaluate status and effective dates"]
    L --> M{"Publication policy and run checks approved?"}
    M -- "No" --> N["Hold revision for review"]
    M -- "Yes" --> O["Publish catalogue revision atomically"]
    O --> P["Record counts, errors and audit trail"]
    K --> P
```

**Status:** `DESIGN CANDIDATE`. Partial publication with quarantined rows is **OPEN (`DEC-03`)**; neither branch claims real implementation or execution.

See [data flow and synchronization](../05_data_flow_and_synchronization.md) and [validation and errors](../06_validation_and_error_handling.md).
