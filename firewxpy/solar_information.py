import firewxpy.standard as standard
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import numpy as np
import warnings
import os
warnings.filterwarnings('ignore')

from dateutil import tz
from pysolar import solar, radiation
from datetime import datetime, timedelta

def get_solar_noon(times_list, solar_elevation):

    times_list, solar_elevation = times_list, solar_elevation
    max_elevation = np.nanmax(solar_elevation)
    for i, j in zip(times_list, solar_elevation):
        if j == max_elevation:
            return i

def get_solar_midnight(times_list, solar_elevation):

    times_list, solar_elevation = times_list, solar_elevation
    min_elevation = np.nanmin(solar_elevation)
    for i, j in zip(times_list, solar_elevation):
        if j == min_elevation:
            return i 

def plot_daily_solar_information(latitude, longitude):
    
    r'''
    This function plots a daily solar graph and gives other types of solar information. 

    Required Arguments: 1) latitude (Float) - The latitude coordinate in decimal degrees format. 
                     2) longitude (Float) - The longitude coordinate in decimal degrees format. 

    Optional Arguments: None

    Return: A graphic showing the following information saved to f:Weather Data/Solar Information:

    1) Daily solar elevation graphic
    2) A data table showing the following information:
        i) Maximum Daily Solar Elevation (solar-noon sun angle)
        ii) Minimum Daily Solar Elevation (solar-midnight sun angle)
        iii) Difference in daily solar elevation between current day, equinox, summer solstice and winter solstice
        iv) Total Daily Solar Radiation [W/m^2]


    '''


    latitude, longitude = latitude, longitude
    local, utc = standard.plot_creation_time()
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    
    start = utc
    year = start.year
    month = start.month
    day = start.day
    
    start = datetime(year, month, day, tzinfo=to_zone)
    if latitude >= 0:
        start_summer_solstice = datetime(year, 6, 21, tzinfo=to_zone)
        start_winter_solstice = datetime(year, 12, 21, tzinfo=to_zone)
    if latitude < 0:
        start_winter_solstice = datetime(year, 6, 21, tzinfo=to_zone)
        start_summer_solstice = datetime(year, 12, 21, tzinfo=to_zone)    
        
    start_equinox = datetime(year, 3, 21, tzinfo=to_zone)
    times_list = [start + timedelta(minutes=i *15) for i in range(24*4)]
    times_list_summer_solstice = [start_summer_solstice + timedelta(minutes=i *15) for i in range(24*4)]
    times_list_winter_solstice = [start_winter_solstice + timedelta(minutes=i *15) for i in range(24*4)]
    times_list_equinox = [start_equinox + timedelta(minutes=i *15) for i in range(24*4)]
    
    solar_elevation = [solar.get_altitude(latitude, longitude, t) for t in times_list]
    solar_radiation = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list, solar_elevation)]
    solar_azimuth = [solar.get_azimuth(latitude, longitude, t) for t in times_list]
    
    solar_elevation_summer = [solar.get_altitude(latitude, longitude, t) for t in times_list_summer_solstice]
    solar_radiation_summer = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_summer_solstice, solar_elevation_summer)]
    solar_azimuth_summer = [solar.get_azimuth(latitude, longitude, t) for t in times_list_summer_solstice]
    
    solar_elevation_winter = [solar.get_altitude(latitude, longitude, t) for t in times_list_winter_solstice]
    solar_radiation_winter = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_winter_solstice, solar_elevation_winter)]
    solar_azimuth_winter = [solar.get_azimuth(latitude, longitude, t) for t in times_list_winter_solstice]
    
    solar_elevation_equinox = [solar.get_altitude(latitude, longitude, t) for t in times_list_equinox]
    solar_radiation_equinox = [radiation.get_radiation_direct(t, ele) for t, ele in zip(times_list_equinox, solar_elevation_equinox)]
    solar_azimuth_equinox = [solar.get_azimuth(latitude, longitude, t) for t in times_list_equinox]
    
    
    max_elevation = np.nanmax(solar_elevation)
    min_elevation = np.nanmin(solar_elevation)
    
    max_elevation_summer = np.nanmax(solar_elevation_summer)
    min_elevation_summer = np.nanmin(solar_elevation_summer)
    
    max_elevation_winter = np.nanmax(solar_elevation_winter)
    min_elevation_winter = np.nanmin(solar_elevation_winter)
    
    max_elevation_equinox = np.nanmax(solar_elevation_equinox)
    min_elevation_equinox = np.nanmin(solar_elevation_equinox)
    
    sum_rad = np.nansum(solar_radiation)
    
    diff_ele_ss = max_elevation - max_elevation_summer
    diff_ele_ws = max_elevation - max_elevation_winter
    diff_ele_e = max_elevation - max_elevation_equinox
    
    solar_noon = get_solar_noon(times_list, solar_elevation)
    solar_midnight = get_solar_midnight(times_list, solar_elevation)
    
    plt.style.use('fivethirtyeight')
    props = dict(boxstyle='round', facecolor='wheat', alpha=1)
    props_table = dict(boxstyle='round', facecolor='darkslateblue', alpha=1)

    print("Creating Image - Please Wait...")
    
    fig = plt.figure(figsize=(15,9))
    fig.set_facecolor('silver')
    gs = gridspec.GridSpec(2, 4)
    
    fig.suptitle("Daily Solar Information | Date: " + local.strftime('%m/%d/%Y'), color='black', fontsize=28, fontweight='bold')
    
    if latitude >= 0 and longitude <= 0:
        fig.text(0.315, 0.9, "Latitude: " + str(abs(latitude)) + " (\N{DEGREE SIGN}N) | Longitude: " + str(abs(longitude)) + " (\N{DEGREE SIGN}W)", color='black', fontsize=16, fontweight='bold')
    if latitude >= 0 and longitude > 0:
        fig.text(0.315, 0.9, "Latitude: " + str(abs(latitude)) + " (\N{DEGREE SIGN}N) | Longitude: " + str(abs(longitude)) + " (\N{DEGREE SIGN}E)", color='black', fontsize=16, fontweight='bold')
    if latitude < 0 and longitude <= 0:
        fig.text(0.315, 0.9, "Latitude: " + str(abs(latitude)) + " (\N{DEGREE SIGN}S) | Longitude: " + str(abs(longitude)) + " (\N{DEGREE SIGN}W)", color='black', fontsize=16, fontweight='bold')
    if latitude < 0 and longitude > 0:
        fig.text(0.315, 0.9, "Latitude: " + str(abs(latitude)) + " (\N{DEGREE SIGN}S) | Longitude: " + str(abs(longitude)) + " (\N{DEGREE SIGN}E)", color='black', fontsize=16, fontweight='bold')
    
    ax1 = fig.add_subplot(gs[0:2, 0:4])
    ax1.plot(times_list, solar_elevation, c='orange', label=start.strftime('%b %d'), alpha=1)
    ax1.plot(times_list, solar_elevation_summer, c='red', label='Summer Solstice', alpha=1)
    ax1.plot(times_list, solar_elevation_winter, c='blue', label='Winter Solstice', alpha=1)
    ax1.plot(times_list, solar_elevation_equinox, c='magenta', label='Equinox', alpha=1)
    ax1.axhspan(90, 0, color='gold', alpha=0.25)
    ax1.axhspan(0, -6, color='dodgerblue', alpha=0.25)
    ax1.axhspan(-6, -12, color='blue', alpha=0.25)
    ax1.axhspan(-12, -18, color='midnightblue', alpha=0.25)
    ax1.axhspan(-18, -90, color='black', alpha=0.25)
    ax1.xaxis.set_major_formatter(md.DateFormatter('%H', tz=to_zone))
    ax1.set_xlabel("Hour", color='black', fontsize=12, fontweight='bold')
    ax1.set_ylabel("Solar Elevation Angle (Degrees)", color='black', fontsize=12, fontweight='bold')
    ax1.axhline(0, c='black', linestyle='--', linewidth=2)
    ax1.tick_params(axis='x', colors='black')
    ax1.tick_params(axis='y', colors='black')
    ax1.legend(loc=(0.88,0.9), prop={'size': 8})
    ax1.set_ylim(-90, 90)
    ax1.text(0.01, 0.95, 'DAYTIME (0-90 \N{DEGREE SIGN}ABOVE)', fontsize=7, fontweight='bold', transform=ax1.transAxes, bbox=props)
    ax1.text(0.01, 0.4775, 'CIVIL TWILIGHT (0-6 \N{DEGREE SIGN}BELOW)', fontsize=7, fontweight='bold', transform=ax1.transAxes, bbox=props)
    ax1.text(0.01, 0.445, 'NAUTICAL TWILIGHT (6-12 \N{DEGREE SIGN}BELOW)', fontsize=7, fontweight='bold', transform=ax1.transAxes, bbox=props)
    ax1.text(0.01, 0.41, 'ASTRONOMICAL TWILIGHT (12-18 \N{DEGREE SIGN}BELOW)', fontsize=7, fontweight='bold', transform=ax1.transAxes, bbox=props)
    ax1.text(0.01, 0.3, 'NIGHTIME (18-90 \N{DEGREE SIGN}BELOW)', fontsize=7, fontweight='bold', transform=ax1.transAxes, bbox=props)
    
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
    
    ax1.text(0.3, 0.01, "Maximum Elevation: "+sym1+""+ str(round(max_elevation, 1)) + " [\N{DEGREE SIGN} From Horizon] @ "+solar_noon.strftime('%H:%M Local')+"\n\nMinimum Elevation: "+sym2+""+ str(round(min_elevation, 1)) + " [\N{DEGREE SIGN} From Horizon] @ "+solar_midnight.strftime('%H:%M Local')+"\n\nMaximum Elevation Difference:\nSummer Solstice: "+str(round(diff_ele_ss,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym1+""+str(round(max_elevation_summer,1))+" [\N{DEGREE SIGN} From Horizon]\nEquinox: "+sym+""+str(round(diff_ele_e,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym3+""+str(round(max_elevation_equinox,1))+" [\N{DEGREE SIGN} From Horizon]\nWinter Solstice: "+str(round(diff_ele_ws,1))+" [\N{DEGREE SIGN}] | Max Elevation: "+sym4+""+str(round(max_elevation_winter,1))+" [\N{DEGREE SIGN} From Horizon]\n\nTotal Daily Solar Radiation: " + str(round(sum_rad, 1)) + " (W/m^2)", fontsize=10, fontweight='bold', color='white', transform=ax1.transAxes, bbox=props_table)


    fig.text(0.08, 0.04, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nImage Created: " + local.strftime('%m/%d/%Y %H:%M Local') + " (" + utc.strftime('%H:%M UTC') + ")", fontsize=10, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)    
    
    if latitude >= 0:
        lat_char = 'N'
    if latitude < 0:
        lat_char = 'S'
    if longitude >= 0:
        lon_char = 'E'
    if longitude < 0:
        lon_char = 'W'
    
    lat_name = str(abs(latitude))
    lon_name = str(abs(longitude))
    
    fname = f"{lat_name}{lat_char}_{lon_name}{lon_char}_SolarInfo.png"

    path = f"Weather Data/Solar Information/{fname}"

    if os.path.exists(f"Weather Data"):
        print("Already Satisfied: f:Weather Data exists.")
        
        if os.path.exists(f"Weather Data/Solar Information"):
            print("Already Satisfied: f:Weather Data/Solar Information exists.")
            fig.savefig(path)
            print(f"Image saved to: {path}")
            

        else:
            print("f:Weather Data does not exist. Building the new branch...")
            os.mkdir(f"Weather Data/Solar Information")
            print("Successfully built new branch")
            fig.savefig(path)
            print(f"Image saved to: {path}")            

    else:
        print("f:Weather Data does not exist. Building the new directory...")
        os.mkdir(f"Weather Data")
        os.mkdir(f"Weather Data/Solar Information")
        print("Successfully built directory.")
        fig.savefig(path)
        print(f"Image saved to: {path}")        
        
