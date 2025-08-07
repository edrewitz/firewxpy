"""
This class hosts the functions that return forecast model data from various different sources. 

(C) Eric J. Drewitz 2025
"""

import xarray as xr
import netCDF4
import urllib.request
import os
import sys
import logging
import firewxpy.utils.standard as standard
import warnings
warnings.filterwarnings('ignore')

from firewxpy.utils.settings import coords_for_forecast_model_data

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

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