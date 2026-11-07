# SMCEP v0.8 — Anchored synthetic meta-capacity pilot

## Run

```bash
python smcep_v08.py --seeds 12 --generations 25 --candidates 6 --probes 16 --out ./results
```

Requires Python 3 and numpy. Outputs `trajectories.csv` and `summary.json`.

## What changed from v0.7

- `C_anchor`: every agent's proposal policy is tested on the same fixed reference configuration, rather than its own current (potentially optimized) configuration. This reduces changing-headroom confounding.
- Policy candidates can be selected using separate *development* tasks; anchored *evaluation* tasks are not visible to selection.
- All groups retain shared seeds, task families and development budgets. C/D differ only in selection noise.
- B and E_scope cannot modify the policy, so `C_anchor` is fixed by design. This is a control, not empirical proof of model validity.

## Crucial limitations

1. `C_anchor` is the best-of-k opportunity on synthetic tasks. It is **not** independent real-world research capability or demonstrated recursive self-improvement.
2. The synthetic proposal mechanism and utility function are designed by the researchers. The model cannot establish universal necessary/sufficient conditions for RSI.
3. `F_anchor` is a local paired contrast with the unchanged branch, not a demonstration of sustained causal recursion.
4. A/B/C comparisons conflate scope and policy permissions; E_scope and E_policy are exploratory controls.
5. The reported means are descriptive, from 12 seeds, without confirmatory statistical inference or preregistration.
6. The `false_accept` flag compares noisy selection utility to synthetic true selection utility, not to independent held-out performance.
7. `C_anchor` is measured with the same reference task family across generations, but separate from development tasks; differences can reflect distribution shift or policy overfitting.

## Files

- `smcep_v08.py`: reproducible source code
- `trajectories.csv`: all seed/group/generation measurements
- `summary.json`: summary statistics, paired descriptive comparisons and limitations
- `run_log.txt`: execution output
