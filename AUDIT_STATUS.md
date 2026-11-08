# SMCEP reproducibility audit status — 2026-11-08

## Scope and evidence

The repository includes the original source code, archived `trajectories.csv`, and `summary.json` for the five exploratory pilots, plus the historical v0.5 illustration. The accompanying audit discussion reported successful reruns of v0.5 and v0.6–v1.0; for v0.6 and v0.9 it specifically reported byte-identical CSVs and JSON equality after excluding the output-directory parameter. Earlier v0.7, v0.8 and v1.0 reruns were reported as CSV-identical. **This documentation update does not independently re-execute every pilot or establish a fully pinned, cross-platform environment.** Preserve original outputs and independently rerun before making stronger claims.

| Version | Status carried forward from prior audit discussion | Qualification |
|---|---|---|
| v0.5 | Executed; archived CSV numerical values matched | Historical deterministic illustration only |
| v0.6 | Executed; CSV byte-identical; JSON equivalent excluding output path | 12 seeds, 20 generations, 8 candidates, 16 probes; override larger script defaults |
| v0.7 | Executed; CSV byte-identical | Full JSON semantic equality not independently documented here |
| v0.8 | Executed; CSV byte-identical | Full JSON semantic equality not independently documented here |
| v0.9 | Executed; CSV byte-identical; JSON equivalent excluding output path | 12 seeds, 25 generations, 6 candidates, 12 probes |
| v1.0 | Executed; CSV byte-identical | Full JSON semantic equality not independently documented here |

JSON output paths are environment metadata, not experimental results. A semantic comparison should exclude only documented path fields and report any other difference. The archived `run_log.txt` files are not uniform command-line execution logs; some contain serialized summary data.

## Open reproducibility tasks

- Record the exact Python, NumPy, pandas and Matplotlib versions used for the **original** archive runs; the present `requirements.txt` gives compatible minimums, not an original environment lock.
- Add a clean-environment continuous-integration test and verify JSON content for all pilots.
- Create an immutable GitHub Release and, if desired, an archived DOI after final code/documentation review.
- Distinguish simulator-specific computational reproduction from independent empirical validation in real LLMs.
