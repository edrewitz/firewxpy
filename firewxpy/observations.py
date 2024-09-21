
r'''
This file hosts the current and past observation graphics without the 2.5km x 2.5km Real Time Mesoscale Analysis Data. 
The functions in this file only make graphics from the METAR data. 

This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''

import pytz
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import firewxpy.parsers
import firewxpy.calc
import firewxpy.colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib.dates as md
import firewxpy.standard as standard

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from dateutil import tz
from pysolar import solar, radiation
from firewxpy.utilities import file_functions
from firewxpy.data_access import previous_day_weather_summary_and_all_data

mpl.rcParams['font.weight'] = 'bold'

def graphical_daily_summary(station_id):


    r'''
    This function creates a graphical daily weather summary and solar information for the previous day's ASOS observations at any particular ASOS site. 

    Required Arguments: 1) station_id (String) - The 4-letter station identifier of the ASOS station

    Optional Arguments: 1) file_save_path (String) - The file path at which the user wants to save the image to. Default is set to None
                                                     which returns the figure without saving it anywhere. 

    Returns: A figure showing a graphical daily weather summary and solar information for the previous day's ASOS observations. 
             The parameters on this daily weather summary are: 1) Temperature
                                                               2) Relative Humidity
                                                               3) Wind Speed
                                                               4) Solar Elevation Angle
                                                               5) Solar Radiation
    

    '''

    station_id = station_id.upper()

    df, maximum_temperature, maximum_temperature_time, maximum_temperature_time_local, minimum_temperature, minimum_temperature_time, minimum_temperature_time_local, minimum_relative_humidity, minimum_relative_humidity_time, minimum_relative_humidity_time_local, maximum_relative_humidity, maximum_relative_humidity_time, maximum_relative_humidity_time_local, maximum_wind_speed, wind_dir, maximum_wind_speed_time, maximum_wind_speed_time_local, maximum_wind_gust, maximum_wind_gust_time, maximum_wind_gust_time_local, station_id, previous_day_utc = previous_day_weather_summary_and_all_data(station_id)

    time = df['date_time']
    time = pd.to_datetime(time)
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    start = time.iloc[0]
    year = start.year
    month = start.month
    day = start.day
    
    start = datetime(year, month, day, tzinfo=to_zone)
    start_summer_solstice = datetime(year, 6, 21, tzinfo=to_zone)
    start_winter_solstice = datetime(year, 12, 21, tzinfo=to_zone)
    start_equinox = datetime(year, 3, 21, tzinfo=to_zone)
    times_list = [start + timedelta(minutes=i *15) for i in range(24*4)]
    times_list_summer_solstice = [start_summer_solstice + timedelta(minutes=i *15) for i in range(24*4)]
    times_list_winter_solstice = [start_winter_solstice + timedelta(minutes=i *15) for i in range(24*4)]
    times_list_equinox = [start_equinox + timedelta(minutes=i *15) for i in range(24*4)]
    
    temperature = df['air_temperature']
    relative_humidity = df['relative_humidity']
    wind_speed = df['wind_speed']
    latitude = df['latitude'].iloc[0]
    longitude = df['longitude'].iloc[0]
    
    
    solar_elevation = [solar.get_altitude(latitude, longitude, t) for t in times_list]
    solar_radiation = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list, solar_elevation)]
    
    solar_elevation_summer = [solar.get_altitude(latitude, longitude, t) for t in times_list_summer_solstice]
    solar_radiation_summer = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_summer_solstice, solar_elevation_summer)]
    
    solar_elevation_winter = [solar.get_altitude(latitude, longitude, t) for t in times_list_winter_solstice]
    solar_radiation_winter = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_winter_solstice, solar_elevation_winter)]
    
    solar_elevation_equinox = [solar.get_altitude(latitude, longitude, t) for t in times_list_equinox]
    solar_radiation_equinox = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_equinox, solar_elevation_equinox)]
    
    max_elevation = np.nanmax(solar_elevation)
    min_elevation = np.nanmin(solar_elevation)

    max_elevation_summer = np.nanmax(solar_elevation_summer)
    min_elevation_summer = np.nanmin(solar_elevation_summer)

    max_elevation_winter = np.nanmax(solar_elevation_winter)
    min_elevation_winter = np.nanmin(solar_elevation_winter)

    max_elevation_equinox = np.nanmax(solar_elevation_equinox)
    min_elevation_equinox = np.nanmin(solar_elevation_equinox)

    max_rad = np.nanmax(solar_radiation)

    diff_ele_ss = max_elevation - max_elevation_summer
    diff_ele_ws = max_elevation - max_elevation_winter
    diff_ele_e = max_elevation - max_elevation_equinox


    plt.style.use('seaborn-v0_8-darkgrid')
    
    
    fig = plt.figure(figsize=(10,12))
    fig.suptitle(station_id + " Daily Weather Summary | Date: " + previous_day_utc.strftime('%m/%d/%Y'), color='white', fontsize=28, fontweight='bold')
    
    if latitude >= 0 and longitude <= 0:
        fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}N) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}W)", color='white', fontsize=20, fontweight='bold')
    if latitude >= 0 and longitude > 0:
        fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}N) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}E)", color='white', fontsize=20, fontweight='bold')
    if latitude < 0 and longitude <= 0:
        fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}S) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}W)", color='white', fontsize=20, fontweight='bold')
    if latitude < 0 and longitude > 0:
        fig.text(0.125, 0.925, "Station Latitude: " + str(round(abs(latitude), 1)) + " (\N{DEGREE SIGN}S) | Station Longitude: " + str(round(abs(longitude), 1)) + " (\N{DEGREE SIGN}E)", color='white', fontsize=20, fontweight='bold')
    
    
    
    fig.set_facecolor('gray')
    gs = gridspec.GridSpec(3, 2)
    
    
    ax0 = fig.add_subplot(gs[0:1, 0:1])
    ax0.plot(time, temperature, c='red')
    ax0.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax0.set_ylim(int(round(minimum_temperature - 2, 0)), int(round(maximum_temperature + 2, 0)))
    ax0.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax0.set_ylabel("Temperature (\N{DEGREE SIGN}F)", color='white', fontsize=8, fontweight='bold')
    ax0.set_title("Temperature", color='white', fontsize=11, fontweight='bold')
    ax0.tick_params(axis='x', colors='white')
    ax0.tick_params(axis='y', colors='white')
    
    ax1 = fig.add_subplot(gs[1:2, 0:1])
    ax1.plot(time, relative_humidity, c='green')
    ax1.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax1.set_ylim(minimum_relative_humidity - 5, maximum_relative_humidity + 5)
    ax1.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax1.set_ylabel("Relative Humidity (%)", color='white', fontsize=8, fontweight='bold')
    ax1.set_title("Relative Humidity", color='white', fontsize=11, fontweight='bold')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    
    ax2 = fig.add_subplot(gs[2:3, 0:1])
    ax2.plot(time, wind_speed, c='purple')
    ax2.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax2.set_ylim(0, maximum_wind_speed + 2)
    ax2.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax2.set_ylabel("Wind Speed (MPH)", color='white', fontsize=8, fontweight='bold')
    ax2.set_title("Wind Speed", color='white', fontsize=11, fontweight='bold')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    
    ax3 = fig.add_subplot(gs[0:1, 1:2])
    ax3.plot(times_list, solar_elevation, c='orange', label=start.strftime('%m/%d'), alpha=0.5)
    ax3.plot(times_list, solar_elevation_summer, c='red', label='Summer Solstice', alpha=0.5)
    ax3.plot(times_list, solar_elevation_winter, c='blue', label='Winter Solstice', alpha=0.5)
    ax3.plot(times_list, solar_elevation_equinox, c='magenta', label='Equinox', alpha=0.5)
    ax3.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax3.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax3.set_ylabel("Solar Elevation Angle (Degrees)", color='white', fontsize=8, fontweight='bold')
    ax3.set_title("Solar Elevation Angle", color='white', fontsize=11, fontweight='bold')
    ax3.axhline(0, c='black', linestyle='--', linewidth=2)
    fig.text(0.55, 0.855, "Elevation Angle > 0 = Day\nElevation Angle < 0 = Night", fontsize=9, fontweight='bold')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.legend(loc=(0.3,0.01), prop={'size': 8})
    
    ax4 = fig.add_subplot(gs[1:2, 1:2])
    ax4.plot(times_list, solar_radiation, c='orange')
    ax4.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax4.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax4.set_ylabel("Solar Radiation (W/m^2)", color='white', fontsize=8, fontweight='bold')
    ax4.set_title("Solar Radiation", color='white', fontsize=11, fontweight='bold')
    ax4.tick_params(axis='x', colors='white')
    ax4.tick_params(axis='y', colors='white')


    local_time, utc_time = standard.plot_creation_time()

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    try:
        maximum_temperature = int(round(maximum_temperature, 0))
        maximum_temperature = str(maximum_temperature)
        maximum_temperature_time_local = maximum_temperature_time_local.strftime('%H:%M Local')
        maximum_temperature_time = maximum_temperature_time.strftime('%H:%M UTC')
    except Exception as e:
        maximum_temperature = 'NA'
        maximum_temperature_time_local = 'NA'
        maximum_temperature_time = 'NA'
    try:
        minimum_temperature = int(round(minimum_temperature, 0))
        minimum_temperature = str(minimum_temperature)
        minimum_temperature_time_local = minimum_temperature_time_local.strftime('%H:%M Local')
        minimum_temperature_time = minimum_temperature_time.strftime('%H:%M UTC')
    except Exception as e:
        minimum_temperature = 'NA'
        minimum_temperature_time_local = 'NA'
        minimum_temperature_time = 'NA'
    try:
        maximum_relative_humidity = int(round(maximum_relative_humidity, 0))
        maximum_relative_humidity = str(maximum_relative_humidity)
        maximum_relative_humidity_time_local = maximum_relative_humidity_time_local.strftime('%H:%M Local')
        maximum_relative_humidity_time = maximum_relative_humidity_time.strftime('%H:%M UTC')
    except Exception as e:
        maximum_relative_humidity = 'NA'
        maximum_relative_humidity_time_local = 'NA'
        maximum_relative_humidity_time = 'NA'
    try:
        minimum_relative_humidity = int(round(minimum_relative_humidity, 0))
        minimum_relative_humidity = str(minimum_relative_humidity)
        minimum_relative_humidity_time_local = minimum_relative_humidity_time_local.strftime('%H:%M Local')
        minimum_relative_humidity_time = minimum_relative_humidity_time.strftime('%H:%M UTC')
    except Exception as e:
        minimum_relative_humidity = 'NA'
        minimum_relative_humidity_time_local = 'NA'
        minimum_relative_humidity_time = 'NA'
    try:
        maximum_wind_speed = int(round(maximum_wind_speed, 0))
        maximum_wind_speed = str(maximum_wind_speed)
        maximum_wind_speed_time_local = maximum_wind_speed_time_local.strftime('%H:%M Local')
        maximum_wind_speed_time = maximum_wind_speed_time.strftime('%H:%M UTC')
    except Exception as e:
        maximum_wind_speed = 'NA'
        maximum_wind_speed_time_local = 'NA'
        maximum_wind_speed_time = 'NA'
    try:
        maximum_wind_gust = int(round(maximum_wind_gust, 0))
        maximum_wind_gust = str(maximum_wind_gust)
        maximum_wind_gust_time_local = maximum_wind_gust_time_local.strftime('%H:%M Local')
        maximum_wind_gust_time = maximum_wind_gust_time.strftime('%H:%M UTC')
    except Exception as e:
        maximum_wind_gust = 'NA'
        maximum_wind_gust_time_local = 'NA'
        maximum_wind_gust_time = 'NA'

    if diff_ele_e >= 0:
        sym='+'
    else:
        sym=''

    if max_elevation >= 0:
        sym1 = '+'
    else:
        sym1 = ''

    if min_elevation >= 0:
        sym2 = '+'
    else:
        sym2 = ''

    if max_elevation_equinox >= 0:
        sym3 = '+'
    else:
        sym3 = ''

    if max_elevation_winter >= 0:
        sym4 = '+'
    else:
        sym4 = ''

    fig.text(0.55, 0.115, "Maximum Temperature: " +maximum_temperature +" [\N{DEGREE SIGN}F] " + maximum_temperature_time_local + " ("+ maximum_temperature_time+")\n\nMinimum Temperature: " + minimum_temperature +" [\N{DEGREE SIGN}F] "+ minimum_temperature_time_local + " ("+ minimum_temperature_time+")\n\nMaximum RH: " + maximum_relative_humidity +" [%] "+ maximum_relative_humidity_time_local + " ("+ maximum_relative_humidity_time +")\n\nMinimum RH: " + minimum_relative_humidity +" [%] "+ minimum_relative_humidity_time_local + " ("+ minimum_relative_humidity_time +")\n\nMaximum Wind Speed: " + maximum_wind_speed +" [MPH] "+ maximum_wind_speed_time_local + " ("+ maximum_wind_speed_time +")\n\nMaximum Wind Gust: " + maximum_wind_gust +" [MPH] "+ maximum_wind_gust_time_local + " ("+ maximum_wind_gust_time +")\n\nMaximum Elevation: "+sym1+""+ str(round(max_elevation, 1)) + " [\N{DEGREE SIGN} From Horizon]\n\nMinimum Elevation: "+sym2+""+ str(round(min_elevation, 1)) + " [\N{DEGREE SIGN} From Horizon]\n\nMaximum Elevation Difference:\nSummer Solstice: "+str(round(diff_ele_ss,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym1+""+str(round(max_elevation_summer,1))+" [\N{DEGREE SIGN} From Horizon]\nEquinox: "+sym+""+str(round(diff_ele_e,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym3+""+str(round(max_elevation_equinox,1))+" [\N{DEGREE SIGN} From Horizon]\nWinter Solstice: "+str(round(diff_ele_ws,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym4+""+str(round(max_elevation_winter,1))+" [\N{DEGREE SIGN} From Horizon]\n\nMaximum Solar Radiation: " + str(round(max_rad, 1)) + " (W/m^2)", color='black', fontsize=8, fontweight='bold', bbox=props, zorder=6)

    
    fig.text(0.27, 0.07, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=14, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)    

    file_functions.save_daily_weather_summary(fig, station_id)


    
