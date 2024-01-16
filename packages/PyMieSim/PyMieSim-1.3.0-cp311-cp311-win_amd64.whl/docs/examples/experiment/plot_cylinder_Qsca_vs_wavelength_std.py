"""
Cylinder: Qsca vs wavelength std
================================

"""

# %%
# Importing the package dependencies: numpy, PyMieSim
import numpy as np
from PyMieSim.experiment import CylinderSet, SourceSet, Setup
from PyMieSim.materials import Silver
from PyMieSim import measure

# %%
# Defining the ranging parameters for the scatterer distribution
scatterer_set = CylinderSet(
    diameter=np.linspace(400e-9, 1400e-9, 10),
    material=Silver,
    n_medium=1
)

# %%
# Defining the source to be employed.
source_set = SourceSet(
    wavelength=np.linspace(200e-9, 1800e-9, 300),
    linear_polarization=[0],
    optical_power=1e-3,
    NA=0.2
)

# %%
# Defining the experiment setup
experiment = Setup(
    scatterer_set=scatterer_set,
    source_set=source_set
)

# %%
# Measuring the properties
data = experiment.Get(measure.Qsca)

# %%
# Plotting the results
figure = data.plot(
    x=source_set.wavelength,
    y_scale='log',
    std=scatterer_set.diameter
)

_ = figure.show()
