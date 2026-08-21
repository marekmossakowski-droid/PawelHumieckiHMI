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
| HC-ARS-REP-001 | Multi-audience reporting | ARS → ADR → SA → REQ → IMP | Baselined |
| HC-ADR-001 | HMI and edge/data responsibilities separated | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-002 | KVK strategy is observation-only | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-003 | Immutable internal animal identity | ADR → SA → LEL → REQ | Baselined |
| HC-ADR-004 | Media are provenance-linked evidence objects | ADR → SA → LEL → REQ | Baselined |
| HC-ADR-005 | Persistence is local-first with recovery | ADR → SA → REQ → S2 | Baselined |
| HC-ADR-006 | Veterinary nomenclature controlled/versioned; human authority final | ADR → SA → LEL → REQ | Baselined |
| HC-ADR-007 | Reports derive from canonical records | ADR → SA → REQ → IMP | Baselined |
| HC-SA-001 | Edge/application layer owns canonical lifecycle | SA → LEL → REQ → S1/S3 | Baselined |
| HC-SA-002 | Durable store is independent of HMI replacement | SA → REQ → S2 | Baselined |
| HC-SA-003 | KVK observation adapter has no write/actuation route | SA → LEL → REQ → IMP | Baselined |
| HC-SA-006 | HoofCare failure cannot affect KVK safety | SA → REQ → IMP | Baselined |
| HC-LEL-001 | Explicit session states and terminal semantics | LEL → REQ → S1 | Baselined |
| HC-LEL-002 | Ambiguous identity fails closed | LEL → REQ → S1/S3 | Baselined |
| HC-LEL-004 | KVK events are observation-only | LEL → REQ → IMP | Baselined |
| HC-LEL-005 | Durable/idempotent canonical transitions | LEL → REQ → S1/S2/S3 | Baselined |
| HC-REQ-HMI-001 | Structured HMI workflow has no KVK actuation affordance | REQ → IMP → S3/S4 | Baselined |
| HC-REQ-ID-001 | Identity ambiguity fails closed | REQ → S1/S3 | Baselined |
| HC-REQ-DATA-001 | Durable local store/audit/synthetic bench boundary | REQ → S2 | Baselined |
| HC-REQ-KVK-001 | KVK remains observation-only; physical integration blocked pending audit | REQ → IMP | Baselined |
| HC-REQ-MVP-001 | Bench MVP requires acceptance and negative tests | REQ → S1-S7 | Baselined |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | Approved / Baselined PR #8 |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | ACTIVE — PR #8 |

## Runtime slice lineage

| ID | Evidence / invariant | Artifact | Status |
|---|---|---|---|
| HC-S1-RED-001 | Tests fail before domain implementation | tests/test_session_core.py | Verified RED @ `52b4fca3ca719b035d2cc7c5091447c607b6fd83` |
| HC-S1-CORE-001 | Session lifecycle and identity core | src/hoofcare/domain/session.py | MERGED / VERIFIED PR #9 |
| HC-S1-FAILCLOSED-001 | Ambiguous identity cannot bind animal history | domain + tests | MERGED / VERIFIED PR #9 |
| HC-S1-IDEMP-001 | Duplicate event IDs are idempotent | domain + tests | MERGED / VERIFIED PR #9 |
| HC-S1-TERM-001 | Completion guard and terminal states | domain + tests | MERGED / VERIFIED PR #9 |
| HC-S2-RED-001 | Persistence tests fail before store exists | tests/test_persistence.py | Verified RED @ `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` |
| HC-S2-STORE-001 | Snapshot persistence outside HMI | src/hoofcare/persistence/local_store.py | MERGED / VERIFIED PR #10 |
| HC-S2-RECOVERY-001 | Restart recovery | persistence + tests | MERGED / VERIFIED PR #10 |
| HC-S2-ATOMIC-001 | Atomic local snapshot replacement | persistence + tests | MERGED / VERIFIED PR #10 |
| HC-S2-AUDIT-001 | Append-only ordered amendments | persistence + tests | MERGED / VERIFIED PR #10 |
| HC-S2-FAILCLOSED-001 | Corrupt snapshot fails closed | persistence + tests | MERGED / VERIFIED PR #10 |
| HC-S3-RED-001 | HMI-edge contract tests fail before contract exists | tests/test_hmi_edge_contract.py | Verified RED @ `882afd05b9cbb94bc3265652becc245992998271` |
| HC-S3-CONTRACT-001 | Local in-process result/error contract | src/hoofcare/application/contract.py | Implemented / GREEN |
| HC-S3-IDEMP-001 | Repeated request_id returns idempotent result | contract + tests | Implemented / GREEN |
| HC-S3-FAILCLOSED-001 | Ambiguous/invalid identity stays explicit and fail-closed | contract + domain + tests | Implemented / GREEN |
| HC-S3-NOACT-001 | No KVK actuation/command surface is exposed | contract + tests | Implemented / GREEN |

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
- PR #10 S2 approved head `fca836ca9b4f99ea059b5f79f0dd8eef402e3ecb` → merge `c5f60dbf11b04b680c6f51f2e610d33906b08637`.

## Closure rule
No runtime row becomes Closed without fresh verification evidence and controlled merge on the exact approved head.
