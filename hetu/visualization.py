"""
hetu.visualization
==================
Quick-look plots for He-Tu lattice trajectories.
Requires matplotlib (optional dependency).
"""

import numpy as np


def plot_trajectory(traj, B=1.0, title="HetuLattice trajectory", show=True):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("pip install matplotlib")

    T = len(traj)
    ts = np.arange(T)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle(title, fontsize=13, fontweight="bold")

    axes[0].plot(ts, traj.mean(axis=1), color="#1565c0", lw=1.5)
    axes[0].axhline(B/2, color="gray", ls="--", lw=1, label=f"B/2={B/2}")
    axes[0].set_xlabel("Step"); axes[0].set_ylabel("Mean E")
    axes[0].set_title("Mean Energy"); axes[0].legend()

    axes[1].plot(ts, traj.std(axis=1), color="#c62828", lw=1.5, label="sigma_E")
    axes[1].axhline(B/2, color="gray", ls="--", lw=1, label=f"B/2={B/2}")
    axes[1].set_xlabel("Step"); axes[1].set_ylabel("sigma_E")
    axes[1].set_title("Variance (Theorem 3)"); axes[1].legend()

    axes[2].plot(ts, traj.sum(axis=1), color="#2e7d32", lw=1.5)
    axes[2].set_xlabel("Step"); axes[2].set_ylabel("Total Energy")
    axes[2].set_title("Energy Sum (Theorem 1)")

    plt.tight_layout()
    if show:
        plt.show()
    return fig


def plot_amplitude_sweep(B=1.0, alpha=0.5, amplitudes=None,
                         steps=100, seed=42, show=True):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("pip install matplotlib")
    from .lattice import HetuLattice

    if amplitudes is None:
        amplitudes = np.logspace(np.log10(0.88), np.log10(10.0), 18)

    sigmas = []
    for A in amplitudes:
        lat = HetuLattice(B=B, alpha=alpha, amplitude=A, seed=seed)
        E = lat.reset()
        for _ in range(steps):
            E = lat.step(E)
        sigmas.append(lat.variance(E))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogx(amplitudes, sigmas, "o-", color="#1565c0", lw=1.5,
                label="sigma_E(T) -- He-Tu HLBM")
    ax.axhline(B/2, color="#c62828", ls="--", lw=1.5,
               label=f"Theorem 3 bound  B/2 = {B/2}")
    ax.set_xlabel("Forcing Amplitude A (log scale)")
    ax.set_ylabel("sigma_E after T steps")
    ax.set_title("Amplitude Sweep: Theorem 3 Verification\n(Kao 2026, Genesis 3D-HLBM)")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if show:
        plt.show()
    return fig, amplitudes, sigmas
