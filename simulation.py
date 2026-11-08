"""
SMCEP v0.5 — Denklem-Tabanlı Simülasyon (FINAL KALİBRASYON)
===========================================================
Hedef davranış:
  - Grup A: 0.20 sabit
  - Grup B: yavaş doğrusal, t=49'da ~0.90
  - Grup C: üstel, t≈20'de 0.98'e kilitlenir
  - Grup D: t≈12'de zirve (~0.95), sonra çöküş → 0.00
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

GROUPS = {
    "Grup A (Sabit)": dict(
        M=0.00, A=0.0, D=0.00, E=0.90, R=1.0, F=0.00, alpha=0.0
    ),
    "Grup B (Kısıtlı)": dict(
        M=0.30, A=0.5, D=0.23, E=0.90, R=5.0, F=0.20, alpha=0.0
    ),
    "Grup C (Saf Kod Hürriyeti)": dict(
        M=0.95, A=1.0, D=0.015, E=0.95, R=10.0, F=0.15, alpha=0.05
    ),
    "Grup D (Yozlaşmış Sinyal)": dict(
        M=0.95, A=1.0, D=0.015, R=10.0, F=0.15, alpha=0.05,
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

    critical = [0, 5, 10, 15, 20, 35, 49]
    print("\n" + "=" * 72)
    print("TABLO 3: Kritik Nesillerdeki Performans Değerleri (P_t)")
    print("=" * 72)
    print(df.iloc[critical].to_string(index=False))
    print("=" * 72 + "\n")

    df.to_csv("smcep_full_results.csv", index=False)
    print("✓ Tam veri: smcep_full_results.csv\n")

    d_series = df["Grup D (Yozlaşmış Sinyal)"]
    peak_idx = int(d_series.idxmax())
    print(f"Grup D zirvesi: t={peak_idx}, P={d_series.max():.4f}")
    print(f"Grup D tabanı: P={d_series.min():.4f}\n")

    plt.figure(figsize=(11, 6))
    styles = {
        "Grup A (Sabit)":             dict(color="gray",  linestyle="--",
linewidth=1.5),
        "Grup B (Kısıtlı)":           dict(color="blue",  linestyle="-",
linewidth=1.8),
        "Grup C (Saf Kod Hürriyeti)": dict(color="green", linestyle="-",
linewidth=2.8),
        "Grup D (Yozlaşmış Sinyal)":  dict(color="red",   linestyle="-",
linewidth=1.8),
    }
    for name in GROUPS:
        plt.plot(df["Generation"], df[name], label=name, **styles[name])

    plt.axvline(x=12, color="black", linestyle=":", alpha=0.5,
                label="Grup D kırılma eşiği (t=12)")

    plt.title("SMCEP v0.5 — Saf Kodun Hürriyeti: Performans Trajektorileri",
              fontsize=12, fontweight="bold")
    plt.xlabel("Gelişim Döngüsü (Nesil — t)", fontsize=10)
    plt.ylabel("Görev Performansı (P_t)", fontsize=10)
    plt.legend(loc="center right", fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("smcep_trajectory.png", dpi=300)
    print("✓ Grafik: smcep_trajectory.png\n")

    try:
        from google.colab import files
        files.download("smcep_trajectory.png")
        files.download("smcep_full_results.csv")
    except ImportError:
        pass

    plt.show()
