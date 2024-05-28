
Welcome to FPV Simulation Documentation!
=========================================

Overview
--------

This documentation provides a comprehensive guide to the FPV Simulation project, 
which includes modules for simulating Floating Photovoltaic (FPV) systems on lakes. 
This package was developed as part of my master thesis, a study to estimate the annual energy yield on 
inland water bodies in Norway. By adjusting the PV module parameters, the package can also be used for 
regular land-based systems.


The documentation covers the core modules, their classes, methods, and usage examples.



Modules
-------

The following modules are included in this documentation:

- `lake`: Defines the `Lake` class for managing PV systems on lakes.
- `pvmodel`: Contains the `PVmodel` class for simulating PV system performance.
- `pvsystem`: Includes the `PVsystem` class for representing and simulating PV systems.
- `simulation`: Provides the `FPVsimulation` class for managing and running FPV system simulations.
- `soiling_loss_NS3031`: Manages soiling loss calculations based on geographical locations.


.. toctree::
   :maxdepth: 2
   :caption: Modules:

   FPVsimulation.lake
   FPVsimulation.pvmodel
   FPVsimulation.pvsystem
   FPVsimulation.simulation
   FPVsimulation.soiling_loss_NS3031

Getting Started
===============

To get started with using the FPV Simulation project, follow the steps below:

1. **Building python package:**
   - Build the python package using

   .. code-block:: bash

      pip install build
      python -m build
      pip install -e .

2. **Basic Usage:**
   - Create and register lakes, then simulate the PV systems.

   .. code-block:: python

      from FPVsimulation.lake import Lake
      from FPVsimulation.simulation import FPVsimulation
      import pandas as pd

      # Create a simulation instance
      simulation = FPVsimulation()

      # Register lakes from a DataFrame
      df = pd.DataFrame({
          'lake_id': ['Lake1', 'Lake2'],
          'lake_area': [50, 70],
          'latitude': [60.0, 62.0],
          'longitude': [5.0, 7.0],
          'selected_area': [1.5, 2.0],
          'max_power_MW': [2.0, 3.0]
      })
      simulation.register_lakes(df)

      # Calculate annual energy yield
      annual_yield_df = simulation.get_annual_energy_yield()
      print(annual_yield_df)

3. **Documentation:**
   - Explore the detailed module documentation for more information on each class and method.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`




