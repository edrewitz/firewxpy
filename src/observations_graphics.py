r'''
This file hosts the current and past observation graphics without the 2.5km x 2.5km Real Time Mesoscale Analysis Data. 
The functions in this file only make graphics from the METAR data. 

This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import pytz
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import parsers
import data_access as da
import geometry
import calc
import colormaps
import pandas as pd
import matplotlib.gridspec as gridspec

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from NWS_Generic_Forecast_Graphics import standard
from dateutil import tz

def daily_weather_summary_previous_day(station_id):
    maximum_temperature, maximum_temperature_time, maximum_temperature_time_local, minimum_temperature, minimum_temperature_time, minimum_temperature_time_local, minimum_relative_humidity, minimum_relative_humidity_time, minimum_relative_humidity_time_local, maximum_relative_humidity, maximum_relative_humidity_time, maximum_relative_humidity_time_local, maximum_wind_speed, wind_direction, maximum_wind_speed_time, maximum_wind_speed_time_local, maximum_wind_gust, maximum_wind_gust_time, maximum_wind_gust_time_local, station_id, date = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.previous_day_weather_summary(station_id)

    fig = plt.figure(figsize=(7,5))
    fig.set_facecolor('bisque')
    plt.axis('off')

    fig.text(0.1, 0.85, station_id + " Daily Weather Summary\n         Date: " + date.strftime('%m/%d/%Y'), color='black', fontsize=25, fontweight='bold') 
    
    try:
        maximum_temperature = int(round(maximum_temperature, 0))
        fig.text(0.15, 0.77, "Maximum Temperature: " + str(maximum_temperature) +" (\N{DEGREE SIGN}F)", color='red', fontsize=18, fontweight='bold')
        fig.text(0.15, 0.73, "Time of occurrence: "+ maximum_temperature_time_local.strftime('%H:%M Local') + " ("+ maximum_temperature_time.strftime('%H:%M UTC')+")", color='red', fontsize=14, fontweight='bold')
        
    except Exception as a:
        fig.text(0.15, 0.77, "Maximum Temperature: Not Available", color='red', fontsize=18, fontweight='bold')

    try:
        minimum_temperature = int(round(minimum_temperature, 0))
        fig.text(0.15, 0.66, "Minimum Temperature: " + str(minimum_temperature) +" (\N{DEGREE SIGN}F)", color='blue', fontsize=18, fontweight='bold')
        fig.text(0.15, 0.62, "Time of occurrence: "+ minimum_temperature_time_local.strftime('%H:%M Local') + " ("+ minimum_temperature_time.strftime('%H:%M UTC')+")", color='blue', fontsize=14, fontweight='bold')
    except Exception as b:
        fig.text(0.15, 0.66, "Minimum Temperature: Not Available", color='blue', fontsize=18, fontweight='bold')

    try:
        maximum_relative_humidity = int(round(maximum_relative_humidity, 0))
        fig.text(0.15, 0.55, "Maximum Relative Humidity: " + str(maximum_relative_humidity) +" (%)", color='darkgreen', fontsize=18, fontweight='bold')
        fig.text(0.15, 0.51, "Time of occurrence: "+ maximum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ maximum_relative_humidity_time.strftime('%H:%M UTC')+")", color='darkgreen', fontsize=14, fontweight='bold')
    except Exception as c:
        fig.text(0.15, 0.55, "Maximum Relative Humidity: Not Available", color='darkgreen', fontsize=18, fontweight='bold')

    try:
        minimum_relative_humidity = int(round(minimum_relative_humidity, 0))
        fig.text(0.15, 0.44, "Minimum Relative Humidity: " + str(minimum_relative_humidity) +" (%)", color='saddlebrown', fontsize=18, fontweight='bold')
        fig.text(0.15, 0.4, "Time of occurrence: "+ minimum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ minimum_relative_humidity_time.strftime('%H:%M UTC')+")", color='saddlebrown', fontsize=14, fontweight='bold')
    except Exception as d:
        fig.text(0.15, 0.44, "Minimum Relative Humidity: Not Available", color='saddlebrown', fontsize=18, fontweight='bold')

    try:
        maximum_wind_speed = int(round(maximum_wind_speed, 0))
        fig.text(0.15, 0.33, "Maximum Wind Speed: " + wind_direction + " at " + str(maximum_wind_speed) +" (MPH)", color='magenta', fontsize=18, fontweight='bold')
        fig.text(0.15, 0.29, "Time of occurrence: "+ maximum_wind_speed_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_speed_time.strftime('%H:%M UTC')+")", color='magenta', fontsize=14, fontweight='bold')
    except Exception as e:
        fig.text(0.15, 0.33, "Maximum Wind Speed: Not Available", color='magenta', fontsize=18, fontweight='bold')

    try:
        maximum_wind_gust = int(round(maximum_wind_gust, 0))
        fig.text(0.15, 0.22, "Maximum Wind Gust: " + str(maximum_wind_gust) +" (MPH)", color='purple', fontsize=18, fontweight='bold')
        fig.text(0.15, 0.18, "Time of occurrence: "+ maximum_wind_gust_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_gust_time.strftime('%H:%M UTC')+")", color='purple', fontsize=14, fontweight='bold')
    except Exception as f:
        fig.text(0.15, 0.22, "Maximum Wind Gust: Not Available", color='purple', fontsize=18, fontweight='bold')
        
    local_time, utc_time = standard.plot_creation_time()

    fig.text(0.15, 0.05, "Table Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC')+")", fontsize=12, fontweight='bold')

    return fig
