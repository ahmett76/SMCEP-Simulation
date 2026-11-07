# SMCEP synthetic pilot archive (v0.6–v1.0)

This directory contains the original synthetic exploratory pilot source code, per-version README files, logs, summaries, and trajectories. These are **not** real-LLM self-modification experiments. Metric definitions and implementations vary across versions; do not pool their results as independent replications.

- `smcep_v06/` — initial performance/capacity probe.
- `smcep_v07/` — scope and policy ablations.
- `smcep_v08/` — fixed-reference anchor probe.
- `smcep_v09/` — ID/OOD fixed-reference probes.
- `smcep_v10/` — paired frozen/evolving policy experiment.

For v1.0, from this repository's root directory, run:

```bash
python simulations/smcep_v10/smcep_v10.py --seeds 12 --generations 25 --candidates 6 --probes 12 --out simulations/smcep_v10
```

The v1.0 script imports `smcep_v09.py` from the sibling `smcep_v09/` directory. Install `numpy` before running. Consult the per-version README files for additional details. The scripts have been packaged and checked for duplicate files, but have **not** been rerun as part of this packaging step.
