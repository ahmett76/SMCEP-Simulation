# SMCEP v0.7 — Synthetic pilot

Run: `python smcep_v07.py --seeds 12 --generations 25 --candidates 6 --probes 24 --out ./results`

Files: `trajectories.csv`, `summary.json`, `run_log.txt`.

This is an exploratory synthetic simulation, **not evidence of real AI recursive self-improvement**.

Six groups: A static; B restricted component edits; C broad component + policy edits; D same as C with higher evaluator noise; E_scope broad component edits only; E_policy restricted component edits with policy edits.

Each seed uses the same starting agent, hidden performance tasks, and matched candidate generation where configurations permit. Selection tasks change by generation. Candidate scores in the selection loop receive noise; hidden performance and development probes do not. `C` is a best-of-k opportunity score measured against the *current* baseline, so it may decline as the agent approaches a local optimum even if search ability does not decline. `F` is the paired difference in this opportunity score between the selected candidate and unchanged state, not a validated estimate of durable causal recursive self-improvement. Probe outputs never feed back into training.

Key limitations:
- The model operates on a toy continuous parameter landscape, not code-writing LLM agents.
- The generator does not learn a complex development strategy; it can mutate step size and a scalar direction bias.
- `C` confounds remaining headroom with search capability; a fixed-reference or cross-agent benchmark is needed.
- Only a small exploratory pilot (12 seeds, 25 generations), no confirmatory statistical inference.
- D varies noise, not adversarial reward hacking.
- There is no independently verified multi-generation transfer mechanism.
- A/B/C comparisons confound edit scope and policy permission; ablations are exploratory, not a full factorial design.
