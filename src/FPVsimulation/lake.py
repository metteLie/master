from FPVsimulation.pvsystem import PVsystem
import numpy as np

class Lake():
    """
    A class used to represent a Lake with an array of PV systems.

    Attributes
    ----------
    lake_id : str
        Identifier for the lake.
    lake_area : float
        Area of the lake in square kilometers.
    systems : list
        List of PV systems installed on the lake.
    covered_area : float
        Total area covered by the PV systems on the lake.

    Methods
    -------
    __str__():
        Returns a string representation of the lake details.
    __repr__():
        Returns a formal string representation of the Lake instance.
    register_pvsystem(latitude, longitude, system_area, max_power_MW):
        Registers a new PV system on the lake.
    get_annual_energy_yield(PVparams):
        Calculates the annual energy yield for all PV systems on the lake.
    """
    def __init__(self, lake_id, lake_area):
        """
        Constructs all the necessary attributes for the Lake object.

        Parameters
        ----------
        lake_id : str
            Identifier for the lake.
        lake_area : float
            Area of the lake in square kilometers.
        """
        self.lake_id = lake_id
        self.lake_area = lake_area
        self.systems = []
        self.covered_area = 0
    
    def __str__(self):
        """
        Constructs all the necessary attributes for the Lake object.

        Parameters
        ----------
        lake_id : str
            Identifier for the lake.
        lake_area : float
            Area of the lake in square kilometers.
        """
        return f"""
        Lake {self.lake_id} 
        - Area: {self.lake_area} km2, 
        - Number of systems: {len(self.systems)}, 
        - Covered Area: {round(self.covered_area/self.lake_area*100, 2)}%"""

    def __repr__(self):
        """
        Returns a formal string representation of the Lake instance.

        Returns
        -------
        str
            String representation of the Lake instance with lake_id and lake_area.
        """
        return f"Lake(lake_id={self.lake_id}, lake_area={self.lake_area})"

    def register_pvsystem(self, latitude, longitude, system_area, max_power_MW):
        """
        Registers a new PV system on the lake.

        Parameters
        ----------
        latitude : float
            Latitude of the PV system.
        longitude : float
            Longitude of the PV system.
        system_area : float
            Area covered by the PV system in square kilometers.
        max_power_MW : float
            Maximum power output of the PV system in megawatts.
        """
        system_area = system_area
        pv_system = PVsystem(latitude, longitude, system_area, max_power_MW)
        self.systems.append(pv_system)
        self.covered_area+=system_area
    
    def get_annual_energy_yield(self, PVparams):
        """
        Calculates the annual energy yield for all PV systems on the lake.

        Parameters
        ----------
        PVparams : dict
            Dictionary containing parameters for PV system performance calculation.

        Returns
        -------
        list
            List of dictionaries containing lake_id, lake_area, system_area, latitude, longitude, 
            annual energy yield, and radiation data for each PV system.
        """
        data = []
        for system in self.systems:
            system_data = {
                'lake_id': self.lake_id,
                'lake_area': self.lake_area,
                'system_area': system.system_area,
                'latitude': system.latitude,
                'longitude': system.longitude, 
                'annual_energy_yield_kWh': system.get_annual_energy_yield(PVparams),
                'raddata': system.raddatabase
            }
            data.append(system_data)
        return data


