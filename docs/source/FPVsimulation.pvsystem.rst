FPVsimulation.pvsystem module
=============================


This module defines the `PVsystem` class, which represents a photovoltaic (PV) system and simulates its performance.

Classes
-------

.. autoclass:: FPVsimulation.pvsystem.PVsystem
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__

Example Usage
-------------

.. code-block:: python

    from pvsystem import PVsystem

    # Create a new PV system
    my_pvsystem = PVsystem(latitude=60.0, longitude=5.0, system_area=1.5, max_power_MW=2.0)

    # Get annual energy yield
    annual_yield = my_pvsystem.get_annual_energy_yield()


