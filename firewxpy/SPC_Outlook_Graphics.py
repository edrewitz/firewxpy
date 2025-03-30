"""
This file hosts the functions to plot the latest SPC Outlooks. 


This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

"""
#### IMPORTS ####

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import firewxpy.settings as settings
import firewxpy.standard as standard
import firewxpy.dims as dims
import os
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings('ignore')

from metpy.plots import USCOUNTIES
from matplotlib.patheffects import withStroke
from firewxpy.calc import scaling, unit_conversion
from firewxpy.utilities import file_functions
from firewxpy.data_access import NDFD_GRIDS
from firewxpy.parsers import NDFD
from metpy.units import units
from dateutil import tz
from datetime import datetime, timedelta

mpl.rcParams['font.weight'] = 'bold'
props = dict(boxstyle='round', facecolor='wheat', alpha=1)

mpl.rcParams['ytick.labelsize'] = 6

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

mapcrs = ccrs.PlateCarree()
datacrs = ccrs.PlateCarree()

local_time, utc_time = standard.plot_creation_time()
timezone = standard.get_timezone_abbreviation()
tzone = standard.get_timezone()

def plot_critical_fire_weather_risk_outlook(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, signature_fontsize=6, stamp_fontsize=5):


    r'''
    This function plots the latest available NOAA/NWS SPC Critical Fire Weather Risk Outlook. 

    Required Arguments: None

    Optional Arguments: 

    1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Negative values denote the western hemisphere and positive 
       values denote the eastern hemisphere. 

    2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Negative values denote the western hemisphere and positive 
       values denote the eastern hemisphere. 

    3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Positive values denote the northern hemisphere and negative 
       values denote the southern hemisphere. 

    4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Positive values denote the northern hemisphere and negative 
       values denote the southern hemisphere.
    
    5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
       This is a feature of matplotlib, as per their definition, the shrink is:
       "Fraction by which to multiply the size of the colorbar." 
       This should only be changed if the user wishes to change the size of the colorbar. 
       Preset values are called from the settings module for each state and/or gacc_region.

    6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                           

    8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

    16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

    17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

    18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

    19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
        and passing the data in or if the function needs to download the data. A value of False means the data
        is downloaded inside of the function while a value of True means the user is downloading the data outside
        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
        things, it is recommended to set this value to True and download the data outside of the function and pass
        it in so that the amount of data requests on the host servers can be minimized. 

    27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
        This setting is only to be changed if the user wants to limit the amount of downloads from the 
        NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
        if the user wishes to download the data outside of this function. 

    28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
        This setting is only to be changed if the user wants to limit the amount of downloads from the 
        NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
        if the user wishes to download the data outside of this function. 

    29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
        Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
        changed to None. 

    30) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
        If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
        None and the gacc_region variable must be set to one of the acceptable abbreviations. 

        Here is a list of acceptable gacc_region abbreviations:

        South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
        
        North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
        
        Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
        
        Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
        
        Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
        
        Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
        
        Southern: 'SACC' or 'sacc' or 'SE' or 'se'
        
        Eastern: 'EACC' or 'eacc' or 'E' or 'e'
        
        Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
        
        Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

    31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.     

    37) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    38) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    Return: Saves individual images to f:Weather Data/SPC Outlooks/Critical Fire Weather Risk Outlook/{reference_system}. 
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = np.arange(4, 12, 2)  

    cmap = colormaps.SPC_Critical_Fire_Weather_Risk_Outlook_colormap()

    reference_system = reference_system


    if reference_system == 'Custom' or reference_system == 'custom':
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        show_psa_borders = show_psa_borders
        show_cwa_borders = show_cwa_borders
        show_nws_firewx_zones = show_nws_firewx_zones
        show_nws_public_zones = show_nws_public_zones

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
        if reference_system == 'States & Counties':
            show_state_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC Only':
            show_gacc_borders = True
        if reference_system == 'GACC & PSA':
            show_gacc_borders = True
            show_psa_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.25
        if reference_system == 'CWA Only':
            show_cwa_borders = True
        if reference_system == 'NWS CWAs & NWS Public Zones':
            show_cwa_borders = True
            show_nws_public_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_public_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
            show_cwa_borders = True
            show_nws_firewx_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_firewx_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & Counties':
            show_cwa_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_firewx_zones = True
            nws_firewx_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & NWS Public Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_public_zones = True
            nws_public_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & NWS CWA':
            show_gacc_borders = True
            show_psa_borders = True
            show_cwa_borders = True
            cwa_border_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & Counties':
            show_gacc_borders = True
            show_psa_borders = True
            show_county_borders = True
            county_border_linewidth=0.25
        if reference_system == 'GACC & Counties':
            show_gacc_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
                
    try:  
        western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        if state == 'AK' or state == 'ak':
           print(f"This product is only availiable for CONUS.\nSorry OCONUS folks...")
        if state != 'AK' and state != 'ak' or gacc_region != None:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

    except Exception as e:
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        x1=x1
        y1=y1
        x2=x2
        y2=y2
        x3=x3
        y3=y3
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

    path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Critical Fire Weather Risk Outlook', reference_system, None, spc=True)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
    if data == False:

        ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.critfireo.bin', state)

    else:
        ds_short = ds_short
        ds_extended = ds_extended

    short_stop = len(ds_short['step'])
    extended_stop = len(ds_extended['step'])
    extended_start = short_stop + 1

    short_times = ds_short['valid_time']
    extended_times = ds_extended['valid_time']
    short_times = short_times.to_pandas()
    extended_times = extended_times.to_pandas()

    short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 24)
    extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 24)

    init_hr = 12
    hour = short_start_times_utc[0].hour
    dt = False
    if hour == init_hr:
        start = 0
        skip = False
    else:
        if local_time.hour >= 18 and local_time.hour <= 2:
            start = 0
            skip = False
            dt = True
            hours = hour - init_hr
        else:
            start = 1
            skip = True

    if skip == True:
        extended_start = extended_start - 1
    else:
        extended_start = extended_start

    for i in range(start, short_stop, 1):

        fname = f"A_Short_Term_{i}.png"
        if skip == False:
            index = 1 + i
        else:
            index = i

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        start = short_start_times[i]
        end = short_end_times[i]             

        cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=[5, 7, 9])
        cbar.ax.set_yticklabels(['Elevated', 'Critical', 'Extreme'])

        plt.title(f"SPC Outlook [Day {index}]\nCritical Fire Weather Outlook", fontsize=8, fontweight='bold', loc='left')
        if dt == False:
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
        else:
            start_hour = short_start_times[0].hour - hours
            end_hour = short_end_times[0].hour - hours
            plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/SPC", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
    print(f"Saved short-term forecast graphics to {path_print}")


    for i in range(0, extended_stop, 1):

        fname = f"B_Extended_Term_{i}.png"

        index = extended_start + i

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        start = extended_start_times[i]
        end = extended_end_times[i]

        cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)

        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=[5, 7, 9])
        cbar.ax.set_yticklabels(['Elevated', 'Critical', 'Extreme'])

        plt.title(f"SPC Outlook [Day {index}]\nCritical Fire Weather Outlook", fontsize=8, fontweight='bold', loc='left')
        plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/SPC", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
    print(f"Saved extended forecast graphics to {path_print}")


def plot_dry_lightning_outlook(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds_short=None, ds_extended=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, signature_fontsize=6, stamp_fontsize=5):


    r'''
    This function plots the latest available NOAA/NWS SPC Dry Lightning Outlook. 

    Required Arguments: None

    Optional Arguments: 

    1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Negative values denote the western hemisphere and positive 
       values denote the eastern hemisphere. 

    2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Negative values denote the western hemisphere and positive 
       values denote the eastern hemisphere. 

    3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Positive values denote the northern hemisphere and negative 
       values denote the southern hemisphere. 

    4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Positive values denote the northern hemisphere and negative 
       values denote the southern hemisphere.
    
    5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
       This is a feature of matplotlib, as per their definition, the shrink is:
       "Fraction by which to multiply the size of the colorbar." 
       This should only be changed if the user wishes to change the size of the colorbar. 
       Preset values are called from the settings module for each state and/or gacc_region.

    6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                           

    8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

    16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

    17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

    18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

    19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
        and passing the data in or if the function needs to download the data. A value of False means the data
        is downloaded inside of the function while a value of True means the user is downloading the data outside
        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
        things, it is recommended to set this value to True and download the data outside of the function and pass
        it in so that the amount of data requests on the host servers can be minimized. 

    27) ds_short (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
        This setting is only to be changed if the user wants to limit the amount of downloads from the 
        NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
        if the user wishes to download the data outside of this function. 

    28) ds_extended (xarray.dataarray) - The xarray data array of the downloaded NWS Extended Forecast dataset from the NWS FTP Server. 
        This setting is only to be changed if the user wants to limit the amount of downloads from the 
        NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
        if the user wishes to download the data outside of this function. 

    29) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
        Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
        changed to None. 

    30) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
        If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
        None and the gacc_region variable must be set to one of the acceptable abbreviations. 

        Here is a list of acceptable gacc_region abbreviations:

        South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
        
        North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
        
        Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
        
        Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
        
        Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
        
        Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
        
        Southern: 'SACC' or 'sacc' or 'SE' or 'se'
        
        Eastern: 'EACC' or 'eacc' or 'E' or 'e'
        
        Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
        
        Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

    31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.     

    37) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    38) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    Return: Saves individual images to f:Weather Data/SPC Outlooks/Dry Lightning Outlook/{reference_system}. 
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = np.arange(4, 10, 2)

    cmap = colormaps.SPC_Dry_Lightning_Risk_Outlook_colormap()

    reference_system = reference_system


    if reference_system == 'Custom' or reference_system == 'custom':
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        show_psa_borders = show_psa_borders
        show_cwa_borders = show_cwa_borders
        show_nws_firewx_zones = show_nws_firewx_zones
        show_nws_public_zones = show_nws_public_zones

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
        if reference_system == 'States & Counties':
            show_state_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC Only':
            show_gacc_borders = True
        if reference_system == 'GACC & PSA':
            show_gacc_borders = True
            show_psa_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.25
        if reference_system == 'CWA Only':
            show_cwa_borders = True
        if reference_system == 'NWS CWAs & NWS Public Zones':
            show_cwa_borders = True
            show_nws_public_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_public_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
            show_cwa_borders = True
            show_nws_firewx_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_firewx_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & Counties':
            show_cwa_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_firewx_zones = True
            nws_firewx_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & NWS Public Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_public_zones = True
            nws_public_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & NWS CWA':
            show_gacc_borders = True
            show_psa_borders = True
            show_cwa_borders = True
            cwa_border_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & Counties':
            show_gacc_borders = True
            show_psa_borders = True
            show_county_borders = True
            county_border_linewidth=0.25
        if reference_system == 'GACC & Counties':
            show_gacc_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
                
    try:  
        western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        if state == 'AK' or state == 'ak':
           print(f"This product is only availiable for CONUS.\nSorry OCONUS folks...")
        if state != 'AK' and state != 'ak' or gacc_region != None:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

    except Exception as e:
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        x1=x1
        y1=y1
        x2=x2
        y2=y2
        x3=x3
        y3=y3
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

    path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Dry Lightning Outlook', reference_system, None, spc=True)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
    if data == False:

        ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.dryfireo.bin', state)

    else:
        ds_short = ds_short
        ds_extended = ds_extended

    short_stop = len(ds_short['step'])
    extended_stop = len(ds_extended['step'])
    extended_start = short_stop + 1

    short_times = ds_short['valid_time']
    extended_times = ds_extended['valid_time']
    short_times = short_times.to_pandas()
    extended_times = extended_times.to_pandas()

    short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 24)
    extended_start_times, extended_end_times, extended_start_times_utc = NDFD.get_valid_times_xarray(ds_extended, 24)

    init_hr = 12
    hour = short_start_times_utc[0].hour
    dt = False
    if hour == init_hr:
        start = 0
        skip = False
    else:
        if local_time.hour >= 18 and local_time.hour <= 2:
            start = 0
            skip = False
            dt = True
            hours = hour - init_hr
        else:
            start = 1
            skip = True

    if skip == True:
        extended_start = extended_start - 1
    else:
        extended_start = extended_start

    for i in range(start, short_stop, 1):

        fname = f"A_Short_Term_{i}.png"
        if skip == False:
            index = 1 + i
        else:
            index = i

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        start = short_start_times[i]
        end = short_end_times[i]             

        cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=[5, 7])
        cbar.ax.set_yticklabels(['Isolated', 'Scattered'])

        plt.title(f"SPC Outlooks [Day {index}]\nDry Lightning Outlook", fontsize=8, fontweight='bold', loc='left')
        if dt == False:
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
        else:
            start_hour = short_start_times[0].hour - hours
            end_hour = short_end_times[0].hour - hours
            plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 {timezone}')} - {end.strftime(f'%a %d/{end_hour}:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/SPC", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
    print(f"Saved short-term forecast graphics to {path_print}")


    for i in range(0, extended_stop, 1):

        fname = f"B_Extended_Term_{i}.png"

        index = extended_start + i

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        start = extended_start_times[i]
        end = extended_end_times[i]

        cs = ax.contourf(ds_extended['longitude'][:, :], ds_extended['latitude'][:, :], ds_extended['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)

        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=[5, 7])
        cbar.ax.set_yticklabels(['Isolated', 'Scattered'])

        plt.title(f"SPC Outlooks [Day {index}]\nDry Lightning Outlook", fontsize=8, fontweight='bold', loc='left')
        plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/SPC", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)   

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
    print(f"Saved extended forecast graphics to {path_print}")


def plot_convective_outlook(western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, shrink=0.7, show_rivers=True, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=1, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.5, nws_public_zones_linewidth=0.5, state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', data=False, ds=None, state='conus', gacc_region=None, x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, signature_fontsize=6, stamp_fontsize=5):


    r'''
    This function plots the latest available NOAA/NWS SPC Convective Outlook. 

    Required Arguments: None

    Optional Arguments: 

    1) western_bound (Integer or Float) - Default = None. Western extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Negative values denote the western hemisphere and positive 
       values denote the eastern hemisphere. 

    2) eastern_bound (Integer or Float) - Default = None. Eastern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Negative values denote the western hemisphere and positive 
       values denote the eastern hemisphere. 

    3) southern_bound (Integer or Float) - Default = None. Southern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Positive values denote the northern hemisphere and negative 
       values denote the southern hemisphere. 

    4) northern_bound (Integer or Float) - Default = None. Northern extent of the plot in decimal degrees. 
       The default setting is None. If set to None, the user must select a state or gacc_region. 
       This setting should be changed from None to an integer or float value if the user wishes to
       have a custom area selected. Positive values denote the northern hemisphere and negative 
       values denote the southern hemisphere.
    
    5) shrink (Integer or Float) - Default = 0.7. This is how the colorbar is sized to the figure. 
       This is a feature of matplotlib, as per their definition, the shrink is:
       "Fraction by which to multiply the size of the colorbar." 
       This should only be changed if the user wishes to change the size of the colorbar. 
       Preset values are called from the settings module for each state and/or gacc_region.

    6) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
        Default setting is True. Users should change this value to False if they wish to hide rivers.

    7) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                           

    8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide state borders. 

    9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
        Default setting is False. Users should change this value to False if they wish to hide county borders. 

    10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display GACC borders. 

    11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display PSA borders.

    12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display CWA borders.

    13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

    14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
        Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

    15) state_border_linewidth (Integer) - Linewidth (thickness) of the state borders. Default setting is 2. 

    16) county_border_linewidth (Integer) - Linewidth (thickness) of the county borders. Default setting is 1. 

    17) gacc_border_linewidth (Integer) - Linewidth (thickness) of the GACC borders. Default setting is 2. 

    18) psa_border_linewidth (Integer) - Linewidth (thickness) of the PSA borders. Default setting is 1. 

    19) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
        To change to a dashed line, users should set state_border_linestyle='--'. 

    20) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
        To change to a dashed line, users should set county_border_linestyle='--'. 

    21) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
        To change to a dashed line, users should set gacc_border_linestyle='--'. 

    22) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    23) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    24) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    25) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
        To change to a dashed line, users should set psa_border_linestyle='--'. 

    26) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
        and passing the data in or if the function needs to download the data. A value of False means the data
        is downloaded inside of the function while a value of True means the user is downloading the data outside
        of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
        things, it is recommended to set this value to True and download the data outside of the function and pass
        it in so that the amount of data requests on the host servers can be minimized. 

    27) ds (xarray.dataarray) - The xarray data array of the downloaded NWS Short-Term Forecast dataset from the NWS FTP Server. 
        This setting is only to be changed if the user wants to limit the amount of downloads from the 
        NWS FTP Server. Default setting is None. Please see the documentation for the data_access module 
        if the user wishes to download the data outside of this function. 

    28) state (String) - The two letter state abbreviation for the state the user wishes to make the graphic for. 
        If the user wishes to make a graphic for the entire CONUS, there are 2 acceptable abbreviations: 'CONUS' or 'conus'. 
        Example: If the user wishes to make a plot for the state of California both 'CA' or 'ca' are
        acceptable. Default setting is 'conus'. If the user wishes to make a plot based on gacc_region, this value must be 
        changed to None. 

    29) gacc_region (String) - The abbreviation for each of the 10 GACC regions. Default setting is None. 
        If the user wishes to make a plot based on GACC Region than state, the state variable must be set to 
        None and the gacc_region variable must be set to one of the acceptable abbreviations. 

        Here is a list of acceptable gacc_region abbreviations:

        South Ops: 'OSCC' or 'oscc' or 'SOPS' or 'sops'
        
        North Ops: 'ONCC' or 'oncc' or 'NOPS' or 'nops'
        
        Great Basin: 'GBCC' or 'gbcc' or 'GB' or 'gb'
        
        Northern Rockies: 'NRCC' or 'nrcc' or 'NR' or 'nr'
        
        Rocky Mountain: 'RMCC' or 'rmcc' or 'RM' or 'rm'
        
        Southwest: 'SWCC' or 'swcc' or 'SW' or 'sw'
        
        Southern: 'SACC' or 'sacc' or 'SE' or 'se'
        
        Eastern: 'EACC' or 'eacc' or 'E' or 'e'
        
        Pacific Northwest: 'PNW' or 'pnw' or 'NWCC' or 'nwcc' or 'NW' or 'nw'
        
        Alaska: Setting state='AK' or state='ak' suffices here. Leave gacc_region=None and set the state variable as shown. 

    30) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

    31) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

    32) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

    33) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

    34) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

    35) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.     

    36) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

    37) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

    Return: Saves individual images to f:Weather Data/SPC Outlooks/Convective Outlook/{reference_system}. 
    '''
    PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
    
    GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
    
    CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
    
    FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
    
    PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

    state = state

    if gacc_region != None:
        state = gacc_region
    else:
        state = state

    levels = [1, 2, 3, 4, 5, 6, 8]

    cmap = colormaps.spc_convective_outlook_colormap()

    reference_system = reference_system


    if reference_system == 'Custom' or reference_system == 'custom':
        show_state_borders = show_state_borders
        show_county_borders = show_county_borders
        show_gacc_borders = show_gacc_borders
        show_psa_borders = show_psa_borders
        show_cwa_borders = show_cwa_borders
        show_nws_firewx_zones = show_nws_firewx_zones
        show_nws_public_zones = show_nws_public_zones

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
        if reference_system == 'States & Counties':
            show_state_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC Only':
            show_gacc_borders = True
        if reference_system == 'GACC & PSA':
            show_gacc_borders = True
            show_psa_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.25
        if reference_system == 'CWA Only':
            show_cwa_borders = True
        if reference_system == 'NWS CWAs & NWS Public Zones':
            show_cwa_borders = True
            show_nws_public_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_public_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
            show_cwa_borders = True
            show_nws_firewx_zones = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                nws_firewx_zones_linewidth=0.25
        if reference_system == 'NWS CWAs & Counties':
            show_cwa_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
        if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_firewx_zones = True
            nws_firewx_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & NWS Public Zones':
            show_gacc_borders = True
            show_psa_borders = True
            show_nws_public_zones = True
            nws_public_zones_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & NWS CWA':
            show_gacc_borders = True
            show_psa_borders = True
            show_cwa_borders = True
            cwa_border_linewidth=0.25
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                psa_border_linewidth=0.5
        if reference_system == 'GACC & PSA & Counties':
            show_gacc_borders = True
            show_psa_borders = True
            show_county_borders = True
            county_border_linewidth=0.25
        if reference_system == 'GACC & Counties':
            show_gacc_borders = True
            show_county_borders = True
            if state == 'US' or state == 'us' or state == 'USA' or state == 'usa':
                county_border_linewidth=0.25
                
    try:  
        western_bound, eastern_bound, southern_bound, northern_bound, x1, y1, x2, y2, x3, y3, shrink, de, signature_fontsize, stamp_fontsize = settings.get_region_info('NAM', state)
        if state == 'AK' or state == 'ak':
           print(f"This product is only availiable for CONUS.\nSorry OCONUS folks...")
        if state != 'AK' and state != 'ak' or gacc_region != None:
            directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

        sp, x, y = settings.get_sp_dims_and_textbox_coords(state)

    except Exception as e:
        western_bound = western_bound
        eastern_bound = eastern_bound
        southern_bound = southern_bound
        northern_bound = northern_bound
        x1=x1
        y1=y1
        x2=x2
        y2=y2
        x3=x3
        y3=y3
        directory_name = '/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/'

    path, path_print = file_functions.noaa_graphics_paths(state, gacc_region, 'Convective Outlook', reference_system, None, spc=True)

    for file in os.listdir(f"{path}"):
        try:
            os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
    if data == False:

        ds_short, ds_extended = NDFD_GRIDS.get_ndfd_grids_xarray(directory_name, 'ds.conhazo.bin', state)

    else:
        ds_short = ds

    short_stop = len(ds_short['step'])

    short_times = ds_short['valid_time']
    short_times = short_times.to_pandas()

    short_start_times, short_end_times, short_start_times_utc = NDFD.get_valid_times_xarray(ds_short, 24)

    init_hr = 12
    hour = short_start_times_utc[0].hour
    dt = False
    if hour == init_hr:
        start = 0
        skip = False
    else:
        if local_time.hour >= 18 and local_time.hour <= 2:
            start = 0
            skip = False
            dt = True
            hours = hour - init_hr
        else:
            start = 1
            skip = True

    for i in range(start, short_stop, 1):

        fname = f"A_Short_Term_{i}.png"
        if skip == False:
            index = 1 + i
        else:
            index = i

        fig = plt.figure(figsize=(12,12))
        fig.set_facecolor('aliceblue')
        ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
        ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], datacrs)
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax.add_feature(provinces, linewidth=1, zorder=1)
        
        if show_rivers == True:
            ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass  

        start = short_start_times[i]
        end = short_end_times[i]             

        cs = ax.contourf(ds_short['longitude'][:, :], ds_short['latitude'][:, :], ds_short['unknown'][i, :, :], levels=levels, cmap=cmap, transform=datacrs, alpha=0.5)
        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=[2, 3, 4, 5, 6, 8])
        cbar.ax.set_yticklabels(['Thunderstorms', 'Marginal Risk', 'Slight Risk', 'Enhanced Risk', 'Moderate Risk', 'High Risk'])

        plt.title(f"SPC Outlooks [Day {index}]\nConvective Outlook", fontsize=8, fontweight='bold', loc='left')
        if dt == False:
            plt.title(f"Valid: {start.strftime(f'%a %d/%H:00 {timezone}')} - {end.strftime(f'%a %d/%H:00 {timezone}')}", fontsize=7, fontweight='bold', loc='right')
        else:
            start_hour = short_start_times[0].hour - hours
            end_hour = short_end_times[0].hour - hours
            plt.title(f"Valid: {start.strftime(f'%a %d/{start_hour}:00 UTC')} - {end.strftime(f'%a %d/{end_hour}:00 UTC')}", fontsize=7, fontweight='bold', loc='right')

        ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/SPC", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
        ax.text(x2, y2, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
        ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)  

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
    print(f"Saved forecast graphics to {path_print}")









