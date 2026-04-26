"""
hetu — He-Tu Symmetry-Constrained Projection Library
DOI: https://doi.org/10.5281/zenodo.19784150

Citation
--------
@article{kao2026genesis,
  title  = {Genesis 3D-HLBM: A Symmetry-Constrained Discrete Lattice
            Model with Bounded Energy Dynamics and a PDE Energy Bridge},
  author = {Kao, Yao-Kai},
  year   = {2026},
  doi    = {10.5281/zenodo.19784150},
  url    = {https://github.com/jackykao0811/hetu}
}
"""
from ._version  import __version__
from .projection import project, project_field, idempotence_check
from .lattice    import HetuLattice
from .analysis   import energy_sum, variance, is_bounded, nonexpansive_check

__author__    = "Yao-Kai Kao"
__email__     = "jackykao0811@gmail.com"
__doi__       = "10.5281/zenodo.19784150"
__all__ = ["project","project_field","idempotence_check",
           "HetuLattice","energy_sum","variance","is_bounded","nonexpansive_check"]
