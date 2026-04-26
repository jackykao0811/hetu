# hetu — He-Tu Symmetry-Constrained Projection Library

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19784150.svg)](https://doi.org/10.5281/zenodo.19784150)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

**He-Tu Lattice-Based Model (HLBM)** — a parameter-free, provably stable
discrete dynamical system based on the He-Tu (河圖) symmetry pairing structure.

> "We adopt the Kao He-Tu projection..."
> — the citation we want in your paper

## Installation

```bash
pip install hetu
```

Or from source:

```bash
git clone https://github.com/jackykao0811/hetu
cd hetu
pip install -e .
```

## Quick Start

```python
from hetu import project, HetuLattice
import numpy as np

# Single projection
E  = np.random.rand(27)
Ep = project(E, B=1.0, alpha=0.5)

print(f"Energy sum:  {Ep.sum():.6f}")   # always = 13.5
print(f"Max value:   {Ep.max():.6f}")   # always <= 1.0
print(f"Std dev:     {Ep.std():.6f}")   # always <= 0.5

# Full dynamical system  T = P ∘ F ∘ D
lat  = HetuLattice(B=1.0, alpha=0.5, amplitude=0.5, seed=42)
E    = lat.reset()
traj = lat.run(E, steps=200)

print(f"Final variance: {traj[-1].std():.6f}  (bound: {1.0/2})")
```

## Proved Properties

| Theorem | Statement | Status |
|---------|-----------|--------|
| Theorem 1 | Total energy invariance: Σ P(E) = 13B + α | ✓ Proved |
| Theorem 2 | Pointwise boundedness: P(E)[i] ∈ [0, B] | ✓ Proved |
| Theorem 3 | Variance bound: σ_E ≤ B/2 (Popoviciu) | ✓ Proved |
| Theorem 4 | Non-expansiveness: ‖P(E)−P(F)‖₂ ≤ ‖E−F‖₂ | ✓ Proved |
| Prop. 5.1 | Idempotence: P(P(E)) = P(E) | ✓ Proved |

## Verify theorems numerically

```python
from hetu import HetuLattice
from hetu.analysis import verify_all_theorems

lat = HetuLattice(B=1.0, alpha=0.5, amplitude=0.5, seed=0)
verify_all_theorems(lat, steps=200, verbose=True)
```

Output:
```
====================================================
  He-Tu Theorem Verification  (200 steps)
  B=1.0, alpha=0.5
====================================================
  Theorem 1 (Energy Invariance)          PASS ✓
  Theorem 2 (Boundedness)                PASS ✓
  Theorem 3 (Variance Bound)             PASS ✓
  Theorem 4 (Non-expansiveness)          PASS ✓
  Proposition 5.1 (Idempotence)          PASS ✓
====================================================
```

## Citation

If you use this library, please cite:

```bibtex
@article{kao2026genesis,
  title   = {Genesis 3D-HLBM: A Symmetry-Constrained Discrete Lattice
             Model with Bounded Energy Dynamics and a PDE Energy Bridge},
  author  = {Kao, Yao-Kai},
  year    = {2026},
  doi     = {10.5281/zenodo.19784150},
  url     = {https://github.com/jackykao0811/hetu}
}
```

## API Reference

### `hetu.project(E, B, alpha, pairs, center_idx)`
Core projection operator. Non-expansive orthogonal projection.

### `hetu.project_field(E, B, alpha)`
Vectorised projection for batch of fields, shape `(batch, 27)`.

### `hetu.idempotence_check(E, B, alpha)`
Verify `P(P(E)) == P(E)`.

### `hetu.HetuLattice(B, alpha, amplitude, seed)`
Full dynamical system with `.step()`, `.run()`, `.reset()`.

### `hetu.analysis.verify_all_theorems(lattice, steps, verbose)`
Automated theorem verification suite.

## License

MIT License — Yao-Kai Kao (2026)

## Related

- Paper: [Genesis 3D-HLBM (arXiv)](https://arxiv.org)
- DOI: [10.5281/zenodo.19784150](https://doi.org/10.5281/zenodo.19784150)
- Source: [github.com/jackykao0811/hetu](https://github.com/jackykao0811/hetu)
