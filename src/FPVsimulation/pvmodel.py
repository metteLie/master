import numpy as np
import pandas as pd 

default_PVmodel_parameters = {
    'tilt': 0,
    'azimuth': 180, 
    'eff_nom': 19,                      # Nominal efficiency of the PV module
    'beta': 0.003,                      # Temperature coefficient
    'U': 46,                            # Overall heat transfer coefficient
    'system_derate_factor': 0.837,      # System derate factor
    'b0': 0.05,                         # Incidence Angle Modifier (IAM) coefficient
    }



class PVmodel():
    """
    A class to represent a Photovoltaic (PV) model and simulate its performance.

    Attributes
    ----------
    params : dict
        Parameters for the PV model.
    
    Methods
    -------
    __get_cell_temperature_profile(gpoa_df):
        Calculates the cell temperature profile based on given weather data.
    __get_IAM_profile(G_poa_df):
        Calculates the Incidence Angle Modifier (IAM) profile based on given data.
    get_module_performance(G_poa_df):
        Calculates the module performance metrics based on given data.
    """


    def __init__(self, parameters):
        """
        Constructs all the necessary attributes for the PVmodel object.

        Parameters
        ----------
        parameters : dict
            Parameters for the PV model.
        """

        self.params = parameters

    def set_parameters(self, params):
        """
        Update the default parameters.

        Default parameters
        ------------------
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
            self.params[param] = value

    def __get_cell_temperature_profile(self, gpoa_df):
        """
        Calculates the cell temperature profile based on given weather data.

        Parameters
        ----------
        gpoa_df : pandas.DataFrame
            DataFrame containing weather data, with columns 'T2m' (ambient temperature) and 
            'poa_global_W/m2' (plane of array irradiance in W/m^2).

        Returns
        -------
        pandas.Series
            Series containing the cell temperature for each time step.
        """

        # Calculate cell temperature using ambient temperature and irradiance
        return gpoa_df['T2m'] + gpoa_df['poa_global_W/m2'] / self.params['U']
       
    def __get_IAM_profile(self, G_poa_df):
        """
        Calculates the Incidence Angle Modifier (IAM) profile based on given data.

        Parameters
        ----------
        G_poa_df : pandas.DataFrame
            DataFrame containing angle of incidence (AOI) data in degrees.

        Returns
        -------
        numpy.ndarray
            Array containing the IAM for each time step, clipped to a minimum of 0.
        """
        aoi_rad = G_poa_df['aoi']*np.pi/180
        IAM = np.where(G_poa_df['aoi'] < 90, 1 - self.params['b0'] * (1 / np.cos(aoi_rad) - 1), 0)
        return IAM.clip(min=0)
    
    def get_module_performance(self, G_poa_df): 
        """
        Calculates the module performance metrics based on given data.

        Parameters
        ----------
        G_poa_df : pandas.DataFrame
            DataFrame containing weather and irradiance data, with columns 'T2m' (ambient temperature), 
            'poa_global_W/m2' (plane of array irradiance in W/m^2), and 'aoi' (angle of incidence in degrees).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the temperature efficiency, IAM, module temperature, and module efficiency for each time step.
        """
        T_STC = 25
        T_module = self.__get_cell_temperature_profile(G_poa_df)
        temperature_eff = 1 - self.params['beta']*(T_module - T_STC)
        IAM = self.__get_IAM_profile(G_poa_df)
        module_efficiency = (self.params['eff_nom']* IAM * temperature_eff )
        return pd.DataFrame({'temperature_eff': module_efficiency,
                             'IAM': IAM, 'T_module': T_module,
                             'module_efficiency': module_efficiency })


