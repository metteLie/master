from FPVsimulation.pvmodel import PVmodel, default_PVmodel_parameters
from FPVsimulation.soiling_loss_NS3031 import soiling_loss_NS3031_gdf
import pvlib
import requests
import pandas as pd
from shapely.geometry import Point


class PVsystem():
    """
    A class to represent a Photovoltaic (PV) system and simulate its performance.

    Attributes
    ----------
    latitude : float
        Latitude of the PV system.
    longitude : float
        Longitude of the PV system.
    system_area : float
        Area covered by the PV system in square kilometers.
    max_power_MW : float
        Maximum power output of the PV system in megawatts.
    raddatabase : str
        The radiation database used for simulation.

    Methods
    -------
    __get_tmy_profile_api():
        Retrieves Typical Meteorological Year (TMY) data from an online API.
    __get_G_POA_profile(PVparams=default_PVmodel_parameters, weather=None):
        Calculates the Plane of Array (POA) irradiance profile.
    __get_system_loss_soiling():
        Calculates the soiling loss for the system.
    __get_system_performance(PVparams=default_PVmodel_parameters, G_poa_df=None):
        Calculates the system performance metrics.
    __get_power_profiles(G_poa_df, perf_df, PVparams):
        Calculates the power output profiles.
    get_system_simulation_data(PVparams=default_PVmodel_parameters, weather=None):
        Simulates the system performance and returns the data.
    get_annual_energy_yield(PVparams=default_PVmodel_parameters, weather=None):
        Calculates the annual energy yield of the system.
    get_monthly_aggregates(PVparams=default_PVmodel_parameters, weather=None):
        Calculates the monthly aggregates of the system performance.
    """
    def __init__(self, latitude, longitude, system_area, max_power_MW):
        """
        Constructs all the necessary attributes for the PVsystem object.

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
        self.latitude = latitude
        self.longitude = longitude
        self.system_area = system_area
        self.max_power_MW = max_power_MW
        self.raddatabase = None
          
    def __get_tmy_profile_api(self):
        """
        Retrieves Typical Meteorological Year (TMY) data from an online API.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing TMY data with columns for weather parameters.
        """
        api_url = 'https://re.jrc.ec.europa.eu/api/v5_2/tmy?'

        params = {'lat': self.latitude,
                'lon': self.longitude, 
                'usehorizon': 1, 
                'raddatabase': 'PVGIS-SARAH2',
                'outputformat': 'json'}

        response = requests.get(api_url, params=params)
   
        if response.status_code == 200:
            tmy_df = pd.DataFrame(response.json()['outputs']['tmy_hourly'])
        else:
            params['raddatabase'] = 'PVGIS-ERA5'
            response = requests.get(api_url, params=params)
    
            assert response.status_code == 200, f"Error: {response.status_code}, {response.text}"
            tmy_df = pd.DataFrame(response.json()['outputs']['tmy_hourly'])

        self.raddatabase = params['raddatabase']  
        tmy_df['raddatabase'] = params['raddatabase']
        tmy_df['time(UTC)'] =  pd.to_datetime(tmy_df['time(UTC)'], format='%Y%m%d:%H%M')
        tmy_df = tmy_df.set_index('time(UTC)')

        
        return tmy_df

    def __get_G_POA_profile(self, PVparams=default_PVmodel_parameters, weather=None):        
        """
        Calculates the Plane of Array (POA) irradiance profile.

        Parameters
        ----------
        PVparams : dict, optional
            Parameters for the PV model (default is default_PVmodel_parameters).
        weather : pandas.DataFrame, optional
            DataFrame containing weather data (default is None).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing POA irradiance and weather parameters.
        """
        """
        source: https://pvsc-python-tutorials.github.io/PVSC48-Python-Tutorial/Tutorial%202%20-%20POA%20Irradiance.html
        """
        if weather is None: 
            # Get TMY weather data if no weather data is provided
            __weather = self.__get_tmy_profile_api().copy()
        else: 
            __weather = weather.copy()

        # Create a location object using latitude and longitude
        __location = pvlib.location.Location(latitude=self.latitude,
                                    longitude=self.longitude)
        __times = __weather.copy().index 
        # Get solar position data
        __solar_position = __location.get_solarposition(__times)
        
        
        if PVparams['tilt']==0:
            # Use GHI as POA when the tilt is zero
            __G_poa_df = pd.DataFrame({'poa_global_W/m2': __weather['G(h)']})
            __G_poa_df['aoi'] = __solar_position['zenith']
        else:
            # Calculate POA irradiance for tilted surfaces
            __G_poa_df = pvlib.irradiance.get_total_irradiance(
                    surface_tilt=PVparams['tilt'],  # tilted 20 degrees from horizontal
                    surface_azimuth=PVparams['azimuth'],  # facing South
                    dni=weather['Gb(n)'],
                    ghi=weather['G(h)'],
                    dhi=weather['Gd(h)'],
                    solar_zenith=__solar_position['apparent_zenith'],
                    solar_azimuth=__solar_position['azimuth'],
                    model='isotropic')
            __G_poa_df['aoi'] = pvlib.irradiance.aoi(
                    PVparams['tilt'],
                    PVparams['azimuth'],
                    __solar_position['apparent_zenith'],
                    __solar_position['azimuth']
                )
            
        __G_poa_df = pd.concat([__G_poa_df, __weather], axis=1)
        return __G_poa_df[['poa_global_W/m2', 'T2m', 'WS10m', 'aoi', 'raddatabase']]
    
    def __get_system_loss_soiling(self):
        """
        Calculates the soiling loss for the system based on location.

        Returns
        -------
        float
            Soiling loss percentage for the system.
        """
        # Create a Point object for the system center
        center = Point(self.longitude, self.latitude)
        soiling_loss_gdf = soiling_loss_NS3031_gdf.copy()

        # Calculate the distance between the system center and each municipality center for soiling loss
        soiling_loss_gdf['distance'] = soiling_loss_NS3031_gdf['geometry'].distance(center)

        # Get the soiling data belonging to the nearest municipality
        nearest_point = soiling_loss_gdf.loc[soiling_loss_gdf['distance'].idxmin()]

        return nearest_point['soiling']


    def __get_system_performance(self, PVparams=default_PVmodel_parameters, G_poa_df=None):
        """
        Calculates the system performance metrics.

        Parameters
        ----------
        PVparams : dict, optional
            Parameters for the PV model (default is default_PVmodel_parameters).
        G_poa_df : pandas.DataFrame, optional
            DataFrame containing POA irradiance and weather parameters (default is None).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing system performance metrics.
        """

        # Create a PV model with the provided parameters
        module = PVmodel(PVparams)
        # Get module performance metrics
        perf_df = module.get_module_performance(G_poa_df)
        # Calculate soiling losses
        monthly_soiling = self.__get_system_loss_soiling()
        perf_df['s_soiling'] = perf_df.index.month.map(lambda month: monthly_soiling[month-1])
        # Calculate overall system performance
        perf_df['syst_perf'] = (
            (perf_df['module_efficiency']/100)*
            (1-perf_df['s_soiling']/100)*
            PVparams['system_derate_factor']
            )
        return perf_df
    
    def __get_power_profiles(self, G_poa_df, perf_df, PVparams):
        """
        Calculates the power output profiles.

        Parameters
        ----------
        G_poa_df : pandas.DataFrame
            DataFrame containing POA irradiance and weather parameters.
        perf_df : pandas.DataFrame
            DataFrame containing system performance metrics.
        PVparams : dict
            Parameters for the PV model.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing power output profiles.
        """
        power_df = pd.DataFrame()
        # Calculate power output per square meter
        power_df['Power_out_W/m2'] = G_poa_df['poa_global_W/m2'] * perf_df['syst_perf']
        # Calculate total power output
        power_df['Power_out_W'] = power_df['Power_out_W/m2'] * self.system_area

        # Adjust power output if it exceeds the maximum power capacity
        if self.max_power_MW is not None:
            P_peak = max(power_df['Power_out_W'])
            if P_peak > self.max_power_MW * 10**6:
                self.system_area *= self.max_power_MW * 10**6 / P_peak
                power_df['Power_out_W'] *= self.max_power_MW * 10**6 / P_peak
        
        return power_df
        

    def get_system_simulation_data(self, PVparams=default_PVmodel_parameters, weather=None):
        """
        Simulates the FPV system and returns hourly data.

        Parameters
        ----------
        PVparams : dict, optional
            Parameters for the PV model (default is default_PVmodel_parameters).
        weather : pandas.DataFrame, optional
            DataFrame containing weather data (default is None).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing simulated system performance data with the following columns:
            - poa_global_W/m2: Plane of array irradiance in W/m^2.
            - T2m: Ambient temperature at 2 meters in degrees Celsius.
            - WS10m: Wind speed at 10 meters in m/s.
            - aoi: Angle of incidence in degrees.
            - temperature_eff: Temperature efficiency factor.
            - IAM: Incidence Angle Modifier.
            - T_module: Module temperature in degrees Celsius.
            - module_efficiency: Module efficiency in percentage.
            - s_soiling: Soiling loss factor in percentage.
            - syst_perf: System performance factor.
            - Power_out_W/m2: Power output per square meter in Watts.
            - Power_out_W: Total power output in Watts.
            - energy_yield_kWh: Energy yield in kilowatt-hours.
        """
        # Get POA irradiance profile
        G_poa_df = self.__get_G_POA_profile(PVparams, weather)
        # Get system performance metrics
        perf_df = self.__get_system_performance(PVparams, G_poa_df)
        # Get power output profiles
        power_df = self.__get_power_profiles(G_poa_df, perf_df, PVparams)
        simulated_data = pd.concat([G_poa_df, perf_df, power_df], axis=1)

        # Calculate energy yield
        simulated_data['energy_yield_kWh'] = simulated_data['Power_out_W']/1_000
        return simulated_data
    
    def get_annual_energy_yield(self,PVparams=default_PVmodel_parameters, weather=None):
        """
        Calculates the annual energy yield of the PV system.

        Parameters
        ----------
        PVparams : dict, optional
            Parameters for the PV model (default is default_PVmodel_parameters).
        weather : pandas.DataFrame, optional
            DataFrame containing weather data (default is None).

        Returns
        -------
        float
            Total annual energy yield in kilowatt-hours (kWh).
        """
        # Simulate the system performance and calculate the total annual energy yield
        simulated_data = self.get_system_simulation_data(PVparams, weather)
        return simulated_data['energy_yield_kWh'].sum()
    
    def get_montly_aggragates(self, PVparams=default_PVmodel_parameters, weather=None):
        """
        Calculates the monthly aggregates of the system energy yield.

        Parameters
        ----------
        PVparams : dict, optional
            Parameters for the PV model (default is default_PVmodel_parameters).
        weather : pandas.DataFrame, optional
            DataFrame containing weather data (default is None).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing monthly aggregates with the following columns:
            - ('energy_yield_kWh', 'sum'): Total energy yield in kilowatt-hours (kWh) for the month.
            - ('energy_yield_kWh', 'max'): Maximum daily energy yield in kilowatt-hours (kWh) for the month.
            - ('Power_out_W', 'max'): Maximum power output in Watts for the month.
            - ('Power_out_W', 'avg_Ppeak'): Average daily peak power output in Watts for the month.
        """
        if weather is None:
            weather = self.__get_G_POA_profile(PVparams=PVparams)
        
        # Get hourly simulation data
        hourly_df = self.get_system_simulation_data(weather=weather, PVparams=PVparams)

        # Calculate daily maximum power output
        daily_max_power = hourly_df['Power_out_W'].resample('D').max()

        # Aggregate monthly data for energy yield and power output
        monthly_df = hourly_df.groupby(hourly_df.index.month).agg({'energy_yield_kWh': ['sum', 'max'], 
                                                                   'Power_out_W': 'max'})
        monthly_df['Power_out_W', 'avg_Ppeak'] = daily_max_power.groupby(daily_max_power.index.month).mean()                                           
        return monthly_df.rename_axis('Month')
    
