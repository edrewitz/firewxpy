
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
import firewxpy.data_access as da
import firewxpy.calc
import firewxpy.colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib.dates as md
import firewxpy.standard

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from dateutil import tz
from pysolar import solar, radiation
from firewxpy.utilities import file_functions

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

    df, maximum_temperature, maximum_temperature_time, maximum_temperature_time_local, minimum_temperature, minimum_temperature_time, minimum_temperature_time_local, minimum_relative_humidity, minimum_relative_humidity_time, minimum_relative_humidity_time_local, maximum_relative_humidity, maximum_relative_humidity_time, maximum_relative_humidity_time_local, maximum_wind_speed, wind_dir, maximum_wind_speed_time, maximum_wind_speed_time_local, maximum_wind_gust, maximum_wind_gust_time, maximum_wind_gust_time_local, station_id, previous_day_utc = da.UCAR_THREDDS_SERVER_OPENDAP_Downloads.METARs.previous_day_weather_summary_and_all_data(station_id)

    time = df['date_time']
    time = pd.to_datetime(time)
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    times = []
    for t in time:
        year = t.year
        month = t.month
        day = t.day
        hour = t.hour
        minute = t.minute
        time_stamp = pd.Timestamp(year, month, day, hour, minute, tz=to_zone)
        times.append(time_stamp)
    
    start = time.iloc[0]
    year = start.year
    month = start.month
    day = start.day
    
    start = datetime(year, month, day, tzinfo=to_zone)
    times_list = [start + timedelta(minutes=i *15) for i in range(24*4)]
    
    temperature = df['air_temperature']
    relative_humidity = df['relative_humidity']
    wind_speed = df['wind_speed']
    latitude = df['latitude'].iloc[0]
    longitude = df['longitude'].iloc[0]
    
    
    solar_elevation = [solar.get_altitude(latitude, longitude, t) for t in times_list]
    solar_radiation = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list, solar_elevation)]
    
    max_elevation = np.nanmax(solar_elevation)
    min_elevation = np.nanmin(solar_elevation)
    max_radiation = np.nanmax(solar_radiation)
    max_temperature = np.nanmax(temperature)
    min_temperature = np.nanmin(temperature)
    max_rh = np.nanmax(relative_humidity)
    min_rh = np.nanmin(relative_humidity)
    max_wind = np.nanmax(wind_speed)
    max_radiation = np.nanmax(solar_radiation)

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
    ax0.set_ylim(minimum_temperature - 2, maximum_temperature + 2)
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
    ax3.plot(times_list, solar_elevation, c='orange')
    ax3.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax3.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax3.set_ylabel("Solar Elevation Angle (Degrees)", color='white', fontsize=8, fontweight='bold')
    ax3.set_title("Solar Elevation Angle", color='white', fontsize=11, fontweight='bold')
    ax3.axhline(0, c='black', linestyle='--', linewidth=2)
    fig.text(0.55, 0.855, "Elevation Angle > 0 = Day\nElevation Angle < 0 = Night", fontsize=9, fontweight='bold')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    
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
    except Exception as e:
        maximum_temperature = 'NA'
    try:
        minimum_temperature = int(round(minimum_temperature, 0))
        minimum_temperature = str(minimum_temperature)
    except Exception as e:
        minimum_temperature = 'NA'
    try:
        maximum_relative_humidity = int(round(maximum_relative_humidity, 0))
        maximum_relative_humidity = str(maximum_relative_humidity)
    except Exception as e:
        maximum_relative_humidity = 'NA'
    try:
        minimum_relative_humidity = int(round(minimum_relative_humidity, 0))
        minimum_relative_humidity = str(minimum_relative_humidity)
    except Exception as e:
        minimum_relative_humidity = 'NA'
    try:
        maximum_wind_speed = int(round(maximum_wind_speed, 0))
        maximum_wind_speed = str(maximum_wind_speed)
    except Exception as e:
        maximum_wind_speed = 'NA'
    try:
        maximum_wind_gust = int(round(maximum_wind_gust, 0))
        maximum_wind_gust = str(maximum_wind_gust)
    except Exception as e:
        maximum_wind_gust = 'NA'

        if maximum_wind_gust != 'NA':

            fig.text(0.487, 0.13, "Maximum Temperature: " +maximum_temperature +" (\N{DEGREE SIGN}F) " + maximum_temperature_time_local.strftime('%H:%M Local') + " ("+ maximum_temperature_time.strftime('%H:%M UTC')+")\n\nMinimum Temperature: " + minimum_temperature +" (\N{DEGREE SIGN}F) "+ minimum_temperature_time_local.strftime('%H:%M Local') + " ("+ minimum_temperature_time.strftime('%H:%M UTC')+")\n\nMaximum RH: " + maximum_relative_humidity +" (%) "+ maximum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ maximum_relative_humidity_time.strftime('%H:%M UTC')+")\n\nMinimum RH: " + minimum_relative_humidity +" (%) "+ minimum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ minimum_relative_humidity_time.strftime('%H:%M UTC')+")\n\nMaximum Wind Speed: " + maximum_wind_speed +" (MPH) "+ maximum_wind_speed_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_speed_time.strftime('%H:%M UTC')+")\n\nMaximum Wind Gust: " + maximum_wind_gust +" (MPH) "+ maximum_wind_gust_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_gust_time.strftime('%H:%M UTC')+")\n\nMaximum Elevation: " + str(round(max_elevation, 1)) + " Degrees Above the Horizon\n\nMinimum Elevation: " + str(round(min_elevation, 1)) + " Degrees Below the Horizon\n\nMaximum Solar Radiation: " + str(round(max_radiation, 1)) + " (W/m^2)", color='black', fontsize=11, fontweight='bold', bbox=props, zorder=10)

        if maximum_wind_gust == 'NA':

            fig.text(0.487, 0.13, "Maximum Temperature: " +maximum_temperature +" (\N{DEGREE SIGN}F) " + maximum_temperature_time_local.strftime('%H:%M Local') + " ("+ maximum_temperature_time.strftime('%H:%M UTC')+")\n\nMinimum Temperature: " + minimum_temperature +" (\N{DEGREE SIGN}F) "+ minimum_temperature_time_local.strftime('%H:%M Local') + " ("+ minimum_temperature_time.strftime('%H:%M UTC')+")\n\nMaximum RH: " + maximum_relative_humidity +" (%) "+ maximum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ maximum_relative_humidity_time.strftime('%H:%M UTC')+")\n\nMinimum RH: " + minimum_relative_humidity +" (%) "+ minimum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ minimum_relative_humidity_time.strftime('%H:%M UTC')+")\n\nMaximum Wind Speed: " + maximum_wind_speed +" (MPH) "+ maximum_wind_speed_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_speed_time.strftime('%H:%M UTC')+")\n\nMaximum Elevation: " + str(round(max_elevation, 1)) + " Degrees Above the Horizon\n\nMinimum Elevation: " + str(round(min_elevation, 1)) + " Degrees Below the Horizon\n\nMaximum Solar Radiation: " + str(round(max_radiation, 1)) + " (W/m^2)", color='black', fontsize=11, fontweight='bold', bbox=props, zorder=10)
    
    fig.text(0.27, 0.07, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=14, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)    

    file_functions.save_daily_weather_summary(fig, station_id)

    
