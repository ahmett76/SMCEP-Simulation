# SMCEP T0–T7 — audited local GitHub release candidate (2026-11-11)

**Status: NOT PUBLISHED.** This candidate contains the full SMCEP 17 manuscript with T0–T7 integration, 24 original T0–T3 JSON files, four preserved T4–T7 source ZIP archives, and audit/traceability notes. It has **not** been uploaded to GitHub. The manuscript is a preprint working version, not an independently replicated confirmation of recursive self-improvement.

## Layout
- `manuscript/`: `SMCEP17_T0_T7_figure_evidence_revision_2026-11-11.tex` (current figure-integrated manuscript; prior version retained)
- `real_llm/T0-T3/`: 24 source JSON records; v1/v2 normalized T3 files are distinct
- `archives/`: original T4, T5, T6, T7 ZIP archives, preserved byte-for-byte
- `audit/`: provenance, verification, and publication-gate reports
- `SHA256SUMS.txt`: hashes of all package files except this manifest

## Interpretation constraints
- T2: behavioral results 8/9 in each arm, without validated future-development-capacity gain.
- T3: 12 normalized outputs pass **static syntax parsing**. The behavioral package specifies 60 **planned** cases; no independently documented T3 VM per-test execution was located in the reviewed records. Do not report a T3 functional pass rate.
- T4–T5: six VM audit evaluations record 120 completed test statuses and 94 PASS. Per-evaluation metadata says 60 expected vs 20 completed; 360 expected slots must not be presented as completed. T5 cycle-2 API delivery failures are operational, not proven algorithmic failures.
- T6: archived counts include 527 events, 186 candidates, 164 evaluations, 54 measurements. Missing capacity values are NULL, not measured zero gains.
- T7: 84/84 real-model calibration outcomes have a ceiling effect. The subsequent 100-repetition, 50-generation experiment is a **stochastic simulation**, not a real-model recursive run.
- Two historical T4 methodology documents remain unavailable for hash verification; no preregistration assertion follows from the present archive.

## Release checks still required
1. Independently review all source archives for secrets, credentials, personal information, and redistribution rights.
2. Verify the actual high-resolution figures required by the manuscript: `SMCEP_Figure_2_clean.png`, `SMCEP_Figure_3_clean.png`, and optional `smcep_historical_trajectory.png`. **Do not publish the 20×20 pixel compilation placeholders** found in local compilation-test folders.
3. Compile the complete manuscript with the authentic figures and review rendered pages and references.
4. Verify external T3 VM execution provenance if it exists; otherwise preserve the explicit uncertainty in the manuscript.
5. Review and approve publication, then record a Git commit/tag and archive DOI as applicable.

All original research archives are retained without modification. No new model experiments were run while assembling this candidate.

## Added descriptive comparison figure (2026-11-11)
- `figures/SMCEP_Synthetic_vs_RealLLM_evidence_2026-11-11.png` and `.pdf`: original two-panel graphic from existing archived figures, without new experiments.
- Panel A reports synthetic v1.0 changes in task performance and ID/OOD development probes; panel B reports T4/T5 VM PASS fractions from recorded statuses. **Different scales, different estimands, different units: do not infer a cross-study effect size or verified C improvement.**
- The updated LaTeX manuscript references the PNG; copy it into the LaTeX compilation directory or configure TEXINPUTS. Existing manuscript PNGs are not bundled or replaced.
- `audit/SMCEP_Release_Static_Scan_2026-11-11.md` records a limited automated disclosure scan, not a legal license clearance or guarantee of absence of secrets.
