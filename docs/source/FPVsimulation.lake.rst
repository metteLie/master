.. _lake:

FPVsimulation.lake module
=========================

This module defines the `Lake` class used to represent a lake with an array of photovoltaic (PV) systems.

Classes
-------

.. autoclass:: FPVsimulation.lake.Lake
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__, __str__, __repr__

Example Usage
-------------

.. code-block:: python

    from lake import Lake

    # Create a new lake
    my_lake = Lake(lake_id='Lake123', lake_area=50)

    # Register a PV system
    my_lake.register_pvsystem(latitude=60.0, longitude=5.0, system_area=1.5, max_power_MW=2.0)

    # Calculate annual energy yield
    energy_yield = my_lake.get_annual_energy_yield(PVparams)