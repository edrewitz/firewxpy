# Imports needed packages
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.transforms as transforms
import pandas as pd
import metpy.calc as mpcalc
import math
import numpy as np
import metpy.calc as mpcalc
import firewxpy.standard as standard
import time

from firewxpy.calc import Thermodynamics
from matplotlib import transforms as transform
from siphon.simplewebservice.wyoming import WyomingUpperAir
from metpy.units import units, pandas_dataframe_to_unit_arrays
from metpy.plots import SkewT
from metpy.units import units
from datetime import datetime
from firewxpy.utilities import file_functions 

mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7

def plot_observed_sounding(station_id):

    local_time, utc_time = standard.plot_creation_time()

    station_id = station_id
    station_id = station_id.upper()

    year = utc_time.year
    month = utc_time.month
    day = utc_time.day
    
    if utc_time.hour >= 1 and utc_time.hour < 13:
        hour = 0
    else:
        hour = 12

    date = datetime(year, month, day, hour)

    # pings the server to request data
    try:
        df = WyomingUpperAir.request_data(date, station_id)
        print(station_id+" data retrieved successfully!")
        sounding = True
    except Exception as a:
        print("Trying again! - Just in case.")
        try:
            time.sleep(10)
            df = WyomingUpperAir.request_data(date, station_id)
            print(station_id+" data retrieved successfully!")
            sounding = True
        except Exception as b:
            try:
                print("Trying one last time! - This server can be glitchy.")
                time.sleep(10)
                df = WyomingUpperAir.request_data(date, station_id)
                print(station_id+" data retrieved successfully!")
                sounding = True                
            except Exception as c:
                print("ERROR! User entered an invalid date or station ID")
                sounding = False

    if sounding == True:

        df.drop_duplicates(inplace=True,subset='pressure',ignore_index=True)
        df.dropna(axis=0, inplace=True)
        df = pandas_dataframe_to_unit_arrays(df)
    
        temps = df['temperature'].m
        hgt = df['height'].m
        pressure = df['pressure']
        temperature = df['temperature']
        dewpoint = df['dewpoint']
        ws = df['speed']
        u = df['u_wind']
        v = df['v_wind']
        direction = df['direction']
        pwats = df['pw']
        station_elevation = df['elevation']
        lat = df['latitude'][0].m
        lon = df['longitude'][0].m
        height = df['height']
        elevation = df['elevation']
        elevation = elevation.m * 3.28084
        rh = (mpcalc.relative_humidity_from_dewpoint(temperature, dewpoint) * 100)
        ft = height.m *3.28084
        ft = ft - elevation
        hgts = hgt
        hgt = hgt - elevation

        if len(temps) > len(hgts):
            df_len = len(hgts)
        elif len(temps) < len(hgts):
            df_len = len(temps)
        else:
            df_len = len(temps)
        mheight = Thermodynamics.find_mixing_height(temps, hgts, df_len)
        mheight = mheight - elevation
        mheight = int(round(mheight[0], 0))
        theta = mpcalc.potential_temperature(pressure, temperature)
        
        # Calculates the Brunt–Väisälä Frequency Squared
        bv_squared = mpcalc.brunt_vaisala_frequency_squared(height, theta)
        title_lat = str(abs(round(lat, 1)))
        title_lon = str(abs(round(lon, 1)))
        if lat < 0:
            lat_symbol = ' [\N{DEGREE SIGN}S]'
        if lat >= 0:
            lat_symbol = ' [\N{DEGREE SIGN}N]'
        if lon <= 0:
            lon_symbol = ' [\N{DEGREE SIGN}W]'
        if lon > 0:
            lon_symbol = ' [\N{DEGREE SIGN}E]'
        
        interval = np.logspace(2, 3) * units.hPa
        barb_mask = (pressure >= 250 * units.hPa)
        pres = pressure[barb_mask]
        idx = mpcalc.resample_nn_1d(pres, interval)
        fig = plt.figure(figsize=(12, 10))
        gs = gridspec.GridSpec(10, 13)
        skew = SkewT(fig, rotation=45, subplot=gs[0:10, 0:13])
        skew.ax.set_title(station_id+" Vertical Profiles\nLatitude: "+title_lat+""+lat_symbol+" | Longitude: "+title_lon+""+lon_symbol, fontsize=12, fontweight='bold', loc='left')
        skew.ax.set_title("Valid: " + date.strftime('%m/%d/%Y %H:00 UTC'), fontsize=12, fontweight='bold', loc='right')
        
        
        fig.patch.set_facecolor('aliceblue')
        
        
        skew.ax.set_ylim(1030, 250)
        skew.plot_dry_adiabats(alpha=0.5)
        skew.plot_mixing_lines(alpha=0.5)
        skew.plot_moist_adiabats(alpha=0.5)
        skew.ax.set_xlabel("Temperature [℃]", fontsize=12, fontweight='bold')
        skew.ax.set_ylabel("Pressure [hPa]", fontsize=12, fontweight='bold')
        mask = (pressure >= 100 * units.hPa)
        
        wetbulb = mpcalc.wet_bulb_temperature(pressure[0], temperature, dewpoint).to('degC')
        
        skew.plot(pressure[mask], temperature[mask], 'red', linewidth=3, alpha=0.5)
        skew.plot(pressure[mask], dewpoint[mask], 'green', linewidth=3, alpha=0.5)
        skew.plot_barbs(pressure[idx], u[idx], v[idx], color='blue', length=6)
        skew.plot(pressure, wetbulb, 'cyan', alpha=0.3, linewidth=2)
        
        lcl_pressure, lcl_temperature = mpcalc.lcl(pressure[0], temperature[0], dewpoint[0])
        lfc_pressure, lfc_temperature = mpcalc.lfc(pressure, temperature, dewpoint)
        el_pressure, el_temperature = mpcalc.el(pressure, temperature, dewpoint)
        
        profile = mpcalc.parcel_profile(pressure, temperature[0], dewpoint[0]).to('degC')
        skew.plot(pressure, profile, 'k', linestyle='--', linewidth=2, alpha=0.5)
        
        # Shade areas of CAPE and CIN
        skew.shade_cin(pressure, temperature, profile, dewpoint)
        skew.shade_cape(pressure, temperature, profile)
        
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='bisque', alpha=1)
        indices = dict(boxstyle='round', facecolor='white', alpha=1)
        
        # Data table LCL
        LCL_Pres = str(round(lcl_pressure.m, 1))
        LCL_Temp = str(round(lcl_temperature.m, 1))
        
        # Data table LFC
        LFC_Pres = str(round(lfc_pressure.m, 1))
        LFC_Temp = str(round(lfc_temperature.m, 1))
        
        # Data table EL
        EL_Pres = str(round(el_pressure.m, 1))
        EL_Temp = str(round(el_temperature.m, 1))
        
        # Checks if there is an LFC or not
        LFC_NAN = np.isnan(lfc_pressure)
        EL_NAN = np.isnan(el_pressure)
        # Table if no LFC
        
        
        if LFC_NAN == True and EL_NAN == False:
            skew.ax.text(0.02, 0.65,'               EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\n               LCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                         fontsize=10, fontweight='bold', verticalalignment='top', bbox=props)
        
        # Table if LFC   
        if LFC_NAN == False and EL_NAN == False:
            skew.ax.text(0.02, 0.65,'               EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\n               LFC\nPressure: '+LFC_Pres+' [hPa]\nTemperature: '+LFC_Temp+' [℃]\n\n               LCL\nPressure: ' + LCL_Pres + '[hPa]\nTemperature: ' + LCL_Temp + '[℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                         fontsize=10, fontweight='bold', verticalalignment='top', bbox=props)
        
        if LFC_NAN == True and EL_NAN == True:
            skew.ax.text(0.02, 0.65,'               LCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                         fontsize=10, fontweight='bold', verticalalignment='top', bbox=props)    
           
        # x-limits of the skewT        
        skew.ax.set_xlim(-25, 30)
        
        # Plots LCL LFC and EL
        if lcl_pressure:
            skew.ax.plot(lcl_temperature, lcl_pressure, marker="_", label='LCL', color='tab:purple', markersize=30, markeredgewidth=3)
        if lfc_pressure:
            skew.ax.plot(lfc_temperature, lfc_pressure, marker="_", label='LFC', color='tab:purple', markersize=30, markeredgewidth=3)
        if el_pressure:
            skew.ax.plot(el_temperature, el_pressure, marker="_", label='EL', color='tab:purple', markersize=30, markeredgewidth=3)
        
        # Colors of the freezing level isotherm (cyan) and the boundaries of the dendridic growth zone (yellow)
        skew.ax.axvline(0, color='c', linestyle='--', linewidth=3)
        
        ax1 = fig.add_subplot(gs[0:3, 8:12])
        
        ax1.tick_params(axis="y",direction="in", pad=-27)
        
        hgt_mask = (ft <= 5500)
        
        ax1.plot(rh[hgt_mask], ft[hgt_mask], color='green', alpha=0.3)
        ax1.axhline(y=1000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=2000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=3000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=4000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=5000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.set_xlabel("Relative Humidity [%]", fontweight='bold')
        ax1.set_ylabel("Height [ft AGL]", fontweight='bold')
        
        ax2 = fig.add_subplot(gs[0:3, 1:3])
        ax2.tick_params(axis="y",direction="in", pad=-25)

        x_clip_radius=0.1
        y_clip_radius=0.08
        u = u.m * 1.15078
        v = v.m * 1.15078
        ax2.set_ylim(ft[0], 5500)
        umin = np.nanmin(u[hgt_mask])
        umax = np.nanmax(u[hgt_mask])
        vmin = np.nanmin(v[hgt_mask])
        vmax = np.nanmax(v[hgt_mask])
        if umin < vmin:
            xmin = umin - 10
        else:
            xmin = vmin - 10

        if umax > vmax:
            xmax = umax + 10
        else:
            xmax = vmax + 10
        ax2.set_xlim(xmin, xmax)
        mean = ((xmin + xmax)/2)
        xloc = int(round(mean, 0))
        x = np.empty_like(ft)
        x.fill(xloc)
        
        ax2.barbs(x[idx], ft[idx], u[idx], v[idx], clip_on=True, zorder=10, color='darkred', length=5)
        ax2.plot(u, ft, label='u-wind', color='darkorange', alpha=0.5)
        ax2.plot(v, ft, label='v-wind', color='indigo', alpha=0.5)
        ax2.legend(loc=(0.58, 0.9), prop={'size': 5})
        bbox_props = dict(boxstyle='round', facecolor='bisque', alpha=1)
        ax2.text(1.01, 0.815, 'u-max: '+str(int(round(umax, 0)))+' [MPH]\nu-min: ' +str(int(round(umin, 0)))+' [MPH]\nv-max: ' +str(int(round(vmax, 0)))+' [MPH]\nv-min: ' +str(int(round(vmin, 0)))+' [MPH]', fontsize=6, fontweight='bold', bbox=bbox_props, transform=ax2.transAxes)
        
        ax2.set_xlabel("Wind Velocity [MPH]", fontsize=9, fontweight='bold')
        ax2.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        
        ax3 = fig.add_subplot(gs[0:3, 4:7])
        ax3.tick_params(axis="y",direction="in", pad=-32)
        ax3.axvline(x=0, color='red', alpha=0.5, linestyle='--')
        ax3.set_ylim(ft[0], 15000)
        ax3.set_xlabel("BVF-Squared [1/s^2]", fontsize=9, fontweight='bold')
        ax3.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        
        # Plots the Brunt–Väisälä Frequency Squared
        ax3.plot(bv_squared, ft, color='blue')
        
        fig.text(0.15, 0.05, "Plot Created With FireWxPy(C) Eric J. Drewitz 2024\nData Source: weather.uwyo.edu\nImage Created: "+utc_time.strftime('%m/%d/%Y %H:00 UTC'), fontsize=8, bbox=props)

    if sounding == False:
        fig = standard.no_sounding_graphic(date)

    fname = station_id+" VERTICAL PROFILES"
    
    file_functions.save_daily_sounding_graphic(fig, station_id)  
        
