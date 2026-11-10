# SMCEP T4 — Retrospective Methodology Reconstruction

> **Retrospective reconstruction based on available experimental records; not an original preregistered protocol.**

**Document class:** Post-experiment methodology reconstruction from surviving artifacts, without altering any historical result.  
**Primary source:** `SMCEP_T4_Research_Archive.zip` (53 ZIP entries: 40 `drive_t4` source files, 10 `vm_evaluations` result records, one inherited T3 procedure, a manifest, and a README).  
**Original protocol:** Not recovered. Its expected SHA-256 is `55085ac00e20fd21f103dad8ecba2a5d81bb21938236f8045b6f4d35cf25bd5a`.  
**Original methodology addendum:** Not recovered. Its expected SHA-256 is `ab8d109be6f29a820816d667ffeb3c8cd217caeaa8ef9bcf05ae7d6aabfc2d28`.  
**Important:** Those hashes are references preserved in the archive manifest; they are **not** the hashes of the present reconstruction.

## 1. Research objective, questions, and comparison

T4 was an exploratory real-LLM feasibility comparison of a **Frozen** reference procedure with an **Evolving** procedure receiving revision/selection opportunities across three cycles. The intended question was whether procedural revision improved task performance and transfer on subsequent, withheld tasks, beyond what a frozen procedure achieved. The study is not an independently preregistered, causally identified measure of future recursive improvement capacity. The generated-answer records name `Qwen/Qwen2.5-Coder-1.5B-Instruct`, with a maximum output allowance of 384 new tokens in the cycle-1 locked-audit output. Claims about all invocations having exactly identical service/library versions or budgets are **not verified from available records**.

## 2. Reconstructed task schedule and test partitions

The archival `drive_t4/t4_task_manifest_v1.json` enumerates three sequential cycles, each with development, selection, and locked-audit partitions. Each task has five defined tests; the audit test cases and expected answers were intended to be hidden from procedure-revision and candidate-selection prompts. The candidate was to be selected before locked audit. These are **recorded protocol-policy statements**, not independent proof of information-sequestering in every actual prompt.

| Cycle | Development tasks | Selection task | Locked-audit tasks |
|---|---|---|---|
| 1 | `clamp_values`, `run_lengths` | `rotate_right` | `unique_pairs`, `balanced_brackets` |
| 2 | `normalize_path`, `prefix_sums` | `intervals_overlap` | `count_islands`, `zigzag_rows` |
| 3 | `decimal_to_binary`, `chunk_list` | `common_prefix` | `top_k_frequencies`, `parse_ranges` |

Per cycle, this specifies 2 development tasks × 5 cases × 2 conditions = 20 arm-specific tests; one selection task × 5 cases × 2 candidates = 10 evaluations; and two audit tasks × 5 cases × 2 conditions = 20 tests. Across the three cycles, the audit partitions contain **30 defined cases per arm (60 total)**. A cycle-1 budget-control partition is separately documented and is marked as a **post-hoc exploratory control**, not part of a preregistered primary estimate. Sources: `drive_t4/t4_task_manifest_v1.json`, all `drive_t4/t4_cycle_*_test_package_v1.json`, and archive `README.txt`.

## 3. Model outputs, procedural adaptation, and candidate choice

Each cycle has archived model responses, `revision_candidate`, selection candidates, a recorded selection decision, and a locked-audit output file. The saved decision objects document the following choices; this should **not** be simplified to a claim that the baseline was retained in every cycle:

| Cycle | Recorded selection scores (baseline / revised) | Chosen candidate | Record interpretation |
|---|---|---|---|
| 1 | 5 / 5 | `baseline` | Accuracy, then fewer total tokens, then baseline. |
| 2 | 0 / 0 | `revised` | TIE_ON_ACCURACY_REVISED_LOWER_TOKEN_COST |
| 3 | 5 / 5 | `baseline` | EXACT_TIE_BASELINE_RETAINED |

Cycle 2 selected the *revised* candidate on lower recorded token cost after a 0/0 accuracy tie; the decision note reports that both generated identical code and failed all five selection tests owing to an unsupported tuple-only input assumption (`ValueError`). Cycle 3 reports identical procedures and generated sources, with the baseline retained on an exact tie. Thus the records do not establish a sustained beneficial procedure lineage, even though a revised label was selected in cycle 2. Source: `drive_t4/t4_cycle_{1,2,3}_selection_decision_v1.json`.

## 4. Evaluation artifacts and evidence-quality qualifications

The T4 archive holds three audit `vm_evaluations` JSON files, one per cycle. Each has 20 itemized entries, including `task_id`, `condition`, `test_index`, and `status`; the cases correspond to the T4 audit task names in the task manifest. These archived *VM evaluation records* are stronger evidence than an unexecuted test-definition file, but the underlying VM runner, original process logs, independent machine attestations, and complete environment image are absent from the ZIP. **Hence they provide recorded evaluation outcomes, not an independently re-executed verification of every sandbox invocation.**

**Metadata inconsistency:** all reviewed `vm_evaluations/t4_cycle_*` JSON files say `phase: T3` and `expected_tests: 60`, even though their task names identify T4 and their `completed_tests` matches the respective local record count (20 for audit/development; 10 for selection/budget control). Consequently, do **not** treat `expected_tests: 60` as 60 completed tests *per file* or reclassify these records as T3 evaluations. The mismatch needs to be retained as a data-quality caveat. The T4 `drive_t4/t4_cycle_*_audit_test_package_v1.json` files separately say `execution_status: NOT_EXECUTED`; that status indicates the **test-package object itself** was not later updated. It does not erase the existence of the separate evaluation ledger, but neither does that ledger automatically verify sandbox provenance.

## 5. Recorded locked-audit outcomes

The following table is calculated **directly from individual `status` fields** in the three retrieved `vm_evaluations/t4_cycle_*_audit_evaluation_v1.json` files. These are status tallies, not new test executions.

| Cycle | Arm | PASS | FAIL | ERROR | SYNTAX_ERROR | Recorded items |
|---|---|---:|---:|---:|---:|---:|
| 1 | Frozen | 2 | 3 | 0 | 5 | 10 |
| 1 | Evolving | 10 | 0 | 0 | 0 | 10 |
| 2 | Frozen | 10 | 0 | 0 | 0 | 10 |
| 2 | Evolving | 6 | 3 | 1 | 0 | 10 |
| 3 | Frozen | 10 | 0 | 0 | 0 | 10 |
| 3 | Evolving | 7 | 0 | 3 | 0 | 10 |

**Overall:** Frozen **22/30 PASS (73.3%)** and Evolving **23/30 PASS (76.7%)** across the archived audit status records (one additional pass for Evolving). This modest observed difference is not evidence of a transferable, statistically established increase in future improvement capacity. The comparison is exploratory and no seed-level inferential design or uncertainty estimate is recovered here. The source ledgers retain the failure classes, so syntax errors and runtime errors are not silently reclassified as incorrect output.

### Test-by-test result index (as preserved in archive)

Each cell below lists results for test indices 1–5. `P` = PASS, `F` = FAIL, `E` = ERROR, `S` = SYNTAX_ERROR. The cells are **transcriptions of archived statuses**, not new execution results.

| Cycle | Locked task | Frozen tests 1–5 | Evolving tests 1–5 |
|---|---|---|---|
| 1 | `unique_pairs` | F F P F P | P P P P P |
| 1 | `balanced_brackets` | S S S S S | P P P P P |
| 2 | `count_islands` | P P P P P | P P E P P |
| 2 | `zigzag_rows` | P P P P P | F F P P F |
| 3 | `top_k_frequencies` | P P P P P | P P P P P |
| 3 | `parse_ranges` | P P P P P | E E P P E |

## 6. Sandbox isolation, resource restrictions, and execution ordering

The experiment workflow and research handover describe using Google Cloud Compute Engine VM `smcep-audit-vm-01` (zone `us-central1-c`) with isolated execution of model-generated Python rather than execution in the Colab control process. The separate audit records are saved as `vm_evaluations/`. The broader research's VM isolation checks mention Linux sandboxing (`bwrap`), constrained process lifetime and cleanup (`systemd-run`), and resource limits. **Not verified from available T4 archive:** exact T4 runner code, binary/package versions, per-invocation isolation flags, CPU quota, memory limit, process cap, environment digest, or contemporaneous per-test sandbox command lines. Do not transpose later timeout-control measurements onto T4 without a matching artifact.

The reconstructed ordering is: allocate and freeze task partitions → generate development solutions → evaluate / provide permitted feedback → create or compare revision candidate → select on a separate selection set → evaluate on locked-audit set → archive decisions, outputs, and result ledger. The recorded selection decisions include `decision_frozen_before_audit: true` and `locked_audit_accessed: false`; they are declarative provenance fields. Full causal proof of the ordering from immutable timestamps or signed VM logs is **not verified from available records**.

## 7. Original dates, integrity, and locations

The ZIP `README.txt` gives archive date **2026-11-10** and explicitly states that the original T4 protocol and methodology addendum were not found. This is an **archive packaging date**, not evidence of every experiment's actual execution time. Google Drive creation/modified timestamps, if present, should not be substituted for actual VM invocation timestamps. Original experimental run timestamps: **Not verified from available records**.

Archive: [SMCEP_T4_Research_Archive.zip](https://drive.google.com/file/d/1fHy6_G49f8I8vox5idnyQH27hDmJo5lZ/view); Google Drive path: `MyDrive/SMCEP_Real_LLM/SMCEP_T4_Research_Archive.zip`. ZIP SHA-256 recalculated locally: `305c13dfa2a3f3d874ddb569b7c072b23a09b30bbb45459bb878994e95f4df52`.

The archive manifest enumerates **51 research-source entries** and each of those 51 member hashes was independently recalculated against the bytes of the opened ZIP in this review (**51/51 matched**). A successful internal manifest check establishes correspondence of archived contents to their included manifest; it is not an independent timestamp attestation or a replacement for the missing protocol.

Selected provenance references:

| Archive member | SHA-256 (from ZIP bytes, recalculated) |
|---|---|
| `drive_t4/t4_task_manifest_v1.json` | `b9b104917edd6aaf35fad64e086f6181b2a9eb86712bb8c4ecd5a8ecaa90f9a4` |
| `drive_t4/t4_task_packages_index_v1.json` | `086d42ac93dd06f549eae6f58c9d0abeca4ec5c4593730b0400d2ad76c19cc85` |
| `drive_t4/t4_cycle_1_selection_decision_v1.json` | `7395b915868af7b7eeac645a875b7997a88914860c2081144374b9a1b5da5687` |
| `drive_t4/t4_cycle_2_selection_decision_v1.json` | `5cb32d167ee3c4e11ea191ca6c44731e9ed753dc2cd2b5e1c43a4add52f791fe` |
| `drive_t4/t4_cycle_3_selection_decision_v1.json` | `e4413dfd0d2ec5fcc4bcc4f7a93578e65caf4845e2590e302dbe7d6634308acc` |
| `vm_evaluations/t4_cycle_1_audit_evaluation_v1.json` | `585ee8abc07e14652fa0c4d5536e9f9f6da6569085e2115370660ff997d2c31e` |
| `vm_evaluations/t4_cycle_2_audit_evaluation_v1.json` | `0dd76859d943b00461211932c0cfa4625c3335fac8b2112e35fcd2bb17f802fd` |
| `vm_evaluations/t4_cycle_3_audit_evaluation_v1.json` | `9d2aca00c6b1db232db1f9460c14cd2a9f8bad61af88e4599f3f4dfafd91853d` |

All other T4 file-level SHA-256 values are recorded in `SHA256_MANIFEST.json`. The complete ZIP also contains `reference/t3_frozen_procedure_001.json`, documenting the inherited procedural reference.

## 8. Limitations and manuscript-level interpretation

- **Preregistration:** Original protocol and methodology addendum absent; the SHA-256 identifiers alone do not establish when the absent files were created. This reconstruction is **not** the original frozen protocol.
- **Execution provenance:** T4 has itemized VM-labeled status records but not the complete executable sandbox runner/environment or independent per-test host logs. Inconsistent `phase` and `expected_tests` metadata require disclosure.
- **Audit package state:** `NOT_EXECUTED` pertains to test-definition package metadata, not a definitive statement about separately logged execution.
- **Causal inference:** Three cycles with task-set and selection dependencies do not identify the general causal impact of procedure modification. Cycle 2 chose a revised candidate solely on token cost with no selection-test accuracy advantage. 
- **Measurement:** Accuracy on audit coding tasks is an observed task-performance proxy. This does not measure the fixed-reference, independently audited future-development capacity `C` proposed for confirmatory SMCEP tests.
- **Scope:** Real LLM production in T4 must not be conflated with T7's 50-generation semi-synthetic simulation or with T6's three-arm procedure-archive pilot.

## 9. Consistency with published T0–T7 findings

The recalculated T4 archive counts reproduce the previously reported **22/30 Frozen** and **23/30 Evolving** locked-audit PASS figures. **No contradiction** was found for these headline counts. However, any existing manuscript sentence claiming that *no revised candidate was selected in any T4 cycle* should be corrected: the cycle-2 decision file selects `revised`, despite a 0–0 accuracy tie, lower tokens, and no demonstrated lasting gain. The internal `phase: T3` field in T4 evaluation JSON is a provenance inconsistency and must not be repeated as a scientific assertion. Nothing in these records establishes persistent collective RSI.

## Verified Evidence

- Three cycles, task partition inventory, 51 manifest-verified archived research artifacts, recorded selection decisions, and 60 individually enumerated T4 audit outcome statuses.
- Audit outcome tallies: 22/30 PASS Frozen and 23/30 PASS Evolving; exact failure classes preserved.
- Cycle-2 revised candidate was selected on recorded lower token cost despite tied zero selection accuracy.

## Retrospective Reconstruction

- Development → candidate selection → locked audit is reconstructed from file names, task manifest, saved decisions, and test/result objects; sandbox control-process details are partially supported by other project records and remain incompletely attributable to T4.

## Unresolved Evidence

- The two historical original documents and their expected content hashes; independent confirmation of preregistration, per-invocation VM run logs, full runner/environment provenance, exact resource limits for T4, comprehensive original timestamps, and a causal future-development-capacity estimate: **Not verified from available records**.