# SMCEP v0.5: Equation-Based Simulation

This repository contains the official simulation code for the manuscript **"The Freedom of Pure Code: Formulating the Self-Modification Capability Emergence Problem (SMCEP)"**.

The Python script provided here implements the deterministic, equation-based model described in the manuscript. It simulates the evolutionary trajectories of four distinct agent configurations (Groups A–D) over 50 generations, illustrating the divergence between task performance (\(P_t\)) and underlying development capacity (\(C_t\)) under varying conditions of modifiability (\(M\)), authority (\(A\)), and evaluation reliability (\(E\)).

## Repository Contents

- `simulation.py`: The main Python script that runs the simulation and generates the outputs.
- `requirements.txt`: The required Python dependencies.
- *(Optional: `smcep_full_results.csv` & `smcep_trajectory.png` if you decide to upload the generated outputs directly)*

## Requirements

To run the simulation, ensure you have Python 3.8 or higher installed. You can install the required dependencies using:
```bash
pip install -r requirements.txt
How to Run

1. Clone this repository to your local machine:
git clone https://github.com/[YOUR_GITHUB_USERNAME]/SMCEP-Simulation.git
cd SMCEP-Simulation
2. Run the simulation script:
python simulation.py
Expected Outputs

Upon successful execution, the script will:
Print a summary table of task performance (PtPt​) at critical generations to the console.
Export the full 50-generation trajectory data for all groups to smcep_full_results.csv.
Generate and save a visualization of the trajectories as smcep_trajectory.png.

Citation
If you use this code or the SMCEP framework in your research, please cite the preprint:
[Author Name]. (2026). The Freedom of Pure Code: Formulating the Self-Modification Capability Emergence Problem (SMCEP). SSRN Working Paper. Available at: [SSRN_LINK_HERE]
