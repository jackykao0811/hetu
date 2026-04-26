import numpy as np
from .projection import project

def energy_sum(E): return float(E.sum())
def variance(E):   return float(E.std())
def is_bounded(E, B=1.0, tol=1e-10):
    return bool(np.all(E >= -tol) and np.all(E <= B+tol))

def nonexpansive_check(E, F, B=1.0, alpha=0.5, tol=1e-10):
    """Verify Theorem 4: ||P(E)-P(F)||_2 <= ||E-F||_2."""
    PE = project(E, B=B, alpha=alpha); PF = project(F, B=B, alpha=alpha)
    before = float(np.linalg.norm(E-F)); after = float(np.linalg.norm(PE-PF))
    ratio  = after/before if before > 1e-15 else 0.0
    return {"before":before,"after":after,"ratio":ratio,"satisfied":ratio<=1.0+tol}

def verify_all_theorems(lattice, steps=200, tol=1e-9, verbose=True):
    """
    Run full theorem verification suite. Returns dict of {name: bool}.

    Examples
    --------
    >>> from hetu import HetuLattice
    >>> from hetu.analysis import verify_all_theorems
    >>> lat = HetuLattice(seed=0)
    >>> verify_all_theorems(lat, verbose=True)
    """
    S_star = 13*lattice.B + lattice.alpha
    E = lattice.reset()
    t1=t2=t3=t4=p5=True
    rng2 = np.random.default_rng(999)
    for _ in range(steps):
        E = lattice.step(E)
        if abs(energy_sum(E)-S_star) > tol:      t1=False
        if not is_bounded(E,B=lattice.B,tol=tol): t2=False
        if variance(E) > lattice.B/2.0+tol:       t3=False
        F = rng2.uniform(0,lattice.B,size=27)
        if not nonexpansive_check(E,F,B=lattice.B,alpha=lattice.alpha,tol=tol)["satisfied"]: t4=False
        PE=lattice.project(E); PPE=lattice.project(PE)
        if np.max(np.abs(PE-PPE))>tol: p5=False

    results = {
        "Theorem 1 (Energy Invariance)":t1,
        "Theorem 2 (Boundedness)":t2,
        "Theorem 3 (Variance Bound)":t3,
        "Theorem 4 (Non-expansiveness)":t4,
        "Proposition 5.1 (Idempotence)":p5,
    }
    if verbose:
        print(f"\n{'='*52}")
        print(f"  He-Tu Theorem Verification  ({steps} steps)")
        print(f"  B={lattice.B}, alpha={lattice.alpha}")
        print(f"{'='*52}")
        for name,passed in results.items():
            print(f"  {name:<38}  {'PASS' if passed else 'FAIL'}")
        print(f"{'='*52}\n")
    return results
