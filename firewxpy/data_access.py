'''
This file hosts all the functions used for data access. 
These functions request data from the various data sources.
Depending on the data source, the data will be downloaded either from an FTP server or an OPENDAP server. 
 - National Weather Service Forecast Data is downloaded from the National Weather Service FTP server. 
 - Real Time Mesoscale Analysis is downloaded from OPENDAP servers: 1) UCAR THREDDS Server or 2) NCEP NOMADS Server

 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS


'''

##### IMPORTS NEEDED PYTHON MODULES #######
import xarray as xr
import metpy
import metpy.calc as mpcalc
import firewxpy.parsers as parsers
import pandas as pd
import cartopy.crs as ccrs
import requests
import firewxpy.calc as calc
import firewxpy.raws_sigs as raws
import numpy as np
import netCDF4
import time as t
import urllib.request
import os
import sys
import logging
import firewxpy.standard as standard
import warnings
warnings.filterwarnings('ignore')

from siphon.catalog import TDSCatalog
from metpy.cbook import get_test_data
from io import StringIO
from metpy.io import parse_metar_file
from metpy.units import units, pandas_dataframe_to_unit_arrays
from dateutil import tz
from firewxpy.settings import coords_for_forecast_model_data

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta


def station_coords(station_id):

    r'''
    This function returns the latitude and lonigitude coordinates for any airport. 

    Required Arguments:

    1) station_id (String) - The ID for the ASOS station. 

    Returns: The latitude/longitude coordinates of the ASOS station in decimal degrees.

    '''

    station_id = station_id.upper()
    
    # Pings server for airport data
    df = pd.read_csv(get_test_data('airport-codes.csv'))
    
    # Queries our airport types (airport sizes)
    df = df[(df['type'] == 'large_airport') | (df['type'] == 'medium_airport') | (df['type'] == 'small_airport')]

    df = df[df['ident'] == station_id]

    longitude = df['longitude_deg']
    latitude = df['latitude_deg']

    longitude = longitude.iloc[0]
    latitude = latitude.iloc[0]
    
    return longitude, latitude   

class model_data:

    r'''
    This class hosts the functions that return forecast model data from various different sources. 
    
    '''

    def get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound):

        r'''
        This function retrieves the latest forecast model data from NCEP/NOMADS OPENDAP. 

        Required Arguments:

        1) model (String) - The forecast model that is being used. 

        2) region (String) - The abbreviation for the region used. 

        3) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        4) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        5) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere. 

        6) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere.

        Optional Arguments: None

        Returns: An xarray.data_array of the forecast model data. 

        '''

        local_time, utc_time = standard.plot_creation_time()
        yesterday = utc_time - timedelta(hours=24)

        western_bound, eastern_bound, southern_bound, northern_bound = coords_for_forecast_model_data(region, western_bound, eastern_bound, southern_bound, northern_bound)

        if model == 'GFS0p25':
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_18z'

        if model == 'GFS0p25_1h':

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_18z'            
        

        if model == 'GFS0p50':

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_18z' 

        if model == 'GFS1p00':

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_18z' 

        if model == 'GEFS0p50':
            
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_00z_pgrb2a'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_06z_pgrb2a'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_12z_pgrb2a'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_18z_pgrb2a'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_00z_pgrb2a'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_06z_pgrb2a'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_12z_pgrb2a'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_18z_pgrb2a'

        if model == 'GEFS0p50_all':
            
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_18z'

        if model == 'CMCENS':

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+utc_time.strftime('%Y%m%d')+'/cmcensavg_00z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+utc_time.strftime('%Y%m%d')+'/cmcensavg_12z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+yesterday.strftime('%Y%m%d')+'/cmcensavg_00z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+yesterday.strftime('%Y%m%d')+'/cmcensavg_12z'      
        if model == 'NAM':
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_18z' 

        if model == 'NA NAM':
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_18z'   

        if model == 'NAM 1hr':
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_18z' 

        if model == 'NAM 1hr' or model == 'NAM':
            
            western_bound = western_bound * -1
            eastern_bound = eastern_bound * -1
            if utc_time.hour >= 0 and utc_time.hour < 6:
                
                try:
                    ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("00z run downloaded successfully!")
                except Exception as e:
                    print("00z run not available yet. Now trying the 18z run from yesterday.")
                    try:
                        ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("18z run downloaded successfully!")
                    except Exception as e:
                        print("18z run from yesterday is not available. Now trying the 12z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("12z run downloaded successfully!")
                        except Exception as e:
                            print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("06z run downloaded successfully!")    
                            except Exception as e:
                                print("06z run from yesterday is not available. Now trying the 00z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_00z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("00z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 6 and utc_time.hour < 12:
                
                try:
                    ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("06z run downloaded successfully!")
                except Exception as e:
                    print("06z run not available yet. Now trying the 00z run.")
                    try:
                        ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("00z run downloaded successfully!")
                    except Exception as e:
                        print("00z run from yesterday is not available. Now trying the 18z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("18z run downloaded successfully!")
                        except Exception as e:
                            print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("12z run downloaded successfully!")    
                            except Exception as e:
                                print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("06z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 12 and utc_time.hour < 18:
                
                try:
                    ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("12z run downloaded successfully!")
                except Exception as e:
                    print("12z run not available yet. Now trying the 06z run.")
                    try:
                        ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("06z run downloaded successfully!")
                    except Exception as e:
                        print("06z run from yesterday is not available. Now trying the 00z run.")
                        try:
                            ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("00z run downloaded successfully!")
                        except Exception as e:
                            print("00z run is not available. Now trying the 18z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("18z run downloaded successfully!")    
                            except Exception as e:
                                print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("12z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")

            
            if utc_time.hour >= 18 and utc_time.hour < 24:
                
                try:
                    ds = xr.open_dataset(url_18z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("18z run downloaded successfully!")
                except Exception as e:
                    print("18z run not available yet. Now trying the 12z run.")
                    try:
                        ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("12z run downloaded successfully!")
                    except Exception as e:
                        print("12z run from yesterday is not available. Now trying the 06z run.")
                        try:
                            ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("06z run downloaded successfully!")
                        except Exception as e:
                            print("06z run is not available. Now trying the 00z run.")
                            try:
                                ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("00z run downloaded successfully!")    
                            except Exception as e:
                                print("00z run is not available. Now trying the 18z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("18z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")

            
        else:

            western_bound = western_bound
            eastern_bound = eastern_bound
        
            if utc_time.hour >= 0 and utc_time.hour < 6:
                
                try:
                    ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("00z run downloaded successfully!")
                except Exception as e:
                    print("00z run not available yet. Now trying the 18z run from yesterday.")
                    try:
                        ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("18z run downloaded successfully!")
                    except Exception as e:
                        print("18z run from yesterday is not available. Now trying the 12z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("12z run downloaded successfully!")
                        except Exception as e:
                            print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("06z run downloaded successfully!")    
                            except Exception as e:
                                print("06z run from yesterday is not available. Now trying the 00z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_00z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("00z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
                    
            
            if utc_time.hour >= 6 and utc_time.hour < 12:
                
                try:
                    ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("06z run downloaded successfully!")
                except Exception as e:
                    print("06z run not available yet. Now trying the 00z run.")
                    try:
                        ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("00z run downloaded successfully!")
                    except Exception as e:
                        print("00z run from yesterday is not available. Now trying the 18z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("18z run downloaded successfully!")
                        except Exception as e:
                            print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("12z run downloaded successfully!")    
                            except Exception as e:
                                print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("06z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 12 and utc_time.hour < 18:
                
                try:
                    ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("12z run downloaded successfully!")
                except Exception as e:
                    print("12z run not available yet. Now trying the 06z run.")
                    try:
                        ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("06z run downloaded successfully!")
                    except Exception as e:
                        print("06z run from yesterday is not available. Now trying the 00z run.")
                        try:
                            ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("00z run downloaded successfully!")
                        except Exception as e:
                            print("00z run is not available. Now trying the 18z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("18z run downloaded successfully!")    
                            except Exception as e:
                                print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("12z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 18 and utc_time.hour < 24:
                
                try:
                    ds = xr.open_dataset(url_18z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print("18z run downloaded successfully!")
                except Exception as e:
                    print("18z run not available yet. Now trying the 12z run.")
                    try:
                        ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print("12z run downloaded successfully!")
                    except Exception as e:
                        print("12z run from yesterday is not available. Now trying the 06z run.")
                        try:
                            ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print("06z run downloaded successfully!")
                        except Exception as e:
                            print("06z run is not available. Now trying the 00z run.")
                            try:
                                ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print("00z run downloaded successfully!")    
                            except Exception as e:
                                print("00z run is not available. Now trying the 18z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                    print("18z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")


                    

        ds = ds.metpy.parse_cf()
        
        return ds

    def get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude):

        r'''
        This function downloads and retrieves the latest data for the Rapid Refresh Model from the 
        NCEP/NOMADS OPENDAP server. 

        Required Arguments:

        1) model (String) - The forecast model that is being used. 
           Choices 1) RAP 2) RAP 32 (32km Full North America)

        2) station_id (String) - The ID for the ASOS station. If the user wishes to pick a custom point
           that is not an ASOS location, enter 'Custom' or 'custom' for the station_id. 

        3) longitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
           enter the longitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
           place. 

        4) latitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
           enter the latitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
           place. 

        Optional Arguments: None

        Returns: An xarray.data_array of the Rapid Refresh Model for the closest grid point to the specified location. 
        
        '''
    
        local_time, utc_time = standard.plot_creation_time()
        yesterday = utc_time - timedelta(hours=24)
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude, latitude = station_coords(station_id)
    
        hours = []
        for i in range(0, 5, 1):
            hour = utc_time.hour - i
            hours.append(hour)
    
        if model == 'RAP' or model == 'rap':

            url_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[0]}z"
            url_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[1]}z"
            url_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[2]}z"
            url_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[3]}z"
            url_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[4]}z"

            url_5 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[0]}z"
            url_6 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[1]}z"
            url_7 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[2]}z"
            url_8 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[3]}z"
            url_9 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[4]}z"
    
            y_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_19z"
            y_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_20z"
            y_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_21z"
            y_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_22z"
            y_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_23z"

        if model == 'RAP 32' or model == 'rap 32':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
            latitude = latitude
            longitude = 360 - longitude

            url_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[0]}z"
            url_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[1]}z"
            url_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[2]}z"
            url_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[3]}z"
            url_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[4]}z"

            url_5 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[0]}z"
            url_6 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[1]}z"
            url_7 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[2]}z"
            url_8 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[3]}z"
            url_9 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[4]}z"
            
            y_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_19z"
            y_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_20z"
            y_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_21z"
            y_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_22z"
            y_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_23z"


        if utc_time.hour >= 14 and utc_time.hour < 24:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            ds = xr.open_dataset(url_3, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                ds = xr.open_dataset(url_4, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")
        

        if utc_time.hour == 13:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            ds = xr.open_dataset(url_3, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")

        if utc_time.hour == 12:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")

        if utc_time.hour == 11:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")
        

        if utc_time.hour == 10:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")


        
        if utc_time.hour >= 4 and utc_time.hour < 10:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")

        if utc_time.hour == 3:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {hours[1]}z RAP.")
                try:
                    ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]}z RAP is unavailable. Trying to retrieve the {hours[2]}z RAP.")
                    try:
                        ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]} RAP.")   
                    except Exception as e:
                        print(f"{hours[2]}z RAP is unavailable. Trying to retrieve the {hours[3]}z RAP.")
                        try:
                            ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {hours[3]} RAP.")     
                        except Exception as e:
                            print(f"{hours[3]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 23z RAP.")
                            try:
                                ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")      


        if utc_time.hour == 2:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]}z RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 23z RAP.")
                        try:
                            ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.")     
                        except Exception as e:
                            print(f"{yesterday.strftime('%Y%m%d')} 23z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                            try:
                                ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 22z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")   

        if utc_time.hour == 1:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]} RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {hours[1]}z RAP.")
                try:
                    ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 23z RAP.")
                    try:
                        ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.")   
                    except Exception as e:
                        print(f"{yesterday.strftime('%Y%m%d')} 23z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                        try:
                            ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 22z RAP.")     
                        except Exception as e:
                            print(f"{yesterday.strftime('%Y%m%d')} 22z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                            try:
                                ds = xr.open_dataset(y_2, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 21z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")   

        if utc_time.hour == 0:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                print(f"Successfully retrieved the {hours[0]} RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} RAP.")
                try:
                    ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                    print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.")                    
                except Exception as e:
                    print(f"{yesterday.strftime('%Y%m%d')} 23z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                    try:
                        ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                        print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 22z RAP.")   
                    except Exception as e:
                        print(f"{yesterday.strftime('%Y%m%d')} 22z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 21z RAP.")
                        try:
                            ds = xr.open_dataset(y_2, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                            print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 21z RAP.")     
                        except Exception as e:
                            print(f"{yesterday.strftime('%Y%m%d')} 21z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 20z RAP.")
                            try:
                                ds = xr.open_dataset(y_1, engine='netcdf4',).sel(lon=longitude, lat=latitude, method='nearest')
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 20z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")   
    
    
        ds = ds.metpy.parse_cf()
        
        return ds


    def get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound, two_point_cross_section=False):

        r'''
        This function retrieves the latest dataset for the hourly RAP model from the NOAA/NCEP/NOMADS server. 

        1) model (String) - The forecast model that is being used. 
           Choices 1) RAP 2) RAP 32 (32km Full North America)

        2) region (String) - The abbreviation for the region used. 

        3) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        4) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Negative values denote the western hemisphere and positive 
           values denote the eastern hemisphere. 

        5) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere. 

        6) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
           The default setting is None. If set to None, the user must select a state or gacc_region. 
           This setting should be changed from None to an integer or float value if the user wishes to
           have a custom area selected. Positive values denote the northern hemisphere and negative 
           values denote the southern hemisphere.

        Optional Arguments: 

        1) two_point_cross_section (Boolean) - Default = False. When downloading the data and intending to make a cross-section 
           between two points, set two_point_cross_section=True. 

        Returns: An xarray.data_array of the forecast model data. 

        '''
    
        local_time, utc_time = standard.plot_creation_time()
        yesterday = utc_time - timedelta(hours=24)

        if region == 'Custom' or region == 'custom' and two_point_cross_section == True:
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1                    
    
        western_bound, eastern_bound, southern_bound, northern_bound = coords_for_forecast_model_data(region, western_bound, eastern_bound, southern_bound, northern_bound)
        
        hours = []
        for i in range(0, 5, 1):
            hour = utc_time.hour - i
            hours.append(hour)


        if model == 'RAP' or model == 'rap':

            western_bound = western_bound * -1
            eastern_bound = eastern_bound * -1

            url_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[0]}z"
            url_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[1]}z"
            url_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[2]}z"
            url_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[3]}z"
            url_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_{hours[4]}z"

            url_5 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[0]}z"
            url_6 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[1]}z"
            url_7 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[2]}z"
            url_8 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[3]}z"
            url_9 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap_0{hours[4]}z"
    
            y_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_19z"
            y_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_20z"
            y_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_21z"
            y_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_22z"
            y_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap_23z"

        if model == 'RAP 32' or model == 'rap 32':


            url_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[0]}z"
            url_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[1]}z"
            url_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[2]}z"
            url_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[3]}z"
            url_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_{hours[4]}z"

            url_5 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[0]}z"
            url_6 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[1]}z"
            url_7 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[2]}z"
            url_8 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[3]}z"
            url_9 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{utc_time.strftime('%Y%m%d')}/rap32_0{hours[4]}z"
            
            y_0 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_19z"
            y_1 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_20z"
            y_2 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_21z"
            y_3 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_22z"
            y_4 = f"http://nomads.ncep.noaa.gov:80/dods/rap/rap{yesterday.strftime('%Y%m%d')}/rap32_23z"


        if utc_time.hour >= 14 and utc_time.hour < 24:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_4, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_4, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")   
            
        
        if utc_time.hour == 13:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_4, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_4, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")        
        
        if utc_time.hour == 12:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_2, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")

        
        if utc_time.hour == 11:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_1, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")
        
        if utc_time.hour == 10:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_0, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")
                                

        if utc_time.hour >= 4 and utc_time.hour < 10:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]} RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]} RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]} RAP is unavailable. Trying to retrieve the {hours[3]} RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]}z RAP.")     
                        except Exception as e:
                            print(f"{hours[3]} RAP is unavailable. Trying to retrieve the {hours[4]} RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(url_9, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {hours[4]}z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")

        if utc_time.hour == 3:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {hours[1]}z RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]}z RAP is unavailable. Trying to retrieve the {hours[2]}z RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]} RAP.")   
                    except Exception as e:
                        print(f"{hours[2]}z RAP is unavailable. Trying to retrieve the {hours[3]}z RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(url_8, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {hours[3]} RAP.")     
                        except Exception as e:
                            print(f"{hours[3]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 23z RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")      


        if utc_time.hour == 2:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]}z RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {hours[1]} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]}z RAP is unavailable. Trying to retrieve the {hours[2]} RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(url_7, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {hours[2]}z RAP.")   
                    except Exception as e:
                        print(f"{hours[2]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 23z RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.")     
                        except Exception as e:
                            print(f"{yesterday.strftime('%Y%m%d')} 23z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 22z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")   

        if utc_time.hour == 1:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]} RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {hours[1]}z RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(url_6, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {hours[1]}z RAP.")                    
                except Exception as e:
                    print(f"{hours[1]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 23z RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.")   
                    except Exception as e:
                        print(f"{yesterday.strftime('%Y%m%d')} 23z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 22z RAP.")     
                        except Exception as e:
                            print(f"{yesterday.strftime('%Y%m%d')} 22z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(y_2, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(y_2, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 21z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")   

        if utc_time.hour == 0:
            try:
                print(f"Trying to retrieve the {hours[0]}z RAP.")
                if model == 'RAP 32' or model == 'rap 32':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                if model == 'RAP' or model == 'rap':
                    ds = xr.open_dataset(url_5, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                print(f"Successfully retrieved the {hours[0]} RAP.")
            except Exception as e:
                print(f"{hours[0]}z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} RAP.")
                try:
                    if model == 'RAP 32' or model == 'rap 32':
                        ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    if model == 'RAP' or model == 'rap':
                        ds = xr.open_dataset(y_4, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                    print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 23z RAP.")                    
                except Exception as e:
                    print(f"{yesterday.strftime('%Y%m%d')} 23z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 22z RAP.")
                    try:
                        if model == 'RAP 32' or model == 'rap 32':
                            ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        if model == 'RAP' or model == 'rap':
                            ds = xr.open_dataset(y_3, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                        print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 22z RAP.")   
                    except Exception as e:
                        print(f"{yesterday.strftime('%Y%m%d')} 22z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 21z RAP.")
                        try:
                            if model == 'RAP 32' or model == 'rap 32':
                                ds = xr.open_dataset(y_2, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            if model == 'RAP' or model == 'rap':
                                ds = xr.open_dataset(y_2, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                            print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 21z RAP.")     
                        except Exception as e:
                            print(f"{yesterday.strftime('%Y%m%d')} 21z RAP is unavailable. Trying to retrieve the {yesterday.strftime('%Y%m%d')} 20z RAP.")
                            try:
                                if model == 'RAP 32' or model == 'rap 32':
                                    ds = xr.open_dataset(y_1, engine='netcdf4',).sel(lon=slice(360-western_bound, 360-eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                if model == 'RAP' or model == 'rap':
                                    ds = xr.open_dataset(y_1, engine='netcdf4',).sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))
                                print(f"Successfully retrieved the {yesterday.strftime('%Y%m%d')} 20z RAP.") 
                            except Exception as e:
                                print(f"Latest available RAP data is over 4 hours old. Aborting...")  
    
    
        ds = ds.metpy.parse_cf()
        
        return ds

    def get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude):

        r'''
        This function downloads and retrieves the latest data for the forecast model data from the 
        NCEP/NOMADS OPENDAP server. 

        Required Arguments:

        1) model (String) - The forecast model that is being used. 

        2) station_id (String) - The ID for the ASOS station. If the user wishes to pick a custom point
           that is not an ASOS location, enter 'Custom' or 'custom' for the station_id. 

        3) longitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
           enter the longitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
           place. 

        4) latitude (Integer or Float) - If the user is entering a custom location that is not an ASOS station location,
           enter the latitude value in this place in decimal degrees. If using an ASOS station location, enter None in this
           place. 

        Optional Arguments: None

        Returns: An xarray.data_array of the forecast model data for the closest grid point to the specified location. 
        
        '''

        local_time, utc_time = standard.plot_creation_time()
        yesterday = utc_time - timedelta(hours=24)

        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude, latitude = station_coords(station_id)

        if model == 'GFS0p25':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_18z'

        if model == 'GFS0p25_1h':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p25_1hr_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p25_1hr_18z'            
        

        if model == 'GFS0p50':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_0p50_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p50/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_0p50_18z' 

        if model == 'GFS1p00':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+utc_time.strftime('%Y%m%d')+'/gfs_1p00_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gfs_1p00/gfs'+yesterday.strftime('%Y%m%d')+'/gfs_1p00_18z' 

        if model == 'GEFS0p50':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude
            
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_00z_pgrb2a'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_06z_pgrb2a'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_12z_pgrb2a'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gec00_18z_pgrb2a'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_00z_pgrb2a'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_06z_pgrb2a'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_12z_pgrb2a'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gec00_18z_pgrb2a'

        if model == 'GEFS0p50_all':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude
            
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+utc_time.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs'+yesterday.strftime('%Y%m%d')+'/gefs_pgrb2ap5_all_18z'

        if model == 'CMCENS':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude

            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+utc_time.strftime('%Y%m%d')+'/cmcensavg_00z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+utc_time.strftime('%Y%m%d')+'/cmcensavg_12z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+yesterday.strftime('%Y%m%d')+'/cmcensavg_00z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/cmcens/cmcens'+yesterday.strftime('%Y%m%d')+'/cmcensavg_12z' 
            
        if model == 'NAM':
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_18z' 

        if model == 'NA NAM':

            if longitude < 0:
                longitude = longitude * -1
            else:
                longitude = longitude
    
            latitude = latitude
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam_na_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam_na_18z'   

        if model == 'NAM 1hr':
        
            url_00z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_00z'
            url_06z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_06z'
            url_12z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_12z'
            url_18z_run = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+utc_time.strftime('%Y%m%d')+'/nam1hr_18z'
            
            yday_00z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_00z'
            yday_06z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_06z'
            yday_12z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_12z'
            yday_18z = 'http://nomads.ncep.noaa.gov:80/dods/nam/nam'+yesterday.strftime('%Y%m%d')+'/nam1hr_18z' 

        if model == 'NAM 1hr' or model == 'NAM':
            
            if utc_time.hour >= 0 and utc_time.hour < 6:
                
                try:
                    ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("00z run downloaded successfully!")
                except Exception as e:
                    print("00z run not available yet. Now trying the 18z run from yesterday.")
                    try:
                        ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("18z run downloaded successfully!")
                    except Exception as e:
                        print("18z run from yesterday is not available. Now trying the 12z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("12z run downloaded successfully!")
                        except Exception as e:
                            print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("06z run downloaded successfully!")    
                            except Exception as e:
                                print("06z run from yesterday is not available. Now trying the 00z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_00z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("00z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
                   
            
            if utc_time.hour >= 6 and utc_time.hour < 12:
                
                try:
                    ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("06z run downloaded successfully!")
                except Exception as e:
                    print("06z run not available yet. Now trying the 00z run.")
                    try:
                        ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("00z run downloaded successfully!")
                    except Exception as e:
                        print("00z run from yesterday is not available. Now trying the 18z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("18z run downloaded successfully!")
                        except Exception as e:
                            print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("12z run downloaded successfully!")    
                            except Exception as e:
                                print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("06z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 12 and utc_time.hour < 18:
                
                try:
                    ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("12z run downloaded successfully!")
                except Exception as e:
                    print("12z run not available yet. Now trying the 06z run.")
                    try:
                        ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("06z run downloaded successfully!")
                    except Exception as e:
                        print("06z run from yesterday is not available. Now trying the 00z run.")
                        try:
                            ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("00z run downloaded successfully!")
                        except Exception as e:
                            print("00z run is not available. Now trying the 18z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("18z run downloaded successfully!")    
                            except Exception as e:
                                print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("12z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 18 and utc_time.hour < 24:
                
                try:
                    ds = xr.open_dataset(url_18z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("18z run downloaded successfully!")
                except Exception as e:
                    print("18z run not available yet. Now trying the 12z run.")
                    try:
                        ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("12z run downloaded successfully!")
                    except Exception as e:
                        print("12z run from yesterday is not available. Now trying the 06z run.")
                        try:
                            ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("06z run downloaded successfully!")
                        except Exception as e:
                            print("06z run is not available. Now trying the 00z run.")
                            try:
                                ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("00z run downloaded successfully!")    
                            except Exception as e:
                                print("00z run is not available. Now trying the 18z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("18z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
        else:

            longitude = 360 - longitude
        
            if utc_time.hour >= 0 and utc_time.hour < 6:
                
                try:
                    ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("00z run downloaded successfully!")
                except Exception as e:
                    print("00z run not available yet. Now trying the 18z run from yesterday.")
                    try:
                        ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("18z run downloaded successfully!")
                    except Exception as e:
                        print("18z run from yesterday is not available. Now trying the 12z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("12z run downloaded successfully!")
                        except Exception as e:
                            print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("06z run downloaded successfully!")    
                            except Exception as e:
                                print("06z run from yesterday is not available. Now trying the 00z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_00z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("00z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
                    
            
            if utc_time.hour >= 6 and utc_time.hour < 12:
                
                try:
                    ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("06z run downloaded successfully!")
                except Exception as e:
                    print("06z run not available yet. Now trying the 00z run.")
                    try:
                        ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("00z run downloaded successfully!")
                    except Exception as e:
                        print("00z run from yesterday is not available. Now trying the 18z run for yesterday.")
                        try:
                            ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("18z run downloaded successfully!")
                        except Exception as e:
                            print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("12z run downloaded successfully!")    
                            except Exception as e:
                                print("12z run from yesterday is not available. Now trying the 06z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_06z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("06z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 12 and utc_time.hour < 18:
                
                try:
                    ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("12z run downloaded successfully!")
                except Exception as e:
                    print("12z run not available yet. Now trying the 06z run.")
                    try:
                        ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("06z run downloaded successfully!")
                    except Exception as e:
                        print("06z run from yesterday is not available. Now trying the 00z run.")
                        try:
                            ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("00z run downloaded successfully!")
                        except Exception as e:
                            print("00z run is not available. Now trying the 18z run from yesterday.")
                            try:
                                ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("18z run downloaded successfully!")    
                            except Exception as e:
                                print("18z run from yesterday is not available. Now trying the 12z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_12z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("12z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")
            
            if utc_time.hour >= 18 and utc_time.hour < 24:
                
                try:
                    ds = xr.open_dataset(url_18z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                    print("18z run downloaded successfully!")
                except Exception as e:
                    print("18z run not available yet. Now trying the 12z run.")
                    try:
                        ds = xr.open_dataset(url_12z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                        print("12z run downloaded successfully!")
                    except Exception as e:
                        print("12z run from yesterday is not available. Now trying the 06z run.")
                        try:
                            ds = xr.open_dataset(url_06z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                            print("06z run downloaded successfully!")
                        except Exception as e:
                            print("06z run is not available. Now trying the 00z run.")
                            try:
                                ds = xr.open_dataset(url_00z_run, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                print("00z run downloaded successfully!")    
                            except Exception as e:
                                print("00z run is not available. Now trying the 18z run from yesterday.")
                                try:
                                    ds = xr.open_dataset(yday_18z, engine='netcdf4').sel(lon=longitude, lat=latitude, method='nearest')
                                    print("18z run downloaded successfully!")      
                                except Exception as e:
                                    print("Latest available dataset is over a day old. Not even worth the time at this point!")




        ds = ds.metpy.parse_cf()
        
        return ds

    def get_nomads_model_data_via_https(model, region, typeOfLevel, western_bound, eastern_bound, southern_bound, northern_bound, get_u_and_v_wind_components=False, add_wind_gusts=True):

        r'''
        This function grabs the latest model data from the NOAA/NCEP/NOMADS HTTPS Server and returns it to the user. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree ensemble mean
           2) GEFS0p25 CHEM - GEFS 0.25x0.25 coarse and fine particulates
           3) GEFS0p50 CHEM - GEFS 0.5x0.5 coarse and fine particulates
           4) UKMET - UKMET model

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        3) typeOfLevel (String) - This determines which parameters are available for the GEFS 0.25x0.25 Ensemble Mean. The choices are as
                                  follows: 

                                  1) surface
                                  2) meanSea
                                  3) depthBelowLandLayer
                                  4) heightAboveGround
                                  5) atmosphereSingleLayer
                                  6) cloudCeiling
                                  7) heightAboveGroundLayer
                                  8) pressureFromGroundLayer
        
                                  For both the UKMET and GEFS CHEM you can enter a value of None here. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region.
    
        Optional Arguments: 
        
        1) get_u_and_v_wind_components (Boolean) - Default = False. When having the typeOfLevel set to 'heightAboveGround' there is an issue
                                                   with retrieving the u and v wind components. You will see an error message. Fortunately, 
                                                   in FireWxPy we fix that for you so you can disregard the errors. When setting this value to True
                                                   you will also return lists of the u and v datasets. 
    
        2) add_wind_gusts (Boolean) - Default = True. When having get_u_and_v_wind_components=True, you can opt to add an additional list to be 
                                      returned which will have the wind gust dataset. 
    
        Returns: Depending on the values you enter above determines how many lists of datasets are returned. 
                 If the user does not use 'GEFS0p25 ENS MEAN' for the model of choice, a single list of the datasets are returned. 
                 If the user uses 'GEFS0p25 ENS MEAN' and does not have typeOfLevel set to 'heightAboveGround', a single list of the datasets are returned. 
                 If the user uses 'GEFS0p25 ENS MEAN' and does have typeOfLevel set to 'heightAboveGround' while get_u_and_v_wind_components=False, a single list of the datasets are returned. 
                 If the user uses 'GEFS0p25 ENS MEAN' and does have typeOfLevel set to 'heightAboveGround' while get_u_and_v_wind_components=True and get_u_and_v_wind_components=False,
                 a list of the 'heightAboveGround' datasets, u-wind datasets and v-wind datasets will be returned. 
                 If the user uses 'GEFS0p25 ENS MEAN' and does have typeOfLevel set to 'heightAboveGround' while get_u_and_v_wind_components=True and get_u_and_v_wind_components=True,
                 a list of the 'heightAboveGround' datasets, u-wind datasets, v-wind datasets and gust datasets will be returned.
                             
        '''    
        sys.tracebacklimit = 0
        logging.disable()
    
        local_time, utc_time = standard.plot_creation_time()
        yesterday = utc_time - timedelta(hours=24)
    
        western_bound, eastern_bound, southern_bound, northern_bound = coords_for_forecast_model_data(region, western_bound, eastern_bound, southern_bound, northern_bound) 
    
        if os.path.exists(f"{model} Data"):
            print(f"Already Satisfied: 'f:{model} Data' exists.")
        else:
            print(f"'f:{model} Data' does not exist\nCreating 'f:{model} Data'.")
            os.mkdir(f"{model} Data")
            print(f"'f:{model} Data' created successfully.")
        
        for file in os.listdir(f"{model} Data"):
            try:
                os.remove(f"{model} Data/{file}")
            except Exception as e:
                pass
        
        print(f"Any old files (if any) in 'f:{model} Data' have been deleted.")
    
        forecast_hours = []

        if model == 'UKMET':

            if model == 'UKMET':

                url_today = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/ukmet/prod/ukmet.{utc_time.strftime('%Y%m%d')}/"
                url_yday = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/ukmet/prod/ukmet.{yesterday.strftime('%Y%m%d')}/"
    
                fname_00z = f"nrukmet.t00z.ukm25.grib2"
                fname_12z = f"nrukmet.t12z.ukm25.grib2"

            if utc_time.hour >= 12 and utc_time.hour < 24:
                try:
                    urllib.request.urlretrieve(f"{url_today}/{fname_12z}", f"{fname_12z}")
                    os.replace(f"{fname_12z}", f"{model} Data/{fname_12z}")
                    print(f"Downloaded {fname_12z} to f:{model} Data/{fname_12z}") 
                except Exception as e:
                    print(f"12z {model} is not available. Trying to download 00z {model} run.")
                    try:
                        urllib.request.urlretrieve(f"{url_today}/{fname_00z}", f"{fname_00z}")
                        os.replace(f"{fname_00z}", f"{model} Data/{fname_00z}")
                        print(f"Downloaded {fname_00z} to f:{model} Data/{fname_00z}")
                    except Exception as e:
                        print(f"00z {model} is not available. Trying to download yesterday's 12z {model} run.")
                        try:
                            urllib.request.urlretrieve(f"{url_yday}/{fname_12z}", f"{fname_12z}")
                            os.replace(f"{fname_12z}", f"{model} Data/{fname_12z}")
                            print(f"Downloaded {fname_12z} to f:{model} Data/{fname_12z}") 
                        except Exception as e:
                            print(f"Newest data is more than 24 hours old. Aborting...")

            if utc_time.hour >= 0 and utc_time.hour < 12:
                try:
                    urllib.request.urlretrieve(f"{url_today}/{fname_00z}", f"{fname_00z}")
                    os.replace(f"{fname_00z}", f"{model} Data/{fname_00z}")
                    print(f"Downloaded {fname_00z} to f:{model} Data/{fname_00z}") 
                except Exception as e:
                    print(f"00z {model} is not available. Trying to download yesterday's 12z {model} run.")
                    try:
                        urllib.request.urlretrieve(f"{url_yday}/{fname_12z}", f"{fname_12z}")
                        os.replace(f"{fname_12z}", f"{model} Data/{fname_12z}")
                        print(f"Downloaded {fname_12z} to f:{model} Data/{fname_12z}")
                    except Exception as e:
                        print(f"12z {model} is not available. Trying to download yesterday's 00z {model} run.")
                        try:
                            urllib.request.urlretrieve(f"{url_yday}/{fname_00z}", f"{fname_00z}")
                            os.replace(f"{fname_00z}", f"{model} Data/{fname_00z}")
                            print(f"Downloaded {fname_00z} to f:{model} Data/{fname_00z}") 
                        except Exception as e:
                            print(f"Newest data is more than 24 hours old. Aborting...")

            for item in os.listdir(f"{model} Data"):
                if item.endswith(".idx"):
                    os.remove(f"{model} Data/{item}")

            try:
                ds = xr.open_dataset(f"{model} Data/{fname_12z}", engine='cfgrib').sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
            except Exception as e:
                ds = xr.open_dataset(f"{model} Data/{fname_00z}", engine='cfgrib').sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))

            return ds
                            
        
        if model == 'GEFS0p25 ENS MEAN' or model == 'GEFS0p25 CHEM' or model == 'GEFS0p50 CHEM':

            if model == 'GEFS0p25 CHEM' or model == 'GEFS0p50 CHEM':
                
                for i in range(0, 12, 3):
                    hour = f"00{i}"
                    forecast_hours.append(hour)
                for i in range(12, 102, 3):
                    hour = f"0{i}"
                    forecast_hours.append(hour)
                for i in range(102, 123, 3):
                    hour = f"{i}"
                    forecast_hours.append(hour)

                if model == 'GEFS0p25 CHEM':
                
                    url_00z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/00/chem/pgrb2ap25/"
                    url_06z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/06/chem/pgrb2ap25/"
                    url_12z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/12/chem/pgrb2ap25/"
                    url_18z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/18/chem/pgrb2ap25/"
            
                    yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/00/chem/pgrb2ap25/"
                    yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/06/chem/pgrb2ap25/"
                    yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/12/chem/pgrb2ap25/"
                    yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/18/chem/pgrb2ap25/"
        
                    fnames_00z = []
                    fnames_06z = []
                    fnames_12z = []
                    fnames_18z = []
                    for hour in forecast_hours:
                        fname_00z = f"gefs.chem.t00z.a2d_0p25.f{hour}.grib2"
                        fnames_00z.append(fname_00z)
                        fname_06z = f"gefs.chem.t06z.a2d_0p25.f{hour}.grib2"
                        fnames_06z.append(fname_06z)
                        fname_12z = f"gefs.chem.t12z.a2d_0p25.f{hour}.grib2"
                        fnames_12z.append(fname_12z)
                        fname_18z = f"gefs.chem.t18z.a2d_0p25.f{hour}.grib2"
                        fnames_18z.append(fname_18z)


                if utc_time.hour >= 0 and utc_time.hour < 6:
                    try:
                        for fname in fnames_00z:
                            urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                    except Exception as e:
                        try:
                            for fname in fnames_18z:
                                urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                                print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                        except Exception as e:
                            try:
                                for fname in fnames_12z:
                                    urllib.request.urlretrieve(f"{yday_12z}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                                    print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                            except Exception as e:
                                try:
                                    for fname in fnames_06z:
                                        urllib.request.urlretrieve(f"{yday_06z}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                        print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                except Exception as e:
                                    try:
                                        for fname in fnames_00z:
                                            urllib.request.urlretrieve(f"{yday_00z}/{fname}", f"geavg.t00z.pgrb2s.0p25.f{hour}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 00z - Not even worth downloading at this point!")
        
                if utc_time.hour >= 6 and utc_time.hour < 12:
                    try:
                        for fname in fnames_06z:
                            urllib.request.urlretrieve(f"{url_06z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                    except Exception as e:
                        try:
                            for fname in fnames_00z:
                                urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                                print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                        except Exception as e:
                            try:
                                for fname in fnames_18z:
                                    urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                                    print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                            except Exception as e:
                                try:
                                    for fname in fnames_12z:
                                        urllib.request.urlretrieve(f"{yday_12z}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                        print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                except Exception as e:
                                    try:
                                        for fname in fnames_06z:
                                            urllib.request.urlretrieve(f"{yday_06z}/{fname}", f"{fname}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 06z - Not even worth downloading at this point!")
        
                if utc_time.hour >= 12 and utc_time.hour < 18:
                    try:
                        for fname in fnames_12z:
                            urllib.request.urlretrieve(f"{url_12z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                    except Exception as e:
                        try:
                            for fname in fnames_06z:
                                urllib.request.urlretrieve(f"{url_06z_run}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                                print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                        except Exception as e:
                            try:
                                for fname in fnames_00z:
                                    urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                                    print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                            except Exception as e:
                                try:
                                    for fname in fnames_18z:
                                        urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                        print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                except Exception as e:
                                    try:
                                        for fname in fnames_12z:
                                            urllib.request.urlretrieve(f"{yday_12z}/{fname}", f"geavg.t12z.pgrb2s.0p25.f{hour}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                            print(f"Downloaded {fname} to f:{model} Data/{fname}")  
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 12z - Not even worth downloading at this point!")
        
                if utc_time.hour >= 18 and utc_time.hour < 24:
                    try:
                        for fname in fnames_18z:
                            urllib.request.urlretrieve(f"{url_18z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                    except Exception as e:
                        try:
                            for fname in fnames_12z:
                                urllib.request.urlretrieve(f"{url_12z_run}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                                print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                        except Exception as e:
                            try:
                                for fname in fnames_06z:
                                    urllib.request.urlretrieve(f"{url_06z_run}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                                    print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                            except Exception as e:
                                try:
                                    for fname in fnames_00z:
                                        urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                        print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                except Exception as e:
                                    try:
                                        for fname in fnames_18z:
                                            urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                            print(f"Downloaded {fname} to f:{model} Data/{fname}") 
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 18z - Not even worth downloading at this point!")
        
                for item in os.listdir(f"{model} Data"):
                    if item.endswith(".idx"):
                        os.remove(f"{model} Data/{item}")
                
                fpaths = []
                for file in os.listdir(f"{model} Data"):
                    fname = os.path.basename(file)
                    fpath = f"{model} Data/{fname}"
                    fpaths.append(fpath)

                datasets = []
                for file in fpaths:
                    ds = xr.open_dataset(file, engine='cfgrib').sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                    datasets.append(ds)
                    print(f"Extrated dataset from {file}")
                    
                return datasets

            if model == 'GEFS0p25 ENS MEAN':

                for i in range(0, 12, 3):
                    hour = f"00{i}"
                    forecast_hours.append(hour)
                for i in range(12, 75, 3):
                    hour = f"0{i}"
                    forecast_hours.append(hour)
                for i in range(78, 102, 6):
                    hour = f"0{i}"
                    forecast_hours.append(hour)
                for i in range(102, 243, 6):
                    hour = f"{i}"
                    forecast_hours.append(hour)

                if model == 'GEFS0p25 ENS MEAN':
                
                    url_00z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/"
                    url_06z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/"
                    url_12z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/"
                    url_18z_run = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{utc_time.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/"
            
                    yday_00z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/"
                    yday_06z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/"
                    yday_12z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/"
                    yday_18z = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.{yesterday.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/"
        
                    fnames_00z = []
                    fnames_06z = []
                    fnames_12z = []
                    fnames_18z = []
                    for hour in forecast_hours:
                        fname_00z = f"geavg.t00z.pgrb2s.0p25.f{hour}"
                        fnames_00z.append(fname_00z)
                        fname_06z = f"geavg.t06z.pgrb2s.0p25.f{hour}"
                        fnames_06z.append(fname_06z)
                        fname_12z = f"geavg.t12z.pgrb2s.0p25.f{hour}"
                        fnames_12z.append(fname_12z)
                        fname_18z = f"geavg.t18z.pgrb2s.0p25.f{hour}"
                        fnames_18z.append(fname_18z)                    
    
                if utc_time.hour >= 0 and utc_time.hour < 6:
                    try:
                        for fname in fnames_00z:
                            urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                    except Exception as e:
                        try:
                            for fname in fnames_18z:
                                urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                        except Exception as e:
                            try:
                                for fname in fnames_12z:
                                    urllib.request.urlretrieve(f"{yday_12z}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                            except Exception as e:
                                try:
                                    for fname in fnames_06z:
                                        urllib.request.urlretrieve(f"{yday_06z}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                except Exception as e:
                                    try:
                                        for fname in fnames_00z:
                                            urllib.request.urlretrieve(f"{yday_00z}/{fname}", f"geavg.t00z.pgrb2s.0p25.f{hour}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 00z - Not even worth downloading at this point!")
        
                if utc_time.hour >= 6 and utc_time.hour < 12:
                    try:
                        for fname in fnames_06z:
                            urllib.request.urlretrieve(f"{url_06z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                    except Exception as e:
                        try:
                            for fname in fnames_00z:
                                urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                        except Exception as e:
                            try:
                                for fname in fnames_18z:
                                    urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                            except Exception as e:
                                try:
                                    for fname in fnames_12z:
                                        urllib.request.urlretrieve(f"{yday_12z}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                except Exception as e:
                                    try:
                                        for fname in fnames_06z:
                                            urllib.request.urlretrieve(f"{yday_06z}/{fname}", f"{fname}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 06z - Not even worth downloading at this point!")
        
                if utc_time.hour >= 12 and utc_time.hour < 18:
                    try:
                        for fname in fnames_12z:
                            urllib.request.urlretrieve(f"{url_12z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                    except Exception as e:
                        try:
                            for fname in fnames_06z:
                                urllib.request.urlretrieve(f"{url_06z_run}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                        except Exception as e:
                            try:
                                for fname in fnames_00z:
                                    urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                            except Exception as e:
                                try:
                                    for fname in fnames_18z:
                                        urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                except Exception as e:
                                    try:
                                        for fname in fnames_12z:
                                            urllib.request.urlretrieve(f"{yday_12z}/{fname}", f"geavg.t12z.pgrb2s.0p25.f{hour}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 12z - Not even worth downloading at this point!")
        
                if utc_time.hour >= 18 and utc_time.hour < 24:
                    try:
                        for fname in fnames_18z:
                            urllib.request.urlretrieve(f"{url_18z_run}/{fname}", f"{fname}")
                            os.replace(f"{fname}", f"{model} Data/{fname}")
                    except Exception as e:
                        try:
                            for fname in fnames_12z:
                                urllib.request.urlretrieve(f"{url_12z_run}/{fname}", f"{fname}")
                                os.replace(f"{fname}", f"{model} Data/{fname}")
                        except Exception as e:
                            try:
                                for fname in fnames_06z:
                                    urllib.request.urlretrieve(f"{url_06z_run}/{fname}", f"{fname}")
                                    os.replace(f"{fname}", f"{model} Data/{fname}")
                            except Exception as e:
                                try:
                                    for fname in fnames_00z:
                                        urllib.request.urlretrieve(f"{url_00z_run}/{fname}", f"{fname}")
                                        os.replace(f"{fname}", f"{model} Data/{fname}")
                                except Exception as e:
                                    try:
                                        for fname in fnames_18z:
                                            urllib.request.urlretrieve(f"{yday_18z}/{fname}", f"{fname}")
                                            os.replace(f"{fname}", f"{model} Data/{fname}")
                                    except Exception as e:
                                        print(f"Latest dataset is older than {yesterday.strftime('%Y-%m-%d')} 18z - Not even worth downloading at this point!")
        
                for item in os.listdir(f"{model} Data"):
                    if item.endswith(".idx"):
                        os.remove(f"{model} Data/{item}")
                
                fpaths = []
                for file in os.listdir(f"{model} Data"):
                    fname = os.path.basename(file)
                    fpath = f"{model} Data/{fname}"
                    fpaths.append(fpath)
        
                if get_u_and_v_wind_components == False:
                    datasets = []
                    for file in fpaths:
                        ds = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                        datasets.append(ds)
                        
                    return datasets
        
                if get_u_and_v_wind_components == True:
                    datasets = []
                    u = []
                    v = []
        
                    if add_wind_gusts == False:
                        for file in fpaths:
                            ds = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            u_wind = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10u'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            v_wind = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10v'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            datasets.append(ds)
                            u.append(u_wind)
                            v.append(v_wind)
                            
                        return datasets, u, v
        
                    if add_wind_gusts == True:
        
                        gusts = []
                        for file in fpaths:
                            ds = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': typeOfLevel}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            u_wind = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10u'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            v_wind = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName': '10v'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            data = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'typeOfLevel': 'surface'}).sel(longitude=slice(360-western_bound, 360-eastern_bound, 1), latitude=slice(northern_bound, southern_bound, 1))
                            gust = data['gust']
                            gusts.append(gust)
                            datasets.append(ds)
                            u.append(u_wind)
                            v.append(v_wind)
                            
                        return datasets, u, v, gusts


    def msc_datamart_datasets(product, directory_path):

        r'''
        This function retrieves the latest data from the Canadian RDPA

        Required Arguments:

        1) product (String) - The type of product: 1) 'RDPA 6hr' 2) 'RDPA 24hr'

        Optional Arguments: None

        Returns: An xarray.data_array of the latest RDPA data. 

        '''

        local_time, utc_time = standard.plot_creation_time()
        yesterday = utc_time - timedelta(hours=24)

        directory_path = directory_path        
        

        if product == 'RDPA 6hr':

            today_00z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/00/'+utc_time.strftime('%Y%m%d')+'T00Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            today_06z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/06/'+utc_time.strftime('%Y%m%d')+'T06Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            today_12z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/12/'+utc_time.strftime('%Y%m%d')+'T12Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            today_18z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/18/'+utc_time.strftime('%Y%m%d')+'T18Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            
            yday_00z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/00/'+yesterday.strftime('%Y%m%d')+'T00Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            yday_06z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/06/'+yesterday.strftime('%Y%m%d')+'T06Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            yday_12z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/12/'+yesterday.strftime('%Y%m%d')+'T12Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '
            yday_18z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/18/'+yesterday.strftime('%Y%m%d')+'T18Z_MSC_RDPA_APCP-Accum6h_Sfc_RLatLon0.09_PT0H.grib2 '

        if product == 'RDPA 24hr':

            today_00z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/00/'+utc_time.strftime('%Y%m%d')+'T00Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            today_06z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/06/'+utc_time.strftime('%Y%m%d')+'T06Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            today_12z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/12/'+utc_time.strftime('%Y%m%d')+'T12Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            today_18z_run = 'https://dd.weather.gc.ca/'+utc_time.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/18/'+utc_time.strftime('%Y%m%d')+'T18Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            
            yday_00z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/00/'+yesterday.strftime('%Y%m%d')+'T00Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            yday_06z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/06/'+yesterday.strftime('%Y%m%d')+'T06Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            yday_12z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/12/'+yesterday.strftime('%Y%m%d')+'T12Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '
            yday_18z_run = 'https://dd.weather.gc.ca/'+yesterday.strftime('%Y%m%d')+'/WXO-DD/model_rdpa/10km/18/'+yesterday.strftime('%Y%m%d')+'T18Z_MSC_RDPA_APCP-Accum24h_Sfc_RLatLon0.09_PT0H.grib2 '            
            
        file_today_00z = os.path.basename(today_00z_run)
        file_today_06z = os.path.basename(today_06z_run)
        file_today_12z = os.path.basename(today_12z_run)
        file_today_18z = os.path.basename(today_18z_run)
        
        file_yday_00z = os.path.basename(yday_00z_run)
        file_yday_06z = os.path.basename(yday_06z_run)
        file_yday_12z = os.path.basename(yday_12z_run)
        file_yday_18z = os.path.basename(yday_18z_run)        

        try:
            os.remove(f"{directory_path}/{file_today_00z}")
            print(f"{file_today_00z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_today_06z}")
            print(f"{file_today_06z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_today_12z}")
            print(f"{file_today_12z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_today_18z}")
            print(f"{file_today_18z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_yday_00z}")
            print(f"{file_yday_00z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_yday_06z}")
            print(f"{file_yday_06z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_yday_12z}")
            print(f"{file_yday_12z} removed.")
        except Exception as e:
            pass
        
        try:
            os.remove(f"{directory_path}/{file_yday_18z}")
            print(f"{file_yday_18z} removed.")
        except Exception as e:
            pass


        if utc_time.hour >= 0 and utc_time.hour < 6:
            try:
                urllib.request.urlretrieve(f"{today_00z_run}", f"{file_today_00z}")
                ds = xr.open_dataset(file_today_00z, engine='cfgrib')
                print("Today's 00z run retrieved successfully.")
            except Exception as e:
                print("Today's 00z run is unavailable. Now trying to download yesterday's 18z run.")
                try:
                    urllib.request.urlretrieve(f"{yday_18z_run}", f"{file_yday_18z}")
                    ds = xr.open_dataset(file_yday_18z, engine='cfgrib')
                    print("Yesterday's 18z run retrieved successfully.")
                except Exception as e:
                    print("Yesterday's 18z run is unavailable. Now trying to download yesterday's 12z run.")
                    try:
                        urllib.request.urlretrieve(f"{yday_12z_run}", f"{file_yday_12z}")
                        ds = xr.open_dataset(file_yday_12z, engine='cfgrib')
                        print("Yesterday's 12z run retrieved successfully.")
                    except Exception as e:
                        print("Yesterday's 12z run is unavailable. Now trying to download yesterday's 06z run.")
                        try:
                            urllib.request.urlretrieve(f"{yday_06z_run}", f"{file_yday_06z}")
                            ds = xr.open_dataset(file_yday_06z, engine='cfgrib')
                            print("Yesterday's 06z run retrieved successfully.")
                        except Exception as e:
                            print("Yesterday's 06z run is unavailable. Now trying to download yesterday's 00z run.")
                            try:
                                urllib.request.urlretrieve(f"{yday_00z_run}", f"{file_yday_00z}")
                                ds = xr.open_dataset(file_yday_00z, engine='cfgrib')
                                print("Yesterday's 00z run retrieved successfully.") 
                            except Exception as e:
                                print("The latest available dataset is over a day old. Not even worth it at this point!")
                            
        if utc_time.hour >= 6 and utc_time.hour < 12:
            try:
                urllib.request.urlretrieve(f"{today_06z_run}", f"{file_today_06z}")
                ds = xr.open_dataset(file_today_06z, engine='cfgrib')
                print("Today's 06z run retrieved successfully.")
            except Exception as e:
                print("Today's 06z run is unavailable. Now trying to download today's 00z run.")
                try:
                    urllib.request.urlretrieve(f"{today_00z_run}", f"{file_today_00z}")
                    ds = xr.open_dataset(file_today_00z, engine='cfgrib')
                except Exception as e:
                    print("Today's 00z run is unavailable. Now trying to download yesterday's 18z run.")
                    try:
                        urllib.request.urlretrieve(f"{yday_18z_run}", f"{file_yday_18z}")
                        ds = xr.open_dataset(file_yday_18z, engine='cfgrib')
                        print("Yesterday's 18z run retrieved successfully.")
                    except Exception as e:
                        print("Yesterday's 18z run is unavailable. Now trying to download yesterday's 12z run.")
                        try:
                            urllib.request.urlretrieve(f"{yday_12z_run}", f"{file_yday_12z}")
                            ds = xr.open_dataset(file_yday_12z, engine='cfgrib')
                            print("Yesterday's 12z run retrieved successfully.")
                        except Exception as e:
                            print("Yesterday's 12z run is unavailable. Now trying to download yesterday's 06z run.")
                            try:
                                urllib.request.urlretrieve(f"{yday_06z_run}", f"{file_yday_06z}")
                                ds = xr.open_dataset(file_yday_06z, engine='cfgrib')
                                print("Yesterday's 06z run retrieved successfully.")
                            except Exception as e:
                                print("The latest available dataset is over a day old. Not even worth it at this point!")
        
        if utc_time.hour >= 12 and utc_time.hour < 18:
            try:
                urllib.request.urlretrieve(f"{today_12z_run}", f"{file_today_12z}")
                ds = xr.open_dataset(file_today_12z, engine='cfgrib')
                print("Today's 12z run retrieved successfully.")
            except Exception as e:
                print("Today's 12z run is unavailable. Now trying to download today's 06z run.")
                try:
                    urllib.request.urlretrieve(f"{today_06z_run}", f"{file_today_06z}")
                    ds = xr.open_dataset(file_today_06z, engine='cfgrib')
                    print("Today's 06z run retrieved successfully.")
                except Exception as e:
                    print("Today's 06z run is unavailable. Now trying to download today's 00z run.")
                    try:
                        urllib.request.urlretrieve(f"{today_00z_run}", f"{file_today_00z}")
                        ds = xr.open_dataset(file_today_00z, engine='cfgrib')
                        print("Today's 00z run retrieved successfully.")
                    except Exception as e:
                        print("Today's 00z run is unavailable. Now trying to download yesterday's 18z run.")
                        try:
                            urllib.request.urlretrieve(f"{yday_18z_run}", f"{file_yday_18z}")
                            ds = xr.open_dataset(file_yday_18z, engine='cfgrib')
                            print("Yesterday's 18z run retrieved successfully.")
                        except Exception as e:
                            print("Yesterday's 18z run is unavailable. Now trying to download yesterday's 12z run.")
                            try:
                                urllib.request.urlretrieve(f"{yday_12z_run}", f"{file_yday_12z}")
                                ds = xr.open_dataset(file_yday_12z, engine='cfgrib')
                                print("Yesterday's 12z run retrieved successfully.")
                            except Exception as e:
                                print("The latest available dataset is over a day old. Not even worth it at this point!")
        
        if utc_time.hour >= 18 and utc_time.hour < 24:
            try:
                urllib.request.urlretrieve(f"{today_18z_run}", f"{file_today_18z}")
                ds = xr.open_dataset(file_today_18z, engine='cfgrib')
                print("Today's 18z run retrieved successfully.")
            except Exception as e:
                print("Today's 18z run is unavailable. Now trying to download today's 12z run.")
                try:
                    urllib.request.urlretrieve(f"{today_12z_run}", f"{file_today_12z}")
                    ds = xr.open_dataset(file_today_12z, engine='cfgrib')
                    print("Today's 12z run retrieved successfully.")
                except Exception as e:
                    print("Today's 12z run is unavailable. Now trying to download today's 06z run.")
                    try:
                        urllib.request.urlretrieve(f"{today_06z_run}", f"{file_today_06z}")
                        ds = xr.open_dataset(file_today_06z, engine='cfgrib')
                        print("Today's 06z run retrieved successfully.")
                    except Exception as e:
                        print("Today's 06z run is unavailable. Now trying to download today's 00z run.")
                        try:
                            urllib.request.urlretrieve(f"{today_00z_run}", f"{file_today_00z}")
                            ds = xr.open_dataset(file_today_00z, engine='cfgrib')
                            print("Today's 00z run retrieved successfully.")
                        except Exception as e:
                            print("Today's 00z run is unavailable. Now trying to download yesterday's 18z run.")
                            try:
                                urllib.request.urlretrieve(f"{yday_18z_run}", f"{file_yday_18z}")
                                ds = xr.open_dataset(file_yday_18z, engine='cfgrib')
                                print("Yesterday's 18z run retrieved successfully.")
                            except Exception as e:
                                print("The latest available dataset is over a day old. Not even worth it at this point!")


        return ds

class RTMA:

    r'''
    
    This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

    This class hosts the functions the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''

    
    def get_rtma_datasets(region, current_time):
    
        r'''
        
        This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Arguments:

        1) region (String) - The abbreviation for the region (state, GACC Region, CONUS, etc.)
        
        2) Current Time in UTC

        Returns: 
        
        1) The latest 2.5km x 2.5km RTMA Dataset
        
        2) 1) The 2.5km x 2.5km RTMA Dataset from 24-Hours prior to the current dataset
        
        3) The time corresponding to the dataset
        
        4) The time corresponding to the dataset from 24-Hours prior to the current dataset 
    
        '''
        
        times = []
        new_times = []
        for i in range(0, 5):
            time = pd.to_datetime(current_time - timedelta(hours=i))
            times.append(time)
    
        for t in times:
            new_time = t - timedelta(hours=24)
            new_times.append(new_time)

        if region == 'AK' or region == 'ak':
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'
        
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+new_times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+new_times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+new_times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+new_times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+new_times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'

        elif region == 'HI' or region == 'hi':
            
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'
        
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+new_times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+new_times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+new_times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+new_times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+new_times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'        
        
        else:
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[0].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[1].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[2].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[3].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[4].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[4].strftime('%H')+'z'
        
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+new_times[0].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+new_times[1].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+new_times[2].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+new_times[3].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+new_times[4].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[4].strftime('%H')+'z'
    
        try:
            if region == 'AK' or region == 'ak':
                ds = xr.open_dataset(url_0, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                print("Data was successfully retrieved for " + new_times[0].strftime('%m/%d/%Y %HZ'))
            else:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + new_times[0].strftime('%m/%d/%Y %HZ'))        
            strtime = times[0]
            strtime_24 = new_times[0]
            return ds, ds_24, strtime, strtime_24
            
        except Exception as a:
            try:
                print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                if region == 'AK' or region == 'ak':
                    ds = xr.open_dataset(url_1, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                    print("Data was successfully retrieved for " + new_times[1].strftime('%m/%d/%Y %HZ'))
                else:
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + new_times[1].strftime('%m/%d/%Y %HZ'))        
                strtime = times[1]
                strtime_24 = new_times[1]
                return ds, ds_24, strtime, strtime_24
                
            except Exception as b:
                    try:
                        print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                        if region == 'AK' or region == 'ak':
                            ds = xr.open_dataset(url_2, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                            print("Data was successfully retrieved for " + new_times[2].strftime('%m/%d/%Y %HZ'))
                        else:
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + new_times[2].strftime('%m/%d/%Y %HZ')) 
                            strtime = times[2]
                            strtime_24 = new_times[2]
                            return ds, ds_24, strtime, strtime_24
                        
                    except Exception as c:
                        try:
                            print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                            if region == 'AK' or region == 'ak':
                                ds = xr.open_dataset(url_3, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                print("Data was successfully retrieved for " + new_times[3].strftime('%m/%d/%Y %HZ'))
                            else:
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + new_times[3].strftime('%m/%d/%Y %HZ')) 
                            strtime = times[3]
                            strtime_24 = new_times[3]
                            return ds, ds_24, strtime, strtime_24
                            
                        except Exception as d:
    
                            try:
                                print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                if region == 'AK' or region == 'ak':
                                    ds = xr.open_dataset(url_4, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                    print("Data was successfully retrieved for " + new_times[4].strftime('%m/%d/%Y %HZ'))
                                else:
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + new_times[4].strftime('%m/%d/%Y %HZ')) 
                                strtime = times[4]
                                strtime_24 = new_times[4]
                                return ds, ds_24, strtime, strtime_24
                                
                            except Exception as e:
                                print("The latest dataset is over 4 hours old which isn't current. Please try again later.")

            
        except Exception as f:
            print(f"No Data available for {state} at {current_time.strftime('%m/%d/%Y %HZ')}")


class NDFD_GRIDS:

    r'''

    This class hosts the active function that downloads the NOAA/NWS/NDFD Gridded Data. 

    This class hosts the function the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''

    def get_ndfd_grids_xarray(directory_name, parameter, state):

        r'''

        This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

        Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

        Required Arguments: 
        
        1) directory_name (String) - The name of the directory (see FireWxPy documentation for directory paths)

        2) parameter (String) - The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

        3) state (String) - The state or region being used. 

        Returns: An xarray.data_array of the latest NWS/SPC Forecast data

        '''
    
        directory_name = directory_name
        parameter = parameter

        if os.path.exists(f"NWS Data"):
            pass
        else:
            os.mkdir(f"NWS Data")

        for file in os.listdir(f"NWS Data"):
            try:
                os.remove(f"NWS Data"/{file})
            except Exception as e:
                pass

        if parameter == 'ds.maxrh.bin':
            short_term_fname = 'ds.maxrh_short.bin'
            extended_fname = 'ds.maxrh_extended.bin'
    
        if parameter == 'ds.minrh.bin':
            short_term_fname = 'ds.minrh_short.bin'
            extended_fname = 'ds.minrh_extended.bin'
    
        if parameter == 'ds.maxt.bin':
            short_term_fname = 'ds.maxt_short.bin'
            extended_fname = 'ds.maxt_extended.bin'
    
        if parameter == 'ds.mint.bin':
            short_term_fname = 'ds.mint_short.bin'
            extended_fname = 'ds.mint_extended.bin'

        if parameter == 'ds.rhm.bin':
            short_term_fname = 'ds.rhm_short.bin'
            extended_fname = 'ds.rhm_extended.bin'    

        if parameter == 'ds.temp.bin':
            short_term_fname = 'ds.temp_short.bin'
            extended_fname = 'ds.temp_extended.bin' 

        if parameter == 'ds.wspd.bin':
            short_term_fname = 'ds.wspd_short.bin'
            extended_fname = 'ds.wspd_extended.bin'  

        if parameter == 'ds.wgust.bin':
            short_term_fname = 'ds.wgust_short.bin'
            extended_fname = 'ds.wgust_extended.bin'   

        if parameter == 'ds.wdir.bin':
            short_term_fname = 'ds.wdir_short.bin'
            extended_fname = 'ds.wdir_extended.bin'  

        if parameter == 'ds.critfireo.bin':
            short_term_fname = 'ds.critfireo_short.bin'
            extended_fname = 'ds.critfireo_extended.bin'     

        if parameter == 'ds.dryfireo.bin':
            short_term_fname = 'ds.dryfireo_short.bin'
            extended_fname = 'ds.dryfireo_extended.bin' 

        if parameter == 'ds.conhazo.bin':
            short_term_fname = 'ds.conhazo_short.bin'
            extended_fname = 'ds.conhazo_extended.bin' 


        if os.path.exists(short_term_fname):
            os.remove(short_term_fname)
            urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.001-003/{parameter}", f"{parameter}")
            os.rename(parameter, short_term_fname)
        else:
            urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.001-003/{parameter}", f"{parameter}")
            os.rename(parameter, short_term_fname)
        
        if os.path.exists(extended_fname):
            try:
                os.remove(extended_fname)
                urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.004-007/{parameter}", f"{parameter}")
                os.rename(parameter, extended_fname)
                extended = True
            except Exception as e:
                extended = False
        else:
            try:
                urllib.request.urlretrieve(f"https://tgftp.nws.noaa.gov{directory_name}VP.004-007/{parameter}", f"{parameter}")
                os.rename(parameter, extended_fname)
                extended = True
            except Exception as e:
                extended = False

        os.replace(short_term_fname, f"NWS Data/{short_term_fname}")
        try:
            os.replace(extended_fname, f"NWS Data/{extended_fname}")
        except Exception as e:
            pass

        short_path = f"NWS Data/{short_term_fname}"
        try:
            extended_path = f"NWS Data/{extended_fname}"
        except Exception as e:
            pass

        try:
            os.remove(parameter)
        except Exception as e:
            pass

        if state != 'AK' or state != 'ak' or state == None:
            ds1 = xr.open_dataset(short_path, engine='cfgrib')
        else:
            ds1 = xr.open_dataset(short_path, engine='cfgrib').sel(x=slice(20, 1400, 2), y=slice(100, 1400, 2)) 
        try:
            if ds1['time'][1] == True:
                ds1 = ds1.isel(time=1)
            else:
                ds1 = ds1.isel(time=0)
        except Exception as e:
            try:
                ds1 = ds1.isel(time=0)
            except Exception as e:
                ds1 = ds1

        if extended == True:
            try:
    
                if state != 'AK' or state != 'ak' or state == None:
                    ds2 = xr.open_dataset(extended_path, engine='cfgrib')
                else:
                    ds2 = xr.open_dataset(extended_path, engine='cfgrib').sel(x=slice(20, 1400, 2), y=slice(100, 1400, 2)) 
        
                try:
                    if ds2['time'][1] == True:
                            ds2 = ds2.isel(time=1)
                    else:
                        ds2 = ds2.isel(time=0)  
                except Exception as e:
                    try:
                        ds2 = ds2.isel(time=0)
                    except Exception as e:
                        ds2 = ds2
            except Exception as e:
                pass
        else:
            ds2 = False
            
        ds1 = ds1.metpy.parse_cf()

        if extended == True:
            try:
                ds2 = ds2.metpy.parse_cf() 
            except Exception as e:
                ds2 = False
        else:
            pass

        for item in os.listdir(f"NWS Data"):
            if item.endswith(".idx"):
                os.remove(f"NWS Data/{item}")
            
        print(f"Retrieved {parameter} NDFD grids.")
    
        return ds1, ds2
    
class obs:

    r'''
    This class hosts functions to access observational data

    '''

    def previous_day_weather_summary(station_id):
    
        r'''
        This function retrieves the 24 hour observations for the previous day and returns the extreme maximum and minimum values as well as the times associated with those values.
    
        Inputs:
               1) station_id (String) - The 4 letter station identifier for the observational site. 
    
        Returns:
                1) Maximum Temperature (°F)
                2) The time the maximum temperature occurred
                3) Minimum Temperature (°F)
                4) The time the minimum temperature occurred
                5) Minimum Relative Humidity (%)
                6) The time the minimum relative humidity occurred
                7) Maximum Relative Humidity (%)
                8) The time the maximum relative humidity occurred
                9) Maximum Wind Speed (MPH)
                10) The time the maximum wind speed occurred
                11) Maximum Wind Gust (MPH)
                12) The time the maximum wind gust occurred 
    
        '''
    
        local_time, utc_time = standard.plot_creation_time()
        year = local_time.year
        month = local_time.month
        day = local_time.day
        station_id = station_id
    
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
        backup_server_status = backup_server_response.status_code
        
        hour = 0
        date = datetime(year, month, day, hour)
        
        to_zone = tz.tzutc()
        from_zone = tz.tzlocal()
        
        time = date.replace(tzinfo=from_zone)
        date_utc = date.astimezone(to_zone)
        
        new_date_utc = date_utc.replace(tzinfo=None)
        
        previous_day_utc = new_date_utc - timedelta(days=2)
        
        # Pings server for airport data
        airports_df = pd.read_csv(get_test_data('airport-codes.csv'))
        
        # Queries our airport types (airport sizes)
        airports_df = airports_df[(airports_df['type'] == 'large_airport') | (airports_df['type'] == 'medium_airport') | (airports_df['type'] == 'small_airport')]
        
        # Accesses the METAR data
    
        if main_server_status == 200:
            print("Main UCAR THREDDS Server is online. Connecting!")
            try:
                print("Downloading...")
                metar_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
            
            except Exception as e:
                print("Downloading...")
                metar_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
    
        if main_server_status != 200 and backup_server_status == 200:
            print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!") 
            try:
                print("Downloading...")
                metar_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
            
            except Exception as e:
                print("ERROR! Cannot connect to either the main or backup server. Aborting!")
    
        if main_server_status != 200 and backup_server_status != 200:
            print("ERROR! Cannot connect to either the main or backup server. Aborting!")
    
        metar_file = metar_cat.datasets.filter_time_range(previous_day_utc, previous_day_utc + timedelta(days=1))
        
        sfc_data_list = []
        for i in range(0,25):
            data = metar_file[i].remote_open()
            metar_text = StringIO(data.read().decode('latin-1'))
            sfc_data = parse_metar_file(metar_text)
            sfc_units = sfc_data.units
            sfc_data_list.append(sfc_data)
        
        df = pd.concat(sfc_data_list)
        
        df = df.loc[:, ['station_id', 'latitude', 'longitude', 'date_time', 'air_temperature', 'dew_point_temperature', 'wind_speed', 'wind_gust', 'wind_direction']]
    
        df['relative_humidity'] = calc.Thermodynamics.relative_humidity_from_temperature_and_dewpoint_celsius(df['air_temperature'], df['dew_point_temperature'])
       
        df = df[df['station_id'] == station_id]
        
        df['air_temperature'] = calc.unit_conversion.celsius_to_fahrenheit(df['air_temperature'])
        df['wind_speed'] = calc.unit_conversion.knots_to_mph(df['wind_speed'])
        df['wind_gust'] = calc.unit_conversion.knots_to_mph(df['wind_gust'])
        
        df = df.sort_values(['air_temperature'], ascending=False)
        print(df)
        maximum_temperature = df['air_temperature'].iloc[0]
        maximum_temperature_time = df['date_time'].iloc[0]
        maximum_temperature_time_utc = maximum_temperature_time.replace(tzinfo=to_zone)
        maximum_temperature_time_local = maximum_temperature_time_utc.astimezone(from_zone)
        minimum_temperature = df['air_temperature'].iloc[-1]
        minimum_temperature_time = df['date_time'].iloc[-1]
        minimum_temperature_time_utc = minimum_temperature_time.replace(tzinfo=to_zone)
        minimum_temperature_time_local = minimum_temperature_time_utc.astimezone(from_zone)
        
        df = df.sort_values(['relative_humidity'], ascending=True)
        minimum_relative_humidity = df['relative_humidity'].iloc[0]
        minimum_relative_humidity_time = df['date_time'].iloc[0]
        minimum_relative_humidity_time_utc = minimum_relative_humidity_time.replace(tzinfo=to_zone)
        minimum_relative_humidity_time_local = minimum_relative_humidity_time_utc.astimezone(from_zone)
        maximum_relative_humidity = df['relative_humidity'].iloc[-1]
        maximum_relative_humidity_time = df['date_time'].iloc[-1]
        maximum_relative_humidity_time_utc = maximum_relative_humidity_time.replace(tzinfo=to_zone)
        maximum_relative_humidity_time_local = maximum_relative_humidity_time_utc.astimezone(from_zone)
        
        df = df.sort_values(['wind_speed'], ascending=False)
        maximum_wind_speed = df['wind_speed'].iloc[0]
        wind_direction = df['wind_direction'].iloc[0]
        wind_dir = parsers.checks.wind_direction_number_to_abbreviation(wind_direction)
        maximum_wind_speed_time = df['date_time'].iloc[0]
        maximum_wind_speed_time_utc = maximum_wind_speed_time.replace(tzinfo=to_zone)
        maximum_wind_speed_time_local = maximum_wind_speed_time_utc.astimezone(from_zone)
        
        df = df.sort_values(['wind_gust'], ascending=False)
        maximum_wind_gust = df['wind_gust'].iloc[0]
        maximum_wind_gust_time = df['date_time'].iloc[0]
        maximum_wind_gust_time_utc = maximum_wind_gust_time.replace(tzinfo=to_zone)
        maximum_wind_gust_time_local = maximum_wind_gust_time_utc.astimezone(from_zone)
    
        df = df.sort_values(['date_time'], ascending=True)
    
        print("Data retrieved successfully!")
    
        return df, maximum_temperature, maximum_temperature_time, maximum_temperature_time_local, minimum_temperature, minimum_temperature_time, minimum_temperature_time_local, minimum_relative_humidity, minimum_relative_humidity_time, minimum_relative_humidity_time_local, maximum_relative_humidity, maximum_relative_humidity_time, maximum_relative_humidity_time_local, maximum_wind_speed, wind_dir, maximum_wind_speed_time, maximum_wind_speed_time_local, maximum_wind_gust, maximum_wind_gust_time, maximum_wind_gust_time_local, station_id, previous_day_utc


    def get_metar_data():
    
        r'''
        This function downloads and returns the latest METAR data. 
        
        Inputs: None 
    
        Returns: 
        
        1) df (Pandas DataFrame) - DataFrame of the latest METAR data
        
        2) time (datetime) - The time of the latest METAR dataset 
        '''
    
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
        backup_server_status = backup_server_response.status_code
        
        # Pings server for airport data
        airports_df = pd.read_csv(get_test_data('airport-codes.csv'))
        
        # Queries our airport types (airport sizes)
        airports_df = airports_df[(airports_df['type'] == 'large_airport') | (airports_df['type'] == 'medium_airport') | (airports_df['type'] == 'small_airport')]
        
        # Accesses the METAR data
    
        if main_server_status == 200:
            
            try:
                metar_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
    
            
            except Exception as e:
                metar_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
    
        if main_server_status != 200 and backup_server_status == 200:
            try:
                metar_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
    
                print("Successfully connected to the backup server! Downloading Data...")
            
            except Exception as e:
                print("ERROR! Cannot connect to either the main or backup server. Aborting!")
    
        if main_server_status != 200 and backup_server_status != 200:
            print("ERROR! Cannot connect to either the main or backup server. Aborting!")

        ds = metar_cat.datasets[-5]

        if os.path.exists(f"METAR Data"):
            pass
        else:
            os.mkdir(f"METAR Data")

        for file in os.listdir(f"METAR Data"):
            try:
                os.remove(f"METAR Data/{file}")
            except Exception as e:
                pass

        ds.download()
        os.replace(ds.name, f"METAR Data/{ds.name}")
        file_size = (os.path.getsize(f"METAR Data/{ds.name}")/1000000)

        if file_size < 1.2:
            os.remove(f"METAR Data/{ds.name}")
            ds = metar_cat.datasets[-6]
            ds.download()
            os.replace(ds.name, f"METAR Data/{ds.name}")
        else:
            pass
        
        df = parse_metar_file(f"METAR Data/{ds.name}")
        name = os.path.basename(f"METAR Data/{ds.name}")
        year = f"{name[6]}{name[7]}{name[8]}{name[9]}"
        month = f"{name[10]}{name[11]}"
        day = f"{name[12]}{name[13]}"
        hour = f"{name[15]}{name[16]}"

        time = datetime(int(year), int(month), int(day), int(hour))

        df = df.dropna(subset=['latitude', 'longitude', 'air_temperature', 'dew_point_temperature', 'cloud_coverage', 'eastward_wind', 'northward_wind'])
        
        return df, time

class FEMS:

    r'''
    This class hosts functions to retrieve the latest fuels data from FEMS
    '''

    def get_single_station_data(station_id, number_of_days, start_date=None, end_date=None, fuel_model='Y', to_csv=True):

        r'''
        This function retrieves the dataframe for a single RAWS station in FEMS

        Required Arguments:

        1) station_id (Integer) - The WIMS or RAWS ID of the station. 

        2) number_of_days (Integer or String) - How many days the user wants the summary for (90 for 90 days).
           If the user wants to use a custom date range enter 'Custom' or 'custom' in this field. 

        Optional Arguments:

        1) start_date (String) - Default = None. The start date if the user wants to define a custom period. Enter as a string
           in the following format 'YYYY-mm-dd'

        2) end_date (String) - Default = None. The end date if the user wants to define a custom period. Enter as a string
           in the following format 'YYYY-mm-dd'

        3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
           Fuel Models List:

           Y - Timber
           X - Brush
           W - Grass/Shrub
           V - Grass
           Z - Slash

        4) to_csv (Boolean) - Default = True. This will save the data into a CSV file and build a directory to hold the CSV files. 

        Returns: A Pandas DataFrame of the NFDRS data from FEMS.            

        '''

        if number_of_days == 'Custom' or number_of_days == 'custom':

            df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?stationIds={str(station_id)}&endDate={end_date}Z&startDate={start_date}Z&dataFormat=csv&dataset=all&fuelModels={fuel_model}")    
        else:

            try:
                now = datetime.now(UTC)
            except Exception as e:
                now = datetime.utcnow()
                
            start = now - timedelta(days=number_of_days)
            
            df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?stationIds={str(station_id)}&endDate={now.strftime(f'%Y-%m-%d')}T{now.strftime(f'%H:%M:%S')}Z&startDate={start.strftime(f'%Y-%m-%d')}T{start.strftime(f'%H:%M:%S')}Z&dataFormat=csv&dataset=all&fuelModels={fuel_model}") 

        if to_csv == True:

            if os.path.exists(f"FEMS Data"):
                pass
            else:
                os.mkdir(f"FEMS Data")

            fname = f"{station_id} {number_of_days} Days Fuel Model {fuel_model}.csv"
            
            try:
                os.remove(f"FEMS Data/{fname}")
            except Exception as e:
                pass

            file = df.to_csv(fname, index=False)
            os.replace(f"{fname}", f"FEMS Data/{fname}")
        else:
            pass
        
        return df


    def get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date):

        r'''
        This function does the following:

        1) Downloads all the data for the Critical RAWS Stations for each GACC Region

        2) Builds the directory where the RAWS data CSV files will be hosted

        3) Saves the CSV files to the paths which are sorted by Predictive Services Area (PSA)

        Required Arguments:

        1) gacc_region (String) - The 4-letter GACC abbreviation

        2) number_of_years_for_averages (Integer) - The number of years for the average values to be calculated on. 

        3) fuel_model (String) - The fuel model being used. 
           Fuel Models List:

           Y - Timber
           X - Brush
           W - Grass/Shrub
           V - Grass
           Z - Slash 

        4) start_date (String) - If the user wishes to use a selected start date as the starting point enter the start_date
           as a string in the following format: YYYY-mm-dd

        Returns: The RAWS CSV data files sorted into the folders which are the different SIGs for each GACC
        '''

        gacc_region = gacc_region.upper()

        df_station_list = raws.get_sigs(gacc_region)

        try:
            now = datetime.now(UTC)
        except Exception as e:
            now = datetime.utcnow()

        if start_date == None:
            number_of_days = number_of_years_for_averages * 365
                
            start = now - timedelta(days=number_of_days)

        else:
            start_date = start_date
            
            year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
            month = f"{start_date[5]}{start_date[6]}"
            day = f"{start_date[8]}{start_date[9]}"

            year = int(year)
            month = int(month)
            day = int(day)

            start = datetime(year, month, day, 0, 0, 0)

        for station, psa in zip(df_station_list['RAWSID'], df_station_list['PSA Code']):
            
            df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr?stationIds={station}&endDate={now.strftime('%Y-%m-%dT%H:%M:%S')}Z&startDate={start.strftime('%Y-%m-%dT%H:%M:%S')}Z&dataFormat=csv&dataset=observation&fuelModels={fuel_model}")
                
            if os.path.exists(f"FEMS Data"):
                pass
            else:
                os.mkdir(f"FEMS Data")   

            if os.path.exists(f"FEMS Data/Stations"):
                pass
            else:
                os.mkdir(f"FEMS Data/Stations") 

            if os.path.exists(f"FEMS Data/Stations/{gacc_region}"):
                pass
            else:
                os.mkdir(f"FEMS Data/Stations/{gacc_region}") 

            if os.path.exists(f"FEMS Data/Stations/{gacc_region}/{psa}"):
                pass
            else:
                os.mkdir(f"FEMS Data/Stations/{gacc_region}/{psa}") 

            fname = f"{station}.csv"
    
            file = df.to_csv(fname, index=False)
            os.replace(f"{fname}", f"FEMS Data/Stations/{gacc_region}/{psa}/{fname}")


    def get_nfdrs_forecast_data(gacc_region, fuel_model):

        """
        This function retrieves the latest fuels forecast data from FEMS.

        Required Arguments:

        1) gacc_region (String) - The 4-letter GACC abbreviation

        2) fuel_model (String) - The fuel model being used. 
           Fuel Models List:

           Y - Timber
           X - Brush
           W - Grass/Shrub
           V - Grass
           Z - Slash 

        Returns: The RAWS CSV files with the fuels forecast data from FEMS.
        """
    
        gacc_region = gacc_region.upper()
        
        df_station_list = raws.get_sigs(gacc_region)
        
        try:
            start = datetime.now(UTC)
        except Exception as e:
            start = datetime.utcnow()
    
        end = start + timedelta(days=7)
    
        for station, psa in zip(df_station_list['RAWSID'], df_station_list['PSA Code']):
            df = pd.read_csv(f"https://fems.fs2c.usda.gov/api/climatology/download-nfdr-daily-summary/?dataset=forecast&startDate={start.strftime('%Y-%m-%d')}&endDate={end.strftime('%Y-%m-%d')}&dataFormat=csv&stationIds={station}&fuelModels={fuel_model}")
    
            if os.path.exists(f"FEMS Data"):
                pass
            else:
                os.mkdir(f"FEMS Data")   
    
            if os.path.exists(f"FEMS Data/Forecasts"):
                pass
            else:
                os.mkdir(f"FEMS Data/Forecasts") 
    
            if os.path.exists(f"FEMS Data/Forecasts/{gacc_region}"):
                pass
            else:
                os.mkdir(f"FEMS Data/Forecasts/{gacc_region}") 
    
            if os.path.exists(f"FEMS Data/Forecasts/{gacc_region}/{psa}"):
                pass
            else:
                os.mkdir(f"FEMS Data/Forecasts/{gacc_region}/{psa}") 
    
            fname = f"{station}.csv"
    
            file = df.to_csv(fname, index=False)
            os.replace(f"{fname}", f"FEMS Data/Forecasts/{gacc_region}/{psa}/{fname}")


