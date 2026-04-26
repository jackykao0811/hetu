import numpy as np
from typing import Optional, List, Tuple

def _build_pairs_3x3x3():
    pairs, seen = [], set()
    center = np.array([1,1,1])
    for x in range(3):
        for y in range(3):
            for z in range(3):
                p  = np.array([x,y,z])
                pp = 2*center - p
                idx  = x*9+y*3+z
                idxp = pp[0]*9+pp[1]*3+pp[2]
                if idx == idxp: continue
                key = tuple(sorted([idx,idxp]))
                if key not in seen:
                    seen.add(key); pairs.append((idx,idxp))
    return pairs

_PAIRS_3x3x3 = _build_pairs_3x3x3()
_CENTER_IDX  = 13   # (1,1,1)

def project(E, B=1.0, alpha=0.5, pairs=None, center_idx=None, inplace=False):
    """
    He-Tu orthogonal projection onto the constraint manifold.

    For each antipodal pair {p,p'}:
        delta     = 0.5 * (B - E[p] - E[p'])
        P(E)[p]   = E[p]  + delta
        P(E)[p']  = E[p'] + delta
    Center: P(E)[c] = alpha (fixed)

    Properties (Kao 2026):
    - Non-expansive:  ||P(E)-P(F)||_2 <= ||E-F||_2  (Theorem 4)
    - Idempotent:     P(P(E)) = P(E)                 (Prop 5.1)
    - Energy-conserving: sum(P(E)) = 13B+alpha       (Theorem 1)
    - Bounded:        P(E)[i] in [0,B]               (Theorem 2)

    Reference: Kao, Y.-K. (2026). DOI: 10.5281/zenodo.19784150
    """
    if pairs is None:     pairs      = _PAIRS_3x3x3
    if center_idx is None: center_idx = _CENTER_IDX
    Ep = E if inplace else np.array(E, dtype=float)
    for i,j in pairs:
        d = 0.5*(B - Ep[i] - Ep[j])
        Ep[i] += d; Ep[j] += d
    Ep[center_idx] = alpha
    return Ep

def project_field(E, B=1.0, alpha=0.5, pairs=None, center_idx=None):
    """Vectorised projection for batch of fields, shape (batch, 27)."""
    if E.ndim == 1:
        return project(E, B=B, alpha=alpha, pairs=pairs, center_idx=center_idx)
    result = np.empty_like(E, dtype=float)
    for k in range(len(E)):
        result[k] = project(E[k], B=B, alpha=alpha,
                             pairs=pairs, center_idx=center_idx)
    return result

def idempotence_check(E, B=1.0, alpha=0.5, tol=1e-12):
    """Verify Proposition 5.1: P(P(E)) == P(E)."""
    PE  = project(E,  B=B, alpha=alpha)
    PPE = project(PE, B=B, alpha=alpha)
    return float(np.max(np.abs(PE - PPE))) < tol
