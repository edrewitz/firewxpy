"""

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

(C) Eric J. Drewitz 2025
"""
import pandas as pd
import xarray as xr
import netCDF4
import warnings
warnings.filterwarnings('ignore')

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

def get_rtma_datasets(region, current_time):

    """
    
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

    """
    
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