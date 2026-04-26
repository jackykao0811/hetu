import numpy as np
from .projection import project, _PAIRS_3x3x3, _CENTER_IDX

class HetuLattice:
    """
    Genesis 3D-HLBM: He-Tu Symmetry-Constrained Lattice Dynamical System.
    Update operator: T = P o F o D

    Parameters
    ----------
    B         : balance constant
    alpha     : center node energy
    amplitude : forcing amplitude
    seed      : random seed

    Reference: Kao, Y.-K. (2026). DOI: 10.5281/zenodo.19784150
    """
    def __init__(self, B=1.0, alpha=0.5, amplitude=0.1, seed=None):
        self.B = float(B); self.alpha = float(alpha)
        self.amplitude = float(amplitude)
        self.rng = np.random.default_rng(seed)
        self._pairs   = _PAIRS_3x3x3
        self._center  = _CENTER_IDX
        self._nbrs    = self._build_neighbors()

    def _build_neighbors(self):
        nbrs = {}
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    idx = x*9+y*3+z; ns = []
                    for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                        nx,ny,nz = x+dx,y+dy,z+dz
                        if 0<=nx<3 and 0<=ny<3 and 0<=nz<3:
                            ns.append(nx*9+ny*3+nz)
                    nbrs[idx] = ns
        return nbrs

    def diffuse(self, E):
        """(D) Convex averaging — non-expansive under l2."""
        Enew = np.empty_like(E)
        for idx,ns in self._nbrs.items():
            Enew[idx] = (E[idx] + sum(E[n] for n in ns)) / (1+len(ns))
        return Enew

    def force(self, E):
        """(F) Bounded stochastic perturbation, clipped to [0,B]."""
        return np.clip(E + self.rng.uniform(-self.amplitude, self.amplitude, E.shape), 0.0, self.B)

    def project(self, E):
        """(P) He-Tu parallel orthogonal projection."""
        return project(E, B=self.B, alpha=self.alpha, pairs=self._pairs, center_idx=self._center)

    def step(self, E):
        """One full step: T(E) = P(F(D(E)))."""
        return self.project(self.force(self.diffuse(E)))

    def run(self, E0, steps=100):
        """Run steps iterations. Returns trajectory shape (steps+1, 27)."""
        traj = np.empty((steps+1, 27)); traj[0] = E0; E = E0.copy()
        for t in range(steps):
            E = self.step(E); traj[t+1] = E
        return traj

    def reset(self):
        """Canonical initial state: all nodes at B/2."""
        E = np.full(27, self.B/2.0); E[self._center] = self.alpha; return E

    def energy_sum(self, E): return float(E.sum())
    def variance(self, E):   return float(E.std())

    def constraint_residual(self, E):
        """Max |E[p]+E[p']-B| over all pairs. Should be 0 after projection."""
        return float(max(abs(E[i]+E[j]-self.B) for i,j in self._pairs))

    def __repr__(self):
        return f"HetuLattice(B={self.B}, alpha={self.alpha}, amplitude={self.amplitude})"
