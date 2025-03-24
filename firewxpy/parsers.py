"""
This file is written by (C) Meteorologist Eric J. Drewitz
                                     USDA/USFS

"""

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from dateutil import tz
from datetime import datetime, timedelta
from firewxpy.calc import unit_conversion

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

class NDFD:

    r'''
    This class hosts functions to parse the NDFD GRIB2 files

    '''

    def ndfd_to_dataframe(ds, parameter, diff=False, temperature_to_F=False, decimate=None):

        r'''
        This function parses the NDFD GRIB2 file and converts the data array into a pandas dataframe

        Required Arguments:

        1) ds (xarray.dataarray) - The NDFD GRIB2 dataset

        2) parameter (String) - The variable name. 

        Optional Arguments:

        1) diff (Boolean) - Default = False. If set to True, the difference between value[i+1] and value[i] will be returned (val[i+1] - val[i]). 

        2) temperature_to_F (Boolean) - Default = False. If set to True, values will be converted from Kelvin to Fahrenheit.

        3) decimate (Integer) - Default = None. If set to a non-None value, the data will be decimated on both the x and y coordinates by the magnitude of the set value.

        Return: A pandas dataframe of the NDFD values. 

        '''

        ds = ds

        try:
            stop = len(ds['valid_time'])
        except Exception as e:
            stop = len(ds['step'])

        vals = []

        if temperature_to_F == True:
            ds[parameter] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds[parameter])
        else:
            pass

        if decimate != None:
            if diff == False:
                for i in range(0, stop, 1):
                    val = ds[parameter][i, ::decimate, ::decimate].to_dataframe()
                    vals.append(val) 
            else:
                for i in range(1, stop, 1):
                    try:
                        val = ds[parameter][i, ::decimate, ::decimate] - ds[parameter][i-1, ::decimate, ::decimate]
                        val = val.to_dataframe()
                        vals.append(val)    
                    except Exception as e:
                        pass                
            
        if decimate == None:

            if diff == False:
                for i in range(0, stop, 1):
                    val = ds[parameter][i, :, :].to_dataframe()
                    vals.append(val) 
    
            else:
                for i in range(1, stop, 1):
                    try:
                        val = ds[parameter][i, :, :] - ds[parameter][i-1, :, :]
                        val = val.to_dataframe()
                        vals.append(val)    
                    except Exception as e:
                        pass

        return vals
        

    def get_valid_times_xarray(ds, time_interval):

        r'''
        This function will get all of the forecast validity times for the time length of the grid for the specific weather element in NDFD. 

        Required Arguments:

        1) ds (xarray.dataarray) - The NDFD GRIB2 dataset

        2) time_interval (Integer) - The time length of the grid in hours. 

        Returns: A list of the start and end times in local time for each forecast interval. 

        '''

        ds = ds

        stop = len(ds['valid_time'])

        start_times = []
        end_times = []
        start_times_utc = []

        for i in range(0, stop, 1):
            end_time = ds['valid_time'][i]
            end_time = end_time.to_pandas()
            end_time = pd.to_datetime(end_time)
            end_time = end_time.replace(tzinfo=from_zone)
            end_time = end_time.astimezone(to_zone)
            end_times.append(end_time)

        for i in range(0, stop, 1):
            start_time = end_times[i] - timedelta(hours=time_interval)
            start_times.append(start_time)
            start_time_utc = start_time.replace(tzinfo=to_zone)
            start_time_utc = start_time.astimezone(from_zone)
            start_times_utc.append(start_time_utc)

        return start_times, end_times, start_times_utc

class checks:

    r'''

    This class hosts functions to check various things:

    1) Wind Direction
    2) RTMA vs. METAR Observation times

    '''

    def wind_direction_number_to_abbreviation(wind_direction):

        r'''
        This function takes the numerical wind direction and assigns an abbreviation (i.e. N vs. NW) to the value

        Inputs:
                1) wind_direction (Integer or Float)

        Returns:
                1) wind_direction (String)

        '''
        wind_direction = wind_direction
        
        if wind_direction >= 358 or wind_direction <= 2:
            wind_dir = 'N'
        if wind_direction > 2 and wind_direction <= 30:
            wind_dir = 'NNE'
        if wind_direction > 30 and wind_direction <= 60:
            wind_dir = 'NE'
        if wind_direction > 60 and wind_direction < 88:
            wind_dir = 'ENE'
        if wind_direction >= 88 and wind_direction <= 92:
            wind_dir = 'E'
        if wind_direction > 92 and wind_direction <= 120:
            wind_dir = 'ESE'
        if wind_direction > 120 and wind_direction <= 150:
            wind_dir = 'SE'
        if wind_direction > 150 and wind_direction < 178:
            wind_dir = 'SSE'
        if wind_direction >= 178 and wind_direction <= 182:
            wind_dir = 'S'
        if wind_direction > 182 and wind_direction <= 210:
            wind_dir = 'SSW'
        if wind_direction > 210 and wind_direction <= 240:
            wind_dir = 'SW'
        if wind_direction > 240 and wind_direction < 268:
            wind_dir = 'WSW'
        if wind_direction >= 268 and wind_direction <= 272:
            wind_dir = 'W'
        if wind_direction > 272 and wind_direction <= 300:
            wind_dir = 'WNW'
        if wind_direction > 300 and wind_direction <= 330:
            wind_dir = 'NW'
        if wind_direction > 330 and wind_direction < 358:
            wind_dir = 'NNW'

        return wind_dir
    

    def check_RTMA_vs_METAR_Times(real_time_mesoscale_analysis_time, metar_observation_time):

        r'''
        This function compares the time of the RTMA and the time of the observations to make them match. 

        Required Arguments: 

        1) real_time_mesoscale_analysis_time (datetime) - The time of the RTMA

        2) metar_observation_time (datetime) - The time of the METAR observations

        Returns: The latest time where there is a match between RTMA & METAR Observations

        '''

        metar_time = metar_observation_time

        rtma_time = real_time_mesoscale_analysis_time

        time_diff = metar_time.hour - rtma_time.hour

        if metar_time.hour > rtma_time.hour:
            new_metar_time = metar_time - timedelta(hours=time_diff)

        if metar_time.hour < rtma_time.hour:
            hour = rtma_time.hour
            new_metar_time = metar_time - timedelta(days=1)
            year = new_metar_time.year
            month = new_metar_time.month
            day = new_metar_time.day
            new_metar_time = datetime(year, month, day, hour)

        else:
            new_metar_time = rtma_time
            

        return new_metar_time






        
