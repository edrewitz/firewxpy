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
import pygrib
import xarray as xr
import metpy
import metpy.calc as mpcalc
import firewxpy.parsers as parsers
import pandas as pd
import cartopy.crs as ccrs
import requests
import firewxpy.calc as calc
import numpy as np
import netCDF4
import time as t
import firewxpy.standard as standard
import warnings
warnings.filterwarnings('ignore')

from ftplib import FTP
from siphon.catalog import TDSCatalog
from metpy.cbook import get_test_data
from io import StringIO
from metpy.io import parse_metar_file
from metpy.units import units, pandas_dataframe_to_unit_arrays
from dateutil import tz
from datetime import datetime, timedelta

class info:

    r'''

    This class hosts all the functions that are used if an error message is needed to be returned. 
    Each error message function returns detailed instructions to the user so they do not need to look for the proper syntax for a parameter or a directory. 

    '''

    def directory_name_error():
        error_msg = f"""
    
        WARNING: USER ENTERED AN INVALID DIRECTORY NAME
    
        HERE IS THE URL FOR THE NOAA/NWS FTP SERVER WEBSITE: https://tgftp.nws.noaa.gov/
    
        HERE IS THE LIST OF VALID DIRECTORY NAMES ***NOTE USER STILL NEEDS TO ENTER THE LAST PORTION OF THE DIRECTORY NAME***
        
        AN EXAMPLE OF THE LAST PORTION OF A DIRECTORY NAME IS AS FOLLOWS: /VP.001-003/
    
        FULL DIRECTORY NAME LIST:
    
        ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
        CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
        CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
        CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
        CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
        CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
        EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
        GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
        HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
        MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
        NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
        NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
        NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
        NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
        NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
        OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
        PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
        PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
        PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
        SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
        SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
        SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
        SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
        UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
        
        """
        print(error_msg)
    
    def directory_list():
        dir_list = f"""
        
        FULL DIRECTORY NAME LIST:
            
        ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
        CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
        CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
        CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
        CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
        CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
        EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
        GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
        HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
        MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
        NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
        NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
        NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
        NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
        NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
        OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
        PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
        PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
        PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
        SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
        SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
        SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
        SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
        UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
        
        """
        print(dir_list)
    
    
    def parameter_name_error():
        error_msg = f"""
    
        WARNING - THIS ERROR COULD BE ATTRIBUTED TO EITHER OF THE FOLLOWING:

        1) USER ENTERED AN INVALID PARAMETER NAME

        2) USER SCHEDULED THE SCRIPT TO RUN BETWEEN THE 17TH AND 47TH MINUTE OF THE HOUR
    
        FOR THE FULL LIST OF PARAMETER NAMES VISIT THE FOLLOWING LINK:
    
        https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
    
        """
        print(error_msg)
    
    
    def parameter_list():
        param_list = f"""
    
        FOR THE FULL LIST OF PARAMETERS, PLEASE VISIT THE FOLLOWING LINK:
    
        https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
    
        """
        print(param_list)
    
    def invalid_element():
        error_msg = f"""
    
        WARNING: USER ENTERED INVALID SYNTAX FOR THE FORECAST PARAMETER.
    
        VISIT THIS LINK FOR THE FULL LIST OF ALL FORECAST PARAMETERS IN THE PROPER SYNTAX
    
        https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/NDFD/NWS/CONUS/CONDUIT/Best.html
    
        """
        print(error_msg)

    def syntax_error():
        error_msg = f"""
    
        WARNING: DATA COULD NOT BE RETRIEVED. 
    
        THIS IS DUE TO A LIKELY SYNTAX ERROR. 
    
        THIS IS MOST LIKELY DUE TO THE PARAMETER BEING DEFINED WITH INCORRECT SYNTAX
    
        FOR THE FULL OPENDAP LIST OF PARAMETERS FOR REAL TIME MESOSCALE ANALYSIS DATA VISIT
    
        https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html
    
        """
    
        print(error_msg)


    def invalid_parameter_NOMADS_RTMA_Alaska():
        error_msg = f"""

        WARNING: USER ENTERED AN INVALID PARAMETER NAME

        HERE IS THE LIST OF VALID PARAMETER NAMES FOR ALASKA RTMA DATA

        Variables:
            (total of 13)
             
            ceilceil
            ** cloud ceiling ceiling [m]
             
            dpt2m
            ** 2 m above ground dew point temperature [k]
             
            gust10m
            ** 10 m above ground wind speed (gust) [m/s]
             
            hgtsfc
            ** surface geopotential height [gpm]
             
            pressfc
            ** surface pressure [pa]
             
            spfh2m
            ** 2 m above ground specific humidity [kg/kg]
             
            tcdcclm
            ** entire atmosphere (considered as a single layer) total cloud cover [%]
             
            tmp2m
            ** 2 m above ground temperature [k]
             
            ugrd10m
            ** 10 m above ground u-component of wind [m/s]
             
            vgrd10m
            ** 10 m above ground v-component of wind [m/s]
             
            vissfc
            ** surface visibility [m]
             
            wdir10m
            ** 10 m above ground wind direction (from which blowing) [degtrue]
             
            wind10m
            ** 10 m above ground wind speed [m/s]

        """
        print(error_msg)

class RTMA_Alaska:

    r'''
    
    This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data for Alaska. 

    This class hosts the functions the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''

    def get_RTMA_dataset(current_time):
    
        r'''
    
        This function retrieves the latest RTMA Dataset for the user. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Argument: 1) Current Time in UTC

        Returns: 1) The latest 2.5km x 2.5km RTMA Dataset

                 2) The time corresponding to the dataset
    
        '''
        
        times = []
        for i in range(0, 5):
            time = pd.to_datetime(current_time - timedelta(hours=i))
            times.append(time)
    
        url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
        url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
        url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
        url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
        url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'
    
        try:
            ds = xr.open_dataset(url_0, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
            print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
            strtime = times[0]
            return ds, strtime
            
        except Exception as a:
            try:
                print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                ds = xr.open_dataset(url_1, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                strtime = times[1]
                return ds, strtime
                
            except Exception as b:
                    try:
                        print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                        ds = xr.open_dataset(url_2, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                        print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                        strtime = times[2]
                        return ds, strtime
                        
                    except Exception as c:
                        try:
                            print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_3, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                            print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                            strtime = times[3]
                            return ds, strtime
                        except Exception as d:
    
                            try:
                                print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_4, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                strtime = times[4]
                                return ds, strtime
                                
                            except Exception as e:
                                print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
    
            
        except Exception as f:
            error = info.invalid_parameter_NOMADS_RTMA_Alaska()
            print(error)


    def get_RTMA_24_hour_comparison_datasets(current_time):
    
        r'''
        
        This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user for Alaska. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Argument: 1) Current Time in UTC

        Returns: 1) The latest 2.5km x 2.5km RTMA Dataset

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
    
        try:
            ds = xr.open_dataset(url_0, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
            print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
            ds_24 = xr.open_dataset(url_5, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
            print("Data was successfully retrieved for " + new_times[0].strftime('%m/%d/%Y %HZ'))
            strtime = times[0]
            strtime_24 = new_times[0]
            return ds, ds_24, strtime, strtime_24
            
        except Exception as a:
            try:
                print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                ds = xr.open_dataset(url_1, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_6, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                print("Data was successfully retrieved for " + new_times[1].strftime('%m/%d/%Y %HZ'))
                strtime = times[1]
                strtime_24 = new_times[1]
                return ds, ds_24, strtime, strtime_24
                
            except Exception as b:
                    try:
                        print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                        ds = xr.open_dataset(url_2, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                        print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                        ds_24 = xr.open_dataset(url_7, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                        print("Data was successfully retrieved for " + new_times[2].strftime('%m/%d/%Y %HZ'))
                        strtime = times[2]
                        strtime_24 = new_times[2]
                        return ds, ds_24, strtime, strtime_24
                        
                    except Exception as c:
                        try:
                            print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_3, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                            print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_8, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                            print("Data was successfully retrieved for " + new_times[3].strftime('%m/%d/%Y %HZ'))
                            strtime = times[3]
                            strtime_24 = new_times[3]
                            return ds, ds_24, strtime, strtime_24
                            
                        except Exception as d:
    
                            try:
                                print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_4, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_9, engine='netcdf4').sel(lon=slice(360-180, 360-120, 2), lat=slice(50, 72, 2)) 
                                print("Data was successfully retrieved for " + new_times[4].strftime('%m/%d/%Y %HZ'))
                                strtime = times[4]
                                strtime_24 = new_times[4]
                                return ds, ds_24, strtime, strtime_24
                                
                            except Exception as e:
                                print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
    
            
        except Exception as f:
            error = info.invalid_parameter_NOMADS_RTMA_Alaska()
            print(error)


class RTMA_Hawaii:

    r'''
    
    This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data for CONUS. 

    This class hosts the functions the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''

    def get_RTMA_dataset(current_time):
    
        r'''
    
        This function retrieves the latest RTMA Dataset for the user. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Argument: 1) Current Time in UTC

        Returns: 1) The latest 2.5km x 2.5km RTMA Dataset

                 2) The time corresponding to the dataset
    
        '''
        
        times = []
        for i in range(0, 5):
            time = pd.to_datetime(current_time - timedelta(hours=i))
            times.append(time)
    
        url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
        url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
        url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
        url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
        url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'
    
        try:
            ds = xr.open_dataset(url_0, engine='netcdf4')
            print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
            strtime = times[0]
            return ds, strtime
            
        except Exception as a:
            try:
                print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                ds = xr.open_dataset(url_1, engine='netcdf4')
                print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                strtime = times[1]
                return ds, strtime
                
            except Exception as b:
                    try:
                        print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                        ds = xr.open_dataset(url_2, engine='netcdf4')
                        print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                        strtime = times[2]
                        return ds, strtime
                        
                    except Exception as c:
                        try:
                            print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_3, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                            strtime = times[3]
                            return ds, strtime
                        except Exception as d:
    
                            try:
                                print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_4, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                strtime = times[4]
                                return ds, strtime
                                
                            except Exception as e:
                                print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
    
            
        except Exception as f:
            error = info.invalid_parameter_NOMADS_RTMA_Alaska()
            print(error)
    
    
    def get_RTMA_24_hour_comparison_datasets(current_time):
    
        r'''
        
        This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Argument: 1) Current Time in UTC

        Returns: 1) The latest 2.5km x 2.5km RTMA Dataset

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
    
        try:
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
            error = info.invalid_parameter_NOMADS_RTMA_Alaska()
            print(error)


class RTMA_CONUS:

    r'''
    
    This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

    This class hosts the functions the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''

    def get_RTMA_dataset(current_time):
    
        r'''
    
        This function retrieves the latest RTMA Dataset for the user. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Argument: 1) Current Time in UTC

        Returns: 1) The latest 2.5km x 2.5km RTMA Dataset

                 2) The time corresponding to the dataset
    
        '''
        
        times = []
        for i in range(0, 5):
            time = pd.to_datetime(current_time - timedelta(hours=i))
            times.append(time)
    
        url_0 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[0].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[0].strftime('%H')+'z'
        url_1 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[1].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[1].strftime('%H')+'z'
        url_2 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[2].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[2].strftime('%H')+'z'
        url_3 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[3].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[3].strftime('%H')+'z'
        url_4 = 'http://nomads.ncep.noaa.gov:80/dods/rtma2p5/rtma2p5'+times[4].strftime('%Y%m%d')+'/rtma2p5_anl_'+times[4].strftime('%H')+'z'
    
        try:
            ds = xr.open_dataset(url_0, engine='netcdf4')
            print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
            strtime = times[0]
            return ds, strtime
            
        except Exception as a:
            try:
                print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                ds = xr.open_dataset(url_1, engine='netcdf4')
                print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                strtime = times[1]
                return ds, strtime
                
            except Exception as b:
                    try:
                        print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                        ds = xr.open_dataset(url_2, engine='netcdf4')
                        print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                        strtime = times[2]
                        return ds, strtime
                        
                    except Exception as c:
                        try:
                            print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_3, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                            strtime = times[3]
                            return ds, strtime
                        except Exception as d:
    
                            try:
                                print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_4, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                strtime = times[4]
                                return ds, strtime
                                
                            except Exception as e:
                                print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
    
            
        except Exception as f:
            error = info.invalid_parameter_NOMADS_RTMA_Alaska()
            print(error)
    
    
    def get_RTMA_24_hour_comparison_datasets(current_time):
    
        r'''
        
        This function retrieves the latest RTMA Dataset and the RTMA Dataset for 24-Hours prior to the current dataset for the user. 

        Data Source: NOAA/NCEP/NOMADS (https://nomads.ncep.noaa.gov/)

        Required Argument: 1) Current Time in UTC

        Returns: 1) The latest 2.5km x 2.5km RTMA Dataset

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
            error = info.invalid_parameter_NOMADS_RTMA_Alaska()
            print(error)


    def RTMA_Relative_Humidity_Synced_With_METAR(current_time, mask):
    
        r'''

        This function retrieves the latest RTMA Relative Humidity Dataset and METAR Dataset for the user. 

        Data Source: UCAR/THREDDS (https://thredds.ucar.edu/)

        Required Argument: 1) Current Time in UTC

                           2) (Mask) Minimum radius allowed between points. If units are not provided, meters is assumed. 

        Returns: A list of all the aformentioned data:

                 RTMA RH Data = data[0]
                 The time corresponding to the dataset = data[1]
                 Surface METAR Data = data[2]
                 METAR u-component of wind (kt) = data[3]
                 METAR v-component of wind (kt) = data[4]
                 METAR RH Data = data[5]
                 Mask (Minimum radius allowed between points) = data[6]
                 Time of METAR Observations = data[7]
                 Projection for the data = data[8]     
        
        '''
    
        current_time = current_time
        mask = mask
    
        metar_time = latest_metar_time(current_time)
    
        rtma_data, rtma_time = get_current_rtma_relative_humidity_data(current_time)
    
        plot_projection = rtma_data.metpy.cartopy_crs
        
        new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(rtma_time, metar_time)
    
        sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised = get_METAR_Data(new_metar_time, plot_projection, mask)
    
        data = []
        data.append(rtma_data)
        data.append(rtma_time)
        data.append(sfc_data)
        data.append(sfc_data_u_kt)
        data.append(sfc_data_v_kt)
        data.append(sfc_data_rh)
        data.append(sfc_data_mask)
        data.append(metar_time_revised)
        data.append(plot_projection)
    
        return data

    def RTMA_Synced_With_METAR(parameter, current_time, mask):
    
        r'''
        This function is the recommended method to download the Real Time Mesoscale Analysis dataset with the METAR dataset as this function syncs the time of the
        latest available Real Time Mesoscale Analysis dataset with the latest available complete METAR dataset. 
    
        Inputs: 1) parameter (String) - The weather parameter the user wishes to download. 
                                       To find the full list of parameters, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html
    
                2) current_time (Datetime) - Current date and time in UTC. 
                3) mask (Integer) - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed. 
        
        Returns: 1) rtma_data - The latest avaiable Real Time Mesoscale Analysis dataset
                 2) rtma_time - The time of the latest avaiable Real Time Mesoscale Analysis dataset
                 3) sfc_data - The entire METAR dataset. 
                 4) sfc_data_u_kt - The u-component (west-east) of the wind velocity in knots. 
                 5) sfc_data_v_kt - The v-component (north-south) of the wind velocity in knots. 
                 6) sfc_data_rh - The relative humidity in the METAR dataset. 
                 7) sfc_data_mask - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed.
                 8) metar_time_revised - The corrected time (if needed) for the latest complete METAR dataset. 
                 9) plot_projection - The coordinate reference system of the data being plotted. This is usually PlateCarree.
        '''
    
        parameter = parameter
        current_time = current_time
        mask = mask
    
        metar_time = latest_metar_time(current_time)
    
        rtma_data, rtma_time = RTMA_CONUS.get_current_rtma_data(current_time, parameter)
    
        plot_projection = rtma_data.metpy.cartopy_crs
        
        new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(rtma_time, metar_time)
    
        sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised = get_METAR_Data(new_metar_time, plot_projection, mask)
        data = []
        data.append(rtma_data)
        data.append(rtma_time)
        data.append(sfc_data)
        data.append(sfc_data_u_kt)
        data.append(sfc_data_v_kt)
        data.append(sfc_data_rh)
        data.append(sfc_data_mask)
        data.append(metar_time_revised)
        data.append(plot_projection)
    
        return data


    def get_current_rtma_data(current_time, parameter):
    
        r"""
        This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis for any available parameter. 
    
        Inputs:
               1) current_time (Datetime) - Current time in UTC.
               2) parameter (String) - The weather parameter the user wishes to download. 
                                       To find the full list of parameters, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html
    
        Returns: 1) If there are zero errors, the latest dataset and the time of the dataset for the requested parameter will be returned. 
                 2) If there is an error, an error message is returned. 
    
        """
    
        times = []
    
        for i in range(0,5):
            new_time = current_time - timedelta(hours=i)
            times.append(new_time)
    
        try:
            main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
            main_server_status = main_server_response.status_code
        except Exception as a:
            pass
            
        try:
            first_backup_server_response = requests.get("https://thredds-test.unidata.ucar.edu/thredds/catalog/catalog.xml")
            first_backup_server_status = first_backup_server_response.status_code
        except Exception as b:
            pass
         
        try:
            second_backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
            second_backup_server_status = second_backup_server_response.status_code
        except Exception as c:
            pass
    
        if main_server_status == 200:
            print("Main UCAR THREDDS Server is online. Connecting!")
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter = rtma_data[parameter].squeeze()
    
                print("Data retrieval for " + current_time.strftime('%m/%d/%Y %H00 UTC') + " is successful")
                
                return rtma_parameter, current_time
                
            except Exception as e:
        
                print(parameter + " Data is unavailiable for "+current_time.strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[0].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter = rtma_data[parameter].squeeze()
                    time = times[0]
        
                    print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    return rtma_parameter, time
        
                except Exception as a:
        
                    print(parameter + " Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
                   
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter = rtma_data[parameter].squeeze()
                        time = times[1]
            
                        print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        return rtma_parameter, time
        
        
                    except Exception as b:
                                    
                        print(parameter + " Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
        
                        try:
                            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter = rtma_data[parameter].squeeze()
                            time = times[2]
            
                            print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                            return rtma_parameter, time
        
                        except Exception as c:
                                    
                            print(parameter + " Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
        
                            try:
                                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                                rtma_parameter = rtma_data[parameter].squeeze()
                                time = times[3]
                
                                print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                                return rtma_parameter, time
                            
                        
                            except syntaxError as k:
                                error = info.syntax_error()
        
                                return error
    
        if main_server_status != 200 and first_backup_server_status == 200:
            print("Main UCAR THREDDS Server is down. Connected to the first backup UCAR THREDDS Server!")
            try:
                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter = rtma_data[parameter].squeeze()
    
                print("Data retrieval for " + current_time.strftime('%m/%d/%Y %H00 UTC') + " is successful")
                
                return rtma_parameter, current_time
                
            except Exception as e:
        
                print(parameter + " Data is unavailiable for "+current_time.strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[0].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter = rtma_data[parameter].squeeze()
                    time = times[0]
        
                    print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    return rtma_parameter, time
        
                except Exception as a:
        
                    print(parameter + " Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
                   
                    try:
                        rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter = rtma_data[parameter].squeeze()
                        time = times[1]
            
                        print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        return rtma_parameter, time
        
        
                    except Exception as b:
                                    
                        print(parameter + " Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter = rtma_data[parameter].squeeze()
                            time = times[2]
            
                            print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                            return rtma_parameter, time
        
                        except Exception as c:
                                    
                            print(parameter + " Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
        
                            try:
                                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                                rtma_parameter = rtma_data[parameter].squeeze()
                                time = times[3]
                
                                print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                                return rtma_parameter, time
                            
                        
                            except syntaxError as k:
                                error = info.syntax_error()
        
                                return error
    
        if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status == 200:
    
            print("Main UCAR THREDDS Server is down. Connected to the second backup UCAR THREDDS Server!")
            try:
                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter = rtma_data[parameter].squeeze()
    
                print("Data retrieval for " + current_time.strftime('%m/%d/%Y %H00 UTC') + " is successful")
                
                return rtma_parameter, current_time
                
            except Exception as e:
        
                print(parameter + " Data is unavailiable for "+current_time.strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[0].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter = rtma_data[parameter].squeeze()
                    time = times[0]
        
                    print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    return rtma_parameter, time
        
                except Exception as a:
        
                    print(parameter + " Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
                   
                    try:
                        rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter = rtma_data[parameter].squeeze()
                        time = times[1]
            
                        print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        return rtma_parameter, time
        
        
                    except Exception as b:
                                    
                        print(parameter + " Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter = rtma_data[parameter].squeeze()
                            time = times[2]
            
                            print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                            return rtma_parameter, time
        
                        except Exception as c:
                                    
                            print(parameter + " Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
        
                            try:
                                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                                rtma_parameter = rtma_data[parameter].squeeze()
                                time = times[3]
                
                                print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                                return rtma_parameter, time
                            
                        
                            except syntaxError as k:
                                error = info.syntax_error()
        
                                return error
            
            print("Unable to connect to either the main or backup servers. Aborting!")
    
        if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status != 200:
            print("Unable to connect to either the main or backup servers. Aborting!")


class NDFD_CONUS:

    r'''

    This class hosts the active function that downloads the NOAA/NWS/NDFD Gridded Data. 

    This class hosts the function the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''

    def download_NDFD_grids(directory_name, parameter):

        r'''

        This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

        Scripts that download files from the CONUS directory are recommended to be run between the 48th and 15th 
        minute to avoid the script idiling. The reason is because the files in the CONUS directory update between the 15th
        and 48th minute of the hour (and downloading them during that time makes them extremely hard to work with!!). Due
        to this, if there is an issue with the data, the program will automatically idle until the 48th minute and resume and try again to download the latest data. 

        Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

        Required Arguments: 1) The name of the directory (see FireWxPy documentation for directory paths)

                            2) The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

        Returns: 1) The files holding the forecast data in a GRIB2 format. 

                 2) An xarray data-array of the same forecast data. 

                 3) The count of the number of files in the short-term forecast period. 

                 4) The count of the number of files in the extended forecast period. 

        '''
    
        directory_name = directory_name
        parameter = parameter
    
        try:
    
            grbs, ds, count_short, count_extended = get_NWS_NDFD_7_Day_grid_data(directory_name, parameter)
    
            print("Downloaded data successfully!")
        except Exception as a:
    
            standard.idle()
    
            print("Trying again to download data...")
    
            grbs, ds, count_short, count_extended = get_NWS_NDFD_7_Day_grid_data(directory_name, parameter)
    
            print("Downloaded data successfully!")
    
        return grbs, ds, count_short, count_extended


    def download_short_term_NDFD_grids(directory_name, parameter):

        r'''

        This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

        Scripts that download files from the CONUS directory are recommended to be run between the 48th and 15th 
        minute to avoid the script idiling. The reason is because the files in the CONUS directory update between the 15th
        and 48th minute of the hour (and downloading them during that time makes them extremely hard to work with!!). Due
        to this, if there is an issue with the data, the program will automatically idle until the 48th minute and resume and try again to download the latest data. 

        Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

        Required Arguments: 1) The name of the directory (see FireWxPy documentation for directory paths)

                            2) The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

        Returns: 1) The files holding the forecast data in a GRIB2 format. 

                 2) An xarray data-array of the same forecast data. 

                 3) The count of the number of files in the short-term forecast period. 

                 4) The count of the number of files in the extended forecast period. 

        '''
    
        directory_name = directory_name
        parameter = parameter
    
        try:
    
            ds = get_NWS_NDFD_short_term_grid_data(directory_name, parameter)
    
            print("Downloaded data successfully!")
        except Exception as a:
    
            standard.idle()
    
            print("Trying again to download data...")
    
            ds = get_NWS_NDFD_short_term_grid_data(directory_name, parameter)
    
            print("Downloaded data successfully!")
    
        return ds

    def download_extended_NDFD_grids(directory_name, parameter):

        r'''

        This function retrieves the latest NWS Forecast (NDFD) files from the NWS FTP Server. 

        Scripts that download files from the CONUS directory are recommended to be run between the 48th and 15th 
        minute to avoid the script idiling. The reason is because the files in the CONUS directory update between the 15th
        and 48th minute of the hour (and downloading them during that time makes them extremely hard to work with!!). Due
        to this, if there is an issue with the data, the program will automatically idle until the 48th minute and resume and try again to download the latest data. 

        Data Source: NOAA/NWS/NDFD (tgftp.nws.noaa.gov)

        Required Arguments: 1) The name of the directory (see FireWxPy documentation for directory paths)

                            2) The parameter that the user wishes to download. (i.e. ds.maxt.bin for max temperature)

        Returns: 1) The files holding the forecast data in a GRIB2 format. 

                 2) An xarray data-array of the same forecast data. 

                 3) The count of the number of files in the short-term forecast period. 

                 4) The count of the number of files in the extended forecast period. 

        '''
    
        directory_name = directory_name
        parameter = parameter
    
        try:
    
            ds = get_NWS_NDFD_extended_grid_data(directory_name, parameter)
    
            print("Downloaded data successfully!")
        except Exception as a:
    
            standard.idle()
    
            print("Trying again to download data...")
    
            ds = get_NWS_NDFD_extended_grid_data(directory_name, parameter)
    
            print("Downloaded data successfully!")
    
        return ds

class NDFD_Alaska:

    r'''

    This class hosts the active function that downloads the NOAA/NWS/NDFD Gridded Data for Alaska. 

    This class hosts the function the users will import and call if the users wish to download the data outside of the 
    plotting function and pass the data into the plotting function.
    
    This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

    '''    

    def get_short_and_extended_grids(parameter):
        
        '''
                 This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
                 This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
        
                 Inputs:

                    1) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                            Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                            https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
        
                Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                         This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
                 
        '''
    
        ###################################################
        # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
        ###################################################

        parameter = parameter

        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'

        ds_short = NDFD_Alaska.get_NWS_NDFD_short_term_grid_data(directory_name, parameter)
        print("Retrieved the short-term Alaska grids.")
        ds_extended = NDFD_Alaska.get_NWS_NDFD_extended_grid_data(directory_name, parameter)
        print("Retrieved the extended Alaska grids.")

        return ds_short, ds_extended
    


    def get_NWS_NDFD_7_Day_grid_data(parameter):
        
        '''
                 This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
                 This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
        
                 Inputs:

                    1) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                            Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                            https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
        
                Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                         This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
                 
        '''
    
        ###################################################
        # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
        ###################################################
    
        ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
        ftp = FTP('tgftp.nws.noaa.gov')
        ftp.login()

        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/'
    
        ### SEARCHES FOR THE CORRECT DIRECTORY ###
        try:
            dirName_short = directory_name + 'VP.001-003/'
            param = parameter
            files = ftp.cwd(dirName_short)
    
            ### SEARCHES FOR THE CORRECT PARAMETER ###
            try:
                ################################
                # DOWNLOADS THE NWS NDFD GRIDS #
                ################################
                
                with open(param, 'wb') as fp:
                    ftp.retrbinary('RETR ' + param, fp.write)
    
                dirName_extended = directory_name + 'VP.004-007/'
                param = parameter
                files = ftp.cwd(dirName_extended)
    
                with open(param, 'ab') as fp:
                    ftp.retrbinary('RETR ' + param, fp.write)
                
                ftp.close()
    
                
                #########################
                # DATA ARRAYS PARAMETER #
                #########################
                ds = xr.load_dataset(param, engine='cfgrib')
                ds = ds.metpy.parse_cf()
                return ds
    
            ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###
    
            except Exception as a:
                param_error = info.parameter_name_error()
                return param_error
    
        ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
            
        except Exception as e:
            dir_error = info.directory_name_error()
            return dir_error


    def get_NWS_NDFD_short_term_grid_data(directory_name, parameter):
        
        '''
                 This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
                 This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
        
                 Inputs:
                     1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                                  The directory determines the domain the forecast data is valid for. 
                                                  Here is the full directory list: 
                                                                            ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
                                                                            CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
                                                                            CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
                                                                            CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
                                                                            CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
                                                                            CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
                                                                            EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
                                                                            GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
                                                                            HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
                                                                            MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
                                                                            NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
                                                                            NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
                                                                            NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
                                                                            NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
                                                                            NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
                                                                            OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
                                                                            PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
                                                                            PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
                                                                            PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
                                                                            SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
                                                                            SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
                                                                            SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
                                                                            SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
                                                                            UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
        
        
                    2) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                            Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                            https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
        
                Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                         This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
                 
        '''
    
        ###################################################
        # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
        ###################################################
    
        ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
        ftp = FTP('tgftp.nws.noaa.gov')
        ftp.login()
    
        ### SEARCHES FOR THE CORRECT DIRECTORY ###
        try:
            dirName = directory_name + 'VP.001-003/'
            param = parameter
            files = ftp.cwd(dirName)
    
            ### SEARCHES FOR THE CORRECT PARAMETER ###
            try:
                ################################
                # DOWNLOADS THE NWS NDFD GRIDS #
                ################################
                
                with open(param, 'wb') as fp:
                    ftp.retrbinary('RETR ' + param, fp.write)
                    
                ftp.close()
                ds = xr.load_dataset(param, engine='cfgrib').sel(x=slice(20, 1400, 2), y=slice(100, 1400, 2)) 
                ds = ds.metpy.parse_cf()
                return ds
    
            ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###
    
            except Exception as a:
                param_error = info.parameter_name_error()
                return param_error
    
        ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
            
        except Exception as e:
            dir_error = info.directory_name_error()
            return dir_error
    
    def get_NWS_NDFD_extended_grid_data(directory_name, parameter):
        
        '''
                 This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
                 This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
        
                 Inputs:
                     1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                                  The directory determines the domain the forecast data is valid for. 
                                                  Here is the full directory list: 
                                                                            ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
                                                                            CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
                                                                            CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
                                                                            CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
                                                                            CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
                                                                            CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
                                                                            EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
                                                                            GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
                                                                            HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
                                                                            MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
                                                                            NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
                                                                            NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
                                                                            NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
                                                                            NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
                                                                            NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
                                                                            OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
                                                                            PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
                                                                            PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
                                                                            PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
                                                                            SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
                                                                            SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
                                                                            SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
                                                                            SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
                                                                            UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
        
        
                    2) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                            Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                            https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
        
                Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                         This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
                 
        '''
    
        ###################################################
        # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
        ###################################################
    
        ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
        ftp = FTP('tgftp.nws.noaa.gov')
        ftp.login()
    
        ### SEARCHES FOR THE CORRECT DIRECTORY ###
        try:
            dirName = directory_name + 'VP.004-007/'
            param = parameter
            files = ftp.cwd(dirName)
    
            ### SEARCHES FOR THE CORRECT PARAMETER ###
            try:
                ################################
                # DOWNLOADS THE NWS NDFD GRIDS #
                ################################
                
                with open(param, 'wb') as fp:
                    ftp.retrbinary('RETR ' + param, fp.write)
    
                ftp.close()
                ds = xr.load_dataset(param, engine='cfgrib').sel(x=slice(20, 1400, 2), y=slice(100, 1400, 2)) 
                ds = ds.metpy.parse_cf()
                return ds
    
            ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###
    
            except Exception as a:
                param_error = info.parameter_name_error()
                return param_error
    
        ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
            
        except Exception as e:
            dir_error = info.directory_name_error()
            return dir_error

def get_NWS_NDFD_7_Day_grid_data(directory_name, parameter):
    
    '''
             This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
             This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
    
             Inputs:
                 1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                              The directory determines the domain the forecast data is valid for. 
                                              Here is the full directory list: 
                                                                        ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
                                                                        CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
                                                                        CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
                                                                        CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
                                                                        CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
                                                                        CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
                                                                        EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
                                                                        GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
                                                                        HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
                                                                        MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
                                                                        NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
                                                                        NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
                                                                        NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
                                                                        NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
                                                                        NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
                                                                        OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
                                                                        PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
                                                                        PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
                                                                        PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
                                                                        SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
                                                                        SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
                                                                        SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
                                                                        SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
                                                                        UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
    
    
                2) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                        Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                        https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
    
            Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                     This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
             
    '''

    ###################################################
    # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
    ###################################################

    ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
    ftp = FTP('tgftp.nws.noaa.gov')
    ftp.login()

    ### SEARCHES FOR THE CORRECT DIRECTORY ###
    try:
        dirName_short = directory_name + 'VP.001-003/'
        param = parameter
        files = ftp.cwd(dirName_short)

        ### SEARCHES FOR THE CORRECT PARAMETER ###
        try:
            ################################
            # DOWNLOADS THE NWS NDFD GRIDS #
            ################################
            
            with open(param, 'wb') as fp:
                ftp.retrbinary('RETR ' + param, fp.write)

            grbs_short = pygrib.open(param)
            grbs_short.seek(0)
            count_short = 0
            for grb in grbs_short:
                count_short = count_short + 1

            dirName_extended = directory_name + 'VP.004-007/'
            param = parameter
            files = ftp.cwd(dirName_extended)

            with open(param, 'ab') as fp:
                ftp.retrbinary('RETR ' + param, fp.write)
            
            ftp.close()

            
            #########################
            # DATA ARRAYS PARAMETER #
            #########################
            grbs = pygrib.open(param)
            grbs.seek(0)
            count = 0
            for grb in grbs:
                count = count + 1
            count_extended = count - count_short
            ds = xr.load_dataset(param, engine='cfgrib')
            ds = ds.metpy.parse_cf()
            return grbs, ds, count_short, count_extended

        ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###

        except Exception as a:
            param_error = info.parameter_name_error()
            return param_error

    ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
        
    except Exception as e:
        dir_error = info.directory_name_error()
        return dir_error


def get_NWS_NDFD_short_term_grid_data(directory_name, parameter):
    
    '''
             This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
             This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
    
             Inputs:
                 1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                              The directory determines the domain the forecast data is valid for. 
                                              Here is the full directory list: 
                                                                        ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
                                                                        CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
                                                                        CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
                                                                        CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
                                                                        CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
                                                                        CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
                                                                        EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
                                                                        GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
                                                                        HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
                                                                        MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
                                                                        NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
                                                                        NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
                                                                        NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
                                                                        NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
                                                                        NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
                                                                        OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
                                                                        PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
                                                                        PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
                                                                        PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
                                                                        SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
                                                                        SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
                                                                        SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
                                                                        SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
                                                                        UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
    
    
                2) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                        Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                        https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
    
            Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                     This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
             
    '''

    ###################################################
    # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
    ###################################################

    ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
    ftp = FTP('tgftp.nws.noaa.gov')
    ftp.login()

    ### SEARCHES FOR THE CORRECT DIRECTORY ###
    try:
        dirName = directory_name + 'VP.001-003/'
        param = parameter
        files = ftp.cwd(dirName)

        ### SEARCHES FOR THE CORRECT PARAMETER ###
        try:
            ################################
            # DOWNLOADS THE NWS NDFD GRIDS #
            ################################
            
            with open(param, 'wb') as fp:
                ftp.retrbinary('RETR ' + param, fp.write)
                
            ftp.close()
            ds = xr.load_dataset(param, engine='cfgrib')
            ds = ds.metpy.parse_cf()
            return ds

        ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###

        except Exception as a:
            param_error = info.parameter_name_error()
            return param_error

    ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
        
    except Exception as e:
        dir_error = info.directory_name_error()
        return dir_error

def get_NWS_NDFD_extended_grid_data(directory_name, parameter):
    
    '''
             This function connects to the National Weather Service FTP Server and returns the forecast data for the parameter of interest in a GRIB2 file.
             This function is specifically for downloading the entire National Weather Service Forecast (Days 1-7) Forecast grids. 
    
             Inputs:
                 1) directory_name (String) - The directory name is the complete filepath on the National Weather Service FTP server. 
                                              The directory determines the domain the forecast data is valid for. 
                                              Here is the full directory list: 
                                                                        ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
                                                                        CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
                                                                        CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
                                                                        CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
                                                                        CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
                                                                        CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
                                                                        EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
                                                                        GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
                                                                        HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
                                                                        MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
                                                                        NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
                                                                        NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
                                                                        NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
                                                                        NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
                                                                        NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
                                                                        OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
                                                                        PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
                                                                        PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
                                                                        PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
                                                                        SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
                                                                        SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
                                                                        SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
                                                                        SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
                                                                        UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
    
    
                2) parameter (String) - The parameter corresponds to the weather element the user is interested in (i.e. temperature, relative humidity, wind speed etc.)
                                        Here is a link to the spreadsheet that contains all of the proper syntax for each parameter:
                                        https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK
    
            Returns: This function returns the National Weather Service NDFD gridded forecast data in a GRIB2 file for the entire forecast period (Days 1-7). 
                     This function may also return an error message for either: 1) A bad file path (invalid directory_name) or 2) An invalid parameter (if the spelling of the parameter syntax is incorrect)
             
    '''

    ###################################################
    # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
    ###################################################

    ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
    ftp = FTP('tgftp.nws.noaa.gov')
    ftp.login()

    ### SEARCHES FOR THE CORRECT DIRECTORY ###
    try:
        dirName = directory_name + 'VP.004-007/'
        param = parameter
        files = ftp.cwd(dirName)

        ### SEARCHES FOR THE CORRECT PARAMETER ###
        try:
            ################################
            # DOWNLOADS THE NWS NDFD GRIDS #
            ################################
            
            with open(param, 'wb') as fp:
                ftp.retrbinary('RETR ' + param, fp.write)

            ftp.close()
            ds = xr.load_dataset(param, engine='cfgrib')
            ds = ds.metpy.parse_cf()
            return ds

        ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###

        except Exception as a:
            param_error = info.parameter_name_error()
            return param_error

    ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
        
    except Exception as e:
        dir_error = info.directory_name_error()
        return dir_error

def get_rtma_24_hour_comparison_data_with_u_and_v_components(current_time):


    current_time = current_time

    rtma_data, rtma_time = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_rtma_data_24_hour_difference(current_time, 'Wind_speed_Analysis_height_above_ground')

    t.sleep(15)

    rtma_time_24 = rtma_time - timedelta(hours=24)

    u, u_time = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(current_time, 'u-component_of_wind_Analysis_height_above_ground')

    t.sleep(15)

    u_24, u_24_time = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(rtma_time_24, 'u-component_of_wind_Analysis_height_above_ground')

    t.sleep(15)

    v, v_time = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(current_time, 'v-component_of_wind_Analysis_height_above_ground')

    t.sleep(15)

    v_24, v_24_time = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(rtma_time_24, 'v-component_of_wind_Analysis_height_above_ground')

    data = []

    data.append(rtma_data)
    data.append(rtma_time)
    data.append(rtma_time_24)
    data.append(u)
    data.append(u_time)
    data.append(u_24)
    data.append(u_24_time)
    data.append(v)
    data.append(v_time)
    data.append(v_24)
    data.append(v_24_time)

    return data



def get_rtma_data_past_6hrs(parameter):


    parameter = parameter
    local_time, utc_time = standard.plot_creation_time()
    times = []

    for i in range(0, 10):
        time = utc_time - timedelta(hours=i)
        times.append(time)

    t1 = times[0]
    t2 = times[1]
    t3 = times[2]
    t4 = times[3]
    t5 = times[4]
    t6 = times[5]
    t7 = times[6]
    t8 = times[7]
    t9 = times[8]
    t10 = times[9]

    rtma_data_0, rtma_time_0 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t1, parameter)

    t.sleep(15)

    rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t2, parameter)

    t.sleep(15)
    
    if rtma_time_0.hour == rtma_time_1.hour:

        rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t3, parameter)
        t.sleep(15)

        if rtma_time_0.hour == rtma_time_1.hour:

            rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t4, parameter)
            t.sleep(15)
            
            rtma_data_2, rtma_time_2 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t5, parameter)
            t.sleep(15)
    
            rtma_data_3, rtma_time_3 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t6, parameter)
            t.sleep(15)
    
            rtma_data_4, rtma_time_4 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t7, parameter)
            t.sleep(15)
    
            rtma_data_5, rtma_time_5 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t8, parameter)
            t.sleep(15)
    
            rtma_data_6, rtma_time_6 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t9, parameter)
            t.sleep(15)

            rtma_data_7, rtma_time_7 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t10, parameter)


        else:

            rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t3, parameter)
            t.sleep(15)
            
            rtma_data_2, rtma_time_2 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t4, parameter)
            t.sleep(15)
    
            rtma_data_3, rtma_time_3 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t5, parameter)
            t.sleep(15)
    
            rtma_data_4, rtma_time_4 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t6, parameter)
            t.sleep(15)
    
            rtma_data_5, rtma_time_5 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t7, parameter)
            t.sleep(15)
    
            rtma_data_6, rtma_time_6 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t8, parameter)
            t.sleep(15)

            rtma_data_7, rtma_time_7 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t9, parameter)
            t.sleep(15)

    else:
        t.sleep(15)

        rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t2, parameter)
        t.sleep(15)

        rtma_data_2, rtma_time_2 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t3, parameter)
        t.sleep(15)

        rtma_data_3, rtma_time_3 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t4, parameter)
        t.sleep(15)

        rtma_data_4, rtma_time_4 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t5, parameter)
        t.sleep(15)

        rtma_data_5, rtma_time_5 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t6, parameter)
        t.sleep(15)

        rtma_data_6, rtma_time_6 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t7, parameter)
        t.sleep(15)

        rtma_data_7, rtma_time_7 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_data(t8, parameter)
    
    rtma_data, rtma_times = parsers.save.append_data_RTMA_6hr_timelapse(rtma_data_0, rtma_data_1, rtma_data_2, rtma_data_3, rtma_data_4, rtma_data_5, rtma_data_6, rtma_data_7, rtma_time_0, rtma_time_1, rtma_time_2, rtma_time_3, rtma_time_4, rtma_time_5, rtma_time_6, rtma_time_7)

    return rtma_data, rtma_times



def get_rtma_data_24_hour_difference(current_time, parameter):

    r"""
    This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis dataset and the dataset from 24 hours prior to the current dataset. 
    This function will then take the difference between the two datasets to show the 24 hour difference and create a new dataset based on that.

    24 hour difference dataset = current dataset - dataset from 24 hours prior to the current dataset

    Inputs:
           1) current_time (Datetime) - Current time in UTC.
           2) parameter (String) - The weather parameter the user wishes to download. 
                                   To find the full list of parameters, visit: https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html

    Returns: 1) If there are zero errors, the latest 24 hour difference dataset and the time of the latest available dataset for the requested parameter will be returned. 
             2) If there is an error, an error message is returned. 

    """

    times = []
    times_24 = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        old_time = new_time - timedelta(hours=24)
        times.append(new_time)
        times_24.append(old_time)
        
        
    try:
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
    except Exception as a:
        pass
    
    try:
        first_backup_server_response = requests.get("https://thredds-test.unidata.ucar.edu/thredds/catalog/catalog.xml")
        first_backup_server_status = first_backup_server_response.status_code
    except Exception as b:
        pass
    
    try:
        second_backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        second_backup_server_status = second_backup_server_response.status_code
    except Exception as c:
        pass
    
    if main_server_status == 200:
        print("Main UCAR THREDDS Server is online. Connecting!")
        
        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_parameter = rtma_data[parameter].squeeze()
    
            rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
    
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_parameter - rtma_parameter_24, time
            
        except Exception as e:
            
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
            print("Will try to download the most recent datasets from "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter = rtma_data[parameter].squeeze()
        
                rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter_24 = rtma_data_24[parameter].squeeze()
        
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_parameter - rtma_parameter_24, time
         
            except Exception as a:
    
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                print("Will try to download the most recent datasets from "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter = rtma_data[parameter].squeeze()
            
                    rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter_24 = rtma_data_24[parameter].squeeze()
            
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_parameter - rtma_parameter_24, time
    
    
                except Exception as b:
                                
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                    print("Will try to download the most recent datasets from "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter = rtma_data[parameter].squeeze()
                
                        rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_parameter - rtma_parameter_24, time
    
                    except Exception as c:
                                
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                        print("Will try to download the most recent datasets from "+times[4].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter = rtma_data[parameter].squeeze()
                    
                            rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                    
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_parameter - rtma_parameter_24, time
                                  
                    
                        except syntaxError as k:
                            error = info.syntax_error()
    
                            return error

    
    if main_server_status != 200 and first_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!")
        
        try:
            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_parameter = rtma_data[parameter].squeeze()
    
            rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
    
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_parameter - rtma_parameter_24, time
            
        except Exception as e:
            
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
            print("Will try to download the most recent datasets from "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter = rtma_data[parameter].squeeze()
        
                rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter_24 = rtma_data_24[parameter].squeeze()
        
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_parameter - rtma_parameter_24, time
         
            except Exception as a:
    
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                print("Will try to download the most recent datasets from "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter = rtma_data[parameter].squeeze()
            
                    rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter_24 = rtma_data_24[parameter].squeeze()
            
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_parameter - rtma_parameter_24, time
    
    
                except Exception as b:
                                
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                    print("Will try to download the most recent datasets from "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter = rtma_data[parameter].squeeze()
                
                        rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_parameter - rtma_parameter_24, time
    
                    except Exception as c:
                                
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                        print("Will try to download the most recent datasets from "+times[4].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter = rtma_data[parameter].squeeze()
                    
                            rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                    
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_parameter - rtma_parameter_24, time
                                  
                    
                        except syntaxError as k:
                            error = info.syntax_error()
    
                            return error

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connected to the second backup UCAR THREDDS Server!")
        
        try:
            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_parameter = rtma_data[parameter].squeeze()
    
            rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
    
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_parameter - rtma_parameter_24, time
            
        except Exception as e:
            
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
            print("Will try to download the most recent datasets from "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter = rtma_data[parameter].squeeze()
        
                rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_parameter_24 = rtma_data_24[parameter].squeeze()
        
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_parameter - rtma_parameter_24, time
         
            except Exception as a:
    
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                print("Will try to download the most recent datasets from "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter = rtma_data[parameter].squeeze()
            
                    rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_parameter_24 = rtma_data_24[parameter].squeeze()
            
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_parameter - rtma_parameter_24, time
    
    
                except Exception as b:
                                
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                    print("Will try to download the most recent datasets from "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter = rtma_data[parameter].squeeze()
                
                        rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_parameter - rtma_parameter_24, time
    
                    except Exception as c:
                                
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                        print("Will try to download the most recent datasets from "+times[4].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter = rtma_data[parameter].squeeze()
                    
                            rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                    
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_parameter - rtma_parameter_24, time
                                  
                    
                        except syntaxError as k:
                            error = info.syntax_error()
    
                            return error

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status != 200:
        print("Unable to connect to either the main or backup servers. Aborting!")


def get_rtma_relative_humidity_data_past_6hrs():


    
    local_time, utc_time = standard.plot_creation_time()
    times = []

    for i in range(0, 10):
        time = utc_time - timedelta(hours=i)
        times.append(time)

    t1 = times[0]
    t2 = times[1]
    t3 = times[2]
    t4 = times[3]
    t5 = times[4]
    t6 = times[5]
    t7 = times[6]
    t8 = times[7]
    t9 = times[8]
    t10 = times[9]

    rtma_data_0, rtma_time_0 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t1)

    t.sleep(15)

    rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t2)

    t.sleep(15)

    if rtma_time_0.hour == rtma_time_1.hour:

        rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t3)

        t.sleep(15)

        if rtma_time_0.hour == rtma_time_1.hour:

            rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t4)

            t.sleep(15)

            rtma_data_2, rtma_time_2 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t5)

            t.sleep(15)
    
            rtma_data_3, rtma_time_3 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t6)

            t.sleep(15)
    
            rtma_data_4, rtma_time_4 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t7)

            t.sleep(15)
    
            rtma_data_5, rtma_time_5 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t8)

            t.sleep(15)
    
            rtma_data_6, rtma_time_6 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t9)

            t.sleep(15)

            rtma_data_7, rtma_time_7 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t10)

        else:

            rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t3)

            t.sleep(15)
            
            rtma_data_2, rtma_time_2 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t4)

            t.sleep(15)
    
            rtma_data_3, rtma_time_3 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t5)

            t.sleep(15)
    
            rtma_data_4, rtma_time_4 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t6)

            t.sleep(15)
    
            rtma_data_5, rtma_time_5 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t7)

            t.sleep(15)
    
            rtma_data_6, rtma_time_6 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t8)

            t.sleep(15)

            rtma_data_7, rtma_time_7 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t9)

    else:

        rtma_data_1, rtma_time_1 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t2)

        t.sleep(15)

        rtma_data_2, rtma_time_2 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t3)

        t.sleep(15)

        rtma_data_3, rtma_time_3 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t4)

        t.sleep(15)

        rtma_data_4, rtma_time_4 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t5)

        t.sleep(15)

        rtma_data_5, rtma_time_5 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t6)

        t.sleep(15)

        rtma_data_6, rtma_time_6 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t7)

        t.sleep(15)

        rtma_data_7, rtma_time_7 = UCAR_THREDDS_SERVER_OPENDAP_Downloads.CONUS.get_current_rtma_relative_humidity_data(t8)
    
    rtma_data, rtma_times = parsers.save.append_data_RTMA_6hr_timelapse(rtma_data_0, rtma_data_1, rtma_data_2, rtma_data_3, rtma_data_4, rtma_data_5, rtma_data_6, rtma_data_7, rtma_time_0, rtma_time_1, rtma_time_2, rtma_time_3, rtma_time_4, rtma_time_5, rtma_time_6, rtma_time_7)

    return rtma_data, rtma_times


def get_current_rtma_relative_humidity_data(current_time):

    r"""
    This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis for temperature and dewpoint. 
    This function then uses MetPy to create a relative humidity dataset from the temperature and dewpoint datasets. 
    This function then returns the relative humidity dataset. 

    Inputs:
           1) current_time (Datetime) - Current time in UTC.

    Returns: 1) If there are zero errors, the latest relative humidity dataset and the time for that dataset are returned. 
             2) If there is an error, an error message is returned. 

    """

    times = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        times.append(new_time)

    try:
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
    except Exception as a:
        pass
        
    try:
        first_backup_server_response = requests.get("https://thredds-test.unidata.ucar.edu/thredds/catalog/catalog.xml")
        first_backup_server_status = first_backup_server_response.status_code
    except Exception as b:
        pass
    
    try:
        second_backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        second_backup_server_status = second_backup_server_response.status_code
    except Exception as c:
        pass
    
    if main_server_status == 200:
        print("Main UCAR THREDDS Server is online. Connecting!")

        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
               
                return rtma_rh *100, time

            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, time

                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connected to the first backup UCAR THREDDS Server!")
        try:
            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connected to the second backup UCAR THREDDS Server!")
        try:
            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status != 200:
        print("Unable to connect to either the main or backup servers. Aborting!")


def get_red_flag_warning_parameters_using_wind_speed(current_time):

    r"""
    This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis datasets for: 1) Temperature, 2) Dewpoint and 3) Wind Speed. 
    This function uses MetPy to create a relative humidity dataset from the temperature and dewpoint datasets. 
    This function then returns the relative humidity dataset, wind speed dataset and the time for the datasets. 

    Inputs:
           1) current_time (Datetime) - Current time in UTC. 

    Returns:
            1) 2.5km x 2.5km Real Time Mesoscale Analysis Relative Humidity dataset. 
            2) 2.5km x 2.5km Real Time Mesoscale Analysis Wind Speed dataset. 
            3) Time of the latest available datasets. 

    """

    times = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        times.append(new_time)

    try:
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
    except Exception as a:
        pass
        
    try:
        first_backup_server_response = requests.get("https://thredds-test.unidata.ucar.edu/thredds/catalog/catalog.xml")
        first_backup_server_status = first_backup_server_response.status_code
    except Exception as b:
        pass
        
    try:
        second_backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        second_backup_server_status = second_backup_server_response.status_code
    except Exception as c:
        pass

    if main_server_status == 200:
        print("Main UCAR THREDDS Server is online. Connecting!")

        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, rtma_wind * 2.23694, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, rtma_wind, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, rtma_wind, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                        rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, rtma_wind, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                            rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, rtma_wind, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!")

        try:
            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, rtma_wind * 2.23694, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, rtma_wind, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, rtma_wind, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                        rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, rtma_wind, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                            rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, rtma_wind, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None


    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connected to the second backup UCAR THREDDS Server!")

        try:
            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, rtma_wind * 2.23694, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, rtma_wind, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, rtma_wind, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                        rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, rtma_wind, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                            rtma_wind = rtma_data['Wind_speed_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, rtma_wind, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None



    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status != 200:
        print("Unable to connect to either the main or backup servers. Aborting!")
                            


def get_red_flag_warning_parameters_using_wind_gust(current_time):

    r"""
    This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis datasets for: 1) Temperature, 2) Dewpoint and 3) Wind Gust. 
    This function uses MetPy to create a relative humidity dataset from the temperature and dewpoint datasets. 
    This function then returns the relative humidity dataset, wind gust dataset and the time for the datasets. 

    Inputs:
           1) current_time (Datetime) - Current time in UTC. 

    Returns:
            1) 2.5km x 2.5km Real Time Mesoscale Analysis Relative Humidity dataset. 
            2) 2.5km x 2.5km Real Time Mesoscale Analysis Wind Gust dataset. 
            3) Time of the latest available datasets. 

    """

    times = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        times.append(new_time)

    try:
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
    except Exception as a:
        pass
        
    try:
        first_backup_server_response = requests.get("https://thredds-test.unidata.ucar.edu/thredds/catalog/catalog.xml")
        first_backup_server_status = first_backup_server_response.status_code
    except Exception as b:
        pass
        
    try:
        second_backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        second_backup_server_status = second_backup_server_response.status_code
    except Exception as c:
        pass

    if main_server_status == 200:
        print("Main UCAR THREDDS Server is online. Connecting!")

        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, rtma_gust * 2.23694, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, rtma_gust, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, rtma_gust, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                        rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, rtma_gust, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                            rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, rtma_gust, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!")

        try:
            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, rtma_gust * 2.23694, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, rtma_gust, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, rtma_gust, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                        rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, rtma_gust, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                            rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, rtma_gust, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!")

        try:
            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return rtma_rh *100, rtma_gust * 2.23694, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return rtma_rh *100, rtma_gust, time
      
            except Exception as a:
    
                print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                    time = times[2]
                    
                    return rtma_rh *100, rtma_gust, time
    
                except Exception as b:
                                
                    print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                        rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return rtma_rh *100, rtma_gust, time
    
                    except Exception as c:
                                
                        print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                        
                        try:
                            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                            rtma_gust = rtma_data['Wind_speed_gust_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                            print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return rtma_rh *100, rtma_gust, time
                                   
                    
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None


    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status != 200:
        print("Unable to connect to either the main or backup servers. Aborting!")


def get_rtma_relative_humidity_24_hour_difference_data(current_time):

    r"""
    This function retrieves the latest available 2.5km x 2.5km Real Time Mesoscale Analysis temperature and dewpoint dataset and the temperature and dewpoint dataset from 24 hours prior to the current dataset. 
    This function will then use MetPy to create a relative humidity dataset for the latest available time and for 24 hours prior to the latest available time. 
    The function will then take the difference between the two relative humidity datasets to show the 24 hour difference and create a new dataset based on that.

    24 hour difference relative humidity dataset = current relative humidity dataset - relative humidity dataset from 24 hours prior to the current dataset

    Inputs:
           1) current_time (Datetime) - Current time in UTC.

    Returns: 1) If there are zero errors, the latest 24 hour relative humidity difference dataset and the time of the latest available relative humidity dataset for the requested parameter will be returned. 
             2) If there is an error, an error message is returned. 

    """

    times = []
    times_24 = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        old_time = new_time - timedelta(hours=24)
        times.append(new_time)
        times_24.append(old_time)
        
    try:
        main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
        main_server_status = main_server_response.status_code
    except Exception as a:
        pass
    
    try:
        first_backup_server_response = requests.get("https://thredds-test.unidata.ucar.edu/thredds/catalog/catalog.xml")
        first_backup_server_status = first_backup_server_response.status_code
    except Exception as b:
        pass
    
    try:
        second_backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
        second_backup_server_status = second_backup_server_response.status_code
    except Exception as c:
        pass

    if main_server_status == 200:
        print("Main UCAR THREDDS Server is online. Connecting!")

        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
    
            rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
            print("Data retrieval for both " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return (rtma_rh - rtma_rh_24) *100, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[0].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
        
                rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                print("Data retrieval for both " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return (rtma_rh - rtma_rh_24) *100, time 
                
            except Exception as a:
    
                print("Relative Humidity Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[1].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            
                    rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                    print("Data retrieval for both " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    
                    time = times[2]
                    return (rtma_rh - rtma_rh_24) *100, time 
                    
                except Exception as b:
                                
                    print("Relative Humidity Data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[2].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                
                        rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                        print("Data retrieval for both " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return (rtma_rh - rtma_rh_24) *100, time 
     
                    except Exception as c:
                                
                        print("Relative Humidity Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[3].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                
                        try:
                            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    
                            rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                            print("Data retrieval for both " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return (rtma_rh - rtma_rh_24) *100, time 
            
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!")
        
        try:
            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
    
            rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
            print("Data retrieval for both " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return (rtma_rh - rtma_rh_24) *100, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[0].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
        
                rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                print("Data retrieval for both " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return (rtma_rh - rtma_rh_24) *100, time 
                
            except Exception as a:
    
                print("Relative Humidity Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[1].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            
                    rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                    print("Data retrieval for both " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    
                    time = times[2]
                    return (rtma_rh - rtma_rh_24) *100, time 
                    
                except Exception as b:
                                
                    print("Relative Humidity Data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[2].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                
                        rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                        print("Data retrieval for both " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return (rtma_rh - rtma_rh_24) *100, time 
     
                    except Exception as c:
                                
                        print("Relative Humidity Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[3].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                
                        try:
                            rtma_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    
                            rtma_cat_24 = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                            print("Data retrieval for both " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return (rtma_rh - rtma_rh_24) *100, time 
            
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connected to the second backup UCAR THREDDS Server!")
        
        try:
            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
    
            rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
            print("Data retrieval for both " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")

            time = times[0]
            
            return (rtma_rh - rtma_rh_24) *100, time
            
        except Exception as e:
    
            print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[0].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[1].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
        
                rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                print("Data retrieval for both " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                time = times[1]
                
                return (rtma_rh - rtma_rh_24) *100, time 
                
            except Exception as a:
    
                print("Relative Humidity Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[1].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[2].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            
                    rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                    rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                    print("Data retrieval for both " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    
                    time = times[2]
                    return (rtma_rh - rtma_rh_24) *100, time 
                    
                except Exception as b:
                                
                    print("Relative Humidity Data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[2].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                
                        rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                        rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                        print("Data retrieval for both " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                        time = times[3]
                        
                        return (rtma_rh - rtma_rh_24) *100, time 
     
                    except Exception as c:
                                
                        print("Relative Humidity Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[3].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                
                        try:
                            rtma_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data = rtma_data.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    
                            rtma_cat_24 = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                            rtma_data_24 = rtma_data_24.metpy.parse_cf().metpy.assign_latitude_longitude()
                            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                    
                            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                            print("Data retrieval for both " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")

                            time = times[4]
                            
                            return (rtma_rh - rtma_rh_24) *100, time 
            
                        except Exception as k:
                            print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")
    
                            return None

    if main_server_status != 200 and first_backup_server_status != 200 and second_backup_server_status != 200:
        print("Unable to connect to either the main or backup servers. Aborting!")




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
    
    previous_day_utc = new_date_utc - timedelta(days=1)
    
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

    print("Data retrieved successfully!")

    return maximum_temperature, maximum_temperature_time, maximum_temperature_time_local, minimum_temperature, minimum_temperature_time, minimum_temperature_time_local, minimum_relative_humidity, minimum_relative_humidity_time, minimum_relative_humidity_time_local, maximum_relative_humidity, maximum_relative_humidity_time, maximum_relative_humidity_time_local, maximum_wind_speed, wind_dir, maximum_wind_speed_time, maximum_wind_speed_time_local, maximum_wind_gust, maximum_wind_gust_time, maximum_wind_gust_time_local, station_id, previous_day_utc


def previous_day_weather_summary_and_all_data(station_id):

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


def get_METAR_Data(current_time, plot_projection, mask):

    r'''
    This function downloads and returns the latest METAR data. 
    This function also uses MetPy to calculate the relative humidity dataset from the temperature and dewpoint datasets. 
    
    Inputs: 1) current_time (Datetime) - Current date and time in UTC. 
            2) plot_projection (Cartopy Coordinate Reference System) - The coordinate reference system of the data being plotted. This is usually PlateCarree. 
                                                                       This function is to be used if the user does not want the Real Time Mesoscale Analysis data synced with the METAR. 
                                                                       METAR data updates faster than Real Time Mesoscale Analysis data so that is the only advantage of having both 
                                                                       datasets not time synced. However in most cases, this is NOT the recommended option and the time synced data
                                                                       is recommended. 
           
            3) mask (Integer) - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed. 

    Returns: 1) sfc_data - The entire METAR dataset. 
             2) sfc_data_u_kt - The u-component (west-east) of the wind velocity in knots. 
             3) sfc_data_v_kt - The v-component (north-south) of the wind velocity in knots. 
             4) sfc_data_rh - The relative humidity in the METAR dataset. 
             5) sfc_data_mask - Distance in meters to mask METAR stations apart from eachother so stations don't clutter the plot. The higher the value, the less stations are displayed. 
             6) metar_time - The time of the METAR report. 

    '''
    metar_time = current_time

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
        print("Main UCAR THREDDS Server is online. Connecting!")
        
        try:
            metar_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')

        
        except Exception as e:
            metar_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')

    if main_server_status != 200 and backup_server_status == 200:
        print("Main UCAR THREDDS Server is down. Connecting to the backup UCAR THREDDS Server!") 
        try:
            metar_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')

            print("Successfully connected to the backup server! Downloading Data...")
        
        except Exception as e:
            print("ERROR! Cannot connect to either the main or backup server. Aborting!")

    if main_server_status != 200 and backup_server_status != 200:
        print("ERROR! Cannot connect to either the main or backup server. Aborting!")
        
    # Opens METAR file
    metar_file = metar_cat.datasets.filter_time_nearest(metar_time).remote_open()
    
    # Decodes bytes into strings
    metar_text = StringIO(metar_file.read().decode('latin-1'))
    
    # Parses through data
    sfc_data = parse_metar_file(metar_text, year=metar_time.year, month=metar_time.month)
    sfc_units = sfc_data.units
    
    # Creates dataframe
    sfc_data = sfc_data[sfc_data['station_id'].isin(airports_df['ident'])]
    
    sfc_data = pandas_dataframe_to_unit_arrays(sfc_data, sfc_units)
    
    sfc_data['u'], sfc_data['v'] = mpcalc.wind_components(sfc_data['wind_speed'], sfc_data['wind_direction'])
    
    sfc_data_u_kt = sfc_data['u'].to('kts')
    sfc_data_v_kt = sfc_data['v'].to('kts')
    
    sfc_data_rh = mpcalc.relative_humidity_from_dewpoint(sfc_data['air_temperature'], sfc_data['dew_point_temperature'])
    
    
    locs = plot_projection.transform_points(ccrs.PlateCarree(), sfc_data['longitude'].m, sfc_data['latitude'].m)
    #print(locs[:, :])
    
    # Creates mask for plotting METAR obs
    sfc_data_mask = mpcalc.reduce_point_density(locs[:, :], mask)

    print("METAR Data successfully retrieved for " + metar_time.strftime('%m/%d/%Y %H00 UTC'))
    return sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time

def get_METAR_Data_CONUS(current_time):

    r'''

    This function downloads and returns the latest METAR data. 
    This function also uses MetPy to calculate the relative humidity dataset from the temperature and dewpoint datasets. 
    This function is only used for METAR observations in Hawaii. 
    
    Inputs: 1) current_time (Datetime) - Current date and time in UTC. 

    Returns: 1) sfc_data - The entire METAR dataset. 
             2) sfc_data_u_kt - The u-component (west-east) of the wind velocity in knots. 
             3) sfc_data_v_kt - The v-component (north-south) of the wind velocity in knots. 
             4) sfc_data_rh - The relative humidity in the METAR dataset. 
             5) metar_time - The time of the METAR report. 

    '''
    metar_time = current_time
    
    # Pings server for airport data
    airports_df = pd.read_csv(get_test_data('airport-codes.csv'))
    
    # Queries our airport types (airport sizes)
    airports_df = airports_df[(airports_df['type'] == 'large_airport') | (airports_df['type'] == 'medium_airport') | (airports_df['type'] == 'small_airport')]
    
    # Accesses the METAR data
    try:
        metar_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
    
    except Exception as e:
        metar_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
        
    # Opens METAR file
    metar_file = metar_cat.datasets.filter_time_nearest(metar_time).remote_open()
    
    # Decodes bytes into strings
    metar_text = StringIO(metar_file.read().decode('latin-1'))
    
    # Parses through data
    sfc_data = parse_metar_file(metar_text, year=metar_time.year, month=metar_time.month)
    sfc_units = sfc_data.units
    
    # Creates dataframe
    sfc_data = sfc_data[sfc_data['station_id'].isin(airports_df['ident'])]
    
    sfc_data = pandas_dataframe_to_unit_arrays(sfc_data, sfc_units)
    
    sfc_data['u'], sfc_data['v'] = mpcalc.wind_components(sfc_data['wind_speed'], sfc_data['wind_direction'])
    
    sfc_data_u_kt = sfc_data['u'].to('kts')
    sfc_data_v_kt = sfc_data['v'].to('kts')
    
    sfc_data_rh = mpcalc.relative_humidity_from_dewpoint(sfc_data['air_temperature'], sfc_data['dew_point_temperature'])

    print("METAR Data successfully retrieved for " + metar_time.strftime('%m/%d/%Y %H00 UTC'))
    return sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time



def get_METAR_Data_Hawaii(current_time):

    r'''

    This function downloads and returns the latest METAR data. 
    This function also uses MetPy to calculate the relative humidity dataset from the temperature and dewpoint datasets. 
    This function is only used for METAR observations in Hawaii. 
    
    Inputs: 1) current_time (Datetime) - Current date and time in UTC. 

    Returns: 1) sfc_data - The entire METAR dataset. 
             2) sfc_data_u_kt - The u-component (west-east) of the wind velocity in knots. 
             3) sfc_data_v_kt - The v-component (north-south) of the wind velocity in knots. 
             4) sfc_data_rh - The relative humidity in the METAR dataset. 
             5) metar_time - The time of the METAR report. 

    '''
    metar_time = current_time
    
    # Pings server for airport data
    airports_df = pd.read_csv(get_test_data('airport-codes.csv'))
    
    # Queries our airport types (airport sizes)
    airports_df = airports_df[(airports_df['type'] == 'large_airport') | (airports_df['type'] == 'small_airport')]
    
    # Accesses the METAR data
    try:
        metar_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
    
    except Exception as e:
        metar_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')
        
    # Opens METAR file
    metar_file = metar_cat.datasets.filter_time_nearest(metar_time).remote_open()
    
    # Decodes bytes into strings
    metar_text = StringIO(metar_file.read().decode('latin-1'))
    
    # Parses through data
    sfc_data = parse_metar_file(metar_text, year=metar_time.year, month=metar_time.month)
    sfc_units = sfc_data.units
    
    # Creates dataframe
    sfc_data = sfc_data[sfc_data['station_id'].isin(airports_df['ident'])]
    
    sfc_data = pandas_dataframe_to_unit_arrays(sfc_data, sfc_units)
    
    sfc_data['u'], sfc_data['v'] = mpcalc.wind_components(sfc_data['wind_speed'], sfc_data['wind_direction'])
    
    sfc_data_u_kt = sfc_data['u'].to('kts')
    sfc_data_v_kt = sfc_data['v'].to('kts')
    
    sfc_data_rh = mpcalc.relative_humidity_from_dewpoint(sfc_data['air_temperature'], sfc_data['dew_point_temperature'])

    print("METAR Data successfully retrieved for " + metar_time.strftime('%m/%d/%Y %H00 UTC'))
    return sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time
    

def latest_metar_time(current_time):

    r'''
    This function is a timecheck to ensure the latest full dataset is downloaded rather than an incomplete dataset. 
    After 30 minutes past the hour, the newer dataset begins to trickle in, however at this time the new dataset is missing several observations. 
    This check uses the python datetime module to get the current time and if the current minute is past the 30 minute mark, the metar_time
    which is the time variable used in our dataset query will be adjusted to back to the top of the current hour to ensure the latest complete 
    dataset is the dataset that is downloaded. 

    Inputs: 1) current_time (Datetime) - Current date and time in UTC. 

    Returns: 1) metar_time (Datetime) - The corrected time if the script the user is running runs past the 30 minute mark. 
    '''

    
    runtime = current_time
    minute = runtime.minute
    # Times for METAR reports
    if runtime.minute <30:
        metar_time = datetime.utcnow() 
    if runtime.minute >=30:
        metar_time = datetime.utcnow() - timedelta(minutes=minute)

    return metar_time


def RTMA_Synced_With_METAR_Hawaii(parameter, current_time):

    r'''

    THIS FUNCTION RETURNS THE LATEST RTMA DATASET WITH THE LATEST METAR DATASET AND SYNCS UP BOTH DATASETS TO BE REPRESENTATIVE OF THE SAME TIME SINCE THE METAR DATA IS AVAILIABLE MUCH QUICKER THAN THE RTMA DATA. THIS ALLOWS USERS TO OVERLAY METAR DATA ONTO RTMA DATA AND HAVE THE TIMES BETWEEN BOTH DATASETS MATCH. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2024

    '''

    parameter = parameter
    current_time = current_time

    metar_time = UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.latest_metar_time(current_time)

    lon_vals, lat_vals, time, relative_humidity_to_plot = NOMADS_OPENDAP_Downloads.RTMA_Hawaii.get_RTMA_Data_single_parameter(current_time, parameter)

    
    new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(time, metar_time)


    sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.get_METAR_Data_Hawaii(new_metar_time)

    return lon_vals, lat_vals, time, relative_humidity_to_plot, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised



def RTMA_Synced_With_METAR_GUAM(parameter, current_time, mask):

    r'''

    THIS FUNCTION RETURNS THE LATEST RTMA DATASET WITH THE LATEST METAR DATASET AND SYNCS UP BOTH DATASETS TO BE REPRESENTATIVE OF THE SAME TIME SINCE THE METAR DATA IS AVAILIABLE MUCH QUICKER THAN THE RTMA DATA. THIS ALLOWS USERS TO OVERLAY METAR DATA ONTO RTMA DATA AND HAVE THE TIMES BETWEEN BOTH DATASETS MATCH. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2024

    '''

    parameter = parameter
    current_time = current_time
    mask = mask

    metar_time = latest_metar_time(current_time)

    rtma_data, rtma_time = get_current_rtma_data(current_time, parameter)

    plot_projection = rtma_data.metpy.cartopy_crs
    
    new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(rtma_time, metar_time)

    sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised = UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.get_METAR_Data(new_metar_time, plot_projection, mask)

    return rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_projection


def RTMA_Relative_Humidity_Synced_With_METAR_GUAM(current_time, mask):

    r'''
    THIS FUNCTION RETURNS THE LATEST RTMA RELATIVE HUMIDITY DATASET WITH THE LATEST METAR DATASET AND SYNCS UP BOTH DATASETS TO BE REPRESENTATIVE OF THE SAME TIME SINCE THE METAR DATA IS AVAILIABLE MUCH QUICKER THAN THE RTMA DATA. THIS ALLOWS USERS TO OVERLAY METAR DATA ONTO RTMA DATA AND HAVE THE TIMES BETWEEN BOTH DATASETS MATCH. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2024
    '''

    current_time = current_time
    mask = mask

    metar_time = latest_metar_time(current_time)

    rtma_data, rtma_time = GUAM.get_current_rtma_relative_humidity_data(current_time)

    plot_projection = rtma_data.metpy.cartopy_crs
    
    new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(rtma_time, metar_time)

    sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised = get_METAR_Data(new_metar_time, plot_projection, mask)

    return rtma_data, rtma_time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, sfc_data_mask, metar_time_revised, plot_projection


def RTMA_Relative_Humidity_Synced_With_METAR_Hawaii(current_time):

    r'''
    THIS FUNCTION RETURNS THE LATEST RTMA RELATIVE HUMIDITY DATASET WITH THE LATEST METAR DATASET AND SYNCS UP BOTH DATASETS TO BE REPRESENTATIVE OF THE SAME TIME SINCE THE METAR DATA IS AVAILIABLE MUCH QUICKER THAN THE RTMA DATA. THIS ALLOWS USERS TO OVERLAY METAR DATA ONTO RTMA DATA AND HAVE THE TIMES BETWEEN BOTH DATASETS MATCH. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2024
    '''

    current_time = current_time

    metar_time = latest_metar_time(current_time)

    lon_vals, lat_vals, time, relative_humidity_to_plot = RTMA_Hawaii.get_RTMA_relative_humidity(current_time)

    
    new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(time, metar_time)


    sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = get_METAR_Data_Hawaii(new_metar_time)

    return lon_vals, lat_vals, time, relative_humidity_to_plot, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised


def RTMA_Dataset_Synced_With_METAR(current_time):

    r'''
    THIS FUNCTION RETURNS THE LATEST RTMA RELATIVE HUMIDITY DATASET WITH THE LATEST METAR DATASET AND SYNCS UP BOTH DATASETS TO BE REPRESENTATIVE OF THE SAME TIME SINCE THE METAR DATA IS AVAILIABLE MUCH QUICKER THAN THE RTMA DATA. THIS ALLOWS USERS TO OVERLAY METAR DATA ONTO RTMA DATA AND HAVE THE TIMES BETWEEN BOTH DATASETS MATCH. 

    (C) METEOROLOGIST ERIC J. DREWITZ 2024
    '''

    current_time = current_time

    metar_time = latest_metar_time(current_time)

    ds, time = get_RTMA_dataset(current_time)

    
    new_metar_time = parsers.checks.check_RTMA_vs_METAR_Times(time, metar_time)


    sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised = UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.get_METAR_Data_CONUS(new_metar_time)

    return ds, time, sfc_data, sfc_data_u_kt, sfc_data_v_kt, sfc_data_rh, metar_time_revised



def get_rtma_data_past_6hrs():


    
    local_time, utc_time = standard.plot_creation_time()
    times = []

    for i in range(0, 10):
        time = utc_time - timedelta(hours=i)
        times.append(time)

    t1 = times[0]
    t2 = times[1]
    t3 = times[2]
    t4 = times[3]
    t5 = times[4]
    t6 = times[5]
    t7 = times[6]
    t8 = times[7]
    t9 = times[8]
    t10 = times[9]

    ds_0, rtma_time_0 = get_RTMA_dataset(t1)

    t.sleep(15)

    ds_1, rtma_time_1 = get_RTMA_dataset(t2)

    t.sleep(15)

    if rtma_time_0.hour == rtma_time_1.hour:

        ds_1, rtma_time_1 = get_RTMA_dataset(t3)

        t.sleep(15)

        if rtma_time_0.hour == rtma_time_1.hour:

            ds_1, rtma_time_1 = get_RTMA_dataset(t4)

            t.sleep(15)

            ds_2, rtma_time_2 = get_RTMA_dataset(t5)

            tsleep(15)
    
            ds_3, rtma_time_3 = get_RTMA_dataset(t6)

            t.sleep(15)
    
            ds_4, rtma_time_4 = get_RTMA_dataset(t7)

            t.sleep(15)
    
            ds_5, rtma_time_5 = get_RTMA_dataset(t8)

            t.sleep(15)
    
            ds_6, rtma_time_6 = get_RTMA_dataset(t9)

            t.sleep(15)

            ds_7, rtma_time_7 = get_RTMA_dataset(t10)

            t.sleep(15)


        else:

            ds_1, rtma_time_1 = get_RTMA_dataset(t3)

            t.sleep(15)
            
            ds_2, rtma_time_2 = get_RTMA_dataset(t4)

            t.sleep(15)
    
            ds_3, rtma_time_3 = get_RTMA_dataset(t5)

            t.sleep(15)
    
            ds_4, rtma_time_4 = get_RTMA_dataset(t6)

            t.sleep(15)
    
            ds_5, rtma_time_5 = get_RTMA_dataset(t7)

            t.sleep(15)
    
            ds_6, rtma_time_6 = get_RTMA_dataset(t8)

            t.sleep(15)

            ds_7, rtma_time_7 = get_RTMA_dataset(t9)

            t.sleep(15)

    else:

        ds_1, rtma_time_1 = get_RTMA_dataset(t2)

        t.sleep(15)

        ds_2, rtma_time_2 = get_RTMA_dataset(t3)

        t.sleep(15)

        ds_3, rtma_time_3 = get_RTMA_dataset(t4)

        t.sleep(15)

        ds_4, rtma_time_4 = get_RTMA_dataset(t5)

        t.sleep(15)

        ds_5, rtma_time_5 = get_RTMA_dataset(t6)

        t.sleep(15)

        ds_6, rtma_time_6 = get_RTMA_dataset(t7)

        t.sleep(15)

        ds_7, rtma_time_7 = get_RTMA_dataset(t8)
    
    ds_list, rtma_times = parsers.save.append_data_RTMA_6hr_timelapse(ds_0, ds_1, ds_2, ds_3, ds_4, ds_5, ds_6, ds_7, rtma_time_0, rtma_time_1, rtma_time_2, rtma_time_3, rtma_time_4, rtma_time_5, rtma_time_6, rtma_time_7)

    return ds_list, rtma_times        

            

    class RTMA_Alaska:

        r'''
        THIS CLASS HOSTS FUNCTIONS THAT RETRIEVE THE REAL TIME MESOSCALE ANALYSIS DATA FOR ALASKA
        
        '''

        def get_RTMA_Data_single_parameter(current_time, parameter):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            param = parameter
            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                strtime = times[0]
                
            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    strtime = times[1]
                    
                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            strtime = times[2]
                            
                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                strtime = times[3]
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    strtime = times[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            try:
                parameter_data = ds[parameter]
                lat = parameter_data['lat']
                lon = parameter_data['lon']
                
                lat_vals = lat[:].squeeze()
                lon_vals = lon[:].squeeze()

                # CONVERTS KELVIN TO FAHRENHEIT
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    parameter_data = (frac * (parameter_data - 273.15)) + 32

                # CONVERTS M/S TO MPH
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    parameter_data = parameter_data * 2.23694

                if param == 'wdir10m':
                    parameter_data = units('degree') * parameter_data

                # CONVERTS METERS TO FEET
                if param == 'vissfc' or param == 'ceilceil':
                    parameter_data = parameter_data * 3.28084

                # CONVERTS PASCALS TO HECTOPASCALS
                if param == 'pressfc':
                    parameter_data = parameter_data * 0.01

                if param == 'tcdcclm':
                    parameter_data = units('percent') * parameter_data

                data_to_plot = parameter_data[0, :, :]
                
                return lon_vals, lat_vals, strtime, data_to_plot
                
            except Exception as f:
                error = info.invalid_parameter_NOMADS_RTMA_Alaska()
                print(error)

                

        def get_RTMA_Data_24_hour_change_single_parameter(current_time, parameter):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            param = parameter
            times = []
            times_24 = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)
                time_24 = pd.to_datetime(time - timedelta(hours=24))
                times_24.append(time_24)

            ### LATEST TIME URLS ###
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'


            ### 24 HOURS AGO URLS ###
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[0].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[1].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[2].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[3].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[4].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + times_24[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]
                time_24 = times_24[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + times_24[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]
                    time_24 = times_24[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + times_24[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]
                            time_24 = times_24[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + times_24[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]
                                time_24 = times_24[3]
                            
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times_24[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
                                    time_24 = times_24[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            try:
                parameter_data = ds[parameter]
                lat = parameter_data['lat']
                lon = parameter_data['lon']
                
                lat_vals = lat[:].squeeze()
                lon_vals = lon[:].squeeze()

                parameter_data_24 = ds_24[parameter]

                # CONVERT KELVIN TO FAHRENHEIT
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    parameter_data = (frac * (parameter_data - 273.15)) + 32
                    parameter_data_24 = (frac * (parameter_data_24 - 273.15)) + 32

                # CONVERT M/S TO MPH
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    parameter_data = parameter_data * 2.23694
                    parameter_data_24 = parameter_data_24 * 2.23694

                if param == 'wdir10m':
                    parameter_data = units('degree') * parameter_data
                    parameter_data_24 = units('degree') * parameter_data_24

                # CONVERT METERS TO FEET
                if param == 'vissfc' or param == 'ceilceil':
                    parameter_data = parameter_data * 3.28084
                    parameter_data = parameter_data * 3.28084

                # CONVERT PASCALS TO HECTOPASCALS
                if param == 'pressfc':
                    parameter_data = parameter_data * 0.01
                    parameter_data_24 = parameter_data_24 * 0.01

                if param == 'tcdcclm':
                    parameter_data = units('percent') * parameter_data
                    parameter_data_24 = units('percent') * parameter_data_24

                data_to_plot = parameter_data[0, :, :] - parameter_data_24[0, :, :]
                
                return lon_vals, lat_vals, time, time_24, data_to_plot
                
            except Exception as f:
                error = info.invalid_parameter_NOMADS_RTMA_Alaska()
                print(error)

        
        def get_RTMA_relative_humidity(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100


        def get_RTMA_red_flag_warning_parameters_using_wind_speed(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']

            frac = 9/5
            temperature_f = (frac * (temperature - 273.15)) + 32

            wind_speed = ds['wind10m']
            wind_speed_mph = wind_speed * 2.23694
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
            temperature_to_plot = temperature_f[0, :, :]
            wind_speed_to_plot = wind_speed_mph[0, :, :]
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100, temperature_to_plot, wind_speed_to_plot

        def get_RTMA_red_flag_warning_parameters_using_wind_gust(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']

            frac = 9/5
            temperature_f = (frac * (temperature - 273.15)) + 32

            wind_gust = ds['gust10m']
            wind_gust_mph = wind_gust * 2.23694
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
            temperature_to_plot = temperature_f[0, :, :]
            wind_gust_to_plot = wind_gust_mph[0, :, :]
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100, temperature_to_plot, wind_gust_to_plot


        def get_RTMA_Data_24_hour_change_relative_humidity(current_time):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            times = []
            times_24 = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)
                time_24 = pd.to_datetime(time - timedelta(hours=24))
                times_24.append(time_24)

            ### LATEST TIME URLS ###
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[0].strftime('%Y%m%d')+'/akrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[1].strftime('%Y%m%d')+'/akrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[2].strftime('%Y%m%d')+'/akrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[3].strftime('%Y%m%d')+'/akrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times[4].strftime('%Y%m%d')+'/akrtma_anl_'+times[4].strftime('%H')+'z'


            ### 24 HOURS AGO URLS ###
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[0].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[1].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[2].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[3].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/akrtma/akrtma'+times_24[4].strftime('%Y%m%d')+'/akrtma_anl_'+times_24[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + times_24[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]
                time_24 = times_24[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + times_24[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]
                    time_24 = times_24[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + times_24[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]
                            time_24 = times_24[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + times_24[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]
                                time_24 = times_24[3]
                                
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times_24[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
                                    time_24 = times_24[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            temperature = ds['tmp2m']
            temperature_24 = ds_24['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            dewpoint_24 = ds_24['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            temperature_k_24 = units('kelvin') * temperature_24
            dewpoint_k_24 = units('kelvin') * dewpoint_24
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_24 = mpcalc.relative_humidity_from_dewpoint(temperature_k_24, dewpoint_k_24)

            diff = relative_humidity[0, :, :] - relative_humidity_24[0, :, :]
                
            return lon_vals, lat_vals, time, time_24, diff * 100



    class RTMA_Hawaii:
        
        r'''
        THIS CLASS HOSTS FUNCTIONS THAT RETRIEVE THE REAL TIME MESOSCALE ANALYSIS DATA FOR HAWAII
        
        '''

        def get_RTMA_Data_single_parameter(current_time, parameter):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            param = parameter
            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                strtime = times[0]
                
            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    strtime = times[1]
                    
                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            strtime = times[2]
                            
                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                strtime = times[3]
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    strtime = times[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            try:
                parameter_data = ds[parameter]
                lat = parameter_data['lat']
                lon = parameter_data['lon']
                
                lat_vals = lat[:].squeeze()
                lon_vals = lon[:].squeeze()

                # CONVERTS KELVIN TO FAHRENHEIT
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    parameter_data = (frac * (parameter_data - 273.15)) + 32

                # CONVERTS M/S TO MPH
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    parameter_data = parameter_data * 2.23694

                if param == 'wdir10m':
                    parameter_data = units('degree') * parameter_data

                # CONVERTS METERS TO FEET
                if param == 'vissfc' or param == 'ceilceil':
                    parameter_data = parameter_data * 3.28084

                # CONVERTS PASCALS TO HECTOPASCALS
                if param == 'pressfc':
                    parameter_data = parameter_data * 0.01

                if param == 'tcdcclm':
                    parameter_data = units('percent') * parameter_data

                data_to_plot = parameter_data[0, :, :]
                
                return lon_vals, lat_vals, strtime, data_to_plot
                
            except Exception as f:
                error = info.invalid_parameter_NOMADS_RTMA_Alaska()
                print(error)

                

        def get_RTMA_Data_24_hour_change_single_parameter(current_time, parameter):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            param = parameter
            times = []
            times_24 = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)
                time_24 = pd.to_datetime(time - timedelta(hours=24))
                times_24.append(time_24)

            ### LATEST TIME URLS ###
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'


            ### 24 HOURS AGO URLS ###
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[0].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[1].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[2].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[3].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[4].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + times_24[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]
                time_24 = times_24[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + times_24[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]
                    time_24 = times_24[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + times_24[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]
                            time_24 = times_24[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + times_24[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]
                                time_24 = times_24[3]
                            
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times_24[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
                                    time_24 = times_24[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            try:
                parameter_data = ds[parameter]
                lat = parameter_data['lat']
                lon = parameter_data['lon']
                
                lat_vals = lat[:].squeeze()
                lon_vals = lon[:].squeeze()

                parameter_data_24 = ds_24[parameter]

                # CONVERT KELVIN TO FAHRENHEIT
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    parameter_data = (frac * (parameter_data - 273.15)) + 32
                    parameter_data_24 = (frac * (parameter_data_24 - 273.15)) + 32

                # CONVERT M/S TO MPH
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    parameter_data = parameter_data * 2.23694
                    parameter_data_24 = parameter_data_24 * 2.23694

                if param == 'wdir10m':
                    parameter_data = units('degree') * parameter_data
                    parameter_data_24 = units('degree') * parameter_data_24

                # CONVERT METERS TO FEET
                if param == 'vissfc' or param == 'ceilceil':
                    parameter_data = parameter_data * 3.28084
                    parameter_data = parameter_data * 3.28084

                # CONVERT PASCALS TO HECTOPASCALS
                if param == 'pressfc':
                    parameter_data = parameter_data * 0.01
                    parameter_data_24 = parameter_data_24 * 0.01

                if param == 'tcdcclm':
                    parameter_data = units('percent') * parameter_data
                    parameter_data_24 = units('percent') * parameter_data_24

                data_to_plot = parameter_data[0, :, :] - parameter_data_24[0, :, :]
                
                return lon_vals, lat_vals, time, time_24, data_to_plot
                
            except Exception as f:
                error = info.invalid_parameter_NOMADS_RTMA_Alaska()
                print(error)

        
        def get_RTMA_relative_humidity(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100


        def get_RTMA_red_flag_warning_parameters_using_wind_speed(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']

            wind_speed = ds['wind10m']
            wind_speed_mph = wind_speed * 2.23694
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
            wind_speed_to_plot = wind_speed_mph[0, :, :]
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100, wind_speed_to_plot


        def get_RTMA_red_flag_warning_parameters_using_wind_gust(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']

            wind_gust = ds['gust10m']
            wind_gust_mph = wind_gust * 2.23694
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
            wind_gust_to_plot = wind_gust_mph[0, :, :]
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100, wind_gust_to_plot


        def get_RTMA_Data_24_hour_change_relative_humidity(current_time):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            times = []
            times_24 = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)
                time_24 = pd.to_datetime(time - timedelta(hours=24))
                times_24.append(time_24)

            ### LATEST TIME URLS ###
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[0].strftime('%Y%m%d')+'/hirtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[1].strftime('%Y%m%d')+'/hirtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[2].strftime('%Y%m%d')+'/hirtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[3].strftime('%Y%m%d')+'/hirtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times[4].strftime('%Y%m%d')+'/hirtma_anl_'+times[4].strftime('%H')+'z'


            ### 24 HOURS AGO URLS ###
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[0].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[1].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[2].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[3].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/hirtma/hirtma'+times_24[4].strftime('%Y%m%d')+'/hirtma_anl_'+times_24[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + times_24[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]
                time_24 = times_24[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + times_24[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]
                    time_24 = times_24[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + times_24[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]
                            time_24 = times_24[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + times_24[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]
                                time_24 = times_24[3]
                                
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times_24[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
                                    time_24 = times_24[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            temperature = ds['tmp2m']
            temperature_24 = ds_24['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            dewpoint_24 = ds_24['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            temperature_k_24 = units('kelvin') * temperature_24
            dewpoint_k_24 = units('kelvin') * dewpoint_24
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_24 = mpcalc.relative_humidity_from_dewpoint(temperature_k_24, dewpoint_k_24)

            diff = relative_humidity[0, :, :] - relative_humidity_24[0, :, :]
                
            return lon_vals, lat_vals, time, time_24, diff * 100


    class RTMA_Puerto_Rico:
        
        r'''
        THIS CLASS HOSTS FUNCTIONS THAT RETRIEVE THE REAL TIME MESOSCALE ANALYSIS DATA FOR HAWAII
        
        '''

        def get_RTMA_Data_single_parameter(current_time, parameter):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            param = parameter
            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[0].strftime('%Y%m%d')+'/prrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[1].strftime('%Y%m%d')+'/prrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[2].strftime('%Y%m%d')+'/prrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[3].strftime('%Y%m%d')+'/prrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[4].strftime('%Y%m%d')+'/prrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                strtime = times[0]
                
            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    strtime = times[1]
                    
                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            strtime = times[2]
                            
                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                strtime = times[3]
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    strtime = times[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            try:
                parameter_data = ds[parameter]
                lat = parameter_data['lat']
                lon = parameter_data['lon']
                
                lat_vals = lat[:].squeeze()
                lon_vals = lon[:].squeeze()

                # CONVERTS KELVIN TO FAHRENHEIT
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    parameter_data = (frac * (parameter_data - 273.15)) + 32

                # CONVERTS M/S TO MPH
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    parameter_data = parameter_data * 2.23694

                if param == 'wdir10m':
                    parameter_data = units('degree') * parameter_data

                # CONVERTS METERS TO FEET
                if param == 'vissfc' or param == 'ceilceil':
                    parameter_data = parameter_data * 3.28084

                # CONVERTS PASCALS TO HECTOPASCALS
                if param == 'pressfc':
                    parameter_data = parameter_data * 0.01

                if param == 'tcdcclm':
                    parameter_data = units('percent') * parameter_data

                data_to_plot = parameter_data[0, :, :]
                
                return lon_vals, lat_vals, strtime, data_to_plot
                
            except Exception as f:
                error = info.invalid_parameter_NOMADS_RTMA_Alaska()
                print(error)

                

        def get_RTMA_Data_24_hour_change_single_parameter(current_time, parameter):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            param = parameter
            times = []
            times_24 = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)
                time_24 = pd.to_datetime(time - timedelta(hours=24))
                times_24.append(time_24)

            ### LATEST TIME URLS ###
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[0].strftime('%Y%m%d')+'/prrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[1].strftime('%Y%m%d')+'/prrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[2].strftime('%Y%m%d')+'/prrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[3].strftime('%Y%m%d')+'/prrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[4].strftime('%Y%m%d')+'/prrtma_anl_'+times[4].strftime('%H')+'z'


            ### 24 HOURS AGO URLS ###
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[0].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[1].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[2].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[3].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[4].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + times_24[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]
                time_24 = times_24[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + times_24[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]
                    time_24 = times_24[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + times_24[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]
                            time_24 = times_24[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + times_24[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]
                                time_24 = times_24[3]
                            
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times_24[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
                                    time_24 = times_24[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            try:
                parameter_data = ds[parameter]
                lat = parameter_data['lat']
                lon = parameter_data['lon']
                
                lat_vals = lat[:].squeeze()
                lon_vals = lon[:].squeeze()

                parameter_data_24 = ds_24[parameter]

                # CONVERT KELVIN TO FAHRENHEIT
                if param == 'tmp2m' or param == 'dpt2m':
                    frac = 9/5
                    parameter_data = (frac * (parameter_data - 273.15)) + 32
                    parameter_data_24 = (frac * (parameter_data_24 - 273.15)) + 32

                # CONVERT M/S TO MPH
                if param == 'wind10m' or param == 'gust10m' or param == 'ugrd10m' or param == 'vgrd10m':
                    parameter_data = parameter_data * 2.23694
                    parameter_data_24 = parameter_data_24 * 2.23694

                if param == 'wdir10m':
                    parameter_data = units('degree') * parameter_data
                    parameter_data_24 = units('degree') * parameter_data_24

                # CONVERT METERS TO FEET
                if param == 'vissfc' or param == 'ceilceil':
                    parameter_data = parameter_data * 3.28084
                    parameter_data = parameter_data * 3.28084

                # CONVERT PASCALS TO HECTOPASCALS
                if param == 'pressfc':
                    parameter_data = parameter_data * 0.01
                    parameter_data_24 = parameter_data_24 * 0.01

                if param == 'tcdcclm':
                    parameter_data = units('percent') * parameter_data
                    parameter_data_24 = units('percent') * parameter_data_24

                data_to_plot = parameter_data[0, :, :] - parameter_data_24[0, :, :]
                
                return lon_vals, lat_vals, time, time_24, data_to_plot
                
            except Exception as f:
                error = info.invalid_parameter_NOMADS_RTMA_Alaska()
                print(error)

        
        def get_RTMA_relative_humidity(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[0].strftime('%Y%m%d')+'/prrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[1].strftime('%Y%m%d')+'/prrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[2].strftime('%Y%m%d')+'/prrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[3].strftime('%Y%m%d')+'/prrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[4].strftime('%Y%m%d')+'/prrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100


        def get_RTMA_Data_24_hour_change_relative_humidity(current_time):

            r'''

            THIS FUNCTION RETRIEVES THE RTMA DATA FOR A SINGLE PARAMETER

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''
            times = []
            times_24 = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)
                time_24 = pd.to_datetime(time - timedelta(hours=24))
                times_24.append(time_24)

            ### LATEST TIME URLS ###
            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[0].strftime('%Y%m%d')+'/prrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[1].strftime('%Y%m%d')+'/prrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[2].strftime('%Y%m%d')+'/prrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[3].strftime('%Y%m%d')+'/prrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[4].strftime('%Y%m%d')+'/prrtma_anl_'+times[4].strftime('%H')+'z'


            ### 24 HOURS AGO URLS ###
            url_5 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[0].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[0].strftime('%H')+'z'
            url_6 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[1].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[1].strftime('%H')+'z'
            url_7 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[2].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[2].strftime('%H')+'z'
            url_8 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[3].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[3].strftime('%H')+'z'
            url_9 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times_24[4].strftime('%Y%m%d')+'/prrtma_anl_'+times_24[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                ds_24 = xr.open_dataset(url_5, engine='netcdf4')
                print("Data was successfully retrieved for " + times_24[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]
                time_24 = times_24[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds_24 = xr.open_dataset(url_6, engine='netcdf4')
                    print("Data was successfully retrieved for " + times_24[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]
                    time_24 = times_24[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds_24 = xr.open_dataset(url_7, engine='netcdf4')
                            print("Data was successfully retrieved for " + times_24[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]
                            time_24 = times_24[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds_24 = xr.open_dataset(url_8, engine='netcdf4')
                                print("Data was successfully retrieved for " + times_24[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]
                                time_24 = times_24[3]
                                
                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds_24 = xr.open_dataset(url_9, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times_24[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
                                    time_24 = times_24[4]
                                    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            temperature = ds['tmp2m']
            temperature_24 = ds_24['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            dewpoint_24 = ds_24['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            temperature_k_24 = units('kelvin') * temperature_24
            dewpoint_k_24 = units('kelvin') * dewpoint_24
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_24 = mpcalc.relative_humidity_from_dewpoint(temperature_k_24, dewpoint_k_24)

            diff = relative_humidity[0, :, :] - relative_humidity_24[0, :, :]
                
            return lon_vals, lat_vals, time, time_24, diff * 100


        def get_RTMA_red_flag_warning_parameters_using_wind_speed(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[0].strftime('%Y%m%d')+'/prrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[1].strftime('%Y%m%d')+'/prrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[2].strftime('%Y%m%d')+'/prrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[3].strftime('%Y%m%d')+'/prrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[4].strftime('%Y%m%d')+'/prrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']

            wind_speed = ds['wind10m']
            wind_speed_mph = wind_speed * 2.23694
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
            wind_speed_to_plot = wind_speed_mph[0, :, :]
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100, wind_speed_to_plot


        def get_RTMA_red_flag_warning_parameters_using_wind_gust(current_time):

            r'''
            THIS FUNCTION RETRIVES THE RTMA DATA FOR THE USUAL FIRE WEATHER PARAMETERS (TEMPERATURE, DEWPOINT, WIND SPEED AND RELATIVE HUMIDITY

            (C) METEOROLOGIST ERIC J. DREWITZ 2024

            '''

            
            times = []
            for i in range(0, 5):
                time = pd.to_datetime(current_time - timedelta(hours=i))
                times.append(time)

            url_0 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[0].strftime('%Y%m%d')+'/prrtma_anl_'+times[0].strftime('%H')+'z'
            url_1 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[1].strftime('%Y%m%d')+'/prrtma_anl_'+times[1].strftime('%H')+'z'
            url_2 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[2].strftime('%Y%m%d')+'/prrtma_anl_'+times[2].strftime('%H')+'z'
            url_3 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[3].strftime('%Y%m%d')+'/prrtma_anl_'+times[3].strftime('%H')+'z'
            url_4 = 'http://nomads.ncep.noaa.gov:80/dods/prrtma/prrtma'+times[4].strftime('%Y%m%d')+'/prrtma_anl_'+times[4].strftime('%H')+'z'

            try:
                ds = xr.open_dataset(url_0, engine='netcdf4')
                print("Data was successfully retrieved for " + times[0].strftime('%m/%d/%Y %HZ'))
                time = times[0]

            except Exception as a:
                try:
                    print("There is no data for " + times[0].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[1].strftime('%m/%d/%Y %HZ'))
                    ds = xr.open_dataset(url_1, engine='netcdf4')
                    print("Data was successfully retrieved for " + times[1].strftime('%m/%d/%Y %HZ'))
                    time = times[1]

                except Exception as b:
                        try:
                            print("There is no data for " + times[1].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[2].strftime('%m/%d/%Y %HZ'))
                            ds = xr.open_dataset(url_2, engine='netcdf4')
                            print("Data was successfully retrieved for " + times[2].strftime('%m/%d/%Y %HZ'))
                            time = times[2]

                        except Exception as c:
                            try:
                                print("There is no data for " + times[2].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[3].strftime('%m/%d/%Y %HZ'))
                                ds = xr.open_dataset(url_3, engine='netcdf4')
                                print("Data was successfully retrieved for " + times[3].strftime('%m/%d/%Y %HZ'))
                                time = times[3]

                            except Exception as d:
    
                                try:
                                    print("There is no data for " + times[3].strftime('%m/%d/%Y %HZ') + " trying to retrieve data from the previous analysis at " + times[4].strftime('%m/%d/%Y %HZ'))
                                    ds = xr.open_dataset(url_4, engine='netcdf4')
                                    print("Data was successfully retrieved for " + times[4].strftime('%m/%d/%Y %HZ'))
                                    time = times[4]
    
                                except Exception as e:
                                    print("The latest dataset is over 4 hours old which isn't current. Please try again later.")
            
            temperature = ds['tmp2m']
            lat = temperature['lat']
            lon = temperature['lon']

            wind_gust = ds['gust10m']
            wind_gust_mph = wind_gust * 2.23694
            
            lat_vals = lat[:].squeeze()
            lon_vals = lon[:].squeeze()
            
            dewpoint = ds['dpt2m']
            temperature_k = units('kelvin') * temperature
            dewpoint_k = units('kelvin') * dewpoint
            
            relative_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_k, dewpoint_k)

            relative_humidity_to_plot = relative_humidity[0, :, :] 
            wind_gust_to_plot = wind_gust_mph[0, :, :]
                
            return lon_vals, lat_vals, time, relative_humidity_to_plot * 100, wind_gust_to_plot


