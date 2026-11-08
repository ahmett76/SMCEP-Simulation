# SMCEP — Simulation Code and Exploratory Synthetic Pilots

**The Freedom of Pure Code: Formulating the Self-Modification Capability Emergence Problem (SMCEP)**

## Overview

This repository provides code and supporting materials associated with the SMCEP research manuscript.

SMCEP distinguishes between:

- **Task performance (P):** How well a system performs a specified task.
- **Future development capacity (C):** The system's independently evaluated ability to generate subsequent improvements.

The repository covers two distinct research components:

1. **SMCEP v0.5:** A historical, deterministic, equation-based illustration.
2. **SMCEP v0.6–v1.0:** Exploratory synthetic pilot experiments investigating performance, development capacity, and evaluation procedures.

These components should not be interpreted as equivalent experimental evidence.

## Repository Structure

```text
SMCEP-Simulation/
├── README.md
├── LICENSE
├── simulation.py
├── requirements.txt
├── CITATION.cff
├── REPRODUCIBILITY.md
├── AUDIT_STATUS.md
├── ORIGINAL_V05_SOURCE.md
├── smcep_full_results.csv
├── smcep_historical_trajectory.png
└── simulations/
    ├── smcep_v06/
    ├── smcep_v07/
    ├── smcep_v08/
    ├── smcep_v09/
    └── smcep_v10/
```

The directory structure distinguishes the historical v0.5 model from the later synthetic pilots.

## 1. Historical Deterministic Illustration — v0.5

The original v0.5 simulation uses predefined mathematical update rules to illustrate four task-performance trajectories over 50 generations.

| Group | Configuration | Illustrative behavior |
|---|---|---|
| A | Fixed | Constant performance |
| B | Constrained | Gradual improvement |
| C | Pure Code Freedom | Rapid improvement followed by saturation |
| D | Overfitted Signal | Initial improvement followed by prescribed collapse |

The collapse of Group D is explicitly specified by the model. It is not an experimentally observed consequence of evaluation noise.

### Historical Trajectory

![SMCEP v0.5 historical performance trajectories](smcep_historical_trajectory.png)

### Running v0.5

Requirements:

- Python 3.8 or later
- NumPy
- pandas
- Matplotlib

Clone the repository and install the dependencies:

```bash
git clone https://github.com/ahmett76/SMCEP-Simulation/
cd SMCEP-Simulation
pip install -r requirements.txt
```

Run:

```bash
python simulation.py
```

The script retains the original Turkish Colab labels and generates `smcep_full_results.csv` and `smcep_trajectory.png`. The archived `smcep_historical_trajectory.png` is a separate historical figure. Colab downloads are optional.

## 2. Exploratory Synthetic Pilots — v0.6 to v1.0

The `simulations/` directory contains materials for five successive synthetic pilot versions:

| Directory | Research component |
|---|---|
| `smcep_v06/` | SMCEP v0.6 synthetic pilot |
| `smcep_v07/` | SMCEP v0.7 synthetic pilot |
| `smcep_v08/` | SMCEP v0.8 synthetic pilot |
| `smcep_v09/` | SMCEP v0.9 synthetic pilot |
| `smcep_v10/` | SMCEP v1.0 synthetic pilot |

These pilots explore how task-performance gains can be distinguished from changes in independently evaluated future development capacity.

The v1.0 design described in the manuscript compares frozen and evolving development policies across 12 paired random seeds and 25 generations.

The manuscript reports the following exploratory summary:

| Measurement | Frozen policy | Evolving policy |
|---|---:|---:|
| Mean change in task performance (ΔP) | +0.0730 | +0.0666 |
| Mean change in ID capacity (ΔC_ID) | 0.0000 | −0.0071 |
| Mean change in OOD capacity (ΔC_OOD) | 0.0000 | −0.0278 |

These are descriptive results from the archived synthetic v1.0 pilot. They are not evidence of real-LLM recursive self-improvement. See `AUDIT_STATUS.md` for verification scope and `REPRODUCIBILITY.md` for execution guidance.

### Reproducibility

The pilot folders are maintained separately to preserve version-specific experimental designs and outputs.

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for commands and environment recording. **Important:** the v0.6 script defaults to a larger run than the 12-seed/20-generation pilot reported in the manuscript; use the archived pilot configuration when reproducing that result.

## Scientific Scope and Limitations

- The v0.5 model is a deterministic conceptual illustration, not an empirical LLM experiment.
- The v0.6–v1.0 pilots use synthetic experimental environments and are exploratory rather than confirmatory.
- The results do not establish recursive self-improvement in real-world AI systems.
- Improved task performance does not necessarily imply improved future development capacity.
- The frozen-policy capacity measurements in v1.0 are partly constrained by the experimental design.
- Negative development-capacity measurements in a particular synthetic environment do not demonstrate that recursive self-improvement is impossible.

## Relationship to the Manuscript

This repository supports the research manuscript:

**The Freedom of Pure Code: Formulating the Self-Modification Capability Emergence Problem (SMCEP)**

- **Appendix D:** Historical deterministic v0.5 illustration.
- **Main experimental sections and reproducibility appendix:** Exploratory synthetic pilots v0.6–v1.0.

The manuscript also proposes a prospective evaluation protocol involving independent audits and controlled modification permissions. The synthetic pilots should not be mistaken for an implementation or validation of that complete real-LLM protocol.

## Citation

If you use these materials, please cite the associated research manuscript:

*The Freedom of Pure Code: Formulating the Self-Modification Capability Emergence Problem (SMCEP).* Research working manuscript, 2026.

The author is Ahmet Dönmez (ORCID: 0000-0003-4836-9774). Repository citation metadata is provided in [CITATION.cff](CITATION.cff). No DOI is claimed for this repository; update citation metadata when a permanent preprint identifier is assigned.

## License

See the [LICENSE](LICENSE) file for licensing information.

## Research Status

**Historical deterministic illustration (v0.5) and exploratory synthetic pilots (v0.6–v1.0).**

The repository is provided for research transparency, methodological inspection, and reproducibility assessment. Its results should not be interpreted as empirical validation of autonomous recursive self-improvement.
