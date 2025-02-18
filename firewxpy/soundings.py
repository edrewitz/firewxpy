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
import time as tim
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import metpy.plots as mpplots

from firewxpy.calc import Thermodynamics, unit_conversion
from matplotlib import transforms as transform
from siphon.simplewebservice.wyoming import WyomingUpperAir
from metpy.units import units, pandas_dataframe_to_unit_arrays
from metpy.plots import SkewT
from metpy.units import units
from datetime import datetime, timedelta
from firewxpy.utilities import file_functions 
from firewxpy.data_access import model_data, station_coords
from metpy.plots import USCOUNTIES
from matplotlib.patheffects import withStroke

mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 5
mpl.rcParams['ytick.labelsize'] = 5

pd.options.mode.copy_on_write = True

local_time, utc_time = standard.plot_creation_time()

datacrs = ccrs.PlateCarree()
mapcrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)

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


def plot_forecast_soundings(model, station_id, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):

    r'''
        This function plots the vertical profile forecasts for a given point and shows the transport wind and precipitation forecast in the vicinity of the point. 

        Required Arguments:

        1) model (String) - This is the model the user must select. 
                               
               Here are the choices: 
               1) GFS0p25 - GFS 0.25x0.25 degree
               2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
               3) GFS0p50 - GFS 0.5x0.5 degree
               4) GFS1p00 - GFS 1.0x1.0 degree
               5) NAM - North American Model
               6) NAM 1hr - North American Model with 1 hour intervals 
               7) RAP - RAP for the CONUS
               8) RAP 32 - 32km North American RAP

        2) station_id (String) - The 4-letter airport station identifier. 
                                 If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

        Optional Arguments:

        1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
        
        2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
        
        3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
            and passing the data in or if the function needs to download the data. A value of False means the data
            is downloaded inside of the function while a value of True means the user is downloading the data outside
            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
            things, it is recommended to set this value to True and download the data outside of the function and pass
            it in so that the amount of data requests on the host servers can be minimized. 


        4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
            in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
            outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

        5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                 wishes to use a reference system not on this list, please see items 17-23. 
            
            Reference Systems: 
            
            1) 'States & Counties'
            2) 'States Only'
            3) 'GACC Only'
            4) 'GACC & PSA'
            5) 'CWA Only'
            6) 'NWS CWAs & NWS Public Zones'
            7) 'NWS CWAs & NWS Fire Weather Zones'
            8) 'NWS CWAs & Counties'
            9) 'GACC & PSA & NWS Fire Weather Zones'
            10) 'GACC & PSA & NWS Public Zones'
            11) 'GACC & PSA & NWS CWA'
            12) 'GACC & PSA & Counties'
            13) 'GACC & Counties'


        6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.   

        Returns: A set of forecast vertical profile graphics saved to f:Weather Data/Forecast Model Data/{model}/Soundings/{latitude}{lat_symbol}/{longitude}{lon_symbol}/{reference_system}
    
    '''

    mpl.rcParams['xtick.labelsize'] = 5
    mpl.rcParams['ytick.labelsize'] = 5

    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    if reference_system == 'Custom' or reference_system == 'custom':
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        show_psa_borders = show_psa_borders
        show_cwa_borders = show_cwa_borders
        show_nws_firewx_zones = show_nws_firewx_zones
        show_nws_public_zones = show_nws_public_zones

        state_border_linewidth = state_border_linewidth
        county_border_linewidth = county_border_linewidth
        gacc_border_linewidth = gacc_border_linewidth
        cwa_border_linewidth = cwa_border_linewidth
        nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
        nws_public_zones_linewidth = nws_public_zones_linewidth
        psa_border_linewidth = psa_border_linewidth

    if reference_system != 'Custom' and reference_system != 'custom':
        
        show_state_borders = False
        show_county_borders = False
        show_gacc_borders = False
        show_psa_borders = False
        show_cwa_borders = False
        show_nws_firewx_zones = False
        show_nws_public_zones = False

        if reference_system == 'States Only':
            show_state_borders = True
            state_border_linewidth=1 
        if reference_system == 'States & Counties':
            show_state_borders = True
            show_county_borders = True
            state_border_linewidth=1 
            county_border_linewidth=0.25
        if reference_system == 'GACC Only':
            show_gacc_borders = True
            gacc_border_linewidth=1
        if reference_system == 'GACC & PSA':
            show_gacc_borders = True
            show_psa_borders = True
            gacc_border_linewidth=1
            psa_border_linewidth=0.25
        if reference_system == 'CWA Only':
            show_cwa_borders = True
            cwa_border_linewidth=1
        if reference_system == 'NWS CWAs & NWS Public Zones':
            show_cwa_borders = True
            show_nws_public_zones = True
            cwa_border_linewidth=1
            nws_public_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
            show_cwa_borders = True
            show_nws_firewx_zones = True
            cwa_border_linewidth=1
            nws_firewx_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & Counties':
            show_cwa_borders = True
            show_county_borders = True
            cwa_border_linewidth=1
            county_border_linewidth=0.25
        if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_firewx_zones = True
            gacc_border_linewidth=1
            psa_border_linewidth=0.5
            nws_firewx_zones_linewidth=0.25
        if reference_system == 'GACC & PSA & NWS Public Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_public_zones = True
            gacc_border_linewidth=1
            psa_border_linewidth=0.5
            nws_public_zones_linewidth=0.25
        if reference_system == 'GACC & PSA & NWS CWA':
            show_gacc_borders = True
            show_psa_borders = True
            show_cwa_borders = True
            gacc_border_linewidth=1
            psa_border_linewidth=0.5
            cwa_border_linewidth=0.25
        if reference_system == 'GACC & PSA & Counties':
            show_gacc_borders = True
            show_psa_borders = True
            show_county_borders = True
            gacc_border_linewidth=1
            psa_border_linewidth=0.5
            county_border_linewidth=0.25 
        if reference_system == 'GACC & Counties':
            show_gacc_borders = True
            show_county_borders = True
            gacc_border_linewidth=1
            county_border_linewidth=0.25 

    if data == False:
        if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
            ds_point = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
            
            longitude = ds_point['tmpprs']['lon'].values
            latitude = ds_point['tmpprs']['lat'].values
            western_bound = longitude - 6
            eastern_bound = longitude + 6
            northern_bound = latitude + 3
            southern_bound = latitude - 3
            
            ds_area = model_data.get_hourly_rap_data_area_forecast(model, 'custom', western_bound, eastern_bound, southern_bound, northern_bound)
    
        else:
            if model == 'RAP 32' or model == 'rap 32':
                ds_point = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
            else:
                ds_point = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
            
            longitude = ds_point['tmpprs']['lon'].values
            latitude = ds_point['tmpprs']['lat'].values
            western_bound = longitude - 6
            eastern_bound = longitude + 6
            northern_bound = latitude + 3
            southern_bound = latitude - 3

            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':

                if western_bound > 180:
                    western_bound_data = (360 - western_bound)
                if eastern_bound >180:
                    eastern_bound_data = (360 - eastern_bound)

                if model == 'RAP 32' or model == 'rap 32':

                    if western_bound < 0:
                        western_bound_data = western_bound * -1 
                    if eastern_bound < 0:
                        eastern_bound_data = eastern_bound * -1 
                    ds_area = model_data.get_hourly_rap_data_area_forecast(model, 'custom', western_bound_data, eastern_bound_data, southern_bound, northern_bound)

                else:
                    ds_area = model_data.get_nomads_opendap_data(model, 'custom', western_bound_data, eastern_bound_data, southern_bound, northern_bound)

            else:
            
                ds_area = model_data.get_nomads_opendap_data(model, 'custom', western_bound, eastern_bound, southern_bound, northern_bound)
            
    if data == True:

        ds = ds

        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude 
            latitude = latitude
            western_bound = longitude - 6
            eastern_bound = longitude + 6
            northern_bound = latitude + 3
            southern_bound = latitude - 3
        else:
            longitude, latitude = station_coords(station_id)
            western_bound = longitude - 6
            eastern_bound = longitude + 6
            northern_bound = latitude + 3
            southern_bound = latitude - 3

        if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
            
            if longitude < 0:
                longitude = 360 + longitude
            else:
                longitude = longitude   

            if western_bound < 0:
                western_bound_data = western_bound * -1 
            if eastern_bound < 0:
                eastern_bound_data = eastern_bound * -1 
        
            ds_point = ds.sel(lon=longitude, lat=latitude, method='nearest')
            ds_area = ds.sel(lon=slice(360-western_bound_data, 360-eastern_bound_data, 1), lat=slice(southern_bound, northern_bound, 1))

        else:
            ds_point = ds.sel(lon=longitude, lat=latitude, method='nearest')
            ds_area = ds.sel(lon=slice(western_bound, eastern_bound, 1), lat=slice(southern_bound, northern_bound, 1))            

    if station_id == 'Custom' or station_id == 'custom':
        longitude = longitude
        latitude = latitude

    else:
        longitude = ds_point['tmpprs']['lon'].values
        latitude = ds_point['tmpprs']['lat'].values

    if longitude > 180:
        longitude = (360 - longitude) * -1
    else:
        longitude = longitude


    path, path_print, lat_symbol, lon_symbol = file_functions.point_forecast_sounding_graphics_paths(model, latitude, longitude, reference_system)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass

    print(f"Any old images (if any) in {path_print} have been deleted.")

    title_lon = str(round(float(abs(longitude)), 1))
    title_lat = str(round(float(abs(latitude)), 1))

    stop = (len(ds_point['time']) - 1)

    time = ds_point['time']
    times = time.to_pandas()

    if stop >= 100:
        step = 2
    else:
        step = 1

    for i in range(0, stop, step):

        fname = f"Image_{i}.png"
        
        rh = ds_point['rhprs'][i,:]
        rh.dropna(dim='lev')
        temperature = ds_point['tmpprs'][i,:] - 273.15
        temperature.dropna(dim='lev')
        levels = temperature['lev'].to_numpy().flatten()


        dwpt = mpcalc.dewpoint_from_relative_humidity(temperature * units('degC'), rh * units('percent'))
        temperature = temperature.to_numpy().flatten()

        wetbulb = mpcalc.wet_bulb_temperature(levels * units('hPa'), temperature * units('degC'), dwpt)
        height_ft = (ds_point['hgtprs'][i, :]) * 3.28084
        height_sfc = (ds_point['hgtsfc'][i])  * 3.28084
        height_agl = height_ft - height_sfc
        sfc_pressure = (ds_point['pressfc'][i]) / 100
        sfc_pressure = sfc_pressure.to_numpy().flatten()
        u = (ds_point['ugrdprs'][i,:]) * 2.23694
        v = (ds_point['vgrdprs'][i,:]) * 2.23694
        ws = mpcalc.wind_speed(u * units('mph'), v * units('mph'))
        try:
            total_cloud_cover = ds_point['tcdcprs'][i,:]
            total_cloud_cover.dropna(dim='lev')
            total_cloud_cover = total_cloud_cover.to_numpy().flatten()
            cloud_cover = True
        except Exception as e:
            cloud_cover = False
        vv = ds_point['vvelprs'][i,:]
        vv = vv.to_numpy().flatten()
        pwat = (ds_point['pwatclm'][i].values) * 0.039370
        
        m_hgt_mask = (height_agl >= 0) & (levels <= sfc_pressure)
        heights = []
        for j in range(0, (len(temperature[m_hgt_mask]) - 1)):
            if int(round(float(temperature[m_hgt_mask][j+1]),0)) >= int(round(float(temperature[m_hgt_mask][j]),0)):
                m_height = height_agl[m_hgt_mask][j]
                heights.append(m_height)

        try:
            mixing_height_idx = heights[0]
            mixing_height = mixing_height_idx.values
        except Exception as e:
            mixing_height = 99999

        f_heights = []
        for j in range(0, (len(temperature[m_hgt_mask]) - 1)):
            if temperature[m_hgt_mask][j+1] <= 0 and temperature[m_hgt_mask][j] > 0:
                f_height = height_agl[m_hgt_mask][j+1]
                heights.append(f_height)

        try:
            frz_height_idx = f_heights[0]
            freezing_level = frz_height_idx.values
        except Exception as e:
            freezing_level = 0
            
        height_0c = (ds_point['hgt0c'][i].values) * 3.28084

        t2m = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds_point['tmp2m'][i].values)
        rh2m = ds_point['rh2m'][i].values

        if t2m >= 33:
            freezing_level = height_0c
        else:
            freezing_level = freezing_level

        try:
            ds_area['pratesfc'][i,:]
            title = f"PRECIPITATION RATE [IN/HR]"
            prate = True
        except Exception as e:
            prate = False
            if step == 2:
                title = f"6HR PRECIPITATION [IN]"
            if step == 1:
                title = f"3HR PRECIPITATION [IN]"

        i = i
        k = i -1
        
        try:
            for j in range(0, k):

                ds_area['psum'][j, :, :] = sum(ds_area['apcpsfc'][j, :, :])
                ds_area['apcpsfc'][i, :, :] = ds_area['apcpsfc'][i, :, :] - ds_area['psum'][j, :, :]  

        except Exception as e:

            ds_area['apcpsfc'][i, :, :] = ds_area['apcpsfc'][i, :, :]


        fig = plt.figure(figsize=(18, 7))
        gs = gridspec.GridSpec(10, 19)
        skew = SkewT(fig, rotation=45, subplot=gs[0:10, 0:9])
        if station_id == 'Custom' or station_id == 'custom':
            skew.ax.set_title(f"{model.upper()} Forecast\nLatitude: {title_lat}{lat_symbol} | Longitude: {title_lon}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
    
        else:
            skew.ax.set_title(f"{model.upper()} Forecast\nStation: {station_id.upper()}\nLatitude: {title_lat}{lat_symbol} | Longitude: {title_lon}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
    
        
        skew.ax.set_title(f"Valid: {times.iloc[i].strftime('%a %m/%d/%Y %H:00 UTC')}\nInitialization: {times.iloc[0].strftime('%a %m/%d/%Y %H:00 UTC')}", fontsize=7, fontweight='bold', loc='right')
        
        
        fig.patch.set_facecolor('aliceblue')

        skew_mask = (levels <= sfc_pressure)
        barb_mask = (levels <= sfc_pressure) & (levels > 100)

        skew.ax.set_ylim(sfc_pressure, 100)
        skew.ax.set_xlim(-40, 45)
        skew.plot_dry_adiabats(label='Dry Adiabats', alpha=0.5)
        skew.plot_mixing_lines(label='Mixing Ratio Lines', alpha=0.5)
        skew.plot_moist_adiabats(label='Moist Adiabats', alpha=0.5)
        skew.ax.legend(loc=(0, 0.875), prop={'size': 10})
        skew.ax.set_xlabel("Temperature [℃]", fontsize=10, fontweight='bold')
        skew.ax.set_ylabel("Pressure [hPa]", fontsize=10, fontweight='bold')

        skew.plot(levels[skew_mask], temperature[skew_mask], 'red', alpha=0.5, linewidth=2)
        skew.plot(levels[skew_mask], dwpt[skew_mask], 'green', alpha=0.5, linewidth=2)

        skew.plot(levels[skew_mask], wetbulb[skew_mask], 'cyan', alpha=0.5, linewidth=1)
        skew.plot_barbs(levels[barb_mask], u[barb_mask], v[barb_mask], color='blue', length=6)

        ax1 = fig.add_subplot(gs[0:4, 9:11])
        ax1.tick_params(axis="y",direction="in", pad=-20)
        hgt_mask = (height_agl >= 0) & (height_agl <= 10000)
        ax1.plot(rh[hgt_mask], height_agl[hgt_mask], color='darkgreen', alpha=0.5)
        ax1.set_title(f"RH [%] vs. Height [FT]\n[Lowest 10000FT AGL]", fontweight='bold', fontsize=7)
        ax1.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax1.set_yticks([2000, 4000, 6000, 8000, 10000])
        ax1.set_ylim(0, 10500)
        ax1.text(0.605, 0.92, f"MAX: {int(round(float(np.nanmax(rh[hgt_mask])), 0))} [%]\nMIN: {int(round(float(np.nanmin(rh[hgt_mask])), 0))} [%]", fontweight='bold', fontsize=5, bbox=props, transform=ax1.transAxes)


        ax2 = fig.add_subplot(gs[0:4, 11:13])
        ax2.tick_params(axis="y",direction="in", pad=-20)
        ax2.set_title(f"Wind [MPH] vs. Height [FT]\n[Lowest 10000FT AGL]", fontweight='bold', fontsize=6)
        ax2.set_yticks([2000, 4000, 6000, 8000, 10000])
        ax2.set_ylim(0, 10500)
        ax2.plot(ws[hgt_mask], height_agl[hgt_mask], color='darkred', alpha=0.5)
        xmin = np.nanmin(ws[hgt_mask])
        xmax = np.nanmax(ws[hgt_mask])
        ax2.set_xlim(xmin, xmax)
        mean = ((xmin + xmax)/2)
        xloc = int(round(mean, 0))
        x = np.empty_like(height_agl)
        x.fill(xloc)
        ax2.barbs(x[hgt_mask], height_agl[hgt_mask], u[hgt_mask], v[hgt_mask], clip_on=True, zorder=10, color='darkblue', length=5, alpha=0.5)
        ax2.text(0.55, 0.92, f"MAX: {int(round(float(np.nanmax(ws[hgt_mask])), 0))} [MPH]\nMIN: {int(round(float(np.nanmin(ws[hgt_mask])), 0))} [MPH]", fontweight='bold', fontsize=5, bbox=props, transform=ax2.transAxes)

        if cloud_cover == True:
        
            ax3 = fig.add_subplot(gs[0:4, 13:16])
            ax3.tick_params(axis="y",direction="in", pad=-20)
            ax3.set_title(f"TOTAL CLOUD COVER [%] vs. HEIGHT [FT]\n[Lowest 30000FT AGL]", fontweight='bold', fontsize=5)
            ax3.set_yticks([5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000])
            ax3.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            ax3.set_ylim(0, 30500)
            cloud_mask = (height_agl >= 0) & (height_agl <= 30000)
            ax3.plot(total_cloud_cover[cloud_mask], height_agl[cloud_mask], color='cyan', alpha=0.5)
            ax3.text(0.68, 0.875, f"MAX: {int(round(float(np.nanmax(total_cloud_cover[cloud_mask])), 0))} [%]\nMIN: {int(round(float(np.nanmin(total_cloud_cover[cloud_mask])), 0))} [%]", fontweight='bold', fontsize=6, bbox=props, transform=ax3.transAxes)
    
            ax4 = fig.add_subplot(gs[0:4, 16:19])
            ax4.set_ylim(0, 10500)
            ax4.tick_params(axis="y",direction="in", pad=-20)
            ax4.set_title(f"VERTICAL VELOCITY [Pa/s] vs. HEIGHT [FT]\n[LOWEST 10000FT AGL]", fontweight='bold', fontsize=5)
            ax4.set_yticks([2000, 4000, 6000, 8000, 10000])
            ax4.plot(vv[hgt_mask], height_agl[hgt_mask], color='darkorange', alpha=0.5)
            ax4.text(0.59, 0.875, f"MAX: {round(float(np.nanmax(vv[hgt_mask])), 2)} [Pa/s]\nMIN: {round(float(np.nanmin(vv[hgt_mask])), 2)} [Pa/s]", fontweight='bold', fontsize=6, bbox=props, transform=ax4.transAxes)

        else:
            ax4 = fig.add_subplot(gs[0:4, 13:19])
            ax4.set_ylim(0, 10500)
            ax4.tick_params(axis="y",direction="in", pad=-20)
            ax4.set_title(f"VERTICAL VELOCITY [Pa/s] vs. HEIGHT [FT]\n[LOWEST 10000FT AGL]", fontweight='bold', fontsize=6)
            ax4.set_yticks([2000, 4000, 6000, 8000, 10000])
            ax4.plot(vv[hgt_mask], height_agl[hgt_mask], color='darkorange', alpha=0.5)   
            ax4.text(0.78, 0.875, f"MAX: {round(float(np.nanmax(vv[hgt_mask])), 2)} [Pa/s]\nMIN: {round(float(np.nanmin(vv[hgt_mask])), 2)} [Pa/s]", fontweight='bold', fontsize=6, bbox=props, transform=ax4.transAxes)


        speeds = np.arange(10, 81, 1)
        speed_ticks = speeds[::5]
        cmap = colormaps.wind_speed_colormap()
        
        ax5 = fig.add_subplot(gs[5:9, 9:14], projection=mapcrs)
        ax5.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax5.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax5.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax5.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax5.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax5.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax5.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax5.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax5.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax5.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax5.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax5.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax5.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax5.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass

        
        ax5.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax5.set_title(f"10M TRANSPORT WIND [MPH]", fontsize=7, fontweight='bold')
        ax5.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax5.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
        
        lon_2d, lat_2d = np.meshgrid(ds_area['lon'], ds_area['lat'])

        if model == 'NAM' or model == 'RAP':
            decimate = 7
        elif model == 'GFS0p50' or model == 'GEFS0p50' or model == 'GFS1p00':
            decimate = 1
        else:
            decimate = 3
        
        stn = mpplots.StationPlot(ax5, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                         transform=ccrs.PlateCarree(), zorder=3, fontsize=6, clip_on=True)


        if model == 'GEFS0P50':

            stn.plot_barb((ds_area['ugrd10m'][0, i, ::decimate, ::decimate] * 2.23694), (ds_area['vgrd10m'][0, i, ::decimate, ::decimate] * 2.23694), color='black', alpha=1, zorder=3, linewidth=0.5)
                
            cs = ax5.contourf(ds_area['lon'], ds_area['lat'], (mpcalc.wind_speed((ds_area['ugrd10m'][0, i, :, :] *units('m/s')), (ds_area['vgrd10m'][0, i, :, :] *units('m/s'))) * 2.23694), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=1, pad=0.01, location='bottom', ticks=speed_ticks, ax=ax5)
            
        else:
            
            stn.plot_barb((ds_area['ugrd10m'][i, ::decimate, ::decimate] * 2.23694), (ds_area['vgrd10m'][i, ::decimate, ::decimate] * 2.23694), color='black', alpha=1, zorder=3, linewidth=0.5)

            cs = ax5.contourf(ds_area['lon'], ds_area['lat'], (mpcalc.wind_speed((ds_area['ugrd10m'][i, :, :] *units('m/s')), (ds_area['vgrd10m'][i, :, :] *units('m/s'))) * 2.23694), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=1, pad=0.01, location='bottom', ticks=speed_ticks, ax=ax5)


        cmap_p = colormaps.precipitation_colormap()

        levels_p = [round(0.01, 2), round(0.05, 2), round(0.1, 1), round(0.2, 1), round(0.3, 1), round(0.4, 1), round(0.5, 1), round(0.6, 1), round(0.7, 1), round(0.8, 1), round(0.9, 1), int(round(1, 0)), round(1.25, 2), round(1.5, 1), round(1.75, 2), int(round(2, 0)), round(2.5, 1), int(round(3,0))]
        ticks_p = levels_p
        levels_pr = [round(0.01, 2), round(0.05, 2), round(0.1, 1), round(0.15, 2), round(0.2, 1), round(0.3, 1), round(0.4, 1), round(0.5, 1), round(0.6, 1), round(0.7, 1), round(0.8, 1), round(0.9, 1), int(round(1, 0)), round(1.5, 1), int(round(2, 0)), round(2.5, 1), int(round(3, 0))]
        ticks_pr = levels_pr

        ax6 = fig.add_subplot(gs[5:9, 14:19], projection=mapcrs)
        ax6.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax6.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax6.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax6.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax6.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax6.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax6.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax6.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax6.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax6.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax6.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax6.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax6.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax6.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass            

        ax6.set_title(f"{title}", fontsize=7, fontweight='bold')
        ax6.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax6.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

        ax6.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        
        lon_2d, lat_2d = np.meshgrid(ds_area['lon'], ds_area['lat'])

        decimate = decimate * 2

        stn1 = mpplots.StationPlot(ax6, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                         transform=ccrs.PlateCarree(), zorder=3, fontsize=6, clip_on=True)
             
            
        if prate == False:
            qpf = ds_area['apcpsfc'][i, :, :] * 0.039370

            qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
    
            stn1.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs1 = ax6.contourf(ds_area['lon'], ds_area['lat'], (ds_area['apcpsfc'][i, :, :] * 0.039370), cmap=cmap_p, transform=datacrs, levels=levels_p, alpha=0.35, extend='max')
            cbar1 = fig.colorbar(cs1, shrink=1, pad=0.01, location='bottom', ticks=ticks_p, ax=ax6)
        else:
            qpf = ds_area['pratesfc'][i, :, :] * 141.73236

            qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
    
            stn1.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

            cs1 = ax6.contourf(ds_area['lon'], ds_area['lat'], (ds_area['pratesfc'][i, :, :] * 141.73236), cmap=cmap_p, transform=datacrs, levels=levels_pr, alpha=0.35, extend='max')
            cbar1 = fig.colorbar(cs1, shrink=1, pad=0.01, location='bottom', ticks=ticks_pr, ax=ax6)      
    

        fig.text(0.5, 0.085, f"ENTIRE ATMOSPHERE PWAT: {round(float(pwat), 2)} [IN]\nMIXING HEIGHT: {int(round(float(mixing_height), 0))} [FT AGL]\nFREEZING LEVEL: {int(round(float(freezing_level), 0))} [FT AGL]\n2-METER TEMPERATURE: {int(round(float(t2m),0))} [°F] | 2-METER RH: {int(round(float(rh2m),0))} [%]", fontweight='bold', fontsize=10, bbox=props)

        fig.text(0.76, 0.085, "Plot Created With FireWxPy\n(C) Eric J. Drewitz "+utc_time.strftime('%Y')+"\nData Source: NOAA/NCEP/NOMADS\nImage Created: "+utc_time.strftime('%m/%d/%Y %H:00 UTC'), fontsize=8, bbox=props)
        
        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
        tim.sleep(10)

def plot_observed_sounding(station_id):

    r'''
        This function downloads the latest avaliable sounding data from the University of Wyoming and plots the upper-air profiles.
        
        Required Arguments:
        
        station_id (String) - The 3 or 4 letter station identifier for the upper-air site.
        Example: San Diego, CA will be entered as plot_observed_sounding('nkx')
        
        Optional Arguments: None
        
        Returns: Saves the upper-air profiles graphic to the Soundings folder.

    '''


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
        tim.sleep(10)
        print("Trying again!")
        try:
            df = WyomingUpperAir.request_data(dates[0], station_id)
            print("Successfully retrieved data for: "+dates[0].strftime('%m/%d %H:00 UTC'))
            date = dates[0]
            data = True
        except Exception as e:
            tim.sleep(10)
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
                    tim.sleep(10)
                    print("Trying again!")
                    try:
                        df = WyomingUpperAir.request_data(dates[1], station_id)
                        print("Successfully retrieved data for: "+dates[1].strftime('%m/%d %H:00 UTC'))
                        date = dates[1]
                        data = True
                    except Exception as e:
                        tim.sleep(10)
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
                                tim.sleep(10)
                                print("Trying again!")
                                try:
                                    df = WyomingUpperAir.request_data(dates[2], station_id)
                                    print("Successfully retrieved data for: "+dates[2].strftime('%m/%d %H:00 UTC'))
                                    date = dates[2]
                                    data = True
                                except Exception as e:
                                    tim.sleep(10)
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
            tim.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[3], station_id)
                print("Successfully retrieved data for: "+dates[3].strftime('%m/%d %H:00 UTC'))
                date = dates[3]
                data = True
            except Exception as e:
                tim.sleep(10)
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
                        tim.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[4], station_id)
                            print("Successfully retrieved data for: "+dates[4].strftime('%m/%d %H:00 UTC'))
                            date = dates[4]
                            data = True
                        except Exception as e:
                            tim.sleep(10)
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
            tim.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[5], station_id)
                print("Successfully retrieved data for: "+dates[5].strftime('%m/%d %H:00 UTC'))
                date = dates[5]
                data = True
            except Exception as e:
                tim.sleep(10)
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
                        tim.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[6], station_id)
                            print("Successfully retrieved data for: "+dates[6].strftime('%m/%d %H:00 UTC'))
                            date = dates[6]
                            data = True
                        except Exception as e:
                            tim.sleep(10)
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
                                    tim.sleep(10)
                                    print("Trying again!")
                                    try:
                                        df = WyomingUpperAir.request_data(dates[7], station_id)
                                        print("Successfully retrieved data for: "+dates[7].strftime('%m/%d %H:00 UTC'))
                                        date = dates[7]
                                        data = True
                                    except Exception as e:
                                        tim.sleep(10)
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
            tim.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[8], station_id)
                print("Successfully retrieved data for: "+dates[8].strftime('%m/%d %H:00 UTC'))
                date = dates[8]
                data = True
            except Exception as e:
                tim.sleep(10)
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
                        tim.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[9], station_id)
                            print("Successfully retrieved data for: "+dates[9].strftime('%m/%d %H:00 UTC'))
                            date = dates[9]
                            data = True
                        except Exception as e:
                            tim.sleep(10)
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
                                    tim.sleep(10)
                                    print("Trying again!")
                                    try:
                                        df = WyomingUpperAir.request_data(dates[10], station_id)
                                        print("Successfully retrieved data for: "+dates[10].strftime('%m/%d %H:00 UTC'))
                                        date = dates[10]
                                        data = True
                                    except Exception as e:
                                        tim.sleep(10)
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
            tim.sleep(10)
            print("Trying again!")
            try:
                df = WyomingUpperAir.request_data(dates[11], station_id)
                print("Successfully retrieved data for: "+dates[11].strftime('%m/%d %H:00 UTC'))
                date = dates[11]
            except Exception as e:
                tim.sleep(10)
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
                        tim.sleep(10)
                        print("Trying again!")
                        try:
                            df = WyomingUpperAir.request_data(dates[12], station_id)
                            print("Successfully retrieved data for: "+dates[12].strftime('%m/%d %H:00 UTC'))
                            date = dates[12]
                        except Exception as e:
                            tim.sleep(10)
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
        tim.sleep(10)
        try:
            print("Trying Again!")
            df_24 = WyomingUpperAir.request_data(date_24, station_id)
            print("Successfully retrieved data for: "+date_24.strftime('%m/%d %H:00 UTC'))
        except Exception as e:
            tim.sleep(10)
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
        
        ax1.tick_params(axis="y",direction="in", pad=-22)
        
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
        ax2.tick_params(axis="y",direction="in", pad=-20)

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
        x_24 = np.empty_like(ft_24)
        x_24.fill(xloc)
        
        ax2.barbs(x[idx], ft[idx], u[idx], v[idx], clip_on=True, zorder=10, color='darkred', label=label_date, length=5, alpha=0.5)
        
        try:
            ax2.barbs(x_24[idx_24], ft_24[idx_24], u_24[idx_24], v_24[idx_24], clip_on=True, zorder=10, color='darkblue', label=label_date_24, length=5, alpha=0.5)
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
        ax3.tick_params(axis="y",direction="in", pad=-27)
        ax3.axvline(x=0, color='gray', alpha=0.5, linestyle='--')
        ax3.set_ylim(ft[0], 15000)
        ax3.set_xlabel("BVF-Squared [1/s^2]", fontsize=9, fontweight='bold')
        ax3.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        ax3.set_yticks([2000, 4000, 6000, 8000, 10000, 12000, 14000])
        
        # Plots the Brunt–Väisälä Frequency Squared
        ax3.plot(bv_squared, ft, color='red', alpha=0.5, label=label_date)
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
        
        fig.text(0.16, 0.05, "Plot Created With FireWxPy(C) Eric J. Drewitz "+utc_time.strftime('%Y')+"\nData Source: weather.uwyo.edu\nImage Created: "+utc_time.strftime('%m/%d/%Y %H:00 UTC'), fontsize=8, bbox=props)

    if sounding == False:
        fig = standard.no_sounding_graphic(date)

    fname = station_id+" VERTICAL PROFILES"
    
    file_functions.save_daily_sounding_graphic(fig, station_id, None)  

def plot_observed_sounding_custom_date_time(station_id, year, month, day, hour):

    r'''
        This function downloads the latest avaliable sounding data from the University of Wyoming and plots the upper-air profiles.
        
        Required Arguments:
        
        station_id (String) - The 3 or 4 letter station identifier for the upper-air site. Example: San Diego, CA will be entered as plot_observed_sounding('nkx')
        
        year (Integer) - The four digit year (i.e. 2024)
        
        month (Integer) - The one or two digit month.
        
        day (Integer) - The nth day of the month.
        
        hour (Integer) - The hour of the sounding in UTC.
        
        Optional Arguments: None
        
        Returns: Saves the upper-air profiles graphic to the Soundings folder.
    '''

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
            tim.sleep(10)
            df = WyomingUpperAir.request_data(date, station_id)
            print(station_id+' '+date.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
            sounding = True
        except Exception as b:
            try:
                print("Trying one last time! - This server can be glitchy.")
                tim.sleep(10)
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
            tim.sleep(10)
            df_24 = WyomingUpperAir.request_data(date_24, station_id)
            print(station_id+' '+date_24.strftime('%m/%d/%Y %H:00 UTC')+' data retrieved successfully!')
        except Exception as b:
            try:
                print("Trying one last time! - This server can be glitchy.")
                tim.sleep(10)
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
        ax2.tick_params(axis="y",direction="in", pad=-20)

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
        x_24 = np.empty_like(ft_24)
        x_24.fill(xloc)
        
        ax2.barbs(x[idx], ft[idx], u[idx], v[idx], clip_on=True, zorder=10, color='darkred', label=label_date, length=5, alpha=0.5)
        
        try:
            ax2.barbs(x_24[idx_24], ft_24[idx_24], u_24[idx_24], v_24[idx_24], clip_on=True, zorder=10, color='darkblue', label=label_date_24, length=5, alpha=0.5)
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
        ax3.tick_params(axis="y",direction="in", pad=-28)
        ax3.axvline(x=0, color='gray', alpha=0.5, linestyle='--')
        ax3.set_ylim(ft[0], 15000)
        ax3.set_xlabel("BVF-Squared [1/s^2]", fontsize=9, fontweight='bold')
        ax3.set_ylabel("Height [ft AGL]", fontsize=9, fontweight='bold')
        ax3.set_yticks([2000, 4000, 6000, 8000, 10000, 12000, 14000])
        
        # Plots the Brunt–Väisälä Frequency Squared
        ax3.plot(bv_squared, ft, color='red', alpha=0.5, label=label_date)
        try:
            ax3.plot(bv_squared_24, ft_24, color='blue', alpha=0.5, label=label_date_24)
        except Exception as e:
            pass

        ax3.legend(loc=(0.57, 0.9), prop={'size': 5})

        ax4 = fig.add_subplot(gs[4:6, 1:4])

        ax4.tick_params(axis="y",direction="in", pad=-22)
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
        
        fig.text(0.16, 0.05, "Plot Created With FireWxPy(C) Eric J. Drewitz "+utc_time.strftime('%Y')+"\nData Source: weather.uwyo.edu\nImage Created: "+utc_time.strftime('%m/%d/%Y %H:00 UTC'), fontsize=8, bbox=props)

    if sounding == False:
        fig = standard.no_sounding_graphic(date)

    fname = station_id+" VERTICAL PROFILES"
    
    file_functions.save_daily_sounding_graphic(fig, station_id, date)  
