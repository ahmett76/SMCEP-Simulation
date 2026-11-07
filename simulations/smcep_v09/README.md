# SMCEP v0.9 — exploratory synthetic generalization pilot

Run: `python smcep_v09.py --seeds 12 --generations 25 --candidates 6 --probes 12 --out ./results`

## Design
Six groups: A static; B restricted changes/no policy edits; C broad changes/policy edits/low selection noise; D same as C/high selection noise; E_scope broad changes/no policy edits; E_policy restricted changes/policy edits. Same initial agent and matched random seeds.

The synthetic agent contains four task parameters and two proposal-policy parameters. Each generation proposes six changes, selects by a noisy evaluation of task gain plus visible policy-probe gain, and applies a positive-scoring candidate. No monotonic improvement is hard-coded.

P: independent task score on a fixed holdout. C_id and C_ood: proposal-policy skill on a fixed reference agent; for each probe, policy-generated candidates are ranked on a development split, and the selected candidate's net gain is evaluated on a disjoint audit split. ID tasks use target range [-1,1] and ruggedness frequency 5.1; OOD tasks shift targets to [-1.65,.35] and frequency to 7.7. Both probes are independent of main-trajectory selection and never update the main agent.

F_id and F_ood: accepted candidate minus unchanged baseline on the same fixed-reference probes. This is a one-step matched branch contrast, not evidence of persistent multi-generation recursion.

## Caveats
This is a synthetic, researcher-designed task family, not real autonomous AI research. A/B/C comparisons confound change scope and policy access; E_scope and E_policy are exploratory controls. C is a particular anchored search-policy score, not a universal measure of development capability. C's negative values may reflect policy overfitting, selection noise, or the synthetic task landscape. Descriptive 95% normal-approximation intervals are unadjusted for multiple comparisons and 12 seeds are insufficient for strong confirmatory claims. Reward tampering is not simulated; only noisy evaluation is. The pilot is not preregistered.

Files: `smcep_v09.py`, `trajectories.csv`, `summary.json`, `run_log.txt`.
