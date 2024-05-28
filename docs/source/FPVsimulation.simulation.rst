FPVsimulation.simulation module
===============================


This module defines the `FPVsimulation` class to simulate Floating Photovoltaic (FPV) systems on multiple lakes.

Classes
-------

.. autoclass:: FPVsimulation.simulation.FPVsimulation
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__

Example Usage
-------------

.. code-block:: python

    from simulation import FPVsimulation
    import pandas as pd

    # Initialize simulation
    simulation = FPVsimulation()

    # Register lakes from a dataframe
    df = pd.DataFrame({
        'lake_id': ['Lake1', 'Lake2'],
        'lake_area': [50, 70],
        'latitude': [60.0, 62.0],
        'longitude': [5.0, 7.0],
        'selected_area': [105, 200], # m^2
        'max_power_MW': [2.0, 3.0]
    })
    simulation.register_lakes(df)

    # Calculate annual energy yield
    annual_yield_df = simulation.get_annual_energy_yield()

