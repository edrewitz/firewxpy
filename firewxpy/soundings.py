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
from datetime import datetime, timedelta
from firewxpy.utilities import file_functions 

mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7

pd.options.mode.copy_on_write = True

def clean_height_data(height_data):

    height_data = height_data
    
    end = len(height_data) - 1

    for i in range(0, end):
        if height_data.iloc[i+1] < height_data.iloc[i]:
            if height_data.iloc[i] >= 5000 and height_data.iloc[i] < 10000:
                height_data.iloc[i+1] = height_data.iloc[i+1] + 10000
            if height_data.iloc[i] >= 15000 and height_data.iloc[i] < 20000:
                height_data.iloc[i+1] = height_data.iloc[i+1] + 20000
            else:
                height_data.iloc[i+1] = height_data.iloc[i+1] + 30000
    return height_data


def plot_observed_sounding(station_id):

    local_time, utc_time = standard.plot_creation_time()

    station_id = station_id
    station_id = station_id.upper()

    dates = []
    sounding = True
    for i in range(0, 13):
        date = utc_time - timedelta(hours=i)
        dates.append(date)

    try:
        print("Searching for data at time: "+dates[0].strftime('%m/%d %H:00 UTC'))
        df = WyomingUpperAir.request_data(dates[0], station_id)
        print("Successfully retrieved data for: "+dates[0].strftime('%m/%d %H:00 UTC'))
        date = dates[0]
        data = True
    except Exception as e:
        time.sleep(10)
        print("Trying again!")
        try:
            df = WyomingUpperAir.request_data(dates[0], station_id)
            print("Successfully retrieved data for: "+dates[0].strftime('%m/%d %H:00 UTC'))
            date = dates[0]
            data = True
        except Exception as e:
            time.sleep(10)
            print("Trying one last time! This server can be glitchy...")
            try:
                df = WyomingUpperAir.request_data(dates[0], station_id)
                print("Successfully retrieved data for: "+dates[0].strftime('%m/%d %H:00 UTC'))
                date = dates[0]
                data = True
            except Exception as e:
                print("Searching for data at time: "+dates[1].strftime('%m/%d %H:00 UTC'))
                try:
                   df = WyomingUpperAir.request_data(dates[1], station_id)
                   print("Successfully retrieved data for: "+dates[1].strftime('%m/%d %H:00 UTC')) 
                   date = dates[1]
                   data = True
                except Exception as e:
                    time.sleep(10)
                    print("Trying again!")
                    try:
                        df = WyomingUpperAir.request_data(dates[1], station_id)
                        print("Successfully retrieved data for: "+dates[1].strftime('%m/%d %H:00 UTC'))
                        date = dates[1]
                        data = True
                    except Exception as e:
                        time.sleep(10)
                        print("Trying one last time! This server can be glitchy...")
                        try:
                            df = WyomingUpperAir.request_data(dates[1], station_id)
                            print("Successfully retrieved data for: "+dates[1].strftime('%m/%d %H:00 UTC'))
                            date = dates[1] 
                            data = True
                        except Exception as e:
                            print("Searching for data at time: "+dates[2].strftime('%m/%d %H:00 UTC'))
                            try:
                               df = WyomingUpperAir.request_data(dates[2], station_id)
                               print("Successfully retrieved data for: "+dates[2].strftime('%m/%d %H:00 UTC')) 
                               date = dates[2] 
                               data = True
                            except Exception as e:
                                time.sleep(10)
                                print("Trying again!")
                                try:
                                    df = WyomingUpperAir.request_data(dates[2], station_id)
                                    print("Successfully retrieved data for: "+dates[2].strftime('%m/%d %H:00 UTC'))
                                    date = dates[2]
                                    data = True
                                except Exception as e:
                                    time.sleep(10)
                                    print("Trying one last time! This server can be glitchy...")
                                    try:
                                        df = WyomingUpperAir.request_data(dates[2], station_id)
                                        print("Successfully retrieved data for: "+dates[2].strftime('%m/%d %H:00 UTC')) 
                                        date = dates[2]
                                        data = True
                                    except Exception as e:
                                        data = False

    if data == False:
        print("Searching for data at time: "+dates[3].strftime('%m/%d %H:00 UTC'))
        try:
           df = WyomingUpperAir.request_data(dates[3], station_id)
           print("Successfully retrieved data for: "+dates[3].strftime('%m/%d %H:00 UTC'))
           date = dates[3] 
           data = True
        except Exception as e:
            time.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[3], station_id)
                print("Successfully retrieved data for: "+dates[3].strftime('%m/%d %H:00 UTC'))
                date = dates[3]
                data = True
            except Exception as e:
                time.sleep(10)
                print("Trying one last time! This server can be glitchy...")
                try:
                    df = WyomingUpperAir.request_data(dates[3], station_id)
                    print("Successfully retrieved data for: "+dates[3].strftime('%m/%d %H:00 UTC')) 
                    date = dates[3]
                    data = True
                except Exception as e:
                    print("Searching for data at time: "+dates[4].strftime('%m/%d %H:00 UTC'))
                    try:
                       df = WyomingUpperAir.request_data(dates[4], station_id)
                       print("Successfully retrieved data for: "+dates[4].strftime('%m/%d %H:00 UTC'))
                       date = dates[4]
                       data = True 
                    except Exception as e:
                        time.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[4], station_id)
                            print("Successfully retrieved data for: "+dates[4].strftime('%m/%d %H:00 UTC'))
                            date = dates[4]
                            data = True
                        except Exception as e:
                            time.sleep(10)
                            print("Trying one last time! This server can be glitchy...")
                            try:
                                df = WyomingUpperAir.request_data(dates[4], station_id)
                                print("Successfully retrieved data for: "+dates[4].strftime('%m/%d %H:00 UTC')) 
                                date = dates[4]
                                data = True
                            except Exception as e:
                                data = False                    
                                
                                
    if data == False:                         
        print("Searching for data at time: "+dates[5].strftime('%m/%d %H:00 UTC'))
        try:
           df = WyomingUpperAir.request_data(dates[5], station_id)
           print("Successfully retrieved data for: "+dates[5].strftime('%m/%d %H:00 UTC'))
           date = dates[5]
           data = True
        except Exception as e:
            time.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[5], station_id)
                print("Successfully retrieved data for: "+dates[5].strftime('%m/%d %H:00 UTC'))
                date = dates[5]
                data = True
            except Exception as e:
                time.sleep(10)
                print("Trying one last time! This server can be glitchy...")
                try:
                    df = WyomingUpperAir.request_data(dates[5], station_id)
                    print("Successfully retrieved data for: "+dates[5].strftime('%m/%d %H:00 UTC')) 
                    date = dates[5]
                    data = True
                except Exception as e:
                    print("Searching for data at time: "+dates[6].strftime('%m/%d %H:00 UTC'))
                    try:
                       df = WyomingUpperAir.request_data(dates[6], station_id)
                       print("Successfully retrieved data for: "+dates[6].strftime('%m/%d %H:00 UTC'))
                       date = dates[6]
                       data = True 
                    except Exception as e:
                        time.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[6], station_id)
                            print("Successfully retrieved data for: "+dates[6].strftime('%m/%d %H:00 UTC'))
                            date = dates[6]
                            data = True
                        except Exception as e:
                            time.sleep(10)
                            print("Trying one last time! This server can be glitchy...")
                            try:
                                df = WyomingUpperAir.request_data(dates[6], station_id)
                                print("Successfully retrieved data for: "+dates[6].strftime('%m/%d %H:00 UTC')) 
                                date = dates[6]
                                data = True
                            except Exception as e:
                                print("Searching for data at time: "+dates[7].strftime('%m/%d %H:00 UTC'))
                                try:
                                   df = WyomingUpperAir.request_data(dates[7], station_id)
                                   print("Successfully retrieved data for: "+dates[7].strftime('%m/%d %H:00 UTC')) 
                                   date = dates[7]
                                   data = True 
                                except Exception as e:
                                    time.sleep(10)
                                    print("Trying again!")
                                    try:
                                        df = WyomingUpperAir.request_data(dates[7], station_id)
                                        print("Successfully retrieved data for: "+dates[7].strftime('%m/%d %H:00 UTC'))
                                        date = dates[7]
                                        data = True
                                    except Exception as e:
                                        time.sleep(10)
                                        print("Trying one last time! This server can be glitchy...")
                                        try:
                                            df = WyomingUpperAir.request_data(dates[7], station_id)
                                            print("Successfully retrieved data for: "+dates[7].strftime('%m/%d %H:00 UTC')) 
                                            date = dates[7]
                                            data = True
                                        except Exception as e:
                                            data = False                                            
                                            
                                            
                                            
    if data == False:                                            
        print("Searching for data at time: "+dates[8].strftime('%m/%d %H:00 UTC'))
        try:
           df = WyomingUpperAir.request_data(dates[8], station_id)
           print("Successfully retrieved data for: "+dates[8].strftime('%m/%d %H:00 UTC')) 
           date = dates[8]
           data = True 
        except Exception as e:
            time.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[8], station_id)
                print("Successfully retrieved data for: "+dates[8].strftime('%m/%d %H:00 UTC'))
                date = dates[8]
                data = True
            except Exception as e:
                time.sleep(10)
                print("Trying one last time! This server can be glitchy...")
                try:
                    df = WyomingUpperAir.request_data(dates[8], station_id)
                    print("Successfully retrieved data for: "+dates[8].strftime('%m/%d %H:00 UTC'))
                    date = dates[8]
                    data = True
                except Exception as e:
                    print("Searching for data at time: "+dates[9].strftime('%m/%d %H:00 UTC'))
                    try:
                       df = WyomingUpperAir.request_data(dates[9], station_id)
                       print("Successfully retrieved data for: "+dates[9].strftime('%m/%d %H:00 UTC'))
                       date = dates[9]
                       data = True 
                    except Exception as e:
                        time.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[9], station_id)
                            print("Successfully retrieved data for: "+dates[9].strftime('%m/%d %H:00 UTC'))
                            date = dates[9]
                            data = True
                        except Exception as e:
                            time.sleep(10)
                            print("Trying one last time! This server can be glitchy...")
                            try:
                                df = WyomingUpperAir.request_data(dates[9], station_id)
                                print("Successfully retrieved data for: "+dates[9].strftime('%m/%d %H:00 UTC'))   
                                date = dates[9]
                                data = True
                            except Exception as e:
                                print("Searching for data at time: "+dates[10].strftime('%m/%d %H:00 UTC'))
                                try:
                                   df = WyomingUpperAir.request_data(dates[10], station_id)
                                   print("Successfully retrieved data for: "+dates[10].strftime('%m/%d %H:00 UTC'))
                                   date = dates[10]
                                   data = True
                                except Exception as e:
                                    time.sleep(10)
                                    print("Trying again!")
                                    try:
                                        df = WyomingUpperAir.request_data(dates[10], station_id)
                                        print("Successfully retrieved data for: "+dates[10].strftime('%m/%d %H:00 UTC'))
                                        date = dates[10]
                                        data = True
                                    except Exception as e:
                                        time.sleep(10)
                                        print("Trying one last time! This server can be glitchy...")
                                        try:
                                            df = WyomingUpperAir.request_data(dates[10], station_id)
                                            print("Successfully retrieved data for: "+dates[10].strftime('%m/%d %H:00 UTC'))   
                                            date = dates[10]
                                            data = True
                                        except Exception as e:
                                            data = False                                                                                            
                                            
                                            
    if data == False:                                
        print("Searching for data at time: "+dates[11].strftime('%m/%d %H:00 UTC'))
        try:
           df = WyomingUpperAir.request_data(dates[11], station_id)
           print("Successfully retrieved data for: "+dates[11].strftime('%m/%d %H:00 UTC'))
           date = dates[11] 
        except Exception as e:
            time.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[11], station_id)
                print("Successfully retrieved data for: "+dates[11].strftime('%m/%d %H:00 UTC'))
                date = dates[11]
            except Exception as e:
                time.sleep(10)
                print("Trying one last time! This server can be glitchy...")
                try:
                    df = WyomingUpperAir.request_data(dates[11], station_id)
                    print("Successfully retrieved data for: "+dates[11].strftime('%m/%d %H:00 UTC'))
                    date = dates[11]
                except Exception as e:
                    print("Searching for data at time: "+dates[12].strftime('%m/%d %H:00 UTC'))
                    try:
                       df = WyomingUpperAir.request_data(dates[12], station_id)
                       print("Successfully retrieved data for: "+dates[12].strftime('%m/%d %H:00 UTC')) 
                       date = dates[12] 
                    except Exception as e:
                        time.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[12], station_id)
                            print("Successfully retrieved data for: "+dates[12].strftime('%m/%d %H:00 UTC'))
                            date = dates[12]
                        except Exception as e:
                            time.sleep(10)
                            print("Trying one last time! This server can be glitchy...")
                            try:
                                df = WyomingUpperAir.request_data(dates[12], station_id)
                                print("Successfully retrieved data for: "+dates[12].strftime('%m/%d %H:00 UTC'))  
                                date = dates[12]
                            except Exception as e:
                                print("No Sounding Data has been recorded within the past 12 hours.")
                                sounding = False



    try:
        date_24 = date - timedelta(hours=24)
        print("Searching for data at time: "+date_24.strftime('%m/%d %H:00 UTC'))
        df_24 = WyomingUpperAir.request_data(date_24, station_id)
        print("Successfully retrieved data for: "+date_24.strftime('%m/%d %H:00 UTC'))
    except Exception as e:
        time.sleep(10)
        try:
            print("Trying Again!")
            df_24 = WyomingUpperAir.request_data(date_24, station_id)
            print("Successfully retrieved data for: "+date_24.strftime('%m/%d %H:00 UTC'))
        except Exception as e:
            time.sleep(10)
            try:
                print("Trying one last time! This server can be glitchy...")
                df_24 = WyomingUpperAir.request_data(date_24, station_id)
                print("Successfully retrieved data for: "+date_24.strftime('%m/%d %H:00 UTC'))
            except Exception as e:
                pass
    
    if sounding == True:

        df.drop_duplicates(inplace=True,subset='pressure',ignore_index=True)
        df.dropna(axis=0, inplace=True)
        df['height'] = clean_height_data(df['height'])
        mheight = Thermodynamics.find_mixing_height(df['temperature'], df['height'])
        elev = df['elevation'] * 3.28084
        mheight = mheight - elev
        mheight = mheight.iloc[0]
        mheight = int(round(mheight, 0))
        d = pandas_dataframe_to_unit_arrays(df)
    
        temps = d['temperature'].m
        hgt = d['height'].m
        pressure = d['pressure']
        temperature = d['temperature']
        dewpoint = d['dewpoint']
        ws = d['speed']
        u = d['u_wind']
        v = d['v_wind']
        direction = d['direction']
        pwats = d['pw']
        station_elevation = d['elevation']
        lat = d['latitude'][0].m
        lon = d['longitude'][0].m
        height = d['height']
        elevation = d['elevation']
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

        theta = mpcalc.potential_temperature(pressure, temperature)

        try:
            df_24.drop_duplicates(inplace=True,subset='pressure',ignore_index=True)
            df_24.dropna(axis=0, inplace=True)
            df_24['height'] = clean_height_data(df_24['height'])
            mheight_24 = Thermodynamics.find_mixing_height(df_24['temperature'], df_24['height'])
            elev_24 = df_24['elevation'] * 3.28084
            mheight_24 = mheight_24 - elev_24
            mheight_24 = mheight_24.iloc[0]
            mheight_24 = int(round(mheight_24, 0))
            d_24 = pandas_dataframe_to_unit_arrays(df_24)
    
            temperature_24 = d_24['temperature']
            temps_24 = d_24['temperature'].m
            dewpoint_24 = d_24['dewpoint']
            hgt_24 = d_24['height'].m
            rh_24 = (mpcalc.relative_humidity_from_dewpoint(temperature_24, dewpoint_24) * 100)
            pressure_24 = d_24['pressure']
            u_24 = d_24['u_wind']
            v_24 = d_24['v_wind']
            u_24 = u_24.m * 1.15078
            v_24 = v_24.m * 1.15078
            height_24 = d_24['height']
            elevation_24 = d_24['elevation']
            elevation_24 = elevation_24.m * 3.28084
    
            ft_24 = height_24.m *3.28084
            ft_24 = ft_24 - elevation_24
            hgts_24 = hgt_24
            hgt_24 = hgt_24 - elevation_24
            
            if len(temps_24) > len(hgts_24):
                df_len_24 = len(hgts_24)
            elif len(temps_24) < len(hgts_24):
                df_len_24 = len(temps_24)
            else:
                df_len_24 = len(temps_24)
    
            theta_24 = mpcalc.potential_temperature(pressure_24, temperature_24)
            mheight_diff = mheight - mheight_24
            bv_squared_24 = mpcalc.brunt_vaisala_frequency_squared(height_24, theta_24) 

        except Exception as e:
            pass
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
        barb_mask = (pressure >= 100 * units.hPa)
        pres = pressure[barb_mask]
        idx = mpcalc.resample_nn_1d(pres, interval)
        interval_24 = np.logspace(2, 3) * units.hPa
        barb_mask_24 = (pressure_24 >= 100 * units.hPa)
        pres_24 = pressure_24[barb_mask_24]
        idx_24 = mpcalc.resample_nn_1d(pres_24, interval_24)
        fig = plt.figure(figsize=(12, 10))
        gs = gridspec.GridSpec(10, 13)
        skew = SkewT(fig, rotation=45, subplot=gs[0:12, 0:13])
        skew.ax.set_title(station_id+" Vertical Profiles\nLatitude: "+title_lat+""+lat_symbol+" | Longitude: "+title_lon+""+lon_symbol, fontsize=12, fontweight='bold', loc='left')
        skew.ax.set_title("Valid: " + date.strftime('%m/%d/%Y %H:00 UTC'), fontsize=12, fontweight='bold', loc='right')
        
        
        fig.patch.set_facecolor('aliceblue')
        
        
        skew.ax.set_ylim(1030, 100)
        skew.plot_dry_adiabats(label='Dry Adiabats', alpha=0.5)
        skew.plot_mixing_lines(label='Mixing Ratio Lines', alpha=0.5)
        skew.plot_moist_adiabats(label='Moist Adiabats', alpha=0.5)
        skew.ax.legend(loc=(0, 0), prop={'size': 10})
        skew.ax.set_xlabel("Temperature [℃]", fontsize=12, fontweight='bold')
        skew.ax.set_ylabel("Pressure [hPa]", fontsize=12, fontweight='bold')
        mask = (pressure >= 100 * units.hPa)
        skew.ax.set_ylim(1030, 100)
        skew.ax.set_xlim(-45, 45)
        
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

        label_date = date.strftime('%m/%d %H:00 UTC')
        label_date_24 = date_24.strftime('%m/%d %H:00 UTC')

        try:
            if mheight_diff >= 0:
                sym = '+'
            else:
                sym = ''
        except Exception as e:
            pass

        try:
        
            if LFC_NAN == True and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]\n24-HR ΔMixing Height: '+sym+''+str(mheight_diff)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            # Table if LFC   
            if LFC_NAN == False and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLFC\nPressure: '+LFC_Pres+' [hPa]\nTemperature: '+LFC_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + '[hPa]\nTemperature: ' + LCL_Temp + '[℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]\n24-HR ΔMixing Height: '+sym+''+str(mheight_diff)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            if LFC_NAN == True and EL_NAN == True:
                skew.ax.text(0.05, 0.3,'LCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]\n24-HR ΔMixing Height: '+sym+''+str(mheight_diff)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)    

        except Exception as e:

            if LFC_NAN == True and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            # Table if LFC   
            if LFC_NAN == False and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLFC\nPressure: '+LFC_Pres+' [hPa]\nTemperature: '+LFC_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + '[hPa]\nTemperature: ' + LCL_Temp + '[℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            if LFC_NAN == True and EL_NAN == True:
                skew.ax.text(0.04, 0.3,'LCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)       
        
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
        
        hgt_mask = (ft <= 6000)
        
        ax1.plot(rh[hgt_mask], ft[hgt_mask], color='green', label=label_date, alpha=0.5)
        try:
            hgt_mask_24 = (ft_24 <= 6000)
            ax1.plot(rh_24[hgt_mask_24], ft_24[hgt_mask_24], color='blue', label=label_date_24, alpha=0.5)
        except Exception as e:
            pass
        
        ax1.axhline(y=1000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=2000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=3000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=4000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=5000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.set_xlabel("Relative Humidity [%]", fontweight='bold')
        ax1.set_ylabel("Height [ft AGL]", fontweight='bold')
        ax1.legend(loc=(0.65, 0.9), prop={'size': 5})
        ax1.set_yticks([1000, 2000, 3000, 4000, 5000])
        
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
        
        ax2.barbs(x[idx], ft[idx], u[idx], v[idx], clip_on=True, zorder=10, color='darkred', label=label_date, length=5, alpha=0.5)
        
        try:
            ax2.barbs(x[idx_24], ft_24[idx_24], u_24[idx_24], v_24[idx_24], clip_on=True, zorder=10, color='darkblue', label=label_date_24, length=5, alpha=0.5)
        except Exception as e:
            pass
            
        ax2.plot(u, ft, label='u-wind', color='darkorange', alpha=0.5)
        ax2.plot(v, ft, label='v-wind', color='indigo', alpha=0.5)
        ax2.legend(loc=(0.9, 0), prop={'size': 5})
        bbox_props = dict(boxstyle='round', facecolor='bisque', alpha=1)
        ax2.text(1.01, 0.815, 'u-max: '+str(int(round(umax, 0)))+' [MPH]\nu-min: ' +str(int(round(umin, 0)))+' [MPH]\nv-max: ' +str(int(round(vmax, 0)))+' [MPH]\nv-min: ' +str(int(round(vmin, 0)))+' [MPH]', fontsize=6, fontweight='bold', bbox=bbox_props, transform=ax2.transAxes)
        
        ax2.set_xlabel("Wind Velocity [MPH]", fontsize=9, fontweight='bold')
        ax2.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        ax2.set_yticks([1000, 2000, 3000, 4000, 5000])
        
        ax3 = fig.add_subplot(gs[0:3, 4:7])
        ax3.tick_params(axis="y",direction="in", pad=-32)
        ax3.axvline(x=0, color='gray', alpha=0.5, linestyle='--')
        ax3.set_ylim(ft[0], 15000)
        ax3.set_xlabel("BVF-Squared [1/s^2]", fontsize=9, fontweight='bold')
        ax3.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        ax3.set_yticks([2000, 4000, 6000, 8000, 10000, 12000, 14000])
        
        # Plots the Brunt–Väisälä Frequency Squared
        ax3.plot(bv_squared, ft, color='red', alpha=0.5, label=label_date,)
        try:
            ax3.plot(bv_squared_24, ft_24, color='blue', alpha=0.5, label=label_date_24)
        except Exception as e:
            pass

        ax3.legend(loc=(0.57, 0.9), prop={'size': 5})

        ax4 = fig.add_subplot(gs[4:6, 1:4])

        ax4.tick_params(axis="y",direction="in", pad=-27)
        ax4.set_yticks([2000, 4000, 6000, 8000, 10000])
        ax4.set_xlabel("Temperature [℃]", fontsize=9, fontweight='bold')
        ax4.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        
        hgts_mask = (ft <= 12000)
        
        ax4.plot(temps[hgts_mask], ft[hgts_mask], color='darkred', label=label_date, alpha=0.5)
        try:
            hgts_mask_24 = (ft_24 <= 12000)
            ax4.plot(temps_24[hgts_mask_24], ft_24[hgts_mask_24], color='magenta', label=label_date_24, alpha=0.5)
        except Exception as e:
            pass        

        ax4.legend(loc=(0.2, 1.01), prop={'size': 7})
        
        fig.text(0.16, 0.05, "Plot Created With FireWxPy(C) Eric J. Drewitz 2024\nData Source: weather.uwyo.edu\nImage Created: "+utc_time.strftime('%m/%d/%Y %H:00 UTC'), fontsize=8, bbox=props)

    if sounding == False:
        fig = standard.no_sounding_graphic(date)

    fname = station_id+" VERTICAL PROFILES"
    
    file_functions.save_daily_sounding_graphic(fig, station_id, None)  

def plot_observed_sounding_custom_date_time(station_id, year, month, day, hour):

    local_time, utc_time = standard.plot_creation_time()

    station_id = station_id
    station_id = station_id.upper()    
    

    date = datetime(year, month, day, hour)
    date_24 = date - timedelta(hours=24)

    # pings the server to request data
    try:
        df = WyomingUpperAir.request_data(date, station_id)
        print(station_id+' '+date.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
        sounding = True
    except Exception as a:
        print("Trying again! - Just in case.")
        try:
            time.sleep(10)
            df = WyomingUpperAir.request_data(date, station_id)
            print(station_id+' '+date.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
            sounding = True
        except Exception as b:
            try:
                print("Trying one last time! - This server can be glitchy.")
                time.sleep(10)
                df = WyomingUpperAir.request_data(date, station_id)
                print(station_id+' '+date.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
                sounding = True                
            except Exception as c:
                print("ERROR! User entered an invalid date or station ID")
                sounding = False

    try:
        df_24 = WyomingUpperAir.request_data(date_24, station_id)
        print(station_id+' '+date_24.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
    except Exception as a:
        print("Trying again! - Just in case.")
        try:
            time.sleep(10)
            df_24 = WyomingUpperAir.request_data(date_24, station_id)
            print(station_id+' '+date_24.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
        except Exception as b:
            try:
                print("Trying one last time! - This server can be glitchy.")
                time.sleep(10)
                df_24 = WyomingUpperAir.request_data(date_24, station_id)
                print(station_id+' '+date_24.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')              
            except Exception as c:
                print(station_id+' '+date_24.strftime('%m/%d/%Y %H:00 UTC')+' data not availiable.\nThere will be no 24-HR Comparisons on this plot.')

    if sounding == True:

        df.drop_duplicates(inplace=True,subset='pressure',ignore_index=True)
        df.dropna(axis=0, inplace=True)
        df['height'] = clean_height_data(df['height'])
        mheight = Thermodynamics.find_mixing_height(df['temperature'], df['height'])
        elev = df['elevation'] * 3.28084
        mheight = mheight - elev
        mheight = mheight.iloc[0]
        mheight = int(round(mheight, 0))
        d = pandas_dataframe_to_unit_arrays(df)
    
        temps = d['temperature'].m
        hgt = d['height'].m
        pressure = d['pressure']
        temperature = d['temperature']
        dewpoint = d['dewpoint']
        ws = d['speed']
        u = d['u_wind']
        v = d['v_wind']
        direction = d['direction']
        pwats = d['pw']
        station_elevation = d['elevation']
        lat = d['latitude'][0].m
        lon = d['longitude'][0].m
        height = d['height']
        elevation = d['elevation']
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

        theta = mpcalc.potential_temperature(pressure, temperature)

        try:
            df_24.drop_duplicates(inplace=True,subset='pressure',ignore_index=True)
            df_24.dropna(axis=0, inplace=True)
            df_24['height'] = clean_height_data(df_24['height'])
            mheight_24 = Thermodynamics.find_mixing_height(df_24['temperature'], df_24['height'])
            elev_24 = df_24['elevation'] * 3.28084
            mheight_24 = mheight_24 - elev_24
            mheight_24 = mheight_24.iloc[0]
            mheight_24 = int(round(mheight_24, 0))
            d_24 = pandas_dataframe_to_unit_arrays(df_24)
    
            temperature_24 = d_24['temperature']
            temps_24 = d_24['temperature'].m
            dewpoint_24 = d_24['dewpoint']
            hgt_24 = d_24['height'].m
            rh_24 = (mpcalc.relative_humidity_from_dewpoint(temperature_24, dewpoint_24) * 100)
            pressure_24 = d_24['pressure']
            u_24 = d_24['u_wind']
            v_24 = d_24['v_wind']
            u_24 = u_24.m * 1.15078
            v_24 = v_24.m * 1.15078
            height_24 = d_24['height']
            elevation_24 = d_24['elevation']
            elevation_24 = elevation_24.m * 3.28084
    
            ft_24 = height_24.m *3.28084
            ft_24 = ft_24 - elevation_24
            hgts_24 = hgt_24
            hgt_24 = hgt_24 - elevation_24
            
            if len(temps_24) > len(hgts_24):
                df_len_24 = len(hgts_24)
            elif len(temps_24) < len(hgts_24):
                df_len_24 = len(temps_24)
            else:
                df_len_24 = len(temps_24)
    
            theta_24 = mpcalc.potential_temperature(pressure_24, temperature_24)
            mheight_diff = mheight - mheight_24
            bv_squared_24 = mpcalc.brunt_vaisala_frequency_squared(height_24, theta_24) 

        except Exception as e:
            pass
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
        barb_mask = (pressure >= 100 * units.hPa)
        pres = pressure[barb_mask]
        idx = mpcalc.resample_nn_1d(pres, interval)
        interval_24 = np.logspace(2, 3) * units.hPa
        barb_mask_24 = (pressure_24 >= 100 * units.hPa)
        pres_24 = pressure_24[barb_mask_24]
        idx_24 = mpcalc.resample_nn_1d(pres_24, interval_24)
        fig = plt.figure(figsize=(12, 10))
        gs = gridspec.GridSpec(10, 13)
        skew = SkewT(fig, rotation=45, subplot=gs[0:12, 0:13])
        skew.ax.set_title(station_id+" Vertical Profiles\nLatitude: "+title_lat+""+lat_symbol+" | Longitude: "+title_lon+""+lon_symbol, fontsize=12, fontweight='bold', loc='left')
        skew.ax.set_title("Valid: " + date.strftime('%m/%d/%Y %H:00 UTC'), fontsize=12, fontweight='bold', loc='right')
        
        
        fig.patch.set_facecolor('aliceblue')
        
        
        skew.ax.set_ylim(1030, 100)
        skew.plot_dry_adiabats(label='Dry Adiabats', alpha=0.5)
        skew.plot_mixing_lines(label='Mixing Ratio Lines', alpha=0.5)
        skew.plot_moist_adiabats(label='Moist Adiabats', alpha=0.5)
        skew.ax.legend(loc=(0, 0), prop={'size': 10})
        skew.ax.set_xlabel("Temperature [℃]", fontsize=12, fontweight='bold')
        skew.ax.set_ylabel("Pressure [hPa]", fontsize=12, fontweight='bold')
        mask = (pressure >= 100 * units.hPa)
        skew.ax.set_ylim(1030, 100)
        skew.ax.set_xlim(-45, 45)
        
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

        label_date = date.strftime('%m/%d %H:00 UTC')
        label_date_24 = date_24.strftime('%m/%d %H:00 UTC')

        try:
            if mheight_diff >= 0:
                sym = '+'
            else:
                sym = ''
        except Exception as e:
            pass

        try:
        
            if LFC_NAN == True and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]\n24-HR ΔMixing Height: '+sym+''+str(mheight_diff)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            # Table if LFC   
            if LFC_NAN == False and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLFC\nPressure: '+LFC_Pres+' [hPa]\nTemperature: '+LFC_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + '[hPa]\nTemperature: ' + LCL_Temp + '[℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]\n24-HR ΔMixing Height: '+sym+''+str(mheight_diff)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            if LFC_NAN == True and EL_NAN == True:
                skew.ax.text(0.05, 0.3,'LCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]\n24-HR ΔMixing Height: '+sym+''+str(mheight_diff)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)    

        except Exception as e:

            if LFC_NAN == True and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            # Table if LFC   
            if LFC_NAN == False and EL_NAN == False:
                skew.ax.text(0.04, 0.3,'EL\nPressure: '+EL_Pres+' [hPa]\nTemperature: '+EL_Temp+' [℃]\n\nLFC\nPressure: '+LFC_Pres+' [hPa]\nTemperature: '+LFC_Temp+' [℃]\n\nLCL\nPressure: ' + LCL_Pres + '[hPa]\nTemperature: ' + LCL_Temp + '[℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)
            
            if LFC_NAN == True and EL_NAN == True:
                skew.ax.text(0.04, 0.3,'LCL\nPressure: ' + LCL_Pres + ' [hPa]\nTemperature: ' + LCL_Temp + ' [℃]\n\nMixing Height: '+str(mheight)+' [ft AGL]', transform=skew.ax.transAxes,
                             fontsize=6, fontweight='bold', verticalalignment='top', bbox=props)       
        
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
        
        hgt_mask = (ft <= 6000)
        
        ax1.plot(rh[hgt_mask], ft[hgt_mask], color='green', label=label_date, alpha=0.5)
        try:
            hgt_mask_24 = (ft_24 <= 6000)
            ax1.plot(rh_24[hgt_mask_24], ft_24[hgt_mask_24], color='blue', label=label_date_24, alpha=0.5)
        except Exception as e:
            pass
        
        ax1.axhline(y=1000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=2000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=3000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=4000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.axhline(y=5000, xmin=0.14, xmax=1, linewidth=0.5, linestyle='--', color='red')
        ax1.set_xlabel("Relative Humidity [%]", fontweight='bold')
        ax1.set_ylabel("Height [ft AGL]", fontweight='bold')
        ax1.legend(loc=(0.65, 0.9), prop={'size': 5})
        ax1.set_yticks([1000, 2000, 3000, 4000, 5000])
        
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
        
        ax2.barbs(x[idx], ft[idx], u[idx], v[idx], clip_on=True, zorder=10, color='darkred', label=label_date, length=5, alpha=0.5)
        
        try:
            ax2.barbs(x[idx_24], ft_24[idx_24], u_24[idx_24], v_24[idx_24], clip_on=True, zorder=10, color='darkblue', label=label_date_24, length=5, alpha=0.5)
        except Exception as e:
            pass
            
        ax2.plot(u, ft, label='u-wind', color='darkorange', alpha=0.5)
        ax2.plot(v, ft, label='v-wind', color='indigo', alpha=0.5)
        ax2.legend(loc=(0.9, 0), prop={'size': 5})
        bbox_props = dict(boxstyle='round', facecolor='bisque', alpha=1)
        ax2.text(1.01, 0.815, 'u-max: '+str(int(round(umax, 0)))+' [MPH]\nu-min: ' +str(int(round(umin, 0)))+' [MPH]\nv-max: ' +str(int(round(vmax, 0)))+' [MPH]\nv-min: ' +str(int(round(vmin, 0)))+' [MPH]', fontsize=6, fontweight='bold', bbox=bbox_props, transform=ax2.transAxes)
        
        ax2.set_xlabel("Wind Velocity [MPH]", fontsize=9, fontweight='bold')
        ax2.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        ax2.set_yticks([1000, 2000, 3000, 4000, 5000])
        
        ax3 = fig.add_subplot(gs[0:3, 4:7])
        ax3.tick_params(axis="y",direction="in", pad=-32)
        ax3.axvline(x=0, color='gray', alpha=0.5, linestyle='--')
        ax3.set_ylim(ft[0], 15000)
        ax3.set_xlabel("BVF-Squared [1/s^2]", fontsize=9, fontweight='bold')
        ax3.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        ax3.set_yticks([2000, 4000, 6000, 8000, 10000, 12000, 14000])
        
        # Plots the Brunt–Väisälä Frequency Squared
        ax3.plot(bv_squared, ft, color='red', alpha=0.5, label=label_date,)
        try:
            ax3.plot(bv_squared_24, ft_24, color='blue', alpha=0.5, label=label_date_24)
        except Exception as e:
            pass

        ax3.legend(loc=(0.57, 0.9), prop={'size': 5})

        ax4 = fig.add_subplot(gs[4:6, 1:4])

        ax4.tick_params(axis="y",direction="in", pad=-27)
        ax4.set_yticks([2000, 4000, 6000, 8000, 10000])
        ax4.set_xlabel("Temperature [℃]", fontsize=9, fontweight='bold')
        ax4.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        
        hgts_mask = (ft <= 12000)
        
        ax4.plot(temps[hgts_mask], ft[hgts_mask], color='darkred', label=label_date, alpha=0.5)
        try:
            hgts_mask_24 = (ft_24 <= 12000)
            ax4.plot(temps_24[hgts_mask_24], ft_24[hgts_mask_24], color='magenta', label=label_date_24, alpha=0.5)
        except Exception as e:
            pass        

        ax4.legend(loc=(0.2, 1.01), prop={'size': 7})
        
        fig.text(0.16, 0.05, "Plot Created With FireWxPy(C) Eric J. Drewitz 2024\nData Source: weather.uwyo.edu\nImage Created: "+utc_time.strftime('%m/%d/%Y %H:00 UTC'), fontsize=8, bbox=props)

    if sounding == False:
        fig = standard.no_sounding_graphic(date)

    fname = station_id+" VERTICAL PROFILES"
    
    file_functions.save_daily_sounding_graphic(fig, station_id, date)  
        
