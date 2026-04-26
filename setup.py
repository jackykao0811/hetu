from setuptools import setup, find_packages
setup(
    name="hetu",
    version="1.0.0",
    author="Yao-Kai Kao",
    author_email="jackykao0811@gmail.com",
    description="He-Tu Symmetry-Constrained Projection Library (Genesis 3D-HLBM)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jackykao0811/hetu",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["numpy>=1.21"],
    extras_require={
        "viz":  ["matplotlib>=3.4"],
        "test": ["pytest>=7.0"],
        "full": ["matplotlib>=3.4", "pytest>=7.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords=[
        "lattice", "projection", "stability", "energy",
        "Navier-Stokes", "He-Tu", "symmetry", "dynamical-systems"
    ],
)
