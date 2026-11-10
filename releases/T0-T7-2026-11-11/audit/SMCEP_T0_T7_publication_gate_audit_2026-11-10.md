# SMCEP T0–T7 — publication gate audit (2026-11-10)

## Scope and method
Inspected the local `SMCEP_GitHub_T0_T7_release_complete_2026-11-10` candidate, the bundled manuscript, T0–T3 JSON records, archive integrity and checksums. The T3 check parses normalized Python source with `ast.parse` and verifies the expected top-level function exists; **it does not execute generated model code** or constitute a functional test. Prior T4–T7 audit findings are cited as archived reports, not independently reproduced here.

## Confirmed
- Candidate contains 34 files, including four preserved T4–T7 ZIPs and 24 T0–T3 JSON records.
- All 33 SHA-256 entries in `SHA256SUMS.txt` match corresponding files; outer ZIP CRC check succeeds.
- The T3 behavioral test package defines six tasks, five tests per task, two arms: 60 **planned** individual test cases.
- Twelve T3 normalized source records (six frozen, six evolving) all parse as Python and contain their expected top-level function. This is a *static* check only.
- T2 failure analysis reports 8/9 behavioral tests passed in each arm, with no measured transfer gain or development capacity C.
- T3 procedure audit records task-specific contamination and `behavioral_transfer_tested=false` at the audit stage.

## Publication blockers / qualifications
1. **T3 execution provenance:** `t3_behavioral_test_package_v1.json` is a package of code and expected outcomes, not a VM execution result. A completed 60/60 or arm-specific behavioral pass rate must not be inferred from the package or static syntax checks. Seek independently recorded isolated-VM execution logs and per-test results before reporting a completed behavioral transfer experiment.
2. **T3 normalization:** The raw output files include markdown fences and explanatory prose; `t3_normalized_outputs_v1.json` and `v2.json` reflect distinct extraction policies. Do not conflate raw instruction compliance, normalized syntax validity, and test success.
3. **T3 task-specific leakage:** The revised procedure references Dijkstra, heapq and shortest-path examples. It is not demonstrated to be a task-general development-policy improvement.
4. **T3 code quality:** Static validity is not correctness. For example, the evolving `count_words` implementation uses a regex that strips punctuation despite the task contract explicitly retaining punctuation; the frozen `transpose_rows` implementation allocates a wrong-shaped output for non-square matrices; both `merge_sorted_unique` implementations can leave duplicate values. These are source-level observations, not measured execution results.
5. **T4–T7 evidence classification:** Maintain separate labels for real-model calibration/limited pilots and T7's 50-generation stochastic mechanism simulation. No real-LLM 50-generation RSI claim is supported.
6. **Manuscript and release:** Bundled manuscript appropriately distinguishes T3 procedure audit and T7 simulation. Final submission still requires explicit per-claim provenance and prepublication disclosure/licensing review. This audit is not a certification of full numerical replication.

## Recommendation
Keep the candidate marked **release candidate, not publication-ready** until T3 VM execution provenance is either located and audited or the manuscript explicitly states T3 functional transfer remains unverified. Retain original archives and versioned normalized outputs. Do not publish a new GitHub release or assert sustained recursive self-improvement on this basis.
