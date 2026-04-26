"""
tests/test_theorems.py  —  pytest suite for Kao (2026) theorems
Run:  pytest tests/ -v
"""
import numpy as np
import pytest
from hetu import project, project_field, idempotence_check, HetuLattice
from hetu.analysis import (energy_sum, variance, is_bounded,
                            nonexpansive_check, verify_all_theorems)

B, ALPHA = 1.0, 0.5
S_STAR   = 13 * B + ALPHA
RNG      = np.random.default_rng(42)

@pytest.fixture
def random_E():
    return RNG.uniform(0, B, size=27)

@pytest.fixture
def lattice():
    return HetuLattice(B=B, alpha=ALPHA, amplitude=0.5, seed=42)

class TestTheorem1:
    def test_single(self, random_E):
        PE = project(random_E, B=B, alpha=ALPHA)
        assert abs(PE.sum() - S_STAR) < 1e-10
    def test_extreme(self):
        for _ in range(100):
            E = RNG.uniform(-10, 10, size=27)
            assert abs(project(E,B=B,alpha=ALPHA).sum() - S_STAR) < 1e-10
    def test_trajectory(self, lattice):
        E = lattice.reset()
        for _ in range(200):
            E = lattice.step(E)
            assert abs(E.sum() - S_STAR) < 1e-9

class TestTheorem2:
    def test_after_proj(self, random_E):
        assert is_bounded(project(random_E, B=B, alpha=ALPHA), B=B)
    def test_trajectory(self, lattice):
        E = lattice.reset()
        for _ in range(200):
            E = lattice.step(E)
            assert is_bounded(E, B=B)

class TestTheorem3:
    def test_after_proj(self, random_E):
        assert project(random_E,B=B,alpha=ALPHA).std() <= B/2 + 1e-10
    def test_trajectory(self, lattice):
        E = lattice.reset()
        for _ in range(200):
            E = lattice.step(E)
            assert E.std() <= B/2 + 1e-9

class TestTheorem4:
    def test_random_pairs(self):
        for _ in range(500):
            E = RNG.uniform(0,B,size=27); F = RNG.uniform(0,B,size=27)
            r = nonexpansive_check(E,F,B=B,alpha=ALPHA)
            assert r["satisfied"], f"ratio={r['ratio']:.6f}"

class TestProp51:
    def test_idempotence(self):
        for _ in range(200):
            E = RNG.uniform(-100,100,size=27)
            assert idempotence_check(E,B=B,alpha=ALPHA)
    def test_residual(self, lattice):
        E = lattice.reset()
        for _ in range(100):
            E = lattice.step(E)
            assert lattice.constraint_residual(E) < 1e-10

class TestBatch:
    def test_project_field(self):
        batch = RNG.uniform(0,B,size=(50,27))
        out   = project_field(batch,B=B,alpha=ALPHA)
        assert out.shape == (50,27)
        for k in range(50):
            assert abs(out[k].sum()-S_STAR) < 1e-10

def test_full_suite():
    lat = HetuLattice(B=B,alpha=ALPHA,amplitude=0.5,seed=0)
    results = verify_all_theorems(lat,steps=200,verbose=False)
    for name,passed in results.items():
        assert passed, f"FAILED: {name}"
