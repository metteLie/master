FPVsimulation.pvmodel module
============================

This module defines the `PVmodel` class, which simulates the performance of a photovoltaic (PV) system.

Classes
-------

.. autoclass:: FPVsimulation.pvsystem.PVmodel
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__

Default Parameters
------------------

.. csv-table:: **Default PV model parameters**
   :header: "Parameter", "Value", "Unit", "description"
   :widths: 15, 5, 5, 50

   "tilt", 0, "deg", "The angle between the surface normal and panel normal"
   "azimuth", 180, "deg", "Anlge facing north, south is 180"
   "eff_nom", 19, "%", "Nominal efficiency of the PV module"
   "beta", 0.003, ":math:`K^{-1}`", "Temperature coefficient"
   "U", 46, ":math:`W/m^2K`", "Overall heat transfer coefficient"
   "system_derate_factor", 0.837, "\-", "System derate factor"
   "b0", 0.05, "\-", "Incidence Angle Modifier (IAM) coefficient"

Example Usage
-------------

.. code-block:: python

    from pvmodel import PVmodel, default_PVmodel_parameters

    # Create a PV model
    pv_model = PVmodel(parameters=default_PVmodel_parameters)

    # Get module performance
    performance = pv_model.get_module_performance(G_poa_df)