# THIS SCRIPT HAS FUNCTIONS THAT PARSE THROUGH GRIB FILES THAT CONTAIN WEATHER DATA TO RETURN SORTED AND ORGANIZED DATA ARRAYS FOR GRAPHICAL CREATION/PLOTTING
#
# DEPENDENCIES INCLUDE:
# 1. PYGRIB
# 2. DATETIME 
#
#  (C) METEOROLOGIST ERIC J. DREWITZ
#               USDA/USFS

##### IMPORTS NEEDED PYTHON MODULES #######

import pandas as pd

from dateutil import tz
from datetime import datetime, timedelta

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

class NDFD:

    r'''
    This class hosts functions to parse the NDFD GRIB2 files

    '''

    def ndfd_to_dataframe(ds, parameter):

        r'''
        This function parses the NDFD GRIB2 file and converts the data array into a pandas dataframe

        Required Arguments:

        1) ds (xarray.dataarray) - The NDFD GRIB2 dataset

        2) parameter (String) - The variable name. 

        Return: A pandas dataframe of the NDFD values. 

        '''

        ds = ds

        stop = len(ds['step'])

        vals = []

        for i in range(0, stop, 1):
            val = ds[parameter][i, :, :].to_dataframe()
            vals.append(val)

        return vals
        

    def get_valid_times(ds, time_interval):

        r'''
        This function will get all of the forecast validity times for the time length of the grid for the specific weather element in NDFD. 

        Required Arguments:

        1) ds (xarray.dataarray) - The NDFD GRIB2 dataset

        2) time_interval (Integer) - The time length of the grid in hours. 

        Returns: A list of the start and end times in local time for each forecast interval. 

        '''

        ds = ds

        stop = len(ds['step'])

        start_times = []
        end_times = []

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

        return start_times, end_times
        


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







        
