# SMCEP v0.6 — Synthetic Agent Pilot

Pilot run: 12 seeds, 20 generations, 8 candidates per generation, 16 future-development probe tasks, 24 selection/performance tasks.

Files:
- `smcep_simulation.py`: reproducible synthetic experiment
- `trajectories.csv`: generation-level observations
- `summary.json`: aggregated group results and parameters
- `run_log.txt`: terminal output

Run:
```bash
python smcep_simulation.py --generations 20 --seeds 12 --candidates 8 --probes 16 --task-count 24 --out .
```

## Methodological status
This is an **exploratory pilot**, not a preregistered confirmatory study, and not evidence about deployed AGI/ASI.

- The candidate-selection evaluator uses an artificial noisy score; selection noise is not yet calibrated to score dispersion.
- The future-development probe uses an oracle to select the best candidate on synthetic tasks. Thus `C` measures *idealized attainable improvement under a fixed proposal budget*, not independently validated realistic autonomous research capability.
- C and D groups share candidate-generation seeds for matching, but their trajectories diverge as updates accumulate.
- A and B/C differ in multiple dimensions; causal isolation of M vs A requires factorial ablations.
- The current model does not include realistic resource costs, adversarial reward hacking, real program edits, external validators, or formal confidence intervals.
- `F` is a within-generation treated-vs-unchanged difference on matched synthetic probe tasks, not proof of sustained recursive improvement.
- `false_accept_rate_given_accept` measures selection-task true-score decline among accepted candidates, not a universally calibrated false-acceptance rate.
- C baseline remains exactly constant in group A because the same fixed probes and fixed candidate random numbers are used across generations.

Interpretation: inspect model weaknesses and calibrate before confirmatory experimentation.
