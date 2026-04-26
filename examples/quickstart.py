"""
quickstart.py — He-Tu Library Quick Start
==========================================
Run:  python examples/quickstart.py

Reference: Kao, Y.-K. (2026). Genesis 3D-HLBM.
DOI: 10.5281/zenodo.19784150
"""
import sys; sys.path.insert(0, "..")
import numpy as np
from hetu import project, HetuLattice
from hetu.analysis import verify_all_theorems

print("=" * 56)
print("  He-Tu Library  —  Quick Start")
print("  Kao (2026)  DOI: 10.5281/zenodo.19784150")
print("=" * 56)

# ── 1. Single projection ──────────────────────────────────────
print("\n[1] Single projection")
E  = np.random.default_rng(0).uniform(0, 1, 27)
Ep = project(E, B=1.0, alpha=0.5)
print(f"  Energy sum  : {Ep.sum():.8f}  (expected 13.5)")
print(f"  Max / Min   : {Ep.max():.4f} / {Ep.min():.4f}  (in [0,1])")
print(f"  Std dev     : {Ep.std():.4f}  (bound: 0.5)")

# ── 2. Run lattice dynamics ───────────────────────────────────
print("\n[2] HetuLattice  T = P∘F∘D  (500 steps, amplitude=2.0)")
lat  = HetuLattice(B=1.0, alpha=0.5, amplitude=2.0, seed=99)
E0   = lat.reset()
traj = lat.run(E0, steps=500)
print(f"  Final energy sum : {traj[-1].sum():.6f}  (expected 13.5)")
print(f"  Final std dev    : {traj[-1].std():.6f}  (bound: 0.5)")
print(f"  Constraint res.  : {lat.constraint_residual(traj[-1]):.2e}  (expected ~0)")

# ── 3. Full theorem verification ─────────────────────────────
print("\n[3] Theorem verification (200 steps)")
results = verify_all_theorems(lat, steps=200, verbose=True)
assert all(results.values()), "Some theorems failed!"
print("All theorems confirmed numerically.")

print("\nCitation:")
print('  Kao, Y.-K. (2026). Genesis 3D-HLBM.')
print('  DOI: 10.5281/zenodo.19784150')
