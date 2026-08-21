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
| HC-REQ-MVP-001 | Bench MVP requires end-to-end acceptance and negative tests | REQ → IMP → S1-S7 | Baselined |
| HC-REQ-MVP-002 | Ambiguous/conflicting identity cannot commit to animal history | REQ → S1/S3/S7 | Baselined |
| HC-REQ-MVP-003 | Persisted in-progress session recovery is required | REQ → S2/S7 | Baselined |
| HC-REQ-MVP-004 | Duplicate events must not duplicate logical records | REQ → S1/S3/S7 | Baselined |
| HC-REQ-MVP-005 | Reference/example media must remain visibly distinguished | REQ → S5/S7 | Baselined |
| HC-REQ-MVP-006 | Bench public interfaces must expose no KVK write/command API | REQ → S3/S4/S6/S7 | Baselined |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | Approved / Baselined PR #8 |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | ACTIVE — PR #8 |

## Runtime slice lineage

| ID | Evidence / invariant | Artifact | Status |
|---|---|---|---|
| HC-S1-RED-001 | Tests fail before domain implementation | tests/test_session_core.py | Verified RED @ `52b4fca3ca719b035d2cc7c5091447c607b6fd83` |
| HC-S1-CORE-001 | Session lifecycle, identity, idempotency and terminal guards | src/hoofcare/domain/session.py | MERGED / VERIFIED PR #9 |
| HC-S2-RED-001 | Persistence tests fail before store exists | tests/test_persistence.py | Verified RED @ `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` |
| HC-S2-STORE-001 | Durable local snapshots, recovery, atomic replace and amendment log | src/hoofcare/persistence/local_store.py | MERGED / VERIFIED PR #10 |
| HC-S3-RED-001 | HMI-edge contract tests fail before contract exists | tests/test_hmi_edge_contract.py | Verified RED @ `882afd05b9cbb94bc3265652becc245992998271` |
| HC-S3-CONTRACT-001 | Local in-process contract, explicit errors/idempotency, no KVK actuation | src/hoofcare/application/contract.py | MERGED / VERIFIED PR #11 |
| HC-S4-RED-001 | HMI workflow tests fail before workflow model exists | tests/test_hmi_workflow.py | Verified RED @ `36608bfcdf02ef4585ee177519d8966ca143dd4b` |
| HC-S4-DASH-001 | Dashboard counters/banner and ordered limb→claw→zone→lesion workflow | src/hoofcare/hmi/workflow.py | MERGED / VERIFIED PR #12 |
| HC-S5-RED-001 | Reporting tests fail before report implementation exists | tests/test_reporting.py | Verified RED @ `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` |
| HC-S5-CANON-001 | Local synthetic PDF from committed canonical report input | src/hoofcare/reporting/report.py | MERGED / VERIFIED PR #13 |
| HC-S6-RED-001 | Simulated adapter tests fail before adapters exist | tests/test_simulated_adapters.py | Verified RED @ `5e62980786207d6caad78dfb82f1921f11d1bfd5` |
| HC-S6-ADAPTER-001 | Deterministic simulated RFID/KVK observations with explicit unavailable/unknown and no actuation surface | src/hoofcare/adapters/simulated.py | MERGED / VERIFIED PR #14 |
| HC-S7-HARNESS-001 | Initial test harness used non-canonical pytest and failed for invalid harness reason | tests/test_bench_mvp_integration.py | Diagnostic only @ `ce9bbb1a2502529014ba7a829484079402282c8d` |
| HC-S7-RED-001 | Corrected canonical unittest acceptance test fails before explicit acceptance summary exists | tests/test_bench_mvp_integration.py | Verified RED @ `5791b86e8bb469d0a4c090880adca2939665ff03` |
| HC-S7-E2E-001 | Synthetic identity→HMI→lesion/treatment→counters→PDF→simulated KVK observation path | src/hoofcare/integration/bench_mvp.py, tests | Implemented / GREEN @ `cc4626182cca558a3939db46f656858c48f3a03a` |
| HC-S7-IDNEG-001 | Ambiguous identity fails closed before treatment history commit | integration harness + tests | Implemented / GREEN |
| HC-S7-MEDIA-001 | Reference media remain explicit `REF:` provenance references | integration harness + report + tests | Implemented / GREEN |
| HC-S7-ACCEPT-001 | Result exposes explicit acceptance summary for end-to-end, synthetic-only, local PDF and no-actuation checks | integration harness + tests | Implemented / GREEN |
| HC-S7-NOACT-001 | Public bench integration surface exposes no KVK command/write/configuration/actuation methods | integration harness + tests | Implemented / GREEN |

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
- PR #12 S4 → `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`.
- PR #13 S5 → `30acc2d9a0833844e7279c68d9884cf9dd124cea`.
- PR #14 S6 approved head `93baa983f7619e6d7464847cc0fa6674d31c0f36` → merge `56da4eaf1316c930ca6095cd068e90bd66e2f624`.

## Closure rule
No runtime row becomes Closed without fresh verification evidence and controlled merge on the exact approved head.
