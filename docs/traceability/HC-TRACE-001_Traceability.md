# HC-TRACE-001 — Traceability

## Status
`ACTIVE — F80 / BENCH IMPLEMENTATION`

## Baselined upstream lineage

| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | Baselined |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | Baselined |
| HC-FND-003 | Current names are engineering codenames only | README / CURRENT_STATE | Baselined |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | Baselined |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | Baselined |
| HC-ARS-OP-001 | Structured rapid operator workflow | ARS → SA → LEL → REQ → IMP | Baselined |
| HC-ARS-VET-001 | Human clinical authority and provenance | ARS → ADR → SA → LEL → REQ | Baselined |
| HC-ARS-DATA-001 | Integrity, auditability and media/session linkage | ARS → SA → LEL → REQ → IMP | Baselined |
| HC-ARS-REP-001 | Multi-audience reporting | ARS → ADR → SA → REQ → IMP → S5 | Baselined |
| HC-ADR-001 | HMI and edge/data responsibilities separated | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-002 | KVK strategy is observation-only | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-003 | Immutable internal animal identity | ADR → SA → LEL → REQ | Baselined |
| HC-ADR-004 | Media are provenance-linked evidence objects | ADR → SA → LEL → REQ → S5 | Baselined |
| HC-ADR-005 | Persistence is local-first with recovery | ADR → SA → REQ → S2 | Baselined |
| HC-ADR-006 | Veterinary nomenclature controlled/versioned; human authority final | ADR → SA → LEL → REQ | Baselined |
| HC-ADR-007 | Reports derive from canonical records | ADR → SA → REQ → IMP → S5 | Baselined |
| HC-SA-001 | Edge/application layer owns canonical lifecycle | SA → LEL → REQ → S1/S3 | Baselined |
| HC-SA-002 | Durable store is independent of HMI replacement | SA → REQ → S2 | Baselined |
| HC-SA-003 | KVK observation adapter has no write/actuation route | SA → LEL → REQ → IMP | Baselined |
| HC-SA-006 | HoofCare failure cannot affect KVK safety | SA → REQ → IMP | Baselined |
| HC-LEL-001 | Explicit session states and terminal semantics | LEL → REQ → S1 | Baselined |
| HC-LEL-002 | Ambiguous identity fails closed | LEL → REQ → S1/S3 | Baselined |
| HC-LEL-004 | KVK events are observation-only | LEL → REQ → IMP | Baselined |
| HC-LEL-005 | Durable/idempotent canonical transitions | LEL → REQ → S1/S2/S3 | Baselined |
| HC-REQ-HMI-001 | Dashboard + structured HMI workflow with no KVK actuation affordance | REQ → IMP → S3/S4 | Baselined |
| HC-REQ-REP-001 | Reports derive from committed canonical records and linked media | REQ → S5 | Baselined |
| HC-REQ-REP-002 | Bench MVP supports local PDF report | REQ → S5 | Baselined |
| HC-REQ-REP-003 | Report model supports farmer/vet/zootechnician/nutritionist/technical sections | REQ → S5 | Baselined |
| HC-REQ-REP-004 | Reports carry report ID, timestamp and source session ID | REQ → S5 | Baselined |
| HC-REQ-REP-005 | Reports carry non-diagnostic clinical disclaimer | REQ → S5 | Baselined |
| HC-REQ-DATA-001 | Durable local store/audit/synthetic bench boundary | REQ → S2/S5 | Baselined |
| HC-REQ-KVK-001 | KVK remains observation-only; physical integration blocked pending audit | REQ → IMP | Baselined |
| HC-REQ-MVP-001 | Bench MVP requires acceptance and negative tests | REQ → S1-S7 | Baselined |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | Approved / Baselined PR #8 |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | ACTIVE — PR #8 |

## Runtime slice lineage

| ID | Evidence / invariant | Artifact | Status |
|---|---|---|---|
| HC-S1-RED-001 | Tests fail before domain implementation | tests/test_session_core.py | Verified RED @ `52b4fca3ca719b035d2cc7c5091447c607b6fd83` |
| HC-S1-CORE-001 | Session lifecycle and identity core | src/hoofcare/domain/session.py | MERGED / VERIFIED PR #9 |
| HC-S2-RED-001 | Persistence tests fail before store exists | tests/test_persistence.py | Verified RED @ `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` |
| HC-S2-STORE-001 | Snapshot persistence outside HMI | src/hoofcare/persistence/local_store.py | MERGED / VERIFIED PR #10 |
| HC-S3-RED-001 | HMI-edge contract tests fail before contract exists | tests/test_hmi_edge_contract.py | Verified RED @ `882afd05b9cbb94bc3265652becc245992998271` |
| HC-S3-CONTRACT-001 | Local in-process result/error contract | src/hoofcare/application/contract.py | MERGED / VERIFIED PR #11 |
| HC-S3-NOACT-001 | No KVK actuation/command surface is exposed | contract + tests | MERGED / VERIFIED PR #11 |
| HC-S4-RED-001 | HMI workflow tests fail before workflow model exists | tests/test_hmi_workflow.py | Verified RED @ `36608bfcdf02ef4585ee177519d8966ca143dd4b` |
| HC-S4-DASH-001 | Dashboard exposes counters and approved operator banner | src/hoofcare/hmi/workflow.py, tests | MERGED / VERIFIED PR #12 |
| HC-S4-PATH-001 | Workflow is ordered limb → claw → zone → lesion → treatment | src/hoofcare/hmi/workflow.py, tests | MERGED / VERIFIED PR #12 |
| HC-S4-ZONE-001 | Required anatomical zones are represented | src/hoofcare/hmi/workflow.py, tests | MERGED / VERIFIED PR #12 |
| HC-S4-LESION-001 | Controlled lesion options include approved bench catalogue | src/hoofcare/hmi/workflow.py, tests | MERGED / VERIFIED PR #12 |
| HC-S4-NOACT-001 | HMI model exposes no KVK machine-control affordance | src/hoofcare/hmi/workflow.py, tests | MERGED / VERIFIED PR #12 |
| HC-S5-RED-001 | Reporting tests fail before report implementation exists | tests/test_reporting.py | Verified RED @ `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` |
| HC-S5-CANON-001 | Report generation requires committed canonical source | src/hoofcare/reporting/report.py, tests | Implemented / GREEN |
| HC-S5-PROV-001 | Report carries report ID, generated timestamp and source session ID | reporting + tests | Implemented / GREEN |
| HC-S5-AUDIENCE-001 | Required audience sections are present | reporting + tests | Implemented / GREEN |
| HC-S5-DISCLAIMER-001 | Output is synthetic/test-only and explicitly non-diagnostic | reporting + tests | Implemented / GREEN |
| HC-S5-LOCALPDF-001 | Bench report emits local PDF-signature document bytes with no network/cloud delivery | reporting + tests | Implemented / GREEN |

## Canonical checkpoints
- PR #1 Foundation → `de68522e4851f645d65dee7dda08ef8fed6af955`.
- PR #2 ARS → `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- PR #3 ARB → `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- PR #4 ADR set → `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- PR #5 System Architecture → `5a0761dec9dbbca538be787839d93017f5c501df`.
- PR #6 LEL → `a7d031317cf25934218cd09a4916449f2bf5b634`.
- PR #7 Requirements → `e34e2a2ae3f709d83c24d528f8930b1b72060961`.
- PR #8 IMP + IA activation → `0d58eb2921df298114c304295a061547598ae541`.
- PR #9 S1 → `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`.
- PR #10 S2 → `c5f60dbf11b04b680c6f51f2e610d33906b08637`.
- PR #11 S3 → `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`.
- PR #12 S4 approved head `c0c925a8a5f8b52ad2eac6cb307f7304959f4229` → merge `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`.

## Closure rule
No runtime row becomes Closed without fresh verification evidence and controlled merge on the exact approved head.
