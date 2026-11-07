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
