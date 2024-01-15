# gamda: GPU-Accelerated Molecular Dynamics Analysis

gamda, a python library which utilizes the CUDA-enable GPU to accelerate the analysis of molecular dynamics (MD)

# Dependency

1. cupy

cupy is the backend of the CUDA kernels for analysis

2. MDAnalysis

MDAnalysis is used to handle the reading of MD trajectories and the selection of atoms

# Installation

## from pypi

```
pip install gamda
```

## from gitee

```
git clone https://gitee.com/gao_hyp_xyj_admin/gamda.git
cd gamda
pip install .
```

# Unittest

```
git clone https://gitee.com/gao_hyp_xyj_admin/gamda.git
cd gamda
cd unittest
python -m unittest
```

# Usage

A simple exampe:

```
# Here, we create a xyz file as an example
with open("test.xyz", "w") as f:
    f.write("3\n3\nO 1.11 2.22 3.33\nH 3.33 2.22 1.11\nH 2.22 2.22 2.22")

# Import the package
import gamda
import numpy as np

# Import the desired observable
from gamda.observable import PositionZ

# Import the disired analyzer
from gamda.analyzer import Histogrammer

# gamda.Universe is a subclass of MDAnalysis.Universe
u = gamda.Universe("test.xyz")

# Get your AtomGroup in host (CPU)
ag = u.select_atoms("element H")

# Get your AtomGroup in device (GPU)
dag = u.get_dag("atom", ag)

# Initialize your observable
z = PositionZ("z", dag, gamda.Argument("z", np.float32(0)))

# Initialize your analyzer and add it to the universe
zdf = Histogrammer("zdf", 0, 4, 4, z)
u.add_analyzer(zdf)

# Print the source code
print(u.source_code)

# Run
u.run()

# Free the memory
u.free()
del u

# Normalize the result and save
zdf.normalize()
zdf.save("test_zdf.txt")

```

# Reference

1. cupy
    - https://github.com/cupy/cupy
2. MDAnalysis
    - N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein. MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations. J. Comput. Chem. 32 (2011), 2319–2327. doi:10.1002/jcc.21787
    - R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler, D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein. MDAnalysis: A Python package for the rapid analysis of molecular dynamics simulations. In S. Benthall and S. Rostrup, editors, Proceedings of the 15th Python in Science Conference, pages 98-105, Austin, TX, 2016. SciPy. doi:10.25080/Majora-629e541a-00e
