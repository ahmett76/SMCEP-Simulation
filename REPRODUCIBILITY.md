# Reproducing the SMCEP simulation archive

The five pilots are **exploratory synthetic simulations**. Version v0.5 is a separate deterministic illustration. Do not combine these as independent replications.

## Environment

Create a Python virtual environment and install `requirements.txt`. The dependency file specifies minimum compatible versions; it is **not** a historical lockfile. Record `python --version` and `python -m pip freeze` with each new reproduction. For reference, the environment in which this documentation was prepared reported Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, and Matplotlib 3.10.8; these are **not verified as the versions used to generate the original archived results**.

## Commands

Run from the repository root. Specify an output directory to avoid script defaults that refer to `/mnt/data`.

```bash
python simulation.py
python simulations/smcep_v06/smcep_simulation.py --seeds 12 --generations 20 --candidates 8 --probes 16 --task-count 24 --out /tmp/smcep_v06_check
python simulations/smcep_v07/smcep_v07.py --out /tmp/smcep_v07_check
python simulations/smcep_v08/smcep_v08.py --out /tmp/smcep_v08_check
python simulations/smcep_v09/smcep_v09.py --out /tmp/smcep_v09_check
python simulations/smcep_v10/smcep_v10.py --out /tmp/smcep_v10_check
```

Check each version's `README.md`, script arguments and archived `summary.json` before comparing outcomes. **The v0.6 default is 30 seeds, 40 generations and 40 probes**, not the reported manuscript configuration. v1.0 imports `smcep_v09.py` from the sibling version directory; retain the original directory structure.

## Comparison protocol

Compare newly produced `trajectories.csv` with the corresponding archived file, then compare the numeric and categorical scientific fields of `summary.json`. Document and exclude only environment-dependent output-path metadata (`parameters.out`) when justified. A changed seed, task/probe count, or any scientific statistic is **not** a harmless metadata difference. Preserve original archived outputs and report any mismatch.

For v0.5, the script's generated `smcep_trajectory.png` differs in filename from the archived `smcep_historical_trajectory.png` and should not be expected to match byte-for-byte.
