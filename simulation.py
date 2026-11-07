"""
SMCEP v0.5 - Equation-Based Simulation (Final Calibration)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def barrier(M, A, M_thr=0.20, A_thr=0.30):
    m_eff = max(0.0, min(1.0, (M - M_thr) / (1.0 - M_thr)))
    a_eff = max(0.0, min(1.0, (A - A_thr) / (1.0 - A_thr)))
    return m_eff * a_eff

def sigma_E(E, E_crit=0.60, sharp=12.0):
    return 1.0 / (1.0 + np.exp(-sharp * (E - E_crit)))

def dynamic_D(D_base, C, alpha, cap=1.0):
    return min(cap, D_base + alpha * C)

def delta_P(M, A, D_t, E, R):
    return barrier(M, A) * D_t * sigma_E(E) * np.log1p(R)

def step(state, params, t):
    P, C = state
    M, A = params["M"], params["A"]
    D_base, R, F = params["D"], params["R"], params["F"]
    alpha = params["alpha"]
    delta_decay = params.get("delta_decay", 0.03)

    if params.get("E_dynamic"):
        E = params["E_high"] if t < params["t_switch"] else params["E_low"]
    else:
        E = params["E"]

    E_crit = params.get("E_crit", 0.60)
    D_t = dynamic_D(D_base, C, alpha)
    dP = delta_P(M, A, D_t, E, R)

    if E < E_crit:
        P -= delta_decay
        C -= delta_decay
    else:
        P += dP
        C += F * dP

    return (max(0.0, min(0.98, P)), max(0.0, C))

# --- Group Parameters ---
GROUPS = {
    "Group A (Static)": dict(M=0.00, A=0.0, D=0.00, E=0.90, R=1.0, F=0.00, alpha=0.0),
    "Group B (Restricted)": dict(M=0.30, A=0.5, D=0.23, E=0.90, R=5.0, F=0.20, alpha=0.0),
    "Group C (Pure Code Freedom)": dict(M=0.95, A=1.0, D=0.015, E=0.95, R=10.0, F=0.15, alpha=0.05),
    "Group D (Corrupted Signal)": dict(M=0.95, A=1.0, D=0.015, R=10.0, F=0.15, alpha=0.05,
        E_dynamic=True, E_high=0.95, E_low=0.30, t_switch=12,
        E_crit=0.60, delta_decay=0.03
    ),
}

GENERATIONS = 50
INITIAL_STATE = (0.20, 0.05)

def run_simulation():
    results = {"Generation": list(range(GENERATIONS))}
    for name, params in GROUPS.items():
        state = INITIAL_STATE
        traj = []
        for t in range(GENERATIONS):
            traj.append(round(state[0], 4))
            state = step(state, params, t)
        results[name] = traj
    return pd.DataFrame(results)

if __name__ == "__main__":
    df = run_simulation()
    
    # Print critical data points
    critical = [0, 5, 10, 15, 20, 35, 49]
    print(df.iloc[critical].to_string(index=False))
    
    # Save data
    df.to_csv("smcep_full_results.csv", index=False)

    # Plot and save figure
    plt.figure(figsize=(11, 6))
    styles = {
        "Group A (Static)": dict(color="gray", linestyle="--"),
        "Group B (Restricted)": dict(color="blue"),
        "Group C (Pure Code Freedom)": dict(color="green", linewidth=2.8),
        "Group D (Corrupted Signal)": dict(color="red"),
    }
    for name in GROUPS:
        plt.plot(df["Generation"], df[name], label=name, **styles[name])
    plt.axvline(x=12, color="black", linestyle=":", alpha=0.5)
    plt.xlabel("Generation (t)")
    plt.ylabel("Performance (P_t)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig("smcep_trajectory.png", dpi=300)
    plt.show()
