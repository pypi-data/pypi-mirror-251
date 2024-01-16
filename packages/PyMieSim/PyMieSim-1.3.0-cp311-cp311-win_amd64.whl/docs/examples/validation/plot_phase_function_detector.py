"""
Goniometrique coupling vs S1 S2
===============================

"""

# %%
# Importing the dependencies: numpy, matplotlib, PyMieSim
import numpy
import matplotlib.pyplot as plt

from PyMieSim.experiment import SphereSet, SourceSet, Setup, PhotodiodeSet
from PyMieSim import measure
from PyMieSim.scatterer import Sphere
from PyMieSim.source import PlaneWave

scatterer_diameter = 0.3e-6
scatterer_index = 1.4
source_wavelength = 1.2e-6

scatterer_set = SphereSet(
    diameter=scatterer_diameter,
    index=scatterer_index,
    n_medium=1.0
)

source_set = SourceSet(
    wavelength=source_wavelength,
    linear_polarization=[0, 90],
    optical_power=1,
    NA=0.2
)

detector_set = PhotodiodeSet(
    NA=[0.1],
    phi_offset=numpy.linspace(-180, 180, 100),
    gamma_offset=0.0,
    sampling=1000,
    polarization_filter=None
)

experiment = Setup(
    scatterer_set=scatterer_set,
    source_set=source_set,
    detector_set=detector_set
)

data = experiment.Get(measure.coupling)

source = PlaneWave(
    wavelength=source_wavelength,
    polarization_value=90,
    polarization_type='linear',
    optical_power=1,
    NA=0.2
)

scatterer = Sphere(
    diameter=scatterer_diameter,
    source=source,
    index=scatterer_index,
    n_medium=1.0
)

s1s2 = scatterer.get_s1s2()
phi, s1, s2 = s1s2.phi, s1s2.S1, s1s2.S2

figure, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4), subplot_kw={'projection': 'polar'})

data0_S1 = numpy.abs(s1)**2
data0_S1 /= data0_S1.max()
data0_S2 = numpy.abs(s2)**2
data0_S2 /= data0_S2.max()

data1 = data.array.squeeze()
data1 /= data1.max()

ax0.plot(numpy.deg2rad(phi), data0_S1, linewidth=3, zorder=1, label='Computed s1')
ax0.plot(numpy.deg2rad(detector_set.phi_offset.values.squeeze()), data1[0], linestyle='--', color='k', zorder=10, label='Computed coupling for polarization: 0')

ax1.plot(numpy.deg2rad(phi), data0_S2, linewidth=3, zorder=1, label='Computed s2')
ax1.plot(numpy.deg2rad(detector_set.phi_offset.values.squeeze()), data1[1], linestyle='--', color='k', zorder=10, label='Computed coupling for polarization: 90')

ax0.legend()
ax1.legend()
plt.show()

# -
