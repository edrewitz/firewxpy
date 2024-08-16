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
import matplotlib.dates as md
import standard

from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from metpy.plots import colortables
from dateutil import tz
from pysolar import solar, radiation

def graphical_daily_summary(station_id, file_save_path=None):

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
    ax0.set_title("Temperature", color='white', fontsize=10, fontweight='bold')
    ax0.tick_params(axis='x', colors='white')
    ax0.tick_params(axis='y', colors='white')
    
    ax1 = fig.add_subplot(gs[1:2, 0:1])
    ax1.plot(time, relative_humidity, c='green')
    ax1.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax1.set_ylim(minimum_relative_humidity - 5, maximum_relative_humidity + 5)
    ax1.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax1.set_ylabel("Relative Humidity (%)", color='white', fontsize=8, fontweight='bold')
    ax1.set_title("Relative Humidity", color='white', fontsize=10, fontweight='bold')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    
    ax2 = fig.add_subplot(gs[2:3, 0:1])
    ax2.plot(time, wind_speed, c='purple')
    ax2.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax2.set_ylim(0, maximum_wind_speed + 2)
    ax2.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax2.set_ylabel("Wind Speed (MPH)", color='white', fontsize=8, fontweight='bold')
    ax2.set_title("Wind Speed", color='white', fontsize=10, fontweight='bold')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    
    ax3 = fig.add_subplot(gs[0:1, 1:2])
    ax3.plot(times_list, solar_elevation, c='orange')
    ax3.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax3.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax3.set_ylabel("Solar Elevation Angle (Degrees)", color='white', fontsize=8, fontweight='bold')
    ax3.set_title("Solar Elevation Angle", color='white', fontsize=10, fontweight='bold')
    ax3.axhline(0, c='black', linestyle='--', linewidth=2)
    fig.text(0.55, 0.855, "Elevation Angle > 0 = Day\nElevation Angle < 0 = Night", fontsize=9, fontweight='bold')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    
    ax4 = fig.add_subplot(gs[1:2, 1:2])
    ax4.plot(times_list, solar_radiation, c='orange')
    ax4.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax4.set_xlabel("Hour", color='white', fontsize=8, fontweight='bold')
    ax4.set_ylabel("Solar Radiation (W/m^2)", color='white', fontsize=8, fontweight='bold')
    ax4.set_title("Solar Radiation", color='white', fontsize=10, fontweight='bold')
    ax4.tick_params(axis='x', colors='white')
    ax4.tick_params(axis='y', colors='white')
    
    fig.text(0.6, 0.30, "Daily Weather Summary", color='white', fontsize=16, fontweight='bold')
    
    try:
        maximum_temperature = int(round(maximum_temperature, 0))
        fig.text(0.483, 0.28, "Maximum Temperature: " + str(maximum_temperature) +" (\N{DEGREE SIGN}F) " + maximum_temperature_time_local.strftime('%H:%M Local') + " ("+ maximum_temperature_time.strftime('%H:%M UTC')+")", color='white', fontsize=14, fontweight='bold')
        
    except Exception as a:
        fig.text(0.483, 0.28, "Maximum Temperature: Not Available", color='white', fontsize=14, fontweight='bold')
    
    try:
        minimum_temperature = int(round(minimum_temperature, 0))
        fig.text(0.483, 0.26, "Minimum Temperature: " + str(minimum_temperature) +" (\N{DEGREE SIGN}F) "+ minimum_temperature_time_local.strftime('%H:%M Local') + " ("+ minimum_temperature_time.strftime('%H:%M UTC')+")", color='white', fontsize=14, fontweight='bold')
    except Exception as b:
        fig.text(0.483, 0.26, "Minimum Temperature: Not Available", color='white', fontsize=14, fontweight='bold')
    
    try:
        maximum_relative_humidity = int(round(maximum_relative_humidity, 0))
        fig.text(0.483, 0.24, "Maximum RH: " + str(maximum_relative_humidity) +" (%) "+ maximum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ maximum_relative_humidity_time.strftime('%H:%M UTC')+")", color='white', fontsize=14, fontweight='bold')
    except Exception as c:
        fig.text(0.483, 0.24, "Maximum RH: Not Available", color='white', fontsize=14, fontweight='bold')
    
    try:
        minimum_relative_humidity = int(round(minimum_relative_humidity, 0))
        fig.text(0.483, 0.22, "Minimum RH: " + str(minimum_relative_humidity) +" (%) "+ minimum_relative_humidity_time_local.strftime('%H:%M Local') + " ("+ minimum_relative_humidity_time.strftime('%H:%M UTC')+")", color='white', fontsize=14, fontweight='bold')
    except Exception as d:
        fig.text(0.483, 0.22, "Minimum RH: Not Available", color='white', fontsize=14, fontweight='bold')
    
    try:
        maximum_wind_speed = int(round(maximum_wind_speed, 0))
        fig.text(0.483, 0.20, "Maximum Wind Speed: " + str(maximum_wind_speed) +" (MPH) "+ maximum_wind_speed_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_speed_time.strftime('%H:%M UTC')+")", color='white', fontsize=14, fontweight='bold')
    except Exception as e:
        fig.text(0.483, 0.20, "Maximum Wind Speed: Not Available", color='white', fontsize=14, fontweight='bold')
    
    try:
        maximum_wind_gust = int(round(maximum_wind_gust, 0))
        fig.text(0.483, 0.18, "Maximum Wind Gust: " + str(maximum_wind_gust) +" (MPH) "+ maximum_wind_gust_time_local.strftime('%H:%M Local') + " ("+ maximum_wind_gust_time.strftime('%H:%M UTC')+")", color='white', fontsize=14, fontweight='bold')
    except Exception as f:
        fig.text(0.483, 0.18, "Maximum Wind Gust: Not Available (No Gusts Reported)", color='white', fontsize=14, fontweight='bold')
    
    fig.text(0.625, 0.15, "Solar Information", color='white', fontsize=16, fontweight='bold')
    if max_elevation >= 0:
        fig.text(0.483, 0.13, "Maximum Elevation: " + str(round(max_elevation, 1)) + " Degrees Above the Horizon", color='white', fontsize=14, fontweight='bold')
    if max_elevation < 0:
        fig.text(0.483, 0.13, "Maximum Elevation: " + str(round(max_elevation, 1)) + " Degrees Below the Horizon", color='white', fontsize=14, fontweight='bold')
    fig.text(0.483, 0.11, "Maximum Solar Radiation: " + str(round(max_radiation, 1)) + " (W/m^2)", color='white', fontsize=14, fontweight='bold')
    
    local_time, utc_time = standard.plot_creation_time()

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)

    fig.text(0.025, 0.02, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: thredds.ucar.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=18, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)    

    if file_save_path == None:
        return fig
    if file_save_path != None:
        parsers.save.save_image(file_save_path)

    
