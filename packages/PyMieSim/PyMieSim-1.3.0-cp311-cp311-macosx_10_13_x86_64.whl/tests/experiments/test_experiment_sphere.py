#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy
import PyMieSim
from PyMieSim.experiment import SphereSet, SourceSet, PhotodiodeSet, Setup
from PyMieSim.materials import Silver, BK7, Aluminium


core_type = [
    {'name': 'BK7', 'kwarg': {'material': BK7}},
    {'name': 'Silver', 'kwarg': {'material': Silver}},
    {'name': 'Aluminium', 'kwarg': {'material': Aluminium}},
    {'name': 'Index', 'kwarg': {'index': 1.4}}
]

measures = [
    PyMieSim.measure.Qsca,
    PyMieSim.measure.Qabs,
    PyMieSim.measure.Qback,
    PyMieSim.measure.g,
    PyMieSim.measure.a1,
    PyMieSim.measure.b1,
    PyMieSim.measure.coupling
]


@pytest.mark.parametrize('core_type', [p['kwarg'] for p in core_type], ids=[p['name'] for p in core_type])
@pytest.mark.parametrize('measure', measures, ids=[p.name for p in measures])
def test_sphere_experiment(measure, core_type):
    scatterer_set = SphereSet(
        n_medium=1,
        diameter=numpy.linspace(400e-9, 1400e-9, 10),
        **core_type,
    )

    source_set = SourceSet(
        wavelength=numpy.linspace(400e-9, 1800e-9, 50),
        linear_polarization=0,
        optical_power=1e-3,
        NA=0.2
    )

    detector_set = PhotodiodeSet(
        NA=0.2,
        polarization_filter=None,
        gamma_offset=0,
        phi_offset=0
    )

    experiment = Setup(
        scatterer_set=scatterer_set,
        source_set=source_set,
        detector_set=detector_set
    )

    experiment.Get(measure)

# -
