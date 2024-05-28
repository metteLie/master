from FPVsimulation.pvmodel import default_PVmodel_parameters
from FPVsimulation.lake import Lake
from copy import deepcopy
import pandas as pd


class FPVsimulation():
    """
    A class to simulate Floating Photovoltaic (FPV) systems on lakes.

    Attributes
    ----------
    lakes : dict
        Dictionary to store Lake objects, keyed by lake ID.
    PVmodel_parameters : dict
        Dictionary to store parameters for the PV model, initialized with default values.

    Methods
    -------
    set_PVmodel_parameters(params)
        Update the default parameters for the PV model.
    register_lakes(dataframe)
        Register lakes from a given dataframe.
    get_annual_energy_yield()
        Calculate the annual energy yield for all registered lakes.
    """
    def __init__(self):
        """
        Initialize the FPVsimulation class.

        Attributes
        ----------
        lakes : dict
            Dictionary to store Lake objects, keyed by lake ID.
        PVmodel_parameters : dict
            Dictionary to store parameters for the PV model, initialized with default values.
        """
        self.lakes={}
        self.PVmodel_parameters = deepcopy(default_PVmodel_parameters)
    
    def set_PVmodel_parameters(self, params):
        """
        Update the default parameters for the PV model.

        Parameters
        ----------
        params : dict
            Dictionary containing parameters to update. Possible keys include:
            - 'eff_nom': float, Nominal efficiency of the PV module [%]
            - 'tau': float, Transmittance coefficient
            - 'alpha': float, Absorption coefficient
            - 'U': float, Heat transfer constant
            - 'beta': float, Temperature coefficient [/K]
            - 'system_derate_factor': float, System derate factor
        """
        for param, value in params.items():
            self.PVmodel_parameters[param] = value
            
    def register_lakes(self, dataframe):
        """
        Register lakes from a given dataframe.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame containing lake information with the following columns:
            - 'lake_id': int or str, Unique identifier for the lake
            - 'lake_area': float, Area of the lake
            - 'latitude': float, Latitude of the lake
            - 'longitude': float, Longitude of the lake
            - 'selected_area': float, Area selected for the PV system
            - 'max_power_MW': float, Maximum power output of the PV system [MW]
        """
        for index, row in dataframe.iterrows():
            lake_id = str(row['lake_id'])
            lake_area = row['lake_area']
            
            if lake_id not in self.lakes:
                self.lakes[lake_id] = Lake(lake_id, lake_area)
            
            lake = self.lakes[lake_id]
            
            latitude = row['latitude']
            longitude = row['longitude']
            system_area = row['selected_area']
            max_power_MW = row['max_power_MW']
            
            lake.register_pvsystem(latitude, longitude, system_area, max_power_MW)
    
    def get_annual_energy_yield(self):
        """
        Calculate the annual energy yield for all systems in registered lakes.

        Returns
        -------
        pd.DataFrame
            DataFrame containing annual energy yield data for each PV system on the lakes.
        """
        # Initialize an empty list to store data for each lake
        data = []

        for i, lake in enumerate(self.lakes.values()):
            print(f'lake {i} of {len(self.lakes)}')
            data+=lake.get_annual_energy_yield(self.PVmodel_parameters)

        # Create a DataFrame from the list of dictionaries
        result_df = pd.DataFrame(data)

        # Print or return the DataFrame
        return result_df
