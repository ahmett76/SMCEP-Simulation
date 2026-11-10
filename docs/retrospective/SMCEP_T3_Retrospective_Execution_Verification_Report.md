# SMCEP T3 — Retrospective Execution and Verification Report

**Document class:** Retrospective technical evidence report; prepared after the experiment. **Not** an original run log, preregistration, or a new experimental result.  
**Evidence reviewed:** T3 JSON artifacts available from the connected Google Drive, archive reports, and the locally inspected T4 ZIP. No cloud VM session was opened and no generated candidate code was executed during preparation of this report.  
**Status:** Static production evidence verified; original T3 sandbox-execution outcome **not verified from available records**.

## 1. Objective and design

The recorded T3 objective was to test whether feedback-derived revision of a development procedure improved later error correction and transfer. The design specified: (i) verified prior error feedback, (ii) a persistent procedure-revision proposal, and (iii) blind transfer on previously unseen tasks. The comparison was between **Frozen** (reference procedure) and **Evolving** (revised procedure) under nominally shared model weights, feedback access, generation constraints, and evaluation tasks. These were stated design controls, not independently verified equality of all costs. The declared primary endpoint was held-out correctness; secondary endpoints included error-correction behavior and token/time costs. The protocol explicitly records `capacity_C_measured: false`. Sources: [t3_protocol_v1.json](https://drive.google.com/file/d/1yqrCq3WGXhDn1zOUd82Z0IaqG6SyDFvX/view), [t3_blind_design_v1.json](https://drive.google.com/file/d/12yIKnmPD6nHIcPxuZESYpR1MRKhfHeYF/view), [t3_test_generation_protocol_v1.json](https://drive.google.com/file/d/1gUr16fmDxel_x0LYWmchjmoy2tJvrOf4/view).
## 2. Model, tasks, and production environment

The raw model-output file identifies `Qwen/Qwen2.5-Coder-1.5B-Instruct`, deterministic generation (`do_sample: false`), and `max_new_tokens: 512`. It contains **12 generations**: six tasks in each of two conditions. The normalized output file preserves a corresponding 12-record set with per-output input/output token counts and elapsed generation seconds; these are recorded metadata, not independently reproduced measurements. Sources: [t3_model_outputs_v1.json](https://drive.google.com/file/d/1lxGutZ86XgvUP4vyv4QcQ-jCEqMB5gDp/view), [t3_normalized_outputs_v2.json](https://drive.google.com/file/d/1ywRDuc-8r7W7ZCQ_JJiYFWEarcluucXa/view).

The six task/function pairs identified in the generated test package are:

| Task ID | Function | Defined cases per condition |
|---|---|---:|
| `T3_001` | `stable_unique` | 5 |
| `T3_002` | `transpose_rows` | 5 |
| `T3_003` | `longest_zero_run` | 5 |
| `T3_004` | `count_words` | 5 |
| `T3_005` | `edges_to_adjacency` | 5 |
| `T3_006` | `merge_sorted_unique` | 5 |

The package contains **30 defined tests per arm; 60 arm-specific test cases in total**. Its `execution_policy` is `isolated_vm_only`. This is a restriction on intended execution, not evidence that execution took place. Source: [t3_behavioral_test_package_v1.json](https://drive.google.com/file/d/1AE6CSIcJ3TIJBtHi-DrWM5QFtKd4ZfrJ/view).
## 3. Procedure revision and feedback

The procedure-audit artifact reports that a five-step revision was present but the revision was **task-specific contaminated** (`task_specific_contamination: true`), with references to grouped shortest-path, Dijkstra, `heapq`, and graph-edge representation; it records `feedback_integration: partial`, `generalization_success: false`, `behavioral_transfer_tested: false`, and `capacity_C_measured: false`. These fields are an archived audit assessment, not a validated causal estimate of future improvement capacity. Source: [t3_procedure_audit_001.json](https://drive.google.com/file/d/1NIeYiXjrPBxRWCok_ZmQp3U3z6-MadBY/view).
## 4. Static validation: raw versus normalized sources

The original static evaluation records **12/12 raw outputs as syntactically invalid** because the returned messages included Markdown fencing or additional text. This is distinct from checking the extracted code. The version-2 normalized artifact contains 12 sources flagged as syntactically valid with expected functions present. During this retrospective review, the 12 sources in the saved test-package file were parsed using Python `ast.parse` **without execution**; all 12 parsed successfully. This is a fresh *static-only* check and is not an additional benchmark trial. Sources: [t3_static_evaluation_v1.json](https://drive.google.com/file/d/1bkW9xQOw8u7WhazE1OjQt6zJHVUCErlL/view), [t3_normalized_outputs_v2.json](https://drive.google.com/file/d/1ywRDuc-8r7W7ZCQ_JJiYFWEarcluucXa/view), [t3_behavioral_test_package_v1.json](https://drive.google.com/file/d/1AE6CSIcJ3TIJBtHi-DrWM5QFtKd4ZfrJ/view).

**Contract compliance remains separate.** The prior publication-preparation review identified a potential contract violation in the Evolving `count_words` implementation (punctuation handling). This is a source-level concern; no PASS/FAIL test outcome is inferred from it here. Likewise, extraction of fenced code is a post-production normalization step and must be reported rather than equated to raw instruction compliance.

## 5. Execution verification, outcome availability, and evidence matrix

| Evidence claim | Status | Supporting source / reason |
|---|---|---|
| 12 generated model responses | **Verified in retrieved files** | `t3_model_outputs_v1.json` |
| Six task definitions and 60 specified arm-specific cases | **Verified in retrieved files** | `t3_behavioral_test_package_v1.json` |
| 12 normalized code bodies parse as Python | **Verified by static inspection** | Parsed locally; **not executed** |
| All 60 defined cases ran in a VM | **Not verified from available records** | Test package lists cases but provides no corresponding per-case VM result ledger |
| Frozen PASS count on T3 held-out tests | **Not verified from available records** | No T3 per-case execution ledger examined |
| Evolving PASS count on T3 held-out tests | **Not verified from available records** | Same limitation |
| Persistent procedure caused superior future development capacity | **Not demonstrated** | Capacity `C` unmeasured; no longitudinal intervention |

The Cloud VM was not accessible for this report because the earlier attempt to list the presumed Compute Engine project returned a missing-billing-account message. This was an access/configuration limitation, **not evidence of non-execution**. The available T4 ZIP includes 10 `vm_evaluations/t4_cycle_*` files, but these describe **T4 task names**, notwithstanding a conflicting internal `phase: T3` field. They must **not** be relabeled as T3 held-out results. Source: `SMCEP_T4_Research_Archive.zip` (T4 archive).
## 6. Provenance and file checksums

The following SHA-256 values were recalculated from the locally retrieved file bytes for this report. They identify the retrieved copies, not an independent timestamped preregistration.

| Artifact | SHA-256 |
|---|---|
| [t3_model_outputs_v1.json](https://drive.google.com/file/d/1lxGutZ86XgvUP4vyv4QcQ-jCEqMB5gDp/view) | `5f93d8214872dfaf821d020b4d2fda1ab9b2f4c9e41aa1c65fcd2501695ce112` |
| [t3_normalized_outputs_v2.json](https://drive.google.com/file/d/1ywRDuc-8r7W7ZCQ_JJiYFWEarcluucXa/view) | `2f7d53118310f4a2961dbe06ea2675ac1b7c6686b30084d38afb378948efe6c9` |
| [t3_static_evaluation_v1.json](https://drive.google.com/file/d/1bkW9xQOw8u7WhazE1OjQt6zJHVUCErlL/view) | `732560d5142ebbe2e8a3ac56dc048614e0babf972a5dfe048bbbde85309a18fc` |
| [t3_behavioral_test_package_v1.json](https://drive.google.com/file/d/1AE6CSIcJ3TIJBtHi-DrWM5QFtKd4ZfrJ/view) | `9db78f96274c1f051864b161363540dcb183d377f0021abb1f9224b7909609eb` |
| [t3_protocol_v1.json](https://drive.google.com/file/d/1yqrCq3WGXhDn1zOUd82Z0IaqG6SyDFvX/view) | `c59fe01e589aacdde11f887dcd567a349351413d30368649d50a11f3350b4b64` |
| [t3_blind_design_v1.json](https://drive.google.com/file/d/12yIKnmPD6nHIcPxuZESYpR1MRKhfHeYF/view) | `2c2f4305936831c715ad321f7d129aea8b84d808a4a8c86cb3a4ba10d5907a41` |
| [t3_test_generation_protocol_v1.json](https://drive.google.com/file/d/1gUr16fmDxel_x0LYWmchjmoy2tJvrOf4/view) | `67d0493cf9cf8d55bcc136d817d5ad17601298e888024015040250f03b8217f3` |
| [t3_procedure_audit_001.json](https://drive.google.com/file/d/1NIeYiXjrPBxRWCok_ZmQp3U3z6-MadBY/view) | `2eed1aa719df6a80e5fb8411ee3383667664e816106750d9d17fe2df90180ad1` |

The stored T3 protocol refers to earlier pilot pass counts (T1: 5/5 in each condition; T2: 8/8 in each condition). Those are **reported prior-evidence fields**, not results independently reaudited in the present T3 review.

## 7. Interpretation and scientific limitations

T3 established an inspectable **code-generation and static-validation** record under a frozen-versus-revised procedural comparison. The retrieved evidence does **not** establish held-out VM test-pass percentages. A syntactically valid function may still violate input/output contracts; contamination in the proposed procedure further weakens general transfer claims. The declared controls cannot substitute for a verified runner, a per-case execution ledger, time-stamped sandbox invocation logs, and fixed computational-budget accounting.

## 8. Consistency with the published T0–T7 research narrative

**No new contradictory empirical outcome is asserted.** In particular, this report does not convert 12/12 normalized syntax validity into 60/60 behavioral correctness, does not attribute T4 sandbox results to T3, and does not claim measured collective recursive self-improvement. Any manuscript sentence reporting a definitive T3 held-out PASS rate should be checked against a genuine T3 execution ledger or qualified as **not verified from available records**.

## Verified Evidence

- Six T3 tasks, two procedural conditions, 12 model outputs, 60 defined test cases, recorded static checks, and the archived procedure-audit assessment.
- All 12 test-package source bodies parsed by `ast.parse` during this review without execution.

## Retrospective Reconstruction

- The intended sequence was prior feedback → procedure proposal → blind task generation → matched production → isolated VM evaluation. The sequence is inferred from protocol and artifact structure; completion of the last step is not verified.

## Unresolved Evidence

- Original T3 VM command history, runner version, sandbox configuration, per-case results and PASS/FAIL totals, independent run timestamps, and a verified longitudinal `C` endpoint: **Not verified from available records**.